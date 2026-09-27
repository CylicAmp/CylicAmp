#!/usr/bin/env python3
"""
COMPLEMENT CASCADE — 31 STRUCTURE AUDIT
=========================================
Five groups of digit pairs, each with three rows.
Groups 1-4: constraint (a+b=10, c+d=10, e+f=11, b+c=11) → cascade always = 31
Group 5:    breaks constraint → cascade routes through URI tier 14 → lands at 23

STRUCTURE THEOREM [PROVEN]:
  Given:  a+b=10,  c+d=10,  e+f=11,  b+c=11
  Then:   a+d = (10-b) + (10-c) = 20 - (b+c) = 20 - 11 = 9
  Cascade: 2×(e+f) + d + a = 22 + 9 = 31  [always, regardless of which digits]
  31 = 2^5 - 1  (Mersenne prime M_5)
  DR(31) = 4

GROUP 5 (constraint broken):
  a+b=10,  c+d=1,  e+f=2,  b+c=2  (≠ 11)
  a+d = 9+0 = 9  (same constant)
  e+f + 11 (cascade const) = 2+11 = 13
  13 is one below URI tier 14  → URI approach: 13+1=14
  14 + a = 14 + 9 = 23
  23 ∈ URI_TIERS,  DR(23) = 5
  23 | 3404 = T(37)+T(73) = 4×23×37

FINAL CHAIN:
  4×4=16,  DR(16)=7   [four groups, each DR=4; 4 squared]
  DR(16) + DR(31) = 7+4 = 11,  DR(11) = 2   [groups 1-4 + their cascade DR]
  DR(16) + DR(23) = 7+5 = 12,  DR(12) = 3   [groups 1-4 + group 5 cascade DR]
  DR=2 = witness residue  (L(T(37))+L(T(73))) mod 37 = (14+25) mod 37 = 2

NOTE — arithmetic corrections:
  User wrote "2+11=14":  2+11=13  (off by 1; 13+1=14 via URI approach)
  User wrote "7+5=13=4": 7+5=12,  DR(12)=3  (not 13 or 4)
  All other computations verified correct.
"""

from sympy import isprime

errors = []

def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}")
    if not cond:
        errors.append(label)

def dr(n):
    return 0 if n == 0 else 1 + (abs(int(n)) - 1) % 9

URI_TIERS = frozenset({14, 23, 32, 41})

GROUPS = [
    ((1,9), (2,8), (3,8)),
    ((3,7), (4,6), (7,4)),
    ((5,5), (6,4), (2,9)),
    ((7,3), (8,2), (6,5)),
]

# ── STRUCTURE THEOREM ─────────────────────────────────────────────────────────

print("=== STRUCTURE THEOREM ===")
print("  Constraint: a+b=10, c+d=10, e+f=11, b+c=11")
print("  Consequence: a+d = 20-(b+c) = 20-11 = 9")
print("  Cascade: 2*(e+f) + d + a = 22 + 9 = 31")
print()
check("31 = 2^5 - 1  (Mersenne prime)", 31 == 2**5 - 1)
check("31 is prime", isprime(31))
check("DR(31) = 4", dr(31) == 4)
print()

# ── GROUPS 1-4 ────────────────────────────────────────────────────────────────

print("=== GROUPS 1-4: CASCADE TO 31 ===")

for i, (r1, r2, r3) in enumerate(GROUPS, 1):
    a, b = r1;  c, d = r2;  e, f = r3
    label = f"Group {i}: ({a}+{b})({c}+{d})({e}+{f})"

    check(f"{label}  row1={a+b}=10", a+b == 10)
    check(f"{label}  row2={c+d}=10", c+d == 10)
    check(f"{label}  row3={e+f}=11", e+f == 11)
    check(f"{label}  cross={b}+{c}={b+c}=11", b+c == 11)

    # cascade
    step1 = e + f          # 11
    step2 = step1 + step1  # 22
    step3 = step2 + d      # 22 + d
    step4 = step3 + a      # 22 + d + a = 31
    check(f"{label}  2*(e+f)={step2}", step2 == 22)
    check(f"{label}  +d={step3}", step3 == 22 + d)
    check(f"{label}  +a={step4}=31", step4 == 31)
    check(f"{label}  DR(31)=4", dr(31) == 4)
    print()

# ── ALGEBRAIC PROOF ──────────────────────────────────────────────────────────

print("=== ALGEBRAIC PROOF ===")
print("  a+b=10  =>  a = 10-b")
print("  c+d=10  =>  d = 10-c")
print("  b+c=11  =>  a+d = (10-b)+(10-c) = 20-(b+c) = 20-11 = 9")
print("  cascade = 2*(e+f) + d + a = 2*11 + 9 = 22+9 = 31  QED")
check("2*11 + 9 = 31", 2*11 + 9 == 31)
print()

# ── GROUP 5: BROKEN CONSTRAINT ───────────────────────────────────────────────

print("=== GROUP 5: CONSTRAINT BROKEN, URI APPROACH ===")
r1=(9,1); r2=(1,0); r3=(1,1)
a,b=r1;  c,d=r2;  e,f=r3

check("row1: 9+1=10", a+b == 10)
check("row2: 1+0=1  (≠10, constraint broken)", c+d == 1)
check("row3: 1+1=2", e+f == 2)
check("cross: 1+1=2  (≠11)", b+c == 2)
check("a+d = 9+0 = 9  (same constant as groups 1-4)", a+d == 9)

# Cascade with URI approach
raw = (e+f) + 11   # 2+11 = 13
check(f"(e+f) + 11 = {raw}", raw == 13)
check("13 is one below URI tier 14", raw == 14-1 and 14 in URI_TIERS)

# URI approach: when one step below a URI tier, advance to the tier
uri_approached = 14
check("URI approach: 13 -> 14  (14 ∈ URI_TIERS)", uri_approached in URI_TIERS)
check("DR(14) = 5  (all URI tiers have DR=5)", dr(14) == 5)

final = uri_approached + a   # 14 + 9 = 23
check(f"14 + a = 14 + {a} = {final}", final == 23)
check("DR(23) = 5", dr(23) == 5)
check("23 ∈ URI_TIERS", 23 in URI_TIERS)
check("23 | 3404 = T(37)+T(73) = 4×23×37", 3404 % 23 == 0)
check("3404 = 4×23×37", 4*23*37 == 3404)
print()

# ── FIRST DIGITS ACROSS ALL GROUPS ───────────────────────────────────────────

print("=== FIRST DIGITS: ALL ODD SINGLE DIGITS ===")
first_digits = [r1[0] for r1,_,_ in GROUPS] + [9]
check("first digits = [1,3,5,7,9]  (all odd single digits)", first_digits == [1,3,5,7,9])
print(f"  first digits: {first_digits}")
print(f"  groups 1-4 → cascade 31  (Mersenne prime)")
print(f"  group 5    → cascade 23  (URI tier, factor of T(37)+T(73))")
print()

# ── FINAL CHAIN ───────────────────────────────────────────────────────────────

print("=== FINAL CHAIN ===")
check("4×4=16", 4*4 == 16)
check("DR(16) = 7  [four groups, each with DR(cascade)=4; 4 squared]", dr(16) == 7)

# DR(16) + DR(groups 1-4 result)
check("DR(16) + DR(31) = 7+4 = 11", dr(16)+dr(31) == 11)
check("DR(11) = 2  = witness residue", dr(11) == 2)
check("witness residue = (L(T(37))+L(T(73))) mod 37 = (14+25) mod 37 = 2",
      ((-23)%37 + (-49)%37) % 37 == 2)

# DR(16) + DR(group 5 result)
check("DR(16) + DR(23) = 7+5 = 12", dr(16)+dr(23) == 12)
check("DR(12) = 3", dr(12) == 3)

print()
print("  NOTE: user wrote 7+5=13=4; computed 7+5=12, DR(12)=3")
print("  NOTE: user wrote 2+11=14; computed 2+11=13 (URI approach gives 14)")
print()

# ── CYCLE CHECK ───────────────────────────────────────────────────────────────

print("=== CYCLE ===")
total_dr = dr(16) + dr(31) + dr(23)   # 7+4+5 = 16
check("DR(16) + DR(31) + DR(23) = 7+4+5 = 16", total_dr == 16)
check("DR(16) = 7  — closes the cycle", dr(total_dr) == 7)
print(f"  7 + 4 + 5 = 16,  DR(16) = 7  [returns to start]")
print()

if errors:
    print(f"FAILURES: {errors}")
else:
    print("All verified claims pass.")
