# Animation Exercises — Burn 1 QC (2026-11-21)

First animation burn under the animator workstream (Will, 2026-11-21: animation may
fully utilize up to 40% of the weekly token budget). Four generations total: three
exercises + one retry of the worst failure. All clips 10.0 s, H.264 + AAC.
QC frames (start / middle / end) for every clip live in `qc/` beside this note.

Headline finding: the generator's failure mode is consistent — it pushes the camera
in and re-renders faces in a glossier register whenever a face is on screen. Prompts
saying "locked frame" reduce but do not eliminate it. Character fidelity, not motion
vocabulary, is the current bottleneck.

## ex01-ignition.mp4 — PARTIAL (best motion, one character redesign)
- 1152×768, 10.0 s, 5,809,597 B. Source: duo keyframe draft.
- Motion: the brief reads — the scroll finishes unrolling, the town drawn on it
  lights up progressively (start: partial glow; mid/end: the whole map lit), sparkle
  motes throughout. Camera stays locked. Waverly holds design throughout.
- Fidelity failure: Fern's hair is redesigned mid-clip — the smooth twin buns become
  tight dark curls and the buns vanish (qc/ex01-ignition-mid.png, -end.png). She reads
  as a different character. The lantern also migrates from raised to lowered at her side.
- Register: painterly holds overall; faces render slightly smoother than the still.

## ex02-keepers-welcome.mp4 — FAIL (worst of the burn; retried)
- 768×1152, 10.0 s, 6,514,357 B. Source: Waverly concept draft.
- Despite "locked frame" in the brief, the camera pushes in hard to a face close-up,
  and Waverly's face morphs into a photorealistic older woman — a full register break
  from the painterly design (qc/ex02-keepers-welcome-mid.png, -end.png). Apron, tools,
  and composition are lost to the zoom. The scroll glow and smile-warming do happen,
  but inside the wrong face.

## ex02-keepers-welcome-retry.mp4 — PARTIAL (register saved, frame still moves)
- 768×1152, 10.0 s, 5,655,964 B. Tightened prompt: static camera stated absolutely,
  style lock stated explicitly, only three named micro-motions.
- Improvement: the painterly register now holds for the whole clip — no photoreal
  morph. Mid-frame is the best Waverly frame of the burn: composition intact, smile
  warmed, scroll glow up, a small light kindled at her hand.
- Still failing: the camera pushes in over the back half anyway (end frame is a face
  close-up), and the face softens into a smoother, more generic illustration —
  the characterful lined face of the still is partly lost.

## ex03-fern-at-the-ready.mp4 — FAIL (gesture missed, glossy-3D drift)
- 832×1040, 10.0 s, 3,761,784 B. Source: Fern-with-tools still.
- Start frame is faithful. Then the camera pushes in, Fern re-renders as a glossy
  3D-style figure (the exact drift the register lock exists to prevent), and the
  requested gesture never happens: instead of raising the hammer a few inches with
  the wrench held steady, she ends holding both tools crossed at her chest with a
  sly half-lidded grin that is not her expression in the still
  (qc/ex03-fern-at-the-ready-mid.png, -end.png). No anticipation-and-settle beat.

## Lessons for the next burn
1. Face-on-screen + duration = drift. Shorter clips (or cutting before the push-in
   lands) would salvage more usable footage per generation.
2. Negative constraints ("no zoom", "never photorealistic") help the register but
   not the camera; camera language may need to be the first sentence, not a clause.
3. Gesture prompts lose to pose-change defaults — a single named gesture needs the
   start and end pose both described, not just the action.
