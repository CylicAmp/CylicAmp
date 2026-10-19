# CLASS: AUDIT
"""
A pasted "verification" of 123, 654, 789 (owner_work #357, 2026-10-19). Third-party text; it opens with "Every line
verifies. This document is clean -- no corrections needed." Nothing below is put in the owner's mouth.

RIGHT (every line re-run):
  123=1+2+3=6, 654=6+5+4=15=6, 789=7+8+9=24=6
  123=3x37+12, 654=17x37+25, 789=21x37+12 ; 12+25+12=49=12
  123+654+789=1566=1+5+6+6=18=9 ; 1566=42x37+12
  654-456=198=99x(6-4) ; 123+456+789=1368 ; 1368+198=1566
  1368=37x37-1=36 mod 37, 198=5x37+13, 36+13=49=12 ; 198=9x22
  654=2x3x109, 1566=2x3x3x3x29, 198=2x3x3x11
  198=743-545 ; 7+4+3=14=5 and 5+4+5=14=5 (equal roots)
WRONG:
  "12 is the residue class of the session's 111 (=3x37)": 111=3x37=0 mod 37, not 12. 123=111+12 is where the 12 is.
  "Every claim checks, no corrections needed": the line above is a correction.
CAN'T CHECK:
  "the increment 11 rides the reversal offset": no increment is named; what is true: 198=18x11.
  "the exact mod-9 equivalence bridge from the four-number set": no four-number set with 743 and 545 is in the repository
    or in the owner's messages (545 is in T280 with 454, 454+545=999; 743 appears nowhere). 743-545=198 is right, and it is forced:
    two numbers with the same digital root differ by a multiple of 9.
  "the F_37 generator layer": 12 is not a generator of the multiplicative group (its order is 9; the generators are
    2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35). 12 does generate the subgroup of order 9, {1,7,9,10,12,16,26,33,34}
    = IC + SA_ST_A + D7 (the H_9 layer of T118). Which of the two the paste means is not said.
FORCED (true for every reversal of three digits, no information about 123/654/789):
  reversing abc gives an offset 99(c-a) = 9x11x(c-a): a multiple of 9, so the digital root cannot change ("mod-9
  transparent"); 99=25 mod 37, so the offset is 25(c-a) mod 37, 13 for c-a=2. The three rows 123, 456, 789 of the
  1..9 grid all have root 6 because they are 3 consecutive digits (sums 6, 15, 24).

CONNECTIONS (the owner's lines and files):
  1368=123+456+789 and 1566=123+654+789 are the sums of #354 (pasted_123456789_output_audit_2026_10_19.py); 1368=37x37-1.
  198=2x99 is the period of 1/9801 (the 198 of the 1/(10^k-1)^2 family, same file: periods 9, 198, 2997).
  1566=12 mod 37 and 12 is the owner's 12 (9+3=12, #268).

FALSIFICATION: any assertion failing.
"""
from sympy import factorint, n_order


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


assert [dr(n) for n in (123, 654, 789)] == [6, 6, 6] and 6 + 5 + 4 == 15 and 7 + 8 + 9 == 24
assert [(n // 37, n % 37) for n in (123, 654, 789)] == [(3, 12), (17, 25), (21, 12)] and 12 + 25 + 12 == 49 and 49 % 37 == 12
assert 123 + 654 + 789 == 1566 and dr(1566) == 9 and 1 + 5 + 6 + 6 == 18 and 1566 == 42 * 37 + 12
assert 654 - 456 == 198 == 99 * (6 - 4) and 123 + 456 + 789 == 1368 and 1368 + 198 == 1566
assert 1368 == 37 * 37 - 1 and 1368 % 37 == 36 and 198 == 5 * 37 + 13 and (36 + 13) % 37 == 12 and 198 == 9 * 22
assert factorint(654) == {2: 1, 3: 1, 109: 1} and factorint(1566) == {2: 1, 3: 3, 29: 1} and factorint(198) == {2: 1, 3: 2, 11: 1}
assert 743 - 545 == 198 and dr(743) == dr(545) == 5 and 198 % 9 == 0

# wrong: 111 is 0 mod 37, and 12 sits in 123 = 111 + 12
assert 111 == 3 * 37 and 111 % 37 == 0 and 123 == 111 + 12 and 111 % 37 != 12

# generator layer
assert n_order(12, 37) == 9 and 12 not in [a for a in range(1, 37) if n_order(a, 37) == 36]
H9 = sorted({pow(12, k, 37) for k in range(1, 10)})
assert H9 == [1, 7, 9, 10, 12, 16, 26, 33, 34] == sorted({1, 10, 26} | {9, 12, 16} | {7, 33, 34})
assert sorted(a for a in range(1, 37) if n_order(a, 37) == 36) == [2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35]

# forced: every reversal of three digits
for a in range(1, 10):
    for c in range(1, 10):
        for b in range(10):
            x, y = 100 * a + 10 * b + c, 100 * c + 10 * b + a
            assert y - x == 99 * (c - a) and (y - x) % 9 == 0 and dr(x) == dr(y) and (y - x) % 37 == 25 * (c - a) % 37
assert 99 % 37 == 25 and 25 * 2 % 37 == 13
assert [sum(range(s, s + 3)) for s in (1, 4, 7)] == [6, 15, 24] and [dr(v) for v in (6, 15, 24)] == [6, 6, 6]
assert 198 == 2 * 99 and 198 // 11 == 18 and 454 + 545 == 999 and 545 % 37 == 27

# connections
def repetend_len(num, den):
    r, seen, i = num, {}, 0
    while r not in seen:
        seen[r] = i
        r = r * 10 % den
        i += 1
    return i - seen[r]


assert repetend_len(1, 9801) == 198 and 1566 % 37 == 12

if __name__ == "__main__":
    print("123, 654, 789: all sums and residues right; 111 is 0 mod 37 (12 is in 123=111+12); 12 has order 9, "
          "generates 1,7,9,10,12,16,26,33,34; 198=2x99 is the period of 1/9801; 743 and the four-number set are not in the repo")
