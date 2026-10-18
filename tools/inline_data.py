#!/usr/bin/env python3
"""One-time, offline build script (NOT part of the website).

Inlines data/terms.json into index.html as:
    <script id="lex-data" type="application/json">{...}</script>
so the site works on GitHub Pages / GitLab Pages / double-clicked file:// —
no server, no fetch, no CORS.

Usage: python3 tools/inline_data.py   (run from repo root)
"""
import json, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
data = root / "data" / "terms.json"
page = root / "index.html"

blob = data.read_text(encoding="utf-8")
json.loads(blob)  # fail fast if malformed

marker_open = '<script id="lex-data" type="application/json">'
html = page.read_text(encoding="utf-8")
start = html.find(marker_open)
if start == -1:
    sys.exit("index.html has no lex-data block (run rebuild or restore page.html)")
end = html.find("</script>", start)
html = html[:start] + marker_open + blob + html[end:]
page.write_text(html, encoding="utf-8")
print(f"inlined {len(json.loads(blob))} terms into index.html ({len(blob):,} bytes)")
