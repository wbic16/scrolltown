# Animation Exercises — Burn 2 QC (2026-11-21, Oracle Artist Iteration 1)

Second burn, run under the Oracle Artist protocol (animator skill §8): hypotheses stated
before generation, verdicts against the written done-definitions, frame evidence for
every claim. Four generations (cap was six). QC frames in `qc2/` beside this note.
New stills generated for this burn are in `stills/` (wide Waverly, wide Fern-with-tools,
Counting House token) — all three passed their still likeness checks before animation.

**Hypotheses under test** (from Burn 1's indicted basis vectors):
- H1: The countermeasure stack (shorter ~5 s clips, wider framing, static camera as the
  prompt's first sentence, explicit style lock) prevents the push-in and the register break.
- H2: Re-asserting identity anchors by name in the prompt pins Fern's identity in motion.
- H3: Naming start AND end poses makes a single small gesture land.
- H4 (control): With no face on screen, pure motion craft (timing, squash, decay) is
  already within the generator's competence, and the camera stays put.

## ex01-ignition-v2.mp4 — PARTIAL (identity fixed; camera and map-style imperfect)
- 1152×768, **10.0 s** (5 s requested — duration request not honored), 4,299,785 B.
  Source: duo keyframe draft, same as Burn 1.
- **Identity: HELD for the full 10 s.** Fern's twin scroll-puff buns stay smooth and
  round in every sampled frame (qc2 start/q1/mid/q3/end) — Burn 1's fatal failure does
  not recur. Scarf bow and key-badge intact throughout; Waverly on-model throughout.
  H2 supported *for near-static characters*.
- **End state: as named.** The lantern is still raised at the end; the town on the
  scroll is fully lit; both characters finish in their starting poses.
- Register: characters stay painterly in all frames — no glossy morph, no photoreal face.
- Deductions: (1) a mild reframing in the first ~2.5 s — the composition tightens
  slightly, then holds; the camera is not perfectly static. (2) The scroll's map art
  shifts register internally: the flat ink drawing becomes a volumetric miniature town
  as it lights. The ignition reads, but the map's own style drifts.
- Verdict: PARTIAL — the strongest character clip across both burns.

## ex02-keepers-welcome-v2.mp4 — PARTIAL (register saved; camera law NOT defeated)
- 768×1152, 5.0 s exactly, 2,501,049 B. Source: new wide still (Waverly ≈ ¼ frame height).
- **The push-in happened anyway.** Start frame is the wide shot as briefed; by mid
  (2.5 s) Waverly fills half the frame in a bust close-up; the end settles at a medium
  shot. H1 is **refuted for the camera**: wide source framing + 5 s + absolute
  static-camera language, first sentence, did not hold the framing.
- **But the register held this time** — unlike Burn 1's photoreal morph, every frame
  stays painterly and Waverly's design (gold streak, plum coat, apron, tools) is intact
  in all three frames, close-up included. The two named micro-motions both read: her
  smile warms, the scroll's glow brightens substantially.
- Verdict: PARTIAL — the stack protects the register, not the camera.

## ex03-fern-at-the-ready-v2.mp4 — FAIL (anticipation swallowed the gesture; identity lost under body motion)
- 1152×768, 5.0 s exactly, 1,623,833 B. Source: new wide Fern-with-tools still
  (start pose exactly as briefed: hammer low, wrench steady).
- **The gesture never happens.** The prompt's "small crouch of anticipation" was
  promoted into the main action: by mid, Fern is in a full crouch; by the end she is
  kneeling on the floor, eyes closed, tools crossed low in her lap — neither the
  hammer-raise nor the named end pose (identical to start) occurs. H3 is **refuted as
  applied**: naming the end pose did not save the shot once a body movement was named.
- **Identity lost under body motion.** In the mid and end frames her smooth twin buns
  have dissolved into dark curls — the same failure as Burn 1's ex01, despite the
  anchors being re-asserted by name in the prompt. H2 is **refuted as sufficient**:
  re-assertion held in ex01-v2 (characters near-static) and failed here (full-body
  crouch). Background props also shift between frames.
- Register: painterly throughout (no glossy 3D this time) — the failure is identity
  and staging, not style.
- Verdict: FAIL.

## ex01-bouncing-ball.mp4 — PARTIAL (the control: sequencing and physics read; fine craft unverified)
- 1152×768, 10.0 s, 24 fps, 1,763,423 B. Source: new Counting House token still.
  No faces anywhere. Frames sampled at 0/1.5/3/4.5/6/7.5/9.9 s.
- **Camera: static in all seven sampled frames** — with no face on screen, the push-in
  never comes. The camera law is face-seeking; H4's camera half is confirmed.
- **The three-material sequence delivered in order.** Wood first: airborne and
  flipping at 1.5 s, settled by 3 s. Brass second: airborne high at 6 s (a visibly
  higher, springier arc than the wood's), falling at 7.5 s, settled by 9.9 s. Paper:
  displaced to the counter's edge by 6 s and settled — it tumbles rather than flutters,
  but it never truly bounces. End state exactly as named: all three at rest.
- Deductions against the rung's written done-definition: the wood token's bounce reads
  as a single flip/spin rather than a visibly decaying bounce series, and contact-frame
  squash cannot be confirmed or refuted at 1.5 s sampling — those two clauses are
  unverified, not passed.
- Verdict: PARTIAL — the best evidence yet that motion craft is available when
  identity is not at stake.

## Basis vectors indicted by Burn 2
1. *"Prompt language + wide framing can hold the camera"* — **refuted** (ex02-v2).
   The push-in is not prompt-controllable. New doctrine: design for the push-in —
   start wider than the intended framing and judge the clip by its end framing —
   or trim/stabilize in assembly.
2. *"Re-asserting anchors in the prompt pins identity"* — **refuted as sufficient,
   refined**: anchors held 10 s for near-static characters (ex01-v2) and failed under
   full-body motion (ex03-v2). Body motion is the re-draw trigger; hair goes first.
3. *"Name anticipation to get anticipation"* — **refuted** (ex03-v2). Any named body
   movement is promoted to the main action. In generated clips, anticipation must be
   a held beat of stillness, never a named crouch or bend.
4. *"Requested duration is a control"* — **refuted in part**: ex02/ex03 came back at
   exactly 5.0 s; ex01-v2 came back at 10.0 s despite the request. Duration is
   advisory — probe every clip and trim to the passing segment.
5. *"The camera law is about faces"* — **supported** by the control (bouncing-ball:
   10 s, seven frames, zero reframing).
