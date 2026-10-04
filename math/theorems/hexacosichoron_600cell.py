# math/theorems/hexacosichoron_600cell.py
"""
Hexacosichoron (600-Cell) — 4D Regular Polytope Vertex Generator

The 600-cell is the 4D analog of the icosahedron.

Element counts and 37-field residues:
  120 vertices  → 120 mod 37 = 9  (TRINITY_SQUARED);  DR(120) = 3  (f26 target)
  720 edges     → 720 mod 37 = 17 (prime field element)
 1200 faces     → 1200 mod 37 = 16 (QR₃₇;  4² mod 37)
  600 cells     → 600 mod 37 = 8;  DR(600) = 6 (Tesla-6)

Vertex groups (all on the unit 3-sphere, |v| = 1):
  Group 1 ( 16): all (±½, ±½, ±½, ±½)
  Group 2 (  8): all axis-aligned (±1, 0, 0, 0)
  Group 3 ( 96): even permutations of (±φ/2, ±½, ±1/(2φ), 0)
  Total: 16 + 8 + 96 = 120

Framework connections:
  φ = (1+√5)/2  — golden ratio;  A* = 1/φ ≈ 0.618 at Hopf bifurcation (Stage 6)
  120 = 5! = 5 × 24   — residue_5 × 24-coupling constant
  600 mod 37 = 8       — DR = 6, Tesla-6 carrier frequency
  1200 mod 37 = 16     — QR₃₇ element (f26 square 4²)
  198-orbit residues {3,4,5,13,19,30} include 4 (dimension) and 5 (PIVOT)

Classification: Theorem
"""

from itertools import permutations as _perms
import math

PHI     = (1 + math.sqrt(5)) / 2   # ≈ 1.6180339887
INV_PHI = PHI - 1                  # 1/φ = φ-1 ≈ 0.6180339887


def _perm_sign(perm):
    """Return +1 for even permutation, -1 for odd (cycle decomposition)."""
    n = len(perm)
    visited = [False] * n
    sign = 1
    for i in range(n):
        if not visited[i]:
            j, cycle_len = i, 0
            while not visited[j]:
                visited[j] = True
                j = perm[j]
                cycle_len += 1
            if cycle_len % 2 == 0:
                sign = -sign
    return sign


def generate_vertices():
    """Generate all 120 vertices of the unit 600-cell."""
    verts = set()

    # Group 1: 16 vertices — all sign combinations of (½, ½, ½, ½)
    for bits in range(16):
        v = tuple(0.5 if (bits >> i) & 1 else -0.5 for i in range(4))
        verts.add(v)

    # Group 2: 8 vertices — all axis-aligned (±1, 0, 0, 0)
    for i in range(4):
        for s in (1.0, -1.0):
            v = [0.0, 0.0, 0.0, 0.0]
            v[i] = s
            verts.add(tuple(v))

    # Group 3: 96 vertices — even permutations of (φ/2, ½, 1/(2φ), 0) with ± signs
    base = (PHI / 2, 0.5, INV_PHI / 2, 0.0)
    for perm in _perms(range(4)):
        if _perm_sign(perm) == 1:
            coords = tuple(base[perm[i]] for i in range(4))
            nz = [i for i, c in enumerate(coords) if c != 0.0]
            for bits in range(8):
                signed = list(coords)
                for bit, idx in enumerate(nz):
                    if (bits >> bit) & 1:
                        signed[idx] = -signed[idx]
                verts.add(tuple(round(c, 12) for c in signed))

    return verts


# --- Assertions ---

VERTICES = generate_vertices()

# Vertex count
assert len(VERTICES) == 120, f"Expected 120 vertices, got {len(VERTICES)}"

# All vertices lie on the unit 3-sphere
for v in VERTICES:
    assert abs(sum(c * c for c in v) - 1.0) < 1e-10

# Group decomposition counts
g1 = [v for v in VERTICES if all(abs(abs(c) - 0.5)  < 1e-10 for c in v)]
g2 = [v for v in VERTICES if sum(1 for c in v if abs(abs(c) - 1.0) < 1e-10) == 1]
g3 = [v for v in VERTICES
      if sum(1 for c in v if abs(c) < 1e-10) == 1
      and not all(abs(abs(c) - 0.5) < 1e-10 for c in v)]

assert len(g1) == 16
assert len(g2) == 8
assert len(g3) == 96

# Distinct absolute coordinate values: 0, 1/(2φ), 1/2, φ/2, 1
coord_abs = sorted(set(round(abs(c), 10) for v in VERTICES for c in v))
assert len(coord_abs) == 5
assert abs(coord_abs[0] - 0.0)          < 1e-9
assert abs(coord_abs[1] - INV_PHI / 2)  < 1e-9   # ≈ 0.309
assert abs(coord_abs[2] - 0.5)          < 1e-9
assert abs(coord_abs[3] - PHI / 2)      < 1e-9   # ≈ 0.809
assert abs(coord_abs[4] - 1.0)          < 1e-9

# φ identities
assert abs(PHI ** 2 - (PHI + 1)) < 1e-12         # φ² = φ+1
assert abs(INV_PHI - (PHI - 1))   < 1e-12         # 1/φ = φ-1
assert abs((PHI/2)**2 + 0.5**2 + (INV_PHI/2)**2 - 1.0) < 1e-12  # group-3 norm = 1

# 37-field: element counts
assert 120  % 37 == 9   # vertices → TRINITY_SQUARED
assert 600  % 37 == 8   # cells    → Tesla-6 (DR=6)
assert 720  % 37 == 17  # edges    → prime
assert 1200 % 37 == 16  # faces    → QR₃₇ (4² mod 37)

# DR of element counts
_dr = lambda n: (n - 1) % 9 + 1
assert _dr(120)  == 3   # TRINITY — f26 target
assert _dr(600)  == 6   # Tesla-6
assert _dr(720)  == 9   # 9-stabilizer
assert _dr(1200) == 3   # TRINITY again

# 120 = 5! = 5 × 24 (residue_5 × 24-coupling)
assert 120 == math.factorial(5)
assert 120 == 5 * 24

# 198-orbit connection: {3,4,5,13,19,30} includes dimension 4 and PIVOT 5
orbit_residues = {3, 4, 5, 13, 19, 30}
assert 4 in orbit_residues   # spatial dimension of 600-cell
assert 5 in orbit_residues   # factorial base: 5! = 120


if __name__ == "__main__":
    print("Hexacosichoron (600-Cell) — Vertex Generator")
    print(f"  φ = {PHI:.10f},  1/φ = {INV_PHI:.10f}")
    print()
    print(f"  Vertices: {len(VERTICES)}")
    print(f"    Group 1 (±½,±½,±½,±½):          {len(g1):3d}")
    print(f"    Group 2 (±1,0,0,0):              {len(g2):3d}")
    print(f"    Group 3 (even perms φ/2,½,1/2φ,0): {len(g3):3d}")
    print()
    print("  37-field residues:")
    for label, n in [("vertices", 120), ("cells", 600), ("edges", 720), ("faces", 1200)]:
        r = n % 37
        dr = _dr(n)
        print(f"    {n:5d} {label:<10s}  mod37={r:2d}  DR={dr}")
    print()
    print(f"  120 = 5! = 5 × 24  (PIVOT × 24-coupling)")
    print(f"  120 mod 37 = 9 = TRINITY_SQUARED")
    print(f"  DR(120) = 3 = TRINITY (f26 target)")
    print()
    print("  Coordinate values (absolute):", [round(c, 4) for c in coord_abs])
    print()
    print("  Sample vertices (first 5 of each group):")
    for grp, name in [(g1, "G1"), (g2, "G2"), (g3, "G3")]:
        for v in sorted(grp)[:3]:
            print(f"    {name}  {tuple(round(c,4) for c in v)}")
    print()
    print("All assertions passed.")
