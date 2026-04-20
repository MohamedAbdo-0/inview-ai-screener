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
HR_CSS = 
st.markdown(HR_CSS, unsafe_allow_html=True)
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
    dot_color = "
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
    lbl_tech = t('lbl_tech') if t('lbl_tech') != 'lbl_tech' else "Technical"
    lbl_comm = t('lbl_comm') if t('lbl_comm') != 'lbl_comm' else "Communication"
    lbl_prob = t('lbl_prob') if t('lbl_prob') != 'lbl_prob' else "Problem Solving"
    lbl_beh  = t('lbl_beh')  if t('lbl_beh') != 'lbl_beh'  else "Behavioral"
    lbl_total = t('lbl_total') if t('lbl_total') != 'lbl_total' else "Overall Score"
    st.markdown(f, unsafe_allow_html=True)
def render_recommendation(report_text: str):
    rt = report_text.upper()
    if "DO NOT HIRE" in rt or "عدم التوظيف" in report_text:
        cls, icon, label = "rec-no-hire", "🔴", t('rec_no_hire') if t('rec_no_hire') != 'rec_no_hire' else "DO NOT HIRE"
    elif "CONSIDER" in rt or "للمراجعة" in report_text:
        cls, icon, label = "rec-consider", "🟡", t('rec_consider') if t('rec_consider') != 'rec_consider' else "CONSIDER — Second Interview Recommended"
    else:
        cls, icon, label = "rec-hire", "🟢", t('rec_hire') if t('rec_hire') != 'rec_hire' else "HIRE — Recommended to Proceed"
    st.markdown(f, unsafe_allow_html=True)
st.markdown(f, unsafe_allow_html=True)
db = get_db()
render_steps(db.get("status", "pending"))
tab1, tab2 = st.tabs([f"📋  {t('tab_prepare')}", f"📊  {t('tab_report')}"])
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
    if db["questions"]:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:.8rem;color:rgba(255,255,255,.4);letter-spacing:.08em;text-transform:uppercase;margin-bottom:12px;">{len(db["questions"])} Questions Added</div>', unsafe_allow_html=True)
        for i, q in enumerate(db["questions"]):
            st.markdown(f, unsafe_allow_html=True)
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
        st.markdown(, unsafe_allow_html=True)
with tab2:
    status = db.get("status", "pending")
    if status in ("pending", "ready_for_candidate"):
        icon  = "⏳" if status == "pending" else "🎙️"
        title = "Setup in Progress" if status == "pending" else "Waiting for Candidate"
        body  = "Add and confirm interview questions first." if status == "pending" else "The interview session is open. Waiting for the candidate to complete it."
        st.markdown(f, unsafe_allow_html=True)
    elif status == "completed":
        st.markdown(, unsafe_allow_html=True)
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
                transcript_md = "
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
    elif status == "analyzed":
        st.markdown(, unsafe_allow_html=True)
        proctor_chip(db.get("proctor_msg", ""))
        with st.expander("🎬 Interview Recording", expanded=False):
            if db.get("video_path") and os.path.exists(db["video_path"]):
                st.video(db["video_path"])
            else:
                st.error(t("video_missing"))
        render_score_cards(db["analysis_report"])
        render_recommendation(db["analysis_report"])
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        with st.expander("📝 Interview Transcript", expanded=False):
            blocks = db.get("transcript_blocks", [])
            if blocks:
                html = '<div class="transcript-wrap"><div class="transcript-title">🗒️ Full Transcript</div>'
                for blk in blocks:
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
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="eval-section">', unsafe_allow_html=True)
        st.markdown(db["analysis_report"])
        st.markdown("</div>", unsafe_allow_html=True)
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