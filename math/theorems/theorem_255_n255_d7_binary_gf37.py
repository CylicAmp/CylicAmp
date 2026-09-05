"""
T255: n=255 — D7 orbit, 2^8-1 binary architecture
GF(37) — 137-map f(x) = 26x mod 37

255 = 3 × 5 × 17 = 2^8 - 1 = 0b11111111 (all-ones 8-bit)
255 mod 37 = 33 ∈ D7 = {7, 33, 34}

Central results:
  255 = 2^8 - 1: maximal 8-bit integer; all-ones binary
  R30(255) = 128 = 2^7: all-ones 8-bit → leading-bit-only 7-bit under Rule 30
  Factor triad 3×5×17: C3(QR) × CAS_EXT(NQR) × NQR17(NQR) = D7 (QR)
  (255-1)/2 = 127 = M_7 (Mersenne prime); 255+2 = 257 = F_3 (Fermat prime)
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

QR_ORBITS  = {"C3", "D7", "IC", "NEG_H", "SA_ST_A", "SA_ST_B"}
NQR_ORBITS = {"C9", "CAS_EXT", "DARK_A", "NQR17", "SEED", "TESLA"}

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

n = 255

# ── Part 1: Factorization and binary identity ─────────────────────────────────

assert n == 3 * 5 * 17
assert n == 2**8 - 1
assert bin(n) == "0b11111111"
assert not is_prime(n)

r = n % 37
assert r == 33
assert orbit_of(n) == "D7"

print(f"Part 1 PASS: {n} = 3×5×17 = 2^8-1 = 0b11111111")
print(f"  {n} mod 37 = {r} ∈ D7 = {{7,33,34}}")

# ── Part 2: 137-orbit of 33 — full D7 orbit ──────────────────────────────────

o1 = f(r)    # 26×33 mod 37
o2 = f(o1)
o3 = f(o2)

assert {r, o1, o2} == ORBITS["D7"]
assert o3 == r

print(f"\nPart 2 PASS: 137-orbit of 33: {r} → {o1} → {o2} → {r}")
print(f"  Complete orbit = D7 = {{7,33,34}}")
print(f"  DR({n}) = {dr(n)} ∈ {orbit_of(dr(n))}")

# ── Part 3: Factor orbit triad — C3 × CAS_EXT × NQR17 ───────────────────────
# Factors: 3∈C3(QR), 5∈CAS_EXT(NQR), 17∈NQR17(NQR)
# Product: 255 mod 37 = 33 ∈ D7(QR)

assert orbit_of(3)  == "C3"
assert orbit_of(5)  == "CAS_EXT"
assert orbit_of(17) == "NQR17"

assert orbit_of(3)  in QR_ORBITS
assert orbit_of(5)  in NQR_ORBITS
assert orbit_of(17) in NQR_ORBITS

# Pairwise products
p35  = (3  * 5)  % 37   # = 15 ∈ DARK_A
p317 = (3  * 17) % 37   # = 51 mod 37 = 14 ∈ C9
p517 = (5  * 17) % 37   # = 85 mod 37 = 11 ∈ NEG_H
p255 = (3  * 5 * 17) % 37  # = 255 mod 37 = 33 ∈ D7

assert p35  == 15 and orbit_of(p35)  == "DARK_A"
assert p317 == 14 and orbit_of(p317) == "C9"
assert p517 == 11 and orbit_of(p517) == "NEG_H"
assert p255 == 33 and orbit_of(p255) == "D7"

print(f"\nPart 3 PASS: factor orbit triad")
print(f"  3∈C3(QR)  × 5∈CAS_EXT(NQR) × 17∈NQR17(NQR)  = 33∈D7(QR)")
print(f"  Pairwise: 3×5=15∈DARK_A  3×17=14∈C9  5×17=11∈NEG_H")
print(f"  QR×NQR×NQR = QR  (NQR×NQR=QR; then QR×QR=QR)")

# ── Part 4: Rule 30 — all-ones 8-bit maps to 2^7 ─────────────────────────────
# 255 = 11111111 in binary
# Rule 30 one step: each interior cell = left XOR (center OR right)
# Padded: 0,1,1,1,1,1,1,1,1,0
# Output: 1,0,0,0,0,0,0,0 = 10000000 = 128 = 2^7

r30 = rule30(n)
assert r30 == 128
assert r30 == 2**7
assert bin(r30) == "0b10000000"
r30_mod = r30 % 37
assert r30_mod == 17
assert orbit_of(r30) == "NQR17"

print(f"\nPart 4 PASS: R30(255) = {r30} = 2^7")
print(f"  0b11111111 → R30 → 0b10000000")
print(f"  All-ones 8-bit maps to leading-bit-only 7-bit")
print(f"  128 mod 37 = {r30_mod} ∈ NQR17")
print(f"  D7 (position) → NQR17 (R30 output)")

# ── Part 5: Mersenne and Fermat prime bookends ────────────────────────────────
# (255-1)/2 = 127 = 2^7 - 1 = M_7 (Mersenne prime)
# 255+2    = 257 = 2^8 + 1 = F_3 (Fermat prime)
# 255 sits between Mersenne and Fermat powers of 2

m7 = (n - 1) // 2
assert m7 == 127
assert m7 == 2**7 - 1
assert is_prime(m7)

f3 = n + 2
assert f3 == 257
assert f3 == 2**8 + 1
assert is_prime(f3)

m7_mod = m7 % 37
f3_mod = f3 % 37

assert orbit_of(m7) == "SA_ST_A"   # 127 mod 37 = 16 ∈ SA_ST_A
assert orbit_of(f3) == "NQR17"     # 257 mod 37 = 35 ∈ NQR17

print(f"\nPart 5 PASS: Mersenne/Fermat bookends")
print(f"  (255-1)/2 = 127 = 2^7-1 = M_7 (Mersenne prime)")
print(f"  127 mod 37 = {m7_mod} ∈ SA_ST_A")
print(f"  255+2 = 257 = 2^8+1 = F_3 (Fermat prime)")
print(f"  257 mod 37 = {f3_mod} ∈ NQR17")
print(f"  M_7 ∈ SA_ST_A(QR); F_3 ∈ NQR17(NQR)")
print(f"  255 = (2^7-1)×2+1 = 2×M_7+1 → safe-prime direction: M_7 is (255-1)/2")

# ── Part 6: Riemann floor ─────────────────────────────────────────────────────

T = float(n)
N_T = T * math.log(T / (2 * math.pi)) / (2 * math.pi)
floor_N = int(N_T)
floor_mod = floor_N % 37

print(f"\nPart 6: floor(N({n})) = {floor_N}; mod 37 = {floor_mod} ∈ {orbit_of(floor_N)}")

# ── Part 7: 1/137 connections ─────────────────────────────────────────────────
# 26 = MULT = 137 mod 37; IC = {1,10,26} = {1, MULT, MULT²}

x137  = (n * 137) % 37   # 255 × 137 mod 37
div137 = (n * 10) % 37   # 255 ÷ 137 ≡ 255 × 137⁻¹ ≡ 255 × 10 mod 37 (10∈IC = 26⁻¹)
mod137 = n % 137

print(f"\nPart 7: 1/137 connections")
print(f"  255 × 137 mod 37 = {x137} ∈ {orbit_of(x137)}")
print(f"  255 × 10 mod 37  = {div137} ∈ {orbit_of(div137)}  (÷137 via MULT⁻¹=10)")
print(f"  255 mod 137      = {mod137} ∈ {orbit_of(mod137)}")

# ── Part 8: QR/NQR parity of the factor triad ────────────────────────────────
# Legendre symbols: (3|37), (5|37), (17|37)

def legendre(a, p=37):
    if a % p == 0: return 0
    return 1 if pow(a, (p-1)//2, p) == 1 else -1

leg3  = legendre(3)
leg5  = legendre(5)
leg17 = legendre(17)

assert leg3  == 1,  f"Legendre(3|37)  = {leg3},  expected +1 (QR)"
assert leg5  == -1, f"Legendre(5|37)  = {leg5},  expected -1 (NQR)"
assert leg17 == -1, f"Legendre(17|37) = {leg17}, expected -1 (NQR)"

# Product of Legendre symbols = Legendre of product
product_leg = leg3 * leg5 * leg17
leg255 = legendre(255)
assert product_leg == leg255 == 1

print(f"\nPart 8 PASS: Legendre symbols")
print(f"  (3|37)={leg3}  (5|37)={leg5}  (17|37)={leg17}")
print(f"  Product: (+1)×(-1)×(-1) = {product_leg} = (255|37) ✓")
print(f"  NQR×NQR = QR: two sign flips return to QR")

# ── Part 9: n=255 standing summary ───────────────────────────────────────────

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  n = {n} = 3×5×17 = 2^8-1; mod 37 = 33 ∈ D7")
print(f"  DR({n}) = {dr(n)} ∈ C3")
print(f"  137-orbit of 33: 33→{o1}→{o2}→33 (D7 orbit)")
print(f"  Factor triad: C3(QR)×CAS_EXT(NQR)×NQR17(NQR) = D7(QR)")
print(f"  R30({n}) = 128 = 2^7; 0b11111111 → 0b10000000; 128 mod 37 = 17 ∈ NQR17")
print(f"  M_7 = 127 ∈ SA_ST_A; F_3 = 257 ∈ NQR17")
print(f"  floor(N({n})) = {floor_N}; mod 37 = {floor_mod} ∈ {orbit_of(floor_N)}")
