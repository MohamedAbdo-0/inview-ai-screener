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
except ImportError as e:
    st.error(f"خطأ في مسار البيئة: {e}")

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

st.set_page_config(page_title="بوابة الشركة (HR)", page_icon="🏢", layout="wide")

st.markdown("""
    <style>
        .block-container { direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, sans-serif; }
        .stButton > button { background-color: #0984e3; color: white; border-radius: 8px; font-weight: bold; }
        .stButton > button:hover { background-color: #74b9ff; }
        .eval-box { background-color: #f1f8ff; border-left: 5px solid #0366d6; border-right: 5px solid #0366d6; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("🏢 بوابة شركة التوظيف (MenaJobs HR)")

db = get_db()
tab1, tab2 = st.tabs(["📝 تجهيز الأسئلة للمرشح", "📊 تقرير نتيجة المقابلة"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        new_q = st.text_area("نص السؤال بصيغة رسمية")
    with col2:
        new_skill = st.text_input("المهارة المستهدفة")
        if st.button("➕ إضافة السؤال للقائمة"):
            if new_q and new_skill:
                db["questions"].append({"question": new_q, "skill": new_skill})
                save_db(db)
                st.success("تم إضافة السؤال بنجاح!")
            else:
                st.error("يرجى تعبئة الحقلين.")
                
    if db["questions"]:
        for i, q in enumerate(db["questions"]):
            st.info(f"**س {i+1}:** {q['question']} *(المهارة: {q['skill']})*")
            
        if st.button("🗑️ حذف جميع الأسئلة"):
            db["questions"] = []
            db["status"] = "pending"
            save_db(db)
            st.rerun()
            
        if st.button("✅ تأكيد وفتح المقابلة للمرشح", type="primary"):
            db["status"] = "ready_for_candidate"
            db["video_path"] = None
            db["analysis_report"] = ""
            save_db(db)
            st.success("تم تأكيد الأسئلة!")

with tab2:
    if db["status"] in ["pending", "ready_for_candidate"]:
        st.warning("⏳ لم يقم المرشح بإجراء المقابلة بعد أو لم يتم اعتماد الأسئلة.")
    elif db["status"] == "completed":
        st.success("🎉 المرشح أتم المقابلة بنجاح!")
        st.markdown(f"**التقرير الأمني للكاميرا:** {db['proctor_msg']}")
        
        st.markdown("### 🎬 تسجيل المقابلة (بامكانك مشاهدته الآن)")
        if db.get("video_path") and os.path.exists(db["video_path"]):
            st.video(db["video_path"])
        else:
            st.warning("Video file missing from server.")
        
        if st.button("🚀 استخراج وتحليل الفيديو وإصدار التقرير النهائي للذكاء الاصطناعي", type="primary", use_container_width=True):
            if not HF_TOKEN:
                st.error("HF_TOKEN غير متوفر.")
                st.stop()
                
            splits = db["splits"]
            vid_path = db["video_path"]
            all_questions = db["questions"]
            
            with st.spinner("🔄 جاري المعالجة..."):
                questions_text_with_answers = ""
                display_transcript_markdown = "### 📝 تفريغ النصوص المقسمة بدقة حسب الأسئلة:\n\n"
                
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
                                transcript_i = "(لم يتحدث المرشح بشيء مسموع في هذا السؤال)"
                        except Exception:
                            transcript_i = "(لم نتمكن من التقاط إجابة دقيقة أو كانت المدة قصيرة جداً)"
                        
                        display_transcript_markdown += f"**السؤال {i+1}: {q['question']}**\n\n> \"{transcript_i}\"\n\n---\n"
                        questions_text_with_answers += f"- السؤال {i+1}: {q['question']} (المهارة: {q['skill']})\n  **النص الحرفي الذي رد به المرشح هنا:** {transcript_i}\n\n"
                        
                        try:
                            os.remove(tmp_audio_path_i)
                        except:
                            pass
                except Exception as e:
                    st.error(f"❌ حدث خطأ: {e}")
                    questions_text_with_answers = None
                    
                if questions_text_with_answers:
                    db["transcript_markdown"] = display_transcript_markdown
                    save_db(db)
                    
                    prompt_content = f"""أنت مدير توظيف آلي وخبير موارد بشرية وتقييم أداء.
الأسئلة التي تم طرحها وإجابة المرشح على كل سؤال بشكل منفصل وموثق:
{questions_text_with_answers}
المطلوب منك كتابة تقرير شامل ومحترف (بالعربية) يشمل:
1. **التحليل الفني والسلوكي لكل سؤال**: قم بذكر رقم السؤال وأعطِ تقييماً تفصيلياً لإجابته وتبريراً منطقياً.
2. **التقييم الشامل**: نقاط القوة الواضحة للمرشح ونقاط الضعف الجوهرية.
3. **القرار النهائي**: النتيجة (مؤهل / غير مؤهل / مراجعة) وتقييم من 10 مع سبب حاسم ومختصر.
رد بتنسيق Markdown احترافي، وامنح المدير تبريرات دقيقة.
"""
                    chat_history = [{"role": "system", "content": "أنت خبير قياس الأداء وتحليل المقابلات الوظيفية باللغة العربية."}, {"role": "user", "content": prompt_content}]
                    try:
                        ai_evaluation = get_ai_response(HF_TOKEN, chat_history)
                        db["analysis_report"] = ai_evaluation
                        db["status"] = "analyzed"
                        save_db(db)
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ من السيرفر: {e}")
                        
    elif db["status"] == "analyzed":
        st.markdown("### 🎬 تسجيل المقابلة الكامل")
        if db.get("video_path") and os.path.exists(db["video_path"]):
            st.video(db["video_path"])
        else:
            st.error("لم يتم العثور على ملف الفيديو في الخادم.")
            
        st.markdown(db["transcript_markdown"])
        st.markdown("<div class='eval-box'>", unsafe_allow_html=True)
        st.markdown("## 🎯 التقرير الاستشاري الدقيق للذكاء الاصطناعي")
        st.markdown(db["analysis_report"])
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("إعادة ضبط وإغلاق الملف الحالي"):
            db["status"] = "pending"
            db["questions"] = []
            db["analysis_report"] = ""
            db["transcript_markdown"] = ""
            save_db(db)
            st.rerun()
