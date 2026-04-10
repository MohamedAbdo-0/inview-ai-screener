import streamlit as st

st.set_page_config(page_title="MenaJobs AI Screener", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
        .block-container { direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, sans-serif; }
        .hero { background: linear-gradient(135deg, #0984e3, #74b9ff); color: white; padding: 40px; border-radius: 15px; margin-bottom: 30px; text-align: center; }
        h1 { font-weight: 800; font-size: 3rem; margin-bottom: 10px; }
        .card { padding: 30px; border-radius: 10px; border: 1px solid #ddd; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; transition: 0.3s; }
        .card:hover { transform: translateY(-5px); box-shadow: 0 8px 15px rgba(0,0,0,0.15); }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>MenaJobs AI Screener</h1>
    <p style="font-size: 1.2rem; opacity: 0.9;">النظام الشامل والذكي لمقابلات التوظيف بالفيديو باستخدام الذكاء الاصطناعي</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🏢 اختيار بوابة الدخول:")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h3 style="color: #0984e3;">👨‍💼 بوابة الشركة (HR Portal)</h3>
        <ul>
            <li>إدخال الأسئلة المطلوبة للمقابلة.</li>
            <li>إرسال دعوة المقابلة للمرشح.</li>
            <li>استعراض نتيجة المقابلة والتقرير الاستشاري فور الانتهاء.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("⬅️ الدخول لبوابة الشركة (HR)", use_container_width=True):
        st.switch_page("pages/1_hr_portal.py")

with col2:
    st.markdown("""
    <div class="card">
        <h3 style="color: #d63031;">👤 بوابة المرشح (Candidate Portal)</h3>
        <ul>
            <li>غرفة فيديو تفاعلية.</li>
            <li>محادثة آلية وتسجيل مستمر.</li>
            <li>نقل آمن للبيانات إلى الشركة.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("⬅️ الدخول كمرشح لإجراء المقابلة 🎥", use_container_width=True):
        st.switch_page("pages/2_candidate_portal.py")