#!/usr/bin/env python3
"""
Validation script for LEXICON glossary dataset.
Enforces the contract defined in .agents/spec.json and TASK.md.
Exits 0 and prints 198 on success. Exits 1 on failure.
"""

import json
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT_DIR / "data" / "terms.json"
SOURCE_FILE = ROOT_DIR / "Terminology.txt"

ALLOWED_CATEGORIES = {
    "web-exploitation",
    "auth-access",
    "crypto-identity",
    "data-databases",
    "distributed-systems",
    "messaging-streaming",
    "http-networking",
    "cloud-infra-ops",
    "reliability-observability",
    "secure-sdlc",
}

ALLOWED_DIFFICULTIES = {"beginner", "intermediate", "advanced"}

ALLOWED_NATURE_WORDS = {"attack", "defense", "technique", "concept", "tooling"}


def validate():
    errors = []

    if not DATA_FILE.exists():
        print(f"ERROR: {DATA_FILE} does not exist", file=sys.stderr)
        sys.exit(1)

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            terms = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to parse JSON from {DATA_FILE}: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(terms, list):
        print("ERROR: data/terms.json must be a JSON array", file=sys.stderr)
        sys.exit(1)

    if len(terms) != 198:
        errors.append(f"Expected exactly 198 terms, found {len(terms)}")

    # Check source names if Terminology.txt exists
    source_names = []
    if SOURCE_FILE.exists():
        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                m = re.match(r"^\d+\.\s*(.+)$", line.strip())
                if m:
                    source_names.append(m.group(1).strip())

    id_set = set()
    for idx, term in enumerate(terms):
        term_id = term.get("id")
        name = term.get("name")

        if not term_id or not isinstance(term_id, str):
            errors.append(f"Term at index {idx} has invalid or missing id: {term_id}")
            continue

        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", term_id):
            errors.append(f"Term '{name}' id '{term_id}' is not valid kebab-case")

        if term_id in id_set:
            errors.append(f"Duplicate id found: '{term_id}'")
        id_set.add(term_id)

    # Detailed field validation
    for idx, term in enumerate(terms):
        term_id = term.get("id", f"index-{idx}")
        name = term.get("name")

        # Name
        if not name or not isinstance(name, str):
            errors.append(f"Term '{term_id}' has missing or non-string name")

        # Category
        cat = term.get("category")
        if cat not in ALLOWED_CATEGORIES:
            errors.append(
                f"Term '{term_id}' has invalid category '{cat}'. Allowed: {ALLOWED_CATEGORIES}"
            )

        # Difficulty
        diff = term.get("difficulty")
        if diff not in ALLOWED_DIFFICULTIES:
            errors.append(
                f"Term '{term_id}' has invalid difficulty '{diff}'. Allowed: {ALLOWED_DIFFICULTIES}"
            )

        # Nature
        nature = term.get("nature")
        if not nature or not isinstance(nature, str):
            errors.append(f"Term '{term_id}' has missing or non-string nature")
        else:
            words = set(nature.strip().split())
            invalid_words = words - ALLOWED_NATURE_WORDS
            if invalid_words or not words:
                errors.append(
                    f"Term '{term_id}' has invalid nature words: {invalid_words}. Allowed: {ALLOWED_NATURE_WORDS}"
                )

        # Definition
        definition = term.get("definition")
        if not definition or not isinstance(definition, str) or len(definition.strip()) < 20:
            errors.append(f"Term '{term_id}' has missing or too short definition")

        # Why it matters
        why = term.get("why_matters")
        if not why or not isinstance(why, str) or len(why.strip()) < 15:
            errors.append(f"Term '{term_id}' has missing or too short why_matters")

        # Example (optional, but if present must be string)
        example = term.get("example")
        if example is not None and not isinstance(example, str):
            errors.append(f"Term '{term_id}' example must be a string if provided")

        # Related terms
        related = term.get("related")
        if not isinstance(related, list):
            errors.append(f"Term '{term_id}' related must be a list")
        else:
            if len(related) < 2:
                errors.append(
                    f"Term '{term_id}' has fewer than 2 related terms ({len(related)})"
                )
            if len(related) > 6:
                errors.append(
                    f"Term '{term_id}' has more than 6 related terms ({len(related)})"
                )
            for rel in related:
                if rel == term_id:
                    errors.append(f"Term '{term_id}' lists itself in related")
                elif rel not in id_set:
                    errors.append(
                        f"Term '{term_id}' references unknown related id '{rel}'"
                    )

        # Links
        links = term.get("links")
        if not isinstance(links, list):
            errors.append(f"Term '{term_id}' links must be a list")
        else:
            if len(links) < 2:
                errors.append(
                    f"Term '{term_id}' has fewer than 2 links ({len(links)})"
                )
            if len(links) > 6:
                errors.append(
                    f"Term '{term_id}' has more than 6 links ({len(links)})"
                )
            for l_idx, link in enumerate(links):
                if not isinstance(link, dict):
                    errors.append(f"Term '{term_id}' link #{l_idx} is not an object")
                    continue
                title = link.get("title")
                url = link.get("url")
                if not title or not isinstance(title, str) or not title.strip():
                    errors.append(f"Term '{term_id}' link #{l_idx} missing title")
                if not url or not isinstance(url, str) or not url.strip():
                    errors.append(f"Term '{term_id}' link #{l_idx} missing url")
                elif not (url.startswith("http://") or url.startswith("https://")):
                    errors.append(
                        f"Term '{term_id}' link #{l_idx} url does not start with http/https: {url}"
                    )

    if errors:
        print(f"FAILED: {len(errors)} validation errors found:", file=sys.stderr)
        for err in errors[:50]:
            print(f"  - {err}", file=sys.stderr)
        if len(errors) > 50:
            print(f"  ... and {len(errors) - 50} more errors", file=sys.stderr)
        sys.exit(1)

    print(f"SUCCESS: 198 terms successfully validated across {len(ALLOWED_CATEGORIES)} categories.")
    print("198")
    sys.exit(0)


if __name__ == "__main__":
    validate()
