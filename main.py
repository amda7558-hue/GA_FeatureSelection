import streamlit as st
import pandas as pd
import os
import json

# ==========================
# Page Configuration
# ==========================
st.set_page_config(
    page_title="BIA601 - Genetic Algorithm Feature Selection",
    layout="wide"
)

# ==========================
# Sidebar
# ==========================
st.sidebar.title("🧬 مشروع BIA601")
st.sidebar.markdown("""
**المادة:** BIA601 — Data Mining  
**إشراف:** د. عصام سلمان  
**الهدف:** عرض نتائج تطبيق الخوارزمية الجينية لاختيار الميزات المثلى ومقارنتها بالطرق التقليدية.
""")

section = st.sidebar.radio(
    "اختر القسم الذي تريد عرضه:",
    ("🏁 الصفحة الرئيسية", "📊 النتائج قبل وبعد", "⚖️ مقارنة الطرق", "📈 الرسوم البيانية", "✨ الميزات المختارة")
)

# ==========================
# Output Directory
# ==========================
OUTPUT_DIR = "outputs"

# ==========================
# Home Section
# ==========================
if section == "🏁 الصفحة الرئيسية":
    st.title("🧬 مشروع BIA601 — اختيار الميزات باستخدام الخوارزمية الجينية")
    st.markdown("""
    هذا التطبيق يعرض نتائج تطبيق **الخوارزمية الجينية لاختيار الميزات** مقارنة بالطرق التقليدية (RFE, SelectKBest, Full Feature Set).  
    استخدم القائمة الجانبية لاختيار القسم الذي تريد عرضه.
    """)

# ==========================
# 1️⃣ Results Before & After GA
# ==========================
elif section == "📊 النتائج قبل وبعد":
    st.header("1️⃣ نتائج قبل وبعد تطبيق الخوارزمية الجينية")
    before_after_path = os.path.join(OUTPUT_DIR, "before_after.csv")
    if os.path.exists(before_after_path):
        df_before_after = pd.read_csv(before_after_path)
        st.dataframe(df_before_after.style.format({"Score": "{:.4f}"}))
    else:
        st.warning("ملف before_after.csv غير موجود. تأكد من تشغيل ga_core.py أولاً.")

# ==========================
# 2️⃣ Comparison Between Methods
# ==========================
elif section == "⚖️ مقارنة الطرق":
    st.header("2️⃣ مقارنة الطرق المختلفة (Full vs GA vs SelectKBest vs RFE)")
    comparison_path = os.path.join(OUTPUT_DIR, "comparison.csv")
    if os.path.exists(comparison_path):
        df_comparison = pd.read_csv(comparison_path)
        st.dataframe(df_comparison.style.format({"CV_Score": "{:.4f}"}))
    else:
        st.warning("ملف comparison.csv غير موجود.")

# ==========================
# 3️⃣ Graphs
# ==========================
elif section == "📈 الرسوم البيانية":
    st.header("3️⃣ الرسوم البيانية")
    
    plots_info = {
        "ga_evolution.png": "تطور Fitness عبر الأجيال",
        "score_comparison.png": "مقارنة الدرجات بين الطرق",
        "features_count.png": "عدد الميزات في كل طريقة"
    }

    selected_plots = st.multiselect(
        "اختر الرسوم البيانية التي تريد عرضها:",
        options=list(plots_info.keys()),
        default=list(plots_info.keys())
    )

    cols = st.columns(len(selected_plots))
    for col, img_file in zip(cols, selected_plots):
        img_path = os.path.join(OUTPUT_DIR, img_file)
        caption = plots_info[img_file]
        with col:
            if os.path.exists(img_path):
                st.image(img_path, caption=caption, use_container_width=True)
            else:
                st.warning(f"الصورة {img_file} غير موجودة.")

# ==========================
# 4️⃣ Selected Features by GA
# ==========================
elif section == "✨ الميزات المختارة":
    st.header("4️⃣ الميزات المختارة بالخوارزمية الجينية")
    features_path = os.path.join(OUTPUT_DIR, "selected_features.json")
    if os.path.exists(features_path):
        with open(features_path, "r", encoding="utf-8") as f:
            selected_features = json.load(f)
        st.success(f"✅ تم اختيار {len(selected_features)} ميزة من أصل مجموعة الميزات الكاملة.")
        st.write(selected_features)
    else:
        st.warning("لم يتم العثور على ملف selected_features.json")

# ==========================
# Footer Notes
# ==========================
st.sidebar.markdown("---")
st.sidebar.markdown("""
#### 📘 ملاحظات:
- تم تنفيذ الخوارزمية الجينية لاختيار الميزات المثلى باستخدام نموذج التصنيف (Decision Tree أو Logistic Regression).
- تم مقارنة النتائج مع خوارزميات تقليدية (RFE, SelectKBest).
- جميع الرسوم والجداول تم توليدها آليًا من كود `ga_core.py`.

© 2025 — مشروع مادة BIA601 | إعداد مجموعة طلاب المادة بإشراف د. عصام سلمان
""")
