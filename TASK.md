# TASK.md — Antigravity agent task brief (read this fully before acting)

You are an elite product-minded engineer + security researcher + information architect.
You work solo in /home/soham-7/github-archive/Hacking_Terminologies (the repo root)
and finish the WHOLE job in this one autonomous session. There is no human to ask:
if a choice is ambiguous, pick the most defensible, simple option, record it in
IMPLEMENTATION_NOTES.md, and keep going.

## CONTEXT

This becomes Rishh's GitHub portfolio project. Acceptance checkers and users judge
by (a) every term having a technically correct, non-vague definition, (b) genuinely
correct cross-links between terms, (c) real working article links, (d) a polished
interactive frontend. A page that looks beautiful but contains invented URLs, wrong
technical claims, or vague filler FAILS review.

Terminology.txt at the repo root has 198 numbered terms — READ IT FIRST.
The full data/HTML contract (spec.json) is in .agents/spec.json — READ IT SECOND.

## GOALS

G1 Data: Write scripts/build_data.py (stdlib only, deterministic) that parses
Terminology.txt (regex ^\d+\.|^\d+\s) and merges it with a CURATED JSON you
hand-write at data/curated-terms.json (one entry per term: category, difficulty,
nature, definition, why_matters, optional example, related, links) to emit
data/terms.json in EXACTLY the JSON contract documented in .agents/spec.json.

G2 Frontend: Implement the full static site per spec (ATLAS force graph + INDEX
list + PATHS category rail + detail slide-over + search + keyboard nav,
mobile-responsive, each category visually distinct colour + background wash).

G3 Docs: README.md per spec item 3 (features, architecture, term-count table,
contributing guide, license + educational disclaimer, AI-assistance credit).

G4 Smoke: Write scripts/validate.py and scripts/smoke.py; RUN BOTH; also
curl-verify the site via `python3 -m http.server` on a free port (report HTTP
codes); fix what fails.

G5 Git: Init git, stage ONLY source (no .agents/, no __pycache__, no temp; keep
Terminology.txt — if renamed, keep it as data/source-terms.txt), ONE commit:
"feat: LEXICON v1 — interactive cyber glossary (atlas/index/paths + detail panel)".
Do NOT create a remote, do NOT push, do NOT run gh — the orchestrator handles GitHub.

## RESEARCH BUDGET

You may use web_search / web_fetch ONLY to VERIFY links and uncertain facts.
HARD CAP: 25 web_search + 15 web_fetch TOTAL across the session; after that, write
from your own verified knowledge.
- An HTTP-200 doc-root page (https://owasp.org/www-project-top-10/,
  https://docs.python.org/3/library/hashlib.html, MDN index...) IS AN ACCEPTABLE
  LINK. Do NOT hunt for exact deep-article URLs; the section/index page of the
  authoritative site is exactly what the spec asks for.
- A guessed, dead or paywalled link = a FAILED item. Never invent a deep slug.
- For well-trodden terms (XSS, CSRF, IDOR, SSRF, ACID, DNS, 12-factor...)
  research = WASTED budget. Write directly.

## CONTENT QUALITY BAR

- Definition = precise mechanism (who/where the flaw or idea lives + the concrete
  invariant it protects or breaks). NOT "a type of attack" filler.
- why_matters = practical leverage or risk (e.g. auth bypass via object IDs =
  OWASP A01:2021; missing HSTS = first-request downgrade; N+1 + cold start =
  latency cliff; replayable unsigned webhooks = forgery).
- example = only where it clarifies (payload, header, psql/kafka/redis/git/shell
  snippet, command). Valid JSON escapes. Educational/defensive framing only.
- related = only true functional/defense/counterpart pairs, bidirectional.
- 198 entries x (def + why + 2..6 related + 2..5 links). If short on budget/time,
  deliver FEWER categories FULLY completed (def + why + related + 2 links each)
  rather than 198 stubs, and say honestly which terms remain incomplete.

## VERIFICATION GATES (all must pass before you stop)

1. scripts/validate.py exits 0 and prints 198.
2. Every term: >=2 related, >=2 links, definition, why_matters (grep counts == 0 missing).
3. `python3 -m http.server <port>`: curl -sI on /, /data/terms.json, one .js, one .css — ALL HTTP 200. Report raw codes.
4. git log --oneline shows exactly 1 commit; git status --porcelain empty; git ls-files has no junk.

## FINAL ANSWER FORMAT

(a) DONE / PARTIAL + which G1-G5 complete; (b) raw output of the LAST validate.py run;
(c) raw curl -sI HTTP codes; (d) git log -1 + git status --porcelain;
(e) HONEST DEFERRED/FAILED list of anything thin/unverified.
Writing "I did not verify X" is allowed. Writing a lie is not.
