import asyncio
import sys
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
    sys.argv = ["streamlit", "run", "Inview.py"]
    sys.exit(cli.main())