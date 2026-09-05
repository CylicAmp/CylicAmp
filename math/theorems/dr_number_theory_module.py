# math/theorems/dr_number_theory_module.py
"""
Digital Root Number Theory Module
==================================
14 functions in 6 sections:

  Digital Roots     (3): dr_fast, dr_iter, dr_validate
  Perfect Numbers   (3): euclid_euler, perfect_info, perfect_list
  37-Family Law     (3): family37_entry, family37_sequence, family37_pattern
  DR-Fibonacci      (2): dr_fibonacci, dr_fibonacci_analysis
  Prime 21 (73)     (1): prime21_analysis
  Utilities         (2): gaps, check_input

Key results verified:
  - 37 ≡ 1 (mod 9) => dr(37k) = dr(k) for all k  (37-family law)
  - 73 ≡ 1 (mod 9) => dr(73k) = dr(k); 73 is the 21st prime, emirp of 37
  - Fibonacci digital roots have period 24, sum-of-cycle = 117
  - dr(n) = 9 if 9|n else n % 9  (for n > 0)
  - Perfect numbers: dr(6)=6, dr(28)=1, dr(496)=1, dr(8128)=1
"""

from math import isqrt


# ── Utilities ─────────────────────────────────────────────────────────────────

def check_input(n, name: str = 'n') -> int:
    """Validate that n is a non-negative integer."""
    if not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"{name} must be >= 0, got {n}")
    return n


def gaps(seq: list) -> list:
    """Consecutive differences in a sequence."""
    if len(seq) < 2:
        return []
    return [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]


# ── internal helper ───────────────────────────────────────────────────────────

def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# ── Digital Roots ─────────────────────────────────────────────────────────────

def dr_fast(n: int) -> int:
    """Digital root via single formula O(1).  dr(0)=0, dr(9k)=9, else n%9."""
    check_input(n)
    if n == 0:
        return 0
    r = n % 9
    return r if r != 0 else 9


def dr_iter(n: int) -> int:
    """Digital root by repeated digit sum until single digit."""
    check_input(n)
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def dr_validate(n: int) -> int:
    """Return dr(n) after asserting fast == iterative."""
    f, i = dr_fast(n), dr_iter(n)
    assert f == i, f"dr_fast({n})={f} != dr_iter({n})={i}"
    return f


# ── Perfect Numbers ───────────────────────────────────────────────────────────

def euclid_euler(p: int):
    """
    Return the Euclid-Euler perfect number 2^(p-1)*(2^p-1) if 2^p-1 is prime,
    else None.  p must be prime for 2^p-1 to have a chance of being prime.
    """
    check_input(p, 'p')
    mp = (1 << p) - 1          # 2^p - 1
    if not _is_prime(mp):
        return None
    return (1 << (p - 1)) * mp


def perfect_info(n: int) -> dict:
    """Properties of a (candidate) perfect number n."""
    check_input(n, 'n')
    proper_divs = [d for d in range(1, n) if n % d == 0]
    return {
        'n':               n,
        'proper_divisors': proper_divs,
        'divisor_sum':     sum(proper_divs),
        'is_perfect':      sum(proper_divs) == n,
        'digital_root':    dr_fast(n),
        'mod_9':           n % 9,
    }


def perfect_list(k: int) -> list:
    """Return the first k perfect numbers (Euclid-Euler form, Mersenne exponents)."""
    check_input(k, 'k')
    # Mersenne prime exponents in order; extend if k > 4 needed
    candidates = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127]
    result = []
    for p in candidates:
        pn = euclid_euler(p)
        if pn is not None:
            result.append(pn)
            if len(result) == k:
                break
    return result


# ── 37-Family Law ─────────────────────────────────────────────────────────────

def family37_entry(n: int) -> bool:
    """
    Check if n is in the 37-family: n ≡ 1 (mod 9).
    Every such n satisfies dr(n*k) = dr(k) for all positive integers k.
    37 and 73 are both prime members; 37 is the canonical entry point.
    """
    check_input(n)
    return n % 9 == 1


def family37_sequence(limit: int) -> list:
    """
    Multiples of 37 up to limit.  Since 37 ≡ 1 (mod 9), dr(37m) = dr(m).
    """
    check_input(limit, 'limit')
    return list(range(37, limit + 1, 37))


def family37_pattern(k: int) -> list:
    """
    Return list of (m, 37m, dr(37m), dr(m)) for m = 1..k.
    Demonstrates that dr(37m) == dr(m) for all m.
    """
    check_input(k, 'k')
    return [(m, 37 * m, dr_fast(37 * m), dr_fast(m)) for m in range(1, k + 1)]


# ── DR-Fibonacci ──────────────────────────────────────────────────────────────

# Period-24 digital root cycle of Fibonacci numbers (F_1=1, F_2=1, ...)
_DR_FIB_CYCLE = [1, 1, 2, 3, 5, 8, 4, 3, 7, 1, 8, 9,
                 8, 8, 7, 6, 4, 1, 5, 6, 2, 8, 1, 9]


def dr_fibonacci(n: int) -> int:
    """Digital root of the nth Fibonacci number (1-indexed).  Period 24."""
    check_input(n, 'n')
    if n == 0:
        return 0    # F_0 = 0
    return _DR_FIB_CYCLE[(n - 1) % 24]


def dr_fibonacci_analysis() -> dict:
    """
    Compute and analyse the period-24 DR cycle of Fibonacci numbers.
    Verifies the hardcoded cycle against actual Fibonacci computation.
    """
    a, b = 1, 1
    actual_dr = []
    for _ in range(48):
        actual_dr.append(dr_fast(a))
        a, b = b, a + b

    assert actual_dr[:24] == actual_dr[24:], "Fibonacci DR period is not 24"
    cycle = actual_dr[:24]
    assert cycle == _DR_FIB_CYCLE, "Hardcoded cycle mismatch"

    return {
        'period':          24,
        'cycle':           cycle,
        'cycle_sum':       sum(cycle),        # 117
        'values_present':  sorted(set(cycle)),
        'count_per_value': {v: cycle.count(v) for v in sorted(set(cycle))},
    }


# ── Prime 21 (73) ─────────────────────────────────────────────────────────────

def prime21_analysis() -> dict:
    """
    Complete analysis of 73 as the 21st prime.

    Key facts:
      - 73 is prime; rank among primes = 21
      - 37 is the emirp (digit-reverse) of 73; also prime
      - 73 ≡ 1 (mod 9) => dr(73) = 1; 37 ≡ 1 (mod 9) => dr(37) = 1
      - 73 and 37 are both in the 37-family (≡ 1 mod 9)
      - bin(73) = 1001001 — a binary palindrome
      - 37 × 73 = 2701; dr(2701) = 1
      - Rank index: 21 = 3 × 7; dr(21) = 3; dr(3 × 7) = dr(21) = 3
      - 37-family law holds for 73: dr(73k) = dr(k) for all k
    """
    n = 73
    emirp = 37

    primes_to_73 = [p for p in range(2, 74) if _is_prime(p)]
    rank = len(primes_to_73)

    bin73 = bin(n)[2:]   # '1001001'
    is_bin_palindrome = (bin73 == bin73[::-1])

    law_holds = all(dr_fast(n * k) == dr_fast(k) for k in range(1, 200))
    emirp_law = all(dr_fast(emirp * k) == dr_fast(k) for k in range(1, 200))

    return {
        'n':                   n,
        'rank_21st_prime':     rank,
        'is_prime':            _is_prime(n),
        'emirp':               emirp,
        'emirp_is_prime':      _is_prime(emirp),
        'dr_73':               dr_fast(n),        # 1
        'dr_37':               dr_fast(emirp),    # 1
        'mod_9_73':            n % 9,             # 1
        'mod_9_37':            emirp % 9,          # 1
        'binary_73':           bin73,              # '1001001'
        'binary_palindrome':   is_bin_palindrome,  # True
        'product_37x73':       n * emirp,          # 2701
        'dr_product':          dr_fast(n * emirp), # 1
        'rank_21_factored':    (3, 7),
        'rank_21_dr':          dr_fast(21),        # 3
        '37_family_law_73':    law_holds,
        '37_family_law_37':    emirp_law,
        'both_in_family':      family37_entry(n) and family37_entry(emirp),
    }


# ── verify ────────────────────────────────────────────────────────────────────

def verify():
    print("Digital Root Number Theory Module — 14 Functions\n")

    # ── Digital Roots ─────────────────────────────────────────────────────────
    print("=" * 60)
    print("DIGITAL ROOTS")
    print("=" * 60)

    test_cases = [(0,0),(1,1),(9,9),(10,1),(18,9),(37,1),(73,1),
                  (100,1),(444,3),(999,9),(3329,8),(10101,3)]
    for n, expected in test_cases:
        assert dr_validate(n) == expected, f"dr({n}) should be {expected}"

    print(f"  dr_fast vs dr_iter agree on {len(test_cases)} test cases  OK")
    print(f"  Notable: dr(444)=3 (NOT 9); dr(37)=1; dr(73)=1; dr(3329)=8  OK")
    print(f"  Formula: dr(n) = 9 if 9|n else n%9  (n>0)  OK\n")

    # ── Perfect Numbers ───────────────────────────────────────────────────────
    print("=" * 60)
    print("PERFECT NUMBERS")
    print("=" * 60)

    first4 = perfect_list(4)
    assert first4 == [6, 28, 496, 8128]

    for pn in first4:
        info = perfect_info(pn)
        assert info['is_perfect'], f"{pn} not perfect"

    assert dr_fast(6)    == 6
    assert dr_fast(28)   == 1
    assert dr_fast(496)  == 1
    assert dr_fast(8128) == 1

    print(f"  First 4 perfect numbers: {first4}  OK")
    print(f"  dr(6)=6, dr(28)=1, dr(496)=1, dr(8128)=1  OK")
    print(f"  euclid_euler: p in {{2,3,5,7}} => Mersenne primes  OK\n")

    # ── 37-Family Law ─────────────────────────────────────────────────────────
    print("=" * 60)
    print("37-FAMILY LAW")
    print("=" * 60)

    # Law: n ≡ 1 (mod 9) => dr(n*k) = dr(k)
    for n in [1, 10, 19, 28, 37, 46, 55, 64, 73, 82, 91, 100]:
        assert family37_entry(n), f"{n} should be in family"
        assert all(dr_fast(n * k) == dr_fast(k) for k in range(1, 100))

    assert not family37_entry(36)
    assert not family37_entry(38)

    pat = family37_pattern(9)
    assert all(row[2] == row[3] for row in pat), "dr(37m) != dr(m) somewhere"

    seq = family37_sequence(200)
    g = gaps(seq)
    assert all(x == 37 for x in g), "multiples of 37 should be uniformly spaced"

    print(f"  37 ≡ 1 (mod 9); dr(37k) = dr(k) for k=1..99  OK")
    print(f"  73 ≡ 1 (mod 9); dr(73k) = dr(k) for k=1..99  OK")
    print(f"  Family members (≡1 mod 9): 1,10,19,28,37,46,55,64,73,...  OK")
    print(f"  Pattern [dr(37m) for m=1..9]: {[r[2] for r in pat]}  OK")
    print(f"  Gaps in multiples-of-37 sequence: all 37  OK\n")

    # ── DR-Fibonacci ──────────────────────────────────────────────────────────
    print("=" * 60)
    print("DR-FIBONACCI")
    print("=" * 60)

    info = dr_fibonacci_analysis()
    assert info['period'] == 24
    assert info['cycle_sum'] == 117    # verified: sum of period-24 cycle
    assert info['cycle'] == _DR_FIB_CYCLE

    # Spot-checks: F_1=1,F_6=8,F_12=144(dr=9),F_24=46368(dr=9)
    assert dr_fibonacci(1)  == 1
    assert dr_fibonacci(6)  == 8
    assert dr_fibonacci(12) == 9
    assert dr_fibonacci(24) == 9
    assert dr_fibonacci(25) == dr_fibonacci(1)   # period

    print(f"  Period: {info['period']}  OK")
    print(f"  Cycle: {info['cycle']}")
    print(f"  Cycle sum: {info['cycle_sum']}  OK")
    print(f"  Values present: {info['values_present']}  (missing: 0)  OK\n")

    # ── Prime 21 (73) ─────────────────────────────────────────────────────────
    print("=" * 60)
    print("PRIME 21 (73)")
    print("=" * 60)

    r = prime21_analysis()
    assert r['rank_21st_prime'] == 21
    assert r['is_prime']
    assert r['emirp_is_prime']
    assert r['dr_73'] == 1
    assert r['dr_37'] == 1
    assert r['binary_palindrome']
    assert r['product_37x73'] == 2701
    assert r['dr_product'] == 1
    assert r['both_in_family']
    assert r['37_family_law_73']
    assert r['37_family_law_37']

    print(f"  73 is the {r['rank_21st_prime']}st prime  OK")
    print(f"  Emirp: 37  (both prime, digit-reverses of each other)  OK")
    print(f"  dr(73)=1, dr(37)=1  (both ≡ 1 mod 9)  OK")
    print(f"  bin(73) = {r['binary_73']}  (binary palindrome)  OK")
    print(f"  37 x 73 = {r['product_37x73']}, dr = {r['dr_product']}  OK")
    print(f"  21 = 3 x 7; dr(21) = {r['rank_21_dr']}  OK")
    print(f"  37-family law holds for both 37 and 73 (k=1..199)  OK\n")

    # ── Utilities ─────────────────────────────────────────────────────────────
    print("=" * 60)
    print("UTILITIES")
    print("=" * 60)

    assert gaps([1, 4, 9, 16, 25]) == [3, 5, 7, 9]
    assert gaps([37, 74, 111])      == [37, 37]
    assert gaps([])                 == []
    assert gaps([5])                == []

    try:
        check_input(-1)
        assert False, "should raise"
    except ValueError:
        pass
    try:
        check_input(1.5)
        assert False, "should raise"
    except TypeError:
        pass

    print(f"  gaps([1,4,9,16,25]) = {gaps([1,4,9,16,25])}  OK")
    print(f"  gaps([37,74,111])   = {gaps([37,74,111])}  OK")
    print(f"  check_input: rejects negative and non-int  OK\n")

    # ── Summary ───────────────────────────────────────────────────────────────
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print("""
  FUNCTIONS (14 total):
    Digital Roots  (3): dr_fast, dr_iter, dr_validate
    Perfect Nums   (3): euclid_euler, perfect_info, perfect_list
    37-Family      (3): family37_entry, family37_sequence, family37_pattern
    DR-Fibonacci   (2): dr_fibonacci, dr_fibonacci_analysis
    Prime 21 (73)  (1): prime21_analysis
    Utilities      (2): gaps, check_input

  KEY RESULTS:
    dr(n) = 9 if 9|n else n%9  (O(1) formula)
    37 ≡ 73 ≡ 1 (mod 9); dr(37k) = dr(73k) = dr(k) for all k
    Perfect numbers 6,28,496,8128 verified; dr in {1,6}
    Fibonacci DR period = 24; cycle sum = 117
    73 = 21st prime; emirp of 37; binary palindrome 1001001
    37 x 73 = 2701; dr(2701) = 1
    """)

    print("All assertions passed.")


if __name__ == "__main__":
    verify()
