#!/usr/bin/env python3
"""
Buddhist Palm imprint — CPU reference render of the SDF used by
shaders/buddhist_palm.glsl. Renders to PNG so the geometry can be checked
before it goes near a GPU.
"""
import numpy as np
from PIL import Image

W = H = 900

def sd_capsule(px, py, ax, ay, bx, by, r):
    pax, pay = px - ax, py - ay
    bax, bay = bx - ax, by - ay
    h = np.clip((pax * bax + pay * bay) / (bax * bax + bay * bay), 0.0, 1.0)
    return np.hypot(pax - bax * h, pay - bay * h) - r

def sd_round_box(px, py, cx, cy, bx, by, r):
    dx = np.abs(px - cx) - bx
    dy = np.abs(py - cy) - by
    return (np.hypot(np.maximum(dx, 0), np.maximum(dy, 0))
            + np.minimum(np.maximum(dx, dy), 0.0) - r)

def hand_sdf(px, py):
    """Palm + thumb + four fingers, unioned with min."""
    d = sd_round_box(px, py, 0.0, -0.10, 0.20, 0.20, 0.10)      # palm
    # four fingers: (x0, y0, x1, y1, radius)
    for x0, y0, x1, y1, r in (
        (-0.20, 0.06, -0.26, 0.44, 0.058),   # index
        (-0.07, 0.09, -0.08, 0.55, 0.060),   # middle
        ( 0.07, 0.09,  0.10, 0.51, 0.058),   # ring
        ( 0.19, 0.06,  0.26, 0.38, 0.050),   # pinky
    ):
        d = np.minimum(d, sd_capsule(px, py, x0, y0, x1, y1, r))
    d = np.minimum(d, sd_capsule(px, py, -0.20, -0.16, -0.44, 0.06, 0.066))  # thumb
    return d

def cracks(px, py, n=13, seed=7):
    """Radial fissures: nearest angular spoke, amplitude growing with radius."""
    rng = np.random.default_rng(seed)
    jit = rng.uniform(-0.16, 0.16, n)
    amp = rng.uniform(0.55, 1.0, n)
    r = np.hypot(px, py) + 1e-6
    a = np.arctan2(py, px)
    out = np.zeros_like(px)
    for k in range(n):
        th = -np.pi + 2 * np.pi * k / n + jit[k]
        # wobble so the fissure is not a straight ray
        th_r = th + 0.22 * np.sin(r * 7.0 + k * 2.1)
        da = np.abs(np.mod(a - th_r + np.pi, 2 * np.pi) - np.pi)
        width = 0.006 + 0.030 * r
        line = np.clip(1.0 - da / width, 0.0, 1.0)
        reach = np.clip((r - 0.28) / 0.9, 0.0, 1.0) * np.exp(-r * 0.8)
        out = np.maximum(out, line * reach * amp[k])
    return out

y, x = np.mgrid[0:H, 0:W]
px = (x - W / 2) / (W * 0.42)
py = (H / 2 - y) / (H * 0.42)

d = hand_sdf(px, py)
c = cracks(px, py)

inside = np.clip(-d / 0.02, 0.0, 1.0)                  # imprint mask
rim    = np.exp(-np.abs(d) * 55.0) * 0.9               # pressed-up rim
depth  = np.clip(-d / 0.16, 0.0, 1.0) ** 0.6           # depression depth

# earth palette
base = np.stack([np.full_like(px, 0.42), np.full_like(px, 0.34),
                 np.full_like(px, 0.26)], -1)
grain = (np.random.default_rng(3).normal(0, 0.022, px.shape))[..., None]
img = base + grain

shadow = (0.30 + 0.70 * (1 - depth))[..., None]
img = img * np.where(inside[..., None] > 0, shadow, 1.0)
img = img + rim[..., None] * np.array([0.26, 0.22, 0.16])
img = img - c[..., None] * np.array([0.34, 0.30, 0.24])
img = img + (c * 0.20)[..., None] * np.array([0.05, 0.03, 0.02])

img = np.clip(img, 0, 1)
Image.fromarray((img * 255).astype(np.uint8)).save(
    '/home/user/CylicAmp/shaders/buddhist_palm.png')
print("wrote shaders/buddhist_palm.png")
print(f"  hand SDF range: {d.min():.3f} .. {d.max():.3f}")
print(f"  imprint covers {100*(d<0).mean():.1f}% of frame")
print(f"  crack intensity max {c.max():.3f}")
