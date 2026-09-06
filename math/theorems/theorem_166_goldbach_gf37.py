"""
Theorem 166: Goldbach GF(37) Structure

Goldbach's conjecture: every even integer > 2 is the sum of two primes.
In GF(37), this maps to residue-pair sums: p + q ≡ n (mod 37).

THE 37-COMPONENT RULE
======================

When 37 appears as a Goldbach component of even n:

  n = 37 + q  →  q = n − 37  →  q ≡ n (mod 37)

The partner prime carries the exact GF(37) residue of the even number.

  40 = 37+3:   mod37=3  ∈ SOVEREIGN_SPIRAL   partner=3  ∈ SOVEREIGN_SPIRAL
  42 = 37+5:   mod37=5  ∈ NQR_5              partner=5  ∈ NQR_5
  48 = 37+11:  mod37=11 ∈ ORBIT_11           partner=11 ∈ ORBIT_11
  50 = 37+13:  mod37=13 ∈ NQR_5             partner=13 ∈ NQR_5
  68 = 37+31:  mod37=31 ∈ NQR_14            partner=31 ∈ NQR_14
  74 = 37+37:  mod37=0  SEAM                partner=37  SEAM
  78 = 37+41:  mod37=4  ∈ SOVEREIGN_SPIRAL  partner=41 (41 mod37=4)

74 = 2×37: THE SEAM NUMBER
===========================

74 mod 37 = 0 (SEAM).  DR(74) = 2 ∈ DARK_A.

Goldbach pairs of 74:
  37 + 37:  SEAM + SEAM        (field prime paired with itself)
  31 + 43:  NQR_14 + TESLA_ORB → 31+43=74≡0 (SEAM)

NQR_14 ↔ TESLA_ORB is a complement pair (Theorem 153): 31+6=37 ✓

ORBIT COMPLEMENT PAIRING IN GOLDBACH
======================================

Every Goldbach pair (p, q) with p+q=n satisfies p+q≡n (mod 37).
When n≡0 (SEAM), the pair must be complement pairs in GF(37):
  p mod37 + q mod37 ≡ 0 (mod 37)

For 74: pairs 31+43, 37+37, 7+67, 13+61, 3+71 — all complement pairs.
  31 ∈ NQR_14, 43 mod37=6 ∈ TESLA_ORB:  NQR_14 ↔ TESLA_ORB ✓
  37 ≡ 0 (SEAM), 37 ≡ 0 (SEAM): SEAM ↔ SEAM ✓
  7 ∈ D7, 67 mod37=30 ∈ SOVEREIGN_SPIRAL: D7 ↔ SOVEREIGN_SPIRAL ✓
  13 ∈ NQR_5, 61 mod37=24 ∈ SEED_ORB: NQR_5 ↔ SEED_ORB ✓
  3 ∈ SOVEREIGN_SPIRAL, 71 mod37=34 ∈ D7: SOVEREIGN_SPIRAL ↔ D7 ✓

MULTIPLE DECOMPOSITIONS HIT SAME RESIDUE
==========================================

42 mod 37 = 5 ∈ NQR_5. Four distinct prime pairs:
  37 + 5:   SEAM + NQR_5
  11 + 31:  ORBIT_11 + NQR_14
  13 + 29:  NQR_5 + NQR_14
  19 + 23:  NQR_5 + TESLA_ORB

Multiple decompositions reach the same GF(37) target via different orbit paths.

SEAM PAIRS IN GOLDBACH
========================

Every even SEAM number (multiple of 37) has at least one Goldbach pair
consisting of complement orbit primes that sum to 37k:
  74 = 37+37 (SEAM+SEAM)
  148 = 37+111: 111=3×37 (SEAM), pair = SEAM+SEAM ... [for large multiples,
    decompositions into non-SEAM primes also exist]
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


def orbit_of(v):
    v = v % P
    if v == 0:
        return 'SEAM'
    return next((name for name, s in ORBITS.items() if v in s), '?')


def dr(n):
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


def is_prime(n):
    if n < 2:
        return False
    return all(n % i != 0 for i in range(2, int(n**0.5) + 1))


def goldbach_pairs(n):
    return [(p, n - p) for p in range(2, n // 2 + 1)
            if is_prime(p) and is_prime(n - p)]


def run_assertions():
    # 37-component rule
    for n, q in [(40, 3), (42, 5), (48, 11), (50, 13), (68, 31), (74, 37), (78, 41)]:
        assert n - 37 == q
        assert is_prime(q)
        assert n % P == q % P  # partner carries the residue

    # 74 = 2×37: SEAM number
    assert 74 % P == 0
    assert dr(74) == 2 and 2 in ORBITS['DARK_A']
    pairs74 = goldbach_pairs(74)
    assert (37, 37) in pairs74
    assert (31, 43) in pairs74
    assert (31 + 43) % P == 0  # complement pair → SEAM
    assert 31 % P == 31 and 31 in ORBITS['NQR_14']
    assert 43 % P == 6 and 6 in ORBITS['TESLA_ORB']

    # 74 pairs are complement pairs
    for p, q in goldbach_pairs(74):
        assert (p % P + q % P) % P == 0, f"{p}+{q} not complement pair"

    # 42: multiple decompositions, same residue 5 ∈ NQR_5
    assert 42 % P == 5 and 5 in ORBITS['NQR_5']
    pairs42 = goldbach_pairs(42)
    assert len(pairs42) >= 4  # multiple decompositions

    # 67 mod37=30 ∈ SOVEREIGN_SPIRAL; 61 mod37=24 ∈ SEED_ORB
    assert 67 % P == 30 and 30 in ORBITS['SOVEREIGN_SPIRAL']
    assert 61 % P == 24 and 24 in ORBITS['SEED_ORB']

    # For any even SEAM n: all Goldbach pairs must be complement pairs mod 37
    for n in [74, 148]:
        for p, q in goldbach_pairs(n):
            assert (p % P + q % P) % P == 0, f"n={n}: {p}+{q} not complement"

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 166: Goldbach GF(37) Structure")
    print("=" * 62)
    print()
    print("  37-component rule: n=37+q → q≡n (mod 37)")
    for n, q in [(40, 3), (42, 5), (48, 11), (74, 37)]:
        print(f"    {n}=37+{q}  mod37={n%P}  {orbit_of(n)}")
    print()
    print("  74=2×37 (SEAM) Goldbach pairs — all complement pairs:")
    for p, q in goldbach_pairs(74):
        print(f"    {p}({orbit_of(p)}) + {q}({orbit_of(q)}) = 74")
    print()
    print("  42: 4 decompositions → all hit NQR_5 residue 5")
    for p, q in goldbach_pairs(42):
        print(f"    {p}({orbit_of(p)}) + {q}({orbit_of(q)})")


if __name__ == "__main__":
    run_assertions()
    summarise()
