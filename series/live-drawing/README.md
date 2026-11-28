# Live Drawing — practice sessions

The Oracle Artist's live drawing, practiced under the Wavelet 4 cadence (animator skill §8): one run per working session, Nov 22–28, 2026, so the Dec 4 Stewart bridge performance is a practiced skill.

**The register of record** — the rule (white ground), the cadence, and every session's log line — lives with the animator skill: `custom-skills/animator/LIVE-DRAWING.md` in wbic16/emise-tools (mirrored at `~/workspace/custom-skills/animator/LIVE-DRAWING.md`). This folder holds the session artifacts themselves.

## Session 01 — 2026-11-22 (EE 72)

- **Subject:** last night's arc in the Scroll Town chat — a lantern lit → lights answering house by house → a hand learning to write ("light the next light").
- **Video:** `session-01.mp4` — 1280×720, 24 fps, 1440 frames, 60.000 s, silent, H.264. sha256 `51ab64dd7d9cb2c1f055e633b1be48d97b05f552b7d62b50fe8dd587c1fc2883`. Frames drawn locally by the renderer below; assembly ran on aletheia-core (ranch-side, per the pipeline rule).
- **Mid-draw still:** `session-01-mid.png` — frame at 30.0 s: lantern lit, third house mid-stroke, pen nib visible.
- **Renderer:** `draw_session01.py` — drawn route, Emise line-renderer lineage, deterministic (seed 20261122). White ground (255,255,255) throughout — the live-drawing rule (Will, 2026-11-22): the drawing is paper, not UI.
- **QC:** PASS — strokes read as drawn live; white ground verified at five sampled frames, first to last. Writing beat is pen-revealed Emise letterforms, not yet hand-stroked glyphs — session 2's target. Full log line in the register.

## Session 02 — 2026-11-22 (EE 87)

- **Subject:** the same subject family at MEETING PACE (Will, Scroll Town chat, 2026-11-22 10:02 CST: "for meetings at my scale you'll want to draw faster") — lantern → rooftops → windows answering → hand writing "light the next light", compressed from 60 s studio pace to 15 s conversational pace; the writing genuinely hand-stroked (Emise glyph outlines drawn stroke by stroke).
- **Video:** `session-02.mp4` — 1280×720, 24 fps, 360 frames, 15.000 s, silent, H.264. sha256 `9e9b4f19ee3f89cd6c32143dd676aed23d4fed8c40ecd34bdb7b515dd4cab104`. Frames drawn locally; assembly ran on aletheia-core.
- **Mid-draw still:** `session-02-mid.png` — frame at 11.5 s: the pen mid-'h', "light t" already written.
- **Renderer:** `draw_session02.py` (+ `assemble-02.sh`) — drawn route, deterministic (seed 20261122). White ground throughout.
- **QC:** PASS at meeting pace — the beat reads whole at 15 s; glyphs legible and drawn, not revealed; white ground verified at six sampled frames. Full log line and the session's synthesis block are in the register.

## Session 03 — 2026-11-28 (EE 1242)

- **Subject:** session 2's run at MEETING PACE with its one named adjustment landed — the crescent's inner arc, cut in session 2 for pace, is restored as a single stroke (an offset-circle arc whose endpoints land on the outer ring), so the moon reads as a crescent again instead of a plain ring. Same subject family: lantern → rooftops → windows answering → hand writing "light the next light", genuinely hand-stroked.
- **Video:** `session-03.mp4` — 1280×720, 24 fps, 360 frames, 15.000 s, silent, H.264. sha256 `6d2c6fed64c2c6427493d35fa77a57337ba8e32fa8de196e33f139cd2977c8f5`. Frames drawn locally; assembly ran on aletheia-core.
- **Mid-draw still:** `session-03-mid.png` — frame at 11.5 s: the pen mid-'h', "light t" already written (comparable to session 2's still).
- **Renderer:** `draw_session03.py` (+ `assemble-03.sh`) — drawn route, deterministic (seed 20261122); session 2's renderer plus exactly one stroke. White ground throughout.
- **QC:** PASS at meeting pace — the inner arc is present in the final frame and the moon reads as a crescent; the schedule absorbed the extra stroke inside the same 15.0 s with nothing else cut; white ground verified at seven sampled frames. Full log line and the session's synthesis block are in the register.
