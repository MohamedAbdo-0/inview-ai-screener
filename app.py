import streamlit as st
import os
import sys
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
CUSTOM_CSS = 
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
try:
    select_language()
except Exception:
    pass
title_full = t('page_title_app') if callable(t) else "Inview AI Screener"
title_parts = title_full.split(' ', 1)
word1 = title_parts[0]
word2 = title_parts[1] if len(title_parts) > 1 else ""
subtitle = t('app_subtitle') if callable(t) else "AI-powered video interviews that are fast, fair, and insightful."
st.markdown(f, unsafe_allow_html=True)
choose_label = t('choose_portal') if callable(t) else "Choose your portal"
st.markdown(f, unsafe_allow_html=True)
hr_title  = t('hr_portal_title')  if callable(t) else "HR Portal"
hr_feat1  = t('hr_feat_1')        if callable(t) else "AI Candidate Screening"
hr_feat2  = t('hr_feat_2')        if callable(t) else "Smart Pipeline Management"
hr_feat3  = t('hr_feat_3')        if callable(t) else "Deep Analytics & Reports"
hr_btn    = t('enter_hr')         if callable(t) else "Enter HR Portal →"
cand_title = t('cand_portal_title') if callable(t) else "Candidate Portal"
cand_feat1 = t('cand_feat_1')       if callable(t) else "AI Video Interview"
cand_feat2 = t('cand_feat_2')       if callable(t) else "Real-time Feedback"
cand_feat3 = t('cand_feat_3')       if callable(t) else "Transparent Scoring"
cand_btn   = t('enter_cand')        if callable(t) else "Enter Candidate Portal →"
st.markdown('<div class="portals-grid">', unsafe_allow_html=True)
col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown(f, unsafe_allow_html=True)
    if st.button(hr_btn, use_container_width=True, key="hr_btn"):
        st.switch_page("pages/1_hr_portal.py")
with col2:
    st.markdown(f, unsafe_allow_html=True)
    if st.button(cand_btn, use_container_width=True, key="cand_btn"):
        st.switch_page("pages/2_candidate_portal.py")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown(, unsafe_allow_html=True)