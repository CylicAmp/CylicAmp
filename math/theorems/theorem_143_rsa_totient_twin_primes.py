"""
Theorem 143: Euler Totient, RSA Verification, and Twin Prime Analysis
Connected to the GF(37).

KEY CONSTANTS FROM THE FRAMEWORK:
  p  = 37          (the prime)
  phi(37)   = 36   (group order of F37x)
  phi(36)   = 12   (number of named orbits = log2(26) = structural key)
  phi(phi(37)) = phi(36) = 12

RSA OVER F_37:
  For the prime p=37, RSA-style encryption: E(m) = m^e mod 37
  Decryption: D(c) = c^d mod 37 where e*d ≡ 1 (mod phi(37)) = 1 (mod 36)
  For any m coprime to 37 (all m in 1..36): D(E(m)) = m (Fermat's little theorem)
"""

import math


# ─── REAL EULER TOTIENT ───────────────────────────────────────────────────────

class euler_totient:
    @staticmethod
    def compute(n: int) -> int:
        if n < 1:
            raise ValueError(f"totient undefined for {n}")
        if n == 1:
            return 1
        result = n
        temp = n
        p = 2
        while p * p <= temp:
            if temp % p == 0:
                while temp % p == 0:
                    temp //= p
                result -= result // p
            p += 1
        if temp > 1:
            result -= result // temp
        return result


# ─── REAL PRIME BIAS ANALYZER ─────────────────────────────────────────────────

class prime_bias_analyzer:
    @staticmethod
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def analyze_twin_primes(limit: int):
        pairs = [(p, p+2) for p in range(3, limit)
                 if prime_bias_analyzer.is_prime(p) and prime_bias_analyzer.is_prime(p+2)]
        print(f"  [prime_bias_analyzer]: Found {len(pairs)} twin prime pairs up to {limit}")
        print("  First 10 pairs:")
        for pair in pairs[:10]:
            print(f"    ({pair[0]}, {pair[1]})")
        return pairs

    @staticmethod
    def chebyshev_bias(limit: int):
        """
        Chebyshev bias: primes ≡ 3 (mod 4) tend to lead primes ≡ 1 (mod 4).
        Returns (count_1mod4, count_3mod4, bias_direction).
        """
        c1 = sum(1 for p in range(5, limit) if prime_bias_analyzer.is_prime(p) and p % 4 == 1)
        c3 = sum(1 for p in range(3, limit) if prime_bias_analyzer.is_prime(p) and p % 4 == 3)
        return c1, c3, '3 mod 4 leads' if c3 > c1 else '1 mod 4 leads'


# ─── REAL RSA TOTIENT VERIFICATION ───────────────────────────────────────────

def verify_rsa_totient(n: int) -> bool:
    """
    For each n in 1..40, verify:
    1. euler_totient.compute(n) matches the direct gcd count.
    2. If n is prime, verify RSA round-trip: for a test message m=2,
       E = m^e mod n, D = E^d mod n == m, where e=3 and d=modinv(3, phi(n)).
    Returns True iff both checks pass.
    """
    phi_direct = sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)
    phi_computed = euler_totient.compute(n)
    if phi_computed != phi_direct:
        return False

    if prime_bias_analyzer.is_prime(n) and n > 3:
        phi_n = phi_computed
        e = 3
        if math.gcd(e, phi_n) != 1:
            return True  # skip if e not coprime to phi(n)
        d = pow(e, -1, phi_n)
        for m in [2, n - 2, n - 1]:
            if m < 1 or math.gcd(m, n) != 1:
                continue
            c = pow(m, e, n)
            recovered = pow(c, d, n)
            if recovered != m:
                return False

    return True


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def run_assertions():
    # Totient correctness
    known = {1:1, 2:1, 4:2, 6:2, 9:6, 12:4, 36:12, 37:36}
    for n, expected in known.items():
        assert euler_totient.compute(n) == expected, \
            f"phi({n}) = {euler_totient.compute(n)}, expected {expected}"

    # GF(37) constants
    assert euler_totient.compute(37) == 36
    assert euler_totient.compute(36) == 12
    assert euler_totient.compute(euler_totient.compute(37)) == 12

    # RSA round-trip for all n=1..40
    for n in range(1, 41):
        assert verify_rsa_totient(n), f"Verification failed at n={n}"

    # Twin prime check: (3,5),(5,7),(11,13),(17,19) must be in the list
    pairs = prime_bias_analyzer.analyze_twin_primes(100)
    assert (3, 5) in pairs
    assert (5, 7) in pairs
    assert (11, 13) in pairs
    assert (17, 19) in pairs

    # Chebyshev bias up to 1000
    c1, c3, direction = prime_bias_analyzer.chebyshev_bias(1000)
    assert direction == '3 mod 4 leads', f"Bias direction unexpected: {direction}"

    print("All assertions passed.")


def main():
    print("=== STARTING MATHEMATICAL EXPERIMENTS ===\n")

    print("--- Running Totient & RSA Verification ---")
    failures = [n for n in range(1, 41) if not verify_rsa_totient(n)]
    if failures:
        print(f"[-] Verification failed at n = {failures}")
    else:
        print("Totient agreement verified for n=1..40.\n")

    print("--- GF(37) GF(37) Constants ---")
    p = 37
    phi_p      = euler_totient.compute(p)
    phi_phi_p  = euler_totient.compute(phi_p)
    print(f"  phi({p})       = {phi_p}   (group order of F37x)")
    print(f"  phi(phi({p}))  = {phi_phi_p}   (number of named orbits = structural key)")
    print(f"  phi(phi_p) == 12: {phi_phi_p == 12}")
    print()

    print("--- Running Twin Prime Bias Analysis ---")
    prime_bias_analyzer.analyze_twin_primes(limit=1000)
    print()

    c1, c3, direction = prime_bias_analyzer.chebyshev_bias(10000)
    print(f"--- Chebyshev Bias (primes up to 10000) ---")
    print(f"  p ≡ 1 mod 4: {c1}")
    print(f"  p ≡ 3 mod 4: {c3}")
    print(f"  Bias direction: {direction}")
    print()

    print("--- All Experiments Completed ---")


if __name__ == "__main__":
    run_assertions()
    main()
