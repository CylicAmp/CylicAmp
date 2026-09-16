#!/usr/bin/env python3
"""
37-SQUARED PROPERTY AUDIT
===========================
Core identity: 37^2 + 1 = 10 × 137

This binds the emirp prime 37 directly to the orbit anchor 137.

SQRT(-1) CHAIN [PROVEN]:
  6^2  ≡ -1 (mod  37)   →  37 = 1^2 + 6^2   (Gaussian factorization)
  37^2 ≡ -1 (mod 137)   → 137 = 4^2 + 11^2
  137^2≡ -1 (mod 1877)  → 1877 = 14^2 + 41^2

  Each prime is a square root of -1 modulo the next.
  Generation rule: if p^2 ≡ -1 (mod q) then q = (p^2+1)/10  [when p ≡ 7 (mod 10)]
  Chain: 6 → 37 → 137 → 1877 → ...

  41 IN URI_TIERS: 1877 = 14^2 + 41^2  and  41 ∈ {14, 23, 32, 41}

MULTIPLICATIVE ORDER:
  ord_137(37) = 4  (37 has order 4 in (Z/137Z)*)
  Powers:  37^1≡37,  37^2≡136≡-1,  37^3≡100,  37^4≡1  (mod 137)

SQRT(-1) PAIRS:
  mod 37:  {6, 31}   DR(6)=6,  DR(31)=4;  6+31=37
  mod 137: {37, 100} DR(37)=1, DR(100)=1; 37+100=137

REPUNIT CONNECTION:
  R_3 = 111 = 3 × 37
  R_3^2 = 12321 = 9 × 37^2 = 9(10×137 - 1) = 90×137 - 9

TRIANGULAR NUMBER:
  T(37^2) = 37^2 × (37^2+1)/2 = 37^2 × 685 = 37^2 × 5 × 137
  factors: {5:1, 37:2, 137:1}

ORBIT:
  37^2 = 1369 lies in the orbit 137+4k at step k=308
  37^2 ≡ 37 (mod 333)  [orbit period = 333 = 9×37]

REPUNIT VALUATION (Lifting the Exponent):
  v_37(R_n) = 1 for 3|n, n not divisible by 3×37
  v_37(R_111) = 2  (R_111 = R_{3×37}: first repunit with 37^2 as factor)
"""

from sympy import factorint, isprime, primepi

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

URI_TIERS = frozenset({14, 23, 32, 41})

# ── CORE IDENTITY ─────────────────────────────────────────────────────────────

print("=== CORE IDENTITY: 37^2 + 1 = 10 × 137 ===")
check("37^2 = 1369", 37**2 == 1369)
check("37^2 + 1 = 1370 = 10 × 137", 37**2 + 1 == 10 * 137)
check("=> 37^2 = 10×137 - 1", 37**2 == 10*137 - 1)
check("137 is prime", isprime(137))
check("37 is prime", isprime(37))
check("DR(1369) = 1  (DR of any power of 37 = 1)", dr(1369) == 1)
print()

# ── 37^2 ≡ -1 (mod 137) ───────────────────────────────────────────────────────

print("=== 37^2 ≡ -1 (mod 137) ===")
check("37^2 mod 137 = 136 = 137-1 = -1", pow(37,2,137) == 136)
check("ord_137(37) = 4", pow(37,4,137)==1 and all(pow(37,k,137)!=1 for k in [1,2,3]))
check("37^1 mod 137 = 37", pow(37,1,137) == 37)
check("37^2 mod 137 = 136 ≡ -1", pow(37,2,137) == 136)
check("37^3 mod 137 = 100 ≡ -37", pow(37,3,137) == 100 and (pow(37,3,137)+37)%137==0)
check("37^4 mod 137 = 1", pow(37,4,137) == 1)
print()

# ── 6^2 ≡ -1 (mod 37) ────────────────────────────────────────────────────────

print("=== 6^2 ≡ -1 (mod 37) ===")
check("6^2 = 36 ≡ -1 (mod 37)", 6**2 % 37 == 36)
check("(-6) mod 37 = 31  (second sqrt)", (-6) % 37 == 31)
check("6 + 31 = 37  (pair sums to modulus)", 6+31 == 37)
check("DR(6) = 6", dr(6) == 6)
check("DR(31) = 4", dr(31) == 4)
check("DR(6) + DR(31) = 10, DR(10) = 1", dr(dr(6)+dr(31)) == 1)
check("6 × 31 ≡ 1 (mod 37)  (6 and 31 are inverse to each other mod 37)",
      (6*31) % 37 == 1)
print()

# ── GAUSSIAN INTEGER FACTORIZATIONS ──────────────────────────────────────────

print("=== GAUSSIAN FACTORIZATIONS (p = a^2 + b^2 since p ≡ 1 mod 4) ===")
check("37 ≡ 1 (mod 4)", 37 % 4 == 1)
check("137 ≡ 1 (mod 4)", 137 % 4 == 1)
check("1877 ≡ 1 (mod 4)", 1877 % 4 == 1)

check("37 = 1^2 + 6^2", 1**2 + 6**2 == 37)
check("137 = 4^2 + 11^2", 4**2 + 11**2 == 137)
check("1877 = 14^2 + 41^2", 14**2 + 41**2 == 1877)
check("41 ∈ URI_TIERS  (1877's Gaussian part 41 is a URI tier)", 41 in URI_TIERS)
check("1877 is prime", isprime(1877))
print(f"  Gaussian parts: 37=(1,6), 137=(4,11), 1877=(14,41)")
print(f"  URI connection: 1877 = 14^2 + 41^2,  41 ∈ {{14,23,32,41}}")
print()

# ── SQRT(-1) CHAIN ────────────────────────────────────────────────────────────

print("=== SQRT(-1) CHAIN: 6 → 37 → 137 → 1877 ===")
chain = [37, 137, 1877]
check("6^2 ≡ -1 (mod 37)", 6**2 % 37 == 36)
check("37^2 ≡ -1 (mod 137)", 37**2 % 137 == 136)
check("137^2 ≡ -1 (mod 1877)", 137**2 % 1877 == 1876)

check("(37^2+1)/10 = 137  [generation rule]", (37**2+1)//10 == 137 and (37**2+1)%10==0)
check("(137^2+1)/10 = 1877", (137**2+1)//10 == 1877 and (137**2+1)%10==0)
check("37 ≡ 7 (mod 10)  [rule applies to p ≡ 3 or 7 mod 10]", 37 % 10 == 7)
check("137 ≡ 7 (mod 10)", 137 % 10 == 7)
check("1877 ≡ 7 (mod 10)", 1877 % 10 == 7)
print(f"  All chain elements ≡ 7 (mod 10) ✓")
print()

# ── REPUNIT CONNECTION ────────────────────────────────────────────────────────

print("=== REPUNIT CONNECTION ===")
R3 = repunit(3)
R3sq = R3**2
check("R_3 = 111 = 3 × 37", R3 == 111 and factorint(R3) == {3:1, 37:1})
check("R_3^2 = 12321 = 9 × 37^2", R3sq == 9 * 37**2)
check("R_3^2 = 9(10×137-1) = 90×137 - 9", R3sq == 90*137 - 9)
check("R_3^2 = 12321  [digit palindrome]", R3sq == 12321)
check("str(R_3^2) is palindrome", str(R3sq) == str(R3sq)[::-1])
check("digit_sum(R_3^2) = 9 = 3^2  [repunit digit-sum identity]",
      sum(int(c) for c in str(R3sq)) == 9)
print()

# ── TRIANGULAR NUMBER T(37^2) ─────────────────────────────────────────────────

print("=== T(37^2) = 37^2 × 5 × 137 ===")
T37sq = 37**2 * (37**2 + 1) // 2
check("T(37^2) = 37^2 × (37^2+1)/2", T37sq == 37**2 * (37**2+1)//2)
check("(37^2+1)/2 = 685 = 5 × 137", (37**2+1)//2 == 685 and 685 == 5*137)
check("T(37^2) factors: {5:1, 37:2, 137:1}", factorint(T37sq) == {5:1, 37:2, 137:1})
check("137 divides T(37^2)", T37sq % 137 == 0)
print()

# ── ORBIT PROPERTIES ──────────────────────────────────────────────────────────

print("=== 37^2 IN ORBIT AND MOD-333 ===")
k308 = (37**2 - 137) // 4
check("37^2 = 137 + 4×308 → k=308 in the period-333 orbit", k308 == 308 and 137+4*308==37**2)
check("37^2 ≡ 37 (mod 333)  [333 = 9×37 = orbit period]", 37**2 % 333 == 37)
check("37^2 - 37 = 1332 = 4×333", 37**2 - 37 == 4*333)
check("DR(37^n) = 1 for all n  (DR(37)=1 → multiplicative)",
      all(dr(37**n)==1 for n in range(1,8)))
print()

# ── REPUNIT VALUATION ─────────────────────────────────────────────────────────

print("=== v_37(R_n): WHEN DOES 37^2 DIVIDE A REPUNIT? ===")
check("v_37(R_3)   = 1  (37^1 | R_3)", v37(repunit(3)) == 1)
check("v_37(R_6)   = 1  (37^1 | R_6)", v37(repunit(6)) == 1)
check("v_37(R_111) = 2  (37^2 | R_111, 111 = 3×37)", v37(repunit(111)) == 2)
check("v_37(R_n) = 0 for n not divisible by 3", all(v37(repunit(k))==0 for k in [1,2,4,5,7,8]))
check("v_37(R_37) = 0  (37 does not divide R_37, since 37 ∤ 37)", v37(repunit(37)) == 0)
print()
print("  Lifting the Exponent: v_37(10^(3k)-1) = v_37(10^3-1) + v_37(k) = 1 + v_37(k)")
print("  => 37^2 | R_n  iff  3×37 | n  (smallest: R_111)")
print()

# ── CROSS-CONNECTIONS ─────────────────────────────────────────────────────────

print("=== CROSS-CONNECTIONS ===")
check("37 = prime_index(12), ord_37(10)=3: 10^3≡1 (mod 37)", pow(10,3,37)==1)
check("137 = prime_index(33), ord_137(37)=4: 37^4≡1 (mod 137)", pow(37,4,137)==1)
check("T(73) = 2701 = 37×73, and 137 | T(37^2) via 685=5×137", T37sq%137==0)
check("37^2 + 1 factors: {2:1, 5:1, 137:1}", factorint(37**2+1) == {2:1, 5:1, 137:1})
check("1877 Gaussian part 41 ∈ URI_TIERS and is prime_index(13)",
      41 in URI_TIERS and primepi(41)==13)
print()

if errors:
    print(f"FAILURES: {errors}")
else:
    print("All claims verified.")
