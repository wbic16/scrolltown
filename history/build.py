#!/usr/bin/env python3
"""Build the History archive site from manifest.txt.

Idempotent: regenerates history/site/ whole from the manifest plus the
media files the manifest points at. Media sources resolve, in order:
  1. paths relative to the scrolltown repo root (this script's ../..),
  2. paths relative to --media-root DIR (a checkout or clone of the repo).
Each media file's SHA-256 is computed; if the manifest records a sha256
it must match, otherwise the build fails rather than publishing an
unverified render. Posters are copied the same way (unhashed).

Usage: python3 build.py [--media-root DIR] [--fill-hashes]
  --fill-hashes  write computed sha256 values back into manifest.txt
                 (first build only; afterwards hashes are verified).
"""
import hashlib, html, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
GROUPS = [
    ("burns", "The Burns", "Four burns of generated clips, learning what the generator actually does — each verdict from frame evidence."),
    ("gates", "The Gates", "The toll gates: full reproductions of public-domain films, in order. A gate passes only on a prepass plus a full render, frame-compared."),
    ("intro", "The Intro", "Studies toward the Scrolltown intro — hand-drawn repros, the tiling field, and the current skill, drawn end to end."),
    ("live", "Live Drawing", "A conversation, drawn in real time on white paper — practiced every session of Wavelet 4 for the Dec 4 performance. Each drawing keeps its white ground inside the picture itself."),
]

def parse_manifest(path):
    entries, cur = [], None
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        if line.strip() == "---":
            if cur: entries.append(cur)
            cur = {}
            continue
        if cur is None or not line.strip() or line.lstrip().startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            cur[k.strip()] = v.strip()
    if cur: entries.append(cur)
    return [e for e in entries if e.get("id")]

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def resolve(rel, roots):
    for r in roots:
        p = os.path.join(r, rel)
        if os.path.isfile(p):
            return p
    return None

CSS = """
:root{color-scheme:light}
html[data-theme="dark"]{color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;font-family:Georgia,'Times New Roman',serif;line-height:1.6;background:#FFFBF0;color:#2C2019}
html[data-theme="dark"] body{background:#20160F;color:#F3E7D3}
header,main,footer{max-width:880px;margin:0 auto;padding:0 20px}
header{padding-top:36px}
h1{font-size:2rem;margin:0 0 4px}
.sub{font-style:italic;margin:0 0 8px;opacity:.85}
.counts{font-size:.9rem;opacity:.75}
.hero{width:100%;border-radius:10px;margin:18px 0 4px}
.hero-cap{font-size:.85rem;opacity:.7;margin:0 0 10px}
h2{margin:42px 0 2px;font-size:1.45rem}
.gsub{margin:0 0 18px;opacity:.8;font-style:italic}
article{border:1px solid rgba(128,100,60,.35);border-radius:12px;padding:18px;margin:0 0 22px;background:rgba(255,255,255,.35)}
html[data-theme="dark"] article{background:rgba(255,255,255,.04)}
article h3{margin:0 0 2px;font-size:1.15rem}
.meta{font-size:.88rem;opacity:.75;margin:0 0 10px}
.chip{display:inline-block;font-weight:bold;font-size:.78rem;letter-spacing:.06em;padding:2px 9px;border-radius:999px;border:1.5px solid currentColor;vertical-align:middle;margin-left:8px}
.v-PASS{color:#1E7A34}.v-PARTIAL{color:#9A6A00}.v-FAIL{color:#B3261E}.v-DRAFT{color:#5B5BD6}
html[data-theme="dark"] .v-PASS{color:#7BD88F}html[data-theme="dark"] .v-PARTIAL{color:#E8C268}html[data-theme="dark"] .v-FAIL{color:#F28B82}html[data-theme="dark"] .v-DRAFT{color:#A5A5F5}
video{width:100%;border-radius:8px;background:#000}
img.poster{width:100%;border-radius:8px;display:block;margin:0 0 10px}
.refl{margin:10px 0 0}
.refl b{font-variant:small-caps;letter-spacing:.04em}
button#theme{float:right;font:inherit;font-size:.85rem;padding:4px 12px;border-radius:999px;border:1px solid currentColor;background:transparent;color:inherit;cursor:pointer}
footer{padding:26px 20px 40px;font-size:.88rem;opacity:.75}
a{color:inherit}
"""

JS = """
(function(){var k='history-theme';try{var t=localStorage.getItem(k);if(t){document.documentElement.dataset.theme=t}}catch(e){}
document.getElementById('theme').addEventListener('click',function(){var cur=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=cur;try{localStorage.setItem(k,cur)}catch(e){}});})();
"""

def main():
    args = sys.argv[1:]
    media_root = None
    fill = "--fill-hashes" in args
    if "--media-root" in args:
        media_root = args[args.index("--media-root") + 1]
    roots = [os.path.abspath(os.path.join(HERE, "..", ".."))]
    if media_root: roots.insert(0, os.path.abspath(media_root))
    manifest_path = os.path.join(HERE, "manifest.txt")
    entries = parse_manifest(manifest_path)
    site = os.path.join(HERE, "site")
    media_out = os.path.join(site, "media")
    if os.path.isdir(site): shutil.rmtree(site)
    os.makedirs(media_out)

    filled = {}
    for e in entries:
        src = resolve(e["media"], roots)
        if not src:
            print(f"FAIL: media not found for {e['id']}: {e['media']}"); sys.exit(1)
        digest = sha256_of(src)
        recorded = e.get("sha256", "")
        if recorded and recorded != digest:
            print(f"FAIL: sha256 mismatch for {e['id']}: manifest {recorded} != file {digest}"); sys.exit(1)
        if not recorded: filled[e["id"]] = digest
        e["_file"] = os.path.basename(e["media"])
        shutil.copyfile(src, os.path.join(media_out, e["_file"]))
        if e.get("poster"):
            psrc = resolve(e["poster"], roots)
            if not psrc:
                print(f"FAIL: poster not found for {e['id']}: {e['poster']}"); sys.exit(1)
            e["_poster"] = os.path.basename(e["poster"])
            shutil.copyfile(psrc, os.path.join(media_out, e["_poster"]))
    # canonical Fern reference anchors the archive header
    fern = resolve("series/fern-reference.png", roots)
    if fern: shutil.copyfile(fern, os.path.join(media_out, "fern-reference.png"))

    if fill and filled:
        lines = open(manifest_path, encoding="utf-8").read().split("\n")
        cur = None; out = []
        for line in lines:
            if line.startswith("id="): cur = line[3:].strip()
            if line.strip() == "sha256=" and cur in filled:
                line = "sha256=" + filled[cur]
            out.append(line)
        open(manifest_path, "w", encoding="utf-8").write("\n".join(out))
        print(f"filled {len(filled)} hashes into manifest.txt")

    counts = {}
    for e in entries: counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1
    count_line = " · ".join(f"{counts[v]} {v.lower()}" for v in ("PASS", "PARTIAL", "FAIL", "DRAFT") if v in counts)
    parts = []
    parts.append("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
                 "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
                 "<title>History — the Scrolltown renders</title>\n"
                 "<meta name=\"description\" content=\"A living archive of the Scrolltown animation programme's renders — every burn, gate, and live drawing, with what it taught us.\">\n"
                 f"<style>{CSS}</style>\n</head>\n<body>\n<header>\n"
                 "<button id=\"theme\" type=\"button\">Light / dark</button>\n"
                 "<h1>History — the Scrolltown renders</h1>\n"
                 "<p class=\"sub\">This archive is the show's memory: every render we have made, kept with its verdict and what it taught us, so we can reflect back on how the work learned.</p>\n"
                 f"<p class=\"counts\">{len(entries)} renders · {count_line}</p>\n")
    if fern:
        parts.append("<img class=\"hero\" src=\"media/fern-reference.png\" alt=\"Fern, the Keeper — the canonical reference every render is checked against\">\n"
                     "<p class=\"hero-cap\">Fern, the Keeper — the canonical reference. Every render in this archive is judged against her, never against the last render.</p>\n")
    parts.append("</header>\n<main>\n")
    for gid, gtitle, gsub in GROUPS:
        group = [e for e in entries if e["group"] == gid]
        if not group: continue
        parts.append(f"<section>\n<h2>{html.escape(gtitle)}</h2>\n<p class=\"gsub\">{html.escape(gsub)}</p>\n")
        for e in group:
            meta = e["date"] + (f" · {e['ee']}" if e.get("ee") else "")
            parts.append("<article>\n"
                         f"<h3>{html.escape(e['title'])}<span class=\"chip v-{e['verdict']}\">{e['verdict']}</span></h3>\n"
                         f"<p class=\"meta\">{html.escape(meta)}</p>\n")
            poster = f" poster=\"media/{e['_poster']}\"" if e.get("_poster") else ""
            parts.append(f"<video controls preload=\"metadata\"{poster} src=\"media/{e['_file']}\"></video>\n")
            if e.get("reflection"):
                parts.append(f"<p class=\"refl\"><b>What we learned —</b> {html.escape(e['reflection'])}</p>\n")
            parts.append("</article>\n")
        parts.append("</section>\n")
    parts.append("</main>\n<footer>\n<p>Scrolltown — a town inside the Great Scroll. New episodes every Saturday from January 2, 2027. This archive grows by procedure: every new render is added to the manifest and the page is rebuilt — it is never edited by hand. No tracking, nothing external, collects nothing.</p>\n</footer>\n"
                 f"<script>{JS}</script>\n</body>\n</html>\n")
    open(os.path.join(site, "index.html"), "w", encoding="utf-8").write("".join(parts))
    total = sum(os.path.getsize(os.path.join(media_out, f)) for f in os.listdir(media_out))
    print(f"built site/: {len(entries)} entries, media {total} bytes, index {os.path.getsize(os.path.join(site,'index.html'))} bytes")

if __name__ == "__main__":
    main()
