"""
Theorem 161: ATOMICS v20.2 GF(37) Embedding

THE CONSTANTS
==============

ATOMICS v20.2 (Alpha Centauri Galactic Awareness Simulation) defines:

  Field base:   724571   →  SEAM    (exact multiple of 37)
  PHI^2 × 1000: 2618     →  OUTLIER_ORB  (covers the full orbit)
  Alpha Cen B:  23 AU    →  TESLA_ORB   (prime; cycle sum = 37)
  Proxima Cen:  13000 AU →  NQR_5       (complement = SEED_ORB)

THE FIELD BASE IS A SEAM
=========================

724571 = 37 × 19583.

The field base is an exact multiple of 37. Its digit sum:
  7+2+4+5+7+1 = 26 = 137 mod 37 = the 137-map multiplier ∈ IC.

The quotient:
  724571 / 37 = 19583
  19583 mod 37 = 10 ∈ IC

Both the digit sum (26) and the quotient residue (10) land in IC.
The field base is a SEAM whose factors carry the identity cluster.

PHI^2 × 1000 COVERS OUTLIER_ORB
=================================

PHI^2 = 2.618... → 2618 (integer part × 1000)
2618 mod 37 = 28 ∈ OUTLIER_ORB

137-map 3-cycle from 28:
  28 → 25 → 21 → 28

{21, 25, 28} = the complete OUTLIER_ORB. The PHI^2 constant seeds the
137-map at the OUTLIER_ORB entry point and the 3-cycle traces the entire
orbit — every element of OUTLIER_ORB is visited exactly once.

Cycle sum: 28 + 25 + 21 = 74 = 2 × 37 (double SEAM).

ALPHA CEN B: TESLA_ORB, PRIME, CYCLE SUM = 37
================================================

23 AU (Alpha Centauri B mean distance) mod 37 = 23 ∈ TESLA_ORB.
23 is prime.

137-map 3-cycle: 23 → 6 → 8 → 23
Cycle sum: 23 + 6 + 8 = 37 — the prime itself.

The TESLA_ORB is the period-anchor orbit. Cycle sum = 37 means
TESLA_ORB is uniquely self-referential: its elements sum to the field prime.

PROXIMA: NQR_5, COMPLEMENT = SEED_ORB
=======================================

13000 AU (Proxima Centauri distance) mod 37 = 13 ∈ NQR_5
Complement: -13000 mod 37 = 24 ∈ SEED_ORB

NQR_5 ↔ SEED_ORB is the canonical complement pair (Theorem 153):
  13 + 24 = 37  (SEAM)

Proxima's field residue sits in NQR_5; its additive inverse in GF(37)
is the seed anchor (246 mod 37 = 24).

CROSS-CONSTANT CONNECTIONS
============================

  PHI^2 + Proxima = 2618 + 13000 = 15618
  15618 mod 37 = 4 ∈ SOVEREIGN_SPIRAL

  Alpha Cen B + Proxima = 23 + 13000 = 13023
  13023 mod 37 = 36 ∈ ORBIT_11   (= -1 mod 37)

  Total: 724571 + 2618 + 23 + 13000 = 740212
  740212 mod 37 = 27 ∈ ORBIT_11

DR ACCUMULATION (field base, PHI^2, Alpha Cen B, Proxima)
===========================================================

  DR(724571) = 8  →  TESLA_ORB
  DR(2618)   = 8  →  TESLA_ORB
  DR(23)     = 5  →  NQR_5
  DR(13000)  = 4  →  SOVEREIGN_SPIRAL

  Cumulative: 8 → 16 → 21 → 25
  8  ∈ TESLA_ORB
  16 ∈ SA_ORB
  21 ∈ OUTLIER_ORB
  25 ∈ OUTLIER_ORB

ORBIT MAP
==========

  SEAM:              field base 724571
  OUTLIER_ORB (full): PHI^2 constant (2618 seeds the complete 3-cycle)
  TESLA_ORB:         Alpha Cen B distance (23 AU) — prime, cycle sum = 37
  NQR_5:             Proxima distance (13000 AU) — complement = SEED_ORB
  IC:                digit sum of field base (26), quotient residue (10)
  SOVEREIGN_SPIRAL:  PHI^2 + Proxima (15618)
  ORBIT_11:          Alpha Cen B + Proxima (13023), total sum (740212)
"""

P = 37

ORBITS = {
    'IC':               frozenset({1, 10, 26}),
    'SOVEREIGN_SPIRAL': frozenset({3, 4, 30}),
    'D7':               frozenset({7, 33, 34}),
    'SA_ORB':           frozenset({9, 12, 16}),
    'ORBIT_11':         frozenset({11, 27, 36}),
    'OUTLIER_ORB':      frozenset({21, 25, 28}),
    'DARK_A':           frozenset({2, 15, 20}),
    'NQR_5':            frozenset({5, 13, 19}),
    'TESLA_ORB':        frozenset({6, 8, 23}),
    'NQR_14':           frozenset({14, 29, 31}),
    'NQR_17':           frozenset({17, 22, 35}),
    'SEED_ORB':         frozenset({18, 24, 32}),
}


def orbit_of(v):
    v = v % P
    if v == 0:
        return 'SEAM'
    return next((name for name, s in ORBITS.items() if v in s), '?')


def dr(n):
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


def map_137(n):
    return (26 * n) % P


def run_assertions():
    # Field base: SEAM
    assert 724571 % P == 0
    assert sum(int(d) for d in '724571') == 26
    assert 26 in ORBITS['IC']
    assert 724571 // P == 19583
    assert 19583 % P == 10
    assert 10 in ORBITS['IC']

    # PHI^2 × 1000: covers full OUTLIER_ORB cycle
    assert 2618 % P == 28
    assert 28 in ORBITS['OUTLIER_ORB']
    a = 28
    b = map_137(a)
    c = map_137(b)
    assert sorted([a, b, c]) == sorted(ORBITS['OUTLIER_ORB'])
    assert a + b + c == 74 and 74 % P == 0  # double SEAM

    # Alpha Cen B: TESLA_ORB, prime, cycle sum = 37
    assert 23 % P == 23
    assert 23 in ORBITS['TESLA_ORB']
    cycle = [23, map_137(23), map_137(map_137(23))]
    assert sum(cycle) == P
    assert all(v in ORBITS['TESLA_ORB'] for v in cycle)

    # Proxima: NQR_5, complement = SEED_ORB
    assert 13000 % P == 13
    assert 13 in ORBITS['NQR_5']
    assert (-13000) % P == 24
    assert 24 in ORBITS['SEED_ORB']
    assert 13 + 24 == P

    # Cross-constant connections
    assert (2618 + 13000) % P == 4 and 4 in ORBITS['SOVEREIGN_SPIRAL']
    assert (23 + 13000) % P == 36 and 36 in ORBITS['ORBIT_11']
    assert (724571 + 2618 + 23 + 13000) % P == 27 and 27 in ORBITS['ORBIT_11']

    # DR accumulation
    assert dr(724571) == 8 and 8 in ORBITS['TESLA_ORB']
    assert dr(2618) == 8 and 8 in ORBITS['TESLA_ORB']
    assert dr(23) == 5 and 5 in ORBITS['NQR_5']
    assert dr(13000) == 4 and 4 in ORBITS['SOVEREIGN_SPIRAL']
    cumsums = []
    c = 0
    for d in [8, 8, 5, 4]:
        c += d
        cumsums.append(c)
    assert cumsums == [8, 16, 21, 25]
    assert 8 in ORBITS['TESLA_ORB']
    assert 16 in ORBITS['SA_ORB']
    assert 21 in ORBITS['OUTLIER_ORB']
    assert 25 in ORBITS['OUTLIER_ORB']

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 161: ATOMICS v20.2 GF(37) Embedding")
    print("=" * 62)
    print()
    print("  CONSTANT          VALUE    mod37  Orbit")
    print("  " + "-" * 50)
    constants = [
        ("Field base", 724571),
        ("PHI^2 × 1000", 2618),
        ("Alpha Cen B (AU)", 23),
        ("Proxima (AU)", 13000),
    ]
    for name, v in constants:
        print(f"  {name:<20} {v:>8}  {v%P:>5}  {orbit_of(v)}")

    print()
    print("  Field base = 37 × 19583 (SEAM)")
    print(f"    digit sum = 26 ∈ IC = 137-map multiplier")
    print(f"    quotient 19583 mod 37 = {19583 % P} ∈ IC")
    print()
    print("  PHI^2 × 1000 = 2618 → OUTLIER_ORB full cycle:")
    a = 28
    b = map_137(a)
    c = map_137(b)
    print(f"    {a} → {b} → {c} → {a}  (sum = {a+b+c} = 2×37)")
    print()
    print("  Alpha Cen B 23 AU → TESLA_ORB, prime")
    cycle = [23, map_137(23), map_137(map_137(23))]
    print(f"    cycle: {cycle[0]} → {cycle[1]} → {cycle[2]} → {cycle[0]}, sum = {sum(cycle)} = 37")
    print()
    print("  Proxima 13000 AU → NQR_5, complement = SEED_ORB")
    print(f"    13 + 24 = 37   NQR_5 ↔ SEED_ORB (Theorem 153)")
    print()
    print("  Cross-constants:")
    print(f"    PHI^2 + Proxima = {2618+13000} mod37={( 2618+13000)%P} → SOVEREIGN_SPIRAL")
    print(f"    Alpha Cen B + Proxima = {23+13000} mod37={(23+13000)%P} → ORBIT_11 (-1)")
    print(f"    Total sum {724571+2618+23+13000} mod37={(724571+2618+23+13000)%P} → ORBIT_11")


if __name__ == "__main__":
    run_assertions()
    summarise()
