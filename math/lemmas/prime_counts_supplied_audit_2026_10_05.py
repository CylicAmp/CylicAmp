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

if __name__ == "__main__":
    print("all assertions pass")
