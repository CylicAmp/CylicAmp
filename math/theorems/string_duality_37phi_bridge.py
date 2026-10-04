"""
String Duality Audit — 37φ Bridge under T-Duality

Classification: Theorem

Defines the T-duality operator D(x) = 37²/x on the 37φ coherence bridge.
The self-dual scale is 37 (the prime modulus); D has fixed points ±37.

Verified claims:
  Duality invariance (tau=1e-12)   D(D(x)) = x                        ✓
  37φ bridge preserved under D     (B/Λ) × (D(B)/D(Λ)) = 1           ✓

Product invariant:
  Λ × D(Λ) = 37φ × 37/φ = 37² = 1369       (exact, no floating error)
  φ + 1/φ = √5                               (golden ratio identity)
  D(Λ) = 37/φ = 37(φ−1) = 37φ − 37 ≈ 22.87 (dual coherence threshold)

Bridge pairing:
  Primal: B  = 77  = 7×11  (Σ first 8 primes, smallest > 37φ, 7|B)
  Dual:   B̃  = 28  = 4×7   (Σ first 5 primes, smallest > 37/φ, 7|B̃)
  DR(B)  = 5  — the absent class from QR₃₇ (bridge sits on the gap)
  DR(B̃) = 1  — identity class
  DR(37²) = DR(1369) = 1

Connection to LoB 88 / G_Ord18_Cycle:
  DR=5 is absent from ⟨3⟩ = QR₃₇.
  The prime bridge sum B=77 has DR=5, placing it outside the QR orbit.
  The dual sum B̃=28 has DR=1 (identity), inside ⟨3⟩ at 28=3^{11} mod 37.
"""

import math


PHI = (1 + math.sqrt(5)) / 2


def dr(n):
    n = int(round(abs(n)))
    return (n - 1) % 9 + 1 if n > 0 else 0


def prime_sieve(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit+1, i):
                sieve[j] = False
    return [i for i in range(2, limit+1) if sieve[i]]


PRIMES = prime_sieve(500)


def prime_bridge(threshold):
    """Smallest N with Σ(first N primes) > threshold and 7 | sum."""
    for n in range(1, len(PRIMES)+1):
        s = sum(PRIMES[:n])
        if s > threshold and s % 7 == 0:
            return n, s
    raise ValueError(f"No prime bridge found for threshold={threshold}")


# ── Core quantities ────────────────────────────────────────────────────────

LAMBDA     = 37 * PHI           # 37φ ≈ 59.867   — primal coherence threshold
LAMBDA_DUAL = 37 / PHI          # 37/φ ≈ 22.867  — dual coherence threshold
TAU        = 1e-12              # numerical tolerance


def D(x):
    """T-duality involution: D(x) = 37²/x  (self-dual at x=±37)."""
    return 37 * 37 / x


# ── Assertions ─────────────────────────────────────────────────────────────

# 1. D is an involution: D(D(x)) = x
assert abs(D(D(LAMBDA)) - LAMBDA) < TAU, "D is not an involution"
assert abs(D(D(1.0))    - 1.0)    < TAU
assert abs(D(D(137.0))  - 137.0)  < TAU

# 2. Duality invariance at the bridge
assert abs(D(D(LAMBDA)) - LAMBDA) < TAU   # matches: "Duality invariance (tau=1e-12): True"

# 3. D maps primal bridge to dual bridge
assert abs(D(LAMBDA) - LAMBDA_DUAL) < TAU, \
    f"D(37φ) ≠ 37/φ: got {D(LAMBDA)}, expected {LAMBDA_DUAL}"

# 4. Product invariant: Λ × D(Λ) = 37²  (exact)
product = LAMBDA * D(LAMBDA)
assert abs(product - 37**2) < TAU, f"Product invariant failed: {product}"

# 5. Golden ratio identities
assert abs(PHI * (1/PHI) - 1.0) < TAU      # φ × (1/φ) = 1
assert abs(PHI + 1/PHI - math.sqrt(5)) < TAU  # φ + 1/φ = √5

# 6. Primal prime bridge: smallest N with Σprimes > 37φ, 7|sum → N=8, B=77
N_primal, B_primal = prime_bridge(LAMBDA)
assert N_primal == 8
assert B_primal == 77
assert B_primal == 7 * 11
assert dr(B_primal) == 5         # DR=5: the absent class from QR₃₇

# 7. Dual prime bridge: smallest N with Σprimes > 37/φ, 7|sum → N=5, B̃=28
N_dual, B_dual = prime_bridge(LAMBDA_DUAL)
assert N_dual == 5
assert B_dual == 28
assert B_dual == 4 * 7
assert dr(B_dual) == 1           # DR=1: identity class

# 8. Bridge preserved under D:
#    (B/Λ) × (D(B)/D(Λ)) = 1   — the ratios are reciprocal
bridge_ratio_product = (B_primal / LAMBDA) * (D(B_primal) / D(LAMBDA))
assert abs(bridge_ratio_product - 1.0) < TAU, \
    f"Bridge ratio product = {bridge_ratio_product}"   # "37φ bridge preserved under D: True"

# 9. DR(37²) = 1
assert dr(37 * 37) == 1

# 10. Dual bridge 28 = 3^11 mod 37 → in ⟨3⟩ = QR₃₇
CYCLE18 = [pow(3, k, 37) for k in range(1, 19)]
assert 28 in CYCLE18, "28 not in ⟨3⟩"
assert CYCLE18.index(28) + 1 == 11   # 3^11 = 28

# Primal bridge 77 mod 37 = 3 = 3^1 (in QR₃₇)
# but DR(77)=5 which is absent from QR₃₇ — the DR signature is the gap
assert 77 % 37 == 3
assert 3 in CYCLE18    # residue IS in QR₃₇
QR37 = frozenset((x*x) % 37 for x in range(1, 37))
DR5_VALUES = [n for n in range(1, 37) if dr(n) == 5]
assert not any(v in QR37 for v in DR5_VALUES), "DR=5 value in QR₃₇"


if __name__ == "__main__":
    print("String Duality Audit — 37φ Bridge under T-Duality")
    print()
    print(f"  D(x) = 37²/x        (self-dual at x=±37)")
    print(f"  Λ  = 37φ = {LAMBDA:.12f}")
    print(f"  D(Λ) = 37/φ = {D(LAMBDA):.12f}")
    print(f"  Λ × D(Λ) = 37² = {int(LAMBDA * D(LAMBDA))}")
    print(f"  φ + 1/φ  = √5 = {PHI + 1/PHI:.12f}")
    print()
    print(f"  Duality invariance |D(D(Λ))-Λ| < tau: {abs(D(D(LAMBDA))-LAMBDA) < TAU}")
    print(f"  37φ bridge preserved under D: {abs(bridge_ratio_product - 1.0) < TAU}")
    print()
    print(f"  Bridge pairing:")
    print(f"    Primal: N={N_primal}, B={B_primal}={B_primal//7}×7,"
          f"  B>Λ={B_primal>LAMBDA},  DR(B)={dr(B_primal)}")
    print(f"    Dual:   N={N_dual},  B̃={B_dual}={B_dual//7}×7,"
          f"  B̃>D(Λ)={B_dual>LAMBDA_DUAL}, DR(B̃)={dr(B_dual)}")
    print()
    print(f"  DR=5 ({DR5_VALUES}): absent from QR₃₇  →  bridge DR=5 sits on the gap")
    print(f"  B mod 37 = {77%37} = 3^1 ∈ QR₃₇  (residue is in cycle, DR is not)")
    print(f"  28 = 3^11 mod 37 ∈ QR₃₇  (dual bridge is inside the cycle)")
    print(f"  DR(37²) = {dr(37*37)}  (product invariant has identity DR)")
    print()
    print("All assertions passed.")
