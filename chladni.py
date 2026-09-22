"""
chladni.py

Virtual Chladni figure simulator.

Physics: 2D wave equation on a square plate with fixed edges.
Eigenfunctions: u(x,y) = sin(mπx/L) * sin(nπy/L)
Nodal lines: where u(x,y) = 0 — where sand accumulates.
Frequency: f(m,n) ∝ sqrt(m² + n²)

DR extension: each (m,n) mode maps to a digital root class.
Improvements over basic demos:
  - Superposition of multiple modes simultaneously
  - DR coloring of nodal regions
  - Frequency sweep animation
  - Export mode shapes to PNG
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button, CheckButtons
import argparse
import os


# ---------------------------------------------------------------------------
# Core math
# ---------------------------------------------------------------------------

def digital_root(n: int) -> int:
    if n <= 0:
        return 9
    return (n - 1) % 9 + 1


def eigenfunction(m: int, n: int, X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """u(x,y) = sin(mπx) * sin(nπy) on unit square [0,1]²."""
    return np.sin(m * np.pi * X) * np.sin(n * np.pi * Y)


def frequency(m: int, n: int) -> float:
    """Relative frequency: f ∝ sqrt(m²+n²)."""
    return np.sqrt(m**2 + n**2)


def nodal_mask(u: np.ndarray, threshold: float = 0.05) -> np.ndarray:
    """Return mask where |u| < threshold — the nodal lines."""
    return np.abs(u) < threshold


def superpose(modes: list, X: np.ndarray, Y: np.ndarray,
              t: float = 0.0) -> np.ndarray:
    """
    Sum multiple modes with time evolution.
    modes: list of (m, n, amplitude, phase) tuples
    """
    u = np.zeros_like(X)
    for m, n, amp, phase in modes:
        f = frequency(m, n)
        u += amp * eigenfunction(m, n, X, Y) * np.cos(2 * np.pi * f * t + phase)
    return u


def mode_dr(m: int, n: int) -> int:
    """Digital root of the mode number m²+n² (frequency² proxy)."""
    return digital_root(m * m + n * n)


# ---------------------------------------------------------------------------
# DR color map for nodal regions
# ---------------------------------------------------------------------------

DR_COLORS = {
    1: "#e74c3c",   # LL-O  red
    2: "#e67e22",   # LL-E  orange
    3: "#f1c40f",   # LH-O  yellow
    4: "#2ecc71",   # LH-E  green
    5: "#1abc9c",   # A51   teal
    6: "#3498db",   # RL-E  blue
    7: "#9b59b6",   # RL-O  purple
    8: "#e91e63",   # RH-E  pink
    9: "#95a5a6",   # RH-O  gray
}

GRID_LABELS = {
    1: "LL-O", 2: "LL-E", 3: "LH-O", 4: "LH-E", 5: "A51",
    6: "RL-E", 7: "RL-O", 8: "RH-E", 9: "RH-O",
}


# ---------------------------------------------------------------------------
# Static single-mode plot
# ---------------------------------------------------------------------------

def plot_mode(m: int, n: int, resolution: int = 400,
              threshold: float = 0.05, save: str = None):
    """Plot a single Chladni mode (m,n)."""
    x = np.linspace(0, 1, resolution)
    y = np.linspace(0, 1, resolution)
    X, Y = np.meshgrid(x, y)
    u = eigenfunction(m, n, X, Y)
    nodal = nodal_mask(u, threshold)

    dr = mode_dr(m, n)
    color = DR_COLORS[dr]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor("#0a0a0a")

    # Left: displacement field
    ax1 = axes[0]
    ax1.set_facecolor("#0a0a0a")
    im = ax1.imshow(u, cmap="RdBu", origin="lower", extent=[0, 1, 0, 1],
                    vmin=-1, vmax=1)
    ax1.contour(X, Y, u, levels=[0], colors=[color], linewidths=1.5)
    ax1.set_title(f"Displacement field  m={m}, n={n}", color="white")
    ax1.set_xlabel("x", color="white"); ax1.set_ylabel("y", color="white")
    ax1.tick_params(colors="white")
    plt.colorbar(im, ax=ax1)

    # Right: Chladni figure (nodal lines = where sand collects)
    ax2 = axes[1]
    ax2.set_facecolor("#0a0a0a")
    sand = np.where(nodal, 1.0, 0.0)
    ax2.imshow(sand, cmap="hot", origin="lower", extent=[0, 1, 0, 1],
               vmin=0, vmax=1)
    ax2.set_title(
        f"Chladni figure  f∝{frequency(m,n):.3f}\n"
        f"DR(m²+n²)={dr}  →  {GRID_LABELS[dr]}",
        color=color
    )
    ax2.set_xlabel("x", color="white"); ax2.set_ylabel("y", color="white")
    ax2.tick_params(colors="white")

    for ax in axes:
        for spine in ax.spines.values():
            spine.set_edgecolor("#333")

    plt.tight_layout()

    if save:
        plt.savefig(save, dpi=150, facecolor=fig.get_facecolor())
        print(f"Saved: {save}")
    else:
        plt.show()
    plt.close()


# ---------------------------------------------------------------------------
# Interactive multi-mode explorer
# ---------------------------------------------------------------------------

def interactive_explorer(resolution: int = 300):
    """
    Interactive Chladni figure explorer.
    - Sliders for m, n, threshold, time
    - Checkbox for superposition mode
    - DR label updates live
    """
    x = np.linspace(0, 1, resolution)
    y = np.linspace(0, 1, resolution)
    X, Y = np.meshgrid(x, y)

    fig = plt.figure(figsize=(14, 8), facecolor="#0a0a0a")
    fig.suptitle("Virtual Chladni Figure Explorer", color="white", fontsize=14)

    ax_main = fig.add_axes([0.05, 0.25, 0.55, 0.65])
    ax_disp = fig.add_axes([0.62, 0.25, 0.35, 0.65])

    ax_main.set_facecolor("#0a0a0a")
    ax_disp.set_facecolor("#0a0a0a")

    # Sliders
    ax_m    = fig.add_axes([0.1, 0.15, 0.35, 0.03])
    ax_n    = fig.add_axes([0.1, 0.10, 0.35, 0.03])
    ax_thr  = fig.add_axes([0.1, 0.05, 0.35, 0.03])
    ax_m2   = fig.add_axes([0.55, 0.15, 0.35, 0.03])
    ax_n2   = fig.add_axes([0.55, 0.10, 0.35, 0.03])

    sl_m   = Slider(ax_m,   "m₁", 1, 12, valinit=3, valstep=1, color="#3498db")
    sl_n   = Slider(ax_n,   "n₁", 1, 12, valinit=2, valstep=1, color="#3498db")
    sl_thr = Slider(ax_thr, "threshold", 0.01, 0.2, valinit=0.05, color="#2ecc71")
    sl_m2  = Slider(ax_m2,  "m₂", 1, 12, valinit=2, valstep=1, color="#e74c3c")
    sl_n2  = Slider(ax_n2,  "n₂", 1, 12, valinit=3, valstep=1, color="#e74c3c")

    # Label
    info_ax = fig.add_axes([0.62, 0.05, 0.35, 0.15])
    info_ax.set_facecolor("#111")
    info_ax.axis("off")
    info_text = info_ax.text(0.05, 0.5, "", color="white", fontsize=10,
                              va="center", family="monospace")

    img_main = [None]
    img_disp = [None]

    def compute_and_draw(_=None):
        m1 = int(sl_m.val);  n1 = int(sl_n.val)
        m2 = int(sl_m2.val); n2 = int(sl_n2.val)
        thr = sl_thr.val

        u1 = eigenfunction(m1, n1, X, Y)
        u2 = eigenfunction(m2, n2, X, Y)
        u_super = (u1 + u2) / 2

        nodal1  = nodal_mask(u1, thr)
        nodal_s = nodal_mask(u_super, thr)

        dr1 = mode_dr(m1, n1)
        dr2 = mode_dr(m2, n2)
        dr_s = digital_root(m1*m1 + n1*n1 + m2*m2 + n2*n2)

        c1 = DR_COLORS[dr1]
        cs = DR_COLORS[dr_s]

        ax_main.clear(); ax_disp.clear()
        ax_main.set_facecolor("#0a0a0a"); ax_disp.set_facecolor("#0a0a0a")

        # Main: single mode nodal
        sand1 = np.where(nodal1, 1.0, 0.0)
        ax_main.imshow(sand1, cmap="hot", origin="lower", extent=[0,1,0,1])
        ax_main.set_title(
            f"Mode ({m1},{n1})  f∝{frequency(m1,n1):.3f}\n"
            f"DR={dr1}  {GRID_LABELS[dr1]}",
            color=c1, fontsize=11
        )
        ax_main.tick_params(colors="white")

        # Disp: superposition nodal
        sand_s = np.where(nodal_s, 1.0, 0.0)
        ax_disp.imshow(sand_s, cmap="hot", origin="lower", extent=[0,1,0,1])
        ax_disp.set_title(
            f"Superposition ({m1},{n1})+({m2},{n2})\n"
            f"DR={dr_s}  {GRID_LABELS[dr_s]}",
            color=cs, fontsize=11
        )
        ax_disp.tick_params(colors="white")

        info_text.set_text(
            f"Mode 1:  m={m1} n={n1}  f∝{frequency(m1,n1):.3f}\n"
            f"  DR(m²+n²={m1**2+n1**2}) = {dr1}  [{GRID_LABELS[dr1]}]\n\n"
            f"Mode 2:  m={m2} n={n2}  f∝{frequency(m2,n2):.3f}\n"
            f"  DR(m²+n²={m2**2+n2**2}) = {dr2}  [{GRID_LABELS[dr2]}]\n\n"
            f"Super:  DR({m1**2+n1**2}+{m2**2+n2**2}={m1**2+n1**2+m2**2+n2**2})"
            f" = {dr_s}  [{GRID_LABELS[dr_s]}]"
        )
        fig.canvas.draw_idle()

    sl_m.on_changed(compute_and_draw)
    sl_n.on_changed(compute_and_draw)
    sl_thr.on_changed(compute_and_draw)
    sl_m2.on_changed(compute_and_draw)
    sl_n2.on_changed(compute_and_draw)

    compute_and_draw()
    plt.show()


# ---------------------------------------------------------------------------
# DR mode map: all (m,n) up to max_mode, colored by DR class
# ---------------------------------------------------------------------------

def dr_mode_map(max_mode: int = 8, resolution: int = 150,
                threshold: float = 0.05, save: str = None):
    """Grid of all Chladni figures up to (max_mode, max_mode), DR-colored."""
    x = np.linspace(0, 1, resolution)
    y = np.linspace(0, 1, resolution)
    X, Y = np.meshgrid(x, y)

    fig, axes = plt.subplots(max_mode, max_mode,
                              figsize=(2 * max_mode, 2 * max_mode))
    fig.patch.set_facecolor("#0a0a0a")
    fig.suptitle("Chladni Mode Map — DR-colored", color="white", fontsize=14)

    for i, m in enumerate(range(1, max_mode + 1)):
        for j, n in enumerate(range(1, max_mode + 1)):
            ax = axes[i][j]
            ax.set_facecolor("#0a0a0a")
            u = eigenfunction(m, n, X, Y)
            nodal = nodal_mask(u, threshold)
            sand = np.where(nodal, 1.0, 0.0)
            dr = mode_dr(m, n)
            color = DR_COLORS[dr]
            ax.imshow(sand, cmap="hot", origin="lower", extent=[0,1,0,1])
            ax.set_title(f"({m},{n}) DR={dr}", color=color, fontsize=6, pad=2)
            ax.axis("off")

    plt.tight_layout()
    if save:
        plt.savefig(save, dpi=120, facecolor=fig.get_facecolor())
        print(f"Saved: {save}")
    else:
        plt.show()
    plt.close()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Virtual Chladni Simulator")
    sub = parser.add_subparsers(dest="cmd")

    p_single = sub.add_parser("mode", help="Plot single mode")
    p_single.add_argument("m", type=int)
    p_single.add_argument("n", type=int)
    p_single.add_argument("--save", default=None)
    p_single.add_argument("--threshold", type=float, default=0.05)

    p_map = sub.add_parser("map", help="DR mode map grid")
    p_map.add_argument("--max", type=int, default=8)
    p_map.add_argument("--save", default=None)

    p_live = sub.add_parser("explore", help="Interactive explorer")

    args = parser.parse_args()

    if args.cmd == "mode":
        plot_mode(args.m, args.n, threshold=args.threshold, save=args.save)
    elif args.cmd == "map":
        dr_mode_map(max_mode=args.max, save=args.save)
    elif args.cmd == "explore":
        interactive_explorer()
    else:
        # Default: show mode map
        print("Usage:")
        print("  python chladni.py mode 3 2          # single mode")
        print("  python chladni.py map --max 8       # DR mode map grid")
        print("  python chladni.py explore           # interactive")
        print()
        print("DR classification of modes up to (6,6):")
        print(f"  {'(m,n)':>8}  {'m²+n²':>6}  {'DR':>4}  {'grid':>6}  {'f∝':>8}")
        print(f"  {'-'*40}")
        for m in range(1, 7):
            for n in range(1, 7):
                f = frequency(m, n)
                s = m*m + n*n
                dr = mode_dr(m, n)
                print(f"  ({m},{n}){' ':>4}  {s:>6}  {dr:>4}  {GRID_LABELS[dr]:>6}  {f:>8.4f}")
