from langchain_openai import ChatOpenAI

def get_llm():
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
