"""
master_matrix_audit.py

The master matrix of number strings and their prime architecture.

─────────────────────────────────────────────────────────────────
STRINGS:
  Blueprint:  "101112132527210111213"   digit_sum=38  DR=2
  8-pair A:   "312111012725"             digit_sum=26  DR=8
  8-pair B:   "527210111213"             digit_sum=26  DR=8
  7-pair C:   "413223144343"             digit_sum=34  DR=7
  7-pair D:   "343441322314"             digit_sum=34  DR=7

REVERSAL STRUCTURE:
  B = reverse(A)  — digit sum invariant under reversal
  D = reverse(C)  — digit sum invariant under reversal

GRID (4 rows × 2 columns, repeated):
  Row 1: A(DR=8)  C(DR=7)    cross-sum 8+7=15 → DR=6
  Row 2: B(DR=8)  D(DR=7)    cross-sum 8+7=15 → DR=6
  Row 3: A(DR=8)  C(DR=7)    cross-sum 8+7=15 → DR=6
  Row 4: B(DR=8)  D(DR=7)    cross-sum 8+7=15 → DR=6

  8-block: 4×8=32 → DR=5
  7-block: 4×7=28 → DR=1
  Combined: 5+1=6

  Cross-add:  8+7=15 → DR=6   (same as combined total)
  Cross-mult: 8×7=56 → DR=2   (= blueprint DR = first prime)

─────────────────────────────────────────────────────────────────
PRIME ARCHITECTURE:

  (M1) DR DOUBLING CYCLE (dr_algebra.py):
       1→2→4→8→7→5→1  (period 6)
       8 and 7 are consecutive: position 4 and 5 in the cycle.
       The matrix pair (DR=8, DR=7) is one step in the DR orbit.

  (M2) ALPHA GRID POSITIONS (alpha_grid.py):
       Grid: 1 2 3 4 (5) 6 7 8 9
       AHL = 8  (RH-E, Right High Even)
       ALO = 7  (RL-O, Right Low Odd)
       The matrix 8-block = AHL; 7-block = ALO.
       Primes in grid: 2(LL-E), 3(LH-O), 5(center), 7(RL-O=ALO).
       7 is the 4th prime AND the ALO position.

  (M3) REPUNIT 2n-1 SEQUENCE (repunit_sequence.py):
       n=4:  2×4−1 = 7   → DR = 7 = ALO  (4th prime IS the value)
       n=9:  2×9−1 = 17  → DR = 8 = AHL  (7th prime DR = AHL)

  (M4) DIGIT SUM PRIME DECOMPOSITIONS:
       8-pair digit_sum = 26 = 2×13  (13 = 6th prime)
       7-pair digit_sum = 34 = 2×17  (17 = 7th prime; criss-cross prime;
                                       slot_diff(191→100) in Z/37Z;
                                       F(9)=34=2×17)
       DR(26) = 8 = AHL  |  DR(34) = 7 = ALO
       The digit sums of each block have the same DR as the block itself.

  (M5) 137 = 3×37 + 2×13 (one_over_137_framework.md):
       3×37 = 111 = repunit_3 (framework repunit)
       2×13 = 26  = digit_sum of 8-pair
       137 = 111 + 26 = repunit + 8-pair digit_sum
       137 mod 37 = 26 (slot 26, same as 100, 248, 359, 582739)

  (M6) MODAL CROSSING (modal_crossing_orbit.py):
       191 mod 37 = 6  → ORBIT_V (inner ring, step 12/18)
       100 mod 37 = 26 → ORBIT_P (outer ring)
       slot_diff = (6−26) mod 37 = 17 (7th prime)
       26 = 8-pair digit_sum = slot of 137 in Z/37Z
       The descent 191→100 connects inner ring (slot of 191) to
       outer ring (slot = 8-pair digit_sum = 2×13th_prime).

  (M7) FULL PRIME CHAIN:
       7 (4th prime) → ALO → 7-pair DR → digit_sum 34=2×17
       17 (7th prime) → slot_diff(191→100) → DR=8 → AHL
       8 (AHL) → 8-pair DR → digit_sum 26=2×13
       13 (6th prime) → 137=3×37+2×13 → 33rd prime
       2 (1st prime) → 8×7 DR → blueprint DR = foundation
       6 → grid combined total → equal-digit DR-6 cluster {6,33,222,111111}
─────────────────────────────────────────────────────────────────
"""

from sympy import isprime

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = n % 9
    return r if r else 9


def collapse(s):
    total = sum(int(c) for c in s if c.isdigit())
    while total >= 10:
        total = sum(int(c) for c in str(total))
    return total


def digit_sum(s):
    return sum(int(c) for c in s if c.isdigit())


# ── String definitions ────────────────────────────────────────────────────────

BLUEPRINT = "101112132527210111213"
A = "312111012725"    # 8-pair forward
B = "527210111213"    # 8-pair reverse
C = "413223144343"    # 7-pair forward
D = "343441322314"    # 7-pair reverse


# ── Collapse verification ─────────────────────────────────────────────────────

check(collapse(BLUEPRINT) == 2, "blueprint DR = 2", collapse(BLUEPRINT), 2)
check(collapse(A) == 8, "A DR = 8", collapse(A), 8)
check(collapse(B) == 8, "B DR = 8", collapse(B), 8)
check(collapse(C) == 7, "C DR = 7", collapse(C), 7)
check(collapse(D) == 7, "D DR = 7", collapse(D), 7)

check(digit_sum(BLUEPRINT) == 38, "blueprint digit_sum = 38", digit_sum(BLUEPRINT), 38)
check(digit_sum(A) == 26, "A digit_sum = 26", digit_sum(A), 26)
check(digit_sum(B) == 26, "B digit_sum = 26", digit_sum(B), 26)
check(digit_sum(C) == 34, "C digit_sum = 34", digit_sum(C), 34)
check(digit_sum(D) == 34, "D digit_sum = 34", digit_sum(D), 34)


# ── Reversal structure ────────────────────────────────────────────────────────

check(A[::-1] == B, "B = reverse(A)", A[::-1], B)
check(C[::-1] == D, "D = reverse(C)", C[::-1], D)


# ── Grid structure ────────────────────────────────────────────────────────────

block8 = 4 * 8
block7 = 4 * 7
check(dr(block8) == 5, "4×8=32 → DR=5", dr(block8), 5)
check(dr(block7) == 1, "4×7=28 → DR=1", dr(block7), 1)
check(dr(dr(block8) + dr(block7)) == 6, "5+1=6 → DR=6", dr(dr(block8) + dr(block7)), 6)

# Cross-add (horizontal)
check(dr(8 + 7) == 6, "8+7=15 → DR=6 (all rows)", dr(8 + 7), 6)

# Cross-multiply
check(dr(8 * 7) == 2, "8×7=56 → DR=2 (blueprint)", dr(8 * 7), 2)
check(dr(8 * 7) == collapse(BLUEPRINT), "8×7 DR = blueprint DR", dr(8 * 7), collapse(BLUEPRINT))

# Bridge: 8+8=16 → DR=7 (leaps to 7-pair root)
check(dr(8 + 8) == 7, "8+8=16 → DR=7 (mirror pair root)", dr(8 + 8), 7)
check(dr(8 + 8 + 7 + 7) == 3, "8+8+7+7=30 → DR=3", dr(8 + 8 + 7 + 7), 3)


# ── M1: DR doubling cycle ─────────────────────────────────────────────────────

DOUBLING_CYCLE = [1, 2, 4, 8, 7, 5]
for i in range(len(DOUBLING_CYCLE)):
    nxt = DOUBLING_CYCLE[(i + 1) % 6]
    check(dr(DOUBLING_CYCLE[i] * 2) == nxt,
          f"DR(2×{DOUBLING_CYCLE[i]}) = {nxt}", dr(DOUBLING_CYCLE[i] * 2), nxt)

check(DOUBLING_CYCLE.index(8) == 3, "8 at position 3 in cycle", DOUBLING_CYCLE.index(8), 3)
check(DOUBLING_CYCLE.index(7) == 4, "7 at position 4 in cycle", DOUBLING_CYCLE.index(7), 4)
# 8 and 7 are consecutive
check(DOUBLING_CYCLE.index(7) == DOUBLING_CYCLE.index(8) + 1,
      "7 immediately follows 8 in doubling cycle", True, True)


# ── M2: Alpha grid ────────────────────────────────────────────────────────────

AHL = 8   # Right High Even (alpha_grid.py)
ALO = 7   # Right Low Odd  (alpha_grid.py)
check(AHL == 8, "AHL = 8", AHL, 8)
check(ALO == 7, "ALO = 7", ALO, 7)
check(collapse(A) == AHL, "8-pair DR = AHL", collapse(A), AHL)
check(collapse(C) == ALO, "7-pair DR = ALO", collapse(C), ALO)

# Primes in grid 1-9
grid_primes = [p for p in range(1, 10) if isprime(p)]
check(grid_primes == [2, 3, 5, 7], "primes in grid = [2,3,5,7]", grid_primes, [2, 3, 5, 7])
check(7 in grid_primes, "7 is prime and = ALO", 7 in grid_primes, True)
check(7 == ALO, "7 = ALO position", 7, ALO)


# ── M3: Repunit 2n-1 sequence ─────────────────────────────────────────────────

check(2 * 4 - 1 == 7, "2×4-1 = 7 = ALO (n=4)", 2 * 4 - 1, 7)
check(dr(2 * 4 - 1) == 7, "DR(7) = 7 = ALO", dr(2 * 4 - 1), 7)
check(2 * 9 - 1 == 17, "2×9-1 = 17 (n=9)", 2 * 9 - 1, 17)
check(dr(2 * 9 - 1) == 8, "DR(17) = 8 = AHL", dr(2 * 9 - 1), 8)


# ── M4: Digit sum prime decompositions ───────────────────────────────────────

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

# 26 = 2×13 (13 = 6th prime)
check(digit_sum(A) == 2 * 13, "8-pair digit_sum = 2×13", digit_sum(A), 2 * 13)
check(isprime(13), "13 is prime", isprime(13), True)
check(PRIMES.index(13) + 1 == 6, "13 = 6th prime", PRIMES.index(13) + 1, 6)
check(dr(26) == 8, "DR(26) = 8 = AHL", dr(26), 8)

# 34 = 2×17 (17 = 7th prime)
check(digit_sum(C) == 2 * 17, "7-pair digit_sum = 2×17", digit_sum(C), 2 * 17)
check(isprime(17), "17 is prime", isprime(17), True)
check(PRIMES.index(17) + 1 == 7, "17 = 7th prime", PRIMES.index(17) + 1, 7)
check(dr(34) == 7, "DR(34) = 7 = ALO", dr(34), 7)

# DR of digit sum matches DR of string
check(dr(digit_sum(A)) == collapse(A), "DR(digit_sum(A)) = collapse(A)", dr(digit_sum(A)), collapse(A))
check(dr(digit_sum(C)) == collapse(C), "DR(digit_sum(C)) = collapse(C)", dr(digit_sum(C)), collapse(C))


# ── M5: 137 = 3×37 + 2×13 ────────────────────────────────────────────────────

from sympy import factorint
check(3 * 37 + 2 * 13 == 137, "3×37 + 2×13 = 137", 3 * 37 + 2 * 13, 137)
check(3 * 37 == 111, "3×37 = 111 = repunit_3", 3 * 37, 111)
check(2 * 13 == 26, "2×13 = 26 = 8-pair digit_sum", 2 * 13, 26)
check(137 == 111 + digit_sum(A), "137 = repunit_3 + 8-pair digit_sum",
      137, 111 + digit_sum(A))
check(137 % 37 == 26, "137 mod 37 = 26 = 8-pair digit_sum", 137 % 37, 26)
check(isprime(137), "137 is prime", isprime(137), True)


# ── M6: Modal crossing (191→100) ─────────────────────────────────────────────

ORBIT_V = [2, 7, 22, 30, 17, 15, 9, 28, 11, 34, 29, 14, 6, 19, 21, 27, 8, 25]
ORBIT_P = [0, 1, 4, 13, 3, 10, 31, 20, 24, 36, 35, 32, 23, 33, 26, 5, 16, 12]

check(191 % 37 == 6, "191 mod 37 = 6 (ORBIT_V slot)", 191 % 37, 6)
check(6 in ORBIT_V, "slot 6 is in ORBIT_V (inner ring)", 6 in ORBIT_V, True)
check(100 % 37 == 26, "100 mod 37 = 26 (ORBIT_P slot)", 100 % 37, 26)
check(26 in ORBIT_P, "slot 26 is in ORBIT_P (outer ring)", 26 in ORBIT_P, True)
check((6 - 26) % 37 == 17, "slot_diff(191→100) = 17 = 7th prime", (6 - 26) % 37, 17)
check(100 % 37 == digit_sum(A), "slot of 100 = 8-pair digit_sum", 100 % 37, digit_sum(A))


# ── M7: Full prime chain summary checks ──────────────────────────────────────

check(dr(8 * 7) == 2, "8×7 → DR=2 = first prime", dr(8 * 7), 2)
check(PRIMES[0] == 2, "first prime = 2 = blueprint DR", PRIMES[0], 2)
check(dr(8 + 7) == 6, "8+7 → DR=6 = grid combined", dr(8 + 7), 6)
# DR-6 cluster from equal-digit audit
for v in [6, 33, 222, 111111]:
    check(dr(v) == 6, f"DR({v})=6 (equal-digit DR-6 cluster)", dr(v), 6)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Master Matrix Audit — Prime Architecture")
    print("=" * 62)

    print("\n── Strings and collapses ──")
    for label, s in [("blueprint", BLUEPRINT), ("A (8-fwd)", A),
                     ("B (8-rev)", B), ("C (7-fwd)", C), ("D (7-rev)", D)]:
        print(f"  {label:12s}  digit_sum={digit_sum(s):2d}  DR={collapse(s)}")

    print(f"\n── Reversal structure ──")
    print(f"  reverse(A) == B: {A[::-1] == B}")
    print(f"  reverse(C) == D: {C[::-1] == D}")

    print(f"\n── Grid collapses ──")
    print(f"  4×8=32 → DR={dr(32)}  |  4×7=28 → DR={dr(28)}  |  combined={dr(5+1)}")
    print(f"  Cross-add  8+7=15 → DR={dr(15)} (all rows, same as combined)")
    print(f"  Cross-mult 8×7=56 → DR={dr(56)} (blueprint DR = first prime)")
    print(f"  Bridge    8+8=16  → DR={dr(16)} (leaps to 7-pair root)")

    print(f"\n── M1: Doubling cycle ──")
    print(f"  1→2→4→8→7→5→1  (period 6)")
    print(f"  8-pair = step 4  |  7-pair = step 5  (consecutive)")

    print(f"\n── M2-M3: Alpha grid and 2n-1 sequence ──")
    print(f"  AHL=8 (RH-E)  ALO=7 (RL-O)  (alpha_grid.py)")
    print(f"  n=4: 2×4-1=7  DR=7=ALO  (4th prime IS the value)")
    print(f"  n=9: 2×9-1=17 DR=8=AHL  (7th prime has DR=AHL)")

    print(f"\n── M4: Digit sum prime decompositions ──")
    print(f"  8-pair: digit_sum=26=2×13  (13=6th prime)  DR(26)={dr(26)}=AHL")
    print(f"  7-pair: digit_sum=34=2×17  (17=7th prime)  DR(34)={dr(34)}=ALO")

    print(f"\n── M5: 137 = repunit + 8-pair digit_sum ──")
    print(f"  137 = 3×37 + 2×13 = 111 + 26")
    print(f"  111 = repunit_3 (framework repunit)")
    print(f"  26  = 8-pair digit_sum")
    print(f"  137 mod 37 = {137%37} = slot 26 ✓")

    print(f"\n── M6: Modal crossing ──")
    print(f"  191 → slot 6 → ORBIT_V (inner ring)")
    print(f"  100 → slot 26 → ORBIT_P (outer ring)")
    print(f"  slot_diff = 17 = 7th prime")
    print(f"  slot 26 = 8-pair digit_sum = 2×13th_prime = 137 mod 37")

    print(f"\n── M7: Prime chain ──")
    print(f"  7(4th)→ALO→DR=7→digit_sum 34=2×17")
    print(f"  17(7th)→slot_diff(191→100)→DR=8→AHL")
    print(f"  8(AHL)→DR=8→digit_sum 26=2×13")
    print(f"  13(6th)→137=111+26→33rd prime")
    print(f"  2(1st)→8×7 DR=2→blueprint")
    print(f"  6→8+7→equal-digit DR-6 cluster {{6,33,222,111111}}")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
