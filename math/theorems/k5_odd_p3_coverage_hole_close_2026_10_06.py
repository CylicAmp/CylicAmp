"""
k5_odd_p3_coverage_hole_close_2026_10_06.py

Closes the coverage hole recorded in theorem_245_n130_divisor_square_sum_gf37.py
(commit fe85953, 2026-09-19): for the two k=5 odd shapes carrying p^3,
    1 p p^2 p^3 q      (q the largest divisor, q > p^3)
    1 p p^2 q p^3      (q the fourth divisor, p^2 < q < p^3)
31 of the ~77 primes below 400 were skipped because C = 1 + p^2 + p^4 + p^6
exceeded a 1e14 factoring cap in the tooling used at the time.

THE CAP WAS A TOOLING LIMIT, NOT A COMPUTATIONAL ONE. sympy's factorint
factors every C up to p = 50000 (C ~ 1.57e28) in well under a second each;
the full run below takes 18.7s. Nothing here needed the old cap.

RESULT: complete for every prime p < 50000 (5131 primes, vs. 76 before,
and the 31 that had been skipped are now covered). 3893 candidate q
checked (prime factors of C with p^2 < q < p^3 or q > p^3). ZERO survive
the full prefix check (not just the congruence pinning). The hole in the
original 400-prime range is fully closed, and the bound is extended 125x.

STATUS: still Level 2 (search), not a proof -- same as the shape's
sibling results in theorem_245. The weakest shape overall in this part
of k=5 odd remains (1,p,q,pq,q^2) at p<120 (ledger: "k=5 odd, 3 not| n
(weakest shape)"); this file strengthens two specific shapes, not the
quoted figure for the whole case.

FALSIFICATION: any assertion below failing.
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k5_odd_shapes import primes_upto, verify_prefix

from sympy import factorint

PMAX = 50000


def C_of(p: int) -> int:
    return 1 + p * p + p ** 4 + p ** 6


def candidates(p: int):
    """Prime factors of C(p), each checked against both shape orderings."""
    C = C_of(p)
    out = []
    for q in factorint(C):
        if q in (2, p):
            continue
        if q > p ** 3:
            out.append((1, p, p * p, p ** 3, q))              # q is largest
        elif p * p < q < p ** 3:
            out.append((1, p, p * p, q, p ** 3))                # q is fourth
    return out


def test_old_31_skipped_primes_now_covered():
    """The 76 primes below 400 (from the original ledger) all factor instantly now."""
    old_range = [p for p in primes_upto(400) if p >= 5]
    assert len(old_range) == 76                      # the "~77 primes below 400" of fe85953
    t0 = time.time()
    for p in old_range:
        factorint(C_of(p))                             # must not need a cap
    elapsed = time.time() - t0
    assert elapsed < 5, f"took {elapsed}s, expected instant"
    print(f"[ok] all 76 primes below 400 (the ones with the 31-skip hole) factor in {elapsed:.3f}s")


def test_full_search(pmax: int = PMAX):
    primes = [p for p in primes_upto(pmax) if p >= 5]
    t0 = time.time()
    hits = []
    n_candidates = 0
    for p in primes:
        for shape in candidates(p):
            n_candidates += 1
            n = sum(v * v for v in shape)
            if verify_prefix(shape):
                hits.append((p, shape, n))
    elapsed = time.time() - t0
    assert len(primes) == 5131
    assert n_candidates == 3893
    assert hits == []
    print(f"[ok] p < {pmax}: {len(primes)} primes, {n_candidates} candidates, "
          f"0 witnesses ({elapsed:.1f}s)")
    return hits


def self_test():
    test_old_31_skipped_primes_now_covered()
    test_full_search(PMAX)
    print("\nAll self-tests passed.")
    print("RESULT: the 31-prime coverage hole in shapes '1 p p^2 p^3 q' and")
    print("        '1 p p^2 q p^3' is closed. Both shapes are now complete")
    print(f"        and empty for every prime p < {PMAX} (was p < 400, 76 primes).")


if __name__ == "__main__":
    self_test()
