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
except ImportError as e:
    st.error(f"خطأ في مسار البيئة: {e}")

st.set_page_config(page_title="المقابلة الحية للمرشح", page_icon="🎥", layout="wide")

st.markdown("""
    <style>
        .block-container { direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, sans-serif; }
        h2 { color: #2e6c80; text-align: center; font-weight: 800;}
    </style>
""", unsafe_allow_html=True)

st.title("🎥 غرفة المقابلة الحية (Candidate Portal)")

db = get_db()

if db["status"] != "ready_for_candidate":
    st.warning("⚠️ لا توجد مقابلة مفعلة حالياً. الرجاء مراجعة الموارد البشرية.")
    st.stop()

if not db["questions"]:
    st.error("⚠️ لم يتم تعيين أسئلة للمقابلة.")
    st.stop()

audio_list_b64 = []
quests_list = []

with st.spinner("🤖 جاري بناء الميتنج..."):
    for i, q in enumerate(db["questions"]):
        audio_path = f"ai_question_audio_{i}.mp3"
        generate_speech(q['question'], audio_path)
        with open(audio_path, "rb") as f:
            b64_audio = base64.b64encode(f.read()).decode("utf-8")
        audio_list_b64.append(f"data:audio/mp3;base64,{b64_audio}")
        quests_list.append(q['question'])

q_json = json.dumps(quests_list)
au_json = json.dumps(audio_list_b64)

result = st_video_recorder(questions_json=q_json, audios_json=au_json, key="candidate_zoom_live_call")

if result:
    st.success("✅ تم إرسال تسجيل المكالمة للشركة بنجاح. يمكنك إغلاق الصفحة الآن.")
    try:
        mime, b64 = result["video"].split(",", 1)
        video_bytes = base64.b64decode(b64)
        splits = result.get("splits", [])
        
        is_safe = False
        proctor_msg = "لم نتمكن من التقاط صورة الفحص"
        
        vid_save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'candidate_video.webm'))
        with open(vid_save_path, "wb") as f_vid:
            f_vid.write(video_bytes)
            
        cap = cv2.VideoCapture(vid_save_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 5)
        ret, frame = cap.read()
        cap.release()
        if ret:
            is_safe, proctor_msg = check_face_presence(frame)

        db["status"] = "completed"
        db["video_path"] = vid_save_path
        db["splits"] = splits
        db["proctor_safe"] = is_safe
        db["proctor_msg"] = proctor_msg
        save_db(db)

    except Exception as e:
        st.error(f"خطأ غير متوقع أثناء المعالجة: {e}")
