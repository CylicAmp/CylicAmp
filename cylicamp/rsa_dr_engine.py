"""
RSA DR Engine — Verified RSA Key Generation + Digital Root Spine Audit
© 2026 Michael Warren Song. All Rights Reserved.

Cryptographic engine decoupled from ML anomaly metrics.
DR spine audit strictly enforces the 1/3 organic baseline ({3,6,9} ratio).

In production, import the ML framework:
    from cylicamp.security_ml_framework import digital_root, flux_ratio, spine_rigidity, NATURAL_FLUX_RATIO
"""

import math


# ── DR spine (1/3 organic baseline) ──────────────────────────────────────────

def digital_root(n: int) -> int:
    if n == 0:
        return 0
    return 1 + ((n - 1) % 9)

DR_FLUX_STATES    = {3, 6, 9}
DR_NATURAL_RATIO  = 1 / 3      # spine theorem: organic data hits {3,6,9} ≈ 33.3% of the time


# ── Primality ─────────────────────────────────────────────────────────────────

def miller_rabin_primality(n: int) -> bool:
    """Deterministic for n < 3,215,031,751 with witnesses [2,3,5,7,11]."""
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    if n in small_primes:
        return True
    if any(n % p == 0 for p in small_primes):
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for a in [2, 3, 5, 7, 11]:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


# ── Number theory utilities ───────────────────────────────────────────────────

def generate_primes_below(limit: int) -> list:
    sieve = [True] * limit
    sieve[0] = sieve[1] = False
    for p in range(2, int(math.isqrt(limit)) + 1):
        if sieve[p]:
            for i in range(p * p, limit, p):
                sieve[i] = False
    return [p for p, is_prime in enumerate(sieve) if is_prime]


def euler_totient(n: int) -> int:
    """phi(n) via trial factorisation."""
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result


# ── RSA engine ────────────────────────────────────────────────────────────────

class VerifiedRSAEngine:
    def __init__(self, limit: int = 300):
        self.primes    = generate_primes_below(limit)
        self.prime_gaps = [self.primes[i + 1] - self.primes[i]
                           for i in range(len(self.primes) - 1)]

    def rsa_key_roundtrip(self, p: int, q: int) -> dict:
        """Generate RSA parameters; raises ValueError if p or q are not prime."""
        if not miller_rabin_primality(p) or not miller_rabin_primality(q):
            raise ValueError(f"Security Fault: p={p} or q={q} failed primality check.")

        n   = p * q
        phi = (p - 1) * (q - 1)
        e   = 65537

        if math.gcd(e, phi) != 1:
            e = 3
            while math.gcd(e, phi) != 1:
                e += 2

        d = pow(e, -1, phi)
        return {"n": n, "phi": phi, "public_e": e, "private_d": d}

    def execute_verified_pipeline(self, p_val: int = 151, q_val: int = 199,
                                   iterations: int = 40) -> tuple:
        """
        Drive state through the modular transform and audit the DR distribution.

        Five interacting forces (5D state space):
            x1 = base state
            x2 = x^3 mod n  (cubic gravity)
            x3 = prime gap modifier
            x4 = totient shift phi(x)
            x5 = digital root (1–9)
        """
        rsa_keys    = self.rsa_key_roundtrip(p_val, q_val)
        n_mod       = rsa_keys["n"]
        gap_len     = len(self.prime_gaps)

        execution_log = []
        current_state = rsa_keys["public_e"]

        for i in range(iterations):
            gap   = self.prime_gaps[i % gap_len]
            phi_x = euler_totient(max(current_state + 1, 1))

            # 5D coordinates for this step
            x1 = current_state
            x2 = pow(current_state, 3, n_mod)
            x3 = gap
            x4 = phi_x
            # x5 assigned after state update

            current_state = (x2 + x3 + x4) % n_mod
            x5 = digital_root(current_state)

            execution_log.append({
                "step":        i + 1,
                "prime_gap":   gap,
                "state_value": current_state,
                "totient":     euler_totient(max(current_state, 1)),
                "digital_root": x5,
                "coords_5d":   (x1, x2, x3, x4, x5),
            })

        # DR spine audit — 1/3 organic baseline
        dr_values  = [e["digital_root"] for e in execution_log]
        spine_ratio = sum(1 for d in dr_values if d in DR_FLUX_STATES) / len(dr_values)

        meta = {
            "dr_spine_ratio":    spine_ratio,
            "dr_spine_deviation": abs(spine_ratio - DR_NATURAL_RATIO),
            "is_organic_signal": abs(spine_ratio - DR_NATURAL_RATIO) < 0.1,
        }
        return rsa_keys, execution_log, meta


# ── Execution ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    engine = VerifiedRSAEngine(limit=400)
    keys, results, meta = engine.execute_verified_pipeline(p_val=151, q_val=199)

    print("=== Verified RSA Parameter Configuration ===")
    print(f"Modulus (n): {keys['n']} | Totient Phi: {keys['phi']}")
    print(f"Public Exponent (e): {keys['public_e']} | Private Exponent (d): {keys['private_d']}")

    print("\n=== DR SPINE AUDIT (The 1/3 Rule) ===")
    print(f"  Spine ratio (3,6,9): {meta['dr_spine_ratio']:.3f}  (natural ≈ 0.333)")
    print(f"  Deviation from 1/3:  {meta['dr_spine_deviation']:.3f}")
    print(f"  Organic signal:      {'YES' if meta['is_organic_signal'] else 'NO — highly structured/anomalous'}")

    print("\n=== 5D State Coordinates (Last 5 Steps) ===")
    print("  step | x1(state) | x2(x³modN) | x3(gap) | x4(phi) | x5(DR)")
    for step in results[-5:]:
        c = step["coords_5d"]
        print(f"  {step['step']:02d}   | {c[0]:9d} | {c[1]:10d} | {c[2]:7d} | {c[3]:7d} | {c[4]}")

    print("\n=== Sample Execution Log (Last 5 States) ===")
    for step in results[-5:]:
        print(f"Step {step['step']:02d} | Gap: {step['prime_gap']:02d} | "
              f"State: {step['state_value']:05d} | Phi: {step['totient']:05d} | DR: {step['digital_root']}")
