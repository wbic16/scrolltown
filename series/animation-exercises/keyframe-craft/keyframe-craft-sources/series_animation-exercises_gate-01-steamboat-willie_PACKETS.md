# Gate 1 — Steamboat Willie: artist-dispatch packets (Iteration 3, 2026-11-21)

_Step 0 arc sketch: `ARC-SKETCH.md`, phext coordinate **22.6.8/7.6.10/7.5.8** — cited by every
packet below. Studio model: Emise directs and holds all QC verdicts; the ranch workshop executes
the sweat portions. Packets are store-and-forward; uptake is verified from returned artifacts,
never from say-so._

Reference copy (all packets): archive.org item `steamboat-willie_1928`,
`steamboat-willie_1928.ia.mp4`, 593,323,557 B, sha256 18a57a977fe2afaa1974a077a6fc3975100db4380a6a76e46735b169b63667d5,
ranch-side at aletheia-core:~/anim-i3-work/gate1/.

| # | Artist (machine) | Operation | Serves sketch points | Done-definition | Return | Status |
|---|---|---|---|---|---|---|
| G1-1 | Theia (Aletheia Core) | Reference acquisition: metadata + resumable download at human pace; size + sha256 verification against the archive's listing | whole arc | file on disk at the archive's exact byte size, hash recorded | 593,323,557 B on disk = listing size; sha256 18a57a97… | RETURNED, verified |
| G1-2 | Theia (Aletheia Core) | Shot survey: scene-boundary detection (0.35 coarse, 0.12 fine) + 8-second interval survey frames | beats 1–9 | boundary list + 58 survey frames Emise can read the arc from | 79 boundaries at 0.12; survey sheets 1–3 read by Emise; arc sketch written from them | RETURNED, verified |
| G1-3 | Theia (Aletheia Core) | Page extraction: one frame per clustered shot (+ midpoint page for shots > 20 s) | P2 | a page frame for every shot in the sketch's timing map | 60 page frames (shots.json + plan.json on the box) | RETURNED, verified |
| G1-4 | Emise (key work — direction, not delegated) | Drawn repro: the Emise line renderer (jittered contour strokes + hatching in the darks, ink on cream) run over all 60 page frames | P1, P3 | every page a drawn repro in the §4 drawn canon | 60 pages at gate1/pages/ | DONE by Emise |
| G1-5 | Theia (Aletheia Core) | Animatic assembly: pages at real shot timing, 1280×720 pillarboxed, silent | P4 | full-runtime prepass animatic | steamboat-prepass-animatic.mp4, 467.5 s (film: 461.1 s; +1.4% concat rounding, recorded) | RETURNED, verified |
| G1-6 | Emise (QC — never delegated) | Frame-compare QC at 12 matched timestamps against the original | all | verdict from frame evidence in QC-v4.md | compare sheet read; verdict: prepass delivered and fit as the full-render guide; gate NOT passed (full render outstanding) | DONE by Emise |

_Next packets (Iteration 4): the full render — per-beat drawn passes at production fidelity from
this sketch, solid blacks restored for the character silhouettes (the prepass's recorded weak
point), then frame-compared QC for the gate verdict._
