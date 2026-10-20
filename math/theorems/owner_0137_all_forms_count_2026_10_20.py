# CLASS: AUDIT
"""
Every form of 0.137 by the owner's moves, counted both ways (owner_work #380, 2026-10-20: "now do the same with 0.137"). Same rule as #378 and #379
(owner_0125_all_forms_count_2026_10_20.py): take units off any digit, put them onto any digit or as new digits on the left or right; the total of the
digits is kept; every count is given with zero and without zero. Process entry: owner_work/PROCESS.md, #380.

THE TOTAL KEPT: 0.137 → 1+3+7 = 11.
  Examples by the owner's moves: take 2 from the 7 → 0.135 → put the 2 in front as 2 → 2.135, as 1 1 → 11.135, on the right → 0.1352, 0.13511,
  onto the first digit → 0.335 ; every one adds to 11.
DIFFERENCE FROM 0.125: a digit can be at most 9, and 11 is bigger than 9. So 11 cannot sit in one digit, and 10 + 1 / 1 + 10 cannot either:
  the ways to write 11 as digits in a row are 2^10 - 3 = 1024 - 3 = 1021 (for 8 it was 2^7 = 128, with no cap reached).

WITHOUT ZERO (digits 1 to 9, at least one digit after the point):
  by number of digits: 1 digit 0, 2 digits 8, 3 digits 45, 4 digits 120, 5 digits 210, 6 digits 252, 7 digits 210, 8 digits 120, 9 digits 45, 10 digits 10,
  11 digits 1 → 1021 digit strings.
  with the point: 2x8 + 3x45 + 4x120 + 5x210 + 6x252 + 7x210 + 8x120 + 9x45 + 10x10 + 11x1 = 6139 ; with whole numbers too: 6139 + 1021 = 7160.
WITH ZERO (zeros allowed among the digits; the part before the point is "0" or does not start with 0; at least one digit after the point):
  by number of digits: 0, 16, 191, 1185, 5308, 19292, 60297, 167791, 425429, 999091, 2199945 for 1 to 11 digits;
  up to 11 digits, the longest form without zero: 3878545. No last length (another 0 always fits).
  For n digits: S(n) + (n-1)(S(n) - S(n-1)), with S(n) = C(n+10, n-1) - n x n the n-digit strings that add to 11 (the n x n removes a 10 or 11 digit).
  Example, 2 digits with zero: 29 38 47 56 65 74 83 92 → 0.29 .. 0.92 (8) and 2.9 .. 9.2 (8) → 16 ; without zero the same 16 (no 2-digit string adding
  to 11 has a 0).
FRAMEWORKS (gf37-audit): 11 = 11 NEG_H (prime) ; 1021 prime, twin with 1019, = 22 NQR17 ; 6139 = 7x877 = 34 D7 ; 7160 = 2x2x2x5x179 = 19 CAS_EXT ;
  3878545 = 5x11x97x727 = 20 DARK_A ; 137 = 26 IC.

FALSIFICATION: any assertion failing.
"""
from itertools import product
from math import comb

from sympy import factorint, isprime

T = 1 + 3 + 7
assert T == 11


def compositions(n, cap=9):
    if n == 0:
        yield ()
        return
    for first in range(1, min(n, cap) + 1):
        for rest in compositions(n - first, cap):
            yield (first,) + rest


comps = list(compositions(T))
assert len(comps) == 1021 == 2 ** 10 - 3 and len(list(compositions(T, cap=99))) == 1024
by_len = {k: sum(1 for c in comps if len(c) == k) for k in range(1, 12)}
assert list(by_len.values()) == [0, 8, 45, 120, 210, 252, 210, 120, 45, 10, 1]
assert all(by_len[k] == comb(10, k - 1) for k in range(3, 12)) and by_len[2] == 10 - 2 and by_len[1] == 1 - 1


def forms(allow_whole=False):
    out = set()
    for c in comps:
        s = "".join(map(str, c))
        for cut in range(0, len(s) + (1 if allow_whole else 0)):
            left, right = s[:cut], s[cut:]
            out.add((left or "0") + ("." + right if right else ""))
    return out


F = forms()
assert len(F) == 6139 == sum(k * v for k, v in by_len.items()) and len(forms(True)) == 7160 == 6139 + 1021
for e in ("0.137", "2.135", "11.135", "0.1352", "0.13511", "0.335"):
    assert e in F and sum(int(ch) for ch in e if ch.isdigit()) == 11


def S(n):
    return comb(n + 10, n - 1) - n * n


def with_zero_formula(n):
    return S(1) if n == 1 else S(n) + (n - 1) * (S(n) - S(n - 1))


def with_zero_brute(n):
    total = 0
    for digs in product(range(10), repeat=n):
        if sum(digs) != T:
            continue
        for cut in range(0, n):
            if cut >= 1 and digs[0] == 0:
                continue
            total += 1
    return total


assert [with_zero_brute(n) for n in range(1, 6)] == [with_zero_formula(n) for n in range(1, 6)] == [0, 16, 191, 1185, 5308]
wz = [with_zero_formula(n) for n in range(1, 12)]
assert wz == [0, 16, 191, 1185, 5308, 19292, 60297, 167791, 425429, 999091, 2199945] and sum(wz) == 3878545
assert S(2) == 8 and wz[1] == 16

assert isprime(11) and isprime(1021) and isprime(1019) and 1021 % 37 == 22
assert factorint(6139) == {7: 1, 877: 1} and factorint(7160) == {2: 3, 5: 1, 179: 1} and factorint(3878545) == {5: 1, 11: 1, 97: 1, 727: 1}
assert (6139 % 37, 7160 % 37, 3878545 % 37, 137 % 37) == (34, 19, 20, 26)

if __name__ == "__main__":
    print("0.137 (keeps 11): without zero 6139 (7160 with whole numbers; 1021 digit strings); with zero 3878545 up to 11 digits")
