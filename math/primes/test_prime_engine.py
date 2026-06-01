"""
test_prime_engine.py

Tests for prime_engine.py covering:
  1. Correctness of digital_root()
  2. is_prime() agrees with known primes up to 10000
  3. prime_generator() yields every prime and no composites (up to 1000)
  4. DR pre-filter: DR ∈ {3,6,9} → never prime (for n > 3)
  5. Alpha grid labels are correct for known primes
  6. Proof certificate: DR∈{3,6,9} positions empty in generator output
  7. Generator is truly infinite (can step past any threshold)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prime_engine import (
    digital_root, is_prime, prime_generator, first_n_primes,
    grid_label, DR_PRIME_ALLOWED, DR_PROVEN_EMPTY
)


# ---------------------------------------------------------------------------
# Reference sieve (Eratosthenes) for ground truth
# ---------------------------------------------------------------------------

def sieve(limit):
    """Return set of primes up to limit."""
    is_p = [True] * (limit + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_p[i]:
            for j in range(i*i, limit+1, i):
                is_p[j] = False
    return {i for i in range(2, limit+1) if is_p[i]}


PRIMES_10000 = sieve(10000)


# ---------------------------------------------------------------------------
# 1. digital_root correctness
# ---------------------------------------------------------------------------

def test_digital_root_basic():
    cases = {
        1: 1, 9: 9, 10: 1, 18: 9, 19: 1, 27: 9,
        100: 1, 999: 9, 37: 1, 5: 5, 13: 4, 37: 1,
    }
    for n, expected in cases.items():
        assert digital_root(n) == expected, f"DR({n}) expected {expected}, got {digital_root(n)}"


def test_digital_root_divisibility_by_3():
    """DR(n) ∈ {3,6,9} ↔ 3|n."""
    for n in range(1, 500):
        dr = digital_root(n)
        if dr in {3, 6, 9}:
            assert n % 3 == 0, f"DR({n})={dr} but 3 ∤ {n}"
        else:
            assert n % 3 != 0, f"DR({n})={dr} but 3 | {n}"


# ---------------------------------------------------------------------------
# 2. is_prime() agreement with sieve
# ---------------------------------------------------------------------------

def test_is_prime_matches_sieve_up_to_10000():
    errors = []
    for n in range(0, 10001):
        engine_says = is_prime(n)
        sieve_says  = n in PRIMES_10000
        if engine_says != sieve_says:
            errors.append((n, engine_says, sieve_says))
    assert not errors, f"is_prime disagreements: {errors[:10]}"


# ---------------------------------------------------------------------------
# 3. prime_generator() — no misses, no false positives up to 1000
# ---------------------------------------------------------------------------

def test_generator_correctness_up_to_1000():
    primes_1000 = {p for p in PRIMES_10000 if p <= 1000}
    generated = set()
    for p, label, dr in prime_generator(2):
        if p > 1000:
            break
        generated.add(p)

    missed   = primes_1000 - generated
    spurious = generated - primes_1000
    assert not missed,   f"Missed primes: {sorted(missed)[:10]}"
    assert not spurious, f"Spurious composites: {sorted(spurious)[:10]}"


def test_generator_yields_in_order():
    prev = 0
    for p, _, _ in prime_generator(2):
        if p > 500:
            break
        assert p > prev, f"Out of order: {prev} then {p}"
        prev = p


# ---------------------------------------------------------------------------
# 4. DR pre-filter completeness: no prime > 3 has DR ∈ {3,6,9}
# ---------------------------------------------------------------------------

def test_dr_filter_no_prime_dr_3_6_9():
    """Empirical verification up to 10000 that the proven theorem holds."""
    violations = []
    for p in PRIMES_10000:
        if p <= 3:
            continue
        dr = digital_root(p)
        if dr in DR_PROVEN_EMPTY:
            violations.append((p, dr))
    assert not violations, f"DR-filter theorem violated: {violations[:5]}"


def test_composites_with_dr_prime_allowed_exist():
    """Confirm false positives exist (filter is not sufficient alone)."""
    false_positives = [
        n for n in range(5, 100)
        if digital_root(n) in DR_PRIME_ALLOWED and n not in PRIMES_10000 and n % 2 != 0
    ]
    assert len(false_positives) > 0, "Expected composites in the candidate set"


# ---------------------------------------------------------------------------
# 5. Alpha grid labels for known primes
# ---------------------------------------------------------------------------

def test_grid_labels_known_primes():
    known = {
        2: "LL-E",    # DR=2
        3: "LH-O",    # DR=3
        5: "A51",     # DR=5
        7: "RL-O",    # DR=7
        11: "LL-E",   # DR=2
        13: "LH-E",   # DR=4
        17: "RH-E",   # DR=8
        19: "LL-O",   # DR=1
        23: "A51",    # DR=5
        29: "LL-E",   # DR=2
        31: "LH-E",   # DR=4
        37: "LL-O",   # DR=1
        41: "A51",    # DR=5
        43: "RL-O",   # DR=7
        47: "LL-E",   # DR=2  (4+7=11→2)
    }
    for p, expected_label in known.items():
        got = grid_label(p)
        assert got == expected_label, f"grid_label({p}) expected {expected_label}, got {got}"


# ---------------------------------------------------------------------------
# 6. RL-E (DR=6) and RH-O (DR=9) positions: zero primes yielded up to 10000
# ---------------------------------------------------------------------------

def test_proven_empty_positions_absent_from_generator():
    empty_dr_primes = []
    for p, label, dr in prime_generator(2):
        if p > 10000:
            break
        if dr in DR_PROVEN_EMPTY and p > 3:
            empty_dr_primes.append((p, label, dr))
    assert not empty_dr_primes, f"Generator yielded primes at proven-empty DRs: {empty_dr_primes}"


# ---------------------------------------------------------------------------
# 7. Generator is infinite (can exceed any threshold)
# ---------------------------------------------------------------------------

def test_generator_reaches_large_prime():
    target = 100003   # known prime
    found = False
    for p, label, dr in prime_generator(100000):
        if p == target:
            found = True
            break
        if p > 100010:
            break
    assert found, f"Expected to find prime {target} in generator"


def test_generator_dr_distribution_roughly_uniform():
    """Among first 1000 primes > 3, each allowed DR class should appear."""
    counts = {dr: 0 for dr in DR_PRIME_ALLOWED}
    n_collected = 0
    for p, label, dr in prime_generator(5):
        if n_collected >= 1000:
            break
        counts[dr] += 1
        n_collected += 1
    for dr in DR_PRIME_ALLOWED:
        assert counts[dr] > 0, f"DR={dr} class produced no primes in first 1000"
    # Each class should have between 10% and 30% (uniform expectation ~16.7%)
    for dr, cnt in counts.items():
        assert 80 < cnt < 250, f"DR={dr} count {cnt} suspiciously far from uniform"


# ---------------------------------------------------------------------------
# 8. first_n_primes helper
# ---------------------------------------------------------------------------

def test_first_n_primes():
    result = first_n_primes(10)
    primes_only = [p for p, _, _ in result]
    assert primes_only == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29], \
        f"first_n_primes(10) wrong: {primes_only}"


# ---------------------------------------------------------------------------
# Run all tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        test_digital_root_basic,
        test_digital_root_divisibility_by_3,
        test_is_prime_matches_sieve_up_to_10000,
        test_generator_correctness_up_to_1000,
        test_generator_yields_in_order,
        test_dr_filter_no_prime_dr_3_6_9,
        test_composites_with_dr_prime_allowed_exist,
        test_grid_labels_known_primes,
        test_proven_empty_positions_absent_from_generator,
        test_generator_reaches_large_prime,
        test_generator_dr_distribution_roughly_uniform,
        test_first_n_primes,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR {test.__name__}: {type(e).__name__}: {e}")
            failed += 1

    print()
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    if failed:
        sys.exit(1)
