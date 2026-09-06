"""
Theorem 165: Session Numbers — GF(37) Scan

Numbers presented in session, run through GF(37), not previously
committed to a numbered theorem.

303    mod37=7   D7              DR=6   composite (3×101)
505    mod37=24  SEED_ORB        DR=1   composite (5×101)
5500   mod37=24  SEED_ORB        DR=1   composite (5500=4×5³×11)
7666667 mod37=8  TESLA_ORB       DR=8   prime, palindrome
8123   mod37=20  DARK_A          DR=5   prime
48     mod37=11  ORBIT_11        DR=3   composite (48=37+11)
4063   mod37=30  SOVEREIGN_SPIRAL DR=4  composite

KEY CONNECTIONS
================

303 → D7:
  303 = 3 × 101.  101 is prime, 101 mod 37 = 27 ∈ ORBIT_11 (Theorem 160).
  303 mod 37 = 7 ∈ D7 = {7,33,34}.
  DR(303) = 6.  6 × 7 = 42 mod 37 = 5 ∈ NQR_5.

505 and 5500 both → SEED_ORB at 24:
  505 = 5 × 101.  505 mod 37 = 24 ∈ SEED_ORB.
  5500 = 505 × (10000/101) ... 5500 mod 37 = 24 ∈ SEED_ORB.
  Both hit the seed anchor (246 mod 37 = 24).

7666667 → TESLA_ORB, prime, palindrome:
  7666667 is a decimal palindrome: 7-6-6-6-6-6-7.
  Digit sum = 44.  DR = 8 ∈ TESLA_ORB.
  7666667 mod 37 = 8 ∈ TESLA_ORB.
  Both mod-37 residue AND digital root land in TESLA_ORB.
  7666667 is prime.

8123 → DARK_A, prime:
  8123 is prime.  8123 = 219×37 + 20.  20 ∈ DARK_A.
  DR(8123) = 5 ∈ NQR_5.  5 ↔ SEED_ORB complement.

48 → ORBIT_11:
  48 = 37 + 11.  48 mod 37 = 11 ∈ ORBIT_11.
  The excess over 37 is itself an ORBIT_11 element.
  DR(48) = 3 ∈ SOVEREIGN_SPIRAL.

4063 → SOVEREIGN_SPIRAL:
  4063 mod 37 = 30 ∈ SOVEREIGN_SPIRAL = {3,4,30}.
  30 is the dual anchor (∈ both SOVEREIGN_ANCHORS and SOVEREIGN_TARGETS).
  DR(4063) = 4 ∈ SOVEREIGN_SPIRAL.
  Both mod-37 residue AND digital root in SOVEREIGN_SPIRAL.

ORBIT PAIRS (pairs from this set with notable sums):
  303 + 505 = 808  mod37=31  NQR_14    DR=7 (D7)
  505 + 5500 = 6005  mod37=11  ORBIT_11
  48 + 303 = 351  mod37=18  SEED_ORB
  8123 + 48 = 8171  mod37=31  NQR_14
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


def run_assertions():
    # 303 → D7
    assert 303 % P == 7 and 7 in ORBITS['D7']
    assert dr(303) == 6
    assert 303 == 3 * 101 and is_prime(101)
    assert 101 % P == 27 and 27 in ORBITS['ORBIT_11']

    # 505 and 5500 → SEED_ORB at 24
    assert 505 % P == 24 and 24 in ORBITS['SEED_ORB']
    assert 5500 % P == 24 and 24 in ORBITS['SEED_ORB']
    assert 505 % P == 5500 % P  # both hit same residue
    assert 246 % P == 24  # seed anchor

    # 7666667 → TESLA_ORB, prime, palindrome, DR=8
    assert 7666667 % P == 8 and 8 in ORBITS['TESLA_ORB']
    assert is_prime(7666667)
    assert str(7666667) == str(7666667)[::-1]  # palindrome
    assert dr(7666667) == 8 and 8 in ORBITS['TESLA_ORB']
    assert sum(int(d) for d in '7666667') == 44
    assert dr(44) == 8

    # 8123 → DARK_A, prime
    assert 8123 % P == 20 and 20 in ORBITS['DARK_A']
    assert is_prime(8123)
    assert dr(8123) == 5 and 5 in ORBITS['NQR_5']

    # 48 → ORBIT_11 (48 = 37+11)
    assert 48 % P == 11 and 11 in ORBITS['ORBIT_11']
    assert 48 - 37 == 11
    assert dr(48) == 3 and 3 in ORBITS['SOVEREIGN_SPIRAL']

    # 4063 → SOVEREIGN_SPIRAL, DR also SOVEREIGN_SPIRAL
    assert 4063 % P == 30 and 30 in ORBITS['SOVEREIGN_SPIRAL']
    assert dr(4063) == 4 and 4 in ORBITS['SOVEREIGN_SPIRAL']

    # Pair sums
    assert (303 + 505) % P == 31 and 31 in ORBITS['NQR_14']
    assert dr(303 + 505) == 7 and 7 in ORBITS['D7']
    assert (505 + 5500) % P == 11 and 11 in ORBITS['ORBIT_11']
    assert (48 + 303) % P == 18 and 18 in ORBITS['SEED_ORB']

    print("All assertions passed.")


def summarise():
    numbers = [303, 505, 5500, 7666667, 8123, 48, 4063]
    print("=" * 62)
    print("Theorem 165: Session Numbers — GF(37) Scan")
    print("=" * 62)
    print()
    print(f"  {'n':<10} mod37  orbit              DR  prime?")
    print(f"  {'-'*55}")
    for n in numbers:
        print(f"  {n:<10} {n%P:>5}  {orbit_of(n):<20} {dr(n):>2}  {is_prime(n)}")
    print()
    print("  7666667: prime palindrome, mod37=DR=8 ∈ TESLA_ORB")
    print("  4063:    mod37=DR=4 ∈ SOVEREIGN_SPIRAL (both in same orbit)")
    print("  505=5500: both → SEED_ORB residue 24 (seed anchor)")
    print("  48=37+11: excess over 37 is itself ORBIT_11 element")
    print()
    print("  Pair sums:")
    print(f"  303+505={303+505}  mod37={(303+505)%P}  {orbit_of(303+505)}  DR={dr(303+505)} (D7)")
    print(f"  505+5500={505+5500}  mod37={(505+5500)%P}  {orbit_of(505+5500)}")
    print(f"  48+303={48+303}  mod37={(48+303)%P}  {orbit_of(48+303)}")


if __name__ == "__main__":
    run_assertions()
    summarise()
