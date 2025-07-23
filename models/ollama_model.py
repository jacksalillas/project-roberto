# models/ollama_model.py
from langchain_ollama import ChatOllama  # ✅ new package

def get_llm():
    return ChatOllama(model="mistral", temperature=0.4)
