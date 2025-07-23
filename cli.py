# CLI.py

import argparse
import re
import json # Import json module

from agents.super_agent import get_super_agent
from models import get_model
from tools import RAGService
from tools.cache_service import CacheService # Import CacheService
from langchain_core.messages import HumanMessage, AIMessage
from llama_index.embeddings.ollama import OllamaEmbedding # Import OllamaEmbedding

from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory

from rich.console import Console, Group
from rich.status import Status
from rich.text import Text
from rich.panel import Panel
from rich.syntax import Syntax
from rich.align import Align

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

    welcome_message = Text("Welcome to Roberto, your personal AI assistant!", style="bold yellow")
    exit_message = Text("Type 'exit', 'quit', 'bye', or 'q' to end the session.", style="dim")
    panel_content = Text.assemble(welcome_message, "\n", exit_message)

    panel = Panel(panel_content, border_style="cyan", padding=(0, 2), expand=False)
    console.print(panel)

def main():
    display_banner()
    rag_service = RAGService()
    embed_model = OllamaEmbedding(model_name="nomic-embed-text") # Initialize OllamaEmbedding
    cache_service = CacheService(embed_model=embed_model) # Initialize CacheService with embed_model
    llm = get_model("ollama")
    agent = get_super_agent(llm)
    history = InMemoryHistory()
    messages = [] # Initialize messages list for conversation history

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
            user_input = prompt("You > ", history=history, style=custom_style).strip()

            if user_input.lower() in ['exit', 'quit', 'bye', 'q']:
                console.print("Goodbye!")
                break

            if user_input.startswith("index "):
                path_to_index = user_input[len("index "):].strip()
                if path_to_index:
                    with Status("Indexing documents...", spinner="dots", console=console):
                        rag_service.load_and_index_documents(path_to_index)
                else:
                    _print_error("Please provide a path to index.")
            else:
                cached_response = cache_service.get(user_input)
                if cached_response:
                    _print_roberto_response(cached_response)
                    messages.append(HumanMessage(content=user_input)) # Add user message to history
                    messages.append(AIMessage(content=cached_response)) # Add cached response to history
                else:
                    messages.append(HumanMessage(content=user_input)) # Add user message to history
                    with Status("💭 Roberto is thinking...", spinner="dots", console=console):
                        result = agent.invoke({"messages": messages}) # Pass full history
                    roberto_response_content = result["messages"][-1].content
                    _print_roberto_response(roberto_response_content)
                    messages.append(result["messages"][-1]) # Add Roberto's response to history

                    # Determine if the response is for a temporary fact
                    is_temporary_fact = False
                    temporary_keywords = ["weather", "time", "date", "current", "now"]
                    if any(keyword in user_input.lower() for keyword in temporary_keywords):
                        is_temporary_fact = True

                    cache_service.set(user_input, roberto_response_content, is_temporary=is_temporary_fact) # Cache the response

        except EOFError:
            console.print("Goodbye!")
            break
        except FileNotFoundError as e:
            _print_error(f"{e}")
        except KeyboardInterrupt:
            console.print("Operation cancelled. Type 'exit' or 'quit' to quit.")
            continue
        except Exception as e:
            _print_error(f"{e}")

def _print_roberto_response(response_content: str):
    code_block_pattern = r"""```(?P<lang>\w+)?\n(?P<code>[\s\S]*?)```"""
    matches = list(re.finditer(code_block_pattern, response_content))

    output_renderables = []
    last_idx = 0

    # Extract sources if present
    sources_pattern = r"\n\nSources: (.+)"
    sources_match = re.search(sources_pattern, response_content)
    sources_text = ""
    if sources_match:
        sources_text = sources_match.group(1)
        response_content = response_content[:sources_match.start()]

    for match in matches:
        if match.start() > last_idx:
            before = response_content[last_idx:match.start()]
            output_renderables.append(Text(before.strip()))

        lang = match.group('lang') or 'python'
        code = match.group('code').strip()
        syntax = Syntax(code, lang, theme="monokai", line_numbers=True)
        output_renderables.append(syntax)

        last_idx = match.end()

    if last_idx < len(response_content):
        after = response_content[last_idx:]
        output_renderables.append(Text(after.strip()))

    if not output_renderables:
        output_renderables = [Text(response_content.strip() or "(No response)")]

    response_panel = Panel(
        Group(*output_renderables),
        title="💡 Roberto says:",
        title_align="left",
        border_style="cyan",
        padding=(1, 2),
        expand=False
    )
    console.print(response_panel)

    if sources_text:
        try:
            sources_data = json.loads(sources_text)
            if "sources" in sources_data and isinstance(sources_data["sources"], list):
                formatted_sources = ", ".join([f"<{s}>" for s in sources_data["sources"]])
                console.print(Text(f"\nSources: {formatted_sources}", style="dim"))
            else:
                console.print(Text(f"\nSources: {sources_text}", style="dim")) # Fallback if not expected JSON
        except json.JSONDecodeError:
            console.print(Text(f"\nSources: {sources_text}", style="dim")) # Fallback if not JSON


def _print_error(error_msg: str):
    error_text = Text(error_msg, style="bold red")
    panel = Panel(
        Align.left(error_text),
        title="❌ Error:",
        title_align="left",
        border_style="red",
        padding=(1, 2),
        expand=False
    )
    console.print(panel)

if __name__ == "__main__":
    main()
