"""
T263: n=263 — C3 orbit, prime
GF(37) framework — 137-map f(x) = 26x mod 37

263 prime; 263 mod 37 = 4 ∈ C3 = {3, 4, 30}

Central results:
  262 mod37=3∈C3; 263 mod37=4∈C3: consecutive integers, same orbit
  (263-1)/2 = 131; 131 mod 37 = 20 ∈ DARK_A; 131 is prime
  R30(263) = 396; 396 mod 37 = 26 ∈ IC = MULT
  DR(263) = 2 ∈ DARK_A
  C3 primes under 300: {3, 41, 67, 151, 263}
  floor(N(263)) mod 37 = 8 ∈ TESLA
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

def rule30_verbose(n, show=True):
    bits = list(map(int, bin(n)[2:]))
    padded = [0] + bits + [0]
    out = []
    for i in range(1, len(padded)-1):
        left, center, right = padded[i-1], padded[i], padded[i+1]
        val = left ^ (center | right)
        out.append(val)
        if show:
            print(f"    i={i}: {left}{center}{right} -> {val}")
    result = int("".join(map(str, out)), 2)
    if show:
        print(f"    Input:  {n} = 0b{bin(n)[2:]}")
        print(f"    Output: {result} = 0b{''.join(map(str, out))}")
    return result

import math

n = 263

# ── Part 1: Identity ──────────────────────────────────────────────────────────

assert is_prime(n)
r = n % 37
assert r == 4
assert orbit_of(n) == "C3"

assert 262 % 37 == 3 and orbit_of(262) == "C3"
assert 263 % 37 == 4 and orbit_of(263) == "C3"

print(f"Part 1 PASS: {n} prime; {n} mod 37 = {r} ∈ C3")
print(f"  262 mod37=3∈C3; 263 mod37=4∈C3: consecutive integers, same orbit")

# ── Part 2: 137-orbit of 4 ────────────────────────────────────────────────────

o1 = f(4); o2 = f(o1); o3 = f(o2)
assert {4, o1, o2} == ORBITS["C3"]
assert o3 == 4

print(f"\nPart 2 PASS: 137-orbit of 4: 4→{o1}→{o2}→4 (complete C3 orbit)")

# ── Part 3: (n-1)/2 = 131 prime ∈ DARK_A ─────────────────────────────────────

half = (n - 1) // 2
assert half == 131
assert is_prime(131)
assert half % 37 == 20
assert orbit_of(half) == "DARK_A"

print(f"\nPart 3 PASS: (263-1)/2 = 131 prime; 131 mod 37 = 20 ∈ DARK_A")
print(f"  263 ∈ C3; (263-1)/2 = 131 ∈ DARK_A")

# ── Part 4: R30(263) = 396 ∈ IC = MULT ───────────────────────────────────────

print(f"\nPart 4: R30(263) bit trace:")
r30 = rule30_verbose(n, show=True)
assert r30 == 396
r30_mod = r30 % 37
assert r30_mod == 26
assert orbit_of(r30) == "IC"

print(f"\n  R30(263) = {r30}; {r30} mod 37 = {r30_mod} = MULT ∈ IC")
print(f"  Rule 30 output lands on the 137-map multiplier (26 = 137 mod 37)")

# ── Part 5: C3 primes ────────────────────────────────────────────────────────

c3_primes = [p for p in range(2, 300) if is_prime(p) and p % 37 in ORBITS["C3"]]
assert 263 in c3_primes
assert c3_primes == [3, 41, 67, 151, 263]

print(f"\nPart 5: C3 primes under 300: {c3_primes}")
for p in c3_primes:
    print(f"  {p} mod37={p%37} ∈ C3")

# ── Part 6: DR ────────────────────────────────────────────────────────────────

dr_n = dr(n)
assert dr_n == 2
assert orbit_of(dr_n) == "DARK_A"

print(f"\nPart 6: DR(263) = {dr_n} ∈ DARK_A")
print(f"  (263-1)/2=131∈DARK_A; DR(263)=2∈DARK_A: halving and DR agree on orbit")

# ── Part 7: Riemann floor ─────────────────────────────────────────────────────

T = float(n)
floor_N = int(T * math.log(T / (2 * math.pi)) / (2 * math.pi))
floor_mod = floor_N % 37
assert floor_mod == 8
assert orbit_of(floor_N) == "TESLA"

print(f"\nPart 7: floor(N(263)) = {floor_N}; mod 37 = {floor_mod} ∈ TESLA")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  n = 263 prime; mod 37 = 4 ∈ C3")
print(f"  262 and 263 consecutive, both C3")
print(f"  (263-1)/2 = 131 prime ∈ DARK_A")
print(f"  R30(263) = 396 mod37 = 26 = MULT ∈ IC")
print(f"  C3 primes <300: {{3, 41, 67, 151, 263}}")
print(f"  DR(263) = 2 ∈ DARK_A = (n-1)/2 orbit")
print(f"  floor(N(263)) = {floor_N}; mod37={floor_mod} ∈ TESLA")
