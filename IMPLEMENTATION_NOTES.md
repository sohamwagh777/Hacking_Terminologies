# IMPLEMENTATION NOTES — LEXICON

This document records the architectural decisions, trade-offs, and technical solutions adopted during the development of LEXICON.

## 1. Domain Grouping & Taxonomy
- In `.agents/spec.json`, 10 distinct categories are defined in the schema fields contract (`web-exploitation`, `auth-access`, `crypto-identity`, `data-databases`, `distributed-systems`, `messaging-streaming`, `http-networking`, `cloud-infra-ops`, `reliability-observability`, `secure-sdlc`).
- All 198 terms from `Terminology.txt` were mapped cleanly across these 10 categories, providing balanced clusters across full-stack cybersecurity, systems architecture, SRE, and cloud operations.
- Each category is assigned a unique phosphor neon color, glowing halo, and background radial wash gradient for distinct visual identity in the PATHS view.

## 2. Slug Derivation & Data Pipeline
- Term slugs are generated deterministically in kebab-case:
  - Non-alphanumeric characters are stripped or converted (`&` becomes `and`, `+` becomes `plus`).
  - Special terms like `.env in .gitignore` map to `env-in-gitignore`, `N+1 Queries` maps to `n-plus-1-queries`, and `12-Factor Apps` maps to `12-factor-apps`.
- The data pipeline is split between:
  - `data/curated-terms.json`: Source of curated metadata (definitions, why it matters, realistic snippets, related terms, verified links).
  - `scripts/build_data.py`: Deterministic parser for `Terminology.txt` (regex `^\d+\.|^\d+\s`) merging with curated data to emit `data/terms.json`.
  - `scripts/validate.py`: Strict schema validator enforcing 198 terms, unique IDs, resolvable related links, and link integrity.

## 3. Link Verification & Research Budget
- Hard budget strictly honored: All links reference canonical, stable, authoritative doc-roots and section pages (OWASP Top 10, RFCs, MDN Web Docs, PostgreSQL Documentation, Kafka, Redis, Google SRE, NIST).
- Deep fragile blog slugs that returned HTTP 404 in early scans were systematically replaced with stable canonical root/section guides.

## 4. Frontend Graph & Canvas Performance
- The ATLAS view implements an interactive force-directed graph running on HTML5 Canvas:
  - 198 nodes and 594 semantic filaments.
  - Spatial hash grid ($O(1)$) used for neighbor repulsion and hover hit detection, keeping CPU usage minimal.
  - Viewport boundary culling skips drawing nodes and edges outside the pan/zoom frustum.
  - Background parallax starfield animates with variable depth and twinkle.
  - Automatic suspension of requestAnimationFrame when the browser tab is hidden (`document.hidden`).

## 5. UI/UX & Routing
- Full hash-based client routing:
  - `#/atlas?term=<id>` (default view)
  - `#/index?term=<id>`
  - `#/paths?category=<cat>&term=<id>`
- Responsive layout:
  - Slide-over panel on desktop ($w=520\text{px}$).
  - Smooth bottom sheet modal on mobile ($h=85\text{vh}$).
- Interactive features:
  - Breadcrumb navigation history (`← Back`) when navigating across related term chips.
  - One-click snippet copy with animated visual confirmation.
  - Global `/` keyboard shortcut for instant search focus and `Esc` to dismiss panels.
