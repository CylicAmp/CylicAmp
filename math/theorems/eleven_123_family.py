"""
11 as 123-family representative

Definition of the 123 family:
  Any arithmetic or algebraic formula that, once fully calculated,
  contains a 1, a 2, and a 3 — as values, digits, or digital roots —
  in ANY order. The three values do not have to appear sequentially.

  There are three styles (orderings of {1,2,3}):
    1-2-3  (forward):  1+2=3
    2-1-3  (rotated):  11+10=21=3  (21 holds 2 and 1; DR=3)
    3-2-1  (reverse):  3+8=11, DR(11)=2, 1 inside 11

  All six permutations of {1,2,3} are valid 123-family instances —
  connecting directly to S3, the symmetric group on three elements.

11+10=21, DR(21)=3. Instantiates the 2-1-3 style:
  DR(11)=2, DR(10)=1, DR(21)=3.

Key structural facts about 11:

  1. 11 = 37 - 26
     11 is the additive inverse of the 137-map multiplier (26) in GF(37).
     11 + 26 = 37 ≡ 0 (mod 37).

  2. 11 is prime, DR(11)=2 (LL-E in alpha grid).

  3. 137-map orbit of 11: {11, 27, 36}
     26*11 = 286 ≡ 27 (mod 37)
     26*27 = 702 ≡ 36 (mod 37)
     26*36 = 936 ≡ 11 (mod 37)
     36 ≡ -1 (mod 37): the orbit of 11 passes through -1.

The Fibonacci-seed grid (four rows whose digits are Fibonacci-derived):

  11235  (digits 1,1,2,3,5 = first 5 Fibonacci numbers)
  12371
  13459
  14562

Anti-diagonal sums (r+c = const):
  d=0: [1]           sum=1   DR=1
  d=1: [1,1]         sum=2   DR=2
  d=2: [2,2,1]       sum=5   DR=5
  d=3: [3,3,3,1]     sum=10  DR=1
  d=4: [5,7,4,4]     sum=20  DR=2
  d=5: [1,5,5]       sum=11  DR=2
  d=6: [9,6]         sum=15  DR=6
  d=7: [2]           sum=2   DR=2

DR sequence: 1-2-5-1-2 | 2-6-2

The split at position 5 is structural — the diagonal lines peak at 4 elements
(d=4, full row count), then the EXIT SIDE begins at d=5 with exactly 3 remaining:
  Entry side (d=0..4): element counts 1,2,3,4,4 -> DRs 1,2,5,1,2 -> sum=11
  Exit  side (d=5..7): element counts 3,2,1     -> DRs 2,6,2     -> sum=10

The 6 comes from d=6: values [9,6], 9+6=15, DR(15)=6.
Two different colors in the image mark the two groups (11 and 10).

  First 5 DRs sum = 1+2+5+1+2 = 11
  Last  3 DRs sum = 2+6+2     = 10
  Total:              11+10   = 21, DR(21) = 3

This reproduces: 11+10=21=3

The 10^3 ≡ 1 (mod 37) split property (from ord_37(10)=3):
  Any 5-digit number n=hi*1000+lo satisfies n ≡ hi+lo (mod 37).

Applied to the four rows:
  11235: 11+235=246 (reference seed), mod37=24 (CB,PR)
  12371: 12+371=383 (prime),          mod37=13 (CB,PR)
  13459: 13+459=472,                  mod37=28
  14562: 14+562=576=24²,              mod37=21 (ST)

  11235 mod 37 = 246 mod 37 = 24 (CB, PR) — links to the reference seed.

Alpha palindrome (red layer):
  3-8-7-3 | 3-7-8-3
  3=LH-O, 8=AHL(CB), 7=RL-O, 3=LH-O
  3+8=11, 7+3=10  =>  11+10=21=3  (same identity)
  Each half sums to 21 (sovereign target, ST).

Bottom sequence: 11, 122, 133, 315, 744, 155, 962
  962 = 26 * 37  (137-map multiplier × the prime)
  Sum = 2442, DR(2442) = 3
"""

import math

def dr(n):
    return (n - 1) % 9 + 1

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

PRIMITIVE_ROOTS_37 = {2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35}
CASCADE_BASE       = {8, 13, 24}
SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}
ALPHA_GRID = {
    1:'LL-O', 2:'LL-E', 3:'LH-O', 4:'LH-E',
    5:'A51',
    6:'RL-E', 7:'RL-O', 8:'RH-E(AHL)', 9:'RH-O'
}

# ── Assertions ───────────────────────────────────────────────────────────────

# 11 is the additive complement of 26 in GF(37)
assert 11 + 26 == 37
assert (-26) % 37 == 11

# 11 is prime, DR=2 (LL-E)
assert is_prime(11)
assert dr(11) == 2

# 123-family: DR(10)+DR(11) -> DR(10+11)
assert dr(10) == 1 and dr(11) == 2 and dr(10 + 11) == 3

# 137-map orbit of 11 = {11, 27, 36}
orbit_11 = []
x = 11
for _ in range(4):
    orbit_11.append(x)
    x = (26 * x) % 37
assert orbit_11[:3] == [11, 27, 36]
assert 36 % 37 == 37 - 1    # 36 ≡ -1 (mod 37)

# 10^3 ≡ 1 (mod 37) — split property
assert (10 ** 3) % 37 == 1
assert 1000 % 37 == 1

# Five-digit split: n ≡ hi(2 digits) + lo(3 digits) (mod 37)
BLUE_NUMBERS = [11235, 12371, 13459, 14562]
BLUE_SPLITS  = [(11, 235), (12, 371), (13, 459), (14, 562)]
for num, (hi, lo) in zip(BLUE_NUMBERS, BLUE_SPLITS):
    assert num % 37 == (hi + lo) % 37

# 11235: hi+lo = 246 = reference seed
assert 11 + 235 == 246
assert 246 % 37 == 24 and 24 in CASCADE_BASE and 24 in PRIMITIVE_ROOTS_37
assert 11235 % 37 == 24

# 14562: hi+lo = 576 = 24², mod37 = 21 (ST)
assert 14 + 562 == 576
assert 576 == 24 ** 2
assert 14562 % 37 == 21 and 21 in SOVEREIGN_TARGETS

# Anti-diagonal DR sequence of the grid
GRID = [
    [1, 1, 2, 3, 5],
    [1, 2, 3, 7, 1],
    [1, 3, 4, 5, 9],
    [1, 4, 5, 6, 2],
]
anti_sums = []
for d in range(8):
    vals = [GRID[r][d - r] for r in range(4) if 0 <= d - r < 5]
    anti_sums.append(sum(vals))

anti_dr = [dr(s) for s in anti_sums]
assert anti_dr == [1, 2, 5, 1, 2, 2, 6, 2]   # yellow sequence from image
assert sum(anti_dr[:5]) == 11                  # 1+2+5+1+2=11
assert sum(anti_dr[5:])  == 10                 # 2+6+2=10
assert sum(anti_dr[:5]) + sum(anti_dr[5:]) == 21
assert dr(21) == 3                             # 11+10=21=3

# Alpha palindrome: 3+8=11, 7+3=10
assert 3 + 8 == 11
assert 7 + 3 == 10
assert 3 + 8 + 7 + 3 == 21 and dr(21) == 3    # each half sums to 21

# Bottom sequence
BOTTOM = [11, 122, 133, 315, 744, 155, 962]
assert 962 == 26 * 37
assert sum(BOTTOM) == 2442
assert dr(2442) == 3


if __name__ == '__main__':
    def tag(n):
        t = []
        if is_prime(n):             t.append('p')
        if n in CASCADE_BASE:       t.append('CB')
        if n in SOVEREIGN_ANCHORS:  t.append('SA')
        if n in SOVEREIGN_TARGETS:  t.append('ST')
        if n in PRIMITIVE_ROOTS_37: t.append('PR')
        if n in ALPHA_GRID:         t.append(ALPHA_GRID[n])
        return ','.join(t) if t else '.'

    print("11 as 123-family representative")
    print("=" * 50)
    print()
    print(f"11 + 26 = {11+26}  (additive inverse of 137-map multiplier)")
    print(f"DR(10)={dr(10)}, DR(11)={dr(11)}, DR(10+11)=DR(21)={dr(21)}")
    print(f"137-map orbit of 11: {{11,27,36}}, 36 = -1 mod 37")
    print()
    print("Fibonacci-seed grid: 10^3 ≡ 1 (mod 37) split property")
    print(f"  {'Number':>8}  {'hi':>4}  {'lo':>5}  {'hi+lo':>6}  {'mod37':>6}  tag")
    for num, (hi, lo) in zip(BLUE_NUMBERS, BLUE_SPLITS):
        s = hi + lo
        print(f"  {num:>8}  {hi:>4}  {lo:>5}  {s:>6}  {s%37:>6}  {tag(s%37)}")
    print()
    print("Anti-diagonal DR sequence of grid:")
    print(f"  {' '.join(str(d) for d in anti_dr[:5])} | {' '.join(str(d) for d in anti_dr[5:])}")
    print(f"  sum: {sum(anti_dr[:5])} + {sum(anti_dr[5:])} = {sum(anti_dr)}, DR={dr(sum(anti_dr))}")
    print()
    print("Alpha palindrome:  3-8-7-3 | 3-7-8-3")
    print(f"  3+8={3+8}, 7+3={7+3} -> {3+8}+{7+3}={3+8+7+3}, DR={dr(3+8+7+3)}")
    print()
    print("Bottom sequence:")
    for v in BOTTOM:
        print(f"  {v:>5}: DR={dr(v)}, mod37={v%37} ({tag(v%37)})")
    print(f"  Sum={sum(BOTTOM)}, DR={dr(sum(BOTTOM))}")
    print(f"  962 = 26×37: {962 == 26*37}")
    print()
    print("All assertions passed.")
