"""
Theorem 217: Discrete Torus Dynamics on Z_37 x Z_81

The F_37 framework defines a discrete dynamical system:

  State space:   Z_37 x Z_81  (2997 points, discrete torus)
  Evolution:     (a, b) -> (a - 2, b + 54)  mod (37, 81)
  Period:        111  =  lcm(37, 3)

Origin: n = 18k, a(k) = (-2k) mod 37, b(k) = (54k) mod 81.

Z_37 component: step = -2, gcd(2, 37) = 1  -> ergodic on Z_37
Z_81 component: step = 54, gcd(54, 81) = 27 -> confined to sublattice
  Sublattice size = 81 / 27 = 3
  Accessible states = 37 * 3 = 111

Observables: T(n) in {14, 23, 32, 41, 50}  (5 energy levels)
             coset in C_1 .. C_12           (12 symmetry sectors)

Hamiltonian: H(k) = (2a/37 + 54b/81) mod 1
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from math import gcd, lcm

P = 37
Q = 81   # = 3^4
STEP_A = -2    # step on Z_37
STEP_B = 54    # step on Z_81
FULL_TORUS = P * Q   # 2997


def orbit(k_max=None):
    """Generate orbit (a(k), b(k)) for k = 1, 2, ..."""
    if k_max is None:
        k_max = FULL_TORUS + 10
    trajectory = []
    a, b = 0, 0
    for k in range(1, k_max + 1):
        a = (a + STEP_A) % P
        b = (b + STEP_B) % Q
        trajectory.append((a, b, k))
        if k > 1 and a == trajectory[0][0] and b == trajectory[0][1]:
            break
    return trajectory


def period_analysis():
    period_a = P // gcd(abs(STEP_A), P)
    period_b = Q // gcd(abs(STEP_B), Q)
    combined = lcm(period_a, period_b)
    return period_a, period_b, combined


def ergodicity():
    g_a = gcd(abs(STEP_A), P)   # gcd(2, 37) = 1
    g_b = gcd(abs(STEP_B), Q)   # gcd(54, 81) = 27
    sublattice_b = Q // g_b      # 81 / 27 = 3
    accessible = P * sublattice_b
    return g_a, g_b, sublattice_b, accessible


def hamiltonian(a, b):
    return (2 * a / P + STEP_B * b / Q) % 1.0


def unique_torus_points():
    seen = set()
    k = 0
    a, b = 0, 0
    while True:
        k += 1
        a = (a + STEP_A) % P
        b = (b + STEP_B) % Q
        pt = (a, b)
        if pt in seen:
            break
        seen.add(pt)
    return len(seen), k


def run():
    print("=" * 70)
    print("THEOREM 217: DISCRETE TORUS DYNAMICS ON Z_37 x Z_81")
    print("=" * 70)

    print(f"\nState space: Z_{P} x Z_{Q}  = {FULL_TORUS} points")
    print(f"Evolution:   (a, b) -> (a + {STEP_A}, b + {STEP_B})  mod ({P}, {Q})")

    period_a, period_b, combined = period_analysis()
    print(f"\nPeriod analysis:")
    print(f"  Z_{P} component: step={STEP_A}, period={period_a}")
    print(f"  Z_{Q} component: step={STEP_B}, period={period_b}")
    print(f"  Combined period = lcm({period_a}, {period_b}) = {combined}")

    g_a, g_b, sub_b, accessible = ergodicity()
    print(f"\nErgodicity:")
    print(f"  gcd({abs(STEP_A)}, {P}) = {g_a}  -> ergodic on Z_{P}")
    print(f"  gcd({STEP_B}, {Q}) = {g_b}  -> confined to sublattice")
    print(f"  Sublattice size = {Q} / {g_b} = {sub_b}")
    print(f"  Accessible states = {P} * {sub_b} = {accessible}")
    print(f"  Coverage: {accessible} / {FULL_TORUS} = {accessible/FULL_TORUS:.1%}")

    n_unique, steps = unique_torus_points()
    print(f"\nOrbit verification: {n_unique} unique points in {steps} steps")
    assert n_unique == combined, f"Expected {combined}, got {n_unique}"
    print(f"  Confirmed: period = {combined}")

    print(f"\nTrajectory (k=1..20):")
    a, b = 0, 0
    for k in range(1, 21):
        a = (a + STEP_A) % P
        b = (b + STEP_B) % Q
        H = hamiltonian(a, b)
        print(f"  k={k:3d}: a={a:2d}, b={b:2d},  H={H:.4f}")

    print(f"\nAfter {P} steps: a advances by {(STEP_A * P) % P} (mod {P}),"
          f" b advances by {(STEP_B * P) % Q} (mod {Q})")
    print(f"After {period_b} steps: a advances by {(STEP_A * period_b) % P} (mod {P}),"
          f" b advances by {(STEP_B * period_b) % Q} (mod {Q})")

    print(f"\nClassification:")
    print(f"  A. Free particle on torus: linear flow, fully integrable.")
    print(f"  B. Coupled oscillators: omega_1 = 2/37, omega_2 = 2/3.")
    print(f"  C. One mode frozen: Z_81 confined to sublattice of size {sub_b}.")
    print(f"  Full ergodicity requires gcd(step, dim) = 1.")
    print(f"  For Z_81: need step coprime to 81, e.g. step=1 -> period = lcm(37,81) = {lcm(P,Q)}.")

    return {
        "period": combined,
        "period_a": period_a,
        "period_b": period_b,
        "accessible": accessible,
        "full_torus": FULL_TORUS,
        "coverage": accessible / FULL_TORUS,
    }


if __name__ == "__main__":
    run()
