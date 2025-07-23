from langchain.tools import tool

@tool
def refactor_code(code: str) -> str:
    """Improve or refactor Python or Bash code passed in as a string."""
    # LLM handles logic; just structure input/output.
    return f"Please improve this code:\n\n{code}"
