# CLASS: AUDIT
"""
Pasted text on emirps and palindromes (2026-11-21): 3-digit overlaps, 5-digit nested palindromes, the four 2-digit
emirp pairs under concatenation and the four operations, the sum 418 -- and the two things it offers next (7-digit
palindromes from 3-digit emirps; the digit-sum and mod-37 map of the 2- and 3-digit emirps), built here. Audit on arrival.

RIGHT, every number:
  2-digit emirps 13 17 31 37 71 73 79 97 (four pairs).  131 313 373 797 prime; 171 = 3^2 x 19, 717 = 3 x 239,
  737 = 11 x 67, 979 = 11 x 89.  The 5 primes 17971 71317 71917 79397 97379 are prime and the 9 factorizations are right.
  1331 = 11^3, 3113 = 11 x 283, 1771 = 7 x 11 x 23, 7117 = 11 x 647, 3773 = 7^3 x 11, 7337 = 11 x 23 x 29,
  7997 = 11 x 727, 9779 = 7 x 11 x 127;  sums 44 88 110 176 = 11 x digit sum;  differences 18 54 36 18 = 9 x digit gap;
  products 403 1207 2701 7663;  quotients 2.3846 4.1765 1.9730 1.2278;  13+31+17+71+37+73+79+97 = 418 = 2 x 11 x 19.
  Forced: abba is a multiple of 11 (every even-length palindrome is); both digits of an emirp are odd, so digit sums and
  digit gaps are even -> multiples of 22 and 18.

WRONG (each changes a result):
  1. "5 prime out of 14 nested combinations": the 14 are not one rule. Nested emirps (ab and bc both emirps, c != a)
     give 10 palindromes, 3 prime (17971, 71317, 97379). 71917 and 79397 do not nest: their inner pairs 19 and 93 are
     not emirps (91 = 7 x 13, 93 = 3 x 31). Taking every emirp e with any middle digit d (e d rev(e)) gives 80, 20 prime.
  2. "7-digit palindromic primes such as 10701 or 1130311": 10701 has 5 digits and is 3^2 x 29 x 41;
     1130311 = 7 x 13 x 12421. Neither is prime.

BUILT -- 7-digit palindromes e d rev(e) from the 28 three-digit emirps: 280 palindromes, 46 prime (listed below).
BUILT -- the map:
  2-digit: digit sums 4 8 4 10 8 10 16 16, roots 4 8 4 1 8 1 7 7; by 37: 13 17 31 0 34 36 5 23; pair sums by 37 7 14 36 28.
  3-digit (28 emirps, total 16370): digit sums 5 8 13 14 16 17 19 20 22; roots 1 2 4 5 7 8 -- never 3, 6, 9, because a
  root of 3, 6 or 9 means divisible by 3 (true of every prime above 3). 22 residues by 37.
  No 3-digit emirp has e + rev(e) divisible by 37: e + rev(e) leaves 27(a+c) + 20b by 37, which is 0 only when
  a + c = 2b, and then the digit sum is 3b, so e divides by 3.

FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime

rev = lambda n: int(str(n)[::-1])
dr = lambda n: 1 + (n - 1) % 9
EM2 = [n for n in range(10, 100) if isprime(n) and isprime(rev(n)) and rev(n) != n]
EM3 = [n for n in range(100, 1000) if isprime(n) and isprime(rev(n)) and rev(n) != n]
assert EM2 == [13, 17, 31, 37, 71, 73, 79, 97] and len(EM3) == 28 and sum(EM3) == 16370

# the paste's numbers
assert [isprime(n) for n in (131, 313, 373, 797)] == [True] * 4
assert [factorint(n) for n in (171, 717, 737, 979)] == [{3: 2, 19: 1}, {3: 1, 239: 1}, {11: 1, 67: 1}, {11: 1, 89: 1}]
P5 = [17971, 71317, 71917, 79397, 97379]
C5 = {13731: {3: 1, 23: 1, 199: 1}, 17371: {29: 1, 599: 1}, 31713: {3: 1, 11: 1, 31: 2}, 37173: {3: 1, 12391: 1},
      37973: {13: 1, 23: 1, 127: 1}, 73137: {3: 1, 24379: 1}, 73937: {107: 1, 691: 1}, 79197: {3: 1, 26399: 1},
      97179: {3: 1, 29: 1, 1117: 1}}
assert all(isprime(n) for n in P5) and all(factorint(n) == f for n, f in C5.items())
TABLE = {(13, 31): ({11: 3}, {11: 1, 283: 1}, 44, 18, 403, 2.3846), (17, 71): ({7: 1, 11: 1, 23: 1}, {11: 1, 647: 1}, 88, 54, 1207, 4.1765),
         (37, 73): ({7: 3, 11: 1}, {11: 1, 23: 1, 29: 1}, 110, 36, 2701, 1.9730), (79, 97): ({11: 1, 727: 1}, {7: 1, 11: 1, 127: 1}, 176, 18, 7663, 1.2278)}
for (a, b), (fab, fba, s, d, m, q) in TABLE.items():
    assert factorint(int(f"{a}{b}")) == fab and factorint(int(f"{b}{a}")) == fba
    assert (a + b, b - a, a * b, round(b / a, 4)) == (s, d, m, q)
    da, db = divmod(a, 10)
    assert a + b == 11 * (da + db) and b - a == 9 * (db - da) and (a + b) % 22 == 0 and (b - a) % 18 == 0
assert sum(EM2) == 418 and factorint(418) == {2: 1, 11: 1, 19: 1}
assert all(int(str(n) + str(n)[::-1]) % 11 == 0 for n in range(10, 10000))   # even-length palindromes divide by 11

# fault 1: the 14 five-digit palindromes
nested = [int(f"{a}{b}{c}{b}{a}") for a in "1379" for b in "1379" for c in "1379"
          if int(a + b) in EM2 and int(b + c) in EM2 and a != c]
assert len(nested) == 10 and [n for n in nested if isprime(n)] == [17971, 71317, 97379]
assert set(P5) | set(C5) != set(nested) and 71917 not in nested and 79397 not in nested
assert 19 not in EM2 and factorint(91) == {7: 1, 13: 1} and factorint(93) == {3: 1, 31: 1}
five = [int(f"{e}{d}{str(e)[::-1]}") for e in EM2 for d in range(10)]
assert len(five) == 80 and sum(isprime(n) for n in five) == 20

# fault 2: the examples
assert len("10701") == 5 and factorint(10701) == {3: 2, 29: 1, 41: 1} and factorint(1130311) == {7: 1, 13: 1, 12421: 1}

# built: 7-digit palindromes from 3-digit emirps
seven = [int(f"{e}{d}{str(e)[::-1]}") for e in EM3 for d in range(10)]
P7 = [n for n in seven if isprime(n)]
assert len(seven) == 280 and len(P7) == 46 and all(str(n) == str(n)[::-1] for n in seven)
assert P7[:5] == [1074701, 1134311, 1490941, 1496941, 1572751] and P7[-1] == 9919199

# built: the map
assert [sum(map(int, str(e))) for e in EM2] == [4, 8, 4, 10, 8, 10, 16, 16] and [dr(e) for e in EM2] == [4, 8, 4, 1, 8, 1, 7, 7]
assert [e % 37 for e in EM2] == [13, 17, 31, 0, 34, 36, 5, 23] and [(a + b) % 37 for a, b in TABLE] == [7, 14, 36, 28]
assert sorted({sum(map(int, str(e))) for e in EM3}) == [5, 8, 13, 14, 16, 17, 19, 20, 22]
assert sorted({dr(e) for e in EM3}) == [1, 2, 4, 5, 7, 8] and len({e % 37 for e in EM3}) == 22
assert not [e for e in EM3 if (e + rev(e)) % 37 == 0]
assert all(((27 * (a + c) + 20 * b) % 37 == 0) == (a + c == 2 * b) for a in range(10) for b in range(10) for c in range(10))
assert all(int(f"{a}{(a + c) // 2}{c}") % 3 == 0 for a in range(1, 10) for c in range(10) if (a + c) % 2 == 0)

if __name__ == "__main__":
    print("emirp paste: every number right; nested emirps give 10 palindromes, 3 prime (not 5 of 14);")
    print("10701 and 1130311 are not prime; 7-digit e d rev(e): 46 of 280 prime;", P7)
