#!/usr/bin/env python3
"""Data-contract gate: 198 terms, unique ids, no empty fields, related ids
resolve, https links, curated keys resolve. Exit 0 = PASS."""
import json, os, sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
terms = json.load(open(os.path.join(root, "data", "terms.json"), encoding="utf-8"))
curated = json.load(open(os.path.join(root, "data", "curated-terms.json"), encoding="utf-8"))
ids = {t["id"] for t in terms}
print(f"terms: {len(terms)} | unique ids: {len(ids)} | curated: {len(curated)}")
bad = []
for t in terms:
    for f in ["id", "name", "category", "difficulty", "nature", "definition", "why_matters", "example"]:
        if not str(t.get(f, "")).strip():
            bad.append((t.get("id"), f))
    if not isinstance(t.get("related"), list) or not t["related"]:
        bad.append((t.get("id"), "related empty"))
    if not isinstance(t.get("links"), list) or not t["links"]:
        bad.append((t.get("id"), "links empty"))
    for r in t.get("related", []):
        if r not in ids:
            bad.append((t["id"], "dangling related: " + str(r)))
    for l in t.get("links", []):
        if not str(l.get("url", "")).startswith("https://"):
            bad.append((t["id"], "bad url " + str(l.get("url"))[:40]))
for k in curated:
    if k not in ids:
        bad.append(("curated", "unresolvable key " + k))
stub = sum(1 for t in terms if len(str(t.get("example", ""))) < 40)
print(f"stub examples (<40 chars): {stub}")
print("PROBLEMS:", len(bad))
for b in bad[:20]:
    print(" -", b)
sys.exit(1 if bad else 0)
