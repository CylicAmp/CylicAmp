"""
CylicAmp Experiment Runner

Runs all verified experiments using the existing module stack.
"""
import time
import math

from cylicamp.euler_totient import totient_product_formula, rsa_demo
from cylicamp.chebyshev_bias import demonstrate as chebyshev_demo, _sieve, chi3
from cylicamp.pipeline import print_pipeline


def verify_totient(n_max: int = 40) -> bool:
    """Cross-check product formula against GCD count for n=1..n_max."""
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    for n in range(1, n_max + 1):
        phi_formula  = totient_product_formula(n)
        phi_iterative = sum(1 for i in range(1, n + 1) if gcd(i, n) == 1)
        if phi_formula != phi_iterative:
            print(f"  MISMATCH at n={n}: formula={phi_formula}, iterative={phi_iterative}")
            return False
    return True


def analyze_twin_primes(limit: int = 1_000_000) -> None:
    """Twin prime modular bias analysis (uses existing sieve)."""
    print(f"  Running sieve up to {limit:,}...")
    S = _sieve(limit)

    twin_count = 0
    mod3 = {0: 0, 1: 0, 2: 0}
    mod4 = {1: 0, 3: 0}

    for p in range(3, limit - 1, 2):
        if S[p] and S[p + 2]:
            twin_count += 1
            mod3[p % 3] += 1
            if p % 4 in mod4:
                mod4[p % 4] += 1

    print(f"  Found {twin_count:,} twin prime pairs")
    print(f"  Mod-3 distribution: {mod3}")
    print(f"  Twin primes p ≡ 1 (mod 4): {mod4[1]:,}")
    print(f"  Twin primes p ≡ 3 (mod 4): {mod4[3]:,}")
    # Structural necessity: p ≡ 2 (mod 3) always for twin prime lower element
    violations = mod3[0] + mod3[1]
    print(f"  Violations of p≡2(mod3): {violations}  "
          f"{'STRUCTURAL NECESSITY CONFIRMED' if violations == 0 else 'FAILED'}")


def main():
    print("=" * 60)
    print("  CYLICAMP EXPERIMENT RUNNER")
    print("=" * 60)

    # --- Totient verification ---
    print("\n[1] TOTIENT & RSA VERIFICATION")
    print("-" * 40)
    t0 = time.perf_counter()
    ok = verify_totient(40)
    t1 = time.perf_counter()
    if ok:
        print(f"  Product formula matches GCD count for n=1..40  ✓")
    print(f"  Time: {(t1-t0)*1000:.2f}ms")
    rsa_demo(p=61, q=53)

    # --- Twin prime bias ---
    print("\n[2] TWIN PRIME BIAS ANALYSIS")
    print("-" * 40)
    t0 = time.perf_counter()
    analyze_twin_primes(limit=1_000_000)
    t1 = time.perf_counter()
    print(f"  Time: {t1-t0:.4f}s")

    # --- Chebyshev bias (full) ---
    print("\n[3] CHEBYSHEV BIAS (full report)")
    print("-" * 40)
    t0 = time.perf_counter()
    chebyshev_demo(limit=1_000_000)
    t1 = time.perf_counter()
    print(f"\n  Time: {t1-t0:.4f}s")

    # --- Pipeline on key numbers ---
    print("\n[4] PIPELINE: KEY NUMBERS")
    print("-" * 40)
    for n in [3, 9, 37, 432, 419]:
        print_pipeline(n)

    print("\n" + "=" * 60)
    print("  ALL EXPERIMENTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
