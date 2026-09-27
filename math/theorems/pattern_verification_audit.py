"""
Pattern Verification Audit — Doubling, Grid, Mirror, Permutation

Classification: Theorem

Five structural patterns verified and connected to the F₃₇ anchor framework.

Pattern 1 — Doubling chain:
  1→2→4→8  (powers of 2: 2⁰→2¹→2²→2³)
  Connects to: 2 is the minimal primitive root mod 37; 2^12 = 26

Pattern 2 — 6×4 grid:
  Four rows of six entries drawn from {2,4}; each row sums to 16 = 2⁴.
  Total = 64 = 2⁶ = 4²;  6+4 = 10 (SCALAR pivot, since 10² ≡ 26 mod 37).
  Grid carries exactly 8 fours and 16 twos — same four/two ratio as matrix
  rows in the Master Record (8 sevens per 12-digit row).
  Bonus: 64 mod 37 = 27 = 3³ ∈ QR₃₇ — the grid total lands on the 3rd
  element of the 18-cycle ⟨3⟩, connecting the grid directly to the residue orbit.

Pattern 3 — 88+66:
  88+66 = 154;  digit sum of original digits: 8+8+6+6 = 28 = dual bridge B̃.
  DR(28) = 1 (identity);  28 = 3^11 mod 37 ∈ QR₃₇ (confirmed in LoB 88).
  Cascade: 28 → 2+8 = 10 → 1+0 = 1 (identity DR).

Pattern 4 — {1,2,8} permutations:
  All 6 permutations of {1,2,8} sum to 1+2+8 = 11.
  11 = 3^15 mod 37 ∈ QR₃₇;  DR(11) = 2;  11 appears in Master Record bridge.
  Sum 11 is invariant under permutation by commutativity of addition.

Pattern 5 — 123/321 mirror:
  123+321 = 444;  444+444 = 888.
  DR(444) = DR(12) = 3  (anchor target DR=3).
  DR(888) = DR(24) = 6  (coupling DR — matches address root DR=6).
  123+321+123+321 = 888 = sum of four three-digit mirrors.
"""

from itertools import permutations
from collections import Counter


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


# ── Framework constants ────────────────────────────────────────────────────

CYCLE18    = [pow(3, k, 37) for k in range(1, 19)]
QR37       = frozenset((x * x) % 37 for x in range(1, 37))
# 26 = 137 mod 37
BRIDGE_DUAL = 28    # dual prime bridge from string_duality_37phi_bridge

# ── Pattern 1: Doubling chain ──────────────────────────────────────────────

chain = [1, 2, 4, 8]
assert chain[0] == 1
assert all(chain[i] * 2 == chain[i+1] for i in range(len(chain)-1)), \
    "Doubling chain broken"
assert chain == [2**k for k in range(4)]

# Connects to primitive root 2 and 26
assert pow(2, 12, 37) == 26    # 2^12 = 26 mod 37

# ── Pattern 2: 6×4 grid ────────────────────────────────────────────────────

GRID = [
    [4, 2, 2, 2, 2, 4],
    [2, 4, 2, 2, 4, 2],
    [2, 2, 4, 4, 2, 2],
    [4, 2, 2, 2, 2, 4],
]

COLS = 6
ROWS = 4

assert len(GRID) == ROWS
assert all(len(row) == COLS for row in GRID)

row_sums = [sum(row) for row in GRID]
assert all(s == 16 for s in row_sums), f"Row sums not all 16: {row_sums}"

total_sum = sum(row_sums)
assert total_sum == 64
assert 64 == 2**6 == 4**3

# 6+4 = 10 pivot
assert COLS + ROWS == 10
assert (10 * 10) % 37 == 26    # 10² ≡ 26 mod 37

# Entry counts: 8 fours, 16 twos
flat = [v for row in GRID for v in row]
counts = Counter(flat)
assert counts[4] == 8
assert counts[2] == 16
assert counts[4] + counts[2] == ROWS * COLS

# Bonus: 64 mod 37 = 27 = 3³ — grid total lands in the residue cycle
assert total_sum % 37 == 27
assert 27 == pow(3, 3, 37)
assert 27 in QR37
assert CYCLE18.index(27) + 1 == 3    # 3³ = 27 is the 3rd element of the 18-cycle

# ── Pattern 3: 88+66 ──────────────────────────────────────────────────────

A, B = 88, 66
total_3 = A + B
assert total_3 == 154

# Digit sum of original operands → dual bridge
digit_sum_operands = sum(int(d) for d in str(A) + str(B))
assert digit_sum_operands == 28
assert digit_sum_operands == BRIDGE_DUAL

# 28 ∈ QR₃₇, = 3^11 mod 37
assert BRIDGE_DUAL in QR37
assert CYCLE18.index(BRIDGE_DUAL) + 1 == 11    # 3^11 = 28

# DR cascade: 28 → 10 → 1
assert 2 + 8 == 10
assert 1 + 0 == 1
assert dr(BRIDGE_DUAL) == 1    # identity DR

# ── Pattern 4: {1,2,8} permutations ───────────────────────────────────────

DIGITS = [1, 2, 8]
DIGIT_SUM = sum(DIGITS)
assert DIGIT_SUM == 11

perms = list(permutations(DIGITS))
assert len(perms) == 6    # 3! = 6

perm_sums = [sum(p) for p in perms]
assert all(s == DIGIT_SUM for s in perm_sums), \
    "Sum not invariant across permutations — addition not commutative?"

# 11 = 3^15 mod 37 ∈ QR₃₇
assert 11 in QR37
assert CYCLE18.index(11) + 1 == 15    # 3^15 = 11
assert dr(11) == 2

# ── Pattern 5: 123/321 mirror ─────────────────────────────────────────────

N1, N2 = 123, 321
assert N1 + N2 == 444

# Palindrome pair: digits of 321 reverse those of 123
assert str(N2) == str(N1)[::-1]

# DR chain
assert dr(444) == 3    # 4+4+4=12, 1+2=3 → f26 target DR
assert 444 + 444 == 888
assert dr(888) == 6    # 8+8+8=24, 2+4=6 → coupling DR (= address root)
assert N1 + N2 + N1 + N2 == 888

# DR(3)=3 is anchor target; DR(6)=6 is coupling signature
F26_ANCHOR_TARGET_DR = 3
COUPLING_DR = 6
assert dr(444) == F26_ANCHOR_TARGET_DR
assert dr(888) == COUPLING_DR


if __name__ == "__main__":
    print("Pattern Verification Audit")
    print()

    print("Pattern 1 — Doubling chain:")
    print(f"  {' → '.join(str(v) for v in chain)}")
    print(f"  2^12 mod 37 = {pow(2,12,37)} = 26 ✓")
    print()

    print("Pattern 2 — 6×4 grid:")
    for i, row in enumerate(GRID, 1):
        print(f"  Row {i}: {'-'.join(str(v) for v in row)} = {sum(row)}")
    print(f"  Total sum: {total_sum} = 2^6 = 4^3")
    print(f"  6+4 = {COLS+ROWS}  (10² mod 37 = {26} = 26 ✓)")
    print(f"  Fours: {counts[4]},  Twos: {counts[2]}")
    print(f"  Bonus: 64 mod 37 = {total_sum % 37} = 3³ ∈ QR₃₇  (cycle position {CYCLE18.index(27)+1}) ✓")
    print()

    print("Pattern 3 — 88+66:")
    print(f"  {A}+{B} = {total_3}")
    print(f"  Digit sum of operands: {digit_sum_operands} = dual bridge B̃ ✓")
    print(f"  28 = 3^11 mod 37 ∈ QR₃₇,  DR(28)={dr(28)} (identity) ✓")
    print()

    print("Pattern 4 — {{1,2,8}} permutations:")
    for p in perms:
        print(f"  {p[0]}+{p[1]}+{p[2]} = {sum(p)}")
    print(f"  All sums = {DIGIT_SUM} = 3^15 mod 37 ∈ QR₃₇ ✓")
    print()

    print("Pattern 5 — 123/321 mirror:")
    print(f"  123+321 = {N1+N2},  DR={dr(N1+N2)} (anchor target, DR=3) ✓")
    print(f"  444+444 = {888},    DR={dr(888)} (coupling signature) ✓")
    print(f"  123+321+123+321 = {N1+N2+N1+N2} ✓")
    print()

    print("All assertions passed.")
