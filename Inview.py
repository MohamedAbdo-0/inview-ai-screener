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
st.markdown(f, unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center; margin-bottom: 40px;'>{t('choose_portal')}</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown(f, unsafe_allow_html=True)
    if st.button(t('enter_hr'), use_container_width=True, key="hr_btn"):
        st.switch_page("pages/1_hr_portal.py")
with col2:
    st.markdown(f, unsafe_allow_html=True)
    if st.button(t('enter_cand'), use_container_width=True, key="cand_btn"):
        st.switch_page("pages/2_candidate_portal.py")