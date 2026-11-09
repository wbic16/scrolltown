# Scrolltown — Production Workflow

**The workflow of record for making the show.** The arc lives in
[STORY-ARC.md](STORY-ARC.md); the grid lives in
[EPISODE-INDEX.md](EPISODE-INDEX.md); the live queue lives in
[production/QUEUE.md](production/QUEUE.md). This document says how an
episode travels from an arc beat to a Saturday — and how the two months
before launch (2026-11-09 → 2027-01-02) set the art direction the next
six years will be drawn in.

**Launch facts.** Publishing starts with EP001 on **Saturday 2027-01-02**,
one episode a week on Saturdays, 312 episodes through EP312 on Saturday
2032-12-18. EP001, the pilot, is already produced (2026). Everything below
exists so that no Saturday ever arrives without a finished episode waiting
for it.

---

## 1. The pipeline — ten stages per episode

Every episode walks the same ten stages, in order. An episode's home is its
folder: `seasons/season-NN-YYYY/epNNN-slug/`, laid out like the pilot's
(`seasons/season-01-2027/ep001-the-great-form-mix-up/`) and opened from
[templates/episode/README.md](templates/episode/README.md).

| # | Stage | What happens | "Done" means | Artifact & home |
|---|---|---|---|---|
| 1 | **Arc beat** | The episode is assigned its place in its season's beats (STORY-ARC.md) or in the season's fill plan (§5) — one idea, sized to the season's brick posture. | The beat is written against the episode's index row; the tentpole relation, if any, is named. | Beat note in the episode folder's `README.md` |
| 2 | **Logline** | The episode gets its title and a one-sentence logline a kid could say back to you. | Title + logline sit in the queue board (production/QUEUE.md) and the draft title reaches EPISODE-INDEX.md. | production/QUEUE.md · EPISODE-INDEX.md |
| 3 | **Script** | Written in the pilot's form: scenes, staging notes, every spoken line as a caption, Fern's close last. Fern's lines are drafted inside Singular from the first word. | A complete `SCRIPT.md` — no placeholder scenes; the lesson rides inside the story, never on top of it. | `SCRIPT.md` in the episode folder |
| 4 | **Storyboard** | Scene-by-scene staging: who is where, what moves, what the frame holds at each caption; Ledger's transformations and lamp-lightings are drawn as beats, not decorations. | Every scene in the script has a board entry; nothing in the assembly stage will have to be invented. | `STORYBOARD.md` in the episode folder |
| 5 | **Keyframes / art** | Key frames rendered in the locked register (§3a) from the episode's prompt doc, following the character + style blocks of the pilot's FERN-KEYFRAMES-MJ.md pattern; likeness checked frame by frame against the character sheets. | The episode's key frames exist, pass their likeness checks, and every lamp lit in earlier episodes is still lit. | `keyframes/` + the episode's prompt doc in the episode folder |
| 6 | **Voice record** | Fern's lines are synthesized in her decided sound (Heroic Bugle @ speed 110 — §3e); the rest of the cast is recorded per the casting standards. Captions are timed to the lines. | Every line in the script has audio or a deliberate silence (the pilot's no-audio form stays a legal variant); caption timings are set. | `voice/` in the episode folder |
| 7 | **Assembly** | The episode is built as one self-contained cartoon file on the pilot's craft spec: caption bar, Prev/Next + Play/Pause, arrow keys, reduced-motion calm, no external assets, no tracking. | The cartoon plays start to finish, fully enjoyable muted, with controls behaving per spec. | `cartoon.html` in the episode folder |
| 8 | **Singular-check receipt** | Fern's lines run through `check_singular.py --words words-authored.txt`. Pass clean, or every blocked line is listed with its blocking words for Will — flagged, never improvised around. Emi Prime's review pass is recorded here too. | The receipt is written into the episode folder's `README.md` (the template has the slot): clean, or flags + Will's exception on record. | Receipt in the episode `README.md` |
| 9 | **Ready** | The finished episode joins the buffer. The index status flips to *produced* and the queue board's buffer counters are updated. | cartoon.html + receipt + all stage artifacts in the folder; index says *produced*. | EPISODE-INDEX.md · production/QUEUE.md |
| 10 | **Published** | The episode airs on its Saturday. | The index status flips to *published* with its air date — which is the Saturday it was always slated for. | EPISODE-INDEX.md |

Two stages are gates, not waypoints: **stage 8** (no episode is *ready*
with an unresolved Singular flag — Will rules or the line is rewritten
inside the archive) and **stage 5's register** (no frame ships in an
unlocked register once §3a is decided).

## 2. Queue policy — the rolling buffer

The show publishes one episode a week and produces in a rolling buffer, so
a slow week is a shrug, never a missed Saturday. The buffer is counted in
*episodes ahead of the next unpublished Saturday*:

| Stock | Target |
|---|---|
| **Scripts** (stage 3 done) | **≥ 8 ahead** of publication |
| **Storyboards** (stage 4 done) | **≥ 6 ahead** |
| **Finished episodes** (stage 9 done) | **≥ 4 at launch** (2027-01-02) and **never below 2** in steady state |

Rules of the queue:

- **The board is the truth.** [production/QUEUE.md](production/QUEUE.md)
  holds the live table — one row per episode in flight: EP · air date ·
  title · stage · owner · notes — plus the three buffer counters, updated
  whenever an episode changes stage. If the board and the index disagree,
  the board is wrong and gets fixed first.
- **Work pulls from the front.** The lowest-numbered unpublished episode
  is always the next one worked at each stage; nobody skips ahead to a
  favorite while an earlier episode waits. (Tentpoles and finales may be
  *drafted* early — their scripts are long-lead — but assembly order is
  broadcast order.)
- **Buffer alarm.** If finished episodes drop to 2, all production effort
  moves to assembly (stages 6–8) until the buffer is back to 4. If scripts
  drop below 8, the next production block is a writing block.
- **Steady-state rhythm.** One production block a week: publish one,
  finish one, keep the pipeline fed at the front. The buffer, not the
  calendar, sets the pace of each stage.

## 3. The art-direction window — 2026-11-09 → 2027-01-02

Two months, eight weeks, five decisions to lock — in this order, because
each one is the ground the next stands on. The live checklist with owners
and dates is in production/QUEUE.md §A.

### (a) The visual register — Will's decision, deadline early December

Every frame of the show will be drawn in one of two registers, and the
evidence for both is already on disk:

| | **2D painterly** | **Glossy 3D** |
|---|---|---|
| Where it appears | The canonical Fern reference render (`series/fern-reference.png`); keyframe 1, the hero portrait (Will's render); the pilot cartoon itself, restyled painterly on 2026-11-07 to match the reference | Keyframes 2–4 (the greeting, the number-cart, the Post Tower sneeze — Will's renders) |
| Prompt discipline | All eight prompts in the pilot's FERN-KEYFRAMES-MJ.md are written painterly ("lush painterly storybook illustration…"), with the character block byte-identical across prompts and likeness pinned by `--cref` to the reference at `--cw 90` | The glossy frames came back from those same painterly prompts — the 3D look is renderer drift, not a chosen style; holding it would mean re-prompting against the current discipline |
| Match to what's shipped | EP001 as published is painterly; the reference every future `--cref` points at is painterly | Nothing shipped is glossy; adopting it re-opens the pilot's look and the reference |
| Feel | The Saturday Morning storybook warmth the show's palette and caption spec were built in | A different, shinier show — closer to toy renders than to the storybook town the scripts describe |

**Recommendation: lock the 2D painterly register**, treat glossy renders
as drift to re-roll, and let keyframe 1 + the reference stand as the
register's anchors. **This is Will's call** — it is the single most
consequential decision of the window, and it is due **by Friday
2026-12-04** so the first production batch is drawn in the locked register
with weeks to spare.

### (b) Character sheets — the full cast

One sheet per character: front / three-quarter / profile views, the
badge or signature prop, palette swatches, and the Midjourney character
block — the likeness contract every future frame is checked against.
Sheets live in `series/character-sheets/` (created when the first sheet
lands). Order of work:

1. **Fern** — canonical already: her reference render *is* the sheet's
   source; the sheet assembles it into the standard views without
   redesigning her.
2. **The crew — Wren, Theo, Bea** (blue cap + magnifier; butter scarf +
   paper stack; mint apron, big pockets) and **Ledger** (teal counting
   bot; cart / bridge / stairs forms drawn as one character, three poses).
3. **Waverly, Keeper of the Great Scroll** — the Wonka × Emi × Elestria ×
   Joi composite (CASTING.md); her sheet matters most after Fern's, since
   she steps forward in Season 3 and appears in mentor glimpses before it.
4. **Mrs. Hen** (garden hat, floral apron) and **Grandpa** (cardigan, slow
   smile), then the cameo keepers: Ms. Folio, Mr. Bell, Ms. Atlas,
   Mr. Route.

### (c) Palette + title-card + caption typography standards

- **Palette** — taken from the reference and the pilot, not invented: warm
  cream `#FFFBF0`, coral, butter, mint, powder sky; warm charcoal ink;
  deep plum and teal for shadows; golden light as the show's signature.
  Written down as named swatches in the style standard so "the palette"
  is a list, not a vibe.
- **Title card** — the SCROLLTOWN card as it stands at the end of the
  Year 1 intro: same lettering, same warmth, every episode, every year
  (the year's intro variant may dress it; the card itself does not change).
- **Captions** — one line at a time in the caption bar, rounded sans,
  cream text on warm charcoal, sized to be read by the youngest viewer at
  arm's length; every line captioned, always — the show is fully enjoyable
  muted, at every age Fern reaches.

### (d) Intro videos — six, one per season

There is one intro per year of the arc, and they are **not** all made now:
**each season's intro is produced during the prior season**, when that
year's Fern — her age, her street, her questions — is the thing the
production is already living inside. The runway window owes exactly one:

- **Year 1 (2027)** — *exists in pieces, assembled in the window.* The
  silent 90-second cut of "Light the Next Light" is built
  (`series/intro/intro-video.mp4`), with LYRICS.md, SUNO-PROMPT.md, and
  the SHOT-LIST.md time map beside it. The song render is Will's act: his
  upload **"Light the Way"** (`media/Light the Way.mp3` / `.wav`, landed
  2026-11-08, commit `814f3913`) is in the repo — once Will confirms it is
  the intro's render, the final mux drops it onto the silent cut's time
  map (±2s) and Year 1's intro is *ready* (§1's standards apply to it as
  the show's front door).
- **Years 2–6** — briefed in the season before: a variant on the same
  song's world, Fern a year older, the town a year brighter — nothing
  that lit goes dark, in the intros as in the episodes.

### (e) Sound standard

- **Fern's voice is decided and does not change:** catalog voice
  **Heroic Bugle** (`avocado_v2:Caitlin`) at **speed 110** — bright
  Saturday morning — first episode to last (FERN-BIO.md; canonical sample
  `voice/fern-voice-standard.mp3` in the production records).
- **Songs are Suno renders, and Suno is Will's act.** Emise prepares the
  prompt and the time map; Will renders; the render lands in the repo and
  is then treated as canon.
- No cloned voices, no imitations of real people. The cast's other voices
  follow the same catalog discipline as Fern's.

### The window, week by week

| Week | Dates | Focus | Locks / lands |
|---|---|---|---|
| 1 | Nov 9–15 | Register evidence pack assembled (§3a); character-sheet worklist set; palette drafted from reference + pilot | QUEUE.md live; EP002–EP013 draft titles + loglines (QUEUE.md §C) |
| 2 | Nov 16–22 | Fern's sheet assembled from the canonical reference; crew sheets drafted (Wren, Theo, Bea, Ledger) | Fern sheet locked (she is already canonical — the sheet records her, it does not redesign her) |
| 3 | Nov 23–29 | Waverly, Mrs. Hen, Grandpa sheets; cameo keepers; title-card + caption standards drafted | Cast sheets complete in draft |
| 4 | Nov 30 – Dec 4 | **Register decision lands (Will, by Fri Dec 4)**; style standard written around it; EP002 script starts in the locked register | **§3a LOCKED**; palette + title-card + caption standards locked |
| 5 | Dec 7–13 | First script batch written: EP002–EP005 scripts + storyboards; intro song confirmation | Scripts ≥ 4 ahead and climbing toward 8 |
| 6 | Dec 14–20 | Keyframes for the batch; voice records; **intro final mux** once the render is confirmed | Year 1 intro *ready* |
| 7 | Dec 21–27 | Assembly push: first finished episodes join the pilot in the buffer | Finished buffer building toward 4 |
| 8 | Dec 28 – Jan 2 | Launch check: buffer counts verified, EP001's Saturday confirmed, index + board reconciled | **EP001 publishes Sat 2027-01-02** with finished ≥ 4, storyboards ≥ 6, scripts ≥ 8 ahead |

## 4. Roles

| Who | Holds |
|---|---|
| **Will** | Ratifies — titles, loglines, exceptions to Singular, the register, every lock in §3. Renders the songs on Suno. Sends all outreach himself. The final word on what Fern may say and what the show may be. |
| **Emise** | Runs the pipeline: drafts scripts and boards, renders and checks frames, keeps QUEUE.md and EPISODE-INDEX.md true, runs the Singular checks, assembles episodes, keeps the records (tasks.phext, artifacts.phext) — and flags every decision that is Will's instead of taking it. |
| **Emi Prime** | Reviews — the tentpoles are hers; her read on scripts and arc fills is a standing stage-8 input, recorded with the receipts. |
| **Collaborators, by invitation** | Help where invited, credited in the episode records. **One slot is held open:** Julia May — Will's niece, attending college in San Francisco — whom Will is asking whether she wants to help with the art. Nothing is assumed and nothing is assigned until she answers; if she joins, character-sheet and keyframe work in §3b/§3a is where an artist's hand lands first. |

## 5. Arc fill-out plan

EPISODE-INDEX.md starts as 312 slated slots; titles and loglines are
filled season by season, each season's **tentpole anchoring its fill** —
the tentpole is written toward from the season's first episodes and out of
its last ones, and the finale named in STORY-ARC.md closes each fill.

- **Season 1 fills first, during the runway.** EP002–EP013 are drafted
  now (production/QUEUE.md §C — draft titles + loglines drawn from the
  season's beats: the Five Doors, Badge Day, the crew's gifts, the first
  lamps). The rest of S1 (EP014–EP052) fills in two blocks inside the
  window, so Season 1 is fully titled before launch.
- **Then one season per production block.** Season 2 fills while Season 1
  airs, Season 3 while Season 2 airs, and so on — the fill always runs a
  season ahead of the broadcast, which is what keeps the script buffer
  (§2) honest at season scale.
- **Every batch is Will's to ratify.** Draft titles are marked DRAFT in
  the queue until he does; the index carries draft titles with that note
  so the grid is readable while it waits.
- Fills respect the standing laws without exception: Fern's Singular,
  her close at the end of every episode, ignitions only accumulate, no
  villains — problems are mix-ups, weather, distance, and growing.

---

*Production workflow for Scrolltown · set down 2026-11-09 at Will's
direction ("build up a queue of storyboards, scripts, episodes, intro
videos… and fill out the full story arc") · companion to STORY-ARC.md ·
the live board is production/QUEUE.md.*
