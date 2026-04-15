#!/usr/bin/env python3
"""
Lucas-Lehmer Sequence — Symbolic Verification via SymPy
========================================================
Tests α = 2 + √2 in Z[√2] / M for Mersenne primality.
Runs the Lucas-Lehmer sequence s_{i+1} = s_i² - 2 (mod M)
and confirms s_{p-2} ≡ 0 iff M = 2^p - 1 is prime.

© 2026 Michael Warren Song. All Rights Reserved.
"""

import sympy as sp
from sympy import sqrt, Mod, simplify, expand, gcd

# Define α = 2 + √2 and conjugate β = 2 - √2
sqrt2 = sqrt(2)
alpha = 2 + sqrt2
beta  = 2 - sqrt2


def run_ll_sequence(p, verbose=True):
    """
    Run the Lucas-Lehmer sequence for M = 2^p - 1.
    Returns True if M is prime.
    """
    M = 2**p - 1

    if verbose:
        print(f"p = {p},  M = 2^{p} - 1 = {M}")
        print(f"α = 2 + √2,  β = 2 - √2")
        print(f"Sequence s_i = α^{{2^i}} + β^{{2^i}} mod M")
        print()

    s = 4
    if verbose:
        print(f"  s_0 = {s}")

    for i in range(1, p - 1):
        s = Mod(s**2 - 2, M)
        if verbose:
            print(f"  s_{i} ≡ {s}  (mod {M})")

    is_prime = (s == 0)

    if verbose:
        print()
        print(f"  Final s_{{p-2}} = s_{p-2} ≡ {s}  (mod {M})")
        print(f"  → {'PRIME ✓' if is_prime else 'COMPOSITE ✗'}")
        print()

    return is_prime


def run_all(test_primes=None):
    if test_primes is None:
        # Test odd primes up to 23
        test_primes = [p for p in range(3, 24) if sp.isprime(p)]

    print("=" * 55)
    print("  Lucas-Lehmer Symbolic Verification")
    print("  © 2026 Michael Warren Song")
    print("=" * 55)
    print()

    print(f"  {'p':>4}  {'M = 2^p-1':>10}  {'LL result':>10}  {'Confirmed':>10}")
    print("  " + "-" * 42)

    for p in test_primes:
        M = 2**p - 1
        ll   = run_ll_sequence(p, verbose=False)
        conf = sp.isprime(M)
        match = "✓" if ll == conf else "✗ MISMATCH"
        print(f"  {p:>4}  {M:>10}  {'Prime' if ll else 'Composite':>10}  {match:>10}")

    print()


if __name__ == "__main__":
    # Detailed run for p=5
    print("── Detailed run: p = 5 ──")
    run_ll_sequence(5, verbose=True)

    print("── Detailed run: p = 7 ──")
    run_ll_sequence(7, verbose=True)

    # Summary table
    run_all()
