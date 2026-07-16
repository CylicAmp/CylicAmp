"""
Kinematic Focal Zoom — Multiplicative Orbit on Z/333Z

Residue 167 satisfies 2^35 ≡ 167 (mod 333). 167 is prime.

Orbit: k → 2^k mod 333, k = 0..35  (36 points on circle of radius 25)
Camera pans from origin to target T ≈ (-24.999, -0.236) while zooming in.

Viewport kinematics (t ∈ [0,1]):
  s(t) = 1.35 - 0.8t              (scale, linear decay)
  p(t) = 3t² - 2t³               (cubic smoothstep, progress)
  C(t) = (1-p(t))·C₀ + p(t)·T   (camera center path)
  H(t) = s(t)·28                  (viewport half-width, equal aspect)

Output: kinematic_focus_residue167.mp4
        72 frames @ 24 fps | dark theme
"""

import math
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter


# ── Constants ────────────────────────────────────────────────────────────────

MOD      = 333
K_MAX    = 35          # 2^35 ≡ 167 (mod 333)
RADIUS   = 25.0        # circle radius for residue positions
N_FRAMES = 72
FPS      = 24
H0       = 28.0        # initial viewport half-width

# Verified
assert pow(2, K_MAX, MOD) == 167
assert all(pow(167, 1, p) != 0 for p in [2, 3, 5, 7, 11, 13])  # basic primality hint


# ── Orbit ────────────────────────────────────────────────────────────────────

def build_orbit():
    """36 points: k=0..35, residue = 2^k mod 333, mapped to circle of radius 25."""
    pts = []
    for k in range(K_MAX + 1):
        r = pow(2, k, MOD)
        theta = 2 * math.pi * r / MOD
        pts.append((RADIUS * math.cos(theta), RADIUS * math.sin(theta), r, k))
    return pts   # (x, y, residue, k)


# ── Target ───────────────────────────────────────────────────────────────────

TARGET_RES = 167
TARGET_THETA = 2 * math.pi * TARGET_RES / MOD
TX = RADIUS * math.cos(TARGET_THETA)   # ≈ -24.9989
TY = RADIUS * math.sin(TARGET_THETA)   # ≈ -0.2359

assert abs(TX - (-24.998887453760275)) < 1e-6
assert abs(TY - (-0.235851805647420))  < 1e-6


# ── Kinematics ───────────────────────────────────────────────────────────────

def smoothstep(t):
    return 3 * t**2 - 2 * t**3

def scale(t):
    return 1.35 - 0.8 * t

def center(t):
    p = smoothstep(t)
    return (1 - p) * 0.0 + p * TX, (1 - p) * 0.0 + p * TY

def viewport(t):
    """Returns (cx, cy, half_width)."""
    cx, cy = center(t)
    hw = scale(t) * H0
    return cx, cy, hw


# ── Color map ────────────────────────────────────────────────────────────────

def orbit_color(k, k_max=K_MAX):
    """Blue (k=0) → magenta (k=k_max)."""
    frac = k / k_max
    r = frac
    g = 0.2 * (1 - frac)
    b = 1.0 - 0.4 * frac
    return (r, g, b)


# ── Draw one frame ────────────────────────────────────────────────────────────

def draw_frame(ax, t, orbit):
    ax.clear()
    ax.set_facecolor("#050814")

    cx, cy, hw = viewport(t)
    ax.set_xlim(cx - hw, cx + hw)
    ax.set_ylim(cy - hw, cy + hw)
    ax.set_aspect("equal")
    ax.axis("off")

    # Residue circle (faint)
    circle = plt.Circle((0, 0), RADIUS, color="#1a2040", fill=False,
                         linewidth=0.6, linestyle="--", alpha=0.5)
    ax.add_patch(circle)

    # Web — connect consecutive orbit points
    for i in range(len(orbit) - 1):
        x0, y0 = orbit[i][0], orbit[i][1]
        x1, y1 = orbit[i+1][0], orbit[i+1][1]
        c = orbit_color(i)
        ax.plot([x0, x1], [y0, y1], color=c, linewidth=0.5, alpha=0.35)

    # Orbit points
    for x, y, res, k in orbit:
        c = orbit_color(k)
        size = 6 if k < K_MAX else 0   # target drawn separately
        if size > 0:
            ax.scatter(x, y, color=c, s=size, zorder=3, alpha=0.9)

    # Target — residue 167
    tx, ty = orbit[K_MAX][0], orbit[K_MAX][1]
    ax.scatter(tx, ty, color="#ff9900", s=120, zorder=6, marker="*")
    ax.annotate(
        f"TARGET\n167\n($2^{{35}}$ mod 333)",
        xy=(tx, ty), xytext=(tx + hw * 0.08, ty + hw * 0.06),
        color="#ffcc44", fontsize=6.5, fontfamily="monospace",
        arrowprops=dict(arrowstyle="-", color="#ffcc44", lw=0.6),
    )

    # Frame label
    frame_num = round(t * (N_FRAMES - 1))
    ax.text(
        cx - hw * 0.92, cy + hw * 0.88,
        f"Frame {frame_num} / {N_FRAMES - 1}",
        color="#aaaacc", fontsize=7, fontfamily="monospace",
    )
    ax.text(
        cx - hw * 0.92, cy + hw * 0.78,
        f"t = {t:.3f}   s = {scale(t):.3f}   p = {smoothstep(t):.3f}",
        color="#7788aa", fontsize=6, fontfamily="monospace",
    )
    ax.text(
        cx - hw * 0.92, cy + hw * 0.68,
        f"center = ({center(t)[0]:.2f}, {center(t)[1]:.2f})",
        color="#7788aa", fontsize=6, fontfamily="monospace",
    )

    # Title (fades out as we zoom in)
    alpha_title = max(0.0, 1.0 - t * 2)
    if alpha_title > 0:
        ax.text(
            0, hw * 0.93,
            "Kinematic Focal Zoom — Multiplicative Orbit on Z/333Z",
            color="#ccddff", fontsize=8, ha="center",
            fontfamily="monospace", alpha=alpha_title,
        )

    # Final frame verification text
    if t >= 0.99:
        ax.text(
            cx - hw * 0.92, cy - hw * 0.78,
            f"$2^{{35}} = 167$ (mod 333)",
            color="#44ff88", fontsize=8, fontfamily="monospace",
        )
        ax.text(
            cx - hw * 0.92, cy - hw * 0.88,
            "167 is prime",
            color="#44ff88", fontsize=8, fontfamily="monospace",
        )


# ── Main ──────────────────────────────────────────────────────────────────────

def render(output_path=None):
    if output_path is None:
        output_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "..", "kinematic_focus_residue167.mp4"
        )
    output_path = os.path.abspath(output_path)

    orbit = build_orbit()

    fig, ax = plt.subplots(figsize=(6, 6), dpi=120)
    fig.patch.set_facecolor("#050814")

    def animate(frame):
        t = frame / (N_FRAMES - 1)
        draw_frame(ax, t, orbit)

    anim = FuncAnimation(fig, animate, frames=N_FRAMES, interval=1000 // FPS)

    # Try ffmpeg first, fall back to PNG sequence
    try:
        writer = FFMpegWriter(fps=FPS, metadata={"title": "Kinematic Focal Zoom"})
        anim.save(output_path, writer=writer)
        print(f"Saved → {output_path}")
    except Exception as e:
        print(f"ffmpeg unavailable ({e}), writing PNG sequence instead")
        seq_dir = output_path.replace(".mp4", "_frames")
        os.makedirs(seq_dir, exist_ok=True)
        for frame in range(N_FRAMES):
            t = frame / (N_FRAMES - 1)
            draw_frame(ax, t, orbit)
            fig.savefig(os.path.join(seq_dir, f"frame_{frame:03d}.png"),
                        facecolor="#050814", dpi=120)
        print(f"PNG sequence → {seq_dir}/")
        print(f"Encode with:  ffmpeg -r {FPS} -i {seq_dir}/frame_%03d.png "
              f"-c:v libx264 -pix_fmt yuv420p {output_path}")

    plt.close(fig)
    return output_path


# ── Verification ─────────────────────────────────────────────────────────────

def verify():
    assert pow(2, 35, 333) == 167,   "2^35 mod 333 must be 167"

    # 167 is prime (trial division to sqrt)
    n = 167
    assert all(n % i != 0 for i in range(2, int(n**0.5) + 1)), "167 must be prime"

    orbit = build_orbit()
    assert len(orbit) == 36,         "orbit must have 36 points (k=0..35)"
    assert orbit[K_MAX][2] == 167,   "k=35 must land on residue 167"

    # Target coordinates
    assert abs(orbit[K_MAX][0] - TX) < 1e-10
    assert abs(orbit[K_MAX][1] - TY) < 1e-10

    # Kinematics boundary conditions
    assert abs(scale(0) - 1.35) < 1e-10
    assert abs(scale(1) - 0.55) < 1e-10
    assert abs(smoothstep(0)) < 1e-10
    assert abs(smoothstep(1) - 1.0) < 1e-10
    cx0, cy0 = center(0)
    assert abs(cx0) < 1e-10 and abs(cy0) < 1e-10
    cx1, cy1 = center(1)
    assert abs(cx1 - TX) < 1e-10 and abs(cy1 - TY) < 1e-10

    print("All assertions passed.")


if __name__ == "__main__":
    verify()
    render()
