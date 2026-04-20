# Inview AI Screener — HR Portal
import streamlit as st
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from db_manager import get_db, save_db
    import core_functions
    import importlib
    importlib.reload(core_functions)
    from core_functions import (
        transcribe_audio,
        get_ai_response,
        build_analysis_prompt,
    )
    from i18n import t, get_base_css, select_language
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

st.set_page_config(
    page_title="Inview — HR Portal",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

select_language()

# ── DESIGN SYSTEM ──────────────────────────────────────────────────────────────
HR_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500&family=Tajawal:wght@300;400;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --orange:       #ff6b35;
    --orange-dim:   rgba(255,107,53,0.12);
    --orange-border:rgba(255,107,53,0.30);
    --teal:         #1a936f;
    --teal-dim:     rgba(26,147,111,0.12);
    --teal-border:  rgba(26,147,111,0.30);
    --blue:         #0984e3;
    --blue-dim:     rgba(9,132,227,0.10);
    --red:          #e17055;
    --red-dim:      rgba(225,112,85,0.12);
    --amber:        #fdcb6e;
    --amber-dim:    rgba(253,203,110,0.12);
    --surface:      rgba(255,255,255,0.055);
    --border:       rgba(255,255,255,0.10);
    --text:         #ffffff;
    --muted:        rgba(255,255,255,0.55);
    --bg:           #080c14;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'DM Sans','Tajawal',sans-serif;
    color: var(--text);
}

[data-testid="stAppViewContainer"]::before {
    content:'';position:fixed;inset:0;pointer-events:none;
    background:
        radial-gradient(ellipse 70% 50% at 15% -5%, rgba(255,107,53,.14) 0%,transparent 60%),
        radial-gradient(ellipse 50% 40% at 85% 105%, rgba(26,147,111,.12) 0%,transparent 55%);
    z-index:0;
}

#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebar"]{display:none!important}

.main .block-container{
    padding: 2rem 3rem !important;
    max-width: 1300px !important;
    margin: 0 auto;
    position: relative; z-index: 1;
}

/* ── PAGE HEADER ── */
.page-header {
    display: flex; align-items: center; gap: 16px;
    margin-bottom: 36px; padding-bottom: 24px;
    border-bottom: 1px solid var(--border);
}
.page-icon {
    width: 52px; height: 52px; border-radius: 14px;
    background: var(--orange-dim); border: 1px solid var(--orange-border);
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
}
.page-title {
    font-family:'Syne',sans-serif; font-size:1.6rem;
    font-weight:800; margin:0; letter-spacing:-.02em;
}
.page-badge {
    margin-left:auto;
    background: var(--orange-dim); border:1px solid var(--orange-border);
    border-radius:100px; padding:5px 14px;
    font-size:11px; font-weight:500; letter-spacing:.1em;
    text-transform:uppercase; color:var(--orange);
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background:transparent!important;
    gap:8px; border-bottom:1px solid var(--border)!important;
}
.stTabs [data-baseweb="tab"] {
    background:transparent!important;
    border-radius:10px 10px 0 0!important;
    color:var(--muted)!important;
    padding:10px 24px!important;
    font-family:'Syne',sans-serif!important;
    font-size:.85rem!important; font-weight:600!important;
    border:none!important; transition:all .2s!important;
}
.stTabs [aria-selected="true"] {
    color:var(--text)!important;
    background:var(--orange-dim)!important;
    border-bottom:2px solid var(--orange)!important;
}

/* ── QUESTION CARDS ── */
.q-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--orange);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 10px;
    display: flex; align-items: flex-start; gap: 14px;
    transition: border-color .2s;
}
.q-card:hover { border-left-color: var(--teal); }
.q-num {
    font-family:'JetBrains Mono',monospace;
    font-size:.75rem; color:var(--orange);
    background:var(--orange-dim); border-radius:6px;
    padding:3px 8px; flex-shrink:0; margin-top:2px;
}
.q-text { flex:1; font-size:.9rem; line-height:1.55; }
.q-skill {
    font-size:.75rem; color:var(--muted);
    background:var(--surface); border:1px solid var(--border);
    border-radius:100px; padding:3px 10px; flex-shrink:0;
}

/* ── STATUS BANNER ── */
.status-banner {
    border-radius:14px; padding:20px 24px;
    display:flex; align-items:center; gap:16px;
    margin-bottom:28px;
}
.status-banner.pending  { background:var(--amber-dim); border:1px solid rgba(253,203,110,.3); }
.status-banner.success  { background:var(--teal-dim);  border:1px solid var(--teal-border);  }
.status-banner.danger   { background:var(--red-dim);   border:1px solid rgba(225,112,85,.3); }
.status-icon { font-size:1.6rem; }
.status-text { font-size:.9rem; line-height:1.5; }
.status-text strong { display:block; font-size:1rem; margin-bottom:3px; }

/* ── PROCTORING BADGE ── */
.proctor-chip {
    display:inline-flex; align-items:center; gap:8px;
    background:var(--surface); border:1px solid var(--border);
    border-radius:100px; padding:7px 16px;
    font-size:.82rem; margin-bottom:20px;
}
.proctor-dot { width:8px; height:8px; border-radius:50%; flex-shrink:0; }

/* ── TRANSCRIPT CARD ── */
.transcript-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px;
    margin: 24px 0;
}
.transcript-title {
    font-family:'Syne',sans-serif; font-size:1rem;
    font-weight:700; margin-bottom:20px;
    display:flex; align-items:center; gap:10px;
    color:var(--text);
}
.q-block {
    border-left:2px solid var(--orange-border);
    padding: 12px 16px;
    margin-bottom:16px;
    border-radius: 0 8px 8px 0;
    background:rgba(255,107,53,.04);
}
.q-block-label {
    font-size:.75rem; font-weight:600;
    color:var(--orange); letter-spacing:.08em;
    text-transform:uppercase; margin-bottom:6px;
}
.q-block-question { font-size:.88rem; font-weight:500; margin-bottom:8px; }
.q-block-answer {
    font-size:.85rem; color:var(--muted); line-height:1.65;
    font-style:italic;
}

/* ── SCORE CARDS ── */
.scores-grid {
    display:grid; grid-template-columns:repeat(4,1fr);
    gap:14px; margin:24px 0;
}
.score-card {
    background:var(--surface); border:1px solid var(--border);
    border-radius:14px; padding:20px 16px; text-align:center;
}
.score-card .sc-val {
    font-family:'Syne',sans-serif; font-size:1.8rem;
    font-weight:800; display:block; margin-bottom:4px;
}
.score-card .sc-lbl {
    font-size:.72rem; color:var(--muted);
    letter-spacing:.08em; text-transform:uppercase;
}
.score-card.total {
    background:var(--orange-dim); border-color:var(--orange-border);
    grid-column:span 4;
}
.score-card.total .sc-val {
    font-size:2.4rem;
    background:linear-gradient(135deg,#ff6b35,#f7c59f);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text;
}

/* ── RECOMMENDATION BADGES ── */
.rec-hire    { background:rgba(26,147,111,.15); border:1px solid var(--teal-border);   border-radius:14px; padding:20px 24px; }
.rec-consider{ background:var(--amber-dim);     border:1px solid rgba(253,203,110,.3); border-radius:14px; padding:20px 24px; }
.rec-no-hire { background:var(--red-dim);       border:1px solid rgba(225,112,85,.3);  border-radius:14px; padding:20px 24px; }
.rec-title { font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:800; margin-bottom:8px; }
.rec-reason{ font-size:.88rem; color:var(--muted); line-height:1.6; }

/* ── EVALUATION CONTAINER ── */
.eval-section {
    background:var(--surface); border:1px solid var(--border);
    border-radius:16px; padding:32px;
    margin:20px 0;
}
.eval-section h1,.eval-section h2,.eval-section h3 {
    font-family:'Syne',sans-serif!important;
    letter-spacing:-.02em;
}
.eval-section table {
    width:100%; border-collapse:collapse;
    font-size:.88rem; margin:12px 0;
}
.eval-section th {
    background:var(--orange-dim); color:var(--orange);
    padding:10px 14px; text-align:left; font-weight:600;
    font-size:.78rem; letter-spacing:.06em; text-transform:uppercase;
}
.eval-section td {
    padding:10px 14px; border-bottom:1px solid var(--border);
    color:var(--muted);
}
.eval-section td:first-child { color:var(--text); font-weight:500; }

/* ── STREAMLIT OVERRIDES ── */
[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input {
    background:var(--surface)!important;
    border:1px solid var(--border)!important;
    color:var(--text)!important;
    border-radius:10px!important;
    font-family:'DM Sans',sans-serif!important;
}
[data-testid="stTextArea"] textarea:focus,
[data-testid="stTextInput"] input:focus {
    border-color:var(--orange)!important;
    box-shadow:0 0 0 2px var(--orange-border)!important;
}

[data-testid="stButton"] > button {
    border-radius:10px!important;
    font-family:'Syne',sans-serif!important;
    font-size:.85rem!important; font-weight:600!important;
    letter-spacing:.04em!important;
    transition:all .25s!important;
}
[data-testid="stButton"][data-key="add_q"] > button {
    background:var(--orange-dim)!important;
    border:1px solid var(--orange-border)!important;
    color:var(--orange)!important;
}
[data-testid="stButton"][data-key="confirm_btn"] > button,
[data-testid="stButton"][data-key="analyze_btn"] > button {
    background:linear-gradient(135deg,#ff6b35,#e55a20)!important;
    border:none!important; color:#fff!important;
    box-shadow:0 4px 20px rgba(255,107,53,.3)!important;
}
[data-testid="stButton"][data-key="confirm_btn"] > button:hover,
[data-testid="stButton"][data-key="analyze_btn"] > button:hover {
    transform:translateY(-2px)!important;
    box-shadow:0 8px 28px rgba(255,107,53,.45)!important;
}
[data-testid="stButton"][data-key="delete_btn"] > button {
    background:var(--red-dim)!important;
    border:1px solid rgba(225,112,85,.3)!important;
    color:var(--red)!important;
}
[data-testid="stButton"][data-key="reset_btn"] > button {
    background:var(--surface)!important;
    border:1px solid var(--border)!important;
    color:var(--muted)!important;
}

[data-testid="stVideo"] { border-radius:14px!important; overflow:hidden!important; }
[data-testid="stSpinner"] > div { color:var(--orange)!important; }

/* ── PROGRESS STEPS ── */
.steps-row {
    display:flex; gap:0; margin-bottom:32px;
}
.step {
    flex:1; text-align:center; position:relative;
    padding:14px 8px 10px;
}
.step::after {
    content:''; position:absolute;
    top:22px; left:50%; width:100%; height:1px;
    background:var(--border);
}
.step:last-child::after { display:none; }
.step-num {
    width:30px; height:30px; border-radius:50%;
    display:inline-flex; align-items:center; justify-content:center;
    font-family:'Syne',sans-serif; font-size:.8rem; font-weight:700;
    position:relative; z-index:1; margin-bottom:6px;
}
.step.done .step-num  { background:var(--teal); color:#fff; }
.step.active .step-num{ background:var(--orange); color:#fff; }
.step.idle .step-num  { background:var(--surface); border:1px solid var(--border); color:var(--muted); }
.step-label { font-size:.72rem; color:var(--muted); letter-spacing:.06em; text-transform:uppercase; }
.step.active .step-label { color:var(--orange); }
.step.done .step-label   { color:var(--teal); }

/* RTL */
[dir="rtl"] .page-badge { margin-left:0; margin-right:auto; }
[dir="rtl"] .q-card { border-left:none; border-right:3px solid var(--orange); }
[dir="rtl"] .q-block { border-left:none; border-right:2px solid var(--orange-border); border-radius:8px 0 0 8px; }
</style>
"""

st.markdown(HR_CSS, unsafe_allow_html=True)

# ── HELPER: STATUS → STEP INDEX ───────────────────────────────────────────────
STATUS_STEP = {
    "pending":              0,
    "ready_for_candidate":  1,
    "completed":            2,
    "analyzed":             3,
}

def render_steps(current_status: str):
    step_idx = STATUS_STEP.get(current_status, 0)
    labels = ["Setup Questions", "Waiting Candidate", "Interview Done", "Report Ready"]
    html = '<div class="steps-row">'
    for i, lbl in enumerate(labels):
        if i < step_idx:
            cls = "done";  num = "✓"
        elif i == step_idx:
            cls = "active"; num = str(i+1)
        else:
            cls = "idle";  num = str(i+1)
        html += f'<div class="step {cls}"><div class="step-num">{num}</div><div class="step-label">{lbl}</div></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def proctor_chip(msg: str):
    safe = "safe" in msg.lower() or "آمن" in msg
    dot_color = "#1a936f" if safe else "#e17055"
    icon = "🛡️" if safe else "⚠️"
    st.markdown(
        f'<div class="proctor-chip">'
        f'<span class="proctor-dot" style="background:{dot_color}"></span>'
        f'{icon} <strong>Proctoring:</strong> {msg}'
        f"</div>",
        unsafe_allow_html=True,
    )


def render_score_cards(report_text: str):
    """Extract scores from the AI report and render visual score cards."""
    import re
    # Match English or Arabic keywords
    total_match = re.search(r"(Total Score|الدرجة النهائية)[:\s*]+(\d+)\s*/\s*100", report_text)
    tech_match  = re.search(r"(Technical Score|الدرجة الفنية)[:\s*]+(\d+)\s*/\s*40", report_text)
    comm_match  = re.search(r"(Communication Score|درجة التواصل)[:\s*]+(\d+)\s*/\s*20", report_text)
    prob_match  = re.search(r"(Problem Solving Score|درجة حل المشكلات)[:\s*]+(\d+)\s*/\s*20", report_text)
    beh_match   = re.search(r"(Behavioral Score|الدرجة السلوكية)[:\s*]+(\d+)\s*/\s*20", report_text)

    total = total_match.group(2) if total_match else "—"
    tech  = tech_match.group(2)  if tech_match  else "—"
    comm  = comm_match.group(2)  if comm_match  else "—"
    prob  = prob_match.group(2)  if prob_match  else "—"
    beh   = beh_match.group(2)   if beh_match   else "—"

    # Use translations for labels if available, else fallback
    lbl_tech = t('lbl_tech') if t('lbl_tech') != 'lbl_tech' else "Technical"
    lbl_comm = t('lbl_comm') if t('lbl_comm') != 'lbl_comm' else "Communication"
    lbl_prob = t('lbl_prob') if t('lbl_prob') != 'lbl_prob' else "Problem Solving"
    lbl_beh  = t('lbl_beh')  if t('lbl_beh') != 'lbl_beh'  else "Behavioral"
    lbl_total = t('lbl_total') if t('lbl_total') != 'lbl_total' else "Overall Score"

    st.markdown(f"""
    <div class="scores-grid">
        <div class="score-card">
            <span class="sc-val" style="color:#0984e3">{tech}<span style="font-size:.9rem;opacity:.6">/40</span></span>
            <span class="sc-lbl">{lbl_tech}</span>
        </div>
        <div class="score-card">
            <span class="sc-val" style="color:#1a936f">{comm}<span style="font-size:.9rem;opacity:.6">/20</span></span>
            <span class="sc-lbl">{lbl_comm}</span>
        </div>
        <div class="score-card">
            <span class="sc-val" style="color:#fdcb6e">{prob}<span style="font-size:.9rem;opacity:.6">/20</span></span>
            <span class="sc-lbl">{lbl_prob}</span>
        </div>
        <div class="score-card">
            <span class="sc-val" style="color:#a29bfe">{beh}<span style="font-size:.9rem;opacity:.6">/20</span></span>
            <span class="sc-lbl">{lbl_beh}</span>
        </div>
        <div class="score-card total">
            <span class="sc-val">{total}<span style="font-size:2.4rem;opacity:.5">/100</span></span>
            <span class="sc-lbl">{lbl_total}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_recommendation(report_text: str):
    """Detect the final recommendation and render a styled card."""
    rt = report_text.upper()
    # Check for English or Arabic keywords
    if "DO NOT HIRE" in rt or "عدم التوظيف" in report_text:
        cls, icon, label = "rec-no-hire", "🔴", t('rec_no_hire') if t('rec_no_hire') != 'rec_no_hire' else "DO NOT HIRE"
    elif "CONSIDER" in rt or "للمراجعة" in report_text:
        cls, icon, label = "rec-consider", "🟡", t('rec_consider') if t('rec_consider') != 'rec_consider' else "CONSIDER — Second Interview Recommended"
    else:
        cls, icon, label = "rec-hire", "🟢", t('rec_hire') if t('rec_hire') != 'rec_hire' else "HIRE — Recommended to Proceed"

    st.markdown(f"""
    <div class="{cls}">
        <div class="rec-title">{icon} Final Recommendation: {label}</div>
    </div>
    """, unsafe_allow_html=True)


# ── PAGE ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
    <div class="page-icon">🏢</div>
    <div>
        <div class="page-title">{t('hr_main_title')}</div>
        <div style="font-size:.82rem;color:rgba(255,255,255,.45);margin-top:2px;">Inview AI Screener</div>
    </div>
    <div class="page-badge">HR Dashboard</div>
</div>
""", unsafe_allow_html=True)

db = get_db()
render_steps(db.get("status", "pending"))

tab1, tab2 = st.tabs([f"📋  {t('tab_prepare')}", f"📊  {t('tab_report')}"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — PREPARE INTERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.markdown('<div style="font-size:.8rem;color:rgba(255,255,255,.4);letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px;">Question</div>', unsafe_allow_html=True)
        new_q = st.text_area(
            label="",
            placeholder=t("q_text"),
            height=130,
            label_visibility="collapsed",
        )

    with col2:
        st.markdown('<div style="font-size:.8rem;color:rgba(255,255,255,.4);letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px;">Skill Tag</div>', unsafe_allow_html=True)
        new_skill = st.text_input(
            label="",
            placeholder=t("q_skill"),
            label_visibility="collapsed",
        )
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        if st.button(f"＋  {t('add_q_btn')}", use_container_width=True, key="add_q"):
            if new_q and new_skill:
                db["questions"].append({"question": new_q, "skill": new_skill})
                save_db(db)
                st.success(t("q_added_success"))
                st.rerun()
            else:
                st.error(t("fill_fields_err"))

    # Question list
    if db["questions"]:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:.8rem;color:rgba(255,255,255,.4);letter-spacing:.08em;text-transform:uppercase;margin-bottom:12px;">{len(db["questions"])} Questions Added</div>', unsafe_allow_html=True)

        for i, q in enumerate(db["questions"]):
            st.markdown(f"""
            <div class="q-card">
                <span class="q-num">Q{i+1}</span>
                <span class="q-text">{q['question']}</span>
                <span class="q-skill">🏷 {q['skill']}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        ca, cb = st.columns(2)
        with ca:
            if st.button(f"🗑  {t('delete_all_q_btn')}", use_container_width=True, key="delete_btn"):
                db["questions"] = []
                db["status"] = "pending"
                save_db(db)
                st.rerun()
        with cb:
            if st.button(f"✅  {t('confirm_open_interview_btn')}", use_container_width=True, key="confirm_btn", type="primary"):
                db["status"] = "ready_for_candidate"
                db["video_path"] = None
                db["analysis_report"] = ""
                save_db(db)
                st.success(t("questions_confirmed"))
                st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center;padding:40px 20px;color:rgba(255,255,255,.3);">
            <div style="font-size:2.5rem;margin-bottom:12px;">📝</div>
            <div style="font-size:.9rem;">No questions added yet. Start by adding your first question above.</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — REPORT
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    status = db.get("status", "pending")

    # ── PENDING / READY ──────────────────────────────────────────────────────
    if status in ("pending", "ready_for_candidate"):
        icon  = "⏳" if status == "pending" else "🎙️"
        title = "Setup in Progress" if status == "pending" else "Waiting for Candidate"
        body  = "Add and confirm interview questions first." if status == "pending" else "The interview session is open. Waiting for the candidate to complete it."
        st.markdown(f"""
        <div class="status-banner pending">
            <div class="status-icon">{icon}</div>
            <div class="status-text"><strong>{title}</strong>{body}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── COMPLETED — NEEDS ANALYSIS ───────────────────────────────────────────
    elif status == "completed":
        st.markdown("""
        <div class="status-banner success">
            <div class="status-icon">🎉</div>
            <div class="status-text"><strong>Interview Completed</strong>The candidate has finished the interview. Review the recording and run AI analysis.</div>
        </div>
        """, unsafe_allow_html=True)

        proctor_chip(db.get("proctor_msg", ""))

        if db.get("video_path") and os.path.exists(db["video_path"]):
            st.markdown('<div style="font-size:.8rem;color:rgba(255,255,255,.4);letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px;">Recording</div>', unsafe_allow_html=True)
            st.video(db["video_path"])
        else:
            st.warning(t("video_missing"))

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        if st.button(f"🤖  {t('extract_analyze_btn')}", type="primary", use_container_width=True, key="analyze_btn"):
            if not HF_TOKEN:
                st.error(t("hf_token_err"))
                st.stop()

            splits        = db["splits"]
            vid_path      = db["video_path"]
            all_questions = db["questions"]

            questions_text_with_answers = ""
            transcript_blocks           = []

            progress = st.progress(0, text="Extracting audio segments…")

            try:
                import imageio_ffmpeg
                import subprocess as _sp
                ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

                for i, q in enumerate(all_questions):
                    progress.progress(
                        int((i / len(all_questions)) * 60),
                        text=f"Transcribing answer {i+1}/{len(all_questions)}…"
                    )
                    start_t  = float(splits[i])
                    end_t    = float(splits[i + 1])
                    duration = max(0.1, end_t - start_t)
                    tmp_wav  = f"temp_audio_{i}.wav"

                    _sp.run(
                        [ffmpeg_exe, "-ss", str(start_t), "-i", vid_path,
                         "-t", str(duration),
                         "-vn", "-acodec", "pcm_s16le",
                         "-ar", "16000", "-ac", "1", tmp_wav, "-y"],
                        check=True, capture_output=True,
                    )

                    try:
                        transcript_i = transcribe_audio(tmp_wav, HF_TOKEN, lang=st.session_state.lang)
                        if not transcript_i or not transcript_i.strip():
                            transcript_i = t("no_speech")
                    except Exception:
                        transcript_i = t("short_ans_err")

                    transcript_blocks.append({
                        "question": q["question"],
                        "skill":    q["skill"],
                        "answer":   transcript_i,
                        "index":    i + 1,
                    })

                    questions_text_with_answers += (
                        f"Question {i+1}: {q['question']} (Skill: {q['skill']})\n"
                        f"Candidate's Answer: {transcript_i}\n\n"
                    )

                    try:
                        os.remove(tmp_wav)
                    except Exception:
                        pass

            except Exception as e:
                st.error(f"{t('error_accured')} {e}")
                questions_text_with_answers = None

            if questions_text_with_answers:
                # Build structured transcript markdown
                transcript_md = "## 📝 Interview Transcript\n\n"
                for blk in transcript_blocks:
                    transcript_md += (
                        f"**Q{blk['index']}: {blk['question']}** *(Skill: {blk['skill']})*\n\n"
                        f"> {blk['answer']}\n\n---\n\n"
                    )
                db["transcript_markdown"] = transcript_md
                db["transcript_blocks"]   = transcript_blocks
                save_db(db)

                progress.progress(70, text="Running AI deep analysis…")

                chat_history = build_analysis_prompt(questions_text_with_answers, lang=st.session_state.lang)
                try:
                    ai_report = get_ai_response(HF_TOKEN, chat_history)
                    db["analysis_report"] = ai_report
                    db["status"]          = "analyzed"
                    save_db(db)
                    progress.progress(100, text="Done!")
                    st.rerun()
                except Exception as e:
                    st.error(f"{t('server_error')} {e}")

    # ── ANALYZED — SHOW FULL REPORT ──────────────────────────────────────────
    elif status == "analyzed":
        st.markdown("""
        <div class="status-banner success">
            <div class="status-icon">✅</div>
            <div class="status-text"><strong>Analysis Complete</strong>Full evaluation report is ready below.</div>
        </div>
        """, unsafe_allow_html=True)

        proctor_chip(db.get("proctor_msg", ""))

        # Video
        with st.expander("🎬 Interview Recording", expanded=False):
            if db.get("video_path") and os.path.exists(db["video_path"]):
                st.video(db["video_path"])
            else:
                st.error(t("video_missing"))

        # Score cards
        render_score_cards(db["analysis_report"])

        # Recommendation banner
        render_recommendation(db["analysis_report"])

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # Transcript
        with st.expander("📝 Interview Transcript", expanded=False):
            blocks = db.get("transcript_blocks", [])
            if blocks:
                html = '<div class="transcript-wrap"><div class="transcript-title">🗒️ Full Transcript</div>'
                for blk in blocks:
                    # Remove newlines from HTML to prevent rendering issues in st.markdown
                    html += (
                        f'<div class="q-block">'
                        f'<div class="q-block-label">Q{blk["index"]} · {blk["skill"]}</div>'
                        f'<div class="q-block-question">{blk["question"]}</div>'
                        f'<div class="q-block-answer">"{blk["answer"]}"</div>'
                        f'</div>'
                    )
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.markdown(db.get("transcript_markdown", ""))

        # Full AI Report
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="eval-section">', unsafe_allow_html=True)
        st.markdown(db["analysis_report"])
        st.markdown("</div>", unsafe_allow_html=True)

        # Reset
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if st.button(f"🔄  {t('reset_close_btn')}", use_container_width=True, key="reset_btn"):
            db.update({
                "status":             "pending",
                "questions":          [],
                "analysis_report":    "",
                "transcript_markdown":"",
                "transcript_blocks":  [],
                "video_path":         None,
                "proctor_msg":        "",
            })
            save_db(db)
            st.rerun()
