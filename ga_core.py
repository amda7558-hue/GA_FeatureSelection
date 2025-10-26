import os, warnings, json, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from dataclasses import dataclass
from typing import Literal

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import RFE, SelectKBest, f_classif
from sklearn.metrics import make_scorer, f1_score

warnings.filterwarnings("ignore")
print("Libraries loaded successfully ✅")

# =================== CONFIGURATION ===================
CONFIG = {
    "DATA_PATH": "breast_cancer_wisconsin.csv",  # غيّر المسار حسب اسم ملفك
    "MODEL_NAME": "logreg",                      # أو "dt"
    "METRIC": "accuracy",                        # "accuracy" أو "f1"
    "CV_SPLITS": 5,
    "RANDOM_STATE": 42,
    "POP_SIZE": 30,
    "GENERATIONS": 20,
    "PC": 0.9,
    "PM": 0.02,
    "ELITISM": 2,
    "LAMBDA": 0.005,
    "MIN_FEATURES": 1,
    "EARLY_STOP": True,
    "PATIENCE": 8
}

def get_scorer(metric: str):
    m = metric.lower()
    if m in ("f1","f1_macro"):
        return make_scorer(f1_score, average="macro")
    return "accuracy"

SCORER = get_scorer(CONFIG["METRIC"])

# =================== DATA PREPARATION ===================
def prepare_X_y(df: pd.DataFrame):
    # اكتشاف العمود الهدف تلقائياً
    target_col = None
    for c in df.columns:
        if c.lower() in ["diagnosis","target","label","class"]:
            target_col = c
            break
    if target_col is None:
        target_col = df.columns[-1]

    y_raw = df[target_col]
    if y_raw.dtype == object:
        mapping = {"malignant":1, "benign":0, "m":1, "b":0, "yes":1, "no":0}
        y = y_raw.astype(str).str.strip().str.lower().map(lambda v: mapping.get(v, v))
        try:
            y = y.astype(int)
        except Exception:
            y = (y_raw.astype('category').cat.codes).astype(int)
    else:
        y = y_raw.astype(int)

    X = df.drop(columns=[target_col]).copy()
    drop_cols = []
    for col in X.columns:
        if not pd.api.types.is_numeric_dtype(X[col]):
            try:
                X[col] = pd.to_numeric(X[col], errors="coerce")
            except Exception:
                drop_cols.append(col)
    if drop_cols:
        X = X.drop(columns=drop_cols)
    X = X.fillna(X.median(numeric_only=True))
    return X, y, target_col

if not os.path.exists(CONFIG["DATA_PATH"]):
    raise FileNotFoundError(f"❌ ملف البيانات غير موجود: {CONFIG['DATA_PATH']}")

df = pd.read_csv(CONFIG["DATA_PATH"])
X, y, target_col = prepare_X_y(df)
print(f"✅ Data loaded: X={X.shape}, y={y.shape}, target='{target_col}'")

# =================== GA CLASSES & FUNCTIONS ===================
@dataclass
class GAConfig:
    pop_size: int
    generations: int
    pc: float
    pm: float
    elitism: int
    penalty_lambda: float
    model_name: Literal["logreg","dt"]
    scorer: object
    cv_splits: int
    random_state: int
    min_features: int
    early_stop: bool = True
    patience: int = 10

def make_model(name: str, seed: int = 42):
    if name == "logreg":
        return Pipeline([("scaler", StandardScaler()),
                         ("clf", LogisticRegression(max_iter=500, solver="liblinear", random_state=seed))])
    elif name == "dt":
        return DecisionTreeClassifier(random_state=seed)
    else:
        raise ValueError("Unknown model: "+name)

def fitness(mask: np.ndarray, X: np.ndarray, y: np.ndarray, cfg: GAConfig):
    if mask.sum() < cfg.min_features: return -np.inf
    cols = np.where(mask)[0]
    model = make_model(cfg.model_name, cfg.random_state)
    cv = StratifiedKFold(n_splits=cfg.cv_splits, shuffle=True, random_state=cfg.random_state)
    acc = cross_val_score(model, X[:, cols], y, cv=cv, scoring=cfg.scorer).mean()
    penalty = cfg.penalty_lambda * (len(cols)/X.shape[1])
    return float(acc - penalty)

def tournament(pop, fit, rng, k=3):
    idxs = rng.choice(len(pop), size=k, replace=False)
    return pop[idxs[np.argmax(fit[idxs])]].copy()

def crossover(p1, p2, rng, pc):
    if rng.rand() < pc:
        point = rng.randint(1, len(p1))
        return np.r_[p1[:point], p2[point:]], np.r_[p2[:point], p1[point:]]
    return p1.copy(), p2.copy()

def mutate(ind, rng, pm, min_features):
    mut = rng.rand(len(ind)) < pm
    ind[mut] = ~ind[mut]
    if ind.sum() < min_features:
        off = np.where(~ind)[0]
        if len(off) > 0:
            ind[rng.choice(off)] = True
    return ind

def run_ga(X_df: pd.DataFrame, y_ser: pd.Series, cfg: GAConfig):
    t0 = time.time()
    rng = np.random.RandomState(cfg.random_state)
    X_arr = X_df.values.astype(float)
    y_arr = y_ser.values.astype(int)
    n = X_arr.shape[1]

    pop = rng.rand(cfg.pop_size, n) < 0.5
    for i in range(cfg.pop_size):
        if pop[i].sum() < cfg.min_features:
            pop[i, rng.randint(0, n)] = True

    fit = np.array([fitness(ind, X_arr, y_arr, cfg) for ind in pop])
    best = pop[np.argmax(fit)].copy()
    best_fit = float(fit.max())
    history, no_improve = [], 0

    for g in range(cfg.generations):
        new = []
        elite = np.argsort(-fit)[:cfg.elitism]
        for i in elite:
            new.append(pop[i].copy())
        while len(new) < cfg.pop_size:
            p1 = tournament(pop, fit, rng)
            p2 = tournament(pop, fit, rng)
            c1, c2 = crossover(p1, p2, rng, cfg.pc)
            new += [mutate(c1, rng, cfg.pm, cfg.min_features),
                    mutate(c2, rng, cfg.pm, cfg.min_features)]
        pop = np.array(new[:cfg.pop_size])
        fit = np.array([fitness(ind, X_arr, y_arr, cfg) for ind in pop])
        gen_best, gen_mean = float(fit.max()), float(fit.mean())
        history.append({"gen": g, "best": gen_best, "mean": gen_mean})

        if gen_best > best_fit + 1e-12:
            best_fit = gen_best
            best = pop[np.argmax(fit)].copy()
            no_improve = 0
        else:
            no_improve += 1

        if cfg.early_stop and no_improve >= cfg.patience:
            print(f"[EarlyStop] no improvement for {cfg.patience} generations at gen={g}.")
            break

    print(f"GA finished in {time.time()-t0:.2f}s. Best fitness={best_fit:.4f}")
    return best, best_fit, pd.DataFrame(history)

cfg = GAConfig(
    pop_size=CONFIG["POP_SIZE"],
    generations=CONFIG["GENERATIONS"],
    pc=CONFIG["PC"],
    pm=CONFIG["PM"],
    elitism=CONFIG["ELITISM"],
    penalty_lambda=CONFIG["LAMBDA"],
    model_name=CONFIG["MODEL_NAME"],
    scorer=SCORER,
    cv_splits=CONFIG["CV_SPLITS"],
    random_state=CONFIG["RANDOM_STATE"],
    min_features=CONFIG["MIN_FEATURES"],
    early_stop=CONFIG["EARLY_STOP"],
    patience=CONFIG["PATIENCE"]
)

best_mask, best_fit, hist = run_ga(X, y, cfg)
selected_cols = X.columns[best_mask].tolist()
print(f"✅ Selected {len(selected_cols)} features out of {X.shape[1]}")

# =================== EVALUATION ===================
def cv_score(model, X, y, scorer, cv_splits=5, seed=42):
    cv = StratifiedKFold(n_splits=cv_splits, shuffle=True, random_state=seed)
    return cross_val_score(model, X, y, cv=cv, scoring=scorer).mean()

full_model = make_model(cfg.model_name, cfg.random_state)
score_full = cv_score(full_model, X.values, y.values, cfg.scorer, cfg.cv_splits, cfg.random_state)
score_selected = cv_score(full_model, X[selected_cols].values, y.values, cfg.scorer, cfg.cv_splits, cfg.random_state)

before_after = pd.DataFrame({
    "Setting": ["Full features", "GA-selected"],
    "Score": [score_full, score_selected],
    "Metric": [CONFIG["METRIC"], CONFIG["METRIC"]],
    "NumFeatures": [X.shape[1], len(selected_cols)]
})

k = max(1, len(selected_cols))
skb = SelectKBest(score_func=f_classif, k=k)
rfe = RFE(LogisticRegression(max_iter=500, solver="liblinear", random_state=cfg.random_state), n_features_to_select=k)

pipe_skb = Pipeline([("sel", skb), ("scaler", StandardScaler()),
                     ("clf", LogisticRegression(max_iter=500, solver="liblinear", random_state=cfg.random_state))])
pipe_rfe = Pipeline([("rfe", rfe), ("scaler", StandardScaler()),
                     ("clf", LogisticRegression(max_iter=500, solver="liblinear", random_state=cfg.random_state))])

score_skb = cv_score(pipe_skb, X.values, y.values, cfg.scorer, cfg.cv_splits, cfg.random_state)
score_rfe = cv_score(pipe_rfe, X.values, y.values, cfg.scorer, cfg.cv_splits, cfg.random_state)

comparison = pd.DataFrame({
    "Method": ["Full", "GA", f"SelectKBest(k={k})", f"RFE(k={k})"],
    "CV_Score": [score_full, score_selected, score_skb, score_rfe],
    "Metric": [CONFIG["METRIC"]]*4,
    "NumFeatures": [X.shape[1], len(selected_cols), k, k]
}).sort_values("CV_Score", ascending=False).reset_index(drop=True)

mask_df = pd.DataFrame({"feature": X.columns, "selected": [bool(m) for m in best_mask]})

# =================== SAVE OUTPUTS ===================
os.makedirs("outputs", exist_ok=True)
before_after.to_csv("outputs/before_after.csv", index=False)
comparison.to_csv("outputs/comparison.csv", index=False)
mask_df.to_csv("outputs/feature_mask.csv", index=False)
with open("outputs/selected_features.json", "w", encoding="utf-8") as f:
    json.dump(selected_cols, f, ensure_ascii=False, indent=2)

plt.figure(figsize=(6,4))
plt.plot(hist["gen"], hist["best"], label="Best")
plt.plot(hist["gen"], hist["mean"], label="Mean")
plt.xlabel("Generation"); plt.ylabel("Fitness"); plt.title("GA Evolution")
plt.legend(); plt.tight_layout()
plt.savefig("outputs/ga_evolution.png", dpi=160); plt.close()

plt.figure(figsize=(6,4))
plt.bar(comparison["Method"], comparison["CV_Score"])
plt.title(f"Score comparison ({CONFIG['METRIC']})"); plt.ylabel(f"CV {CONFIG['METRIC']}")
plt.tight_layout()
plt.savefig("outputs/score_comparison.png", dpi=160); plt.close()

plt.figure(figsize=(6,4))
plt.bar(comparison["Method"], comparison["NumFeatures"])
plt.title("Number of features"); plt.ylabel("#Features")
plt.tight_layout()
plt.savefig("outputs/features_count.png", dpi=160); plt.close()

print("✅ All outputs saved successfully in 'outputs/' folder.")
print("Done.")
