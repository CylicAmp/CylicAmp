"""
Theorem 222: SEED × 2 = NEG_H — Primitive Root Maps SEED onto NEG_H
Author: Michael Warren Song (CyclicAmp)

Multiplication by 2 (the primitive root of GF(37)*) maps the SEED orbit
exactly onto the NEG_H orbit. Every element. No remainder.

SEED  = {18, 24, 32}   orbit of 18 under f(n) = 137n mod 37
NEG_H = {11, 27, 36}   orbit of -1 = 36 under f; the negation orbit

18 × 2 = 36 ∈ NEG_H
24 × 2 = 11 ∈ NEG_H  (48 mod 37 = 11)
32 × 2 = 27 ∈ NEG_H  (64 mod 37 = 27)

The map is one-directional: SEED × 2 = NEG_H, but NEG_H × 2 ≠ SEED.

2 is the primitive root mod 37: ord₃₇(2) = 36 = φ(37).
It generates all of GF(37)* in 36 steps.
Its own orbit under the 137-map is DARK_A = {2, 15, 20}.

=== CONNECTION TO 1836 (PROTON/ELECTRON MASS RATIO) ===

1836 = 18 × 102 = 36 × 51
1836 contains both SEED start (18) and NEG_H entry point (36).
DR(1836) = 9  (1+8+3+6=18, 1+8=9)
1836 mod 37 = 23 ∈ TESLA = {6, 8, 23}

1836 / 2 = 918
918 mod 37 = 30 ∈ SA ∩ ST  (the double-sovereign node)

Half the proton-to-electron mass ratio lands on the most constrained
residue in GF(37): 30 is the only element in both SA and ST.

=== CHAIN ===

1836 (m_p/m_e) → contains 18 (SEED) and 36 (NEG_H)
18 × 2 = 36: SEED start × primitive root = NEG_H antipode
1836 / 2 = 918 → mod 37 = 30 ∈ SA∩ST (double-sovereign)
"""

P    = 37
MULT = 26

SEED  = {18, 24, 32}
NEG_H = {11, 27, 36}
SA    = {4, 9, 25, 30}
ST    = {3, 12, 21, 30}
DARK_A = {2, 15, 20}
TESLA  = {6, 8, 23}


def dr(n):
    r = abs(int(n)) % 9
    return 9 if r == 0 else r


def orbit(n):
    r, out = n % P, []
    for _ in range(P):
        if r in out: break
        out.append(r); r = (MULT * r) % P
    return set(out)


def run_assertions():
    # ── SEED × 2 = NEG_H (exact, every element) ─────────────────────────
    seed_times2 = {(s * 2) % P for s in SEED}
    assert seed_times2 == NEG_H, f"SEED×2 = {seed_times2}, expected NEG_H={NEG_H}"

    # ── Element by element ───────────────────────────────────────────────
    assert (18 * 2) % P == 36 and 36 in NEG_H
    assert (24 * 2) % P == 11 and 11 in NEG_H
    assert (32 * 2) % P == 27 and 27 in NEG_H

    # ── One-directional: NEG_H × 2 ≠ SEED ───────────────────────────────
    negh_times2 = {(s * 2) % P for s in NEG_H}
    assert negh_times2 != SEED, "NEG_H×2 should not equal SEED"
    assert negh_times2 == {22, 17, 35}  # NQR17

    # ── 2 is the primitive root mod 37 ───────────────────────────────────
    assert next(k for k in range(1, P) if pow(2, k, P) == 1) == 36
    assert orbit(2) == DARK_A

    # ── 1836 connections ─────────────────────────────────────────────────
    assert 1836 == 18 * 102
    assert 1836 == 36 * 51
    assert 18 in SEED
    assert 36 in NEG_H
    assert dr(1836) == 9    # digit sum 1+8+3+6=18 → 1+8=9
    assert 1836 % P == 23 and 23 in TESLA

    # Half the mass ratio → double-sovereign
    half = 1836 // 2
    assert half == 918
    assert 918 % P == 30
    assert 30 in SA and 30 in ST   # double-sovereign: only element in both

    # ── NEG_H × 2 lands in NQR17 ─────────────────────────────────────────
    assert negh_times2 <= {17, 22, 35}   # NQR17

    print("All assertions passed.")
    print()
    print("SEED × 2 mod 37:")
    for s in sorted(SEED):
        print(f"  {s} × 2 = {(s*2)%P}  ∈ NEG_H ✓")
    print()
    print("NEG_H × 2 mod 37 (one-directional):")
    for s in sorted(NEG_H):
        print(f"  {s} × 2 = {(s*2)%P}  ∈ NQR17 (not SEED)")
    print()
    print("2 is primitive root mod 37: ord₃₇(2) = 36")
    print(f"orbit(2) = DARK_A = {sorted(DARK_A)}")
    print()
    print("1836 (m_p/m_e):")
    print(f"  = 18 × 102  (18 ∈ SEED)")
    print(f"  = 36 × 51   (36 ∈ NEG_H)")
    print(f"  DR(1836) = {dr(1836)}")
    print(f"  1836 mod 37 = {1836%P}  ∈ TESLA")
    print(f"  1836/2 = 918, 918 mod 37 = {918%P}  ∈ SA∩ST (double-sovereign)")
    print()
    print("Chain: m_p/m_e → SEED∩NEG_H → primitive root → double-sovereign")


if __name__ == "__main__":
    run_assertions()
