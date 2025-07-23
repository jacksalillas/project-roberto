# main.py

import argparse
from agents.super_agent import get_super_agent
from models import get_model
from tools import RAGService
from langchain_core.messages import HumanMessage

def main():
    parser = argparse.ArgumentParser(description="Roberto: Your Personal AI Assistant")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Agent task parser
    parser_agent = subparsers.add_parser("task", help="Run a task with the super agent")
    parser_agent.add_argument("--llm", required=True, choices=["ollama", "openai", "gemini"])
    parser_agent.add_argument("--task", required=True)

    # RAG indexing parser
    parser_index = subparsers.add_parser("index", help="Index documents for the RAG service")
    parser_index.add_argument("--path", action="append", required=True, help="Path to the documents to index (can be specified multiple times)")

    args = parser.parse_args()

    if args.command == "task":
        llm = get_model(args.llm)
        agent = get_super_agent(llm)
        result = agent.invoke({"messages": [HumanMessage(content=args.task)]})
        print(result["messages"][-1].content)
    elif args.command == "index":
        rag_service = RAGService()
        for p in args.path:
            rag_service.load_and_index_documents(p)

if __name__ == "__main__":
    main()
