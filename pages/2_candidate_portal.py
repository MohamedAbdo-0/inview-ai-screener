import streamlit as st
import cv2
import os
import sys
import base64
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from db_manager import get_db, save_db
    import core_functions
    import importlib
    importlib.reload(core_functions)
    from core_functions import check_face_presence, generate_speech
    import video_recorder
    importlib.reload(video_recorder)
    from video_recorder import st_video_recorder
    from i18n import t, get_base_css, select_language, get_lang
except ImportError as e:
    st.error(f"خطأ في مسار البيئة: {e}")

st.set_page_config(page_title="Candidate Portal", page_icon="🎥", layout="wide")

select_language()

st.markdown(get_base_css(), unsafe_allow_html=True)
st.markdown("""
    <style>
        h2 { color: #2e6c80; text-align: center; font-weight: 800;}
    </style>
""", unsafe_allow_html=True)

st.title(t("cand_main_title"))

db = get_db()

if db["status"] != "ready_for_candidate":
    st.warning(t("no_interview_active"))
    st.stop()

if not db["questions"]:
    st.error(t("no_questions_set"))
    st.stop()

audio_list_b64 = []
quests_list = []

with st.spinner(t("building_meeting")):
    for i, q in enumerate(db["questions"]):
        audio_path = f"ai_question_audio_{i}.mp3"
        generate_speech(q['question'], audio_path, get_lang())
        with open(audio_path, "rb") as f:
            b64_audio = base64.b64encode(f.read()).decode("utf-8")
        audio_list_b64.append(f"data:audio/mp3;base64,{b64_audio}")
        quests_list.append(q['question'])

q_json = json.dumps(quests_list)
au_json = json.dumps(audio_list_b64)

result = st_video_recorder(questions_json=q_json, audios_json=au_json, key="candidate_zoom_live_call")

if result:
    st.success(t("interview_sent"))
    try:
        mime, b64 = result["video"].split(",", 1)
        video_bytes = base64.b64decode(b64)
        splits = result.get("splits", [])
        
        is_safe = False
        proctor_msg = t("no_face_proctor")
        
        vid_save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'candidate_video.webm'))
        with open(vid_save_path, "wb") as f_vid:
            f_vid.write(video_bytes)
            
        cap = cv2.VideoCapture(vid_save_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 5)
        ret, frame = cap.read()
        cap.release()
        if ret:
            is_safe, proctor_msg = check_face_presence(frame, get_lang())

        db["status"] = "completed"
        db["video_path"] = vid_save_path
        db["splits"] = splits
        db["proctor_safe"] = is_safe
        db["proctor_msg"] = proctor_msg
        save_db(db)

    except Exception as e:
        st.error(f"{t('unexpected_err')} {e}")

