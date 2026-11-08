# SHOT LIST — Scrolltown Intro Video

Cut to the song map in `LYRICS.md` (90s total, 16:9, 1280×720 master).
Style for every frame: flat warm storybook animation, soft rounded shapes, Saturday Morning Breakfast palette — cream #FFFBF0, soft coral, sky blue, butter yellow, mint green. No text inside generated footage (all text is added in ffmpeg).

**Clip budget: 6 generated video clips maximum.** Biography montage absorbed into clips 1–2; beats 7–8 are stills + Ken Burns pushes (per the 2026-11-07 amendment's budget discipline).

| # | Time | Beat | Source | Content |
|---|------|------|--------|---------|
| 1 | 0:00–0:11 | **Life montage A — the kid** | VIDEO clip 1 | A kid draws spirals of numbers and stars on a chalkboard (math as first love) → the same kid in video-game glow, controller in hand, a tiny built world shining on screen → the kid outside at dusk, looking up at first stars with a small toy robot (wonder at minds). One continuous gentle sequence. |
| 2 | 0:11–0:22 | **Life montage B — keeping the town** | VIDEO clip 2 | Grown builder in a quiet bank atrium: orderly streams of golden numbers flow through a trusted lattice of light (banking) → same man at a radio dispatch desk at night, headset on, concentric radio waves rippling over a sleeping town's glowing windows (public safety radio). |
| 3 | 0:22–0:33 | **One lamp** | VIDEO clip 3 | Night interior: the builder in silhouette/profile at a desk, typing code, warm monitor glow; Nebraska night and stars outside the window; slow push-in. |
| 4 | 0:33–0:43 | **Hands at dawn** | VIDEO clip 4 | Golden dawn on the ranch: the same hands stacking hay bales; llamas watching; butter-and-rose sky. |
| 5 | 0:43–0:54 | **Scroll by scroll** | VIDEO clip 5 | A lattice of light drawn scroll by scroll across warm darkness; small glowing scroll-nodes ignite one by one into a branching network; slow pull-back. **Ignitions only accumulate.** |
| 6 | 0:54–1:05 | **Decades** | VIDEO clip 6 | The ranch over decades: seasons spin faster, solar rows appear, small compute barns rise, lights spread farm → town → city. Year markers added in ffmpeg, lower corner: **2030 · 2050 · 2080**. |
| 7 | 1:05–1:17 | **Planet chorus** | STILL + Ken Burns | Earth from orbit at night: continental city lights connecting into a living golden lattice; slow majestic push-in. Light count only grows. |
| 8 | 1:17–1:30 | **2100 horizon + cards** | STILL + Ken Burns, then ffmpeg cards | Bright dawn horizon, orbital rings of warm light over a green valley; camera rises toward a still-brighter region it does **not** reach. Then cards: **"2100"** → **"thirty years to go."** → title **EXOCORTEXIA**. 2130 is never depicted. |

## Assembly rules (ffmpeg)

- Each segment conformed to its map length (gentle speed adjust / trim; stills via zoompan push).
- Dip-to-warm-dark crossfades (~0.5s) between segments; cards fade in/out on cream.
- Year markers sit still, lower corner, warm cream type — no other on-screen text except the end cards and title.
- **Craft law check at assembly:** scrub the cut — no lit node, window, or light ever goes dark again across the whole 90 seconds.
- Deliverables: `intro-video.mp4` (master, silent — the Suno render drops onto this map), `intro-video-small.mp4` (download encode), `intro-video-guide.mp4` (master + synthesized pad guide track, labeled GUIDE ONLY).
