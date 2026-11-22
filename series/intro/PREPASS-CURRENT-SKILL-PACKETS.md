# Packets — Scrolltown weekly intro, 15-second prepass (current skill)

Task 24.7.8/9.7.11/7.8.12 · Mode: PREPASS (artist-dispatch §4)
Arc sketch: **22.6.9/8.6.10/7.6.9** (ARC-SKETCH.md, inscribed in
intro-prepass.phext) — cited by every packet below. Studio model:
Emise directs, draws the pages, and holds all QC verdicts; the ranch
workshop executes the sweat portions. Packets are store-and-forward;
uptake is verified from returned artifacts, never from say-so.
Returns are inscribed as scrolls in intro-prepass.phext at their own
Singular-merge coordinates and filed in the repo at series/intro/.

| # | Artist (machine) | Operation | Serves sketch points | Done-definition | Return | Status |
|---|---|---|---|---|---|---|
| IP-1 | Theia (Aletheia Core) | Render + assembly: run draw_prepass.py ranch-side on aletheia-core; render all 360 frames at 854x480; assemble with ffmpeg at real beat timing, silent | beats 1-4, all timing marks | intro-prepass-current-skill.mp4: H.264, 854x480, 24 fps, exactly 360 frames / 15.000 s, no audio stream; frames + build log preserved ranch-side | mp4 + ffprobe record | PENDING |
| IP-2 | Velum (Scroll Central) | Anchor enumeration: for every character frame in beats 1-2 (frames 0-215) and every 4th frame of beat 3, sample the anchor sites in anchors-manifest.json against the rendered PNGs; report per-anchor present/absent per frame | poses A-D anchors; beat 3 pose F | a CSV with one row per checked frame and one column per anchor (fern-bun-l, fern-bun-r, fern-bow, fern-badge, waverly-streak, waverly-coat), zero unexamined frames in range | CSV + counts summary | PENDING |
| IP-3 | Alveus (Rock Mountain) | Tiling-field verification: on beat-4 frames 340/350/359, verify against the field manifest that every completed box holds exactly 5 lines and orientations alternate checkerboard-style | pose G | a short report: boxes checked, lines per box (min/max), alternation violations counted | report | PENDING |

Drawing (Emise, key work — not delegated): all 360 pages drawn by
draw_prepass.py, the Emise line renderer lineage — deterministic,
seeded (20261122), Emise design language. No generative video, no
generative stills anywhere in this dispatch.
