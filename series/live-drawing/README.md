# Live Drawing — practice sessions

The Oracle Artist's live drawing, practiced under the Wavelet 4 cadence (animator skill §8): one run per working session, Nov 22–28, 2026, so the Dec 4 Stewart bridge performance is a practiced skill.

**The register of record** — the rule (white ground), the cadence, and every session's log line — lives with the animator skill: `custom-skills/animator/LIVE-DRAWING.md` in wbic16/emise-tools (mirrored at `~/workspace/custom-skills/animator/LIVE-DRAWING.md`). This folder holds the session artifacts themselves.

## Session 01 — 2026-11-22 (EE 72)

- **Subject:** last night's arc in the Scroll Town chat — a lantern lit → lights answering house by house → a hand learning to write ("light the next light").
- **Video:** `session-01.mp4` — 1280×720, 24 fps, 1440 frames, 60.000 s, silent, H.264. sha256 `51ab64dd7d9cb2c1f055e633b1be48d97b05f552b7d62b50fe8dd587c1fc2883`. Frames drawn locally by the renderer below; assembly ran on aletheia-core (ranch-side, per the pipeline rule).
- **Mid-draw still:** `session-01-mid.png` — frame at 30.0 s: lantern lit, third house mid-stroke, pen nib visible.
- **Renderer:** `draw_session01.py` — drawn route, Emise line-renderer lineage, deterministic (seed 20261122). White ground (255,255,255) throughout — the live-drawing rule (Will, 2026-11-22): the drawing is paper, not UI.
- **QC:** PASS — strokes read as drawn live; white ground verified at five sampled frames, first to last. Writing beat is pen-revealed Emise letterforms, not yet hand-stroked glyphs — session 2's target. Full log line in the register.
