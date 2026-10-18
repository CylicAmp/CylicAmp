#!/usr/bin/env python3
"""The owner's seven rows 123 / 312 / 231 / 123 / 312 / 231 / 123 (labels 1, 2, 3 on the three 123s), one colour per row.

The owner's key: red, green, blue stand for 1, 2, 3 and then repeat (owner_work 2026-10-17). So the rows labelled 1, 2, 3 (rows 1, 4, 7)
are red, green, blue. The four rows in between get the colours between them: rows 2 and 3 are at 60 and 120 degrees on the opponent ring (red, yellow, green, blue), rows 5 and 6 at 210 and 240 degrees. That makes seven colours. Beside each row: its number, its label, and its value mod 37 (each row is the last
digit moved to the front, which is times 26: 12, 16, 9, 12, 16, 9, 12).

    python3 tools/draw_123_rows.py     ->  reference/rotation_rows_123_seven_colours.png
"""
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROWS = ["123", "312", "231", "123", "312", "231", "123"]
LABEL = {0: "= 1", 3: "= 2", 6: "= 3"}
RED, YELLOW, GREEN, BLUE = (0.89, 0.12, 0.12), (0.95, 0.80, 0.08), (0.10, 0.70, 0.20), (0.12, 0.28, 0.95)


def blend(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


# Opponent ring (red-green and blue-yellow poles): red 0, yellow 90, green 180, blue 270 degrees. Rows 1, 4, 7 (labels 1, 2, 3) are red, green, blue.
# Rows 2 and 3 sit at 60 and 120 degrees (orange-yellow, yellow-green: the way from red to green goes through yellow); rows 5 and 6 at 210 and 240 degrees (teal, azure).
RING = [(0, RED), (90, YELLOW), (180, GREEN), (270, BLUE)]


def at(angle):
    for (a0, c0), (a1, c1) in zip(RING, RING[1:]):
        if a0 <= angle <= a1:
            return blend(c0, c1, (angle - a0) / (a1 - a0))


COLOURS = [at(a) for a in (0, 60, 120, 180, 210, 240, 270)]
NAMES = ["red", "orange-yellow", "yellow-green", "green", "teal", "azure", "blue"]
OUT = pathlib.Path(__file__).resolve().parent.parent / "reference" / "rotation_rows_123_seven_colours.png"

same = lambda a, b: all(abs(x - y) < 1e-9 for x, y in zip(a, b))
assert len(ROWS) == len(COLOURS) == 7 and same(COLOURS[0], RED) and same(COLOURS[3], GREEN) and same(COLOURS[6], BLUE)
assert [int(r) % 37 for r in ROWS] == [12, 16, 9, 12, 16, 9, 12]
assert all(int(a[-1] + a[:-1]) == int(b) for a, b in zip(ROWS, ROWS[1:3]))

fig, ax = plt.subplots(figsize=(6.2, 7.4))
for i, (row, col) in enumerate(zip(ROWS, COLOURS)):
    y = 6 - i
    ax.add_patch(plt.Rectangle((0, y), 3.6, 0.86, color=col))
    ax.text(0.25, y + 0.43, row, va="center", ha="left", fontsize=30, color="white", fontweight="bold", family="monospace")
    ax.text(1.95, y + 0.43, LABEL.get(i, ""), va="center", ha="left", fontsize=26, color="white", fontweight="bold", family="monospace")
    ax.text(3.8, y + 0.43, f"{int(row) % 37}  (mod 37)", va="center", ha="left", fontsize=13, color="#333333")
    ax.text(-0.15, y + 0.43, str(i + 1), va="center", ha="right", fontsize=13, color="#333333")
ax.set_xlim(-0.6, 6.4)
ax.set_ylim(-0.2, 7.4)
ax.axis("off")
ax.set_title("123 turned seven times, one colour per row\nred = 1, green = 2, blue = 3 (rows 1, 4, 7); in between: on the red-yellow-green-blue ring",
             fontsize=11, loc="left")
fig.savefig(OUT, dpi=140, bbox_inches="tight", facecolor="white")
print(f"wrote {OUT.name}: " + ", ".join(f"{r} {n}" for r, n in zip(ROWS, NAMES)))
