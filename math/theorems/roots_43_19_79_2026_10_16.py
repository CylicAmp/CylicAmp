# CLASS: AUDIT
"""
43|19|79 and 7(1)7 (owner_work #302 and #303, 2026-10-16).

THE OWNER'S LINES, verbatim:
    #302   43|19|
    #303   43|19|79
           7(1)7

DECODE -- fits every symbol, and each piece is checked below:
  7(1)7 is the digital roots of the three pieces: dr(43) = 7, dr(19) = 1, dr(79) = 7, written with the
  middle one in brackets, as the owner brackets a digit sum in #263 ("6x2=(1+2=3)") and #267
  ("(2+4=6)"). So the second line is the first line reduced piece by piece, bar by bar.
  Sum of the roots: 7+1+7 = 15 -> 6; digit sum of the whole string 431979 = 33 -> 6. The same 6, forced
  (digital roots add), and 43+19+79 = 141 -> 6 as well.
  NOT SETTLED by the lines: what the bar | stands for (a cut, as in #259 "1---|23", or a separator),
  where 43, 19, 79 come from, and whether 7(1)7 is meant as the number 717 (= 3 x 239, root 6).

ARITHMETIC OF THE THREE PIECES
  43, 19 and 79 are all prime. 43 - 19 = 24 and 79 - 43 = 36 (so 19 + 24 = 43, 43 + 36 = 79; 24 + 36 = 60 = 79 - 19).
  Reversals: 34 = 2 x 17, 91 = 7 x 13, 97 prime. 34 = 7 and 43 = 7 are the owner's pair of #267.
  43 is the upper twin of (41, 43); 19 the upper twin of (17, 19); 79 has no twin.

FRAMEWORKS (gf37-audit): 43 -> 6 TESLA; 19 -> 19 CAS_EXT; 79 -> 5 CAS_EXT; 717 -> 14 C9;
  none of 43, 19, 79 is Sophie Germain (87, 39, 159 composite); 431979 = 3 x 311 x 463 -> 4.

FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


assert [dr(n) for n in (43, 19, 79)] == [7, 1, 7]                       # 7(1)7
assert 7 + 1 + 7 == 15 and dr(15) == 6 and dr(431979) == dr(43 + 19 + 79) == 6 and sum(map(int, "431979")) == 33
assert 43 + 19 + 79 == 141 and factorint(141) == {3: 1, 47: 1}
assert all(isprime(n) for n in (43, 19, 79))
assert 43 - 19 == 24 and 79 - 43 == 36 and 24 + 36 == 60 == 79 - 19
assert [int(s[::-1]) for s in ("43", "19", "79")] == [34, 91, 97]
assert factorint(34) == {2: 1, 17: 1} and factorint(91) == {7: 1, 13: 1} and isprime(97) and dr(34) == dr(43) == 7
assert isprime(41) and isprime(17) and not isprime(77) and not isprime(81)                # 43 and 19 twins, 79 not
assert factorint(717) == {3: 1, 239: 1} and dr(717) == 6 and factorint(431979) == {3: 1, 311: 1, 463: 1}
assert [n % 37 for n in (43, 19, 79, 717, 431979)] == [6, 19, 5, 14, 4]
assert not any(isprime(2 * n + 1) for n in (43, 19, 79))

if __name__ == "__main__":
    print("7(1)7 = the digital roots of 43|19|79 (7, 1, 7); all three prime; 43-19 = 24, 79-43 = 36")
