import json
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "database.json")

def init_db():
    if not os.path.exists(DB_FILE):
        db = {
            "questions": [],
            "status": "pending",
            "video_path": None,
            "splits": [],
            "proctor_safe": False,
            "proctor_msg": "",
            "analysis_report": "",
            "transcript_markdown": ""
        }
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=4)

def get_db():
    init_db()
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
