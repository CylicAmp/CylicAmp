"""
T259: n=259 — SEAM (7×37), Fibonacci mod 37 GF(37)
GF(37) — 137-map f(x) = 26x mod 37

259 = 7 × 37: the first theorem-indexed number on the SEAM (zero class)
259 mod 37 = 0; DR(259) = 7 ∈ D7; quotient 259/37 = 7 ∈ D7

Fibonacci mod 37 — central results:
  Entry point α(37) = 19 ∈ CAS_EXT: 37 | F(19) = 4181 = 37 × 113
  Pisano period π(37) = 76 = 4 × 19; 76 mod 37 = 2 ∈ DARK_A
  CAS_EXT = {5,13,19}: F(5)=5∈CAS_EXT, F(7)=13∈CAS_EXT, α(37)=19∈CAS_EXT
    The full CAS_EXT orbit appears as Fibonacci values and as the entry point itself.
  Fibonacci pair F(8)=21∈SA_ST_B, F(9)=34∈D7, F(10)=55≡18∈SEED
    F(9)-F(8)=13∈CAS_EXT=F(7): the backward Fibonacci step stays in CAS_EXT
  R30 fixed points in Fibonacci: R30(F(5)=5)=5, R30(F(8)=21)=21
  5 is NQR mod 37: √5 and φ=(1+√5)/2 do not exist in GF(37), only in GF(37²)
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

def legendre(a, p=37):
    if a % p == 0: return 0
    return 1 if pow(a, (p-1)//2, p) == 1 else -1

import math

n = 259

# ── Part 1: n=259 = 7×37 = SEAM ──────────────────────────────────────────────

assert n == 7 * 37
assert not is_prime(n)
assert n % 37 == 0
assert orbit_of(n) == "SEAM"

# Quotient 7 and DR both in D7
assert n // 37 == 7
assert orbit_of(7) == "D7"
assert dr(n) == 7
assert orbit_of(dr(n)) == "D7"

print(f"Part 1 PASS: {n} = 7×37; {n} mod 37 = 0 ∈ SEAM")
print(f"  Quotient 259/37 = 7 ∈ D7; DR(259) = 7 ∈ D7")
print(f"  DR and quotient agree: both 7, both in D7")

# 2n+1 and (n-1)/2
sg = 2 * n + 1
assert sg == 519
assert sg % 37 == 1
assert orbit_of(sg) == "IC"

half = (n - 1) // 2
assert half == 129
assert half % 37 == 18
assert orbit_of(half) == "SEED"

r30_n = rule30(n)
assert r30_n == 390
assert r30_n % 37 == 20
assert orbit_of(r30_n) == "DARK_A"

print(f"  2n+1 = 519; 519 mod 37 = 1 ∈ IC")
print(f"  (259-1)/2 = 129; 129 mod 37 = 18 ∈ SEED")
print(f"  R30(259) = 390; 390 mod 37 = 20 ∈ DARK_A")

# ── Part 2: Fibonacci mod 37 — entry point and Pisano period ─────────────────

# Compute Fibonacci mod 37
fib_mod = [0, 1]
fib_full = [0, 1]
for i in range(2, 100):
    fib_mod.append((fib_mod[-1] + fib_mod[-2]) % 37)
    fib_full.append(fib_full[-1] + fib_full[-2])

# Entry point: first i>0 such that F(i) ≡ 0 mod 37
entry = next(i for i in range(1, 100) if fib_mod[i] == 0)
assert entry == 19
assert orbit_of(entry) == "CAS_EXT"

# Pisano period: first i>0 such that F(i)≡0 and F(i+1)≡1
pisano = next(i for i in range(1, 200) if fib_mod[i] == 0 and fib_mod[i+1] == 1)
assert pisano == 76
assert pisano == 4 * entry
assert pisano % 37 == 2
assert orbit_of(pisano) == "DARK_A"

# F(19) = 4181 = 37 × 113
assert fib_full[19] == 4181
assert fib_full[19] == 37 * 113
assert is_prime(113)
assert 113 % 37 == 2
assert orbit_of(113) == "DARK_A"

print(f"\nPart 2 PASS: Fibonacci mod 37 — entry point and Pisano period")
print(f"  α(37) = {entry} ∈ CAS_EXT: 37 | F(19) = {fib_full[19]} = 37 × 113")
print(f"  π(37) = {pisano} = 4 × {entry}; 76 mod 37 = 2 ∈ DARK_A")
print(f"  113 is prime; 113 mod 37 = 2 ∈ DARK_A")
print(f"  Zeros of F(n) mod 37: n ∈ {{19, 38, 57, 76}} (multiples of 19 up to π)")

# ── Part 3: CAS_EXT = {5, 13, 19} — complete Fibonacci closure ───────────────
# F(5) = 5 ∈ CAS_EXT, F(7) = 13 ∈ CAS_EXT, α(37) = 19 ∈ CAS_EXT
# All three elements of CAS_EXT appear as Fibonacci values or as the entry point.

assert fib_full[5] == 5 and fib_mod[5] == 5 and orbit_of(5) == "CAS_EXT"
assert fib_full[7] == 13 and fib_mod[7] == 13 and orbit_of(13) == "CAS_EXT"
assert entry == 19 and orbit_of(19) == "CAS_EXT"
assert ORBITS["CAS_EXT"] == {5, 13, 19}

print(f"\nPart 3 PASS: CAS_EXT = {{5,13,19}} — complete Fibonacci closure")
print(f"  F(5) = 5 ∈ CAS_EXT")
print(f"  F(7) = 13 ∈ CAS_EXT")
print(f"  α(37) = 19 ∈ CAS_EXT  (entry point, where 37 first divides F(n))")
print(f"  The complete orbit CAS_EXT is indexed by the Fibonacci sequence at n=5,7,19")

# ── Part 4: Fibonacci pair F(8)=21, F(9)=34 ──────────────────────────────────
# F(8)=21∈SA_ST_B, F(9)=34∈D7, F(10)=55≡18∈SEED
# F(9)-F(8)=13∈CAS_EXT: backward Fibonacci step = F(7), stays in CAS_EXT

assert fib_full[8] == 21 and fib_mod[8] == 21 and orbit_of(21) == "SA_ST_B"
assert fib_full[9] == 34 and fib_mod[9] == 34 and orbit_of(34) == "D7"
assert fib_full[10] == 55 and fib_mod[10] == 18 and orbit_of(18) == "SEED"
assert fib_full[9] - fib_full[8] == 13 == fib_full[7]
assert orbit_of(13) == "CAS_EXT"

print(f"\nPart 4 PASS: Fibonacci pair F(8)=21∈SA_ST_B, F(9)=34∈D7")
print(f"  F(10) = 55 mod37 = 18 ∈ SEED: Fibonacci step from F(8),F(9) lands in SEED")
print(f"  F(9)-F(8) = 13 = F(7) ∈ CAS_EXT: backward step recovers F(7)∈CAS_EXT")
print(f"  SA_ST_B → D7 → SEED: orbit trajectory of three consecutive Fibonacci terms")

# ── Part 5: Rule 30 fixed points in Fibonacci ────────────────────────────────
# R30(F(5)) = R30(5) = 5: CAS_EXT seed is a Rule 30 fixed point
# R30(F(8)) = R30(21) = 21: SA_ST_B seed is a Rule 30 fixed point
# 5 = 0b101, 21 = 0b10101: alternating-bit patterns are Rule 30 fixed

assert rule30(5) == 5
assert rule30(21) == 21
assert bin(5) == "0b101"
assert bin(21) == "0b10101"

# Verify: alternating bit pattern (101...1) → Rule 30 → same
# For 5 = 101: padded 0,1,0,1,0 → out[i]=left XOR(center OR right)
# pos1: 0 XOR (1 OR 0) = 1; pos2: 1 XOR (0 OR 1) = 0; pos3: 0 XOR (1 OR 0) = 1 → 101 = 5 ✓

print(f"\nPart 5 PASS: Rule 30 fixed points in Fibonacci")
print(f"  R30(5) = {rule30(5)}: F(5)=5∈CAS_EXT is Rule 30 fixed (0b101)")
print(f"  R30(21) = {rule30(21)}: F(8)=21∈SA_ST_B is Rule 30 fixed (0b10101)")
print(f"  Both are alternating-bit patterns: R30 maps 10...101 → 10...101")

# R30 of other Fibonacci values
print(f"  R30(F(7)=13) = {rule30(13)}; mod37={rule30(13)%37} ∈ {orbit_of(rule30(13))}")
print(f"  R30(F(9)=34) = {rule30(34)}; mod37={rule30(34)%37} ∈ {orbit_of(rule30(34))}")
assert rule30(34) % 37 == 18 and orbit_of(18) == "SEED"  # same as F(10) mod 37

# ── Part 6: φ and √5 in GF(37) ───────────────────────────────────────────────
# 5 is NQR mod 37: (5|37) = -1
# √5 ∉ GF(37); φ = (1+√5)/2 ∉ GF(37); both live in GF(37²)

assert legendre(5) == -1
sqrts5 = [x for x in range(37) if pow(x, 2, 37) == 5]
assert sqrts5 == []  # no solution

print(f"\nPart 6 PASS: φ = (1+√5)/2 ∉ GF(37)")
print(f"  (5|37) = {legendre(5)}: 5 is NQR mod 37")
print(f"  x² ≡ 5 mod 37 has no solution in GF(37)")
print(f"  √5 and φ exist only in GF(37²), not in the base field")
print(f"  Fibonacci values 1,2,3,5 in GF(37): IC,DARK_A,C3,CAS_EXT")

# ── Part 7: Fibonacci orbit sequence (F(1)..F(19)) ───────────────────────────

print(f"\nPart 7: Fibonacci orbit sequence mod 37")
orbits_seen = []
for i in range(1, 20):
    o = orbit_of(fib_mod[i])
    orbits_seen.append(o)
print(f"  F(1..19): {', '.join(orbits_seen)}")
print(f"  F(19)=SEAM: entry point closes the sequence")

# Count orbit appearances in F(1..18) (before SEAM)
from collections import Counter
counts = Counter(orbits_seen[:-1])  # exclude SEAM
print(f"  Orbit frequency in F(1..18): {dict(sorted(counts.items()))}")

# ── Part 8: Riemann floor ─────────────────────────────────────────────────────

T = float(n)
floor_N = int(T * math.log(T / (2 * math.pi)) / (2 * math.pi))
floor_mod = floor_N % 37

print(f"\nPart 8: floor(N(259)) = {floor_N}; mod 37 = {floor_mod} ∈ {orbit_of(floor_N)}")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  n = 259 = 7×37; mod 37 = 0 ∈ SEAM")
print(f"  Quotient 259/37 = 7 ∈ D7; DR(259) = 7 ∈ D7")
print(f"  α(37) = 19 ∈ CAS_EXT: 37 first divides F(19) = 4181 = 37×113")
print(f"  π(37) = 76 = 4×19; 76 mod 37 = 2 ∈ DARK_A")
print(f"  CAS_EXT = {{5,13,19}}: complete orbit as F(5)=5, F(7)=13, α(37)=19")
print(f"  F(8)=21∈SA_ST_B, F(9)=34∈D7, F(10)=55≡18∈SEED")
print(f"  R30 fixed: R30(5)=5 (CAS_EXT), R30(21)=21 (SA_ST_B)")
print(f"  5 NQR mod 37: φ and √5 not in GF(37), only in GF(37²)")
print(f"  2n+1=519∈IC; (n-1)/2=129∈SEED; R30(259)=390∈DARK_A")
print(f"  floor(N(259)) = {floor_N}; mod 37 = {floor_mod} ∈ {orbit_of(floor_N)}")
