# math/theorems/palindrome_divisors_ord10_audit.py
"""
Three-section audit:

A. 12-digit palindromes from 191919×k and 111111×k families.
B. All 128 divisors of 191919919191 clustered by DR and mod-37.
C. Multiplicative order ord_m(10) table; digital-root utility classes.
"""

import math
from collections import defaultdict


def is_palindrome(n: int) -> bool:
    s = str(n)
    return s == s[::-1]


def dr(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


def mul_order(base: int, m: int) -> int | None:
    """Multiplicative order of base mod m, or None if gcd(base,m) != 1."""
    if math.gcd(base, m) != 1:
        return None
    k, val = 1, base % m
    while val != 1:
        val = (val * base) % m
        k += 1
        if k > m:           # should not happen for valid m
            return None
    return k


def pow_sequence(base: int, m: int, length: int = 8) -> list:
    """[base^0 mod m, base^1 mod m, ..., base^(length-1) mod m]."""
    return [(base ** i) % m for i in range(length)]


# ── A. Palindrome search ──────────────────────────────────────────────────────

def verify_palindromes():
    print("=" * 70)
    print("A. 12-digit palindromes")
    print("=" * 70)

    # 191919 × k family
    results_191919 = []
    for k in range(521053, 530000):          # 191919×521053 ≈ 1.0e11 first 12-digit
        prod = 191919 * k
        if prod >= 10 ** 12:
            break
        if is_palindrome(prod):
            results_191919.append((k, prod))

    # 111111 × k family (structural candidates from the exposition)
    results_111111 = []
    for k in [900991, 1001001, 1801981, 2702971]:
        prod = 111111 * k
        if is_palindrome(prod):
            results_111111.append((k, prod))

    # Broader 111111 scan for 12-digit palindromes
    for k in range(900901, 1000000):
        prod = 111111 * k
        if len(str(prod)) != 12:
            continue
        if is_palindrome(prod):
            results_111111.append((k, prod))
            if len(results_111111) >= 5:
                break

    print(f"\n  191919 × k palindromes found: {len(results_191919)}")
    for k, p in results_191919[:10]:
        print(f"    k={k}  product={p}  DR={dr(p)}  mod37={p%37}")

    print(f"\n  111111 × k palindromes:")
    for k, p in results_111111:
        print(f"    k={k}  product={p}  DR={dr(p)}  mod37={p%37}")

    # Verify 111111 × 900991 = 100110011001
    assert 111111 * 900991 == 100110011001
    assert is_palindrome(100110011001)
    print(f"\n  111111 × 900991 = 100110011001  palindrome ✓")
    print()


# ── B. Divisors of 191919919191 — DR and mod-37 clusters ─────────────────────

PRIMES_191919919191 = [3, 7, 11, 13, 37, 167, 10343]
N = 191919919191


def build_divisors() -> list:
    divisors = [1]
    for p in PRIMES_191919919191:
        divisors = divisors + [d * p for d in divisors]
    return sorted(divisors)


def verify_divisors():
    print("=" * 70)
    print("B. Divisors of 191919919191 — DR and mod-37 clusters")
    print("=" * 70)

    divisors = build_divisors()
    assert len(divisors) == 128        # 2^7 squarefree
    assert divisors[0] == 1
    assert divisors[-1] == N
    assert all(N % d == 0 for d in divisors)

    # DR clusters
    dr_clusters: dict = defaultdict(list)
    for d in divisors:
        dr_clusters[dr(d)].append(d)

    # mod-37 clusters
    mod37_clusters: dict = defaultdict(list)
    for d in divisors:
        mod37_clusters[d % 37].append(d)

    print(f"\n  Total divisors: {len(divisors)}  (2^7 = 128)  ✓")

    print(f"\n  DR clusters:")
    for r in sorted(dr_clusters):
        cnt = len(dr_clusters[r])
        print(f"    DR{r} [{cnt:>3}]: {dr_clusters[r][:6]}"
              + (" ..." if cnt > 6 else ""))

    print(f"\n  mod-37 clusters (non-empty):")
    for r in sorted(mod37_clusters):
        cnt = len(mod37_clusters[r])
        print(f"    ≡{r:>2} [{cnt:>3}]: {mod37_clusters[r][:4]}"
              + (" ..." if cnt > 4 else ""))

    # 37 | divisor iff 37 | d, i.e. 37 is a factor
    divs_divisible_37 = [d for d in divisors if d % 37 == 0]
    assert len(divs_divisible_37) == 64    # half of 128 (37 is one of 7 factors)
    print(f"\n  Divisors divisible by 37: {len(divs_divisible_37)}  (= 128/2 = 64)  ✓")
    print()


# ── C. Multiplicative order ord_m(10) and digital-root utility ───────────────

def verify_ord10():
    print("=" * 70)
    print("C. Multiplicative order ord_m(10) and digital-root utility")
    print("=" * 70)

    # Table rows: (m, expected_ord, invariant_class)
    # ord = None means gcd(10,m) > 1
    table = [
        (2,  None, "Terminal Boundary"),
        (3,  1,    "Perfect Invariant"),
        (4,  None, "Terminal Boundary"),
        (5,  None, "Terminal Boundary"),
        (6,  None, "Delayed Constant"),     # 10^i → 4 for i≥1
        (7,  6,    "Cyclic Permutation"),
        (8,  None, "Terminal Boundary"),
        (9,  1,    "Perfect Invariant Master"),
        (11, 2,    "Alternating Invariant"),
        (13, 6,    "Cyclic Permutation"),
        (37, 3,    "3-Block Invariant"),
    ]

    print(f"\n  {'m':>4}  {'ord':>5}  {'Powers 10^0..7 mod m':<40}  Class")
    print(f"  {'-'*90}")
    for m, expected_ord, cls in table:
        actual_ord = mul_order(10, m)
        assert actual_ord == expected_ord, \
            f"ord_{m}(10): expected {expected_ord}, got {actual_ord}"
        seq = pow_sequence(10, m, 8)
        print(f"  {m:>4}  {str(actual_ord or '∅'):>5}  {str(seq):<40}  {cls}")

    # Specific structural verifications
    # mod 9: 10 ≡ 1 → all powers = 1 → plain digit sum invariant
    assert all((10 ** i) % 9 == 1 for i in range(20))

    # mod 3: same
    assert all((10 ** i) % 3 == 1 for i in range(20))

    # mod 11: alternating 1, -1 (i.e. 1, 10)
    assert [(10 ** i) % 11 for i in range(6)] == [1, 10, 1, 10, 1, 10]

    # mod 37: period 3 — [1, 10, 26, 1, 10, 26, ...]
    assert [(10 ** i) % 37 for i in range(6)] == [1, 10, 26, 1, 10, 26]
    # Consequence: 3-digit block sum invariant
    # N = XYZ·WUV → N mod 37 = (XYZ + WUV) mod 37
    assert (191919 % 37) == ((191 + 919) % 37) == ((191 + 919) % 37)
    sample = 191919919191
    blocks = [int(str(sample)[i:i+3]) for i in range(0, 12, 3)]
    assert sample % 37 == sum(blocks) % 37
    assert blocks == [191, 919, 919, 191]
    assert sum(blocks) % 37 == 0    # 191+919+919+191 = 2220 = 60×37

    # mod 6: 10^0=1, 10^i≡4 for i≥1 (delayed constant)
    assert (10 ** 0) % 6 == 1
    assert all((10 ** i) % 6 == 4 for i in range(1, 10))

    print(f"\n  mod 9:  all 10^i ≡ 1  →  plain digit sum invariant  ✓")
    print(f"  mod 11: 10^i alternates 1,10  →  alternating digit sum  ✓")
    print(f"  mod 37: period 3 [1,10,26]  →  3-digit block sum  ✓")
    print(f"  mod 6:  delayed constant  →  units column treated separately  ✓")
    print(f"\n  Block verification (191919919191):")
    print(f"    blocks = {blocks}")
    print(f"    sum = {sum(blocks)} = 60×37  →  mod 37 = 0  ✓")
    print()
    print("All assertions passed.")


def verify():
    verify_palindromes()
    verify_divisors()
    verify_ord10()


if __name__ == "__main__":
    verify()
