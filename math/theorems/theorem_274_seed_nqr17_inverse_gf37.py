"""
T274: SEED ↔ NQR17 — complete multiplicative inverse orbits in GF(37)

SEED   = {18, 24, 32}   pipeline reference orbit; seed 246 mod37=24∈SEED
NQR17  = {17, 22, 35}   named for smallest element, 17 (prime)

=== COMPLETE INVERSE PAIRING ===

Every element of SEED is the multiplicative inverse of an element of NQR17:

  18 × 35 ≡ 1 (mod 37)    [630 = 17×37 + 1]
  24 × 17 ≡ 1 (mod 37)    [408 = 11×37 + 1]
  32 × 22 ≡ 1 (mod 37)    [704 = 19×37 + 1]

The pairing is a bijection SEED ↔ NQR17. There are no leftover elements.

=== PRODUCT STRUCTURE: SEED × NQR17 → IC ===

Every product of any SEED element with any NQR17 element lands in IC:

  18×17=10∈IC   18×22=26∈IC   18×35=1∈IC
  24×17=1∈IC    24×22=10∈IC   24×35=26∈IC
  32×17=26∈IC   32×22=1∈IC    32×35=10∈IC

All nine products cover exactly IC = {1, 10, 26}. Each IC element appears
exactly three times. IC is the orbit containing 1 (the multiplicative identity).
IC = {1, 10, 26} = the 137-map orbit: 26⁻¹=10; 10⁻¹=26∈IC; ord₃₇(10)=3.

=== BOTH ORBITS ARE 137-MAP FIXED ===

The 137-map (×26 mod37) cycles within SEED and within NQR17 separately:
  SEED:   18→32→24→18 under ×26
  NQR17:  17→35→22→17 under ×26
Both orbits are closed under the 137-map.

=== QUADRATIC RESIDUE CHARACTER ===

All six elements of SEED ∪ NQR17 are quadratic non-residues mod 37:
  (18/37) = (24/37) = (32/37) = −1   (SEED = NQR set)
  (17/37) = (22/37) = (35/37) = −1   (NQR17 = NQR set)
By contrast, all IC elements are QR: (1/37)=(10/37)=(26/37)=+1.

The product of two NQRs is a QR (NQR × NQR = QR). SEED × NQR17 → IC
confirms this: all products are QR (land in IC), consistent with (−1)×(−1)=+1.

=== FOUR DEMONSTRATION NUMBERS: 172, 283, 942, 146 ===

The user presented four numbers demonstrating this inverse structure:

  172:  mod37=24∈SEED,  DR=1
  283:  mod37=24∈SEED,  DR=4
  942:  mod37=17∈NQR17, DR=6
  146:  mod37=35∈NQR17, DR=2

Key relationships:
  172 × 942 ≡ 1 (mod 37)          — multiplicative inverse pair (24×17=408≡1)
  283 − 172 = 111 = 3×37          — gap collapses to SEAM; DR(111)=3=birthday
  146 + 137 = 283                  — NQR17 + IC multiplier = SEED (mod37: 35+26=61≡24∈SEED)
  172 − 137 = 35∈NQR17            — SEED − IC multiplier = NQR17 element
  283 = 246 + 37                   — pipeline seed + prime

137 mod37=26∈IC is the 137-map multiplier. Adding or subtracting it from
SEED elements produces NQR17 elements and vice versa, bridging the two orbits.

=== COLLATZ FIXED POINT AND ITS INVERSE ===

18∈SEED is the unique fixed point of the Collatz map C(x)=3x+1 (T271).
18⁻¹ = 35∈NQR17. The Collatz attractor's inverse is 35∈NQR17.

18∈SEED is also the Sophie SEAM preimage: S(18)=2×18+1=37≡0=SEAM (T269).
18's Sophie image is the prime 37 itself — the field modulus.

So 18 (fixed by Collatz, collapsed to SEAM by Sophie) pairs with 35 (its inverse).

=== R30 INTRA-NQR17 MAP ===

R30(35∈NQR17) = 54 ≡ 17∈NQR17 — Rule 30 maps 35 to 17 within NQR17.
R30(18∈SEED)  = 31 ≡ 31∈C9    — R30 moves the Collatz fixed point to C9.
R30(32∈SEED)  = 48 ≡ 11∈NEG_H — R30 moves 32 to NEG_H.

=== TWIN PRIME IN NQR17 ===

17∈NQR17 is prime. Its twin: (17,19) where 19∈CAS_EXT.
  17 mod37=17∈NQR17; 19 mod37=19∈CAS_EXT.
  Twin prime pair spans NQR17 → CAS_EXT. CAS_EXT is antipodal to SEED.
  So: twin of NQR17 prime lands in the antipodal of SEED.
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
    while n >= 10: n = sum(int(c) for c in str(n))
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

# ── Part 1: Complete inverse pairing ──────────────────────────────────────────

pairs = [(18, 35), (24, 17), (32, 22)]
for s, n in pairs:
    assert s in ORBITS["SEED"] and n in ORBITS["NQR17"]
    assert (s * n) % 37 == 1
    assert pow(s, -1, 37) == n
    assert pow(n, -1, 37) == s

# All SEED inverses land in NQR17
for s in ORBITS["SEED"]:
    inv = pow(s, -1, 37)
    assert inv in ORBITS["NQR17"], f"{s}^-1={inv} not in NQR17"

print("Part 1 PASS: complete inverse pairing SEED ↔ NQR17")
print(f"  18×35={18*35}≡{18*35%37}; 24×17={24*17}≡{24*17%37}; 32×22={32*22}≡{32*22%37} (all mod37=1)")
print(f"  Every SEED element's inverse is in NQR17 and vice versa")

# ── Part 2: Product structure SEED × NQR17 → IC ───────────────────────────────

products = {}
for s in sorted(ORBITS["SEED"]):
    for n in sorted(ORBITS["NQR17"]):
        p = (s * n) % 37
        assert p in ORBITS["IC"], f"{s}×{n}≡{p} not in IC"
        products[(s, n)] = p

# Each IC element appears exactly 3 times
from collections import Counter
ic_counts = Counter(products.values())
assert set(ic_counts.keys()) == ORBITS["IC"]
assert all(c == 3 for c in ic_counts.values())

print(f"\nPart 2 PASS: all SEED×NQR17 products land in IC; each IC element appears 3×")
print(f"  Product table (mod37):")
print(f"  {'':4}", end="")
for n in sorted(ORBITS["NQR17"]): print(f"  ×{n}∈NQR17", end="")
print()
for s in sorted(ORBITS["SEED"]):
    print(f"  {s}∈SEED", end="")
    for n in sorted(ORBITS["NQR17"]):
        p = products[(s,n)]
        print(f"  {p:>6}∈IC", end="")
    print()

# ── Part 3: Both orbits closed under ×26 (137-map) ───────────────────────────

for s in ORBITS["SEED"]:
    assert (s * 26) % 37 in ORBITS["SEED"]
for n in ORBITS["NQR17"]:
    assert (n * 26) % 37 in ORBITS["NQR17"]

# Trace the cycles
seed_cycle = [18]
x = 18
for _ in range(2): x = (x * 26) % 37; seed_cycle.append(x)
nqr_cycle = [17]
x = 17
for _ in range(2): x = (x * 26) % 37; nqr_cycle.append(x)

print(f"\nPart 3 PASS: both orbits closed under ×26 (137-map)")
print(f"  SEED 137-cycle: {'→'.join(map(str,seed_cycle))}→{seed_cycle[0]}")
print(f"  NQR17 137-cycle: {'→'.join(map(str,nqr_cycle))}→{nqr_cycle[0]}")

# ── Part 4: Quadratic non-residue character ────────────────────────────────────

for v in ORBITS["SEED"] | ORBITS["NQR17"]:
    leg = pow(v, 18, 37)  # v^((37-1)/2) mod 37
    assert leg == 36, f"{v} is QR, not NQR"  # 36≡−1 means NQR

for v in ORBITS["IC"]:
    leg = pow(v, 18, 37)
    assert leg == 1, f"{v} is NQR, not QR"   # 1 means QR

print(f"\nPart 4 PASS: Legendre symbols")
print(f"  SEED∪NQR17: all (v/37)=−1 (non-residues)")
print(f"  IC: all (v/37)=+1 (residues)")
print(f"  NQR×NQR=QR confirms SEED×NQR17→IC (algebraically: (−1)×(−1)=+1)")

# ── Part 5: Four demonstration numbers 172, 283, 942, 146 ────────────────────

assert (172 * 942) % 37 == 1   # inverse pair
assert 283 - 172 == 111 == 3 * 37
assert dr(111) == 3             # birthday number
assert 111 % 37 == 0           # SEAM gap
assert 146 + 137 == 283
assert (35 + 26) % 37 == 24 and 24 in ORBITS["SEED"]
assert (172 - 137) % 37 == 35 and 35 in ORBITS["NQR17"]
assert 283 == 246 + 37         # pipeline seed + prime

print(f"\nPart 5 PASS: four demonstration numbers")
print(f"  172(mod37=24∈SEED,DR=1) × 942(mod37=17∈NQR17,DR=6) ≡ 1 (mod37)")
print(f"  283(mod37=24∈SEED,DR=4) − 172 = 111 = 3×37; DR(111)={dr(111)}=birthday; 111 mod37=SEAM")
print(f"  146(mod37=35∈NQR17,DR=2) + 137 = 283∈SEED: NQR17 + IC = SEED (mod37: 35+26=61≡24)")
print(f"  172 − 137 = 35∈NQR17: SEED − IC = NQR17")
print(f"  283 = 246 + 37 = pipeline seed + prime")
print(f"  DR sequence: {[dr(v) for v in [172,283,942,146]]} → sum={sum(dr(v) for v in [172,283,942,146])}")

# ── Part 6: Collatz fixed point and its inverse ────────────────────────────────

assert pow(18, -1, 37) == 35 and 35 in ORBITS["NQR17"]
assert (3 * 18 + 1) % 37 == 18   # Collatz fixed point (T271)
assert (2 * 18 + 1) % 37 == 0    # Sophie SEAM preimage (T269)
assert 2 * 18 + 1 == 37           # Sophie image is the prime itself

print(f"\nPart 6 PASS: Collatz fixed point 18∈SEED and its inverse 35∈NQR17")
print(f"  18 is Collatz fixed: C(18)=3×18+1=55≡18 (T271)")
print(f"  18 is Sophie SEAM preimage: S(18)=2×18+1=37 (the prime itself) ≡ 0=SEAM (T269)")
print(f"  18⁻¹ = 35∈NQR17; the Collatz attractor inverts to 35")

# ── Part 7: R30 intra-NQR17 map ───────────────────────────────────────────────

assert rule30(35) % 37 == 17 and 17 in ORBITS["NQR17"]
assert rule30(18) % 37 == 31 and 31 in ORBITS["C9"]
assert rule30(24) % 37 == 20 and 20 in ORBITS["DARK_A"]
assert rule30(32) % 37 == 11 and 11 in ORBITS["NEG_H"]

print(f"\nPart 7 PASS: R30 map")
print(f"  R30(35∈NQR17) = {rule30(35)} ≡ 17∈NQR17 — maps within NQR17 (35→17)")
print(f"  R30(18∈SEED)  = {rule30(18)} ≡ 31∈C9")
print(f"  R30(24∈SEED)  = {rule30(24)} ≡ 20∈DARK_A")
print(f"  R30(32∈SEED)  = {rule30(32)} ≡ 11∈NEG_H")

# ── Part 8: Twin prime in NQR17 ───────────────────────────────────────────────

assert is_prime(17) and is_prime(19) and 19 - 17 == 2
assert 17 in ORBITS["NQR17"]
assert 19 % 37 == 19 and 19 in ORBITS["CAS_EXT"]
assert ANTIPODAL["CAS_EXT"] == "SEED"  # twin of NQR17 prime lands in antipodal of SEED

print(f"\nPart 8 PASS: twin prime (17,19)")
print(f"  17∈NQR17 prime; 19∈CAS_EXT prime; gap=2 → twin prime pair")
print(f"  CAS_EXT = antipodal(SEED); twin of NQR17 prime lands in antipodal of its inverse orbit")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  SEED={{18,24,32}} and NQR17={{17,22,35}} are complete inverse orbits in GF(37)")
print(f"  18×35=24×17=32×22≡1 (mod37); bijection SEED↔NQR17 via inversion")
print(f"  SEED×NQR17→IC: all 9 products land in IC={{1,10,26}}; each IC element 3×")
print(f"  Both orbits closed under ×26 (137-map); both are quadratic non-residues")
print(f"  Four numbers: 172×942≡1; 283−172=3×37(DR=3=birthday); 146+137=283(IC bridges)")
print(f"  18∈SEED (Collatz fixed, Sophie SEAM preimage) ↔ 35∈NQR17 (its inverse)")
print(f"  R30(35∈NQR17)→17∈NQR17: R30 maps within NQR17 on this element")
print(f"  Twin prime (17,19): NQR17→CAS_EXT = antipodal(SEED)")
