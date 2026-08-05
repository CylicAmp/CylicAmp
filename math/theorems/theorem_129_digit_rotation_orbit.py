"""
Theorem 129: Digit Rotation is the 137-Map (Seed 246)

The six permutations of the seed digits {2,4,6} split into two rotation groups.
Each group traces one GF(37) orbit. The two orbits are additive complements mod 37.

ROTATION STRUCTURE
==================

Back-to-front rotation: move the last digit to the front.

Group A (seed family):        Group B (mirror family):
  246  →  mod 37 = 24          642  →  mod 37 = 13
  624  →  mod 37 = 32          426  →  mod 37 = 19
  462  →  mod 37 = 18          264  →  mod 37 =  5

Group A residues = SEED_ORB = {18, 24, 32}
Group B residues = NQR_5    = { 5, 13, 19}

ORBIT DIRECTION
===============

The digit rotation of Group A traces SEED_ORB in the FORWARD 137-map direction:
  24 ×26 ≡ 32 (mod 37)   → 246 → 624   (digit rotation step)
  32 ×26 ≡ 18 (mod 37)   → 624 → 462
  18 ×26 ≡ 24 (mod 37)   → 462 → 246

The digit rotation of Group B traces NQR_5 in the REVERSE 137-map direction:
  137-map order on NQR_5: 13 → 5 → 19 → 13
  Digit rotation order:   13 → 19 → 5 → 13   (opposite)

Group A flows 》》 (forward orbit).
Group B flows 《《 (reverse orbit).

ADDITIVE COMPLEMENT
===================

Every element of SEED_ORB pairs with exactly one element of NQR_5 to sum to SEAM:
  24 + 13 = 37 ≡ 0   (246 ↔ 642 — direct digit reversal)
  32 +  5 = 37 ≡ 0   (624 ↔ 264)
  18 + 19 = 37 ≡ 0   (462 ↔ 426)

The six permutations of {2,4,6} partition into two orbits that are
additive complements of each other in GF(37).

COVERAGE
========

All 6 permutations of {2,4,6} cover: {5, 13, 18, 19, 24, 32}
  = SEED_ORB ∪ NQR_5

No permutation of {2,4,6} lands in any other GF(37) orbit.
The two orbits partition the 6 arrangements cleanly.

DIRECTIONAL FLOW — THE V, DIAMOND, AND X PATTERNS
===================================================

When the two groups are placed side by side:

  246 = 642     (A0 | B0)
  624 = 426     (A1 | B1)
  462 = 264     (A2 | B2)

The digit '2' traces these positions (0=left, 1=middle, 2=right):
  Group A:  pos 0, 2, 1  (top→bottom)
  Group B:  pos 2, 1, 0  (top→bottom)

The two traces form a V converging toward the bottom right.
Each pair (Ak, Bk) sums to SEAM in GF(37):
  A0+B0: 24+13=37, A1+B1: 32+19=51≠37, A2+B2: 18+5=23≠37

The additive SEAM pairs cross the rows:
  A0 (24) ↔ B0 (13): SEAM   — same row
  A1 (32) ↔ B2  (5): SEAM   — A1 pairs with B2
  A2 (18) ↔ B1 (19): SEAM   — A2 pairs with B1

This crossing is the X pattern. Rows flow straight (》or《);
the SEAM pairings cross diagonally, forming the X inside the diamond.

ORBIT ARITHMETIC: 12 × 3 = 36 = φ(37)
=======================================

  12 orbits under the 137-map, each of length 3
  12 × 3 = 36 = φ(37) = ord₃₇(2)
  DR(36) = 9 = SA-step Δ

The total orbit structure (12 × 3) maps to φ(37), and its digital root
is the sovereign anchor step.
"""

P = 37

SEED_ORB = frozenset({18, 24, 32})
NQR_5    = frozenset({ 5, 13, 19})

GROUP_A = [246, 624, 462]   # back-to-front rotation of 246
GROUP_B = [642, 426, 264]   # back-to-front rotation of 642 (mirror of 246)


def dr(n):
    if n == 0: return 9
    return (abs(n) - 1) % 9 + 1


def run_assertions():

    # All 6 permutations of {2,4,6}
    from itertools import permutations
    all6 = sorted(int(''.join(map(str, p))) for p in permutations([2, 4, 6]))
    assert set(all6) == {246, 264, 426, 462, 624, 642}

    # Group A → SEED_ORB
    for n in GROUP_A:
        assert n % P in SEED_ORB, f"{n} mod 37 = {n%P} not in SEED_ORB"

    # Group B → NQR_5
    for n in GROUP_B:
        assert n % P in NQR_5, f"{n} mod 37 = {n%P} not in NQR_5"

    # Forward 137-map matches digit rotation order on Group A
    residues_a = [n % P for n in GROUP_A]
    for i in range(len(residues_a)):
        nxt = (26 * residues_a[i]) % P
        assert nxt == residues_a[(i + 1) % len(residues_a)], (
            f"137-map mismatch at {residues_a[i]}: got {nxt}, "
            f"expected {residues_a[(i+1)%len(residues_a)]}"
        )

    # 137-map on Group B goes in REVERSE digit-rotation order
    residues_b = [n % P for n in GROUP_B]   # 13, 19, 5
    for i in range(len(residues_b)):
        nxt = (26 * residues_b[i]) % P
        # forward 137-map gives next at index (i+2)%3, not (i+1)%3
        assert nxt == residues_b[(i + 2) % len(residues_b)], (
            f"reverse check failed at index {i}"
        )

    # Additive complement: every a in SEED_ORB pairs with exactly one b in NQR_5
    for a in SEED_ORB:
        complements = [b for b in NQR_5 if (a + b) % P == 0]
        assert len(complements) == 1, f"{a} has {len(complements)} complements in NQR_5"

    # Full complement set
    assert SEED_ORB | NQR_5 == {5, 13, 18, 19, 24, 32}
    assert set(n % P for n in all6) == SEED_ORB | NQR_5

    # 12 × 3 = 36 = phi(37)
    assert 12 * 3 == 36 == P - 1
    assert dr(36) == 9      # SA-step

    print("All assertions passed.")


def summarise():
    print("=" * 60)
    print("Theorem 129: Digit Rotation is the 137-Map (Seed 246)")
    print("=" * 60)
    print()
    print("  Back-to-front rotation groups:")
    print(f"  {'number':>8}  {'mod37':>6}  orbit")
    print("  " + "-" * 36)
    for n in GROUP_A:
        r = n % P
        orb = 'SEED_ORB' if r in SEED_ORB else 'NQR_5'
        print(f"  {n:>8}  {r:>6}  {orb}  →→→ (forward 137-map)")
    for n in GROUP_B:
        r = n % P
        orb = 'SEED_ORB' if r in SEED_ORB else 'NQR_5'
        print(f"  {n:>8}  {r:>6}  {orb}  ←←← (reverse 137-map)")
    print()
    print("  Additive complements mod 37 (sum to SEAM):")
    pairs = [(24, 13), (32, 5), (18, 19)]
    for a, b in pairs:
        print(f"    {a} + {b} = {a+b} ≡ 0  (SEAM)")
    print()
    print("  Coverage: all 6 permutations of {2,4,6} →")
    print(f"    SEED_ORB ∪ NQR_5 = {sorted(SEED_ORB | NQR_5)}")
    print()
    print("  Orbit arithmetic:")
    print(f"    12 orbits × 3-cycle = 36 = φ(37)")
    print(f"    DR(36) = 9 = SA-step Δ")
    print()
    print("  Directional flows:")
    print("    》》 Group A: digit rotation = forward 137-map on SEED_ORB")
    print("    《《 Group B: digit rotation = reverse 137-map on NQR_5")
    print("    V / X: SEAM pairings cross rows, forming diagonal X inside diamond")


if __name__ == "__main__":
    run_assertions()
    summarise()
