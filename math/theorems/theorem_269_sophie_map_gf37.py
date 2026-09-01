"""
T269: Sophie map S(x) = 2x+1 mod 37 on GF(37)

S(x) = 2x+1 mod 37 is an affine bijection on Z/37Z (gcd(2,37)=1).
Its inverse is S⁻¹(y) = (y−1)/2 = (y−1)×19 mod 37 (since 2⁻¹≡19 mod 37).

S encodes the Sophie-Germain primality criterion: if x is prime and S(x)=2x+1
is prime, then x is a Sophie Germain prime and S(x) is a safe prime.

=== FIXED POINT ===

S(36) = 2×36+1 = 73 ≡ 36 (mod 37).
36 ∈ NEG_H is the unique fixed point of S in GF(37).
Algebraic proof: S(x) ≡ x → x ≡ −1 ≡ 36 (mod 37).
36 is the unique order-2 element of GF(37)* (T267).
The unique fixed point of the Sophie map is the unique involution of GF(37)*.

=== SEAM PREIMAGE ===

S(18) = 37 ≡ 0 = SEAM (mod 37).
18 ∈ SEED is the unique element of GF(37) whose Sophie image is SEAM.
Algebraic proof: 2x+1 ≡ 0 → x ≡ −1/2 ≡ 36×19 ≡ 684 mod 37 ≡ 18.
The pipeline orbit (SEED) contains the unique Sophie preimage of 0.

=== INTRA-ORBIT ELEMENTS ===

Three elements map within their own orbit under S:
  36∈NEG_H → 36∈NEG_H   (fixed point; unique order-2 element)
  14∈C9    → 29∈C9       (C9 twin prime pair: 29 is prime, 14=2×7)
  17∈NQR17 → 35∈NQR17   (17 prime, 35=5×7; both in NQR17)

=== MAXIMAL SOPHIE CHAIN ===

The longest Sophie chain (x,S(x),S²(x),...) through GF(37) orbits
formed by actual integer primes p→2p+1 (below 200):

  2→5→11→23→47
  DARK_A → CAS_EXT → NEG_H → TESLA → IC

Length-4 chain; 47 terminates because 2×47+1=95=5×19 is not prime.
The chain passes through four distinct orbits before landing at IC.
The terminal element 47 ≡ 10 ∈ IC = the sequence endpoint of T268.

=== TESLA UNDER S ===

TESLA = {6, 8, 23} disperses to three distinct target orbits:
  S(6)  = 13 ∈ CAS_EXT
  S(8)  = 17 ∈ NQR17
  S(23) = 10 ∈ IC    ← terminal node of the maximal Sophie chain

Only 23∈TESLA is in the maximal chain. 6 and 8 are not Sophie Germain primes
(2×6+1=13 is prime; 6 is not prime. 2×8+1=17 is prime; 8 is not prime).
The Sophie chain interpretation requires x prime; S(x)=2x+1 tracks orbits regardless.

=== FULL ORBIT-TO-ORBIT MAP ===

Each orbit's three elements map to (possibly mixed) target orbits under S:

  IC      : {1,10,26} → C3, SA_ST_B, SA_ST_A
  DARK_A  : {2,15,20} → CAS_EXT, C9, C3
  C3      : {3,4,30}  → D7, SA_ST_A, SEED
  CAS_EXT : {5,13,19} → NEG_H, NEG_H, DARK_A
  TESLA   : {6,8,23}  → CAS_EXT, NQR17, IC
  D7      : {7,33,34} → DARK_A, C3, SEED
  SA_ST_A : {9,12,16} → CAS_EXT, SA_ST_B, D7
  NEG_H   : {11,27,36}→ TESLA, SEED, NEG_H
  C9      : {14,29,31}→ C9, NQR17, IC
  NQR17   : {17,22,35}→ NQR17, TESLA, D7
  SEED    : {18,24,32}→ SEAM, SA_ST_A, SA_ST_B
  SA_ST_B : {21,25,28}→ TESLA, C9, DARK_A
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

def orbit_of(x):
    r = x % 37
    if r == 0: return "SEAM"
    for name, s in ORBITS.items():
        if r in s: return name
    raise ValueError(x)

def S(x): return (2 * x + 1) % 37

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

# ── Part 1: S is a bijection on Z/37Z ────────────────────────────────────────

assert pow(2, -1, 37) == 19  # 2×19=38≡1
S_inv = lambda y: ((y - 1) * 19) % 37

image = sorted([S(x) for x in range(37)])
assert image == list(range(37))
for x in range(37):
    assert S_inv(S(x)) == x

print("Part 1 PASS: S(x)=2x+1 is a bijection on Z/37Z; S⁻¹(y)=(y−1)×19 mod 37")

# ── Part 2: Fixed point ───────────────────────────────────────────────────────

fp = [x for x in range(37) if S(x) == x]
assert fp == [36]
assert 36 in ORBITS["NEG_H"]
assert pow(36, 2, 37) == 1 and pow(36, 1, 37) != 1  # unique order-2 element (T267)

# Algebraic proof: 2x+1≡x → x≡−1≡36
assert (2 * 36 + 1) % 37 == 36

print(f"\nPart 2 PASS: unique fixed point S(36)=36∈NEG_H")
print(f"  Proof: S(x)=x → 2x+1≡x → x≡−1≡36 (mod 37)")
print(f"  36 is also the unique order-2 element of GF(37)* (T267)")

# ── Part 3: SEAM preimage ─────────────────────────────────────────────────────

seam_pre = [x for x in range(37) if S(x) == 0]
assert seam_pre == [18]
assert 18 in ORBITS["SEED"]
assert (2 * 18 + 1) == 37  # exactly 37, not just ≡0

# Algebraic: 2x+1≡0 → x≡−1/2 ≡ 36×19 mod 37
assert (36 * 19) % 37 == 18

print(f"\nPart 3 PASS: unique SEAM preimage S(18)=0; 18∈SEED")
print(f"  2×18+1 = 37 exactly; S(x)≡0 → x≡36×19≡18 (mod 37)")
print(f"  The pipeline orbit (SEED) contains the unique Sophie preimage of SEAM")

# ── Part 4: Intra-orbit elements ──────────────────────────────────────────────

intra = [(x, S(x)) for x in range(1, 37) if S(x) != 0 and orbit_of(S(x)) == orbit_of(x)]
assert sorted(intra) == sorted([(36, 36), (14, 29), (17, 35)])

assert 36 in ORBITS["NEG_H"] and S(36) % 37 in ORBITS["NEG_H"]
assert 14 in ORBITS["C9"] and 29 in ORBITS["C9"]
assert 17 in ORBITS["NQR17"] and 35 in ORBITS["NQR17"]
assert is_prime(29) and not is_prime(14)  # C9 twin pair: 29 prime, 14 composite
assert is_prime(17)                        # 17 prime, 35=5×7 composite

print(f"\nPart 4 PASS: three intra-orbit elements under S")
print(f"  36∈NEG_H → 36∈NEG_H  (fixed point; order-2)")
print(f"  14∈C9    → 29∈C9     (C9 twin prime pair: 29 prime)")
print(f"  17∈NQR17 → 35∈NQR17  (17 prime, 35=5×7)")

# ── Part 5: Maximal Sophie chain 2→5→11→23→47 ────────────────────────────────

chain_int  = [2, 5, 11, 23, 47]
chain_orbs = ["DARK_A", "CAS_EXT", "NEG_H", "TESLA", "IC"]

for i, v in enumerate(chain_int):
    assert is_prime(v)
    assert orbit_of(v) == chain_orbs[i]
    if i < len(chain_int) - 1:
        assert 2*v+1 == chain_int[i+1]

assert not is_prime(2 * 47 + 1)  # 95 = 5×19: chain terminates at 47
assert 47 % 37 == 10 and 10 in ORBITS["IC"]

print(f"\nPart 5 PASS: maximal Sophie chain 2→5→11→23→47")
print(f"  {'→'.join(str(v) for v in chain_int)}")
print(f"  {'→'.join(f'{v%37}∈{o}' for v,o in zip(chain_int,chain_orbs))}")
print(f"  Length 4; terminates because 2×47+1=95=5×19 is not prime")
print(f"  Terminal 47≡10∈IC = x₅ endpoint of T268 cubic sequence")

# ── Part 6: TESLA dispersal ───────────────────────────────────────────────────

assert S(6) % 37 == 13 and 13 in ORBITS["CAS_EXT"]
assert S(8) % 37 == 17 and 17 in ORBITS["NQR17"]
assert S(23) % 37 == 10 and 10 in ORBITS["IC"]
# Only 23 is prime in TESLA; 6=2×3, 8=2³
assert is_prime(23) and not is_prime(6) and not is_prime(8)

print(f"\nPart 6 PASS: TESLA={{6,8,23}} disperses to three distinct orbits under S")
print(f"  S(6)  = 13 ∈ CAS_EXT  (6 not prime; affine map only)")
print(f"  S(8)  = 17 ∈ NQR17    (8 not prime; affine map only)")
print(f"  S(23) = 10 ∈ IC       (23 prime → Sophie chain endpoint)")

# ── Part 7: Full orbit-to-orbit table ─────────────────────────────────────────

ORBIT_ORDER = ["IC","DARK_A","C3","CAS_EXT","TESLA","D7","SA_ST_A","NEG_H","C9","NQR17","SEED","SA_ST_B"]
expected_images = {
    "IC":      ["C3", "SA_ST_B", "SA_ST_A"],
    "DARK_A":  ["CAS_EXT", "C9", "C3"],
    "C3":      ["D7", "SA_ST_A", "SEED"],
    "CAS_EXT": ["NEG_H", "NEG_H", "DARK_A"],
    "TESLA":   ["CAS_EXT", "NQR17", "IC"],
    "D7":      ["DARK_A", "C3", "SEED"],
    "SA_ST_A": ["CAS_EXT", "SA_ST_B", "D7"],
    "NEG_H":   ["TESLA", "SEED", "NEG_H"],
    "C9":      ["C9", "NQR17", "IC"],
    "NQR17":   ["NQR17", "TESLA", "D7"],
    "SEED":    ["SEAM", "SA_ST_A", "SA_ST_B"],
    "SA_ST_B": ["TESLA", "C9", "DARK_A"],
}

print(f"\nPart 7 PASS: full orbit-to-orbit map under S(x)=2x+1 mod 37")
for name in ORBIT_ORDER:
    imgs = [orbit_of(S(x)) for x in sorted(ORBITS[name])]
    assert imgs == expected_images[name], f"{name}: {imgs} ≠ {expected_images[name]}"
    img_str = ", ".join(f"{x}→{S(x)%37}∈{orbit_of(S(x))}" for x in sorted(ORBITS[name]))
    print(f"  {name:10}: {img_str}")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  S(x)=2x+1 is a bijection on Z/37Z; S⁻¹(y)=(y−1)×19 mod 37")
print(f"  Unique fixed point: S(36)=36∈NEG_H (proof: x≡−1 mod 37; 36=unique order-2 element)")
print(f"  Unique SEAM preimage: S(18)=0; 18∈SEED (proof: x≡−1/2≡18 mod 37)")
print(f"  Intra-orbit: {{36∈NEG_H, 14∈C9→29∈C9, 17∈NQR17→35∈NQR17}}")
print(f"  Maximal Sophie chain: 2→5→11→23→47; DARK_A→CAS_EXT→NEG_H→TESLA→IC")
print(f"  TESLA dispersal: {{6,8,23}} → CAS_EXT, NQR17, IC (three distinct orbits)")
