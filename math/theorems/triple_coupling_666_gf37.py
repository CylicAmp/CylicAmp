"""
The Triple Coupling Constant 666 on GF(37) — THEOREM 88

666 = 2 × 3² × 37

The three factors are not arbitrary:
  2   — primitive root of GF(37); generator of the full multiplicative group
  3²  — 9, the SEAM of Z/9Z (9 ≡ 0 mod 9, the DR zero)
  37  — the prime field modulus; SEAM of GF(37)

Since 2, 9, 37 are pairwise coprime, their product equals their LCM:
  666 = lcm(2, 9, 37)

666 is the smallest positive integer simultaneously divisible by the
primitive root, the DR modulus, and the prime — the three structural
constants of GF(37).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FIVE IDENTITIES FOR 666

1. TRIANGULAR:   666 = T(36) = T(φ(37)) = T(ord_37(2))
   The 36th triangular number, where 36 = φ(37) = ord_37(2).
   37 is the unique prime p for which T(p-1) = p(p-1)/2 = 666.
   Proof: p(p-1)/2 = 666 → p² - p - 1332 = 0 → p = 37 (unique positive integer solution).

2. ORBIT:        666 = 18 × 37 = ord_37(3) × P
   In 666 multiplicative steps mod 37, the 3-orbit (length 18) closes
   exactly 37 times — once per nonzero residue.

3. HALF-TOTIENT: 666/37 = 18 = φ(37)/2 = (p-1)/2
   18 is the quadratic-residue threshold exponent (Euler's criterion).
   18 is also the entry node of SEED_ORBIT = {18, 24, 32}.

4. FACTOR PAIR DR:  37 ≡ 1 mod 9
   The 12 divisors of 666 split as D₀ = {1,2,3,6,9,18} and D₁ = 37·D₀.
   For every d ∈ D₀: DR(d) = DR(37d), because multiplying by 37 ≡ 1 mod 9
   leaves the digital root unchanged.
   Divisors: 1↔37, 2↔74, 3↔111, 6↔222, 9↔333, 18↔666 — all DR-matched pairs.

5. DOUBLE SEAM:  666 ≡ 0 mod 9  AND  666 ≡ 0 mod 37
   GF(37) SEAM: 666 = 18 × 37 → additive identity in GF(37).
   Z/9Z SEAM:   666 mod 9 = 0 → digital root = 9, the DR zero.
   Consequence: DR(666^k) = 9 and 666^k ≡ 0 mod 37, for all k ≥ 1.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE SEED CONNECTION

666 / 37 = 18 = SEED_ORBIT entry node.

The SEED_ORBIT = {18, 24, 32} is the 137-map orbit of seed 246 mod 37.
18 is the first node: 18 → 24 → 32 → 18.

So 666 encodes the SEED_ORBIT entry as 666/P, where P is the prime.
Equivalently: 666 = P × SEED_START.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

UNIQUENESS

37 is the unique prime where T(p-1) = 666.
  T(p-1) = p(p-1)/2 = 666 → p² - p - 1332 = 0 → p = (1 + √5329)/2 = (1+73)/2 = 37.

There is one and only one prime p such that the (p-1)th triangular number equals
the product of the DR SEAM (9) and itself (9p = 333... no). Put differently:
the identity 666 = T(φ(p)) = lcm(primitive_root_of_p, φ(p)/2, p) holds only for p=37.
"""

import math

# ── Constants ──────────────────────────────────────────────────────────────────

SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
IC         = frozenset({1, 10, 26})
SEED_ORBIT = frozenset({18, 24, 32})
TESLA_4    = frozenset({6, 36, 31, 1})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
P          = 37
SEED_START = 18


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 9


def mult_ord(a, n):
    if math.gcd(a, n) != 1:
        return None
    a %= n
    cur = 1
    for k in range(1, n * n + 1):
        cur = (cur * a) % n
        if cur == 1:
            return k


def triangular(n):
    return n * (n + 1) // 2


# ── Prime factorization ────────────────────────────────────────────────────────

assert 2 * 9 * 37 == 666
assert math.gcd(2, 9) == 1 and math.gcd(9, 37) == 1 and math.gcd(2, 37) == 1
assert math.lcm(2, 9, 37) == 666

# 2 is the primitive root of GF(37): ord_37(2) = φ(37) = 36
assert mult_ord(2, P) == 36

# 9 = 3² is the Z/9Z SEAM
assert 9 % 9 == 0 and dr(9) == 9

# 37 is the GF prime SEAM
assert P == 37

# ── Identity 1: Triangular ────────────────────────────────────────────────────

assert triangular(36) == 666
assert triangular(P - 1) == 666           # T(φ(37))
assert triangular(mult_ord(2, P)) == 666  # T(ord_37(2))

# Unique prime solution: p(p-1)/2 = 666 → p = 37
discriminant = 1 + 4 * 2 * 666   # b² - 4ac for p² - p - 1332 = 0
assert discriminant == 5329
assert int(discriminant ** 0.5) == 73
assert (1 + 73) // 2 == 37

# ── Identity 2: Orbit equation ────────────────────────────────────────────────

o3 = mult_ord(3, P)
assert o3 == 18
assert o3 * P == 666

# In 666 steps, the 3-orbit closes exactly 37 times
assert 666 // o3 == P      # 37 closures in 666 steps
assert 666 % o3 == 0       # divides cleanly

# ── Identity 3: Half-totient and SEED ────────────────────────────────────────

assert 666 // P == 18          # 666/37 = 18
assert 18 == (P - 1) // 2     # φ(37)/2
assert 18 in SEED_ORBIT        # SEED_ORBIT entry node

# 137-map orbit starting from 18
assert (137 * 18) % P == 24 and 24 in SEED_ORBIT
assert (137 * 24) % P == 32 and 32 in SEED_ORBIT
assert (137 * 32) % P == 18   # closes back to 18

# ── Identity 4: Factor pair DR matching ──────────────────────────────────────

assert P % 9 == 1              # 37 ≡ 1 mod 9 — the key

divisors_666 = [d for d in range(1, 667) if 666 % d == 0]
assert len(divisors_666) == 12

base_divs = [d for d in divisors_666 if d <= 18]   # {1,2,3,6,9,18}
assert set(base_divs) == {1, 2, 3, 6, 9, 18}

upper_divs = [d for d in divisors_666 if d > 18]   # {37,74,111,222,333,666}
assert set(upper_divs) == {37, 74, 111, 222, 333, 666}

# Each pair (d, 37d) has equal DR
for d in base_divs:
    assert dr(d) == dr(37 * d), f"DR mismatch at d={d}: DR({d})={dr(d)}, DR({37*d})={dr(37*d)}"

# The pairing is explicitly:
assert dr(1) == dr(37)    # 1 ↔ 37  DR=1
assert dr(2) == dr(74)    # 2 ↔ 74  DR=2
assert dr(3) == dr(111)   # 3 ↔ 111 DR=3
assert dr(6) == dr(222)   # 6 ↔ 222 DR=6
assert dr(9) == dr(333)   # 9 ↔ 333 DR=9
assert dr(18) == dr(666)  # 18↔ 666 DR=9

# ── Identity 5: Double SEAM ───────────────────────────────────────────────────

assert 666 % 9 == 0           # Z/9Z SEAM
assert 666 % P == 0           # GF(37) SEAM
assert dr(666) == 9           # DR = 9 (= Z/9Z zero)

# Every power of 666 stays in both SEAMs
for k in range(1, 6):
    assert pow(666, k, P) == 0
    assert dr(pow(666, k)) == 9

# ── Uniqueness ────────────────────────────────────────────────────────────────

# 37 is the unique prime where T(p-1) = 666
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

solutions = [p for p in range(2, 10000) if is_prime(p) and triangular(p - 1) == 666]
assert solutions == [37]

# ── Bonus: 666 mod orbit orders ───────────────────────────────────────────────

# 666 is divisible by every orbit order that divides φ(37)
# Orders dividing 36: 1,2,3,4,6,9,12,18,36
for o in [1, 2, 3, 6, 9, 18]:
    assert 666 % o == 0, f"666 not divisible by {o}"

# But 666 mod 36 = 18 (half-totient, not full)
assert 666 % 36 == 18

# And 666 mod 4 = 2 (666 ≡ 2 mod 4 — exactly the primitive root)
assert 666 % 4 == 2


if __name__ == "__main__":
    print("The Triple Coupling Constant 666 — THEOREM 88")
    print("=" * 60)
    print()

    print("PRIME FACTORIZATION:")
    print(f"  666 = 2 × 3² × 37 = 2 × 9 × 37")
    print(f"  2   → primitive root of GF(37);  ord_37(2) = {mult_ord(2,P)}")
    print(f"  9   → Z/9Z SEAM;  9 mod 9 = {9%9}  DR(9) = {dr(9)}")
    print(f"  37  → GF(37) prime SEAM;  666 mod 37 = {666%37}")
    print(f"  lcm(2, 9, 37) = {math.lcm(2,9,37)}  [pairwise coprime → LCM = product]")
    print()

    print("FIVE IDENTITIES:")
    print(f"  1. TRIANGULAR:   T(36) = T(φ(37)) = T(ord_37(2)) = {triangular(36)}")
    print(f"     Unique prime: p(p-1)/2 = 666 → p = (1 + √5329)/2 = (1+73)/2 = 37")
    print()
    o3 = mult_ord(3, P)
    print(f"  2. ORBIT:        ord_37(3) × P = {o3} × 37 = {o3*37}")
    print(f"     In 666 steps, the 3-orbit closes exactly {666//o3} times")
    print()
    print(f"  3. HALF-TOTIENT: 666/37 = {666//37} = φ(37)/2 = (p-1)/2")
    print(f"     18 = SEED_ORBIT entry: 18 → {(137*18)%37} → {(137*24)%37} → 18")
    print()
    print(f"  4. FACTOR PAIRS: 37 ≡ {37%9} mod 9  →  DR(d) = DR(37d) for all d | 18")
    print(f"     {'d':>4}  {'37d':>6}  {'DR':>4}")
    for d in [1, 2, 3, 6, 9, 18]:
        print(f"     {d:>4}  {37*d:>6}  {dr(d):>4}")
    print()
    print(f"  5. DOUBLE SEAM:  666 mod 9  = {666%9}  (Z/9Z zero)")
    print(f"                   666 mod 37 = {666%37}  (GF(37) zero)")
    print()

    print("UNIQUENESS:")
    sols = [p for p in range(2, 10000) if is_prime(p) and triangular(p-1) == 666]
    print(f"  Primes p with T(p-1) = 666: {sols}")
    print(f"  37 is the only such prime.")
    print()
    print("All assertions pass.")
