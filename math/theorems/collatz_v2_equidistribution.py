"""
collatz_v2_equidistribution.py

2-adic valuation distribution in the Collatz / Syracuse map.
Bridges the probabilistic contraction theorem to Problem 3:
"prove contraction-in-expectation implies individual convergence."

─────────────────────────────────────────────────────────────────
STRUCTURE:
  §1  Exact distribution of v₂(3n+1) for odd n        [PROVEN]
  §2  Expected log-ratio per Syracuse step              [PROVEN]
  §3  Moment generating function M_X(t)                [PROVEN]
  §4  Cramér rate I(0) — conditional large-dev bound   [PROVEN conditional]
  §5  Empirical check on n=27 orbit                    [OBSERVED]
  §6  The equidistribution conjecture                  [OPEN]
─────────────────────────────────────────────────────────────────

KEY GAP (stated precisely):
  The Cramér bound in §4 applies to i.i.d. sequences.
  The Collatz orbit is deterministic. Transferring the bound to a
  specific starting value n requires:

    Conjecture (§6): For every odd positive integer n, the empirical
    frequency of {v₂(3T^k(n)+1) = j} over the first N Syracuse steps
    converges to 1/2^j as N → ∞, at a rate sufficient to invoke the
    large-deviation estimate.

  This is an equidistribution statement about a deterministic
  dynamical system. It is not known for any infinite family of n.
"""

import math
from collections import Counter
from scipy.optimize import minimize_scalar
from sympy import isprime


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def v2(n):
    """2-adic valuation: largest k such that 2^k | n."""
    if n == 0:
        return float('inf')
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


# ──────────────────────────────────────────────────────────────────────────────
# §1  EXACT DISTRIBUTION OF v₂(3n+1) FOR ODD n          [PROVEN]
# ──────────────────────────────────────────────────────────────────────────────
#
# Theorem: For n uniform over odd residues mod 2^m (any m ≥ 1),
#   P(v₂(3n+1) = k) = 1/2^k   for k = 1, 2, 3, ...
#
# Proof sketch:
#   v₂(3n+1) ≥ k  iff  3n+1 ≡ 0 (mod 2^k)  iff  n ≡ -3^{-1} (mod 2^k).
#   Since 3 is odd, 3^{-1} exists mod 2^k and is odd, so -3^{-1} is also odd.
#   Among 2^{m-1} odd residues mod 2^m, exactly 2^{m-k} satisfy this,
#   giving P(v₂ ≥ k) = 2^{m-k}/2^{m-1} = 1/2^{k-1}.
#   P(v₂ = k) = P(v₂ ≥ k) - P(v₂ ≥ k+1) = 1/2^{k-1} - 1/2^k = 1/2^k.

# Verify exactly by enumeration over odd residues mod 2^m
for m in range(4, 11):
    odd_residues = [n for n in range(2**m) if n % 2 == 1]
    v2_counts = Counter(v2(3*n + 1) for n in odd_residues)
    total = len(odd_residues)
    for k in range(1, m):
        expected = total // 2**k
        assert v2_counts[k] == expected, (
            f"m={m}, k={k}: got {v2_counts[k]}, expected {expected}"
        )


# ──────────────────────────────────────────────────────────────────────────────
# §2  EXPECTED LOG-RATIO PER SYRACUSE STEP               [PROVEN]
# ──────────────────────────────────────────────────────────────────────────────
#
# Let X = log(3/2^k) where k ~ P(k) = 1/2^k.
# Then E[X] = Σ_{k≥1} (1/2^k) log(3/2^k)
#           = log(3) · Σ 1/2^k  −  log(2) · Σ k/2^k
#           = log(3) · 1        −  log(2) · 2
#           = log(3) − 2·log(2) = log(3/4)

E_X = math.log(3) - 2 * math.log(2)
assert abs(E_X - math.log(3/4)) < 1e-15
assert E_X < 0    # negative: contraction in expectation

# Verify the two series exactly
series_1 = sum(1/2**k for k in range(1, 100))    # → 1
series_2 = sum(k/2**k for k in range(1, 100))    # → 2
assert abs(series_1 - 1) < 1e-10    # 100-term truncation; tail < 1e-28
assert abs(series_2 - 2) < 1e-10    # tail ≈ 103/2^100 < 1e-28

E_X_series = math.log(3) * series_1 - math.log(2) * series_2
assert abs(E_X_series - E_X) < 1e-12


# ──────────────────────────────────────────────────────────────────────────────
# §3  MOMENT GENERATING FUNCTION                         [PROVEN]
# ──────────────────────────────────────────────────────────────────────────────
#
# M_X(t) = E[e^{tX}] = Σ_{k≥1} (1/2^k) · (3/2^k)^t
#         = 3^t · Σ_{k≥1} (1/2^{k(t+1)})
#         = 3^t / (2^{t+1} - 1)     for t > -1  (convergence condition)

def MGF(t):
    """M_X(t) = 3^t / (2^{t+1} - 1),  domain t > -1."""
    return 3**t / (2**(t+1) - 1)

def log_MGF(t):
    return t * math.log(3) - math.log(2**(t+1) - 1)

# Verify at t=0: M_X(0) = 1 (total probability)
assert abs(MGF(0) - 1.0) < 1e-15

# Verify derivative at t=0 equals E[X] = log(3/4)
h = 1e-7
dlogMGF_at_0 = (log_MGF(h) - log_MGF(-h)) / (2*h)
assert abs(dlogMGF_at_0 - E_X) < 1e-5

# Cross-check MGF against direct summation
for t in [0.1, 0.5, 1.0, 2.0]:
    direct = sum((1/2**k) * (3/2**k)**t for k in range(1, 200))
    formula = MGF(t)
    assert abs(direct - formula) / formula < 1e-10


# ──────────────────────────────────────────────────────────────────────────────
# §4  CRAMÉR RATE I(0)  —  CONDITIONAL LARGE-DEVIATION BOUND
# ──────────────────────────────────────────────────────────────────────────────
#
# Cramér's theorem (i.i.d. case):
#   If X_1, X_2, ... are i.i.d. copies of X, then
#   P( X_1 + ... + X_N ≥ 0 ) ≤ exp(-N · I(0))
# where I(0) = sup_{t≥0} [-log M_X(t)] = -min_{t≥0} log M_X(t).
#
# Since log M_X is convex and d/dt log M_X |_{t=0} = E[X] = log(3/4) < 0,
# the minimum occurs at some t* > 0 where d/dt log M_X = 0:
#
#   d/dt log M_X(t) = log(3) - 2^{t+1} log(2) / (2^{t+1}-1) = 0
#   →  2^{t*+1} = log(3) / log(3/2)  ≈  2.7095
#   →  t*  ≈  0.4380
#
# STATUS: The bound exp(-N · I(0)) is [PROVEN] for i.i.d. X_i.
#         Its application to a SPECIFIC Collatz orbit is [CONDITIONAL]:
#         it requires the empirical v₂ distribution to match the i.i.d.
#         model (see §6).

res   = minimize_scalar(log_MGF, bounds=(0, 20), method='bounded')
T_STAR = res.x
I_0    = -res.fun

assert abs(T_STAR - 0.4380) < 1e-3
assert abs(I_0 - 0.0550) < 1e-3
assert I_0 > 0    # positive rate confirms exponential decay

# What t* satisfies: 2^{t*+1} = log3/log(3/2)
U_STAR = math.log(3) / math.log(3/2)
assert abs(2**(T_STAR + 1) - U_STAR) < 1e-5

# Cramér bound at selected N values
for N, bound in [(10, math.exp(-10 * I_0)),
                 (100, math.exp(-100 * I_0)),
                 (1000, math.exp(-1000 * I_0))]:
    assert bound > 0
    assert bound < 1


# ──────────────────────────────────────────────────────────────────────────────
# §5  EMPIRICAL v₂ DISTRIBUTION: n=27 ORBIT             [OBSERVED]
# ──────────────────────────────────────────────────────────────────────────────
#
# The orbit of 27 under the Syracuse map (odd steps only) has 42 elements.
# We record v₂(3n+1) for each of the 41 transitions and compare to P(k)=1/2^k.
# 41 steps is a small sample; deviations from theory are expected.

def syracuse_orbit(n):
    """Sequence of odd values in the Collatz orbit of odd n, ending at 1."""
    orbit = [n]
    while n != 1:
        val = 3*n + 1
        val //= 2**v2(val)
        orbit.append(val)
        n = val
    return orbit

orbit_27 = syracuse_orbit(27)
assert orbit_27[0] == 27 and orbit_27[-1] == 1
N_STEPS = len(orbit_27) - 1    # 41

v2_seq = [v2(3*n + 1) for n in orbit_27[:-1]]
v2_empirical = Counter(v2_seq)

# Empirical frequencies
EMP = {k: v2_empirical[k] / N_STEPS for k in range(1, 6)}
THEORY = {k: 1 / 2**k for k in range(1, 6)}

# Empirical mean k
emp_mean = sum(k * v2_empirical[k] for k in v2_empirical) / N_STEPS

# With 41 steps the empirical distribution need not match theory closely —
# we only assert it lies in a reasonable range (within 3 std devs for k=1)
# Std dev for Bernoulli(1/2) over 41 trials: sqrt(41 * 1/2 * 1/2) / 41 ≈ 0.078
assert abs(EMP[1] - THEORY[1]) < 0.15    # observed: 0.585 vs 0.500
assert abs(EMP[2] - THEORY[2]) < 0.10    # observed: 0.244 vs 0.250


# ──────────────────────────────────────────────────────────────────────────────
# §6  THE EQUIDISTRIBUTION CONJECTURE                    [OPEN]
# ──────────────────────────────────────────────────────────────────────────────
#
# CONJECTURE: For every odd positive integer n, the empirical frequency
#   F_j(N, n) = #{i < N : v₂(3 T^i(n) + 1) = j} / N
# satisfies  lim_{N→∞} F_j(N, n) = 1/2^j   for each j ≥ 1.
#
# WHAT IT WOULD GIVE (if proven):
#   By the conditional Cramér bound from §4, with rate I(0) ≈ 0.055,
#   no Collatz orbit can sustain net growth: the empirical log-mean
#   = Σ_j F_j(N,n) · log(3/2^j) → log(3/4) < 0.
#   Large deviations in the arithmetic of the orbit would be bounded
#   by exp(-N · I(0)), ruling out divergence via a quantitative estimate.
#
# WHAT IT DOES NOT IMMEDIATELY GIVE:
#   Equidistribution of v₂ does not by itself rule out a non-trivial
#   integer cycle, which could have equidistributed v₂ values while
#   cycling. Ruling out cycles requires the separate modular analysis
#   in collatz_mod37_basin.py.
#
# STATUS: Not known for any infinite family of starting values n.
#         Extensive numerical evidence supports it (e.g., n=27 above),
#         but a proof requires new techniques relating deterministic
#         dynamics on Z to the 2-adic harmonic analysis on Q_2.


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Collatz v₂ Equidistribution — Probabilistic Bridge")
    print("=" * 62)

    print("\n── §1  DISTRIBUTION OF v₂(3n+1) ──")
    print("  P(v₂(3n+1) = k) = 1/2^k  [PROVEN]")
    print("  Verified by enumeration for odd n mod 2^m, m = 4..10")

    print("\n── §2  EXPECTED LOG-RATIO ──")
    print(f"  E[log(T(n)/n)] = log(3/4) ≈ {E_X:.6f}  [PROVEN]")
    print(f"  = log(3)·1 − log(2)·2  (two exact series)")

    print("\n── §3  MOMENT GENERATING FUNCTION ──")
    print(f"  M_X(t) = 3^t / (2^{{t+1}} − 1),   domain t > −1")
    print(f"  M_X(0) = {MGF(0):.4f}  (= 1 ✓)")
    print(f"  (d/dt log M_X)|_{{t=0}} = {dlogMGF_at_0:.6f}  (= E[X] ✓)")

    print("\n── §4  CRAMÉR RATE I(0) ──")
    print(f"  t* = {T_STAR:.6f}  (critical point: 2^{{t*+1}} = log3/log(3/2) ≈ {U_STAR:.4f})")
    print(f"  log M_X(t*) = {res.fun:.8f}")
    print(f"  I(0) = {I_0:.8f}  (exponential decay rate per step)")
    print(f"  Cramér bound (i.i.d. model):")
    for N in [10, 50, 100, 1000]:
        b = math.exp(-N * I_0)
        print(f"    N={N:4d}:  P(orbit grows) ≤ e^{{−{N}×{I_0:.4f}}} = {b:.2e}")
    print(f"  [CONDITIONAL on §6 equidistribution conjecture]")

    print("\n── §5  n=27 ORBIT (empirical) ──")
    print(f"  Syracuse steps: {N_STEPS}")
    print(f"  Empirical mean k: {emp_mean:.4f}  (theory: 2.0000)")
    print(f"  {'k':>4}  {'observed':>10}  {'theory':>10}  {'diff':>8}")
    for k in range(1, 6):
        obs = EMP.get(k, 0)
        thy = THEORY[k]
        print(f"  {k:>4}  {obs:>10.4f}  {thy:>10.4f}  {obs-thy:>+8.4f}")

    print("\n── §6  EQUIDISTRIBUTION CONJECTURE [OPEN] ──")
    print("  lim_{N→∞} F_j(N,n) = 1/2^j  for all odd n, all j ≥ 1")
    print("  Status: not proven for any infinite family of n")
    print("  Bridge to conjecture: I(0) ≈ 0.055 gives the quantitative rate")
    print("  once equidistribution is established for a specific orbit.")

    print()
    print("All assertions passed.")
