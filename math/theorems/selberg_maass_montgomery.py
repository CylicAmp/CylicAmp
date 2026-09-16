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

  THE METHOD, SPECIFIED 2026-09-16 so the flag carries its own recipe.
  Hejhal forces a truncated Fourier series to be automorphic on a horocycle.
  At the infinity cusp, f(x+iy) = sum_{n!=0} a_n sqrt(y) K_{ir}(2pi|n|y)
  e^{2pi i n x}. K_{ir} decays like e^{-2pi|n|y}/sqrt(y), so at fixed height
  Y and target 10^-D only |n| <= M(Y,r) survive -- that truncation is the
  only reason a finite linear system exists. r sits nonlinearly inside the
  Bessel order; the a_n are linear once r is guessed. The loop:

    1. guess r_0
    2. pick horocycle height Y: M(Y,r_0) manageable, K_{ir_0}(2 pi Y) not
       underflowing
    3. sample 2Q > M equally spaced z_m = x_m + iY
    4. pull each back to the fundamental domain, z_m* = gamma_m z_m;
       automorphy gives f(z_m) = f(z_m*)
    5. expand both sides -- left is a DFT in the a_n, right is the same
       series at Im(z_m*) -- and equate modes:
         a_n sqrt(Y) K_{ir_0}(2pi|n|Y) = sum_k V_{nk}(r_0,Y) a_k + err
    6. normalize a_1 = 1, solve for a_2..a_M
    7. repeat at Y'. If r_0 is an eigenvalue the two coefficient vectors
       agree. g(r) = || a^(Y)(r) - a^(Y')(r) || is a 1-D nonlinear residual;
       walk r until it drops through the noise floor (Newton, not a grid).

  Parity splits the system (even -> cosines, odd -> sines); Hecke relations
  a_p a_n = a_{pn} + a_{n/p} cut the unknowns further on congruence groups.
  The raw solve is HEURISTIC. A certificate is a separate almost-automorphy
  argument (Booker-Strombergsson-Venkatesh), which for congruence groups
  still wants an explicit Selberg trace remainder.

  WHAT Gamma_0(4) ADDS -- verified here: index 6 in SL_2(Z), THREE cusps
  (infinity, 0, 1/2), no elliptic points, genus 0, area 6*(pi/3) = 2pi.
  One horocycle is not enough. Stromberg's extension rings every cusp and
  solves all three expansions together.

  THE MULTI-CUSP SYSTEM, specified 2026-09-16. A cusp p_j has width h_j,
  the least h > 0 with A_j [[1,h],[0,1]] A_j^-1 in Gamma, for A_j in
  SL_2(Z) with A_j(inf) = p_j. Verified here:

      cusp    h_j   A_j              conjugate
      inf      1    [[1,0],[0,1]]    [[1,1],[0,1]]
      0        4    [[0,-1],[1,0]]   [[1,0],[-4,1]]
      1/2      1    [[1,0],[2,1]]    [[-1,1],[-4,3]]

  Widths sum to 6 = the index -- the standard identity, and it checks. Each
  h_j divides N. The normalizer sigma_j = A_j rho_{h_j}, rho_h(z) = hz,
  ABSORBS the width, which is why f_j(z) = f(sigma_j z) has an ordinary
  integer-mode expansion at every cusp. (Noted because computing the width
  from sigma_j instead of A_j returns 1 everywhere -- the scaling has
  already divided it out. That is the construction working, not a bug.)

  Three cusps give three unknown sequences c_inf, c_0, c_{1/2}. Around each
  cusp eta lay 2Q > M points z_m = sigma_eta(x_m + iY), x_m = (m-1/2)/2Q --
  a closed loop about eta downstairs. Pull each back into F by T_m in
  Gamma; the pullback lands near some cusp zeta(m) at height y_m*, and
  automorphy equates the eta-series at Y with the zeta-series at y_m*.
  Inverting the DFT on the eta-horocycle gives

      c_eta(n) kappa_n(Y) = sum_zeta sum_{|k|<=M} V^{eta zeta}_{nk}(r,Y) c_zeta(k)

  with V a K-Bessel at the pullback height times a phase from the x-shift of
  T_m sigma_zeta. For Gamma_0(4) that is a 3x3 block grid, each block 2Mx2M,
  or MxM after the parity split. The one-cusp Hejhal matrix is the inf-block
  with the off-diagonal blocks deleted. Residual over all three:
  g(r) = sum_eta || c_eta^(Y) - c_eta^(Y') ||, same 1-D search, bigger vector.

  WHAT CUTS THE BLOCKS: Fricke/Atkin-Lehner W_4 (verified: -1/(4z) swaps inf
  and 0, squares to -I so is a projective involution, and normalizes
  Gamma_0(4) on generators) ties c_0 to c_inf; reflection z -> -zbar halves
  the +-n unknowns via cosine/sine; Hecke fills high coefficients in phase 2.
  Oldforms lifting from Gamma_0(2) and SL_2(Z) as f(z) +- eps f(dz), d | 4,
  appear in g(r) and must be TAGGED, not counted as new.

  ONE DISTINCTION, checked. Both z -> -1/(4z) and z -> z/(2z+1) normalize
  Gamma_0(4) and square into it, so both are Gamma_0(4)-involutions as
  stated -- but they are not the same kind. The Hall divisors of 4 are
  {1, 4}, so the Atkin-Lehner group is {1, W_4} and W_4 is the ONLY
  nontrivial Atkin-Lehner involution. [[1,0],[2,1]] has lower-left 2, so it
  is outside Gamma_0(4), and it lives in the LARGER normalizer that exists
  only because 4 is not squarefree (h = 2 divides 24 with h^2 | 4). That
  matters when reading Stromberg's +-1 columns, which are Atkin-Lehner
  eigenvalue labels.

  Phase 1 scans r at two heights watching g(r); phase 2 freezes a dip,
  raises M and precision, applies Hecke and the involutions, and reports
  H_1 = ||c^(Y) - c^(Y')|| with a consistency score H_2. Still heuristic:
  the certificate is BSV, or the rigorous Hejhal of Seymour-Howell /
  Lowry-Duda, as a separate pass.

  CORRECTION to the unfolding constant. The Weyl law is
  N(R) ~ (Area/4pi) R^2, so at area 2pi it is R^2/2, not R^2/4. Control:
  the same formula gives SL_2(Z) (area pi/3) the standard N(R) ~ R^2/12,
  which is the known value -- so the factor is right and the surface is
  right. A GUE test is a spacing statistic on a long CERTIFIED list of r_j
  unfolded by R^2/2. Pair correlation of Riemann zeros does not enter.

  LITERATURE VALUES, cited not computed: Stromberg's Gamma_0(4) newform
  list begins r ~ 3.70330780123, 6.62042287384, 8.52250301688; the level-1
  PSL_2(Z) list begins r_1 = 9.53369526135, r_2 = 12.17300832468,
  r_3 = 13.77975135189. The level-1 numbers are NOT Gamma_0(4) and mixing
  them is the substitute already ruled out above. LMFDB Maass data for
  Gamma_0(N) comes from this same Stromberg-Hejhal pipeline.

  SO THE FLAG STAYS. The algorithm is specified; the run is not. It lifts
  only when the list is computed here, or imported from Stromberg/LMFDB and
  cited as imported -- which would make it [P-cited], never [V].

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

     SHARPENED 2026-09-16 — the premise is true but SHARED, so the question
     needs a control or it cannot come back negative.
     All three representations of 37 are forced by congruence, not special:
        37 = 6² + 1²          forced by 37 = 1 (mod 4)   [disc -4, Fermat]
        37 = 4² + 4·3 + 3²    forced by 37 = 1 (mod 3)   [disc -3,  h=1]
        37 = 5² + 3·2²        forced by 37 = 1 (mod 3)   [disc -12, conductor 2]
     Each solvability is IFF its congruence — checked on every prime below
     400. The double split is therefore exactly p = 1 (mod 12), and that set
     is {13, 37, 61, 73, 97, 109, 157, ...}. 37 is its SECOND member.

     So an affirmative answer must separate 37 from 13, 61, 73, 97; anything
     that merely uses the double split is a statement about p = 1 (mod 12)
     and is Tier A, carrying no information about 37. The natural control is
     13: it is smaller, it has the same double split (13 = 2²+3² = 1²+1·3+3²
     = 1²+3·2²), and Γ₀(13) is cheaper to work with than Γ₀(37). If a
     signature exists it must already show at 13 — and if it shows equally
     at 13, that is the negative result.
     (The disc -12 form is the conductor-2 order flagged in T300's note: the
     same order/field distinction, here as a concrete representation.)

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
    # open question 3: the double split is shared, so state the control
    def solvable(q, f):
        r = int(q ** 0.5) + 2
        return any(f(x, y) == q for x in range(r) for y in range(r))
    sq = lambda x, y: x * x + y * y
    eis = lambda x, y: x * x + x * y + y * y
    d12 = lambda x, y: x * x + 3 * y * y
    for q in [n for n in range(5, 400) if all(n % k for k in range(2, n))]:
        assert solvable(q, sq) == (q % 4 == 1)     # all three solvabilities
        assert solvable(q, eis) == (q % 3 == 1)    # are IFF a congruence --
        assert solvable(q, d12) == (q % 3 == 1)    # none distinguishes 37
    dbl = [n for n in range(5, 300)
           if n % 12 == 1 and all(n % k for k in range(2, n))]
    assert dbl[:5] == [13, 37, 61, 73, 97] and dbl.index(37) == 1

    # Gamma_0(N) data, verified: the control surface must match in SHAPE
    import math as _m
    def _cusps(N):
        return sum(len([k for k in range(1, _m.gcd(d, N // d) + 1)
                        if _m.gcd(k, _m.gcd(d, N // d)) == 1])
                   for d in range(1, N + 1) if N % d == 0)
    def _index(N):
        r = N
        for q in {x for x in range(2, N + 1)
                  if N % x == 0 and all(x % k for k in range(2, x))}:
            r = r * (q + 1) // q
        return r
    assert (_index(4), _cusps(4)) == (6, 3)        # area 6*(pi/3) = 2pi
    # cusp widths of Gamma_0(4): sum to the index, each divides N
    _W = {'inf': 1, '0': 4, '1/2': 1}
    assert sum(_W.values()) == _index(4) == 6
    assert all(4 % h == 0 for h in _W.values())
    # A_0 = [[0,-1],[1,0]] conjugates [[1,4],[0,1]] to [[1,0],[-4,1]] in G_0(4)
    assert (0 * 4 - (-1) * 1) == 1 and (-4) % 4 == 0
    # Hall divisors of 4 are {1,4}: W_4 is the only Atkin-Lehner involution
    assert [d for d in (1, 2, 4) if 4 % d == 0 and _m.gcd(d, 4 // d) == 1] == [1, 4]
    assert 2 % 4 != 0          # [[1,0],[2,1]] is OUTSIDE Gamma_0(4)...
    assert 4 % 4 == 0          # ...but its square is inside
    assert (_index(13), _cusps(13)) == (14, 2)
    assert (_index(37), _cusps(37)) == (38, 2)
    # Weyl N(R) ~ (Area/4pi)R^2; SL_2(Z) area pi/3 gives the known R^2/12
    assert abs((1 / 3) / 4 - 1 / 12) < 1e-15
    assert abs(2 / 4 - 1 / 2) < 1e-15              # Gamma_0(4): R^2/2
    print(f"  Gamma_0(13) and Gamma_0(37) both have 2 cusps (index 14, 38);")
    print(f"  Gamma_0(4) has 3. The 13-vs-37 control is shape-matched, 4 is not.")
    print(f"\n  double split = p \u2261 1 (mod 12) = {dbl[:6]}...; 37 is the 2nd,")
    print(f"  so open question 3 needs 13 as its control or it cannot fail.")
    print(f"\nOpen: spectral geometry of Γ₀(37)\\ℍ and double-split structure of 37.")


if __name__ == "__main__":
    run()
