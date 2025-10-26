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
# CSS للألوان والخطوط المريحة
# ---------------------------
st.markdown("""
<style>
body {background-color: #FAFAFA; color: #1D3557; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
h1, h2, h3 {color: #1D3557;}
.stButton>button {background-color: #457B9D; color: white; border-radius: 8px; padding: 0.5em 1em;}
.stButton>button:hover {background-color: #1D3557; color: #F1FAEE;}
.stDataFrame th {background-color: #A8DADC; color: #1D3557;}
.stDataFrame td {background-color: #F1FAEE; color: #1D3557;}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.title("🧬 مشروع BIA601")
section = st.
