#!/usr/bin/env python3
"""The panel proposed in section 7 of the owner's handoff
(reference/phi3_phi12_at_137_handoff_2026_09_12.md, owner_work message #241):

    "One bar set: {13, 2473, 10957} for Phi_12(137) = 352256593.
     One marked cut prime on S: 13.
     Alongside the existing Phi_3 panel, whose cut is empty.
     This is a display of section 2.3. It should carry the scope note from section 3.1."

The Phi_3 panel it refers to is not in this repo (searched 2026-10-13), so both panels are drawn
here from the handoff's section 2 data, side by side. Bar height = log10 of each prime factor.

    python3 reference/phi12_panel.py      -> reference/phi12_panel.png
"""
import math
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sympy import factorint, gcd, primefactors

A, S = 137, 113115117167
PHI3, PHI12 = A * A + A + 1, A ** 4 - A ** 2 + 1
CUT3 = sorted(set(primefactors(PHI3)) & set(primefactors(S)))
CUT12 = sorted(set(primefactors(PHI12)) & set(primefactors(S)))
assert (PHI3, PHI12) == (18907, 352256593)
assert CUT3 == [] and CUT12 == [13] and gcd(S, PHI3) == 1 and gcd(S, PHI12) == 13

OUT = pathlib.Path(__file__).resolve().parent / "phi12_panel.png"


def draw(ax, value, name, cut):
    ps = sorted(factorint(value))
    colors = ["#c0392b" if p in cut else "#5d6d7e" for p in ps]
    bars = ax.bar([str(p) for p in ps], [math.log10(p) for p in ps], color=colors, width=0.55)
    for b, p in zip(bars, ps):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.08, f"{p}" + ("\non S" if p in cut else ""),
                ha="center", va="bottom", fontsize=10, color=b.get_facecolor())
    ax.set_title(f"{name}(137) = {value}\n= " + " · ".join(map(str, ps)), fontsize=11)
    ax.set_ylabel("log10(p)")
    ax.set_ylim(0, 5.2)
    ax.text(0.5, -0.2, f"TapeCut = {{{', '.join(map(str, cut))}}}" if cut else "TapeCut = { }   (gcd(S, Φ₃(137)) = 1)",
            transform=ax.transAxes, ha="center", fontsize=10)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


fig, (left, right) = plt.subplots(1, 2, figsize=(11, 5.2))
draw(left, PHI3, "Φ₃", CUT3)
draw(right, PHI12, "Φ₁₂", CUT12)
fig.suptitle("Prime divisors of Φₙ(137) against the tape S = 113115117167 = 13 · 8701162859", fontsize=12)
fig.text(0.5, 0.015, "Scope (handoff §3.1): S has only two prime divisors, so '13 is the only prime on both the Φ₁₂ "
         "family and the tape' is drawn from a 2-element set — true as stated, thin as evidence.",
         ha="center", fontsize=8.5, style="italic", wrap=True)
fig.tight_layout(rect=(0, 0.06, 1, 0.94))
fig.savefig(OUT, dpi=130)

if __name__ == "__main__":
    print(f"wrote {OUT.name}: Φ₃ cut {CUT3}, Φ₁₂ cut {CUT12}")
