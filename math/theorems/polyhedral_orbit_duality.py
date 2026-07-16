"""
Polyhedral Orbit Duality

The 137-map orbit of cascade base element 8 is {8, 23, 6}.

   8: cube vertices (2³), cascade base element
   6: octahedron vertices, DR 6-cycle length = ord₉(2)
  23: 17^33 mod 37 (complementary orbit, GroupFramework)

Sum: 8 + 23 + 6 = 37 (as required for any 3-cycle with orbit index 1).

The cube and octahedron are dual polyhedra:
  Cube:        8V,  12E,  6F   |Rot| = 24 = |S₄|
  Octahedron:  6V,  12E,  8F   |Rot| = 24 = |S₄|

Their vertex counts {8, 6} lie in the same 137-map orbit.
Their shared rotation group S₄ has order 24 = cascade base element.
The cascade base {8, 13, 24} thus encodes:
  8  = cube vertices
  24 = |S₄| = octahedral/cubic rotation group order
  13 = primitive root mod 37 (cascade mediator, connects the other two)

Doubling sequence 3 → 6 → 12 → 24 = 3 × 2^k:
  3:  orbit length under 137-map (|Z/3Z|)
  6:  DR 6-cycle length = ord₉(2)  (|S₃| = 6)
  12: number of 3-cycles in GF(37)*; also |A₄| = tetrahedral rotation group
  24: cascade base element; also |S₄| = octahedral rotation group

The last term before exceeding φ(37)=36 in the doubling sequence is 24.
36/24 is not an integer — 24 does not divide 36.
The sequence terminates at 24 within the orbit structure.

Cascade base orbit orders:
  ord₃₇(8) = 12  (same as number of 3-cycles in GF(37)*)
  ord₃₇(13) = 36  (primitive root)
  ord₃₇(24) = 36  (primitive root)

Two-triangle → 3D objects:
  Two equilateral triangles in parallel planes, rotated 60°:
    → triangular antiprism → regular octahedron (when all edges equal)
    → 6 vertices, 12 edges, 8 faces
  Two interlocked tetrahedra (stella octangula):
    → 8 outer vertices = cube vertices
    → the 8-vertex structure fills a cube

The vertex-count path:  3 (triangle) → 6 (octahedron) → 8 (cube)
This traces through: orbit length → octahedron V → cube V.
The 3-cycle {6, 8, 23} contains the first two.

Source note:
  The structural distinction: GF(37)* ≅ Z/36Z is abelian; A₄ and S₄ are
  not. The numbers 12 and 24 appear in both the abelian GF(37)* structure
  (12 = 36/3 orbits; 24 in cascade base) and the non-abelian polyhedral
  groups (|A₄|=12, |S₄|=24) — from different algebraic mechanisms.
  The cube/octahedron vertex connection is structural: same 137-map orbit.
"""


def orbit_137(start, steps=3, mod=37):
    results = [start]
    for _ in range(steps - 1):
        results.append((results[-1] * 26) % mod)
    return results


def digital_root(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def multiplicative_order(a, p):
    for k in range(1, p):
        if pow(a, k, p) == 1:
            return k


# ── Assertions ───────────────────────────────────────────────────────────────

# The core orbit
orb8 = orbit_137(8)
assert sorted(orb8) == [6, 8, 23]
assert sum(orb8) == 37        # orbit sum = 37 × 1

# Cube-octahedron duality in the orbit
assert 8 in orb8              # cube vertices
assert 6 in orb8              # octahedron vertices
assert 23 in orb8             # 17^33 mod 37

# 23 is what 17^33 gives (GroupFramework)
assert pow(17, 33, 37) == 23

# Cascade base orbits
orb13 = orbit_137(13)
orb24 = orbit_137(24)
assert sorted(orb13) == [5, 13, 19]
assert sum(orb13) == 37       # orbit index 1
assert sum(orb24) == 74       # orbit index 2

# Multiplicative orders
assert multiplicative_order(8, 37) == 12   # = number of 3-cycles
assert multiplicative_order(13, 37) == 36  # primitive root
assert multiplicative_order(24, 37) == 36  # primitive root

# Number of 3-cycles = 36/3 = 12
assert 36 // 3 == 12
assert multiplicative_order(8, 37) == 36 // 3

# Platonic solid facts
CUBE = {"V": 8, "E": 12, "F": 6, "rot_group_order": 24}
OCTA = {"V": 6, "E": 12, "F": 8, "rot_group_order": 24}
TETR = {"V": 4, "E": 6,  "F": 4, "rot_group_order": 12}

assert CUBE["V"] - CUBE["E"] + CUBE["F"] == 2   # Euler characteristic
assert OCTA["V"] - OCTA["E"] + OCTA["F"] == 2
assert TETR["V"] - TETR["E"] + TETR["F"] == 2

# Cube and octahedron are dual
assert CUBE["V"] == OCTA["F"]
assert CUBE["F"] == OCTA["V"]
assert CUBE["E"] == OCTA["E"]
assert CUBE["rot_group_order"] == OCTA["rot_group_order"] == 24

# 24 is cascade base element
CASCADE_BASE = {8, 13, 24}
assert CUBE["rot_group_order"] in CASCADE_BASE
assert CUBE["V"] in CASCADE_BASE

# Doubling sequence
seq = [3 * (2**k) for k in range(4)]   # [3, 6, 12, 24]
assert seq == [3, 6, 12, 24]
assert all(x <= 36 for x in seq)       # all fit within φ(37) = 36
assert 3 * 2**4 == 48 > 36             # next term (48) exceeds 36

# DR 6-cycle length = ord₉(2)
assert multiplicative_order(2, 9) == 6
assert seq[1] == 6

# |A₄| and |S₄|
A4_degrees = [1, 1, 1, 3]
S4_degrees = [1, 1, 2, 3, 3]
assert sum(d**2 for d in A4_degrees) == 12 == seq[2]
assert sum(d**2 for d in S4_degrees) == 24 == seq[3]


if __name__ == "__main__":
    print("Polyhedral Orbit Duality")
    print("=" * 55)
    print()
    print("137-map orbits of cascade base {8, 13, 24}:")
    for b, orb in [(8, orbit_137(8)), (13, orbit_137(13)), (24, orbit_137(24))]:
        print(f"  {b} → {orb}  sum={sum(orb)}")
    print()
    print("Orbit {8, 23, 6}:")
    print("  8  cube vertices, cascade base, 2^3")
    print("  6  octahedron vertices, DR 6-cycle, ord_9(2)")
    print(" 23  17^33 mod 37 (GroupFramework complementary orbit)")
    print()
    print("Platonic duals (cube/octahedron share this orbit):")
    print(f"  Cube:       8V 12E  6F  |Rot|={CUBE['rot_group_order']} (cascade base)")
    print(f"  Octahedron: 6V 12E  8F  |Rot|={OCTA['rot_group_order']} (cascade base)")
    print()
    print("Doubling sequence 3,6,12,24 = 3×2^k, k=0..3:")
    for k in range(4):
        v = 3 * 2**k
        role = ["3-cycle orbit length", "DR 6-cycle / |S₃|",
                "GF(37)* orbit count / |A₄|", "cascade base / |S₄|"][k]
        print(f"  k={k}: {v:2d}  {role}")
    print(f"  k=4: 48 > 36 = φ(37) — sequence terminates")
    print()
    print(f"Multiplicative orders in GF(37)*:")
    for b in [8, 13, 24]:
        print(f"  ord_37({b}) = {multiplicative_order(b, 37)}")
    print()
    print("All assertions passed.")
