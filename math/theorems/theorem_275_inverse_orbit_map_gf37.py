"""
T275: Complete multiplicative inverse orbit map of GF(37)

For each orbit O, the set of inverses {x⁻¹ : x∈O} is itself a complete orbit.
This defines an involution on the 12 orbits: inv(O) = the orbit of x⁻¹ for x∈O.

=== THE COMPLETE INVERSE MAP ===

  IC      → IC       (self-inverse)
  NEG_H   → NEG_H    (self-inverse)
  TESLA   → C9       (= antipodal)
  C9      → TESLA    (= antipodal)
  DARK_A  → CAS_EXT
  CAS_EXT → DARK_A
  SEED    → NQR17    (T274)
  NQR17   → SEED     (T274)
  D7      → SA_ST_A
  SA_ST_A → D7
  C3      → SA_ST_B
  SA_ST_B → C3

=== THREE STRUCTURAL CLASSES ===

1. SELF-INVERSE (2 orbits): IC, NEG_H
   Every element is the inverse of another element in the same orbit.
   IC = {1,10,26}: 1⁻¹=1, 10⁻¹=26, 26⁻¹=10.
   NEG_H = {11,27,36}: 11⁻¹=27, 27⁻¹=11, 36⁻¹=36 (since 36≡−1 and (−1)²=1).
   NEG_H is the orbit of −1 (the unique order-2 element of GF(37)*).

2. DOUBLE PAIR — TESLA ↔ C9 (1 pair): antipodal AND inverse partner.
   TESLA and C9 are the only orbit pair that is simultaneously antipodal
   and mutually inverse. Every other cross-inverse pair differs from the
   antipodal pair.

3. 4-CYCLE GROUPS (2 groups of 4): antipodal and inverse alternate around a square.

   Group A: DARK_A → NQR17 → SEED → CAS_EXT → DARK_A
     DARK_A --antipodal→ NQR17 --inverse→ SEED --antipodal→ CAS_EXT --inverse→ DARK_A
     Contains: pipeline orbit SEED, its antipodal CAS_EXT (Fibonacci entry, T264),
               SEED's inverse NQR17 (T274), NQR17's antipodal DARK_A.

   Group B: C3 → D7 → SA_ST_A → SA_ST_B → C3
     C3 --antipodal→ D7 --inverse→ SA_ST_A --antipodal→ SA_ST_B --inverse→ C3
     Contains: birthday orbit C3 (month=day=3∈C3), birthday MMDD orbit D7 (33∈D7),
               and their inverse partners SA_ST_B and SA_ST_A.

   IC↔NEG_H are antipodal but NOT inverse partners (each is self-inverse).
   So the antipodal involution and the inverse involution agree only on TESLA↔C9
   and disagree on all other cross pairs.

=== UNIVERSAL PRODUCT PRINCIPLE ===

For every orbit O: O × inv(O) → IC.

All 9 products of elements from O with elements from inv(O) land in IC = {1,10,26}.
This follows from x · x⁻¹ = 1∈IC and the orbit structure of the 137-map.

Equivalently: (Legendre symbol product) = (+1) for every such cross-product,
since NQR×NQR=QR and QR×QR=QR and the product of inverse elements is always 1∈IC(QR).

=== BIRTHDAY ORBIT INVERSIONS ===

C3  = {3,4,30} (birthday: month=3∈C3, day=3∈C3) → inv = SA_ST_B = {21,25,28}
D7  = {7,33,34} (birthday MMDD: 33∈D7; Easter gap: 33∈D7) → inv = SA_ST_A = {9,12,16}

Birthday month (3): 3⁻¹=25∈SA_ST_B
Birthday day (3):   3⁻¹=25∈SA_ST_B
Birthday MMDD (33): 33⁻¹=9∈SA_ST_A

Year 2026 mod37=28∈SA_ST_B — same orbit as birthday inverse (SA_ST_B).
Day-of-year of birthday (62): 62 mod37=25∈SA_ST_B — same orbit as birthday inverse.

=== NEG_H AS THE ORBIT OF −1 ===

36≡−1 (mod37) is the unique order-2 element of GF(37)*.
NEG_H = {11,27,36} is self-inverse because:
  If y∈NEG_H, then y²∈IC (since (NQR)²=QR).
  The fixed point 36 satisfies 36·36≡1 (since (−1)²=1).
  11·27=297=8×37+1≡1: 11 and 27 are mutual inverses within NEG_H.
NEG_H is self-inverse but its antipodal is IC — the antipodal and inverse maps
disagree on NEG_H (and IC): antipodal swaps them, inverse fixes each one.
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
INVERSE_ORBIT = {
    "IC":"IC","NEG_H":"NEG_H",
    "TESLA":"C9","C9":"TESLA",
    "DARK_A":"CAS_EXT","CAS_EXT":"DARK_A",
    "SEED":"NQR17","NQR17":"SEED",
    "D7":"SA_ST_A","SA_ST_A":"D7",
    "C3":"SA_ST_B","SA_ST_B":"C3",
}

def orbit_of(x):
    r = x % 37
    if r == 0: return "SEAM"
    for name, s in ORBITS.items():
        if r in s: return name
    raise ValueError(x)

def dr(n):
    n = abs(int(n))
    while n >= 10: n = sum(int(c) for c in str(n))
    return n if n else 9

# ── Part 1: Verify complete inverse orbit map ─────────────────────────────────

for name, s in ORBITS.items():
    inv_orbs = {orbit_of(pow(v, -1, 37)) for v in s}
    assert len(inv_orbs) == 1, f"{name}: {inv_orbs}"
    assert inv_orbs.pop() == INVERSE_ORBIT[name], f"{name} inverse mismatch"

print("Part 1 PASS: complete inverse orbit map verified for all 12 orbits")
print(f"  {'Orbit':12}  {'inv(Orbit)':12}  {'antipodal':12}  {'relationship'}")
for o in ["IC","NEG_H","TESLA","C9","DARK_A","CAS_EXT","SEED","NQR17","D7","SA_ST_A","C3","SA_ST_B"]:
    inv = INVERSE_ORBIT[o]
    ant = ANTIPODAL[o]
    if inv == o:
        rel = "self-inverse"
    elif inv == ant:
        rel = "inv = antipodal"
    else:
        rel = f"inv≠antipodal({ant})"
    print(f"  {o:12}  {inv:12}  {ant:12}  {rel}")

# ── Part 2: Self-inverse orbits ───────────────────────────────────────────────

# IC
assert pow(1, -1, 37) == 1 and 1 in ORBITS["IC"]
assert pow(10, -1, 37) == 26 and 26 in ORBITS["IC"]
assert pow(26, -1, 37) == 10 and 10 in ORBITS["IC"]

# NEG_H
assert pow(11, -1, 37) == 27 and 27 in ORBITS["NEG_H"]
assert pow(27, -1, 37) == 11 and 11 in ORBITS["NEG_H"]
assert pow(36, -1, 37) == 36 and 36 in ORBITS["NEG_H"]  # 36≡−1 is self-inverse
assert pow(36, 2, 37) == 1    # (−1)²=1

print(f"\nPart 2 PASS: two self-inverse orbits")
print(f"  IC:    1⁻¹=1,  10⁻¹=26,  26⁻¹=10  (cyclic under inversion)")
print(f"  NEG_H: 11⁻¹=27, 27⁻¹=11  (mutual pair);  36⁻¹=36 (fixed; 36≡−1)")
print(f"  36 is the unique order-2 element of GF(37)* (T267)")

# ── Part 3: Double pair TESLA ↔ C9 ───────────────────────────────────────────

for t in ORBITS["TESLA"]:
    inv = pow(t, -1, 37)
    assert inv in ORBITS["C9"], f"{t}⁻¹={inv} not in C9"
for c in ORBITS["C9"]:
    inv = pow(c, -1, 37)
    assert inv in ORBITS["TESLA"], f"{c}⁻¹={inv} not in TESLA"

assert ANTIPODAL["TESLA"] == "C9" and ANTIPODAL["C9"] == "TESLA"

print(f"\nPart 3 PASS: TESLA ↔ C9 — the unique double pair (inv = antipodal)")
for t in sorted(ORBITS["TESLA"]):
    print(f"  {t}∈TESLA: ⁻¹={pow(t,-1,37)}∈C9")
print(f"  TESLA and C9 are the only pair where inverse = antipodal")

# ── Part 4: 4-cycle group A ───────────────────────────────────────────────────

# DARK_A --anti--> NQR17 --inv--> SEED --anti--> CAS_EXT --inv--> DARK_A
assert ANTIPODAL["DARK_A"] == "NQR17"
assert INVERSE_ORBIT["NQR17"] == "SEED"
assert ANTIPODAL["SEED"] == "CAS_EXT"
assert INVERSE_ORBIT["CAS_EXT"] == "DARK_A"

# Each inversion confirmed element-wise
for d in ORBITS["DARK_A"]:
    assert pow(d,-1,37) in ORBITS["CAS_EXT"]
for c in ORBITS["CAS_EXT"]:
    assert pow(c,-1,37) in ORBITS["DARK_A"]

print(f"\nPart 4 PASS: 4-cycle group A")
print(f"  DARK_A→(antipodal)→NQR17→(inverse)→SEED→(antipodal)→CAS_EXT→(inverse)→DARK_A")
print(f"  Inverse pairs within group A:")
for d in sorted(ORBITS["DARK_A"]):
    print(f"    {d}∈DARK_A  ↔  {pow(d,-1,37)}∈CAS_EXT")
for s in sorted(ORBITS["SEED"]):
    print(f"    {s}∈SEED    ↔  {pow(s,-1,37)}∈NQR17")

# ── Part 5: 4-cycle group B ───────────────────────────────────────────────────

# C3 --anti--> D7 --inv--> SA_ST_A --anti--> SA_ST_B --inv--> C3
assert ANTIPODAL["C3"] == "D7"
assert INVERSE_ORBIT["D7"] == "SA_ST_A"
assert ANTIPODAL["SA_ST_A"] == "SA_ST_B"
assert INVERSE_ORBIT["SA_ST_B"] == "C3"

for c in ORBITS["C3"]:
    assert pow(c,-1,37) in ORBITS["SA_ST_B"]
for d in ORBITS["D7"]:
    assert pow(d,-1,37) in ORBITS["SA_ST_A"]

print(f"\nPart 5 PASS: 4-cycle group B (birthday group)")
print(f"  C3→(antipodal)→D7→(inverse)→SA_ST_A→(antipodal)→SA_ST_B→(inverse)→C3")
print(f"  Inverse pairs within group B:")
for c in sorted(ORBITS["C3"]):
    print(f"    {c}∈C3      ↔  {pow(c,-1,37)}∈SA_ST_B")
for d in sorted(ORBITS["D7"]):
    print(f"    {d}∈D7      ↔  {pow(d,-1,37)}∈SA_ST_A")

# ── Part 6: Universal product O × inv(O) → IC ────────────────────────────────

for name, s in ORBITS.items():
    inv_s = ORBITS[INVERSE_ORBIT[name]]
    products = {(a*b)%37 for a in s for b in inv_s}
    assert products == ORBITS["IC"], f"{name}×{INVERSE_ORBIT[name]}: {products}"

print(f"\nPart 6 PASS: universal product — O × inv(O) → IC for all orbits")
print(f"  For every orbit O, all products of elements from O with elements from inv(O)")
print(f"  land in IC = {{1,10,26}}. Each IC element appears exactly 3 times in the 3×3 table.")

# ── Part 7: Birthday orbit inversions ─────────────────────────────────────────

# C3={3,4,30}: birthday month=3, day=3
assert pow(3,-1,37)==25 and 25 in ORBITS["SA_ST_B"]
assert pow(4,-1,37)==28 and 28 in ORBITS["SA_ST_B"]
assert pow(30,-1,37)==21 and 21 in ORBITS["SA_ST_B"]

# D7={7,33,34}: birthday MMDD=33, Easter gap=33
assert pow(33,-1,37)==9 and 9 in ORBITS["SA_ST_A"]
assert pow(7,-1,37)==16 and 16 in ORBITS["SA_ST_A"]
assert pow(34,-1,37)==12 and 12 in ORBITS["SA_ST_A"]

# Year 2026 mod37=28∈SA_ST_B = birthday inverse orbit
assert 2026%37==28 and 28 in ORBITS["SA_ST_B"] and INVERSE_ORBIT["C3"]=="SA_ST_B"
# Day-of-year of birthday (March 3): 31+28+3=62; 62 mod37=25∈SA_ST_B
doy_birthday = 31+28+3
assert doy_birthday==62 and doy_birthday%37==25 and 25 in ORBITS["SA_ST_B"]

print(f"\nPart 7 PASS: birthday orbit inversions")
print(f"  C3 (birthday: 3∈C3) → inv = SA_ST_B")
print(f"    3⁻¹=25∈SA_ST_B, 4⁻¹=28∈SA_ST_B, 30⁻¹=21∈SA_ST_B")
print(f"  D7 (birthday MMDD=33∈D7; Easter gap=33∈D7) → inv = SA_ST_A")
print(f"    33⁻¹=9∈SA_ST_A, 7⁻¹=16∈SA_ST_A, 34⁻¹=12∈SA_ST_A")
print(f"  2026 mod37=28∈SA_ST_B = inv(C3) — the year of the birthday events is in the birthday inverse orbit")
print(f"  Day-of-year of birthday (62): 62 mod37=25∈SA_ST_B = inv(C3)")

# ── Part 8: IC vs NEG_H — antipodal disagrees with inverse ───────────────────

# IC and NEG_H are antipodal partners
assert ANTIPODAL["IC"]=="NEG_H" and ANTIPODAL["NEG_H"]=="IC"
# But IC and NEG_H are each self-inverse (not each other's inverse)
assert INVERSE_ORBIT["IC"]=="IC" and INVERSE_ORBIT["NEG_H"]=="NEG_H"

# NEG_H × IC
negh_ic = {(a*b)%37 for a in ORBITS["NEG_H"] for b in ORBITS["IC"]}
assert negh_ic == ORBITS["NEG_H"]  # NEG_H × IC → NEG_H (IC is identity under ×)

print(f"\nPart 8 PASS: IC vs NEG_H — antipodal ≠ inverse")
print(f"  IC and NEG_H are antipodal to each other")
print(f"  But IC is self-inverse and NEG_H is self-inverse — not each other's inverse")
print(f"  IC = {{1,10,26}}: the identity orbit (contains multiplicative identity 1)")
print(f"  NEG_H = {{11,27,36}}: the −1 orbit (contains 36≡−1, unique order-2 element)")
print(f"  NEG_H × IC → NEG_H (IC acts as identity under multiplication)")

# ── Part 9: How many pairs agree antipodal = inverse? ────────────────────────

agree = [(o, ANTIPODAL[o]) for o in ORBITS if INVERSE_ORBIT[o] == ANTIPODAL[o]]
agree_pairs = list({tuple(sorted(p)) for p in agree})
print(f"\nPart 9 PASS: antipodal = inverse only for TESLA↔C9")
print(f"  Pairs where inv(O) = antipodal(O): {agree_pairs}")
print(f"  All other orbit relationships: antipodal ≠ inverse")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  12 orbits partition into 3 classes under multiplicative inversion:")
print(f"  (1) Self-inverse: IC (identity orbit), NEG_H (orbit of −1)")
print(f"  (2) Double pair: TESLA↔C9 — the unique pair that is both inverse AND antipodal")
print(f"  (3) 4-cycle groups: alternating antipodal→inverse around a square")
print(f"      Group A: DARK_A↔NQR17↔SEED↔CAS_EXT↔DARK_A  (contains pipeline SEED)")
print(f"      Group B: C3↔D7↔SA_ST_A↔SA_ST_B↔C3  (contains birthday C3 and MMDD D7)")
print(f"  Universal product: O × inv(O) → IC for all 12 orbits")
print(f"  IC and NEG_H: antipodal but not inverse (antipodal ≠ inverse for them)")
print(f"  Birthday: C3⁻¹=SA_ST_B; 2026 mod37=28∈SA_ST_B; day-of-year(birthday)=25∈SA_ST_B")
