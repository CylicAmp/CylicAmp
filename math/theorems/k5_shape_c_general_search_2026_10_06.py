"""
k5_shape_c_general_search_2026_10_06.py

Extends search_C (k5_odd_shapes.py) from q < r <= 5000 to q < r <= 150000:
a 30x extension of the general (any q, not fixed to 3) Level-2 search for
shape C, {1, q, r, s, qr}, q < r < s.

NAMING NOTE, to avoid a stale cross-reference: "the two-prime system"
(commit e60f87e, "k=5 odd two-prime system") names the q=3 branch only
-- two FREE primes (r, s) with q fixed at 3. That branch is CLOSED, at
Level 1, by the ordering argument in k5_shape_c_q3.py (commit e49f752).
What remains open is the branch k5_shape_c_q3.py itself flags as
untouched: q NOT fixed, so q, r, s are three free primes (SCOPE note in
that file). This search extends THAT branch computationally; it does not
touch the already-closed q=3 case.

METHOD: search_C is reused unchanged from k5_odd_shapes.py (no logic is
duplicated here, per prior-art). This file only raises its bound and
records what the extension found.

RESULT, pmax = 150000 (132,501,117 candidates admitted by (C2)):
  Exactly 3 pairs survive BOTH congruences (C3), the same count found at
  pmax = 60000 -- no new survivor between 60000 and 150000:
    (q, r, s) = (3, 13, 17)           n = 1989              [already recorded, dies on 9|n]
    (q, r, s) = (3, 53197, 69073)     n = 33070287429        [already recorded, dies on 9|n]
    (q, r, s) = (6221, 9281, 10301)   n = 3333573062832605   [NEW at this bound]
  All three die on verify_prefix: zero witnesses.

THE NEW NEAR-MISS: n = 3333573062832605 = 5 * 19 * 59 * 6221 * 9281 * 10301.
Unlike the q=3 pair (which dies on 9 | n, one step below the top), this one
dies immediately: 5 and 19 are both far below q = 6221, so the true smallest
divisors are 1, 5, 19, 59, 95, ... -- nothing like {1, q, r, s, qr}. It
satisfies (C2) and (C3) by coincidence of size, not because n is close to
admissible.

STATUS: still Level 2 only. No Level 1 argument for the general (free q)
branch is given here, and none is claimed. The search is COMPLETE for
every prime pair q < r <= 150000 (search_C's own completeness, unchanged).
Falsification: a fourth near-miss appearing below 150000, or any witness.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k5_odd_shapes import search_C, is_prime

PMAX = 150000

PRIOR_NEAR_MISSES = {(3, 13, 17), (3, 53197, 69073)}
NEW_NEAR_MISS = (6221, 9281, 10301)


def n_of(q: int, r: int, s: int) -> int:
    return 1 + q * q + r * r + s * s + q * q * r * r


def test_extended_search_matches_prior_bound() -> None:
    """Re-run at the old bound: must reproduce exactly the prior published count."""
    r5000 = search_C(5000)
    assert r5000["candidates"] == 298436
    assert r5000["near_misses"] == [(3, 13, 17)]
    assert r5000["witnesses"] == []
    print("[ok] pmax=5000 reproduces the prior published result exactly")


def test_new_near_miss_dies_immediately() -> None:
    q, r, s = NEW_NEAR_MISS
    assert is_prime(q) and is_prime(r) and is_prime(s) and q < r < s
    n = n_of(q, r, s)
    assert n == 3333573062832605
    # survives both (C3) congruences
    assert (1 + r * r + s * s) % q == 0
    assert (1 + q * q + s * s) % r == 0
    # but has small prime factors far below q -- dies hard, not marginally
    for p in (5, 19, 59):
        assert n % p == 0 and p < q
    print("[ok] (6221, 9281, 10301): survives (C3) but 5, 19, 59 | n, all << q")


def test_extended_search(pmax: int = PMAX) -> dict:
    t0 = time.time()
    result = search_C(pmax)
    elapsed = time.time() - t0
    near = set(result["near_misses"])
    assert result["witnesses"] == []
    assert near == PRIOR_NEAR_MISSES | {NEW_NEAR_MISS}, near
    print(f"[ok] search_C({pmax}): {result['candidates']:,} candidates, "
          f"{len(near)} near-misses, 0 witnesses ({elapsed:.1f}s)")
    return result


def self_test() -> None:
    test_extended_search_matches_prior_bound()
    test_new_near_miss_dies_immediately()
    test_extended_search(PMAX)
    print("\nAll self-tests passed.")
    print("RESULT: shape C (general, free q) extended from q<r<=5000 to")
    print(f"        q<r<={PMAX}: no witnesses, one new near-miss found,")
    print("        dying immediately rather than marginally.")
    print("STATUS: Level 2 only. The branch is NOT closed.")


if __name__ == "__main__":
    self_test()
