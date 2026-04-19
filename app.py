# Inview AI Screener
import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
try:
    from i18n import t, get_base_css, select_language
except ImportError:
    st.error("i18n file missing.")

st.set_page_config(page_title="Inview AI Screener", page_icon="🚀", layout="wide")

select_language()

st.markdown(get_base_css(), unsafe_allow_html=True)
st.markdown("""
    <style>
        .hero { background: linear-gradient(135deg, #0984e3, #74b9ff); color: white; padding: 40px; border-radius: 15px; margin-bottom: 30px; text-align: center; }
        h1 { font-weight: 800; font-size: 3rem; margin-bottom: 10px; }
        .card { padding: 30px; border-radius: 10px; border: 1px solid #ddd; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; transition: 0.3s; }
        .card:hover { transform: translateY(-5px); box-shadow: 0 8px 15px rgba(0,0,0,0.15); }
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="hero">
    <h1>{t('page_title_app')}</h1>
    <p style="font-size: 1.2rem; opacity: 0.9;">{t('app_subtitle')}</p>
</div>
""", unsafe_allow_html=True)

st.markdown(t('choose_portal'))

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="card">
        <h3 style="color: #0984e3;">{t('hr_portal_title')}</h3>
        <ul>
            <li>{t('hr_feat_1')}</li>
            <li>{t('hr_feat_2')}</li>
            <li>{t('hr_feat_3')}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button(t('enter_hr'), use_container_width=True):
        st.switch_page("pages/1_hr_portal.py")

with col2:
    st.markdown(f"""
    <div class="card">
        <h3 style="color: #d63031;">{t('cand_portal_title')}</h3>
        <ul>
            <li>{t('cand_feat_1')}</li>
            <li>{t('cand_feat_2')}</li>
            <li>{t('cand_feat_3')}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button(t('enter_cand'), use_container_width=True):
        st.switch_page("pages/2_candidate_portal.py")