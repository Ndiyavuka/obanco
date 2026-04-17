#!/usr/bin/env python3
"""
Ingest a Claude.ai data export into the conversations/ store.

Usage:
    python scripts/ingest_claude_export.py <path-to-conversations.json>
    python scripts/ingest_claude_export.py <path-to-export.zip>

The export zip / JSON comes from: claude.ai → Settings → Export Data.

Output:
    conversations/raw/YYYY/MM/<uuid>.json   — one file per conversation
    conversations/INDEX.md                  — searchable flat index
"""

import json
import os
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "conversations" / "raw"
INDEX_PATH = REPO_ROOT / "conversations" / "INDEX.md"


def load_conversations(source: str) -> list[dict]:
    path = Path(source)
    if not path.exists():
        sys.exit(f"Error: {source} not found.")

    if path.suffix == ".zip":
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
            json_name = next((n for n in names if n.endswith("conversations.json")), None)
            if not json_name:
                sys.exit(f"Error: no conversations.json found inside {path.name}. Files: {names}")
            with zf.open(json_name) as f:
                return json.load(f)

    with open(path, encoding="utf-8") as f:
        return json.load(f)


def parse_date(raw: str | None) -> datetime | None:
    if not raw:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            dt = datetime.strptime(raw, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None


def save_conversation(conv: dict) -> Path:
    uuid = conv.get("uuid", "unknown")
    created_raw = conv.get("created_at")
    dt = parse_date(created_raw)
    year = dt.strftime("%Y") if dt else "unknown"
    month = dt.strftime("%m") if dt else "unknown"

    dest_dir = RAW_DIR / year / month
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{uuid}.json"

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(conv, f, ensure_ascii=False, indent=2)

    return dest


def build_index(conversations: list[dict]) -> str:
    lines = [
        "# Claude Conversations — Index",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}  ",
        f"Total: {len(conversations)} conversations",
        "",
        "| Date | Title | UUID | Messages |",
        "|------|-------|------|----------|",
    ]

    sorted_convs = sorted(
        conversations,
        key=lambda c: c.get("created_at") or "",
        reverse=True,
    )

    for conv in sorted_convs:
        uuid = conv.get("uuid", "—")
        title = (conv.get("name") or "Untitled").replace("|", "\\|").strip()
        created_raw = conv.get("created_at", "")
        dt = parse_date(created_raw)
        date_str = dt.strftime("%Y-%m-%d") if dt else "unknown"
        msg_count = len(conv.get("chat_messages", []))
        short_uuid = uuid[:8] if len(uuid) >= 8 else uuid
        lines.append(f"| {date_str} | {title} | `{short_uuid}…` | {msg_count} |")

    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python scripts/ingest_claude_export.py <conversations.json or export.zip>")

    source = sys.argv[1]
    print(f"Loading from: {source}")
    conversations = load_conversations(source)

    if not isinstance(conversations, list):
        sys.exit("Error: expected a JSON array of conversations at the top level.")

    print(f"Found {len(conversations)} conversations. Saving raw dumps...")

    saved = 0
    skipped = 0
    for conv in conversations:
        dest = save_conversation(conv)
        if dest.exists():
            saved += 1
        else:
            skipped += 1

    print(f"Saved {saved} files to conversations/raw/")

    print("Writing INDEX.md...")
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(build_index(conversations), encoding="utf-8")
    print(f"Index written: {INDEX_PATH}")

    print("\nDone.")
    print(f"  Raw dumps : conversations/raw/YYYY/MM/<uuid>.json")
    print(f"  Index     : conversations/INDEX.md")


if __name__ == "__main__":
    main()
