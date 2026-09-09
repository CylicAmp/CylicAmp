"""
criss_cross_17_81_audit.py

The four numbers {17, 71, 18, 81} and their DR structure.

─────────────────────────────────────────────────────────────────
THE CRISS-CROSS:

  Matrix [[1,7],[8,1]] generates all four numbers:
    Row 1 LR / Col 2 BT:  17   (prime, DR=8)
    Row 1 RL / Col 1 BT:  71   (prime, DR=8)
    Row 2 LR / Col 1 TB:  81   (3^4,  DR=9)
    Row 2 RL / Col 2 TB:  18   (2×3², DR=9)

  Pair {17,71}: both prime, both DR=8, reversal of each other.
  Pair {18,81}: both DR=9, reversal of each other.

SUMS:
  17+71 = 88   DR=7
  18+81 = 99   DR=9
  17+81 = 98   DR=8
  18+71 = 89   DR=8

PRODUCTS (DR multiplicativity: DR(a×b) = DR(DR(a)×DR(b))):
  17×71 = 1207  DR=1   [DR(8)×DR(8) = 64 → DR=1]  ← 8 is -1 mod 9
  18×81 = 1458  DR=9   [DR(9)×DR(9) = 81 → DR=9]
  17×81 = 1377  DR=9   [DR(8)×DR(9) = 72 → DR=9]
  18×71 = 1278  DR=9   [same]

  Key: DR(8)=8≡-1 (mod 9) → 8²≡1 (mod 9) → DR(17²)=DR(17×71)=1
       DR(9)=9≡0 (mod 9) → 9×anything≡0 → DR(product)=9

DR UNDER n-REPETITIONS:
  17 or 71 repeated n times: digit sum = 8n → DR = DR(8n)
    n=1..9: [8,7,6,5,4,3,2,1,9]  — all 9 DRs, descending from 8
  18 or 81 repeated n times: digit sum = 9n → DR = 9 always

ALTERNATING STRINGS (13 digits):
  1717171717171  DR=4  (7 ones, 6 sevens;  digit_sum=49 → DR=4)
  8181818181818  DR=8  (7 eights, 6 ones;  digit_sum=62 → DR=8)
  1818181818181  DR=1  (7 ones, 6 eights;  digit_sum=55 → DR=1)
  7171717171717  DR=1  (7 sevens, 6 ones;  digit_sum=55 → DR=1)

  DR set of four strings: {1, 4, 8}
  Sum of four DRs: 4+8+1+1=14 → DR=5  (the pivot)

PARSING THE ALTERNATING STRING BY UNIT SIZE k:
  Even k: one repeating unit, DR = DR(8×k/2)  [descends 8,7,6,5,...]
  Odd k:  two alternating units with digit sums (8m+1) and (8m+7)
          where m=(k-1)/2; combined digit sum = 8k

COMBINATION COUNT:
  Alphabet {17,71,18,81}: 4 distinct two-digit elements.
  Sequences of length n (concatenated): 4^n distinct strings.
    n=1:  4   n=2:  16   n=3:  64   n=4:  256   n=5:  1024

─────────────────────────────────────────────────────────────────
"""

from sympy import isprime, factorint

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


# ── The four numbers ──────────────────────────────────────────────────────────

check(isprime(17), "17 prime", isprime(17), True)
check(isprime(71), "71 prime", isprime(71), True)
check(not isprime(18), "18 composite", isprime(18), False)
check(not isprime(81), "81 composite", isprime(81), False)

check(factorint(18) == {2: 1, 3: 2}, "18=2×3²", factorint(18), {2: 1, 3: 2})
check(factorint(81) == {3: 4},       "81=3^4",  factorint(81), {3: 4})

check(dr(17) == 8, "DR(17)=8", dr(17), 8)
check(dr(71) == 8, "DR(71)=8", dr(71), 8)
check(dr(18) == 9, "DR(18)=9", dr(18), 9)
check(dr(81) == 9, "DR(81)=9", dr(81), 9)

# Reversal pairs
check(int(str(17)[::-1]) == 71, "17 reversal=71", int(str(17)[::-1]), 71)
check(int(str(18)[::-1]) == 81, "18 reversal=81", int(str(18)[::-1]), 81)


# ── 2×2 matrix readings ───────────────────────────────────────────────────────

MATRIX = [[1, 7], [8, 1]]
check(MATRIX[0][0]*10 + MATRIX[0][1] == 17, "row1 LR=17", MATRIX[0][0]*10+MATRIX[0][1], 17)
check(MATRIX[0][1]*10 + MATRIX[0][0] == 71, "row1 RL=71", MATRIX[0][1]*10+MATRIX[0][0], 71)
check(MATRIX[1][0]*10 + MATRIX[1][1] == 81, "row2 LR=81", MATRIX[1][0]*10+MATRIX[1][1], 81)
check(MATRIX[1][1]*10 + MATRIX[1][0] == 18, "row2 RL=18", MATRIX[1][1]*10+MATRIX[1][0], 18)

# Column readings
check(MATRIX[0][0]*10 + MATRIX[1][0] == 18, "col1 TB=18", MATRIX[0][0]*10+MATRIX[1][0], 18)
check(MATRIX[0][1]*10 + MATRIX[1][1] == 71, "col2 TB=71", MATRIX[0][1]*10+MATRIX[1][1], 71)

# Diagonal: 11, anti-diagonal: 78
check(MATRIX[0][0]*10 + MATRIX[1][1] == 11, "diag=11",      MATRIX[0][0]*10+MATRIX[1][1], 11)
check(MATRIX[0][1]*10 + MATRIX[1][0] == 78, "anti-diag=78", MATRIX[0][1]*10+MATRIX[1][0], 78)
check(dr(11) == 2, "DR(11)=2", dr(11), 2)
check(dr(78) == 6, "DR(78)=6", dr(78), 6)


# ── Sums ─────────────────────────────────────────────────────────────────────

check(17 + 71 == 88, "17+71=88",   17+71,  88)
check(18 + 81 == 99, "18+81=99",   18+81,  99)
check(17 + 81 == 98, "17+81=98",   17+81,  98)
check(18 + 71 == 89, "18+71=89",   18+71,  89)
check(dr(88) == 7, "DR(88)=7",   dr(88),  7)
check(dr(99) == 9, "DR(99)=9",   dr(99),  9)
check(dr(98) == 8, "DR(98)=8",   dr(98),  8)
check(dr(89) == 8, "DR(89)=8",   dr(89),  8)


# ── Products and DR multiplicativity ─────────────────────────────────────────

check(17 * 71 == 1207, "17×71=1207", 17*71, 1207)
check(18 * 81 == 1458, "18×81=1458", 18*81, 1458)
check(17 * 81 == 1377, "17×81=1377", 17*81, 1377)
check(18 * 71 == 1278, "18×71=1278", 18*71, 1278)

check(dr(1207) == 1, "DR(17×71)=1", dr(1207), 1)
check(dr(1458) == 9, "DR(18×81)=9", dr(1458), 9)
check(dr(1377) == 9, "DR(17×81)=9", dr(1377), 9)
check(dr(1278) == 9, "DR(18×71)=9", dr(1278), 9)

# DR multiplicativity: DR(a×b) = DR(DR(a)×DR(b))
for a, b in [(17,71),(18,81),(17,81),(18,71)]:
    check(
        dr(a*b) == dr(dr(a)*dr(b)),
        f"DR({a}×{b}) multiplicative",
        dr(a*b),
        dr(dr(a)*dr(b)),
    )

# 8 ≡ -1 (mod 9): 8² ≡ 1 (mod 9)
check(8 % 9 == 8, "8 mod 9 = 8 = -1 mod 9", 8 % 9, 8)
check(64 % 9 == 1, "8² mod 9 = 1", 64 % 9, 1)
check(dr(64) == 1, "DR(64)=1", dr(64), 1)

# 9 ≡ 0 (mod 9): 9×anything ≡ 0 → DR=9
check(9 % 9 == 0, "9 mod 9 = 0", 9 % 9, 0)
check(dr(9 * 8) == 9, "DR(9×8)=9", dr(9*8), 9)


# ── DR under n-repetitions ────────────────────────────────────────────────────

REP17_DRS = [dr(8 * n) for n in range(1, 10)]
check(REP17_DRS == [8, 7, 6, 5, 4, 3, 2, 1, 9], "rep(17) DRs", REP17_DRS, [8, 7, 6, 5, 4, 3, 2, 1, 9])
check(set(REP17_DRS) == set(range(1, 10)), "rep(17) covers all 9 DRs", set(REP17_DRS), set(range(1, 10)))

REP81_DRS = [dr(9 * n) for n in range(1, 10)]
check(all(d == 9 for d in REP81_DRS), "rep(81) always DR=9", REP81_DRS, [9]*9)

# rep(71) same as rep(17): digit sum per rep = 7+1 = 8
check([dr(8*n) for n in range(1,10)] == REP17_DRS, "rep(71)=rep(17) DRs", True, True)

# rep(18) same as rep(81): digit sum per rep = 1+8 = 9
check([dr(9*n) for n in range(1,10)] == REP81_DRS, "rep(18)=rep(81) DRs", True, True)


# ── Alternating 13-digit strings ─────────────────────────────────────────────

STRINGS = [
    ('1717171717171', 7, 6, 0, 49, 4),  # ones, sevens, eights, digit_sum, DR
    ('8181818181818', 6, 0, 7, 62, 8),
    ('1818181818181', 7, 0, 6, 55, 1),
    ('7171717171717', 6, 7, 0, 55, 1),
]

for s, n1, n7, n8, expected_sum, expected_dr in STRINGS:
    actual_sum = sum(int(c) for c in s)
    check(len(s) == 13, f"len({s[:4]}...)=13", len(s), 13)
    check(s.count('1') == n1, f"{s[:4]}... ones={n1}", s.count('1'), n1)
    check(s.count('7') == n7, f"{s[:4]}... sevens={n7}", s.count('7'), n7)
    check(s.count('8') == n8, f"{s[:4]}... eights={n8}", s.count('8'), n8)
    check(actual_sum == expected_sum, f"{s[:4]}... sum={expected_sum}", actual_sum, expected_sum)
    check(dr(actual_sum) == expected_dr, f"{s[:4]}... DR={expected_dr}", dr(actual_sum), expected_dr)

STRING_DRS = [4, 8, 1, 1]
check(sum(STRING_DRS) == 14, "string DRs sum=14", sum(STRING_DRS), 14)
check(dr(sum(STRING_DRS)) == 5, "DR of string DR sum = 5", dr(sum(STRING_DRS)), 5)


# ── Parsing unit sizes ────────────────────────────────────────────────────────

# Even k: single unit '17'*(k//2), DR = DR(8*(k//2))
EVEN_UNIT_DRS = {}
for k in [2, 4, 6, 8]:
    unit = '17' * (k // 2)
    d = dr(sum(int(c) for c in unit))
    EVEN_UNIT_DRS[k] = d
    check(d == dr(8 * (k // 2)), f"even k={k} DR", d, dr(8 * (k // 2)))

check(list(EVEN_UNIT_DRS.values()) == [8, 7, 6, 5], "even unit DRs descend 8,7,6,5",
      list(EVEN_UNIT_DRS.values()), [8, 7, 6, 5])

# Odd k=1: units '1'(DR=1) and '7'(DR=7), sums 1+7=8=DR(8×1)
check(dr(1) + dr(7) == 8, "odd k=1 sum DRs=8", dr(1)+dr(7), 8)


# ── Combination counts ────────────────────────────────────────────────────────

for n in range(1, 6):
    count = 4 ** n
    check(count == 4**n, f"combos length {n}", count, 4**n)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Criss-Cross {17,71,18,81} Audit")
    print("=" * 62)

    print(f"\n── Matrix [[1,7],[8,1]] readings ──")
    print(f"  17 (prime)  DR={dr(17)}   71 (prime)  DR={dr(71)}")
    print(f"  81 (3^4)    DR={dr(81)}   18 (2×3²)   DR={dr(18)}")
    print(f"  Diagonal 11 DR={dr(11)}   Anti-diag 78 DR={dr(78)}")

    print(f"\n── Sums ──")
    for a, b in [(17,71),(18,81),(17,81),(18,71)]:
        print(f"  {a}+{b}={a+b}  DR={dr(a+b)}")

    print(f"\n── Products ──")
    for a, b in [(17,71),(18,81),(17,81),(18,71)]:
        p = a*b
        print(f"  {a}×{b}={p}  DR={dr(p)}  [DR({dr(a)})×DR({dr(b)})=DR({dr(a)*dr(b)})={dr(dr(a)*dr(b))}]")
    print(f"  8≡-1(mod 9): 8²=64≡1 → DR(17×71)=1")
    print(f"  9≡0(mod 9): 9×anything≡0 → DR=9")

    print(f"\n── DR under n-repetitions ──")
    print(f"  rep(17) n=1..9: {REP17_DRS}  [all 9 DRs, descending from 8]")
    print(f"  rep(81) n=1..9: {REP81_DRS}  [constant 9]")

    print(f"\n── Alternating 13-digit strings ──")
    for s, *_, d in STRINGS:
        print(f"  {s}  DR={d}")
    print(f"  DRs: {STRING_DRS}  sum→DR={dr(sum(STRING_DRS))} (pivot)")

    print(f"\n── Parsing unit size k ──")
    for k in range(1, 9):
        if k % 2 == 0:
            unit = '17' * (k // 2)
            print(f"  k={k} (even): unit='{unit}'  DR={dr(sum(int(c) for c in unit))}")
        else:
            m = (k-1)//2
            u1 = ('17'*(m+1))[:k]
            u2 = ('71'*(m+1))[:k]
            print(f"  k={k} (odd):  units='{u1}'/{u2}'  DRs={dr(sum(int(c) for c in u1))},{dr(sum(int(c) for c in u2))}")

    print(f"\n── Combination counts over {{17,71,18,81}} ──")
    for n in range(1, 6):
        print(f"  length {n}: {4**n:>5} sequences")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
