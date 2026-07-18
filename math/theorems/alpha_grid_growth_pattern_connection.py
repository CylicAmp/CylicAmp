"""
Alpha Grid — Growth Pattern Connection

The alpha grid 1234-(5)-6789 and the n->2n->(3n) growth pattern
are the same structure. The first 9 rows of the growth pattern
map exactly onto the 9 alpha grid positions.

Alpha grid:
  1: LL-O    2: LL-E    3: LH-O    4: LH-E
  (5): A51  (center axis)
  6: RL-E    7: RL-O    8: RH-E(AHL)    9: RH-O

Row 1: n=1(LL-O)   2n=2(LL-E,p,PR)   (3n)=3(LH-O,p,ST)
Row 2: n=2(LL-E)   2n=4(LH-E,SA)     (3n)=6(RL-E)
Row 3: n=3(LH-O)   2n=6(RL-E)        (3n)=9(RH-O,SA)
Row 4: n=4(LH-E)   2n=8(AHL,CB)      (3n)=12(ST)          <- three in one
Row 5: n=5(A51)    2n=10(.)          (3n)=15(PR)
Row 6: n=6(RL-E)   2n=12(ST)         (3n)=18(PR)
Row 7: n=7(RL-O)   2n=14(.)          (3n)=21(ST)
Row 8: n=8(AHL,CB) 2n=16(.)          (3n)=24(CB,PR)
Row 9: n=9(RH-O)   2n=18(PR)         (3n)=27(.)           <- all DR=9

Parity structure (locked):
  2n column is ALWAYS even — doubling makes everything even.
  3n parity mirrors n — odd*3=odd, even*3=even.
  So the parity of the whole table is determined by n alone.

Alpha grid parity assignments:
  Odd positions  (O): LL-O(1), LH-O(3), A51(5), RL-O(7), RH-O(9)
  Even positions (E): LL-E(2), LH-E(4), RL-E(6), RH-E/AHL(8)

Key structural facts:
  A51=5 is prime and primitive root mod 37 — the center generates.
  AHL=8 is cascade base — the alpha high is a structural generator.
  Row 4 (LH-E->AHL->ST) is the only row in first 9 where 2n hits AHL.
  The path 4->8->12 is the "three in one": LH-E -> AHL -> sovereign target.

GF(37) period = 37, DR period = 9, LCM = 333.
The alpha grid (positions 1-9) is the first DR cycle.
After row 9, the alpha grid positions repeat but the GF(37) tags evolve.
Zero has no alpha grid position — it appears only at the seams (rows 37,74,...,333).

Connection to primes:
  The first three primes (2,3,5) land on alpha positions LL-E, LH-O, A51.
  2 = LL-E (even, low-left)
  3 = LH-O (odd, high-left)
  5 = A51  (center axis)
  The first prime (2) is even. All others are odd.
  This is why 2 is structurally different — it's the only even prime,
  and the only prime that lands on an even alpha position.

Connection to 9*i pattern:
  9*5 mod 37 = 8 = AHL (cascade base)
  9*5 + 1 mod 37 = 9 = RH-O (sovereign anchor)
  The multiplication-by-9 operation maps A51 to AHL in GF(37).
  Center axis -> alpha high in one step.
"""

def dr(n):
    return (n - 1) % 9 + 1

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}
CASCADE_BASE       = {8, 13, 24}
PRIMITIVE_ROOTS_37 = {2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35}

ALPHA_GRID = {
    1:'LL-O', 2:'LL-E', 3:'LH-O', 4:'LH-E',
    5:'A51',
    6:'RL-E', 7:'RL-O', 8:'RH-E(AHL)', 9:'RH-O'
}

# ── Assertions ───────────────────────────────────────────────────────────────

# Alpha grid positions 1-9 map to themselves in rows 1-9
for n in range(1, 10):
    assert n % 37 == n
    assert n in ALPHA_GRID

# Row 4: three in one
assert 4 in SOVEREIGN_ANCHORS          # n=4: LH-E, SA
assert 8 in CASCADE_BASE               # 2n=8: AHL, CB
assert 12 in SOVEREIGN_TARGETS         # 3n=12: ST
assert dr(12) == 3                     # DR pulls back to 3

# A51 = 5 is prime and primitive root
assert is_prime(5)
assert 5 in PRIMITIVE_ROOTS_37

# AHL = 8 is cascade base
assert 8 in CASCADE_BASE

# 2 is the only even prime — only even alpha position that's prime
assert is_prime(2) and 2 % 2 == 0
assert all(p % 2 == 1 for p in [3, 5, 7, 11, 13, 17, 19, 23])

# 9*5 mod 37 = AHL, 9*5+1 mod 37 = RH-O
assert (9 * 5) % 37 == 8    # A51 -> AHL under *9
assert (9 * 5 + 1) % 37 == 9  # -> RH-O

# Parity: 2n is always even
for n in range(1, 334):
    assert (2 * n) % 2 == 0

# Parity: 3n mirrors n
for n in range(1, 334):
    assert (3 * n) % 2 == n % 2

# First three primes land on alpha positions LL-E, LH-O, A51
assert ALPHA_GRID[2] == 'LL-E'
assert ALPHA_GRID[3] == 'LH-O'
assert ALPHA_GRID[5] == 'A51'

import math
assert math.lcm(9, 37) == 333

print("Alpha Grid — Growth Pattern Connection")
print("=" * 55)
print()
print("First 9 rows (alpha grid layer):")
print(f"{'Row':>4}  {'n':>8}  {'2n':>12}  {'(3n)':>12}")
print("-" * 50)
rows_data = [
    (1, "1(LL-O)",      "2(LL-E,p,PR)",  "3(LH-O,p,ST)"),
    (2, "2(LL-E,p,PR)", "4(LH-E,SA)",    "6(RL-E)"),
    (3, "3(LH-O,p,ST)", "6(RL-E)",       "9(RH-O,SA)"),
    (4, "4(LH-E,SA)",   "8(AHL,CB)",     "12(ST) <- three in one"),
    (5, "5(A51,p,PR)",  "10(.)",         "15(PR)"),
    (6, "6(RL-E)",      "12(ST)",        "18(PR)"),
    (7, "7(RL-O,p)",    "14(.)",         "21(ST)"),
    (8, "8(AHL,CB)",    "16(.)",         "24(CB,PR)"),
    (9, "9(RH-O,SA)",   "18(PR)",        "27(.) <- all DR=9"),
]
for row, n, two_n, three_n in rows_data:
    print(f"{row:>4}  {n:>12}  {two_n:>16}  {three_n}")

print()
print("9*i -> GF(37) connection:")
print(f"  9*5 mod 37 = {(9*5)%37} = AHL  (A51 center -> alpha high)")
print(f"  9*5+1 mod 37 = {(9*5+1)%37} = RH-O  (sovereign anchor)")
print()
print(f"LCM(9,37) = {math.lcm(9,37)} — full cycle length")
print()
print("All assertions passed.")
