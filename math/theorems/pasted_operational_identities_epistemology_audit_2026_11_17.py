# CLASS: AUDIT
"""
Pasted "Sharpened Operational Identities & Exact Formulations" and "Foundational Epistemology & Invariant Taxonomy"
(2026-11-17), from another tool, relayed by the owner. It takes in the corrections of
pasted_operational_taxonomy_audit_2026_11_17.py (UACI discrete vs continuous, ord - 64, 58 / 46 visits) and adds
a master table with Lemma 13.

RIGHT:
  discrete UACI mean (1/(N^2 F)) sum |x - y| = (N^2 - 1)/(3NF) = (N + 1)/(3N) = 257/768 = 33.4635416...%;
    257/768 - 1/3 = 1/768 = 0.1302%;
  the proof of tau(n) = n - 9 sum floor(n/10^k): sum_{k=1}^{j} 10^(j-k) = (10^j - 1)/9, and the j = 0 term drops out;
  ASCII 247 / 215 against the alphabet positions 9 + 1 + 13 = 23;
  Langton: v = (-1/52, -1/52), |v| = sqrt2/52 = 0.027196 cells per step; 58 white and 46 black visits per period;
  37 is the 12th prime.

FAULTS THAT CHANGE A RESULT:
  1. "mu_cont = (1/F) int_0^1 int_0^1 |u - v| du dv = 1/3": the double integral over the unit square is already 1/3;
     with the 1/F in front it is 1/765. The continuous value is int int |u - v| = 1/3, without 1/F.
  2. Lemma 2 "12 -> 21 -> 13 -> 31 -> 10 (root constant)": the roots are 3, 3, 4, 4, 1 -- each swap keeps its root
     (10a + b and 10b + a differ by 9(a - b)), the chain does not. And 31 -> 10 is still not derived.
  3. Lemma 13 "sum of NIST gains = 37" marked PROVEN: 37 = 892 - 855 is a count from one run of sampled sequences
     (pasted_tmc_manuscript_pages_11_13_audit_2026_11_17.py), a measurement, not something a proof can give.
  4. The root's range written Z_9^* (the units 1, 2, 4, 5, 7, 8): the root takes all of 1 .. 9, and 3, 6, 9 are not
     units.
  Still standing from before: Lemma 1 "{10, ..., 17}; 11 not in C+" (11 = 2 + 9 is in it); Lemma 10
  "Phi_8 = 73 x 101 x 137" (Phi_8(10) = 10001 = 73 x 137).

FALSIFICATION: any assertion failing.
"""
import math
from fractions import Fraction

import sympy as sp

N, F = 256, 255
s = sum(abs(a - b) for a in range(N) for b in range(N))
assert s == N * (N * N - 1) // 3
assert Fraction(s, N * N * F) == Fraction(N * N - 1, 3 * N * F) == Fraction(N + 1, 3 * N) == Fraction(257, 768)
assert Fraction(257, 768) - Fraction(1, 3) == Fraction(1, 768) and round(100 / 768, 4) == 0.1302

u, v = sp.symbols("u v")
box = sp.integrate(sp.integrate(sp.Piecewise((u - v, u >= v), (v - u, True)), (u, 0, 1)), (v, 0, 1))
assert sp.nsimplify(box) == sp.Rational(1, 3) and sp.nsimplify(box) / F == sp.Rational(1, 765)

for j in range(1, 12):
    assert sum(10 ** (j - k) for k in range(1, j + 1)) == (10 ** j - 1) // 9
assert sum(map(ord, "I AM")) == 247 and sum(map(ord, "IAM")) == 215 and sum(ord(c) - 64 for c in "IAM") == 23
assert round(math.sqrt(2) / 52, 6) == 0.027196 and math.isclose(math.hypot(-2, -2) / 104, math.sqrt(2) / 52)
assert sp.prime(12) == 37


def root(n):
    return 1 + (n - 1) % 9


assert [root(n) for n in (12, 21, 13, 31, 10)] == [3, 3, 4, 4, 1]
assert all((10 * a + b - (10 * b + a)) == 9 * (a - b) for a in range(10) for b in range(10))
assert {root(n) for n in range(1, 1000)} == set(range(1, 10))
assert [r for r in range(1, 9) if math.gcd(r, 9) == 1] == [1, 2, 4, 5, 7, 8]
assert 11 in {a + b for a in range(1, 10) for b in range(1, 10) if a < b and a + b >= 10}
assert sp.cyclotomic_poly(8, 10) == 10001 == 73 * 137

if __name__ == "__main__":
    print("identities right (257/768, tau proof, 23, sqrt2/52); stray 1/F; lemma 2 roots 3,3,4,4,1; lemma 13's 37 is a measurement")
