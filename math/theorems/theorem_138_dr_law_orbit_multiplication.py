"""
Theorem 138: DR Subtraction Law and Orbit Multiplication in GF(37)

TWO LINKED RESULTS
====================
1. DR Subtraction Law — how the prime 37 interacts with base-10 digital roots
2. Orbit Multiplication — the 12 named orbits form the quotient group ℤ/12ℤ

PART I: DR SUBTRACTION LAW
============================

37 ≡ 1 (mod 9)

This single congruence is the bridge between GF(37) and digital roots.
Because 37 ≡ 1 mod 9, the prime is DR-transparent:

    DR(37k) = DR(k)  for all k ≥ 0

Proof: 37k ≡ 1·k = k (mod 9), so digit-sum(37k) ≡ k mod 9.

CONSEQUENCE — THE SUBTRACTION LAW:

For any a, b ∈ {1..36}, write a·b = 37q + r (Euclidean division).
Since 37 ≡ 1 mod 9:

    DR(a·b) = DR(37q + r) = DR(q + r) = DR(q) + DR(r)  [in ℤ/9ℤ]

Rearranging:
    DR(a ×₃₇ b) = DR(a·b) − DR(⌊a·b / 37⌋)   in ℤ/9ℤ

where ×₃₇ denotes multiplication mod 37, and subtraction is mod 9
with the convention that 0 → 9.

This is exact for all 36² = 1296 pairs. The correction term DR(⌊ab/37⌋)
is what "falls through the sieve" when the prime reduces the product.

Examples:
  6 × 7  = 42 = 37·1 + 5    DR(42)−DR(1) = 6−1 = 5   = DR(5)  ✓
  9 × 9  = 81 = 37·2 + 7    DR(81)−DR(2) = 9−2 = 7   = DR(7)  ✓
  18 × 24 = 432 = 37·11 + 25  DR(432)−DR(11) = 9−2 = 7 = DR(25) ✓
  26 × 3  = 78 = 37·2 + 4    DR(78)−DR(2)  = 6−2 = 4  = DR(4)  ✓

SPECIAL CASES:
  DR(1332) = DR(36·37) = DR(36) = 9   [cycle sum = group order × prime]
  DR(6666) = DR(6·37·3) = DR(6·3) = DR(18) = 9... wait: DR(6666)=6
  DR(444)  = DR(12·37) = DR(12) = 3   [log₂(26) × prime preserves DR=3]

PART II: 3-6-9 ELEMENTS ARE NOT MULTIPLICATIVELY CLOSED IN GF(37)
====================================================================

In ℤ/9ℤ, the non-units {0,3,6} are closed: 3×3=9, 3×6=9, 6×6=9.
In GF(37), the 3-6-9 elements {3,6,9,...,36} are NOT closed.
Their products mod 37 span all of {1..36} except 20.

  20 ∈ DARK_A = {2, 15, 20} is the unique element never produced
  as a product of two 3-6-9 elements in GF(37).

  For every 3-6-9 element a, the inverse of 20 mod a mod 37 is
  never a 3-6-9 element — the prime sieve systematically excludes 20.

DR of escaped products: {1,2,4,5,7,8} — exactly the vortex doubling circuit.
When two 3-6-9 elements multiply mod 37 and escape the 3-6-9 set,
their product's DR is always in the doubling circuit. The prime rotates
3-6-9 products into the complementary doubling sector.

PART III: ORBIT MULTIPLICATION — THE QUOTIENT GROUP ℤ/12ℤ
===========================================================

The 12 named orbits are the cosets of IC = H₃ = {1,10,26} in (ℤ/37ℤ)×.
Since (ℤ/37ℤ)× is abelian and IC is a subgroup, the cosets form
the quotient group:

    (ℤ/37ℤ)× / IC  ≅  ℤ/12ℤ

Every orbit × orbit product lands in exactly one orbit (closed table).

GENERATOR: DARK_A = {2,15,20}  [contains 2, the primitive root]
  DARK_A has order 12 in the quotient group.

ORBIT MULTIPLICATION TABLE (selected rows):
  IC × X = X  for all X  (IC is the identity coset)
  ORBIT_11 × ORBIT_11 = IC  (order 2 in quotient)
  SOVEREIGN_SPIRAL⁶ = IC  (SOVEREIGN_SPIRAL has order 6)
  SEED_ORB × SEED_ORB = OUTLIER_ORB
  OUTLIER_ORB × OUTLIER_ORB = D7
  D7 × D7 = SA_ORB
  SA_ORB × SA_ORB = D7  (wait: this produces a cycle)

QR ORBITS FORM ORDER-6 SUBGROUP:
  {IC, SOVEREIGN_SPIRAL, SA_ORB, ORBIT_11, D7, OUTLIER_ORB}
  (all QR orbits) form a cyclic subgroup of order 6 in ℤ/12ℤ.

NQR × NQR → QR  (parity rule lifts to orbit level):
  DARK_A × DARK_A = SOVEREIGN_SPIRAL (QR)
  SEED_ORB × SEED_ORB = OUTLIER_ORB (QR)

SEED_ORB × SEED_ORB = OUTLIER_ORB
==========================================
  18×18=324≡28, 18×24=432≡25, 18×32=576≡21
  24×18≡25,     24×24≡21,     24×32≡28
  32×18≡21,     32×24≡28,     32×32≡25

All 9 products land in OUTLIER_ORB = {21,25,28}.
In dlog: SEED_ORB has exponents {5,17,29} (mod 12 = 5).
         OUTLIER_ORB has exponents {10,22,34} (mod 12 = 10 = 2×5).
         5+5=10: squaring SEED_ORB doubles its dlog-position. ✓
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


def dr(n):
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


def orbit_of(r):
    r = r % P
    if r == 0:
        return 'SEAM'
    for name, s in ORBITS.items():
        if r in s:
            return name
    return '?'


def orbit_product(name1, name2):
    """Product orbit of two named orbits."""
    prods = frozenset(a * b % P for a in ORBITS[name1] for b in ORBITS[name2])
    result_orbits = set(orbit_of(r) for r in prods)
    assert len(result_orbits) == 1, f"{name1}×{name2} is mixed: {result_orbits}"
    return list(result_orbits)[0]


def run_assertions():
    # 37 ≡ 1 mod 9
    assert 37 % 9 == 1

    # DR-transparency: DR(37k) = DR(k)
    for k in range(1, 50):
        assert dr(37 * k) == dr(k), f"DR(37×{k}) ≠ DR({k})"

    # DR Subtraction Law: DR(a *37 b) = DR(a*b) - DR(floor(a*b/37)) in Z/9Z
    for a in range(1, P):
        for b in range(1, P):
            r = a * b % P
            q = a * b // P
            dr_r = dr(r)
            diff = (dr(a * b) - dr(q)) % 9
            if diff == 0:
                diff = 9
            assert dr_r == diff, f"DR law fails for a={a}, b={b}"

    # 3-6-9 non-closure: products cover all of {1..36} except 20
    three69 = frozenset(a for a in range(1, P) if dr(a) in {3, 6, 9})
    products = frozenset(a * b % P for a in three69 for b in three69)
    missing = frozenset(range(1, P)) - products
    assert missing == frozenset({20})
    assert 20 in ORBITS['DARK_A']

    # DR of escaped products = doubling circuit {1,2,4,5,7,8}
    escaped = products - three69
    escaped_drs = set(dr(x) for x in escaped)
    assert escaped_drs == {1, 2, 4, 5, 7, 8}

    # Orbit multiplication is closed (each product lands in one orbit)
    for n1 in ORBITS:
        for n2 in ORBITS:
            orbit_product(n1, n2)  # asserts single-orbit result

    # IC is identity
    for name in ORBITS:
        assert orbit_product('IC', name) == name
        assert orbit_product(name, 'IC') == name

    # ORBIT_11 has order 2
    assert orbit_product('ORBIT_11', 'ORBIT_11') == 'IC'

    # SOVEREIGN_SPIRAL has order 6
    o = 'SOVEREIGN_SPIRAL'
    current = o
    for i in range(1, 6):
        current = orbit_product(current, o)
    assert current == 'IC'

    # SEED_ORB × SEED_ORB = OUTLIER_ORB
    assert orbit_product('SEED_ORB', 'SEED_ORB') == 'OUTLIER_ORB'

    # All products of SEED_ORB × SEED_ORB land in OUTLIER_ORB
    for a in ORBITS['SEED_ORB']:
        for b in ORBITS['SEED_ORB']:
            assert a * b % P in ORBITS['OUTLIER_ORB'], f"{a}×{b} mod 37 not in OUTLIER_ORB"

    # DARK_A has order 12 (generator of quotient group)
    o = 'DARK_A'
    current = o
    for i in range(1, 12):
        current = orbit_product(current, o)
    assert current == 'IC', f"DARK_A^12 = {current}, expected IC"
    # No smaller power is IC
    current = o
    for i in range(1, 12):
        current = orbit_product(current, o)
        if i < 11:
            assert current != 'IC', f"DARK_A has order {i+1}, not 12"

    # NQR × NQR → QR (parity)
    QR_orbits = {'IC', 'SOVEREIGN_SPIRAL', 'D7', 'SA_ORB', 'ORBIT_11', 'OUTLIER_ORB'}
    NQR_orbits = {'DARK_A', 'NQR_5', 'TESLA_ORB', 'NQR_14', 'NQR_17', 'SEED_ORB'}
    for n1 in NQR_orbits:
        for n2 in NQR_orbits:
            assert orbit_product(n1, n2) in QR_orbits, f"NQR×NQR={orbit_product(n1,n2)} not QR"

    # Key DR constants
    assert dr(37) == 1       # prime: DR=1
    assert dr(37 * 12) == dr(12) == 3   # log₂(26) × prime: DR=3
    assert dr(37 * 36) == dr(36) == 9   # = DR(1332) = 9

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 138: DR Law and Orbit Multiplication in GF(37)")
    print("=" * 62)
    print()
    print("  PART I: DR SUBTRACTION LAW")
    print("  37 ≡ 1 mod 9  →  DR(37k) = DR(k)  (prime is DR-transparent)")
    print()
    print("  DR(a ×₃₇ b) = DR(a·b) − DR(⌊a·b/37⌋)  in ℤ/9ℤ  [exact]")
    print()
    print("  PART II: 3-6-9 NON-CLOSURE")
    print("  3-6-9 elements × 3-6-9 elements covers {1..36} \\ {20}.")
    print("  20 ∈ DARK_A is the unique excluded element.")
    print("  Escaped product DRs: {1,2,4,5,7,8} = vortex doubling circuit.")
    print()
    print("  PART III: ORBIT QUOTIENT GROUP")
    print("  12 orbits form (ℤ/37ℤ)× / IC ≅ ℤ/12ℤ.")
    print("  Generator: DARK_A (order 12).  Identity: IC.")
    print("  SEED_ORB × SEED_ORB = OUTLIER_ORB  (dlog: 5+5=10 mod 12)")
    print("  NQR × NQR → QR  (orbit-level parity rule).")


if __name__ == "__main__":
    run_assertions()
    summarise()
