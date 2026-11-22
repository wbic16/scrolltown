#!/usr/bin/env python3
"""draw_prepass.py — Scrolltown 15s weekly intro PREPASS, drawn route.

Task 24.7.8/9.7.11/7.8.12. Arc sketch 22.6.9/8.6.10/7.6.9 (cited by
every packet). Deterministic, seeded (20261122): the Emise line
renderer lineage — programmatic pages in the Emise design language
(flowing sharp line, fast-hand jitter and overshoot kept, hatching
in Will's manner), characters drawn from the same primitives every
page so identity anchors hold BY CONSTRUCTION and are then
enumerated (packet IP-2), never assumed. No generative anything.

Format: 854x480, 24 fps, 360 frames, exactly 15.000 s, silent.
  frames   0- 95  Beat 1 — Fern lifts her lantern
  frames  96-215  Beat 2 — Waverly unrolls the Great Scroll
  frames 216-311  Beat 3 — pull wide, the real town answers
  frames 312-359  Beat 4 — SCROLLTOWN over the woven tiling field
Four-frame warm dips sit on the beat boundaries (96, 216, 312).

Usage: draw_prepass.py [all|N,N,...] [outdir]
Writes frame_%03d.png + anchors-manifest.json + field-manifest.json
+ build_log.json into outdir.
"""
import json, math, os, random, sys
from PIL import Image, ImageDraw, ImageFont

SEED = 20261122
W, H = 854, 480
SS = 2
FPS = 24
TOTAL = 360
FONT_PATH = os.environ.get("EMISE_FONT",
    os.path.expanduser("~/workspace/emise-font/out/Emise.ttf"))

INK    = (43, 32, 25)
PAPER  = (253, 251, 240)
BLUE   = (27, 52, 178)
SKIN   = (244, 196, 150)
HAIR   = (74, 46, 32)
SWEATER= (250, 240, 214)
CORAL  = (232, 106, 79)
BUTTER = (246, 199, 92)
BRASS  = (196, 150, 52)
MINT   = (148, 216, 178)
PLUM   = (86, 44, 92)
GOLD   = (232, 178, 60)
HAIRW  = (38, 26, 22)
AMBER  = (255, 183, 77)
FLAME  = (255, 176, 66)
DARKWIN= (52, 44, 58)
CREAM2 = (244, 232, 200)

def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def clamp01(t): return max(0.0, min(1.0, t))

class Painter:
    """All drawing at SS supersample; coordinates given at 1x."""
    def __init__(self):
        self.img = Image.new("RGB", (W * SS, H * SS), PAPER)
        self.d = ImageDraw.Draw(self.img, "RGBA")
        self.overlay = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
        self.od = ImageDraw.Draw(self.overlay)

    def S(self, v): return v * SS

    def line(self, pts, fill=INK, width=2, rng=None, jit=1.2, overshoot=0.0):
        p = [(x * SS, y * SS) for (x, y) in pts]
        if rng is not None:
            p = [(x + rng.uniform(-jit, jit) * SS * 0.4,
                  y + rng.uniform(-jit, jit) * SS * 0.4) for (x, y) in p]
        if overshoot and len(p) == 2:
            (x0, y0), (x1, y1) = p
            dx, dy = x1 - x0, y1 - y0
            L = math.hypot(dx, dy) or 1.0
            p = [(x0 - dx / L * overshoot * SS, y0 - dy / L * overshoot * SS),
                 (x1 + dx / L * overshoot * SS, y1 + dy / L * overshoot * SS)]
        self.d.line(p, fill=fill, width=max(1, int(width * SS)))

    def poly(self, pts, fill, outline=INK, width=2):
        p = [(x * SS, y * SS) for (x, y) in pts]
        self.d.polygon(p, fill=fill, outline=outline, width=max(1, int(width * SS)))

    def rect(self, box, fill, outline=None, width=2):
        b = [v * SS for v in box]
        self.d.rectangle(b, fill=fill,
                         outline=outline, width=max(1, int(width * SS)) if outline else 1)

    def ellipse(self, box, fill, outline=None, width=2):
        b = [v * SS for v in box]
        self.d.ellipse(b, fill=fill,
                       outline=outline, width=max(1, int(width * SS)) if outline else 1)

    def hatch_rect(self, box, color, rng, spacing=5, width=1):
        # 45-degree hatch (constant x+y), each segment clipped to the box
        x0, y0, x1, y1 = box
        c = x0 + y0
        while c < x1 + y1:
            xa = max(x0, c - y1); xb = min(x1, c - y0)
            if xb > xa:
                self.line([(xa, c - xa), (xb, c - xb)], fill=color,
                          width=width, rng=rng, jit=0.7)
            c += spacing + rng.uniform(-1.2, 1.2)

    def glow(self, cx, cy, r, color=FLAME, peak=110):
        for i in range(5, 0, -1):
            rr = r * i / 5
            a = int(peak * (6 - i) / 5)
            self.od.ellipse([(cx - rr) * SS, (cy - rr) * SS,
                             (cx + rr) * SS, (cy + rr) * SS],
                            fill=color + (a,))

    def finish(self):
        out = Image.alpha_composite(self.img.convert("RGBA"), self.overlay)
        return out.convert("RGB").resize((W, H), Image.LANCZOS)

# ---------------------------------------------------------------- sky/town
def sky(p, top=(56, 40, 76), horizon=(216, 138, 92), h=404):
    bands = 24
    for i in range(bands):
        t = i / bands
        c = tuple(int(top[k] + (horizon[k] - top[k]) * t) for k in range(3))
        y0 = h * i / bands
        p.rect([0, y0, W, h * (i + 1) / bands + 1], fill=c)

def house(p, x, gy, w, h, rng, lit=(), body=(96, 74, 88), roof=(64, 44, 54)):
    """One house, base at ground gy. lit = set of window indices lit (0..3)."""
    p.rect([x, gy - h, x + w, gy], fill=body, outline=INK, width=2)
    p.poly([(x - 4, gy - h), (x + w / 2, gy - h - w * 0.42), (x + w + 4, gy - h)],
           fill=roof, outline=INK, width=2)
    p.hatch_rect([x + 3, gy - h + 3, x + w - 3, gy - 6], (0, 0, 0), rng, spacing=7)
    wins = []
    for r in range(2):
        for cix in range(2):
            wx = x + w * (0.22 + 0.36 * cix)
            wy = gy - h * (0.62 - 0.3 * r)
            wins.append((wx, wy))
    for i, (wx, wy) in enumerate(wins):
        p.rect([wx - 5, wy - 6, wx + 5, wy + 6],
               fill=AMBER if i in lit else DARKWIN, outline=INK, width=1)
    p.rect([x + w / 2 - 5, gy - 16, x + w / 2 + 5, gy], fill=(70, 50, 40),
           outline=INK, width=1)
    return wins

# ---------------------------------------------------------------- Fern
def draw_fern(p, cx, gy, s, arm_raise, lit, rng, anchors=None, tag="fern"):
    """Fern, feet at (cx, gy), total height s. arm_raise 0..1, lit 0..1.
    Returns lantern flame center."""
    u = s / 190.0  # unit against the 190px reference staging
    def X(dx): return cx + dx * u
    def Y(dy): return gy - dy * u
    # legs + sneakers
    p.rect([X(-16), Y(52), X(-3), Y(10)], fill=CORAL, outline=INK, width=2)
    p.rect([X(3), Y(52), X(16), Y(10)], fill=CORAL, outline=INK, width=2)
    p.ellipse([X(-22), Y(12), X(-1), Y(1)], fill=MINT, outline=INK, width=2)
    p.ellipse([X(1), Y(12), X(22), Y(1)], fill=MINT, outline=INK, width=2)
    # torso: sweater + overalls bib + straps
    p.poly([(X(-24), Y(52)), (X(24), Y(52)), (X(21), Y(108)), (X(-21), Y(108))],
           fill=SWEATER, outline=INK, width=2)
    p.rect([X(-15), Y(96), X(15), Y(52)], fill=CORAL, outline=INK, width=2)
    p.rect([X(-15), Y(108), X(-7), Y(96)], fill=CORAL, outline=INK, width=1)
    p.rect([X(7), Y(108), X(15), Y(96)], fill=CORAL, outline=INK, width=1)
    p.ellipse([X(-11), Y(100), X(-5), Y(94)], fill=BRASS, outline=INK, width=1)
    p.ellipse([X(5), Y(100), X(11), Y(94)], fill=BRASS, outline=INK, width=1)
    # head + hair + buns (anchors)
    hx, hy, hr = cx, Y(140), 30 * u
    p.ellipse([hx - hr * 1.12, hy - hr * 1.05, hx + hr * 1.12, hy + hr * 0.75],
              fill=HAIR, outline=INK, width=2)
    bun_l = (hx - hr * 0.78, hy - hr * 0.92)
    bun_r = (hx + hr * 0.78, hy - hr * 0.92)
    br = hr * 0.46
    p.ellipse([bun_l[0] - br, bun_l[1] - br, bun_l[0] + br, bun_l[1] + br],
              fill=HAIR, outline=INK, width=2)
    p.ellipse([bun_r[0] - br, bun_r[1] - br, bun_r[0] + br, bun_r[1] + br],
              fill=HAIR, outline=INK, width=2)
    for b in (bun_l, bun_r):  # scroll swirl on each bun
        p.line([(b[0] - br * 0.5, b[1]), (b[0] + br * 0.4, b[1] - br * 0.3)],
               fill=(120, 84, 52), width=1, rng=rng, jit=0.5)
    p.ellipse([hx - hr * 0.82, hy - hr * 0.55, hx + hr * 0.82, hy + hr * 0.95],
              fill=SKIN, outline=INK, width=2)
    p.ellipse([hx - hr * 0.34, hy + hr * 0.02, hx - hr * 0.16, hy + hr * 0.24],
              fill=(146, 84, 32), width=1)
    p.ellipse([hx + hr * 0.16, hy + hr * 0.02, hx + hr * 0.34, hy + hr * 0.24],
              fill=(146, 84, 32), width=1)
    for fx in (-0.52, -0.38, 0.38, 0.52):
        for fy in (0.34, 0.46):
            p.ellipse([hx + hr * fx - 1.3 * u, hy + hr * fy - 1.3 * u,
                       hx + hr * fx + 1.3 * u, hy + hr * fy + 1.3 * u],
                      fill=(196, 120, 74), width=1)
    p.line([(hx - hr * 0.2, hy + hr * 0.58), (hx + hr * 0.2, hy + hr * 0.58)],
           fill=(146, 84, 32), width=2, rng=rng, jit=0.4)
    # scarf bow at neck (anchor)
    bow = (hx, Y(112))
    p.poly([(bow[0], bow[1]), (bow[0] - 15 * u, bow[1] - 8 * u),
            (bow[0] - 14 * u, bow[1] + 7 * u)], fill=BUTTER, outline=INK, width=2)
    p.poly([(bow[0], bow[1]), (bow[0] + 15 * u, bow[1] - 8 * u),
            (bow[0] + 14 * u, bow[1] + 7 * u)], fill=BUTTER, outline=INK, width=2)
    p.ellipse([bow[0] - 5 * u, bow[1] - 5 * u, bow[0] + 5 * u, bow[1] + 5 * u],
              fill=BUTTER, outline=INK, width=2)
    # key-badge on dark cord (anchor)
    badge = (hx, Y(84))
    p.line([(hx - 9 * u, Y(110)), badge, (hx + 9 * u, Y(110))],
           fill=(40, 32, 28), width=2, rng=rng, jit=0.4)
    p.ellipse([badge[0] - 6.5 * u, badge[1] - 6.5 * u,
               badge[0] + 6.5 * u, badge[1] + 6.5 * u],
              fill=BRASS, outline=INK, width=2)
    p.ellipse([badge[0] - 2.4 * u, badge[1] - 2.4 * u,
               badge[0] + 2.4 * u, badge[1] + 2.4 * u],
              fill=(120, 88, 30), width=1)
    # left arm resting
    p.line([(X(-21), Y(102)), (X(-30), Y(66))], fill=SWEATER, width=int(7 * u) + 2)
    p.line([(X(-21), Y(102)), (X(-30), Y(66))], fill=INK, width=1, rng=rng, jit=0.5)
    # right arm + lantern: hand travels an arc from hip to raised
    sh = (X(21), Y(102))
    hand_dn = (X(34), Y(58))
    hand_up = (X(40), Y(138))
    t = ease(arm_raise)
    hx2 = hand_dn[0] + (hand_up[0] - hand_dn[0]) * t
    hy2 = hand_dn[1] + (hand_up[1] - hand_dn[1]) * t - math.sin(t * math.pi) * 8 * u
    p.line([sh, (hx2, hy2)], fill=SWEATER, width=int(7 * u) + 2)
    p.line([sh, (hx2, hy2)], fill=INK, width=1, rng=rng, jit=0.5)
    # lantern hangs below the hand when low, rides at hand when raised
    lx = hx2 + 4 * u
    ly = hy2 + (16 * u) * (1 - t) + 4 * u
    p.line([(hx2, hy2), (lx, ly - 8 * u)], fill=INK, width=2)
    p.poly([(lx - 9 * u, ly - 8 * u), (lx + 9 * u, ly - 8 * u),
            (lx + 7 * u, ly + 12 * u), (lx - 7 * u, ly + 12 * u)],
           fill=(88, 66, 40), outline=INK, width=2)
    flame_c = (lx, ly + 2 * u)
    fr = (3 + 6 * lit) * u
    p.ellipse([flame_c[0] - fr * 0.62, flame_c[1] - fr, flame_c[0] + fr * 0.62,
               flame_c[1] + fr], fill=FLAME, outline=(180, 110, 20), width=1)
    if anchors is not None:
        anchors[f"{tag}-bun-l"] = [round(bun_l[0], 1), round(bun_l[1], 1), "hair"]
        anchors[f"{tag}-bun-r"] = [round(bun_r[0], 1), round(bun_r[1], 1), "hair"]
        anchors[f"{tag}-bow"] = [round(bow[0], 1), round(bow[1], 1), "butter"]
        anchors[f"{tag}-badge"] = [round(badge[0], 1), round(badge[1], 1), "brass"]
    return flame_c

# ---------------------------------------------------------------- Waverly
def draw_waverly(p, cx, gy, s, rng, anchors=None):
    """Waverly standing, facing left toward the scroll. Height s."""
    u = s / 210.0
    def X(dx): return cx + dx * u
    def Y(dy): return gy - dy * u
    # long coat
    p.poly([(X(-22), Y(0)), (X(24), Y(0)), (X(17), Y(128)), (X(-16), Y(128))],
           fill=PLUM, outline=INK, width=2)
    p.hatch_rect([X(-14), Y(60), X(14), Y(8)], (58, 26, 64), rng, spacing=6)
    p.line([(X(0), Y(126)), (X(1), Y(4))], fill=GOLD, width=2, rng=rng, jit=0.5)
    p.rect([X(-14), Y(112), X(15), Y(86)], fill=(214, 188, 150), outline=INK, width=1)  # apron
    p.line([(X(-8), Y(104)), (X(-4), Y(92))], fill=BLUE, width=2, rng=rng, jit=0.4)     # quill
    # head + long hair + gold streak (anchors)
    hx, hy, hr = cx, Y(158), 27 * u
    p.poly([(hx - hr * 1.05, hy - hr * 0.4), (hx + hr * 1.05, hy - hr * 0.4),
            (hx + hr * 0.9, Y(84)), (hx - hr * 0.9, Y(84))], fill=HAIRW, outline=INK, width=2)
    p.ellipse([hx - hr, hy - hr * 1.1, hx + hr, hy + hr * 0.8], fill=HAIRW, outline=INK, width=2)
    p.ellipse([hx - hr * 0.8, hy - hr * 0.5, hx + hr * 0.8, hy + hr * 0.9],
              fill=(246, 204, 158), outline=INK, width=2)
    streak = (hx - hr * 0.52, hy + hr * 0.1)
    p.line([(hx - hr * 0.45, hy - hr * 0.95), (hx - hr * 0.58, hy + hr * 0.2),
            (hx - hr * 0.5, Y(96))], fill=GOLD, width=int(3.4 * u) + 1, rng=rng, jit=0.5)
    p.ellipse([hx - hr * 0.3, hy + hr * 0.05, hx - hr * 0.13, hy + hr * 0.26],
              fill=(90, 52, 30), width=1)
    p.line([(hx - hr * 0.22, hy + hr * 0.55), (hx + hr * 0.1, hy + hr * 0.55)],
           fill=(120, 70, 40), width=2, rng=rng, jit=0.4)
    # arms forward, holding the scroll's right roll
    p.line([(X(-14), Y(118)), (X(-44), Y(96))], fill=PLUM, width=int(7 * u) + 2)
    p.line([(X(-14), Y(118)), (X(-44), Y(96))], fill=INK, width=1, rng=rng, jit=0.5)
    if anchors is not None:
        anchors["waverly-streak"] = [round(streak[0], 1), round(streak[1], 1), "gold"]
        anchors["waverly-coat"] = [round(X(6), 1), round(Y(40), 1), "plum"]
    return (X(-44), Y(96))

# ---------------------------------------------------------------- scroll
def draw_scroll(p, x_roll_r, gy_top, open_t, lit_houses, rng):
    """The Great Scroll: right roll fixed at x_roll_r; unrolls leftward.
    gy_top = top edge y. Returns nothing. Drawn town: 10 tiny houses."""
    full_w = 400
    wdt = 30 + (full_w - 30) * ease(open_t)
    x1 = x_roll_r - wdt
    hgt = 120
    y1 = gy_top + hgt
    # parchment
    p.rect([x1, gy_top, x_roll_r, y1], fill=CREAM2, outline=INK, width=2)
    p.hatch_rect([x1 + 4, y1 - 6, x_roll_r - 4, gy_top + 4], (206, 188, 148), rng, spacing=9)
    # rolls: right (held) and left (free end)
    for rx in (x_roll_r, x1):
        p.rect([rx - 7, gy_top - 12, rx + 7, y1 + 12], fill=(150, 108, 62), outline=INK, width=2)
        p.ellipse([rx - 7, gy_top - 16, rx + 7, gy_top - 6], fill=(178, 134, 84), outline=INK, width=1)
    if open_t < 0.25:
        return
    # drawn town on the page: baseline + 10 tiny ink houses
    base = y1 - 18
    p.line([(x1 + 14, base), (x_roll_r - 14, base)], fill=INK, width=2, rng=rng, jit=0.6)
    span = (x_roll_r - 28) - (x1 + 14)
    for i in range(10):
        hx = x1 + 16 + span * (i + 0.5) / 10
        hw = min(26, span / 10 - 4)
        hh = 20 + (i * 7 % 13)
        p.rect([hx - hw / 2, base - hh, hx + hw / 2, base], fill=None or (238, 226, 192), outline=INK, width=1)
        p.poly([(hx - hw / 2 - 2, base - hh), (hx, base - hh - 8), (hx + hw / 2 + 2, base - hh)],
               fill=(238, 226, 192), outline=INK, width=1)
        p.rect([hx - 3, base - hh + 8, hx + 3, base - hh + 15],
               fill=AMBER if i < lit_houses else (120, 108, 84), outline=INK, width=1)
    # drawn hills + sun lines
    p.line([(x1 + 16, gy_top + 22), (x1 + 70, gy_top + 12), (x1 + 120, gy_top + 22)],
           fill=INK, width=1, rng=rng, jit=0.6)

# ---------------------------------------------------------------- wide town
TOWN_RNG = random.Random(SEED + 7)
TOWN = []
_x = 18
while _x < W - 60:
    _w = TOWN_RNG.uniform(56, 92)
    _h = TOWN_RNG.uniform(64, 118)
    TOWN.append((_x, _w, _h))
    _x += _w + TOWN_RNG.uniform(10, 26)
WIN_SCHEDULE = []
for hi, (hx, hw, hh) in enumerate(TOWN):
    for wi in range(4):
        WIN_SCHEDULE.append((hi, wi))
TOWN_RNG.shuffle(WIN_SCHEDULE)
WIN_ONSET = {k: 222 + int(78 * i / max(1, len(WIN_SCHEDULE) - 1))
             for i, k in enumerate(WIN_SCHEDULE)}

def draw_wide_town(p, f, rng):
    sky(p)
    gy = 402
    # tower silhouette, center-back
    p.rect([0, gy, W, 448], fill=(70, 54, 48), width=1)
    p.rect([402, gy - 218, 452, gy], fill=(74, 56, 74), outline=INK, width=2)
    p.poly([(396, gy - 218), (427, gy - 252), (458, gy - 218)], fill=(54, 40, 56), outline=INK, width=2)
    p.ellipse([410, gy - 208, 444, gy - 174], fill=AMBER if f > 250 else (226, 208, 170),
              outline=INK, width=2)
    p.line([(427, gy - 191), (427, gy - 202)], fill=INK, width=2)
    p.line([(427, gy - 191), (437, gy - 186)], fill=INK, width=2)
    # river bend, bottom
    p.poly([(0, 448), (240, 424), (520, 442), (854, 428), (854, 480), (0, 480)],
           fill=(70, 96, 128), outline=INK, width=2)
    for i in range(7):
        yy = 440 + i * 5
        p.line([(40 + (i * 53) % 300, yy), (180 + (i * 53) % 300, yy)],
               fill=(120, 150, 190), width=1, rng=rng, jit=0.8)
    p.rect([0, gy, W, gy + 6], fill=(60, 46, 40), width=1)
    for hi, (hx, hw, hh) in enumerate(TOWN):
        lit = {wi for wi in range(4) if WIN_ONSET[(hi, wi)] <= f}
        house(p, hx, gy, hw, hh, rng, lit=lit,
              body=(104, 80, 94) if hi % 2 else (92, 70, 86))
    return gy

# ---------------------------------------------------------------- tiling field
FIELD_N = 10
FIELD_CELL = 46.0
FIELD_C = (W / 2, H / 2 - 8)
SQ2 = math.sqrt(2.0)
def field_lines():
    rng = random.Random(SEED + 99)
    lines = []
    for i in range(FIELD_N):
        for j in range(FIELD_N):
            parity = (i + j) % 2
            for k in range(5):
                off = (k + 1) / 6
                if parity == 0:
                    a, b = (i, j + off), (i + 1, j + off)
                else:
                    a, b = (i + off, j), (i + off, j + 1)
                lines.append({"box": [i, j], "idx": k, "parity": parity,
                              "a": a, "b": b, "birth": 312 + rng.randrange(0, 20)})
    return lines
FIELD = field_lines()
def g2s(u, v):
    x = (u - FIELD_N / 2) * FIELD_CELL
    y = (v - FIELD_N / 2) * FIELD_CELL
    return (FIELD_C[0] + (x - y) / SQ2, FIELD_C[1] + (x + y) / SQ2)
def field_manifest():
    out = []
    for L in FIELD:
        ax, ay = g2s(*L["a"]); bx, by = g2s(*L["b"])
        out.append({"box": L["box"], "idx": L["idx"], "parity": L["parity"],
                    "mid": [round((ax + bx) / 2, 1), round((ay + by) / 2, 1)],
                    "a": [round(ax, 1), round(ay, 1)], "b": [round(bx, 1), round(by, 1)]})
    return out

# ---------------------------------------------------------------- beats
def beat1(f):
    p = Painter()
    rng = random.Random(SEED + f)
    sky(p)
    gy = 404
    p.rect([0, gy, W, H], fill=(70, 54, 48), width=1)
    # dark houses behind; nearest window answers late in the beat
    house(p, 560, gy, 120, 128, rng, lit={1} if f > 78 else set())
    house(p, 66, gy, 96, 100, rng, lit=set(), body=(88, 68, 82))
    house(p, 700, gy, 92, 92, rng, lit=set(), body=(88, 68, 82))
    # anticipation: held still frames 8-20, then one eased lift
    raise_t = ease(clamp01((f - 20) / 62))
    lit = clamp01((f - 30) / 50)
    anchors = {}
    flame = draw_fern(p, 330, gy, 196, raise_t, lit, rng, anchors)
    if lit > 0.05:
        p.glow(flame[0], flame[1], 26 + 74 * lit, peak=int(40 + 70 * lit))
        p.glow(330, gy - 4, 60 + 90 * lit, color=(255, 150, 70), peak=36)
    return p.finish(), anchors

def beat2(f):
    p = Painter()
    rng = random.Random(SEED + f)
    sky(p)
    gy = 404
    p.rect([0, gy, W, H], fill=(70, 54, 48), width=1)
    house(p, 778, gy, 68, 96, rng, lit={1, 3})
    house(p, 40, gy, 84, 88, rng, lit=set(), body=(88, 68, 82))
    anchors = {}
    # Fern smaller at the left edge, lantern raised toward Waverly
    flame = draw_fern(p, 118, gy, 150, 1.0, 1.0, rng, anchors)
    p.glow(flame[0], flame[1], 74, peak=96)
    # Waverly right of center; scroll unrolls leftward from her hands
    hand = draw_waverly(p, 716, gy, 216, rng, anchors)
    open_t = ease(clamp01((f - 110) / 60)) if f >= 96 else 0.0
    lit_houses = max(0, min(10, int((f - 150) / 6) + 1)) if f >= 150 else 0
    draw_scroll(p, 668, 208, open_t, lit_houses, rng)
    return p.finish(), anchors

def beat3(f):
    p = Painter()
    rng = random.Random(SEED + f)
    gy = draw_wide_town(p, f, rng)
    anchors = {}
    # Fern + Waverly small at center; anchors attempted at small scale
    draw_fern(p, 392, gy, 56, 1.0, 1.0, rng, anchors)
    draw_waverly(p, 470, gy, 62, rng, anchors)
    img = p.finish()
    # the pull: crop fraction eases 0.46 -> 1.0 across frames 224-280
    z = 0.46 + 0.54 * ease(clamp01((f - 224) / 56))
    if z < 0.999:
        cw, ch = int(W * z), int(H * z)
        cx0 = int((W - cw) * 0.5); cy0 = int((H - ch) * 0.62)
        img = img.crop((cx0, cy0, cx0 + cw, cy0 + ch)).resize((W, H), Image.LANCZOS)
        sc = 1.0 / z
        for k in list(anchors):
            x, y, fam = anchors[k]
            anchors[k] = [round((x - cx0) * sc, 1), round((y - cy0) * sc, 1), fam]
    return img, anchors

def beat4(f):
    p = Painter()
    rng = random.Random(SEED + f)
    p.rect([0, 0, W, H], fill=PAPER, width=1)
    for L in FIELD:
        if f >= L["birth"]:
            a = g2s(*L["a"]); b = g2s(*L["b"])
            lr = random.Random(SEED + L["box"][0] * 131 + L["box"][1] * 17 + L["idx"])
            p.line([a, b], fill=BLUE, width=2, rng=lr, jit=1.4, overshoot=1.6)
    # dim the field, keep the lit town strip at the bottom
    p.od.rectangle([0, 0, W * SS, H * SS], fill=(253, 251, 240, 120))
    img0 = p.finish()
    p2 = Painter(); p2.img = img0.resize((W * SS, H * SS), Image.LANCZOS).convert("RGB"); p2.d = ImageDraw.Draw(p2.img, "RGBA")
    p2.overlay = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    p2.od = ImageDraw.Draw(p2.overlay)
    gy = 452
    p2.rect([0, gy - 44, W, H], fill=(56, 42, 54), width=1)
    r2 = random.Random(SEED + 5)
    for hi, (hx, hw, hh) in enumerate(TOWN):
        house(p2, hx, gy + 22, hw * 0.8, 44, r2, lit={0, 1, 2, 3},
              body=(104, 80, 94) if hi % 2 else (92, 70, 86))
    img = p2.finish()
    # SCROLLTOWN letters, one per 3 frames from 324, Emise font (img is 1x here)
    word = "SCROLLTOWN"
    size = 92
    tmp = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    while size > 10:
        font = ImageFont.truetype(FONT_PATH, size)
        if tmp.textlength(word, font=font) <= 600:
            break
        size -= 4
    shown = max(0, min(len(word), int((f - 324) / 3) + 1)) if f >= 324 else 0
    if shown:
        d = ImageDraw.Draw(img)
        total = d.textlength(word, font=font)
        x = (W - total) / 2
        y = 150
        for i, ch in enumerate(word[:shown]):
            lr = random.Random(SEED + 1000 + i)
            d.text((x + lr.uniform(-1.5, 1.5), y + lr.uniform(-1.5, 1.5)),
                   ch, font=font, fill=(16, 34, 138))
            x += d.textlength(ch, font=font)
    return img, {}

BEATS = [(0, 95, beat1), (96, 215, beat2), (216, 311, beat3), (312, 359, beat4)]
DIPS = [96, 216, 312]

def render_frame(f):
    for lo, hi, fn in BEATS:
        if lo <= f <= hi:
            img, anchors = fn(f)
            break
    # warm dip on beat boundaries
    for b in DIPS:
        dist = abs(f - b + 0.5)
        if dist < 2.5:
            a = int(150 * (1 - dist / 2.5))
            ov = Image.new("RGBA", img.size, (24, 14, 10, a))
            img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    return img, anchors

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    outdir = args[1] if len(args) > 1 else "frames"
    os.makedirs(outdir, exist_ok=True)
    if args and args[0] != "all":
        frames = [int(x) for x in args[0].split(",")]
    else:
        frames = list(range(TOTAL))
    manifest = {}
    for f in frames:
        img, anchors = render_frame(f)
        img.save(os.path.join(outdir, f"frame_{f:03d}.png"))
        if anchors:
            manifest[str(f)] = anchors
        if f % 60 == 0:
            print(f"frame {f}", flush=True)
    if frames == list(range(TOTAL)):
        with open(os.path.join(outdir, "anchors-manifest.json"), "w") as fh:
            json.dump(manifest, fh, indent=1)
        with open(os.path.join(outdir, "field-manifest.json"), "w") as fh:
            json.dump(field_manifest(), fh, indent=1)
        with open(os.path.join(outdir, "build_log.json"), "w") as fh:
            json.dump({"seed": SEED, "frames": TOTAL, "fps": FPS, "size": [W, H],
                       "renderer": "draw_prepass.py (Emise line renderer lineage)",
                       "sketch": "22.6.9/8.6.10/7.6.9"}, fh, indent=1)
    print("done:", len(frames), "frames ->", outdir)

if __name__ == "__main__":
    main()
