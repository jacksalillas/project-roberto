
import json
from langchain_core.tools import tool

@tool
def web_search(query: str) -> str:
    """Search the web for information on a given query and return the content and source URLs."""
    search_results = google_web_search(query=query)
    
    # Assuming google_web_search returns a dictionary with a 'results' key,
    # where each result has 'url' and 'snippet'/'content'
    content = ""
    sources = []
    
    if search_results and 'results' in search_results:
        for result in search_results['results']:
            if 'snippet' in result:
                content += result['snippet'] + "\n"
            elif 'content' in result: # Fallback for 'content' if 'snippet' is not present
                content += result['content'] + "\n"
            if 'url' in result:
                sources.append(result['url'])
    
    # Return a JSON string containing both content and sources
    return json.dumps({"content": content.strip(), "sources": sources})
