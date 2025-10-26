import streamlit as st
import pandas as pd
import os
import json
import subprocess
import sys

# ==========================
# Page Configuration
# ==========================
st.set_page_config(
    page_title="BIA601 - Genetic Algorithm Feature Selection",
    layout="wide"
)

OUTPUT_DIR = "outputs"

# ==========================
# Check required files
# ==========================
required_files = [
    "before_after.csv",
    "comparison.csv",
    "selected_features.json",
    "ga_evolution.png",
    "score_comparison.png",
    "features_count.png"
]

missing_files = [f for f in required_files if not os.path.exists(os.path.join(OUTPUT_DIR, f))]

if missing_files:
    with st.spinner("⚡ جاري توليد الملفات المطلوبة باستخدام ga_core.py... يرجى الانتظار"):
        try:
            subprocess.run([sys.executable, "ga_core.py"], check=True)
            st.success("✅ تم توليد جميع الملفات بنجاح!")
        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء تشغيل ga_core.py: {e}")

# ==========================
# Custom CSS for nice visuals
# ==========================
st.markdown("""
<style>
body {background-color: #F9F9F9; color: #222222; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
.dataframe th {background-color: #A8DADC; color: #1D3557; text-align: center;}
.dataframe td {background-color: #F1FAEE; color: #1D3557; text-align: center;}
h1, h2, h3, h4 {color: #1D3557;}
.stAlert>div>div>div>div {background-color: #C1F0C1 !important; color: #1B3B1B !important;}
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
# Results Before & After
# ==========================
elif section == "📊 النتائج قبل وبعد":
    st.markdown("## 1️⃣ نتائج قبل
