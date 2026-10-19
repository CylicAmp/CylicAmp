# CLASS: AUDIT
"""
The pasted script on 1/998001, magic constants, cuban numbers, Fe24Ni24Cr18O18, QNR mod 17 and the
chain 13, 413, 11651, 245031 (owner_work #343, 2026-10-19). Audit on arrival.

THE PASTE: a Python script and its printed output, relayed by the owner (another tool's script; its
origin is not stated). Nothing below puts a claim of the script in the owner's mouth.

PRIOR ART (found by grep before writing; they already hold the first block):
  math/theorems/repunit_square_998001.py (T415) -- 1/998001 = 0.000 001 002 003 ... 997 999,
      period 2997 = 3 x 999, the series x^2/(1-x)^2 at x = 1/1000.
  math/theorems/period_999_2997.py (T383) -- ord_729(10) = 81, ord_1369(10) = 111, 2997 = 3^4 x 37.
  What is new here: the full order test, the two faults in the pasted script, the sum of the
  triplets, and the link between 369 and 271 through 11111 = 41 x 271.

RIGHT (every printed line re-run, all match):
  999x999 = 998001 = 3^6 x 37^2
  ord of 10 mod 3^6 = 81, mod 37^2 = 111, lcm = 2997 = 81x37
  10^2997 = 1 mod 998001
  repetend = 2997 digits = 999 triplets, 999 different, only 998 missing
  137 x 729927 = 99999999 ; 10^3 = 1 mod 37
  magic constants n(n^2+1)/2 : 3->15, 5->65, 7->175, 9->369, 11->671, 13->1105
  cuban numbers 3n^2+3n+1 : 1, 7, 19, 37, 61, 91, 127, 169, 217, 271 ; C3 = 37, C6 = 127, C9 = 271
  24+24+18+18 = 84
  QNR mod 17 = 3, 5, 6, 7, 10, 11, 12, 14 ; 5 is in the list
  13 prime, 413 = 7x59, 11651 = 61x191, 245031 = 3x81677 ; ratios 31.769, 28.211, 21.031

WRONG (two faults in the pasted script):
  1. "around the 999 boundary" prints triplets[330:336] = 330 331 332 333 334 335.
     That is not the boundary. The boundary is triplets[995:] = 995 996 997 999.
  2. The order test is  pow(10, 2997//3, N) != 1  (10^999 only).
     2997 = 3^4 x 37 has two maximal divisors, 999 and 81. 10^81 must be tested too:
     10^81 mod 998001 != 1 and 10^999 mod 998001 != 1 together make the order exactly 2997.

NOT CHECKABLE: where the Fe24Ni24Cr18O18 formula and the chain 13 -> 413 -> 11651 -> 245031 come from.
  "I can't check this": the paste does not say what the formula is a formula of, or how each
  number of the chain is produced from the one before.

NEW LINES, owner's notation:
  998001 = 999x999 ; 999 = 27x37 ; 998001 = 729x1369
  triplets 000 001 002 ... 997 999 : 998 + 1 = 999 triplets ; 999 triplets x 3 digits = 2997
  the sum of the triplets = 0+1+2+...+997+999 = 497503+999 = 498502 = 499500-998
  triplet number 123 sits at place 123 (123 = 3x41)
  369 = 9x41 ; 271 prime ; 41x271 = 11111 ; 369 and 271 both divide 11111x9 = 99999 : 1/369 = 0.00271 (period 5)
  4x4x4-3x3x3 = 64-27 = 37 ; 7x7x7-6x6x6 = 343-216 = 127 ; 10x10x10-9x9x9 = 1000-729 = 271
  9x82/2 = 369 = 9x41 ; 1+2+3+...+81 = 3321 = 9x369
  271 = 269+2 ; 538 = 2x269 : 269 and 271 are a twin pair
  24+18 = 42 ; 84 = 2x42 ; 84 = 12x7

RESIDUES mod 37 (gf37-audit): 998001 SEAM(0), 2997 SEAM, 999 SEAM, 369 NEG_H(36), 271 SA_ST_A(12),
  127 SA_ST_A(16), 413 TESLA(6), 11651 D7(33), 245031 NQR17(17), 84 IC(10), 13 CAS_EXT(13).

FALSIFICATION: any assertion failing.
"""
import math
from sympy import factorint, isprime

N = 998001

# --- RIGHT ---
assert 999 * 999 == N == 3**6 * 37**2
assert pow(10, 81, 3**6) == 1 and pow(10, 27, 3**6) != 1                  # order mod 3^6 is 81
assert pow(10, 111, 37**2) == 1 and pow(10, 3, 37**2) != 1 and pow(10, 37, 37**2) != 1   # 111
assert math.lcm(81, 111) == 2997 == 81 * 37
assert pow(10, 2997, N) == 1

# --- WRONG 2: the pasted order test is not enough; the full one ---
assert pow(10, 2997 // 3, N) != 1          # the pasted test, passes
assert pow(10, 2997 // 37, N) != 1         # 10^81, the test the paste leaves out, passes too
assert [d for d in range(1, 2998) if 2997 % d == 0 and pow(10, d, N) == 1] == [2997]   # order is exactly 2997

digits = str(10**2997 // N).zfill(2997)
triplets = [digits[i:i + 3] for i in range(0, 2997, 3)]
assert len(digits) == 2997 and len(triplets) == 999 == len(set(triplets))
assert sorted(set(f"{i:03d}" for i in range(1000)) - set(triplets)) == ["998"]
assert triplets[:3] == ["000", "001", "002"] and triplets[123] == "123"
assert all(triplets[i] == f"{i:03d}" for i in range(998)) and triplets[998] == "999"

# --- WRONG 1: the slice the paste labels "the 999 boundary" ---
assert triplets[330:336] == ["330", "331", "332", "333", "334", "335"]
assert triplets[995:] == ["995", "996", "997", "999"]

# --- new lines ---
assert sum(map(int, triplets)) == 498502 == 499500 - 998 == sum(range(1000)) - 998
assert sum(map(int, triplets)) == sum(range(998)) + 999 == 497503 + 999
assert 123 == 3 * 41 and 369 == 9 * 41 and isprime(271) and 41 * 271 == 11111
assert 11111 * 9 == 99999 and 99999 % 369 == 0 and 99999 // 369 == 271
assert str(10**5 // 369).zfill(5) == "00271" and pow(10, 5, 369) == 1
assert 137 * 729927 == 99999999 and pow(10, 3, 37) == 1 and str(10**3 // 37).zfill(3) == "027"
assert str(10**8 // 137).zfill(8) == "00729927"

magic = {n: n * (n * n + 1) // 2 for n in (3, 5, 7, 9, 11, 13)}
assert magic == {3: 15, 5: 65, 7: 175, 9: 369, 11: 671, 13: 1105}
assert 9 * 82 // 2 == 369 == 9 * 41 and sum(range(1, 82)) == 3321 == 9 * 369

cub = [3 * n * n + 3 * n + 1 for n in range(10)]
assert cub == [1, 7, 19, 37, 61, 91, 127, 169, 217, 271]
assert (cub[3], cub[6], cub[9]) == (37, 127, 271) and cub[3] == 4**3 - 3**3 and cub[6] == 7**3 - 6**3 == 127 == 2**7 - 1
assert cub[9] == 10**3 - 9**3 == 1000 - 729 == 271
assert [isprime(c) for c in cub] == [False, True, True, True, True, False, True, False, False, True]
assert factorint(91) == {7: 1, 13: 1}
assert isprime(269) and isprime(271) and 538 == 2 * 269

assert 24 + 24 + 18 + 18 == 84 == 2 * (24 + 18) == 12 * 7
qnr = [a for a in range(1, 17) if pow(a, 8, 17) == 16]
assert qnr == [3, 5, 6, 7, 10, 11, 12, 14] and 5 in qnr

chain = [13, 413, 11651, 245031]
assert [factorint(v) for v in chain] == [{13: 1}, {7: 1, 59: 1}, {61: 1, 191: 1}, {3: 1, 81677: 1}]
assert isprime(81677)
assert [round(chain[i + 1] / chain[i], 3) for i in range(3)] == [31.769, 28.211, 21.031]
assert [v % 37 for v in chain] == [13, 6, 33, 17]
assert [x % 37 for x in (998001, 2997, 999, 369, 271, 127, 84)] == [0, 0, 0, 36, 12, 16, 10]

if __name__ == "__main__":
    print("1/998001: 999x999=998001=3^6x37^2, order of 10 = 2997 (10^81 and 10^999 both different from 1), "
          "999 triplets, 998 missing; the paste's two faults: the slice label (330:336 is not the boundary, 995: is) "
          "and the order test (10^81 left out); 369=9x41, 271 | 11111=41x271")
