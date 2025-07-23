# tools/todo_writer.py
from langchain.tools import tool
from datetime import datetime
from tools.vault_utils import resolve_vault_path, write_to_heynote, write_to_obsidian

@tool
def todo_tool(task: str) -> str:
    """Add a TODO item to the appropriate vault or fallback to Heynote."""
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    tagged_task = f"- [ ] {task} ({date_str})"

    # Try matching vault
    vault_name = resolve_vault_path(task)
    if vault_name:
        vault_path = f"{vault_name}/TODOs.md"
        write_to_obsidian(vault_path, tagged_task)
        return f"✅ TODO added to {vault_name.split('/')[-1]}: {vault_path}"
    else:
        write_to_heynote(task, tagged_task)
        return f"✅ TODO written to Heynote (fallback)"
