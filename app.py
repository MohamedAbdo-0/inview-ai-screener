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

st.markdown(f"""
<div class="main-hero">
    <h1 class="glow-text" style="font-size: 4rem; margin-bottom: 0;">{t('page_title_app').split(' ')[0]}</h1>
    <h2 style="font-weight: 300; opacity: 0.8; margin-top: -10px;">{t('page_title_app').split(' ', 1)[1] if ' ' in t('page_title_app') else ''}</h2>
    <p style="font-size: 1.3rem; opacity: 0.7; max-width: 700px; margin: 20px auto;">{t('app_subtitle')}</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"<h3 style='text-align: center; margin-bottom: 40px;'>{t('choose_portal')}</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="glass-card">
        <h3 style="color: #0984e3; margin-top: 0;">{t('hr_portal_title')}</h3>
        <p style="font-size: 0.9rem; opacity: 0.8; margin-bottom: 20px;">Manage your recruitment pipeline with AI-driven insights.</p>
        <ul class="feature-list">
            <li>{t('hr_feat_1')}</li>
            <li>{t('hr_feat_2')}</li>
            <li>{t('hr_feat_3')}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button(t('enter_hr'), use_container_width=True, key="hr_btn"):
        st.switch_page("pages/1_hr_portal.py")

with col2:
    st.markdown(f"""
    <div class="glass-card">
        <h3 style="color: #00cec9; margin-top: 0;">{t('cand_portal_title')}</h3>
        <p style="font-size: 0.9rem; opacity: 0.8; margin-bottom: 20px;">Experience a fair and intelligent AI video interview.</p>
        <ul class="feature-list">
            <li>{t('cand_feat_1')}</li>
            <li>{t('cand_feat_2')}</li>
            <li>{t('cand_feat_3')}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button(t('enter_cand'), use_container_width=True, key="cand_btn"):
        st.switch_page("pages/2_candidate_portal.py")