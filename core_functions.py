# Inview AI Screener — Core Functions
import cv2
from huggingface_hub import InferenceClient
import time
import subprocess
import sys


# ── SPEECH TO TEXT ────────────────────────────────────────────────────────────
def transcribe_audio(audio_file_path: str, hf_token: str) -> str:
    client = InferenceClient(token=hf_token)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            result = client.automatic_speech_recognition(
                audio_file_path,
                model="openai/whisper-large-v3-turbo"
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
            raise ValueError(f"Connection failed: {e}")


# ── AI CHAT ───────────────────────────────────────────────────────────────────
def get_ai_response(hf_token: str, chat_history: list) -> str:
    client = InferenceClient(token=hf_token)
    model = "Qwen/Qwen2.5-7B-Instruct"
    response = client.chat_completion(
        model=model,
        messages=chat_history,
        max_tokens=3500,
    )
    return response.choices[0].message.content


# ── TEXT TO SPEECH ────────────────────────────────────────────────────────────
def generate_speech(text: str, output_path: str = "ai_response.mp3", lang: str = "ar"):
    voice = "ar-SA-HamedNeural" if lang == "ar" else "en-US-AriaNeural"
    command = (
        f'"{sys.executable}" -m edge_tts '
        f'--voice "{voice}" --text "{text}" --write-media "{output_path}"'
    )
    subprocess.run(command, shell=True, check=True)
    return output_path


# ── FACE DETECTION ────────────────────────────────────────────────────────────
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


# ── DEEP ANALYSIS PROMPT BUILDER ─────────────────────────────────────────────
def build_analysis_prompt(questions_text: str, lang: str = "en") -> list:
    """
    Returns a chat_history (system + user) for a detailed, structured
    AI evaluation of a candidate's interview answers.
    """

    system_prompt = """You are an expert Senior HR Analyst and Organizational Psychologist 
with 15+ years of experience evaluating candidates across technical and behavioral interviews.

Your role is to provide an OBJECTIVE, DETAILED, and STRUCTURED evaluation report.
You must be precise, evidence-based, and reference specific parts of the candidate's answers.
Always maintain a professional and constructive tone.

Output ONLY valid Markdown — no JSON, no code blocks, no preamble."""

    user_prompt = f"""Analyze the following interview transcript and produce a **comprehensive candidate evaluation report**.

---
{questions_text}
---

## Report Structure (follow exactly):

---

# 🧠 Candidate Evaluation Report

## 1. Executive Summary
Write 3–4 sentences summarizing the candidate's overall performance, standout qualities, and key concerns.

---

## 2. Per-Question Breakdown

For **each question**, provide:
- **Question:** (restate briefly)
- **Answer Quality:** (Excellent / Good / Average / Weak)
- **Score:** X / 10
- **Analysis:** 2–3 sentences on depth, clarity, and relevance of the answer.
- **Key Strengths in this answer:** (bullet points)
- **Gaps or Missed Points:** (bullet points)

---

## 3. Competency Assessment

Rate each competency from 1–10 with a short justification:

| Competency | Score | Justification |
|---|---|---|
| Technical Knowledge | X/10 | ... |
| Problem-Solving Ability | X/10 | ... |
| Communication & Clarity | X/10 | ... |
| Critical Thinking | X/10 | ... |
| Confidence & Delivery | X/10 | ... |
| Depth of Experience | X/10 | ... |

---

## 4. Strengths & Highlights
List the top 3–5 genuine strengths demonstrated across the interview, with evidence from the answers.

---

## 5. Areas for Development
List 3–5 specific gaps or weaknesses, with actionable suggestions for improvement.

---

## 6. Cultural & Behavioral Fit Signals
Based on the answers, identify any signals about the candidate's work style, teamwork orientation, adaptability, or potential red flags.

---

## 7. Overall Score
**Total Score: XX / 100**

Provide a breakdown:
- Technical Score: X/40
- Communication Score: X/20
- Problem Solving Score: X/20
- Behavioral Score: X/20

---

## 8. Final Recommendation

Choose one:
> 🟢 **HIRE** — Strong candidate, recommend moving forward.
> 🟡 **CONSIDER** — Promising but requires a second interview or specific assessment.
> 🔴 **DO NOT HIRE** — Does not meet the required standards at this time.

**Reasoning:** (2–3 sentences explaining the decision based on the evidence above.)

---
"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": user_prompt},
    ]
