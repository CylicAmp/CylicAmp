# CLASS: LEMMA
"""
Owner, 2026-10-04: "3 x 11 = 33 = 6 = 33, 222, 111111 = (246) / = 246 poly
math twin primes connections perhaps".

THE SPLIT: 33 -> 3+3 = 6, and 6 = 3+3 = 2+2+2 = 1+1+1+1+1+1 -- the same move as
8 = 4+4 = 2+2+2+2 = eight 1s (ladder_loops_squares.py), where the part counts
2, 4, 8 read 248. For 6 the part counts are 2, 3, 6, which read 236; the
owner wrote 246, the pipeline's reference seed, one key from 236. Both are
checked below.

TWIN PRIMES -- the real connection:
  Every twin-prime pair above (3, 5) is (6k-1, 6k+1): one of three consecutive
  numbers is divisible by 3 and the middle one must be, and it is even. So
  twin-prime centres are multiples of 6. 6 itself -- the digit sum of 33 --
  is the centre of (5, 7).
  3 and 11 are both lower twins: (3, 5) and (11, 13).
  246 = 6 x 41 is a multiple of 6 but not a centre: 245 = 5 x 7^2, 247 = 13 x 19.
  236 is not a multiple of 6. 248 neither.
  (138 is a centre: (137, 139) -- 137 is a twin prime.)

THE LADDER ROWS AS TWIN CENTRES: every 4-piece ladder row is divisible by 6
(digit_ladder_12312_91128.py), so every row is eligible. Seven of rows 1-144
are centres of twin primes:
    row 9   91128   (91127, 91129)     row 14  56238   (56237, 56239)
    row 44  89898   (89897, 89899)     row 66  347142  (347141, 347143)
    row 81  911172  (911171, 911173)   row 116 898242  (898241, 898243)
    row 131 562272  (562271, 562273)
  Baseline: multiples of 6 of the same sizes are twin centres 4.6-6.8% of the
  time, which predicts about 7.6 of 144. Seven is ordinary -- the rows qualify
  because they are multiples of 6, and then hit at the usual rate. Row 9,
  91128, the last row of the owner's original ladder image, is one of them.

FALSIFICATION: any assertion below failing.
"""
from sympy import isprime

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def row(a):
    return int(f"{dr(a)}{dr(a + 1)}{dr(2 * a + 1)}{2 * a + 10}")

def centre(n):
    return isprime(n - 1) and isprime(n + 1)

assert 3 * 11 == 33 and dr(33) == 6 == 3 + 3 == 2 + 2 + 2 == 6 * 1
assert all(n % 6 == 0 for n in range(5, 100000) if centre(n))
assert centre(6) and centre(138) and isprime(137)
assert centre(4) and centre(6)
assert isprime(3) and isprime(5) and isprime(11) and isprime(13)
assert 246 == 6 * 41 and not centre(246) and 245 == 5 * 49 and 247 == 13 * 19
assert 236 % 6 and not centre(236) and not centre(248)
assert all(row(a) % 6 == 0 for a in range(1, 145))
HITS = [a for a in range(1, 145) if centre(row(a))]
assert HITS == [9, 14, 44, 66, 81, 116, 131]
assert [row(a) for a in HITS] == [91128, 56238, 89898, 347142, 911172, 898242, 562272]

if __name__ == "__main__":
    for a in HITS:
        print(a, row(a), (row(a) - 1, row(a) + 1))
    print("all assertions pass")
