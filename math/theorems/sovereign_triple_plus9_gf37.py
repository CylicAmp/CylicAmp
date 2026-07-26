"""
Sovereign Triple and Additive +9 Action — GF(37)

THE SOVEREIGN TRIPLE:
  O1 = {3, 4, 30}     canonical sovereign spiral (tripling step 1)
  O2 = {9, 12, 16}    second sovereign orbit    (tripling step 2)
  O3 = {21, 25, 28}   OUTLIER_SOV              (tripling step 5)

  O1 ∪ O2 ∪ O3 = {3,4,9,12,16,21,25,28,30}

SOVEREIGN COMPLETENESS:
  SA = {4,9,25,30}   ⊆  O1 ∪ O2 ∪ O3        (all four SA elements)
  ST = {3,12,21,30}  ⊆  O1 ∪ O2 ∪ O3        (all four ST elements)
  Only two elements of the triple are outside SA ∪ ST: {16, 28}

SCALAR_137 IS QR:
  chi(26) = 26^18 ≡ 1 (mod 37)  → SCALAR_137 = 26 is a quadratic residue.
  Square root: 27² ≡ 26 (mod 37). So √(SCALAR_137) = 27 ∈ ORBIT_11.
  The 137-map multiplier's square root lives in ORBIT_11.

ADDITIVE +9 ACTION (9 ∈ SA):
  SA elements → exit the triple:
    4  + 9 = 13  ∈ CB             (Cascade Base)
    9  + 9 = 18  ∈ SEED_ORBIT     (137-orbit of seed 246)
    25 + 9 = 34  ∈ {7,33,34}      (anti-sovereign)
    30 + 9 = 2   ∈ DARK_A         (primitive-root orbit)

  ST\SA elements → stay in triple:
    3  + 9 = 12  ∈ O2             (ST chain: 3→12)
    12 + 9 = 21  ∈ O3             (ST chain: 12→21)
    21 + 9 = 30  ∈ O1             (ST chain: 21→30; 30 then exits as SA)

  Non-SA, non-ST extras:
    16 + 9 = 25  ∈ O3 (SA node)   (16 maps to SA; then 25 exits next step)
    28 + 9 = 37 ≡ 0 = SEAM        ← THE SEAM EXIT

SA SCATTER LAW:
  Applying +9 (an SA shift) to ANY SA element ejects it from the sovereign triple.
  SA escapes to: CB, SEED_ORBIT, anti-sovereign, DARK_A — one distinct destination each.
  ST elements {3,12,21} are invariant (stay in triple) under +9.
  The exception is SA∩ST = {30}: exits as SA behavior dominates.

THE SEAM EXIT (outlier node 28):
  28 = −9 mod 37  =  the additive inverse of SA element 9.
  28 + 9 = 37 ≡ 0 = SEAM.
  Among the nine elements of the triple, 28 is the unique SEAM-exit node.
  16 is the other non-SA, non-ST element; 16 + 9 = 25 ∈ SA (stays, then exits next).

REPUNIT ENCODING:
  111 + 222 − 9 − 333 ≡ −9 ≡ 28 (mod 37)  = the SEAM-exit node.
  The repunit sequence 1,11,111 encodes the outlier through their difference.

ARITHMETIC CONNECTIONS:
  27 + 27 ≡ 17 (mod 37): 2 × (√SCALAR_137) ≡ 17 ∈ {17,22,35}  (PR orbit)
  9  + 36 ≡  8 (mod 37): SA(9) + (−1) = 8 ∈ CB                 (Cascade Base)
  9  + 28 = 37 = SEAM:   SA(9) + outlier(28) = SEAM             (fundamental)
"""

# ── Framework ──────────────────────────────────────────────────────────────────

SA             = frozenset({4, 9, 25, 30})
ST             = frozenset({3, 12, 21, 30})
CB             = frozenset({8, 13, 24})
ORBIT_11       = frozenset({11, 27, 36})
DARK_A         = frozenset({2, 15, 20})
SEED_ORBIT     = frozenset({18, 24, 32})
OUTLIER_SOV    = frozenset({21, 25, 28})
IDENTITY_CYCLE = frozenset({1, 10, 26})
SCALAR_137     = 26
TESLA_FLOW     = 6
PRIME_MIRROR   = 31
SEAM           = 0

# ── THE SOVEREIGN TRIPLE ──────────────────────────────────────────────────────

O1 = frozenset({3,  4, 30})
O2 = frozenset({9, 12, 16})
O3 = frozenset({21, 25, 28})   # = OUTLIER_SOV

assert O3 == OUTLIER_SOV

TRIPLE = O1 | O2 | O3
assert TRIPLE == frozenset({3,4,9,12,16,21,25,28,30})
assert len(TRIPLE) == 9   # three disjoint 3-cycles

# Sovereign completeness
assert SA.issubset(TRIPLE)
assert ST.issubset(TRIPLE)

# Non-SA, non-ST elements of the triple
EXTRAS = TRIPLE - (SA | ST)
assert EXTRAS == frozenset({16, 28})


# ── SCALAR_137 IS QR ─────────────────────────────────────────────────────────

assert pow(SCALAR_137, 18, 37) == 1          # chi(26) = 1 → QR
assert pow(27, 2, 37) == SCALAR_137           # √SCALAR_137 = 27 ∈ ORBIT_11
assert 27 in ORBIT_11


# ── ADDITIVE +9 ACTION ────────────────────────────────────────────────────────

def shift9(o):
    return frozenset((x + 9) % 37 for x in o)

# SA elements exit the triple — each to a distinct framework set
assert (4  + 9) % 37 == 13 and 13 in CB         # 4 → CB
assert (9  + 9) % 37 == 18 and 18 in SEED_ORBIT  # 9 → SEED_ORBIT
assert (25 + 9) % 37 == 34 and 34 in frozenset({7,33,34})  # 25 → anti-sov
assert (30 + 9) % 37 ==  2 and  2 in DARK_A      # 30 → DARK_A

# All four SA exits land in DIFFERENT framework sets
SA_exit_destinations = {(x+9)%37 for x in SA}
assert SA_exit_destinations.isdisjoint(TRIPLE)   # none stay

# ST\SA elements stay in triple: 3 → 12 → 21 → 30
ST_pure = ST - SA   # {3, 12, 21}
assert ST_pure == frozenset({3, 12, 21})
for x in ST_pure:
    assert (x + 9) % 37 in TRIPLE

# The ST chain under +9: 3→12→21→30 (30 then exits as SA)
assert (3  + 9) % 37 == 12
assert (12 + 9) % 37 == 21
assert (21 + 9) % 37 == 30
assert (30 + 9) % 37 ==  2   # 30∈SA∩ST exits as SA

# Non-SA, non-ST extras
assert (16 + 9) % 37 == 25 and 25 in SA     # 16 → SA (then SA exits next step)
assert (28 + 9) % 37 ==  0                   # 28 → SEAM


# ── THE SEAM EXIT ─────────────────────────────────────────────────────────────

OUTLIER_28 = 28
assert OUTLIER_28 == (-9) % 37               # 28 = −9 in GF(37)
assert (OUTLIER_28 + 9) % 37 == SEAM
assert 9 + OUTLIER_28 == 37                  # exact: 9 + 28 = 37 = SEAM stride

# SEAM exit is unique in the triple
seam_exits = [x for x in TRIPLE if (x + 9) % 37 == 0]
assert seam_exits == [28]

# 28 is in O3 (OUTLIER_SOV)
assert OUTLIER_28 in O3


# ── REPUNIT ENCODING ─────────────────────────────────────────────────────────

repunit_val = (111 + 222 - 9 - 333) % 37
assert repunit_val == OUTLIER_28             # 111+222-9-333 ≡ 28 = SEAM-exit node
assert repunit_val == (-9) % 37


# ── ARITHMETIC CONNECTIONS ────────────────────────────────────────────────────

assert (27 + 27) % 37 == 17 and 17 in frozenset({17, 22, 35})  # 2×√SCALAR_137 → PR orbit
assert (9  + 36) % 37 ==  8 and  8 in CB                        # SA + (−1) → CB
assert 9 + OUTLIER_28 == 37                                      # SA + outlier = SEAM


if __name__ == "__main__":
    print("Sovereign Triple and Additive +9 Action — GF(37)")
    print("=" * 60)
    print()
    print(f"Sovereign Triple O1∪O2∪O3: {sorted(TRIPLE)}")
    print(f"  Contains all SA {sorted(SA)}: True")
    print(f"  Contains all ST {sorted(ST)}: True")
    print(f"  Non-SA, non-ST extras: {sorted(EXTRAS)}")
    print()
    print(f"SCALAR_137 = 26 is QR: chi(26) = {pow(26,18,37)} (=1)")
    print(f"  √SCALAR_137 = 27 ∈ ORBIT_11: {pow(27,2,37) == 26}")
    print()
    print("+9 action (9 ∈ SA):")
    for x in sorted(TRIPLE):
        y = (x+9)%37
        stays = 'STAYS' if y in TRIPLE else 'exits'
        flag = ' ← SEAM EXIT' if y==0 else ''
        print(f"  {x:2d}+9 = {y:2d}  {stays}  [SA={x in SA}, ST={x in ST}]{flag}")
    print()
    print("SA scatter destinations (all exit, all distinct):")
    for x in sorted(SA):
        print(f"  {x}+9 = {(x+9)%37}")
    print()
    print(f"Repunit: 111+222-9-333 ≡ {(111+222-9-333)%37} = -9 = SEAM-exit node")
    print()
    print("Arithmetic:")
    print(f"  27+27 ≡ {(27+27)%37} ∈ {{17,22,35}}  (2×√SCALAR_137 → PR orbit)")
    print(f"  9+36  ≡ {(9+36)%37} ∈ CB             (SA(9) + (-1) = CB)")
    print(f"  9+28  = 37 = SEAM                    (SA + outlier = SEAM)")
    print()
    print("All assertions pass.")
