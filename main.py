import streamlit as st
import subprocess
import sys
import os

OUTPUT_DIR = "outputs"

# -------------------------------
# زر لتشغيل الخوارزمية الجينية
# -------------------------------
st.markdown("### ⚡ تشغيل الخوارزمية الجينية")
if st.button("تشغيل الخوارزمية الجينية (ga_core.py)"):
    with st.spinner("⚡ جاري التنفيذ... يرجى الانتظار"):
        try:
            subprocess.run([sys.executable, "ga_core.py"], check=True)
            st.success("✅ انتهى التنفيذ، يمكنك الآن استعراض النتائج.")
        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء تشغيل ga_core.py: {e}")

# -------------------------------
# باقي الكود بعد ذلك
# -------------------------------
section = st.sidebar.radio(
    "اختر القسم الذي تريد عرضه:",
    ("🏁 الصفحة الرئيسية", "📊 النتائج قبل وبعد", "⚖️ مقارنة الطرق", "📈 الرسوم البيانية", "✨ الميزات المختارة")
)

# مثال: قبل وبعد قسم النتائج
if section == "📊 النتائج قبل وبعد":
    before_after_path = os.path.join(OUTPUT_DIR, "before_after.csv")
    if os.path.exists(before_after_path):
        import pandas as pd
        df_before_after = pd.read_csv(before_after_path)
        st.dataframe(df_before_after)
    else:
        st.warning("ملف before_after.csv غير موجود. شغّل الخوارزمية أولاً.")
