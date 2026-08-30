"""
T252: Cyclic System of Cubic Equations — GF(37) Orbit Decomposition

System (over the integers, unique real solution x=y=z=3):
    x³ = 9(y² - 3y + 3)
    y³ = 9(z² - 3z + 3)
    z³ = 9(x² - 3x + 3)

Central results:
  1. The cube roots of 27 in GF(37) are exactly the C3 orbit = {3, 4, 30}.
  2. The coefficient 9 ∈ SA_ST_A = C3² — the square orbit of the solution.
  3. The target 27 ∈ NEG_H = C3³ — the cube orbit of the solution.
  4. Orbit multiplication chain: C3 → SA_ST_A → NEG_H encodes the system.
  5. GF(37) has exactly 4 solutions: (3,3,3) symmetric, plus cyclic rotations
     of (0,12,4) — passing through SEAM. SEAM is the field prime 37 itself.
  6. The primitive root 3: at step 6, 3⁶ mod 37 = 26 = MULT (137-map multiplier).

Standing analysis applied to n=252:
  252 = 4 × 63 = 4 × 9 × 7 = 2² × 3² × 7
  252 mod 37 = 252 - 6×37 = 252 - 222 = 30 ∈ C3 = {3, 4, 30}
  n itself lands in the solution orbit.
"""

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
    if r == 0:
        return "SEAM"
    for name, s in ORBITS.items():
        if r in s:
            return name
    raise ValueError(f"{x} mod 37 = {r} unclassified")

def f(x):
    return (26 * x) % 37

def dr(n):
    n = abs(n)
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n if n else 9

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

def rule30(n):
    bits = list(map(int, bin(n)[2:]))
    padded = [0] + bits + [0]
    out = []
    for i in range(1, len(padded) - 1):
        L, C, R = padded[i-1], padded[i], padded[i+1]
        out.append(L ^ (C | R))
    return int("".join(map(str, out)), 2)

n = 252

# ── Part 1: n=252 modular identity ───────────────────────────────────────────

r_n = n % 37
assert r_n == 30, f"252 mod 37 = {r_n}, expected 30"
assert orbit_of(n) == "C3", f"orbit mismatch"
assert n == 4 * 9 * 7, f"factorization check"
assert 4 % 37 in ORBITS["C3"] and 9 % 37 in ORBITS["SA_ST_A"] and 7 % 37 in ORBITS["D7"]
print(f"Part 1 PASS: 252 mod 37 = {r_n} ∈ C3 = {{3,4,30}}")
print(f"  252 = 4×9×7 = C3 × SA_ST_A × D7")
print(f"  n itself lands in the solution orbit of the cyclic cubic system")

# ── Part 2: The cubic polynomial x³ - 27 over GF(37) ────────────────────────
# x³ - 27 = (x - 3)(x² + 3x + 9) over Z
# Over GF(37), x² + 3x + 9 = 0 has solutions:
#   discriminant = 9 - 36 = -27 ≡ 10 mod 37  (since -27+37=10)
#   √10 mod 37: we need t² ≡ 10 mod 37

disc = (-27) % 37
assert disc == 10
assert orbit_of(disc) == "IC"  # 10 ∈ IC = {1, 10, 26}

# Find √10 mod 37
sqrt10 = next(t for t in range(1, 37) if (t * t) % 37 == 10)
assert sqrt10 == 11
assert (11 * 11) % 37 == 10

# Roots of x² + 3x + 9 = 0 over GF(37):
inv2 = pow(2, -1, 37)  # = 19
root1 = ((-3 + sqrt10) * inv2) % 37  # = (8 * 19) % 37 = 152 % 37 = 4
root2 = ((-3 - sqrt10) * inv2) % 37  # = (-14 * 19) % 37 = (-266) % 37 = 30

cube_roots_27 = sorted([3, root1, root2])
assert cube_roots_27 == [3, 4, 30], f"cube roots: {cube_roots_27}"
assert set(cube_roots_27) == ORBITS["C3"]

for r in cube_roots_27:
    assert pow(r, 3, 37) == 27, f"{r}³ mod 37 ≠ 27"

print(f"\nPart 2 PASS: x³ ≡ 27 mod 37 has roots {{3, 4, 30}} = C3 orbit")
print(f"  Discriminant of x²+3x+9 = 10 ∈ IC; √10 ≡ 11 mod 37")
print(f"  Roots: (-3 ± 11)/2 mod 37 → 4 and 30 (both ∈ C3)")

# ── Part 3: Orbit multiplication chain C3 → SA_ST_A → NEG_H ─────────────────

# C3² = SA_ST_A
c3_sq = {(a * b) % 37 for a in ORBITS["C3"] for b in ORBITS["C3"]}
assert c3_sq == ORBITS["SA_ST_A"], f"C3² = {sorted(c3_sq)}, expected SA_ST_A"

# C3³ = SA_ST_A × C3 = NEG_H
c3_cu = {(a * b) % 37 for a in c3_sq for b in ORBITS["C3"]}
assert c3_cu == ORBITS["NEG_H"], f"C3³ = {sorted(c3_cu)}, expected NEG_H"

# System encoding: coefficient 9 ∈ C3², target 27 ∈ C3³
assert 9 in c3_sq and 27 in c3_cu
assert orbit_of(9) == "SA_ST_A"
assert orbit_of(27) == "NEG_H"

print(f"\nPart 3 PASS: Orbit multiplication chain:")
print(f"  C3    = {{3,4,30}}         (solutions)")
print(f"  C3²   = SA_ST_A = {{9,12,16}}   (coefficient 9)")
print(f"  C3³   = NEG_H = {{11,27,36}} (target 27)")

# ── Part 4: All solutions of the cyclic system in GF(37) ─────────────────────

# System: x³ ≡ 9(y²-3y+3), y³ ≡ 9(z²-3z+3), z³ ≡ 9(x²-3x+3) mod 37
solutions = []
for x in range(37):
    for y in range(37):
        if pow(x, 3, 37) == (9 * (y*y - 3*y + 3)) % 37:
            for z in range(37):
                if (pow(y, 3, 37) == (9 * (z*z - 3*z + 3)) % 37 and
                    pow(z, 3, 37) == (9 * (x*x - 3*x + 3)) % 37):
                    solutions.append((x, y, z))

assert len(solutions) == 4, f"expected 4 solutions, got {len(solutions)}"

sym = [(x,y,z) for x,y,z in solutions if x==y==z]
asym = [(x,y,z) for x,y,z in solutions if not (x==y==z)]

assert sym == [(3, 3, 3)]
assert set(asym) == {(0,12,4), (4,0,12), (12,4,0)}

# Verify asymmetric orbits: (SEAM, SA_ST_A, C3) — cyclic rotation
for sol in asym:
    orbs = tuple(orbit_of(v) for v in sol)
    assert set(orbs) == {"SEAM", "SA_ST_A", "C3"}, f"unexpected orbits: {orbs}"

# Asymmetric solution sum and product
asym_sum = sum(asym[0]) % 37
asym_prod = 1
for v in asym[0]: asym_prod = (asym_prod * v) % 37

print(f"\nPart 4 PASS: Exactly 4 solutions in GF(37):")
print(f"  Symmetric:   (3,3,3) — all in C3")
print(f"  Asymmetric:  (0,12,4), (4,0,12), (12,4,0) — SEAM, SA_ST_A, C3 (cyclic)")
print(f"  Asym triple sum  = {0+12+4} mod 37 = {(0+12+4)%37} ∈ {orbit_of(16)}")
print(f"  Asym triple prod = 0×12×4 = 0 ≡ SEAM (zero element absorbs)")

# ── Part 5: Order of 3 and QR subgroup generation ────────────────────────────

assert pow(3, 36, 37) == 1  # 3 is in (Z/37Z)*

# Compute order of 3
order_3 = min(k for k in range(1, 37) if pow(3, k, 37) == 1)
assert order_3 == 18, f"ord₃₇(3) = {order_3}, expected 18"

# 3^18 ≡ 1 means Legendre(3|37) = 3^18 = 1 → 3 is a QR mod 37
assert pow(3, (37-1)//2, 37) == 1  # Legendre symbol = 1: 3 is a QR
# 3 generates the QR subgroup of index 2 in (Z/37Z)*

tower = [(k, pow(3,k,37), orbit_of(pow(3,k,37))) for k in range(1, 19)]
print(f"\nPart 5 PASS: ord₃₇(3) = 18; 3 generates the QR subgroup of (Z/37Z)*")
print(f"  Legendre(3|37) = 1 → 3 is a quadratic residue mod 37")
print("  Power tower of 3 (full period = 18):")
for k, val, orb in tower:
    mark = " ← MULT" if val == 26 else (" ← MULT²" if val == 10 else (
           " ← target" if val == 27 else ""))
    print(f"    3^{k:>2} mod 37 = {val:>2} ∈ {orb:<8}{mark}")

# Key relationships still hold
assert pow(3, 6, 37) == 26   # = MULT (137-map multiplier)
assert pow(3, 12, 37) == 10  # = MULT²
assert pow(3, 3, 37) == 27   # = target of cubic system
assert pow(3, 9, 37) == 36   # = NEG_H element, 36≡-1 mod 37

# The 18-step tower covers exactly 6 orbits, each 3 times — the 6 QR orbits
tower_orbits_18 = [orbit_of(pow(3, k, 37)) for k in range(1, 19)]
orbit_visits = {}
for k, orb in enumerate(tower_orbits_18, 1):
    orbit_visits.setdefault(orb, []).append(k)
print(f"\n  6 QR orbits, each visited 3 times:")
for orb, ks in sorted(orbit_visits.items()):
    assert len(ks) == 3, f"{orb} visited {len(ks)} times"
    print(f"    {orb:<8}: steps {ks}")

# The 6 QR orbits = {C3, SA_ST_A, NEG_H, D7, SA_ST_B, IC}
# These are exactly the orbits where both QR and solution structure live
qr_orbits = set(orbit_visits.keys())
assert "C3" in qr_orbits and "SA_ST_A" in qr_orbits and "NEG_H" in qr_orbits
assert "IC" in qr_orbits
# Non-QR orbits (NQR half): not visited by powers of 3
nqr_expected = {"DARK_A", "CAS_EXT", "TESLA", "C9", "NQR17", "SEED"}
visited = set(orbit_visits.keys())
assert visited.isdisjoint(nqr_expected), f"Unexpected NQR visit: {visited & nqr_expected}"
print(f"\n  NQR orbits (NOT generated by 3): {sorted(nqr_expected)}")
print(f"  System's C3, SA_ST_A, NEG_H all lie in the QR half — closed under 3's subgroup")

# ── Part 6: Standing analysis for n=252 ──────────────────────────────────────

# 252 mod 37 = 30 ∈ C3 (Part 1)
# 137-orbit of 30
o1 = f(30)   # 26×30 mod 37
o2 = f(o1)
o3 = f(o2)
assert {30, o1, o2} == ORBITS["C3"]
assert o3 == 30

# DR
dr_252 = dr(252)
assert dr_252 == 9
print(f"\nPart 6: 252 standing analysis")
print(f"  252 mod 37 = 30; 137-orbit: 30 → {o1} → {o2} → 30")
print(f"  DR(252) = {dr_252} ∈ {orbit_of(dr_252)}")

# Twin prime: 251 is prime (from T251), 253 = 11×23 (not prime)
# 252 = 251+1 = bridge between 251 and the non-twin composite side
assert not is_prime(252)
assert is_prime(251)
assert not is_prime(253)
print(f"  252 = 251+1; 251 is prime (T251), 253=11×23 (not prime) — no twin straddling here")

# Sophie Germain: 252 not prime; check 251 (done in T251)
# 252 as a bridge: 252 = 4×63 = 4×9×7; each factor maps:
#   4∈C3, 9∈SA_ST_A, 7∈D7 → product: C3×SA_ST_A×D7
c3_sa = {(a*b)%37 for a in ORBITS["C3"] for b in ORBITS["SA_ST_A"]}
assert orbit_of(list(c3_sa)[0]) == "NEG_H"  # C3×SA_ST_A = C3³ = NEG_H
c3_sa_d7 = {(a*b)%37 for a in c3_sa for b in ORBITS["D7"]}
print(f"  Factor orbits: 4(C3) × 9(SA_ST_A) × 7(D7)")
print(f"  C3 × SA_ST_A = NEG_H; NEG_H × D7 = {orbit_of(list(c3_sa_d7)[0])}")
print(f"  Product mod 37 = 252 mod 37 = 30 ∈ C3 ✓")

# Rule 30
r30 = rule30(n)
r30_mod = r30 % 37
print(f"\n  R30(252) = {r30}; {r30} mod 37 = {r30_mod} ∈ {orbit_of(r30_mod)}")

# Riemann
import math
T = float(n)
N_T = T * math.log(T / (2 * math.pi)) / (2 * math.pi)
floor_N = int(N_T)
floor_mod = floor_N % 37
print(f"  floor(N(252)) = {floor_N}; mod 37 = {floor_mod} ∈ {orbit_of(floor_N)}")

# ── Part 7: Perfect cube structure — the binomial identity ───────────────────
# x³ - 27 = (x-3)³ + 9(x-3) · (??? ) — expand to see clean form
# x³ - 27 = x³ - 9x² + 27x - 27 + 9x² - 27x = (x-3)³ + 9x(x-3)
# So: x³ - 27 = (x-3)[(x-3)² + 9x]
# At the real solution x=3: (x-3)=0 → SEAM
# At the GF(37) asymmetric solutions: (x-3) maps x=4→1∈IC, x=30→27∈NEG_H, x=0→(-3)≡34∈D7

shifts = [(x, (x-3)%37, orbit_of((x-3)%37)) for x in [3,4,30,0,12]]
print(f"\nPart 7: (x-3) shifts for all solution components:")
for x, s, orb in shifts:
    print(f"  x={x}: x-3 ≡ {s} ∈ {orb}")

# At x=4: (x-3)=1∈IC, 9x=36∈NEG_H; (1)²+36=37≡0=SEAM → whole bracket = SEAM
x=4
bracket = ((x-3)**2 + 9*x) % 37
assert bracket == 0
assert orbit_of((x-3)%37) == "IC"  # 1∈IC
assert orbit_of((9*x)%37) == "NEG_H"  # 36∈NEG_H
print(f"  At x=4: (x-3)=1∈IC; 9x=36∈NEG_H; (x-3)²+9x = {bracket} ≡ SEAM")
print(f"  IC + NEG_H = 1+36 = 37 ≡ 0 — IC and NEG_H straddle the field prime")

x=30
bracket30 = ((x-3)**2 + 9*x) % 37
assert orbit_of((x-3)%37) == "NEG_H"  # 27∈NEG_H
print(f"  At x=30: (x-3)=27∈NEG_H; 9x=270%37={270%37}∈{orbit_of(270)}")
print(f"           (x-3)²+9x = {bracket30} mod 37 ∈ {orbit_of(bracket30)}")

print("\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  n = {n}; n mod 37 = 30 ∈ C3 (solution orbit of the cubic system)")
print(f"  Cyclic cubic: GF(37) has exactly 4 solutions")
print(f"    (3,3,3): symmetric, orbit C3")
print(f"    (0,12,4) and rotations: SEAM × SA_ST_A × C3")
print(f"  Orbit chain: C3 → SA_ST_A (coeff 9) → NEG_H (target 27)")
print(f"  ord₃₇(3)=18 (QR subgroup generator); 3^6=26=MULT; 3^3=27=target")
print(f"  n=252 = 4×9×7 = C3 × SA_ST_A × D7; product lands in C3 (n mod 37=30)")
print(f"  R30(252) mod 37 = {r30_mod} ∈ {orbit_of(r30_mod)}")
print(f"  floor(N(252)) mod 37 = {floor_mod} ∈ {orbit_of(floor_N)}")
