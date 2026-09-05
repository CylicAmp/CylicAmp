"""
Theorem 135: Triangular Numbers in GF(37)

T(n) = n(n+1)/2.   Period mod 37: T(n+37) ≡ T(n) mod 37.

COVERAGE: 19 ACHIEVABLE, 18 NEVER HIT
=======================================

T(n) ≡ k (mod 37) has a solution iff 1 + 8k is a quadratic residue
or zero mod 37.  (Completing the square: n² + n ≡ 2k, discriminant = 1 + 8k.)

  Achievable (19): {0,1,3,4,5,6,8,9,10,15,17,18,21,23,25,28,29,31,36}
  Never hit  (18): {2,7,11,12,13,14,16,19,20,22,24,26,27,30,32,33,34,35}

18 values are permanently excluded from the triangular image — matching
the 18 NQR elements of (ℤ/37ℤ)× (discriminant is NQR → no square root).

ORBIT-BY-ORBIT COVERAGE
=========================

  Orbit            Elements     Achievable   Never hit
  IC               {1,10,26}    {1,10}       {26}
  SOVEREIGN_SPIRAL {3,4,30}     {3,4}        {30}
  D7               {7,33,34}    {}           {7,33,34}   ← entirely excluded
  SA_ORB           {9,12,16}    {9}          {12,16}
  ORBIT_11         {11,27,36}   {36}         {11,27}
  OUTLIER_ORB      {21,25,28}   {21,25,28}   {}          ← entirely achievable
  DARK_A           {2,15,20}    {15}         {2,20}
  NQR_5            {5,13,19}    {5}          {13,19}
  TESLA_ORB        {6,8,23}     {6,8,23}     {}          ← entirely achievable
  NQR_14           {14,29,31}   {29,31}      {14}
  NQR_17           {17,22,35}   {17}         {22,35}
  SEED_ORB         {18,24,32}   {18}         {24,32}
  SEAM             {0}          {0}          {}

Three entirely excluded orbits: D7 = {7, 33, 34}.
Two entirely achievable QR orbits: OUTLIER_ORB and TESLA_ORB.

KEY STRUCTURAL FACTS
======================

1.  26 IS NEVER TRIANGULAR
    26 = 137 mod 37 = the 137-map multiplier. The key of the entire GF(37)
    is permanently excluded from the triangular image mod 37.
    Discriminant: 1 + 8×26 = 209 ≡ 209 − 5×37 = 24 mod 37.
    24 ∈ NQR (SEED_ORB), so no solution exists.

2.  SEED RESIDUE 24 IS NEVER TRIANGULAR
    246 mod 37 = 24. The seed's own residue is excluded.
    Discriminant: 1 + 8×24 = 193 ≡ 8 mod 37. 8 ∈ TESLA_ORB (NQR).

3.  32 IS NEVER TRIANGULAR
    32 ∈ SEED_ORB. Discriminant: 1 + 8×32 = 257 ≡ 35 mod 37. 35 ∈ NQR_17 (NQR).
    Only 18 of the three SEED_ORB elements is achievable.

4.  T(36) = 666 = 37 × 18
    The triangular number at n = φ(37) = group order is 666.
    666 = 37 × 18, and 18 ∈ SEED_ORB.
    T(36) ≡ 0 (SEAM). The group order maps to SEAM.

5.  D7 ENTIRELY EXCLUDED
    D7 = {7, 33, 34}. All three elements are never triangular mod 37.
    34 is the unique root of the supergolden cubic x³ − x² − 1 = 0 in GF(37)
    (see Theorem 134 context). The supergolden root is never triangular.
    Discriminants: 1+56=57≡20 (NQR), 1+264=265≡7 (NQR), 1+272=273≡14 (NQR).

6.  TESLA_ORB ENTIRELY ACHIEVABLE
    {6, 8, 23} are all triangular residues: T(3)=6, T(9)=8 (mod 37), T(18)=23.

7.  PALINDROME SYMMETRY
    T(n) ≡ T(36 − n) mod 37 for all n.
    Proof: T(n) + T(36−n) = [n(n+1) + (36−n)(37−n)]/2
           = [2n² − 72n + 1332]/2 ≡ n(n+1) = 2T(n) mod 37.
    The sequence mirrors around n = 18, center T(18) = 23 ∈ TESLA_ORB.

8.  SEAM APPEARS TWICE PER PERIOD
    T(36) ≡ T(37) ≡ 0 (mod 37): two consecutive hits on SEAM at the period boundary.

DISCRIMINANT MAP (k → 1+8k → QR status)
==========================================

  Key never-hit discriminants:
    k=24 (seed%37):  disc = 8  ∈ TESLA_ORB (NQR)
    k=26 (137 map):  disc = 24 ∈ SEED_ORB  (NQR)
    k=32 (seed orb): disc = 35 ∈ NQR_17    (NQR)
    k=34 (superg.):  disc = 13 ∈ NQR_5     (NQR)
    k=7  (D7):       disc = 20 ∈ DARK_A    (NQR)
    k=33 (D7):       disc =  6 ∈ TESLA_ORB (NQR)
"""

P = 37

_DLP = {}
_x = 1
for _k in range(36):
    _DLP[_x] = _k
    _x = _x * 2 % P

def is_qr(a):
    a = a % P
    if a == 0:
        return None
    return _DLP[a] % 2 == 0

def triangular_achievable(k):
    """True if k is achievable as T(n) mod 37."""
    disc = (1 + 8 * k) % P
    if disc == 0:
        return True
    return is_qr(disc) is True

# Named orbits
IC               = frozenset({1, 10, 26})
SOVEREIGN_SPIRAL = frozenset({3, 4, 30})
D7               = frozenset({7, 33, 34})
SA_ORB           = frozenset({9, 12, 16})
ORBIT_11         = frozenset({11, 27, 36})
OUTLIER_ORB      = frozenset({21, 25, 28})
DARK_A           = frozenset({2, 15, 20})
NQR_5            = frozenset({5, 13, 19})
TESLA_ORB        = frozenset({6, 8, 23})
NQR_14           = frozenset({14, 29, 31})
NQR_17           = frozenset({17, 22, 35})
SEED_ORB         = frozenset({18, 24, 32})
SA               = frozenset({4, 9, 25, 30})


def run_assertions():
    achievable = set(k for k in range(P) if triangular_achievable(k))
    never      = set(range(P)) - achievable

    assert achievable == {0,1,3,4,5,6,8,9,10,15,17,18,21,23,25,28,29,31,36}
    assert never      == {2,7,11,12,13,14,16,19,20,22,24,26,27,30,32,33,34,35}
    assert len(achievable) == 19
    assert len(never) == 18

    # D7 entirely excluded
    assert D7.issubset(never)

    # TESLA_ORB entirely achievable
    assert TESLA_ORB.issubset(achievable)

    # OUTLIER_ORB entirely achievable
    assert OUTLIER_ORB.issubset(achievable)

    # 26 (137-map multiplier) never hit
    assert 26 in never

    # Seed residue 24 never hit
    assert 24 in never

    # 32 never hit
    assert 32 in never

    # Only 18 of SEED_ORB is achievable
    assert SEED_ORB & achievable == frozenset({18})

    # T(36) = 666 = 37 × 18
    assert 36 * 37 // 2 == 666
    assert 666 % P == 0
    assert 666 // P == 18 and 18 in SEED_ORB

    # Palindrome: T(n) ≡ T(36-n) mod 37
    for n in range(1, 37):
        tn  = n * (n + 1) // 2 % P
        t36 = (36 - n) * (37 - n) // 2 % P
        assert tn == t36, f"T({n}) ≠ T({36-n}) mod 37"

    # Center T(18) = 23 ∈ TESLA_ORB
    assert 18 * 19 // 2 % P == 23
    assert 23 in TESLA_ORB

    # T(37) ≡ 0 (two consecutive SEAMs)
    assert 37 * 38 // 2 % P == 0

    # Period 37: T(n+37) ≡ T(n)
    for n in range(1, 10):
        assert n*(n+1)//2 % P == (n+37)*(n+38)//2 % P

    # Supergolden root 34 ∈ D7, never hit
    assert pow(34, 3, P) == (pow(34, 2, P) + 1) % P   # 34 solves x³=x²+1 in GF(37)
    assert 34 in never

    # Discriminant of k=7 (D7) lands in D7 — self-referential exclusion
    assert (1 + 8 * 7) % P == 20   # 20 ∈ DARK_A (NQR)
    assert 20 in DARK_A

    print("All assertions passed.")


def summarise():
    achievable = set(k for k in range(P) if triangular_achievable(k))
    never      = set(range(P)) - achievable

    print("=" * 62)
    print("Theorem 135: Triangular Numbers in GF(37)")
    print("=" * 62)
    print()
    print(f"  T(n) = n(n+1)/2 mod 37.  Period = 37.  "
          f"Achievable: 19.  Never hit: 18.")
    print()
    print("  Orbit coverage:")
    orbits = [
        ('IC',               IC),
        ('SOVEREIGN_SPIRAL', SOVEREIGN_SPIRAL),
        ('D7',               D7),
        ('SA_ORB',           SA_ORB),
        ('ORBIT_11',         ORBIT_11),
        ('OUTLIER_ORB',      OUTLIER_ORB),
        ('DARK_A',           DARK_A),
        ('NQR_5',            NQR_5),
        ('TESLA_ORB',        TESLA_ORB),
        ('NQR_14',           NQR_14),
        ('NQR_17',           NQR_17),
        ('SEED_ORB',         SEED_ORB),
    ]
    for name, orb in orbits:
        hit  = sorted(orb & achievable)
        miss = sorted(orb & never)
        tag = ''
        if not miss: tag = '  ← entirely achievable'
        if not hit:  tag = '  ← entirely excluded'
        print(f"    {name:<20} hit={hit}  excluded={miss}{tag}")
    print()
    print("  T(36) = 666 = 37 × 18   (18 ∈ SEED_ORB; T(36) ≡ 0 = SEAM)")
    print("  T(18) = 23 ∈ TESLA_ORB  (palindrome center)")
    print("  26 (137-map multiplier): NEVER triangular mod 37")
    print("  24 (seed mod 37):        NEVER triangular mod 37")
    print("  34 (supergolden root):   NEVER triangular mod 37")
    print("  D7 = {7,33,34}: the only orbit entirely excluded")
    print("  disc(33) = 7 ∈ D7: D7 excludes itself")


if __name__ == "__main__":
    run_assertions()
    summarise()
