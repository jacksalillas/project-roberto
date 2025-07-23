# tools/note_writer.py
from langchain.tools import tool
from datetime import datetime
from tools.vault_utils import sanitize_filename, resolve_vault_path, write_to_obsidian, write_to_heynote

@tool
def note_tool(note: str) -> str:
    """Write a note to the appropriate vault or fallback to Heynote."""
    today = datetime.now().strftime("%Y-%m-%d")
    title = sanitize_filename(note[:50])
    filename = f"{today} - {title}.md"

    vault_name = resolve_vault_path(note)
    if vault_name:
        vault_path = f"{vault_name}/{filename}"
        write_to_obsidian(vault_path, note)
        obsidian_result = f"✅ Note written to Obsidian vault: {vault_name.split('/')[-1]}: {vault_path}"
    else:
        obsidian_result = None

    heynote_path = f"{title}.txt"
    write_to_heynote(note, heynote_path)
    heynote_result = f"✅ Note written to Heynote buffer: {heynote_path}"

    result = "\n".join(filter(None, [obsidian_result, heynote_result]))
    return result
