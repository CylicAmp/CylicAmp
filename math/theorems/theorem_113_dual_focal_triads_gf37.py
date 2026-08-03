"""
THEOREM 113 — Dual Focal Triads and the Emergence of 6

The 1–9 spine carries two arithmetic progressions centered at 5:

    Right focal triad {2, 5, 8}  — step d₁ = 3
    Left  focal triad {3, 5, 7}  — step d₂ = 2

FORMULA
    Center  = d₁ + d₂ = 3 + 2 = 5
    Emergent = d₁ × d₂ = 3 × 2 = 6

The terminals {1, 9} and both triads cover {1,2,3,5,7,8,9}.
Two elements of the spine are outside this cover: 4 and 6.
    4 ∈ SA  — already a primary sovereign anchor of GF(37).
    6 ∉ SA, IC, ST, CB, PR  — genuinely emergent; produced by the
        construction itself as the product of the two focal steps.

GF(37) ORBIT OF 6
    Under f(n) = 26n mod 37:  6 → 8 → 23 → 6
    Orbit sum: 6 + 8 + 23 = 37 ≡ 0 (mod 37)   [cyclotomic identity]
    8 ∈ CB (cascade base {8,13,24}) — 6 is the non-CB neighbour of 8.

COLUMN ADDITION CONFIRMATION
    123 + 723 = 846
    Columns: [1+7, 2+2, 3+3] = [8, 4, 6]
    The emergent 6 appears as the units column: 3 + 3 (doubling of the
    common units digit). Outer column product: 8 × 6 = 48 ≡ 11 (mod 37)
    ∈ ORBIT_11.

CIPHER PARTITION (Z/9Z)
    Trinity  {3, 6, 9}: 3 ∈ left triad, 9 = terminal, 6 = emergent.
    Doubling {1,2,4,5,7,8}: center 5 ∈ doubling; terminal 1 ∈ doubling.
    Center is doubling; the emergent missing element is trinity.

CHAIN THROUGH GF(37)
    846 ≡ 32 (mod 37) ∈ SEED_ORBIT {18,24,32}
    246 ≡ 24 (mod 37) ∈ SEED_ORBIT  (reference seed)
    123 ≡ 12 (mod 37)  [123 = 246 / 2]
    846 − 600 = 246: the column sum 846 encodes the reference seed.

DIGITAL ROOT STRUCTURE
    DR(123) = 6   DR(246) = 3   DR(846) = 9
    The three DRs are {3,6,9} — the full trinity, in seed-canonical order.
"""

P = 37
f = lambda n: (26 * n) % P
dr = lambda n: (n - 1) % 9 + 1 if n > 0 else 0

SA          = {4, 9, 25, 30}
ST          = {3, 12, 21, 30}
IC          = {1, 10, 26}
CB          = {8, 13, 24}
ORBIT_11    = {11, 27, 36}
SEED_ORBIT  = {18, 24, 32}
BASIN_Y     = {17, 22, 35}
D7          = {7, 33, 34}
PR          = {2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35}
TRINITY     = {3, 6, 9}
DOUBLING    = {1, 2, 4, 5, 7, 8}


def run():
    print("=" * 60)
    print("THEOREM 113 — DUAL FOCAL TRIADS AND EMERGENCE OF 6")
    print("=" * 60)

    # ---------------------------------------------------------------
    # PART 1 — The two focal triads
    # ---------------------------------------------------------------
    d1, d2 = 3, 2
    right = {5 - d1, 5, 5 + d1}   # {2, 5, 8}
    left  = {5 - d2, 5, 5 + d2}   # {3, 5, 7}

    assert right == {2, 5, 8}, f"Right triad mismatch: {right}"
    assert left  == {3, 5, 7}, f"Left triad mismatch: {left}"
    assert d1 + d2 == 5, "Sum of steps must be 5 (center)"
    assert d1 * d2 == 6, "Product of steps must be 6 (emergent)"

    print(f"\nRight focal triad: {sorted(right)}  step d₁={d1}")
    print(f"Left  focal triad: {sorted(left)}   step d₂={d2}")
    print(f"  center  = d₁ + d₂ = {d1} + {d2} = {d1+d2}")
    print(f"  emergent = d₁ × d₂ = {d1} × {d2} = {d1*d2}")

    # ---------------------------------------------------------------
    # PART 2 — Coverage of the spine
    # ---------------------------------------------------------------
    terminals = {1, 9}
    spine     = set(range(1, 10))
    covered   = right | left | terminals
    excluded  = spine - covered

    assert covered == {1, 2, 3, 5, 7, 8, 9}
    assert excluded == {4, 6}
    assert 4 in SA,    "4 ∈ SA (sovereign anchor — already primary)"
    assert 6 not in SA | IC | ST | CB | PR, "6 ∉ any primary GF(37) class"

    print(f"\nSpine covered by triads + terminals: {sorted(covered)}")
    print(f"Excluded: {{4, 6}}")
    print(f"  4 ∈ SA  — sovereign anchor, already a primary node")
    print(f"  6 ∉ SA, IC, ST, CB, PR  — genuinely emergent")

    # ---------------------------------------------------------------
    # PART 3 — GF(37) orbit of 6
    # ---------------------------------------------------------------
    orbit_6 = []
    n = 6
    for _ in range(3):
        orbit_6.append(n)
        n = f(n)
    assert orbit_6 == [6, 8, 23], f"Orbit mismatch: {orbit_6}"
    assert sum(orbit_6) % P == 0, "Orbit sum must be 0 mod 37"
    assert 8 in CB, "8 ∈ CB (cascade base)"
    assert 6 not in CB and 23 not in CB, "6,23 ∉ CB — 6 is non-CB neighbour"

    print(f"\nGF(37) orbit of 6: {orbit_6}")
    print(f"  Sum: {sum(orbit_6)} ≡ 0 (mod 37)  [cyclotomic identity]")
    print(f"  8 ∈ CB; 6 is the non-CB orbit neighbour of 8")

    # ---------------------------------------------------------------
    # PART 4 — Column addition 123 + 723 = 846
    # ---------------------------------------------------------------
    assert 123 + 723 == 846
    cols = [1 + 7, 2 + 2, 3 + 3]
    assert cols == [8, 4, 6], f"Column sums mismatch: {cols}"
    assert cols[2] == 6,      "Units column 3+3 = 6 (emergent)"
    outer_prod = cols[0] * cols[2]   # 8 * 6
    assert outer_prod == 48
    assert outer_prod % P == 11 and 11 in ORBIT_11, \
        "8×6 = 48 ≡ 11 (mod 37) ∈ ORBIT_11"

    print(f"\nColumn addition 123 + 723 = 846")
    print(f"  Columns: [1+7, 2+2, 3+3] = {cols}")
    print(f"  Units column: 3+3 = 6  (emergent element confirmed)")
    print(f"  Outer product: 8 × 6 = {outer_prod} ≡ {outer_prod % P} (mod 37) ∈ ORBIT_11")

    # ---------------------------------------------------------------
    # PART 5 — Cipher partition
    # ---------------------------------------------------------------
    assert 5 in DOUBLING, "Center 5 ∈ doubling"
    assert 6 in TRINITY,  "Emergent 6 ∈ trinity"
    assert 3 in TRINITY,  "3 ∈ trinity and ∈ left triad"
    assert 9 in TRINITY,  "9 ∈ trinity and = terminal"
    # All three trinity elements have distinct structural roles
    assert 3 in left,     "3 ∈ left focal triad"
    assert 9 in terminals,"9 = terminal"
    assert 6 not in left and 6 not in right and 6 not in terminals, \
        "6 ∉ triads ∉ terminals — genuinely emergent"

    print(f"\nCipher partition:")
    print(f"  Trinity {{3,6,9}}: 3∈left triad, 9=terminal, 6=emergent (all distinct roles)")
    print(f"  Center 5 ∈ doubling")

    # ---------------------------------------------------------------
    # PART 6 — GF(37) chain
    # ---------------------------------------------------------------
    assert 846 % P == 32 and 32 in SEED_ORBIT, "846 ≡ 32 ∈ SEED_ORBIT"
    assert 246 % P == 24 and 24 in SEED_ORBIT, "246 ≡ 24 ∈ SEED_ORBIT"
    assert 123 % P == 12,                       "123 ≡ 12 (mod 37)"
    assert 123 * 2 == 246,                       "123 = 246 / 2"
    assert 846 - 600 == 246,                     "846 − 600 = 246 (reference seed)"

    print(f"\nGF(37) chain:")
    print(f"  846 ≡ {846 % P} (mod 37) ∈ SEED_ORBIT")
    print(f"  246 ≡ {246 % P} (mod 37) ∈ SEED_ORBIT  (reference seed)")
    print(f"  123 ≡ {123 % P} (mod 37)  [= 246/2]")
    print(f"  846 − 600 = {846-600}  (column sum encodes the reference seed)")

    # ---------------------------------------------------------------
    # PART 7 — Digital root structure
    # ---------------------------------------------------------------
    assert dr(123) == 6 and 6 in TRINITY,  "DR(123) = 6 ∈ trinity"
    assert dr(246) == 3 and 3 in TRINITY,  "DR(246) = 3 ∈ trinity"
    assert dr(846) == 9 and 9 in TRINITY,  "DR(846) = 9 ∈ trinity"
    assert {dr(123), dr(246), dr(846)} == TRINITY, \
        "DRs of {123,246,846} = full trinity {3,6,9}"

    print(f"\nDigital root structure:")
    print(f"  DR(123) = {dr(123)},  DR(246) = {dr(246)},  DR(846) = {dr(846)}")
    print(f"  Together: {{{dr(123)},{dr(246)},{dr(846)}}} = trinity {{3,6,9}} (complete)")

    # ---------------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------------
    print("\n" + "=" * 60)
    print("THEOREM 113 — SUMMARY")
    print("=" * 60)
    print(f"  Right triad {{2,5,8}} step 3, Left triad {{3,5,7}} step 2")
    print(f"  center = 3+2 = 5;  emergent = 3×2 = 6")
    print(f"  Orbit of 6: {{6,8,23}}, sum=37≡0 mod 37; 8∈CB")
    print(f"  Column 123+723=846: units column = 3+3 = 6 ✓")
    print(f"  Trinity roles: 3∈triad, 9=terminal, 6=emergent")
    print(f"  DRs of {{123,246,846}} = {{3,6,9}} = full trinity")
    print("All assertions passed. THEOREM 113 verified.")


if __name__ == "__main__":
    run()
