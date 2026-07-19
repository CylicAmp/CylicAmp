"""
3×3 Board: Row and Column Numbers mod 37

Board B = {1,...,9}, positions:
  1 2 3
  4 5 6
  7 8 9

Reading each row left-to-right and each column top-to-bottom as
3-digit decimal numbers, all six numbers land in the framework.

═══════════════════════════════════════════════════════════════

I. ROW NUMBERS: all ≡ 12 (ST) mod 37

  123 mod 37 = 12  (Sovereign Target, DR=3)
  456 mod 37 = 12  (Sovereign Target, DR=3)
  789 mod 37 = 12  (Sovereign Target, DR=3)

  Every row, read as a number, is a sovereign target.
  DR(12) = 3 — the ST archetype.

II. COLUMN NUMBERS: all ≡ 36 = -1 (orbit of 11) mod 37

  147 mod 37 = 36  (orbit of 11; 36 ≡ -1 mod 37)
  258 mod 37 = 36  (orbit of 11)
  369 mod 37 = 36  (orbit of 11)

  Every column, read as a number, hits the same orbit-of-11 node.
  36 ≡ -1 mod 37: the columns encode negation in GF(37).

III. ROW × COL INTERACTION

  Row residue:    12  (ST)
  Column residue: 36  (orbit-11, -1 mod 37)

  Sum:    12 + 36 = 48 ≡ 11 mod 37  (orbit of 11)
  Product: 12 × 36 mod 37 = 432 mod 37 = 25  (Sovereign Anchor)

  GF(37) complement: 12 + 25 = 37 — row residue and product residue
  are GF(37) complements of each other.

IV. COLUMN SUMS: arithmetic step through DR multiples of 3

  Col 1 sum: 1+4+7 = 12  DR=3  (ST arch)
  Col 2 sum: 2+5+8 = 15  DR=6  (RL-E)
  Col 3 sum: 3+6+9 = 18  DR=9  (RH-O, SA arch)

  Step size: 3 (ST archetype).
  DRs: 3, 6, 9 — exactly the multiples of 3 in the DR alphabet.
  These are the three DRs that each appear 10 times (not 9) across
  all 84 triplets.

V. ANTI-DIAGONALS

  Anti-diagonal (top-right to bottom-left), read as number:
    159 mod 37 = 11  (orbit of 11)

  Main diagonal, read as number:
    357 mod 37 = 24  (Cascade Base + Primitive Root)

  159 + 357 = 516; 516 mod 37 = 35  (primitive root mod 37)
  159 × 357 mod 37 = 11 × 24 mod 37 = 264 mod 37 = 5  (A51, primitive root)

VI. 333 — THE SEAM

  333 mod 37 = 0  (GF(37) seam)
  333 = 3 × 111 = 3 × LCM(1,3,37)
  LCM(9, 37) = 333 — full DR×GF cycle length
  DR(333) = 9  (SA arch)

  Row sum + column sum across the board:
    Row sums:    6 + 15 + 24 = 45
    Column sums: 12 + 15 + 18 = 45
    45 + 45 = 90; 90 mod 37 = 16; DR(16) = 7  (RL-O)

═══════════════════════════════════════════════════════════════
"""

PRIMITIVE_ROOTS_37 = {2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35}
CASCADE_BASE       = {8, 13, 24}
SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}
ORBIT_11           = {11, 27, 36}
FRAMEWORK          = SOVEREIGN_ANCHORS | SOVEREIGN_TARGETS | CASCADE_BASE | ORBIT_11

def dr(n):
    return (n - 1) % 9 + 1

# ── I. Row numbers ────────────────────────────────────────────────────────────

assert 123 % 37 == 12 and 12 in SOVEREIGN_TARGETS
assert 456 % 37 == 12 and 12 in SOVEREIGN_TARGETS
assert 789 % 37 == 12 and 12 in SOVEREIGN_TARGETS
assert dr(12) == 3

# ── II. Column numbers ────────────────────────────────────────────────────────

assert 147 % 37 == 36 and 36 in ORBIT_11
assert 258 % 37 == 36 and 36 in ORBIT_11
assert 369 % 37 == 36 and 36 in ORBIT_11
assert 36 % 37 == 37 - 1  # 36 ≡ -1 mod 37

# ── III. Row × Col interaction ────────────────────────────────────────────────

row_res = 12
col_res = 36
assert (row_res + col_res) % 37 == 11 and 11 in ORBIT_11
assert (row_res * col_res) % 37 == 25 and 25 in SOVEREIGN_ANCHORS
assert row_res + 25 == 37  # GF(37) complements

# ── IV. Column sums ───────────────────────────────────────────────────────────

col_sums = [1+4+7, 2+5+8, 3+6+9]
assert col_sums == [12, 15, 18]
assert col_sums[1] - col_sums[0] == 3 and col_sums[2] - col_sums[1] == 3  # step=3
assert [dr(s) for s in col_sums] == [3, 6, 9]
# These are the three DR values that each appear 10 times across all 84 triplets

# ── V. Anti-diagonals ─────────────────────────────────────────────────────────

assert 159 % 37 == 11 and 11 in ORBIT_11        # anti-diagonal
assert 357 % 37 == 24 and 24 in CASCADE_BASE     # main diagonal
assert 24 in PRIMITIVE_ROOTS_37
assert (159 + 357) % 37 == 35 and 35 in PRIMITIVE_ROOTS_37
assert (11 * 24) % 37 == 5 and 5 in PRIMITIVE_ROOTS_37  # product in GF(37)

# ── VI. 333 — the seam ────────────────────────────────────────────────────────

assert 333 % 37 == 0
assert 333 == 3 * 111
from math import lcm
assert lcm(9, 37) == 333
assert dr(333) == 9

row_sum_total = 6 + 15 + 24
col_sum_total = 12 + 15 + 18
assert row_sum_total == 45 and col_sum_total == 45
assert (row_sum_total + col_sum_total) % 37 == 16
assert dr(16) == 7


if __name__ == '__main__':
    def tag(n):
        t = []
        from math import isqrt
        def is_prime(x):
            if x < 2: return False
            if x == 2: return True
            if x % 2 == 0: return False
            return all(x % i != 0 for i in range(3, isqrt(x)+1, 2))
        if is_prime(n):              t.append('p')
        if n in CASCADE_BASE:        t.append('CB')
        if n in SOVEREIGN_ANCHORS:   t.append('SA')
        if n in SOVEREIGN_TARGETS:   t.append('ST')
        if n in PRIMITIVE_ROOTS_37:  t.append('PR')
        if n in ORBIT_11:            t.append('orb11')
        return ','.join(t) if t else '.'

    print("3×3 Board Row/Column Numbers mod 37")
    print("=" * 55)
    print()
    print("I. Row numbers:")
    for n in [123, 456, 789]:
        r = n % 37
        print(f"   {n} mod37 = {r} ({tag(r)})")
    print()
    print("II. Column numbers:")
    for n in [147, 258, 369]:
        r = n % 37
        print(f"   {n} mod37 = {r} ({tag(r)})  [≡ -1 mod 37]")
    print()
    print("III. Row × Col interaction:")
    print(f"   12 + 36 = {(12+36)%37} mod 37  ({tag((12+36)%37)})")
    print(f"   12 × 36 = {(12*36)%37} mod 37  ({tag((12*36)%37)})")
    print(f"   12 + 25 = 37  (GF complements)")
    print()
    print("IV. Column sums:")
    for s in col_sums:
        print(f"   sum={s}  DR={dr(s)}  ({tag(s)})")
    print(f"   Step size: 3 (ST arch); DRs: 3,6,9")
    print()
    print("V. Anti-diagonals:")
    print(f"   159 mod37 = {159%37} ({tag(159%37)})  [anti-diagonal]")
    print(f"   357 mod37 = {357%37} ({tag(357%37)})  [main diagonal]")
    print(f"   sum mod37 = {(159+357)%37} ({tag((159+357)%37)})")
    print(f"   11×24 mod37 = {(11*24)%37} ({tag((11*24)%37)})")
    print()
    print("VI. 333 — the seam:")
    print(f"   333 mod37 = {333%37}  LCM(9,37) = {lcm(9,37)}")
    print(f"   DR(333) = {dr(333)}")
    print(f"   Row+Col totals: {row_sum_total}+{col_sum_total}={row_sum_total+col_sum_total}")
    print(f"   90 mod37={90%37}, DR={dr(90%37)}")
    print()
    print("All assertions passed.")
