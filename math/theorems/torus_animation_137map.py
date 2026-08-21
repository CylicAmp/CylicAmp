# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 252: Torus Animation of the 137-Map Phase Engine
================================================================================

The three sovereign orbits under f(n) = 26n mod 37 embed naturally on a torus
T² = S¹ × S¹.

EMBEDDING:
  Outer angle θ  =  2π · n / 37   (position in Z_37)
  Inner angle φ  =  2π · k / 3    (phase step k = 0, 1, 2 within the orbit)

  Torus coordinates (R=major radius, r=minor radius):
    x = (R + r·cos(φ)) · cos(θ)
    y = (R + r·cos(φ)) · sin(θ)
    z =  r · sin(φ)

THREE ORBITS:
  Tier 1 / SEED_ORBIT = {18, 24, 32}   (orbit of seed 246)
  Tier 2 / C3         = {3,  4,  30}   (fully sovereign coset)
  Tier 3 / H          = {1,  26, 10}   (sovereign kernel)

PHASE-STEP ARROW:
  Each application of ×26 mod 37 advances k by 1 (φ by 2π/3) and
  moves n to 26n mod 37.  The arrow on the torus surface shows this
  as a helical step: outer angle shifts by 2π·(26-1)/37 per step
  while the inner angle advances by 2π/3.

MATHEMATICAL ASSERTIONS VERIFIED:
  1. All three orbits have order 3 under f(n) = 26n mod 37.
  2. Elements embed to distinct (θ, φ) pairs — no collisions on T².
  3. Orbit products:
       prod(SEED) mod 37 = 18·24·32 mod 37 = 23  (prime)
       prod(C3)   mod 37 = 3·4·30   mod 37 = 27  (= 3³)
       prod(H)    mod 37 = 1·26·10  mod 37 = 1   ∈ H  (identity)
  4. No overlap between the three orbits.
  5. Union covers 9 of 36 elements of GF(37)*.

ANIMATION:
  Frames rotate the viewing azimuth 0° → 360°.  Each orbit arc is drawn
  as a closed 3-point loop on the torus surface; phase arrows show the
  ×26 direction.  The torus shell is rendered semi-transparent.
================================================================================
"""

import sys
import os
import math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

P = 37
H_SET     = {1, 10, 26}
SA        = {4, 9, 25, 30}
ST        = {3, 12, 21, 30}
SEED_ORBIT = {18, 24, 32}
C3        = {3, 4, 30}

ORBITS = [
    ("SEED", [18, 24, 32], "#e05c2a"),   # amber-red
    ("C3",   [3,  4,  30], "#2a8ae0"),   # blue
    ("H",    [1,  26, 10], "#2ae07a"),   # green
]

R = 3.0   # major radius
r = 1.0   # minor radius


def torus_xyz(n, k):
    """Map GF(37) element n at phase step k to 3D torus coordinates."""
    theta = 2 * math.pi * n / P
    phi   = 2 * math.pi * k / 3
    x = (R + r * math.cos(phi)) * math.cos(theta)
    y = (R + r * math.cos(phi)) * math.sin(theta)
    z =  r * math.sin(phi)
    return x, y, z


def torus_surface():
    u = np.linspace(0, 2 * np.pi, 80)
    v = np.linspace(0, 2 * np.pi, 40)
    U, V = np.meshgrid(u, v)
    X = (R + r * np.cos(V)) * np.cos(U)
    Y = (R + r * np.cos(V)) * np.sin(U)
    Z =  r * np.sin(V)
    return X, Y, Z


def verify():
    print("THEOREM 252: TORUS ANIMATION OF THE 137-MAP PHASE ENGINE")
    print("=" * 60)

    all_elements = []
    for label, orbit, _ in ORBITS:
        # 1. Order-3 check
        for start in orbit:
            v = start
            for _ in range(3):
                v = v * 26 % P
            assert v == start, f"orbit({start}) not closed"

        # 2. Distinct torus positions
        pts = [torus_xyz(n, k) for k, n in enumerate(orbit)]
        assert len(set(pts)) == 3

        # 3. Orbit products
        prod = 1
        for n in orbit:
            prod = prod * n % P
        print(f"  prod({label}) mod37 = {prod}  SA:{prod in SA}  H:{prod in H_SET}")

        all_elements.extend(orbit)

    # 4. No overlaps
    assert len(set(all_elements)) == 9

    # 5. Union size
    assert len(set(all_elements)) == 9
    print(f"  Union covers {len(set(all_elements))} of {P-1} elements of GF({P})*")

    # Extra: ord_37(26) = 3
    assert pow(26, 3, P) == 1
    print(f"  ord_37(26) = 3  check")

    print("  All assertions passed.")


def build_animation(n_frames=72, out_path=None):
    if out_path is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_path = os.path.join(here, "torus_animation_137map.gif")

    X, Y, Z = torus_surface()

    fig = plt.figure(figsize=(8, 6), facecolor='#0d0d0d')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#0d0d0d')
    ax.set_axis_off()

    def draw_frame(frame):
        ax.cla()
        ax.set_facecolor('#0d0d0d')
        ax.set_axis_off()

        azim = frame * 360 / n_frames
        ax.view_init(elev=25, azim=azim)

        # torus shell
        ax.plot_surface(X, Y, Z, alpha=0.10, color='#555577',
                        rstride=2, cstride=2, linewidth=0)

        # orbit arcs
        for label, orbit, color in ORBITS:
            pts = [torus_xyz(n, k) for k, n in enumerate(orbit)]
            pts.append(pts[0])   # close the loop
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            zs = [p[2] for p in pts]
            ax.plot(xs, ys, zs, color=color, linewidth=2.2, alpha=0.95)
            # nodes
            ax.scatter(xs[:-1], ys[:-1], zs[:-1], color=color,
                       s=50, zorder=5, depthshade=False)
            # phase arrows (step 0 → 1)
            x0, y0, z0 = pts[0]
            x1, y1, z1 = pts[1]
            ax.quiver(x0, y0, z0,
                      x1-x0, y1-y0, z1-z0,
                      length=0.6, normalize=True,
                      color=color, alpha=0.75, arrow_length_ratio=0.4)
            # label at first node
            ax.text(xs[0]*1.08, ys[0]*1.08, zs[0]+0.12,
                    f"{label}\n{orbit[0]}", color=color,
                    fontsize=7, ha='center')

        ax.set_title("T252 — 137-Map Orbits on T²\n"
                     "SEED {18,24,32}  ·  C3 {3,4,30}  ·  H {1,26,10}",
                     color='#cccccc', fontsize=9, pad=4)

        lim = R + r + 0.5
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_zlim(-r - 0.3, r + 0.3)

    ani = animation.FuncAnimation(fig, draw_frame, frames=n_frames,
                                  interval=50, blit=False)

    writer = animation.PillowWriter(fps=20)
    ani.save(out_path, writer=writer)
    plt.close(fig)
    print(f"  Animation saved → {out_path}")
    return out_path


def run():
    verify()
    print()
    build_animation()


if __name__ == "__main__":
    run()
