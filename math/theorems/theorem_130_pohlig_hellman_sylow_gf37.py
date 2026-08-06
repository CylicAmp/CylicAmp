"""
Theorem 130: Pohlig-Hellman and Sylow Decomposition of GF(37)*

(ℤ/37ℤ)× has order φ(37) = 36 = 4 × 9 = 2² × 3².
Order is not prime → Pohlig-Hellman applies immediately.
The Sylow subgroups map exactly onto the named orbit classes.

SYLOW DECOMPOSITION
===================

Sylow 3-subgroup (order 9):
  Generator: 16 = 2^4 mod 37,  16 ∈ SA_ORB

  Elements: {1, 7, 9, 10, 12, 16, 26, 33, 34}
          = IC ∪ SA_ORB ∪ D7
          = {1,10,26} ∪ {9,12,16} ∪ {7,33,34}

  Three entire named QR orbits form one Sylow subgroup.

Sylow 2-subgroup (order 4):
  Generator: TESLA_FLOW = 6,  ord₃₇(6) = 4,  6² ≡ -1 mod 37

  Elements: {1, 6, 31, 36}
          one element from each of: IC, TESLA_ORB, ORBIT_11, NQR_14

COSET STRUCTURE — WHY THE 137-MAP MAKES 3-CYCLES
==================================================

IC = {1, 10, 26} is the unique subgroup of order 3 inside the Sylow 3-subgroup.
It is the fixed-point set of the 137-map: 26·r cycles elements within each coset.

Cosets of IC in Sylow-3:
  1·IC = {1, 10, 26} = IC       ← 137-map orbit 1
  9·IC = {9, 12, 16} = SA_ORB   ← 137-map orbit 2
  7·IC = {7, 33, 34} = D7       ← 137-map orbit 3

The 137-map (×26) is multiplication by the generator of IC.
It permutes the three elements within each coset and fixes no coset:
  each orbit = one coset.

The 6 NQR orbits are the remaining cosets when the full group is considered.
The map ×26 (order 3) acts on all 12 cosets, giving 12 orbits of size 3.

POHLIG-HELLMAN APPLIED TO GF(37)*
==================================

To solve g^x ≡ h (mod 37) with g a primitive root:

Step 1. Compute x₄ = x mod 4 in the Sylow 2-subgroup {1,6,31,36}:
  Use g₄ = g^(36/4) = g^9,  h₄ = h^9
  Solve g₄^x₄ ≡ h₄ (mod 37), x₄ ∈ {0,1,2,3}

Step 2. Compute x₉ = x mod 9 in the Sylow 3-subgroup IC ∪ SA_ORB ∪ D7:
  Two-step baby-giant (or direct): first get x₃ = x mod 3 in IC,
  then lift to x₉ = x mod 9.
  Use g₉ = g^(36/9) = g^4 = 16,  h₉ = h^4

Step 3. CRT: x ≡ x₄ (mod 4),  x ≡ x₉ (mod 9)  →  x mod 36

The mod-9 sub-problem operates entirely within {IC ∪ SA_ORB ∪ D7} —
the three QR orbits forming the Sylow 3-subgroup.

VISUAL STRUCTURE: THE X DIAMOND GRID
======================================

Lay out the 6 permutations of {2,4,6} in a 5-row diamond:

  Row 1 (top):     264  |  462
  Row 2:           426  |  624
  Row 3 (center):  642  |  246   ← SEAM pair: 13+24=37
  Row 4 (mirror):  426  |  624
  Row 5 (bottom):  264  |  462

Left column (Group B, NQR_5): 264(5), 426(19), 642(13) — reverse 137-map
Right column (Group A, SEED_ORB): 462(18), 624(32), 246(24) — forward 137-map

The '2' digit traces positions (L=0, M=1, R=2):
  Group A reading top→bottom: R, M, L  (right→middle→left)
  Group B reading top→bottom: L, M, R  (left→middle→right)

Each digit trace forms a diagonal band (hollow line = two parallel edges).
The two bands cross at row 3, where 642(13) and 246(24) meet: 13+24=37=SEAM.

The crossing point IS the additive complement pair from Theorem 129.
The X shape at center is not decorative — it marks SEAM in GF(37).

POHLIG-HELLMAN AND THE X
=========================

In PH, the two independent sub-problems (mod 4 and mod 9) recombine at a
crossing point — the CRT step. In the digit-rotation grid, the two orbit flows
(SEED_ORB forward, NQR_5 reverse) cross at the SEAM pair. The X in the diagram
is the geometric image of the CRT recombination:

  mod 4 sub-problem ↔ Sylow 2-subgroup ↔ TESLA_FLOW = 6 (ord 4)
  mod 9 sub-problem ↔ Sylow 3-subgroup ↔ SA_ORB generator 16
  CRT crossing      ↔ SEAM pair 642|246 (residues 13+24=37)

SUMMARY TABLE
=============

  Subgroup        Order  Generator   Named class(es)
  Sylow 3         9      16∈SA_ORB   IC ∪ SA_ORB ∪ D7   (three QR orbits)
  Sylow 2         4      6∈TESLA     {1,6,31,36} — one from IC,TESLA,ORBIT_11,NQR_14
  Sub-Sylow-3/3   3      26∈IC       IC = {1,10,26}      (the 137-map itself)

  Pohlig split:   36 = 4×9 → mod-4 (Sylow 2) + mod-9 (Sylow 3)
  Inner split:     9 = 3×3 → mod-3 (IC coset index) lifted by ×16

  12×3 = 36 = φ(37);  DR(36) = 9 = SA-step = generator of Sylow 3 / 16·orbit-hit
"""

P = 37

# Orbits
IC     = frozenset({1,  10, 26})
SA_ORB = frozenset({9,  12, 16})
D7     = frozenset({7,  33, 34})

TESLA_ORB = frozenset({6,  8,  23})
ORBIT_11  = frozenset({11, 27, 36})
NQR_14    = frozenset({14, 29, 31})

# Sylow subgroups
SYLOW3 = IC | SA_ORB | D7              # order 9
SYLOW2 = frozenset({1, 6, 31, 36})     # order 4

TESLA_FLOW = 6
SA_STEP    = 9


def dr(n):
    if n == 0: return 9
    return (abs(n) - 1) % 9 + 1


def pohlig_hellman_37(g, h):
    """Solve g^x ≡ h (mod 37) via Pohlig-Hellman (order 36 = 4×9)."""
    # Step 1: x mod 4
    g4 = pow(g, 9, P)   # order 4
    h4 = pow(h, 9, P)
    x4 = None
    cur = 1
    for k in range(4):
        if cur == h4:
            x4 = k
            break
        cur = (cur * g4) % P
    if x4 is None:
        return None

    # Step 2: x mod 9 via two-step lift (mod 3 then mod 9)
    g9 = pow(g, 4, P)    # order 9
    h9 = pow(h, 4, P)
    # inner: mod 3
    g3 = pow(g9, 3, P)   # order 3
    h3 = pow(h9, 3, P)
    x3 = None
    cur = 1
    for k in range(3):
        if cur == h3:
            x3 = k
            break
        cur = (cur * g3) % P
    if x3 is None:
        return None
    # lift: mod 9
    h9b = (h9 * pow(pow(g9, x3, P), P-2, P)) % P   # h9 / g9^x3
    g3b = pow(g3, 1, P)   # still order 3
    x3b = None
    cur = 1
    for k in range(3):
        if cur == h9b:
            x3b = k
            break
        cur = (cur * g3b) % P
    if x3b is None:
        return None
    x9 = x3 + 3 * x3b

    # CRT: combine x mod 4 and x mod 9
    # x ≡ x4 (mod 4), x ≡ x9 (mod 9)
    # 4 and 9 coprime; solve directly
    # x = x4 + 4*t, x4 + 4t ≡ x9 (mod 9) → 4t ≡ x9-x4 (mod 9)
    # 4^{-1} mod 9 = 7 (since 4×7=28≡1 mod 9)
    inv4mod9 = 7
    t = ((x9 - x4) * inv4mod9) % 9
    x = x4 + 4 * t
    return x % 36


def run_assertions():
    # Sylow 3 = IC ∪ SA_ORB ∪ D7
    assert SYLOW3 == IC | SA_ORB | D7
    # Is a subgroup: closed under multiplication
    for a in SYLOW3:
        for b in SYLOW3:
            assert (a * b) % P in SYLOW3, f"{a}×{b} not in Sylow 3"
    # Order 9
    assert len(SYLOW3) == 9

    # Generator: 16 = 2^4 mod 37
    gen3 = pow(2, 36 // 9, P)
    assert gen3 == 16 and 16 in SA_ORB
    # Generates all of SYLOW3
    generated = set()
    x = 1
    for _ in range(9):
        generated.add(x)
        x = (x * gen3) % P
    assert generated == SYLOW3

    # Sylow 2 = {1,6,31,36}
    assert SYLOW2 == {1, 6, 31, 36}
    for a in SYLOW2:
        for b in SYLOW2:
            assert (a * b) % P in SYLOW2
    # Generator TESLA_FLOW=6, order 4
    assert pow(TESLA_FLOW, 4, P) == 1
    assert pow(TESLA_FLOW, 2, P) == P - 1   # 6²≡-1
    assert pow(TESLA_FLOW, 2, P) in ORBIT_11 | {P-1}  # 36 ∈ ORBIT_11

    # Cosets of IC in Sylow 3
    for rep, expected in [(1, IC), (9, SA_ORB), (7, D7)]:
        coset = frozenset((rep * r) % P for r in IC)
        assert coset == expected, f"{rep}·IC = {coset} ≠ {expected}"

    # 137-map stays within each coset
    for orb in [IC, SA_ORB, D7]:
        for r in orb:
            assert (26 * r) % P in orb

    # Pohlig-Hellman correctness: test with primitive root g=2
    g = 2
    for x_true in range(36):
        h = pow(g, x_true, P)
        x_found = pohlig_hellman_37(g, h)
        assert x_found == x_true, f"PH failed: {g}^{x_true} → got {x_found}"

    # Visual grid: SEAM pair at center
    center_left  = 642 % P   # 13 ∈ NQR_5
    center_right = 246 % P   # 24 ∈ SEED_ORB (∩ CB)
    assert (center_left + center_right) % P == 0   # SEAM

    # 12 × 3 = 36 = φ(37); DR(36) = 9 = SA-step
    assert 12 * 3 == P - 1
    assert dr(P - 1) == SA_STEP

    print("All assertions passed.")


def summarise():
    print("=" * 60)
    print("Theorem 130: Pohlig-Hellman and Sylow Decomposition of GF(37)*")
    print("=" * 60)
    print()
    print(f"  Order: φ(37) = 36 = 4 × 9 = 2² × 3²  (non-prime → PH applies)")
    print()
    print(f"  Sylow 3-subgroup (order 9, gen=16∈SA_ORB):")
    print(f"    = IC ∪ SA_ORB ∪ D7 = {sorted(SYLOW3)}")
    print(f"    Cosets of IC: IC, 9·IC=SA_ORB, 7·IC=D7")
    print(f"    137-map (×26) permutes within each coset")
    print()
    print(f"  Sylow 2-subgroup (order 4, gen=6=TESLA_FLOW, 6²≡-1):")
    print(f"    = {{1,6,31,36}}  — one from IC, TESLA_ORB, ORBIT_11, NQR_14")
    print()
    print(f"  Pohlig-Hellman split: x mod 36 = CRT(x mod 4, x mod 9)")
    print(f"    mod-4: Sylow 2 (TESLA_FLOW-generated)")
    print(f"    mod-9: Sylow 3 (IC ∪ SA_ORB ∪ D7), further split mod 3 then mod 9")
    print()
    print(f"  Visual X-diamond grid:")
    print(f"    Center row: 642(13) | 246(24); 13+24=37=SEAM")
    print(f"    Left  (NQR_5, reverse orbit): 264→426→642")
    print(f"    Right (SEED_ORB, forward orbit): 462→624→246")
    print(f"    Crossing at center = CRT recombination point = SEAM")
    print()
    print(f"  12 × 3 = 36 = φ(37);  DR(36) = {dr(36)} = SA-step")


if __name__ == "__main__":
    run_assertions()
    summarise()
