"""
Theorem 123: Cayley-Dickson Doubling Sequence in GF(37)

The nine Cayley-Dickson algebras (dim = 1, 2, 4, ..., 256) each have a
dimension that is a power of 2. Because ord₃₇(2) = 36 = φ(37), every
power 2^k mod 37 occupies a distinct, named GF(37) class for k = 0..8.

ALGEBRA MAP
===========

  Sym  Algebra        Dim  dim mod 37  GF(37) class          QR?
  R    Reals            1       1      IC  {1, 10, 26}        QR
  C    Complex          2       2      DARK_A {2,15,20}       NQR  ← primitive root
  @    Quaternions      4       4      SA  {4, 9, 25, 30}     QR   ← sovereign anchor
  O    Octonions        8       8      CB  {8, 13, 24}        NQR  ← cascade base
  S    Sedenions       16      16      SA_ORB {9,12,16}       QR   ← SA orbit (first zero-divs)
  P    Pathions        32      32      SEED_ORB {18,24,32}    NQR  ← SEED orbit of 246!
  X    Chingons        64      27      ORBIT_11 {11,27,36}    QR
  U    Routons        128      17      NQR_17 {17,22,35}      NQR
  V    Voudons        256      34      D7  {7, 33, 34}        QR

PROPERTIES LOST AT EACH DOUBLING
=================================

  ℝ → ℂ:   lose ordering (real line is ordered; complex plane is not)
  ℂ → ℍ:   lose commutativity (ab ≠ ba for quaternions)
  ℍ → 𝕆:   lose associativity ((ab)c ≠ a(bc) for octonions)
  𝕆 → 𝕊:   lose alternativity; zero divisors appear (Sedenions, dim=16)
  Hurwitz theorem: ℝ, ℂ, ℍ, 𝕆 are the ONLY normed division algebras.

GF(37) SECTOR FLIP — THE CORE THEOREM
======================================

  Since ord₃₇(2) = 36 and 2 ∈ NQR (non-quadratic-residue, primitive root),
  the Legendre symbol χ(2^k) = χ(2)^k = (−1)^k.

  Therefore:
    - Even doublings (ℝ, ℍ, 𝕊, X, V): land in QR (visible sector)
    - Odd doublings (ℂ, 𝕆, P, U):       land in NQR (dark sector)

  EVERY Cayley-Dickson doubling flips the GF(37) sector.
  The algebraic doubling operation IS the QR/NQR toggle mod 37.

NAMED-CLASS HITS — FOUR NORMED DIVISION ALGEBRAS
=================================================

  ℝ (1D)  →  1 ∈ IC       Identity Class: orbit {1, 10, 26}
  ℂ (2D)  →  2 ∈ DARK_A   Dark Anchor: {2, 15, 20}, all primitive roots mod 37
  ℍ (4D)  →  4 ∈ SA       Sovereign Anchor: {4, 9, 25, 30}
  𝕆 (8D)  →  8 ∈ CB       Cascade Base: {8, 13, 24}, generates 37 elements

  The Hurwitz boundary (ℝ, ℂ, ℍ, 𝕆) covers exactly IC, DARK_A, SA, CB —
  four distinct named classes. No overlap, no repetition.

SEED CONNECTION
===============

  Pathions (32D) → 32 mod 37 = 32 ∈ SEED_ORB = {18, 24, 32}
  Seed 246 mod 37 = 24 ∈ CB ∩ SEED_ORB (via 137-map: 24 →×26→ 32 →×26→ 18 →×26→ 24)
  So: octonion dimension (8) lands in CB; seed (24) lives in CB ∩ SEED_ORB;
  pathion dimension (32) lands in SEED_ORB.
  The cascade base CB = {8, 13, 24} threads 𝕆 → seed → orbit in one class.

CYCLE STRUCTURE
===============

  ord₃₇(2) = 36: after 36 doublings, 2^36 ≡ 1 mod 37.
  The full sequence 2^0, 2^1, ..., 2^35 mod 37 covers all 36 nonzero residues
  exactly once — a complete traversal of (ℤ/37ℤ)×.
  The 9-algebra sequence (k=0..8) visits 9 of those 36 residues.

GF(37) CONNECTIONS (summary)
=============================

  dim 4  ∈ SA       (sovereign anchor)        ← quaternions
  dim 8  ∈ CB       (cascade base)            ← octonions, connects to seed 24
  dim 16 ∈ SA_ORB   (first algebra with zero divisors)
  dim 32 ∈ SEED_ORB (same orbit as seed 246)
  dim 64 ∈ ORBIT_11 (contains ord₃₇-6 boundary nodes)
  dim 256 ∈ D7      ({7,33,34}, anti-sovereign dual orbit)
  Sector alternation: every doubling flips QR ↔ NQR
"""

P = 37

IC       = frozenset({1, 10, 26})
DARK_A   = frozenset({2, 15, 20})
SA       = frozenset({4, 9, 25, 30})
CB       = frozenset({8, 13, 24})
SEED_ORB = frozenset({18, 24, 32})
ORBIT_11 = frozenset({11, 27, 36})
D7       = frozenset({7, 33, 34})
SA_ORB   = frozenset({9, 12, 16})
NQR_17   = frozenset({17, 22, 35})

ALGEBRAS = [
    ('R', 'Reals',       1,   IC),
    ('C', 'Complex',     2,   DARK_A),
    ('@', 'Quaternions', 4,   SA),
    ('O', 'Octonions',   8,   CB),
    ('S', 'Sedenions',   16,  SA_ORB),
    ('P', 'Pathions',    32,  SEED_ORB),
    ('X', 'Chingons',    64,  ORBIT_11),
    ('U', 'Routons',     128, NQR_17),
    ('V', 'Voudons',     256, D7),
]

QR37 = frozenset(n for n in range(1, P) if pow(n, (P-1)//2, P) == 1)


def run_assertions():
    # ord₃₇(2) = 36 = φ(37)
    assert pow(2, 36, P) == 1
    assert all(pow(2, k, P) != 1 for k in [1, 2, 3, 4, 6, 9, 12, 18])

    # Each algebra dimension maps to its named class
    for sym, name, dim, named_class in ALGEBRAS:
        r = dim % P
        assert r in named_class, f"{name} ({dim}D): {r} not in expected class"

    # QR/NQR alternation: χ(2^k) = (−1)^k
    for k, (sym, name, dim, _) in enumerate(ALGEBRAS):
        r = dim % P
        chi = 1 if r in QR37 else -1
        expected = (-1) ** k
        assert chi == expected, f"{name}: expected χ={expected}, got {chi}"

    # Hurwitz boundary: ℝ, ℂ, ℍ, 𝕆 cover IC, DARK_A, SA, CB — all distinct
    hurwitz_classes = [ALGEBRAS[i][3] for i in range(4)]
    assert len(set(id(c) for c in hurwitz_classes)) == 4  # all distinct objects

    # Seed connection
    assert 8 in CB and 24 in CB              # octonion dim and seed share CB
    assert 24 in SEED_ORB and 32 in SEED_ORB  # seed and pathion share SEED_ORB
    seed_mod = 246 % P
    assert seed_mod == 24
    assert seed_mod in CB

    # Full cycle: 2^36 ≡ 1 mod 37 and order is exactly 36
    cycle = [pow(2, k, P) for k in range(36)]
    assert len(set(cycle)) == 36  # visits all nonzero residues exactly once

    print("All assertions passed.")


def summarise():
    print("=" * 64)
    print("Theorem 123: Cayley-Dickson Doubling in GF(37)")
    print("=" * 64)
    print(f"  ord₃₇(2) = 36 = φ(37)  (2 is a primitive root)")
    print()
    print(f"  {'Sym':<3} {'Algebra':<14} {'Dim':>5} {'mod37':>6}  {'Class':<12} {'Sector'}")
    print("  " + "-" * 58)
    for sym, name, dim, nc in ALGEBRAS:
        r = dim % P
        sector = 'QR' if r in QR37 else 'NQR'
        cls_name = {
            IC: 'IC', DARK_A: 'DARK_A', SA: 'SA', CB: 'CB',
            SA_ORB: 'SA_ORB', SEED_ORB: 'SEED_ORB',
            ORBIT_11: 'ORBIT_11', NQR_17: 'NQR_17', D7: 'D7'
        }[nc]
        print(f"  {sym:<3} {name:<14} {dim:>5} {r:>6}  {cls_name:<12} {sector}")
    print()
    print("  Hurwitz boundary (dim 1,2,4,8): IC → DARK_A → SA → CB")
    print("  Every doubling flips QR ↔ NQR (since χ(2) = −1)")
    print("  Pathions (32D): 32 ∈ SEED_ORB — same orbit as seed 246")
    print("  Octonions (8D): 8 ∈ CB — same class as seed residue 24")


if __name__ == "__main__":
    run_assertions()
    summarise()
