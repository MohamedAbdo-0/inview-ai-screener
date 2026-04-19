# Inview AI Screener - Video Recorder Component
import os
import streamlit.components.v1 as components

frontend_dir = os.path.dirname(__file__)

_video_recorder = components.declare_component(
    "video_recorder",
    path=frontend_dir
)

def st_video_recorder(questions_json="[]", audios_json="[]", key=None):
    component_value = _video_recorder(
        questions=questions_json,
        audios=audios_json,
        key=key,
        default=None
    )
    return component_value
