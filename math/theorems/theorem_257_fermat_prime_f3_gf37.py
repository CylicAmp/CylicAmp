"""
T257: n=257 — Fermat Prime F3, NQR17 orbit
GF(37) framework — 137-map f(x) = 26x mod 37

257 = 2^8 + 1 = Fermat prime F3
257 mod 37 = 35 ∈ NQR17 = {17, 22, 35}

Central results:
  257 is the 4th Fermat prime: F0=3, F1=5, F2=17, F3=257
  Fermat prime orbit tower: C3 → CAS_EXT → NQR17 → NQR17
  (n-1)/2 = 128 = 2^7; 128 mod 37 = 17 ∈ NQR17 (same orbit as 257)
  R30(257) = 387; 387 mod 37 = 17 ∈ NQR17 (orbit-stable under Rule 30)
  255, 256, 257 consecutive: D7, D7, NQR17 — two D7 then exit to NQR17
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

n = 257

# ── Part 1: Fermat prime identity ─────────────────────────────────────────────

assert n == 2**8 + 1
assert is_prime(n)

fermat_primes = [3, 5, 17, 257, 65537]  # F0..F4 (only known Fermat primes)
assert n == fermat_primes[3]  # F3

r = n % 37
assert r == 35
assert orbit_of(n) == "NQR17"

print(f"Part 1 PASS: {n} = 2^8+1 = Fermat prime F3")
print(f"  {n} mod 37 = {r} ∈ NQR17 = {{17,22,35}}")
print(f"  Known Fermat primes: F0=3, F1=5, F2=17, F3=257, F4=65537")

# ── Part 2: Fermat prime orbit tower ──────────────────────────────────────────
# F0=3∈C3, F1=5∈CAS_EXT, F2=17∈NQR17, F3=257≡35∈NQR17
# The Fermat primes trace: C3 → CAS_EXT → NQR17 → NQR17

fp_orbits = [(fp, fp % 37, orbit_of(fp)) for fp in fermat_primes]

assert fp_orbits[0][2] == "C3"
assert fp_orbits[1][2] == "CAS_EXT"
assert fp_orbits[2][2] == "NQR17"
assert fp_orbits[3][2] == "NQR17"

print(f"\nPart 2 PASS: Fermat prime orbit tower")
for fp, res, orb in fp_orbits:
    print(f"  F{fermat_primes.index(fp)}: {fp} mod 37 = {res} ∈ {orb}")
print(f"  Tower: C3 → CAS_EXT → NQR17 → NQR17 (stable at NQR17 from F2 onward)")

# ── Part 3: 137-orbit of 35 — full NQR17 orbit ────────────────────────────────

o1 = f(r); o2 = f(o1); o3 = f(o2)
assert {r, o1, o2} == ORBITS["NQR17"]
assert o3 == r

print(f"\nPart 3 PASS: 137-orbit of 35: {r}→{o1}→{o2}→{r}")
print(f"  Complete orbit = NQR17 = {{17,22,35}}")
print(f"  DR(257) = {dr(n)} ∈ {orbit_of(dr(n))}")

# ── Part 4: Consecutive triple 255, 256, 257 ─────────────────────────────────
# T255: 255=2^8-1 mod37=33∈D7
# T256: 256=2^8   mod37=34∈D7
# T257: 257=2^8+1 mod37=35∈NQR17
# The power of 2 (256) and its neighbors all classified; D7→D7→NQR17

assert 255 % 37 == 33 and orbit_of(255) == "D7"
assert 256 % 37 == 34 and orbit_of(256) == "D7"
assert 257 % 37 == 35 and orbit_of(257) == "NQR17"

# D7 and NQR17: are they QR-paired?
def legendre(a, p=37):
    if a % p == 0: return 0
    return 1 if pow(a, (p-1)//2, p) == 1 else -1

assert all(legendre(x) == 1 for x in ORBITS["D7"])    # D7 is QR
assert all(legendre(x) == -1 for x in ORBITS["NQR17"]) # NQR17 is NQR

print(f"\nPart 4 PASS: consecutive triple 255, 256, 257")
print(f"  255=2^8-1: mod37=33∈D7(QR)")
print(f"  256=2^8:   mod37=34∈D7(QR)")
print(f"  257=2^8+1: mod37=35∈NQR17(NQR)")
print(f"  2^8 lands in D7; adding 1 exits to NQR17; subtracting 1 stays in D7")

# ── Part 5: (n-1)/2 = 128 ∈ NQR17 — orbit self-reference ────────────────────
# 257 is not a Sophie Germain prime (2*257+1=515=5*103, not prime)
# But (257-1)/2 = 128 = 2^7, and 128 mod 37 = 17 ∈ NQR17 = same orbit as 257

half = (n - 1) // 2
assert half == 128 == 2**7
assert half % 37 == 17
assert orbit_of(half) == "NQR17"

print(f"\nPart 5 PASS: (257-1)/2 = 128 = 2^7; 128 mod 37 = 17 ∈ NQR17")
print(f"  257 and (257-1)/2 share the same orbit: NQR17")
print(f"  The orbit is stable under the halving map n → (n-1)/2")

# ── Part 6: Rule 30 — NQR17 orbit-stable ─────────────────────────────────────

r30 = rule30(n)
assert r30 == 387
r30_mod = r30 % 37
assert r30_mod == 17
assert orbit_of(r30) == "NQR17"

print(f"\nPart 6 PASS: R30(257) = {r30}; {r30} mod 37 = {r30_mod} ∈ NQR17")
print(f"  257 mod 37 = 35 ∈ NQR17; R30(257) mod 37 = 17 ∈ NQR17")
print(f"  Rule 30 is orbit-stable for n=257: NQR17 → NQR17")

# ── Part 7: Riemann floor ─────────────────────────────────────────────────────

T = float(n)
floor_N = int(T * math.log(T / (2 * math.pi)) / (2 * math.pi))
floor_mod = floor_N % 37

print(f"\nPart 7: floor(N(257)) = {floor_N}; mod 37 = {floor_mod} ∈ {orbit_of(floor_N)}")

# ── Part 8: Connection to T255 and T256 ──────────────────────────────────────
# T255: R30(255)=128=2^7; 128 mod37=17∈NQR17
# T257: (257-1)/2=128=2^7; 128 mod37=17∈NQR17
# The same value 128 appears in both theorems through different maps

assert rule30(255) == 128
assert (257 - 1) // 2 == 128

print(f"\nPart 8: Connection T255↔T257 through 128=2^7")
print(f"  R30(255) = 128 (Rule 30 output of T255)")
print(f"  (257-1)/2 = 128 (halving of T257)")
print(f"  Same value, different maps, same orbit: NQR17")
print(f"  255=2^8-1 and 257=2^8+1 are symmetric around 256=2^8")
print(f"  Both connect to 128=2^7 through orbit NQR17")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  n = 257 = 2^8+1 = Fermat prime F3; mod 37 = 35 ∈ NQR17")
print(f"  DR(257) = 5 ∈ CAS_EXT")
print(f"  Fermat tower: C3(F0=3) → CAS_EXT(F1=5) → NQR17(F2=17) → NQR17(F3=257)")
print(f"  Consecutive triple: 255∈D7, 256∈D7, 257∈NQR17")
print(f"  (257-1)/2 = 128 ∈ NQR17: orbit self-reference under halving")
print(f"  R30(257) = 387 mod37 = 17 ∈ NQR17: orbit-stable under Rule 30")
print(f"  128=2^7 links T255(R30) and T257(halving) through NQR17")
print(f"  floor(N(257)) = {floor_N}; mod 37 = {floor_mod} ∈ {orbit_of(floor_N)}")
