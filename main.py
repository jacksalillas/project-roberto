# main.py

import argparse
from agents.super_agent import get_super_agent
from models import get_model

parser = argparse.ArgumentParser()
parser.add_argument("--llm", required=True, choices=["ollama", "openai", "gemini"])
parser.add_argument("--task", required=True)
args = parser.parse_args()

llm = get_model(args.llm)
agent = get_super_agent(llm)

result = agent.invoke({"input": args.task})
print(result)
