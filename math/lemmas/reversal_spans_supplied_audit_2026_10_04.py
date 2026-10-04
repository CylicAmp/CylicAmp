# CLASS: AUDIT
"""
Audit of supplied tables (2026-10-04): the spans 12..21, 13..31, 14..41 -- each
from a two-digit number ab to its reversal ba -- with kind, digit sum, n mod 9,
running sum and primes so far; plus the owner's lines
    10+45=5+4=9
    1+9=1

REPRODUCED: every digit sum, residue, running sum, prime count and gap in all
three tables. Primes 13,17,19 | 13,17,19,23,29,31 | 17,19,23,29,31,37,41.
(Two mismatches in the first check were transcription slips in the audit, not
in the tables.)

FORCED BY THE REVERSAL (proved for every ab -> ba, a < b):
  - Both ends have the same digit sum a+b (3, 4, 5): reversal keeps the digits.
  - The span has 9(b-a)+1 numbers: 10, 19, 28 -- digital root 1 every time.
    "1+9=1": 19 -> 1+9 = 10 -> 1.
  - The total is (ab+ba)(9(b-a)+1)/2 = 11(a+b)(9(b-a)+1)/2: 165, 418, 770,
    all multiples of 11 (ab + ba = 11(a+b)).
  - The total reduces to a+b: 165 -> 3, 418 -> 4, 770 -> 5. Mod 9, 11 = 2,
    9(b-a)+1 = 1 and halving is x5, so total = 2*5*(a+b) = a+b.
  So the opening digit sum, the closing digit sum and the whole span's total
  all reduce to the same number.

THE OWNER'S LINE 10+45=5+4=9: 45 -> 4+5 = 9, and written backwards 5+4 = 9 --
reversal keeps the digit sum, the same law as the spans' ends. 10 -> 1, and
1+9 = 10 -> 1; 10+45 = 55 -> 5+5 = 10 -> 1. (10 is the length of the 12..21
span; 45 is the running sum at 16 in the 14..41 span and also 1+2+...+9.)

"RUNNING SUMS THAT LAND ON VALUES PRODUCED BY THE CUTS":
  27, 45 and 144 are splits of 1413, the first zero's digits (14+13, 1+41+3,
  141+3; collatz_zeros_supplied_audit_2026_10_04.py). 99, 198, 315 and 729
  are NOT splits of 1413; no cut producing them is defined in the supplied text.
  All seven are multiples of 9, and running sums hit multiples of 9 often.

SPAN 15..51 (owner: "keep going to 15 through 51"):
  37 numbers (9(5-1)+1); total 1221 = 3 x 11 x 37 = 11 x 6 x 37 / 2, reduces
  to 6 = 1+5 = 5+1. Primes 17, 19, 23, 29, 31, 37, 41, 43, 47 (nine), gaps
  2, 4, 6, 2, 6, 4, 2, 4. Digit sum 9 at 18, 27, 36, 45. Opens and closes on
  digit sum 6. Running sum 841 = 29^2 at 43.
  Running sums divisible by 9 come in pairs every 9 numbers -- (21, 126),
  (23, 171), (30, 360), (32, 423), (39, 675), (41, 756), (48, 1071), (50, 1170)
  -- forced: the sum 15..n is (n^2 + n - 210)/2, which is 0 mod 9 exactly
  when n = 3 or 5 mod 9.
  The span length 37 is forced by 15 -> 51 (b - a = 4); 37 is in it because
  the problem puts it there. (1221 reads as 12|21, the ends of the first span;
  that is this one total, not a law.)

10 THROUGH 19 (owner: "10+45=5+4=9 / 1+9=1+9=1"):
  The ten numbers 10..19 have tens digits 1+1+...+1 = 10 and units digits
  0+1+...+9 = 45. Their digits all together: 10 + 45 = 55 -> 5+5 = 10 -> 1.
  45 -> 4+5 = 9 (and 5+4 = 9 reversed); 10 -> 1; 1+9 = 10 -> 1. The last
  number, 19, gives the same: 1+9 = 10 -> 1. Their sum 145 = 100 + 45 also
  reduces to 1 (a sum and its digit sums agree mod 9).

FALSIFICATION: any assertion below failing.
"""
from sympy import isprime

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def ds(n):
    return sum(map(int, str(n)))

SUPPLIED = {
    (12, 21): ([3, 4, 5, 6, 7, 8, 9, 10, 2, 3], [12, 25, 39, 54, 70, 87, 105, 124, 144, 165],
               [0, 1, 1, 1, 1, 2, 2, 3, 3, 3]),
    (13, 31): ([4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 3, 4],
               [13, 27, 42, 58, 75, 93, 112, 132, 153, 175, 198, 222, 247, 273, 300, 328, 357, 387, 418],
               [1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 6]),
    (14, 41): ([5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 4, 5],
               [14, 29, 45, 62, 80, 99, 119, 140, 162, 185, 209, 234, 260, 287, 315, 344, 374, 405, 437,
                470, 504, 539, 575, 612, 650, 689, 729, 770],
               [0, 0, 0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 7]),
}
for (lo, hi), (DS, RS, PR) in SUPPLIED.items():
    ns = list(range(lo, hi + 1))
    assert DS == [ds(n) for n in ns]
    assert RS == [sum(ns[:i + 1]) for i in range(len(ns))]
    assert PR == [sum(isprime(m) for m in ns[:i + 1]) for i in range(len(ns))]
assert [p for p in range(14, 42) if isprime(p)] == [17, 19, 23, 29, 31, 37, 41]

for a in range(1, 9):
    for b in range(a + 1, 10):
        lo, hi = 10 * a + b, 10 * b + a
        ns = range(lo, hi + 1)
        assert ds(lo) == ds(hi) == a + b
        assert len(ns) == 9 * (b - a) + 1 and dr(len(ns)) == 1
        assert sum(ns) == 11 * (a + b) * (9 * (b - a) + 1) // 2 and sum(ns) % 11 == 0
        assert dr(sum(ns)) == dr(a + b)
assert [sum(range(l, h + 1)) for l, h in ((12, 21), (13, 31), (14, 41))] == [165, 418, 770]
assert [dr(x) for x in (165, 418, 770)] == [3, 4, 5]

assert ds(45) == ds(54) == 9 and dr(10) == 1 and dr(1 + 9) == 1 and dr(10 + 45) == 1
assert sum(range(1, 10)) == 45 and SUPPLIED[(14, 41)][1][2] == 45
SPLITS_1413 = {1413, 414, 27, 18, 144, 45, 9}
CUT_VALUES = [27, 45, 99, 144, 198, 315, 729]
assert [v for v in CUT_VALUES if v in SPLITS_1413] == [27, 45, 144]
assert all(v % 9 == 0 for v in CUT_VALUES) and 729 == 3 ** 6

ns = list(range(15, 52))
R = [sum(ns[:i + 1]) for i in range(len(ns))]
assert len(ns) == 37 and R[-1] == 1221 == 3 * 11 * 37 and dr(1221) == 6
assert [p for p in ns if isprime(p)] == [17, 19, 23, 29, 31, 37, 41, 43, 47]
assert [n for n in ns if ds(n) == 9] == [18, 27, 36, 45] and ds(15) == ds(51) == 6
assert R[ns.index(43)] == 841 == 29 ** 2
assert [n for n in ns if R[ns.index(n)] % 9 == 0] == [21, 23, 30, 32, 39, 41, 48, 50]
assert all(((n * n + n - 210) // 2 % 9 == 0) == (n % 9 in (3, 5)) for n in range(15, 2000))
tens, units = sum(n // 10 for n in range(10, 20)), sum(n % 10 for n in range(10, 20))
assert (tens, units) == (10, 45) and sum(ds(n) for n in range(10, 20)) == 55
assert dr(55) == dr(10) == dr(19) == dr(145) == 1 and sum(range(10, 20)) == 145 == 100 + 45

if __name__ == "__main__":
    print("all assertions pass")
