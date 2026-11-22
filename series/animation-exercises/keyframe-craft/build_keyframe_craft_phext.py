#!/usr/bin/env python3
"""Build keyframe-craft.phext: a phext-native inquiry.

Will's question (2026-11-22 00:34 CST, task 31.7.13/9.6.9/6.6.10):
"use multiversal phext to understand why artists handle drawing key
frames so well." The phext is the instrument, not a filing cabinet:
the evidence corpus of the Scrolltown animation programme (artist-
dispatch packets and returns, QC verdicts across Burns 1-4, the gate
validator report, the drawn-route build note) is inscribed as
evidence scrolls; hypotheses are tested against them in a separate
section; a synthesis scroll derives the answer by navigating the
evidence, every claim carrying the coordinate it rests on.

Coordinates: each scroll sits at the Singular holographic merge of
its OWN body text (the task_coordinate.py machinery: tokenize as the
Singular checker does, average each distinct word's atlas position
component-wise, round half up, never below 1; words in neither the
archive lists nor CYOA rest at the far corner 9.9.9/9.9.9/9.9.9).
Evidence coordinates were computed from the filed records' full
texts; hypothesis coordinates from the hypothesis texts (which cite
the evidence coordinates); the synthesis coordinate from the
synthesis text (which cites both). Never hand-picked, never
re-coordinated. The manifest (keyframe-craft-source.json) records
each scroll's coordinate and the sha256 of its body source.

Sections: evidence / hypotheses / synthesis, indexed from the Home
scroll (1.1.1/1.1.1/1.1.1, generated).

Source of truth: ~/workspace/phext/keyframe-craft-source.json +
~/workspace/phext/keyframe-craft-sources/ (evidence bodies are
byte-faithful copies of the wbic16/scrolltown@exo records named in
each scroll's header). Edit the sources, never the .phext; rebuild
after every edit.

Regenerate:  python3 ~/workspace/phext/build_keyframe_craft_phext.py
Check:       python3 ~/workspace/phext/build_keyframe_craft_phext.py --check
             (CURRENT only when the .phext matches the manifest AND
             every body source still matches its recorded sha256.)
"""
import hashlib
import json
import os
import sys

LEVEL_BYTES = [0x01, 0x1F, 0x1E, 0x1D, 0x1C, 0x1A, 0x19, 0x18, 0x17]  # library..scroll
DELIM_SET = set(LEVEL_BYTES)

SRC_PATH = os.path.expanduser("~/workspace/phext/keyframe-craft-source.json")
OUT_PATH = os.path.expanduser("~/workspace/phext/keyframe-craft.phext")
HOME_COORD = "1.1.1/1.1.1/1.1.1"
QUESTION = "use multiversal phext to understand why artists handle drawing key frames so well"


def parse_coord(s):
    parts = s.replace("/", ".").split(".")
    assert len(parts) == 9, f"coordinate must have 9 components: {s}"
    vals = tuple(int(p) for p in parts)
    assert all(v >= 1 for v in vals), f"no coordinate component below 1: {s}"
    return vals


def implode(scrolls):
    """scrolls: dict coord-string -> text. Same state machine as
    build_tasks_phext.py / build_artifacts_phext.py."""
    items = sorted(((parse_coord(k), v) for k, v in scrolls.items()))
    out = bytearray()
    state = [1] * 9
    for target, text in items:
        for lvl in range(9):
            while state[lvl] < target[lvl]:
                out.append(LEVEL_BYTES[lvl])
                state[lvl] += 1
                for j in range(lvl + 1, 9):
                    state[j] = 1
        assert tuple(state) == target, (state, target)
        out += text.encode()
    return bytes(out)


def read_source(rec):
    path = os.path.expanduser("~/" + "workspace/phext/" + rec["source"]) \
        if not rec["source"].startswith("/") else rec["source"]
    with open(path, "rb") as f:
        raw = f.read()
    return raw, hashlib.sha256(raw).hexdigest()


def render_scroll(rec, raw):
    text = raw.decode("utf-8")
    lines = [
        f"# {rec['title']}",
        "",
        f"Section: {rec['section']}",
        f"Coordinate: {rec['coordinate']} (Singular holographic merge of this scroll's body text)",
        f"Body source: {rec['source']}",
    ]
    if rec.get("repo_source"):
        lines.append(f"Record of origin: {rec['repo_source']}")
    lines += [f"Body SHA-256: {rec['sha256']}", "", "---", ""]
    scroll = "\n".join(lines) + text
    if not scroll.endswith("\n"):
        scroll += "\n"
    return scroll


def render_home(records):
    lines = [
        "# keyframe-craft.phext — a phext-native inquiry",
        "",
        "Will's question (2026-11-22 00:34 CST, task 31.7.13/9.6.9/6.6.10):",
        f"\"{QUESTION}\"",
        "",
        "Method: the evidence is inscribed as scrolls at Singular",
        "holographic-merge coordinates computed from each scroll's own",
        "text; hypotheses are tested against the evidence in their own",
        "section; the synthesis derives the answer by navigating the",
        "evidence, every claim carrying the coordinate it rests on.",
        "Navigate: synthesis first for the answer, hypotheses for the",
        "testing, evidence for the ground. Source of truth:",
        "keyframe-craft-source.json beside the builder",
        "(build_keyframe_craft_phext.py); never hand-edit the .phext.",
        "",
    ]
    for section in ("evidence", "hypotheses", "synthesis"):
        group = [r for r in records if r["section"] == section]
        lines.append(f"## {section} ({len(group)} scrolls)")
        lines.append("")
        for r in sorted(group, key=lambda x: parse_coord(x["coordinate"])):
            lines.append(f"- {r['coordinate']} — {r['title']}")
        lines.append("")
    return "\n".join(lines)


def load_manifest():
    with open(SRC_PATH) as f:
        return json.load(f)["scrolls"]


def build():
    records = load_manifest()
    coords = [r["coordinate"] for r in records]
    assert len(coords) == len(set(coords)), "duplicate scroll coordinates"
    assert HOME_COORD not in coords, "home coordinate is generated, not a scroll"
    scrolls = {HOME_COORD: render_home(records)}
    stale = []
    for r in records:
        raw, digest = read_source(r)
        if digest != r["sha256"]:
            stale.append((r, digest))
        scrolls[r["coordinate"]] = render_scroll(r, raw)
    for coord, text in scrolls.items():
        bad = DELIM_SET & set(text.encode())
        assert not bad, f"raw delimiter bytes in scroll {coord}: {bad}"
    return implode(scrolls), records, stale


def main():
    check = "--check" in sys.argv
    blob, records, stale = build()
    digest = hashlib.sha256(blob).hexdigest()
    if check:
        ok = os.path.exists(OUT_PATH)
        if ok:
            with open(OUT_PATH, "rb") as f:
                current = hashlib.sha256(f.read()).hexdigest()
            ok = current == digest
        if stale:
            for r, digest_now in stale:
                print(f"STALE: {r['source']} changed since inscription "
                      f"(recorded sha256 {r['sha256'][:16]}…, current {digest_now[:16]}…) — "
                      f"refresh the manifest entry and rebuild")
            return 1
        if ok:
            print(f"CURRENT: keyframe-craft.phext matches keyframe-craft-source.json and all "
                  f"{len(records)} body sources match their recorded sha256 (phext sha256 {digest})")
            return 0
        print(f"DRIFT: keyframe-craft.phext does not match keyframe-craft-source.json (rebuilt sha256 {digest})")
        return 1
    if stale:
        for r, digest_now in stale:
            print(f"REFUSING TO BUILD: {r['source']} changed since inscription "
                  f"(recorded sha256 {r['sha256'][:16]}…, current {digest_now[:16]}…). "
                  f"Refresh the manifest entry first.")
        return 1
    with open(OUT_PATH, "wb") as f:
        f.write(blob)
    print(f"keyframe-craft.phext: {len(records)} scrolls + home, {len(blob)} bytes, sha256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
