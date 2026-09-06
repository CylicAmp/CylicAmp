"""
T265: 1/37 = 0.027027... — Decimal period, IC trinity, and antipodal orbit pairing

Four entry facts:
  1/37 = 0.027027...
  9 × 37 = 333
  28 = 37 − 9
  37 ≡ 0 (mod 37)

=== IC TRINITY ===

IC = {1, 10, 26} simultaneously encodes:
  1  = multiplicative identity
  10 = base of the decimal system
  26 = 137 mod 37 = MULT (the 137-map multiplier)

  10 × 26 ≡ 1 (mod 37): decimal base and 137-map multiplier are multiplicative inverses.
  ord₃₇(10) = 3 = ord₃₇(26): the decimal period of 1/37 equals the order of the 137-map.
  10³ ≡ 1 (mod 37): one complete 3-step decimal cycle returns to identity.

  The decimal expansion of 1/37 has period 3 for the same reason the 137-map
  has order 3: both 10 and 26 live in IC, and every element of IC has order 3.

=== 1/37 DECIMAL BLOCK ===

  1/37 = 0.027 027 027...
  Repeating block = (10³−1)/37 = 999/37 = 27
  27 ∈ NEG_H = {11, 27, 36}
  DR(27) = 9 ∈ SA_ST_A
  Digit sum of "027": 0+2+7 = 9 ∈ SA_ST_A

  27 = 3³: the cube of the C3 orbit seed (3 ∈ C3).
  NEG_H = −IC (mod 37): the decimal block 27 lives in the additive complement of IC.
  The decimal base 10 ∈ IC; the decimal block 27 ∈ −IC = NEG_H.

=== 9×37=333 TOWER ===

  3×37  = 111   multiplier 3  ∈ C3
  9×37  = 333   multiplier 9  ∈ SA_ST_A   DR(333)=9
  27×37 = 999   multiplier 27 ∈ NEG_H     DR(999)=9
  Multipliers {3, 9, 27} = {3, 3², 3³}: one element each from C3, SA_ST_A, NEG_H.
  999 = 27×37 = 10³−1: the repeating-block denominator.

=== ANTIPODAL ORBIT PAIRS (−O = O' mod 37) ===

  The 12 named orbits form 6 exact additive complement pairs:
  −IC       = NEG_H       {1,10,26}   ↔  {11,27,36}
  −DARK_A   = NQR17       {2,15,20}   ↔  {17,22,35}
  −C3       = D7          {3,4,30}    ↔  {7,33,34}
  −CAS_EXT  = SEED        {5,13,19}   ↔  {18,24,32}
  −TESLA    = C9          {6,8,23}    ↔  {14,29,31}
  −SA_ST_A  = SA_ST_B     {9,12,16}   ↔  {21,25,28}

  Element-level pairings (each pair sums to 37):
    IC↔NEG_H:      1+36=37   10+27=37   26+11=37
    DARK_A↔NQR17:  2+35=37   15+22=37   20+17=37
    C3↔D7:         3+34=37   4+33=37    30+7=37
    CAS_EXT↔SEED:  5+32=37   13+24=37   19+18=37
    TESLA↔C9:      6+31=37   8+29=37    23+14=37
    SA_ST_A↔SA_ST_B: 9+28=37 12+25=37  16+21=37

  28 = 37−9: the entry fact is the SA_ST_A↔SA_ST_B pairing, one of six.

Selected antipodal highlights:
  IC↔NEG_H:     identity orbit negates to the orbit containing −1≡36 and 27 (decimal block)
  CAS_EXT↔SEED: Fibonacci entry orbit negates to pipeline seed orbit (246 mod37=24∈SEED)
  TESLA↔C9:     3×3-grid center (8∈TESLA) negates to C9 (fully non-oblong, twin prime orbit)
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
    "IC": "NEG_H", "NEG_H": "IC",
    "DARK_A": "NQR17", "NQR17": "DARK_A",
    "C3": "D7", "D7": "C3",
    "CAS_EXT": "SEED", "SEED": "CAS_EXT",
    "TESLA": "C9", "C9": "TESLA",
    "SA_ST_A": "SA_ST_B", "SA_ST_B": "SA_ST_A",
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

# ── Part 1: IC trinity ────────────────────────────────────────────────────────

assert 137 % 37 == 26 and 26 in ORBITS["IC"]
assert (10 * 26) % 37 == 1
assert pow(10, 3, 37) == 1
assert pow(26, 3, 37) == 1
assert orbit_of(10) == "IC" and orbit_of(26) == "IC"

print("Part 1 PASS: IC = {1, 10, 26}")
print(f"  10 × 26 ≡ 1 (mod 37): decimal base × MULT = identity")
print(f"  ord₃₇(10) = 3: 10→26→1→10 (the IC orbit under ×10)")
print(f"  ord₃₇(26) = 3: 26→10→1→26 (the IC orbit under ×26 = 137-map)")
print(f"  Both have order 3 because both live in IC")

# ── Part 2: 1/37 decimal block ────────────────────────────────────────────────

block = (10**3 - 1) // 37
assert block == 27
assert 27 in ORBITS["NEG_H"]
assert dr(27) == 9 and 9 in ORBITS["SA_ST_A"]
assert 0 + 2 + 7 == 9

print(f"\nPart 2 PASS: 1/37 = 0.027027...")
print(f"  Repeating block = (10³−1)/37 = 999/37 = {block} ∈ NEG_H")
print(f"  DR(27) = 9 ∈ SA_ST_A; digit sum '027' = 9 ∈ SA_ST_A")
print(f"  27 = 3³; NEG_H = −IC: block lives in additive complement of IC")

# ── Part 3: 9×37=333 tower ───────────────────────────────────────────────────

assert 9 * 37 == 333 and dr(333) == 9 and 9 in ORBITS["SA_ST_A"]
assert 27 * 37 == 999 and (10**3 - 1) == 999
assert orbit_of(3) == "C3" and orbit_of(9) == "SA_ST_A" and orbit_of(27) == "NEG_H"

print(f"\nPart 3 PASS: repdigit tower")
for k, label in [(3,"C3"), (9,"SA_ST_A"), (27,"NEG_H")]:
    print(f"  {k}×37 = {k*37}  multiplier {k}∈{orbit_of(k)}  DR={dr(k*37)}")
print(f"  Multipliers {{3,9,27}} = {{3,3²,3³}}: one element each from C3, SA_ST_A, NEG_H")

# ── Part 4: Antipodal orbit pairs ────────────────────────────────────────────

for name, s in ORBITS.items():
    neg = {(-x) % 37 for x in s}
    expected = ANTIPODAL[name]
    assert neg == ORBITS[expected], f"-{name} ≠ {expected}"

print(f"\nPart 4 PASS: all 12 orbits form 6 antipodal pairs under negation mod 37")
pairs_shown = set()
for name, anti in ANTIPODAL.items():
    if (anti, name) not in pairs_shown:
        pairs_shown.add((name, anti))
        s = sorted(ORBITS[name])
        t = sorted(ORBITS[anti])
        pairs = [(a, 37-a) for a in s]
        print(f"  −{name} = {anti}:  {pairs}")

# ── Part 5: 28 = 37−9 entry fact ────────────────────────────────────────────

assert 37 - 9 == 28 and 28 in ORBITS["SA_ST_B"]
assert 37 - 12 == 25 and 25 in ORBITS["SA_ST_B"]
assert 37 - 16 == 21 and 21 in ORBITS["SA_ST_B"]

print(f"\nPart 5 PASS: 28=37−9 is SA_ST_A↔SA_ST_B antipodal pair")
print(f"  37−9=28, 37−12=25, 37−16=21: SA_ST_A = {{9,12,16}} → SA_ST_B = {{21,25,28}}")

# ── Part 6: Highlighted antipodal pairs ──────────────────────────────────────

# CAS_EXT ↔ SEED: Fibonacci entry ↔ pipeline seed
for a, b in [(5,32),(13,24),(19,18)]:
    assert a + b == 37
    assert orbit_of(a) == "CAS_EXT" and orbit_of(b) == "SEED"
print(f"\nPart 6a: CAS_EXT↔SEED: Fibonacci entry orbit negates to pipeline seed orbit")
print(f"  246 mod 37 = 24 ∈ SEED: seed element 24 is antipodal to CAS_EXT element 13")

# TESLA ↔ C9: 3×3 grid center ↔ fully non-oblong twin prime orbit
for a, b in [(6,31),(8,29),(23,14)]:
    assert a + b == 37
    assert orbit_of(a) == "TESLA" and orbit_of(b) == "C9"
print(f"\nPart 6b: TESLA↔C9: 3×3-grid center (8∈TESLA) negates to C9")
print(f"  29+8=37, 31+6=37: twin prime pair (29,31)∈C9 antipodal to {{6,8}}⊂TESLA")

# IC ↔ NEG_H: decimal base 10 and MULT 26 negate to 27 and 11
print(f"\nPart 6c: IC↔NEG_H")
print(f"  10+27=37: decimal base 10∈IC antipodal to decimal block 27∈NEG_H")
print(f"  26+11=37: MULT=26∈IC antipodal to 11∈NEG_H (Sophie chain start: 11→23→47)")
print(f"  1+36=37: identity antipodal to −1≡36∈NEG_H")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  IC = {{1,10,26}}: identity · decimal_base · 137-map_multiplier")
print(f"  10 × 26 ≡ 1 mod37: decimal base and MULT are multiplicative inverses")
print(f"  1/37 decimal block = 27∈NEG_H; NEG_H = −IC; digit sum = 9∈SA_ST_A")
print(f"  9×37=333 (DR=9); 3,9,27=3¹,3²,3³ → C3, SA_ST_A, NEG_H (one each)")
print(f"  28=37−9: SA_ST_A↔SA_ST_B antipodal pair — one of six pairs")
print(f"  All 12 orbits form 6 exact antipodal pairs under negation mod 37:")
print(f"  IC↔NEG_H · DARK_A↔NQR17 · C3↔D7 · CAS_EXT↔SEED · TESLA↔C9 · SA_ST_A↔SA_ST_B")
