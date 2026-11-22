# QC — Scrolltown weekly intro, 15-second prepass (current skill)

Task 24.7.8/9.7.11/7.8.12 · Arc sketch **22.6.9/8.6.10/7.6.9** ·
Packets 30.6.8/8.6.12/7.6.9 (intro-prepass.phext)
Video: intro-prepass-current-skill.mp4 — H.264, 854x480, 24 fps,
360 frames, duration 15.000000 s, silent, sha256
1294fb199ab7823910a7d640b244a1e84ae9633ea56fb42477f49c8bc4a552f1
(local copy byte-identical to the ranch assembly).
Renderer: draw_prepass.py, seeded 20261122, drawn route only —
no generative video or stills. All pages are ORIGINAL-DRAWN, so
the gate validator (repro pages) does not apply; the mechanical
checks for this dispatch are Velum's anchor enumeration and
Alveus's field verification.

## Packet returns

- IP-1 Theia (Aletheia Core) — RETURNED, verified: 360 frames
  rendered ranch-side, assembled ranch-side; ffprobe record meets
  the done-definition exactly (360 frames / 15.000 s / no audio).
- IP-2 Velum (Scroll Central) — RETURNED: anchors-enumeration.csv,
  240 frames checked (beats 1-2 every frame; beat 3 every 4th),
  zero unexamined frames in range.
- IP-3 Alveus (Rock Mountain) — RETURNED: field-verification.json,
  frames 340/350/359 sampled against the field manifest.

## Anchor enumeration (Velum, IP-2)

Beat 1 (96 frames): bun-l 96/96 · bun-r 78/96 · bow 95/96 ·
badge 95/96. Beat 2 (120 frames): bun-l 120/120 · bun-r 120/120 ·
bow 118/120 · badge 118/120 · Waverly streak 116/120 · coat
118/120. Beat 3 (24 sampled): bun-l 24/24 · bun-r 24/24 ·
bow 16/24 · badge 0/24 · streak 23/24 · coat 19/24.
Reading the misses: boundary misses sit on the warm-dip frames
(95/96/215), where the dip darkens every family at once. Beat 1's
bun-r misses are one run, frames 76-93: the raised lantern's peak
glow sits beside her head and washes the right bun out of the hair
color family — the bun is drawn (same primitives every page) but
does not READ under the glow. Beat 3's badge is drawn at ~2 px and
does not read at wide scale at all.

## Per-beat verdicts (Emise, from the contact sheet + enumeration)

- Beat 1 (Fern lifts her lantern) — PARTIAL. The held breath, the
  one eased lift, the answering window: the arc reads whole. The
  glow/bun-r readability loss (frames 76-93) is a named defect.
  Full-render fix: cap the glow peak and keep its center off her
  head, or rim the buns in ink weight the glow cannot wash.
- Beat 2 (Waverly unrolls the Great Scroll) — PASS at prepass
  grade. The unroll eases open; the drawn town lights house by
  house, ten houses in reading order, none going dark; anchors
  hold at 116/120 or better on every column.
- Beat 3 (pull wide, the town answers) — PARTIAL. The pull is a
  real drawn move (crop eases 0.46 -> 1.0, frames 224-280); the
  real windows answer in seeded waves and all are lit by frame
  300; the tower and the river read. Where the current staging
  stops: at wide scale the characters are specks — badge 0/24,
  bow 16/24 — present by construction, unreadable by enumeration.
- Beat 4 (title over the tiling field) — PARTIAL. SCROLLTOWN
  letters in, one per three frames from 324, Emise font, over the
  woven field; Alveus verifies parity alternation and finds
  428/500 lines at their manifest midpoints, 83/100 boxes complete
  at five lines. The misses are geometry, not weave: the diamond's
  half-diagonal (~325 px) exceeds the frame's half-height, so the
  corner boxes clip off-canvas, and the lit town strip occludes
  the lowest rows. Full-render fix: scale the field to fit
  (cell ~36) and raise the strip line.

## Prepass verdict

PASS as a prepass: the whole 15-second arc is present, in order,
at the sketch's timings, and judges whole — which is the only
thing a prepass is for. Two staging fixes and one honest limit
carry to the full render: glow discipline at the lift's climax,
a field scaled to its frame, and character identity at wide
scale (unresolved — the drawn route's current edge, stated
plainly rather than polished over).
