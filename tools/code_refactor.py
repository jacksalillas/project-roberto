# tools/code_refactor.py

from langchain.tools import tool

@tool
def refactor_code(code_snippet: str) -> str:
    """Refactors a given code snippet for readability and performance."""
    # Dummy implementation (LLM will do the reasoning in context)
    return f"Refactored version of your code:\n\n{code_snippet}"
