import streamlit as st
import pandas as pd
import os
import json

# ==========================
# Page Configuration
# ==========================
st.set_page_config(
    page_title="BIA601 - Genetic Algorithm Feature Selection",
    layout="wide",
)

# ==========================
# Custom CSS for better visuals
# ==========================
st.markdown("""
<style>
/* General font and background */
body {
    background-color: #F9F9F9;
    color: #222222;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Sidebar styling */
.css-1d391kg {  /* This class may change with Streamlit updates */
    background-color: #E8F0F2;
    padding: 1rem;
}

/* Table styling */
.dataframe th {
    background-color: #A8DADC;
    color: #1D3557;
    text-align: center;
}

.dataframe td {
    background-color: #F1FAEE;
    color: #1D3557;
    text-align: center;
}

/* Headings */
h1, h2, h3, h4 {
    color: #1D3557;
}

/* Success messages */
.stAlert>div>div>div>div {
    background-color: #C1F0C1 !important;
    color: #1B3B1B !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# Sidebar
# ==========================
st.sidebar.markdown("""
<div style="text-align:center; background-color:#A8DADC; padding:10px; border-radius:10px;">
<h2>🧬 مشروع BIA601</h2>
<p style="color:#1D3557;">المادة: BIA601 — Data Mining<br>
إشراف: د. عصام سلمان</p>
</div>
""", unsafe_allow_html=True)

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
    st.markdown("""
    <div style="padding:20px; background-color:#F1FAEE; border-radius:10px;">
    <h1>🧬 مشروع BIA601 — اختيار الميزات باستخدام الخوارزمية الجينية</h1>
    <p style="font-size:18px; color:#1D3557;">
    هذا التطبيق يعرض نتائج تطبيق <b>الخوارزمية الجينية لاختيار الميزات</b> مقارنة بالطرق التقليدية 
    (RFE, SelectKBest, Full Feature Set).<br>
    استخدم القائمة الجانبية لاختيار القسم الذي تريد عرضه.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================
# 1️⃣ Results Before & After GA
# ==========================
elif section == "📊 النتائج قبل وبعد":
    st.markdown("## 1️⃣ نتائج قبل وبعد تطبيق الخوارزمية الجينية", unsafe_allow_html=True)
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
    st.markdown("## 2️⃣ مقارنة الطرق المختلفة (Full vs GA vs SelectKBest vs RFE)", unsafe_allow_html=True)
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
    st.markdown("## 3️⃣ الرسوم البيانية", unsafe_allow_html=True)
    
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
                st.warning(f"الصورة {img_file} غير موجود.")

# ==========================
# 4️⃣ Selected Features by GA
# ==========================
elif section == "✨ الميزات المختارة":
    st.markdown("## 4️⃣ الميزات المختارة بالخوارزمية الجينية", unsafe_allow_html=True)
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
<div style="padding:10px; background-color:#F1FAEE; border-radius:10px; color:#1D3557;">
<h4>📘 ملاحظات:</h4>
<ul>
<li>تم تنفيذ الخوارزمية الجينية لاختيار الميزات المثلى باستخدام نموذج التصنيف (Decision Tree أو Logistic Regression).</li>
<li>تم مقارنة النتائج مع خوارزميات تقليدية (RFE, SelectKBest).</li>
<li>جميع الرسوم والجداول تم توليدها آليًا من كود <b>ga_core.py</b>.</li>
</ul>
<p>© 2025 — مشروع مادة BIA601 | إعداد مجموعة طلاب المادة بإشراف د. عصام سلمان</p>
</div>
""", unsafe_allow_html=True)
