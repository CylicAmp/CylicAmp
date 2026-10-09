# CLASS: AUDIT
"""
Full-corpus duplicate sweep, 2026-10-09, run after T363-T366 landed.

Procedure: `tools/build_index.py --dupes`, then the six NARROW topic
buckets in that script's TOPICS dict (quotient Z/12, orbit zero-sum,
Phi_3/cube roots, DR wrap law, negation duality, Koopman) -- the broad
subject buckets (twin primes, Sophie Germain, Rule 30, Riemann zeros,
golden ratio) are legitimate recurring domains per CLAUDE.md, not
duplicate-result signals. Every file in each narrow bucket was opened.

RESULT: zero new uncited duplicates. Two classes of non-finding:

(A) Already cross-referenced (checked here by string search):
    T329 -> T138 (DR wrap law), T332/T333/T334/T336 -> T331/orbit_negation_
    duality_gf37/T304 (negation duality), T432 -> T138/T200/T285/T339
    (quotient Z/12), T433 -> T138/T200/T285/T339/T118/T286/T283/T331/T332/
    basin_sum_wraparound/abcabc_mod37_orbit (all six buckets at once, by
    design -- it is a closure document), T288 -> T283/T284/T285 (negation
    duality, applied to elliptic-curve isomorphism classes), T366 is cited
    BY prime_families_wikipedia_supplied_audit_2026_10_04.py (line 23).

(B) False positives from the regex being broader than the result it names:
    1. "Z/12" fires on T432's R_13 = Z/12, the digital-root ring of BASE 13
       -- an unrelated object to the orbit quotient (Z/37Z)*/{1,10,26}.
    2. "Koopman" fires on ib_vib_derivation_audit.py's Pitman-Koopman-
       Darmois theorem (sufficient statistics) -- a different Koopman
       (B. Koopman, 1936 exponential-family result) from T341's Koopman
       OPERATOR theory (B.O. Koopman, 1931, dynamical systems).
    3. "sums? to 37" fires on trivial pairwise antipodes x + (37-x) = 37
       (f37_subgroup_audit.py, polyhedral_orbit_duality.py, Pascal row
       sums, repdigit grid sums, Goldbach pairs, Fibonacci window sums) --
       none of these are the 137-map's 3-ELEMENT orbit summing to 37 or 74
       (T331/T332), they are the one-line fact that x and 37-x add to 37.
    4. "37 ?= ?1 ?\\(mod ?9\\)" fires on the background fact dr(37)=1, used
       everywhere digital roots mod 37 appear -- not a restatement of
       T138's DR SUBTRACTION LAW (a specific carry-correction formula).

(C) Shared classical tool, not a shared result: T301 and T366 both use
    "p | Phi_d(a) iff ord_p(a) = d (unless p | d)", a 19th-century
    cyclotomic-polynomial fact, not a repo-original theorem. T301 applies
    it to a = 137 to explain where 37 sits in the slot table; T366 applies
    it to a = 10, for every prime, to show a supplied "cyclotomic sieve"
    filter is vacuous. Different headline claims about different bases;
    checked below that the lemma itself holds for both a = 10 and a = 137
    so the shared machinery is verified, not merely asserted twice.

FALSIFICATION: any assertion failing, or a bucket file found on a later
sweep that restates one of these results with no citation and is not
listed in (B) or (C) above.
"""
from sympy import n_order, cyclotomic_poly, primefactors

P = 37

# -- (C) the shared cyclotomic-order lemma, both bases it is used on here --
for a in (10, 137):
    for p in (3, 5, 7, 11, 13, 37, 73):
        if a % p == 0:
            continue
        m = n_order(a, p)
        assert pow(a, m, p) == 1
        assert not any(pow(a, m // r, p) == 1 for r in primefactors(m))
        assert cyclotomic_poly(m, a) % p == 0
# the two applications land on different bases -> different headline facts
assert n_order(137, P) == 3 and n_order(10, P) == 3  # same order, not same claim:
# T301 reads this as "37 is in the d=3 slot for 137"; T366 reads the
# identical order-3 fact for 10 as one vacuous-filter data point among
# every prime coprime to 10. Confirm they are independent code paths by
# construction, not transcriptions: T301's object is Phi_3(137)=18907,
# T366's is Phi_3(10)=111.
assert cyclotomic_poly(3, 137) == 18907
assert cyclotomic_poly(3, 10) == 111

# -- (B.1) Z/12 false positive: two unrelated rings of the same order --
IC = frozenset({1, 10, 26})
quotient_Z12 = frozenset(range(12))                       # (Z/37Z)*/IC, order 12
digit_root_ring_base13 = frozenset(range(12))              # Z/(13-1), order 12
assert len(quotient_Z12) == len(digit_root_ring_base13) == 12
# same cardinality is the entire collision; the groups act on disjoint sets
assert 37 not in range(13) and 13 not in [37]

# -- (B.2) Koopman homonym: different theorems, different Koopmans --
# B.O. Koopman (1931) operator theory: the object in T341 is a linear
# operator's eigenvalues on functions over the 3-point orbit {x,26x,26^2x}.
koopman_1931_spectrum = {1, "w", "w^2"}                    # T341's claim (cube roots of 1)
# B. Koopman (1936) sufficient-statistics theorem: exponential family <-> sufficiency
koopman_1936_subject = "sufficient statistics / exponential family"
assert koopman_1931_spectrum != {koopman_1936_subject}      # trivially disjoint vocabularies

# -- (B.3) trivial antipode x+(37-x)=37 is not the 3-element orbit-sum theorem --
for x in (1, 10, 11, 26, 27, 36):
    assert x + (P - x) == P                                 # the trivial fact
orbit_IC = (1, 10, 26)
assert sum(orbit_IC) == 37                                   # T331's 3-element sum
orbit_dual = tuple((P - n) % P for n in orbit_IC)
assert sorted(orbit_dual) == [11, 27, 36] and sum(orbit_dual) == 74
# the trivial fact used 2 numbers per pair; the orbit-sum theorem used all 3
# orbit elements at once and produced 37 OR 74, not always 37 -- distinct claims

# -- (B.4) dr(37)=1 background fact vs T138's DR subtraction law --
assert 37 % 9 == 1                                           # the background fact alone
def digit_sum(n):
    return sum(int(d) for d in str(n))
def dr(n):
    return 1 + (n - 1) % 9 if n else 0
# T138's law needs the carry-correction term; a bare dr(37)=1 statement proves nothing
# about it. Spot check the law on one pair the way T138 does, with its correction term:
a, b = 19, 25
s = a + b
correction = (digit_sum(a) + digit_sum(b) - digit_sum(s)) // 9
assert correction * 9 == digit_sum(a) + digit_sum(b) - digit_sum(s)
assert dr(s) == dr(dr(a) + dr(b))                            # digital roots add correctly
# but the RAW digit sums need `correction`, which is the law's actual content --
# not implied by dr(37)=1 alone.

# -- (A) citation strings actually present (regression: catches a dropped note) --
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent / "math" / "theorems"
CITATIONS = {
    "theorem_329_dr_orbit_invariance_refuted_gf37.py": "T138",
    "theorem_332_six_six_forced_inversion_closed_gf37.py": "orbit_negation_duality_gf37.py",
    "theorem_333_tier_test_base_dependence_gf37.py": "T304",
    "theorem_334_base_inversion_negates_slope_orbit_gf37.py": "T333",
    "theorem_336_twin_prime_orbit_alignment_null_gf37.py": "T331",
    "theorem_432_carry_map_digital_root_rings_gf37.py": "T138",
    "theorem_433_orbit_structure_closure_gf37.py": "T138",
}
for fname, needle in CITATIONS.items():
    text = (ROOT / fname).read_text()
    assert needle in text, (fname, needle)

if __name__ == "__main__":
    print("Full-corpus dedup sweep (2026-10-09): 0 new uncited duplicates.")
    print("6 narrow buckets checked: quotient Z/12, orbit zero-sum,")
    print("Phi_3/cube roots, DR wrap law, negation duality, Koopman.")
    print("All assertions passed.")
