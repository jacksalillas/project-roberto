
from langchain_core.tools import tool
@tool
def web_search(query: str) -> str:
    """Search the web for information on a given query."""
    # The google_web_search function is provided by the environment
    return google_web_search(query=query)
