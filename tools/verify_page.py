#!/usr/bin/env python3
"""LEXICON final gate. Run from repo root.
1. Browser-equivalent lex-data extraction (ends at FIRST real </script>) must parse as JSON == data/terms.json count.
2. Every non-JSON <script> passes node --check.
3. DOM-stub smoke: app scripts execute top-level without throw; loaded term count == data count.
Exit 0 = all PASS with raw evidence printed.
"""
import json, subprocess, sys, os, re, tempfile
from html.parser import HTMLParser

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(repo, "index.html"), encoding="utf-8").read()
fails = []

# --- gate 1: browser-view lex-data ---
marker = '<script id="lex-data" type="application/json">'
i = html.find(marker)
if i == -1:
    print("FAIL: no lex-data block"); sys.exit(1)
end = html.find("</" + "script>", i)   # browser terminates block at first real close tag
block = html[i + len(marker):end]
data = json.load(open(os.path.join(repo, "data", "terms.json"), encoding="utf-8"))
try:
    terms = json.loads(block)
    print(f"PASS lex-data: parses, {len(terms)} terms (data file: {len(data)})")
    if len(terms) != len(data):
        fails.append(f"count mismatch inline {len(terms)} vs data {len(data)}")
except Exception as e:
    fails.append(f"lex-data JSON parse FAIL: {e}")
    print(f"FAIL lex-data: {e}")
if re.search(r"<\s*/\s*script", block.replace("<\\/", "<ESC>"), re.I):
    fails.append("lex-data contains unescaped </script sequence")

# --- gate 2: every non-JSON script passes node --check ---
class SP(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False); self.blocks=[]; self.cur=None; self.typ=None
    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.cur = ""; self.typ = dict(attrs).get("type", "js") or "js"
    def handle_data(self, d):
        if self.cur is not None: self.cur += d
    def handle_endtag(self, tag):
        if tag == "script" and self.cur is not None:
            self.blocks.append((self.typ, self.cur)); self.cur = None
p = SP(); p.feed(html)
tmp = tempfile.mkdtemp(prefix="lexgate-")
js_blocks = []
n_ok = 0
for k, (t, c) in enumerate(p.blocks):
    if t == "application/json":
        continue
    if not c.strip():
        continue
    js_blocks.append(c)
    fp = os.path.join(tmp, f"b{k}.js"); open(fp, "w", encoding="utf-8").write(c)
    r = subprocess.run(["node", "--check", fp], capture_output=True, text=True)
    if r.returncode == 0:
        n_ok += 1
    else:
        first = (r.stderr or "").strip().splitlines()
        fails.append(f"node --check FAIL block{k}: {first[0] if first else '?'}")
        print(f"FAIL node --check block{k}: {first[0] if first else '?'}")
print(f"PASS node --check: {n_ok}/{len(js_blocks)} blocks ok")

# --- gate 3: DOM-stub smoke ---
smoke = r'''
const fs = require("fs");
const el = (tag) => {
  const e = {
    tag, children: [], style: {}, dataset: {}, classList: { add(){}, remove(){}, toggle(){}, contains(){return false} },
    attrs: {}, _listeners: {},
    setAttribute(k,v){ this.attrs[k]=String(v); }, getAttribute(k){ return this.attrs[k] ?? null; },
    appendChild(c){ this.children.push(c); return c; }, removeChild(c){ return c; },
    addEventListener(ev,f){ (this._listeners[ev]=this._listeners[ev]||[]).push(f); },
    removeEventListener(){}, querySelector(){ return null; }, querySelectorAll(){ return []; },
    focus(){}, blur(){}, click(){}, remove(){},
    getContext(){ return ctxStub(); },
    get innerHTML(){ return this._html||""; }, set innerHTML(v){ this._html=v; },
    get textContent(){ return this._tc||""; }, set textContent(v){ this._tc=String(v); },
    get value(){ return this._v||""; }, set value(v){ this._v=v; },
    get offsetWidth(){ return 1200; }, get offsetHeight(){ return 800; },
    get firstChild(){ return this.children[0]||null; },
  };
  return e;
};
const ctxStub = () => new Proxy({}, { get: (t,prop) => {
  if (prop === "canvas") return el("canvas");
  if (prop === "measureText") return () => ({ width: 10 });
  if (prop === "createLinearGradient" || prop === "createRadialGradient") return () => ({ addColorStop(){} });
  if (prop === "getImageData") return (x,y,w,h) => ({ data: new Uint8ClampedArray(w*h*4) });
  return () => {};
}, set: () => true });
const registry = new Map();
const getEl = (id) => { if (!registry.has(id)) registry.set(id, el("div")); return registry.get(id); };
const lexData = fs.readFileSync(process.argv[2], "utf-8");
registry.set("lex-data", Object.assign(el("script"), { textContent: lexData }));
global.document = {
  getElementById: (id) => (id === "lex-data" ? registry.get("lex-data") : getEl(id)),
  createElement: (t) => el(t), createTextNode: (t) => ({ nodeType: 3, nodeValue: t }),
  querySelector: (s) => getEl("qs:"+s), querySelectorAll: () => [],
  addEventListener: () => {}, body: el("body"), head: el("head"),
  documentElement: el("html"), readyState: "complete",
};
global.window = global; global.self = global;
global.addEventListener = () => {}; global.removeEventListener = () => {};
global.location = { hash: "", pathname: "/index.html", search: "", href: "http://localhost/index.html" };
global.history = { pushState(){}, replaceState(){}, back(){}, forward(){} };
global.scrollTo = () => {}; global.alert = () => {}; global.confirm = () => false; global.prompt = () => null;
global.navigator = { userAgent: "node-smoke", clipboard: { writeText: () => Promise.resolve() } };
global.localStorage = { _s:{}, getItem(k){ return this._s[k] ?? null; }, setItem(k,v){ this._s[k]=String(v); }, removeItem(k){ delete this._s[k]; } };
global.requestAnimationFrame = (f) => { return 1; }; global.cancelAnimationFrame = () => {};
global.matchMedia = () => ({ matches: false, addEventListener(){}, addListener(){} });
global.devicePixelRatio = 1; global.innerWidth = 1200; global.innerHeight = 800;
global.getComputedStyle = () => ({ getPropertyValue: () => "" });
global.MutationObserver = class { observe(){} disconnect(){} };
global.ResizeObserver = class { observe(){} disconnect(){} };
global.IntersectionObserver = class { observe(){} disconnect(){} };
global.AudioContext = class { createOscillator(){ return { connect(){}, start(){}, stop(){}, frequency:{value:0,exponentialRampToValueAtTime(){}} }; } createGain(){ return { connect(){}, gain:{value:0,linearRampToValueAtTime(){},setValueAtTime(){}} }; } get currentTime(){return 0;} get destination(){return {};} };
for (const f of process.argv.slice(3)) {
  const src = fs.readFileSync(f, "utf-8");
  try { new Function(src)(); console.log("LOADED", f); }
  catch (e) { console.error("THROW in", f, ":", e.message); process.exit(1); }
}
console.log("SMOKE PASS");
'''
smoke_path = os.path.join(tmp, "smoke.js")
open(smoke_path, "w", encoding="utf-8").write(smoke)
js_files = []
for k, (t, c) in enumerate(p.blocks):
    if t != "application/json" and c.strip():
        js_files.append(os.path.join(tmp, f"b{k}.js"))
block_json_path = os.path.join(tmp, "lex.json")
open(block_json_path, "w", encoding="utf-8").write(block)
r = subprocess.run(["node", smoke_path, block_json_path] + js_files, capture_output=True, text=True, timeout=60)
print(r.stdout.strip())
if r.stderr.strip():
    print("stderr:", r.stderr.strip()[:500])
if r.returncode != 0:
    fails.append(f"smoke runner exit {r.returncode}")

if fails:
    print("\n== GATE FAILURES ==")
    [print(" -", f) for f in fails]
    sys.exit(1)
print("\nALL GATES PASS")
