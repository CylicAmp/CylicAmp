"""
T283: Antipodal = negation in GF(37)

The six antipodal orbit pairs are exactly the six negation pairs under −n mod 37.

=== KEY RESULTS ===

1. THE NEGATION PAIRING (six identities)
   −IC = NEG_H       −DARK_A = NQR17     −C3 = D7
   −CAS_EXT = SEED   −TESLA = C9         −SA_ST_A = SA_ST_B

2. ELEMENTWISE SEAM SUMS
   For every x ∈ GF(37)*: x + (−x) ≡ 0 = SEAM (mod 37).
   Every orbit pair sums to SEAM elementwise — 18 equations, all exact.

3. ALGEBRAIC REASON — COMMUTATIVITY OF LINEAR MAPS
   137-map f(x) = 26x and negation g(x) = 36x = −x are both GF(37)* multiplications.
   They commute: f(g(x)) = 26·36·x = 936x ≡ 9x; g(f(x)) = 36·26·x = 936x ≡ 9x.
   So g maps orbits to orbits. g has order 2, no orbit of size 3 is self-negating,
   forcing the 12 orbits to pair into exactly 6 antipodal pairs.

4. NO SELF-NEGATING ORBIT
   An orbit O is self-negating iff −1 ∈ {1, 26, 10} (the stabilizer of the 137-map).
   −1 ≡ 36 ∈ NEG_H. The 137-map stabilizer is IC = {1,10,26}. 36 ∉ IC.
   So no orbit equals its own negation — the 6-pair partition is forced.

5. SEAM AS FIXED POINT
   SEAM (= 0) is the unique fixed point of negation: −0 ≡ 0.
   GF(37)* excludes 0; negation acts on it without fixed points.
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

# ── Part 1: The six negation identities ──────────────────────────────────────

print("Part 1: Antipodal = negation — six orbit identities")

PAIRS = [("IC","NEG_H"),("DARK_A","NQR17"),("C3","D7"),
         ("CAS_EXT","SEED"),("TESLA","C9"),("SA_ST_A","SA_ST_B")]

for O, neg_O in PAIRS:
    neg_set = {(-x) % 37 for x in ORBITS[O]}
    assert neg_set == ORBITS[neg_O], f"−{O} ≠ {neg_O}: got {neg_set}"
    print(f"  −{O:<8} = {neg_O:<8}  {sorted(ORBITS[O])} → {sorted(neg_set)}")

# Verify in both directions
for O, neg_O in PAIRS:
    assert {(-x) % 37 for x in ORBITS[neg_O]} == ORBITS[O]

print(f"  All 6 pairs verified in both directions")
print(f"  Part 1 PASS")

# ── Part 2: Elementwise SEAM sums ────────────────────────────────────────────

print("\nPart 2: Elementwise SEAM sums — every x + (−x) = 37 = SEAM")

count = 0
for O, neg_O in PAIRS:
    for x in sorted(ORBITS[O]):
        nx = (-x) % 37
        assert (x + nx) % 37 == 0, f"{x}+{nx} ≢ 0 mod 37"
        assert x + nx == 37, f"{x}+{nx} ≠ 37"
        assert nx in ORBITS[neg_O], f"-{x}={nx} not in {neg_O}"
        count += 1

assert count == 18  # 6 pairs × 3 elements each = 18 equations

for O, neg_O in PAIRS:
    pairs_str = ", ".join(f"{x}+{(-x)%37}=37" for x in sorted(ORBITS[O]))
    print(f"  {O}↔{neg_O}: {pairs_str}")

print(f"  All 18 elementwise sums = 37 ≡ 0 = SEAM ✓")
print(f"  Part 2 PASS")

# ── Part 3: Algebraic reason — commutativity ─────────────────────────────────

print("\nPart 3: Algebraic reason — f and g commute as GF(37)* multiplications")

MULT = 26   # 137 mod 37 — the 137-map multiplier
NEG  = 36   # −1 mod 37

# f(x) = 26x, g(x) = 36x; composition = multiplication of scalars
fg = (MULT * NEG) % 37   # f∘g = 26×36 mod 37
gf = (NEG * MULT) % 37   # g∘f = 36×26 mod 37
assert fg == gf           # GF(37) is commutative

# Verify on all elements
for x in range(1, 37):
    assert (MULT * ((NEG * x) % 37)) % 37 == (NEG * ((MULT * x) % 37)) % 37

print(f"  f(x) = {MULT}x (137-map), g(x) = {NEG}x = −x")
print(f"  f∘g = {MULT}×{NEG} mod 37 = {fg}")
print(f"  g∘f = {NEG}×{MULT} mod 37 = {gf}")
print(f"  f∘g = g∘f = {fg} (GF(37) multiplication commutes)")
print(f"  Verified on all 36 elements of GF(37)*")
print(f"  Corollary: g maps f-orbits to f-orbits")
print(f"  Part 3 PASS")

# ── Part 4: No self-negating orbit ───────────────────────────────────────────

print("\nPart 4: No self-negating orbit — the 6-pair partition is forced")

# An orbit O is self-negating iff −O = O, i.e., iff −1 acts as a permutation of O.
# −1 = 36. For −1 to map O to itself, 36 must be in the stabilizer of the 137-map,
# i.e., 36 must act as some power of 26 on O. The stabilizer is {1, 26, 10} = IC.
# 36 ∉ IC, so no orbit is self-negating.

stabilizer = {pow(MULT, k, 37) for k in range(3)}
assert stabilizer == {1, 26, 10} == ORBITS["IC"]
assert NEG not in stabilizer  # 36 ∉ IC

# Direct check: no orbit equals its own negation
for name, s in ORBITS.items():
    neg_s = {(-x) % 37 for x in s}
    assert neg_s != s, f"Orbit {name} is self-negating!"

print(f"  137-map stabilizer {{1, 26⁰, 26¹, 26²}} = {{1,26,10}} = IC")
print(f"  −1 = 36 ∈ NEG_H; 36 ∉ IC — −1 is not in the stabilizer")
print(f"  No 3-element orbit equals its own negation (verified all 12 orbits)")
print(f"  Therefore g = (×−1) pairs all 12 orbits into exactly 6 disjoint antipodal pairs")
print(f"  Part 4 PASS")

# ── Part 5: SEAM as fixed point ───────────────────────────────────────────────

print("\nPart 5: SEAM as the unique fixed point of negation")

assert (-0) % 37 == 0          # 0 is fixed
fixed_pts = [x for x in range(37) if (-x) % 37 == x]
assert fixed_pts == [0]        # only 0 in Z/37Z

# In GF(37)*, −x = x iff 2x ≡ 0 iff x = 0. Since 0 ∉ GF(37)*, no fixed points there.
for x in range(1, 37):
    assert (-x) % 37 != x

print(f"  Fixed points of negation in Z/37Z: {fixed_pts}")
print(f"  −0 ≡ 0: SEAM is self-negating (0 = the prime's zero boundary)")
print(f"  GF(37)* = {{1..36}}: zero fixed points of negation")
print(f"  Negation acts on GF(37)* as a fixed-point-free involution")
print(f"  The 6 orbit pairs are the 6 orbits of this involution on {{12 orbits}}")
print(f"  Part 5 PASS")

# ── Part 6: Orbit-level negation table ───────────────────────────────────────

print("\nPart 6: Complete orbit negation table")

print(f"  {'Orbit':<10} {'Elements':>20}  {'−Elements':>20}  {'= Orbit':<10}")
for name, s in sorted(ORBITS.items()):
    neg_s = {(-x) % 37 for x in s}
    neg_name = orbit_of(next(iter(neg_s)))
    print(f"  {name:<10} {str(sorted(s)):>20}  {str(sorted(neg_s)):>20}  {neg_name:<10}")

print(f"  Part 6 PASS")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  −IC=NEG_H, −DARK_A=NQR17, −C3=D7, −CAS_EXT=SEED, −TESLA=C9, −SA_ST_A=SA_ST_B")
print(f"  Antipodal = negation: the six ANTIPODAL pairs are the six negation pairs in GF(37)")
print(f"  Elementwise: x + (−x) = 37 = SEAM for all x ∈ GF(37)* (18 equations, all exact)")
print(f"  Algebraic reason: f(x)=26x and g(x)=36x commute → g maps orbits to orbits")
print(f"  No self-negating orbit: −1=36∈NEG_H ∉ IC (stabilizer) → fixed-point-free pairing")
print(f"  SEAM = unique fixed point of negation in Z/37Z; GF(37)* has zero fixed points")
