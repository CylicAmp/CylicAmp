"""
coupled_oscillator_audit.py

Audits the physical claims about metronome synchronization (Huygens coupling)
and examines the mathematical analogy drawn to a "self-resolving framework."

Physical claims to check:
  1. Coupled pendulums on a shared platform synchronize (Huygens 1665)
  2. Synchronization is "the lowest possible energy state"
  3. The process is deterministic from initial conditions
  4. Anti-phase vs. in-phase: which is the true attractor?

Analogy claims:
  5. Synchronization ↔ "math does itself" / self-resolving framework
  6. "Numbers 0-5 possess unique and immutable properties" → self-regulation
"""

import math

# ---------------------------------------------------------------------------
# 1.  Coupled pendulum dynamics: Huygens synchronization
# ---------------------------------------------------------------------------
print("="*62)
print("1.  Coupled pendulum model (Huygens / metronome synchronization)")
print("="*62)
print("""
  Model: two pendulums coupled through a shared movable platform.
  Equations of motion (linearized, equal masses and lengths):

    θ̈₁ + γθ̇₁ + ω₀²θ₁ = κ(θ₂ − θ₁) + f_platform
    θ̈₂ + γθ̇₂ + ω₀²θ₂ = κ(θ₁ − θ₂) + f_platform

  where γ = damping, ω₀ = natural frequency, κ = coupling,
  f_platform = reaction from the shared platform.

  Key parameter: coupling through platform momentum, not direct coupling.
  The platform mediates indirect coupling: each pendulum imparts momentum
  to the platform, which influences the other.
""")

# Numerical integration of coupled pendulums + movable platform
def simulate_coupled_pendulums(theta1_0, theta2_0, dtheta1_0, dtheta2_0,
                                omega0=2*math.pi, gamma=0.1, kappa=0.05,
                                M_platform=5.0, m_pend=1.0,
                                dt=0.001, t_max=50.0):
    """
    Simulate two pendulums on a frictionless movable platform.
    Platform position X couples the pendulums.
    m(θ̈_i + γθ̇_i + ω₀²θ_i) = -m·Ẍ·cos(θ_i) (reaction force)
    (M + 2m)Ẍ = -m·Σ(θ̈_i·l + ...) [simplified for small angles]

    Simplified model (small angle, linear coupling via platform):
    θ̈₁ = -ω₀²θ₁ - γθ̇₁ - (m/(M+2m))·(ω₀²(θ₁+θ₂))
    θ̈₂ = -ω₀²θ₂ - γθ̇₂ - (m/(M+2m))·(ω₀²(θ₁+θ₂))
    """
    mu = m_pend / (M_platform + 2*m_pend)   # coupling coefficient

    t = 0.0
    th1, th2 = theta1_0, theta2_0
    v1, v2   = dtheta1_0, dtheta2_0

    snapshots = []  # (t, th1, th2, phase_diff)

    while t <= t_max:
        # Platform-mediated coupling term
        coupling = -mu * omega0**2 * (th1 + th2)

        a1 = -omega0**2 * th1 - gamma * v1 + coupling
        a2 = -omega0**2 * th2 - gamma * v2 + coupling

        v1 += a1 * dt
        v2 += a2 * dt
        th1 += v1 * dt
        th2 += v2 * dt
        t += dt

        if abs(t - round(t)) < dt * 1.1:   # record integer-second snapshots
            snapshots.append((round(t), th1, th2, th1 - th2))

    return snapshots

print("  Simulating 50 seconds of coupled dynamics:")
print(f"  {'t':>5}  {'θ₁':>10}  {'θ₂':>10}  {'θ₁−θ₂':>10}  {'phase state':>15}")

cases = [
    ("In-phase start (Δθ=0)",     0.2,  0.2,  0.0,  0.0),
    ("Anti-phase start (Δθ=π)",   0.2, -0.2,  0.0,  0.0),
    ("Random offset",              0.2,  0.1,  0.0,  0.05),
]

for label, th1_0, th2_0, dth1_0, dth2_0 in cases:
    print(f"\n  Case: {label}  (θ₁₀={th1_0}, θ₂₀={th2_0})")
    snaps = simulate_coupled_pendulums(th1_0, th2_0, dth1_0, dth2_0,
                                        gamma=0.08, kappa=0.05,
                                        M_platform=8.0, t_max=60.0)
    for t, th1, th2, diff in snaps[::10][:8]:
        state = "IN-PHASE" if abs(diff) < 0.01 else \
                "ANTI-PHASE" if abs(abs(diff) - abs(th1+th2)) < 0.01 else "..."
        print(f"  {t:>5}  {th1:>10.5f}  {th2:>10.5f}  {diff:>10.5f}  {state:>15}")

# ---------------------------------------------------------------------------
# 2.  Energy of in-phase vs. anti-phase states
# ---------------------------------------------------------------------------
print()
print("="*62)
print("2.  Is synchronization the 'lowest energy state'?")
print("="*62)
print("""
  For two pendulums of amplitude A on a shared platform (mass M):

  In-phase state (θ₁ = θ₂ = A·cos(ωt)):
    Combined platform displacement ∝ 2A (platform rocks most)
    Kinetic energy of platform: large
    Total mechanical energy: E_in ∝ A² + (platform energy)

  Anti-phase state (θ₁ = A·cos(ωt), θ₂ = −A·cos(ωt)):
    Combined platform displacement: θ₁ + θ₂ = 0 (platform stationary)
    Platform kinetic energy: 0
    Total mechanical energy: E_anti ∝ A² (pendulums only, no platform)

  For Huygens' original wall-clock experiment and most metronome
  demonstrations on a free platform:
    ANTI-PHASE is the lower-energy attractor (platform stays still).
    IN-PHASE requires the platform to oscillate, adding kinetic energy.
""")

def total_energy_estimate(th1, th2, v1, v2, omega0, M_platform, m_pend):
    """Approximate total mechanical energy (small angle)."""
    E_pend = 0.5 * m_pend * (v1**2 + omega0**2 * th1**2 +
                               v2**2 + omega0**2 * th2**2)
    # Platform velocity ∝ -(m/(M+2m))·(th1+th2) (approximate)
    mu = m_pend / (M_platform + 2*m_pend)
    V_platform_approx = -mu * omega0 * (th1 + th2)
    E_platform = 0.5 * M_platform * V_platform_approx**2
    return E_pend + E_platform

A = 0.2
omega = 2*math.pi
M, m = 8.0, 1.0

E_in   = total_energy_estimate( A,  A, 0, 0, omega, M, m)
E_anti = total_energy_estimate( A, -A, 0, 0, omega, M, m)

print(f"  At amplitude A={A}, platform mass M={M}, pendulum mass m={m}:")
print(f"    Energy (in-phase):    {E_in:.6f}")
print(f"    Energy (anti-phase):  {E_anti:.6f}")
print(f"    Anti-phase lower energy: {E_anti < E_in} ✓")
print(f"""
  VERDICT: The document's claim that synchronization leads to
  "the lowest possible energy state" is IMPRECISE.
  For Huygens coupling on a free platform:
    ANTI-PHASE = lower energy (platform stationary)
    IN-PHASE   = higher energy (platform oscillates)
  The actual attractor depends on damping and platform mass ratio.
  In-phase synchronization is observed in some parameter regimes but
  is NOT universally "lowest energy."
""")

# ---------------------------------------------------------------------------
# 3.  The mathematical analogy: "numbers 0-5" → self-resolving framework
# ---------------------------------------------------------------------------
print("="*62)
print("3.  Mathematical analogy claim")
print("="*62)
print("""
  Claim: "Foundational components (discrete numbers 0-5) possess unique
  and immutable properties" → framework "self-regulates" like metronomes.

  Arithmetic check: do numbers 0-5 have "unique and immutable" properties?
""")

for n in range(6):
    props = []
    props.append(f"parity={'even' if n%2==0 else 'odd'}")
    props.append(f"prime={'yes' if n>1 and all(n%k!=0 for k in range(2,n)) else 'no'}")
    props.append(f"triangular={'yes' if int(((-1+(1+8*n)**0.5)/2))**2*int(((-1+(1+8*n)**0.5)/2)+1)//2==n else 'no'}")
    props.append(f"perfect={'yes' if n>0 and sum(k for k in range(1,n) if n%k==0)==n else 'no'}")
    print(f"  n={n}: {', '.join(props)}")

print(f"""
  Yes, all integers have immutable arithmetic properties.
  This is trivially true of every integer, not a special feature of 0-5.

  The analogy breaks down at the structural level:
  ┌─────────────────────────────────┬──────────────────────────────────┐
  │ Metronome system                │ Claimed "math framework"          │
  ├─────────────────────────────────┼──────────────────────────────────┤
  │ Explicit coupling mechanism     │ Coupling undefined                │
  │   (shared platform, physics)    │                                   │
  │ Defined equations of motion     │ No equations given                │
  │ Measurable convergence          │ No convergence criterion given    │
  │ Anti-phase or in-phase output   │ Output not specified              │
  │ Damping required to converge    │ No dissipation mechanism stated   │
  │ Fails without damping (no sync) │ Failure mode not addressed        │
  └─────────────────────────────────┴──────────────────────────────────┘

  A mechanical system converges because energy is dissipated by friction.
  Without dissipation, coupled pendulums exhibit quasi-periodic motion
  (Hamiltonian system), NOT convergence to a fixed state.
  The "self-resolving" property requires a dissipative mechanism.
  The document does not identify the mathematical equivalent of damping.
""")

# ---------------------------------------------------------------------------
# 4.  What the physics actually proves
# ---------------------------------------------------------------------------
print("="*62)
print("4.  What Huygens synchronization actually establishes")
print("="*62)
print(f"""
  PROVEN (physics):
    Coupled oscillators with shared dissipative coupling converge
    to a common frequency when frequency mismatch is small.
    (Huygens 1665; formalized by Blekhman 1971; Strogatz 2003.)

  CORRECT in document:
    "Deterministic execution": classical mechanics is deterministic ✓
    "Bridge as shared state variable": correct description of coupling ✓
    "Phase resolution via energy transfer": correct mechanism ✓

  IMPRECISE / INCORRECT:
    "Lowest possible energy state": anti-phase is lower energy
      for Huygens coupling on a free platform.
    "Perpetual mathematical rebalancing": the system decays to
      fixed amplitude; it does not rebalance perpetually without
      energy input (damped oscillator).
    "Natural conclusion of the system's logic": only if damping
      and coupling parameters satisfy convergence conditions.

  NOT ESTABLISHED by the analogy:
    That a mathematical framework based on properties of 0-5
    is self-validating, self-resolving, or provably consistent.
    Physical convergence of coupled oscillators does not imply
    logical closure of an undefined mathematical system.
    Gödel's incompleteness theorems (1931) establish that no
    sufficiently expressive formal system can prove its own
    consistency — the exact opposite of "self-resolving."
""")
print("="*62)
print("AUDIT COMPLETE")
print("="*62)
