# Inview AI Screener
import streamlit as st
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from db_manager import get_db, save_db
    import core_functions
    import importlib
    importlib.reload(core_functions)
    from core_functions import transcribe_audio, get_ai_response
    from i18n import t, get_base_css, select_language
except ImportError as e:
    st.error(f"خطأ في مسار البيئة: {e}")

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

st.set_page_config(page_title="Inview HR Portal", page_icon="🏢", layout="wide")

select_language()

st.markdown(get_base_css(), unsafe_allow_html=True)
st.markdown("""
    <style>
        .stButton > button { background-color: #0984e3; color: white; border-radius: 8px; font-weight: bold; }
        .stButton > button:hover { background-color: #74b9ff; }
        .eval-box { background-color: #f1f8ff; border-left: 5px solid #0366d6; border-right: 5px solid #0366d6; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title(t("hr_main_title"))

db = get_db()
tab1, tab2 = st.tabs([t("tab_prepare"), t("tab_report")])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        new_q = st.text_area(t("q_text"))
    with col2:
        new_skill = st.text_input(t("q_skill"))
        if st.button(t("add_q_btn")):
            if new_q and new_skill:
                db["questions"].append({"question": new_q, "skill": new_skill})
                save_db(db)
                st.success(t("q_added_success"))
            else:
                st.error(t("fill_fields_err"))
                
    if db["questions"]:
        for i, q in enumerate(db["questions"]):
            st.info(f"**{t('q_word')} {i+1}:** {q['question']} *({t('skill_word')}: {q['skill']})*")
            
        if st.button(t("delete_all_q_btn")):
            db["questions"] = []
            db["status"] = "pending"
            save_db(db)
            st.rerun()
            
        if st.button(t("confirm_open_interview_btn"), type="primary"):
            db["status"] = "ready_for_candidate"
            db["video_path"] = None
            db["analysis_report"] = ""
            save_db(db)
            st.success(t("questions_confirmed"))

with tab2:
    if db["status"] in ["pending", "ready_for_candidate"]:
        st.warning(t("wait_candidate"))
    elif db["status"] == "completed":
        st.success(t("cand_completed"))
        st.markdown(f"{t('proctor_report')} {db['proctor_msg']}")
        
        st.markdown(t("watch_interview"))
        if db.get("video_path") and os.path.exists(db["video_path"]):
            st.video(db["video_path"])
        else:
            st.warning(t("video_missing"))
        
        if st.button(t("extract_analyze_btn"), type="primary", use_container_width=True):
            if not HF_TOKEN:
                st.error(t("hf_token_err"))
                st.stop()
                
            splits = db["splits"]
            vid_path = db["video_path"]
            all_questions = db["questions"]
            
            with st.spinner(t("processing")):
                questions_text_with_answers = ""
                display_transcript_markdown = t("transcript_title")
                
                try:
                    import imageio_ffmpeg
                    import subprocess
                    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
                    
                    for i, q in enumerate(all_questions):
                        start_time = float(splits[i])
                        end_time = float(splits[i+1])
                        duration = max(0.1, end_time - start_time)
                        tmp_audio_path_i = f"temp_audio_{i}.wav"
                        
                        subprocess.run([ffmpeg_exe, "-i", vid_path, "-ss", str(start_time), "-t", str(duration), "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", tmp_audio_path_i, "-y"], check=True, capture_output=True)
                        
                        try:
                            transcript_i = transcribe_audio(tmp_audio_path_i, HF_TOKEN)
                            if not transcript_i or transcript_i.strip() == "":
                                transcript_i = t("no_speech")
                        except Exception:
                            transcript_i = t("short_ans_err")
                        
                        display_transcript_markdown += f"**{t('question_word')} {i+1}: {q['question']}**\n\n> \"{transcript_i}\"\n\n---\n"
                        questions_text_with_answers += f"- {t('question_word')} {i+1}: {q['question']} ({t('skill_word')}: {q['skill']})\n  **{t('literal_text')}** {transcript_i}\n\n"
                        
                        try:
                            os.remove(tmp_audio_path_i)
                        except:
                            pass
                except Exception as e:
                    st.error(f"{t('error_accured')} {e}")
                    questions_text_with_answers = None
                    
                if questions_text_with_answers:
                    db["transcript_markdown"] = display_transcript_markdown
                    save_db(db)
                    
                    prompt_content = t("ai_prompt").format(text=questions_text_with_answers)
                    chat_history = [{"role": "system", "content": t("ai_sys_prompt")}, {"role": "user", "content": prompt_content}]
                    try:
                        ai_evaluation = get_ai_response(HF_TOKEN, chat_history)
                        db["analysis_report"] = ai_evaluation
                        db["status"] = "analyzed"
                        save_db(db)
                        st.rerun()
                    except Exception as e:
                        st.error(f"{t('server_error')} {e}")
                        
    elif db["status"] == "analyzed":
        st.markdown(t("full_interview"))
        if db.get("video_path") and os.path.exists(db["video_path"]):
            st.video(db["video_path"])
        else:
            st.error(t("video_missing"))
            
        st.markdown(db["transcript_markdown"])
        st.markdown("<div class='eval-box'>", unsafe_allow_html=True)
        st.markdown(t("ai_report_title"))
        st.markdown(db["analysis_report"])
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button(t("reset_close_btn")):
            db["status"] = "pending"
            db["questions"] = []
            db["analysis_report"] = ""
            db["transcript_markdown"] = ""
            save_db(db)
            st.rerun()

