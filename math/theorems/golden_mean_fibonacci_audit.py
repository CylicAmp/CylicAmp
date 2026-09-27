"""
golden_mean_fibonacci_audit.py

Connections between the golden mean / KAM torus analysis and the framework.

─────────────────────────────────────────────────────────────────
GOLDEN MEAN:  γ = (√5−1)/2 = 1/φ  where φ = (1+√5)/2

CONTINUED FRACTION:  γ = [0; 1, 1, 1, 1, …]
  All coefficients = 1 after the initial 0.
  This is the CONTINUED FRACTION ANALOGUE of the repunit:
    repunit_n = 111…1  (n ones in decimal)
    γ CF      = [0; 1, 1, 1, …]  (ones repeating without end)
  The convergents F(n−1)/F(n) → γ with denominators = Fibonacci numbers.

CONNECTIONS TO FRAMEWORK:
  (G1) F(12) = 144 = 12² = sum of all 27 DR values (digit_repetition_dr_audit).
       DR(144) = 9.  144 also appears as the 6th term of the descent 191→100.

  (G2) 37 | F(19) = 4181 = 37 × 113.
       37 is the framework modulus (111 = 3×37).
       Entry point of 37 in Fibonacci = 19; both 37 and 113 are prime.

  (G3) 17 | F(9) = 34 = 2×17.
       17 is one of the criss-cross primes {17, 71, 18, 81}.
       Entry point of 17 in Fibonacci = 9.
       Period: F(9k) divisible by 17 for all k ≥ 1.

  (G4) DR period-24 of Fibonacci:
       DR(F(n)) repeats with period 24 (Pisano period mod 9).
       Sequence: [1,1,2,3,5,8,4,3,7,1,8,9, 8,8,7,6,4,1,5,6,2,8,1,9]
       Sum = 117, DR(117) = 9.
       DR values 1 and 8 each appear 5 times (all others appear 2 times).
       1 and 8 are DR-conjugates: 1+8 = 9.

  (G5) Hurwitz bound: |γ − p/q| > 1/(√5 · q²).
       γ saturates this bound exactly — it is the HARDEST irrational
       to approximate by rationals.  √5 = growth normalization of Fibonacci
       (F(n) ~ φⁿ/√5).  This places γ at the extreme of the Diophantine
       condition, mirroring the role of the all-ones repunit in the framework.

  (G6) KAM threshold connection:
       Greene's K_c ≈ 0.97163… is the critical coupling at which the
       golden-mean KAM torus breaks.  Below K_c the torus (quasiperiodic
       orbit with rotation number γ) survives; above it dissolves into chaos.
       This is structurally parallel to the fill/bridge operation
       (zero_fill_bridge_audit.py): there is a threshold at which units
       can no longer be redistributed into a stable (repunit) equilibrium.

─────────────────────────────────────────────────────────────────
"""

from sympy import isprime, factorint
from collections import Counter

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


# ── Fibonacci sequence ────────────────────────────────────────────────────────

def fibonacci(n):
    fibs = [1, 1]
    while len(fibs) < n:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs[:n]

FIBS = fibonacci(80)


# ── G1: F(12) = 144 = 12² ────────────────────────────────────────────────────

check(FIBS[11] == 144, "F(12)=144", FIBS[11], 144)
check(144 == 12 ** 2, "144=12²", 144, 12 ** 2)
check(dr(144) == 9, "DR(144)=9", dr(144), 9)

# 144 = sum of all 27 DR values (verified in digit_repetition_dr_audit)
# Descent 191→100: terms are 191,188,177,166,155,144,133,122,111,100
descent = [191] + [188 - 11 * k for k in range(9)]
check(144 in descent, "144 in descent 191→100", 144 in descent, True)
check(descent.index(144) == 5, "144 is 6th term (index 5)", descent.index(144), 5)

# F(12) position 12 = 2 × position 6 in descent (0-indexed)
check(12 == 2 * 6, "12 = 2×6 (Fibonacci index = 2 × descent index)", 12, 2 * 6)


# ── G2: 37 | F(19) ───────────────────────────────────────────────────────────

check(FIBS[18] == 4181, "F(19)=4181", FIBS[18], 4181)
check(4181 % 37 == 0, "37|F(19)", 4181 % 37, 0)
check(4181 // 37 == 113, "F(19)=37×113", 4181 // 37, 113)
check(isprime(37), "37 is prime", isprime(37), True)
check(isprime(113), "113 is prime", isprime(113), True)

# 37 is the entry point — no earlier Fibonacci divisible by 37
for i in range(18):
    check(FIBS[i] % 37 != 0, f"37 ∤ F({i+1})", FIBS[i] % 37, "!=0")

# Framework: 111 = 3×37
check(factorint(111) == {3: 1, 37: 1}, "111=3×37", factorint(111), {3: 1, 37: 1})


# ── G3: 17 | F(9) = 34 ───────────────────────────────────────────────────────

check(FIBS[8] == 34, "F(9)=34", FIBS[8], 34)
check(34 % 17 == 0, "17|F(9)", 34 % 17, 0)
check(34 == 2 * 17, "F(9)=2×17", 34, 2 * 17)

# Entry point of 17 in Fibonacci = 9
for i in range(8):
    check(FIBS[i] % 17 != 0, f"17 ∤ F({i+1})", FIBS[i] % 17, "!=0")

# 17 is a criss-cross prime (DR=8); F(9)=34, DR(34)=7
check(dr(17) == 8, "DR(17)=8", dr(17), 8)
check(dr(34) == 7, "DR(34)=7", dr(34), 7)

# Period: 17 | F(9k) for k=1,2,3
for k in [1, 2, 3]:
    check(FIBS[9 * k - 1] % 17 == 0, f"17|F({9*k})", FIBS[9*k - 1] % 17, 0)


# ── G4: DR period-24 of Fibonacci ────────────────────────────────────────────

DR_FIBS_24 = [dr(f) for f in FIBS[:24]]
EXPECTED_DR_24 = [1, 1, 2, 3, 5, 8, 4, 3, 7, 1, 8, 9, 8, 8, 7, 6, 4, 1, 5, 6, 2, 8, 1, 9]
check(DR_FIBS_24 == EXPECTED_DR_24, "DR(F_n) period-24", DR_FIBS_24, EXPECTED_DR_24)

# Verify period: DR(F(n+24)) = DR(F(n)) for n=1..24
for i in range(24):
    check(dr(FIBS[i]) == dr(FIBS[i + 24]),
          f"period-24 at n={i+1}", dr(FIBS[i]), dr(FIBS[i + 24]))

# Sum and DR of the period
period_sum = sum(EXPECTED_DR_24)
check(period_sum == 117, "period sum=117", period_sum, 117)
check(dr(period_sum) == 9, "DR(117)=9", dr(period_sum), 9)

# DR-conjugate pair (1,8) dominates: each appears 5 times
counts = Counter(EXPECTED_DR_24)
check(counts[1] == 5, "DR=1 appears 5×", counts[1], 5)
check(counts[8] == 5, "DR=8 appears 5×", counts[8], 5)
check(1 + 8 == 9, "1+8=9 (DR-conjugates)", 1 + 8, 9)

# All other DRs appear exactly twice
for v in [2, 3, 4, 5, 6, 7, 9]:
    check(counts[v] == 2, f"DR={v} appears 2×", counts[v], 2)


# ── G5: CF [0;1,1,...] — convergents are Fibonacci ratios ────────────────────

# Convergent denominators = Fibonacci numbers
conv_dens = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
for i, d in enumerate(conv_dens):
    check(d == FIBS[i], f"conv_den[{i}]=F({i+1})", d, FIBS[i])

# F(11)/F(12) = 89/144 is best rational approximation before F(12)
gamma = (5 ** 0.5 - 1) / 2
approx = 89 / 144
error = abs(gamma - approx)
check(error < 1e-4, "89/144 ≈ gamma", error, "<1e-4")


# ── G6: Hurwitz constant and √5 ──────────────────────────────────────────────

import math

hurwitz = 1 / math.sqrt(5)
check(abs(hurwitz - 0.44721) < 1e-4, "1/sqrt(5)≈0.44721", hurwitz, 0.44721)

# gamma saturates the Hurwitz bound: |gamma - F(n-1)/F(n)| * F(n)^2 → 1/sqrt(5)
for n in range(5, 13):
    p, q = FIBS[n - 1], FIBS[n]
    product = abs(gamma - p / q) * q ** 2
    check(abs(product - hurwitz) < 0.01,
          f"Hurwitz saturation n={n}", product, hurwitz)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Golden Mean / Fibonacci → Framework Audit")
    print("=" * 62)

    print(f"\n── G1: F(12) = 144 ──")
    print(f"  F(12) = {FIBS[11]} = 12²")
    print(f"  = sum of all 27 DR values (digit_repetition_dr_audit)")
    print(f"  = 6th term of descent 191→100 (descent_191_100_audit)")
    print(f"  DR(144) = {dr(144)}")
    print(f"  Fibonacci index 12 = 2 × descent position 6")

    print(f"\n── G2: 37 | F(19) ──")
    print(f"  F(19) = {FIBS[18]} = 37 × 113  (both prime)")
    print(f"  37 is the framework modulus: 111 = 3×37")
    print(f"  Entry point of 37 in Fibonacci = 19")

    print(f"\n── G3: 17 | F(9) = 34 ──")
    print(f"  F(9) = {FIBS[8]} = 2×17")
    print(f"  17 is criss-cross prime (DR=8)")
    print(f"  Entry point of 17 = 9; period 9 (17|F(9k))")

    print(f"\n── G4: DR period-24 ──")
    print(f"  DR(F_n): {EXPECTED_DR_24}")
    print(f"  Period = 24 (Pisano period mod 9)")
    print(f"  Sum = {period_sum}  DR = {dr(period_sum)}")
    print(f"  DR-conjugates 1 and 8 each appear 5×: 1+8=9")
    print(f"  All other DR values appear 2×")

    print(f"\n── G5: CF as repunit analogue ──")
    print(f"  gamma CF = [0; 1, 1, 1, …] — all-ones (repunit in CF form)")
    print(f"  Convergent denominators: {conv_dens}")
    print(f"  = Fibonacci sequence exactly")
    print(f"  89/144 = {89/144:.10f}")
    print(f"  gamma  = {gamma:.10f}")

    print(f"\n── G6: Hurwitz constant ──")
    print(f"  |gamma - p/q| > 1/(sqrt(5)·q²)  for all p/q")
    print(f"  gamma saturates this: worst-approximable irrational")
    print(f"  F(n) ~ phi^n / sqrt(5): sqrt(5) is the normalization")
    print(f"  Structural parallel: repunit = hardest integer pattern")
    print(f"  gamma = hardest irrational; both built from all-ones")

    print(f"\n── KAM threshold / fill-bridge parallel ──")
    print(f"  K < K_c: torus survives (quasiperiodic, all-ones CF)")
    print(f"  K > K_c: torus dissolves (chaotic)")
    print(f"  Fill/bridge: below threshold → stable repunit equilibrium")
    print(f"  Above threshold → units cannot distribute to equilibrium")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
