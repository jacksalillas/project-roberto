# main.py

import argparse
from agents.super_agent import get_super_agent
from models import get_model
from tools import RAGService
from langchain_core.messages import HumanMessage

from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory

from rich.console import Console
from rich.status import Status # Import Status for loading indicators

console = Console()

def display_banner():
    # ROBERTO banner with gradient colors
    banner_lines = [
        "██████╗  ██████╗ ██████╗ ███████╗██████╗ ████████╗ ██████╗ ",
        "██╔══██╗██╔═══██╗██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗",
        "██████╔╝██║   ██║██████╔╝█████╗  ██████╔╝   ██║   ██║   ██║",
        "██╔══██╗██║   ██║██╔══██╗██╔══╝  ██╔══██╗   ██║   ██║   ██║",
        "██║  ██║╚██████╔╝██████╔╝███████╗██║  ██║   ██║   ╚██████╔╝",
        "╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ "
    ]
    
    # Gradient colors from blue to cyan to green
    colors = ["blue", "bright_blue", "cyan", "bright_cyan", "green", "bright_green"]
    
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        console.print(line, style=f"bold {color}")
    
    console.print("\nWelcome to Roberto, your personal AI assistant!", style="bold yellow")
    console.print("Type 'exit' or 'quit' to end the session.", style="dim")
    console.print("---------------------------------------------------", style="dim")

def main():
    display_banner()

    # Initialize RAGService once
    rag_service = RAGService()

    # For now, we'll hardcode the LLM to ollama for interactive mode
    # In a more advanced setup, we could allow switching LLMs dynamically
    llm = get_model("ollama")
    agent = get_super_agent(llm)

    history = InMemoryHistory()

    while True:
        try:
            user_input = prompt("Roberto > ", history=history).strip()

            if user_input.lower() in ['exit', 'quit']:
                console.print("Goodbye!")
                break

            if user_input.startswith("index "):
                path_to_index = user_input[len("index "):].strip()
                if path_to_index:
                    with Status("Indexing documents...", spinner="dots", console=console):
                        rag_service.load_and_index_documents(path_to_index)
                else:
                    console.print("Please provide a path to index.")
            else:
                # Pass the user input to the agent
                with Status("Roberto is thinking...", spinner="dots", console=console):
                    result = agent.invoke({"messages": [HumanMessage(content=user_input)]})
                console.print(result["messages"][-1].content)

        except EOFError:
            # Ctrl+D pressed
            console.print("Goodbye!")
            break
        except KeyboardInterrupt:
            # Ctrl+C pressed
            console.print("Operation cancelled. Type 'exit' or 'quit' to quit.")
            continue
        except Exception as e:
            console.print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
