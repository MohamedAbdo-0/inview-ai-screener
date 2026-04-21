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
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Apply Global CSS
st.markdown(get_base_css(), unsafe_allow_html=True)

# Select Language at the top
select_language()

# Hero Section
title_full = t('page_title_app')
title_parts = title_full.split(' ', 1)
word1 = title_parts[0]
word2 = title_parts[1] if len(title_parts) > 1 else ""

hero_html = f"""
<div style="text-align: center; padding: 40px 0;">
    <h1 style="font-size: 4rem; font-weight: 800; margin-bottom: 10px;">
        <span style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{word1}</span>
        <span style="color: white;">{word2}</span>
    </h1>
    <p style="font-size: 1.2rem; color: rgba(255,255,255,0.7); max-width: 700px; margin: 0 auto 30px auto;">
        {t('app_subtitle')}
    </p>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

st.markdown(f"<h3 style='text-align: center; margin-bottom: 40px; color: rgba(255,255,255,0.6);'>{t('choose_portal')}</h3>", unsafe_allow_html=True)

# Portal Selection
col1, col2 = st.columns(2, gap="large")

with col1:
    hr_card = f"""
    <div class="glass-card">
        <h2 style="margin-top:0;">{t('hr_portal_title')}</h2>
        <ul style="color: rgba(255,255,255,0.8); margin-bottom: 25px;">
            <li>{t('hr_feat_1')}</li>
            <li>{t('hr_feat_2')}</li>
            <li>{t('hr_feat_3')}</li>
        </ul>
    </div>
    """
    st.markdown(hr_card, unsafe_allow_html=True)
    if st.button(t('enter_hr'), use_container_width=True, key="hr_btn"):
        st.switch_page("pages/1_hr_portal.py")

with col2:
    cand_card = f"""
    <div class="glass-card">
        <h2 style="margin-top:0;">{t('cand_portal_title')}</h2>
        <ul style="color: rgba(255,255,255,0.8); margin-bottom: 25px;">
            <li>{t('cand_feat_1')}</li>
            <li>{t('cand_feat_2')}</li>
            <li>{t('cand_feat_3')}</li>
        </ul>
    </div>
    """
    st.markdown(cand_card, unsafe_allow_html=True)
    if st.button(t('enter_cand'), use_container_width=True, key="cand_btn"):
        st.switch_page("pages/2_candidate_portal.py")

st.markdown("<div style='height:100px'></div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.3);'>© 2026 Inview AI Screener — Intelligent Recruitment Analysis</p>", unsafe_allow_html=True)