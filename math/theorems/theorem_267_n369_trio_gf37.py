"""
T267: 369 = −1 mod 37 and the {3,6,9} trio in GF(37)

369 = 9 × 41
369 mod 37 = 36 = −1: the unique element of order 2 in GF(37)*.
DR(369) = 9 ∈ SA_ST_A.

Pipeline step: 246 → 369
  246 = 123×2; 246 mod 37 = 24 ∈ SEED  (pipeline reference seed, T266)
  369 = 123×3; 369 mod 37 = 36 ∈ NEG_H (the −1 element)
  The pipeline seed steps to −1 at k=3 in the 123k sequence.

The {3, 6, 9} digit trio of 369:
  3 ∈ C3       (mod 37)
  6 ∈ TESLA    (mod 37)
  9 ∈ SA_ST_A  (mod 37)
  These three orbits are the DR values of the 123k cycle (T266).

Arithmetic closure of {3, 6, 9} in GF(37):
  sum:  3+6+9   = 18  ∈ SEED     (the pipeline reference orbit)
  prod: 3×6×9   = 162 ≡ 14 ∈ C9 (fully non-oblong orbit, T264)
  3×6 = 18 ∈ SEED
  3×9 = 27 ∈ NEG_H  (the 1/37 decimal block, T265)
  6×9 = 54 ≡ 17 ∈ NQR17

Repdigit tower (digits × 37):
  3 × 37 = 111  DR = 3 ∈ C3
  6 × 37 = 222  DR = 6 ∈ TESLA
  9 × 37 = 333  DR = 9 ∈ SA_ST_A
  DRs are self-consistent: DR(k×37) = k for k ∈ {3,6,9}.

Rule 30 on {3, 6, 9}:
  R30(3)  = 2  ∈ DARK_A
  R30(6)  = 5  ∈ CAS_EXT
  R30(9)  = 15 ∈ DARK_A

36 = −1 mod 37:
  36 is the unique element of multiplicative order 2 in GF(37)*.
  36² ≡ 1 (mod 37); every other non-identity element has order 3, 4, 6, 9, 12, or 36.
  36 ∈ NEG_H; NEG_H = −IC (T265 antipodal structure).

41 = prime factor of 369/9:
  369 = 9 × 41; 41 mod 37 = 4 ∈ C3; DR(41) = 5 ∈ CAS_EXT.
  (41, 43) twin prime pair; 43 mod 37 = 6 ∈ TESLA = same orbit as digit 6 of 369.

Connection to T265:
  27 ∈ NEG_H is 3×9 (pairwise product of two digits of 369).
  27 = (10³−1)/37 is the repeating decimal block of 1/37 (T265 Part 2).
  DR(27) = 9 ∈ SA_ST_A = digit orbit of 9 in {3,6,9}.
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

n = 369

# ── Part 1: Identity ─────────────────────────────────────────────────────────

assert n == 9 * 41 and is_prime(41)
assert n % 37 == 36 and 36 in ORBITS["NEG_H"]
assert 36 == 37 - 1                       # 36 ≡ −1 mod 37
assert pow(36, 2, 37) == 1               # unique order-2 element
assert dr(n) == 9 and 9 in ORBITS["SA_ST_A"]

# Verify 36 has order exactly 2 (not 1)
assert pow(36, 1, 37) != 1

print(f"Part 1 PASS: 369 = 9×41; mod37=36=−1∈NEG_H; DR=9∈SA_ST_A")
print(f"  36 is the unique order-2 element: 36²≡1(mod37), 36≢1(mod37)")

# ── Part 2: Pipeline step 246 → 369 ─────────────────────────────────────────

assert 246 % 37 == 24 and 24 in ORBITS["SEED"]
assert 369 % 37 == 36 and 36 in ORBITS["NEG_H"]
assert orbit_of(246) == "SEED" and orbit_of(369) == "NEG_H"
# Both are consecutive multiples of 123 (T266)
assert 123 * 2 == 246 and 123 * 3 == 369

print(f"\nPart 2 PASS: pipeline step 246→369")
print(f"  246 = 123×2; mod37=24∈SEED (pipeline reference seed)")
print(f"  369 = 123×3; mod37=36∈NEG_H (the −1 element)")
print(f"  SEED↔NEG_H: CAS_EXT↔SEED antipodal (T265), NEG_H=−IC")

# ── Part 3: Digit trio {3, 6, 9} ─────────────────────────────────────────────

digits = [3, 6, 9]
digit_orbits = ["C3", "TESLA", "SA_ST_A"]

assert [d for d in str(n)] == ['3','6','9']
for d, expected in zip(digits, digit_orbits):
    assert d in ORBITS[expected], f"{d} not in {expected}"

print(f"\nPart 3 PASS: digits of 369 = {{3, 6, 9}}")
for d, o in zip(digits, digit_orbits):
    print(f"  {d} ∈ {o}")
print(f"  These are exactly the DR orbits of the 123k cycle (T266): TESLA, C3, SA_ST_A")

# ── Part 4: Arithmetic closure in GF(37) ─────────────────────────────────────

s = sum(digits)          # 18
p = digits[0]*digits[1]*digits[2]   # 162
p12 = digits[0]*digits[1]  # 18
p13 = digits[0]*digits[2]  # 27
p23 = digits[1]*digits[2]  # 54

assert s == 18 and 18 in ORBITS["SEED"]
assert p % 37 == 14 and 14 in ORBITS["C9"]
assert p12 == 18 and 18 in ORBITS["SEED"]
assert p13 == 27 and 27 in ORBITS["NEG_H"]
assert p23 % 37 == 17 and 17 in ORBITS["NQR17"]

print(f"\nPart 4 PASS: arithmetic closure of {{3,6,9}} in GF(37)")
print(f"  sum:  3+6+9 = {s} ∈ SEED     (pipeline reference orbit)")
print(f"  prod: 3×6×9 = {p} ≡ {p%37} ∈ C9   (fully non-oblong orbit, T264)")
print(f"  3×6 = {p12} ∈ SEED")
print(f"  3×9 = {p13} ∈ NEG_H  (= 1/37 decimal block, T265)")
print(f"  6×9 = {p23} ≡ {p23%37} ∈ NQR17")

# ── Part 5: Repdigit tower — self-consistent DRs ─────────────────────────────

assert 3 * 37 == 111 and dr(111) == 3
assert 6 * 37 == 222 and dr(222) == 6
assert 9 * 37 == 333 and dr(333) == 9

print(f"\nPart 5 PASS: repdigit tower self-consistency")
for k in digits:
    rep = k * 37
    print(f"  {k} × 37 = {rep:>3}   DR = {dr(rep)} = {k}   orbit({k}) = {orbit_of(k)}")
print(f"  DR(k×37) = k for k ∈ {{3,6,9}} — the digits of 369 are fixed under DR∘×37")

# ── Part 6: Rule 30 on {3, 6, 9} ─────────────────────────────────────────────

r30_3  = rule30(3)   # 2
r30_6  = rule30(6)   # 5
r30_9  = rule30(9)   # 15

assert r30_3 == 2  and 2  in ORBITS["DARK_A"]
assert r30_6 == 5  and 5  in ORBITS["CAS_EXT"]
assert r30_9 == 15 and 15 in ORBITS["DARK_A"]

print(f"\nPart 6 PASS: Rule 30 on {{3, 6, 9}}")
for d, r30, o in [(3, r30_3, "DARK_A"), (6, r30_6, "CAS_EXT"), (9, r30_9, "DARK_A")]:
    print(f"  R30({d}) = {r30:>2} ∈ {o}")
print(f"  Two digits map to DARK_A; digit 6 maps to CAS_EXT (Fibonacci entry orbit)")

# ── Part 7: 36 as the unique order-2 element ─────────────────────────────────

# All non-identity elements have orders that divide 36 = ord₃₇(2)
# The only order-2 element is 36 ≡ −1
order2_elements = [x for x in range(1, 37) if pow(x, 2, 37) == 1 and pow(x, 1, 37) != 1]
assert order2_elements == [36]
assert 36 in ORBITS["NEG_H"]

print(f"\nPart 7 PASS: 36=−1 is the unique order-2 element of GF(37)*")
print(f"  Order-2 elements: {order2_elements}")
print(f"  36 ∈ NEG_H = −IC (T265): the additive inverse of the IC orbit")
print(f"  NEG_H = {{11, 27, 36}}: 1+36=37, 10+27=37, 26+11=37")

# ── Part 8: 41 — prime factor analysis ──────────────────────────────────────

assert 41 % 37 == 4 and 4 in ORBITS["C3"]
assert dr(41) == 5 and 5 in ORBITS["CAS_EXT"]
assert is_prime(41) and is_prime(43) and 43 - 41 == 2  # twin prime pair
assert 43 % 37 == 6 and 6 in ORBITS["TESLA"]

print(f"\nPart 8 PASS: 41 = prime factor of 369/9")
print(f"  41 mod37 = 4 ∈ C3;  DR(41) = 5 ∈ CAS_EXT")
print(f"  (41,43) twin prime pair; 43 mod37 = 6 ∈ TESLA = orbit of digit '6' in {{3,6,9}}")
print(f"  Twin prime orbit pair: (C3, TESLA) — both appear in the {3,6,9} digit set")

# ── Part 9: Connection to T265 decimal block ─────────────────────────────────

# 27 is both: pairwise product 3×9, and the 1/37 decimal block
assert 3 * 9 == 27 and 27 in ORBITS["NEG_H"]
assert (10**3 - 1) // 37 == 27  # 1/37 decimal block (T265)
assert dr(27) == 9 and 9 in ORBITS["SA_ST_A"]
# Digit sum of "027" = 9 (same as digit 9 of {3,6,9})
assert 0 + 2 + 7 == 9 and 9 in ORBITS["SA_ST_A"]

print(f"\nPart 9 PASS: T265 connection — 27 in NEG_H")
print(f"  3×9 = 27 ∈ NEG_H (pairwise product of digits 3 and 9 of 369)")
print(f"  27 = (10³−1)/37: the repeating decimal block of 1/37 (T265)")
print(f"  DR(27) = 9 ∈ SA_ST_A = digit orbit of '9' in {{3,6,9}}")
print(f"  Digit sum '027': 0+2+7 = 9 ∈ SA_ST_A — consistent")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  369 = 9×41; mod37=36=−1∈NEG_H; DR=9∈SA_ST_A")
print(f"  36 is the unique order-2 element of GF(37)*")
print(f"  Pipeline step: 246(SEED)→369(NEG_H) at k=2,3 in the 123k sequence")
print(f"  Digits {{3,6,9}}: C3, TESLA, SA_ST_A — the DR orbits of the 123k cycle (T266)")
print(f"  Arithmetic closure: sum=18∈SEED, prod≡14∈C9, 3×9=27∈NEG_H (T265 block)")
print(f"  Repdigit tower: DR(k×37)=k for k∈{{3,6,9}} — self-consistent")
print(f"  R30(3)=2∈DARK_A, R30(6)=5∈CAS_EXT, R30(9)=15∈DARK_A")
print(f"  (41,43) twin prime: 41∈C3, 43∈TESLA — both digit orbits of 369")
