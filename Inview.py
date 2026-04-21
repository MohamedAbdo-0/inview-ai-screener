import streamlit as st
import os
import sys

# Ensure local imports work
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from i18n import t, get_base_css, select_language
except ImportError:
    st.error("i18n file missing.")
    st.stop()

st.set_page_config(
    page_title="Inview AI Screener",
    page_icon="🚀",
    layout="wide",
)

# Apply Global CSS
st.markdown(get_base_css(), unsafe_allow_html=True)

# Language Selector
select_language()

# Hero Section
title_part1 = "Inview"
title_part2 = "AI Screener"
subtitle = t('app_subtitle')

st.markdown(f"""
<div style="text-align: center; padding: 50px 0;">
    <h1 style="font-size: 3.5rem; font-weight: 800;">
        <span style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title_part1}</span>
        <span style="color: white;"> {title_part2}</span>
    </h1>
    <p style="font-size: 1.2rem; color: rgba(255,255,255,0.7); margin-bottom: 40px;">{subtitle}</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"<h3 style='text-align: center; margin-bottom: 30px;'>{t('choose_portal')}</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(f"""
    <div class="glass-card">
        <h2>{t('hr_portal_title')}</h2>
        <p style="opacity:0.8;">{t('hr_feat_1')}</p>
        <p style="opacity:0.8;">{t('hr_feat_3')}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button(t('enter_hr'), use_container_width=True, key="inview_hr_btn"):
        st.switch_page("pages/1_hr_portal.py")

with col2:
    st.markdown(f"""
    <div class="glass-card">
        <h2>{t('cand_portal_title')}</h2>
        <p style="opacity:0.8;">{t('cand_feat_1')}</p>
        <p style="opacity:0.8;">{t('cand_feat_2')}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button(t('enter_cand'), use_container_width=True, key="inview_cand_btn"):
        st.switch_page("pages/2_candidate_portal.py")