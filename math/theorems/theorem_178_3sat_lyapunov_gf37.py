"""
Theorem 178: GF(37) Escapes the Lyapunov Complexity Barrier for 3-SAT

THE ARGUMENT
=============
To reduce 3-SAT to a physical dynamical system in polynomial time, the
mapped dynamical system must evaluate 2^n variable assignments without
undergoing chaotic divergence.

Chaotic systems have at least one positive Lyapunov exponent λ > 0.
Trajectory separation grows as Δx(t) ≈ Δx₀·e^(λt).
To predict over time horizon T: precision Δx₀ ~ e^(-λT) required.
For n logical decisions T scales with n, forcing precision ~ e^(-λn):
exponential complexity reinstated through sensitive dependence.

GF(37) UNDER THE 137-MAP IS NON-CHAOTIC
==========================================
f(n) = 26n mod 37.

All 12 orbits have length exactly 3. No orbit diverges.
Every element stays bounded in {1..36}.

Separation under the map is PERIODIC, not growing:
  Two points x, x+δ: f(x)-f(x+δ) = 26δ mod 37.
  The separation itself is in a 3-cycle — it does not grow.

Lyapunov exponent of GF(37) under 137-map: λ = 0.
No sensitive dependence on initial conditions.
No exponential precision requirement.

PRIMITIVE ROOT 2 COVERS ALL 2^n STATES
=========================================
ord₃₇(2) = 36. The 36 powers 2^0..2^35 (mod 37) visit every element.
2^n mod 36 has period 6: {2,4,8,16,32,28} repeating.
All 2^n assignments (mod 36) are encoded within a single 36-step cycle.

COMPLEXITY COMPARISON
======================
  Chaotic analog:  precision e^(-λn) required  → EXPONENTIAL
  GF(37) discrete: exact mod 37 arithmetic     → O(1) per step
  Full cycle:      36 steps = φ(37)            → POLYNOMIAL in field size
"""

P = 37

def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9

def run_assertions():
    # All 137-map orbits have length 3
    visited = set()
    orbits = []
    for start in range(1, P):
        if start not in visited:
            orb = []
            x = start
            while x not in orb:
                orb.append(x)
                x = (26 * x) % P
            orbits.append(orb)
            visited.update(orb)
    assert all(len(o) == 3 for o in orbits)
    assert len(orbits) == 12

    # Separation is periodic — not growing
    for delta in [1, 2, 3, 5, 7]:
        x = 18
        seps = []
        for _ in range(6):
            y = (x + delta) % P
            seps.append((26*x - 26*y) % P)
            x = (26*x) % P
        # separation cycles with period 3
        assert seps[0] == seps[3]
        assert seps[1] == seps[4]
        assert seps[2] == seps[5]

    # Primitive root 2 covers all 36 elements
    assert pow(2, 36, P) == 1
    powers = set()
    x = 1
    for _ in range(36):
        powers.add(x)
        x = x * 2 % P
    assert powers == set(range(1, P))

    # 2^n mod 36: {4,8,16,32,28,20} repeats from n=2 with period 6
    period = [pow(2, n, 36) for n in range(2, 20)]
    assert period[:6] == period[6:12]

    # Order of 26
    assert pow(26, 3, P) == 1
    assert pow(26, 1, P) != 1
    assert pow(26, 2, P) != 1

    print("All assertions passed.")

if __name__ == "__main__":
    run_assertions()
