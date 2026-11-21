#!/usr/bin/env python3
"""gate_validator.py — mechanical per-page validator for toll-gate repro pages.

Built 2026-11-21 (task 21.6.7/8.5.10/5.5.6) after Will judged the Gate 1
Steamboat Willie prepass "doesn't look good yet" and ordered a validator.
QC-v4 had checked the prepass by sampled visual frame-compare at 12
timestamps; this instrument checks EVERY page against its matched original
frame, structurally — the repro is a contour+hatching rendering, so the
comparison is structure, not pixels.

Measures per page (working size = the page's own 1040x864 canvas; the
original frame is resampled onto it):

  (a) Edge agreement. The original is reduced to a strong-edge map
      (gradient magnitude on a lightly blurred grayscale, top band).
      The repro's ink strokes ARE its contours, so the repro edge map is
      its ink mask. Scores: coverage = fraction of the original's strong
      edges within TAU px (Chebyshev) of repro ink; symmetric Chamfer =
      mean clipped distance both ways (original edges -> repro ink,
      repro ink -> original edges).
  (b) Ink mass. Per-cell (8x6 grid) ink-density comparison, plus
      solid_density: the repro's ink density inside the original's
      near-black regions — the direct measure of the prepass's known
      weak point, solid-black figures rendered as wash + sparse hatch
      instead of dense ink (arc sketch P3, QC-v4). The film's own gray
      wash backgrounds are excluded from "original ink" by thresholding
      below the wash.
  (c) Component sanity, in the figure band. Connected components of at
      least FIG_MIN px (half resolution), the original's near-black
      solids against the repro's ink. Only the extreme bounds gate: a
      solid shattered into stroke confetti (figure-count log-ratio very
      negative) or true figure merging (very positive). Richer component
      comparisons were tested and rejected on evidence — on line art
      they read stroke connectivity, not figure merging; the merged-
      figure failure in this renderer is carried by the edges measure
      (merging destroys contour correspondence). Full calibration
      evidence: VALIDATOR-REPORT.md.
  (d) Title/lettering pages are auto-FLAGGED for human review regardless
      of score. The validator does not pretend to judge letterforms.

Verdict: PASS only if every scored measure clears its threshold and the
page is not a title page. Standing rule (Will's direction, 2026-11-21):
no repro page enters an assembly (flipbook, full render) unless it
validator-PASSes or carries a resolved human-review flag.

Usage:
  gate_validator.py --gate-dir DIR [--out PREFIX] [--pages a,b,c]
Expects in DIR: pages/pageNNpP-tTTTT.T.png, shotframes2/shotNNpP-tTTTT.T.png,
plan.json ([shot, part, timestamp] per page), titles.json (optional list of
page stems in title shots; defaults to the Gate 1 cards).
Outputs PREFIX-scores.json and prints the per-page table.
"""

import argparse
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

# ---- thresholds (calibrated on Gate 1, 2026-11-21; see VALIDATOR-REPORT.md)
TAU = 4                # px, edge coverage tolerance (Chebyshev, 1040x864 canvas)
CHAMFER_CLIP = 16      # px, distances clipped here for the Chamfer mean
EDGE_COV_MIN = 0.72    # fraction of original strong edges covered
CHAMFER_MAX = 2.2      # symmetric mean clipped distance, px
INK_LOG2_MAX = 2.2     # |log2(repro ink / original ink)| ceiling
INK_DEMAND_MIN = 0.045     # orig ink fraction needed for the ratio test
BLACK_DEMAND_MIN = 0.08    # orig near-black fraction that counts as demand
INK_IN_BLACK_MIN = 0.015   # min repro ink density inside demanded black
FIG_MIN = 100          # px at half res: smallest figure-band component
FIG_MERGE_MAX = 1.0    # log2(orig figures / repro figures): merging bound
FIG_FRAG_MAX = 2.5     # shattering bound (negative direction)
GRID = (8, 6)          # ink-mass grid, cols x rows

INK_LUM = 150          # repro ink: luminance below this on cream paper
ORIG_INK_LUM = 90      # original ink: below the film's gray wash background
ORIG_BLACK_LUM = 45    # original near-black (solid figure) threshold
WASH_HI = 215          # repro wash band: INK_LUM..WASH_HI inside orig black


def load_gray(path, size=None):
    im = Image.open(path).convert("L")
    if size is not None and im.size != size:
        im = im.resize(size, Image.LANCZOS)
    return np.asarray(im).astype(np.float32)


def dilate(mask, steps):
    """Chebyshev dilation by `steps` px (3x3 structuring element)."""
    m = mask
    for _ in range(steps):
        p = np.pad(m, 1, mode="constant")
        m = (p[:-2, :-2] | p[:-2, 1:-1] | p[:-2, 2:] |
             p[1:-1, :-2] | p[1:-1, 1:-1] | p[1:-1, 2:] |
             p[2:, :-2] | p[2:, 1:-1] | p[2:, 2:])
    return m


def clipped_distance(target_mask, source_mask, clip):
    """For each pixel in target_mask, Chebyshev distance to source_mask,
    clipped at `clip`. Built by accumulating first-hit dilation rings."""
    dist = np.full(target_mask.shape, clip, dtype=np.float32)
    covered = np.zeros_like(target_mask)
    frontier = source_mask.copy()
    remaining = target_mask.copy()
    hit = remaining & frontier
    dist[hit] = 0.0
    covered |= hit
    for d in range(1, clip):
        frontier = dilate(frontier, 1)
        hit = remaining & frontier & ~covered
        if not hit.any():
            break
        dist[hit] = float(d)
        covered |= hit
    return dist, covered


def strong_edges(gray):
    """Strong-edge map of an original film frame: gradient magnitude on a
    lightly blurred grayscale; 'strong' = top band above a floor."""
    im = Image.fromarray(gray.astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(1.2))
    g = np.asarray(im).astype(np.float32)
    gx = np.zeros_like(g)
    gy = np.zeros_like(g)
    gx[:, 1:-1] = g[:, 2:] - g[:, :-2]
    gy[1:-1, :] = g[2:, :] - g[:-2, :]
    mag = np.hypot(gx, gy)
    thr = max(28.0, np.percentile(mag, 93.0))
    return mag >= thr, mag


def label_components(mask):
    """Two-pass union-find labeling over row runs. Returns (count, sizes)."""
    h, w = mask.shape
    parent = []

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    prev_runs = []  # (x0, x1, label)
    sizes = []
    for y in range(h):
        row = mask[y]
        runs = []
        x = 0
        while x < w:
            if row[x]:
                x0 = x
                while x < w and row[x]:
                    x += 1
                runs.append([x0, x - 1, -1])
            else:
                x += 1
        cur = []
        for r in runs:
            lab = None
            for pr in prev_runs:
                if r[0] <= pr[1] + 1 and pr[0] <= r[1] + 1:
                    if lab is None:
                        lab = pr[2]
                    else:
                        union(lab, pr[2])
            if lab is None:
                lab = len(parent)
                parent.append(lab)
                sizes.append(0)
            r[2] = lab
            sizes[lab] += r[1] - r[0] + 1
            cur.append(r)
        prev_runs = cur
    roots = {}
    total = []
    for i, s in enumerate(sizes):
        r = find(i)
        if r not in roots:
            roots[r] = 0
            total.append(roots[r])
        roots[r] += s
    vals = sorted(roots.values(), reverse=True)
    return len(vals), vals


def downscale_mask(mask, factor=2):
    h, w = mask.shape
    h2, w2 = h // factor, w // factor
    return mask[:h2 * factor, :w2 * factor].reshape(
        h2, factor, w2, factor).max(axis=(1, 3))


def validate_page(page_path, frame_path):
    repro = load_gray(page_path)
    size = (repro.shape[1], repro.shape[0])
    orig = load_gray(frame_path, size=size)

    repro_ink = repro < INK_LUM
    orig_ink = orig < ORIG_INK_LUM
    orig_black = orig < ORIG_BLACK_LUM

    # (a) edges
    e_orig, _ = strong_edges(orig)
    d_r, cov_r = clipped_distance(e_orig, repro_ink, CHAMFER_CLIP)
    coverage = float((d_r[e_orig] <= TAU).mean()) if e_orig.any() else 1.0
    chamfer_o = float(d_r[e_orig].mean()) if e_orig.any() else 0.0
    d_o, _ = clipped_distance(repro_ink, e_orig, CHAMFER_CLIP)
    chamfer_r = float(d_o[repro_ink].mean()) if repro_ink.any() else 0.0
    chamfer = 0.5 * (chamfer_o + chamfer_r)

    # (b) ink mass. The film's backgrounds are gray wash (median ~133), so
    # original ink is counted below the wash (ORIG_INK_LUM). The sharp
    # instrument for the known weak point is solid_density: inside the
    # original's near-black regions (eroded 3 px to stay inside figures),
    # how much of the repro is actually ink? Dense hatch reads ~0.4-0.5;
    # wash + sparse hatch — the softening QC-v4 recorded — reads far less.
    ink_o = float(orig_ink.mean())
    ink_r = float(repro_ink.mean())
    ink_log2 = abs(math.log2((ink_r + 1e-6) / (ink_o + 1e-6)))
    black_eroded = ~dilate(~orig_black, 3)
    if black_eroded.sum() > 200:
        solid_density = float(repro_ink[black_eroded].mean())
        wash_frac = float(((repro[black_eroded] >= INK_LUM) &
                           (repro[black_eroded] < WASH_HI)).mean())
    else:
        solid_density = 1.0
        wash_frac = 0.0
    deficit = 1.0 - solid_density
    # Uneroded ink-in-black: the eroded interior of a solid is pure wash in
    # this renderer (measured lum ~205, density ~0.00 on all 60 pages), so
    # the discriminating signal lives at the whole-region level: thin black
    # shapes collect contour ink inside them; big solid masses — the weak
    # class — collect almost none.
    if orig_black.sum() > 200:
        ink_in_black = float(repro_ink[orig_black].mean())
    else:
        ink_in_black = 1.0
    gh, gw = GRID[1], GRID[0]
    H, W = orig_ink.shape
    cell_diffs = []
    for i in range(gh):
        for j in range(gw):
            co = orig_ink[i * H // gh:(i + 1) * H // gh,
                          j * W // gw:(j + 1) * W // gw]
            cr = repro_ink[i * H // gh:(i + 1) * H // gh,
                           j * W // gw:(j + 1) * W // gw]
            cell_diffs.append(abs(float(cr.mean()) - float(co.mean())))
    cell_max = float(max(cell_diffs)) if cell_diffs else 0.0

    # (c) components. Total-count/share comparisons are poisoned by the
    # film itself: at the wash threshold the original's ink percolates
    # into a single component (measured largest-share 0.87-0.99 on clean
    # pages), so v1's share divergence read the film's grain, not the
    # repro. The sanity check therefore runs in the FIGURE BAND: the
    # original's near-black solids vs the repro's ink, half resolution,
    # components of at least FIG_MIN px only. A blobby page merges its
    # figures (repro figure count collapses); a shattered page fragments
    # (count explodes); both are caught against the original's figures.
    n_o, sizes_o = label_components(downscale_mask(orig_ink))
    n_r, sizes_r = label_components(downscale_mask(repro_ink))
    comp_log2 = abs(math.log2((n_r + 1) / (n_o + 1)))
    share_o = (sizes_o[0] / sum(sizes_o)) if sizes_o else 0.0
    share_r = (sizes_r[0] / sum(sizes_r)) if sizes_r else 0.0
    share_div = abs(share_r - share_o)
    _, fig_o_all = label_components(downscale_mask(orig_black))
    _, fig_r_all = label_components(downscale_mask(repro_ink))
    fig_o = [s for s in fig_o_all if s >= FIG_MIN]
    fig_r = [s for s in fig_r_all if s >= FIG_MIN]
    fig_log2 = math.log2((len(fig_o) + 1) / (len(fig_r) + 1))
    fshare_o = (fig_o[0] / sum(fig_o)) if fig_o else 0.0
    fshare_r = (fig_r[0] / sum(fig_r)) if fig_r else 0.0
    fshare_div = abs(fshare_r - fshare_o)

    # Verdict rules (v3, calibrated 2026-11-21 — see VALIDATOR-REPORT.md):
    # - edges: coverage / Chamfer against frozen bounds.
    # - ink: the log-ratio test applies only where the original actually
    #   demands ink (ink_o >= INK_DEMAND_MIN; on near-empty pages the
    #   ratio is noise); the demand test flags pages whose original is
    #   substantially solid black but whose repro answers with wash.
    # - components: only the extreme fragmentation bound gates. Two
    #   richer component formulations (total-ink shares; edge-component
    #   counts/shares) were tested against the calibration sets and
    #   REJECTED on evidence — their clean/weak ranges overlap, because
    #   on line art they read stroke connectivity (the renderer's
    #   texture), not figure merging. In this renderer the merged-figure
    #   ("blobby") failure is carried by the edges measure: merging
    #   destroys the original's contours, so coverage collapses. The
    #   surviving component gate catches the opposite failure — a solid
    #   shattered into stroke confetti (fig_log2 very negative).
    fails = []
    if coverage < EDGE_COV_MIN or chamfer > CHAMFER_MAX:
        fails.append("edges")
    if ((ink_o >= INK_DEMAND_MIN and ink_log2 > INK_LOG2_MAX) or
            (float(orig_black.mean()) >= BLACK_DEMAND_MIN and
             ink_in_black < INK_IN_BLACK_MIN)):
        fails.append("ink")
    if fig_log2 > FIG_MERGE_MAX or fig_log2 < -FIG_FRAG_MAX:
        fails.append("components")

    return {
        "edge_coverage": round(coverage, 4),
        "chamfer": round(chamfer, 3),
        "ink_orig": round(ink_o, 4),
        "ink_repro": round(ink_r, 4),
        "ink_log2": round(ink_log2, 3),
        "solid_deficit": round(deficit, 4),
        "solid_density": round(solid_density, 4),
        "ink_in_black": round(ink_in_black, 4),
        "wash_frac": round(wash_frac, 4),
        "fig_orig": len(fig_o),
        "fig_repro": len(fig_r),
        "fig_log2": round(fig_log2, 3),
        "fshare_div": round(fshare_div, 4),
        "black_frac_orig": round(float(orig_black.mean()), 4),
        "cell_max_diff": round(cell_max, 4),
        "comp_orig": n_o,
        "comp_repro": n_r,
        "comp_log2": round(comp_log2, 3),
        "share_orig": round(share_o, 4),
        "share_repro": round(share_r, 4),
        "share_div": round(share_div, 4),
        "fail_classes": fails,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate-dir", required=True)
    ap.add_argument("--out", default="validator-scores")
    ap.add_argument("--pages", default=None,
                    help="comma-separated page stems to run (default: all)")
    args = ap.parse_args()

    gate = args.gate_dir
    plan = json.load(open(os.path.join(gate, "plan.json")))
    titles_path = os.path.join(gate, "titles.json")
    if os.path.exists(titles_path):
        title_stems = set(json.load(open(titles_path)))
    else:
        # Gate 1 cards: shot 0 (main title + STEAMBOAT WILLIE card) and
        # shot 54 (THE END card), per ARC-SKETCH.md beats 1 and 9.
        title_stems = {"page00p0", "page54p0"}

    pages_dir = os.path.join(gate, "pages")
    frames_dir = os.path.join(gate, "shotframes2")
    results = []
    for shot, part, t in plan:
        stem = f"page{shot:02d}p{part}"
        if args.pages and stem not in args.pages.split(","):
            continue
        page_file = next(f for f in os.listdir(pages_dir)
                         if f.startswith(stem + "-"))
        frame_file = page_file.replace("page", "shot", 1)
        r = validate_page(os.path.join(pages_dir, page_file),
                          os.path.join(frames_dir, frame_file))
        r["page"] = stem
        r["t"] = round(float(t), 1)
        r["shot"] = shot
        if stem in title_stems:
            r["fail_classes"] = sorted(set(r["fail_classes"] + ["title"]))
        r["verdict"] = "FLAG" if r["fail_classes"] else "PASS"
        results.append(r)
        print(f"{stem} t={r['t']:6.1f} cov={r['edge_coverage']:.3f} "
              f"cham={r['chamfer']:5.2f} inkL={r['ink_log2']:.2f} "
              f"blk={r['black_frac_orig']:.3f} iib={r['ink_in_black']:.4f} "
              f"figL={r['fig_log2']:+.2f} fshD={r['fshare_div']:.2f} "
              f"-> {r['verdict']} {','.join(r['fail_classes'])}", flush=True)

    with open(args.out + ".json", "w") as f:
        json.dump({"thresholds": {
            "TAU": TAU, "CHAMFER_CLIP": CHAMFER_CLIP,
            "EDGE_COV_MIN": EDGE_COV_MIN, "CHAMFER_MAX": CHAMFER_MAX,
            "INK_LOG2_MAX": INK_LOG2_MAX,
            "BLACK_DEMAND_MIN": BLACK_DEMAND_MIN,
            "INK_DEMAND_MIN": INK_DEMAND_MIN,
            "INK_IN_BLACK_MIN": INK_IN_BLACK_MIN,
            "FIG_MIN": FIG_MIN, "FIG_MERGE_MAX": FIG_MERGE_MAX,
            "FIG_FRAG_MAX": FIG_FRAG_MAX,
        }, "pages": results}, f, indent=1)
    npass = sum(1 for r in results if r["verdict"] == "PASS")
    print(f"\n{len(results)} pages: {npass} PASS, "
          f"{len(results) - npass} FLAG")


if __name__ == "__main__":
    main()
