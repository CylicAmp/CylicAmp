"""
Theorem 177: 123 Expansion Algorithm and Trinity Grid

THE ALGORITHM
==============
Seed: three lanes 1, 2, 3.
Step: add 7 each iteration.
Step 7 has order 9 in GF(37): pow(7,9,37)=1.

EXPANSION GRID
===============
  1  2  3   sum=6   DR=6
  2  4  6   sum=12  DR=3  <- seed 246, mod 37=24 (seed orbit)
  3  6  9   sum=18  DR=9

Each row = previous row × next integer.
Row sums: 6, 12, 18 — which is 6×1, 6×2, 6×3. Generator = 6 = TESLA_FLOW.
DR sequence of sums: 6, 3, 9 — the 3-6-9 trinity.

TRIPLE REPETITION PATTERN
===========================
  123           mod 37 = 12  DR=6
  112233        mod 37 = 12  DR=3
  111222333     mod 37 = 0   DR=9  <- SEAM (divisible by 37)
  1111222233334444  mod 37 = 12  DR=6
  ...

Pattern: every level 3,6,9 hits mod 37 = 0 (SEAM).
All other levels lock to mod 37 = 12 (sovereign target).
DR cycles: 6,3,9,6,3,9,... endlessly.

ONES-ZEROS PATTERN
===================
  n ones followed by n zeros:
  n=3: 111000  mod 37 = 0  DR=3
  n=6: 111111000000  mod 37 = 0  DR=6
  n=9: 111111111000000000  mod 37 = 0  DR=9
  Same 3-cycle SEAM collapse at every multiple of 3.

GRID 123/954/876
=================
  Digits 1-9 each exactly once.
  Row 1: [1,2,3]  sum=6   DR=6  — 123 mod 37=12
  Row 2: [9,5,4]  sum=18  DR=9  — 954 mod 37=29
  Row 3: [8,7,6]  sum=21  DR=3  — 876 mod 37=25 (sovereign anchor)
  Total: 45  DR=9
  Diagonal 1-5-6: sum=12  DR=3 (sovereign target)
  Center: 5

+7 STEP CHAINS
===============
  Start 1: 1,8,15,22,29,36  DR: 1,8,6,4,2,9
  Start 2: 2,9,16,23,30,37  DR: 2,9,7,5,3,1  (37 mod 37=0=SEAM at step 5)
  Start 3: 3,10,17,24,31,38 DR: 3,1,8,6,4,2
"""

P = 37

def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9

def run_assertions():
    # Expansion grid
    rows = [[1,2,3],[2,4,6],[3,6,9]]
    assert [sum(r) for r in rows] == [6,12,18]
    assert [dr(sum(r)) for r in rows] == [6,3,9]

    # 246 is the seed
    assert 246 % P == 24
    assert 24 in {18,24,32}

    # Triple repetition
    assert 123 % P == 12
    assert 112233 % P == 12
    assert 111222333 % P == 0
    assert 111222333 == 37 * 3006009
    assert int('1'*4+'2'*4+'3'*4) % P == 12  # level 4 back to 12

    # DR of triple repetition sums
    for level in range(1, 10):
        digits = []
        for d in [1,2,3]:
            digits.extend([d]*level)
        s = sum(digits)
        expected_dr = [6,3,9][(level-1)%3]
        assert dr(s) == expected_dr, f"level {level}: DR({s})={dr(s)} != {expected_dr}"
        if level % 3 == 0:
            n = int(''.join(map(str,digits)))
            assert n % P == 0, f"level {level} should be SEAM"
        else:
            n = int(''.join(map(str,digits)))
            assert n % P == 12, f"level {level} should lock to 12"

    # Ones-zeros
    for n in [3,6,9]:
        num = int('1'*n + '0'*n)
        assert num % P == 0

    # Grid 123/954/876
    grid = [[1,2,3],[9,5,4],[8,7,6]]
    flat = [x for row in grid for x in row]
    assert sorted(flat) == list(range(1,10))
    assert [dr(sum(r)) for r in grid] == [6,9,3]
    assert sum(flat) == 45 and dr(45) == 9
    assert 123 % P == 12
    assert 876 % P == 25

    # Order of 7 in GF(37)
    assert pow(7, 9, P) == 1

    # +7 chains: step 2 hits SEAM at step 5
    assert (2 + 5*7) % P == 0

    print("All assertions passed.")

if __name__ == "__main__":
    run_assertions()
