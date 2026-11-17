#!/usr/bin/env python3
"""
Task 3: render the tested decisions -- reads ONLY selector_results.json (written by verify_selector.py).

    python3 make_animation.py      writes selector_animation.svg (10 s loop) and selector_frames.svg (fallback, two frames)

Tolerance held at 1e-5. Frame A (0-5 s): the nine-mark limit, k = 9, 3,072 sides, area tolerance unmet ->
limit_reached. Frame B (5-10 s): the unrestricted word, k = 10, 6,144 sides, both tolerances met.
Two panels: Rebirth keeps the recorded frequency labels (synthesis undefined); Vortex 9 shows the certified ellipse
as a geometry prototype with the node and edge layers unset.
"""
import json
import math
import pathlib
from fractions import Fraction as F

HERE = pathlib.Path(__file__).resolve().parent
res = json.loads((HERE / "selector_results.json").read_text())
rows = {r["k"]: r for r in res["rows"]}
th = {t["eps"]: t for t in res["thresholds"]}

EPS = "1e-5"
A, B = rows[9], rows[10]
assert th[EPS]["nine_mark_interface"] == "limit_reached"
assert A["decisions"][EPS] == "rejected" and B["decisions"][EPS] == "certified"
assert th[EPS]["first_certified_n"] == B["n"] and th[EPS]["preceding_n"] == A["n"]
FREQS = [396, 417, 432, 528, 639, 741, 852, 963]          # recorded labels, kept as given

SCALE = 100                                              # pixels per unit, as in the display tolerance
PW, PH = 520, 900                                        # one panel


def polygon_path(n, cx, cy):
    """the circumscribed n-gon of the unit circle, mapped by diag(2, 3), at 100 px per unit (y up)"""
    r = 1 / math.cos(math.pi / n)
    pts = []
    for j in range(n):
        t = (2 * j + 1) * math.pi / n
        pts.append("%.3f %.3f" % (cx + SCALE * 2 * r * math.cos(t), cy - SCALE * 3 * r * math.sin(t)))
    return "M " + " L ".join(pts) + " Z"


def fmt(x):
    return "%.4g" % float(F(x))


def frame_texts(row, mode):
    n = row["n"]
    d = row["decisions"][EPS]
    if d == "rejected":
        status = "area tolerance unmet"
        extra = "nine-mark limit (k ≤ 9): limit_reached"
    else:
        status = "both tolerances met"
        extra = "unrestricted unary word: k = %d" % row["k"]
    return {
        "head": "%s sides · %s" % (format(n, ","), status),
        "sub": extra,
        "gap": "area gap 6g_n in [%s, %s], tolerance 1e-5" % (fmt(row["ellipse_gap_lower"]), fmt(row["ellipse_gap_upper"])),
        "disp": "outline error ≤ %s px (limit 0.25 px)" % fmt(row["display_bound_px"]),
        "word": "word 1^%d" % row["k"],
    }


def panel(x0, title, kind, row, color):
    cx, cy = x0 + PW / 2, 390
    t = frame_texts(row, kind)
    out = [f'<text x="{x0 + 24}" y="44" class="title">{title}</text>',
           f'<path d="{polygon_path(row["n"], cx, cy)}" fill="none" stroke="{color}" stroke-width="1.5"/>',
           f'<text x="{x0 + 24}" y="{PH - 118}" class="head" fill="{color}">{t["head"]}</text>',
           f'<text x="{x0 + 24}" y="{PH - 92}" class="sub">{t["sub"]} · {t["word"]}</text>',
           f'<text x="{x0 + 24}" y="{PH - 68}" class="sub">{t["gap"]}</text>',
           f'<text x="{x0 + 24}" y="{PH - 44}" class="sub">{t["disp"]}</text>']
    if kind == "rebirth":
        for i, f in enumerate(FREQS):
            ang = math.pi / 2 - 2 * math.pi * i / len(FREQS)
            c, s = math.cos(ang), math.sin(ang)
            anchor = "start" if c > 0.3 else "end" if c < -0.3 else "middle"
            lx = cx + (2 * SCALE * c + (10 if c > 0.3 else -10 if c < -0.3 else 0))
            ly = cy - (3 * SCALE * s + (16 if s > 0.3 else -26 if s < -0.3 else 0)) + 5
            out.append(f'<text x="{lx:.1f}" y="{ly:.1f}" class="freq" text-anchor="{anchor}">{f} Hz</text>')
        out.append(f'<text x="{cx}" y="{cy + 6}" class="note" text-anchor="middle">recorded labels only</text>')
        out.append(f'<text x="{cx}" y="{cy + 26}" class="note" text-anchor="middle">synthesis open: P_7, s, phases, amplitudes</text>')
    else:
        out.append(f'<text x="{cx}" y="{cy - 4}" class="note" text-anchor="middle">certified ellipse (geometry prototype)</text>')
        out.append(f'<text x="{cx}" y="{cy + 16}" class="note" text-anchor="middle">node layer: unset · edge layer: unset</text>')
    return "\n".join(out)


STYLE = """<style>
  .bg { fill: #f6f7f8; } .div { stroke: #d3d8de; }
  text { font-family: 'IBM Plex Sans', system-ui, sans-serif; fill: #1b2026; }
  .title { font-size: 22px; font-weight: 600; } .head { font-size: 19px; font-weight: 600; }
  .sub { font-size: 14px; fill: #5b6672; } .note { font-size: 13px; fill: #5b6672; }
  .freq { font-size: 14px; font-weight: 500; fill: #1b2026; } .banner { font-size: 15px; fill: #5b6672; }
</style>"""
RED, BLUE = "#b3261e", "#1f5f8b"


def frame(row, color, x_off=0, y_off=0):
    g = [f'<g transform="translate({x_off},{y_off})">',
         f'<rect class="bg" width="{2 * PW}" height="{PH}"/>',
         f'<line class="div" x1="{PW}" y1="20" x2="{PW}" y2="{PH - 20}"/>',
         panel(0, "Rebirth", "rebirth", row, color),
         panel(PW, "Vortex 9", "vortex", row, color),
         "</g>"]
    return "\n".join(g)


W, H = 2 * PW, PH + 40
banner = f'<text x="24" y="{PH + 26}" class="banner">area tolerance 1e-5 · ellipse diag(2,3) · 100 px per unit · decisions from selector_results.json</text>'
anim = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">', STYLE,
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
        '<g>', frame(A, RED),
        '<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.48;0.5;0.98;1" dur="10s" repeatCount="indefinite"/></g>',
        '<g opacity="0">', frame(B, BLUE),
        '<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.48;0.5;0.98;1" dur="10s" repeatCount="indefinite"/></g>',
        banner, "</svg>"]
(HERE / "selector_animation.svg").write_text("\n".join(anim) + "\n")

still = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {2 * PH + 60}" width="{W}" height="{2 * PH + 60}">', STYLE,
         f'<rect width="{W}" height="{2 * PH + 60}" fill="#ffffff"/>',
         frame(A, RED), frame(B, BLUE, 0, PH + 20),
         f'<text x="24" y="{2 * PH + 46}" class="banner">frame 1: nine-mark limit (limit_reached) · frame 2: unrestricted word · tolerance 1e-5 · from selector_results.json</text>',
         "</svg>"]
(HERE / "selector_frames.svg").write_text("\n".join(still) + "\n")
print("wrote selector_animation.svg and selector_frames.svg from rows k = 9 and k = 10")
