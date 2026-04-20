# 🚀 Inview AI Screener - Technical Documentation

**Inview AI Screener** is an advanced, interactive, End-to-End AI-powered recruitment platform built entirely with Python. It automates the initial screening phase by acting as an intelligent HR interviewer that conducts a live video session, records responses, and generates deep analytical hiring reports.

---

## 🌟 1. System Overview & Workflow
The platform utilizes a modern, decentralized architecture connecting high-performance AI models:

1. **Setup Phase (HR Portal):** Recruiters input questions and link them to specific skills or competencies.
2. **Interview Engine (Candidate Room):** A premium, glassmorphism-styled environment where the AI poses questions using neural TTS (Arabic/English). The browser records a continuous video stream.
3. **Data Pipeline:** Upon submission, the video and a precise "timestamp array" (capturing sub-second question transitions) are sent to the backend.
4. **AI Processing Room:** The system uses `FFMPEG` for native media slicing, `Whisper-v3` for high-fidelity transcription, and `Qwen 2.5` for multi-dimensional candidate evaluation.

---

## 🔬 2. Advanced AI Pillars (Data Science Perspective)

### A. Speech & Audio Processing (ASR & TTS)
* **Neural TTS:** Leveraging `Edge-TTS` with high-quality voices (Hamed for Arabic, Aria for English) to ensure a natural, non-robotic interview experience.
* **Whisper-Large-v3:** The state-of-the-art ASR model is used for decoding speech. We implemented a robust failover system that switches between full and turbo models to guarantee transcription reliability.

### B. NLP & Prompt Engineering
* Powered by `Qwen 2.5 - 7B`, the AI provides professional HR-grade reports.
* **Bilingual Analysis:** The system automatically identifies the UI language and instructs the AI to generate the report in the matching language (Arabic or English).
* **Detailed Scoring:** Candidates are scored across Technical, Communication, Problem Solving, and Behavioral metrics.

### C. Computer Vision (AI Proctoring)
* **Security Layer:** Using `OpenCV` (Haar Cascades) to monitor the video stream frame-by-frame for candidate presence. It flags anomalies like "No face detected" or "Multiple people detected" to the recruiter.

### D. Native Media Engineering
* To ensure zero-overlap in transcription, the system performs "At-Source Slicing" using FFMPEG, extracting isolated audio segments for each question based on the candidate's actual interaction speed.

---

## 📂 3. Software Architecture (File Breakdown)

1. **`app.py`**: The main entry point featuring the premium redesigned Glassmorphism UI.
2. **`core_functions.py`**: The logical kernel housing ML wrappers (ASR, LLM, Computer Vision).
3. **`i18n.py`**: The internationalization backbone managing bilingual state and dynamic RTL/LTR styling.
4. **`db_manager.py`**: Lightweight JSON database handler to manage interview states and persistence.
5. **`pages/`**: Contains the split logic for the HR Dashboard and the Candidate Session Room.
6. **`video_recorder/`**: Custom Streamlit Component (JS/HTML/CSS) managing the MediaRecorder API and timestamp tracking.

---

## 🚀 4. Installation & Setup
1. Clone the repo and install dependencies: `pip install -r requirements.txt`
2. Configure environment: Add your `HF_TOKEN` to the `.env` file.
3. Run the application: `python start.py`

---
> Built for the future of talent acquisition, Inview combines visual elegance with industrial-grade AI performance.
