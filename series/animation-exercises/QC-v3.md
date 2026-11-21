# QC — Iteration 2 (Burn 3), 2026-11-21

Frame-level QC for the second Oracle Artist burn. Method: every clip probed
(ffprobe) and read by frames before any verdict — sparse quintiles
(start/q1/mid/q3/end) for character clips, dense 0.5 s sampling for the two
physics rungs, and per-frame enumeration where a packet demanded it.
Done-definitions are the animator skill §2 wordings. Verdicts:
Pass / Partial / Fail, with the evidence named. Files: clips at this folder's
root; frames in `qc3/`; sweat-batch returns in `batch-2.1/` and `batch-2.2/`;
packets in `PACKETS.md`. Full narrative: the animator skill's ITERATIONS.md,
Iteration 2.

## Probes (all ranch-verified)

| clip | size | fps | frames | duration |
|---|---|---|---|---|
| ex03-fern-at-the-ready-v3.mp4 | 1152×768 | 24 | 120 | 5.00 s |
| ex02-keepers-welcome-v3.mp4 | 1248×704 | 24 | 120 | 5.00 s |
| ex02-pendulum.mp4 | 1152×768 | 24 | 240 | 10.00 s |
| ex01-bouncing-ball-v2.mp4 | 1152×768 | 24 | 240 | 10.00 s |
| probe-two-keyframe-ignition.mp4 | 1152×768 | 24 | 120 | 5.00 s |

All five clips are silent (no audio stream). Requested durations were
honoured this burn (5 s asks returned 5.0 s; 10 s asks returned 10.0 s) —
against Iteration 1's mixed behaviour; duration stays advisory in the skill.

## ex03-fern-at-the-ready v3 — the arm-only test — **Fail**

Hypothesis: with anticipation language removed entirely and motion restricted
to the hammer arm (body, head, hair, feet explicitly held; start pose = end
pose), both the gesture and the identity anchors survive.

Evidence (`qc3/ex03-v3-*.png`): the camera never moved — framing identical at
start/q1/mid/q3/end. The gesture LANDED: at q1 the hammer is rising; at mid it
is raised beside her head; at end it is back down — start pose = end pose,
left arm, body, head and feet unmoved throughout, exactly as specified. But
the hair re-drew anyway: the smooth twin scroll-buns are already curling at
q1 (t≈1.25 s) and are full tight curls at mid and end. And the end frame
carries an un-named expression — eyes closed, pleased grin — where the prompt
named her gentle smile.

Verdict reasoning: the rung's identity clause fails (buns are an anchor;
§4: a frame missing an anchor fails QC outright). The hypothesis splits:
motion restriction is CONFIRMED for gesture and camera, REFUTED for identity —
any motion of the character herself, even one arm with the head held still,
triggers the hair re-draw. Anchors hold only when the character is fully
still and the motion is in the world around her (see Batch 2.1's enumeration
and the probe's endpoints).

## ex02-keepers-welcome v3 — design for the push-in — **Partial**

Hypothesis: with Waverly at ≤⅕ of frame height in the key (new xwide still,
`qc3/stills/waverly-xwide-still.webp` — figure ≈1/6–1/7 of frame height), the
inevitable push-in lands somewhere good; verdict judged on the END framing.

Evidence (`qc3/ex02-v3-*.png`): the push-in was total — from the wide street
to a face-filling close-up, complete by mid-clip. Register held: painterly in
every sampled frame, no photoreal morph (Burn 1's failure did not recur), and
Waverly at the landing is on-model (gold streak, plum coat, apron tools). The
end framing is, as a found composition, warm and handsome. BUT the landing
was invented, not designed: the rolled scroll she holds in the key is an
unrolled scroll covered in pseudo-writing by mid-clip — a text-bearing prop
the key never contained. The prompt's "start and end on this same wide
composition" was not honoured in any frame after the first seconds.

Verdict reasoning: designing for the push-in survives as doctrine (judge the
landing, not the zoom), refined: the landing is a FOUND composition and must
pass its own QC — its characteristic defect is invented props, especially
text-bearing ones. As the ex02 rung (two believable micro-motions, on-model),
the clip fails the micro-motion clause — the camera move consumed the shot.

## ex02-pendulum (NEW rung) — **Partial** (closest to a pass this programme)

Key: new lantern still (`qc3/stills/pendulum-lantern-still.webp`) — lantern
hanging still and vertical on a short chain, face-free.
Done-definition (§2 ex02): swing decays by easing, not uniform steps;
overshoot settles through two diminishing arcs; a frame chart shows spacing
clustered at the extremes.

Evidence (`qc3/pendulum-dense-sheet.png`, 0.5 s sampling, 20 frames): the
lantern swings through three arcs of visibly diminishing amplitude (largest
≈t1.0 s, smaller ≈t3.5 s, smallest ≈t6.0 s), is near-vertical from t7.0 s,
and hangs still at center for the final ~2.5 s. Camera static in all 20
frames; register painterly throughout; flame lit the whole time. The
spacing-at-extremes clause could NOT be settled: a brightness-centroid track
(240 frames, ranch-side) was contaminated by the houses' lit windows inside
the tracking region (detected "extremes" include artifacts; spacing ratio
0.82 is suggestive only and is NOT claimed). Silhouette/template tracking is
the Iteration 3 re-measurement; no new generation is needed.

Verdict reasoning: swing, decay-by-easing, two diminishing overshoots, and
settle are frame-verified; one clause of three unverified ⇒ Partial.

## ex01-bouncing-ball v2 — wood only — **Fail**

Hypothesis: a single-material burn (wood token only) plus dense sampling
settles the two clauses Iteration 1 left unverified (decaying multi-bounce;
contact-frame squash).

Evidence (`qc3/bball2-dense-sheet.png`): the key still (Iteration 1's
counting-token still) contains the full prop set — and the generator animated
a DUPLICATE: a second wooden token appears mid-air at t0.5 s and performs the
bounces while the key's own token never moves. The bounce series does not
decay monotonically either: the token settles ≈t4.0 s, re-launches to full
height at t5.0–5.5 s, bounces again, and settles ≈t8.5 s. Contact squash
remains unverified at 0.5 s sampling (one motion-blurred contact ≈t6.0 s is
suggestive, not evidence).

Verdict reasoning: single-token and decay clauses fail on dense evidence.
Basis vector indicted is the KEY, not the generator: a multi-prop still is
not a single-object key. Iteration 3 re-keys with a dedicated still — the
wood token alone on a bare counter — and tracks contacts by silhouette.

## Two-keyframe route probe — **Partial**

Route: START = the filed Fern+Waverly duo keyframe draft (lantern raised,
scroll partly unrolled); END = ex01-ignition-v2's end frame (town lit).
Question: does a named START + named END honour both endpoints better than
single-still animation?

Evidence (`qc3/probe-*.png`): frame 0 IS the start still, exactly. The end
frame delivers the end still's CONTENT — scroll fully unrolled, whole town
lit, both keepers holding its edges, Fern's lantern still raised, all anchors
intact (buns smooth, streak, plum coat) — but it is a new drawing in the end
still's spirit, not the end frame itself: tighter framing (a mild push-in),
and both faces carry un-named closed-eye contented smiles. Identity held at
both endpoints because both characters hold near-static poses (consistent
with the ex03 v3 refinement).

Verdict reasoning: the route honours the start exactly and the end
thematically. It is NOT yet pose-to-pose control and must not be budgeted as
the gesture fix until an end-frame-exact result exists.

## Batch 2.1 — per-frame packet on ex01-ignition-v2 (Velum) — returned

Full packet in `PACKETS.md`. Returns in `batch-2.1/`:

- **Frames 000–059, composition-offset measurement** (`offsets-000-059.csv`):
  phase correlation against frame 000 gives translation dx = 0 px on all 60
  frames and |dy| ≤ 2 px. The reframing Burn 2 reported is NOT a translation.
  A scale measurement (`scale-000-059.txt`, best-fit scale by template
  correlation) reads 1.00 through frame ~025 and 1.04 from frame ~030 on: the
  reframing is a ≈4 % push-in completing by ≈frame 030, then stable.
- **Counter-crop conform** (`corrected-000-059.mp4`): the conform was applied
  with the measured offsets; because the measured translation is ≈0, the
  corrected frames are the originals to within 2 px — recorded honestly: the
  conform had nothing to correct; the residual defect is scale, which a crop
  conform cannot undo without re-rendering the frame edges.
- **Frames 060–239, identity-anchor verification** (`anchors-060-239.csv`,
  sheets in `batch-2.1/sheets/`, per-character crops in
  `batch-2.1/cropsheets/`): ENUMERATED, all 180 frames read individually —
  Fern buns 180/180, Fern scarf bow 180/180, Fern key-badge 180/180, Waverly
  gold streak 180/180, Waverly plum coat 180/180. Eyelid blinks noted in the
  table (Fern ≈098–100, ≈163–165, ≈192–194; Waverly ≈060–062, ≈162–165,
  ≈185–188) are motion, not anchor loss. Bar §8(iii)'s evidence is upgraded
  from sampled to enumerated for the near-static case.

## Batch 2.2 — variant stills, intro keyframes 5–8 (Alveus) — returned as DRAFTS

Four variant stills seeded from the canonical Fern reference, one per
FERN-KEYFRAMES-MJ.md frame 5–8, in `batch-2.2/` with `LIK
...[truncated 768 chars]