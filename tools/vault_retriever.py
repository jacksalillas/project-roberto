# tools/vault_retriever.py
from langchain.tools import tool
import os

@tool
def vault_search(query: str) -> str:
    """Search across Obsidian vaults and Heynote files for the given query."""
    base_paths = [
        "/Users/jackrich/Library/Mobile Documents/iCloud~md~obsidian/Documents",
        "/Users/jackrich/Library/Mobile Documents/com~apple~CloudDocs/Heynote"
    ]
    matches = []
    for base in base_paths:
        for root, _, files in os.walk(base):
            for file in files:
                if file.endswith(('.md', '.txt')):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r") as f:
                            if query.lower() in f.read().lower():
                                matches.append(f"Found in {path}")
                    except:
                        continue
    return "\n".join(matches) if matches else "No relevant content found in any vault."
