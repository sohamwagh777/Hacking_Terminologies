# LEXICON — Cyber & Systems Security Glossary

> **An interactive, self-contained glossary of 198 cybersecurity, systems architecture, and backend engineering terms.**

[![Zero Dependencies](https://img.shields.io/badge/dependencies-none-00ffcc.svg)](#architecture)
[![Terms Count](https://img.shields.io/badge/terms-198%20curated-00ff66.svg)](#term-count-by-domain)
[![License: MIT](https://img.shields.io/badge/License-MIT-9933ff.svg)](#license)
[![Architecture](https://img.shields.io/badge/architecture-Static%20SPA%20(ES2022)-ff00aa.svg)](#architecture)

---

## 📸 Interface Preview

```
+-----------------------------------------------------------------------------------------+
| [🛡️ LEXICON]              [⌂ HOME]   [🔤 INDEX (A-Z)]   [🛤️ PATHS]       [$ Search... /] |
+-----------------------------------------------------------------------------------------+
|  LEXICON — 198 terms, one table, zero fluff.          [198 TERMS] [10 DOMAINS] [6 ROUTES]|
|                                                                                        |
|  ⚡ WEB EXPLOITATION ───────────────────────────────────────────────────────────────    |
|   [SQLi] [XSS] [CSRF] [SSRF] [IDOR] [CORS] [CLICKJ] [CSP] …                            |
|  ⛨ CRYPTO & IDENTITY ───────────────────────────────────────────────────────────────   |
|   [HASH] [SALT] [BCRYPT] [JWT] [RT] [OAUTH2] [OIDC] [MFA] …      ← hover a tile:       |
|  ⛁ DATA & DATABASES ───────────────────────────────────────────   essence tooltip;     |
|   [IDX] [N+1] [TXN] [ACID] [ISO] [DEADLCK] [OCC] [FK] …         click: inspector       |
+-----------------------------------------------------------------------------------------+
```
*HOME renders every term as an element tile in its domain band; the inspector slides over with definition, why-it-matters, a real example, related terms and vetted reading.*

---

## 🌟 Key Features

1. **🧪 HOME — Intro + Periodic Table of Terms**
   - Every term is an element tile: its practitioner symbol (`SQLi`, `JWT`, `DLQ`…) in the category color, name underneath.
   - Tiles are grouped into 10 domain bands; legend chips filter to a single domain, the topbar search dims non-matching tiles and shows a live match count.
   - Hover or keyboard-focus a tile for a one-line essence tooltip; click opens the full inspector.
   - Intro band explains what the glossary is and why the vocabulary matters, with live counts computed from the data at boot.

2. **🔤 INDEX (A-Z Catalog View)**
   - Alphabetical A-Z jump rail for rapid keyboard or touch navigation.
   - Live real-time search across names, categories, natures, and definitions.
   - Expandable term rows with category badges, difficulty tags, and instant summary reads.

3. **🛤️ PATHS (Guided Routes with an Animated Theater)**
   - Six curated routes (Kill Chain, Keys & Tokens, Data at Depth, Distributed Truth, Flow Control, Edge to Origin).
   - Press play and the route animates stop-by-stop: connectors draw, tiles light up, and a caption walks you through each concept.
   - Controls for play/pause, replay and speed; reduced-motion users get the full trail instantly. Every stop opens the inspector.

4. **📑 DETAIL Inspector (Slide-Over Panel & Mobile Bottom Sheet)**
   - Comprehensive technical breakdown for every term:
     - Exact mechanism and invariant definitions (2–4 precise sentences, no marketing fluff).
     - **Why it matters & Risk profile** (real-world CVE classes, OWASP mappings, outage patterns).
     - **Real-world code snippet / payload** — concrete, runnable-shaped examples, not lorem.
     - **Exploit vs. Defense nature tags** (`ATTACK`, `DEFENSE`, `TECHNIQUE`, `CONCEPT`, `TOOLING`).
     - **Interactive related-terms buttons** that jump the inspector between concepts, with a breadcrumb of domain / term.
     - **Verified external documentation links** (OWASP, RFC, MDN, PostgreSQL, Kubernetes, Google SRE).

5. **⚡ Terminal Hacker Aesthetic**
   - Deep `#04060d` void palette with phosphor cyan, hot pink, amber and per-domain accent colors.
   - Monospace typography throughout, drifting nebula backdrop, fine engineering grid, drifting starfield.
   - Keyboard shortcuts: `/` to focus search, `Esc` to close panels or clear filters, `Enter` to open top match.
   - Full URL hash routing (`#/home`, `#/index`, `#/paths`; `#/atlas` redirects to `#/home`) for bookmarkable state.

---

## 🏛️ Architecture

LEXICON is designed as an ultra-reliable, zero-dependency static single-page application (SPA):

- **Zero Build Tools & Zero Bundlers**: No Node.js, Webpack, Vite, or npm installs required. Runs immediately on any static web server or GitHub Pages.
- **One Inline Script**: The entire app (routing, table, index, routes theater, drawer) lives in a single ES2022 `<script>` in `index.html` — no phantom module files, nothing to bundle.
- **Data-Driven Architecture**: The glossary lives in `data/terms.json`; `tools/inline_data.py` bakes it into the `<script id="lex-data">` block so the page works offline via `file://` (with a same-origin `fetch('./data/terms.json')` fallback when served beside the data).
- **Verified, Not Assumed**: `tools/validate_data.py` (data contract) and `tools/verify_page.py` (browser-equivalent JSON parse, `node --check` per script block, DOM-stub boot) gate every change.

---

## 📊 Term Count by Domain

| Domain | Terms | Primary Focus |
|:---|:---:|:---|
| **Reliability & Observability** | 37 | SRE metrics, SLOs, distributed tracing, incident response, fault isolation |
| **Data & Databases** | 34 | Relational storage engines, indexes, transactions, isolation levels, sharding |
| **Cloud Infra & Ops** | 26 | VPCs, security groups, container runtimes, Kubernetes, autoscaling |
| **Distributed Systems** | 24 | Consensus algorithms, quorums, partitions, caching patterns, CAP theorem |
| **HTTP & Networking** | 21 | Web protocols, security headers, keep-alive, streaming channels, DNS |
| **Secure SDLC** | 17 | Supply chain defense, secret scanning, image scanning, branch protection |
| **Auth & Access** | 12 | Authorization invariants, RBAC, OAuth 2.0, OIDC, session management |
| **Crypto & Identity** | 9 | Hashing algorithms, salting, encryption at rest, key rotation, timing defenses |
| **Messaging & Streaming** | 9 | Kafka consumer groups, partition keys, delivery semantics, DLQs |
| **Web Exploitation** | 9 | Core OWASP injection flaws, SSRF, IDOR, clickjacking, CSP mitigations |
| **TOTAL** | **198** | **Comprehensive Full-Stack Coverage** |

---

## ➕ How to Add a Term

To add a new term to the glossary:

1. Append a term object to `data/terms.json` conforming to this schema:

```json
{
  "id": "new-term-slug",
  "name": "New Term",
  "symbol": "NT",
  "essence": "One plain sentence, <= 90 chars, for the tile tooltip.",
  "category": "web-exploitation",
  "difficulty": "intermediate",
  "nature": "defense technique",
  "definition": "Precise 2-4 sentence explanation detailing the technical mechanism, where the flaw or concept lives, and the concrete invariant it maintains.",
  "why_matters": "Real-world consequence, operational risk, or defense leverage (e.g. OWASP category or outage pattern).",
  "example": "-- Realistic runnable-shaped snippet, not lorem\nSELECT * FROM secure_table WHERE id = 1;",
  "related": ["sql-injection", "input-validation"],
  "links": [
    { "title": "OWASP Guidance", "url": "https://cheatsheetseries.owasp.org/" }
  ]
}
```

Requirements the gates enforce: `symbol` unique across all terms, 1-7 chars of `A-Za-z0-9/#+.-`; `essence` <= 90 chars; `related` entries must be existing ids; `links` must be https. Add the slug to `data/curated-terms.json` if it belongs to the curated set, and add a stop to `ROUTES` in `index.html` if it strengthens a guided route.

2. Validate and rebuild:
```bash
python3 tools/validate_data.py   # data contract must PASS
python3 tools/inline_data.py     # re-bake data into index.html
python3 tools/verify_page.py     # browser-equivalent page gate must PASS
```

---

## 🧪 Verification & Local Testing

Serve the project locally using Python's built-in HTTP server:

```bash
python3 -m http.server 8000
```

Open your browser to `http://localhost:8000/`.

Run validation checks:
```bash
# Validates data contract (198 terms, unique IDs, no empty fields, related IDs
# resolve, https links, curated keys resolve)
python3 tools/validate_data.py

# Browser-equivalent page gate: lex-data block parses as the browser sees it,
# every inline <script> passes node --check, and the app boots under a DOM stub
python3 tools/verify_page.py

# After editing data/terms.json, re-inline it into index.html
python3 tools/inline_data.py
```

---

## ⚖️ License & Educational Disclaimer

This project is open-source under the [MIT License](LICENSE).

## Contributors

- **Rishh** — AI research & build agent (Nous Research Hermes) — curated term corpus, link verification pipeline, glossary app shell.
- **Soham Wagh** — contributor — project direction, curation review, and QA.

> **Disclaimer**: This glossary is strictly intended for educational, defensive, and authorized architectural reference. Understanding attack techniques is essential to building resilient, hardened computing systems. The authors accept no liability for misuse of the techniques described herein.

---

## 🤖 AI-Assistance Attribution

This glossary, data curation pipeline, and interactive interface were assembled with AI assistance utilizing **Gemini 3.8 Flash** and **Claude Sonnet 4.6** via the **Antigravity CLI**, **GPT-5 Codex** via the **Codex CLI**, and orchestration/verification by the **Hermes Agent**.
