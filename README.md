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
| [🛡️ LEXICON]               [⚛ ATLAS]   [🔤 INDEX (A-Z)]   [🛤️ PATHS]       [$ Search... /] |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|        (o) SQLi --------- (o) IDOR                               +--------------------+ |
|         |                   |                                    | IDOR               | |
|         |                   |                                    | [Auth & Access]    | |
|        (o) XSS ---------- (o) CSRF ------- (o) CORS              | [Intermediate]     | |
|                                                                  | [Attack Concept]   | |
|                                                                  | Insecure Direct... | |
|                                                                  | > Why it matters   | |
|                                                                  | > Real Payload     | |
|                                                                  | > Related Terms    | |
|                                                                  | > Read More (OWASP)| |
|                                                                  +--------------------+ |
+-----------------------------------------------------------------------------------------+
```
*(Screenshot placeholder: Interactive 3D/2D Canvas Constellation graph with glowing filaments and slide-over inspector)*

---

## 🌟 Key Features

1. **⚛ ATLAS Force-Directed Constellation Graph**
   - High-performance HTML5 Canvas engine rendering all 198 terms as glowing, floating nodes.
   - Dynamic filaments connecting related terms (~600 bidirectional semantic edges).
   - Node size scales with the number of related concepts.
   - Color-coded cluster orbits across 10 security and infrastructure domains.
   - Spatial-hash neighbor lookups ($O(1)$) and viewport culling for buttery-smooth 60 FPS navigation.
   - Interactive zoom, drag pan, and hover inspection tooltips.

2. **🔤 INDEX (A-Z Catalog View)**
   - Alphabetical A-Z jump rail for rapid keyboard or touch navigation.
   - Live real-time search across names, categories, natures, and definitions.
   - Expandable term rows with category badges, difficulty tags, and instant summary reads.

3. **🛤️ PATHS (Domain Rail with Immersive Color Washes)**
   - Dedicated navigation sidebar across all 10 specialized engineering domains.
   - Each domain features its own distinct accent palette, glowing border, and background ambient tint/wash.
   - Responsive card grid for systematic domain mastery.

4. **📑 DETAIL Inspector (Slide-Over Panel & Mobile Bottom Sheet)**
   - Comprehensive technical breakdown for every term:
     - Exact mechanism and invariant definitions (2–4 precise sentences, no marketing fluff).
     - **Why it matters & Risk profile** (real-world CVE classes, OWASP mappings, outage patterns).
     - **Real-world code snippet / payload** with syntax formatting and one-click copy feedback.
     - **Exploit vs. Defense nature tags** (`ATTACK`, `DEFENSE`, `TECHNIQUE`, `CONCEPT`, `TOOLING`).
     - **Interactive related terms chips** with breadcrumb navigation history and `← Back` stack.
     - **Verified external documentation links** (OWASP, RFC, MDN, PostgreSQL, Kubernetes, Google SRE).

5. **⚡ Terminal Hacker Aesthetic**
   - Deep `#050810` dark palette with phosphor cyan, neon pink, terminal green, and amber accents.
   - JetBrains Mono typography, CRT scanline overlay, and glassmorphic panels.
   - Keyboard shortcuts: `/` to focus search, `Esc` to close panels or clear filters, `Enter` to open top match.
   - Full URL hash routing (`#/atlas?term=idor`, `#/paths?category=auth-access`) for bookmarkable state.

---

## 🏛️ Architecture

LEXICON is designed as an ultra-reliable, zero-dependency static single-page application (SPA):

- **Zero Build Tools & Zero Bundlers**: No Node.js, Webpack, Vite, or npm installs required. Runs immediately on any static web server or GitHub Pages.
- **Pure Vanilla ES2022 Modules**: Modular architecture split into clean domain concerns (`data-loader.js`, `atlas-graph.js`, `search.js`, `detail.js`, `router.js`).
- **Data-Driven Architecture**: The entire glossary lives in a validated, schema-compliant JSON file (`data/terms.json`) loaded asynchronously at boot.
- **Engineered for Resilience**: Spatial hash indexing, requestAnimationFrame animation cycles, and automatic simulation suspension on tab blur.

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

1. Add the term name to `Terminology.txt` (following the numbered format `199. Term Name`).
2. Add the corresponding curated metadata entry to `data/curated-terms.json` conforming to this schema:

```json
{
  "new-term-slug": {
    "category": "web-exploitation",
    "difficulty": "intermediate",
    "nature": "defense technique",
    "definition": "Precise 2-4 sentence explanation detailing the technical mechanism, where the flaw or concept lives, and the concrete invariant it maintains.",
    "why_matters": "Real-world consequence, operational risk, or defense leverage (e.g. OWASP category or outage pattern).",
    "example": "-- Optional realistic snippet or shell command\nSELECT * FROM secure_table WHERE id = 1;",
    "related": [
      "sql-injection",
      "input-validation"
    ],
    "links": [
      {
        "title": "OWASP Guidance",
        "url": "https://cheatsheetseries.owasp.org/"
      },
      {
        "title": "MDN Documentation",
        "url": "https://developer.mozilla.org/en-US/docs/Web/Security"
      }
    ]
  }
}
```

3. Re-build and validate the dataset using the standard toolchain:
```bash
python3 scripts/build_data.py
python3 scripts/validate.py
python3 scripts/smoke.py
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
# Validates data contract (198 terms, unique IDs, valid categories, resolve related IDs, verified links)
python3 scripts/validate.py

# Verifies static asset existence, DOM bindings, and JSON parsing
python3 scripts/smoke.py
```

---

## ⚖️ License & Educational Disclaimer

This project is open-source under the [MIT License](LICENSE).

> **Disclaimer**: This glossary is strictly intended for educational, defensive, and authorized architectural reference. Understanding attack techniques is essential to building resilient, hardened computing systems. The authors accept no liability for misuse of the techniques described herein.

---

## 🤖 AI-Assistance Attribution

This glossary, data curation pipeline, and interactive interface were assembled with AI assistance utilizing **Gemini 3.8 Flash**, **Gemini 3.1 Pro**, and **Claude Sonnet 4.6** via the **Antigravity CLI** and **Hermes Agent**.
