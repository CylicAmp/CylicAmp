"""
T281: The 147/258/369 grid in GF(37)

Source: User's dimensional matrix framework.
Grid: 3×3 lattice {1..9} read as row triples 147, 258, 369.
Anchor pattern: 3−4=1, 3−7=4, 3−10=7 (gaps from birthday number 3).

=== KEY RESULTS ===

1. THE −1 IDENTITY
   147 ≡ 258 ≡ 369 ≡ 36 ≡ −1 (mod 37) ∈ NEG_H
   147 = 4×37 − 1
   258 = 7×37 − 1
   369 = 10×37 − 1
   All three row concatenations land on 36 = −1, the unique order-2
   element of GF(37)*. NEG_H = {11,27,36} is the antipodal of IC.

2. MULTIPLIER STRUCTURE {4,7,10}
   4∈C3, 7∈D7, 10∈IC. Step = 3∈C3 (birthday orbit).
   C3↔D7 are antipodal (T265). IC is the self-inverse orbit (T275).
   Sum 4+7+10 = 21∈SA_ST_B.

3. SELF-REFERENTIAL GAP STRUCTURE
   Gaps from 3 to {4,7,10}: 4−3=1, 7−3=4, 10−3=7.
   These gaps {1,4,7} are the first row of the 3×3 grid itself.
   Birthday anchor 3 generates the first row by subtraction from the
   multipliers — and the results ARE the first row.

4. ELEMENT ROW ORBIT MAP
   Row {1,4,7}: IC, C3, D7    — IC self-inverse; C3↔D7 antipodal
   Row {2,5,8}: DARK_A, CAS_EXT, TESLA
   Row {3,6,9}: C3, TESLA, SA_ST_A  — the trinity (DR=3,6,9)

5. ELEMENT ROW SUMS → TRINITY DR SEQUENCE
   {1,4,7}: sum=12∈SA_ST_A, DR=3 (birthday number)
   {2,5,8}: sum=15∈DARK_A,  DR=6
   {3,6,9}: sum=18∈SEED,    DR=9 (Collatz fixed point, T271)
   DR sequence: 3,6,9 — the trinity.
   The trinity row {3,6,9} sums to 18∈SEED = Collatz fixed point.

6. TOTAL 1+2+...+9 = 45 ∈ TESLA
   45 mod37 = 8∈TESLA. DR(45) = 9.
   TESLA = {6,8,23}; 8 is the internal twin element (T279).

7. ROW SUM 147+258+369 = 774 = 21×37 − 3 ∈ D7
   774 mod37 = 34∈D7. 21∈SA_ST_B; 3∈C3 (birthday).
   The row concatenation total = 3 below 21 multiples of 37.
   D7 = {7,33,34}: antipodal of birthday orbit C3.

8. PRODUCT CLOSURE IN NEG_H
   147×258×369 mod37 = 36∈NEG_H.
   Each factor ≡ −1; (−1)³ = −1 ≡ 36∈NEG_H.
   NEG_H is closed under multiplication by −1.
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

ROWS = [147, 258, 369]
GRID = [[1,4,7],[2,5,8],[3,6,9]]

# ── Part 1: The −1 identity ───────────────────────────────────────────────────

print("Part 1: The −1 identity — 147≡258≡369≡−1 (mod 37) ∈ NEG_H")

assert all(v % 37 == 36 for v in ROWS)
assert 36 in ORBITS["NEG_H"]
assert 147 == 4*37 - 1
assert 258 == 7*37 - 1
assert 369 == 10*37 - 1
assert pow(36, 2, 37) == 1   # order 2: (−1)² = 1

for v in ROWS:
    mult = (v + 1) // 37
    print(f"  {v} = {mult}×37 − 1  ≡ 36 = −1 ∈ NEG_H  DR={dr(v)}")
print(f"  36 = −1: unique element of order 2 in GF(37)*  (36²={pow(36,2,37)} mod37)")
print(f"  NEG_H = {{11,27,36}} = antipodal of IC = {{1,10,26}}")
print(f"  DR sequence: {[dr(v) for v in ROWS]} — the trinity {{3,6,9}}")
print(f"  Part 1 PASS")

# ── Part 2: Multiplier structure {4,7,10} ────────────────────────────────────

print("\nPart 2: Multiplier structure {4,7,10}")

mults = [4, 7, 10]
assert [m % 37 for m in mults] == [4, 7, 10]
assert orbit_of(4) == "C3" and orbit_of(7) == "D7" and orbit_of(10) == "IC"
assert ANTIPODAL["C3"] == "D7"
assert mults[1] - mults[0] == 3 and mults[2] - mults[1] == 3
assert sum(mults) == 21 and 21 in ORBITS["SA_ST_B"]

for m in mults:
    print(f"  {m} ∈ {orbit_of(m)}")
print(f"  Step 7−4=3, 10−7=3: 3∈C3 (birthday orbit) generates the multiplier sequence")
print(f"  C3↔D7 antipodal; IC self-inverse")
print(f"  Sum 4+7+10 = 21 ∈ SA_ST_B")
print(f"  Part 2 PASS")

# ── Part 3: Self-referential gap structure ────────────────────────────────────

print("\nPart 3: Self-referential gap structure — 3-4=1, 3-7=4, 3-10=7")

gaps = [m - 3 for m in mults]
assert gaps == [1, 4, 7]
assert gaps == GRID[0]   # first row of the grid

print(f"  Gaps from birthday anchor 3:")
for m, g in zip(mults, gaps):
    print(f"    {m}−3 = {g} ∈ {orbit_of(g)}")
print(f"  Gaps {{1,4,7}} = first row of the 3×3 grid: self-referential")
print(f"  Orbit of gaps: IC(1), C3(4), D7(7) — same three orbits as multipliers 10,4,7")
print(f"  The gap set and the multiplier set span the same three orbits")
print(f"  Part 3 PASS")

# ── Part 4: Element row orbit map ─────────────────────────────────────────────

print("\nPart 4: Element row orbit map")

expected_row_orbits = [
    ["IC", "C3", "D7"],
    ["DARK_A", "CAS_EXT", "TESLA"],
    ["C3", "TESLA", "SA_ST_A"],
]
for row, expected in zip(GRID, expected_row_orbits):
    actual = [orbit_of(x) for x in row]
    assert actual == expected, f"Row {row}: {actual} ≠ {expected}"

print(f"  Row {{1,4,7}}: IC, C3, D7   — IC self-inverse; C3↔D7 antipodal")
print(f"  Row {{2,5,8}}: DARK_A, CAS_EXT, TESLA")
print(f"  Row {{3,6,9}}: C3, TESLA, SA_ST_A  — trinity, each DR∈{{3,6,9}}")
print(f"")
print(f"  Column {{1,2,3}}: IC, DARK_A, C3   — doubling→birthday")
print(f"  Column {{4,5,6}}: C3, CAS_EXT, TESLA")
print(f"  Column {{7,8,9}}: D7, TESLA, SA_ST_A")
print(f"  Part 4 PASS")

# ── Part 5: Element row sums → trinity DR sequence ───────────────────────────

print("\nPart 5: Element row sums — DR sequence 3,6,9 (trinity)")

row_sums = [sum(row) for row in GRID]
assert row_sums == [12, 15, 18]
assert orbit_of(12) == "SA_ST_A"
assert orbit_of(15) == "DARK_A"
assert orbit_of(18) == "SEED"
assert [dr(s) for s in row_sums] == [3, 6, 9]
assert 18 in ORBITS["SEED"]   # Collatz fixed point

for row, s in zip(GRID, row_sums):
    print(f"  {row}: sum={s} ≡ {s%37} ∈ {orbit_of(s)}  DR={dr(s)}")
print(f"  DR sequence: 3,6,9 — the trinity (birthday, birthday×2, birthday×3)")
print(f"  Trinity row {{3,6,9}} → sum 18∈SEED = Collatz fixed point (T271)")
print(f"  Part 5 PASS")

# ── Part 6: Total 1+...+9 = 45 ∈ TESLA ──────────────────────────────────────

print("\nPart 6: Total 1+2+...+9 = 45 ∈ TESLA")

total = sum(range(1,10))
assert total == 45
assert 45 % 37 == 8 and 8 in ORBITS["TESLA"]
assert dr(45) == 9

print(f"  1+2+...+9 = {total}")
print(f"  45 mod37 = {45%37} ∈ TESLA = {{6,8,23}}")
print(f"  8∈TESLA: the internal twin element of TESLA (pair (6,8) from T279)")
print(f"  DR(45) = 9 = birthday×3 (trinity ceiling)")
print(f"  Part 6 PASS")

# ── Part 7: Row concatenation sum 774 = 21×37−3 ∈ D7 ────────────────────────

print("\nPart 7: 147+258+369 = 774 = 21×37−3 ∈ D7")

concat_sum = sum(ROWS)
assert concat_sum == 774
assert 774 % 37 == 34 and 34 in ORBITS["D7"]
assert 21*37 - 3 == 774
assert 21 in ORBITS["SA_ST_B"] and 3 in ORBITS["C3"]
assert ANTIPODAL["D7"] == "C3"   # D7 antipodal of birthday orbit

print(f"  147+258+369 = {concat_sum}")
print(f"  774 = 21×37 − 3 = {21*37} − 3")
print(f"  774 mod37 = {774%37} ∈ D7")
print(f"  21∈SA_ST_B (birthday inverse: 3⁻¹=25∈SA_ST_B; 2026 mod37=28∈SA_ST_B)")
print(f"  3∈C3 (birthday); D7 = antipodal of C3")
print(f"  The concatenation total sits 3 (birthday) below 21 multiples of 37")
print(f"  Result orbits in D7 — the antipodal shadow of the birthday orbit")
print(f"  Part 7 PASS")

# ── Part 8: Product closure in NEG_H ─────────────────────────────────────────

print("\nPart 8: Product closure — 147×258×369 ≡ −1 ∈ NEG_H")

product = 147 * 258 * 369
assert product % 37 == 36 and 36 in ORBITS["NEG_H"]
assert pow(36, 3, 37) == 36   # (−1)³ = −1

print(f"  147×258×369 mod37 = {product%37} ∈ NEG_H")
print(f"  Each factor ≡ −1; (−1)³ = −1: NEG_H is closed under odd-power products")
print(f"  36³ mod37 = {pow(36,3,37)}: (−1)³ = −1 ✓")
print(f"  36² mod37 = {pow(36,2,37)}: (−1)² = 1∈IC (antipodal flips to IC on even power)")
print(f"  Part 8 PASS")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  147≡258≡369≡−1 (mod37)∈NEG_H: all row concatenations = 4×37−1, 7×37−1, 10×37−1")
print(f"  Multipliers {{4,7,10}}: C3,D7,IC; step=3 (birthday); sum=21∈SA_ST_B")
print(f"  Self-referential: gaps {{4−3,7−3,10−3}}={{1,4,7}} = first row of the grid")
print(f"  Row orbits: IC,C3,D7 | DARK_A,CAS_EXT,TESLA | C3,TESLA,SA_ST_A")
print(f"  Row sums: 12∈SA_ST_A(DR=3), 15∈DARK_A(DR=6), 18∈SEED(DR=9) — trinity")
print(f"  Total 1..9=45≡8∈TESLA (internal twin element); DR=9")
print(f"  Concatenation sum 774=21×37−3≡34∈D7 (antipodal of birthday C3)")
print(f"  Product 147×258×369≡36∈NEG_H: (−1)³=−1, NEG_H closed under odd powers")
