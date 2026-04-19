# Inview AI Screener
import asyncio
import sys

# ترقيع (Monkey-patch) لدالة asyncio لتتوافق بشكل إجباري مع إعدادات بايثون 3.14
# لأن مكتبة Streamlit تستدعيها بطريقة قديمة 
_old_get_event_loop = asyncio.get_event_loop

def safe_get_event_loop():
    try:
        return _old_get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop

asyncio.get_event_loop = safe_get_event_loop

from streamlit.web import cli

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(cli.main())
