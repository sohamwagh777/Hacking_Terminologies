#!/usr/bin/env python3
"""
scripts/build_data.py — Deterministic data pipeline for LEXICON.
Parses Terminology.txt using regex (^\\d+\\.|^\\d+\\s) and merges it with
curated metadata from data/curated-terms.json to emit data/terms.json.
Stdlib only.
"""

import json
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SOURCE_FILE = ROOT_DIR / "Terminology.txt"
CURATED_FILE = ROOT_DIR / "data" / "curated-terms.json"
OUTPUT_FILE = ROOT_DIR / "data" / "terms.json"


def slugify(name: str) -> str:
    """Derive clean, deterministic kebab-case slug from term name."""
    s = name.lower()
    s = s.replace('&', ' and ')
    s = s.replace('+', ' plus ')
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')


def build():
    if not SOURCE_FILE.exists():
        print(f"ERROR: Source file {SOURCE_FILE} not found.", file=sys.stderr)
        sys.exit(1)

    if not CURATED_FILE.exists():
        print(f"ERROR: Curated file {CURATED_FILE} not found.", file=sys.stderr)
        sys.exit(1)

    # 1. Parse Terminology.txt
    raw_terms = []
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            # Match ^\d+\. or ^\d+\s per TASK.md
            m = re.match(r"^(\d+)(?:\.|\s)\s*(.+)$", line_str)
            if m:
                index = int(m.group(1))
                name = m.group(2).strip()
                raw_terms.append((index, name))

    if len(raw_terms) != 198:
        print(f"WARNING: Expected 198 terms from Terminology.txt, found {len(raw_terms)}", file=sys.stderr)

    # 2. Load Curated Data
    with open(CURATED_FILE, "r", encoding="utf-8") as f:
        curated_data = json.load(f)

    # 3. Merge & Validate Structure
    final_terms = []
    for idx, name in raw_terms:
        term_id = slugify(name)
        if term_id not in curated_data:
            print(f"ERROR: Term '{name}' (id: '{term_id}') missing from {CURATED_FILE}", file=sys.stderr)
            sys.exit(1)

        curated = curated_data[term_id]

        term_obj = {
            "id": term_id,
            "name": name,
            "category": curated["category"],
            "difficulty": curated["difficulty"],
            "nature": curated["nature"],
            "definition": curated["definition"],
            "why_matters": curated["why_matters"],
            "example": curated.get("example", ""),
            "related": curated["related"],
            "links": curated["links"]
        }
        final_terms.append(term_obj)

    # 4. Write data/terms.json
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_terms, f, indent=2, ensure_ascii=False)

    print(f"Successfully built {OUTPUT_FILE} with {len(final_terms)} terms.")


if __name__ == "__main__":
    build()
