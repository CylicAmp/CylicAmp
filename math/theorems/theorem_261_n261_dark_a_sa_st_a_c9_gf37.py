"""
T261: n=261 — DARK_A orbit, SA_ST_A × C9 closure
GF(37) — 137-map f(x) = 26x mod 37

261 = 3² × 29 = 9 × 29
261 mod 37 = 2 ∈ DARK_A = {2, 15, 20}

Central results:
  261 = C3² × C9: C3²=SA_ST_A; SA_ST_A × C9 = DARK_A (all 9 pairs)
  137-orbit of 2: 2→15→20→2 (complete DARK_A orbit)
  2×261+1 = 523 prime; 523 mod 37 = 5 ∈ CAS_EXT
  (261-1)/2 = 130 ∈ CAS_EXT: same orbit as 523; 130 is T245
  DR(261) = 9 ∈ SA_ST_A: DR equals the first factor of 261
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

n = 261

# ── Part 1: Identity and factorization ────────────────────────────────────────

assert n == 9 * 29
assert n == 3**2 * 29
assert not is_prime(n)
assert is_prime(29)

r = n % 37
assert r == 2
assert orbit_of(n) == "DARK_A"

assert orbit_of(9)  == "SA_ST_A"
assert orbit_of(29) == "C9"

print(f"Part 1 PASS: {n} = 3²×29 = 9×29; {n} mod 37 = {r} ∈ DARK_A")
print(f"  9 ∈ SA_ST_A; 29 ∈ C9 (prime)")

# ── Part 2: C3² = SA_ST_A; SA_ST_A × C9 = DARK_A ────────────────────────────

# C3 × C3 = SA_ST_A
for a in ORBITS["C3"]:
    for b in ORBITS["C3"]:
        assert orbit_of(a * b) == "SA_ST_A", f"{a}×{b} not SA_ST_A"

print(f"\nPart 2 PASS: C3 × C3 = SA_ST_A (all 9 pairs)")
print(f"  3²=9∈SA_ST_A: squaring C3 lands in SA_ST_A")

# SA_ST_A × C9 = DARK_A
for a in ORBITS["SA_ST_A"]:
    for b in ORBITS["C9"]:
        assert orbit_of(a * b) == "DARK_A", f"{a}×{b}={(a*b)%37} not DARK_A"

print(f"  SA_ST_A × C9 = DARK_A (all 9 pairs)")
print(f"  Full chain: C3 × C3 × C9 = SA_ST_A × C9 = DARK_A")
print(f"  9×14=126 mod37=15∈DARK_A  9×29=261 mod37=2∈DARK_A  9×31=279 mod37=20∈DARK_A")

# ── Part 3: 137-orbit of 2 — full DARK_A orbit ───────────────────────────────

o1 = f(2); o2 = f(o1); o3 = f(o2)
assert {2, o1, o2} == ORBITS["DARK_A"]
assert o3 == 2

print(f"\nPart 3 PASS: 137-orbit of 2: 2→{o1}→{o2}→2 (complete DARK_A orbit)")

# ── Part 4: 2n+1 and (n-1)/2 both in CAS_EXT ─────────────────────────────────

sg = 2 * n + 1
assert sg == 523
assert is_prime(sg)
assert sg % 37 == 5
assert orbit_of(sg) == "CAS_EXT"

half = (n - 1) // 2
assert half == 130
assert half % 37 == 19
assert orbit_of(half) == "CAS_EXT"

print(f"\nPart 4 PASS: 2n+1 and (n-1)/2 both ∈ CAS_EXT")
print(f"  2×261+1 = 523 prime; 523 mod 37 = 5 ∈ CAS_EXT")
print(f"  (261-1)/2 = 130; 130 mod 37 = 19 ∈ CAS_EXT")
print(f"  130 = T245 (divisor-square-sum theorem); connection T245↔T261")
print(f"  CAS_EXT = {{5,13,19}}: both maps land in this orbit")

# ── Part 5: DR ────────────────────────────────────────────────────────────────

dr_n = dr(n)
assert dr_n == 9
assert orbit_of(dr_n) == "SA_ST_A"

print(f"\nPart 5: DR(261) = {dr_n} ∈ SA_ST_A")
print(f"  DR(261) = 9 = first factor of 261: DR equals the squared factor")

# ── Part 6: Rule 30 ───────────────────────────────────────────────────────────

r30 = rule30(n)
assert r30 == 397
r30_mod = r30 % 37
assert r30_mod == 27
assert orbit_of(r30) == "NEG_H"

print(f"\nPart 6: R30(261) = {r30}; {r30} mod 37 = {r30_mod} ∈ NEG_H")

# ── Part 7: Riemann floor ─────────────────────────────────────────────────────

T = float(n)
floor_N = int(T * math.log(T / (2 * math.pi)) / (2 * math.pi))
floor_mod = floor_N % 37

print(f"\nPart 7: floor(N(261)) = {floor_N}; mod 37 = {floor_mod} ∈ {orbit_of(floor_N)}")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  n = 261 = 3²×29; mod 37 = 2 ∈ DARK_A")
print(f"  C3²=SA_ST_A; SA_ST_A×C9=DARK_A: all 9+9 pairs verified")
print(f"  137-orbit of 2: 2→{o1}→{o2}→2 (DARK_A orbit)")
print(f"  2n+1=523 prime∈CAS_EXT; (n-1)/2=130∈CAS_EXT (T245)")
print(f"  DR(261)=9∈SA_ST_A = first factor of 261")
print(f"  R30(261)=397 mod37=27∈NEG_H")
print(f"  floor(N(261))={floor_N}; mod37={floor_mod}∈{orbit_of(floor_N)}")
