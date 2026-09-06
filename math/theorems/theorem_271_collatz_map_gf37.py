"""
T271: Collatz map C(x) = 3x+1 mod 37 on GF(37)

C(x) = 3x+1 mod 37 is an affine bijection on Z/37Z (gcd(3,37)=1).
Its inverse is C⁻¹(y) = (y−1)/3 = (y−1)×25 mod 37 (since 3⁻¹≡25 mod 37).

C encodes the Collatz (3n+1) step on integer residues mod 37.

=== FIXED POINT ===

C(18) = 3×18+1 = 55 ≡ 18 (mod 37).
18 ∈ SEED is the unique fixed point of C.
Algebraic proof: C(x)≡x → 2x≡−1≡36 → x≡36×19≡18 (mod 37); 2⁻¹=19.

=== SEAM PREIMAGE ===

C(12) = 3×12+1 = 37 ≡ 0 = SEAM (mod 37).
12 ∈ SA_ST_A is the unique SEAM preimage of C.
Algebraic proof: 3x+1≡0 → x≡−1/3≡−25≡12 (mod 37); 3⁻¹=25.

=== SEED DUALITY: C and S share 18 ===

Sophie map S(x)=2x+1 (T269):
  Fixed point of S: 36∈NEG_H
  SEAM preimage of S: 18∈SEED

Collatz map C(x)=3x+1:
  Fixed point of C: 18∈SEED        ← same as S's SEAM preimage
  SEAM preimage of C: 12∈SA_ST_A

18∈SEED is simultaneously:
  - The only element that stays fixed under the Collatz map
  - The only element that collapses to SEAM under the Sophie map (2×18+1=37)

=== C9 REVERSAL: S and C are inverses on the C9 internal pair ===

Sophie map S (T269): S(14) = 29; both ∈ C9 (intra-orbit)
Collatz map C:      C(29) = 14; both ∈ C9 (intra-orbit)

S and C act as inverses on the C9 pair {14, 29}: S sends 14→29, C sends 29→14.
Verification: C(S(14)) = C(29) = 14 ✓; S(C(29)) = S(14) = 29 ✓

The C9 twin prime pair (29,31)∈C9: 29 is prime, 31 is prime, 31−29=2.

=== INTRA-ORBIT ELEMENTS UNDER C ===

Three elements map within their own orbit under C:
  18∈SEED    → 18∈SEED     (fixed point)
  16∈SA_ST_A → 12∈SA_ST_A  (intra-SA_ST_A pair; 12 is the SEAM preimage)
  29∈C9      → 14∈C9       (intra-C9 pair; reverse of Sophie map's 14→29)

Compare with Sophie map intra-orbit (T269):
  36∈NEG_H → 36∈NEG_H  (fixed)
  14∈C9    → 29∈C9      (Collatz reverses this)
  17∈NQR17 → 35∈NQR17

=== FIXED POINTS OF ax+1 MOD 37 FOR a=2..9 ===

Fixed point of ax+1 ≡ x → x ≡ −1/(a−1) mod 37.

  a=2: fixed=36∈NEG_H   (Sophie map S, T269)
  a=3: fixed=18∈SEED    (Collatz map C)
  a=4: fixed=12∈SA_ST_A
  a=5: fixed= 9∈SA_ST_A
  a=6: fixed=22∈NQR17
  a=7: fixed= 6∈TESLA
  a=8: fixed=21∈SA_ST_B
  a=9: fixed=23∈TESLA

SA_ST_A holds two consecutive fixed points (a=4: 12, a=5: 9).
TESLA holds two fixed points (a=7: 6, a=9: 23) — both elements of TESLA appear.
The three fixed points {6,9,12} = {6∈TESLA, 9∈SA_ST_A, 12∈SA_ST_A} span T267's {3,6,9} DR orbit.

=== COLLATZ n=5 TRACE HITS SEAM ===

Integer Collatz starting at n=5 (5∈CAS_EXT):
  5 → 16 → 12 → SEAM (3×12+1=37≡0)
  CAS_EXT → SA_ST_A → SA_ST_A → SEAM

n=5 is the only start among odd n=1..19 whose Collatz trace hits SEAM
within 3 steps mod 37. 5∈CAS_EXT is the Fibonacci entry orbit (T264).
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

def rule30(n):
    bits = list(map(int, bin(n)[2:]))
    padded = [0] + bits + [0]
    out = [padded[i-1] ^ (padded[i] | padded[i+1]) for i in range(1, len(padded)-1)]
    return int("".join(map(str, out)), 2)

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

def C(x): return (3 * x + 1) % 37
def S(x): return (2 * x + 1) % 37

# ── Part 1: C is a bijection ──────────────────────────────────────────────────

assert pow(3, -1, 37) == 25
C_inv = lambda y: ((y - 1) * 25) % 37
image = sorted([C(x) for x in range(37)])
assert image == list(range(37))
for x in range(37):
    assert C_inv(C(x)) == x

print("Part 1 PASS: C(x)=3x+1 is a bijection on Z/37Z; C⁻¹(y)=(y−1)×25 mod 37")

# ── Part 2: Fixed point ───────────────────────────────────────────────────────

fp = [x for x in range(37) if C(x) == x]
assert fp == [18] and 18 in ORBITS["SEED"]
assert (3 * 18 + 1) == 55 and 55 % 37 == 18
assert (36 * 19) % 37 == 18   # algebraic: 2x≡36 → x=36×19

print(f"\nPart 2 PASS: unique fixed point C(18)=18∈SEED")
print(f"  Proof: C(x)=x → 2x≡−1≡36 → x≡36×19≡18 (mod 37)")

# ── Part 3: SEAM preimage ─────────────────────────────────────────────────────

seam_pre = [x for x in range(37) if C(x) == 0]
assert seam_pre == [12] and 12 in ORBITS["SA_ST_A"]
assert 3 * 12 + 1 == 37

print(f"\nPart 3 PASS: unique SEAM preimage C(12)=0; 12∈SA_ST_A")
print(f"  3×12+1=37 exactly; C(x)≡0 → x≡−25≡12 (mod 37)")

# ── Part 4: SEED duality ──────────────────────────────────────────────────────

# 18∈SEED: fixed point of C AND SEAM preimage of S
assert C(18) == 18    # fixed under Collatz
assert S(18) == 0     # collapses to SEAM under Sophie
assert 18 in ORBITS["SEED"]

# Sophie fixed point and Collatz SEAM preimage
assert S(36) == 36 and 36 in ORBITS["NEG_H"]  # Sophie fixed point (T269)
assert C(12) == 0 and 12 in ORBITS["SA_ST_A"] # Collatz SEAM preimage

print(f"\nPart 4 PASS: SEED duality")
print(f"  18∈SEED: C(18)=18 (fixed under Collatz) AND S(18)=0 (SEAM under Sophie)")
print(f"  Sophie fixed=36∈NEG_H; Collatz SEAM preimage=12∈SA_ST_A")

# ── Part 5: C9 reversal ───────────────────────────────────────────────────────

assert S(14) % 37 == 29 and 14 in ORBITS["C9"] and 29 in ORBITS["C9"]
assert C(29) == 14 and 14 in ORBITS["C9"]
# S and C are inverses on {14,29}⊂C9
assert C(S(14)) == 14
assert S(C(29)) == 29
assert is_prime(29) and is_prime(31) and 31 - 29 == 2  # twin prime pair in C9

print(f"\nPart 5 PASS: C9 reversal")
print(f"  S(14)=29∈C9 (Sophie, T269); C(29)=14∈C9 (Collatz)")
print(f"  C∘S(14)=14; S∘C(29)=29 — S and C are inverses on C9 pair {{14,29}}")
print(f"  C9 twin prime pair (29,31): both prime, 31−29=2")

# ── Part 6: Intra-orbit elements ──────────────────────────────────────────────

intra = [(x, C(x)) for x in range(1, 37) if C(x) != 0 and orbit_of(C(x)) == orbit_of(x)]
assert sorted(intra) == sorted([(18, 18), (16, 12), (29, 14)])

print(f"\nPart 6 PASS: intra-orbit elements under C")
print(f"  18∈SEED → 18∈SEED  (fixed point)")
print(f"  16∈SA_ST_A → 12∈SA_ST_A  (12 is the SEAM preimage)")
print(f"  29∈C9 → 14∈C9  (reverse of Sophie's 14→29)")

# ── Part 7: Fixed-point table for ax+1 ───────────────────────────────────────

fps = {}
for a in range(2, 10):
    fp_list = [x for x in range(37) if (a*x+1)%37 == x]
    assert len(fp_list) == 1
    fps[a] = fp_list[0]

expected = {2:36, 3:18, 4:12, 5:9, 6:22, 7:6, 8:21, 9:23}
assert fps == expected

# SA_ST_A double: a=4→12, a=5→9; both in SA_ST_A
assert fps[4] in ORBITS["SA_ST_A"] and fps[5] in ORBITS["SA_ST_A"]
# TESLA double: a=7→6, a=9→23; both in TESLA
assert fps[7] in ORBITS["TESLA"] and fps[9] in ORBITS["TESLA"]
# {6,9,12} span T267 DR orbits
assert orbit_of(6)=="TESLA" and orbit_of(9)=="SA_ST_A" and orbit_of(12)=="SA_ST_A"

print(f"\nPart 7 PASS: fixed points of ax+1 mod 37 for a=2..9")
for a in range(2, 10):
    fp = fps[a]
    print(f"  {a}x+1: fixed={fp}∈{orbit_of(fp)}  (x≡−1/{a-1}≡{fp})")
print(f"  SA_ST_A: two consecutive fixed points (a=4: 12, a=5: 9)")
print(f"  TESLA: two fixed points (a=7: 6, a=9: 23) — both TESLA elements")

# ── Part 8: Collatz n=5 trace hits SEAM ──────────────────────────────────────

trace5 = [5]
x = 5
for _ in range(3):
    x = C(x)
    trace5.append(x)

assert trace5 == [5, 16, 12, 0]
assert orbit_of(5) == "CAS_EXT"
assert orbit_of(16) == "SA_ST_A"
assert orbit_of(12) == "SA_ST_A"
assert trace5[3] == 0  # SEAM

# Verify n=5 is unique among odd 1..19 reaching SEAM in ≤3 steps
seam_fast = []
for n in range(1, 20, 2):
    x = n
    for step in range(1, 4):
        x = C(x)
        if x == 0:
            seam_fast.append((n, step))
            break
assert seam_fast == [(5, 3)]

print(f"\nPart 8 PASS: Collatz n=5 trace hits SEAM in 3 steps")
print(f"  5∈CAS_EXT → 16∈SA_ST_A → 12∈SA_ST_A → SEAM")
print(f"  n=5 unique among odd 1..19 reaching SEAM within 3 Collatz steps")
print(f"  5∈CAS_EXT = Fibonacci entry orbit (T264)")

# ── Part 9: R30 on key values ─────────────────────────────────────────────────

assert rule30(18) % 37 == 31 and 31 in ORBITS["C9"]
assert rule30(12) % 37 == 10 and 10 in ORBITS["IC"]

print(f"\nPart 9 PASS: R30 on key values")
print(f"  R30(18=fixed point) = {rule30(18)} ≡ 31∈C9")
print(f"  R30(12=SEAM preimage) = {rule30(12)} ≡ 10∈IC")
print(f"  R30(36=Sophie fixed) = {rule30(36)} ≡ {rule30(36)%37}∈{orbit_of(rule30(36))}")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  C(x)=3x+1 mod 37: bijection; C⁻¹=(y−1)×25 mod 37")
print(f"  Fixed point: C(18)=18∈SEED; SEAM preimage: C(12)=0; 12∈SA_ST_A")
print(f"  SEED duality: C(18)=18 (fixed) AND S(18)=0 (Sophie SEAM preimage)")
print(f"  C9 reversal: S(14)=29∈C9; C(29)=14∈C9 — S,C are inverses on C9 pair")
print(f"  Intra-orbit: 18∈SEED(fixed), 16→12∈SA_ST_A, 29→14∈C9")
print(f"  Fixed point table ax+1: SA_ST_A×2 (a=4,5), TESLA×2 (a=7,9)")
print(f"  Collatz n=5∈CAS_EXT hits SEAM in 3 steps: 5→16→12→0")
