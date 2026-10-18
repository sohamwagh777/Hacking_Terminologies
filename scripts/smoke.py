#!/usr/bin/env python3
"""
scripts/smoke.py — Static integrity and smoke verification for LEXICON.
Verifies referenced assets, files, HTML links, JSON integrity, and DOM element bindings.
Exits 0 on success, 1 on failure.
"""

import json
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def check_smoke():
    errors = []
    print("Running LEXICON smoke tests...")

    # 1. Check core files exist
    required_files = [
        "index.html",
        "styles/main.css",
        "styles/atlas.css",
        "scripts/vendor/data-loader.js",
        "scripts/vendor/atlas-graph.js",
        "scripts/vendor/detail.js",
        "scripts/vendor/search.js",
        "scripts/vendor/router.js",
        "data/terms.json",
        "Terminology.txt"
    ]

    for rel_path in required_files:
        full_path = ROOT_DIR / rel_path
        if not full_path.exists():
            errors.append(f"Missing required file: {rel_path}")
        elif full_path.stat().st_size == 0:
            errors.append(f"File is empty: {rel_path}")

    # 2. Check JSON data loads
    terms_file = ROOT_DIR / "data" / "terms.json"
    if terms_file.exists():
        try:
            with open(terms_file, "r", encoding="utf-8") as f:
                terms = json.load(f)
            if not isinstance(terms, list) or len(terms) != 198:
                errors.append(f"data/terms.json expected 198 items, found {len(terms)}")
        except Exception as e:
            errors.append(f"data/terms.json failed to parse: {e}")

    # 3. Check HTML asset references
    index_file = ROOT_DIR / "index.html"
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Find stylesheet hrefs
        css_matches = re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\']([^"\']+)["\']', html_content)
        for href in css_matches:
            if href.startswith("http://") or href.startswith("https://"):
                continue  # External font
            clean_href = href.lstrip("./")
            if not (ROOT_DIR / clean_href).exists():
                errors.append(f"HTML references missing CSS file: {href}")

        # Find script imports in module
        script_matches = re.findall(r'from\s+["\']([^"\']+)["\']', html_content)
        for src in script_matches:
            if src.startswith("http://") or src.startswith("https://"):
                continue
            clean_src = src.lstrip("./")
            if not (ROOT_DIR / clean_src).exists():
                errors.append(f"HTML script imports missing file: {src}")

        # 4. Check DOM Element IDs referenced in JS files exist in index.html
        js_files = list((ROOT_DIR / "scripts").glob("*.js"))
        all_dom_ids_in_html = set(re.findall(r'id=["\']([a-zA-Z0-9_-]+)["\']', html_content))

        for js_file in js_files:
            with open(js_file, "r", encoding="utf-8") as f:
                js_content = f.read()

            id_lookups = re.findall(r'getElementById\(["\']([a-zA-Z0-9_-]+)["\']\)', js_content)
            for dom_id in id_lookups:
                # Some IDs are dynamically rendered by template strings (e.g. inside detail.js)
                dynamic_ids = {"copy-snippet-btn", "code-snippet-body"}
                if dom_id not in all_dom_ids_in_html and dom_id not in dynamic_ids:
                    errors.append(f"{js_file.name} references DOM ID '{dom_id}' not found in index.html")

    if errors:
        print(f"FAILED: {len(errors)} smoke test errors found:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print("SUCCESS: All smoke tests passed! Static assets, JSON integrity, and DOM bindings verified.")
    sys.exit(0)


if __name__ == "__main__":
    check_smoke()
