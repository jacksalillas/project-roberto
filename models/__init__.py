from .ollama_model import get_llm as get_ollama_llm
from .openai_model import get_llm as get_openai_llm
from .gemini_model import get_llm as get_gemini_llm

def get_model(name: str):
    if name == "ollama":
        return get_ollama_llm()
    elif name == "openai":
        return get_openai_llm()
    elif name == "gemini":
        return get_gemini_llm()
    else:
        raise ValueError(f"Unknown model: {name}")
