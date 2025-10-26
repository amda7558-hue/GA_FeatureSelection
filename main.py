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
    layout="wide",
    page_icon="🧬"
)

# ---------------------------
# CSS عصري ومحسن
# ---------------------------
st.markdown("""
<style>
/* RTL وتصميم عام */
body, .block-container {
    direction: rtl;
    text-align: right;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* خلفية متدرجة أنيقة */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* الحاوية الرئيسية */
.main .block-container {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 2rem;
    margin-top: 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* العناوين */
h1 {
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-weight: 800;
    margin-bottom: 2rem;
    font-size: 2.5rem;
}

h2 {
    color: #2C3E50;
    border-right: 4px solid #E76F51;
    padding-right: 15px;
    margin: 2rem 0 1rem 0;
}

h3 {
    color: #34495E;
    border-bottom: 2px solid #F4A261;
    padding-bottom: 10px;
}

/* الأزرار المحسنة */
.stButton>button {
    background: linear-gradient(45deg, #E76F51, #F4A261);
    color: white;
    border: none;
    border-radius: 15px;
    padding: 12px 24px;
    font-weight: bold;
    font-size: 16px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(231, 111, 81, 0.3);
    width: 100%;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(231, 111, 81, 0.4);
    background: linear-gradient(45deg, #FF8C61, #F4A261);
}

/* الشريط الجانبي */
.css-1d391kg, .css-1lcbmhc {
    background: linear-gradient(180deg, #2C3E50 0%, #34495E 100%);
}

.sidebar .sidebar-content {
    background: linear-gradient(180deg, #2C3E50 0%, #34495E 100%);
}

/* Radio buttons محسنة */
.stRadio > div {
    background: rgba(255, 255, 255, 0.1);
    padding: 15px;
    border-radius: 15px;
    margin: 10px 0;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.stRadio label {
    color: white !important;
    font-weight: 500;
    padding: 8px;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.stRadio label:hover {
    background: rgba(255, 255, 255, 0.1);
}

/* الجداول */
.stDataFrame {
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.stDataFrame th {
    background: linear-gradient(45deg, #3498DB, #2980B9);
    color: white;
    font-weight: bold;
    padding: 12px;
    text-align: center;
}

.stDataFrame td {
    background: rgba(236, 240, 241, 0.8);
    padding: 10px;
    text-align: center;
    border-bottom: 1px solid #BDC3C7;
}

/* Expanders */
.streamlit-expanderHeader {
    background: linear-gradient(45deg, #34495E, #2C3E50);
    color: white !important;
    border-radius: 10px;
    padding: 15px;
    font-weight: bold;
    margin: 10px 0;
}

.streamlit-expanderContent {
    background: rgba(236, 240, 241, 0.5);
    border-radius: 0 0 10px 10px;
    padding: 20px;
}

/* Multiselect */
.stMultiSelect > div > div {
    border-radius: 10px;
    border: 2px solid #3498DB;
}

/* الرسائل */
.stSuccess {
    background: linear-gradient(45deg, #27AE60, #2ECC71);
    color: white;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

.stWarning {
    background: linear-gradient(45deg, #E67E22, #F39C12);
    color: white;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

.stError {
    background: linear-gradient(45deg, #E74C3C, #C0392B);
    color: white;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

/* Spinner */
.stSpinner > div {
    border-color: #E76F51 transparent transparent transparent;
}

/* الكروت */
.card {
    background: rgba(255, 255, 255, 0.9);
    padding: 20px;
    border-radius: 15px;
    margin: 15px 0;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    border-left: 5px solid #E76F51;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# الشريط الجانبي المحسن
# ---------------------------
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:20px 0;'>
        <h1 style='color:white; margin:0; font-size:1.8rem;'>🧬 BIA601</h1>
        <p style='color:#BDC3C7; margin:0;'>الخوارزمية الجينية لاختيار الميزات</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    section = st.radio(
        "🚪 اختر القسم:",
        [
            "🏠 الصفحة الرئيسية", 
            "📊 النتائج قبل وبعد", 
            "⚖️ مقارنة الطرق",
            "📈 الرسوم البيانية", 
            "✨ الميزات المختارة", 
            "⚡ تشغيل الخوارزمية"
        ]
    )
    
    st.markdown("---")
    
    st.markdown("""
    <div style='background:rgba(255,255,255,0.1); padding:15px; border-radius:10px;'>
        <h4 style='color:white; margin:0 0 10px 0;'>📘 ملاحظات:</h4>
        <p style='color:#BDC3C7; font-size:14px; margin:5px 0;'>
        • الخوارزمية الجينية لاختيار الميزات المثلى
        </p>
        <p style='color:#BDC3C7; font-size:14px; margin:5px 0;'>
        • مقارنة مع RFE و SelectKBest
        </p>
        <p style='color:#BDC3C7; font-size:14px; margin:5px 0;'>
        • جميع النتائج مُولدة آلياً
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------
# الصفحة الرئيسية المحسنة
# ---------------------------
if section == "🏠 الصفحة الرئيسية":
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align:center; padding:40px 20px;'>
            <h1>🧬 مشروع BIA601</h1>
            <h3 style='color:#7F8C8D;'>اختيار الميزات باستخدام الخوارزمية الجينية</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # كروت المعلومات
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='card'>
            <h3>🎯 الدقة</h3>
            <p>تحسين أداء النماذج من خلال اختيار الميزات الأكثر تأثيراً</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='card'>
            <h3>⚡ الكفاءة</h3>
            <p>تقليل زمن التدريب والحوسبة باستخدام ميزات أقل</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='card'>
            <h3>🔄 المقارنة</h3>
            <p>مقارنة مع الطرق التقليدية مثل RFE و SelectKBest</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='card'>
            <h3>📈 التصور</h3>
            <p>عرض النتائج برسوم بيانية وجداول تفاعلية</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------
# تشغيل الخوارزمية - محسن
# ---------------------------
elif section == "⚡ تشغيل الخوارزمية":
    st.header("⚡ تشغيل الخوارزمية الجينية")
    
    st.markdown("""
    <div class='card'>
        <h3>🚀 معلومات التشغيل</h3>
        <p>سيتم تشغيل الخوارزمية الجينية لاختيار أفضل مجموعة من الميزات بناءً على أداء النموذج.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🎯 تشغيل الخوارزمية الجينية", key="run_ga"):
            with st.spinner("🔄 جاري تنفيذ الخوارزمية... قد يستغرق هذا بضع دقائق"):
                try:
                    result = subprocess.run(
                        [sys.executable, "ga_core.py"],
                        capture_output=True, text=True
                    )
                    if result.returncode == 0:
                        st.success("""
                        ✅ **تم التنفيذ بنجاح!**
                        
                        تم إنشاء جميع الملفات والنتائج في مجلد 'outputs/'
                        """)
                    else:
                        st.error("❌ حدث خطأ أثناء التنفيذ")
                        with st.expander("📋 تفاصيل الخطأ"):
                            st.code(result.stderr)
                except Exception as e:
                    st.error(f"❌ خطأ غير متوقع: {e}")

# ---------------------------
# النتائج قبل وبعد - محسن
# ---------------------------
elif section == "📊 النتائج قبل وبعد":
    st.header("📊 النتائج قبل وبعد تطبيق الخوارزمية الجينية")
    
    path = os.path.join(OUTPUT_DIR, "before_after.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        
        # عرض إحصاءات سريعة
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📈 التحسن في الدقة", 
                     f"{((df.iloc[1,1] - df.iloc[0,1])/df.iloc[0,1]*100):.1f}%")
        
        with col2:
            st.metric("🔽 انخفاض الميزات", 
                     f"{df.iloc[0,2] - df.iloc[1,2]} ميزة")
        
        with col3:
            st.metric("🎯 أفضل دقة", f"{df.iloc[1,1]:.4f}")
        
        with col4:
            st.metric("📊 الدقة الأصلية", f"{df.iloc[0,1]:.4f}")
        
        with st.expander("📋 عرض الجدول الكامل", expanded=True):
            st.dataframe(
                df.style.format({"Score": "{:.4f}"})
                .set_properties(**{'background-color': '#F8F9F9', 'color': '#2C3E50'})
            )
    else:
        st.warning("""
        ⚠️ ملف النتائج غير موجود
        يرجى تشغيل الخوارزمية أولاً من قسم '⚡ تشغيل الخوارزمية'
        """)

# ---------------------------
# مقارنة الطرق - محسن
# ---------------------------
elif section == "⚖️ مقارنة الطرق":
    st.header("⚖️ مقارنة أداء الطرق المختلفة")
    
    path = os.path.join(OUTPUT_DIR, "comparison.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        
        # إيجاد أفضل طريقة
        best_method = df.loc[df['CV_Score'].idxmax()]
        
        st.markdown(f"""
        <div class='card' style='border-left:5px solid #27AE60;'>
            <h3>🏆 أفضل أداء: {best_method['Method']}</h3>
            <p style='font-size:18px; margin:0;'>الدقة: <strong>{best_method['CV_Score']:.4f}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📊 جدول المقارنة الكامل", expanded=True):
            # تلوين الصفوف
            def highlight_max(s):
                is_max = s == s.max()
                return ['background: linear-gradient(45deg, #27AE60, #2ECC71); color: white' if v else '' for v in is_max]
            
            styled_df = df.style.format({"CV_Score": "{:.4f}"})\
                .apply(highlight_max, subset=['CV_Score'])\
                .set_properties(**{'text-align': 'center'})
            
            st.dataframe(styled_df)
            
    else:
        st.warning("""
        ⚠️ ملف المقارنة غير موجود
        يرجى تشغيل الخوارزمية أولاً من قسم '⚡ تشغيل الخوارزمية'
        """)

# ---------------------------
# الرسوم البيانية - محسن
# ---------------------------
elif section == "📈 الرسوم البيانية":
    st.header("📈 التصورات البيانية للنتائج")
    
    plots_info = {
        "ga_evolution.png": "📊 تطور Fitness عبر الأجيال",
        "score_comparison.png": "⚖️ مقارنة الدرجات بين الطرق", 
        "features_count.png": "📊 عدد الميزات في كل طريقة"
    }
    
    available_plots = [plot for plot in plots_info.keys() if os.path.exists(os.path.join(OUTPUT_DIR, plot))]
    
    if available_plots:
        selected_plots = st.multiselect(
            "🎨 اختر الرسوم البيانية:",
            list(plots_info.keys()),
            default=list(plots_info.keys())[:2],
            format_func=lambda x: plots_info[x]
        )
        
        if selected_plots:
            # ترتيب الصور في شبكة متجاوبة
            cols_per_row = 2
            for i in range(0, len(selected_plots), cols_per_row):
                cols = st.columns(cols_per_row)
                for col, img_file in zip(cols, selected_plots[i:i+cols_per_row]):
                    img_path = os.path.join(OUTPUT_DIR, img_file)
                    caption = plots_info[img_file]
                    with col:
                        if os.path.exists(img_path):
                            st.image(img_path, 
                                   caption=caption, 
                                   use_container_width=True)
                        else:
                            st.warning(f"⚠️ {img_file} غير موجود")
    else:
        st.warning("""
        ⚠️ لا توجد رسوم بيانية متاحة
        يرجى تشغيل الخوارزمية أولاً من قسم '⚡ تشغيل الخوارزمية'
        """)

# ---------------------------
# الميزات المختارة - محسن  
# ---------------------------
elif section == "✨ الميزات المختارة":
    st.header("✨ الميزات المختارة بالخوارزمية الجينية")
    
    path = os.path.join(OUTPUT_DIR, "selected_features.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            features = json.load(f)
        
        st.markdown(f"""
        <div class='card'>
            <h3>🎯 ملخص الميزات المختارة</h3>
            <p style='font-size:18px;'>تم اختيار <strong>{len(features)}</strong> ميزة من أصل جميع الميزات المتاحة</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📋 عرض قائمة الميزات المختارة", expanded=True):
            # عرض الميزات في كروت
            cols = st.columns(3)
            for idx, feature in enumerate(features):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div style='
                        background: linear-gradient(45deg, #3498DB, #2980B9);
                        color: white;
                        padding: 15px;
                        border-radius: 10px;
                        margin: 5px 0;
                        text-align: center;
                        font-weight: bold;
                    '>
                        {feature}
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.warning("""
        ⚠️ ملف الميزات غير موجود
        يرجى تشغيل الخوارزمية أولاً من قسم '⚡ تشغيل الخوارزمية'
        """)

# ---------------------------
# التذييل
# ---------------------------
st.markdown("""
<div style='text-align:center; margin-top:50px; padding:20px; background:rgba(52, 73, 94, 0.1); border-radius:10px;'>
    <p style='color:#7F8C8D; margin:0;'>
    © 2025 — مشروع مادة BIA601 | إعداد مجموعة طلاب المادة بإشراف د. عصام سلمان
    </p>
</div>
""", unsafe_allow_html=True)
