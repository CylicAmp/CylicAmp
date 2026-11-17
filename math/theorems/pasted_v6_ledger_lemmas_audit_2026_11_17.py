# CLASS: AUDIT
"""
Pasted "Sharpened Lemmas & Formal Mathematical Proofs (V6 Ledger Edition)" (2026-11-17), from another tool working
on the owner's material, relayed by the owner. Eight lemmas; every number recomputed below. tau in the paste means the
digit sum (not the divisor count).

RIGHT:
  L1  the chain 1 + 1 = 2, 2 + 1 = 3, ..., 8 + 1 = 9 (the owner's carry-on = chain) read as 1 = k + 1 gives
      12 .. 19 (eight values) and never 11 -- follows from that reading rule.
  L3  psi(k) = ((k - 1) mod 3) + 1 is the size of the leading comma block of k zeros (0, 00, 000, 0,000, 00,000 ...);
      period 3 by definition; 1 + 2 + 3 = 6 = 1 x 2 x 3; sigma(6) - 6 = 6; 1 + 2 + 3 + 4 = 10.
  L4  1 + 23 + 10 = 34 -> 7; 1 + 5 + 1 = 7; 151 prime, the 36th prime; phi(37) = 36 = 73 - 37; 151 -> 7.
      The two phases must agree: phase II is the digit sums of phase I's parts, and digit sums keep the remainder
      by 9 (forced).
  L5  7 + 10 = 17 prime, pi(17) = 7; 17 -> 8; 7 + 8 = 15 = T_5 = the magic constant and the trace of the Lo Shu
      square given (8 + 5 + 2); 15 -> 6.
  L6  0 + 50 + 501 + 501 + 50 = 1102 = 2 x 19 x 29 -> 4; wings 100 -> 1, core 1002 -> 3, 1 + 3 = 4 (forced by 9).
  L7  T_n = 1021 + 101n = 100(10 + n) + (21 + n); root T_n = root F_n (T - F = 99 L, forced); T_n + T_(9-n) = 2951
      = 13 x 227 -> 8; F_n + F_(9-n) = 80 -> 8; the eight T_n add to 11804 = 4 x 2951 -> 5.
  L8  twin starts above 3 leave 2 by 3; starts of a 142-gap leave 1 (142 leaves 1 by 3); disjoint -- forced, and
      checked on every case below 100,000.

FAULT THAT CHANGES A RESULT (L2): count(31) = 10 does not follow from the rule the proof uses for 21 and 13
  (max of the previous count + 1, which gives 5 at 31). 10 is 1 + 2 + 3 + 4, the running total -- a different rule.
  And "+1 0,000" does not come from 10: 10 carries 1 and leaves one 0, while 0,000 is four zeros (the length-4
  zero register of L3). The owner's line for that step is not in the paste.

gf37-audit: 151 leaves 3 by 37; 1102 leaves 29; 2951 leaves 28; 11804 leaves 1.

FALSIFICATION: any assertion failing.
"""
from sympy import divisor_sigma, factorint, isprime, prime, primepi, totient


def ds(n):
    return sum(map(int, str(n)))


def root(n):
    return 1 + (n - 1) % 9


assert sorted(10 + (k + 1) for k in range(1, 9)) == [12, 13, 14, 15, 16, 17, 18, 19] and 11 not in range(12, 20)

counts = {12: {1, 2}}
counts[21] = {max(counts[12]) + 1}
counts[13] = {max(counts[21]) + 1}
assert counts[21] == {3} and counts[13] == {4}
assert max(counts[13]) + 1 == 5 != 10 and 1 + 2 + 3 + 4 == 10       # L2: the stated rule gives 5
assert str(10).count("0") == 1 and "0,000".count("0") == 4


def psi(k):
    return ((k - 1) % 3) + 1


for k in range(1, 30):
    zeros = "{:,}".format(10 ** k)[1:].lstrip(",")                  # k zeros grouped by commas
    assert len(zeros.split(",")[0]) == psi(k) and psi(k + 3) == psi(k)
assert 1 + 2 + 3 == 1 * 2 * 3 == 6 and divisor_sigma(6) - 6 == 6

assert 1 + 23 + 10 == 34 and ds(34) == 7 == 1 + 5 + 1 == ds(151)
assert isprime(151) and primepi(151) == 36 and prime(36) == 151 and totient(37) == 36 == 73 - 37
for parts in ((1, 23, 10), (5, 41, 7), (99, 18, 3)):                # forced: digit sums keep the remainder by 9
    assert root(sum(parts)) == root(sum(ds(p) for p in parts))

assert isprime(17) and primepi(17) == 7 and ds(17) == 8 and ds(15) == 6
sq = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
assert all(sum(r) == 15 for r in sq) and all(sum(sq[i][j] for i in range(3)) == 15 for j in range(3))
assert sq[0][0] + sq[1][1] + sq[2][2] == 15 == sq[0][2] + sq[1][1] + sq[2][0]

assert 0 + 50 + 501 + 501 + 50 == 1102 and factorint(1102) == {2: 1, 19: 1, 29: 1} and ds(1102) == 4
assert ds(100) + ds(1002) == 4 == ds(13)


def T(n):
    return 1021 + 101 * n


assert all(T(n) == 100 * (10 + n) + (21 + n) and root(T(n)) == root(31 + 2 * n) for n in range(1, 9))
assert {T(n) + T(9 - n) for n in range(1, 9)} == {2951} and factorint(2951) == {13: 1, 227: 1} and root(2951) == 8
assert {(31 + 2 * n) + (31 + 2 * (9 - n)) for n in range(1, 9)} == {80} and root(80) == 8
assert sum(T(n) for n in range(1, 9)) == 11804 == 4 * 2951 and root(11804) == 5

assert 142 % 3 == 1
for p in range(5, 100_000):
    if isprime(p) and isprime(p + 2):
        assert p % 3 == 2
    if isprime(p) and isprime(p + 142):
        assert p % 3 == 1

assert (151 % 37, 1102 % 37, 2951 % 37, 11804 % 37) == (3, 29, 28, 1)

if __name__ == "__main__":
    print("V6 ledger: lemmas 1, 3-8 right (4, 6, 7, 8 forced); lemma 2's count 10 and '+1 0,000' do not follow")
