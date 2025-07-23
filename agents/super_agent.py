# agents/super_agent.py

from langchain_core.runnables import Runnable
from langchain_core.tools import Tool
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

from pydantic import BaseModel
from typing import Optional

# === Import your LLM and tools ===
from models import get_model
from tools.todo_writer import todo_tool
from tools.note_writer import note_tool
from tools.vault_retriever import vault_search

# === LangGraph state schema ===
class AgentState(BaseModel):
    input: str
    output: Optional[str] = None

# === Tool definitions ===
tools = [
    todo_tool,
    note_tool,
    vault_search,
]

# === Build LangGraph ReAct agent ===
def get_super_agent(llm: Runnable) -> Runnable:
    """Construct a LangGraph ReAct agent with your tools"""
    agent_node = create_react_agent(llm, tools)

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    workflow.set_entry_point("agent")
    workflow.set_finish_point("agent")

    app = workflow.compile()
    return app
