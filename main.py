import streamlit as st
import pandas as pd
import os
import json

# إعداد الصفحة
st.set_page_config(page_title="BIA601 - Genetic Algorithm Feature Selection", layout="wide")

# العنوان الرئيسي
st.title("🧬 مشروع BIA601 — اختيار الميزات باستخدام الخوارزمية الجينية")
st.markdown("""
### 👨‍🏫 إشراف: د. عصام سلمان  
**المادة:** BIA601 — Data Mining  
**الهدف:** عرض نتائج تطبيق الخوارزمية الجينية لاختيار الميزات المثلى ومقارنتها بالطرق التقليدية.
""")

OUTPUT_DIR = "outputs"

# ===============================================================
# 1️⃣ عرض النتائج قبل وبعد
# ===============================================================
st.header("1️⃣ نتائج قبل وبعد تطبيق الخوارزمية الجينية")

before_path = os.path.join(OUTPUT_DIR, "before_after.csv")
if os.path.exists(before_path):
    before_after = pd.read_csv(before_path)
    st.dataframe(before_after.style.format({"Score": "{:.4f}"}))
else:
    st.warning("ملف before_after.csv غير موجود. تأكد من تشغيل ga_core.py أولاً.")

# ===============================================================
# 2️⃣ مقارنة الطرق المختلفة
# ===============================================================
st.header("2️⃣ مقارنة الطرق المختلفة (Full vs GA vs SelectKBest vs RFE)")

comp_path = os.path.join(OUTPUT_DIR, "comparison.csv")
if os.path.exists(comp_path):
    comparison = pd.read_csv(comp_path)
    st.dataframe(comparison.style.format({"CV_Score": "{:.4f}"}))
else:
    st.warning("ملف comparison.csv غير موجود.")

# ===============================================================
# 3️⃣ الرسوم البيانية
# ===============================================================
st.header("3️⃣ الرسوم البيانية")

col1, col2, col3 = st.columns(3)
plots = {
    "ga_evolution.png": "تطور Fitness عبر الأجيال",
    "score_comparison.png": "مقارنة الدرجات بين الطرق",
    "features_count.png": "عدد الميزات في كل طريقة"
}

for (col, (img, caption)) in zip([col1, col2, col3], plots.items()):
    path = os.path.join(OUTPUT_DIR, img)
    with col:
        if os.path.exists(path):
            st.image(path, caption=caption, use_container_width=True)
        else:
            st.warning(f"الصورة {img} غير موجودة.")

# ===============================================================
# 4️⃣ الميزات المختارة بالخوارزمية الجينية
# ===============================================================
st.header("4️⃣ الميزات المختارة بالخوارزمية الجينية")

feat_path = os.path.join(OUTPUT_DIR, "selected_features.json")
if os.path.exists(feat_path):
    with open(feat_path, "r", encoding="utf-8") as f:
        features = json.load(f)
    st.success(f"✅ تم اختيار {len(features)} ميزة من أصل مجموعة الميزات الكاملة.")
    st.write(features)
else:
    st.warning("لم يتم العثور على ملف selected_features.json")

# ===============================================================
# 5️⃣ ملاحظات ختامية
# ===============================================================
st.markdown("---")
st.markdown("""
#### 📘 ملاحظات:
- تم تنفيذ الخوارزمية الجينية لاختيار الميزات المثلى باستخدام نموذج التصنيف (Decision Tree أو Logistic Regression).
- تم مقارنة النتائج مع خوارزميات تقليدية (RFE, SelectKBest).
- جميع الرسوم والجداول تم توليدها آليًا من كود `ga_core.py`.
""")

st.caption("© 2025 — مشروع مادة BIA601 | إعداد مجموعة طلاب المادة بإشراف د. عصام سلمان")
