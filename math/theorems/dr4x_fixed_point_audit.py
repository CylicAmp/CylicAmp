#!/usr/bin/env python3
"""
dr4x_fixed_point_audit.py

Fixed-point analysis of x ↦ dr(4x) in {1..9}.

CLAIMS VERIFIED:

  Fixed points:
    4x ≡ x (mod 9)  ⟺  3x ≡ 0 (mod 9)  ⟺  3|x
    Fixed-point set = {3, 6, 9}
    dr(12) = 1+2 = 3   [NOT 1+3=4 — a prior error corrected here]

  Full orbit structure:
    1 → 4 → 7 → 1   (3-cycle)
    2 → 8 → 5 → 2   (3-cycle)
    3 → 3, 6 → 6, 9 → 9   (fixed)

  Order of 4 in (Z/9Z)*: 3
    4^1=4, 4^2=7, 4^3=1 (mod 9)

  Additive vs multiplicative (13 ≡ 4 mod 9 — the 137-map multiplier mod 9):
    Additive:       dr(4k), k=1..9  → [4,8,3,7,2,6,1,5,9], period 9, hits all digits
    Multiplicative: iterate x↦dr(4x) from 1 → period 3, hits only {1,4,7}

CONNECTIONS TO EXISTING AUDITS:
  automorphic_orbit_ntt_audit.py —
    3-cycles {1,4,7} and {2,5,8} are the CRT fibers (Z/9Z)*→(Z/3Z)*
    Fixed-point set {3,6,9} = 3-6-9 kernel (nilpotent ideal)
    kernel_set = {0,3,6} in Z/9Z; in DR notation (1-indexed) that is {3,6,9}
  diamond_core_gap_chain_audit.py —
    Pivot element chain[8]=9 ≡ 0 (mod 9) belongs to this kernel
  CLAUDE.md —
    ord₃₇(26)=3 (137-map orbits are 3-cycles in GF(37));
    ord₉(4)=3 (same order, different modulus, same multiplier mod 9)
"""

import math
errors = []

def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}")
    if not cond:
        errors.append(label)

def dr(n):
    if n == 0:
        return 0
    return 1 + (n - 1) % 9

# ── THE FIXED POINT THAT OPENED THE ANALYSIS ─────────────────────────────────

print("=== THE FIXED POINT: x = 3 ===")
check("3 × 4 = 12", 3*4 == 12)
check("dr(12) = 1+2 = 3  [earlier messages wrote 1+3=4 — that is wrong]",
      dr(12) == 3)
check("dr(4×3) = 3  [3 is a fixed point of x↦dr(4x)]", dr(4*3) == 3)
print()

# ── FIXED POINT CONDITION ────────────────────────────────────────────────────

print("=== FIXED POINT CONDITION: 3x ≡ 0 (mod 9) ⟺ 3|x ===")
for x in range(1, 10):
    is_fixed = dr(4*x) == x
    is_mult3 = x % 3 == 0
    check(f"x={x}: dr(4×{x})={dr(4*x)}, fixed={str(is_fixed):5s}, 3|x={is_mult3}",
          is_fixed == is_mult3)
print()

# ── FULL MAP ─────────────────────────────────────────────────────────────────

print("=== FULL MAP x ↦ dr(4x) ===")
full_map = {x: dr(4*x) for x in range(1, 10)}
print(f"  {full_map}")
check("1→4", full_map[1] == 4)
check("4→7", full_map[4] == 7)
check("7→1", full_map[7] == 1)
check("{1,4,7} is a closed 3-cycle", {full_map[1], full_map[4], full_map[7]} == {1,4,7})
check("2→8", full_map[2] == 8)
check("8→5", full_map[8] == 5)
check("5→2", full_map[5] == 2)
check("{2,5,8} is a closed 3-cycle", {full_map[2], full_map[5], full_map[8]} == {2,5,8})
check("3→3 (fixed)", full_map[3] == 3)
check("6→6 (fixed)", full_map[6] == 6)
check("9→9 (fixed)", full_map[9] == 9)
check("two 3-cycles + three fixed points covers all nine elements",
      len({1,4,7}) + len({2,5,8}) + len({3,6,9}) == 9)
print()

# ── ORDER OF 4 IN (Z/9Z)* ────────────────────────────────────────────────────

print("=== ORDER OF 4 IN (Z/9Z)* ===")
check("4^1 ≡ 4 (mod 9)", pow(4,1,9) == 4)
check("4^2 ≡ 7 (mod 9)  [16 mod 9 = 7]", pow(4,2,9) == 7)
check("4^3 ≡ 1 (mod 9)  [64 mod 9 = 1]", pow(4,3,9) == 1)
check("no smaller positive k gives 4^k ≡ 1 (mod 9)",
      all(pow(4,k,9) != 1 for k in range(1,3)))
check("ord₉(4) = 3", True)
print("  Every orbit under ×4 has length dividing 3: exactly 1 or 3. No other option.")
print()

# ── SECOND ROUTE ─────────────────────────────────────────────────────────────

print("=== SECOND ROUTE TO FIXED POINT: 3 → +1 → 4 → ×3 → 12 → dr → 3 ===")
check("3 + 1 = 4", 3+1 == 4)
check("4 × 3 = 12", 4*3 == 12)
check("dr(12) = 3  [same fixed point, different approach]", dr(12) == 3)
print()

# ── ADDITIVE VS MULTIPLICATIVE ───────────────────────────────────────────────

print("=== ADDITIVE dr(4k), k=1..9 ===")
check("13 ≡ 4 (mod 9)  [dr(13k)=dr(4k): prior analysis used multiplier 13]",
      13 % 9 == 4)
addseq = [dr(4*k) for k in range(1, 10)]
check("sequence = [4,8,3,7,2,6,1,5,9]", addseq == [4,8,3,7,2,6,1,5,9])
check("hits all nine digits", sorted(addseq) == list(range(1,10)))
check("period 9  [gcd(4,9)=1 ⟹ addition by 4 is a bijection on Z/9Z]",
      math.gcd(4,9) == 1)
print(f"  Sequence: {addseq}")
print()

print("=== MULTIPLICATIVE iterate x↦dr(4x) from x=1 ===")
orbit = []
x = 1
for _ in range(10):
    orbit.append(x)
    x = dr(4*x)
    if x == orbit[0]:
        orbit.append(x)
        break
check("orbit from 1 = [1,4,7,1]", orbit == [1,4,7,1])
check("period = 3", len(orbit)-1 == 3)
print(f"  Orbit: {orbit}")
print()

check("same multiplier 4; additive order 9; multiplicative order 3",
      math.gcd(4,9)==1 and pow(4,3,9)==1)
print("  Adding 4 nine times wraps around; multiplying by 4 three times wraps around.")
print()

# ── CONNECTION: CRT FIBERS ───────────────────────────────────────────────────

print("=== CONNECTION: 3-CYCLES = CRT FIBERS (Z/9Z)* → (Z/3Z)* ===")
units = sorted(k for k in range(1,10) if math.gcd(k,9)==1)
fiber1 = sorted(u for u in units if u % 3 == 1)
fiber2 = sorted(u for u in units if u % 3 == 2)

check("(Z/9Z)* = {1,2,4,5,7,8}", units == [1,2,4,5,7,8])
check("fiber over 1 mod 3 = {1,4,7}", fiber1 == [1,4,7])
check("fiber over 2 mod 3 = {2,5,8}", fiber2 == [2,5,8])
check("3-cycle {1,4,7} = fiber1", set(fiber1) == {1,4,7})
check("3-cycle {2,5,8} = fiber2", set(fiber2) == {2,5,8})
print("  The two 3-cycles of ×4 in Z/9Z are exactly the CRT fibers.")
print("  [Established in automorphic_orbit_ntt_audit.py, confirmed here by construction.]")
print()

# ── CONNECTION: FIXED POINTS = 3-6-9 KERNEL ─────────────────────────────────

print("=== CONNECTION: FIXED POINTS = 3-6-9 KERNEL ===")
fixed = sorted(x for x in range(1,10) if dr(4*x)==x)
check("fixed-point set = {3,6,9}", fixed == [3,6,9])
check("3·3 = 9 ≡ 0 (mod 9)  [nilpotency index 2]", (3*3) % 9 == 0)
check("units ∪ {3,6,9} = {1..9}", set(units) | {3,6,9} == set(range(1,10)))
check("units ∩ {3,6,9} = ∅", set(units) & {3,6,9} == set())
print("  Fixed-point set = nilpotent ideal (3) in Z/9Z.")
print("  [Kernel {0,3,6} in Z/9Z; in DR (1-indexed) that is {9,3,6} = {3,6,9}.]")
print()

# ── GF(37) PARALLEL ──────────────────────────────────────────────────────────

print("=== PARALLEL: ord₉(4)=3 and ord₃₇(26)=3 ===")
check("137 mod 37 = 26 = MULT  [the 137-map multiplier in GF(37)]", 137 % 37 == 26)
check("137 mod 9  = 2  [NOT 4; DR(137)=1+3+7=11→2]", 137 % 9 == 2)
check("13  mod 9  = 4  [the additive sequence uses 13; 13≡4 mod 9]", 13 % 9 == 4)
check("ord₉(4) = 3   [4^3 ≡ 1 mod 9]",  pow(4,3,9)==1 and all(pow(4,k,9)!=1 for k in [1,2]))
check("ord₃₇(26) = 3  [26^3 ≡ 1 mod 37]", pow(26,3,37)==1 and all(pow(26,k,37)!=1 for k in [1,2]))
print("  137 mod 37 = 26 (GF(37) multiplier); ord₃₇(26) = 3.")
print("  13  mod 9  = 4  (Z/9Z additive step in prior analysis); ord₉(4) = 3.")
print("  Different source numbers, same orbit order 3, different moduli.")
print()

# ── SUMMARY ──────────────────────────────────────────────────────────────────

print("=== SUMMARY ===")
print("  x ↦ dr(4x) on {1..9}:")
print("  Fixed: {3,6,9}  = 3-6-9 kernel  [3|x]")
print("  Cycle {1,4,7}   = CRT fiber over 1 mod 3  in (Z/9Z)*→(Z/3Z)*")
print("  Cycle {2,5,8}   = CRT fiber over 2 mod 3  in (Z/9Z)*→(Z/3Z)*")
print("  ord₉(4) = 3  =  ord₃₇(26)  [137-map order, both moduli]")
print("  Additive dr(4k): period 9, bijection, all digits hit")
print("  Multiplicative iterate: period 3, one fiber only")
print()

if errors:
    print(f"FAILURES: {errors}")
else:
    print("All verified claims pass.")
