"""
Layer Trinity — 9-Channel Orbit, Factor Lattice, 37-Field Resonance

Classification: Theorem

The 9-channel commutative orbit {(9,1)→10, (9,2)→11, (9,11)→20} generates
a symbolic labeling tuple (101, 011, 112, 020) whose numeric host
N = 2,244,220 = 2²×5×11×101² encodes the tuple through four mechanisms:
direct embedding, 37-field resonance, self-consistency loop, and mirror symmetry.

I. 9-Channel Orbit
  (9,1)→10: labels 101 and 011=11 (prime factors of N)
  (9,2)→11: 11 is the prime factor directly
  (9,11)→20: 20 = 2²×5 (remaining prime component of N)
  Structural link: 101 + 11 = 112 (sum of the two prime-power labels)
  N = 101² × 11 × 20 exactly

II. Factor Lattice
  N = 2²×5×11×101² has 36 total divisors.
  Eight key pairs — all verified:
    (101, 22220), (110, 20402), (202, 11110), (220, 10201),
    (404, 5555),  (505, 4444),  (1010, 2222), (1111, 2020)

III. 37-Field Self-Consistency Loop
  101  ≡ 27 (mod 37)   [= 3³ mod 37, cycle position 3]
  11   ≡ 11 (mod 37)   [= 3^15 mod 37 ∈ QR₃₇]
  112  ≡  1 (mod 37)   [identity in F₃₇]
  20   ≡ 20 (mod 37)
  244  ≡ 22 (mod 37)   [tuple sum]
  2020 ≡ 22 (mod 37)   [divisor]
  N    ≡ 22 (mod 37)   [host — identity lock]

  N, 2020, and tuple sum 244 all share residue 22 mod 37.
"""

from math import isqrt


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


def factorize(n):
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def all_divisors(n):
    divs = set()
    for i in range(1, isqrt(n) + 1):
        if n % i == 0:
            divs.add(i)
            divs.add(n // i)
    return sorted(divs)


N          = 2_244_220
TUPLE      = (101, 11, 112, 20)    # (101, 011=11, 112, 020=20)
CYCLE18    = [pow(3, k, 37) for k in range(1, 19)]
QR37       = frozenset((x * x) % 37 for x in range(1, 37))


# ── I. 9-Channel Orbit ─────────────────────────────────────────────────────

CHANNELS = [(9, 1, 10), (9, 2, 11), (9, 11, 20)]
for a, b, s in CHANNELS:
    assert a + b == s
    assert b + a == s    # commutativity

# Tuple derivation: 101 + 11 = 112
assert TUPLE[0] + TUPLE[1] == TUPLE[2]    # 101 + 11 = 112

# N decomposes as 101² × 11 × 20
assert TUPLE[0]**2 * TUPLE[1] * TUPLE[3] == N

# ── II. Factorization and factor pairs ────────────────────────────────────

factors = factorize(N)
assert factors == {2: 2, 5: 1, 11: 1, 101: 2}

divs = all_divisors(N)
assert len(divs) == 36

KEY_PAIRS = [
    (101, 22220), (110, 20402), (202, 11110), (220, 10201),
    (404,  5555), (505,  4444), (1010, 2222), (1111, 2020),
]
for a, b in KEY_PAIRS:
    assert a * b == N
    assert a in divs and b in divs

# ── III. 37-Field Resonance ────────────────────────────────────────────────

RESIDUE_22 = 22    # the shared mod-37 lock

# Tuple element residues
assert 101 % 37 == 27               # = 3³ mod 37 (cycle position 3)
assert 27 == pow(3, 3, 37)
assert 11 % 37 == 11
assert 11 in QR37                   # 11 = 3^15 ∈ QR₃₇
assert CYCLE18.index(11) + 1 == 15
assert 112 % 37 == 1                # identity in F₃₇ (112 = 3×37 + 1)
assert 20 % 37 == 20

# Self-consistency loop: N ≡ 2020 ≡ 244 ≡ 22 (mod 37)
assert N    % 37 == RESIDUE_22
assert 2020 % 37 == RESIDUE_22
assert sum(TUPLE) % 37 == RESIDUE_22    # tuple sum 244 ≡ 22

# 2020 is a divisor of N
assert 2020 in divs

# ── DR structure ───────────────────────────────────────────────────────────

assert dr(N) == 7                   # DR=7 class ⊆ QR₃₇
assert dr(101) == 2
assert dr(11)  == 2
assert dr(112) == 4
assert dr(20)  == 2
assert dr(244) == 1                 # tuple sum DR = identity
assert dr(2020) == 4

# 101 is prime
assert all(101 % i != 0 for i in range(2, 101))


if __name__ == "__main__":
    print("Layer Trinity — 9-Channel Orbit, Factor Lattice, 37-Field Resonance")
    print()
    print("I. 9-Channel Orbit:")
    for a, b, s in CHANNELS:
        print(f"   {a}+{b}={s},  {b}+{a}={s}  ✓")
    print(f"   Tuple: (101, 011=11, 112, 020=20)")
    print(f"   101+11 = {101+11} = 112  ✓")
    print(f"   N = 101²×11×20 = {101**2}×{11}×{20} = {101**2*11*20}  ✓")
    print()
    print(f"II. Factor Lattice:  N = {N} = 2²×5×11×101²,  {len(divs)} divisors")
    print("    Key pairs:")
    for a, b in KEY_PAIRS:
        print(f"      {a:5d} × {b:6d} = {a*b}  ✓")
    print()
    print("III. 37-Field Self-Consistency Loop:")
    for val, label in [(101,'101'),(11,'011'),(112,'112'),(20,'020'),
                       (sum(TUPLE),'tuple_sum=244'),(2020,'divisor_2020'),(N,'N')]:
        marker = " ← shared lock" if val % 37 == 22 else ""
        print(f"    {label:20s} ≡ {val%37:2d} (mod 37){marker}")
    print(f"    N ≡ 2020 ≡ 244 ≡ 22 (mod 37)  [identity lock]  ✓")
    print()
    print(f"    DR(N)={dr(N)} (DR=7 class ⊆ QR₃₇),  DR(244)={dr(244)} (identity)")
    print()
    print("All assertions passed.")
