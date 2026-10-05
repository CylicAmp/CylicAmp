# CLASS: AUDIT
"""
Asserted form of DEDUP_T299_QUOTIENT.md (dedup pass of 2026-10-01, commit
1da65c2).  Every "re-checked" line in that note is a check here.

T299: two maps out of Phi_3 = x^2 + x + 1.
  Use 1 (evaluate): Phi_3(137) = 18907 = 7 * 37 * 73; mu_3 in F_37 = {1, 10, 26}.
  Use 2 (quotient, Z[omega]): 4*37 = 148 = 11^2 + 27 * 1^2.
  Forced, not a curve fact: F_37* is cyclic of order 36, one subgroup per
  divisor; the order-6 subgroup is {1, 10, 11, 26, 27, 36} = sixth powers = <11>.
  Scope: n | p-1 and n*gcd(n, p-1) = p-1 collapses to p = n^2 + 1; hits below
  20000: n=6 -> [37], n=4 -> [17], n=2 -> [5] (also asserted in T299's verify_audit).
Quotient cluster: the 12 cosets of IC = {1, 10, 26} in F_37* are exactly the
  12 orbits of x -> 26x (the 137-map), and (Z/37Z)*/IC is cyclic of order 12.

FALSIFICATION: any assertion failing.
"""
from math import gcd

from sympy import factorint, primerange

P = 37
assert 137 ** 2 + 137 + 1 == 18907 and factorint(18907) == {7: 1, 37: 1, 73: 1}
assert sorted([1] + [x for x in range(1, P) if (x * x + x + 1) % P == 0]) == [1, 10, 26]
assert 4 * P == 11 ** 2 + 27 * 1 ** 2

units = range(1, P)
subgroups = {}
for g in units:
    H = frozenset(pow(g, k, P) for k in range(36))
    subgroups.setdefault(len(H), set()).add(H)
assert sorted(subgroups) == [d for d in range(1, 37) if 36 % d == 0]
assert all(len(v) == 1 for v in subgroups.values())                       # one per divisor
order6 = next(iter(subgroups[6]))
assert order6 == {1, 10, 11, 26, 27, 36} == {pow(x, 6, P) for x in units} \
    == {pow(11, k, P) for k in range(6)}

primes = list(primerange(2, 20000))
hits = {n: [q for q in primes if (q - 1) % n == 0 and n * gcd(n, q - 1) == q - 1] for n in (2, 4, 6)}
assert hits == {2: [5], 4: [17], 6: [37]}
assert all(q == n * n + 1 for n, qs in hits.items() for q in qs)

IC = {1, 10, 26}
cosets = {frozenset(x * h % P for h in IC) for x in units}
orbits = {frozenset({x, 26 * x % P, 26 * 26 * x % P}) for x in units}
assert len(cosets) == 12 and cosets == orbits
assert pow(26, 3, P) == 1 and 137 % P == 26
# quotient cyclic of order 12: some coset generates all 12
coset_of = {x: frozenset(x * h % P for h in IC) for x in units}
assert any(len({coset_of[pow(g, k, P)] for k in range(12)}) == 12 for g in units)

if __name__ == "__main__":
    print("DEDUP T299 + quotient cluster: all assertions pass")

# 2026-10-05: T118 states the order-12 quotient itself (cosets of H_3 = IC are the 12 orbits);
# CLAUDE.md's 2026-09-16 exclusion of T118 was wrong and is corrected.
import pathlib as _pl2
_t118 = (_pl2.Path(__file__).parent / "theorem_118_coset_structure_gf37.py").read_text()
assert "has order 36/3 = 12" in _t118 and "The 12 left cosets of H_3 are exactly the 12 orbits of the 137-map" in _t118
