# tools/vault_retriever.py
from langchain.tools import tool
from .rag_tool import rag_query

@tool
def vault_search(query: str) -> str:
    """Search across Obsidian vaults and Heynote files for the given query using the RAG service."""
    return rag_query(query)
