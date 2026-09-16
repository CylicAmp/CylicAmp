"""
odlyzko_schonhage_audit.py

Audits Layer 2 integration document. Three verifiable claims:
  1. Logarithmic substitution u=log x, v=log p and Jacobian collapse
  2. "Riemann-Siegel theta cutoff = exact equivalent of x_min·p_min = 2π"
  3. Odlyzko-Schönhage algorithm: O(N^{1+ε}) for N simultaneous evaluations
"""

import math

# ---------------------------------------------------------------------------
# 1.  Logarithmic substitution: algebra and Jacobian
# ---------------------------------------------------------------------------
print("="*62)
print("1.  Logarithmic substitution u = log x, v = log p")
print("="*62)
print("""
  Substitution: u = ln x, v = ln p  (natural log throughout)
  Region transforms:
    xp ≤ E   →  ln x + ln p ≤ ln E  →  u + v ≤ ln E   ✓ correct
    x ≥ ℓ_x  →  u ≥ ln ℓ_x                              ✓ correct
    p ≥ ℓ_p  →  v ≥ ln ℓ_p                              ✓ correct

  Jacobian:
    x = e^u, p = e^v
    dx dp = e^u e^v du dv = x p · du dv
  so  dx/x · dp/p = du dv                                ✓ correct

  This is the multiplicative Haar measure on (ℝ⁺)²,
  standard in the Mellin-transform setup.
""")

# Volume in (u,v) coordinates (multiplicative measure):
# Region: u ≥ a, v ≥ b, u+v ≤ L  where a=ln ℓ_x, b=ln ℓ_p, L=ln E
# Triangle with legs of length (L-a-b) = ln(E/(ℓ_x ℓ_p)) = ln(E/2π)  (ℏ=1)
def V_mult(E, lx, lp):
    """Volume under multiplicative Haar measure = (1/2)·(ln(E/(lx·lp)))²"""
    L = math.log(E / (lx * lp))
    if L <= 0: return 0.0
    return 0.5 * L * L

def V_mult_numerical(E, lx, lp, n=200000):
    """Direct numerical integration in (u,v) space."""
    a, b = math.log(lx), math.log(lp)
    L = math.log(E)
    # u from a to L-b; for each u, v from b to L-u
    if L - b <= a: return 0.0
    total = 0.0
    du = (L - b - a) / n
    for k in range(n):
        u = a + (k + 0.5) * du
        dv = (L - u) - b
        if dv > 0:
            total += dv * du
    return total

print("  Multiplicative volume V_mult = (1/2)·(ln(E/(ℓ_x·ℓ_p)))²:")
print(f"  {'E':>6}  {'ℓ_x':>5}  {'ℓ_p':>5}  {'formula':>10}  {'numerical':>10}  match")
for E, lx, lp in [(10,.5,.5),(100,.1,.2),(50,.3,.4),(200,.5,1.0)]:
    f = V_mult(E, lx, lp)
    n = V_mult_numerical(E, lx, lp)
    ok = abs(f - n) / max(abs(f), 1e-10) < 1e-3
    print(f"  {E:>6}  {lx:>5}  {lp:>5}  {f:>10.5f}  {n:>10.5f}  {'✓' if ok else 'FAIL'}")

print("""
  Note: This multiplicative volume (1/2)·(ln(E/2π))²  is DIFFERENT from
  the Lebesgue volume E·ln(E/2π) − E + 2π computed in the prior audit.
  The state count via multiplicative measure would give:
    N_mult ≈ (ln T)²/(8π²)  — this does NOT match N(T) ≈ T·ln T/(2π).
  The document conflates the two measures. The correct Weyl count uses
  the standard dx dp measure, not the multiplicative measure.

  The Jacobian calculation is correct.
  The claim that collapsing it "proves isomorphism to prime distributions"
  is an OVERCLAIM. The log substitution linearises the hyperbola; it does
  not establish isomorphism. The prime connection requires the explicit
  formula, which is a separate (proven) theorem.
""")

# ---------------------------------------------------------------------------
# 2.  Riemann-Siegel theta vs. phase-space cutoff
# ---------------------------------------------------------------------------
print("="*62)
print("2.  Claim: RS theta cutoff = phase-space cell x_min·p_min = 2π")
print("="*62)

def theta(T):
    """Riemann-Siegel theta: Im(log Γ(1/4 + iT/2)) - T/2 · log π"""
    # Stirling approximation: Im(log Γ(1/4+iT/2)) ≈ T/2·log(T/2) - T/2 - π/8 + ...
    return (T/2)*math.log(T/(2*math.pi)) - T/2 - math.pi/8 + 1/(48*T)

print("""
  Riemann-Siegel formula: ζ(1/2+iT) = 2·Re(e^{iθ(T)} Σ_{n≤M} n^{-1/2-iT}) + R
  where M = floor(√(T/2π))  and  θ(T) ≈ (T/2)·ln(T/2π) − T/2 − π/8 + ...

  The RS cutoff M = floor(√(T/2π)) is an UPPER LIMIT on the sum index n.
  It is NOT a minimum position cutoff. It is NOT equal to x_min.

  Phase-space: ℓ_x·ℓ_p = 2π  is a MINIMUM cell area (product of IR cutoffs).
  RS formula:  M = √(T/2π)    is a MAXIMUM term index in a Dirichlet series.

  These are structurally different objects:
""")

print(f"  {'T':>8}  {'RS cutoff M':>12}  {'√(T/2π)':>10}  {'2π/M²':>10}  {'cell=2π?':>10}")
for T in [14.13, 21.02, 100, 500, 1000]:
    M = math.floor(math.sqrt(T / (2*math.pi)))
    sqrtT2pi = math.sqrt(T/(2*math.pi))
    prod = 2*math.pi / M**2 if M > 0 else float('nan')
    print(f"  {T:>8.2f}  {M:>12d}  {sqrtT2pi:>10.4f}  {prod:>10.4f}  "
          f"{'≠ 2π' if abs(prod - 2*math.pi) > 0.01 else '≈ 2π'}")

print(f"""
  The RS cutoff M grows as √(T/2π).
  The phase-space cell ℓ_x·ℓ_p = 2π is a FIXED constant.
  These quantities have different dimensions, different T-dependence,
  and different conceptual roles.

  Document claim: "confirmed as the exact equivalent" — INCORRECT.
  Actual relationship: both arise from the same scale (T/2π) but play
  different roles. The RS formula cutoff is the MAXIMUM n in the
  Dirichlet sum, not the phase-space minimum observable scale.
""")

# ---------------------------------------------------------------------------
# 3.  Odlyzko-Schönhage algorithm: O(N^{1+ε}) complexity
# ---------------------------------------------------------------------------
print("="*62)
print("3.  Odlyzko-Schönhage: O(N^{1+ε}) for N simultaneous evaluations")
print("="*62)
print("""
  Reference: A.M. Odlyzko & A. Schönhage, "Fast algorithms and the
  Riemann zeta function," Lecture Notes in Math. 1340 (1988).

  The algorithm evaluates ζ(1/2 + it) for N consecutive values of t
  in a block of size ~N, in total time O(N^{1+ε}).

  Naive baseline:
    Riemann-Siegel formula for one value at height T: O(T^{1/2}) operations.
    The N-th zero is at height T_N ≈ 2πN/ln N (asymptotically).
    Per-zero cost ≈ O(N^{1/2} / (ln N)^{1/2}) ≈ O(N^{1/2}).
    Total for N zeros (naive): O(N · N^{1/2}) = O(N^{3/2}).

  Odlyzko-Schönhage improvement:
    Block the N values into a Dirichlet sum Σ_{n≤M} n^{-1/2-it_j}.
    Rearrange as a single sum that can be evaluated at all t_j via FFT.
    FFT of length M ≈ √N takes O(M log M) ≈ O(N^{1/2} log N).
    With O(N / M) ≈ O(N^{1/2}) such blocks → total O(N log N) ≈ O(N^{1+ε}).
    (The ε absorbs log factors.)

  Complexity comparison:
""")
for N in [100, 1000, 10000, 100000, 1000000]:
    naive = N**1.5
    os_   = N * math.log2(N)**2   # rough O(N log²N) bound
    ratio = naive / os_
    print(f"    N={N:>8d}: naive O(N^1.5)={naive:>12.0f}  "
          f"O-S O(N log²N)≈{os_:>12.0f}  speedup≈{ratio:>6.1f}x")

print(f"""
  Claim: "O(N^{{1+ε}}) complexity for N simultaneous evaluation points"
  STATUS: CORRECT. This is the established complexity of the
  Odlyzko-Schönhage algorithm (1988), verified by Odlyzko's numerical
  computations of 10^7+ zeros and subsequent implementations.
  The algorithm was used to verify GUE statistics for zeros near the
  10^20th zero (Odlyzko 2001).

  The "Fourier mode translation n ↔ e^u" is correct: in u = ln x
  coordinates, n corresponds to x = n, and the Dirichlet sum becomes
  a Fourier-type sum in u-space. The FFT exploits this structure.
""")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("="*62)
print("SUMMARY")
print("="*62)
print(f"""
  Claim                                            Status
  ----------------------------------------------------------
  u=log x, v=log p maps xp≤E to u+v≤ln E          CORRECT ✓
  Jacobian: dx/x · dp/p = du dv                    CORRECT ✓
  Log transform "proves isomorphism to primes"      OVERCLAIM — the
    transform linearises the hyperbola; prime        no.
    connection requires the explicit formula.
  Multiplicative volume = (1/2)·(ln E/2π)²         CORRECT ✓
    but gives N_mult ∝ (ln T)², NOT N(T) ∝ T ln T  MISMATCH — the
    Weyl count must use Lebesgue dx dp, not          no.
    multiplicative measure.
  RS theta cutoff = "exact equivalent" of           INCORRECT —
    x_min·p_min = 2π                                different roles,
                                                    different T-scaling.
  Odlyzko-Schönhage: O(N^{{1+ε}}) for N evals       CORRECT ✓
  Fourier mode n ↔ e^u in u=ln x coordinates       CORRECT ✓
  "Layer 2 locked / module verified"                Framing language.
  "Rigorously formalizes wavefront propagation"     Not yet; requires
    (document's pending claim)                      explicit complexity
                                                    proof in this context.
""")
