"""
T268: x_k = (k³ + 33) mod 37 for k = 1..5 — cubic trajectory in GF(37)

Sequence: [34, 4, 23, 23, 10]
Orbits:   [D7, C3, TESLA, TESLA, IC]

=== KEY RESULTS ===

1. Antipodal entry (k=1,2): D7 ↔ C3 are antipodal (T265). The cubic opens on a
   complementary pair: x₁=34∈D7, x₂=4∈C3, and −D7=C3.

2. Duplicate at k=3,4: Both give x=23∈TESLA.
   Cause: 3³ ≡ 4³ ≡ 27 (mod 37).
   The cube roots of 27 in GF(37) are exactly {3, 4, 30} = C3.
   27 ∈ NEG_H; 27 = 3³; 27 = (10³−1)/37 (the 1/37 decimal block, T265).
   The third cube root k=30 ∈ C3 lies outside the k=1..5 window.

3. Sophie Germain chain across the sequence: 23∈TESLA → 2×23+1=47≡10∈IC.
   The sequence endpoint x₅=10 is the safe prime image of the duplicate value.
   47 is also safe prime safe: (47−1)/2=23 is prime.

4. Shift constant: 33 ∈ D7 (the offset in x_k = k³+33). The cubic is anchored
   inside the D7 orbit: 33 is the ×26 predecessor of 7, which precedes 34 in D7.
   D7 orbit under ×26: 34→33→7→34.

5. R30 output orbit sequence: SEED, TESLA, DARK_A, DARK_A, NEG_H.
   The duplicate input (23,23) produces a duplicate R30 output (DARK_A,DARK_A) —
   no phase shift; the Rule 30 map is deterministic on the value, not on k.

=== ORBIT TRAJECTORIES UNDER ×26 ===

  34∈D7:   34→33→7→34   (D7 is closed)
   4∈C3:    4→30→3→4    (C3 is closed)
  23∈TESLA: 23→6→8→23   (TESLA is closed)
  10∈IC:   10→1→26→10   (IC is closed)

  Each value belongs to its orbit; the ×26 map cycles within it.

=== ANTIPODAL STRUCTURE ===

  −D7  = C3   (T265): x₁∈D7 ↔ x₂∈C3 — sequence opens on antipodal pair
  −IC  = NEG_H       : sequence closes at IC; IC antipodal to NEG_H
  −TESLA = C9        : 23∈TESLA; TESLA antipodal to C9 (fully non-oblong, T264)

=== CUBIC ROOTS OF 27 IN GF(37) ===

  k³ ≡ 27 (mod 37) ⟺ k ∈ C3 = {3, 4, 30}

  Proof: 27 = 3³ mod 37. The cube roots of 3³ are 3×{cube roots of 1}.
  Cube roots of unity in GF(37): {1,10,26} = IC (ord₃₇(10)=3, T265).
  So cube roots of 27 = 3×IC = {3×1, 3×10, 3×26} = {3, 30, 78 mod 37} = {3, 30, 4} = C3.

  The k=1..5 window captures exactly two of the three cubic roots (k=3,4).
  The third cubic root k=30∈C3 would give x₃₀ = 30³+33 ≡ 27+33 = 60 ≡ 23 (mod 37) = TESLA.
  All three cubic root inputs produce the same output: 23∈TESLA.

=== SOPHIE GERMAIN CHAIN ===

  23 is prime; 2×23+1 = 47 is prime → 23 is a Sophie Germain prime.
  47 mod 37 = 10 ∈ IC = x₅ (the sequence endpoint).
  47 is a safe prime: (47−1)/2 = 23 is prime.
  Sophie chain: 23∈TESLA → 47≡10∈IC (length 2).
  The sequence endpoint is the Sophie image of the duplicate value.
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

def rule30(n):
    bits = list(map(int, bin(n)[2:]))
    padded = [0] + bits + [0]
    out = [padded[i-1] ^ (padded[i] | padded[i+1]) for i in range(1, len(padded)-1)]
    return int("".join(map(str, out)), 2)

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

# ── Part 1: Sequence construction ────────────────────────────────────────────

seq = [(k, (k**3 + 33) % 37) for k in range(1, 6)]
vals = [r for _, r in seq]

assert vals == [34, 4, 23, 23, 10]
assert [orbit_of(r) for _, r in seq] == ["D7", "C3", "TESLA", "TESLA", "IC"]

print("Part 1 PASS: x_k = (k³+33) mod 37 for k=1..5")
print(f"  {'k':>2}  {'k³+33':>6}  {'mod37':>5}  orbit")
for k, r in seq:
    raw = k**3 + 33
    print(f"  {k:>2}  {raw:>6}  {r:>5}  {orbit_of(r)}")

# ── Part 2: Antipodal entry at k=1,2 ─────────────────────────────────────────

assert orbit_of(34) == "D7" and orbit_of(4) == "C3"
assert ANTIPODAL["D7"] == "C3"

print(f"\nPart 2 PASS: antipodal entry — x₁=34∈D7, x₂=4∈C3; D7↔C3 are antipodal (T265)")

# ── Part 3: Duplicate — cubic roots of 27 = C3 ────────────────────────────────

assert pow(3, 3, 37) == 27
assert pow(4, 3, 37) == 27
assert pow(30, 3, 37) == 27

cubic_roots_27 = sorted([x for x in range(1, 37) if pow(x, 3, 37) == 27])
assert cubic_roots_27 == sorted(ORBITS["C3"])  # [3, 4, 30]

# Proof via IC cube roots of unity
assert pow(10, 3, 37) == 1 and pow(26, 3, 37) == 1 and pow(1, 3, 37) == 1
cube_roots_unity = sorted([x for x in range(1, 37) if pow(x, 3, 37) == 1])
assert cube_roots_unity == sorted(ORBITS["IC"])  # [1, 10, 26]

# cube roots of 27 = 3 × IC mod 37
assert {(3 * x) % 37 for x in ORBITS["IC"]} == ORBITS["C3"]

# x_k=30 would also give 23 (third cubic root outside window)
assert (30**3 + 33) % 37 == 23 and orbit_of(23) == "TESLA"

print(f"\nPart 3 PASS: duplicate at k=3,4 because 3³≡4³≡27 (mod 37)")
print(f"  Cube roots of 27 in GF(37): {cubic_roots_27} = C3")
print(f"  Proof: cube roots of unity = IC = {{1,10,26}}; cube roots of 27 = 3×IC = C3")
print(f"  Third root k=30∈C3 (outside window) also gives x₃₀=23∈TESLA")
print(f"  27∈NEG_H: 27=3³; also the 1/37 decimal block (T265)")

# ── Part 4: 137-map orbits ────────────────────────────────────────────────────

orbits_map = {
    34: ([34, 33, 7], "D7"),
    4:  ([4, 30, 3], "C3"),
    23: ([23, 6, 8], "TESLA"),
    10: ([10, 1, 26], "IC"),
}
for start, (chain, expected_orbit) in orbits_map.items():
    assert orbit_of(start) == expected_orbit
    x = start
    for nxt in chain[1:]:
        assert (x * 26) % 37 == nxt, f"×26 from {x} ≠ {nxt}"
        x = nxt
    assert (x * 26) % 37 == chain[0]  # closes

print(f"\nPart 4 PASS: 137-map orbits (×26 mod 37)")
for start, (chain, o) in orbits_map.items():
    print(f"  {start}∈{o}: {'→'.join(map(str,chain))}→{chain[0]}")

# ── Part 5: Shift constant 33 ∈ D7 ───────────────────────────────────────────

assert 33 in ORBITS["D7"]
assert (33 * 26) % 37 == 7 and 7 in ORBITS["D7"]
assert (7 * 26) % 37 == 34 and 34 in ORBITS["D7"]

print(f"\nPart 5 PASS: shift constant 33∈D7; D7 orbit: 34→33→7→34 under ×26")

# ── Part 6: DR analysis ───────────────────────────────────────────────────────

dr_vals = {34: 7, 4: 4, 23: 5, 10: 1}
for v, expected in dr_vals.items():
    assert dr(v) == expected

print(f"\nPart 6 PASS: digital roots")
for k, r in seq:
    print(f"  x_{k}={r}∈{orbit_of(r)}: DR={dr(r)}")

# ── Part 7: Rule 30 ───────────────────────────────────────────────────────────

r30_expected = {34: (55, 18, "SEED"), 4: (6, 6, "TESLA"), 23: (20, 20, "DARK_A"), 10: (11, 11, "NEG_H")}
for v, (r30_raw, r30_mod, r30_orbit) in r30_expected.items():
    assert rule30(v) == r30_raw
    assert r30_raw % 37 == r30_mod
    assert orbit_of(r30_raw) == r30_orbit

print(f"\nPart 7 PASS: Rule 30")
for k, r in seq:
    r30 = rule30(r)
    print(f"  R30({r:>2}∈{orbit_of(r):7}) = {r30:>3} ≡ {r30%37:>2} ∈ {orbit_of(r30)}")
print(f"  Duplicate input (23,23) → duplicate R30 output: DARK_A,DARK_A (deterministic on value)")

# ── Part 8: Sophie Germain chain 23∈TESLA → 47≡10∈IC ─────────────────────────

assert is_prime(23)
assert is_prime(47) and 2*23+1 == 47
assert 47 % 37 == 10 and 10 in ORBITS["IC"]
assert is_prime(23) and (47-1)//2 == 23  # 47 is a safe prime
assert not is_prime(2*47+1)  # chain terminates at length 2

# The sequence endpoint x₅ = 10 = 47 mod 37
assert vals[-1] == 10 == 47 % 37

print(f"\nPart 8 PASS: Sophie Germain chain")
print(f"  23∈TESLA is prime; 2×23+1=47 is prime → 23 is Sophie Germain prime")
print(f"  47 mod 37 = 10 ∈ IC = x₅ (sequence endpoint)")
print(f"  47 is safe prime: (47−1)/2=23 is prime")
print(f"  Sophie chain: 23∈TESLA → 47≡10∈IC (length 2; 2×47+1=95=5×19 not prime)")
print(f"  The sequence endpoint is the Sophie image of the duplicate value mod 37")

# ── Part 9: Antipodal structure of orbit sequence ─────────────────────────────

orbit_seq = ["D7", "C3", "TESLA", "TESLA", "IC"]
assert ANTIPODAL["D7"] == "C3"    # x₁ ↔ x₂
assert ANTIPODAL["IC"] == "NEG_H" # x₅ antipodal to NEG_H
assert ANTIPODAL["TESLA"] == "C9" # C9 = fully non-oblong twin prime orbit (T264)

print(f"\nPart 9 PASS: antipodal structure of orbit sequence")
print(f"  D7↔C3: x₁,x₂ are antipodal partners (sequence opens on a complement pair)")
print(f"  IC↔NEG_H: endpoint x₅∈IC; NEG_H is the −IC orbit (T265)")
print(f"  TESLA↔C9: duplicate values; C9 = fully non-oblong orbit (T264)")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  x_k = (k³+33) mod 37: [34,4,23,23,10] → [D7,C3,TESLA,TESLA,IC]")
print(f"  Antipodal entry: x₁∈D7, x₂∈C3 (D7↔C3 antipodal pair)")
print(f"  Duplicate at k=3,4: 3³≡4³≡27 mod 37; cube roots of 27 = C3={3,4,30}")
print(f"  Proved: cube roots of 27 = 3×IC (cube roots of unity) = C3")
print(f"  Shift constant 33∈D7; D7 orbit: 34→33→7→34 under ×26")
print(f"  Sophie chain: 23∈TESLA → 47≡10∈IC = x₅ endpoint")
print(f"  R30: SEED,TESLA,DARK_A,DARK_A,NEG_H (duplicate input → duplicate output)")
