#!/usr/bin/env python3
"""
REPUNIT 37-ADIC VALUATION AT ORBIT MULTIPLES OF 37
====================================================
Orbit: 137 + 4k, k=0..332 (333 terms, period 9×37)
9 multiples of 37 in orbit at steps k ∈ {12,49,86,123,160,197,234,271,308}
Values: 37×{5,9,13,17,21,25,29,33,37}

LTE (Lifting the Exponent) for p=37, ord₃₇(10)=3:
  v₃₇(R_n) = 0               if 3 ∤ n
  v₃₇(R_n) = 1 + v₃₇(n/3)   if 3 | n

RESULT TABLE:
  v  = 37×c  |  3|v?  |  v/3          |  v₃₇(v/3)  |  v₃₇(R_v)
  ------------|--------|---------------|-------------|----------
  185 = 37×5  |  No    |  —            |  —          |  0
  333 = 37×9  |  Yes   |  111 = 3×37   |  1          |  2
  481 = 37×13 |  No    |  —            |  —          |  0
  629 = 37×17 |  No    |  —            |  —          |  0
  777 = 37×21 |  Yes   |  259 = 7×37   |  1          |  2
  925 = 37×25 |  No    |  —            |  —          |  0
  1073= 37×29 |  No    |  —            |  —          |  0
  1221= 37×33 |  Yes   |  407 = 11×37  |  1          |  2
  1369= 37²   |  No    |  —            |  —          |  0

PATTERN:
  Exactly 3 of the 9 orbit multiples have v₃₇(R_v) = 2.
  These are v ∈ {333, 777, 1221} — cofactors {9,21,33} = 3×{3,7,11}.
  The remaining 6 have v₃₇(R_v) = 0 (37 ∤ R_v).

  Cofactors divisible by 3: at positions {1,4,7} (0-indexed) in {5,9,13,...,37}.
  These form an AP: cofactors 9,21,33, step 12.
  Orbit step between them: 3×37 = 111 (value difference 3×37×4 = 444).

  First R_v divisible by 37²: R_333.
  333 = 9×37 = 3²×37. This is the smallest orbit multiple of 37 where 3|v.
  R_111 is the first repunit with 37²; R_333 = R_{3×111} also has v₃₇=2.

T-DUALITY ANCHOR:
  v=1369=37² is at step k=308, cofactor 37.
  3 ∤ 1369  →  v₃₇(R_{1369}) = 0.
  37² appears in R_n only via divisibility by 111; 1369 is not a multiple of 111.
  1369 = 37² is the "winding mirror" in the orbit — present as a value, not as
  a repunit index conferring v₃₇=2.

CROSS-CONNECTION:
  R_111 gives v₃₇=2 (from thirtyseven_squared_audit.py).
  333 = 3×111 is the orbit value linking T-duality and valuation:
    step 49 in orbit, cofactor 9 = 3², value 37×9 = 333 = 3×37×3.
  Values giving v₃₇=2 in orbit: {333, 777, 1221} = 3×{111, 259, 407} = 3×37×{3,7,11}.
"""

from sympy import factorint, isprime

errors = []

def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}")
    if not cond:
        errors.append(label)

def dr(n):
    return 0 if n == 0 else 1 + (abs(int(n)) - 1) % 9

def repunit(k):
    return (10**k - 1) // 9

def v37(n):
    count = 0
    while n % 37 == 0:
        n //= 37
        count += 1
    return count

# Orbit multiples of 37
ORBIT_STEPS   = [12, 49, 86, 123, 160, 197, 234, 271, 308]
ORBIT_COFACTORS = [5, 9, 13, 17, 21, 25, 29, 33, 37]
ORBIT_VALUES  = [137 + 4*k for k in ORBIT_STEPS]

# ── SETUP VERIFICATION ────────────────────────────────────────────────────────

print("=== ORBIT MULTIPLES OF 37: SETUP ===")
check("9 steps", len(ORBIT_STEPS) == 9)
check("values = 37 × cofactors", ORBIT_VALUES == [37*c for c in ORBIT_COFACTORS])
check("cofactors form AP step 4: 5,9,...,37", ORBIT_COFACTORS == list(range(5,38,4)))
check("last value = 37² = 1369", ORBIT_VALUES[-1] == 37**2)
check("ord₃₇(10) = 3  →  37 | R_n iff 3|n", pow(10,3,37)==1 and all(pow(10,k,37)!=1 for k in [1,2]))
check("v₃₇(R_3) = v₃₇(111) = 1", v37(repunit(3)) == 1)
print()

# ── LTE FORMULA ──────────────────────────────────────────────────────────────

print("=== LTE: v₃₇(R_n) = 1 + v₃₇(n/3) when 3|n ===")
check("v₃₇(R_3) = 1", v37(repunit(3)) == 1)
check("v₃₇(R_6) = 1  [3|6, 6/3=2, v₃₇(2)=0]", v37(repunit(6)) == 1)
check("v₃₇(R_111) = 2  [111=3×37, v₃₇(111)=1]", v37(repunit(111)) == 2)
check("v₃₇(R_333) = 2  [333=3×111=3²×37, v₃₇(111)=1]", v37(repunit(333)) == 2)
check("v₃₇(R_1) = 0  [3 ∤ 1]", v37(repunit(1)) == 0)
check("v₃₇(R_37) = 0  [3 ∤ 37]", v37(repunit(37)) == 0)
print()

# ── VALUATION TABLE ───────────────────────────────────────────────────────────

print("=== VALUATION TABLE: v₃₇(R_v) FOR EACH ORBIT MULTIPLE ===")
print(f"  {'k':>4}  {'v':>5}  {'cof':>4}  {'3|v?':>5}  {'v₃₇(R_v)':>9}")
print("  " + "-"*42)

val_list = []
div3_vals = []
not_div3_vals = []

for step, v, cof in zip(ORBIT_STEPS, ORBIT_VALUES, ORBIT_COFACTORS):
    div3 = (v % 3 == 0)
    val = v37(repunit(v))
    val_list.append(val)
    marker = " ← v₃₇=2" if val == 2 else ""
    print(f"  {step:4d}  {v:5d}  37×{cof:2d}  {'Yes' if div3 else 'No':>5}  {val:9d}{marker}")
    if div3:
        div3_vals.append(v)
    else:
        not_div3_vals.append(v)

print()

check("3|v iff 3|cofactor", all((v%3==0) == (c%3==0) for v,c in zip(ORBIT_VALUES, ORBIT_COFACTORS)))
check("exactly 3 values have v₃₇(R_v)=2", val_list.count(2) == 3)
check("exactly 6 values have v₃₇(R_v)=0", val_list.count(0) == 6)
check("v₃₇=2 values are {333,777,1221}", sorted(div3_vals) == [333, 777, 1221])
check("v₃₇=0 values are {185,481,629,925,1073,1369}", sorted(not_div3_vals) == [185,481,629,925,1073,1369])
print()

# ── DIVISIBLE-BY-3 COFACTORS ─────────────────────────────────────────────────

print("=== COFACTORS DIVISIBLE BY 3 ===")
div3_cofs = [c for c in ORBIT_COFACTORS if c % 3 == 0]
check("cofactors with 3|c: {9,21,33}", div3_cofs == [9, 21, 33])
check("these = 3×{3,7,11}", [c//3 for c in div3_cofs] == [3, 7, 11])
check("3,7,11 are all prime", all(isprime(p) for p in [3,7,11]))
check("cofactor step between them = 12", div3_cofs[1]-div3_cofs[0] == 12 and div3_cofs[2]-div3_cofs[1] == 12)
check("value step between v₃₇=2 entries = 444 = 12×37", sorted(div3_vals)[1]-sorted(div3_vals)[0] == 444)
check("DR(444) = 3  (444 = 4×111 = 4×3×37)", dr(444) == 3)
check("positions in cofactor list: {1,4,7}  (every 3rd, starting idx 1)",
      [i for i,c in enumerate(ORBIT_COFACTORS) if c%3==0] == [1, 4, 7])
print()

# ── LTE VERIFICATION FOR v₃₇=2 ENTRIES ──────────────────────────────────────

print("=== LTE CHECK FOR v₃₇(R_v) = 2 ENTRIES ===")
for v, cof in [(333,9),(777,21),(1221,33)]:
    thirds = v // 3
    check(f"v={v}=37×{cof}: v/3={thirds}, v₃₇(v/3)=v₃₇({thirds})=1",
          v37(thirds) == 1)
    check(f"v₃₇(R_{v}) = 1 + v₃₇({thirds}) = 2", v37(repunit(v)) == 2)
    # Also verify factorizations
    f = factorint(thirds)
    print(f"    {thirds} = {f}")
    print()

# ── T-DUALITY ANCHOR: 37² = 1369 ─────────────────────────────────────────────

print("=== T-DUALITY ANCHOR: v = 1369 = 37² ===")
check("step k=308 → v=1369=37²", 137+4*308 == 37**2)
check("3 ∤ 1369  →  v₃₇(R_{1369}) = 0", 1369 % 3 != 0 and v37(repunit(1369)) == 0)
check("37² appears in R_n iff 111|n; 111 ∤ 1369", 1369 % 111 != 0)
check("1369 = 37²: DR(1369) = 1", dr(1369) == 1)
check("1369 ≡ 37 (mod 333)  [37²-37=1332=4×333]", 1369 % 333 == 37)
print(f"  1369 is the orbit's winding mirror (37² value) but contributes")
print(f"  v₃₇(R_{{1369}})=0 — the 37² index milestone is R_{{111}}, not R_{{1369}}.")
print()

# ── CROSS-CONNECTION: R_111 AND ORBIT ────────────────────────────────────────

print("=== CROSS-CONNECTION: R_111 AND THE ORBIT ===")
check("R_111 = R_{3×37}: v₃₇(R_{111}) = 2", v37(repunit(111)) == 2)
check("111 itself is a value in the orbit: 137+4k → 111 not in orbit (111<137)", 111 < 137)
check("333 = 3×111 IS in orbit at step k=49", 137+4*49 == 333)
check("v₃₇(R_{333}) = 2  (333 = 3×111, same valuation)", v37(repunit(333)) == 2)
check("R_{333} = R_{3×111}: v₃₇ = 1 + v₃₇(111) = 1+1 = 2", v37(repunit(333)) == 2)
check("v₃₇(R_{3×111×37}) would be 3  (first repunit with 37³)",
      v37(repunit(3*111*37)) == 3)
check("3×111×37 = 12321 = R_3²  [digit palindrome]", 3*111*37 == 12321)
print()

# ── VALUATION vs DR PATTERN ──────────────────────────────────────────────────

print("=== VALUATION vs DR ===")
orbit_drs = [dr(v) for v in ORBIT_VALUES]
print("  v         v₃₇(R_v)  DR(v)  DR(cof)")
for v, val, cof in zip(ORBIT_VALUES, val_list, ORBIT_COFACTORS):
    print(f"  {v:<7d}  {val}          {dr(v)}      {dr(cof)}")

check("DR(37n) = DR(n) for all n  (since DR(37)=1)",
      all(dr(37*c)==dr(c) for c in ORBIT_COFACTORS))
check("v₃₇=2 cofactors {9,21,33}: DRs = {9,3,6}", [dr(c) for c in div3_cofs] == [9,3,6])
check("sum of DRs for v₃₇=2 cofactors = 18, DR(18)=9", sum(dr(c) for c in div3_cofs)==18 and dr(18)==9)
check("sum of DRs for v₃₇=0 cofactors: {5,13,17,25,29,37}",
      [dr(c) for c in ORBIT_COFACTORS if c%3!=0] == [dr(c) for c in [5,13,17,25,29,37]])
print()

# ── SUMMARY ───────────────────────────────────────────────────────────────────

print("=== SUMMARY ===")
print("  9 orbit multiples of 37: 37×{5,9,13,17,21,25,29,33,37}")
print("  3 give v₃₇(R_v)=2:  v ∈ {333,777,1221}  (cofactors 9,21,33 = 3×{3,7,11})")
print("  6 give v₃₇(R_v)=0:  remainder")
print("  37²=1369 at k=308: v₃₇(R_{1369})=0  (3 ∤ 1369)")
print("  First orbit entry with v₃₇=2: R_{333}; 333=3×37×3=3²×37")
print("  Valuation 3 first achieved at R_{12321}=R_{3²×37²}=R_{3×111×37}")
print()

if errors:
    print(f"FAILURES: {errors}")
else:
    print("All claims verified.")
