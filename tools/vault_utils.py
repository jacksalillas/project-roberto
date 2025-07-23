# tools/vault_utils.py
import os
import re
from datetime import datetime

# Base directories
OBSIDIAN_BASE = "/Users/jackrich/Library/Mobile Documents/iCloud~md~obsidian/Documents"
HEYNOTE_DIR = "/Users/jackrich/Library/Mobile Documents/com~apple~CloudDocs/Heynote"

VAULT_KEYWORDS = {
    "work": "Macquarie",
    "office": "Macquarie",
    "devops": "DevOps Engineer",
    "exam": "DevOps Engineer",
    "study": "DevOps Engineer",
    "s3": "DevOps Engineer",
    "career": "DevOps Engineer",
    "professional": "DevOps Engineer",
    "personal": "Jack-Rich",
    "life": "Jack-Rich",
    "journal": "Jack-Rich",
}

def sanitize_filename(name: str) -> str:
    name = re.sub(r'[^\w\- ]+', '', name)
    return name.replace(' ', '_').strip()[:64]

def resolve_vault_path(text: str) -> str | None:
    for keyword, vault in VAULT_KEYWORDS.items():
        if keyword.lower() in text.lower():
            full_path = os.path.join(OBSIDIAN_BASE, vault)
            if os.path.isdir(full_path):
                return full_path
    return None

def write_to_obsidian(relative_path: str, content: str):
    os.makedirs(os.path.dirname(relative_path), exist_ok=True)
    with open(relative_path, "a") as f:
        f.write(f"\n{content}\n")

def write_to_heynote(content: str, filename: str):
    full_path = os.path.join(HEYNOTE_DIR, filename)
    header = '{"formatVersion":"1.0.0","name":"Note","cursors":{"ranges":[{"anchor":0,"head":0}],"main":0},"foldedRanges":[]}\n∞∞∞markdown-a\n'
    if not os.path.exists(full_path):
        with open(full_path, "w") as f:
            f.write(header + content)
    else:
        with open(full_path, "a") as f:
            f.write(f"\n∞∞∞markdown-a\n{content}\n")
