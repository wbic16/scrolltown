#!/usr/bin/env python3
"""Live Drawing — practice session 03 (Wavelet 4, 2026-11-28).

SESSION 3 = MEETING PACE, session 2's run with its one named adjustment.
Session 2's synthesis indicted exactly one survivor that changed meaning
under compression: the crescent moon, whose inner arc was cut for pace,
leaving a plain ring. This run restores it — ONE stroke: the crescent's
second arc, an offset circle (centre 1162,128, r 24) whose endpoints land
on the outer ring and whose curve bulges across the disc — drawn right
after the outer arc, in the same act, at the same 15 s meeting pace.
Everything else is session 2 unchanged: same subject family — lantern ->
rooftops -> windows answering -> hand writing "light the next light" —
same staging, same seed, same schedule windows; the writing genuinely
HAND-STROKED from the Emise font's own glyph outlines.

Drawn route, Emise line-renderer lineage: deterministic, seeded 20261122;
strokes scheduled and drawn progressively onto a persistent canvas.
THE GROUND IS WHITE (animator skill section 4, drawn canon point 6):
paper white (255,255,255), first frame to last.

Output: PNG frames at 1280x720, 24 fps, 15.0 s, silent (assembly is
separate, ranch-side). Frames land in ./frames-03/.
"""
import math, os, random, sys
from PIL import Image, ImageDraw

W, H, SS = 1280, 720, 2
FPS, DUR = 24, 15.0
WHITE = (255, 255, 255)
INK   = (43, 32, 25)
AMBER = (245, 176, 65)
FLAME = (238, 118, 38)
SEED  = 20261122

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames-03")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- strokes
class Stroke:
    def __init__(self, pts, width=2.4, color=INK):
        self.pts = pts
        self.width = width
        self.color = color
        self.cum = [0.0]
        for a, b in zip(pts, pts[1:]):
            self.cum.append(self.cum[-1] + math.hypot(b[0]-a[0], b[1]-a[1]))
        self.total = self.cum[-1]
        self.t0 = self.t1 = None
        self.drawn = 0.0

    def point_at(self, dist):
        if dist <= 0: return self.pts[0]
        if dist >= self.total: return self.pts[-1]
        for i in range(1, len(self.cum)):
            if dist <= self.cum[i]:
                f = (dist - self.cum[i-1]) / max(1e-6, self.cum[i] - self.cum[i-1])
                a, b = self.pts[i-1], self.pts[i]
                return (a[0] + (b[0]-a[0]) * f, a[1] + (b[1]-a[1]) * f)
        return self.pts[-1]

def jittered(pts, rng, jit=2.2, step=9.0, overshoot=0.0):
    """Looser than session 1: bigger step, bigger fast-hand jitter."""
    out = []
    for a, b in zip(pts, pts[1:]):
        seg = math.hypot(b[0]-a[0], b[1]-a[1])
        n = max(2, int(seg / step))
        for i in range(n):
            f = i / n
            out.append((a[0] + (b[0]-a[0]) * f + rng.uniform(-jit, jit),
                        a[1] + (b[1]-a[1]) * f + rng.uniform(-jit, jit)))
    out.append(pts[-1])
    if overshoot and len(out) >= 2:
        (x1, y1), (x2, y2) = out[-2], out[-1]
        d = math.hypot(x2-x1, y2-y1) or 1.0
        out.append((x2 + (x2-x1)/d * overshoot, y2 + (y2-y1)/d * overshoot))
    return out

def arc_pts(cx, cy, r, a0, a1, n=18, ry=None):
    ry = r if ry is None else ry
    return [(cx + r * math.cos(math.radians(a0 + (a1-a0) * i/n)),
             cy + ry * math.sin(math.radians(a0 + (a1-a0) * i/n))) for i in range(n+1)]

acts = {"a1": [], "a2": [], "lights": []}
def add(act, pts, rng, width=2.4, color=INK, jit=2.2, overshoot=0.0):
    acts[act].append(Stroke(jittered(pts, rng, jit=jit, overshoot=overshoot),
                            width=width, color=color))

rng = random.Random(SEED)
GY = 470

# ---- Act 1: the lantern (same staging as session 1, looser hand) --------
add("a1", [(228, GY), (272, GY)], rng, width=3.4)
add("a1", [(250, GY), (250, 302)], rng, width=3.6)
add("a1", [(250, 302), (332, 302)], rng, width=3.2, overshoot=4)
add("a1", [(330, 302), (330, 320)], rng, width=2.4)
add("a1", [(313, 320), (347, 320)], rng, width=2.8)
add("a1", [(313, 320), (319, 368)], rng, width=2.8)
add("a1", [(347, 320), (341, 368)], rng, width=2.8)
add("a1", [(319, 368), (341, 368)], rng, width=2.8)
add("a1", [(313, 320), (330, 306), (347, 320)], rng, width=2.4)
add("a1", arc_pts(330, 350, 7, 180, 360, n=10, ry=10) +
          [(337, 350), (330, 334), (323, 350)], rng, width=2.4, color=FLAME)
add("a1", [(330, 300), (330, 284)], rng, width=2.2)
for dx, dy in [(-30, -22), (30, -22), (-36, 6), (36, 6)]:
    add("a1", [(330+dx*0.55, 344+dy*0.55), (330+dx, 344+dy)], rng, width=2.2, color=AMBER)

# ---- Act 2: street + five houses (detail cut for pace: no eave hatch,
# ---- no window crossbars, fewer stars — gesture over finish) ------------
add("a2", [(56, GY), (640, GY)], rng, width=2.8)
add("a2", [(640, GY), (1224, GY)], rng, width=2.8)
houses = [
    (430, 112, 104, True), (566, 100, 88, False), (690, 118, 122, True),
    (832, 102, 94, False), (958, 122, 112, True),
]
window_boxes = []
for (hx, hw, hh, chim) in houses:
    top = GY - hh
    add("a2", [(hx, GY), (hx, top), (hx+hw, top), (hx+hw, GY)], rng, width=2.8)
    add("a2", [(hx-10, top), (hx+hw/2, top-38), (hx+hw+10, top)], rng, width=3.0, overshoot=4)
    if chim:
        cx = hx + hw - 30
        add("a2", [(cx, top-26), (cx, top-48), (cx+16, top-48), (cx+16, top-30)], rng, width=2.4)
    dx = hx + hw/2 - 13
    add("a2", [(dx, GY), (dx, GY-44), (dx+26, GY-44), (dx+26, GY)], rng, width=2.4)
    for wx in (hx + 16, hx + hw - 40):
        wy = top + 26
        add("a2", [(wx, wy), (wx+24, wy), (wx+24, wy+28), (wx, wy+28), (wx, wy)], rng, width=2.1)
        window_boxes.append((wx+2, wy+2, wx+22, wy+26))
add("a2", arc_pts(1150, 128, 30, 200, 520, n=16), rng, width=2.4)      # crescent moon, outer arc
add("a2", arc_pts(1162, 128, 24, 71.8, 288.2, n=20), rng, width=2.4)   # crescent INNER arc — restored (session 3's one adjustment): offset circle, endpoints on the outer ring, bulging across the disc
for sx, sy in [(120, 110), (520, 84), (880, 70)]:                     # three stars
    add("a2", [(sx-7, sy), (sx+7, sy)], rng, width=1.8)
    add("a2", [(sx, sy-7), (sx, sy+7)], rng, width=1.8)

# ---- Act 3: windows answer ----------------------------------------------
order = list(range(len(window_boxes)))
random.Random(SEED + 1).shuffle(order)
light_events = []
for k, wi in enumerate(order):
    bx = window_boxes[wi]
    cx, cy = (bx[0]+bx[2])/2, (bx[1]+bx[3])/2
    for dx, dy in [(-16, -14), (16, -14), (-16, 14), (16, 14)]:
        add("lights", [(cx+dx*0.5, cy+dy*0.5), (cx+dx, cy+dy)], rng, width=1.7, color=AMBER)

# ---- Act 4: HAND-STROKED writing -----------------------------------------
# Glyph outline contours extracted from the Emise font itself; each contour
# becomes one pen stroke, drawn in reading order, pen lifting between
# contours and letters. Written at speed — fast writing is the natural form.
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen

class ContourPen(BasePen):
    def __init__(self, glyphSet):
        super().__init__(glyphSet)
        self.contours = []
        self.cur = None
    def _moveTo(self, p): self.cur = [p]
    def _lineTo(self, p): self.cur.append(p)
    def _curveToOne(self, p1, p2, p3):
        p0 = self.cur[-1]
        for i in range(1, 13):
            t = i / 12
            mt = 1 - t
            self.cur.append((
                mt**3*p0[0] + 3*mt*mt*t*p1[0] + 3*mt*t*t*p2[0] + t**3*p3[0],
                mt**3*p0[1] + 3*mt*mt*t*p1[1] + 3*mt*t*t*p2[1] + t**3*p3[1]))
    def _qCurveToOne(self, p1, p2):
        p0 = self.cur[-1]
        for i in range(1, 10):
            t = i / 9
            mt = 1 - t
            self.cur.append((mt*mt*p0[0] + 2*mt*t*p1[0] + t*t*p2[0],
                             mt*mt*p0[1] + 2*mt*t*p1[1] + t*t*p2[1]))
    def _closePath(self):
        if self.cur and self.cur[-1] != self.cur[0]:
            self.cur.append(self.cur[0])
        if self.cur: self.contours.append(self.cur)
        self.cur = None
    def _endPath(self):
        if self.cur: self.contours.append(self.cur)
        self.cur = None

FONT_PATH = os.path.expanduser("~/workspace/emise-font/out/Emise.ttf")
TEXT = "light the next light"
BASE_Y = 622
tt = TTFont(FONT_PATH)
gs = tt.getGlyphSet()
cmap = tt.getBestCmap()
hmtx = tt["hmtx"]
upem = tt["head"].unitsPerEm
adv_total = sum(hmtx[cmap[ord(c)]][0] for c in TEXT)
scale = min((W - 200) / adv_total, 92.0 / upem * 1.0)  # ~ session-1 cap size
if adv_total * scale > W - 200:
    scale = (W - 200) / adv_total
x_cursor = (W - adv_total * scale) / 2
glyph_strokes = []  # Strokes, unscheduled
wrng = random.Random(SEED + 7)
for c in TEXT:
    gname = cmap[ord(c)]
    adv = hmtx[gname][0]
    if c != " ":
        pen = ContourPen(gs)
        gs[gname].draw(pen)
        for contour in pen.contours:
            pts = [(x_cursor + x * scale, BASE_Y - y * scale) for (x, y) in contour]
            if len(pts) >= 2:
                glyph_strokes.append(Stroke(
                    jittered(pts, wrng, jit=0.8, step=6.0), width=2.6, color=INK))
    x_cursor += adv * scale

# baseline guide stroke, drawn just before the writing (as session 1)
guide = Stroke(jittered([(90, BASE_Y + 16), (W - 90, BASE_Y + 16)],
                        random.Random(SEED + 2), jit=0.5), width=1.4,
               color=(150, 138, 126))

# ---- schedule: meeting pace ----------------------------------------------
def schedule(strokes, t_start, t_end, speed=1500.0):
    durs = [max(s.total / speed, 0.06) for s in strokes]
    sc = (t_end - t_start) / sum(durs)
    t = t_start
    for s, d in zip(strokes, durs):
        s.t0, s.t1 = t, t + d * sc
        t = s.t1
schedule(acts["a1"], 0.3, 3.4)
schedule(acts["a2"], 3.4, 7.4)
schedule(acts["lights"], 7.5, 9.3)
for k, wi in enumerate(order):
    light_events.append((7.5 + (9.3 - 7.5) * (k + 0.35) / len(order), window_boxes[wi]))
guide.t0, guide.t1 = 9.35, 9.7
schedule(glyph_strokes, 9.7, 14.2, speed=2600.0)
all_strokes = acts["a1"] + acts["a2"] + acts["lights"] + [guide] + glyph_strokes

# ---- glow ------------------------------------------------------------------
def glow_sprite(size=256):
    g = Image.new("L", (size, size), 0)
    px = g.load()
    c = size / 2
    for y in range(size):
        for x in range(size):
            d = math.hypot(x-c, y-c) / c
            px[x, y] = max(0, int(255 * (1 - d) ** 2)) if d < 1 else 0
    return g
GLOW = glow_sprite()
FLAME_AT = (330, 344)
def glow_alpha(t):
    return 0.0 if t < 2.9 else min(0.5, (t - 2.9) / 1.2 * 0.5)

# ---- render ------------------------------------------------------------------
canvas = Image.new("RGB", (W * SS, H * SS), WHITE)
cd = ImageDraw.Draw(canvas)
S = lambda v: v * SS

def draw_segment(s, d_from, d_to):
    if d_to <= d_from: return
    p_from, p_to = s.point_at(d_from), s.point_at(d_to)
    cd.line([S(p_from[0]), S(p_from[1]), S(p_to[0]), S(p_to[1])],
            fill=s.color, width=max(1, int(s.width * SS)))
    for p in (p_from, p_to):
        r = s.width * SS / 2
        cd.ellipse([S(p[0]) - r, S(p[1]) - r, S(p[0]) + r, S(p[1]) + r], fill=s.color)

n_frames = int(FPS * DUR)
for f in range(n_frames):
    t = f / FPS
    pen = None
    for s in all_strokes:
        if s.t0 is None or t < s.t0: continue
        frac = 1.0 if t >= s.t1 else (t - s.t0) / (s.t1 - s.t0)
        target = frac * s.total
        if target > s.drawn:
            step = 6.0
            d = s.drawn
            while d < target:
                nd = min(d + step, target)
                draw_segment(s, d, nd)
                d = nd
            s.drawn = target
        if s.t0 <= t < s.t1:
            pen = s.point_at(target)
    frame = canvas.copy()
    fd = ImageDraw.Draw(frame, "RGBA")
    for (lt, box) in light_events:
        if t >= lt:
            a = min(235, int(235 * (t - lt) / 0.3)) if t - lt < 0.3 else 235
            fd.rectangle([S(box[0]), S(box[1]), S(box[2]), S(box[3])], fill=AMBER + (a,))
    ga = glow_alpha(t)
    if ga > 0:
        r = int(105 * SS)
        g = GLOW.resize((2 * r, 2 * r))
        warm = Image.new("RGB", (2 * r, 2 * r), (255, 186, 92))
        frame.paste(warm, (int(S(FLAME_AT[0])) - r, int(S(FLAME_AT[1])) - r),
                    g.point(lambda v: int(v * ga)))
        fd = ImageDraw.Draw(frame, "RGBA")
        fd.ellipse([S(324), S(338), S(336), S(356)], fill=FLAME + (235,))
    if pen is not None:
        fd.polygon([(S(pen[0]), S(pen[1] - 11)), (S(pen[0] + 8), S(pen[1])),
                    (S(pen[0]), S(pen[1] + 11)), (S(pen[0] - 8), S(pen[1]))], fill=INK)
    frame = frame.resize((W, H), Image.LANCZOS)
    frame.save(os.path.join(OUT, f"f{f:04d}.png"))
    if f % 120 == 0:
        print(f"frame {f}/{n_frames}", flush=True)
print("frames done:", n_frames, "| glyph strokes:", len(glyph_strokes))
