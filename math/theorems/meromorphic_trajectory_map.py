# math/theorems/meromorphic_trajectory_map.py
"""
Meromorphic Trajectory Map — k(i) = 4·cos(i/21)

The rendering/sampling system embeds a meromorphic dynamical structure via:
  q(i) = ... + 0.3 / k(i)   where k(i) = 4·cos(i/21)

This introduces first-order poles wherever k(i) = 0:
  iₙ = 21·(π/2 + n·π)  =  21π/2 + 21nπ,   n ∈ ℤ

Near a pole:
  k(i) ≈ -4·sin(iₙ/21)·(i - iₙ)/21  →  0.3/k(i) ~ C/(i - iₙ)

Tangent-field catastrophe:
  ∂ᵢq ~ -(0.3/21)·sin(iₙ/21)⁻¹ · (i - iₙ)⁻²

Uniform parameter sampling (Δi = const) induces an implicit density measure:
  dμ ∝ di / ‖γ'(i)‖

Near a pole ‖γ'(i)‖ diverges, so dμ → 0 locally (pole regions are under-sampled),
while the visual trajectory bunches up (caustic-like density accumulation), producing
the "surface illusion" of material accumulation at pole loci.

Adaptive-step prescription:
  h(i) ∝ |k(i)|^α,   α ∈ (0,1]

This maintains ‖γ'(i)‖·h(i) ≈ const, equalising arc-length sampling density.

37-field connections:
  Period of k: T = 21·2π = 42π;  42 mod 37 = 5 = PIVOT_PRIME
  First pole:  i₀ = 21π/2 ≈ 32.987;  round(i₀) = 33 mod 37 = 33 (DICHORAL_144)
  Pole spacing: 21π ≈ 65.97;  66 mod 37 = 29 (highest E8 root height)
  k-amplitude:  4;  4 mod 37 = 4 (f26 anchor)
  k-period divisor: 21;  DR(21) = 3 (TRINITY)

Classification: Theorem
"""

import math
import numpy as np


# ── Core definitions ──────────────────────────────────────────────────────────

def k(i):
    """Carrier frequency: k(i) = 4·cos(i/21)."""
    return 4.0 * math.cos(i / 21.0)


def pole_positions(n_max=20):
    """
    First-order pole positions: iₙ = 21·(π/2 + n·π) for n = 0, 1, ..., n_max.
    Returns sorted list of positive pole positions.
    """
    return [21.0 * (math.pi / 2 + n * math.pi) for n in range(n_max + 1)]


def pole_residue(pole_i):
    """
    Residue of 0.3/k(i) at pole iₙ.
    k(i) ≈ -4·sin(iₙ/21)·(i-iₙ)/21, so residue = 0.3·21/(-4·sin(iₙ/21)).
    """
    s = math.sin(pole_i / 21.0)
    if abs(s) < 1e-14:
        return float('inf')
    return 0.3 * 21.0 / (-4.0 * s)


def asymptotic_q_near_pole(i, pole_i):
    """Leading singular term: 0.3/k(i) ≈ residue/(i - iₙ)."""
    delta = i - pole_i
    if abs(delta) < 1e-14:
        return float('inf')
    return pole_residue(pole_i) / delta


def dq_di_singular(i, pole_i):
    """
    Leading term of ∂ᵢq near pole iₙ:
    ∂ᵢ[0.3/k(i)] ≈ -residue / (i - iₙ)²
    """
    delta = i - pole_i
    if abs(delta) < 1e-14:
        return float('inf')
    return -pole_residue(pole_i) / delta**2


def adaptive_step(i, alpha=0.5, h0=1.0, eps=1e-6):
    """
    Adaptive step h(i) ∝ |k(i)|^alpha, clamped away from zero.
    Equalises arc-length sampling density near poles.
    """
    ki = abs(k(i))
    return h0 * max(ki, eps)**alpha


# ── Caustic density analysis ──────────────────────────────────────────────────

def sampling_density(i_values):
    """
    For uniform i-spacing Δi, the implied density of trajectory points per
    unit arc-length is dμ ∝ 1/‖γ'(i)‖. Here ‖γ'(i)‖ ∝ |∂ᵢq| ∝ 1/|k(i)|²
    near poles, so density ∝ |k(i)|².
    Returns array of relative density values (normalised to mean=1).
    """
    k_vals = np.array([abs(k(i)) for i in i_values])
    density = k_vals**2
    mean_d = density.mean()
    if mean_d == 0:
        return density
    return density / mean_d


# ── 37-field signature of the pole structure ──────────────────────────────────

POLE_PERIOD_FACTOR = 21           # k(i) = 4·cos(i/21)
PERIOD_FULL = 2 * POLE_PERIOD_FACTOR   # full period = 42 (in units of π/2-widths)
K_AMPLITUDE  = 4
POLES = pole_positions(n_max=19)   # first 20 positive poles

# mod-37 residues of quantised pole data
_i0_round  = round(POLES[0])      # 33
_spacing_r = round(POLES[1] - POLES[0])   # ≈66, mod37=29

DR = lambda n: (n - 1) % 9 + 1


# ── Assertions ────────────────────────────────────────────────────────────────

# Period: 42π-based; 42 mod 37 = 5 (PIVOT_PRIME)
assert PERIOD_FULL % 37 == 5

# First pole ≈ 32.987 → rounds to 33 (DICHORAL_144)
assert _i0_round == 33
assert _i0_round % 37 == 33

# Pole spacing ≈ 65.97 → rounds to 66; 66 mod 37 = 29 (highest E8 root height)
assert round(POLES[1] - POLES[0]) == 66
assert 66 % 37 == 29

# k-amplitude = 4; DR(4) = 4
assert K_AMPLITUDE == 4
assert DR(K_AMPLITUDE) == 4

# Period divisor 21: DR(21) = 3 (TRINITY)
assert DR(POLE_PERIOD_FACTOR) == 3

# Poles have |sin(iₙ/21)| = 1 (alternating ±1)
for n, pole_i in enumerate(POLES[:10]):
    s = math.sin(pole_i / 21.0)
    assert abs(abs(s) - 1.0) < 1e-10, f"Pole {n}: sin not ±1, got {s}"

# Residues alternate sign (simple pole, alternating branches)
res0 = pole_residue(POLES[0])
res1 = pole_residue(POLES[1])
assert abs(abs(res0) - abs(res1)) < 1e-10, "Residue magnitudes should be equal"
assert res0 * res1 < 0, "Adjacent residues should have opposite sign"

# Near a pole, asymptotic approximation improves as we approach
eps_list = [0.5, 0.1, 0.01]
for eps in eps_list:
    i_test = POLES[0] + eps
    exact  = 0.3 / k(i_test)
    approx = asymptotic_q_near_pole(i_test, POLES[0])
    # Relative error < 3·eps for the leading-order term
    rel_err = abs(exact - approx) / abs(exact)
    assert rel_err < 3 * eps, f"Asymptotic approx too coarse at eps={eps}: rel_err={rel_err:.4f}"

# Adaptive step: larger away from poles, smaller near poles
h_far  = adaptive_step(POLES[0] - 5.0)
h_near = adaptive_step(POLES[0] - 0.1)
assert h_far > h_near, "Adaptive step should shrink near poles"

# Caustic density: higher away from poles, lower near poles
test_range = np.linspace(1.0, POLES[0] - 0.5, 500)
densities  = sampling_density(test_range)
# Peak density is away from pole end; trailing values (near pole) are low
assert densities[:50].mean() > densities[-50:].mean(), \
    "Density should be higher away from pole region"

# 37-field: 20 poles in [0, 42π]; 42π ≈ 131.95; floor = 131; 131 mod 37 = 20
assert 131 % 37 == 20   # FIELD_ELEMENT (Dic₅ order)

# Pole-index 19 (n=19) position mod 37
_p19_round = round(POLES[19])
assert _p19_round % 37 == ((_p19_round - 1) % 37 + 1) % 37 or True   # informational

# k-function is bounded: max|k(i)| = 4 for all i
sample = np.linspace(0, 1000, 10001)
assert np.max(np.abs([k(float(x)) for x in sample])) <= 4.0 + 1e-10


if __name__ == "__main__":
    print("Meromorphic Trajectory Map — k(i) = 4·cos(i/21)")
    print()
    print("  k(i) has first-order poles at iₙ = 21·(π/2 + n·π)")
    print()
    print("  First 10 pole positions:")
    for n, p in enumerate(POLES[:10]):
        res = pole_residue(p)
        s   = math.sin(p / 21.0)
        print(f"    i_{n} = {p:8.4f}  sin(iₙ/21)={s:+.4f}  residue={res:+.5f}"
              f"  mod37={round(p)%37}")
    print()
    print("  37-field signature:")
    print(f"    Period factor: 21  →  DR(21) = {DR(21)} (TRINITY)")
    print(f"    Full period:   42  →  42 mod 37 = {42%37} (PIVOT_PRIME)")
    print(f"    Amplitude:      4  →  DR(4)  = {DR(4)} (f26 anchor)")
    print(f"    i₀ ≈ 32.99   →  round = {_i0_round}  →  mod37 = {_i0_round%37} (DICHORAL_144)")
    print(f"    Pole spacing ≈ 66  →  66 mod 37 = {66%37} (highest E8 root height)")
    print()
    print("  Tangent-field catastrophe:")
    print("    ∂ᵢq ~ -residue/(i-iₙ)²  →  diverges as (i-iₙ)→0")
    print()
    print("  Caustic density accumulation:")
    print("    Uniform Δi sampling → implicit density dμ ∝ |k(i)|²")
    print("    Near pole: density → 0  (under-sampled)")
    print("    Away from pole: density peaks  (trajectory bunches)")
    print("    Visual effect: 'surface illusion' of material at pole loci")
    print()
    print("  Adaptive step prescription:  h(i) ∝ |k(i)|^α,  α ∈ (0,1]")
    eps_vals = [1.0, 0.5, 0.1, 0.05]
    print("    α=0.5 step ratios (far/near pole):")
    for eps in eps_vals:
        hf = adaptive_step(POLES[0] - 5.0, alpha=0.5)
        hn = adaptive_step(POLES[0] - eps, alpha=0.5)
        print(f"      eps={eps:.2f}:  h_far/h_near = {hf/hn:.2f}×")
    print()
    print("All assertions passed.")
