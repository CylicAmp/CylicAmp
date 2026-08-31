"""
T260: n=260 — IC orbit, CAS_EXT self-product closure
GF(37) framework — 137-map f(x) = 26x mod 37

260 = 2² × 5 × 13 = 4 × 5 × 13
260 mod 37 = 1 ∈ IC = {1, 10, 26}

Central results:
  260 mod 37 = 1: the IC seed (identity element of orbit multiplication)
  260 = C3 × CAS_EXT × CAS_EXT: factor orbits multiply to IC
  CAS_EXT × CAS_EXT = SA_ST_B: {5,13,19}² ⊂ SA_ST_B = {21,25,28}
  C3 × SA_ST_B = IC: the three-orbit chain closes at identity
  2×260+1 = 521 prime; 521 mod 37 = 3 ∈ C3
  DR(260) = 8 ∈ TESLA; floor(N(260)) mod 37 = 6 ∈ TESLA
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

n = 260

# ── Part 1: Identity and factorization ────────────────────────────────────────

assert n == 4 * 5 * 13
assert n == 2**2 * 5 * 13
assert not is_prime(n)

r = n % 37
assert r == 1
assert orbit_of(n) == "IC"

print(f"Part 1 PASS: {n} = 2²×5×13; {n} mod 37 = {r} ∈ IC = {{1,10,26}}")
print(f"  IC is the identity orbit: IC × any_orbit = any_orbit")

# ── Part 2: Factor orbit chain — CAS_EXT² = SA_ST_B → IC ─────────────────────

assert orbit_of(4)  == "C3"
assert orbit_of(5)  == "CAS_EXT"
assert orbit_of(13) == "CAS_EXT"

# CAS_EXT × CAS_EXT: all pairwise products land in SA_ST_B
for a in ORBITS["CAS_EXT"]:
    for b in ORBITS["CAS_EXT"]:
        assert orbit_of(a * b) == "SA_ST_B", f"{a}×{b}={(a*b)%37} not in SA_ST_B"

print(f"\nPart 2 PASS: CAS_EXT × CAS_EXT = SA_ST_B")
print(f"  5×5=25∈SA_ST_B  5×13=65 mod37=28∈SA_ST_B  13×13=169 mod37=21∈SA_ST_B")
print(f"  All 9 products of CAS_EXT pairs land in SA_ST_B")

# C3 × SA_ST_B = IC
for a in ORBITS["C3"]:
    for b in ORBITS["SA_ST_B"]:
        assert orbit_of(a * b) == "IC", f"{a}×{b}={(a*b)%37} not in IC"

print(f"  C3 × SA_ST_B = IC (verified all 9 pairs)")
print(f"  Chain: C3 × CAS_EXT × CAS_EXT = C3 × SA_ST_B = IC")

# Pairwise factor products
p45   = (4  * 5)  % 37   # = 20 ∈ DARK_A
p413  = (4  * 13) % 37   # = 52 mod 37 = 15 ∈ DARK_A
p513  = (5  * 13) % 37   # = 65 mod 37 = 28 ∈ SA_ST_B
p4513 = (4  * 5 * 13) % 37  # = 1 ∈ IC

assert p45  == 20 and orbit_of(p45)  == "DARK_A"
assert p413 == 15 and orbit_of(p413) == "DARK_A"
assert p513 == 28 and orbit_of(p513) == "SA_ST_B"
assert p4513 == 1 and orbit_of(p4513) == "IC"

print(f"  Pairwise: 4×5=20∈DARK_A  4×13=15∈DARK_A  5×13=28∈SA_ST_B")
print(f"  4×5×13=260 mod37=1∈IC")

# ── Part 3: 137-orbit of 1 — full IC orbit ────────────────────────────────────

o1 = f(1); o2 = f(o1); o3 = f(o2)
assert {1, o1, o2} == ORBITS["IC"]
assert o3 == 1

print(f"\nPart 3 PASS: 137-orbit of 1: 1→{o1}→{o2}→1 (complete IC orbit)")
print(f"  IC = {{1, 26, 10}} = {{1, MULT, MULT²}} = {{1, Sigma, Sigma⁻¹}}")

# ── Part 4: 2n+1 = 521 prime ──────────────────────────────────────────────────

sg = 2 * n + 1
assert sg == 521
assert is_prime(sg)
assert sg % 37 == 3
assert orbit_of(sg) == "C3"

print(f"\nPart 4 PASS: 2×260+1 = 521 prime; 521 mod 37 = 3 ∈ C3")
print(f"  260 ∈ IC; 2×260+1 = 521 ∈ C3")
print(f"  521 is prime; (521-1)/2 = 260 = n")

# ── Part 5: DR and Rule 30 ────────────────────────────────────────────────────

dr_n = dr(n)
assert dr_n == 8
assert orbit_of(dr_n) == "TESLA"

r30 = rule30(n)
assert r30 == 398
r30_mod = r30 % 37
assert r30_mod == 28
assert orbit_of(r30) == "SA_ST_B"

print(f"\nPart 5: DR(260) = {dr_n} ∈ TESLA")
print(f"  R30(260) = {r30}; {r30} mod 37 = {r30_mod} ∈ SA_ST_B")
print(f"  R30 output orbit SA_ST_B = CAS_EXT²: same orbit as the self-product closure")

# ── Part 6: Riemann floor ─────────────────────────────────────────────────────

T = float(n)
floor_N = int(T * math.log(T / (2 * math.pi)) / (2 * math.pi))
floor_mod = floor_N % 37
assert floor_mod == 6
assert orbit_of(floor_N) == "TESLA"

print(f"\nPart 6: floor(N(260)) = {floor_N}; mod 37 = {floor_mod} ∈ TESLA")
print(f"  DR(260) = 8 ∈ TESLA; floor(N(260)) mod 37 = 6 ∈ TESLA")
print(f"  DR and Riemann floor share orbit TESLA")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  n = 260 = 2²×5×13; mod 37 = 1 ∈ IC")
print(f"  CAS_EXT × CAS_EXT = SA_ST_B (all 9 pairs verified)")
print(f"  C3 × SA_ST_B = IC: chain C3×CAS_EXT×CAS_EXT = IC")
print(f"  Pairwise: 4×5=20∈DARK_A  4×13=15∈DARK_A  5×13=28∈SA_ST_B")
print(f"  137-orbit of 1: 1→26→10→1 (IC = {{1,Sigma,Sigma⁻¹}})")
print(f"  2n+1=521 prime; 521 mod37=3∈C3")
print(f"  DR(260)=8∈TESLA; R30(260)=398 mod37=28∈SA_ST_B")
print(f"  floor(N(260))={floor_N}; mod37={floor_mod}∈TESLA = DR orbit")
