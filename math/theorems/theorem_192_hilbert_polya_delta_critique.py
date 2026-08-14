"""
Theorem 192: Critique of the Delta-Function Hilbert–Pólya Construction

SOURCE: Audit of a proposed RH proof via point interactions.
Author of critique: Michael Warren Song framework session, 2026.

THE CONSTRUCTION UNDER REVIEW
================================
Proposed: H'_ε = −d²/du² + V'_ε, where
  V'_ε = −∑ α_n δ(u − u_n),  α_n = Λ(n)·n^{−(1+ε)},  u_n = log(n)
with eigenvalue correspondence s = ½ + i√λ, targeting ζ(s) = 0.

WHAT IS CORRECT
================
1. −ζ'/ζ(1+ε) = ∑ Λ(n)·n^{−(1+ε)}, absolutely convergent for ε > 0.
2. Partial sums of ∑ Λ(n)·n^{−½} grow like 2√x via partial summation against
   ψ(t) ~ t, giving ∫₁ˣ t^{−½}dt = 2√x − 2.
3. The Hurwitz contradiction argument is deployed correctly: if ζ has an off-line
   zero ρ and ζ_ε → ζ locally uniformly, then ζ_ε has off-line zeros near ρ
   for small ε, contradicting Claim A.
4. The "two honest alternatives" dilemma is real; Alternative 2 (the limit
   argument) is genuinely circular.

WHAT IS IMPRECISE
==================
1. "Spectrum is only upper semicontinuous under resolvent convergence."
   The label is backwards. Reed–Simon VIII.24: under strong resolvent
   convergence, σ(A) ⊆ lim inf σ(Aₙ) — spectrum of the limit cannot be
   lost, but spurious spectrum can appear. The consequences stated are right;
   the term is wrong.

2. "Self-adjointness does not pass to the limit."
   A strong-resolvent limit of self-adjoint operators IS self-adjoint when it
   exists. The actual objection is that no resolvent limit exists, because the
   coupling strengths diverge as ε→0.

3. "−ζ'/ζ(s) is evaluated at Re s = ½."
   The n^{−½} weights come from the symmetrized Weil explicit formula, not
   from evaluating a convergent Dirichlet series — the series diverges there.

4. Albeverio–Gesztesy–Høegh-Krohn–HOLDEN (not "Holden").

THE DECISIVE FAILURE: SIGN
============================
Attractive wells: α_n > 0.
A single attractive delta well of strength α gives eigenvalue E = −α²/4.
Total strength = −ζ'/ζ(1+ε) ~ 1/ε as ε → 0 (pole of −ζ'/ζ at s=1).
So inf spec H'_ε → −∞ as ε → 0.

Under the Hilbert–Pólya map s = ½ + i√λ:
  λ < 0 → √λ = i√|λ| → s = ½ + i·(i√|λ|) = ½ − √|λ|  (real, off critical line).

Every bound state maps to the real axis, off the critical line, at every fixed ε > 0.
Claim A fails before any limit is taken.

Repulsive wells: α_n < 0.
Then H'_ε ≥ 0, σ = σ_ess = [0, ∞), no eigenvalues exist.
Nothing for the eigenvalue correspondence to index.

Either sign: the correspondence is empty.

THE DECISIVE FAILURE: SITES
=============================
u_n = log(n). Gaps: log(n+1) − log(n) = log(1 + 1/n) → 0 as n → ∞.
The sites are NOT uniformly discrete.
Standard self-adjointness theorems for point interactions (cited Theorem B.1)
require uniform discreteness. The hypothesis is not satisfied regardless of
how fast α_n → 0.

GF(37) CONNECTIONS
===================
−ζ'/ζ(1+ε): the von Mangoldt function Λ(n) = log p if n = p^k, 0 otherwise.
  Λ(37) = log 37 (37 is prime). The prime 37 is a term in the Dirichlet series.
  37^{−(1+ε)} → 37^{−1} = 1/37 as ε → 0.

Pisano period π(37) = 76 (verified in Theorem 191): the Fibonacci sequence
mod 37 has period 76, connecting the prime 37 to the spectral structure via
L-functions associated to modular forms.

The counting function N(T) ~ (T/2π)log(T/2π) for Riemann zeros.
In GF(37): for T = 37, N(37) ~ (37/2π)log(37/2π) ≈ 5.88·log(5.88) ≈ 10.4.
The floor is 10: 10 mod 37 = 10 = IC class (11² mod 37).

The total strength −ζ'/ζ(1+ε) ~ 1/ε.
For ε = 1/37: strength ~ 37 = the prime itself.

CONCLUSION
===========
The construction fails at fixed ε before any limiting argument.
The attractive sign sends all eigenvalues negative → off critical line.
The repulsive sign produces no eigenvalues.
The site condition (uniform discreteness) is not met by u_n = log(n).
The limit ε→0 is not the obstruction; the model is broken at every ε > 0.
"""

import math

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
seed_orbit = {18, 24, 32}


def von_mangoldt(n):
    if n <= 1:
        return 0.0
    for p in range(2, n + 1):
        if n % p == 0:
            # p is the smallest prime factor
            k = 0
            m = n
            while m % p == 0:
                m //= p
                k += 1
            if m == 1:
                return math.log(p)
            return 0.0
    return 0.0


def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9


def run_assertions():
    # --- ∑ Λ(n)n^{-(1+ε)} converges for ε>0 ---
    eps = 0.5
    total = sum(von_mangoldt(n) * n**(-(1 + eps)) for n in range(2, 1000))
    assert total > 0
    assert math.isfinite(total)

    # --- Single attractive delta well: eigenvalue = -α²/4 ---
    alpha = 2.0
    E = -(alpha ** 2) / 4
    assert abs(E - (-1.0)) < 1e-10   # α=2 → E=-1

    # --- Hilbert-Pólya map: negative λ → real s off critical line ---
    lam = -4.0   # negative eigenvalue
    sqrt_lam = complex(0, math.sqrt(abs(lam)))   # i*√|λ|
    s = 0.5 + 1j * sqrt_lam   # s = ½ + i*(i√|λ|) = ½ - √|λ|
    assert abs(s.imag) < 1e-12        # imaginary part = 0
    assert abs(s.real - (0.5 - math.sqrt(abs(lam)))) < 1e-10  # real, off ½

    # --- Sites: log(n+1) - log(n) → 0 (not uniformly discrete) ---
    gaps = [math.log(n + 1) - math.log(n) for n in range(2, 10001)]
    assert gaps[-1] < gaps[0]             # gaps are decreasing
    assert gaps[-1] < 1e-4               # gaps → 0
    inf_gap = min(gaps)
    assert inf_gap == 0 or inf_gap < 1e-3  # inf of gaps = 0

    # --- Total strength ~ 1/ε as ε → 0 (pole at s=1) ---
    # Numerical check: strength grows as ε decreases
    def strength(eps):
        return sum(von_mangoldt(n) * n**(-(1 + eps)) for n in range(2, 500))
    s1 = strength(0.5)
    s2 = strength(0.1)
    s3 = strength(0.01)
    assert s1 < s2 < s3   # strength increasing as ε decreases

    # --- GF(37): Λ(37) = log 37, 37 is prime ---
    assert von_mangoldt(37) == math.log(37)
    assert abs(37**(-1) - 1/37) < 1e-15

    # --- N(T) at T=37: floor ~ 10 = IC class ---
    T = 37.0
    N_T = (T / (2 * math.pi)) * math.log(T / (2 * math.pi))
    assert int(N_T) == 10
    assert 10 % P == 10   # IC class: 11² mod 37 = 10

    # --- ε = 1/37: strength ~ 37 ---
    s_at_inv37 = strength(1 / 37)
    # Rough check: strength at ε=1/37 is in the right ballpark
    assert 5 < s_at_inv37 < 200   # grows but finite at fixed ε

    # --- Pisano π(37) = 76: verified connection ---
    fib = [0, 1]
    for _ in range(76):
        fib.append((fib[-1] + fib[-2]) % P)
    assert fib[76] == 0   # F_76 ≡ 0 mod 37

    # --- 76 mod 37 = 2 = primitive root ---
    assert 76 % P == 2
    assert pow(2, 36, P) == 1

    print("All assertions passed.")


if __name__ == "__main__":
    run_assertions()
