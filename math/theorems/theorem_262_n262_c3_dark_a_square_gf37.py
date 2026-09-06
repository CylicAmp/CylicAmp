"""
T262: n=262 — C3 orbit, DARK_A self-product closure
GF(37) — 137-map f(x) = 26x mod 37

262 = 2 × 131
262 mod 37 = 3 ∈ C3 = {3, 4, 30}

Central results:
  2 ∈ DARK_A; 131 mod 37 = 20 ∈ DARK_A
  DARK_A × DARK_A = C3: two DARK_A factors produce C3
  137-orbit of 3: 3→4→30→3 (complete C3 orbit)
  DR(262) = 1 ∈ IC
  2×262+1 = 525 = 3×5²×7; not prime; 525 mod 37 = 7 ∈ D7
  (262-1)/2 = 130 mod 37 = 19 ∈ CAS_EXT (T245 connection)
  2×131+1 = 263 prime; 263 mod 37 = 4 ∈ C3
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

n = 262

# ── Part 1: Identity and factorization ────────────────────────────────────────

assert n == 2 * 131
assert not is_prime(n)
assert is_prime(131)

r = n % 37
assert r == 3
assert orbit_of(n) == "C3"

assert orbit_of(2)   == "DARK_A"
assert 131 % 37 == 20
assert orbit_of(131) == "DARK_A"

print(f"Part 1 PASS: {n} = 2×131; {n} mod 37 = {r} ∈ C3")
print(f"  2 ∈ DARK_A; 131 mod 37 = 20 ∈ DARK_A")

# ── Part 2: DARK_A × DARK_A = C3 ─────────────────────────────────────────────

for a in ORBITS["DARK_A"]:
    for b in ORBITS["DARK_A"]:
        assert orbit_of(a * b) == "C3", f"{a}×{b}={(a*b)%37} not in C3"

print(f"\nPart 2 PASS: DARK_A × DARK_A = C3 (all 9 pairs)")
print(f"  2×2=4∈C3  2×15=30∈C3  2×20=3∈C3")
print(f"  15×15=225 mod37=3∈C3  15×20=300 mod37=4∈C3  20×20=400 mod37=30∈C3")

# 137-orbit of 3
o1 = f(3); o2 = f(o1); o3 = f(o2)
assert {3, o1, o2} == ORBITS["C3"]
assert o3 == 3

print(f"\nPart 3 PASS: 137-orbit of 3: 3→{o1}→{o2}→3 (complete C3 orbit)")

# ── Part 4: 2×131+1 = 263 prime, both in C3 ──────────────────────────────────

twin_p = 2 * 131 + 1
assert twin_p == 263
assert is_prime(263)
assert 263 % 37 == 4
assert orbit_of(263) == "C3"

print(f"\nPart 4 PASS: 2×131+1 = 263 prime; 263 mod 37 = 4 ∈ C3")
print(f"  131 ∈ DARK_A; 263 = 2×131+1 ∈ C3")
print(f"  262 mod37=3∈C3; 263 mod37=4∈C3: consecutive integers, same orbit")

# ── Part 5: (n-1)/2 = 130 ∈ CAS_EXT — T245 connection ───────────────────────

half = (n - 1) // 2
assert half == 130
assert half % 37 == 19
assert orbit_of(half) == "CAS_EXT"

print(f"\nPart 5 PASS: (262-1)/2 = 130 mod 37 = 19 ∈ CAS_EXT")
print(f"  130 = T245; CAS_EXT connection T245↔T261↔T262")

# ── Part 6: DR and Rule 30 ────────────────────────────────────────────────────

dr_n = dr(n)
assert dr_n == 1
assert orbit_of(dr_n) == "IC"

r30 = rule30(n)
assert r30 == 397
r30_mod = r30 % 37
assert r30_mod == 27
assert orbit_of(r30) == "NEG_H"

print(f"\nPart 6: DR(262) = {dr_n} ∈ IC")
print(f"  R30(262) = {r30}; mod 37 = {r30_mod} ∈ NEG_H")

# ── Part 7: Riemann floor ─────────────────────────────────────────────────────

T = float(n)
floor_N = int(T * math.log(T / (2 * math.pi)) / (2 * math.pi))
floor_mod = floor_N % 37

print(f"\nPart 7: floor(N(262)) = {floor_N}; mod 37 = {floor_mod} ∈ {orbit_of(floor_N)}")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  n = 262 = 2×131; mod 37 = 3 ∈ C3")
print(f"  2∈DARK_A; 131 mod37=20∈DARK_A; DARK_A×DARK_A=C3 (all 9 pairs)")
print(f"  137-orbit of 3: 3→{o1}→{o2}→3")
print(f"  2×131+1=263 prime∈C3; 262 and 263 consecutive, both C3")
print(f"  (262-1)/2=130∈CAS_EXT (T245)")
print(f"  DR(262)=1∈IC; R30(262)=397 mod37=27∈NEG_H")
print(f"  floor(N(262))={floor_N}; mod37={floor_mod}∈{orbit_of(floor_N)}")
