"""
Theorem 160: ABA Portal Palindromes — The Zero as Arithmetic Portal

THE PORTAL PRINCIPLE
=====================

Any number containing a zero has an arithmetic portal: the zero holds the
place of every possible value 1–9. The ABA palindrome A0A is the base form —
outer digit A, portal digit 0, which expands to A1A through A9A.

This generates a complete orbit sweep for each outer digit A = 1..9.

THE STRUCTURE
==============

For each outer digit A (1–9), the ten palindromes A0A through A9A:

1. DR sequence shifts by +2 for each new outer digit:
   A=1: DR starts at 2  (2,3,4,5,6,7,8,9,1,2)
   A=2: DR starts at 4  (4,5,6,7,8,9,1,2,3,4)
   A=3: DR starts at 6  (6,7,8,9,1,2,3,4,5,6)
   A=4: DR starts at 8  (8,9,1,2,3,4,5,6,7,8)
   A=5: DR starts at 1  (1,2,3,4,5,6,7,8,9,1)
   ...and so on — all DRs 1–9 appear in every group

2. Every group contains exactly one SEAM (A×111)

3. Adjacent pair sums rotate through framework orbits

4. Total sums of each group:
   A=1: 1460 mod37=17  NQR_17
   A=2: 2470 mod37=28  OUTLIER_ORB
   A=3: 3480 mod37=2   DARK_A
   A=4: 4490 mod37=13  NQR_5
   A=5: 5500 mod37=24  SEED_ORB  ← seed anchor
   A=6: 6510 mod37=35  NQR_17
   A=7: 7520 mod37=9   SA_ORB
   A=8: 8530 mod37=20  DARK_A
   A=9: 9540 mod37=31  NQR_14

The outer digit 5 group total = 5500 ≡ 24 (mod 37) ∈ SEED_ORB — the seed anchor.

THE SEAM PALINDROMES
=====================

111, 222, 333, 444, 555, 666, 777, 888, 999 — all SEAM (Theorem 157).
These are the A=B cases: when the portal digit equals the outer digit.

THE 101/191 MAGIC PAIR
=======================

Both prime. Both DR=2. Different orbits:
  101 mod 37 = 27 → ORBIT_11
  191 mod 37 = 6  → TESLA_ORB
  101 + 191 = 292 mod 37 = 33 → D7
  191 is the only 1B1 palindrome (B≠0) with DR=2.

THE 414 CONNECTION
===================

202 + 212 = 414 → D7 (Theorem 147: the 414 palindrome orbit).
The adjacent sum of the first two outer-digit-2 portal numbers produces
the canonical D7 palindrome.

COMPLEMENT STRUCTURE
=====================

Every ABA palindrome and its mod-37 complement sum to 37 (SEAM).
The complement orbit pairs are fixed across all groups:
  SEAM ↔ SEAM
  IC ↔ ORBIT_11
  SOVEREIGN_SPIRAL ↔ D7
  NQR_5 ↔ SEED_ORB
  TESLA_ORB ↔ NQR_14
  DARK_A ↔ NQR_17
  SA_ORB ↔ OUTLIER_ORB
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


def aba_group(a):
    return [100*a + 10*b + a for b in range(0, 10)]


def run_assertions():
    # Every group contains exactly one SEAM
    for a in range(1, 10):
        seams = [n for n in aba_group(a) if n % P == 0]
        assert len(seams) == 1
        assert seams[0] == a * 111

    # DR sequences: each group covers all DRs 1-9
    for a in range(1, 10):
        drs = [dr(n) for n in aba_group(a)]
        assert set(drs) == set(range(1, 10)), f"A={a}: DRs {drs} don't cover 1-9"

    # Group total for A=5 hits SEED_ORB
    assert sum(aba_group(5)) == 5500
    assert 5500 % P == 24
    assert 24 in ORBITS['SEED_ORB']

    # 101 and 191 both prime, both DR=2
    assert is_prime(101) and dr(101) == 2
    assert is_prime(191) and dr(191) == 2
    assert 101 % P == 27 and 27 in ORBITS['ORBIT_11']
    assert 191 % P == 6  and 6  in ORBITS['TESLA_ORB']

    # 202 + 212 = 414 → D7
    assert 202 + 212 == 414
    assert 414 % P == 7 and 7 in ORBITS['D7']

    # Complement pairs sum to 37
    for a in range(1, 10):
        for n in aba_group(a):
            r = n % P
            comp = (P - r) % P
            assert (r + comp) % P == 0

    # SEAM palindromes (Theorem 157 parallel)
    for a in range(1, 10):
        seam = a * 111
        assert seam % P == 0

    # Group totals
    expected = {1:17, 2:28, 3:2, 4:13, 5:24, 6:35, 7:9, 8:20, 9:31}
    for a, exp in expected.items():
        assert sum(aba_group(a)) % P == exp, f"A={a}: expected {exp}"

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 160: ABA Portal Palindromes")
    print("=" * 62)
    print()
    print("  Outer digit  Group total  mod37  Orbit")
    print("  " + "-"*45)
    for a in range(1, 10):
        g = aba_group(a)
        s = sum(g)
        star = " ← SEED_ORB (seed anchor)" if orbit_of(s) == 'SEED_ORB' else ""
        print(f"  A={a}          {s:5d}        {s%P:2d}    {orbit_of(s)}{star}")
    print()
    print("  101 (ORBIT_11, DR=2, prime) ↔ 191 (TESLA_ORB, DR=2, prime)")
    print(f"  101+191={101+191} mod37={(101+191)%P} → {orbit_of(101+191)}")
    print()
    print("  202+212=414 → D7 (Theorem 147)")
    print()
    print("  SEAM palindromes: 111,222,333,444,555,666,777,888,999")
    print("  (each = A×111 = A×3×37, Theorem 157)")


if __name__ == "__main__":
    run_assertions()
    summarise()
