
from langchain_core.tools import tool
from .rag_service import RAGService
import json

@tool
def rag_query(query: str, filters_json: str = None) -> str:
    """Query the RAG service to get information from the knowledge base.
    Filters can be provided as a JSON string, e.g., '{"file_name": "my_document.pdf"}'
    """
    rag_service = RAGService()
    parsed_filters = None
    if filters_json:
        try:
            parsed_filters = json.loads(filters_json)
        except json.JSONDecodeError:
            return "Invalid filters_json provided. Please provide a valid JSON string."

    query_engine = rag_service.get_query_engine(filters=parsed_filters)
    if query_engine:
        response = query_engine.query(query)
        return str(response)
    else:
        return "RAG service is not available. Please index some documents first."
