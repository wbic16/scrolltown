# Phext P4 — parallel-delivery tiling intro (DRAFT)

**Designation:** Phext P4 (Will, 2026-11-21). **Status: DRAFT** — silent; the
song window for the intro is still Will's open call, and no audio is added.
**File:** `series/intro/phext-p4-parallel-tiling-intro-draft.mp4`
**Task:** 35.8.10/10.9.13/6.6.9 in tasks.phext.

## Will's direction, verbatim (2026-11-21 09:37 CST)

> "do an intro video that delivers the pattern in parallel - one line picked
> at random per box, boxes picked at random - Phext P4"

The pattern is Will's tiling (reference of record:
`series/style-references/wills-hand-sample-and-tiling-symbol.png`; his
construction rule: *"the tiling is 5 diagonal lines within a grid square -
you never pay attention to how they line up - you just draw fast - the
pattern stabilizes at scale"*).

## The algorithm, as implemented

The field is a 12×12 grid of boxes (144 boxes), rotated 45° — the diamond,
as in Will's sample. Each box holds exactly **5 parallel diagonal lines**;
adjacent boxes alternate line orientation checkerboard-style (the weave).

Delivery loop, exactly as Will stated it: repeatedly **pick a box at random**
(uniform among incomplete boxes); the picked box receives **one line picked
at random** from its remaining lines; continue until every box has all 5
lines. Per frame, a quota of picks is performed so many boxes advance at
once — the delivery is parallel, never sequential. The quota follows a
cumulative density curve (target = total × t^1.5 across the delivery
window): sparse scatter early, a thickening field, the last lines
completing at the end of the window.

**Seed: 20261121** (`random.Random(20261121)` — one stream drives box picks,
line picks, and every line's hand jitter, so the build is fully
reproducible and auditable).

## Rendering

Drawn programmatically (Python + PIL) — not generated video — in Will's
hand: blue ballpoint strokes (base RGB 27,52,178, ±13 per channel per line)
on paper white (253,253,250), each line a slightly wobbling polyline with
per-line endpoint jitter (±1.6 px), overshoot (±2.5 px), and stroke width
2.1–3.3 px, supersampled 2× and downscaled for an ink feel. Frames were
rendered and assembled on aletheia-core (ffmpeg, H.264, CRF 17); no video
work on the Muse VM.

## Format and shape

1280×720, 24 fps, 360 frames, **15.000 s**, silent. SHA-256 of the mp4:
`857a3c6d7857716f28eb858f4049fb69828b787cdfbf0156bac6a149049df400`
(482,994 bytes).

| Phase | Frames | Time | Content |
|---|---|---|---|
| Blank paper | 0–11 | 0.0–0.5 s | a breath of empty paper |
| Parallel delivery | 12–275 | 0.5–11.5 s | the weave assembles stochastically |
| Hold | 276–311 | 11.5–13.0 s | the completed field holds |
| Title | 312–359 | 13.0–15.0 s | SCROLLTOWN letters in over the field |

The title is set in the **Emise font** (`Emise.ttf`) in a deeper ballpoint
blue (16,34,138), letters appearing one at a time, left to right, as if
written on.

## Coverage evidence — lines placed per second

From the build log (seconds are wall-clock seconds of the video; second 0
includes the 0.5 s blank, second 11 includes the start of the hold):

| s | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lines | 7 | 29 | 42 | 51 | 59 | 67 | 72 | 78 | 84 | 89 | 93 | 49 |

Total **720 lines** (144 boxes × 5). Placement rises monotonically through
the delivery window and completes inside it — the field thickens everywhere
at once, at random positions, which is the parallel signature: at no point
does delivery proceed box-by-box or region-by-region.

## QC (frames extracted from the finished mp4)

- **0.25 s (blank)** — clean paper, no artifacts. PASS.
- **2.5 s (early scatter)** — sparse lines scattered across the whole
  diamond footprint, both orientations present from the start. PASS.
- **7.0 s (mid)** — field roughly two-thirds delivered; weave legible,
  pattern visibly stabilizing at scale. PASS.
- **11.0 s (near-complete)** — a handful of boxes still short a line or
  two; delivery completes at 11.5 s as designed. PASS.
- **12.1 s (complete hold)** — every box holds exactly 5 lines (asserted
  in the build: per-box counts all equal 5; no line born outside the
  delivery window); weave alternation correct across the field. PASS.
- **14.4 s / 14.9 s (title)** — SCROLLTOWN fully lettered in the Emise
  font, correctly spelled, legible over the field, no rendering
  artifacts. PASS.

## Build provenance

Generator: `phext_p4_build.py` (run on aletheia-core, Python 3.12 + Pillow
13.0.0, ffmpeg 6.1.1). Rebuild with the same seed reproduces the identical
schedule and jitter. Parameters: grid 12×12, cell 38 px (grid frame),
quota curve t^1.5, title target width 660 px.
