import streamlit as st
import pandas as pd
import os
import json
import subprocess
import sys

OUTPUT_DIR = "outputs"

# ---------------------------
# إعدادات الصفحة
# ---------------------------
st.set_page_config(
    page_title="BIA601 - Genetic Algorithm Feature Selection",
    layout="wide"
)

# ---------------------------
# CSS لتصميم RTL وألوان مريحة للعين
# ---------------------------
st.markdown("""
<style>
/* RTL direction */
body, .block-container {direction: rtl; text-align: right;}

/* خلفية عامة */
body {background-color: #F7F9FB; color: #212529; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}

/* العناوين */
h1, h2, h3 {color: #0D3B66; text-align: right;}

/* النصوص العادية */
p, li {color: #1D3557; font-size: 16px; line-height: 1.6;}

/* أزرار */
.stButton>button {
    background-color: #1D3557;
    color: #F1FAEE;
    border-radius: 8px;
    padding: 0.6em 1.2em;
    font-weight: bold;
    transition: all 0.2s ease-in-out;
}
.stButton>button:hover {
    background-color: #457B9D;
    color: #F1FAEE;
}

/* جداول */
.stDataFrame th {background-color: #A8DADC; color: #1D3557; text-align: center;}
.stDataFrame td {background-color: #E6F0F3; color: #1D3557; text-align: center;}

/* expanders */
.stExpanderHeader {font-weight: bold; color: #0D3B66;}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# الشريط الجانبي
# ---------------------------
st.sidebar.title("🧬 مشروع BIA601")
section = st.sidebar.radio(
    "اختر القسم الذي تريد عرضه:",
    ("🏁 الصفحة الرئيسية", "📊 النتائج قبل وبعد", "⚖️ مقارنة الطرق", "📈 الرسوم البيانية", "✨ الميزات المختارة", "⚡ تشغيل الخوارزمية")
)

# ---------------------------
# الصفحة الرئيسية
# ---------------------------
if section == "🏁 الصفحة الرئيسية":
    st.markdown("""
    <div style="padding:20px; background-color:#E3F2FD; border-radius:12px;">
        <h1>🧬 مشروع BIA601 — اختيار الميزات باستخدام الخوارزمية الجينية</h1>
        <p>
        هذا التطبيق يعرض نتائج تطبيق <b>الخوارزمية الجينية لاختيار الميزات</b> مقارنة بالطرق التقليدية
        (RFE, SelectKBest, Full Feature Set).<br>
        استخدم القائمة الجانبية لاختيار القسم الذي تريد عرضه.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------
# تشغيل الخوارزمية
# ---------------------------
elif section == "⚡ تشغيل الخوارزمية":
    st.header("⚡ تشغيل الخوارزمية الجينية")
    with st.container():
        if st.button("تشغيل ga_core.py"):
            with st.spinner("⚡ جاري التنفيذ... يرجى الانتظار"):
                try:
                    result = subprocess.run(
                        [sys.executable, "ga_core.py"],
                        capture_output=True, text=True
                    )
                    if result.returncode == 0:
                        st.success("✅ انتهى التنفيذ بنجاح! جميع الملفات موجودة في 'outputs/'.")
                    else:
                        st.error("❌ حدث خطأ أثناء تنفيذ ga_core.py")
                        st.text_area("تفاصيل الخطأ:", result.stderr, height=200)
                except Exception as e:
                    st.error(f"❌ خطأ غير متوقع: {e}")

# ---------------------------
# النتائج قبل وبعد
# ---------------------------
elif section == "📊 النتائج قبل وبعد":
    st.header("1️⃣ نتائج قبل وبعد تطبيق الخوارزمية الجينية")
    path = os.path.join(OUTPUT_DIR, "before_after.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        with st.expander("عرض النتائج"):
            st.dataframe(df.style.format({"Score": "{:.4f}"}))
    else:
        st.warning("ملف before_after.csv غير موجود. شغّل الخوارزمية أولاً.")

# ---------------------------
# مقارنة الطرق
# ---------------------------
elif section == "⚖️ مقارنة الطرق":
    st.header("2️⃣ مقارنة الطرق المختلفة (Full vs GA vs SelectKBest vs RFE)")
    path = os.path.join(OUTPUT_DIR, "comparison.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        with st.expander("عرض مقارنة النتائج"):
            st.dataframe(df.style.format({"CV_Score": "{:.4f}"}))
    else:
        st.warning("ملف comparison.csv غير موجود. شغّل الخوارزمية أولاً.")

# ---------------------------
# الرسوم البيانية
# ---------------------------
elif section == "📈 الرسوم البيانية":
    st.header("3️⃣ الرسوم البيانية")
    plots_info = {
        "ga_evolution.png": "تطور Fitness عبر الأجيال",
        "score_comparison.png": "مقارنة الدرجات بين الطرق",
        "features_count.png": "عدد الميزات في كل طريقة"
    }
    selected_plots = st.multiselect(
        "اختر الرسوم البيانية التي تريد عرضها:",
        list(plots_info.keys()),
        default=list(plots_info.keys())
    )
    if selected_plots:
        for i in range(0, len(selected_plots), 3):
            cols = st.columns(3)
            for col, img_file in zip(cols, selected_plots[i:i+3]):
                img_path = os.path.join(OUTPUT_DIR, img_file)
                caption = plots_info[img_file]
                with col:
                    if os.path.exists(img_path):
                        st.image(img_path, caption=caption, use_container_width=True)
                    else:
                        st.warning(f"الصورة {img_file} غير موجود. شغّل الخوارزمية أولاً.")

# ---------------------------
# الميزات المختارة
# ---------------------------
elif section == "✨ الميزات المختارة":
    st.header("4️⃣ الميزات المختارة بالخوارزمية الجينية")
    path = os.path.join(OUTPUT_DIR, "selected_features.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            features = json.load(f)
        with st.expander(f"عرض الميزات المختارة ({len(features)} ميزة)"):
            st.write(features)
    else:
        st.warning("ملف selected_features.json غير موجود. شغّل الخوارزمية أولاً.")

# ---------------------------
# الملاحظات في الشريط الجانبي
# ---------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("""
#### 📘 ملاحظات:
- تم تنفيذ الخوارزمية الجينية لاختيار الميزات المثلى باستخدام نموذج التصنيف (Decision Tree أو Logistic Regression).
- تم مقارنة النتائج مع خوارزميات تقليدية (RFE, SelectKBest).
- جميع الرسوم والجداول تم توليدها آليًا من كود `ga_core.py`.

© 2025 — مشروع مادة BIA601 | إعداد مجموعة طلاب المادة بإشراف د. عصام سلمان
""")
