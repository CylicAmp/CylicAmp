# CLASS: AUDIT
"""
The owner's lines (2026-11-17):  "3333=12 or 66 or 39 / 12121212= / 34343434= / 12121212 / 46464646= / 12121212"
-- the sequence 12121212, 34343434, 12121212, 46464646, 12121212 -- and, pasted under them, "Unified Research Handoff
& Master Ledger Specification" from another tool (gematria section, lemmas 1-9, a ledger marking all PROVEN).

GEMATRIA (A = 1 .. Z = 26), RIGHT: I 9, AM 14, I AM 23 (the 9th prime, pi(23) = 9, 2 + 3 = 5); THAT 49 = 7^2;
  AM I THAT I AM 23 + 49 + 23 = 95 -> 14 -> 5 (I AM THAT I AM gives the same 95); WHO 46 = CIVIC 46 = 2 x 23;
  AM I WHO I AM = AM I CIVIC I AM = 92 = 4 x 23 -> 11 -> 2; the 23 : 46 : 23 = 1 : 2 : 1 balance.
LEMMAS 3-8: as audited in pasted_v6_ledger_lemmas_audit_2026_11_17.py -- right (13 = the 6th prime, 36 -> 9).
LEMMA 9, RIGHT: each pair reduced to its root and repeated -- 12 -> 3333, 34 -> 7777, 46 -> 10 -> 1111; along the
  owner's sequence 3333, 7777, 3333, 1111, 3333; 3 + 7 + 3 + 1 + 3 = 17, pi(17) = 7, 1 + 7 = 8.

FAULTS THAT CHANGE A RESULT:
  Lemma 1 (this version): the set it lists, {10, ..., 17}, contains 11 -- 2 + 9 = 3 + 8 = 4 + 7 = 5 + 6 = 11 -- so
    "11 irreducible" is wrong. (It is also a different lemma from the V6 Lemma 1, the chain 1 + 1 = 2 ... giving
    12 .. 19, which did leave out 11; the ledger keeps the old label "addition chain exclusion".)
  Lemma 2: "31 -> 10" is still not derived (the rule used for 21 and 13 gives 5 at 31; 10 = 1 + 2 + 3 + 4), so the
    ledger's PROVEN for "10 = +1 0,000" is not earned.

THE OWNER'S SEQUENCE, BOTH WAYS:
  pair roots (lemma 9):   3, 7, 3, 1, 3   -> 17 -> 8
  number roots:           3, 1, 3, 4, 3   -> 14 -> 5      (3333 -> 3, 7777 -> 28 -> 1, 1111 -> 4: the same roots)
  single digits:          12, 28, 12, 40, 12 -> 104 -> 5
  pairs:                  48, 136, 48, 184, 48 -> 464 -> 5
  the five numbers:       117,171,716 -> 5
  The 17 sums the pair roots; the numbers themselves (and every cut of them) give 5. Both are right; they count
  different things (a four-copy repeat has root 4 x d, not d).
gf37-audit: 23 -> 23 by 37, 49 -> 12, 46 -> 9, 92 -> 18, 95 -> 21, 3333 -> 3, 7777 -> 7, 1111 -> 1.

FALSIFICATION: any assertion failing.
"""
from sympy import prime, primepi


def g(w):
    return sum(ord(c) - 64 for c in w if c.isalpha())


def root(n):
    return 1 + (n - 1) % 9 if n else 0


assert (g("I"), g("AM"), g("I AM"), g("THAT"), g("WHO"), g("CIVIC")) == (9, 14, 23, 49, 46, 46)
assert prime(9) == 23 and primepi(23) == 9 and root(23) == 5 and 49 == 7 ** 2
assert g("AM I THAT I AM") == g("I AM THAT I AM") == 95 and root(95) == 5 and 9 + 5 == 14
assert g("AM I WHO I AM") == g("AM I CIVIC I AM") == 92 == 4 * 23 and 9 + 2 == 11 and root(92) == 2
assert prime(6) == 13 and prime(36) == 151 and root(36) == 9

C = sorted({x + y for x in range(1, 10) for y in range(1, 10) if x < y and x + y >= 10})
assert C == list(range(10, 18)) and 11 in C and all(x + (11 - x) == 11 and x < 11 - x for x in range(2, 6))

assert max({4} | set()) + 1 == 5 != 10 == 1 + 2 + 3 + 4

seq = ["12121212", "34343434", "12121212", "46464646", "12121212"]
pair_roots = [root(int(s[0]) + int(s[1])) for s in seq]
assert pair_roots == [3, 7, 3, 1, 3] and sum(pair_roots) == 17 and primepi(17) == 7 and 1 + 7 == 8
assert [int(str(d) * 4) for d in pair_roots] == [3333, 7777, 3333, 1111, 3333]
number_roots = [root(int(s)) for s in seq]
assert number_roots == [3, 1, 3, 4, 3] == [root(int(str(d) * 4)) for d in pair_roots] and root(sum(number_roots)) == 5
singles = [sum(map(int, s)) for s in seq]
pairs = [sum(int(s[i:i + 2]) for i in range(0, 8, 2)) for s in seq]
assert singles == [12, 28, 12, 40, 12] and sum(singles) == 104 and root(104) == 5
assert pairs == [48, 136, 48, 184, 48] and sum(pairs) == 464 and root(464) == 5
assert sum(map(int, seq)) == 117171716 and root(117171716) == 5
assert (23 % 37, 49 % 37, 46 % 37, 92 % 37, 95 % 37, 3333 % 37, 7777 % 37, 1111 % 37) == (23, 12, 9, 18, 21, 3, 7, 1)

if __name__ == "__main__":
    print("gematria and lemma 9 right; lemma 1 wrong (11 = 2 + 9 is in its own set); sequence: pair roots 17 -> 8, numbers 5")
