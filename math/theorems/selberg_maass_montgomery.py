# -*- coding: utf-8 -*-
# CLASS: THEOREM
"""
================================================================================
SELBERG / MAASS / MONTGOMERY — Spectral Geometry Research Record
================================================================================

Session origin: "Riemann Zeta Zeros" (June 2025 onward)
Author: Michael Warren Song (CyclicAmp)

EPISTEMIC STATUS:
  [P] = proven / standard mathematics
  [V] = verified by computation in this repo
  [U] = unverified — flagged; early numerical claims were generated text,
        not executed computation. Research question survives; numbers do not.

SETUP [P]:
  Γ₀(4) = congruence subgroup of SL₂(ℤ), conductor 4.
  Quotient surface: Y₀(4) = Γ₀(4)\ℍ (hyperbolic surface, finite area).
  Laplace-Beltrami operator: Δ = -y²(∂²/∂x² + ∂²/∂y²).
  Maass forms: smooth eigenfunctions φ_j of Δ on Y₀(4),
    Δ φ_j = λ_j φ_j,  λ_j = ¼ + r_j²,  r_j ∈ ℝ.

SELBERG TRACE FORMULA [P]:
  Σ_j h(r_j) = (area/4π) ∫ h(r) r tanh(πr) dr
              + Σ_{[γ] primitive} Σ_{k≥1} (log N(γ)) h̃(k log N(γ)) / (N(γ)^{k/2} - N(γ)^{-k/2})
  Spectral side: sum over eigenvalues λ_j.
  Geometric side: sum over lengths of closed geodesics.

MONTGOMERY'S PAIR CORRELATION CONJECTURE [P — conjecture]:
  For the Riemann zeta zeros ½ + iγ_n, the pair correlation is:
    R₂(ξ) = 1 − (sin πξ / πξ)²  (GUE kernel)
  Montgomery (1973): proved this for test functions whose Fourier transform
  has support in (-1,1).

GUE CONNECTION [P — physics/conjecture]:
  The nearest-neighbor spacing distribution of Maass form eigenvalues r_j
  on Γ₀(4)\ℍ is conjectured to follow GUE statistics (Bohigas-Giannoni-Schmit,
  Rudnick-Sarnak). This is the arithmetic quantum chaos hypothesis.
  Not proved; supported by numerical evidence.

DIRICHLET L-FUNCTION [P]:
  χ mod 4: the non-principal character χ(n) = (-1)^{(n-1)/2} for odd n.
  L(s, χ) = 1 - 1/3^s + 1/5^s - 1/7^s + ...
  Zeros of L(s,χ) are conjectured (GRH) to lie on Re(s) = ½.
  The pair correlation of these zeros is also expected to follow GUE.

GF(37) CONNECTIONS:
  37 ≡ 1 (mod 4) → χ mod 4 gives χ(37) = +1 (37 splits in Q(i))
  37 ≡ 1 (mod 3) → 37 splits in Q(√-3) (Eisenstein splitting, T257)
  Hecke operator T_37 acts on S_12(Γ₀(1)) (space containing Δ):
    T_37(Δ) = τ(37) · Δ  (since Δ is a Hecke eigenform)
    τ(37) mod 37 = 31  (computed in T260)
  τ(37) ≢ 0 mod 37: 37 is not a zero of tau — consistent with 37
  being an ordinary prime for the Galois representation ρ_Δ mod 37.

VERIFIED 2026-09-16 [V] — the arithmetic in this file now runs:
  tau(37) = -182213314, from the q-expansion of Delta = q prod (1-q^n)^24
  computed here; tau(1..12) reproduces the standard values as a control.
  tau(37) mod 37 = 31, confirming the figure T260 supplied, and 31 != 0, so
  37 is ordinary for rho_Delta as stated. 31 lies in C9 = {14,29,31}.
  37 mod 4 = 1 and 37 mod 3 = 1, so 37 splits in BOTH Q(i) and Q(sqrt-3);
  explicitly 37 = 6^2 + 1^2 and 37 = 4^2 + 4*3 + 3^2.
  Open question 3 below therefore rests on a verified premise.

UNVERIFIED CLAIMS [U] — scope narrowed 2026-09-16:
  Specific numerical pair-correlation results from the original session
  were flagged as generated text, not executed computation. Exactly two
  items remain unverified, and they are the only two:
  - any specific eigenvalue r_j for Γ₀(4)\ℍ cited in that session
  - any specific GUE fit statistics cited for those eigenvalues

  ASSESSED, not merely flagged. These are not a to-do item. Maass CUSP
  forms have no closed form and no series to sum; producing r_j requires
  Hejhal's algorithm (or a Selberg-trace/Steil variant), which is a
  substantial numerical program not present in this repo and not written
  here. So the status is "cannot be verified in this repo", with the reason
  named -- not "nobody has got round to it".

  AND THE SUBSTITUTE THAT WOULD NOT COUNT: Montgomery pair correlation for
  RIEMANN zeros is easy here (mpmath gives gamma_n directly) and says
  nothing about Γ₀(4). Zeta zeros and Maass eigenvalues are different
  spectra; a GUE fit on the first would not license any claim about the
  second. Recorded so the easy computation is not mistaken for the hard one.

PRIOR COPY: T193 (2026-08-14) carries the same spectral-geometry note,
  appended to a file about process functions on Z_p, flagged from the same
  2026-08-05 L-function audit. This file (2026-08-23) is the fuller record;
  the two never cross-referenced until now.

OPEN QUESTIONS (legitimate, per audit 2026-08-05):
  1. Does the GUE pair-correlation hold for Γ₀(4)\ℍ eigenvalues at
     precision checkable in GF(37)?
  2. What is the connection between the DR=7 stability (DualityVerifier)
     and spectral gaps in the arithmetic surface?
  3. The prime 37 splits in both Q(i) and Q(√-3). Does this double-split
     structure leave a signature in the spectral geometry of Γ₀(4)\ℍ
     or Γ₀(37)\ℍ?

COMPUTATIONAL STATUS:
  No numerical eigenvalue computation in this repo.
  Standard tools: LMFDB, Sage maass_forms module, Stefan Lemurell's data.
================================================================================
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
H = {1, 10, 26}
NEG_H = {11, 27, 36}


def run():
    print("=" * 70)
    print("SELBERG / MAASS / MONTGOMERY — SPECTRAL GEOMETRY RECORD")
    print("=" * 70)

    # Verify GF(37) connections that can be checked here
    print("\nGF(37) CONNECTIONS (verified):")

    # 37 mod 4
    assert P % 4 == 1
    print(f"  37 ≡ {P%4} (mod 4) → χ mod 4: χ(37) = +1 → 37 splits in Q(i)  check")

    # 37 mod 3 (already in T257)
    assert P % 3 == 1
    print(f"  37 ≡ {P%3} (mod 3) → 37 splits in Q(√-3) (Eisenstein, T257)  check")

    # tau(37) mod 37 — computed in T260
    def compute_tau_mod(N, m):
        coeffs = [0]*(N+1); coeffs[0] = 1
        for k in range(1, N+1):
            for _ in range(24):
                for i in range(N, k-1, -1):
                    coeffs[i] = (coeffs[i] - coeffs[i-k]) % m
        return coeffs[N-1]  # tau(N)

    tau37 = compute_tau_mod(37, P)
    print(f"  τ(37) mod 37 = {tau37}  (37 is ordinary for ρ_Δ mod 37)  check")
    assert tau37 != 0
    print(f"  τ(37) ≢ 0 (mod 37): 37 is not a tau-zero  check")

    # Montgomery pair correlation kernel at key points
    import math
    def R2(xi):
        if abs(xi) < 1e-10: return 0.0
        return 1 - (math.sin(math.pi * xi) / (math.pi * xi))**2

    print(f"\nMONTGOMERY PAIR CORRELATION R₂(ξ) = 1 - (sin πξ / πξ)²:")
    for xi in [0.0, 0.5, 1.0, 1.5, 2.0]:
        print(f"  R₂({xi}) = {R2(xi):.6f}")
    print(f"  R₂(1) = {R2(1):.6f}  (complete correlation hole at ξ=1)  check")
    assert abs(R2(1.0) - 1.0) < 1e-10

    # 37 splits in Q(i): verify 37 = a² + b² for some a,b
    splits_qi = [(a,b) for a in range(1,7) for b in range(a,7) if a*a+b*b==37]
    print(f"\n  37 = {splits_qi[0][0]}² + {splits_qi[0][1]}²  (splits in Z[i])  check")
    assert splits_qi

    # ── tau(37), computed here rather than cited (added 2026-09-16) ──────
    # Delta = q * prod_{n>=1} (1 - q^n)^24 ; tau(n) is the coefficient of q^n.
    N = 40
    coef = [0] * (N + 1)
    coef[0] = 1
    for n in range(1, N + 1):
        for _ in range(24):                       # multiply by (1 - q^n)
            nxt = [0] * (N + 1)
            for i, a in enumerate(coef):
                if a:
                    nxt[i] += a
                    if i + n <= N:
                        nxt[i + n] -= a
            coef = nxt
    tau = lambda n: coef[n - 1]                   # shift for the leading q

    # control: the standard values, so a wrong expansion fails loudly here
    assert [tau(n) for n in range(1, 13)] == [
        1, -24, 252, -1472, 4830, -6048, -16744, 84480,
        -113643, -115920, 534612, -370944]
    t37 = tau(37)
    assert t37 == -182213314
    assert t37 % 37 == 31                  # the figure T260 supplied
    assert t37 % 37 != 0                   # 37 ordinary for rho_Delta
    assert 31 in {14, 29, 31}              # C9
    assert 37 % 4 == 1 and 37 % 3 == 1     # splits in BOTH Q(i) and Q(sqrt-3)
    assert 4 * 4 + 4 * 3 + 3 * 3 == 37     # Eisenstein norm form
    print(f"\n  tau(37) = {t37}  (computed here; tau(1..12) matches as control)")
    print(f"  tau(37) mod 37 = {t37 % 37} \u2208 C9, nonzero \u2192 37 ordinary  check")

    print(f"\nEPISTEMIC STATUS SUMMARY:")
    print(f"  [P] Selberg trace formula setup, Montgomery conjecture statement")
    print(f"  [P] GUE pair correlation kernel R₂(ξ) — standard mathematics")
    print(f"  [V] GF(37) connections: splits in Q(i) and Q(√-3), τ(37)≢0")
    print(f"  [V] tau(37) = -182213314 \u2261 31 (mod 37), computed above not cited")
    print(f"  [U] Specific eigenvalue r_j values from original session")
    print(f"  [U] Numerical GUE fit statistics from original session")
    print(f"      \u2514\u2500 ASSESSED: unverifiable in this repo. Maass cusp forms need")
    print(f"         Hejhal's algorithm, which is not here. Not a to-do item.")
    print(f"         A GUE fit on RIEMANN zeros is easy and would not count:")
    print(f"         different spectrum, no licence to transfer the result.")
    print(f"\nOpen: spectral geometry of Γ₀(37)\\ℍ and double-split structure of 37.")


if __name__ == "__main__":
    run()
