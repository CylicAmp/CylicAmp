# math/theorems/primality_10343_audit.py
"""
Primality Investigation — 10343
================================
Claim: 10343 is prime — the terminal factor in
  191919919191 = 3 × 7 × 11 × 13 × 37 × 167 × 10343

Proof strategy: trial division by every prime p ≤ ⌊√10343⌋ = 101.
Exactly 26 such primes; none divides 10343.

Quick eliminations before the core loop:
  - Odd (last digit 3) → not divisible by 2
  - Digit sum 1+0+3+4+3 = 11, 11 mod 3 = 2 → not divisible by 3
  - Last digit ≠ 0,5 → not divisible by 5
"""

import math

N = 10343
N_FULL = 191919919191


def primes_up_to(limit: int) -> list:
    """Sieve of Eratosthenes."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]


def is_prime_trial(n: int) -> bool:
    if n < 2:
        return False
    for p in primes_up_to(int(math.isqrt(n))):
        if n % p == 0:
            return False
    return True


def verify():
    print("Primality Audit — 10343")
    print()

    # ── Quick eliminations ────────────────────────────────────────────────────
    assert N % 2 != 0,   "10343 divisible by 2"
    assert str(N)[-1] not in "05", "10343 ends in 0 or 5"
    digit_sum = sum(int(c) for c in str(N))
    assert digit_sum == 11
    assert digit_sum % 3 == 2   # ≡ 2 (mod 3) → not divisible by 3
    assert N % 3 != 0

    print(f"  n = {N}")
    print(f"  Odd: {N % 2 != 0}  (last digit {str(N)[-1]})  ✓")
    print(f"  Digit sum: {digit_sum},  {digit_sum} mod 3 = {digit_sum % 3}  → not div by 3  ✓")
    print(f"  Last digit not 0 or 5  → not div by 5  ✓")

    # ── Core: trial division by all primes ≤ ⌊√n⌋ ────────────────────────────
    root = math.isqrt(N)
    assert root == 101
    assert root * root <= N < (root + 1) ** 2

    trial_primes = primes_up_to(root)
    assert len(trial_primes) == 26
    assert trial_primes == [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101,
    ]

    residues = {p: N % p for p in trial_primes}
    assert all(r != 0 for r in residues.values()), \
        f"Found divisor: {[p for p,r in residues.items() if r == 0]}"

    print(f"\n  ⌊√{N}⌋ = {root}  ✓")
    print(f"  Primes to test ({len(trial_primes)}): {trial_primes}")
    print(f"\n  Residues (all non-zero):")
    for i, (p, r) in enumerate(residues.items()):
        end = "\n" if (i + 1) % 6 == 0 else ""
        print(f"    {N} mod {p:>3} = {r:>4}", end=end)
    print()

    # ── Primality conclusion ──────────────────────────────────────────────────
    assert is_prime_trial(N)
    print(f"\n  10343 is prime  ✓")

    # ── Full factorization integrity ──────────────────────────────────────────
    PRIMES = [3, 7, 11, 13, 37, 167, N]
    assert all(is_prime_trial(p) for p in PRIMES), "A factor is not prime"
    product = 1
    for p in PRIMES:
        product *= p
    assert product == N_FULL
    assert len(PRIMES) == 7
    assert len(set(PRIMES)) == 7   # all distinct → square-free

    print(f"\n  Full factorization integrity:")
    print(f"  {' × '.join(str(p) for p in PRIMES)} = {product}  ✓")
    print(f"  All 7 factors prime, all distinct (square-free)  ✓")
    print()
    print("All assertions passed.")


if __name__ == "__main__":
    verify()
