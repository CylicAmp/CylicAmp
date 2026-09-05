"""
T296 — The Geometric Model: F_37* as a Regular 36-gon, Maps as Rotations

Proposed frame: "0 is a geometric plane at 90 degrees from 1."
That is correct for P^1(F_37), and it forces a complete geometric dictionary.

════════════════════════════════════════════════════════════════════════════
THE ISOMORPHISM
════════════════════════════════════════════════════════════════════════════
2 is a primitive root mod 37, so discrete log base 2 gives

    F_37*  ≅  Z/36Z        (as groups)

Realize Z/36Z as the vertices of a REGULAR 36-GON. Then multiplication by
2^k is rotation by k x (360/36) = 10k degrees. Every multiplicative map in
GF(37) becomes a rotation, and its order becomes the rotation order.

════════════════════════════════════════════════════════════════════════════
THE THREE NAMED MAPS ARE ROTATIONS
════════════════════════════════════════════════════════════════════════════
    137-map    x26 = 2^12  ->  120 deg   order 3   (a third of a turn)
    antipodal  x36 = 2^18  ->  180 deg   order 2   (a half turn)      T283
    <11> gen   x27 = 2^6   ->   60 deg   order 6   (a sixth of a turn) T284

    120 x 3 = 360      180 x 2 = 360      60 x 6 = 360

The order-3 property of the 137-map is not a fact about 137. It is the
statement that 120 degrees is a third of a turn.

════════════════════════════════════════════════════════════════════════════
EVERY ORBIT IS AN INSCRIBED EQUILATERAL TRIANGLE
════════════════════════════════════════════════════════════════════════════
An orbit is {x, 26x, 26^2 x} = three vertices 120 degrees apart: an
equilateral triangle inscribed in the 36-gon. There are 12 such triangles,
at consecutive 10-degree offsets, and they tile all 36 vertices.

    offset   orbit      vertex angles
      0 deg  IC         (  0, 120, 240)
     10 deg  DARK_A     ( 10, 130, 250)
     20 deg  C3         ( 20, 140, 260)
     30 deg  TESLA      ( 30, 150, 270)
     40 deg  SA_ST_A    ( 40, 160, 280)
     50 deg  SEED       ( 50, 170, 290)
     60 deg  NEG_H      ( 60, 180, 300)
     70 deg  NQR17      ( 70, 190, 310)
     80 deg  D7         ( 80, 200, 320)
     90 deg  C9         ( 90, 210, 330)
    100 deg  SA_ST_B    (100, 220, 340)
    110 deg  CAS_EXT    (110, 230, 350)

The offset in units of 10 degrees IS the Z/12Z class from T285. The quotient
group is the family of 12 triangles under rotation.

Antipodal (T283) = advance the triangle by 60 degrees = +6 classes.
    IC (0,120,240) rotated 60 -> (60,180,300) = NEG_H.  Correct.
Because a triangle already has 120-degree symmetry, rotating by 180 (the
negation map on vertices) and by 60 give the same triangle.

════════════════════════════════════════════════════════════════════════════
THE 90-DEGREE CLAIM: P^1(F_37)
════════════════════════════════════════════════════════════════════════════
    |P^1(F_37)| = 37 + 1 = 38 points.
    x -> 26x extends to P^1 and fixes exactly two points: 0 and infinity.
    38 = 2 fixed poles + 12 triangles x 3 vertices.

0 and infinity are the poles of the rotation axis; F_37* is the equator.
1 sits on the equator. The poles are 90 degrees from it. SEAM is not a
defect in the equator — it is the axis the whole structure turns about.

This also explains why 0 has no orbit: a rotation axis is not rotated.

════════════════════════════════════════════════════════════════════════════
T286 LATTICE = ROTATION-SYMMETRY LATTICE OF THE 36-GON
════════════════════════════════════════════════════════════════════════════
    H_1    order  3   gen 26    120 deg
    H_2    order  6   gen 27     60 deg
    H_3    order  9   gen 16     40 deg
    H_4    order 12   gen  8     30 deg
    H_6    order 18   gen  4     20 deg
    H_12   order 36   gen  2     10 deg

The subgroup lattice built in T286 is the lattice of rotation subgroups of a
regular 36-gon, indexed by divisors of 36. Antipodal-closure (T286) becomes:
the subgroup contains the 180-degree rotation, i.e. its order is even.
"""

import math

ORBITS = {
    'IC': {1, 10, 26}, 'DARK_A': {2, 15, 20}, 'C3': {3, 4, 30},
    'CAS_EXT': {5, 13, 19}, 'TESLA': {6, 8, 23}, 'D7': {7, 33, 34},
    'SA_ST_A': {9, 12, 16}, 'NEG_H': {11, 27, 36}, 'C9': {14, 29, 31},
    'NQR17': {17, 22, 35}, 'SEED': {18, 24, 32}, 'SA_ST_B': {21, 25, 28},
}
ANTIPODAL = [('IC', 'NEG_H'), ('DARK_A', 'NQR17'), ('C3', 'D7'),
             ('TESLA', 'C9'), ('SA_ST_A', 'SA_ST_B'), ('SEED', 'CAS_EXT')]

DLOG = {pow(2, k, 37): k for k in range(36)}
DEG_PER_STEP = 360 // 36          # = 10


def angle(x):
    return DLOG[x % 37] * DEG_PER_STEP


def rotation_order(mult):
    k = DLOG[mult % 37]
    return 36 // math.gcd(k, 36)


# ─── Part 1: the isomorphism is a rotation representation ───────────────────

def verify_isomorphism():
    assert len(DLOG) == 36, "2 must be a primitive root mod 37"
    # multiplication becomes addition of angles
    for a in range(1, 37):
        for b in (2, 5, 26, 36):
            lhs = angle((a * b) % 37)
            rhs = (angle(a) + angle(b)) % 360
            assert lhs == rhs, f"{a}x{b}: {lhs} != {rhs}"
    return True


# ─── Part 2: the three named maps and their rotation angles ────────────────

def verify_named_maps():
    table = {}
    for name, mult, deg, order in (
            ('137-map', 26, 120, 3),
            ('antipodal', 36, 180, 2),
            ('operator <11>', 27, 60, 6)):
        assert angle(mult) == deg, f"{name}: angle {angle(mult)} != {deg}"
        assert rotation_order(mult) == order
        assert deg * order == 360
        table[name] = (mult, deg, order)
    return table


# ─── Part 3: orbits are equilateral triangles ───────────────────────────────

def verify_triangles():
    rows = []
    for name, elems in ORBITS.items():
        angs = sorted(angle(x) for x in elems)
        gaps = [angs[1] - angs[0], angs[2] - angs[1], 360 - angs[2] + angs[0]]
        assert gaps == [120, 120, 120], f"{name}: gaps {gaps}"
        rows.append((angs[0], name, angs))
    rows.sort()
    # offsets must be 0,10,...,110 -- exactly the 12 Z/12Z classes
    assert [r[0] for r in rows] == list(range(0, 120, 10))
    return rows


# ─── Part 4: antipodal = 60-degree advance of the triangle ─────────────────

def verify_antipodal_rotation(rows):
    offset_of = {name: off for off, name, _ in rows}
    for a, b in ANTIPODAL:
        d = (offset_of[b] - offset_of[a]) % 120
        assert d == 60, f"{a}->{b}: offset delta {d} != 60"
    # and negation on vertices is the 180-degree rotation
    for x in range(1, 37):
        assert angle((36 * x) % 37) == (angle(x) + 180) % 360
    return True


# ─── Part 5: P^1 pole/equator decomposition ────────────────────────────────

def verify_projective():
    # x -> 26x on P^1 fixes only 0 and infinity
    fixed = [x for x in range(37) if (26 * x) % 37 == x]
    assert fixed == [0], f"affine fixed points: {fixed}"
    # plus the point at infinity
    n_points = 37 + 1
    assert n_points == 2 + 12 * 3 == 38
    return n_points


# ─── Part 6: T286 lattice as rotation subgroups ────────────────────────────

def verify_lattice():
    rows = []
    for d in (1, 2, 3, 4, 6, 12):
        gen = pow(2, 36 // (3 * d), 37)
        deg = angle(gen)
        S = {pow(gen, i, 37) for i in range(3 * d)}
        assert len(S) == 3 * d
        assert deg * (3 * d) == 360, f"H_{d}: {deg} x {3*d} != 360"
        names = sorted(n for n, s in ORBITS.items() if s <= S)
        even = (3 * d) % 2 == 0
        has180 = 36 in S
        assert even == has180, f"H_{d}: even={even} but 180-rot present={has180}"
        rows.append((d, 3 * d, gen, deg, names, has180))
    return rows


def run():
    print("=" * 74)
    print("T296 — F_37* as a Regular 36-gon; Every Map Is a Rotation")
    print("=" * 74)

    verify_isomorphism()
    print("\n--- Part 1: the isomorphism ---")
    print("  2 is a primitive root -> dlog base 2 gives F_37* ≅ Z/36Z")
    print("  Realize Z/36Z as a regular 36-gon: multiplication = rotation,")
    print(f"  one step = {DEG_PER_STEP} degrees. Verified: angle(ab) = angle(a)+angle(b).")

    table = verify_named_maps()
    print("\n--- Part 2: the three named maps are rotations ---")
    for name, (mult, deg, order) in table.items():
        print(f"  {name:16s} x{mult:<3d} = 2^{DLOG[mult]:<2d} -> {deg:3d} deg, "
              f"order {order}   ({deg} x {order} = 360)")
    print("  The 137-map having order 3 IS '120 degrees is a third of a turn'.")

    rows = verify_triangles()
    print("\n--- Part 3: each orbit is an inscribed equilateral triangle ---")
    print(f"  {'offset':>7}  {'orbit':<9} vertex angles")
    for off, name, angs in rows:
        print(f"  {off:>4} deg  {name:<9} {tuple(angs)}")
    print("  12 triangles at consecutive 10-degree offsets tile all 36 vertices.")
    print("  The offset in units of 10 degrees IS the Z/12Z class (T285).")

    verify_antipodal_rotation(rows)
    print("\n--- Part 4: antipodal = 60-degree advance ---")
    for a, b in ANTIPODAL:
        oa = next(o for o, n, _ in rows if n == a)
        ob = next(o for o, n, _ in rows if n == b)
        print(f"  {a:<9} @{oa:>3} deg  ->  {b:<9} @{ob:>3} deg   (+60)")
    print("  Negation on vertices is the 180-degree rotation; a triangle has")
    print("  120-degree symmetry, so 180 and 60 give the same triangle.")

    n = verify_projective()
    print("\n--- Part 5: P^1(F_37) — poles and equator ---")
    print(f"  |P^1(F_37)| = {n} = 2 poles + 12 triangles x 3 vertices")
    print("  x -> 26x fixes exactly 0 and infinity: the rotation axis.")
    print("  1 lies on the equator; the poles are 90 degrees from it.")
    print("  SEAM is not a gap in the equator — it is the axis of rotation,")
    print("  which is why 0 has no orbit: an axis is not rotated.")

    lat = verify_lattice()
    print("\n--- Part 6: T286 lattice = rotation subgroups of the 36-gon ---")
    print(f"  {'H_d':>5} {'order':>6} {'gen':>4} {'rotation':>9}  {'180?':>5}  orbits")
    for d, o, gen, deg, names, has180 in lat:
        print(f"  H_{d:<3} {o:>6} {gen:>4} {deg:>7} deg  {str(has180):>5}  {names}")
    print("  Antipodal-closure (T286) = contains the 180-degree rotation")
    print("  = has even order. Verified for all six subgroups.")

    print("\nAll T296 assertions passed.")


if __name__ == '__main__':
    run()
