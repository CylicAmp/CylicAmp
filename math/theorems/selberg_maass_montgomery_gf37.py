# -*- coding: utf-8 -*-
"""
================================================================================
SELBERG / MAASS / MONTGOMERY — GF(37) CONNECTIONS
================================================================================

Author: Michael Warren Song (CyclicAmp)

SETUP:
  Surface: Γ₀(4)\ℍ  (hyperbolic surface, congruence subgroup of level 4)
  Maass forms: eigenfunctions of the hyperbolic Laplacian Δ on Γ₀(4)\ℍ
               Δφ = λφ,  λ = ¼ + r²,  r ∈ ℝ
  Montgomery pair correlation:
               R₂(ξ) = 1 − (sin πξ / πξ)²  (= GUE pair correlation)
  Ramanujan tau congruence: τ(n) ≡ σ₁₁(n) (mod 691)

VERIFIED GF(37) CONNECTIONS:

1. CRITICAL LINE → GF(37) FIXED POINT [V]
   Re(s) = 1/2 on the critical strip: denominator 2 inverts mod 37 to 19.
   2⁻¹ ≡ 19 (mod 37).
   19 is the GF(37) representative of the critical line.
   Confirmed: 19 × 2 = 38 ≡ 1 (mod 37).

2. CONGRUENCE LEVEL 4 ∈ SA [V]
   Γ₀(4): the level of the congruence subgroup is 4.
   4 ∈ SA = {4, 9, 25, 30} (Sovereign Anchor, LOCKED).

3. SELBERG'S 3/16 THEOREM [V]
   The best proved general lower bound for the spectral gap of congruence subgroups:
   λ₁ ≥ 3/16.  (Selberg 1965; Ramanujan conjecture for GL(2) would give λ₁ ≥ 1/4.)
   Numerator 3 ∈ ST = {3, 12, 21, 30} (Sovereign Target).
   Denominator 16 = 2⁴: DR(16) = 7.
   DR = 7 is the prime stability check (DualityVerifier threshold in GF(37)).

4. τ(37) mod 37 = 31; DR(31) = 4 ∈ SA [V]
   τ(37) = −182213314  (Ramanujan tau function, coefficient of q³⁷ in q·∏(1−qⁿ)²⁴)
   τ(37) mod 37 = 31.
   31 ∉ any named GF(37) orbit, but DR(31) = 4 ∈ SA.
   Note: τ(37) mod 37 ≠ 0 — 37 is not a tau-zero.

5. 691 mod 37 = 25 ∈ SA [V]
   691 is the Ramanujan congruence prime: τ(n) ≡ σ₁₁(n) (mod 691) for all n.
   691 mod 37 = 25 ∈ SA = {4, 9, 25, 30}.

6. ord₃₇(2) = 36; 36 ∈ NEG_H; DR(36) = 9 ∈ SA [V]
   2 is a primitive root mod 37: ord₃₇(2) = 36 = φ(37).
   36 ∈ NEG_H = {11, 27, 36} (cube roots of −1 mod 37).
   DR(36) = 9 ∈ SA.

MONTGOMERY PAIR CORRELATION:
  R₂(ξ) = 1 − (sin πξ / πξ)²
  This is the GUE (Gaussian Unitary Ensemble) pair correlation function.
  Conjectured (Montgomery 1973) and numerically confirmed (Odlyzko) to describe
  the pair correlation of nontrivial zeros of the Riemann zeta function.
  GF(37) note: the RH critical line maps to 19 in GF(37); the pair correlation
  captures the "repulsion" between zeros, quantized here by the digital-root step Δ=9.

EPISTEMIC STATUS:
  [V] 2⁻¹ mod 37 = 19 — exact.
  [V] Level 4 ∈ SA — exact.
  [V] 3 ∈ ST — exact.
  [V] DR(16) = 7 — exact.
  [V] τ(37) mod 37 = 31; DR(31) = 4 ∈ SA — computed from power series.
  [V] 691 mod 37 = 25 ∈ SA — exact.
  [V] ord₃₇(2) = 36 ∈ NEG_H — exact.
  [P] Selberg 3/16 theorem — proved mathematics (Selberg 1965).
  [P] Ramanujan congruence mod 691 — proved mathematics.
  [C] Montgomery pair correlation = GUE — conjecture, numerically supported.
================================================================================
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
SEED  = {18, 24, 32}
SA    = {4, 9, 25, 30}
ST    = {3, 12, 21, 30}
IC    = {1, 10, 26}
NEG_H = {11, 27, 36}


def dr(n):
    n = abs(n)
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def compute_tau(N):
    coeffs = [0] * (N + 1)
    coeffs[0] = 1
    for k in range(1, N + 1):
        for _ in range(24):
            for m in range(N, k - 1, -1):
                coeffs[m] -= coeffs[m - k]
    return [coeffs[n - 1] for n in range(1, N + 1)]


def run():
    print("=" * 70)
    print("SELBERG / MAASS / MONTGOMERY — GF(37) CONNECTIONS")
    print("=" * 70)
    print("  Surface: Γ₀(4)\\ℍ,  Δφ=λφ,  λ=¼+r²")
    print("  Montgomery: R₂(ξ) = 1 − (sin πξ / πξ)²  [GUE]")

    # 1. Critical line
    inv2 = pow(2, -1, P)
    assert inv2 == 19
    assert inv2 * 2 % P == 1
    print(f"\n1. CRITICAL LINE Re(s)=1/2 → GF(37):")
    print(f"   2⁻¹ mod 37 = {inv2}  check")
    print(f"   19 × 2 mod 37 = {19*2 % P}  (confirms inverse)  check")
    print(f"   19 is the GF(37) representative of the critical line")

    # 2. Level 4
    assert 4 in SA
    print(f"\n2. CONGRUENCE LEVEL:")
    print(f"   Level 4 (Γ₀(4)) ∈ SA = {{4,9,25,30}}  check")

    # 3. Selberg 3/16
    assert 3 in ST
    assert dr(16) == 7
    print(f"\n3. SELBERG 3/16 THEOREM:")
    print(f"   Numerator 3 ∈ ST = {{3,12,21,30}}  check")
    print(f"   Denominator 16 = 2⁴: DR(16) = {dr(16)}  (prime stability DR)  check")

    # 4. tau(37) mod 37
    print(f"\n4. RAMANUJAN TAU AT p=37:")
    taus = compute_tau(37)
    t37 = taus[36]
    assert t37 == -182213314
    assert t37 % P == 31
    assert dr(31) == 4 and 4 in SA
    # verify tau(1..5)
    known = {1:1, 2:-24, 3:252, 4:-1472, 5:4830}
    for n, v in known.items():
        assert taus[n-1] == v
    print(f"   τ(37) = {t37}")
    print(f"   τ(37) mod 37 = {t37 % P}  check")
    print(f"   DR({t37 % P}) = {dr(t37 % P)} ∈ SA  check")
    print(f"   τ(1..5) verified: {[taus[i] for i in range(5)]}  check")

    # 5. 691 mod 37
    assert 691 % P == 25 and 25 in SA
    print(f"\n5. RAMANUJAN CONGRUENCE PRIME 691:")
    print(f"   τ(n) ≡ σ₁₁(n) (mod 691) for all n  [proved]")
    print(f"   691 mod 37 = {691 % P} ∈ SA = {{4,9,25,30}}  check")

    # 6. ord_37(2) = 36
    ord2 = next(k for k in range(1, P) if pow(2, k, P) == 1)
    assert ord2 == 36
    assert 36 in NEG_H
    assert dr(36) == 9 and 9 in SA
    print(f"\n6. PRIMITIVE ROOT 2 mod 37:")
    print(f"   ord₃₇(2) = {ord2} = φ(37)  (2 is primitive root)  check")
    print(f"   36 ∈ NEG_H = {{11,27,36}} (cube roots of −1 mod 37)  check")
    print(f"   DR(36) = {dr(36)} ∈ SA  check")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
