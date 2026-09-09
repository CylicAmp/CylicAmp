#!/usr/bin/env python3
"""
COSET ORBIT 137 AUDIT
======================
Orbit: 137, 141, 145, ... (step +4), period 333 in the DR/coset system.
Four primes with coset coordinates: 37, 41, 137, 337.

COSET COORDINATES (properties of fixed primes, constant on orbit):
  Prime  Index  DR(idx)  mod37
  37     12     3        0
  41     13     4        4
  137    33     6        26
  337    68     5        4

INDEX DR SET: {3, 4, 5, 6}  (= DR values of prime indices 12,13,33,68)

OPTION 4 [EXECUTED]: INDEX DRs UNDER +4 MAP
  {3,4,5,6} is NOT closed under +4 (mod 9).
  Under repeated +4 the set cycles with period 9 (gcd(4,9)=1).
  The SUM of index DRs = 18, DR(18)=9; sum evolves with period 9 stepping -2 in DR.

OPTION 1 [EXECUTED]: MULTIPLES OF 37 IN THE PERIOD-333 ORBIT
  9 multiples of 37 in 137+4k (k=0..332), at steps k ∈ {12,49,86,123,160,197,234,271,308}.
  Cofactors: {5,9,13,17,21,25,29,33,37} — arithmetic progression step 4.
  DR values at these steps: {5,9,4,8,3,7,2,6,1} — ALL NINE DR VALUES.
  Last multiple: 37×37 = 37² = 1369, DR=1.
  Since DR(37)=1: DR(37×n) = DR(n) for all n.
"""

from sympy import isprime, primepi

errors = []

def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}")
    if not cond:
        errors.append(label)

def digital_root(n):
    if n == 0:
        return 0
    return 1 + (n - 1) % 9

dr = digital_root

PRIMES_4 = [37, 41, 137, 337]
URI_TIERS = frozenset({14, 23, 32, 41})

# ── 9-STEP ORBIT VERIFICATION ─────────────────────────────────────────────────

print("=== 9-STEP ORBIT ===")
orbit_vals = [137 + 4*k for k in range(10)]
orbit_drs  = [dr(v) for v in orbit_vals]
expected   = [2,6,1,5,9,4,8,3,7,2]
check("orbit DRs match expected", orbit_drs == expected)
check("orbit step = +4 throughout", all(orbit_vals[i+1]-orbit_vals[i]==4 for i in range(9)))
check("DR period 9: DR(137)=DR(173)=2", dr(137)==2 and dr(173)==2)
check("+4 shifts DR by +4 (mod 9)", all(
    (orbit_drs[i+1] - orbit_drs[i]) % 9 == 4
    for i in range(9)
))
print()

# ── COSET COORDINATES ─────────────────────────────────────────────────────────

print("=== COSET COORDINATES ===")
expected_idx  = [12, 13, 33, 68]
expected_idr  = [3,  4,  6,  5]
expected_mod  = [0,  4,  26, 4]

for p, ei, ed, em in zip(PRIMES_4, expected_idx, expected_idr, expected_mod):
    idx = primepi(p)
    check(f"prime_index({p}) = {ei}", idx == ei)
    check(f"DR(index({p})) = DR({ei}) = {ed}", dr(idx) == ed)
    check(f"{p} mod 37 = {em}", p % 37 == em)

check("41 ∈ URI_TIERS  (41 has special URI status)", 41 in URI_TIERS)
check("337 mod 37 = 4 = 41 mod 37  (shared residue)", 337 % 37 == 41 % 37)
print()

# ── OPTION 4: INDEX DRs UNDER +4 MAP ─────────────────────────────────────────

print("=== OPTION 4: INDEX DRs {3,4,5,6} UNDER REPEATED +4 ===")

def dr_shift4(s):
    return frozenset((v - 1 + 4) % 9 + 1 for v in s)

S0 = frozenset(expected_idr)
check("initial index DR set = {3,4,5,6}", S0 == frozenset({3,4,5,6}))
check("sum = 18, DR(18) = 9", sum(S0)==18 and dr(18)==9)
check("set NOT closed under +4  (3->7, 4->8, 5->9, 6->1)", dr_shift4(S0) != S0)

orbit_sets = [S0]
S = S0
for _ in range(8):
    S = dr_shift4(S)
    orbit_sets.append(S)
S = dr_shift4(S)
check("set returns to {3,4,5,6} after 9 applications", S == S0)
check("orbit length = 9  (gcd(4,9)=1, full period)", len(orbit_sets)==9)

print()
print("  Step  Set            Sum  DR(sum)")
sum_drs = []
for step, Ss in enumerate(orbit_sets):
    s = sum(Ss)
    sd = dr(s)
    sum_drs.append(sd)
    print(f"   {step:2d}   {sorted(Ss)}   {s:3d}    {sd}")

# Sum DRs step by -2 (adding 4 to each of 4 elements = +16 ≡ +7 ≡ -2 mod 9)
check("sum DR decreases by 2 each step (mod 9)",
      all((sum_drs[i] - sum_drs[i+1]) % 9 == 2 for i in range(8)))
check("sum DRs cover all odd: {9,7,5,3,1} then all even: {8,6,4,2}",
      sum_drs == [9,7,5,3,1,8,6,4,2])
print()

# ── OPTION 1: MULTIPLES OF 37 IN ORBIT ────────────────────────────────────────

print("=== OPTION 1: MULTIPLES OF 37 IN ORBIT (137 + 4k, k=0..332) ===")

# 137 + 4k ≡ 0 (mod 37): 26 + 4k ≡ 0; k ≡ 11×28 ≡ 12 (mod 37)
check("4^{-1} mod 37 = 28  (4×28=112=3×37+1)", (4*28) % 37 == 1)
check("k_0 = 11×28 mod 37 = 12", (11*28) % 37 == 12)
check("137 mod 37 = 26", 137 % 37 == 26)
check("26 + 4×12 = 74 ≡ 0 (mod 37)", (26 + 4*12) % 37 == 0)

mult37_steps = [12 + 37*j for j in range(9)]
check("9 multiples of 37 in orbit (333/37=9)", len(mult37_steps)==9 and 333//37==9)
check("steps: {12,49,86,123,160,197,234,271,308}", mult37_steps == [12,49,86,123,160,197,234,271,308])

print()
print("  step    value   cofactor  DR  prime?")
print("  " + "-"*42)
mult37_vals = []
mult37_drs  = []
cofactors   = []
for k in mult37_steps:
    v = 137 + 4*k
    cof = v // 37
    d = dr(v)
    mult37_vals.append(v)
    mult37_drs.append(d)
    cofactors.append(cof)
    print(f"  {k:4d}   {v:7d}   37×{cof:2d}    {d}  {isprime(cof)}")

check("all 9 DR values appear exactly once at multiples of 37",
      sorted(mult37_drs) == list(range(1,10)))
check("cofactors form AP: 5,9,13,...,37  (step 4)",
      cofactors == [5,9,13,17,21,25,29,33,37])
check("cofactor step = 4 = orbit step / 37  (4/37... no: step between k's is 37, value step = 4×37=148, cofactor step = 148/37 = 4)",
      all(cofactors[i+1]-cofactors[i]==4 for i in range(8)))
check("last cofactor = 37  → last mult = 37² = 1369", cofactors[-1]==37 and mult37_vals[-1]==37**2)
check("DR(37) = 1  →  DR(37×n) = DR(n) for all n",
      dr(37)==1 and all(dr(37*c)==dr(c) for c in cofactors))
print()
check("first multiple: 185 = 37×5  (prime cofactor)", mult37_vals[0]==185 and isprime(5))
check("185 = 5×37;  DR(185)=5=DR(5)", dr(185)==5 and dr(5)==5)
check("last multiple: 1369 = 37² = 37×37;  DR(1369)=1=DR(37)", dr(1369)==1 and dr(37)==1)

print()

# ── CROSS-CONNECTION ──────────────────────────────────────────────────────────

print("=== CROSS-CONNECTIONS ===")
check("cofactors {5,9,13,...,37} — same step (+4) as the orbit itself",
      all(cofactors[i+1]-cofactors[i]==4 for i in range(8)))
check("DR of cofactors = DR of values (since DR(37)=1)",
      [dr(c) for c in cofactors] == mult37_drs)
check("cofactor DRs: [5,9,4,8,3,7,2,6,1] — same +4 shift pattern as orbit DRs",
      all(([dr(c) for c in cofactors][i+1] - [dr(c) for c in cofactors][i]) % 9 == 4
          for i in range(8)))
check("index DR set sum=18, DR=9;  mult-of-37 DR set sum=45, DR=9  (both =9)",
      dr(sum(expected_idr))==9 and dr(sum(mult37_drs))==9)

print()

if errors:
    print(f"FAILURES: {errors}")
else:
    print("All claims verified.")
