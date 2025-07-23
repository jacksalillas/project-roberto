from langchain_core.tools import tool
from datetime import datetime

@tool
def get_local_time() -> str:
    """Returns the current local system time as a string. Use this tool when you need to know the current time, for example, to answer questions about what time it is now, or to provide a timestamp for an event."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
