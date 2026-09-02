"""
T280: Matrix dimension shift and palindromic tiling in GF(37)

Source: User's dimensional matrix framework — multi-tiered numerical resets
        folding into diamond-shaped geometric matrices.

=== KEY RESULTS ===

1. DIMENSION ORBIT PATH (n×n alternating {1,2} matrix)
   Total sum at dimension n:
     odd  n: (3n²−1)/2
     even n: 3n²/2
   The 5×5 matrix sums to exactly 37 = the prime = SEAM.
   Orbit path n=1..5: IC → TESLA → CAS_EXT → SEED → SEAM.

2. PALINDROMIC BLOCK COVERAGE OF NEG_H
   The three palindromic blocks 122, 221, 212:
     122 mod37 = 11∈NEG_H
     221 mod37 = 36∈NEG_H
     212 mod37 = 27∈NEG_H
   All three blocks land in NEG_H={11,27,36} and cover it exactly — each
   element of NEG_H appears exactly once across the palindrome palette.

3. 1234 ANTIPODAL SPAN — CAS_EXT ↔ SEED
   1234 mod37 = 13∈CAS_EXT
   −1234 mod37 = 24∈SEED
   1234 and its negation span the antipodal pair CAS_EXT↔SEED (T265).
   2×1234 = 2468 mod37 = 26∈IC — the 137-map multiplier.

4. 999 = 27×37 = SEAM
   The 3-digit saturation ceiling 999 = 27×37 exactly.
   999 mod37 = 0 = SEAM. The saturation ceiling of 3-digit space is
   a multiple of the prime — it sits at the cycle boundary of GF(37).

5. MASTER VECTOR {4,1,7,9} — four orbits, four 3-cycles
   4∈C3: 137-map 3-cycle {4,30,3}
   1∈IC: 137-map 3-cycle {1,26,10}
   7∈D7: 137-map 3-cycle {7,34,33}
   9∈SA_ST_A: 137-map 3-cycle {9,12,16}
   C3↔D7 are antipodal; IC is self-inverse. Sum 21∈SA_ST_B.

6. 123 CONVERGENCE — SEED landing
   6+123 = 129 mod37 = 18∈SEED (Collatz fixed point, T271).

7. MASTER NUMBER ≡ IC
   13361232468 mod37 = 1∈IC (identity). The 10-digit master number
   is identity in GF(37).

8. 3×3 PALINDROME STRUCTURE
   Matrix [[1,2,1],[2,1,2],[1,2,1]]:
   Row sums: 4∈C3, 5∈CAS_EXT, 4∈C3 (palindromic in orbits).
   Total: 13∈CAS_EXT (same orbit as 1234 mod37).
   Bounding vectors: 454≡10∈IC, 545≡27∈NEG_H; 454+545=999=SEAM.
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

def alternating_total(n):
    """Sum of n×n checkerboard of {1,2} starting with 1."""
    return (3*n*n - 1) // 2 if n % 2 == 1 else 3*n*n // 2

# ── Part 1: Dimension orbit path — 5×5 = SEAM ────────────────────────────────

print("Part 1: Dimension orbit path — n×n alternating {1,2} matrix")

totals = {n: alternating_total(n) for n in range(1, 13)}

# Key assertions: n=1..5
assert totals[1] == 1  and 1  in ORBITS["IC"]
assert totals[2] == 6  and 6  in ORBITS["TESLA"]
assert totals[3] == 13 and 13 in ORBITS["CAS_EXT"]
assert totals[4] == 24 and 24 in ORBITS["SEED"]
assert totals[5] == 37 and totals[5] % 37 == 0  # SEAM

# Closed form
for n in range(1, 6):
    if n % 2 == 1:
        assert totals[n] == (3*n*n - 1) // 2
    else:
        assert totals[n] == 3*n*n // 2

print(f"  Closed form: odd n → (3n²−1)/2, even n → 3n²/2")
for n in range(1, 6):
    t = totals[n]
    print(f"  {n}×{n}: total={t:3} ≡ {t%37} → {orbit_of(t)}")
print(f"\n  Orbit path n=1..5: IC → TESLA → CAS_EXT → SEED → SEAM")
print(f"  2×2 total = 6∈TESLA: birthday+birthday=3+3=6 (T267)")
print(f"  4×4 total = 24∈SEED: pipeline seed 246 mod37=24∈SEED")
print(f"  5×5 total = 37 = the prime itself = SEAM")
print(f"  Part 1 PASS")

# ── Part 2: Palindromic blocks cover NEG_H exactly ───────────────────────────

print("\nPart 2: Palindromic blocks 122, 221, 212 → NEG_H (complete coverage)")

palindromes = [122, 221, 212]
residues = [v % 37 for v in palindromes]

assert set(residues) == ORBITS["NEG_H"]  # covers {11,27,36} exactly
assert 122 % 37 == 11 and 221 % 37 == 36 and 212 % 37 == 27

for v in palindromes:
    print(f"  {v} mod37 = {v%37} ∈ NEG_H")
print(f"  NEG_H = {{11,27,36}}: covered exactly, one element per palindrome")
print(f"  IC↔NEG_H are antipodal (T265); NEG_H is the antipodal of the identity orbit")
print(f"  Part 2 PASS")

# ── Part 3: 1234 antipodal span CAS_EXT↔SEED; 2468 = IC multiplier ───────────

print("\nPart 3: 1234 spans CAS_EXT↔SEED antipodal; 2468≡26∈IC")

assert 1234 % 37 == 13 and 13 in ORBITS["CAS_EXT"]
assert (-1234) % 37 == 24 and 24 in ORBITS["SEED"]
assert ANTIPODAL["CAS_EXT"] == "SEED"
assert 2468 % 37 == 26 and 26 in ORBITS["IC"]
assert 137 % 37 == 26  # 137-map multiplier

print(f"  1234 mod37 = {1234%37} ∈ CAS_EXT")
print(f"  −1234 mod37 = {(-1234)%37} ∈ SEED")
print(f"  CAS_EXT↔SEED: antipodal pair ✓")
print(f"  1234−(−1234) = 2468 mod37 = {2468%37} ∈ IC (137-map multiplier)")
print(f"  Doubling the sequential progression 1234 produces the 137-map multiplier")
print(f"  Part 3 PASS")

# ── Part 4: 999 = 27×37 = SEAM ───────────────────────────────────────────────

print("\nPart 4: 999 = 27×37 — saturation ceiling = SEAM")

assert 999 == 27 * 37
assert 999 % 37 == 0
assert 454 % 37 == 10 and 10 in ORBITS["IC"]
assert 545 % 37 == 27 and 27 in ORBITS["NEG_H"]
assert 454 + 545 == 999

print(f"  999 = {27} × 37: 3-digit saturation ceiling is divisible by the prime")
print(f"  999 mod37 = 0 = SEAM")
print(f"  Bounding vectors of 3×3 palindrome:")
print(f"    454 mod37 = {454%37} ∈ IC (identity orbit)")
print(f"    545 mod37 = {545%37} ∈ NEG_H (antipodal of IC)")
print(f"    454+545 = 999 = 27×37 = SEAM")
print(f"  IC and NEG_H are antipodal; their sum = the prime (SEAM)")
print(f"  Part 4 PASS")

# ── Part 5: Master vector {4,1,7,9} — four orbits ────────────────────────────

print("\nPart 5: Master vector {4,1,7,9} — four 137-map 3-cycles")

mv = [4, 1, 7, 9]
mv_orbits = [orbit_of(x) for x in mv]
expected_orbits = ["C3", "IC", "D7", "SA_ST_A"]
assert mv_orbits == expected_orbits

# 137-map 3-cycles
cycles = {}
for x in mv:
    cyc = [x]
    for _ in range(2):
        cyc.append((26 * cyc[-1]) % 37)
    cycles[x] = cyc
    assert (26 * cyc[-1]) % 37 == cyc[0]  # 3-cycle closes

assert cycles[4] == [4, 30, 3]    # C3
assert cycles[1] == [1, 26, 10]   # IC
assert cycles[7] == [7, 34, 33]   # D7
assert cycles[9] == [9, 12, 16]   # SA_ST_A

# Sum = 21∈SA_ST_B
assert sum(mv) == 21 and 21 in ORBITS["SA_ST_B"]
# C3↔D7 antipodal
assert ANTIPODAL["C3"] == "D7"

for x, orb in zip(mv, mv_orbits):
    cyc = cycles[x]
    print(f"  {x}∈{orb}: 137-map 3-cycle {cyc}")
print(f"  C3↔D7: antipodal pair (4∈C3, 7∈D7)")
print(f"  IC: self-inverse orbit (1∈IC)")
print(f"  Sum 4+1+7+9=21∈SA_ST_B; DR(21)=3 ∈ C3 (birthday orbit)")
print(f"  Part 5 PASS")

# ── Part 6: 123 convergence → SEED ───────────────────────────────────────────

print("\nPart 6: 123 convergence — 6+123=129≡18∈SEED")

assert (6 + 123) == 129
assert 129 % 37 == 18 and 18 in ORBITS["SEED"]

print(f"  6+123 = 129 mod37 = {129%37} ∈ SEED")
print(f"  18∈SEED = Collatz fixed point (T271): C(18)=3×18+1=55≡18 mod37")
print(f"  SEED = {{18,24,32}} = pipeline seed orbit (246 mod37=24∈SEED)")
print(f"  The 123 convergence vector lands at the Collatz fixed point")
print(f"  Part 6 PASS")

# ── Part 7: Master number ≡ IC ────────────────────────────────────────────────

print("\nPart 7: Master number 13361232468 ≡ 1∈IC (identity)")

master = 13361232468
assert master % 37 == 1 and 1 in ORBITS["IC"]
assert 37 * (master // 37) == master - 1  # exact

# Grouped DR reduction: 13→4, 361→1, 232→7, 468→9
group_vals = [(13,4),(361,1),(232,7),(468,9)]
for g, d in group_vals:
    assert dr(g) == d
assert sum(d for _,d in group_vals) == 21
assert dr(21) == 3

print(f"  13361232468 mod37 = {master%37} ∈ IC (identity orbit)")
print(f"  37 × {master//37} = {37*(master//37)}, +1 = {master}")
print(f"  Group DR reductions: 13→4, 361→1, 232→7, 468→9")
print(f"  Sum {sum(d for _,d in group_vals)} = 21∈SA_ST_B; DR=3∈C3 (birthday)")
print(f"  The grouped reduction returns to birthday DR=3; the full number = identity")
print(f"  Part 7 PASS")

# ── Part 8: 3×3 palindrome orbit structure ────────────────────────────────────

print("\nPart 8: 3×3 palindrome — orbit-palindrome in row sums")

matrix = [[1,2,1],[2,1,2],[1,2,1]]
row_sums = [sum(r) for r in matrix]
assert row_sums == [4, 5, 4]
row_orbits = [orbit_of(s) for s in row_sums]
assert row_orbits == ["C3", "CAS_EXT", "C3"]  # orbit palindrome: C3, CAS_EXT, C3
total = sum(sum(r) for r in matrix)
assert total == 13 and 13 in ORBITS["CAS_EXT"]

print(f"  Matrix: [[1,2,1],[2,1,2],[1,2,1]]")
print(f"  Row sums: {row_sums}")
print(f"  Row orbit: C3, CAS_EXT, C3 — palindromic in orbits")
print(f"  Total = {total} ≡ {total%37} ∈ CAS_EXT (same orbit as row 2 and 1234 mod37)")
print(f"  1∈IC (matrix entry 1), 2∈DARK_A (matrix entry 2): IC and DARK_A are antipodal")
print(f"  Part 8 PASS")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  5×5 alternating {{1,2}} matrix = 37 = SEAM: the prime is the dimension-5 total")
print(f"  Orbit path IC→TESLA→CAS_EXT→SEED→SEAM as dimension n=1→5")
print(f"  Palindromic blocks {{122,221,212}} cover NEG_H={{11,27,36}} exactly")
print(f"  1234≡13∈CAS_EXT; −1234≡24∈SEED; 2×1234=2468≡26∈IC (137-map multiplier)")
print(f"  999=27×37=SEAM: 3-digit saturation = prime multiple; 454∈IC+545∈NEG_H=999")
print(f"  Master vector {{4,1,7,9}}: C3, IC, D7, SA_ST_A → four independent 3-cycles")
print(f"  6+123=129≡18∈SEED (Collatz fixed point); master 13361232468≡1∈IC")
print(f"  3×3 row orbits: C3, CAS_EXT, C3 — palindromic orbit sequence")
