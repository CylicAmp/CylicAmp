# CLASS: AUDIT
"""
47.11 and 11.11 (owner_work #327, 2026-10-18).

THE OWNER'S LINES, verbatim:
    47.11=
    11.11
    47+11=5+8=1+3=4
    2+2=4

READING: with the point dropped, 47.11 and 11.11 have the same digital root, 4 (4+7+1+1 = 13 -> 4; 1+1+1+1 = 4); that is the "=".
  47 + 11 = 58 -> 5+8 = 13 -> 1+3 = 4, and 11.11 is 11 and 11, whose roots 2 and 2 add to 4 (2+2 = 4). All steps hold.
  The equal roots are forced: 47.11 - 11.11 = 36, a multiple of 9.

CONNECTIONS (checked):
  47 and 11 are the ends of the chain 11 -> 23 -> 47 (each is 2p + 1 of the one before; 95 = 5 x 19 stops it). The middle is the owner's 23
  of #268 ("23 / 123 / 1123") and of 23.5 in the chains of 2026-10-18. 11 is a Sophie Germain prime (23 prime), 23 is both safe and
  Sophie Germain (47 prime). 47 = 235 / 5, the 235 of 235 + 11 = 246 (owner_chains_2026_10_18.py).
  4711 = 7 x 673 (47.11 as the integer 4711, 12 mod 37, SA_ST_A); 1111 = 11 x 101 (1 mod 37, IC).

FRAMEWORKS (gf37-audit): 47 IC, prime, cousin; 11 NEG_H, prime, twin (11, 13); 58 SA_ST_B; 36 NEG_H; 4711 SA_ST_A; 1111 IC.
FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def ds(s):
    return sum(int(c) for c in s if c.isdigit())


assert ds("47.11") == 13 and dr(ds("47.11")) == 4 and ds("11.11") == 4 and dr(ds("11.11")) == 4
assert 47 + 11 == 58 and ds("58") == 13 and dr(58) == 4 and 5 + 8 == 13 and 1 + 3 == 4 and dr(11) == 2 and 2 + 2 == 4
assert abs((47.11 - 11.11) - 36) < 1e-9 and 36 % 9 == 0
assert [isprime(x) for x in (11, 23, 47, 95)] == [True, True, True, False] and 2 * 11 + 1 == 23 and 2 * 23 + 1 == 47 and 2 * 47 + 1 == 95
assert factorint(95) == {5: 1, 19: 1} and isprime(13) and 47 == 235 // 5 and 235 % 5 == 0
assert factorint(4711) == {7: 1, 673: 1} and 4711 % 37 == 12 and factorint(1111) == {11: 1, 101: 1} and 1111 % 37 == 1
assert [n % 37 for n in (47, 11, 58, 36)] == [10, 11, 21, 36]

if __name__ == "__main__":
    print("47.11 and 11.11 both have root 4 (difference 36); 47 + 11 = 58 -> 4; 11, 23, 47 is a Sophie Germain chain through the owner's 23")
