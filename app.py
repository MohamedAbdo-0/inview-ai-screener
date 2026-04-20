# Inview AI Screener — Redesigned
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

# ── DESIGN SYSTEM ──────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&family=Tajawal:wght@300;400;700&display=swap');

:root {
    --grad-1: #ff6b35;
    --grad-2: #f7c59f;
    --grad-3: #efefd0;
    --accent-blue: #004e89;
    --accent-teal: #1a936f;
    --surface: rgba(255,255,255,0.06);
    --border: rgba(255,255,255,0.12);
    --text-primary: #ffffff;
    --text-muted: rgba(255,255,255,0.65);
    --shadow-glow: 0 0 60px rgba(255,107,53,0.25);
}

/* ── GLOBAL RESET ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #080c14 !important;
    font-family: 'DM Sans', 'Tajawal', sans-serif;
    color: var(--text-primary);
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 20% -10%, rgba(255,107,53,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 110%, rgba(26,147,111,0.14) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 50% 50%, rgba(0,78,137,0.10) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

/* Noise texture overlay */
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.4;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

[data-testid="stSidebar"] { display: none !important; }

/* ── MAIN CONTAINER ── */
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
    position: relative;
    z-index: 1;
}

/* ── HERO SECTION ── */
.hero-wrapper {
    min-height: 46vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 70px 40px 40px;
    position: relative;
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,107,53,0.12);
    border: 1px solid rgba(255,107,53,0.35);
    border-radius: 100px;
    padding: 6px 18px;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #ff6b35;
    margin-bottom: 28px;
    animation: fadeSlideDown 0.6s ease both;
}

.badge-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #ff6b35;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(3rem, 7vw, 6rem);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -0.03em;
    margin: 0 0 12px;
    animation: fadeSlideDown 0.7s 0.1s ease both;
}

.hero-title .gradient-word {
    background: linear-gradient(135deg, #ff6b35 0%, #f7c59f 50%, #ff9f7f 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-title .plain-word {
    color: #ffffff;
}

.hero-subtitle {
    font-size: clamp(1rem, 2vw, 1.25rem);
    font-weight: 300;
    color: var(--text-muted);
    max-width: 580px;
    line-height: 1.65;
    margin: 16px auto 0;
    animation: fadeSlideDown 0.7s 0.2s ease both;
}

/* ── DIVIDER ── */
.section-divider {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 0 60px;
    margin: 8px 0 36px;
    animation: fadeSlideDown 0.7s 0.3s ease both;
}

.section-divider::before,
.section-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

.section-label {
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text-muted);
    white-space: nowrap;
}

/* ── PORTAL CARDS ── */
.portals-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    padding: 0 48px 64px;
    animation: fadeSlideUp 0.8s 0.35s ease both;
}

.portal-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 36px;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}

.portal-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--card-gradient);
    opacity: 0.9;
}

.portal-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 24px 60px rgba(0,0,0,0.35), var(--card-glow);
    border-color: var(--card-accent);
}

.portal-card.hr {
    --card-gradient: linear-gradient(90deg, #ff6b35, #f7c59f);
    --card-accent: rgba(255,107,53,0.4);
    --card-glow: 0 0 40px rgba(255,107,53,0.12);
}

.portal-card.candidate {
    --card-gradient: linear-gradient(90deg, #1a936f, #88d8b0);
    --card-accent: rgba(26,147,111,0.4);
    --card-glow: 0 0 40px rgba(26,147,111,0.12);
}

.card-icon {
    width: 52px; height: 52px;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem;
    margin-bottom: 20px;
}

.portal-card.hr .card-icon { background: rgba(255,107,53,0.15); }
.portal-card.candidate .card-icon { background: rgba(26,147,111,0.15); }

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    margin: 0 0 10px;
    color: #ffffff;
}

.card-desc {
    font-size: 0.88rem;
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 24px;
}

.feature-pills {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 32px;
}

.feature-pill {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.83rem;
    color: rgba(255,255,255,0.75);
}

.pill-dot {
    width: 5px; height: 5px;
    border-radius: 50%;
    flex-shrink: 0;
}

.portal-card.hr .pill-dot { background: #ff6b35; }
.portal-card.candidate .pill-dot { background: #1a936f; }

/* ── STATS BAR ── */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: 60px;
    padding: 20px 48px 36px;
    animation: fadeSlideUp 0.8s 0.5s ease both;
}

.stat-item {
    text-align: center;
}

.stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ff6b35, #f7c59f);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: block;
}

.stat-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── LANGUAGE SWITCHER ── */
.lang-area {
    position: fixed;
    top: 20px; right: 24px;
    z-index: 999;
}

/* ── STREAMLIT BUTTON OVERRIDES ── */
[data-testid="stButton"] > button {
    width: 100% !important;
    padding: 14px 28px !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    position: relative !important;
    overflow: hidden !important;
}

[data-testid="stButton"][data-key="hr_btn"] > button {
    background: linear-gradient(135deg, #ff6b35 0%, #e55a20 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 20px rgba(255,107,53,0.35) !important;
}

[data-testid="stButton"][data-key="hr_btn"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(255,107,53,0.5) !important;
}

[data-testid="stButton"][data-key="cand_btn"] > button {
    background: linear-gradient(135deg, #1a936f 0%, #137a5c 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 20px rgba(26,147,111,0.35) !important;
}

[data-testid="stButton"][data-key="cand_btn"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(26,147,111,0.5) !important;
}

[data-testid="stButton"][data-key="lang_btn"] > button {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-muted) !important;
    padding: 8px 16px !important;
    font-size: 0.78rem !important;
    width: auto !important;
    backdrop-filter: blur(8px) !important;
}

/* ── ANIMATIONS ── */
@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── RTL SUPPORT ── */
[dir="rtl"] .portals-grid { direction: rtl; }
[dir="rtl"] .feature-pill { flex-direction: row-reverse; }
[dir="rtl"] .stats-bar { direction: rtl; }
[dir="rtl"] .badge { direction: rtl; }

/* ── RESPONSIVE ── */
@media (max-width: 768px) {
    .portals-grid { grid-template-columns: 1fr; padding: 0 20px 40px; }
    .stats-bar { gap: 30px; flex-wrap: wrap; }
    .hero-wrapper { padding: 50px 20px 30px; }
    .section-divider { padding: 0 20px; }
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── LANGUAGE SELECTOR ─────────────────────────────────────────────────────────
try:
    select_language()
except Exception:
    pass

# ── HERO ─────────────────────────────────────────────────────────────────────
title_full = t('page_title_app') if callable(t) else "Inview AI Screener"
title_parts = title_full.split(' ', 1)
word1 = title_parts[0]
word2 = title_parts[1] if len(title_parts) > 1 else ""

subtitle = t('app_subtitle') if callable(t) else "AI-powered video interviews that are fast, fair, and insightful."

st.markdown(f"""
<div class="hero-wrapper">
    <div class="badge">
        <span class="badge-dot"></span>
        AI-Powered Recruitment
    </div>
    <h1 class="hero-title">
        <span class="gradient-word">{word1}</span>
        {"<br><span class='plain-word'>" + word2 + "</span>" if word2 else ""}
    </h1>
    <p class="hero-subtitle">{subtitle}</p>
</div>
""", unsafe_allow_html=True)

# ── DIVIDER ───────────────────────────────────────────────────────────────────
choose_label = t('choose_portal') if callable(t) else "Choose your portal"
st.markdown(f"""
<div class="section-divider">
    <span class="section-label">{choose_label}</span>
</div>
""", unsafe_allow_html=True)

# ── PORTAL CARDS ─────────────────────────────────────────────────────────────
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
    st.markdown(f"""
    <div class="portal-card hr">
        <div class="card-icon">🏢</div>
        <div class="card-title">{hr_title}</div>
        <div class="card-desc">Manage your recruitment pipeline with AI-driven insights and automated screening.</div>
        <div class="feature-pills">
            <div class="feature-pill"><span class="pill-dot"></span>{hr_feat1}</div>
            <div class="feature-pill"><span class="pill-dot"></span>{hr_feat2}</div>
            <div class="feature-pill"><span class="pill-dot"></span>{hr_feat3}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(hr_btn, use_container_width=True, key="hr_btn"):
        st.switch_page("pages/1_hr_portal.py")

with col2:
    st.markdown(f"""
    <div class="portal-card candidate">
        <div class="card-icon">🎯</div>
        <div class="card-title">{cand_title}</div>
        <div class="card-desc">Experience a fair and intelligent AI video interview from the comfort of your home.</div>
        <div class="feature-pills">
            <div class="feature-pill"><span class="pill-dot"></span>{cand_feat1}</div>
            <div class="feature-pill"><span class="pill-dot"></span>{cand_feat2}</div>
            <div class="feature-pill"><span class="pill-dot"></span>{cand_feat3}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(cand_btn, use_container_width=True, key="cand_btn"):
        st.switch_page("pages/2_candidate_portal.py")

st.markdown('</div>', unsafe_allow_html=True)

# ── STATS BAR ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-bar">
    <div class="stat-item">
        <span class="stat-number">98%</span>
        <span class="stat-label">Accuracy Rate</span>
    </div>
    <div class="stat-item">
        <span class="stat-number">3×</span>
        <span class="stat-label">Faster Hiring</span>
    </div>
    <div class="stat-item">
        <span class="stat-number">AI</span>
        <span class="stat-label">Bias-Free</span>
    </div>
    <div class="stat-item">
        <span class="stat-number">24/7</span>
        <span class="stat-label">Available</span>
    </div>
</div>
""", unsafe_allow_html=True)