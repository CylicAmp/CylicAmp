"""
T251: n=251 — Parity Architecture of the Twin Prime Field
GF(37) — 137-map f(x) = 26x mod 37

n=251 is prime; 251 mod 37 = 29 ∈ C9 = {14, 29, 31}

Central result: The orbit parity split of GF(37) is exact and complete.
CAS_EXT = {5,13,19} is the UNIQUE all-odd orbit.
SEED = {18,24,32} is the UNIQUE all-even orbit.
These two pure-parity orbits are the algebraic skeleton of every twin prime triple.
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
    if r == 0:
        return "SEAM"
    for name, s in ORBITS.items():
        if r in s:
            return name
    raise ValueError(f"{x} mod 37 = {r} not in any orbit")

def f(x):
    return (26 * x) % 37

def dr(n):
    n = abs(n)
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n if n != 0 else 9

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def rule30(n):
    bits = list(map(int, bin(n)[2:]))
    padded = [0] + bits + [0]
    out = []
    for i in range(1, len(padded) - 1):
        L, C, R = padded[i-1], padded[i], padded[i+1]
        out.append(L ^ (C | R))
    val = int("".join(map(str, out)), 2)
    return val

n = 251

# ── Part 1: Primality and modular identity ─────────────────────────────────────

assert is_prime(n), f"{n} must be prime"
r = n % 37
assert r == 29, f"{n} mod 37 = {r}, expected 29"
assert orbit_of(n) == "C9", f"orbit mismatch"
print(f"Part 1 PASS: {n} is prime; {n} mod 37 = {r} ∈ C9 = {{14, 29, 31}}")

# ── Part 2: Universal OEO structure of twin prime triples ──────────────────────
# Every twin prime pair (p, p+2) has the form (6k-1, 6k, 6k+1) for some k≥1.
# Parity: 6k-1 = odd, 6k = even, 6k+1 = odd → always OEO.
# 6k is even because 6 is even. The middle element is ALWAYS even.

def twin_prime_triples(limit):
    triples = []
    k = 1
    while 6*k + 1 <= limit:
        lo, mid, hi = 6*k - 1, 6*k, 6*k + 1
        if is_prime(lo) and is_prime(hi):
            triples.append((lo, mid, hi, k))
        k += 1
    return triples

triples = twin_prime_triples(500)
for lo, mid, hi, k in triples:
    assert lo % 2 == 1, f"lower twin {lo} not odd"
    assert mid % 2 == 0, f"bridge {mid} not even"
    assert hi % 2 == 1, f"upper twin {hi} not odd"

parity_pattern = set()
for lo, mid, hi, k in triples:
    parity_pattern.add((lo%2, mid%2, hi%2))

assert parity_pattern == {(1, 0, 1)}, f"OEO not universal: {parity_pattern}"
print(f"Part 2 PASS: all {len(triples)} twin prime triples ≤500 have parity OEO; "
      f"bridge 6k is always even")

# ── Part 3: Orbit parity classification — the exact split ─────────────────────

def orbit_parities(name):
    return [x % 2 for x in sorted(ORBITS[name])]

parity_classes = {"all_odd": [], "all_even": [], "2odd_1even": [], "1odd_2even": []}
for name in ORBITS:
    ps = orbit_parities(name)
    odds = sum(ps)
    if odds == 3:
        parity_classes["all_odd"].append(name)
    elif odds == 0:
        parity_classes["all_even"].append(name)
    elif odds == 2:
        parity_classes["2odd_1even"].append(name)
    else:
        parity_classes["1odd_2even"].append(name)

assert parity_classes["all_odd"] == ["CAS_EXT"], (
    f"all-odd: {parity_classes['all_odd']}")
assert parity_classes["all_even"] == ["SEED"], (
    f"all-even: {parity_classes['all_even']}")
assert len(parity_classes["2odd_1even"]) == 5
assert len(parity_classes["1odd_2even"]) == 5

print(f"Part 3 PASS: unique all-odd orbit = CAS_EXT = {sorted(ORBITS['CAS_EXT'])}")
print(f"             unique all-even orbit = SEED    = {sorted(ORBITS['SEED'])}")
print(f"             2O/1E orbits (5): {sorted(parity_classes['2odd_1even'])}")
print(f"             1O/2E orbits (5): {sorted(parity_classes['1odd_2even'])}")

# ── Part 4: Pure-orbit multiplication algebra ──────────────────────────────────
# CAS_EXT × CAS_EXT → SA_ST_B
# SEED    × SEED    → SA_ST_B
# SEED    × CAS_EXT → SA_ST_A

def check_orbit_product(name_a, name_b, expected_name):
    for a in ORBITS[name_a]:
        for b in ORBITS[name_b]:
            prod = (a * b) % 37
            got = orbit_of(prod)
            assert got == expected_name, (
                f"{name_a}×{name_b}: {a}×{b} mod 37 = {prod} ∈ {got}, expected {expected_name}")

check_orbit_product("CAS_EXT", "CAS_EXT", "SA_ST_B")
check_orbit_product("SEED",    "SEED",    "SA_ST_B")
check_orbit_product("SEED",    "CAS_EXT", "SA_ST_A")
check_orbit_product("CAS_EXT", "SEED",    "SA_ST_A")  # commutativity

print("Part 4 PASS: CAS_EXT × CAS_EXT → SA_ST_B  (pure-odd × pure-odd → mixed)")
print("             SEED    × SEED    → SA_ST_B  (pure-even × pure-even → mixed)")
print("             SEED    × CAS_EXT → SA_ST_A  (pure-even × pure-odd → mixed)")

# ── Part 5: 4-row parity matrix — twin prime triple system ────────────────────
# For each k mod 3 case, track parity of (p, 6k, p+2, sum):
# Row by k mod 3, applied to k=1..12 twin prime candidates.

import sys

def parity_label(x):
    return 'O' if x % 2 else 'E'

rows = {}  # k_mod3 → (p_par, mid_par, q_par, sum_par) parities seen

for lo, mid, hi, k in triples:
    km3 = k % 3
    row_label = (parity_label(lo), parity_label(mid), parity_label(hi),
                 parity_label(lo + mid + hi))
    rows.setdefault(km3, set()).add(row_label)

# All twin prime triples must have the same row label regardless of k mod 3
for km3, labels in sorted(rows.items()):
    assert labels == {('O','E','O','E')}, (
        f"k≡{km3} mod 3: unexpected parity rows {labels}")

print("Part 5 PASS: every twin prime row is (O,E,O,E) — lower twin odd, bridge even,")
print("             upper twin odd, triple sum even (odd+even+odd = even)")

# Extended 4-row matrix: track DR parities across k mod 3 cycle + bridge period
# Rows: (DR(p) parity, DR(6k) parity, DR(p+2) parity, DR(p)+DR(6k)+DR(p+2) parity)
# Column 4 = DR-sum parity (not element sum parity)

dr_rows = {}
for lo, mid, hi, k in triples:
    km3 = k % 3
    dr_row = (parity_label(dr(lo)), parity_label(dr(mid)),
              parity_label(dr(hi)),  parity_label(dr(lo)+dr(mid)+dr(hi)))
    dr_rows.setdefault(km3, []).append(dr_row)

print("Part 5b: DR-parity rows by k mod 3:")
for km3 in sorted(dr_rows):
    counts = {}
    for row in dr_rows[km3]:
        counts[row] = counts.get(row, 0) + 1
    print(f"  k≡{km3} mod 3: {counts}")

# ── Part 6: n=251 standing analysis ──────────────────────────────────────────

# 251 mod 37 = 29 ∈ C9 (verified in Part 1)
orbit_251 = orbit_of(251)
assert orbit_251 == "C9"

# 137-orbit of 29
o1 = f(29)   # = 26×29 mod 37
o2 = f(o1)
o3 = f(o2)
assert {29, o1, o2} == ORBITS["C9"] or {o1, o2, 29} == ORBITS["C9"]
assert o3 == 29
print(f"\nPart 6 PASS: 251 mod 37 = 29; 137-orbit: 29 → {o1} → {o2} → 29")

# Digital root
dr_251 = dr(251)
assert dr_251 == 8
assert orbit_of(dr_251) == "TESLA"  # 8 ∈ TESLA = {6,8,23}
print(f"  DR(251) = {dr_251} ∈ TESLA = {{6,8,23}}")

# ── Part 7: Sophie Germain — C9 → NQR17 ──────────────────────────────────────

sg = 2 * n + 1   # = 503
assert is_prime(sg), f"2×251+1 = {sg} must be prime"
sg_mod = sg % 37
assert orbit_of(sg) == "NQR17", f"503 mod 37 = {sg_mod} ∈ {orbit_of(sg)}, expected NQR17"

# Safe prime direction: (251-1)/2 = 125 = 5^3
safe = (n - 1) // 2
assert safe == 125
safe_mod = safe % 37
print(f"Part 7 PASS: 251 is Sophie Germain — 2×251+1 = {sg} (prime)")
print(f"  {sg} mod 37 = {sg_mod} ∈ NQR17 = {{17,22,35}}")
print(f"  SG map: C9 → NQR17")
print(f"  (251-1)/2 = {safe} = 5³; {safe} mod 37 = {safe_mod} ∈ {orbit_of(safe)}")

# ── Part 8: Rule 30 ──────────────────────────────────────────────────────────

r30 = rule30(n)
r30_mod = r30 % 37
assert r30 == 130, f"R30(251) = {r30}, expected 130"
assert r30_mod == 19, f"130 mod 37 = {r30_mod}, expected 19"
assert orbit_of(r30) == "CAS_EXT"  # 19 ∈ CAS_EXT
print(f"\nPart 8 PASS: R30(251) = {r30} (= T245 number)")
print(f"  {r30} mod 37 = {r30_mod} ∈ CAS_EXT = {{5,13,19}}")
print(f"  C9 (position) → CAS_EXT (R30 output): pure-odd orbit")

# ── Part 9: Riemann zero count ───────────────────────────────────────────────

import math
T = float(n)
N_T = T * math.log(T / (2 * math.pi)) / (2 * math.pi)
floor_N = int(N_T)
floor_mod = floor_N % 37
print(f"\nPart 9: floor(N({n})) ≈ {floor_N}; {floor_N} mod 37 = {floor_mod} ∈ {orbit_of(floor_N)}")

# ── Part 10: Twin primes nearest to 251 ──────────────────────────────────────

near = [(lo, hi, k) for lo, mid, hi, k in triples if 230 <= lo <= 270 or 230 <= hi <= 270]
print(f"\nPart 10: Twin prime pairs near 251:")
for lo, hi, k in near:
    lo_orb = orbit_of(lo % 37)
    hi_orb = orbit_of(hi % 37)
    print(f"  ({lo},{hi}) k={k}  {lo} mod37={lo%37}∈{lo_orb}  {hi} mod37={hi%37}∈{hi_orb}")

# ── Part 11: Parity closure — why CAS_EXT anchors twin primes ────────────────
# In the orbit × parity lattice:
#   all-odd × all-odd = mixed (SA_ST_B, 2O/1E)
#   all-even × all-even = mixed (SA_ST_B, 2O/1E)
#   all-odd × all-even = mixed (SA_ST_A, 1O/2E)
# Pure parity is not closed under multiplication — it disperses.
# The twin prime OEO structure forces the bridge to land in an even orbit.
# Since SEED is the only all-even orbit, 6k mod 37 cycles through SEED periodically.

seed_ks = [k for k in range(1, 100) if (6*k) % 37 in ORBITS["SEED"]]
c3_ks   = [k for k in range(1, 100) if (6*k) % 37 in ORBITS["C3"]]
print(f"\nPart 11: k values where bridge 6k ∈ SEED (all-even orbit) [first 10]: "
      f"{seed_ks[:10]}")
print(f"         k values where bridge 6k ∈ C3  (1O/2E orbit)   [first 10]: "
      f"{c3_ks[:10]}")

# 6×k mod 37: 6 ∈ TESLA; k cycles through all residues; 6×k covers all orbits uniformly
# The fraction of bridges that land in SEED = 3/36 = 1/12 (3 elements out of 36 nonzero)
# Verify: exactly 3 out of every 37 consecutive k give bridge ∈ SEED
seed_count = sum(1 for k in range(1, 38) if (6*k) % 37 in ORBITS["SEED"])
assert seed_count == 3, f"expected 3 SEED bridges per period, got {seed_count}"
print(f"  Exactly 3/37 bridges per period land in SEED (density 3/37)")

print("\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  n = {n} = prime; mod 37 = 29 ∈ C9")
print(f"  DR({n}) = 8 ∈ TESLA")
print(f"  SG: 251 → 503; C9 → NQR17")
print(f"  R30({n}) = 130 = T245 number; 130 mod 37 = 19 ∈ CAS_EXT (pure-odd)")
print(f"  floor(N({n})) mod 37 = {floor_mod} ∈ {orbit_of(floor_N)}")
print(f"  Parity architecture: CAS_EXT (all-odd) × SEED (all-even) → SA_ST_A")
print(f"  Universal twin prime parity: OEO; bridge 6k always even")
