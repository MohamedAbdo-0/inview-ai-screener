import cv2
from huggingface_hub import InferenceClient
import time
import subprocess
import sys
def transcribe_audio(audio_file_path: str, hf_token: str, lang: str = "ar") -> str:
    client = InferenceClient(token=hf_token)
    max_retries = 3
    model_id = "openai/whisper-large-v3" 
    for attempt in range(max_retries):
        try:
            result = client.automatic_speech_recognition(
                audio_file_path,
                model=model_id,
            )
            if isinstance(result, dict) and "text" in result:
                return result["text"]
            elif hasattr(result, "text"):
                return result.text
            return str(result)
        except Exception as e:
            if "IncompleteRead" in str(e) or attempt < max_retries - 1:
                time.sleep(2)
                continue
            try:
                result = client.automatic_speech_recognition(
                    audio_file_path,
                    model="openai/whisper-large-v3-turbo",
                )
                return result["text"] if isinstance(result, dict) else str(result)
            except:
                raise ValueError(f"Connection failed: {e}")
def get_ai_response(hf_token: str, chat_history: list) -> str:
    client = InferenceClient(token=hf_token)
    model = "Qwen/Qwen2.5-7B-Instruct"
    response = client.chat_completion(
        model=model,
        messages=chat_history,
        max_tokens=3500,
    )
    return response.choices[0].message.content
def generate_speech(text: str, output_path: str = "ai_response.mp3", lang: str = "ar"):
    voice = "ar-SA-HamedNeural" if lang == "ar" else "en-US-AriaNeural"
    command = (
        f'"{sys.executable}" -m edge_tts '
        f'--voice "{voice}" --text "{text}" --write-media "{output_path}"'
    )
    subprocess.run(command, shell=True, check=True)
    return output_path
def check_face_presence(frame, lang: str = "ar"):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    if lang == "ar":
        msg_no_face    = "تحذير: لا يوجد مرشح أمام الكاميرا."
        msg_multi_face = "تحذير أمني: تم رصد أكثر من شخص أمام الكاميرا."
        msg_safe       = "الوضع البصري آمن."
    else:
        try:
            from i18n import translations
            msg_no_face    = translations["en"]["warn_no_face"]
            msg_multi_face = translations["en"]["warn_multi_face"]
            msg_safe       = translations["en"]["safe_face"]
        except Exception:
            msg_no_face    = "Warning: No candidate detected in frame."
            msg_multi_face = "Security Warning: Multiple faces detected."
            msg_safe       = "Visual status: clear."
    if len(faces) == 0:
        return False, msg_no_face
    elif len(faces) > 1:
        return False, msg_multi_face
    return True, msg_safe
def build_analysis_prompt(questions_text: str, lang: str = "en") -> list:
    if lang == "ar":
        system_prompt = 
        user_prompt = f
    else:
        system_prompt = 
        user_prompt = f
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": user_prompt},
    ]