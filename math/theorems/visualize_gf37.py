"""
GF(37) Visualizations

Three panels:
  1. Eisenstein integer lattice colored by norm mod 37
  2. Loeschian norm residue distribution (named classes highlighted)
  3. Random walk on GF(37) colored by orbit

Usage:
    python3 visualize_gf37.py              # saves gf37_plots.png
    python3 visualize_gf37.py show         # display interactively
"""

import sys
import random
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

sys.path.insert(0, __import__('os').path.dirname(__file__))
from gf37_classes import (
    P, IC, SOVEREIGN_SPIRAL, D7, SA_ORB, ORBIT_11, OUTLIER_ORB,
    DARK_A, NQR_5, TESLA_ORB, NQR_14, NQR_17, SEED_ORB,
    SA, ST, CB, QR37, NQR37, SEAM, TESLA_FLOW, SA_STEP,
    orbit_of, classify_residue
)


# ── Colours for each orbit ────────────────────────────────────────────────────

ORBIT_COLOR = {
    'IC':               '#00b4d8',
    'SOVEREIGN_SPIRAL': '#5865f2',
    'D7':               '#a8dadc',
    'SA_ORB':           '#48cae4',
    'ORBIT_11':         '#90e0ef',
    'OUTLIER_ORB':      '#caf0f8',
    'DARK_A':           '#f4845f',
    'NQR_5':            '#e63946',
    'TESLA_ORB':        '#f0c040',
    'NQR_14':           '#ff6b6b',
    'NQR_17':           '#c77dff',
    'SEED_ORB':         '#06d6a0',
    'SEAM':             '#333333',
    '?':                '#888888',
}

HIGHLIGHT = {0: 'SEAM', 11: 'ORBIT_11', 12: 'SA_ORB+ST', 18: 'SEED_ORB', 36: 'φ(37)'}
RED_RESIDUES = {0, 11, 12, 18, 36}


def residue_color(r):
    return ORBIT_COLOR.get(orbit_of(r), '#888888')


# ── Panel 1: Eisenstein lattice ───────────────────────────────────────────────

def plot_eisenstein(ax, lim=10):
    ax.set_facecolor('#08090f')
    cmap = plt.cm.hsv
    for u in range(-lim, lim + 1):
        for v in range(-lim, lim + 1):
            norm = u*u + u*v + v*v
            if norm == 0:
                continue
            r = norm % P
            color = cmap(r / P)
            # Eisenstein lattice: x = u + v*cos(60°), y = v*sin(60°)
            x = u + v * 0.5
            y = v * (math.sqrt(3) / 2)
            ax.plot(x, y, 'o', color=color, ms=4.5, alpha=0.85)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, P-1))
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label='n mod 37', shrink=0.8)
    ax.set_title('Eisenstein Integers: Norm mod 37', color='white', pad=8)
    ax.set_xlabel('u', color='#aaa'); ax.set_ylabel('v', color='#aaa')
    ax.tick_params(colors='#aaa'); ax.set_aspect('equal')
    for spine in ax.spines.values():
        spine.set_edgecolor('#1e2d40')


# ── Panel 2: Loeschian distribution ──────────────────────────────────────────

def loeschian_counts(lim=15):
    counts = [0] * P
    for a in range(-lim, lim + 1):
        for b in range(-lim, lim + 1):
            n = a*a + a*b + b*b
            if n > 0:
                counts[n % P] += 1
    return counts


def plot_distribution(ax, counts):
    ax.set_facecolor('#08090f')
    xs = list(range(P))
    colors = ['#e63946' if r in RED_RESIDUES else '#00b4d8' for r in xs]
    bars = ax.bar(xs, counts, color=colors, width=0.8, alpha=0.9)
    # Annotate highlighted bars
    for r, label in HIGHLIGHT.items():
        ax.annotate(label, xy=(r, counts[r]), xytext=(r, counts[r]+1.5),
                    fontsize=7, color='white', ha='center', rotation=70)
    ax.set_title('Loeschian Norm Residue Distribution', color='white', pad=8)
    ax.set_xlabel('Residue mod 37', color='#aaa')
    ax.set_ylabel('Count', color='#aaa')
    ax.tick_params(colors='#aaa')
    ax.set_facecolor('#08090f')
    for spine in ax.spines.values():
        spine.set_edgecolor('#1e2d40')
    # Mark min
    min_r = min(range(P), key=lambda r: counts[r])
    ax.annotate(f'min: r={min_r}\n({orbit_of(min_r)})',
                xy=(min_r, counts[min_r]), xytext=(min_r+3, counts[min_r]+4),
                fontsize=7, color='#f0c040',
                arrowprops=dict(arrowstyle='->', color='#f0c040', lw=0.8))


# ── Panel 3: Random walk ──────────────────────────────────────────────────────

def plot_random_walk(ax, steps=500, seed=246):
    random.seed(seed)
    pos = 0
    xs = [0]; ys = [pos]
    for _ in range(steps):
        pos = (pos + random.randint(1, P-1)) % P
        xs.append(len(xs)); ys.append(pos)

    ax.set_facecolor('#08090f')
    # Color each point by orbit
    colors = [residue_color(y) for y in ys]
    ax.plot(xs, ys, color='#1e3a5a', lw=0.6, alpha=0.5, zorder=1)
    sc = ax.scatter(xs, ys, c=colors, s=6, zorder=2, alpha=0.9)

    # Named class bands
    for r in sorted(SA):
        ax.axhline(r, color='#5865f2', lw=0.3, alpha=0.3)
    for r in sorted(ST):
        ax.axhline(r, color='#00b4d8', lw=0.3, alpha=0.2)

    ax.set_title(f'Random Walk on GF(37): {steps} Steps (seed=246)', color='white', pad=8)
    ax.set_xlabel('Step', color='#aaa')
    ax.set_ylabel('Position mod 37', color='#aaa')
    ax.set_ylim(-1, P)
    ax.tick_params(colors='#aaa')
    for spine in ax.spines.values():
        spine.set_edgecolor('#1e2d40')

    # Legend patches
    patches = [
        mpatches.Patch(color='#5865f2', label='SA members'),
        mpatches.Patch(color='#00b4d8', label='ST members'),
        mpatches.Patch(color='#06d6a0', label='SEED_ORB'),
        mpatches.Patch(color='#f0c040', label='TESLA_ORB'),
    ]
    ax.legend(handles=patches, fontsize=7, facecolor='#0e1320',
              edgecolor='#1e2d40', labelcolor='white', loc='upper right')


# ── Main ──────────────────────────────────────────────────────────────────────

def main(show=False):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.patch.set_facecolor('#08090f')
    plt.subplots_adjust(wspace=0.35)

    plot_eisenstein(axes[0])
    counts = loeschian_counts(lim=15)
    plot_distribution(axes[1], counts)
    plot_random_walk(axes[2])

    out = 'math/theorems/gf37_plots.png'
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='#08090f')
    print(f"Saved: {out}")
    print(f"Min Loeschian residue: {min(range(P), key=lambda r: counts[r])} "
          f"(count={min(counts[1:])})")
    print(f"Max Loeschian residue: {max(range(P), key=lambda r: counts[r])} "
          f"(count={max(counts)})")

    if show:
        matplotlib.use('TkAgg')
        plt.show()


if __name__ == "__main__":
    main(show='show' in sys.argv)
