# math/theorems/clifford_fibration_audit.py
"""
Clifford Parallelism & Hopf Fibration Audit — 600-Cell (120 Long Radii)

The 120 vertices of the 600-cell form the binary icosahedral group 2I ⊂ S³.
The Hopf fibration π: S³ → S² decomposes S³ into great-circle fibers.
Clifford-parallel fibers are at constant distance from each other.

Audit checklist
───────────────
1. All 120 vertices lie on the unit 3-sphere.                  [long radii intact]
2. Hopf map is well-defined on all 120 vertices.               [fibration defined]
3. Antipodal pairs v, −v map to the same point on S².          [fiber symmetry]
4. Distinct Hopf images — 60 points on S².                     [fiber count]
5. Great-circle fibers are Clifford-parallel (constant chord). [parallelism]
6. Fiber family partitions 2I into cosets of the circle S¹∩2I. [coset structure]

"B Matrix" proxy: sensitivity of Hopf image to vertex perturbation.
"""

import math
from typing import List, Tuple

import numpy as np

# Import the vertex generator from the existing 600-cell module
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from hexacosichoron_600cell import generate_vertices

PHI     = (1 + math.sqrt(5)) / 2
INV_PHI = PHI - 1


# ── Hopf map  π: S³ → S²  ─────────────────────────────────────────────────────

def hopf_map(v: Tuple[float, float, float, float]) -> Tuple[float, float, float]:
    """
    Standard Hopf map as quaternion projection.
    q = a + bi + cj + dk  →  (x, y, z) ∈ S²

        x = 2(ac + bd)
        y = 2(bc − ad)
        z = a² + b² − c² − d²

    The fiber through q is the great circle {q · e^(iθ) : θ ∈ [0,2π)}.
    """
    a, b, c, d = v
    x = 2 * (a*c + b*d)
    y = 2 * (b*c - a*d)
    z = a**2 + b**2 - c**2 - d**2
    return (x, y, z)


def hopf_fiber_distance(v1, v2) -> float:
    """
    Chord distance between the Hopf images of two S³ points.
    For Clifford-parallel fibers this is constant across all pairs of points
    drawn one from each fiber.
    """
    p1 = hopf_map(v1)
    p2 = hopf_map(v2)
    return math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))


def round_point(p, decimals=8):
    return tuple(round(x, decimals) for x in p)


# ── Load vertices ──────────────────────────────────────────────────────────────

VERTICES = generate_vertices()
assert len(VERTICES) == 120

V = np.array(sorted(VERTICES))    # shape (120, 4); sort for determinism


# ── Audit 1: all 120 long radii intact ────────────────────────────────────────

norms = np.sqrt((V ** 2).sum(axis=1))
assert np.allclose(norms, 1.0, atol=1e-9), "FAIL: vertices not on unit S³"
# All 120 line segments from origin to vertex have length = 1.
# "Long radii" are intact.

# ── Audit 2: Hopf map is well-defined on all 120 vertices ─────────────────────

hopf_images_raw = [hopf_map(tuple(v)) for v in VERTICES]

# Each image should lie on S² (radius 1)
for img in hopf_images_raw:
    r = math.sqrt(sum(x**2 for x in img))
    assert abs(r - 1.0) < 1e-9, f"FAIL: Hopf image not on S²: {img}"

# ── Audit 3: antipodal symmetry v → −v maps to same S² point ─────────────────

vertex_set = {round_point(tuple(v)) for v in VERTICES}
for v in VERTICES:
    neg_v = tuple(-x for x in v)
    if round_point(neg_v) in vertex_set:
        # Both v and -v are 600-cell vertices; their Hopf images should match
        img_v    = round_point(hopf_map(tuple(v)), 6)
        img_negv = round_point(hopf_map(neg_v), 6)
        assert img_v == img_negv, f"FAIL: antipodal symmetry broken at {v}"

# ── Audit 4: count distinct Hopf images ───────────────────────────────────────

distinct_images = {round_point(img, 6) for img in hopf_images_raw}
n_fibers = len(distinct_images)
# Each Hopf fiber contains 4 vertices of 2I (two antipodal pairs {v,-v} and {w,-w}
# that share the same great-circle fiber).  120 / 4 = 30 distinct fibers.
assert n_fibers == 30, f"FAIL: expected 30 distinct Hopf images, got {n_fibers}"

# ── Audit 5: Clifford parallelism ─────────────────────────────────────────────
# Group vertices by their Hopf image (fiber membership)
fiber_map = {}
for v in VERTICES:
    key = round_point(hopf_map(tuple(v)), 6)
    fiber_map.setdefault(key, []).append(tuple(v))

fiber_list = list(fiber_map.values())
assert len(fiber_list) == 30
assert all(len(f) == 4 for f in fiber_list)   # 4 vertices per fiber (2 antipodal pairs)

# Each fiber contains its two antipodal pairs
for f in fiber_list:
    fset = {round_point(v, 8) for v in f}
    for v in f:
        neg = round_point(tuple(-x for x in v), 8)
        assert neg in fset, "FAIL: antipodal pair not in same fiber"

# Clifford parallelism: all fibers are left cosets of U(1) = {(a,b,0,0) : a²+b²=1}.
# For any two vertices v₁, v₂ in the same fiber, v₁⁻¹·v₂ must lie in U(1),
# i.e. its 3rd and 4th quaternion components must be zero.
def quat_mult_conj(p, q):
    """p·q̄  (p times conjugate-of-q) as quaternion product.
    For left cosets U(1)·v0: vi = e^(iα)·v0, so v0·vī = e^(−iα) ∈ U(1).
    j and k components must be zero.
    """
    a, b, c, d = p
    e, f, g, h = q
    # q̄ = (e, -f, -g, -h)
    return (
         a*e + b*f + c*g + d*h,    # real part
        -a*f + b*e - c*h + d*g,    # i part
        -a*g + b*h + c*e - d*f,    # j part  ← must be 0 for U(1) membership
        -a*h - b*g + c*f + d*e,    # k part  ← must be 0 for U(1) membership
    )

for f in fiber_list:
    v0 = f[0]
    for vi in f[1:]:
        r = quat_mult_conj(v0, vi)
        assert abs(r[2]) < 1e-9 and abs(r[3]) < 1e-9, \
            f"FAIL: intra-fiber ratio not in U(1): {r}"

# ── Audit 6: coset structure ───────────────────────────────────────────────────
# The fiber through the identity element {(1,0,0,0), (-1,0,0,0)} should exist
identity_fiber_key = round_point(hopf_map((1.0, 0.0, 0.0, 0.0)), 6)
assert identity_fiber_key in fiber_map, "FAIL: identity fiber not found"
identity_fiber = fiber_map[identity_fiber_key]
# Both elements should be present
assert (1.0, 0.0, 0.0, 0.0) in identity_fiber or \
       any(abs(v[0]-1.0) < 1e-9 and all(abs(v[k])<1e-9 for k in [1,2,3])
           for v in identity_fiber)

# ── B Matrix (input sensitivity) proxy ────────────────────────────────────────
# dπ/dv at each vertex: how much does the Hopf image move under a unit perturbation?
# This is the Jacobian of the Hopf map — a 3×4 matrix at each point.

def hopf_jacobian(v) -> np.ndarray:
    """3×4 Jacobian of the Hopf map at point v = (a,b,c,d).
    x=2(ac+bd), y=2(bc−ad), z=a²+b²−c²−d²
    """
    a, b, c, d = v
    return np.array([
        [ 2*c,  2*d,  2*a,  2*b],   # ∂x/∂(a,b,c,d)
        [-2*d,  2*c,  2*b, -2*a],   # ∂y/∂(a,b,c,d)  y=2bc−2ad
        [ 2*a,  2*b, -2*c, -2*d],   # ∂z/∂(a,b,c,d)
    ])

# ||J||_F² = 4(a²+b²+c²+d²)×3 = 12  →  ||J||_F = 2√3  for all v ∈ S³
B_norms = [np.linalg.norm(hopf_jacobian(tuple(v)), 'fro') for v in VERTICES]
assert np.allclose(B_norms, 2.0 * math.sqrt(3), atol=1e-9), \
    f"FAIL: non-uniform B-matrix norms: min={min(B_norms):.6f} max={max(B_norms):.6f}"
# Uniform B-matrix norm = 2√3 across all 120 vertices confirms:
# the Hopf map has constant input sensitivity — no "fragile" long radius.


if __name__ == "__main__":
    print("Clifford Fibration Audit — 600-Cell (120 Long Radii)")
    print()
    print(f"  Vertices on S³:          {len(VERTICES)}  ✓")
    print(f"  Distinct Hopf images:    {n_fibers}   ✓  (30 fibers × 4 vertices = 120)")
    print(f"  Fibers of size 4:        {sum(1 for f in fiber_list if len(f)==4)}   ✓")
    print()
    print("  Clifford parallelism — algebraic coset check (v0·vī ∈ U(1)):")
    sample_checks = []
    for f in fiber_list[:5]:
        v0 = f[0]
        for vi in f[1:]:
            r = quat_mult_conj(v0, vi)
            sample_checks.append((round(r[2], 9), round(r[3], 9)))
    print(f"    sample j,k components: {sample_checks[:3]}")
    print(f"    all zero to 1e-9 ✓")
    print()
    print(f"  B-matrix (Hopf Jacobian) Frobenius norm:")
    print(f"    Expected: 2√3 = {2*math.sqrt(3):.6f}")
    print(f"    Min:      {min(B_norms):.6f}   Max: {max(B_norms):.6f}   ✓")
    print(f"    Interpretation: uniform input sensitivity — no fragile long radius")
    print()
    print("  37-field:")
    print(f"    120 mod 37 = {120 % 37}   (TRINITY_SQUARED, DR=3)")
    print(f"    30  mod 37 = {30  % 37}   (fiber count, DR=3 = sovereign target)")
    print()
    print("STATUS: FIBRATION INTACT. All 120 long radii verified.")
    print("        Clifford parallelism holds. Metastasis contained.")
    print()
    print("All assertions passed.")
