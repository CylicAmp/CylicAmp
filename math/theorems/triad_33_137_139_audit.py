"""
triad_33_137_139_audit.py

The 33-137-139 triad: count, prime, twin prime, and fine-structure constant.

─────────────────────────────────────────────────────────────────
TRIAD:
  33   — count of DR-8 numbers in 1..300
  137  — the 33rd prime; slot 26 in Z/37Z
  139  — twin prime of 137; slot 28 in Z/37Z

CHAIN:
  DR=8 numbers in 1..300: count = 33
  33rd prime               = 137
  137 + 2                  = 139  (twin prime)
  1/137 ≈ α               (fine-structure constant, QED)

KEY FACTS:
  (T1) DR-8 numbers in 1..300 are {8, 17, 26, 35, …, 296}.
       Arithmetic sequence: first = 8, step = 9, last = 296.
       Count = (296 − 8)/9 + 1 = 33.
       DR-8 sequence contains 17 (2nd term, criss-cross prime)
       and 26 (3rd term, slot-26 in Z/37Z = slot of 137).

  (T2) 33rd prime = 137.  (Verified by sieve.)

  (T3) (137, 139) is a twin prime pair.  Twin gap = 2.

  (T4) Fine-structure constant α = 1/137.035999… ≈ 1/137.
       1/137 approximates α to within 0.026%.

  (T5) Slot assignments in Z/37Z:
         33 mod 37 = 33   (slot 33 = 37 − 4)
        137 mod 37 = 26   (slot 26; chain 137→248→359, step 111)
        139 mod 37 = 28   (slot 28)
       Slot gap (137→139) = 28 − 26 = 2 = twin prime gap.

  (T6) DR connections:
       DR(33)  = 6
       DR(137) = 2  (1+3+7=11→2)
       DR(139) = 4  (1+3+9=13→4)
       DR(137) + DR(139) = 2 + 4 = 6 = DR(33).
       DR(137 × 139) = DR(19043) = 8 = the DR of the counting set.

  (T7) 33 = 3 × 11.  Both factors are framework primes:
       111 = 3 × 37; 11 = repunit_2; 33 = 3 × repunit_2.
       DR(33) = 6.  33 appears in the equal-digit DR-6 cluster
       {6, 33, 222, 111111} (all numbers with equal non-zero digits
       that have DR = 6).
─────────────────────────────────────────────────────────────────
"""

from sympy import isprime, factorint

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = n % 9
    return r if r else 9


# ── Sieve ─────────────────────────────────────────────────────────────────────

def primes_up_to_n(count):
    sieve = [True] * (count * 15)
    sieve[0] = sieve[1] = False
    result = []
    for i in range(2, len(sieve)):
        if sieve[i]:
            result.append(i)
            if len(result) >= count:
                break
            for j in range(i * i, len(sieve), i):
                sieve[j] = False
    return result

PRIMES = primes_up_to_n(40)


# ── T1: DR-8 numbers in 1..300 ────────────────────────────────────────────────

DR8 = [n for n in range(1, 301) if dr(n) == 8]
check(len(DR8) == 33, "count DR-8 in 1..300 = 33", len(DR8), 33)
check(DR8[0] == 8,   "first DR-8 = 8",   DR8[0], 8)
check(DR8[1] == 17,  "second DR-8 = 17 (criss-cross prime)", DR8[1], 17)
check(DR8[2] == 26,  "third DR-8 = 26 (slot-26 in Z/37Z)",  DR8[2], 26)
check(DR8[-1] == 296, "last DR-8 = 296", DR8[-1], 296)

# Arithmetic sequence: step 9
for i in range(len(DR8) - 1):
    check(DR8[i + 1] - DR8[i] == 9, f"DR8 step {i}→{i+1} = 9", DR8[i + 1] - DR8[i], 9)

# Count formula
check((296 - 8) // 9 + 1 == 33, "(296-8)/9+1 = 33", (296 - 8) // 9 + 1, 33)

# 17 is criss-cross prime (DR=8)
check(isprime(17), "17 is prime", isprime(17), True)
check(dr(17) == 8, "DR(17) = 8", dr(17), 8)

# 26 is slot-26 in Z/37Z (same slot as 137)
check(26 % 37 == 26, "26 mod 37 = 26", 26 % 37, 26)
check(137 % 37 == 26, "137 mod 37 = 26 (same slot)", 137 % 37, 26)


# ── T2: 33rd prime = 137 ─────────────────────────────────────────────────────

check(PRIMES[32] == 137, "33rd prime = 137", PRIMES[32], 137)
check(isprime(137), "137 is prime", isprime(137), True)


# ── T3: Twin prime (137, 139) ────────────────────────────────────────────────

check(isprime(139), "139 is prime", isprime(139), True)
check(139 - 137 == 2, "twin prime gap = 2", 139 - 137, 2)
check(PRIMES[33] == 139, "34th prime = 139", PRIMES[33], 139)


# ── T4: Fine-structure constant ───────────────────────────────────────────────

ALPHA_INV = 137.035999084   # CODATA 2018
ALPHA = 1 / ALPHA_INV
relative_error = abs(1 / 137 - ALPHA) / ALPHA
check(relative_error < 0.003, "1/137 ≈ α within 0.3%", relative_error, "<0.003")
# More precise: 1/137.036
check(abs(1 / 137.036 - ALPHA) < 1e-9, "1/137.036 ≈ α", abs(1 / 137.036 - ALPHA), "<1e-9")


# ── T5: Slot assignments in Z/37Z ────────────────────────────────────────────

check(33 % 37 == 33,  "33 mod 37 = 33",  33 % 37,  33)
check(137 % 37 == 26, "137 mod 37 = 26", 137 % 37, 26)
check(139 % 37 == 28, "139 mod 37 = 28", 139 % 37, 28)

# Slot gap matches twin prime gap
slot_gap = 139 % 37 - 137 % 37
check(slot_gap == 2, "slot gap 137→139 = 2 = twin gap", slot_gap, 2)

# 33 = 37 - 4
check(33 == 37 - 4, "33 = 37-4", 33, 37 - 4)

# 137 slot chain: +111 preserves slot 26
check((137 + 111) % 37 == 26, "(137+111) mod 37 = 26", (137 + 111) % 37, 26)
check((137 + 222) % 37 == 26, "(137+222) mod 37 = 26", (137 + 222) % 37, 26)


# ── T6: DR connections ────────────────────────────────────────────────────────

check(dr(33) == 6,  "DR(33) = 6",  dr(33), 6)
check(dr(137) == 2, "DR(137) = 2", dr(137), 2)
check(dr(139) == 4, "DR(139) = 4", dr(139), 4)

# DR(137) + DR(139) = DR(33)
check(dr(137) + dr(139) == dr(33), "DR(137)+DR(139) = DR(33) = 6",
      dr(137) + dr(139), dr(33))

# DR(137 × 139) = 8 = the DR of the counting set
product = 137 * 139
check(product == 19043, "137×139 = 19043", product, 19043)
check(dr(product) == 8, "DR(137×139) = 8 (= DR of counting set)", dr(product), 8)

# DR(33) + DR(137) + DR(139) = 6+2+4 = 12; DR(12) = 3
triad_dr_sum = dr(33) + dr(137) + dr(139)
check(triad_dr_sum == 12, "DR sum of triad = 12", triad_dr_sum, 12)
check(dr(triad_dr_sum) == 3, "DR(12) = 3", dr(triad_dr_sum), 3)


# ── T7: 33 = 3 × 11 (framework factors) ─────────────────────────────────────

check(factorint(33) == {3: 1, 11: 1}, "33 = 3×11", factorint(33), {3: 1, 11: 1})
check(factorint(111) == {3: 1, 37: 1}, "111 = 3×37", factorint(111), {3: 1, 37: 1})
check(11 % 37 == 11, "11 = repunit_2 mod 37", 11 % 37, 11)

# Equal-digit DR-6 cluster: 6, 33, 222, 111111
for v in [6, 33, 222, 111111]:
    check(dr(v) == 6, f"DR({v}) = 6", dr(v), 6)

# Geometric combinations
check((33 + 137) % 37 == 22, "(33+137) mod 37 = 22", (33 + 137) % 37, 22)
check((137 - 33) % 37 == 30, "(137-33) mod 37 = 30", (137 - 33) % 37, 30)
check((33 * 137) % 37 == 7,  "(33×137) mod 37 = 7",  (33 * 137) % 37, 7)
check((33 + 137 + 139) % 37 == (309 % 37), "33+137+139 = 309",
      33 + 137 + 139, 309)
check(309 % 37 == 13, "309 mod 37 = 13", 309 % 37, 13)
check(dr(309) == 3, "DR(309) = 3", dr(309), 3)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("33-137-139 Triad Audit")
    print("=" * 62)

    print("\n── T1: DR-8 numbers in 1..300 ──")
    print(f"  Sequence: 8, 17, 26, 35, … 296  (step 9)")
    print(f"  Count = {len(DR8)}")
    print(f"  2nd term: {DR8[1]} (criss-cross prime, DR(17)={dr(17)})")
    print(f"  3rd term: {DR8[2]} (slot-26 in Z/37Z = slot of 137)")

    print(f"\n── T2: 33rd prime ──")
    print(f"  p_33 = {PRIMES[32]}")

    print(f"\n── T3: Twin prime pair ──")
    print(f"  (137, 139)  gap = {139-137}")

    print(f"\n── T4: Fine-structure constant ──")
    print(f"  α⁻¹ = {ALPHA_INV}")
    print(f"  1/137   = {1/137:.10f}")
    print(f"  α       = {ALPHA:.10f}")
    print(f"  rel err = {relative_error:.6f}  ({relative_error*100:.4f}%)")

    print(f"\n── T5: Slots in Z/37Z ──")
    print(f"   33 mod 37 = {33%37}  (= 37−4)")
    print(f"  137 mod 37 = {137%37}  (slot 26)")
    print(f"  139 mod 37 = {139%37}  (slot 28)")
    print(f"  Slot gap 137→139 = {139%37 - 137%37} = twin prime gap")

    print(f"\n── T6: DR connections ──")
    print(f"  DR(33)  = {dr(33)}")
    print(f"  DR(137) = {dr(137)}")
    print(f"  DR(139) = {dr(139)}")
    print(f"  DR(137) + DR(139) = {dr(137)+dr(139)} = DR(33)")
    print(f"  DR(137×139) = DR({product}) = {dr(product)} = DR of counting set")

    print(f"\n── T7: 33 = 3×11 (framework factors) ──")
    print(f"  33 = 3×11;  111 = 3×37;  shared factor 3")
    print(f"  11 = repunit_2;  33 = 3 × repunit_2")
    print(f"  Equal-digit DR-6: 6, 33, 222, 111111")

    print(f"\n── Chain summary ──")
    print(f"  DR=8 count in 1..300  →  33")
    print(f"  33rd prime            →  137")
    print(f"  137 + 2               →  139 (twin)")
    print(f"  1/137                 ≈  α (fine-structure constant)")
    print(f"  137 mod 37            =  26 (slot 26 = slot of 100, 248, 359)")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
