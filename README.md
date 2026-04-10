## 🌟 1. System Overview & Complete Workflow
The **MenaJobs AI Screener** project is an interactive, End-to-End AI-powered recruitment platform constructed purely in Python. It completely automates the screening phase by having an AI act as an HR interviewer, conducting a Zoom-like video session with the candidate, recording their responses continuously, and finally applying deep semantic inference to generate an analytical hiring report.

**📌 The Architectural Workflow:**
1. **Criteria Input (HR Portal):** The HR professional accesses the portal, entering the precise questions alongside the target skills they wish to test.
2. **Interview Simulation (Candidate Room):** The candidate opens their link, and the browser initiates a secure WebRTC session. The AI poses the questions out loud via a professional synthesized male Arabic voice, waiting sequentially for the user's responses while recording a continuous WebM video chunk.
3. **Data Decoding & Timetracking:** Upon completion, the massive WebM blob alongside a highly precise array of JS-collected timestamps (measuring exact sub-second click offsets) is transferred to the server.
4. **AI Inference & Extraction:** The system natively slices the video based on the timestamps to segregate isolated speech segments, transcribes the segments, and channels them through to a generative LLM for qualitative candidate analysis.

---

## 🔬 2. Advanced Algorithmic Details (Data Science & AI Perspective)
This project is deeply rooted in 4 major pillars of modern AI and Data Engineering:

### A. Speech Signal Processing (ASR & TTS)
* **Text-to-Speech (TTS):** Employing `Edge-TTS` via the `ar-SA-HamedNeural` model to dynamically synthesize a hyper-realistic, authoritative male Arabic voice for dictating questions to the candidate in real-time.
* **Automatic Speech Recognition (ASR):** Full reliance on the bleeding-edge `Whisper-Large-v3-Turbo` model provided via HuggingFace Hub for zero-shot acoustic decoding. Handling the chaotic nature of networking, a custom backoff/retry algorithm guarantees the connection persists even if micro-interruptions occur during large file transmissions.

### B. NLP & Prompt Engineering (Semantic Processing)
* Powered by `Qwen 2.5 - 7B`, an open-weights massive language model fine-tuned for instructional alignment.
* The model evaluates the candidate conceptually rather than relying on brittle Keyword-matching. It dictates a 3-part framework forced upon the model through strict engineering:
  1. Deep Technical/Behavioral analysis per individual question correlating exactly to the candidate's transcribed words.
  2. Holistic Extraction identifying overall operational strengths and weaknesses.
  3. Absolute quantitative scoring (Out of 10 ratings) terminating with a Final Output classification (Qualified, Under Review, Disqualified).

### C. Computer Vision & Automated Proctoring (Security)
* Leveraging classical Machine Learning Object Detection via `OpenCV` logic (Haar Cascade Classifiers).
* Processing raw captured video frames algorithmically (scaling via `scaleFactor=1.3`, smoothing via Grayscale transformations) to detect human faces. It enacts an automated red-flag rule: 0 faces detected implies avoidance, while >1 face implies external cheating interference.

### D. Data Pipelines & Native Media Slicing
* Integrating an intelligent Frontend event listener utilizing `Date.now()` to construct a floating timestamps array mapping explicitly when candidates shift from one question context to the other.
* Over on the Backend, an `FFMPEG` pipeline parses this array, issuing precise `-ss` (start) and `-t` (duration) byte-extraction commands to natively slice the continuous WebM file into purely isolated micro-audio bursts, guaranteeing zero NLP semantic overlapping during evaluation.

---

## 📂 3. Exact File Structure & Functional Breakdown (File Tree)

The repository constitutes 10 robust files operating in complete concert:

### ⚙️ Part One: The Logical AI Core Framework
**1. `core_functions.py` (The Mastermind)**
* **Content:** Primary ML wrappers.
* **Deep Mechanics:** All pure algorithmic logic exists here, decoupled from GUI representation. It runs `transcribe_audio` alongside API resilience mechanisms, pushes prompts through `get_ai_response` leveraging up to 2048 response tokens, and triggers the `check_face_presence` CV function.

**2. `db_manager.py` (State Management DB)**
* **Content:** Persistent State layer handler bridging the disjoint systems.
* **Deep Mechanics:** Using `database.json`, it implements classic JSON CRUD endpoints tracking the interview's lifecycle state (pending -> ready_for_candidate -> completed -> analyzed) preventing UI state-loss upon browser refreshes.

---

### 🌐 Part Two: User GUI Portals
**3. `app.py` (Main Gateway)**
* **Content:** Minimalist Landing Router.
* **Deep Mechanics:** Employs clean Streamlit layout cards dynamically routing the incoming user flow explicitly to either the Administrative domain or the Candidate domain.

**4. `pages/1_hr_portal.py` (Command & Control Center)**
* **Content:** The corporate multi-tab dashboard.
* **Deep Mechanics:** This file is visually driven but handles massive background compute. Depending on DB triggers, it iterates the FFMPEG commands for segmentation, instantiates explicit native `st.video()` handlers dynamically passing the recorded video URL back to the HR manager, and assembles the massive Markdown AI result strings.

**5. `pages/2_candidate_portal.py` (The Live Session Engine)**
* **Content:** The isolated UX for the applicant.
* **Deep Mechanics:** Programmatically compiles localized arrays of Base64 MP3 tracks (generated via TTS in real-time) prior to starting, loading them securely into the HTML component ensuring immediate audio playback synchronously with the JavaScript UI states.

---

### 🎥 Part Three: Custom Embedded Component
**6. `video_recorder/index.html` (The Undetectable Media Engine)**
* **Content:** The raw Javascript GUI element injected directly into Streamlit via iFrame.
* **Deep Mechanics:** Uses native browser elements (MediaRecorder API) capturing chunked blobs. The custom JS logic tracks `[0, x, y, z]` timing arrays based purely on UI `onclick` bounds, eventually emitting an integrated JSON object back to the parent container hosting Python execution lines.

**7. `video_recorder/__init__.py`**
* **Content:** Streamlit Component Declarator.
* **Deep Mechanics:** A python layer declaring the frontend components existence to the Streamlit execution tree permitting Python to invoke Javascript while supplying JSON arguments.

---

### 📦 Part Four: Environmental Infrastructure
**8. `requirements.txt`:** The dependency map outlining the Python environment architecture (OpenCV, Pydub, Streamlit, HuggingFace, etc) to ensure fault-tolerance during server setup deployment.
**9. `.env`:** Local hidden file storing environment-specific variables namely the API `HF_TOKEN` safeguarding account permissions.
**10. `start.py`:** The specialized `asyncio.ProactorEventLoop` driver. Formulated explicitly so Python 3.14 Windows instances can maintain endless runtime Streamlit event-loops without experiencing hard asynchronous crashes.
