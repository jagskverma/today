#!/usr/bin/env python3
"""Rebuild index.json from entries/*.md.

Runs in the GitHub Action on every push, and by hand when adding entries
locally. Standard library only, no install step.
"""

import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRIES = ROOT / "entries"
OUT = ROOT / "index.json"

FRONT = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.S)
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
CODE_TICK = re.compile(r"`{1,3}")
LEAD_MARKS = re.compile(r"^\s*(#{1,6}|[-*+]|\d+\.|>)\s*")


def parse_meta(block):
    meta = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            continue
        meta[key.strip().lower()] = value.strip().strip("\"'")
    return meta


def parse_tags(raw):
    raw = (raw or "").strip().strip("[]")
    if not raw:
        return []
    return [part.strip().strip("\"'") for part in raw.split(",") if part.strip()]


def excerpt_of(body):
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith(("#", "```", "|", ">")):
            continue
        line = LINK.sub(r"\1", line)
        line = CODE_TICK.sub("", line)
        line = LEAD_MARKS.sub("", line)
        line = re.sub(r"[*_]{1,3}", "", line).strip()
        if line:
            return line[:160] + ("..." if len(line) > 160 else "")
    return ""


def build_entry(path):
    try:
        datetime.date.fromisoformat(path.stem)
    except ValueError:
        return None

    raw = path.read_text(encoding="utf-8")
    body = raw
    meta = {}
    match = FRONT.match(raw)
    if match:
        meta = parse_meta(match.group(1))
        body = raw[match.end():]

    words = len(body.split())
    entry = {
        "date": path.stem,
        "title": meta.get("title") or path.stem,
        "tags": parse_tags(meta.get("tags")),
        "words": words,
        "chars": len(body.strip()),
        "excerpt": excerpt_of(body),
    }
    weight = meta.get("weight")
    if weight and weight.isdigit() and 1 <= int(weight) <= 4:
        entry["weight"] = int(weight)
    return entry


def main():
    if not ENTRIES.is_dir():
        print("no entries directory", file=sys.stderr)
        return 1

    entries = [e for e in (build_entry(p) for p in sorted(ENTRIES.glob("*.md"))) if e]
    entries.sort(key=lambda e: e["date"])

    words = [e["words"] for e in entries]
    # No build timestamp on purpose: a timestamp makes every run produce new
    # bytes, so CI commits index.json after each push and the next local build
    # conflicts. Every field here is derived from the entries.
    payload = {
        "count": len(entries),
        "total_words": sum(words),
        "max_words": max(words) if words else 0,
        "entries": entries,
    }

    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(entries)} entries, {payload['total_words']} words, longest {payload['max_words']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
