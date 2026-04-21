import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Ensure local imports work
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

# Apply global CSS
st.markdown(get_base_css(), unsafe_allow_html=True)

# Portal-specific styling
HR_CSS = """
<style>
    /* Custom Steps styling */
    .steps-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 40px;
        background: rgba(255,255,255,0.03);
        padding: 20px;
        border-radius: 15px;
    }
    .step {
        display: flex;
        flex-direction: column;
        align-items: center;
        flex: 1;
        position: relative;
    }
    .step-num {
        width: 35px;
        height: 35px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-bottom: 8px;
        z-index: 2;
    }
    .step.done .step-num { background: #4facfe; color: white; }
    .step.active .step-num { background: white; color: #16213e; box-shadow: 0 0 15px #4facfe; }
    .step.idle .step-num { background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.3); }
    .step-label { font-size: 0.8rem; font-weight: 600; opacity: 0.7; }

    /* Score cards */
    .score-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin-bottom: 25px;
    }
    .score-card {
        background: rgba(255,255,255,0.05);
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .score-val { font-size: 1.5rem; font-weight: bold; color: #4facfe; }
    .score-lbl { font-size: 0.7rem; opacity: 0.6; text-transform: uppercase; }

    /* Proctoring Chip */
    .proctor-chip {
        display: inline-flex;
        align-items: center;
        padding: 6px 14px;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255,255,255,0.1);
        font-size: 0.85rem;
        margin-bottom: 15px;
    }
    .proctor-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 8px;
        margin-left: 8px;
    }
</style>
"""
st.markdown(HR_CSS, unsafe_allow_html=True)

select_language()

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
    dot_color = "#00ff88" if safe else "#ff4b4b"
    icon = "🛡️" if safe else "⚠️"
    st.markdown(
        f'<div class="proctor-chip">'
        f'<span class="proctor-dot" style="background:{dot_color}"></span>'
        f'{icon} <strong>Proctoring:</strong> {msg}'
        f"</div>",
        unsafe_allow_html=True,
    )

def render_score_cards(report_text: str):
    import re
    total_match = re.search(r"(Overall Score|الدرجة النهائية)[:\s*]+(\d+)\s*/\s*100", report_text)
    tech_match  = re.search(r"(Technical|المعرفة الفنية)[:\s*]+(\d+)\s*/", report_text)
    comm_match  = re.search(r"(Communication|التواصل)[:\s*]+(\d+)\s*/", report_text)
    prob_match  = re.search(r"(Problem Solving|حل المشكلات)[:\s*]+(\d+)\s*/", report_text)
    beh_match   = re.search(r"(Behavioral|السلوك)[:\s*]+(\d+)\s*/", report_text)

    total = total_match.group(2) if total_match else "—"
    tech  = tech_match.group(2)  if tech_match  else "—"
    comm  = comm_match.group(2)  if comm_match  else "—"
    prob  = prob_match.group(2)  if prob_match  else "—"
    beh   = beh_match.group(2)   if beh_match   else "—"

    st.markdown(f"""
    <div class="score-grid">
        <div class="score-card"><div class="score-lbl">{t('lbl_total')}</div><div class="score-val" style="color:#00f2fe">{total}/100</div></div>
        <div class="score-card"><div class="score-lbl">{t('lbl_tech')}</div><div class="score-val">{tech}</div></div>
        <div class="score-card"><div class="score-lbl">{t('lbl_comm')}</div><div class="score-val">{comm}</div></div>
        <div class="score-card"><div class="score-lbl">{t('lbl_prob')}</div><div class="score-val">{prob}</div></div>
        <div class="score-card"><div class="score-lbl">{t('lbl_beh')}</div><div class="score-val">{beh}</div></div>
    </div>
    """, unsafe_allow_html=True)

def render_recommendation(report_text: str):
    rt = report_text.upper()
    if "DO NOT HIRE" in rt or "عدم التوظيف" in report_text or "لا يلبي المعايير" in report_text:
        cls, icon, label = "rgba(255, 75, 75, 0.2)", "🔴", t('rec_no_hire')
    elif "CONSIDER" in rt or "للمراجعة" in report_text or "مقابلة ثانية" in report_text:
        cls, icon, label = "rgba(255, 171, 0, 0.2)", "🟡", t('rec_consider')
    else:
        cls, icon, label = "rgba(0, 255, 136, 0.2)", "🟢", t('rec_hire')
    
    st.markdown(f"""
    <div style="background:{cls}; padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px;">
        <span style="font-size: 1.2rem;">{icon}</span> <strong>Recommendation:</strong> {label}
    </div>
    """, unsafe_allow_html=True)

header_html = f"""
<div style="display: flex; align-items: center; margin-bottom: 25px;">
    <h1 style="margin: 0; font-size: 2rem;">{t('hr_main_title')}</h1>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

db = get_db()
render_steps(db.get("status", "pending"))

tab1, tab2 = st.tabs([f"📋  {t('tab_prepare')}", f"📊  {t('tab_report')}"])

with tab1:
    col1, col2 = st.columns([2, 1], gap="large")
    with col1:
        st.markdown('<div style="font-size:.8rem;color:rgba(255,255,255,.4);letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px;">Question Content</div>', unsafe_allow_html=True)
        new_q = st.text_area(
            label="",
            placeholder=t("q_text"),
            height=130,
            label_visibility="collapsed",
        )
    with col2:
        st.markdown('<div style="font-size:.8rem;color:rgba(255,255,255,.4);letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px;">Target Skill</div>', unsafe_allow_html=True)
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

    if db["questions"]:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:.8rem;color:rgba(255,255,255,.4);letter-spacing:.08em;text-transform:uppercase;margin-bottom:12px;">{len(db["questions"])} Questions Added</div>', unsafe_allow_html=True)
        for i, q in enumerate(db["questions"]):
            st.markdown(f"""
            <div class="glass-card" style="padding: 15px; margin-bottom: 10px;">
               <div style="font-size: 0.7rem; color: #4facfe;">{t('q_word')} {i+1} — {q['skill']}</div>
               <div style="font-size: 1rem; opacity: 0.9;">{q['question']}</div>
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
        st.markdown(f"<div class='glass-card' style='text-align:center; padding: 40px; opacity:0.6;'>{t('no_questions_set')}</div>", unsafe_allow_html=True)

with tab2:
    status = db.get("status", "pending")
    if status in ("pending", "ready_for_candidate"):
        icon  = "⏳" if status == "pending" else "🎙️"
        title = "Waiting for Candidate" if status == "ready_for_candidate" else "Setup in Progress"
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 50px;">
           <div style="font-size: 3rem; margin-bottom: 20px;">{icon}</div>
           <h3>{title}</h3>
           <p style="opacity: 0.7;">{t('wait_candidate')}</p>
        </div>
        """, unsafe_allow_html=True)
    elif status == "completed":
        st.markdown(f"### 🎉 {t('cand_completed')}")
        proctor_chip(db.get("proctor_msg", ""))
        
        if db.get("video_path") and os.path.exists(db["video_path"]):
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
                
                if questions_text_with_answers:
                    db["transcript_blocks"] = transcript_blocks
                    save_db(db)
                    
                    progress.progress(70, text="Running AI deep analysis…")
                    chat_history = build_analysis_prompt(questions_text_with_answers, lang=st.session_state.lang)
                    
                    ai_report = get_ai_response(HF_TOKEN, chat_history)
                    db["analysis_report"] = ai_report
                    db["status"]          = "analyzed"
                    save_db(db)
                    progress.progress(100, text="Done!")
                    st.rerun()
                    
            except Exception as e:
                st.error(f"{t('error_accured')} {e}")

    elif status == "analyzed":
        st.markdown(f"### {t('full_interview')}")
        proctor_chip(db.get("proctor_msg", ""))
        
        with st.expander(f"🎬 {t('watch_interview')}", expanded=False):
            if db.get("video_path") and os.path.exists(db["video_path"]):
                st.video(db["video_path"])
            else:
                st.error(t("video_missing"))
                
        render_score_cards(db["analysis_report"])
        render_recommendation(db["analysis_report"])
        
        with st.expander(f"📝 {t('transcript_title')}", expanded=False):
            blocks = db.get("transcript_blocks", [])
            for blk in blocks:
                st.markdown(f"**Q{blk['index']}: {blk['question']}**")
                st.info(f"\"{blk['answer']}\"")
                st.markdown("---")
        
        st.markdown(f"### 🤖 {t('ai_report_title')}")
        st.markdown(f'<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(db["analysis_report"])
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button(f"🔄  {t('reset_close_btn')}", use_container_width=True, key="reset_btn"):
            db.update({
                "status":             "pending",
                "questions":          [],
                "analysis_report":    "",
                "transcript_blocks":  [],
                "video_path":         None,
                "proctor_msg":        "",
            })
            save_db(db)
            st.rerun()