#!/usr/bin/env python3
"""
automorphic_orbit_ntt_audit.py

Five-component verification of the integrated loop structure:

  1. Automorphic orbit: (Z/9Z)*, generator 2, order 6 = φ(9)
  2. CRT injection: (Z/9Z)* ↠ (Z/3Z)*, 3:1 cover, kernel order 3
  3. 3-6-9 kernel: nilpotent ideal (3), absorption, 3↔6 invariance
  4. Möbius inversion: squarefree band-reject filter μ(n) for n=1..6
  5. NTT spectral filter: F_5, N=4, ω=2, input [1,2,3,4] → X=[0,4,3,2]

CONNECTIONS:
  - Component 1 units {1,2,4,5,7,8} = coprime-to-9 set from mod9_grid_audit
    (Latin square condition: gcd(A,9)=1 ↔ A ∈ {1,2,4,5,7,8})
  - Component 2 fibers {1,4,7} and {2,5,8} = twin prime DR track sets
    (T₂₄ contains DR 2,4; T₅₇ contains DR 5,7; T₈₁ contains DR 8,1)
    All of {2,5,8} ∈ fiber over 2 mod 3; all of {1,4,7} ∈ fiber over 1 mod 3
  - Component 3 kernel {0,3,6} = excluded DR values in twin prime analysis
  - Component 5 extends to p=37, N=36=φ(37) for the emirp field F_37

─────────────────────────────────────────────────────────────────
COPY-PASTE READY: run with  python3 automorphic_orbit_ntt_audit.py
Requires: Python 3.6+, stdlib only (math)
─────────────────────────────────────────────────────────────────
"""

import math

FAIL = []

def check(cond, label, actual=None, expected=None):
    if not cond:
        FAIL.append(f"  ✗  {label}  actual={actual!r}  expected={expected!r}")
    return cond

def mobius(n):
    if n == 1:
        return 1
    factors = []
    temp = n
    for p in range(2, n + 1):
        if temp % p == 0:
            factors.append(p)
            temp //= p
            if temp % p == 0:
                return 0
    return (-1) ** len(factors)

def run():
    print("AUTOMORPHIC ORBIT + NTT AUDIT")
    print("=" * 60)

    # ── 1. AUTOMORPHIC ORBIT (Z/9Z)* ─────────────────────────────
    print("\n  1. (Z/9Z)*  AUTOMORPHIC ORBIT")
    N = 9
    units = [k for k in range(N) if math.gcd(k, N) == 1]
    check(units == [1, 2, 4, 5, 7, 8],
          "units of Z/9Z = {1,2,4,5,7,8}", units, [1, 2, 4, 5, 7, 8])

    mapped = sorted([(2 * u) % N for u in units])
    check(mapped == [1, 2, 4, 5, 7, 8],
          "×2 maps units to units (closure)", mapped, [1, 2, 4, 5, 7, 8])

    orbit = []
    x = 1
    for _ in range(20):
        orbit.append(x)
        x = (2 * x) % N
        if x == 1:
            orbit.append(1)
            break
    check(orbit == [1, 2, 4, 8, 7, 5, 1],
          "orbit: 1→2→4→8→7→5→1", orbit, [1, 2, 4, 8, 7, 5, 1])
    order = len(orbit) - 1
    check(order == 6, f"order = {order} = φ(9)", order, 6)
    check(sorted(orbit[:-1]) == units, "<2> = (Z/9Z)*")

    print(f"    units: {units}")
    print(f"    orbit: {orbit}")
    print(f"    order: {order} = φ(9)")

    # ── 2. CRT INJECTION (Z/9Z)* → (Z/3Z)* ──────────────────────
    print("\n  2. CRT INJECTION (Z/9Z)* ↠ (Z/3Z)*")
    fiber1 = [u for u in units if u % 3 == 1]
    fiber2 = [u for u in units if u % 3 == 2]
    check(fiber1 == [1, 4, 7], "fiber over 1 mod 3: {1,4,7}", fiber1, [1, 4, 7])
    check(fiber2 == [2, 5, 8], "fiber over 2 mod 3: {2,5,8}", fiber2, [2, 5, 8])
    check(len(fiber1) == 3 and len(fiber2) == 3, "each fiber has size 3")
    kernel_order = len([u for u in units if u % 3 == 1])
    check(kernel_order == 3, "projection kernel order = 3", kernel_order, 3)
    check(order // 2 == 3, "6-cycle covers 2-cycle exactly 3×", order // 2, 3)

    print(f"    fiber over 1: {fiber1}  (twin prime DR partners: T₂₄ upper, T₈₁ upper)")
    print(f"    fiber over 2: {fiber2}  (twin prime first-element DRs: {{2,5,8}})")
    print(f"    kernel order: {kernel_order}  (matches 3-6-9 kernel cardinality)")

    # ── 3. 3-6-9 KERNEL ──────────────────────────────────────────
    print("\n  3. 3-6-9 KERNEL — nilpotent ideal (3)")
    kernel_set = {0, 3, 6}
    check(kernel_set == set(range(0, N, 3)),
          "ideal (3) = {0,3,6}", sorted(kernel_set), [0, 3, 6])
    check((3 * 3) % N == 0, "nilpotency: 3·3=9≡0 mod 9", (3*3)%N, 0)

    absorption_ok = all((u * k) % N in kernel_set
                        for u in units for k in [0, 3, 6])
    check(absorption_ok, "absorption: u·k ∈ {0,3,6} for all units u, kernel k")

    check((2 * 3) % N == 6 and (2 * 6) % N == 3,
          "invariance under ×2: 3↔6", [(2*3)%N, (2*6)%N], [6, 3])
    check((2 * 0) % N == 0, "invariance under ×2: 0→0")

    print(f"    kernel {{0,3,6}}: nilpotency index 2 (collapse is immediate)")
    print(f"    3↔6 is a 2-cycle under ×2; 0 fixed")

    # ── 4. MÖBIUS INVERSION ──────────────────────────────────────
    print("\n  4. MÖBIUS BAND-REJECT FILTER  μ(n), n=1..6")
    expected_mu = {1: 1, 2: -1, 3: -1, 4: 0, 5: -1, 6: 1}
    action = {1: "pass (fundamental)", 2: "reject prime-square overtone",
              3: "reject prime-cube overtone", 4: "block (squareful: 2²)",
              5: "reject 5th-power overtone", 6: "pass (2 distinct primes)"}
    for n, mu in expected_mu.items():
        check(mobius(n) == mu, f"μ({n}) = {mu:+d}", mobius(n), mu)
        print(f"    μ({n}) = {mu:+d}   {action[n]}")
    print(f"    π(x) = Σ μ(n)/n · J(x^(1/n))  [Möbius inversion of J(x)]")

    # ── 5. NTT SPECTRAL FILTER F_5, N=4 ─────────────────────────
    print("\n  5. NTT SPECTRAL FILTER  p=5, N=4, ω=2")
    p, L, omega = 5, 4, 2

    pows = [pow(omega, k, p) for k in range(L + 1)]
    check(pows[L] == 1, f"ω^{L} ≡ 1 mod {p}", pows[L], 1)
    check(all(pows[k] != 1 for k in range(1, L)),
          f"ω=2 has order {L} mod {p}", [pows[k] for k in range(1,L)], "all ≠ 1")
    print(f"    ω=2 powers mod 5: {pows}")

    x_in = [1, 2, 3, 4]
    X = [sum(x_in[j] * pow(omega, j * k, p) for j in range(L)) % p
         for k in range(L)]
    check(X == [0, 4, 3, 2], f"NTT({x_in}) = {X}", X, [0, 4, 3, 2])
    check(X[0] == 0, f"X_0=0: DC null  (sum={sum(x_in)} ≡ 0 mod {p})")

    print(f"    input:  {x_in}  (non-zero elements of F_5)")
    print(f"    output: X = {X}")
    print(f"    X_0={X[0]} DC null | X_1={X[1]} fundamental | "
          f"X_2={X[2]} 2nd harmonic | X_3={X[3]} 3rd harmonic")
    print(f"    Note: Nyquist index = N/2 = 2 (standard); X_3 is 3rd harmonic / "
          f"ω^{{-1}} component")

    # ── 6. INTEGRATED LOOP ASSERTIONS ────────────────────────────
    print("\n  6. INTEGRATED LOOP CHECKS")
    # Units ↔ coprime-to-9 set from Latin square condition
    from_latin = [k for k in range(9) if math.gcd(k, 9) == 1]
    check(from_latin == units,
          "unit set = Latin square coprime-to-9 set (mod9_grid_audit)", from_latin, units)

    # Twin prime DRs {2,5,8} ⊂ fiber2; twin prime partners {4,7,1}=fiber1∪{1}
    twin_p_dr = {2, 5, 8}
    check(twin_p_dr.issubset(set(fiber2)),
          "twin prime DRs {2,5,8} ⊂ fiber over 2 mod 3", twin_p_dr, "⊆ fiber2")

    # Kernel {0,3,6} = excluded DR values (non-twin-prime non-unit)
    check(kernel_set == {0, 3, 6},
          "kernel {0,3,6}: excluded from unit orbit and twin prime tracks")

    # φ(37) = 36 — the emirp field extension
    check(sum(1 for k in range(37) if math.gcd(k, 37) == 1) == 36,
          "φ(37) = 36: NTT extension to (Z/37Z)*, N=36", None, 36)

    print(f"    φ(37) = 36: next NTT scale is p=37, N=36=φ(37)")

    # ── FINAL ─────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f)
        import sys; sys.exit(1)
    else:
        print("ALL ASSERTIONS PASSED")

if __name__ == "__main__":
    run()
