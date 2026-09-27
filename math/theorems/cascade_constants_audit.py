"""
cascade_constants_audit.py

φ, e, π as cascade radii: first-digit axioms, Euler identity,
products/powers tracing the DR doubling cycle and Z/37Z structure.

─────────────────────────────────────────────────────────────────
THREE CONSTANTS, THREE FIRST DIGITS:

  Constant  Value           First digit  Cascade axiom
  ────────  ──────────────  ───────────  ─────────────
  φ (phi)   1.618033988…        1         UNIT
  e         2.718281828…        2         COMPLEXITY
  π (pi)    3.141592653…        3         TRIAD

  CENTER = 0 (NULL): all radii originate here.

FIRST-DIGIT ARITHMETIC:
  Sum     : 1 + 2 + 3 = 6   DR = 6 (fixed point of DR)
  Product : 1 × 2 × 3 = 6   DR = 6
  (Sum = Product; 6 = DR(33) = DR(AHL+ALO) = DR(total doubling matrix))

EULER IDENTITY STRUCTURAL READING:
  e^(iπ) + 1 = 0
  COMPLEXITY radius (e) rotated by TRIAD radius (π) → −UNIT (−1)
  −UNIT + UNIT = 0 = NULL (center)

3+6+9 = 18 = GATE:
  3 = π first digit (TRIAD)
  6 = (e first digit) × (π first digit) = 2 × 3
  9 = NULL anchor (DR base)
  Sum = 18 = (37−1)/2 = CENTER of Z/37Z = fixed point of f(n)=(3n+1) mod 37

PRODUCT/POWER FIRST DIGITS (doubling cycle map):
  e × π  → 8.539…  first digit 8 = AHL  (step 4/6 in cycle 1→2→4→8→7→5)
  e²     → 7.389…  first digit 7 = ALO  (step 5/6)
  π²     → 9.869…  first digit 9 = NULL
  φ²     → 2.618…  first digit 2 = e's axiom; φ²=φ+1 (UNIT self-referential)
  φ×e    → 4.398…  first digit 4         (step 3/6)
  φ×π    → 5.083…  first digit 5         (step 6/6)
  φ^e    → 3.699…  first digit 3 = π's axiom

  The three constant products (e×π, e², π²) hit AHL, ALO, and NULL —
  the same triple that anchors the alpha_grid and doubling cycle.
  AHL × ALO = 8 × 7 = 56 → DR = 2 = e's axiom = blueprint DR.

12-DECIMAL DR COLLAPSE:
  φ: .618033988749  digit-sum = 66  DR = 3 = π's axiom
  e: .718281828459  digit-sum = 63  DR = 9 = NULL
  π: .141592653589  digit-sum = 58  DR = 4

  Sum of 12-decimal DRs: 3 + 9 + 4 = 16  →  DR = 7 = ALO

FIBONACCI AND φ:
  F(n+1)/F(n) → φ as n → ∞
  F(9) = 34 = 2×17 = digit_sum(582739) = digit_sum(937285)
  (the shared digit sum from division_582739_937285_audit.py)
─────────────────────────────────────────────────────────────────
"""

import math
import cmath

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = abs(n) % 9
    return r if r else 9


def first_digit(x):
    x = abs(x)
    if x == 0:
        return 0
    d = math.floor(math.log10(x))
    return int(x / 10 ** d)


def decimal_dr(x, n_digits):
    s = f"{x:.{n_digits + 5}f}".split(".")[1][:n_digits]
    total = sum(int(c) for c in s)
    while total >= 10:
        total = sum(int(c) for c in str(total))
    return total


def decimal_digit_sum(x, n_digits):
    s = f"{x:.{n_digits + 5}f}".split(".")[1][:n_digits]
    return sum(int(c) for c in s)


PHI = (1 + math.sqrt(5)) / 2
E   = math.e
PI  = math.pi


# ── Three constants, three first digits ───────────────────────────────────────

check(first_digit(PHI) == 1, "first_digit(φ) = 1 (UNIT)",       first_digit(PHI), 1)
check(first_digit(E)   == 2, "first_digit(e) = 2 (COMPLEXITY)", first_digit(E),   2)
check(first_digit(PI)  == 3, "first_digit(π) = 3 (TRIAD)",      first_digit(PI),  3)

AXIOM_DIGITS = [first_digit(PHI), first_digit(E), first_digit(PI)]  # [1, 2, 3]


# ── First-digit arithmetic ────────────────────────────────────────────────────

FD_SUM = sum(AXIOM_DIGITS)
FD_PROD = AXIOM_DIGITS[0] * AXIOM_DIGITS[1] * AXIOM_DIGITS[2]

check(FD_SUM == 6,  "1+2+3 = 6",       FD_SUM,  6)
check(FD_PROD == 6, "1×2×3 = 6",       FD_PROD, 6)
check(FD_SUM == FD_PROD, "sum = product = 6", FD_SUM, FD_PROD)
check(dr(FD_SUM) == 6, "DR(6) = 6 (fixed point)", dr(FD_SUM), 6)

# 6 ties to framework: DR(33) = DR(AHL+ALO) = DR(total doubling matrix)
check(dr(33) == 6,  "DR(33) = 6",  dr(33), 6)
check(dr(8 + 7) == 6, "DR(AHL+ALO) = DR(15) = 6", dr(8 + 7), 6)
check(dr(114) == 6, "DR(114 = total doubling matrix) = 6", dr(114), 6)


# ── Euler identity ────────────────────────────────────────────────────────────

euler = cmath.exp(1j * PI) + 1
check(abs(euler) < 1e-14, "e^(iπ)+1 = 0 (machine zero)", abs(euler) < 1e-14, True)

# Structural: e(2) rotated by π(3) → −φ(−1) + φ(1) = 0
check(AXIOM_DIGITS[1] == 2, "e axiom = 2 (COMPLEXITY)", AXIOM_DIGITS[1], 2)
check(AXIOM_DIGITS[2] == 3, "π axiom = 3 (TRIAD)",      AXIOM_DIGITS[2], 3)
check(AXIOM_DIGITS[0] == 1, "φ axiom = 1 (UNIT)",       AXIOM_DIGITS[0], 1)
# e^(iπ) = −1 = −UNIT; + UNIT = 0 = NULL
check(abs(cmath.exp(1j * PI) - (-1)) < 1e-14, "e^(iπ) = −1 = −UNIT",
      abs(cmath.exp(1j * PI) + 1) < 1e-14, True)


# ── 3+6+9 = 18 = GATE ────────────────────────────────────────────────────────

PI_DIGIT   = first_digit(PI)       # 3 = TRIAD
EPI_DIGIT  = first_digit(E) * first_digit(PI)  # 2 × 3 = 6
NULL_DIGIT = 9

check(PI_DIGIT == 3,  "π first digit = 3", PI_DIGIT, 3)
check(EPI_DIGIT == 6, "e_digit × π_digit = 2×3 = 6", EPI_DIGIT, 6)
check(NULL_DIGIT == 9, "NULL anchor = 9", NULL_DIGIT, 9)

GATE_SUM = PI_DIGIT + EPI_DIGIT + NULL_DIGIT
check(GATE_SUM == 18, "3+6+9 = 18", GATE_SUM, 18)
check((37 - 1) // 2 == 18, "(37−1)/2 = 18 = CENTER of Z/37Z", (37 - 1) // 2, 18)
check(dr(18) == 9, "DR(18) = 9", dr(18), 9)

# 18 is the fixed point of f(n)=(3n+1) mod 37 and g(n)=(2n+19) mod 37
check((3 * 18 + 1) % 37 == 18, "f(18) = (3×18+1) mod 37 = 18", (3 * 18 + 1) % 37, 18)
check((2 * 18 + 19) % 37 == 18, "g(18) = (2×18+19) mod 37 = 18", (2 * 18 + 19) % 37, 18)

# Ψ(19,23,29) ≡ 18 mod 37 (from psi_operator_audit)
check(55 % 37 == 18, "Ψ(19,23,29) = 55 ≡ 18 mod 37 (CENTER)", 55 % 37, 18)


# ── Product/power first digits: DR doubling cycle map ────────────────────────

DR_CYCLE = [1, 2, 4, 8, 7, 5]   # period-6 DR doubling cycle

# e × π → 8 = AHL (step 4/6 in cycle)
check(first_digit(E * PI) == 8, "first_digit(e×π) = 8 = AHL", first_digit(E * PI), 8)
check(DR_CYCLE.index(8) == 3, "8 is step 4/6 in doubling cycle (0-indexed 3)", DR_CYCLE.index(8), 3)

# e² → 7 = ALO (step 5/6)
check(first_digit(E ** 2) == 7, "first_digit(e²) = 7 = ALO", first_digit(E ** 2), 7)
check(DR_CYCLE.index(7) == 4, "7 is step 5/6 in doubling cycle (0-indexed 4)", DR_CYCLE.index(7), 4)

# π² → 9 = NULL
check(first_digit(PI ** 2) == 9, "first_digit(π²) = 9 = NULL", first_digit(PI ** 2), 9)
check(dr(9) == 9, "DR(9) = 9 (NULL anchor)", dr(9), 9)

# φ² = φ+1 (golden ratio identity) → first digit 2 = e's axiom
check(abs(PHI ** 2 - (PHI + 1)) < 1e-10, "φ² = φ+1 (golden ratio identity)",
      abs(PHI ** 2 - (PHI + 1)) < 1e-10, True)
check(first_digit(PHI ** 2) == 2, "first_digit(φ²) = 2 = e's axiom", first_digit(PHI ** 2), 2)

# φ×e → 4 (step 3/6), φ×π → 5 (step 6/6)
check(first_digit(PHI * E) == 4, "first_digit(φ×e) = 4 (step 3/6)", first_digit(PHI * E), 4)
check(first_digit(PHI * PI) == 5, "first_digit(φ×π) = 5 (step 6/6)", first_digit(PHI * PI), 5)
check(DR_CYCLE.index(4) == 2, "4 is step 3/6", DR_CYCLE.index(4), 2)
check(DR_CYCLE.index(5) == 5, "5 is step 6/6", DR_CYCLE.index(5), 5)

# φ^e → 3 = π's axiom
check(first_digit(PHI ** E) == 3, "first_digit(φ^e) = 3 = π's axiom", first_digit(PHI ** E), 3)

# AHL × ALO = 56 → DR = 2 = e's axiom = blueprint DR
check(dr(8 * 7) == 2, "DR(AHL×ALO) = DR(56) = 2 = e's axiom", dr(8 * 7), 2)


# ── Products e×π, e², π² cover AHL, ALO, NULL — the alpha_grid anchor triple ─

AHL_ALO_NULL = {first_digit(E * PI), first_digit(E ** 2), first_digit(PI ** 2)}
check(AHL_ALO_NULL == {8, 7, 9}, "{e×π, e², π²} first digits = {AHL, ALO, NULL}",
      AHL_ALO_NULL, {8, 7, 9})


# ── 12-decimal DR collapse ────────────────────────────────────────────────────

DEC_DS_PHI = decimal_digit_sum(PHI, 12)   # 66
DEC_DS_E   = decimal_digit_sum(E, 12)     # 63
DEC_DS_PI  = decimal_digit_sum(PI, 12)    # 58

DEC_DR_PHI = decimal_dr(PHI, 12)   # 3
DEC_DR_E   = decimal_dr(E, 12)     # 9
DEC_DR_PI  = decimal_dr(PI, 12)    # 4

check(DEC_DS_PHI == 66, "decimal_digit_sum(φ, 12) = 66", DEC_DS_PHI, 66)
check(DEC_DS_E   == 63, "decimal_digit_sum(e, 12) = 63", DEC_DS_E,   63)
check(DEC_DS_PI  == 58, "decimal_digit_sum(π, 12) = 58", DEC_DS_PI,  58)

check(DEC_DR_PHI == 3, "12-decimal DR(φ) = 3 = π's axiom", DEC_DR_PHI, 3)
check(DEC_DR_E   == 9, "12-decimal DR(e) = 9 = NULL",       DEC_DR_E,   9)
check(DEC_DR_PI  == 4, "12-decimal DR(π) = 4",              DEC_DR_PI,  4)

DEC_DR_SUM = DEC_DR_PHI + DEC_DR_E + DEC_DR_PI
check(DEC_DR_SUM == 16, "3+9+4 = 16", DEC_DR_SUM, 16)
check(dr(DEC_DR_SUM) == 7, "DR(16) = 7 = ALO", dr(DEC_DR_SUM), 7)


# ── Fibonacci convergence to φ ────────────────────────────────────────────────

def fibonacci(n):
    fibs = [1, 1]
    while len(fibs) < n:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

FIBS = fibonacci(20)

# F(n+1)/F(n) → φ
for i in range(9, 15):
    ratio = FIBS[i] / FIBS[i - 1]
    check(abs(ratio - PHI) < 0.01,
          f"F({i+1})/F({i}) close to φ", abs(ratio - PHI) < 0.01, True)

# F(9) = 34 = 2×17 = digit_sum(582739) = digit_sum(937285)
check(FIBS[8] == 34, "F(9) = 34", FIBS[8], 34)
check(34 == 2 * 17, "34 = 2×17", 34, 2 * 17)
# digit_sum(582739) = 5+8+2+7+3+9 = 34; digit_sum(937285) = 9+3+7+2+8+5 = 34
check(sum(int(c) for c in "582739") == 34, "digit_sum(582739) = F(9) = 34",
      sum(int(c) for c in "582739"), 34)
check(sum(int(c) for c in "937285") == 34, "digit_sum(937285) = F(9) = 34",
      sum(int(c) for c in "937285"), 34)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Cascade Constants Audit: φ, e, π")
    print("=" * 62)

    print("\n── Three constants ──")
    for label, val, d, axiom in [
        ("φ", PHI, 1, "UNIT"),
        ("e", E,   2, "COMPLEXITY"),
        ("π", PI,  3, "TRIAD"),
    ]:
        print(f"  {label} = {val:.12f}  first_digit={d}  axiom={axiom}")

    print(f"\n── First-digit arithmetic ──")
    print(f"  1+2+3 = {FD_SUM}  1×2×3 = {FD_PROD}  sum=product=6  DR(6)=6 (fixed point)")
    print(f"  6 = DR(33) = DR(AHL+ALO) = DR(total doubling matrix = 114)")

    print(f"\n── Euler identity ──")
    print(f"  |e^(iπ)+1| = {abs(euler):.2e}  (machine zero)")
    print(f"  e(COMPLEXITY=2) rotated by π(TRIAD=3) → −1 = −φ(UNIT=1)")
    print(f"  −1 + 1 = 0 = NULL  (center)")

    print(f"\n── 3+6+9 = 18 = GATE ──")
    print(f"  3 = π first digit (TRIAD)")
    print(f"  6 = e_digit × π_digit = 2×3")
    print(f"  9 = NULL anchor")
    print(f"  3+6+9 = 18 = (37−1)/2 = CENTER of Z/37Z")
    print(f"  f(18) = (3×18+1) mod 37 = {(3*18+1)%37}  (GATE fixed point)")
    print(f"  Ψ(19,23,29) = 55 ≡ {55%37} mod 37 (prime triplet → CENTER)")

    print(f"\n── Product/power first digits → DR doubling cycle ──")
    print(f"  {'Expression':>10}  {'Value':>12}  {'First digit':>12}  {'Meaning'}")
    for expr, val, fd, meaning in [
        ("e×π",   E*PI,    first_digit(E*PI),   "8 = AHL  (step 4/6)"),
        ("e²",    E**2,    first_digit(E**2),   "7 = ALO  (step 5/6)"),
        ("π²",    PI**2,   first_digit(PI**2),  "9 = NULL"),
        ("φ²",    PHI**2,  first_digit(PHI**2), "2 = e's axiom (φ²=φ+1)"),
        ("φ×e",   PHI*E,   first_digit(PHI*E),  "4  (step 3/6)"),
        ("φ×π",   PHI*PI,  first_digit(PHI*PI), "5  (step 6/6)"),
        ("φ^e",   PHI**E,  first_digit(PHI**E), "3 = π's axiom"),
    ]:
        print(f"  {expr:>10}  {val:>12.6f}  {fd:>12}  {meaning}")
    print(f"  DR(AHL×ALO) = DR(8×7) = DR(56) = 2 = e's axiom = blueprint DR")

    print(f"\n── 12-decimal DR collapse ──")
    phi_s = f"{PHI:.15f}".split(".")[1][:12]
    e_s   = f"{E:.15f}".split(".")[1][:12]
    pi_s  = f"{PI:.15f}".split(".")[1][:12]
    print(f"  φ: .{phi_s}  digit-sum={DEC_DS_PHI}  DR={DEC_DR_PHI}  (= π's axiom)")
    print(f"  e: .{e_s}  digit-sum={DEC_DS_E}  DR={DEC_DR_E}  (= NULL)")
    print(f"  π: .{pi_s}  digit-sum={DEC_DS_PI}  DR={DEC_DR_PI}")
    print(f"  Sum of DRs: {DEC_DR_PHI}+{DEC_DR_E}+{DEC_DR_PI} = {DEC_DR_SUM}  →  DR={dr(DEC_DR_SUM)} = ALO")

    print(f"\n── Fibonacci → φ ──")
    print(f"  F(9) = {FIBS[8]} = 2×17 = digit_sum(582739) = digit_sum(937285)")
    print(f"  The shared digit sum from division_582739_937285_audit")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
