# math/theorems/phenomenological_effective_model_audit.py
"""
Phenomenological Effective Model — Digit-Boundary Mismatch Drive
=================================================================
Full arithmetic audit of 191919919191 structural claims.

Sections:
  1. Factorization — 7 distinct primes, square-free
  2. 111111 Fusion — 3×7×11×13×37 = 111111; cofactor 167×10343 = 1727281
  3. Digital root — digit sum 60, DR = 6
"""


def factorize(n: int) -> dict:
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def dr(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


N = 191919919191
PRIMES = [3, 7, 11, 13, 37, 167, 10343]


def verify():
    print("=" * 85)
    print("AUDIT: Phenomenological Effective Model — Digit-Boundary Mismatch Drive")
    print("=" * 85)

    # ── 1. Factorization ─────────────────────────────────────────────────────
    print("\n1. FACTORIZATION OF 191919919191")
    print("-" * 60)

    factors = factorize(N)
    assert factors == {p: 1 for p in PRIMES}

    distinct = sorted(factors.keys())
    assert distinct == PRIMES
    assert len(distinct) == 7

    exponents = list(factors.values())
    assert all(e == 1 for e in exponents)

    product = 1
    for p in PRIMES:
        product *= p
    assert product == N

    print(f"  Actual factorization: {factors}")
    print(f"  Distinct primes: {distinct}")
    print(f"  Count: {len(distinct)}")
    print(f"  Claim 'seven distinct primes': ✓ PASS")
    print(f"  Exponents: {exponents}")
    print(f"  All exponents = 1 (square-free): ✓ PASS")
    print(f"  Product verification: {product == N}")
    print(f"  3 × 7 × 11 × 13 × 37 × 167 × 10343 = {product}")
    print(f"  Match: ✓ PASS")

    # ── 2. 111111 Fusion ──────────────────────────────────────────────────────
    print("\n2. THE 111111 FUSION CLAIM")
    print("-" * 60)

    core = 3 * 7 * 11 * 13 * 37
    assert core == 111111

    cofactor = 167 * 10343
    assert cofactor == 1727281
    assert core * cofactor == N
    assert N // core == cofactor

    cofactor_factors = factorize(cofactor)
    assert cofactor_factors == {167: 1, 10343: 1}

    print(f"  3 × 7 × 11 × 13 × 37 = {core}")
    print(f"  Claim '111111': ✓ PASS")
    print()
    print(f"  Claim: 191919919191 = 111111 × 1727281")
    print(f"  191919919191 / 111111 = {N // core}")
    print(f"  111111 × 1727281 = {core * cofactor}")
    print(f"  Match: ✓ PASS")
    print()
    print(f"  Factorization of 1727281: {cofactor_factors}")
    print(f"  = 167 × 10343 = {cofactor}")
    print(f"  Match: ✓ PASS")

    # ── 3. Digital Root ───────────────────────────────────────────────────────
    print("\n3. DIGITAL ROOT OF 191919919191")
    print("-" * 60)

    digit_sum = sum(int(c) for c in str(N))
    assert digit_sum == 60
    assert dr(digit_sum) == 6
    assert dr(N) == 6
    assert 1 + (60 - 1) % 9 == 6

    print(f"  Sum of digits: {digit_sum}")
    print(f"  Digital root (formula): {dr(N)}")
    print(f"  Digital root (digits): 1 + (60 - 1) % 9 = {1 + (60-1)%9}")
    print(f"  Claim 'DR = 6': ✓ PASS")

    print()
    print("All assertions passed.")


if __name__ == "__main__":
    verify()
