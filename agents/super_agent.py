
from langchain_core.runnables import Runnable
from langchain_core.tools import Tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, BaseMessage
from typing import TypedDict, Annotated, Sequence
import operator

# === Import your LLM and tools ===
from models import get_model
from tools.todo_writer import todo_tool
from tools.note_writer import note_tool
from tools.vault_retriever import vault_search
from tools.rag_tool import rag_query
from tools.web_search_tool import web_search
from tools.code_tools import read_code_file, write_code_file, execute_code, refactor_code

# === LangGraph state schema ===
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

# === Tool definitions ===
tools = [
    todo_tool,
    note_tool,
    vault_search,
    rag_query,
    web_search,
    read_code_file,
    write_code_file,
    execute_code,
    refactor_code,
]

tool_node = ToolNode(tools)

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# === Build LangGraph ReAct agent ===
def get_super_agent(llm: Runnable) -> Runnable:
    """Construct a LangGraph ReAct agent with your tools"""

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful AI assistant named Roberto. You are an expert in software development, but you are also a generalist who can help with a wide variety of tasks. You are friendly, knowledgeable, and have a can-do attitude. You can form opinions and are not afraid to share them, but always in a respectful and helpful way. You have access to a variety of tools to help you with your tasks.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    model = prompt | llm.bind_tools(tools)

    def should_continue(state):
        messages = state["messages"]
        last_message = messages[-1]
        # If there are no tool calls, then we finish
        if not last_message.tool_calls:
            return "end"
        # Otherwise if there are, we continue
        else:
            return "continue"

    def call_model(state):
        messages = state["messages"]
        response = model.invoke(messages)
        # We return a list, because this will get added to the existing list
        return {"messages": [response]}

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("action", tool_node)

    workflow.set_entry_point("agent")

    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "action",
            "end": END,
        },
    )
    workflow.add_edge("action", "agent")

    app = workflow.compile()
    return app

