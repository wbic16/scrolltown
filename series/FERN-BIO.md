# Fern — Character Bio (Scrolltown)

**Name:** Fern
**Age:** 8
**Role:** A Keeper of Scrolltown — and the narrator. She is the viewer's eyes and neighbor-guide.
**Home:** A little house-scroll on Home Street, 1.1.1, inside the Great Scroll.

## Who she is
Fern lives inside the Great Scroll, in the town of Scrolltown, where every neighbor keeps their own house-scroll — their stories, forms, and important papers — and every door opens only for its own key-badge. Fern's gift is Keeping: she checks badges at doors, carries papers only to their own houses, and never, ever peeks. "We never peek. It's not our house."

She is curious and unhurried. She talks straight to the viewer, the way a good neighbor does, and she names feelings out loud — her own and yours — because mixed-up is a feeling, and feelings are okay. When the Forms Router Post Tower sneezed and scattered the town's papers, Fern and her crew (Wren who finds, Theo who sorts, Bea who carries) put every page back in its own house — including her Grandpa's best story, which mattered most of all.

Her name is the quiet thesis of the show: a fiddlehead fern unfurls the way a scroll opens. She is a farm kid at heart — patient with animals, good with her hands, brave in the gentle way: she stays kind when things are mixed up.

**Catchphrase / close:** "The scroll is yours, neighbor. See you tomorrow."

## Voice

**Her words — Singular, exclusively.** Fern speaks only in Singular: the words of Will Bickford's Twitter archive, in Write mode — the 19,094 words Will himself authored, the center of the dialect. The test is mechanical, not a matter of taste: every line she speaks must pass `check_singular.py --words words-authored.txt` clean before it ships. If a line cannot be said inside the archive without breaking what it means, nobody improvises outside the list — the line is flagged to Will with the blocking words named, and only Will grants the exception.

Episode 1 was audited under this rule on 2026-11-07: of her 31 lines, 17 were already clean, 7 were rewritten into compliance (meaning, warmth, and teaching unchanged), and 7 stand flagged for Will's word — the blockers are his own coinage "Scrolltown" (the town's name, twice), the cast names Wren, Theo, Bea, and Mrs. Hen, and one badge-check line where Mrs. Hen's name meets "tomato" (the permit's stamp — a read-list word, never authored) plus two fixable words ("keeper," "hers") whose repairs are ready if the name and the stamp are excepted. Both of her catchphrases pass clean, word for word: "We never peek. It's not our house." and "The scroll is yours, neighbor. See you tomorrow."

**Her sound.** Decided (Will, 2026-11-07): the catalog voice **Heroic Bugle** (`avocado_v2:Caitlin`) — bright, curious — at **speed 110**, his "bright Saturday morning" pick from the 90/100/110/120 auditions. Canonical sample: `~/workspace/exocortexia-cartoon/voice/fern-voice-standard.mp3`.

**Ruling (Will, 2026-11-21): "Singular is our default, but it isn't a hard rule."** The 7 flagged lines stand as written — the proper names are permitted (Scrolltown, Wren, Theo, Bea, Mrs. Hen), and the prepared repairs for "keeper," "hers," and "tomato" are NOT applied; the lines stay byte-identical to the shipped pilot. Episode 1 passes its Singular check under this ruling: 24 of 31 lines strict-clean, 7 standing as written under the ruling. The discipline still governs drafting — inside the archive first — with names and coined words permitted.

## Visual design
Fern is rendered in a lush painterly storybook style, standing in golden light in front of the giant luminous Scroll: honey-brown hair in two big round scroll-puff buns with spiral shading and a side-swept fringe; freckles scattered across round cheeks and the bridge of her nose; very large amber-brown eyes with bright white highlights. She wears a cream knit sweater with visible knit texture under coral overalls with brass buttons and rolled cuffs, a butter-yellow scarf wrapped and knotted at her neck, and mint-green sneakers with stripes; her tiny brass scroll key-badge — a small brass disc with a scroll spiral — hangs on a thin black cord at her chest, and she carries a small rolled scroll in her left hand. The palette is warm and glowing — cream, coral, butter, and golden light against the town's deep plum and teal shadows — with soft rounded forms and gentle radiance throughout.

## Midjourney prompt (character render)
```
Fern, an 8-year-old cartoon girl with round cheeks, light freckles and big curious amber-brown eyes, honey-brown hair in two round puffs shaped like the rolled ends of a scroll, cream knit sweater under soft coral overalls, butter-yellow scarf, mint-green sneakers, a tiny brass scroll key-badge on a cord at her chest, holding a small rolled parchment scroll under one arm, standing in a cozy storybook town inside a giant glowing scroll, warm pastel Saturday-morning palette, cream and coral and butter yellow, flat vector children's-book illustration, soft rounded shapes, gentle warm shadows, kind expression, looking at the viewer --ar 4:5 --style raw
```

Wide variant (scene/establishing):
```
the same character design, Fern riding a small wooden number-cart between rounded pastel houses shaped like standing scrolls, doors with tiny brass key-badges, a friendly counting robot and three small friends waving, cozy town inside a great glowing scroll, warm pastel children's-book illustration, flat vector style, soft morning light --ar 16:9 --style raw
```
