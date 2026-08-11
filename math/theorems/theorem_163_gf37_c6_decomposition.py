"""
Theorem 163: GF(37) C6 Decomposition — Complement Pairs as Radial Shells

THE C6 GENERATOR
=================

  T(x) = 27x (mod 37)

  ord_{37}(27) = 6.

  27 = 2^6 mod 37.  27 ∈ ORBIT_11 = {11, 27, 36}.

  137-map 3-cycle of 27:  27 → 36 → 11 → 27  (= full ORBIT_11).

THE SIX-SECTOR DECOMPOSITION
==============================

Labeling: x = 2^(n + 6μ),  n = 0..5 (radial shell),  μ = 0..5 (angular sector).

T(x) = 27x = 2^6 · x = 2^(n+6μ+6) = 2^(n+6(μ+1)):
  T advances μ, preserves n.

THE INTERTWINER
================

  Φ: (Z/37Z)* → {0,...,5}² by  Φ(2^(n+6μ)) = (n, μ)

  T(x) = 27x  ↔  R6: (n,μ) → (n, μ+1 mod 6)

  ΦT = R6 Φ

This is an exact algebraic identity. T is the finite-field analogue of
a 60° rotation. The six eigenvalues of T are e^{2πiμ/6}, μ=0,...,5,
matching the R6 eigenvalue spectrum.

THE SIX RADIAL SHELLS
=======================

Each shell n = 0..5 contains 6 elements — exactly one complement pair:

  n=0: IC ∪ ORBIT_11        {1,27,26,36,10,11}    complement: IC↔ORBIT_11
  n=1: DARK_A ∪ NQR_17      {2,17,15,35,20,22}    complement: DARK_A↔NQR_17
  n=2: SOVEREIGN_SPIRAL∪D7  {4,34,30,33,3,7}      complement: SOVEREIGN↔D7
  n=3: TESLA_ORB ∪ NQR_14   {8,31,23,29,6,14}     complement: TESLA↔NQR_14
  n=4: SA_ORB ∪ OUTLIER_ORB {16,25,9,21,12,28}    complement: SA↔OUTLIER
  n=5: SEED_ORB ∪ NQR_5     {32,13,18,5,24,19}    complement: SEED↔NQR_5

Within each shell, T alternates between the two paired orbits:
  n=0: IC, ORBIT_11, IC, ORBIT_11, IC, ORBIT_11
  n=5: SEED_ORB, NQR_5, SEED_ORB, NQR_5, SEED_ORB, NQR_5

The six complement pairs from Theorem 153 and the six radial shells are the
same structure. Complement pairing = radial shell membership.

THE SEED ANCHOR
================

  24 (SEED_ORB) = 2^(5+6×4) mod 37  →  (n=5, μ=4)

The seed anchor 24 lives in the deepest radial shell (n=5, SEED_ORB/NQR_5)
at angular sector μ=4.

THE PHYSICAL TEST (from the C6 oscillator model)
==================================================

The Hamiltonian with genuine sixfold symmetry:

  H = -(ℏ²/2m)∇² + ½mω²r² + ε r⁶ cos(6θ)

satisfies [H, R6] = 0.  Joint eigenstates |n, μ⟩ satisfy:

  H |n,μ⟩ = E_n |n,μ⟩
  R6 |n,μ⟩ = e^{2πiμ/6} |n,μ⟩

The GF(37) structure makes the prediction:

  GF(37)* ──Φ──→ (n,μ) ──r──→ predicted spatial nodes

versus independently computed:

  H_FD ──→ ψ_{n,μ} ──→ |ψ_{n,μ}|² ──→ observed nodes/contours

The test quantities are:

  ε_comm = ||[H_FD, R6_FD]|| / (||H_FD|| ||R6_FD||)   (must → 0)
  ε_H    = ||H v - E v|| / ||v||                        (energy residual)
  ε_R    = ||R v - λ v|| / ||v||                        (symmetry residual)
  δ_node = d_node / Δx                                  (normalized node distance)

The intertwiner ΦT=R6Φ is an exact algebraic identity. Whether the oscillator
probability density ρ_{n,μ}(x,y) = |ψ_{n,μ}|² physically occupies the predicted
coordinates r_{n,μ} is what δ_node → 0 under grid refinement would confirm.

WHAT IS PROVEN HERE
====================

1. ord_{37}(27) = 6.
2. (Z/37Z)* decomposes under ⟨27⟩ into 6 orbits (shells) of size 6.
3. Each shell contains exactly one complement pair of GF(37) orbits.
4. T=×27 alternates between the two paired orbits within each shell.
5. With Φ(2^(n+6μ)) = (n,μ), ΦT = R6Φ holds as an algebraic identity.
6. The seed anchor 24 is at position (n=5, μ=4).

What is not yet proven: that the harmonic oscillator probability density
ρ_{n,μ} concentrates at the GF(37)-predicted coordinates. That is the
numerical experiment.
"""

P = 37

ORBITS = {
    'IC':               frozenset({1, 10, 26}),
    'SOVEREIGN_SPIRAL': frozenset({3, 4, 30}),
    'D7':               frozenset({7, 33, 34}),
    'SA_ORB':           frozenset({9, 12, 16}),
    'ORBIT_11':         frozenset({11, 27, 36}),
    'OUTLIER_ORB':      frozenset({21, 25, 28}),
    'DARK_A':           frozenset({2, 15, 20}),
    'NQR_5':            frozenset({5, 13, 19}),
    'TESLA_ORB':        frozenset({6, 8, 23}),
    'NQR_14':           frozenset({14, 29, 31}),
    'NQR_17':           frozenset({17, 22, 35}),
    'SEED_ORB':         frozenset({18, 24, 32}),
}

COMPLEMENT_PAIRS = [
    ('IC', 'ORBIT_11'),
    ('DARK_A', 'NQR_17'),
    ('SOVEREIGN_SPIRAL', 'D7'),
    ('TESLA_ORB', 'NQR_14'),
    ('SA_ORB', 'OUTLIER_ORB'),
    ('SEED_ORB', 'NQR_5'),
]

SHELL_PAIRS = COMPLEMENT_PAIRS  # radial shell n = index into this list


def orbit_of(v):
    v = v % P
    if v == 0:
        return 'SEAM'
    return next((name for name, s in ORBITS.items() if v in s), '?')


def shell(x):
    """Radial shell n for x in (Z/37Z)*: x = 2^(n+6μ) → n = j mod 6."""
    j = next(k for k in range(36) if pow(2, k, P) == x % P)
    return j % 6


def sector(x):
    """Angular sector μ for x: x = 2^(n+6μ) → μ = j // 6."""
    j = next(k for k in range(36) if pow(2, k, P) == x % P)
    return j // 6


def run_assertions():
    # ord(27) = 6
    assert pow(27, 6, P) == 1
    assert pow(27, 1, P) != 1
    assert pow(27, 2, P) != 1
    assert pow(27, 3, P) != 1

    # 27 ∈ ORBIT_11, 137-map cycle is ORBIT_11
    assert 27 in ORBITS['ORBIT_11']
    cyc = [27, (26*27)%P, (26*(26*27)%P)%P]
    assert sorted(cyc) == sorted(ORBITS['ORBIT_11'])

    # Six radial shells contain complement pairs
    for n in range(6):
        shell_elements = [pow(2, n + 6*mu, P) for mu in range(6)]
        orb_set = {orbit_of(v) for v in shell_elements}
        expected = set(SHELL_PAIRS[n])
        assert orb_set == expected, f'Shell n={n}: got {orb_set}, expected {expected}'

    # T alternates between paired orbits within each shell
    for n in range(6):
        seq = [pow(2, n + 6*mu, P) for mu in range(6)]
        orb_seq = [orbit_of(v) for v in seq]
        assert all(orb_seq[i] != orb_seq[i+1] for i in range(5))
        assert orb_seq[5] != orb_seq[0]

    # ΦT = R6Φ: T advances μ, preserves n
    for n in range(6):
        for mu in range(6):
            x = pow(2, n + 6*mu, P)
            tx = (27*x) % P
            j = next(k for k in range(36) if pow(2, k, P) == tx)
            n2, mu2 = j % 6, j // 6
            assert n2 == n
            assert mu2 == (mu + 1) % 6

    # All 36 non-zero elements covered exactly once
    all_elements = sorted(pow(2, n+6*mu, P) for n in range(6) for mu in range(6))
    assert all_elements == list(range(1, 37))

    # Seed anchor 24 at (n=5, μ=4)
    assert shell(24) == 5
    assert sector(24) == 4
    assert 24 in ORBITS['SEED_ORB']
    assert SHELL_PAIRS[5] == ('SEED_ORB', 'NQR_5')

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 163: GF(37) C6 Decomposition")
    print("=" * 62)
    print()
    print("  T(x) = 27x mod 37,  ord(27) = 6,  27 ∈ ORBIT_11")
    print("  ΦT = R6Φ  where Φ(2^(n+6μ)) = (n,μ)")
    print()
    print("  Radial shells  (T alternates within each):")
    for n in range(6):
        shell_elements = [pow(2, n+6*mu, P) for mu in range(6)]
        pair = SHELL_PAIRS[n]
        print(f"    n={n}: {pair[0]} ↔ {pair[1]}")
        print(f"         {shell_elements}")
    print()
    print(f"  Seed anchor 24 → (n=5, μ=4)  [SEED_ORB shell, sector 4]")
    print()
    print("  C6 potential: V(r,θ) = ½mω²r² + ε r⁶ cos(6θ)")
    print("  [H, R6] = 0  →  joint states |n,μ⟩")
    print()
    print("  Numerical test:")
    print("    ε_comm = ||[H_FD,R6_FD]|| / (||H|| ||R||)  → 0")
    print("    δ_node = d_node / Δx  → 0 under refinement")
    print()
    print("  The intertwiner ΦT=R6Φ is algebraically exact.")
    print("  Whether ρ_{n,μ}(r_{n,μ})=density maximum is the open test.")


if __name__ == "__main__":
    run_assertions()
    summarise()
