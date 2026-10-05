# CLASS: AUDIT
"""
Owner's page (2026-10-05) with a pasted answer from another assistant.
Context: prime_row_ultimate_rotation.py (prime roots by decade, 43 brings 7 back).

OWNER'S LINES:
  2~ / 3~0 / 5~23 / 7~43: each single-digit prime with the next prime of the
  same digital root. 5 -> 23 and 7 -> 43 are right; 3 -> none ever (every
  later multiple of 3 is composite); 2 -> 11 (the line left it blank).
  1~100: 2+5 = 7 -- there are 25 primes below 100, 2+5 = 7.
  100~1000: 1+4 = 5+3 = 8 -- 143 primes from 100 to 999, -> 8.
  7+8 = (1+5 = 6) -- together 25 + 143 = 168 primes below 1000, 1+6+8 = 15 -> 6.
  Grid 156/248/379: uses 1..9 once; rows 12, 14, 19; columns 6, 16, 23;
  diagonals 14 and 13.

PASTED ANSWER -- CHECKED:
  "No two double-digit primes add to 12" -- correct (the least sum is 11+11 = 22);
  5 + 7 = 12 -- correct.
  Difference-12 pairs 11/23, 17/29, 19/31, 29/41, 31/43 -- all correct; there
  are six more below 100 it does not list: 41/53, 47/59, 59/71, 61/73, 67/79,
  71/83 ("several" is accurate, not complete).
  "143 primes between 100 and 999" -- correct, and the full list by hundreds
  (21, 16, 16, 17, 14, 16, 14, 15, 14) matches exactly.

SECOND PAGE (owner, 2026-10-05):
  2+9 = 1+1 = 2 (fills the blank: 2 -> 11), 3+0 = 3, 5+18 = 2+3 = 5,
  7+36 = 4+3 = 7. The gaps 9, 18, 36 are multiples of 9 (forced: equal digital
  roots differ by a multiple of 9) -- 9 x 1, 2, 4; "9+18x2 = (3+6 = 9) 369".
  357 -> 15, 257 -> 14; 15 + 14 = 29 -> 11 -> 2. 515 -> 11, +2 = 13, +2 = 15 -> 6;
  6 + 2 + 2 = 10 -> 1. 257 = 2^8 + 1 is prime; 357 = 3 x 7 x 17; 515 = 5 x 103.
  Pasted text on three primes: minimum sum 2+2+2 = 6 and the triplet 3, 5, 7
  (the only three primes spaced by 2) -- correct. "Goldbach's weak conjecture"
  is now a theorem (Helfgott 2013): every odd number above 5 is a sum of
  three primes.

THE DOUBLING CHAIN 9 x 2 = 18 x 2 = 36 (owner, 2026-10-05; the gaps 9, 18, 36):
  Written out in order, 9, 2, 18, 2, 36 -> 9218236; the owner's build-up 9, 92,
  921, 9218, 92182, 921823, 9218236 is right. Pasted continuation (another
  assistant): 36 x 2 = 72 -> 9218236272, 72 x 2 = 144 -> 92182362722144, and its
  comma groupings -- correct. Its YouTube citation and "mathematical archives"
  are filler, not sources. Forced: every product (18, 36, 72, 144, ...) reduces to
  9, so the chain's digit sum is 9s plus 2s: 9218236 -> 31 -> 4, and each further
  doubling adds 9 + 2, i.e. +2 to the root.

OWNER'S FACTOR SCRIPT ON 92182362722144 (the chain after 72 x 2 = 144), run as
  written and cross-checked with sympy -- identical:
    92182362722144 = 2^5 x 17 x 67 x 2529147353 (all four prime)
    48 divisors, divisor sum 195027610761648
    sqrt 9601164.654... (not a square), cube root 45173.38... (not a cube)
    hex 0x53d6e0fc0f60, octal 0o2475334077007540,
    binary 0b10100111101011011100000111111000000111101100000
  Digit sum 53 -> 8 = DR(9 + 11 x 4), the chain rule above.

FALSIFICATION: any assertion below failing.
"""
from sympy import primerange, isprime, primepi

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

NEXT = {p: next((q for q in primerange(p + 1, 1000) if dr(q) == dr(p)), None) for p in (2, 3, 5, 7)}
assert NEXT == {2: 11, 3: None, 5: 23, 7: 43}
assert primepi(100) == 25 and dr(25) == 7
assert primepi(999) - primepi(99) == 143 and dr(143) == 8
assert primepi(1000) == 168 == 25 + 143 and dr(168) == dr(7 + 8) == 6
G = [[1, 5, 6], [2, 4, 8], [3, 7, 9]]
assert sorted(x for r in G for x in r) == list(range(1, 10))
assert [sum(r) for r in G] == [12, 14, 19] and [sum(c) for c in zip(*G)] == [6, 16, 23]
assert (G[0][0] + G[1][1] + G[2][2], G[0][2] + G[1][1] + G[2][0]) == (14, 13)

assert min(p + q for p in primerange(10, 100) for q in primerange(10, 100)) == 22 and 5 + 7 == 12
D12 = [(p, p + 12) for p in primerange(10, 100) if isprime(p + 12) and p + 12 < 100]
assert D12[:5] == [(11, 23), (17, 29), (19, 31), (29, 41), (31, 43)] and len(D12) == 11
LISTED = {1: 21, 2: 16, 3: 16, 4: 17, 5: 14, 6: 16, 7: 14, 8: 15, 9: 14}
assert all(len(list(primerange(100 * h, 100 * h + 100))) == c for h, c in LISTED.items())
assert sum(LISTED.values()) == 143

assert [q - p for p, q in ((2, 11), (5, 23), (7, 43))] == [9, 18, 36] and all(g % 9 == 0 for g in (9, 18, 36))
assert all((q - p) % 9 == 0 for p in primerange(2, 300) for q in primerange(p + 1, 300) if dr(p) == dr(q))
assert dr(2 + 9) == 2 and dr(5 + 18) == 5 and dr(7 + 36) == 7 and 3 + 6 == 9
assert (3 + 5 + 7, 2 + 5 + 7) == (15, 14) and dr(15 + 14) == 2 and 5 + 1 + 5 + 2 + 2 == 15 and dr(15) == 6
assert dr(6 + 2 + 2) == 1 and isprime(257) and 257 == 2 ** 8 + 1 and 357 == 3 * 7 * 17 and 515 == 5 * 103
assert 2 + 2 + 2 == 6 and [p for p in primerange(2, 1000) if isprime(p + 2) and isprime(p + 4)] == [3]
for n in range(7, 2000, 2):
    assert any(isprime(a) and isprime(b) and isprime(n - a - b) for a in (2, 3, 5, 7, 11, 13) for b in primerange(2, n))

def chain(k):
    v, out = 9, "9"
    for _ in range(k):
        v *= 2
        out += "2" + str(v)
    return out
assert chain(2) == "9218236" and [chain(2)[:i] for i in range(1, 8)] == ["9", "92", "921", "9218", "92182", "921823", "9218236"]
assert chain(3) == "9218236272" and chain(4) == "92182362722144"
assert f"{int(chain(4)):,}" == "92,182,362,722,144"
assert sum(map(int, chain(2))) == 31 and dr(31) == 4
for k in range(1, 20):
    assert dr(9 * 2 ** k) == 9 and dr(sum(map(int, chain(k)))) == dr(9 + 11 * k)

from sympy import factorint, divisor_count, divisor_sigma
import math
N = 92182362722144
assert N == int(chain(4)) and factorint(N) == {2: 5, 17: 1, 67: 1, 2529147353: 1} and isprime(2529147353)
assert divisor_count(N) == 48 and divisor_sigma(N) == 195027610761648
assert math.isqrt(N) == 9601164 and math.isqrt(N) ** 2 != N and round(N ** (1 / 3)) ** 3 != N
assert (hex(N), oct(N)) == ("0x53d6e0fc0f60", "0o2475334077007540")
assert bin(N) == "0b10100111101011011100000111111000000111101100000"
assert sum(map(int, str(N))) == 53 and dr(53) == 8 == dr(9 + 11 * 4)

if __name__ == "__main__":
    print("all assertions pass")
