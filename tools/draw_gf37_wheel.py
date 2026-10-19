"""
The GF(37) wheel with real planet positions on it.

    python3 tools/draw_gf37_wheel.py records/real_chart_2026_03_03_nasa.json reference/gf37_wheel_march3_2026.png "March 3, 2026, 11:34 UT"

Decan k (the 10-degree arc from 10k to 10k+10 degrees of ecliptic longitude, k = 0..35) carries the number 2^k mod 37.
Turning by one decan is x2, by 120 degrees (12 decans) is x26 (the 137-map), by 180 degrees (18 decans) is x36 = -1.
The 12 orbits of the 137-map are the 12 triangles {k, k+12, k+24}. Longitude 0 is at the left, increasing
counterclockwise, as on an astrological wheel. Planet longitudes are NASA/JPL Horizons values from the JSON.
"""
import colorsys
import json
import math
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

P = 37
SEQ = [pow(2, k, P) for k in range(36)]
SIGNS = ["Ari", "Tau", "Gem", "Can", "Leo", "Vir", "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"]
ORBITS = {"IC": {1, 10, 26}, "NEG_H": {11, 27, 36}, "SA_ST_A": {9, 12, 16}, "C3": {3, 4, 30}, "D7": {7, 33, 34},
          "SEED": {18, 24, 32}, "TESLA": {6, 8, 23}, "CAS_EXT": {5, 13, 19}, "NQR17": {17, 22, 35},
          "DARK_A": {2, 15, 20}, "SA_ST_B": {21, 25, 28}, "C9": {14, 29, 31}}
NAMES = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Chiron",
         "Ceres", "Pallas", "Juno", "Vesta"]


def pt(r, lon):
    a = math.radians(180 + lon)
    return r * math.cos(a), r * math.sin(a)


def main(src, out, title):
    data = json.load(open(src))["bodies"]
    fig, ax = plt.subplots(figsize=(10, 10.2), dpi=140)
    ax.set_aspect("equal")
    ax.axis("off")
    R1, R2, R3 = 0.62, 0.86, 1.0
    colour = {k: colorsys.hsv_to_rgb((k % 12) / 12, 0.55, 0.95) for k in range(36)}
    line_colour = {c: colorsys.hsv_to_rgb(c / 12, 0.85, 0.65) for c in range(12)}
    for k in range(36):
        t = [10 * k + 10 * i / 20 for i in range(21)]
        outer = [pt(R2, x) for x in t]
        inner = [pt(R1, x) for x in reversed(t)]
        ax.fill([p[0] for p in outer + inner], [p[1] for p in outer + inner], color=colour[k], ec="white", lw=1.2)
        x, y = pt((R1 + R2) / 2, 10 * k + 5)
        ax.text(x, y, str(SEQ[k]), ha="center", va="center", fontsize=13, fontweight="bold", color="#222")
    for s in range(12):
        t = [30 * s + 30 * i / 30 for i in range(31)]
        ax.plot(*zip(*[pt(R3, x) for x in t]), color="#444", lw=1.0)
        ax.plot(*zip(*[pt(R2, x) for x in t]), color="#444", lw=1.0)
        ax.plot(*zip(*[pt(x_r, 30 * s) for x_r in (R2, R3)]), color="#444", lw=1.0)
        x, y = pt((R2 + R3) / 2, 30 * s + 15)
        ax.text(x, y, SIGNS[s], ha="center", va="center", fontsize=11, color="#333")
    for c in range(12):
        ks = [c, c + 12, c + 24]
        pts = [pt(R1 - 0.01, 10 * k + 5) for k in ks]
        pts.append(pts[0])
        ax.plot(*zip(*pts), color=line_colour[c], lw=1.4, alpha=0.9)
    # planets: a dot on the outer edge at the true longitude, label outside, labels spread so none overlap
    order = sorted(NAMES, key=lambda n: data[n]["ObsEcLon"])
    lons = [data[n]["ObsEcLon"] for n in order]
    gaps = [((lons[(i + 1) % len(lons)] - lons[i]) % 360) for i in range(len(lons))]
    first = (gaps.index(max(gaps)) + 1) % len(lons)
    order = order[first:] + order[:first]
    raw, off, last = [], 0, None
    for n in order:                                   # unwrapped longitudes, increasing around the circle
        lon = data[n]["ObsEcLon"]
        if last is not None and lon < last:
            off += 360
        raw.append(lon + off)
        last = lon
    ang = raw[:]
    for _ in range(400):                              # push neighbours apart until 7 degrees separate every label
        for i in range(len(ang) - 1):
            d = ang[i + 1] - ang[i]
            if d < 7.0:
                shift = (7.0 - d) / 2
                ang[i] -= shift * 0.5
                ang[i + 1] += shift * 0.5
    disp = {n: ang[i] % 360 for i, n in enumerate(order)}
    sun_x, sun_y = pt(R3, data["Sun"]["ObsEcLon"])
    moon_x, moon_y = pt(R3, data["Moon"]["ObsEcLon"])
    ax.plot([sun_x, moon_x], [sun_y, moon_y], color="#c00", lw=1.2, ls="--", zorder=3)
    for i, n in enumerate(order):
        lon = data[n]["ObsEcLon"]
        k = int(lon // 10)
        x0, y0 = pt(R3, lon)
        ax.plot([x0], [y0], "o", color="black", ms=5, zorder=5)
        rr = 1.13 if i % 2 == 0 else 1.25
        x1, y1 = pt(rr, disp[n])
        ax.plot([x0, x1], [y0, y1], color="#777", lw=0.8, zorder=4)
        ax.text(x1, y1, f"{n} {SEQ[k]}", ha="center", va="center", fontsize=10, zorder=6,
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="#888", lw=0.6))
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.45)
    ax.text(0, 1.42, f"{title}: real positions (NASA/JPL) on the GF(37) wheel", ha="center", fontsize=13)
    ax.text(0, -1.40, "decan k (10 degrees) = 2^k mod 37 | x2 = next decan | x26 = 120 degrees | x36 = 180 degrees | triangle = one orbit",
            ha="center", fontsize=9, color="#333")
    fig.savefig(out, bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
