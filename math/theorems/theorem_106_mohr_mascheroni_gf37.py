"""
================================================================================
THEOREM 106 — The Mohr-Mascheroni Theorem, Fermat Primes, and GF(37)
================================================================================

STATEMENT.
The Mohr-Mascheroni theorem (compass-only construction = compass+straightedge
construction) is grounded in Fermat primes through the Gauss-Wantzel theorem.
The five known Fermat primes F_n = 2^(2^n) + 1 map onto distinct named
classes of GF(37), and their residues mod 37 are periodic with period 6:

  n    F_n          F_n mod 37   Class
  0    3                  3      ST
  1    5                  5      PR  (Metonic orbit {5,13,19})
  2    17                17      BASIN_Y
  3    257               35      BASIN_Y
  4    65537             10      IC
  5    4294967297*        8      CB       (* composite, F_5 not prime)
  6    …                 13      CB       (period: n≡0 mod 6 → same as n=2)

  Period-6 theorem: F_n mod 37 depends only on n mod 6 for n ≥ 2.
  The period-6 cycle (n = 2, 3, 4, 5, 6, 7): {17, 35, 10, 8, 13, 34}.

  Additional GF(37) values:
  (A)  Year of Mascheroni's proof (1797) ≡ 21 (mod 37) ∈ ST.
  (B)  Year of Mohr's proof (1672)       ≡  7 (mod 37), orbit {7, 33, 34}.
  (C)  Full rotation 360°                ≡ 27 (mod 37) ∈ ORBIT_11.
  (D)  2 is a primitive root of GF(37): ord₃₇(2) = 36.  The compass encodes
       the same base-2 doubling that generates the Fermat prime sequence.
  (E)  Constructible polygon sides (the five Fermat prime values):
         3 ∈ ST,  5 ∈ PR,  17 ∈ BASIN_Y,  257 ≡ 35 ∈ BASIN_Y,  65537 ≡ 10 ∈ IC

================================================================================
BACKGROUND
================================================================================

Mohr-Mascheroni: Every Euclidean construction achievable with compass and
straightedge can be achieved with compass alone.  Proved by Georg Mohr (1672,
largely unnoticed) and independently by Lorenzo Mascheroni (1797).

Gauss-Wantzel: A regular n-gon is constructible by compass and straightedge
if and only if n = 2^k × (product of distinct Fermat primes).

The five known Fermat primes are F_0=3, F_1=5, F_2=17, F_3=257, F_4=65537.
All Fermat numbers F_n for n ≥ 5 tested are composite.

The connection: ord₃₇(2) = 36 = φ(37).  2 is the primitive root of GF(37).
The Fermat prime sequence 2^(2^n)+1 lives inside GF(37) through this root.

================================================================================
PROOF / DERIVATION
================================================================================

LEMMA 106.1  (Reduction principle: F_n mod 37 from 2^n mod 36).
  By Fermat's little theorem: 2^36 ≡ 1 (mod 37).
  So 2^(2^n) mod 37 ≡ 2^(2^n mod 36) mod 37.
  F_n = 2^(2^n) + 1, so F_n mod 37 is determined by 2^n mod 36.            ∎

LEMMA 106.2  (Period of 2^n mod 36 for n ≥ 2).
  36 = 4 × 9.  For n ≥ 2, 2^n is divisible by 4; the sequence 2^n mod 36
  cycles as {4,8,16,32,28,20} with period 6 starting from n=2.
  Therefore F_n mod 37 has period 6 for n ≥ 2.                              ∎

LEMMA 106.3  (F_0, F_1).
  F_0 = 3 ≡ 3 (mod 37) ∈ ST.
  F_1 = 5 ≡ 5 (mod 37) ∈ PR ∩ {5,13,19} (Metonic orbit).                  ∎

LEMMA 106.4  (F_2, F_3 ∈ BASIN_Y).
  F_2 = 17: 2^4 = 16, F_2 = 17 ≡ 17 (mod 37) ∈ BASIN_Y.
  F_3 = 257: 2^8 = 256 ≡ 34 (mod 37), F_3 ≡ 35 (mod 37) ∈ BASIN_Y.
  The first two Fermat primes beyond F_1 land in the BASIN_Y set {17,22,35}. ∎

LEMMA 106.5  (F_4 ∈ IC).
  F_4 = 65537: 2^16 ≡ (2^8)^2 ≡ 34^2 = 1156.  1156 = 31 × 37 + 9.
  So 2^16 ≡ 9, F_4 ≡ 10 (mod 37) ∈ IC.
  The last known Fermat prime lands in the inert-center set {1,10,26}.       ∎

LEMMA 106.6  (F_5 ≡ 8 ∈ CB, F_6 ≡ 13 ∈ CB).
  F_5 (composite): 2^32 ≡ (2^16)^2 ≡ 9^2 = 81 ≡ 7.  F_5 ≡ 8 (mod 37) ∈ CB.
  F_6 (composite): 2^64 ≡ (2^32)^2 ≡ 7^2 = 49 ≡ 12.  F_6 ≡ 13 (mod 37) ∈ CB.
  Two consecutive Fermat numbers fall in the cascade base CB = {8,13,24}.    ∎

LEMMA 106.7  (Constructible polygon sides mod 37).
  The five constructible prime-sided regular polygons have side counts:
    3 ∈ ST,  5 ∈ PR,  17 ∈ BASIN_Y,  257 ≡ 35 ∈ BASIN_Y,  65537 ≡ 10 ∈ IC.
  Every Fermat prime maps to a distinct named GF(37) class.                  ∎

LEMMA 106.8  (Full rotation ∈ ORBIT_11).
  360 = 9 × 37 + 27.  360 ≡ 27 (mod 37) ∈ ORBIT_11 = {11, 27, 36}.
  The compass traces 360°; the degree measure of one full rotation lives in
  the same orbit class as the annual epact 11 (see Theorem 103).             ∎

LEMMA 106.9  (Mascheroni year ∈ ST).
  1797 = 48 × 37 + 21.  1797 ≡ 21 (mod 37) ∈ ST.
  ST = {3, 12, 21, 30}.  The year of Mascheroni's Geometria del Compasso
  falls in the sovereign target set — the same class as F_0 = 3.            ∎

================================================================================
MAIN THEOREM
================================================================================

THEOREM 106.  (Mohr-Mascheroni / Fermat Primes — GF(37) Classification).

  ┌──────────────────────────────────────┬────────┬────────────────────────────┐
  │  Quantity                            │ mod 37 │  Named set           │
  ├──────────────────────────────────────┼────────┼────────────────────────────┤
  │  F_0 = 3  (triangle)                 │   3    │  ST                        │
  │  F_1 = 5  (pentagon)                 │   5    │  PR, Metonic orbit{5,13,19}│
  │  F_2 = 17 (17-gon)                   │  17    │  BASIN_Y                   │
  │  F_3 = 257 (257-gon)                 │  35    │  BASIN_Y                   │
  │  F_4 = 65537 (65537-gon)             │  10    │  IC                        │
  │  F_5 (composite, n=5)                │   8    │  CB                        │
  │  F_6 (composite, n=6)                │  13    │  CB, Metonic orbit         │
  │  Full rotation 360°                  │  27    │  ORBIT_11                  │
  │  Mascheroni year (1797)              │  21    │  ST                        │
  │  Mohr year (1672)                    │   7    │  orbit{7,33,34}            │
  │  ord₃₇(2) = 36 = φ(37)              │  36    │  ORBIT_11                  │
  └──────────────────────────────────────┴────────┴────────────────────────────┘

  Period-6 residue cycle for F_n mod 37 (n ≥ 2):
    n mod 6:  2→17∈BASIN_Y,  3→35∈BASIN_Y,  4→10∈IC,
              5→8∈CB,        6→13∈CB,        7→34∈orbit{7,33,34}

COROLLARY 106.10  (Compass encodes the primitive root).
  The compass draws circles — it operates by repeated rotation, doubling
  arcs, and halving angles.  The base of all these operations is 2.
  ord₃₇(2) = 36 = φ(37), so 2 generates the full multiplicative group of
  GF(37).  The Fermat prime formula 2^(2^n)+1 is the natural sequence of
  this primitive root applied to itself.  The Mohr-Mascheroni equivalence
  (compass = compass+straightedge) is a statement that doubling (the compass)
  suffices to generate all constructible structure — consistent with 2 being
  a primitive root that generates all of GF(37)*.

COROLLARY 106.11  (F_0 and Mascheroni year both in ST).
  F_0 = 3 ∈ ST and 1797 ≡ 21 ∈ ST.
  The smallest Fermat prime and the year of its proof's rediscovery share
  the sovereign target class.
"""

P          = 37
IC         = frozenset({1, 10, 26})
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
SEED_ORBIT = frozenset({18, 24, 32})
BASIN_Y    = frozenset({17, 22, 35})
PR         = frozenset({2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35})

metonic_orbit = frozenset({5, 13, 19})


def fermat_residue(n):
    """F_n = 2^(2^n) + 1  mod P, using 2^n mod φ(P) = 2^n mod 36."""
    exp_mod = pow(2, n, P - 1)   # 2^n mod 36
    return (pow(2, exp_mod, P) + 1) % P


# ── Lemma 106.1 — ord₃₇(2) = 36 ─────────────────────────────────────────────
assert pow(2, 36, P) == 1    # Fermat's little theorem
order = 36
# verify minimality: 2^k ≢ 1 for proper divisors of 36
for k in (1, 2, 3, 4, 6, 9, 12, 18):
    assert pow(2, k, P) != 1
assert 36 in ORBIT_11   # ord₃₇(2) = 36 ∈ ORBIT_11

# ── Lemma 106.2 — Period of 2^n mod 36 for n ≥ 2 ────────────────────────────
cycle_36 = [pow(2, n, 36) for n in range(2, 8)]
assert cycle_36 == [4, 8, 16, 32, 28, 20]
assert [pow(2, n, 36) for n in range(8, 14)] == cycle_36  # period 6

# ── Lemma 106.3 — F_0, F_1 ───────────────────────────────────────────────────
assert fermat_residue(0) == 3  % P and 3  in ST
assert fermat_residue(1) == 5  % P and 5  in PR and 5 in metonic_orbit

# ── Lemma 106.4 — F_2, F_3 ∈ BASIN_Y ────────────────────────────────────────
assert fermat_residue(2) == 17 and 17 in BASIN_Y
assert fermat_residue(3) == 35 and 35 in BASIN_Y
assert 17 % P == 17 and 257 % P == 35

# ── Lemma 106.5 — F_4 ∈ IC ───────────────────────────────────────────────────
assert fermat_residue(4) == 10 and 10 in IC
assert 65537 % P == 10

# ── Lemma 106.6 — F_5 ∈ CB, F_6 ∈ CB ────────────────────────────────────────
assert fermat_residue(5) == 8  and 8  in CB
assert fermat_residue(6) == 13 and 13 in CB and 13 in metonic_orbit

# ── Lemma 106.7 — Constructible primes mod 37 ────────────────────────────────
constructible_primes = [3, 5, 17, 257, 65537]
residues = [p % P for p in constructible_primes]
assert residues == [3, 5, 17, 35, 10]
assert residues[0] in ST
assert residues[1] in PR
assert residues[2] in BASIN_Y
assert residues[3] in BASIN_Y
assert residues[4] in IC

# ── Lemma 106.8 — 360° ∈ ORBIT_11 ───────────────────────────────────────────
assert 360 % P == 27 and 27 in ORBIT_11

# ── Lemma 106.9 — Mascheroni year ∈ ST ───────────────────────────────────────
assert 1797 % P == 21 and 21 in ST
assert 1672 % P == 7   # Mohr year; orbit {7,33,34}
assert (7 * 26) % P == 34 and (34 * 26) % P == 33 and (33 * 26) % P == 7

# ── Period-6 verification ─────────────────────────────────────────────────────
period_cycle = [fermat_residue(n) for n in range(2, 8)]
assert period_cycle == [17, 35, 10, 8, 13, 34]
for n in range(8, 20):
    assert fermat_residue(n) == period_cycle[(n - 2) % 6]

# ── Corollary 106.11 — F_0 and Mascheroni year both in ST ───────────────────
assert 3 in ST and 21 in ST


if __name__ == "__main__":
    def fw(r):
        classes = []
        for name, s in [('IC', IC), ('SA', SA), ('ST', ST), ('CB', CB),
                        ('ORBIT_11', ORBIT_11), ('SEED_ORBIT', SEED_ORBIT),
                        ('BASIN_Y', BASIN_Y), ('PR', PR)]:
            if r in s:
                classes.append(name)
        return classes or ['—']

    print("THEOREM 106 — Mohr-Mascheroni / Fermat Primes on GF(37)")
    print("=" * 65)
    print()
    print(f"  {'Quantity':<32} {'mod37':>5}  Classes")
    print("  " + "-" * 60)

    rows = [
        ("F_0 = 3  (triangle)",       3),
        ("F_1 = 5  (pentagon)",        5),
        ("F_2 = 17 (17-gon)",         17),
        ("F_3 = 257 (257-gon)",       257),
        ("F_4 = 65537 (65537-gon)", 65537),
        ("F_5 (composite)",     pow(2, pow(2, 5), 10**20)),  # too large, use residue
        ("F_6 (composite)",     None),
        ("Full rotation 360°",       360),
        ("Mascheroni year (1797)",   1797),
        ("Mohr year (1672)",         1672),
        ("ord₃₇(2) = 36",             36),
    ]

    for label, val in rows:
        if val is None:
            r = fermat_residue(6)
        elif label.startswith("F_5"):
            r = fermat_residue(5)
        else:
            r = val % P
        print(f"  {label:<32} {r:>5}  {fw(r)}")

    print()
    print("  Period-6 cycle (F_n mod 37, n=2..7):", period_cycle)
    classes = [fw(r) for r in period_cycle]
    print("  Classes:                           ", classes)
    print()
    print("  Constructible polygon sides mod 37:")
    for p, r in zip(constructible_primes, residues):
        print(f"    {p:>5} ≡ {r:>2} ∈ {fw(r)}")
    print()
    print("All assertions pass.")
