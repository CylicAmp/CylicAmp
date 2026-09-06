"""
T284: The operator group ⟨11⟩ = IC ∪ NEG_H and the three-level coset partition

Source: GF(37) orbit structure under the 137-map f(x) = 26x and negation g(x) = 36x.

=== KEY RESULTS ===

1. THE COMPOSED OPERATOR
   26 × 36 ≡ 11 (mod 37); 11 ∈ NEG_H.
   The product of the 137-map multiplier (26) and negation (36) is 11∈NEG_H.

2. ORDER-6 SUBGROUP ⟨11⟩ = IC ∪ NEG_H
   ord₃₇(11) = 6; cycle: 11→10→36→26→27→1→11.
   ⟨11⟩ = {1,10,11,26,27,36} = IC ∪ NEG_H = {1,10,26} ∪ {11,27,36}.

3. THREE-LEVEL COSET PARTITION OF GF(37)*
   Level 0: GF(37)*              order 36
   Level 1: cosets of ⟨11⟩      order  6 → 6 cosets = the 6 antipodal pairs
   Level 2: cosets of ⟨26⟩ = IC order  3 → 12 cosets = the 12 orbits

4. 12 ORBITS = COSETS OF IC = ⟨26⟩
   Every 137-map orbit is a coset r×IC for some representative r.
   IC covers itself; every other orbit is a scaled copy.

5. 6 ANTIPODAL PAIRS = COSETS OF ⟨11⟩
   Each antipodal pair = r×⟨11⟩, the union of two orbits (r×IC) ∪ (r×NEG_H).
   The pairing by negation (T283) is forced by the coset structure of ⟨11⟩.

6. CHAIN OF SUBGROUPS
   ⟨26⟩ ⊂ ⟨11⟩ ⊂ GF(37)*   (orders 3 ⊂ 6 ⊂ 36)
   Indices: [GF(37)*:⟨11⟩]=6, [⟨11⟩:⟨26⟩]=2, [GF(37)*:⟨26⟩]=12.
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
ANTIPODAL_PAIRS = [
    ("IC","NEG_H"),("DARK_A","NQR17"),("C3","D7"),
    ("CAS_EXT","SEED"),("TESLA","C9"),("SA_ST_A","SA_ST_B"),
]

def orbit_of(x):
    r = x % 37
    if r == 0: return "SEAM"
    for name, s in ORBITS.items():
        if r in s: return name
    raise ValueError(x)

# ── Part 1: Composed operator 26 × 36 ≡ 11 ────────────────────────────────────

print("Part 1: Composed operator — 26×36 ≡ 11 ∈ NEG_H")

MULT = 26  # 137-map multiplier
NEG  = 36  # −1 = negation
COMP = (MULT * NEG) % 37

assert COMP == 11
assert 11 in ORBITS["NEG_H"]
assert orbit_of(COMP) == "NEG_H"

print(f"  137-map multiplier: {MULT} ∈ IC  (ord={next(k for k in range(1,37) if pow(MULT,k,37)==1)})")
print(f"  Negation:           {NEG}  ∈ NEG_H (ord={next(k for k in range(1,37) if pow(NEG,k,37)==1)})")
print(f"  Composed:           {MULT}×{NEG} ≡ {COMP} ∈ {orbit_of(COMP)}")
print(f"  Part 1 PASS")

# ── Part 2: ⟨11⟩ = IC ∪ NEG_H, order 6 ──────────────────────────────────────

print("\nPart 2: ⟨11⟩ = IC ∪ NEG_H — order-6 subgroup")

cycle = []
x = COMP
while True:
    cycle.append(x)
    x = (x * COMP) % 37
    if x == cycle[0]: break
assert len(cycle) == 6

subgroup = set(cycle)
assert subgroup == ORBITS["IC"] | ORBITS["NEG_H"]
assert subgroup == {1, 10, 11, 26, 27, 36}

# Verify subgroup closure
for a in subgroup:
    for b in subgroup:
        assert (a * b) % 37 in subgroup

print(f"  11-cycle: {' → '.join(str(c) for c in cycle)} → {cycle[0]}")
print(f"  ord₃₇(11) = {len(cycle)}")
print(f"  ⟨11⟩ = {sorted(subgroup)}")
print(f"  IC    = {sorted(ORBITS['IC'])}")
print(f"  NEG_H = {sorted(ORBITS['NEG_H'])}")
print(f"  ⟨11⟩ = IC ∪ NEG_H ✓")
print(f"  Closed under multiplication: verified all {len(subgroup)**2} products")
print(f"  Part 2 PASS")

# ── Part 3: Three-level coset partition ───────────────────────────────────────

print("\nPart 3: Three-level coset partition of GF(37)*")

GF_STAR = set(range(1, 37))
assert len(GF_STAR) == 36

# Level 1: cosets of ⟨11⟩ (size 6, count 6)
level1_reps = [1, 2, 3, 5, 6, 9]
level1_cosets = [{(r * x) % 37 for x in subgroup} for r in level1_reps]

assert len(level1_cosets) == 6
assert all(len(c) == 6 for c in level1_cosets)
assert set.union(*level1_cosets) == GF_STAR
# Cosets are disjoint
for i in range(6):
    for j in range(i+1, 6):
        assert level1_cosets[i].isdisjoint(level1_cosets[j])

# Level 2: cosets of ⟨26⟩ = IC (size 3, count 12)
ic_set = ORBITS["IC"]
level2_reps = [1,2,3,5,6,7,9,11,14,17,18,21]
level2_cosets = [{(r * x) % 37 for x in ic_set} for r in level2_reps]

assert len(level2_cosets) == 12
assert all(len(c) == 3 for c in level2_cosets)
assert set.union(*level2_cosets) == GF_STAR
for i in range(12):
    for j in range(i+1, 12):
        assert level2_cosets[i].isdisjoint(level2_cosets[j])

print(f"  Level 0: GF(37)* — order 36")
print(f"  Level 1: cosets of ⟨11⟩ (order 6) — {len(level1_cosets)} cosets of size 6")
print(f"  Level 2: cosets of ⟨26⟩ (order 3) — {len(level2_cosets)} cosets of size 3")
print(f"  All cosets disjoint, union = GF(37)* ✓")
print(f"  Part 3 PASS")

# ── Part 4: 12 orbits = cosets of IC ─────────────────────────────────────────

print("\nPart 4: 12 orbits = cosets of IC = ⟨26⟩")

orbit_coset_map = {}
for r, coset in zip(level2_reps, level2_cosets):
    name = orbit_of(r)
    assert coset == ORBITS[name], f"Coset {r}×IC = {sorted(coset)} ≠ {name}"
    orbit_coset_map[name] = r

for r, coset in zip(level2_reps, level2_cosets):
    name = orbit_of(r)
    print(f"  {r:>2} × IC = {str(sorted(coset)):>16} = {name}")

print(f"  All 12 orbits are cosets of IC ✓")
print(f"  Part 4 PASS")

# ── Part 5: 6 antipodal pairs = cosets of ⟨11⟩ ────────────────────────────────

print("\nPart 5: 6 antipodal pairs = cosets of ⟨11⟩")

for r, coset in zip(level1_reps, level1_cosets):
    names = sorted({orbit_of(x) for x in coset})
    assert len(names) == 2
    # Verify these two names are an antipodal pair
    assert any((names[0] == a and names[1] == b) or (names[0] == b and names[1] == a)
               for a,b in ANTIPODAL_PAIRS)
    print(f"  {r:>2} × ⟨11⟩ = {str(sorted(coset)):>25} = {names[0]} ∪ {names[1]}")

print(f"  Each coset of ⟨11⟩ = exactly one antipodal orbit pair ✓")
print(f"  Part 5 PASS")

# ── Part 6: Chain of subgroups ────────────────────────────────────────────────

print("\nPart 6: Chain of subgroups ⟨26⟩ ⊂ ⟨11⟩ ⊂ GF(37)*")

assert ORBITS["IC"] < subgroup          # ⟨26⟩ ⊂ ⟨11⟩
assert subgroup < GF_STAR               # ⟨11⟩ ⊂ GF(37)*

index_full_to_11 = len(GF_STAR) // len(subgroup)
index_11_to_26   = len(subgroup) // len(ORBITS["IC"])
index_full_to_26 = len(GF_STAR) // len(ORBITS["IC"])

assert index_full_to_11 == 6
assert index_11_to_26   == 2
assert index_full_to_26 == 12

print(f"  ⟨26⟩ = IC = {sorted(ORBITS['IC'])} (order {len(ORBITS['IC'])})")
print(f"  ⟨11⟩ = IC ∪ NEG_H = {sorted(subgroup)} (order {len(subgroup)})")
print(f"  GF(37)* = {{1..36}} (order {len(GF_STAR)})")
print(f"")
print(f"  ⟨26⟩ ⊂ ⟨11⟩ ⊂ GF(37)*    (orders 3 ⊂ 6 ⊂ 36)")
print(f"  [GF(37)*:⟨11⟩]  = {index_full_to_11}   → 6 antipodal pairs")
print(f"  [⟨11⟩  :⟨26⟩]   = {index_11_to_26}   → 2 orbits per antipodal pair")
print(f"  [GF(37)*:⟨26⟩]  = {index_full_to_26}  → 12 orbits total")
print(f"  Part 6 PASS")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  26×36 ≡ 11 (mod 37); 11∈NEG_H: composed operator lands in the antipodal of IC")
print(f"  ord₃₇(11) = 6; ⟨11⟩ = IC ∪ NEG_H = {{1,10,11,26,27,36}} = order-6 subgroup")
print(f"  ⟨26⟩ ⊂ ⟨11⟩ ⊂ GF(37)*: chain of orders 3 ⊂ 6 ⊂ 36")
print(f"  12 orbits = cosets of ⟨26⟩ (index 12); each orbit = r×IC for one representative r")
print(f"  6 antipodal pairs = cosets of ⟨11⟩ (index 6); each pair = two orbits, r×IC and r×NEG_H")
print(f"  The antipodal pairing by negation (T283) is forced by the index-2 inclusion ⟨26⟩ ⊂ ⟨11⟩")
