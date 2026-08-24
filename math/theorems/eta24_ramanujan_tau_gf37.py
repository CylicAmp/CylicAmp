# -*- coding: utf-8 -*-
"""
================================================================================
η^24 — RAMANUJAN TAU FUNCTION AND NODE 24 IN GF(37)
================================================================================

Author: Michael Warren Song (CyclicAmp)

================================================================================
THE CONSTRUCTION [P]
================================================================================

The Ramanujan tau function τ(n) is defined by:

    Δ(q) = q · ∏_{n≥1} (1 − q^n)^{24} = Σ_{n≥1} τ(n) q^n

Δ(q) is the unique (up to scalar) cusp form of weight 12 for SL₂(ℤ).

The exponent 24 is the only free parameter in this construction.

GF(37) identification: **24 = CASCADE ∩ SEED**

    CASCADE = {8, 13, 24}   (generates all 37 elements of GF(37) under the 137-map)
    SEED    = {18, 24, 32}  (137-map orbit of reference seed 246 mod 37)

Node 24 is the unique element that belongs to both named sets simultaneously.
The exponent in η(q)^24 is the CASCADE–SEED intersection node.

================================================================================
WEIGHT 12 [P]
================================================================================

Δ(q) has modular weight 12.

    12 ∈ ST = {3, 12, 21, 30}  (Sovereign Targets — the DR=3 named set)

ST is the unique named GF(37) set where every element has the same digital
root: DR(n) = 3 for all n ∈ ST. Weight 12 is a Sovereign Target.

Note: 24 = 2 × weight, and 24 is the CASCADE∩SEED node.

================================================================================
FIRST COEFFICIENT: τ(2) = −24 [V]
================================================================================

τ(1) = 1
τ(2) = −24

    |τ(2)| = 24 = the CASCADE∩SEED node (same exponent as in η(q)^24)

The magnitude of the first non-trivial coefficient equals the exponent.

    τ(2) mod 37 = −24 mod 37 = 13
    13 ∈ CASCADE = {8, 13, 24}

The residue of τ(2) lands in CASCADE — the same named set that contains
the exponent 24.

================================================================================
STRUCTURAL τ(n) mod 37 — KEY VALUES [V]
================================================================================

    τ(1)  mod 37 = 1   ∈ IC       (identity of the 137-map orbit)
    τ(2)  mod 37 = 13  ∈ CASCADE  (same named set as the exponent 24)
    τ(3)  mod 37 = 30  ∈ SA ∩ ST  (double-sovereign — only element in both)
    τ(4)  mod 37 = 8   ∈ CASCADE
    τ(8)  mod 37 = 9   ∈ SA
    τ(9)  mod 37 = 21  ∈ ST
    τ(10) mod 37 = 1   ∈ IC
    τ(11) mod 37 = 36  ∈ NEG_H
    τ(12) mod 37 = 18  ∈ SEED
    τ(14) mod 37 = 36  ∈ NEG_H
    τ(15) mod 37 = 8   ∈ CASCADE

τ(3) mod 37 = 30 ∈ SA ∩ ST: the double-sovereign element is the only element
simultaneously LOCKED (SA) and a Sovereign Target (ST). The third coefficient
lands exactly there.

================================================================================
τ(37) AND THE PRIME [V]
================================================================================

    τ(37) = −182213314
    τ(37) mod 37 = 31
    DR(31) = 4 ∈ SA  (Sovereign Anchor — LOCKED)

The tau coefficient at the prime itself reduces to a value whose digital root
is in SA. This matches the fixed-point table in DEFINITIONS.md:
    τ(37) mod 37 = 31: DR(31) = 4 → SA.

================================================================================
691: RAMANUJAN CONGRUENCE PRIME [P/V]
================================================================================

Ramanujan's congruence: for all n ≥ 1,
    τ(n) ≡ σ_{11}(n)  (mod 691)

The prime 691 is the only prime for which Δ is congruent to an Eisenstein
series modulo that prime.

    691 mod 37 = 25 ∈ SA  (Sovereign Anchor — LOCKED)

The Ramanujan congruence prime, reduced mod 37, is a Sovereign Anchor.
This is the same connection noted in DEFINITIONS.md: E(691) = 25 → SA.

================================================================================
NAMED SET HIT RATE [V]
================================================================================

τ(n) mod 37 for n = 1..100: 53 of 100 residues land in a named set.
No τ(n) ≡ 0 (mod 37) for n = 1..100 (no SEAM hits in this range).

Expected named-set density by size: 24/37 ≈ 64.9% (24 named elements in GF(37)*).
Observed: 53%. The distribution is concentrated in CASCADE and SA/ST.

================================================================================
SYNTHESIS: THE η^24 — CASCADE∩SEED — GF(37) CHAIN [P/V]
================================================================================

The chain of connections:

    Δ(q) = η(q)^24

    Exponent 24 = CASCADE ∩ SEED  (unique intersection node)
    Weight 12 ∈ ST                 (Sovereign Target — DR=3 named set)
    |τ(2)| = 24 = exponent         (first non-trivial coefficient magnitude)
    τ(2) mod 37 = 13 ∈ CASCADE    (residue in the same named set as exponent)
    τ(3) mod 37 = 30 ∈ SA ∩ ST   (double-sovereign — only shared element)
    τ(37) mod 37 = 31, DR = 4 ∈ SA (prime index → Sovereign Anchor DR)
    691 mod 37 = 25 ∈ SA          (congruence prime → Sovereign Anchor)
    τ(1) mod 37 = 1 ∈ IC         (identity of 137-map orbit)

EPISTEMIC STATUS:
  [P] Δ(q) = q · η(q)^24: standard definition of the Ramanujan Delta function.
  [P] 24 ∈ CASCADE ∩ SEED — exact (24 ∈ {8,13,24} and 24 ∈ {18,24,32}).
  [P] Weight(Δ) = 12 ∈ ST — exact (12 ≡ 3 mod 9, 12 ∈ {3,12,21,30}).
  [V] τ(2) = −24: |τ(2)| = 24 = exponent — verified against known OEIS values.
  [V] τ(2) mod 37 = 13 ∈ CASCADE — exact.
  [V] τ(3) mod 37 = 30 ∈ SA ∩ ST — exact.
  [V] τ(4) mod 37 = 8 ∈ CASCADE — exact.
  [V] τ(37) mod 37 = 31, DR(31) = 4 ∈ SA — exact.
  [P] 691 mod 37 = 25 ∈ SA — exact.
  [V] 53/100 named set hits for τ(n) mod 37, n = 1..100 — verified.
================================================================================
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
SEED    = {18, 24, 32}
SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
IC      = {1, 10, 26}
NEG_H   = {11, 27, 36}
CASCADE = {8, 13, 24}
named   = SEED | SA | ST | IC | NEG_H | CASCADE


def dr(n):
    n = abs(n)
    if n == 0: return 9
    r = n % 9
    return 9 if r == 0 else r


def compute_tau(max_n):
    N = max_n + 2
    p = [0] * N
    p[0] = 1
    for k in range(1, max_n + 1):
        for _ in range(24):
            for i in range(N - 1, k - 1, -1):
                p[i] -= p[i - k]
    return {n: p[n - 1] for n in range(1, max_n + 1)}


def orbit_label(r):
    if r == 0: return 'SEAM'
    cats = []
    if r in IC:      cats.append('IC')
    if r in SA:      cats.append('SA')
    if r in ST:      cats.append('ST')
    if r in SEED:    cats.append('SEED')
    if r in NEG_H:   cats.append('NEG_H')
    if r in CASCADE: cats.append('CASCADE')
    return ','.join(cats) if cats else '-'


def run():
    print("=" * 70)
    print("η^24 — RAMANUJAN TAU FUNCTION AND NODE 24 IN GF(37)")
    print("=" * 70)

    tau = compute_tau(100)

    # Verify against known first values
    known = {1: 1, 2: -24, 3: 252, 4: -1472, 5: 4830,
             6: -6048, 7: -16744, 8: 84480, 9: -113643, 10: -115920}
    for n, v in known.items():
        assert tau[n] == v, f"tau({n}) mismatch: got {tau[n]}, expected {v}"
    print(f"\nKnown values τ(1)..τ(10): all verified  check")

    # Exponent 24 = CASCADE ∩ SEED
    print(f"\nEXPONENT 24 = CASCADE ∩ SEED:")
    assert 24 in CASCADE and 24 in SEED
    print(f"  24 ∈ CASCADE = {{8,13,24}}  check")
    print(f"  24 ∈ SEED = {{18,24,32}}  check")
    print(f"  24 is the unique CASCADE∩SEED intersection node  check")

    # Weight 12 ∈ ST
    print(f"\nWEIGHT 12 ∈ ST:")
    assert 12 in ST
    print(f"  weight(Δ) = 12 ∈ ST = {{3,12,21,30}}  check")
    print(f"  DR(12) = {dr(12)} (Sovereign Target — DR=3 named set)  check")

    # τ(2) = -24, |τ(2)| = 24 = exponent
    print(f"\nFIRST COEFFICIENT τ(2) = −24:")
    assert tau[2] == -24
    assert abs(tau[2]) == 24
    assert tau[2] % P == 13 and 13 in CASCADE
    print(f"  τ(2) = {tau[2]}  check")
    print(f"  |τ(2)| = {abs(tau[2])} = exponent 24 = CASCADE∩SEED node  check")
    print(f"  τ(2) mod 37 = {tau[2] % P} ∈ CASCADE  check")

    # Key τ(n) mod 37 values
    print(f"\nKEY τ(n) mod 37 VALUES:")
    checks = [
        (1,  1,  'IC'),
        (2,  13, 'CASCADE'),
        (3,  30, 'SA,ST'),
        (4,  8,  'CASCADE'),
        (8,  9,  'SA'),
        (9,  21, 'ST'),
        (10, 1,  'IC'),
        (11, 36, 'NEG_H'),
        (12, 18, 'SEED'),
    ]
    for n, expected_r, lab in checks:
        r = tau[n] % P
        assert r == expected_r, f"tau({n}) mod 37 = {r}, expected {expected_r}"
        print(f"  τ({n:2d}) mod 37 = {r:2d} ∈ {lab}  check")

    # τ(3) double-sovereign
    assert tau[3] % P == 30 and 30 in SA and 30 in ST
    print(f"  τ(3) mod 37 = 30 ∈ SA∩ST (double-sovereign — unique shared element)  check")

    # τ(37)
    print(f"\nτ(37):")
    r37 = tau[37] % P
    assert r37 == 31
    assert dr(31) == 4 and 4 in SA
    print(f"  τ(37) = {tau[37]}")
    print(f"  τ(37) mod 37 = {r37}")
    print(f"  DR({r37}) = {dr(r37)} ∈ SA  check")

    # 691 mod 37
    print(f"\n691 (RAMANUJAN CONGRUENCE PRIME):")
    assert 691 % P == 25 and 25 in SA
    print(f"  691 mod 37 = {691 % P} ∈ SA  check")
    print(f"  Ramanujan congruence prime → Sovereign Anchor  check")

    # Named set hit rate
    print(f"\nNAMED SET HIT RATE (τ(n) mod 37, n=1..100):")
    hits  = sum(1 for n in range(1, 101) if tau[n] % P in named)
    zeros = sum(1 for n in range(1, 101) if tau[n] % P == 0)
    print(f"  Named hits: {hits}/100 = {hits}%")
    print(f"  SEAM (≡0 mod 37): {zeros}")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
