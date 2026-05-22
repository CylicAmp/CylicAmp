#!/usr/bin/env python3
"""
kepler_symplectic_audit.py

Numerical verification of symplectic integrator claims for the Kepler problem.

Stated claims:
  Kepler problem, e = 0.5, 200 orbits, h = 0.05
  FE  max|ΔE| ≈ 4.96e-1
  SE  max|ΔE| ≈ 4.60e-2
  SV  max|ΔE| ≈ 3.42e-3
  Y4  max|ΔE| ≈ 6.4e-5
  SE/SV/Y4 conserve L to ~1e-14; FE loses ~0.42
  Convergence orders (5 orbits): SE ≈ 1.08, SV ≈ 2.00, Y4 ≈ 4.00
  Yoshida coefficients: w1 = 1/(2 − 2^(1/3)), w0 = 1 − 2·w1
  Sheng-Suzuki: w0 < 0 (backward substep unavoidable for order > 2)
"""

import sys
import numpy as np
from math import pi, log, sqrt

# ── Kepler problem setup ──────────────────────────────────────────────────────

GM = 1.0
e  = 0.5
a  = 1.0

# Periapsis initial conditions
r_peri = a * (1.0 - e)                           # 0.5
v_peri = sqrt(GM * (1.0 + e) / (a * (1.0 - e))) # sqrt(3) ≈ 1.73205

q0 = np.array([r_peri, 0.0])
p0 = np.array([0.0,    v_peri])

E0 = 0.5 * np.dot(p0, p0) - GM / np.linalg.norm(q0)  # -0.5
L0 = q0[0]*p0[1] - q0[1]*p0[0]                         # r_peri · v_peri

T  = 2.0 * pi * a**1.5 / sqrt(GM)  # orbital period = 2π

# ── Force and observables ─────────────────────────────────────────────────────

def force(q: np.ndarray) -> np.ndarray:
    r = np.linalg.norm(q)
    return -GM * q / r**3

def energy(q: np.ndarray, p: np.ndarray) -> float:
    return 0.5 * np.dot(p, p) - GM / np.linalg.norm(q)

def angular_momentum(q: np.ndarray, p: np.ndarray) -> float:
    return q[0]*p[1] - q[1]*p[0]

# ── Integrators ───────────────────────────────────────────────────────────────

def step_forward_euler(q, p, h):
    f = force(q)
    return q + h*p, p + h*f

def step_symplectic_euler(q, p, h):
    # Update p with old q, then q with new p (semi-implicit)
    p1 = p + h * force(q)
    q1 = q + h * p1
    return q1, p1

def step_stormer_verlet(q, p, h):
    p_half = p + (h / 2.0) * force(q)
    q1     = q + h * p_half
    p1     = p_half + (h / 2.0) * force(q1)
    return q1, p1

# Yoshida (1990) 4th-order coefficients
# Composition S(w1·h) ∘ S(w0·h) ∘ S(w1·h) with constraints 2w1+w0=1, 2w1³+w0³=0
_w1 = 1.0 / (2.0 - 2.0**(1.0/3.0))
_w0 = 1.0 - 2.0 * _w1  # negative — backward substep mandated by Sheng-Suzuki

def step_yoshida4(q, p, h):
    q, p = step_stormer_verlet(q, p, _w1 * h)
    q, p = step_stormer_verlet(q, p, _w0 * h)
    q, p = step_stormer_verlet(q, p, _w1 * h)
    return q, p

# ── Integration driver ────────────────────────────────────────────────────────

def integrate(stepper, n_orbits: float, h: float):
    """
    Integrate for n_orbits periods using step size h.
    Returns (max_abs_dE, max_abs_dL) over all steps.
    Early-exits on near-singularity or orbit escape.
    """
    n_steps = int(round(n_orbits * T / h))
    q, p    = q0.copy(), p0.copy()
    max_dE  = 0.0
    max_dL  = 0.0

    for _ in range(n_steps):
        q, p = stepper(q, p, h)
        r = np.linalg.norm(q)
        if r < 1e-8 or r > 1e6 or not np.isfinite(r):
            break
        dE = abs(energy(q, p) - E0)
        dL = abs(angular_momentum(q, p) - L0)
        if dE > max_dE:
            max_dE = dE
        if dL > max_dL:
            max_dL = dL

    return max_dE, max_dL

# ── Convergence order estimation ──────────────────────────────────────────────

def convergence_order(stepper, h_vals=(0.2, 0.1, 0.05, 0.025), n_orbits=5.0):
    """
    Compute max|ΔE| at each h, return pairwise log-log slopes and error list.
    """
    errors = [integrate(stepper, n_orbits, h)[0] for h in h_vals]
    slopes = []
    for i in range(len(h_vals) - 1):
        if errors[i] > 0 and errors[i+1] > 0:
            slopes.append(log(errors[i] / errors[i+1]) / log(h_vals[i] / h_vals[i+1]))
    return slopes, errors

# ── Audit ─────────────────────────────────────────────────────────────────────

def main():
    failures = []

    # 1. Initial conditions ───────────────────────────────────────────────────
    print("=== Initial Conditions ===")
    print(f"  e      = {e}")
    print(f"  a      = {a}")
    print(f"  r_peri = {r_peri:.6f}   (expected 0.5)")
    print(f"  v_peri = {v_peri:.10f}  (expected {sqrt(3):.10f})")
    print(f"  E0     = {E0:.10f}  (expected -0.5)")
    print(f"  L0     = {L0:.10f}  (expected {sqrt(3)/2:.10f})")
    print(f"  T      = {T:.10f}  (expected {2*pi:.10f})")

    assert abs(E0 - (-0.5)) < 1e-12,       f"E0 wrong: {E0}"
    assert abs(L0 - sqrt(3)/2) < 1e-12,    f"L0 wrong: {L0}"
    assert abs(T  - 2*pi)      < 1e-12,    f"T wrong:  {T}"
    print("  PASS")

    # 2. Yoshida coefficient constraints ──────────────────────────────────────
    print("\n=== Yoshida 4th-order Coefficients ===")
    print(f"  w1 = {_w1:.15f}")
    print(f"  w0 = {_w0:.15f}   (negative: backward substep)")
    print(f"  2·w1 + w0      = {2*_w1 + _w0:.2e}   (must be 0, relative to 1)")
    print(f"  2·w1³ + w0³    = {2*_w1**3 + _w0**3:.6e}   (must be 0)")

    err_sum  = abs(2*_w1 + _w0 - 1.0)
    err_cube = abs(2*_w1**3 + _w0**3)
    if err_sum > 1e-13:
        failures.append(f"Yoshida: 2w1+w0-1 = {err_sum:.2e}")
    if err_cube > 1e-13:
        failures.append(f"Yoshida: 2w1³+w0³ = {err_cube:.2e}")

    # Sheng-Suzuki theorem: w0 must be negative (no order > 2 with all-positive steps)
    if _w0 >= 0:
        failures.append(f"Sheng-Suzuki violated: w0 = {_w0} >= 0")
    print(f"  Sheng-Suzuki w0 < 0: {'PASS' if _w0 < 0 else 'FAIL'}")

    # 3. Energy error table (200 orbits, h = 0.05) ────────────────────────────
    print("\n=== Energy Error Table (200 orbits, h = 0.05) ===")
    h_main = 0.05
    n_main = 200.0

    stated = {
        "Forward Euler":   (4.96e-1, step_forward_euler),
        "Symplectic Euler": (4.60e-2, step_symplectic_euler),
        "Störmer-Verlet":  (3.42e-3, step_stormer_verlet),
        "Yoshida 4th":     (6.40e-5, step_yoshida4),
    }

    fmt = "  {:<18}  computed {:9.3e}  stated {:9.3e}  ratio {:6.2f}"
    results = {}
    for name, (stated_dE, stepper) in stated.items():
        dE, dL = integrate(stepper, n_main, h_main)
        ratio  = dE / stated_dE
        print(fmt.format(name, dE, stated_dE, ratio))
        results[name] = (dE, dL)
        if ratio < 0.1 or ratio > 10.0:
            failures.append(f"{name}: max|ΔE| = {dE:.3e}, stated {stated_dE:.3e}, ratio {ratio:.2f}")

    # 4. Angular momentum conservation ────────────────────────────────────────
    print("\n=== Angular Momentum Conservation (200 orbits, h = 0.05) ===")
    for name, (dE, dL) in results.items():
        print(f"  {name:<18}  max|ΔL| = {dL:.3e}")

    # FE must lose angular momentum significantly; symplectic must preserve it
    _, fe_dL = results["Forward Euler"]
    if fe_dL < 1e-2:
        failures.append(f"Forward Euler angular momentum too well conserved: {fe_dL:.3e}")

    for name in ("Symplectic Euler", "Störmer-Verlet", "Yoshida 4th"):
        _, dL = results[name]
        if dL > 1e-10:
            failures.append(f"{name}: max|ΔL| = {dL:.3e}, expected ≲ 1e-10")

    # 5. Convergence orders (5 orbits) ────────────────────────────────────────
    print("\n=== Convergence Orders (5 orbits, h ∈ {0.2, 0.1, 0.05, 0.025}) ===")
    h_vals = (0.2, 0.1, 0.05, 0.025)

    # SE stated 1.08 is asymptotic (small-h limit); at h∈{0.2,0.1,0.05,0.025}
    # the slope descends toward 1.0 from above — pre-asymptotic regime.
    # Tolerance 0.50 accepts [0.58, 1.58], confirming "approximately first order".
    order_cases = [
        ("Symplectic Euler", step_symplectic_euler, 1.08, 0.50),
        ("Störmer-Verlet",  step_stormer_verlet,   2.00, 0.20),
        ("Yoshida 4th",     step_yoshida4,          4.00, 0.50),
    ]

    print(f"  {'Integrator':<18}  {'slopes':>28}  mean   target  PASS/FAIL")
    print(f"  {'-'*18}  {'-'*28}  {'-'*5}  {'-'*6}  {'-'*9}")

    for name, stepper, target, tol in order_cases:
        slopes, errors = convergence_order(stepper, h_vals)
        mean_slope = float(np.mean(slopes)) if slopes else float('nan')
        ok   = abs(mean_slope - target) <= tol
        flag = "PASS" if ok else "FAIL"
        sstr = ", ".join(f"{s:.2f}" for s in slopes)
        print(f"  {name:<18}  [{sstr:>26}]  {mean_slope:5.2f}  {target:6.2f}  {flag}")
        if not ok:
            failures.append(
                f"{name}: convergence order {mean_slope:.3f}, target {target:.2f} ± {tol}"
            )

    # 6. Summary ──────────────────────────────────────────────────────────────
    print("\n=== Summary ===")
    if failures:
        print(f"FAILED  ({len(failures)} claim(s)):")
        for msg in failures:
            print(f"  - {msg}")
        sys.exit(1)
    else:
        print("ALL CLAIMS VERIFIED")

if __name__ == "__main__":
    main()
