"""
Run Experiments — Twin Prime Bias + Totient, rooted in GF(37)
"""

import time
import euler_totient
import prime_bias_analyzer


def verify_rsa_totient(n: int) -> bool:
    phi = euler_totient.compute_phi(n)
    iterative = sum(1 for i in range(1, n + 1) if euler_totient.gcd(i, n) == 1)
    return phi == iterative


def main():
    print("=== MATHEMATICAL EXPERIMENTS — GF(37) FRAMEWORK ===\n")

    # Totient verification
    print("--- Totient & RSA Verification (n=1..40) ---")
    ok = all(verify_rsa_totient(n) for n in range(1, 41))
    print(f"  Totient agreement n=1..40: {'PASS' if ok else 'FAIL'}")

    # GF(37) totient connections
    info = euler_totient.gf37_connections()
    print(f"  phi(37)           = {info['phi_37']}  (= ord₃₇(2))")
    print(f"  phi(phi(37))      = {info['phi_phi_37']}  (= count of primitive roots mod 37)")
    print(f"  |QR subgroup|     = {info['qr_subgroup_order']}  (index 2 in G)")
    print(f"  [(ℤ/37ℤ)*:QR]    = {info['index_qr_in_G']}  ↔ π₁(SO(3)) ≅ ℤ₂\n")

    # Twin prime analysis
    print("--- Twin Prime Bias Analysis ---")
    t0 = time.perf_counter()
    prime_bias_analyzer.analyze_twin_primes(limit=1_000_000)
    elapsed = time.perf_counter() - t0
    print(f"\n  Sieve time: {elapsed:.4f}s")
    print("\n=== DONE ===")


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    main()
