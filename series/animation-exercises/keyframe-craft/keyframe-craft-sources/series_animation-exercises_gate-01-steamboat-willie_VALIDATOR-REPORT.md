# Gate Validator — Report: Gate 1 (Steamboat Willie) prepass, all 60 pages

_Built and run 2026-11-21 under task 21.6.7/8.5.10/5.5.6, on Will's order
("Steamboat Willie doesn't look good yet - you need a validtor"). QC-v4 had
checked this prepass by sampled visual frame-compare at 12 timestamps; Will
saw the result and judged it not good enough. This validator is the missing
instrument: it checks EVERY page against its matched original frame,
mechanically and structurally. Run ranch-side on aletheia-core
(`~/anim-i2-work/venv` python: numpy + PIL), against the reference copy of
record (archive.org `steamboat-willie_1928`, sha256 18a57a97…) and the
page/frame pairing in `plan.json` + `shotframes2/`. Scores of record:
`validator-scores.json` beside this report. Gate 1's gate status is
unchanged: NOT PASSED (full render outstanding)._

## Verdict summary

**30 PASS · 30 FLAG** of 60 pages.
FLAG by failure class (a page can carry several): **edges
10 · ink 29 ·
components 2 · title
2**. The flagged pages are Iteration 4's
re-draw queue (`REDRAW-QUEUE.md`).

The headline finding, sharper than the sampled QC could see: **the
renderer's answer to a solid-black region is a flat wash at luminance
≈ 205 with essentially no ink inside it** — eroded-interior ink density
measures 0.00 on all 60 pages, and whole-region ink-in-black runs
0.0004–0.14. QC-v4 described "wash + hatch"; mechanically it is wash
*instead of* hatch inside solids. That is why the film doesn't look good
yet: Mickey's and Pete's silhouettes — the film's whole graphic weight —
are the thing the prepass most consistently fails to draw.

## What the validator measures (structure, not pixels)

Working canvas 1040×864 (the pages' own size; originals resampled onto it).

- **(a) Edges.** The original is reduced to a strong-edge map (gradient
  magnitude, blurred, top band); the repro's ink strokes are its contours.
  *Coverage* = fraction of the original's strong edges within 4 px
  (Chebyshev) of repro ink; *Chamfer* = symmetric mean clipped distance
  (clip 16 px).
- **(b) Ink mass.** Per-cell (8×6) ink-density comparison (diagnostic),
  plus two gating tests: the ink log-ratio |log2(repro ink / original ink)|
  — original ink counted below the film's own gray wash (lum < 90) — applied
  only where the original demands ink (ink fraction ≥ 0.045);
  and the demand test: where the original is ≥ 0.08
  near-black, the repro's ink density inside that black must reach
  0.015.
- **(c) Components, figure band.** Components ≥ 100 px at half
  resolution, the original's near-black solids vs the repro's ink; only the
  extreme log-ratio bounds gate (merging > +1.0,
  shattering < −2.5).
- **(d) Title/lettering pages** (shot 0 and shot 54, the two cards) are
  auto-FLAGGED for human review regardless of score. The validator does not
  pretend to judge letterforms.

## Thresholds of record

| Measure | Bound | | Measure | Bound |
|---|---|---|---|---|
| edge coverage | ≥ 0.72 | | ink log-ratio | ≤ 2.2 (demand-gated) |
| chamfer (px) | ≤ 2.2 | | ink-in-black | ≥ 0.015 at black-demand ≥ 0.08 |
| figure log-ratio | −2.5 … +1.0 | | title pages | always FLAG |

## Acceptance test — the validator, validated

Calibration sets fixed BEFORE the final run, from QC-v4's recorded
observations and the arc sketch: CLEAN = pages QC frame-compare matched
compositionally in wide/static shots (01, 02, 03, 31, 37, 39, 40);
WEAK-TITLE = the two cards (00, 54); WEAK-INK = the highest solid-black
demand character pages (16, 17, 18, 19, 44 — original near-black fraction
0.22–0.44); WEAK-BLOB = the mid-motion pages whose contours collapse
(43, 45p0, 45p1, 22).

- **CLEAN: 7/7 PASS.** Every clean page clears every measure.
- **WEAK-TITLE: 2/2 FLAG** (title rule; both also fail ink — the cards'
  black grounds measure ink-in-black 0.0073 and 0.0004).
- **WEAK-INK: 5/5 FLAG (ink).** Separation is explicit and wide:
  ink log-ratio, weak minimum 3.14 vs clean maximum
  1.68; ink-in-black, weak maximum 0.0156 vs
  clean minimum 0.0276. No overlap on either instrument.
- **WEAK-BLOB: 4/4 FLAG** (edges; three also ink). Separation: coverage,
  weak maximum 0.665 vs clean minimum 0.891;
  Chamfer, weak minimum 2.23 vs clean maximum
  1.12. No overlap.

**Acceptance: PASS.** The pages QC already knew were weak score below the
clean pages on the instruments aimed at their failure class, with margins,
and no clean page is flagged.

Two honest qualifications, on the record:

1. **Two component formulations were tried and rejected on evidence**
   before the figure-band bounds above were adopted: total-ink component
   shares (the original film's ink percolates into a single component —
   largest-share 0.87–0.99 even on clean pages — so the comparison read
   the film's grain) and edge-component counts/shares (clean log-ratio
   range −1.95…−0.54 vs weak −2.44…+0.52: overlap). On line art, component
   counts read stroke connectivity — the renderer's texture — not figure
   merging. The merged-figure failure is therefore carried by the edges
   measure, mechanistically: merging destroys the original's contours,
   and coverage collapses. The surviving component gate catches the
   opposite failure — a solid shattered into stroke confetti — and fires
   on pages 11 and 17 (Pete), corroborating their ink flags.
2. **The midpoint hypothesis was tested and not supported.** The p1
   midpoint pages of long concert shots (36p1, 41p1, 50p1) were suspected
   blobby; mechanically they are sound (coverage 0.87–0.88) and PASS.
   The blobby pages are the fast gag pages around them. QC-v4's
   "occasional mid-motion pages" is hereby pinned to specific pages:
   21, 22, 23, 42, 43, 44, 45p0, 45p1, 47, 53 (the edges class).

Beyond the calibration sets, the validator extends QC's sample: pages
24, 25, 27, 28 (landing/hoist — composition-matched at QC's t=128/152)
fail ink, as do 09, 13, 15, 20, 26, 29, 49, 50p1, 51p1. Composition was
never their problem; ink is. That is the instrument doing the job it was
built for.

## Coverage gap found while pairing

Shot 0 (0–14.2 s) holds TWO cards — the main title and the STEAMBOAT
WILLIE card — but the prepass has a single page for it (page00, t=0.6),
held across both in the animatic. The second card was never drawn. It is
item T-3 in the re-draw queue.

## The standing rule (Will's direction, from this build)

**No repro page enters an assembly — flipbook, full render, any future
intro — unless it validator-PASSes or carries a human-review flag
resolution recorded beside its score.** The MCU flipbook draft already
shipped drew its Gate 1 pages before this rule existed; any re-cut
follows the rule.

## The standard the re-draws are executed under

Re-draws are key frames authored in the **Emise design language** (Will,
2026-11-21): drawn work in the Emise line — the Emise font's flowing,
sharp line evolved from Willbot / Will's handwriting, the fast-hand stroke
character of Will's tiling-symbol reference (jitter and overshoot kept,
alignment unforced), hatching in his manner. The feel test is Will's:
a drawing passes when it feels **"Will->Emise touched"** — his gesture
visibly carried through Emise's keeping hand, never a neutral renderer's
output. A re-drawn page must then ALSO validator-PASS (or carry a resolved
human flag) before it enters any assembly: the design language is how
pages are drawn; the validator is how they are admitted.

## Per-page scores

| Page | t (s) | Beat | Cov | Chamfer | Ink log2 | Black frac | Ink-in-black | Fig log2 | Verdict | Classes |
|---|---|---|---|---|---|---|---|---|---|---|
| page00p0 | 0.6 | 1 Titles | 0.875 | 1.04 | 3.93 | 0.501 | 0.0073 | -1.28 | FLAG | ink, title |
| page01p0 | 14.8 | 2 Mickey at the wheel | 0.941 | 0.72 | 1.23 | 0.074 | 0.0276 | -0.50 | PASS | — |
| page02p0 | 18.8 | 2 Mickey at the wheel | 0.919 | 0.86 | 1.61 | 0.096 | 0.0285 | -1.06 | PASS | — |
| page03p0 | 26.4 | 2 Mickey at the wheel | 0.894 | 0.98 | 1.68 | 0.067 | 0.0576 | -1.32 | PASS | — |
| page04p0 | 29.3 | 2 Mickey at the wheel | 0.870 | 1.12 | 1.97 | 0.065 | 0.0446 | -1.04 | PASS | — |
| page05p0 | 32.8 | 2 Mickey at the wheel | 0.910 | 0.89 | 1.55 | 0.065 | 0.0618 | -1.24 | PASS | — |
| page06p0 | 34.6 | 2 Mickey at the wheel | 0.903 | 0.93 | 1.53 | 0.060 | 0.0421 | -1.43 | PASS | — |
| page07p0 | 38.0 | 2 Mickey at the wheel | 0.887 | 1.00 | 2.00 | 0.069 | 0.0670 | -1.46 | PASS | — |
| page08p0 | 40.4 | 2 Mickey at the wheel | 0.885 | 1.07 | 1.94 | 0.044 | 0.0542 | -0.38 | PASS | — |
| page09p0 | 47.8 | 3 Pete takes the wheel | 0.738 | 2.07 | 2.48 | 0.018 | 0.0521 | -1.28 | FLAG | ink |
| page10p0 | 52.9 | 3 Pete takes the wheel | 0.830 | 1.31 | 2.09 | 0.061 | 0.0250 | -2.04 | PASS | — |
| page11p0 | 70.1 | 3 Pete takes the wheel | 0.789 | 1.69 | 2.91 | 0.097 | 0.0088 | -3.00 | FLAG | ink, components |
| page12p0 | 71.8 | 3 Pete takes the wheel | 0.801 | 1.50 | 1.82 | 0.046 | 0.0565 | -1.77 | PASS | — |
| page13p0 | 75.9 | 3 Pete takes the wheel | 0.737 | 2.10 | 2.96 | 0.089 | 0.0341 | -0.58 | FLAG | ink |
| page14p0 | 81.9 | 3 Pete takes the wheel | 0.796 | 1.64 | 2.16 | 0.074 | 0.0526 | -1.58 | PASS | — |
| page15p0 | 89.1 | 3 Pete takes the wheel | 0.791 | 1.68 | 2.96 | 0.138 | 0.0224 | -0.72 | FLAG | ink |
| page16p0 | 93.4 | 3 Pete takes the wheel | 0.720 | 2.19 | 4.52 | 0.417 | 0.0048 | -2.25 | FLAG | ink |
| page17p0 | 95.6 | 3 Pete takes the wheel | 0.866 | 1.04 | 4.05 | 0.444 | 0.0083 | -3.17 | FLAG | ink, components |
| page18p0 | 101.7 | 3 Pete takes the wheel | 0.879 | 1.09 | 4.11 | 0.293 | 0.0156 | -1.28 | FLAG | ink |
| page19p0 | 103.5 | 3 Pete takes the wheel | 0.763 | 1.77 | 4.67 | 0.405 | 0.0072 | -1.46 | FLAG | ink |
| page20p0 | 106.1 | 3 Pete takes the wheel | 0.744 | 1.94 | 3.73 | 0.128 | 0.0216 | -1.58 | FLAG | ink |
| page21p0 | 114.3 | 4 Podunk Landing | 0.676 | 2.41 | 4.04 | 0.119 | 0.0118 | -1.91 | FLAG | edges, ink |
| page22p0 | 117.8 | 4 Podunk Landing | 0.625 | 2.75 | 5.21 | 0.161 | 0.0064 | -0.41 | FLAG | edges, ink |
| page23p0 | 121.1 | 4 Podunk Landing | 0.680 | 2.30 | 3.76 | 0.209 | 0.0102 | +0.30 | FLAG | edges, ink |
| page24p0 | 129.8 | 4 Podunk Landing | 0.766 | 1.85 | 2.65 | 0.111 | 0.0242 | -1.05 | FLAG | ink |
| page25p0 | 131.9 | 4 Podunk Landing | 0.795 | 1.56 | 3.12 | 0.166 | 0.0180 | -0.45 | FLAG | ink |
| page26p0 | 137.5 | 4 Podunk Landing | 0.811 | 1.63 | 2.51 | 0.017 | 0.0484 | -1.14 | FLAG | ink |
| page27p0 | 145.1 | 4 Podunk Landing | 0.785 | 1.68 | 3.06 | 0.159 | 0.0306 | -2.06 | FLAG | ink |
| page28p0 | 153.8 | 4 Podunk Landing | 0.827 | 1.37 | 2.54 | 0.146 | 0.0263 | -1.25 | FLAG | ink |
| page29p0 | 170.0 | 5 Minnie's arrival | 0.892 | 0.93 | 2.27 | 0.043 | 0.0778 | -1.14 | FLAG | ink |
| page30p0 | 173.1 | 5 Minnie's arrival | 0.844 | 1.35 | 1.83 | 0.118 | 0.0336 | -1.95 | PASS | — |
| page31p0 | 179.5 | 5 Minnie's arrival | 0.940 | 0.65 | 0.78 | 0.026 | 0.0704 | -1.14 | PASS | — |
| page32p0 | 194.3 | 5 Minnie's arrival | 0.826 | 1.44 | 0.68 | 0.026 | 0.1338 | -0.21 | PASS | — |
| page33p0 | 212.6 | 5 Minnie's arrival | 0.873 | 1.07 | 2.18 | 0.133 | 0.0320 | -2.07 | PASS | — |
| page34p0 | 217.7 | 6 The goat eats the music | 0.928 | 0.84 | 1.80 | 0.146 | 0.0501 | -1.25 | PASS | — |
| page35p0 | 221.9 | 6 The goat eats the music | 0.873 | 1.08 | 1.58 | 0.036 | 0.1413 | -1.81 | PASS | — |
| page36p0 | 230.3 | 6 The goat eats the music | 0.839 | 1.40 | 1.75 | 0.052 | 0.0398 | -0.81 | PASS | — |
| page36p1 | 249.4 | 7 Animal orchestra | 0.875 | 1.08 | 1.56 | 0.082 | 0.0407 | -0.89 | PASS | — |
| page37p0 | 269.7 | 7 Animal orchestra | 0.891 | 1.12 | 1.16 | 0.073 | 0.0550 | -1.55 | PASS | — |
| page38p0 | 272.2 | 7 Animal orchestra | 0.780 | 1.68 | 2.05 | 0.095 | 0.0341 | -0.75 | PASS | — |
| page39p0 | 281.8 | 7 Animal orchestra | 0.918 | 0.99 | 1.00 | 0.076 | 0.0409 | -1.38 | PASS | — |
| page40p0 | 285.0 | 7 Animal orchestra | 0.913 | 1.04 | 1.03 | 0.055 | 0.0292 | -1.22 | PASS | — |
| page41p0 | 292.0 | 7 Animal orchestra | 0.911 | 1.10 | 1.12 | 0.074 | 0.0402 | -1.34 | PASS | — |
| page41p1 | 307.2 | 7 Animal orchestra | 0.869 | 1.24 | 1.17 | 0.068 | 0.0341 | -1.45 | PASS | — |
| page42p0 | 323.7 | 7 Animal orchestra | 0.699 | 2.30 | 2.89 | 0.091 | 0.0155 | -0.41 | FLAG | edges, ink |
| page43p0 | 337.7 | 7 Animal orchestra | 0.583 | 3.15 | 4.09 | 0.315 | 0.0067 | -1.00 | FLAG | edges, ink |
| page44p0 | 339.4 | 7 Animal orchestra | 0.716 | 2.12 | 3.14 | 0.218 | 0.0104 | -1.05 | FLAG | edges, ink |
| page45p0 | 341.4 | 7 Animal orchestra | 0.653 | 2.30 | 2.17 | 0.019 | 0.0110 | -1.58 | FLAG | edges |
| page45p1 | 353.2 | 7 Animal orchestra | 0.665 | 2.23 | 2.58 | 0.053 | 0.0071 | -1.00 | FLAG | edges, ink |
| page46p0 | 366.2 | 7 Animal orchestra | 0.737 | 1.83 | 2.19 | 0.056 | 0.0067 | -0.32 | PASS | — |
| page47p0 | 371.6 | 7 Animal orchestra | 0.694 | 2.07 | 2.41 | 0.063 | 0.0064 | +0.17 | FLAG | edges, ink |
| page48p0 | 376.4 | 7 Animal orchestra | 0.874 | 1.03 | 1.59 | 0.085 | 0.0546 | -1.43 | PASS | — |
| page49p0 | 380.1 | 7 Animal orchestra | 0.780 | 1.75 | 2.61 | 0.100 | 0.0188 | -1.50 | FLAG | ink |
| page50p0 | 383.4 | 7 Animal orchestra | 0.853 | 1.17 | 2.07 | 0.121 | 0.0278 | -1.66 | PASS | — |
| page50p1 | 396.9 | 7 Animal orchestra | 0.875 | 1.05 | 2.24 | 0.148 | 0.0293 | -1.70 | FLAG | ink |
| page51p0 | 411.7 | 8 Pete's return | 0.839 | 1.35 | 2.20 | 0.123 | 0.0208 | -0.89 | PASS | — |
| page51p1 | 424.7 | 9 Potatoes / last laugh | 0.762 | 1.71 | 2.71 | 0.125 | 0.0312 | -0.78 | FLAG | ink |
| page52p0 | 438.9 | 9 Potatoes / last laugh | 0.890 | 0.99 | 1.98 | 0.046 | 0.0626 | -0.81 | PASS | — |
| page53p0 | 444.3 | 9 Potatoes / last laugh | 0.697 | 2.16 | 2.85 | 0.054 | 0.0342 | -0.68 | FLAG | edges, ink |
| page54p0 | 454.1 | 9 Potatoes / last laugh | 0.921 | 0.68 | 6.67 | 0.927 | 0.0004 | -0.41 | FLAG | ink, title |

_Run it again: `gate_validator.py --gate-dir <gate dir>` (numpy + PIL;
pairing from plan.json + shotframes2/; title set in titles.json or the
Gate 1 default). Thresholds live at the top of the script and in
validator-scores.json._
