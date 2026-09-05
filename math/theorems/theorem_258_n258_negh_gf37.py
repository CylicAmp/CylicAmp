"""
T258: n=258 — NEG_H orbit, 2*3*43 factorization
GF(37) — 137-map f(x) = 26x mod 37

258 = 2 * 3 * 43
258 mod 37 = 36 ∈ NEG_H = {11, 27, 36}

Central results:
  36 = p-1 = φ(37): 258 mod 37 = ord((F_37)*) — the multiplicative group order
  NEG_H = {11,27,36}: cube roots of -1 mod 37 (x^3 ≡ -1 ≡ 36 mod 37)
  43 mod 37 = 6 ∈ TESLA; 43 is the PRIME curve group order from T254
  (258-1)/2 = 128 = 2^7 ∈ NQR17: same halving value as T257
  2n+1 = 517; 517 mod 37 = 36 ∈ NEG_H: orbit-stable under doubling+1
"""

ORBITS = {
    "IC":      {1, 10, 26},
    "DARK_A":  {2, 15, 20},
    "C3":      {3, 4, 30},
    "CAS_EXT": {5, 13, 19},
    "TESLA":   {6, 8, 23},
    "D7":      {7, 33, 34},
    "SA_ST_A": {9, 12, 16},
    "NEG_H":   {11, 27, 36},
    "C9":      {14, 29, 31},
    "NQR17":   {17, 22, 35},
    "SEED":    {18, 24, 32},
    "SA_ST_B": {21, 25, 28},
}

def orbit_of(x):
    r = x % 37
    if r == 0: return "SEAM"
    for name, s in ORBITS.items():
        if r in s: return name
    raise ValueError(x)

def f(x): return (26 * x) % 37

def dr(n):
    n = abs(n)
    while n >= 10: n = sum(int(d) for d in str(n))
    return n if n else 9

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

def rule30(n):
    bits = list(map(int, bin(n)[2:]))
    padded = [0] + bits + [0]
    out = [padded[i-1] ^ (padded[i] | padded[i+1]) for i in range(1, len(padded)-1)]
    return int("".join(map(str, out)), 2)

import math

n = 258

# ── Part 1: Identity and factorization ────────────────────────────────────────

assert n == 2 * 3 * 43
assert not is_prime(n)
assert is_prime(43)

r = n % 37
assert r == 36
assert orbit_of(n) == "NEG_H"

# 36 = p-1 = φ(37)
assert r == 37 - 1

print(f"Part 1 PASS: {n} = 2×3×43; {n} mod 37 = {r} ∈ NEG_H = {{11,27,36}}")
print(f"  36 = p-1 = φ(37): the multiplicative group order of F_37")

# ── Part 2: NEG_H = cube roots of -1 ─────────────────────────────────────────
# x^3 ≡ -1 ≡ 36 mod 37 iff x ∈ NEG_H

for x in ORBITS["NEG_H"]:
    assert pow(x, 3, 37) == 36, f"{x}^3 mod 37 != 36"

print(f"\nPart 2 PASS: NEG_H = cube roots of -1 mod 37")
print(f"  11^3 mod 37 = {pow(11,3,37)}, 27^3 mod 37 = {pow(27,3,37)}, 36^3 mod 37 = {pow(36,3,37)}")
print(f"  All ≡ 36 ≡ -1 mod 37")

# 137-orbit of 36
o1 = f(r); o2 = f(o1); o3 = f(o2)
assert {r, o1, o2} == ORBITS["NEG_H"]
assert o3 == r

print(f"  137-orbit of 36: {r}→{o1}→{o2}→{r} (complete NEG_H orbit)")

# ── Part 3: Factor 43 — connection to T254 PRIME curve ───────────────────────
# T254 PRIME curve: y²=x³+2x+9 over F_37 has #E=43 (prime group order)
# 43 mod 37 = 6 ∈ TESLA
# 258 = 2*3*43: contains the PRIME curve order as a factor

assert 43 % 37 == 6
assert orbit_of(43) == "TESLA"
assert is_prime(43)
assert n == 2 * 3 * 43

# Factor orbits
assert orbit_of(2)  == "DARK_A"
assert orbit_of(3)  == "C3"
assert orbit_of(43) == "TESLA"

# Products
p23  = (2 * 3)  % 37   # = 6 ∈ TESLA
p243 = (2 * 43) % 37   # 86 mod 37 = 12 ∈ SA_ST_A
p343 = (3 * 43) % 37   # 129 mod 37 = 18 ∈ SEED
p258 = (2*3*43) % 37   # = 36 ∈ NEG_H

assert p23  == 6  and orbit_of(p23)  == "TESLA"
assert p243 == 12 and orbit_of(p243) == "SA_ST_A"
assert p343 == 18 and orbit_of(p343) == "SEED"
assert p258 == 36 and orbit_of(p258) == "NEG_H"

print(f"\nPart 3 PASS: factor 43 links to T254 PRIME elliptic curve")
print(f"  T254 PRIME curve (#E=43): 43 mod 37 = 6 ∈ TESLA")
print(f"  258 = 2×3×43: DARK_A × C3 × TESLA = NEG_H")
print(f"  Pairwise: 2×3=6∈TESLA  2×43=12∈SA_ST_A  3×43=18∈SEED")
print(f"  3×43=129 mod37=18∈SEED: product of C3 and TESLA lands in SEED orbit")

# ── Part 4: 2n+1 orbit-stable ────────────────────────────────────────────────
# 2*258+1 = 517; 517 mod 37 = 36 ∈ NEG_H (same orbit as 258)

sg = 2 * n + 1
assert sg == 517
assert not is_prime(sg)  # 517 = 11*47
sg_mod = sg % 37
assert sg_mod == 36
assert orbit_of(sg) == "NEG_H"

print(f"\nPart 4 PASS: 2n+1 = 517 = 11×47; 517 mod 37 = {sg_mod} ∈ NEG_H")
print(f"  258 and 517 both ∈ NEG_H: orbit-stable under n → 2n+1")
print(f"  11 ∈ NEG_H, 47 mod37=10 ∈ IC: 517 = NEG_H × IC = NEG_H")
assert orbit_of(11 * (47 % 37)) == orbit_of(11 * 10)
print(f"  NEG_H × IC = {orbit_of(11*10%37)} ✓")

# ── Part 5: Halving — bridge to T257 ─────────────────────────────────────────
# (258-1)/2 = 128 = 2^7; same value as (257-1)/2
# Both T257 and T258 produce 128 under halving

half = (n - 1) // 2
assert half == 128 == 2**7
assert half % 37 == 17
assert orbit_of(half) == "NQR17"

print(f"\nPart 5 PASS: (258-1)/2 = 128 = 2^7; 128 mod 37 = 17 ∈ NQR17")
print(f"  (257-1)/2 = 128 (T257) and (258-1)/2 = 128 (T258): same halving value")
print(f"  Consecutive integers 257 and 258 share the same integer halving result")

# ── Part 6: DR and Rule 30 ────────────────────────────────────────────────────

dr_n = dr(n)
assert dr_n == 6
assert orbit_of(dr_n) == "TESLA"

r30 = rule30(n)
assert r30 == 391
r30_mod = r30 % 37
assert r30_mod == 21
assert orbit_of(r30) == "SA_ST_B"

print(f"\nPart 6: DR(258) = {dr_n} ∈ TESLA")
print(f"  R30(258) = {r30}; {r30} mod 37 = {r30_mod} ∈ SA_ST_B")
print(f"  43 mod 37 = 6 ∈ TESLA = DR(258): factor 43 and DR share the same orbit")

# ── Part 7: Riemann floor ─────────────────────────────────────────────────────

T = float(n)
floor_N = int(T * math.log(T / (2 * math.pi)) / (2 * math.pi))
floor_mod = floor_N % 37

print(f"\nPart 7: floor(N(258)) = {floor_N}; mod 37 = {floor_mod} ∈ {orbit_of(floor_N)}")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  n = 258 = 2×3×43; mod 37 = 36 ∈ NEG_H")
print(f"  36 = p-1 = φ(37): multiplicative group order of F_37")
print(f"  NEG_H = cube roots of -1 mod 37: 11^3=27^3=36^3≡36 mod 37")
print(f"  43 ∈ TESLA = DR(258): factor 43 and DR both land in TESLA")
print(f"  43 = PRIME curve order (T254): 258 contains T254's group order as factor")
print(f"  2n+1=517∈NEG_H: orbit-stable under doubling+1")
print(f"  (258-1)/2=128=2^7∈NQR17: same halving value as T257")
print(f"  R30(258)=391 mod37=21∈SA_ST_B")
print(f"  floor(N(258))={floor_N}; mod37={floor_mod}∈{orbit_of(floor_N)}")
