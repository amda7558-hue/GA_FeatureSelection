import streamlit as st
import pandas as pd
import os
import json
import subprocess
import sys

OUTPUT_DIR = "outputs"

# ==========================
# زر لتشغيل الخوارزمية الجينية مع التقاط الأخطاء
# ==========================
st.markdown("### ⚡ تشغيل الخوارزمية الجينية")
if st.button("تشغيل ga_core.py"):
    with st.spinner("⚡ جاري التنفيذ..."):
        try:
            # تشغيل نفس نسخة Python الحالية والتقاط stderr
            result = subprocess.run(
                [sys.executable, "ga_core.py"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                st.success("✅ انتهى التنفيذ بنجاح!")
            else:
                st.error("❌ حدث خطأ أثناء تنفيذ ga_core.py")
                st.text_area("تفاصيل الخطأ:", result.stderr, height=200)
        except Exception as e:
            st.error(f"❌ خطأ غير متوقع: {e}")

# ==========================
# Sidebar لاختيار القسم
# ==========================
st.sidebar.title("🧬 مشروع BIA601")
section = st.sidebar.radio(
    "اختر القسم الذي تريد عرضه:",
    ("🏁 الصفحة الرئيسية", "📊 النتائج قبل وبعد", "⚖️ مقارنة الطرق", "📈 الرسوم البيانية", "✨ الميزات المختارة")
)

# ==========================
# الصفحة الرئيسية
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
# النتائج قبل وبعد
# ==========================
elif section == "📊 النتائج قبل وبعد":
    st.header("1️⃣ نتائج قبل وبعد تطبيق الخوارزمية الجينية")
    path = os.path.join(OUTPUT_DIR, "before_after.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        st.dataframe(df.style.format({"Score": "{:.4f}"}))
    else:
        st.warning("ملف before_after.csv غير موجود. شغّل الخوارزمية أولاً.")

# ==========================
# مقارنة الطرق
# ==========================
elif section == "⚖️ مقارنة الطرق":
    st.header("2️⃣ مقارنة الطرق المختلفة (Full vs GA vs SelectKBest vs RFE)")
