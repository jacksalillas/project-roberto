# CLI.py

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
from rich.status import Status
from rich.text import Text
from rich.panel import Panel # Import Panel for the box

console = Console()

def display_banner():
    # ROBERTO banner with true gradient colors - slanted style
    banner_lines = [
        "      ██████╗  ██████╗ ██████╗ ███████╗██████╗ ████████╗ ██████╗ ",
        "     ██╔══██╗██╔═══██╗██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗",
        "    ██████╔╝██║   ██║██████╔╝█████╗  ██████╔╝   ██║   ██║   ██║",
        "   ██╔══██╗██║   ██║██╔══██╗██╔══╝  ██╔══██╗   ██║   ██║   ██║",
        "  ██║  ██║╚██████╔╝██████╔╝███████╗██║  ██║   ██║   ╚██████╔╝",
        "  ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ "
    ]

    for line in banner_lines:
        text = Text(line, style="bold")
        line_length = len(line)

        for j, char in enumerate(line):
            if char not in [' ', '\n']:
                progress = j / max(1, line_length - 1)
                if progress <= 0.5:
                    ratio = progress * 2
                    r = int(0 * (1 - ratio) + 0 * ratio)
                    g = int(100 * (1 - ratio) + 255 * ratio)
                    b = 255
                else:
                    ratio = (progress - 0.5) * 2
                    r = 0
                    g = 255
                    b = int(255 * (1 - ratio) + 0 * ratio)
                color = f"rgb({r},{g},{b})"
                text.stylize(color, j, j + 1)

        console.print(text)

    # Encapsulate welcome and exit messages in a Panel
    welcome_message = Text("Welcome to Roberto, your personal AI assistant!", style="bold yellow")
    exit_message = Text("Type 'exit' or 'quit' to end the session.", style="dim")

    panel_content = Text.assemble(welcome_message, "\n", exit_message)

    panel = Panel(
        panel_content,
        border_style="cyan",
        padding=(0, 2), # Changed padding to 0 vertical
        expand=False
    )
    console.print(panel)


def main():
    display_banner()
    rag_service = RAGService()
    llm = get_model("ollama")
    agent = get_super_agent(llm)
    history = InMemoryHistory()

    custom_style = Style.from_dict({
        'prompt': 'ansibrightblue bold',
        'input': 'ansiblue',
        'completion-menu.completion': 'bg:#008888 #ffffff',
        'completion-menu.completion.current': 'bg:#00aaaa #000000',
        'scrollbar.background': 'bg:#88aaaa',
        'scrollbar.button': 'bg:#222222',
    })

    while True:
        try:
            user_input = prompt("Roberto > ", history=history, style=custom_style).strip()

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
                with Status("Roberto is thinking...", spinner="dots", console=console):
                    result = agent.invoke({"messages": [HumanMessage(content=user_input)]})
                console.print(result["messages"][-1].content)

        except EOFError:
            console.print("Goodbye!")
            break
        except KeyboardInterrupt:
            console.print("Operation cancelled. Type 'exit' or 'quit' to quit.")
            continue
        except Exception as e:
            console.print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()