#!/usr/bin/env python3
"""Read the owner's M/W drawing (owner_work/images/2026-10-06_8_mw_drawing.jpg, message #8) and print where each coloured path lands.

The owner's key to the colours (owner_work #313, 2026-10-17): "red, green, and blue stands for 1, 2, and 3, and then repeat."
(The green stroke is drawn in teal.) The picture has two rows of text, the owner's message #8: top  -0-00-0-00  and
bottom  00-0-00-0-0 . Zeros in each row are numbered from the left (top zeros 1..6, bottom zeros 1..7). Each path is a zigzag that
alternates between the rows; every vertex of every path sits on a zero.

    python3 tools/read_mw_drawing.py
Needs numpy and Pillow. The expected result is asserted at the end, so a change in the picture or the reading fails loudly.
"""
import pathlib

import numpy as np
from PIL import Image

IMG = pathlib.Path(__file__).resolve().parent.parent / "owner_work" / "images" / "2026-10-06_8_mw_drawing.jpg"
Y0, Y1, X0, X1 = 1150, 1245, 150, 345                   # the drawing in the 933 x 2000 screenshot
TOP_TXT, BOT_TXT = "-0-00-0-00", "00-0-00-0-0"
TOP_X = [165, 183, 201, 218, 240, 258, 276, 295, 311, 332]       # glyph centres measured on the clean top row
ADV = {"0": 21.5, "-": 14.5}                                      # advances measured from the top row


def bottom_centres():
    xs = [170.0]
    for a, b in zip(BOT_TXT, BOT_TXT[1:]):
        xs.append(xs[-1] + (ADV[a] if a == b else (ADV[a] + ADV[b]) / 2))
    return xs


def zero_numbers(text):
    n, out = 0, {}
    for i, ch in enumerate(text):
        if ch == "0":
            n += 1
            out[i] = n
    return out


def main():
    c = np.array(Image.open(IMG).convert("RGB")).astype(int)[Y0:Y1, X0:X1]
    R, G, B = c[..., 0], c[..., 1], c[..., 2]
    paths = {"red (1)": (R > 190) & (G < 100) & (B < 100),
             "green (2)": (R < 140) & (G > 180) & (B > 150) & (B < 240) & (abs(G - B) < 60),
             "blue (3)": (R < 90) & (G < 110) & (B > 190)}
    glyphs = {"top": (TOP_X, zero_numbers(TOP_TXT)), "bottom": (bottom_centres(), zero_numbers(BOT_TXT))}
    result = {}
    for name, m in paths.items():
        xs = np.where(m.any(0))[0]
        cy = np.array([np.where(m[:, x])[0].mean() for x in xs]) + Y0
        sm = np.convolve(cy, np.ones(5) / 5, mode="same")
        pts = [(xs[0] + X0, cy[0])]
        for i in range(4, len(sm) - 4):
            w = sm[max(0, i - 8):i + 9]
            if (sm[i] == w.min() and sm[i] < sm[i - 4] - 1 and sm[i] < sm[i + 4] - 1) or (sm[i] == w.max() and sm[i] > sm[i - 4] + 1 and sm[i] > sm[i + 4] + 1):
                pts.append((xs[i] + X0, sm[i]))
        pts.append((xs[-1] + X0, cy[-1]))
        out = []
        for x, y in pts:
            row = "top" if y < 1200 else "bottom"
            centres, zeros = glyphs[row]
            j = min(range(len(centres)), key=lambda t: abs(centres[t] - x))
            out.append((row, zeros[j]))                  # KeyError would mean the vertex is not on a zero
        result[name] = out
        print(name, out)
    return result


if __name__ == "__main__":
    got = main()
    assert got["red (1)"] == [("bottom", 1), ("top", 1), ("bottom", 3), ("top", 4), ("bottom", 6)]
    assert got["green (2)"] == [("bottom", 2), ("top", 2), ("bottom", 4), ("top", 5)]
    assert got["blue (3)"] == [("top", 3), ("bottom", 5), ("top", 6)]
    print("every vertex is on a zero; green = red moved 1 zero right, blue = red moved 2 zeros right")
