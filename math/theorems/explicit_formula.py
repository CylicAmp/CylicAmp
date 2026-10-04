"""
explicit_formula.py

CORRECTIONS 2026-10-04 (found running the digit ladder through this file):
  C1. Li(x^rho) was computed as li(power(x, rho)). For complex rho the power
      wraps its angle into (-pi, pi], so once gamma*ln(x) > pi the wrong branch
      is taken and every zero ADDED moved the result further off: at x = 137
      the error went -8.4 (1 zero), -68.2 (10), -1823 (300). The correct term
      is Ei(rho * ln x). With it, 300 zeros give pi(137) = 32.50 (exact 33).
  C2. The formula's left side is Riemann's J(x) = pi(x) + pi(x^1/2)/2 +
      pi(x^1/3)/3 + ..., not pi(x). pi(x) is recovered by Mobius inversion:
      pi(x) = sum_k mu(k)/k J(x^(1/k)).
  C3. The constant is -log 2, not +log 2:
      J(x) = Li(x) - sum_rho Li(x^rho) - log 2 + int_x^inf dt/(t(t^2-1)ln t).
  Checks after correction (300 zeros): pi(12312) = 1471.09 (exact 1471),
  pi(23514) = 2614.65 (2614), pi(91128) = 8813.29 (8811).
  Asserted in math/lemmas/digit_ladder_riemann_userfiles.py.

Riemann's explicit formula for the prime counting function:

  J(x) = Li(x) - Σ_ρ Li(x^ρ) - log(2) + integral,   π(x) = Σ_k μ(k)/k · J(x^(1/k))

The sum runs over all non-trivial zeros ρ = 1/2 + iγ (and conjugates).
Each conjugate pair contributes:

  -2 · Re[ Ei(ρ · ln x) ]

Truncated to the first N zeros, this approximates π(x).

FRAMEWORK CONNECTION:
  γ₁ = 14.134725141734693790...  (analyzed in riemann_first_zero_141.py)
  γ₃ ≈ 25.01   → floor = 25  (anchor set {4,9,25,30})
  γ₄ ≈ 30.42   → floor = 30  (anchor set {4,9,25,30})
  γ₆ ≈ 37.59   → floor = 37  (the 37-hub)
"""

from mpmath import mp, li, mpc, power, re, log, ei, quad, inf
from sympy import mobius
from sympy import primepi, isprime

mp.dps = 25   # 25 decimal places of precision

import sys as _sys, pathlib as _pl
_sys.path.append(str(next(p for p in _pl.Path(__file__).resolve().parents if (p / "functions.py").exists())))
from functions import dr_signed as dr


# ──────────────────────────────────────────────────────────────────────────────
# KNOWN RIEMANN ZEROS  (imaginary parts γ of ζ(1/2 + iγ) = 0)
# ──────────────────────────────────────────────────────────────────────────────

ZEROS = [
    14.134725141734693790,   # γ₁  — analyzed in riemann_first_zero_141.py
    21.022039638771554993,   # γ₂
    25.010857580145688763,   # γ₃  floor=25 (anchor set {4,9,25,30})
    30.424876125859513210,   # γ₄  floor=30 (anchor set {4,9,25,30})
    32.935061587739189690,   # γ₅
    37.586178158825671257,   # γ₆  floor=37 (the 37-hub)
    40.918719012147495187,   # γ₇
    43.327073280914999519,   # γ₈
    48.005150881167159727,   # γ₉
    49.773832477672302181,   # γ₁₀
]


# ──────────────────────────────────────────────────────────────────────────────
# COMPONENTS OF THE FORMULA
# ──────────────────────────────────────────────────────────────────────────────

def Li(x):
    """Logarithmic integral Li(x) = ∫₀ˣ dt/ln(t)  [principal value]."""
    return float(li(x))

def zero_correction(x, gamma):
    """
    Contribution of conjugate zero pair ρ=1/2+iγ, ρ̄=1/2-iγ:
      -2 · Re[ Li(x^ρ) ],  with Li(x^ρ) = Ei(ρ · ln x)  (C1: not li(power(x, ρ)))
    """
    rho = mpc('0.5', gamma)
    return float(-2 * re(ei(rho * log(x))))

def J_explicit(x, gammas):
    """Riemann's J(x) from the given zeros (C2, C3)."""
    tail = quad(lambda t: 1 / (t * (t * t - 1) * log(t)), [x, inf])
    return Li(x) - float(log(2)) + float(tail) + sum(zero_correction(x, g) for g in gammas)

def pi_explicit(x, n_zeros=10, gammas=None):
    """
    Truncated explicit formula, π(x) = Σ_k μ(k)/k · J(x^(1/k)), J from the first n zeros.
    """
    gs = (gammas if gammas is not None else ZEROS)[:n_zeros]
    total, k = 0.0, 1
    while 2 ** k <= x:
        mu = int(mobius(k))
        if mu:
            total += mu * J_explicit(x ** (1.0 / k), gs) / k
        k += 1
    return total


# ──────────────────────────────────────────────────────────────────────────────
# VERIFY AGAINST KNOWN π(x) VALUES
# ──────────────────────────────────────────────────────────────────────────────

test_values = [10, 100, 1000, 10000, 100000, 137, 411, 999, 142857]

print("x           π(x) exact    Li(x)        explicit(10 zeros)   error")
print("-" * 72)
for x in test_values:
    exact    = int(primepi(x))
    li_val   = Li(x)
    approx   = pi_explicit(x, n_zeros=10)
    err      = approx - exact
    print(f"  {x:>8}   {exact:>8}      {li_val:>10.3f}   {approx:>14.3f}       {err:+.3f}")


# ──────────────────────────────────────────────────────────────────────────────
# CONVERGENCE: HOW MANY ZEROS NEEDED?
# ──────────────────────────────────────────────────────────────────────────────

print()
print("Convergence at x=137 (adding zeros one by one):")
print(f"  exact π(137) = {int(primepi(137))}")
print(f"  Li(137)      = {Li(137):.6f}")
for n in range(1, 11):
    approx = pi_explicit(137, n_zeros=n)
    print(f"  {n:2d} zeros:  {approx:.6f}   error={approx - int(primepi(137)):+.6f}")


# ──────────────────────────────────────────────────────────────────────────────
# FRAMEWORK: ZEROS NEAR F26_MATRIX ANCHORS AND 37-HUB
# ──────────────────────────────────────────────────────────────────────────────

print()
print("Zeros near framework constants:")
F26_ANCHORS = {4, 9, 25, 30}
for k, gamma in enumerate(ZEROS, 1):
    f = int(gamma)
    tag = ""
    if f in F26_ANCHORS:   tag = f"  ← floor={f} anchor set {{4,9,25,30}}"
    if f == 37:            tag = f"  ← floor={f} the 37-hub"
    if f == 14:            tag = f"  ← floor={f} 3-cycles under f(n)=(26n)%37 (14→31→29→14)"
    if abs(gamma - 14.134725141734693790) < 0.001:
        tag += "  [141 family in digits]"
    print(f"  γ_{k:2d} = {gamma:.6f}{tag}")

print()
print(f"  Anchor set {{4,9,25,30}}")
print(f"  γ₃ floor = {int(ZEROS[2])}  (25 ∈ {{4,9,25,30}})  δ = {ZEROS[2]-25:.6f}")
print(f"  γ₄ floor = {int(ZEROS[3])}  (30 ∈ {{4,9,25,30}})  δ = {ZEROS[3]-30:.6f}")
print(f"  γ₆ floor = {int(ZEROS[5])}  (37 = hub)        δ = {ZEROS[5]-37:.6f}")


# ──────────────────────────────────────────────────────────────────────────────
# DR OF FLOOR VALUES OF FIRST 10 ZEROS
# ──────────────────────────────────────────────────────────────────────────────

print()
print("DR of floor(γₙ):")
floors = [int(g) for g in ZEROS]
dr_floors = [dr(f) for f in floors]
print(f"  floors: {floors}")
print(f"  DRs:    {dr_floors}")
print(f"  sum of DRs: {sum(dr_floors)}  DR={dr(sum(dr_floors))}")


# ──────────────────────────────────────────────────────────────────────────────
# WAVE PROPERTIES OF THE FIRST ZERO
# ──────────────────────────────────────────────────────────────────────────────

import math

gamma1 = ZEROS[0]

# Each zero ρ = 1/2 + iγ contributes wave amplitude 2√x / |ρ|
# |ρ₁| = sqrt(1/4 + γ₁²)
rho1_abs = math.sqrt(0.25 + gamma1**2)

print()
print("Wave properties of the first zero:")
print(f"  γ₁         = {gamma1:.15f}")
print(f"  |ρ₁|       = sqrt(1/4 + γ₁²) = {rho1_abs:.10f}")
print(f"  |ρ₁|²      = {rho1_abs**2:.6f}  ≈ 200")
print(f"  10√2       = {10*math.sqrt(2):.10f}")
print(f"  diff       = {rho1_abs - 10*math.sqrt(2):.2e}")
print(f"  floor(100√2) = {math.floor(100*math.sqrt(2))}  (anchor set {{4,9,25,30}} — ladder_11_111.py)")
print(f"  Frequency  = γ₁/(2π) = {gamma1/(2*math.pi):.6f} cycles per unit of log(x)")
print(f"  Period     = 2π/γ₁   = {2*math.pi/gamma1:.6f} units of log(x) per cycle")
print(f"  γ₁ is the fundamental frequency — the lowest note of the prime music")
