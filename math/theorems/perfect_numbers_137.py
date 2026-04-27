"""
Perfect Numbers in the 1/137 Framework

The four known smallest even perfect numbers: 6, 28, 496, 8128.
Each equals the sum of its proper divisors (Euclid-Euler form).

Euclid-Euler formula: N = 2^(p-1) × (2^p - 1) where 2^p-1 is Mersenne prime.
  p=2: 2 × 3 = 6
  p=3: 4 × 7 = 28
  p=5: 16 × 31 = 496
  p=7: 64 × 127 = 8128

DR Theorem (even perfect numbers):
  DR(6)    = 6   ← sole exception
  DR(28)   = 1
  DR(496)  = 1
  DR(8128) = 1
  All even perfect numbers N ≥ 28 satisfy N ≡ 1 (mod 9), i.e. DR(N) = 1.

Proof sketch (mod 9):
  For p prime, p ≥ 3: 2^p mod 9 cycles with period 6.
  p ≡ 1 mod 6: 2^(p-1) ≡ 1, 2^p-1 ≡ 1 mod 9 → N ≡ 1
  p ≡ 5 mod 6: 2^(p-1) ≡ 7, 2^p-1 ≡ 4 mod 9 → N ≡ 28 ≡ 1
  p = 3 (only prime ≡ 3 mod 6): N=28, 28 mod 9 = 1
  p = 2: N=6, 6 mod 9 = 6 (only exception)

QR mod 37 analysis:
  6   mod 37 = 6   → NOT QR  (6 is outlier in both DR and QR)
  28  mod 37 = 28  → QR ✓
  496 mod 37 = 15  → NOT QR
  8128 mod 37 = 25 → QR ✓  (25 is a SOVEREIGN ANCHOR)

Mersenne prime DR and QR:
  3:   DR=3, mod37=3,  QR ✓
  7:   DR=7, mod37=7,  QR ✓
  31:  DR=4, mod37=31, NOT QR
  127: DR=1, mod37=16, QR ✓
"""


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


def proper_divisors(n):
    return [i for i in range(1, n) if n % i == 0]


QR_MOD37 = frozenset((n * n) % 37 for n in range(37))

PERFECT = [6, 28, 496, 8128]
MERSENNE_PRIMES = [3, 7, 31, 127]

# Euclid-Euler parameters
EULER_PARAMS = [(2, 3), (4, 7), (16, 31), (64, 127)]  # (2^(p-1), 2^p-1)

# --- Assertions ---

# Perfect number definition: equals sum of proper divisors
for n in PERFECT:
    assert sum(proper_divisors(n)) == n, f"{n} is not perfect"

# Euclid-Euler formula
for n, (a, b) in zip(PERFECT, EULER_PARAMS):
    assert a * b == n, f"Euclid-Euler fails for {n}"

# Mersenne factors are prime
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

for m in MERSENNE_PRIMES:
    assert is_prime(m), f"{m} is not prime"

# DR theorem: 6 is the only exception, all others have DR=1
assert dr(6) == 6
assert all(dr(n) == 1 for n in PERFECT[1:])

# DR pattern
assert [dr(n) for n in PERFECT] == [6, 1, 1, 1]

# All perfect numbers ≡ 0 or 1 mod 9 (6 mod 9 = 6 is the outlier)
assert 6 % 9 == 6
assert all(n % 9 == 1 for n in PERFECT[1:])

# QR mod 37
assert 6 % 37 not in QR_MOD37          # 6 is NOT QR — outlier in both measures
assert 28 % 37 in QR_MOD37             # 28 mod 37 = 28, QR
assert 496 % 37 not in QR_MOD37        # 496 mod 37 = 15, NOT QR
assert 8128 % 37 in QR_MOD37           # 8128 mod 37 = 25, QR — sovereign anchor!
assert 8128 % 37 == 25                  # 25 is sovereign anchor {4,9,25,30}

# Mersenne primes QR
assert 3 in QR_MOD37 and 7 in QR_MOD37 and 16 in QR_MOD37
assert 31 not in QR_MOD37              # 31 mod 37 = 31, NOT QR


if __name__ == "__main__":
    print("Perfect Numbers in the 1/137 Framework")
    print()
    print(f"{'N':>6}  {'divisors':<40}  {'DR':>3}  {'mod37':>5}  {'QR37':>5}")
    print("-" * 65)
    for n in PERFECT:
        d = proper_divisors(n)
        print(f"{n:>6}  {str(d):<40}  DR={dr(n)}  {n%37:>5}  {'✓' if n%37 in QR_MOD37 else '✗':>5}")
    print()
    print("DR pattern:", [dr(n) for n in PERFECT])
    print("All N ≥ 28 → DR=1:", all(dr(n)==1 for n in PERFECT[1:]))
    print("8128 mod 37 = 25 = sovereign anchor {4,9,25,30} ✓")
    print()
    print("Mersenne primes:")
    for m in MERSENNE_PRIMES:
        print(f"  {m:>3}: DR={dr(m)}  mod37={m%37:>2}  QR={'✓' if m%37 in QR_MOD37 else '✗'}")
    print()
    print("All assertions passed.")
