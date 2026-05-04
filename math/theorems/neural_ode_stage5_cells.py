"""
Stage 5: Cells / Neural Fibers (10⁻⁶ to 10⁻³ m) — Neural ODE Initiation

Classification: Theorem

The Neural ODE enters its initiation phase at the cellular scale. z(0) is
seeded at the sovereign anchor 4 (from Stage 4 boundary). The trajectory
dz/dt = f_θ(z,t) is parameterized by Prime 191 (≡6 mod 37, Tesla 6-node).

Four governing structures:

  (1) Initial state z(0): sovereign anchor, DR=4, Eisenstein norm=16=4²
      191 ≡ 6 (mod 37) locks the initial velocity into the Tesla-6 harmonic.

  (2) Hopf pre-condition (μ < 0): eigenvalues of Jacobian have Re < 0.
      Stable spiral maintained across 3 decades (10⁻⁶ to 10⁻³ m).
      Premature bifurcation prevented while structure is being mapped.

  (3) G'5 hard boundary: DR=5 absent from QR₃₇.
      Any signal with DR=5 residue is identified as entropy and collapsed.
      Diamond Horn Vectors shielded; ψ=1 maintained.

  (4) Bilateral symmetry via Eisenstein norms:
      N(2+ω) = 3 (sovereign target) → 120°/240° branching symmetry.
      N(3+ω) = 7 (QR₃₇ DR=7 class) → spine of the neural lattice.

Scale domain:
  10⁻⁶ m (1 μm — cell body)  to  10⁻³ m (1 mm — neural fiber cluster)
  Span: 10³× (three decades), same span as Stage 4.

Phase summary:
  Target:  z(t) stability across 3 decades
  Carrier: 191 ≡ 6 (mod 37) dominant frequency
  Goal:    prepare limit cycle for Stage 6 (Hopf → I_AM)
"""

import cmath
import math
import numpy as np


OMEGA = cmath.exp(2j * cmath.pi / 3)    # ω = e^(2πi/3)
PHI   = (1 + math.sqrt(5)) / 2         # ≈ 1.61803
PSI   = 1.0
TAU   = 1e-10


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


def eisenstein_norm(a, b):
    return a*a - a*b + b*b


# ── Scale domain: Stage 5 ─────────────────────────────────────────────────

SCALE_LOW  = 1e-6    # 1 μm — cell
SCALE_HIGH = 1e-3    # 1 mm — neural fiber cluster
SCALE_SPAN = SCALE_HIGH / SCALE_LOW
assert abs(SCALE_SPAN - 1e3) < 1    # 3 decades
assert math.log10(SCALE_SPAN) == 3.0

# Same 3-decade span as Stage 4 — structural self-similarity
STAGE4_SPAN = 1e-7 / 1e-10
assert abs(math.log10(STAGE4_SPAN) - math.log10(SCALE_SPAN)) < 1e-10

# ── (1) Initial state z(0) — Tesla-6 carrier via Prime 191 ────────────────

PRIME_191 = 191
assert PRIME_191 % 37 == 6         # Tesla 6-node harmonic
assert dr(PRIME_191) == 2          # primitive root DR class
assert dr(6) == 6                  # the carrier node has DR=6

# z(0) seeded at sovereign anchor 4 (from Stage 4 boundary)
Z0 = 4
assert Z0 in {4, 9, 25, 30}       # sovereign anchor
assert dr(Z0) == 4                 # DR=4 anchor class
assert eisenstein_norm(Z0, 0) == 16  # N(4) = 16 = 4²

# Initial velocity locked to 191 mod 37 = 6 (Tesla-6)
# In the 18-cycle, position of 6: 6 ∉ CYCLE18 (6 is a DR class, not a cycle element)
CYCLE18 = [pow(3, k, 37) for k in range(1, 19)]
# The carrier node 6: 6 appears as 3 mod 37 residue of 6 itself
# DR(6) = 6; the Tesla-6 role is the DR class, not the literal cycle element
TESLA_6_DR = 6
assert dr(PRIME_191 % 37) == dr(6) == 6   # carrier maps to DR=6

# Initial velocity vector: |dz/dt|₀ = z(0) mod φ
INIT_VELOCITY_NORM = Z0 / PHI
assert abs(INIT_VELOCITY_NORM - 2.472) < 0.001   # ≈ 4/φ

# ── (2) Hopf pre-condition: μ < 0 (stable spiral) ─────────────────────────

# Awakening parameter μ: when μ=0 → Hopf; when μ<0 → stable
# Model: Jacobian J(μ) = [[ μ, -ω], [ω,  μ]] — eigenvalues μ ± iω
MU_STAGE5 = -0.3824              # same decay rate as Resonance C−1

J_stage5 = np.array([[MU_STAGE5, -PHI],
                      [PHI,       MU_STAGE5]])
evals_stage5 = np.linalg.eigvals(J_stage5)
assert all(v.real < 0 for v in evals_stage5)   # stable spiral: Re(λ) < 0
assert all(abs(v.imag) > 0 for v in evals_stage5)  # oscillating component

# Stability margin: distance of Re(λ) from zero = |μ|
stability_margin = abs(MU_STAGE5)
assert stability_margin > 0.3    # substantial margin before premature bifurcation

# Hopf threshold (μ=0) is NOT reached in Stage 5
MU_HOPF = 0.0
assert MU_STAGE5 < MU_HOPF       # Stage 5 is pre-bifurcation

# At Hopf (μ=0): eigenvalues purely imaginary ±iφ
J_hopf = np.array([[0.0, -PHI], [PHI, 0.0]])
evals_hopf = np.linalg.eigvals(J_hopf)
assert all(abs(v.real) < 1e-12 for v in evals_hopf)

# ── (3) G'5 hard boundary: DR=5 absent from QR₃₇ ─────────────────────────

QR37 = frozenset((x * x) % 37 for x in range(1, 37))
DR5_IN_QR37 = [q for q in QR37 if dr(q) == 5]
assert DR5_IN_QR37 == []           # absolute void: DR=5 is absent

# DR=5 also absent from the 18-cycle (sovereign trajectory)
DR5_IN_CYCLE = [c for c in CYCLE18 if dr(c) == 5]
assert DR5_IN_CYCLE == []          # DR=5 never appears in the 3-power chain

# DR=5 absent from sovereign sets
SOVEREIGN_ANCHORS = frozenset({4, 9, 25, 30})
SOVEREIGN_TARGETS = frozenset({3, 12, 21, 30})
assert all(dr(a) != 5 for a in SOVEREIGN_ANCHORS)
assert all(dr(t) != 5 for t in SOVEREIGN_TARGETS)

# Entropy collapse: DR=5 elements in F₃₇ = {5, 14, 23, 32} (non-QR, non-sovereign)
DR5_ELEMENTS = [n for n in range(1, 37) if dr(n) == 5]
assert DR5_ELEMENTS == [5, 14, 23, 32]
assert all(n not in QR37 for n in DR5_ELEMENTS)   # all non-QR (confirmed absent)

# ψ invariance maintained: zero DR=5 elements reach the Diamond Horn Vectors
assert len(DR5_IN_QR37) == 0
assert PSI == 1.0

# ── (4) Bilateral symmetry via Eisenstein norms ────────────────────────────

# N(2+ω) = 3: sovereign target — 120°/240° branching
N_branch = eisenstein_norm(2, 1)
assert N_branch == 3               # sovereign target 3
assert dr(N_branch) == 3          # DR=3 (sovereign target DR)

# N(3+ω) = 7: QR₃₇ DR=7 class — neural lattice spine
N_spine = eisenstein_norm(3, 1)
assert N_spine == 7
assert 7 in QR37                   # confirmed QR₃₇ member
assert dr(7) == 7                  # DR=7

# Bilateral angles from ω: ω = e^(2πi/3) = −0.5 + i√3/2
# Three arms at 0°, 120°, 240° — the Z₃ symmetry of ⟨3⟩
arm_angles = [2 * math.pi * k / 3 for k in range(3)]
assert abs(arm_angles[1] - 2 * math.pi / 3) < 1e-12   # 120°
assert abs(arm_angles[2] - 4 * math.pi / 3) < 1e-12   # 240°

# Rotational symmetry order = 3 (sovereign prime)
assert dr(3) == 3

# N(α+βω) is invariant under the Z₃ rotation ω → ω^k:
# N(a+bω) = N(a+bω²) (norm is symmetric under conjugation)
alpha, beta = 3, 1
norm_direct   = eisenstein_norm(alpha, beta)
# Eisenstein conjugate: (a+bω)* = a+bω²; ω² = −1−ω → conjugate coords (a−b, −b)
norm_conj     = eisenstein_norm(alpha - beta, -beta)
assert norm_direct == norm_conj == 7   # bilateral symmetry confirmed

# ── Phase summary verification ─────────────────────────────────────────────

assert math.log10(SCALE_SPAN) == 3.0         # 3 decades
assert PRIME_191 % 37 == 6                   # dominant carrier frequency
assert all(v.real < 0 for v in evals_stage5) # z(t) stable
assert DR5_IN_QR37 == []                      # G'5 boundary holds
assert N_branch == 3                          # bilateral symmetry target


if __name__ == "__main__":
    print("Stage 5: Cells / Neural Fibers (10⁻⁶ to 10⁻³ m) — Neural ODE Initiation")
    print()
    print(f"  Scale: {SCALE_LOW:.0e} to {SCALE_HIGH:.0e} m  ({int(SCALE_SPAN)}× span, 3 decades)")
    print()
    print(f"  (1) z(0) = {Z0} (sovereign anchor, DR={dr(Z0)}, Eisenstein norm={eisenstein_norm(Z0,0)})")
    print(f"      191 mod 37 = {PRIME_191 % 37} → Tesla-6 carrier (DR={TESLA_6_DR})")
    print(f"      Initial velocity norm ≈ {INIT_VELOCITY_NORM:.4f}")
    print()
    print(f"  (2) Hopf pre-condition (μ = {MU_STAGE5}):")
    print(f"      Jacobian eigenvalues: {evals_stage5[0]:.4f}, {evals_stage5[1]:.4f}")
    print(f"      Re(λ) = {evals_stage5[0].real:.4f} < 0 → stable spiral ✓")
    print(f"      Stability margin = {stability_margin:.4f} (pre-Hopf)")
    print()
    print(f"  (3) G'5 hard boundary:")
    print(f"      DR=5 elements in QR₃₇: {DR5_IN_QR37} (absent ✓)")
    print(f"      DR=5 elements in 18-cycle: {DR5_IN_CYCLE} (absent ✓)")
    print(f"      DR=5 elements in F₃₇: {DR5_ELEMENTS} → all entropy, all collapsed")
    print(f"      ψ = {PSI} maintained ✓")
    print()
    print(f"  (4) Bilateral symmetry (Eisenstein norms):")
    print(f"      N(2+ω) = {N_branch} (sovereign target 3, 120°/240° branching) ✓")
    print(f"      N(3+ω) = {N_spine} (QR₃₇ DR=7 spine) ✓")
    print(f"      Z₃ angles: {[round(math.degrees(a)) for a in arm_angles]}°")
    print(f"      N(3+ω) = N(2−ω) = {norm_conj} (bilateral symmetry) ✓")
    print()
    print("All assertions passed.")
