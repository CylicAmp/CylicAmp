"""
T266: 123×k — DR=6→3→9 cycle, pipeline seed at k=2, uniform orbit coverage

123 = 3 × 41
123 mod 37 = 12 ∈ SA_ST_A = {9, 12, 16}
DR(123) = 6 ∈ TESLA

Multiples of 123 (123, 246, 369, 492, ...):
  DR cycle: 6 → 3 → 9 → 6 → 3 → 9 ... (period 3, all k=1..36)
  DR=6 ∈ TESLA  DR=3 ∈ C3  DR=9 ∈ SA_ST_A
  Each DR value inhabits one orbit from three distinct antipodal pairs (T265):
    TESLA ↔ C9,   C3 ↔ D7,   SA_ST_A ↔ SA_ST_B

246 = 123×2:
  246 mod 37 = 24 ∈ SEED — the pipeline reference seed.
  The reference seed of the CylicAmp pipeline appears naturally at k=2.

369 = 123×3:
  369 mod 37 = 36 = −1 ∈ NEG_H — the additive inverse of 1 in GF(37).
  369 = 9×41; 369/37 = 9 remainder 36.

41 = prime factor of 123:
  41 mod 37 = 4 ∈ C3. (41,43) is a twin prime pair; 43 mod37=6∈TESLA.

Uniform orbit coverage:
  The sequence 123k mod 37 for k=1..36 is a permutation of {1,...,36}
  (since gcd(12,37)=1). Each of the 12 named orbits appears EXACTLY 3 times.
  At k=37: 123×37 mod 37 = 0 → SEAM.
"""

P = 37
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
ANTIPODAL = {
    "IC":"NEG_H","NEG_H":"IC","DARK_A":"NQR17","NQR17":"DARK_A",
    "C3":"D7","D7":"C3","CAS_EXT":"SEED","SEED":"CAS_EXT",
    "TESLA":"C9","C9":"TESLA","SA_ST_A":"SA_ST_B","SA_ST_B":"SA_ST_A",
}

def orbit_of(x):
    r = x % 37
    if r == 0: return "SEAM"
    for name, s in ORBITS.items():
        if r in s: return name
    raise ValueError(x)

def dr(n):
    n = abs(int(n))
    while n >= 10: n = sum(int(d) for d in str(n))
    return n if n else 9

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

n = 123

# ── Part 1: Identity ─────────────────────────────────────────────────────────

assert n == 3 * 41 and is_prime(3) and is_prime(41)
assert n % 37 == 12 and 12 in ORBITS["SA_ST_A"]
assert dr(n) == 6 and 6 in ORBITS["TESLA"]
assert 41 % 37 == 4 and 4 in ORBITS["C3"]
assert is_prime(41) and is_prime(43)  # twin prime pair (41,43)
assert 43 % 37 == 6 and 6 in ORBITS["TESLA"]

print(f"Part 1 PASS: 123 = 3×41; mod37=12∈SA_ST_A; DR=6∈TESLA")
print(f"  41 mod37=4∈C3; (41,43) twin prime; 43 mod37=6∈TESLA")

# ── Part 2: DR cycle 6→3→9 ──────────────────────────────────────────────────

DR_CYCLE = [6, 3, 9]
for k in range(1, 37):
    assert dr(n * k) == DR_CYCLE[(k-1) % 3], f"k={k}: DR={dr(n*k)} ≠ {DR_CYCLE[(k-1)%3]}"

assert 6 in ORBITS["TESLA"] and 3 in ORBITS["C3"] and 9 in ORBITS["SA_ST_A"]

print(f"\nPart 2 PASS: DR cycle 6→3→9 (period 3, all k=1..36)")
print(f"  DR=6∈TESLA  DR=3∈C3  DR=9∈SA_ST_A")
print(f"  Each DR value spans one orbit from three antipodal pairs (T265):")
for dv, o in [(6,"TESLA"),(3,"C3"),(9,"SA_ST_A")]:
    anti = ANTIPODAL[o]
    print(f"    DR={dv}∈{o} ↔ {anti} (antipodal)")

# ── Part 3: 246 = pipeline seed at k=2 ───────────────────────────────────────

assert n * 2 == 246 and 246 % 37 == 24 and 24 in ORBITS["SEED"]
print(f"\nPart 3 PASS: 123×2 = 246; 246 mod37=24∈SEED (pipeline reference seed)")
print(f"  The reference seed of the CylicAmp pipeline appears at k=2 in this sequence")

# All three SEED elements appear in the sequence:
seed_hits = [(k, n*k, (n*k)%37) for k in range(1,37) if (n*k)%37 in ORBITS["SEED"]]
assert len(seed_hits) == 3
print(f"  All 3 SEED elements appear: {[(k,v,r) for k,v,r in seed_hits]}")

# ── Part 4: 369 = 123×3 = -1 mod37 ─────────────────────────────────────────

assert n * 3 == 369 and 369 % 37 == 36 and 36 in ORBITS["NEG_H"]
assert 36 == 37 - 1  # 36 ≡ −1 mod 37
print(f"\nPart 4 PASS: 123×3 = 369; mod37=36=−1∈NEG_H")
print(f"  369 = 9×41; 369/37 = 9 remainder 36 (the −1 element)")

# ── Part 5: Uniform orbit coverage ───────────────────────────────────────────

from collections import Counter
seq = [orbit_of(n * k) for k in range(1, 38)]
cnt = Counter(seq)
assert cnt["SEAM"] == 1 and n * 37 % 37 == 0
for name in ORBITS:
    assert cnt[name] == 3, f"{name} appears {cnt[name]} times, expected 3"

print(f"\nPart 5 PASS: every orbit appears exactly 3 times in k=1..36; SEAM at k=37")
print(f"  gcd(123 mod37, 37) = gcd(12, 37) = 1 → sequence is a permutation of {{1..36}}")
print(f"  36 values / 12 orbits of size 3 = exactly 3 hits per orbit")

# ── Part 6: Sequence table (first 12) ────────────────────────────────────────

print(f"\nPart 6: First 12 multiples")
print(f"  {'k':>3}  {'value':>6}  {'mod37':>5}  {'orbit':12}  DR")
for k in range(1, 13):
    v = n * k
    print(f"  {k:>3}  {v:>6}  {v%37:>5}  {orbit_of(v):12}  {dr(v)}")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  123 = 3×41; mod37=12∈SA_ST_A; DR=6∈TESLA")
print(f"  DR cycle: 6→3→9 period 3 (TESLA, C3, SA_ST_A — one from each antipodal pair)")
print(f"  123×2 = 246 ∈ SEED: pipeline seed appears at k=2")
print(f"  123×3 = 369; mod37=36=−1∈NEG_H")
print(f"  41 mod37=4∈C3; (41,43) twin prime pair; 43 mod37=6∈TESLA=DR orbit")
print(f"  Every orbit appears exactly 3 times in 123k mod37 for k=1..36")
