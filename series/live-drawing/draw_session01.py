#!/usr/bin/env python3
"""Live Drawing — practice session 01 (Wavelet 4, 2026-11-22).

Drawn route, Emise line-renderer lineage (cf. intro-prepass-work/draw_prepass.py):
deterministic, seeded 20261122; strokes are scheduled and drawn progressively
onto a persistent canvas, so the drawing visibly happens stroke by stroke.
Emise design language: flowing sharp line, fast-hand jitter and overshoot kept.

THE GROUND IS WHITE (Will, PH: Revenue, 2026-11-22 08:18 CST — animator skill
section 4, drawn canon point 6): the drawing is paper, not UI. Paper white
(255,255,255), first frame to last.

Subject — last night's arc in the Scroll Town chat:
  Act 1 (0-19s)   a lantern is drawn and lit
  Act 2 (19-38s)  rooftops drawn house by house along the street
  Act 3 (38-45s)  the windows answer, one by one
  Act 4 (45-58s)  a hand learns to write: "light the next light"
  Hold  (58-60s)  the finished page rests

Output: PNG frames at 1280x720, 24 fps, 60.0 s, silent (assembly is separate,
ranch-side). Frames land in ./frames-01/.
"""
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFont

W, H, SS = 1280, 720, 2
FPS, DUR = 24, 60.0
WHITE = (255, 255, 255)
INK   = (43, 32, 25)      # warm charcoal ink, as the prepass lineage
AMBER = (245, 176, 65)
FLAME = (238, 118, 38)
CORAL = (226, 105, 84)
SEED  = 20261122

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames-01")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- strokes
class Stroke:
    """A jittered polyline drawn over [t0, t1]; points are logical px."""
    def __init__(self, pts, width=2.4, color=INK):
        self.pts = pts
        self.width = width
        self.color = color
        # cumulative lengths
        self.cum = [0.0]
        for a, b in zip(pts, pts[1:]):
            self.cum.append(self.cum[-1] + math.hypot(b[0]-a[0], b[1]-a[1]))
        self.total = self.cum[-1]
        self.t0 = self.t1 = None
        self.drawn = 0.0  # length already committed to canvas

    def point_at(self, dist):
        if dist <= 0: return self.pts[0]
        if dist >= self.total: return self.pts[-1]
        for i in range(1, len(self.cum)):
            if dist <= self.cum[i]:
                f = (dist - self.cum[i-1]) / max(1e-6, self.cum[i] - self.cum[i-1])
                a, b = self.pts[i-1], self.pts[i]
                return (a[0] + (b[0]-a[0]) * f, a[1] + (b[1]-a[1]) * f)
        return self.pts[-1]

def jittered(pts, rng, jit=1.1, step=7.0, overshoot=0.0):
    """Subdivide a polyline, add fast-hand jitter, optional end overshoot."""
    out = []
    for a, b in zip(pts, pts[1:]):
        seg = math.hypot(b[0]-a[0], b[1]-a[1])
        n = max(2, int(seg / step))
        for i in range(n):
            f = i / n
            x = a[0] + (b[0]-a[0]) * f + rng.uniform(-jit, jit)
            y = a[1] + (b[1]-a[1]) * f + rng.uniform(-jit, jit)
            out.append((x, y))
    out.append(pts[-1])
    if overshoot and len(out) >= 2:
        (x1, y1), (x2, y2) = out[-2], out[-1]
        d = math.hypot(x2-x1, y2-y1) or 1.0
        out.append((x2 + (x2-x1)/d * overshoot, y2 + (y2-y1)/d * overshoot))
    return out

def arc_pts(cx, cy, r, a0, a1, n=26, ry=None):
    ry = r if ry is None else ry
    return [(cx + r * math.cos(math.radians(a0 + (a1-a0) * i/n)),
             cy + ry * math.sin(math.radians(a0 + (a1-a0) * i/n))) for i in range(n+1)]

# act -> list of Stroke (order = draw order)
acts = {"a1": [], "a2": [], "lights": [], "a3": []}
def add(act, pts, rng, width=2.4, color=INK, jit=1.1, overshoot=0.0):
    acts[act].append(Stroke(jittered(pts, rng, jit=jit, overshoot=overshoot),
                            width=width, color=color))

rng = random.Random(SEED)
GY = 470  # street ground line

# ---- Act 1: the lantern (post at x=250, lantern hangs at x=330) ----------
add("a1", [(228, GY), (272, GY)], rng, width=3.2)                       # base
add("a1", [(250, GY), (250, 302)], rng, width=3.4)                     # post
add("a1", [(250, 302), (332, 302)], rng, width=3.0, overshoot=3)       # crossbar
add("a1", [(330, 302), (330, 320)], rng, width=2.2)                    # chain
add("a1", [(313, 320), (347, 320)], rng, width=2.6)                    # lantern top
add("a1", [(313, 320), (319, 368)], rng, width=2.6)                    # left side
add("a1", [(347, 320), (341, 368)], rng, width=2.6)                    # right side
add("a1", [(319, 368), (341, 368)], rng, width=2.6)                    # bottom
add("a1", [(313, 320), (330, 306), (347, 320)], rng, width=2.2)        # cap
add("a1", arc_pts(330, 350, 7, 180, 360, n=14, ry=10) +
          [(337, 350), (330, 334), (323, 350)], rng, width=2.2, color=FLAME)  # flame
add("a1", [(330, 300), (330, 284)], rng, width=2.0)                    # finial
for dx, dy in [(-30, -22), (30, -22), (-36, 6), (36, 6)]:              # light rays
    add("a1", [(330+dx*0.55, 344+dy*0.55), (330+dx, 344+dy)], rng, width=2.0, color=AMBER)
add("a1", arc_pts(392, 268, 16, 200, 470, n=16), rng, width=1.8)       # wind curl
add("a1", arc_pts(414, 252, 9, 180, 430, n=12), rng, width=1.8)        # wind curl 2

# ---- Act 2: the street and five houses ----------------------------------
add("a2", [(56, GY), (640, GY)], rng, width=2.6)
add("a2", [(640, GY), (1224, GY)], rng, width=2.6)
houses = [  # x, width, height, chimney?
    (430, 112, 104, True), (566, 100, 88, False), (690, 118, 122, True),
    (832, 102, 94, False), (958, 122, 112, True),
]
window_boxes = []  # (x0,y0,x1,y1) in draw order = answering order shuffled by seed later
for (hx, hw, hh, chim) in houses:
    top = GY - hh
    add("a2", [(hx, GY), (hx, top), (hx+hw, top), (hx+hw, GY)], rng, width=2.6)
    add("a2", [(hx-10, top), (hx+hw/2, top-38), (hx+hw+10, top)], rng, width=2.8, overshoot=3)
    if chim:
        cx = hx + hw - 30
        add("a2", [(cx, top-26), (cx, top-48), (cx+16, top-48), (cx+16, top-30)], rng, width=2.2)
    dx = hx + hw/2 - 13  # door
    add("a2", [(dx, GY), (dx, GY-44), (dx+26, GY-44), (dx+26, GY)], rng, width=2.2)
    for wx in (hx + 16, hx + hw - 40):  # two windows
        wy = top + 26
        add("a2", [(wx, wy), (wx+24, wy), (wx+24, wy+28), (wx, wy+28), (wx, wy)], rng, width=1.9)
        add("a2", [(wx+12, wy), (wx+12, wy+28)], rng, width=1.2)
        add("a2", [(wx, wy+14), (wx+24, wy+14)], rng, width=1.2)
        window_boxes.append((wx+2, wy+2, wx+22, wy+26))
    for i in range(3):  # eave hatching, his manner
        hx0 = hx + 10 + i * 9
        add("a2", [(hx0, top+8), (hx0-6, top+20)], rng, width=1.1)
add("a2", arc_pts(1150, 128, 30, 200, 520, n=22), rng, width=2.2)      # crescent moon
add("a2", arc_pts(1161, 122, 25, 200, 520, n=20), rng, width=1.6)
for sx, sy in [(120, 110), (520, 84), (760, 140), (90, 210), (880, 70)]:  # stars
    add("a2", [(sx-7, sy), (sx+7, sy)], rng, width=1.6)
    add("a2", [(sx, sy-7), (sx, sy+7)], rng, width=1.6)

# ---- Act 3: windows answer (burst strokes; fills are timed events) ------
order = list(range(len(window_boxes)))
random.Random(SEED + 1).shuffle(order)
light_events = []  # (time, box)
for k, wi in enumerate(order):
    bx = window_boxes[wi]
    cx, cy = (bx[0]+bx[2])/2, (bx[1]+bx[3])/2
    for dx, dy in [(-16, -14), (16, -14), (-16, 14), (16, 14)]:
        add("lights", [(cx+dx*0.5, cy+dy*0.5), (cx+dx, cy+dy)], rng, width=1.5, color=AMBER)

# ---- schedule ------------------------------------------------------------
def schedule(strokes, t_start, t_end, speed=640.0):
    durs = [max(s.total / speed, 0.20) for s in strokes]
    scale = (t_end - t_start) / sum(durs)
    t = t_start
    for s, d in zip(strokes, durs):
        s.t0, s.t1 = t, t + d * scale
        t = s.t1
schedule(acts["a1"], 0.5, 19.0)
schedule(acts["a2"], 19.0, 38.0)
schedule(acts["lights"], 38.5, 45.0)
# light fill events follow the burst order timing (10 windows over 38.5-45)
for k, wi in enumerate(order):
    light_events.append((38.5 + (45.0 - 38.5) * (k + 0.35) / len(order), window_boxes[wi]))
all_strokes = acts["a1"] + acts["a2"] + acts["lights"]

# ---- glow sprite ----------------------------------------------------------
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
FLAME_AT = (330, 344)  # logical
def glow_alpha(t):  # flame lit at ~ end of flame stroke
    return 0.0 if t < 12.5 else min(0.5, (t - 12.5) / 3.0 * 0.5)

# ---- writing (Act 4): Emise letterforms under a moving pen ----------------
FONT_PATH = os.path.expanduser("~/workspace/emise-font/out/Emise.ttf")
TEXT = "light the next light"
TEXT_T0, TEXT_T1 = 45.5, 58.0
BASE_Y = 622
txt_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
td = ImageDraw.Draw(txt_img)
_size = 92
while True:  # fit the line inside the page margins, whatever the font's metrics
    font = ImageFont.truetype(FONT_PATH, _size)
    if td.textlength(TEXT, font=font) <= W - 200 or _size <= 40:
        break
    _size -= 4
tw = td.textlength(TEXT, font=font)
TX = (W - tw) // 2
td.text((TX, BASE_Y), TEXT, font=font, fill=INK + (255,), anchor="ls")
INK_BOX = txt_img.getbbox()  # true ink extent of the rendered line (logical px)
# baseline guide stroke (a normal stroke, drawn just before the writing)
guide = Stroke(jittered([(INK_BOX[0] - 14, BASE_Y + 16), (INK_BOX[2] + 14, BASE_Y + 16)],
                        random.Random(SEED + 2), jit=0.5), width=1.4, color=(150, 138, 126))
guide.t0, guide.t1 = 44.8, 45.5
all_strokes.append(guide)

# ---- render ---------------------------------------------------------------
canvas = Image.new("RGB", (W * SS, H * SS), WHITE)
cd = ImageDraw.Draw(canvas)
S = lambda v: v * SS

def draw_segment(s, d_from, d_to):
    if d_to <= d_from: return
    p_from, p_to = s.point_at(d_from), s.point_at(d_to)
    cd.line([S(p_from[0]), S(p_from[1]), S(p_to[0]), S(p_to[1])],
            fill=s.color, width=max(1, int(s.width * SS)))
    for p in (p_from, p_to):  # round joints
        r = s.width * SS / 2
        cd.ellipse([S(p[0]) - r, S(p[1]) - r, S(p[0]) + r, S(p[1]) + r], fill=s.color)

n_frames = int(FPS * DUR)
for f in range(n_frames):
    t = f / FPS
    # advance strokes
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
    # window fills (answering lights)
    for (lt, box) in light_events:
        if t >= lt:
            a = min(235, int(235 * (t - lt) / 0.5)) if t - lt < 0.5 else 235
            fd.rectangle([S(box[0]), S(box[1]), S(box[2]), S(box[3])], fill=AMBER + (a,))
    # flame fill + glow
    ga = glow_alpha(t)
    if ga > 0:
        r = int(105 * SS)
        g = GLOW.resize((2 * r, 2 * r))
        warm = Image.new("RGB", (2 * r, 2 * r), (255, 186, 92))
        frame.paste(warm, (int(S(FLAME_AT[0])) - r, int(S(FLAME_AT[1])) - r),
                    g.point(lambda v: int(v * ga)))
        fd = ImageDraw.Draw(frame, "RGBA")
        fd.ellipse([S(324), S(338), S(336), S(356)], fill=FLAME + (235,))
    # writing reveal
    if t >= TEXT_T0:
        frac = min(1.0, (t - TEXT_T0) / (TEXT_T1 - TEXT_T0))
        # reveal across the line's true ink extent, left to right
        reveal_w = int((INK_BOX[0] + frac * (INK_BOX[2] - INK_BOX[0])) * SS)
        if reveal_w > 0:
            crop = txt_img.resize((W * SS, H * SS), Image.LANCZOS).crop((0, 0, reveal_w, H * SS))
            frame.paste(crop, (0, 0), crop)
            fd = ImageDraw.Draw(frame, "RGBA")
        if frac < 1.0:  # pen nib at the frontier
            px_ = INK_BOX[0] + frac * (INK_BOX[2] - INK_BOX[0])
            py_ = BASE_Y - 18 + 3 * math.sin(t * 7)
            fd.polygon([(S(px_), S(py_ - 12)), (S(px_ + 9), S(py_)), (S(px_), S(py_ + 12)),
                        (S(px_ - 9), S(py_))], fill=INK + (255,))
    # stroke pen nib
    if pen is not None:
        fd.polygon([(S(pen[0]), S(pen[1] - 11)), (S(pen[0] + 8), S(pen[1])),
                    (S(pen[0]), S(pen[1] + 11)), (S(pen[0] - 8), S(pen[1]))], fill=INK)
    frame = frame.resize((W, H), Image.LANCZOS)
    frame.save(os.path.join(OUT, f"f{f:04d}.png"))
    if f % 240 == 0:
        print(f"frame {f}/{n_frames}", flush=True)
print("frames done:", n_frames)
