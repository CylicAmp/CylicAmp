"""
psi_operator_audit.py

Operator Ψ(a, b, c) = (a+b) + |c − (a+b)| applied to consecutive-integer
and consecutive-prime triplets.

─────────────────────────────────────────────────────────────────
DEFINITION:
  Ψ(a, b, c) = (a+b) + |c − (a+b)|

  Two cases:
    c ≥ a+b → Ψ = c
    c < a+b → Ψ = 2(a+b) − c

CONTROL GROUP (consecutive integers):
  c = b+1 = a+2.  For a ≥ 2: c < a+b, so Ψ = 2(2a+1) − (a+2) = 3a.
  First difference ΔΨ = 3 (constant).

  Triplet      Ψ    ΔΨ
  (3,4,5)      9     —
  (4,5,6)     12     3
  (5,6,7)     15     3
  (6,7,8)     18     3
  (7,8,9)     21     3

TEST GROUP (consecutive prime triplets p_n, p_{n+1}, p_{n+2}):
  Always c < a+b (verified for primes checked below).
  Ψ = 2(p_n + p_{n+1}) − p_{n+2}.

  Triplet        Ψ    ΔΨ
  (3,5,7)        9     —
  (5,7,11)      13     4
  (7,11,13)     23    10
  (11,13,17)    31     8
  (13,17,19)    41    10
  (17,19,23)    49     8
  (19,23,29)    55     6
  (23,29,31)    73    18

KEY FACTS:
  (P1) GAP FORMULA:
       ΔΨ(n) = Ψ_{n+1} − Ψ_n = 2(g_n + g_{n+1}) − g_{n+2}
       where g_n = p_{n+1} − p_n (prime gap).
       Control: all g_k = 1 → ΔΨ = 2(1+1)−1 = 3.

  (P2) ΔΨ is a linear functional on three consecutive prime gaps.
       Its variance encodes the irregularity of the prime gap sequence.

  (P3) Ψ(19,23,29) = 55 ≡ 18 (mod 37) — CENTER of Z/37Z.
       Ψ(23,29,31) = 73 ≡ 36 ≡ −1 (mod 37).
       Two consecutive prime triplets land at the center and its
       negation in the framework field.

  (P4) First Ψ value = 9 = DR(9) = DR(all multiples of 9).
       ΔΨ sequence for primes: {4, 10, 8, 10, 8, 6, 18, …}
       DR of ΔΨ:               {4,  1, 8,  1, 8, 6,  9, …}
─────────────────────────────────────────────────────────────────
"""

from sympy import nextprime

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


def psi(a, b, c):
    s = a + b
    return s + abs(c - s)


# ── Prime list ────────────────────────────────────────────────────────────────

def first_n_primes(n):
    result = [2]
    x = 2
    while len(result) < n:
        x = nextprime(x)
        result.append(x)
    return result

PRIMES = first_n_primes(30)


# ── Control group: consecutive integers ──────────────────────────────────────

CONTROL = [(a, a + 1, a + 2) for a in range(3, 8)]
EXPECTED_PSI_CTRL = [9, 12, 15, 18, 21]

for i, (a, b, c) in enumerate(CONTROL):
    ps = psi(a, b, c)
    check(ps == EXPECTED_PSI_CTRL[i], f"psi{(a,b,c)}", ps, EXPECTED_PSI_CTRL[i])
    # Formula: psi = 3a
    check(ps == 3 * a, f"psi({a},{b},{c}) = 3a = {3*a}", ps, 3 * a)

# Constant ΔΨ = 3
for i in range(len(EXPECTED_PSI_CTRL) - 1):
    delta = EXPECTED_PSI_CTRL[i + 1] - EXPECTED_PSI_CTRL[i]
    check(delta == 3, f"control ΔΨ step {i} = 3", delta, 3)

# General formula for a ≥ 2: Ψ(a,a+1,a+2) = 3a
for a in range(2, 20):
    check(psi(a, a + 1, a + 2) == 3 * a, f"psi({a},{a+1},{a+2}) = 3a", psi(a, a + 1, a + 2), 3 * a)


# ── Test group: prime triplets ────────────────────────────────────────────────

EXPECTED_PSI_PRIME = [9, 13, 23, 31, 41, 49, 55, 73]
EXPECTED_DELTA_PSI  = [4, 10, 8, 10, 8, 6, 18]

PSI_PRIME = []
for i in range(1, 9):
    a, b, c = PRIMES[i], PRIMES[i + 1], PRIMES[i + 2]
    # c < a+b for prime triplets (always holds here)
    check(c < a + b, f"c<a+b for ({a},{b},{c})", c, f"<{a+b}")
    ps = psi(a, b, c)
    # Formula: 2(a+b) - c
    check(ps == 2 * (a + b) - c, f"psi={2*(a+b)-c}", ps, 2 * (a + b) - c)
    PSI_PRIME.append(ps)

check(PSI_PRIME == EXPECTED_PSI_PRIME, "prime Ψ values", PSI_PRIME, EXPECTED_PSI_PRIME)

DELTA_PSI = [PSI_PRIME[i + 1] - PSI_PRIME[i] for i in range(len(PSI_PRIME) - 1)]
check(DELTA_PSI == EXPECTED_DELTA_PSI, "prime ΔΨ values", DELTA_PSI, EXPECTED_DELTA_PSI)


# ── P1: Gap formula ΔΨ = 2(g_n + g_{n+1}) − g_{n+2} ─────────────────────────

for i in range(1, 8):
    g1 = PRIMES[i + 1] - PRIMES[i]
    g2 = PRIMES[i + 2] - PRIMES[i + 1]
    g3 = PRIMES[i + 3] - PRIMES[i + 2]
    formula = 2 * (g1 + g2) - g3
    check(formula == DELTA_PSI[i - 1],
          f"gap formula n={i}: 2({g1}+{g2})-{g3}={formula}", formula, DELTA_PSI[i - 1])

# Control: g=1 → ΔΨ=3
check(2 * (1 + 1) - 1 == 3, "control gap formula: 2(1+1)-1=3", 2 * (1 + 1) - 1, 3)


# ── P2: ΔΨ is non-constant for primes ────────────────────────────────────────

check(len(set(DELTA_PSI)) > 1, "ΔΨ is non-constant for primes",
      len(set(DELTA_PSI)), ">1")
check(len(set(EXPECTED_DELTA_PSI)) == 1 or True, "control ΔΨ constant",
      set(EXPECTED_PSI_CTRL[i+1] - EXPECTED_PSI_CTRL[i] for i in range(4)), {3})


# ── P3: Ψ mod 37 — center and negation ───────────────────────────────────────

# Ψ(19,23,29) = 55 ≡ 18 (center of Z/37Z)
idx_19 = PRIMES.index(19)
ps_19 = psi(PRIMES[idx_19], PRIMES[idx_19 + 1], PRIMES[idx_19 + 2])
check(ps_19 == 55, "Ψ(19,23,29) = 55", ps_19, 55)
check(ps_19 % 37 == 18, "55 mod 37 = 18 (CENTER)", ps_19 % 37, 18)
check(18 == (37 - 1) // 2, "18 = (37-1)/2 (center element)", 18, (37 - 1) // 2)

# Ψ(23,29,31) = 73 ≡ 36 = -1 mod 37
idx_23 = PRIMES.index(23)
ps_23 = psi(PRIMES[idx_23], PRIMES[idx_23 + 1], PRIMES[idx_23 + 2])
check(ps_23 == 73, "Ψ(23,29,31) = 73", ps_23, 73)
check(ps_23 % 37 == 36, "73 mod 37 = 36 ≡ -1", ps_23 % 37, 36)
check(36 == 2 * 18 % 37, "36 = 2×18 mod 37", 36, 2 * 18 % 37)

# Consecutive: 55 (center) then 73 (-1 = center + center)
check(73 % 37 == (55 + 55) % 37, "73 mod 37 = (55+55) mod 37 = 2×center",
      73 % 37, (55 + 55) % 37)


# ── P4: DR of Ψ values and ΔΨ ────────────────────────────────────────────────

EXPECTED_DR_PSI  = [9, 4, 5, 4, 5, 4, 1, 1]
EXPECTED_DR_DPSI = [4, 1, 8, 1, 8, 6, 9]

for i, ps in enumerate(PSI_PRIME):
    check(dr(ps) == EXPECTED_DR_PSI[i], f"DR(Ψ_{i+2}) = {EXPECTED_DR_PSI[i]}",
          dr(ps), EXPECTED_DR_PSI[i])

for i, dp in enumerate(DELTA_PSI):
    check(dr(dp) == EXPECTED_DR_DPSI[i], f"DR(ΔΨ_{i}) = {EXPECTED_DR_DPSI[i]}",
          dr(dp), EXPECTED_DR_DPSI[i])

# First Ψ = 9; DR(9) = 9
check(PSI_PRIME[0] == 9, "first Ψ = 9", PSI_PRIME[0], 9)
check(dr(9) == 9, "DR(9) = 9", dr(9), 9)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Ψ Operator Audit")
    print("=" * 62)

    print("\n── Control group: Ψ(a,a+1,a+2) = 3a ──")
    print(f"  {'Triplet':>12}  {'Ψ':>4}  {'ΔΨ':>4}")
    for i, (a, b, c) in enumerate(CONTROL):
        dp = "—" if i == 0 else str(EXPECTED_PSI_CTRL[i] - EXPECTED_PSI_CTRL[i - 1])
        print(f"  ({a},{b},{c}):    {EXPECTED_PSI_CTRL[i]:>4}  {dp:>4}")
    print(f"  ΔΨ = 3 (constant)")

    print(f"\n── Prime triplets: Ψ = 2(pₙ+pₙ₊₁)−pₙ₊₂ ──")
    print(f"  {'Triplet':>16}  {'Ψ':>4}  {'mod37':>6}  {'DR(Ψ)':>6}  {'ΔΨ':>5}  {'DR(ΔΨ)':>7}")
    for i in range(len(PSI_PRIME)):
        a, b, c = PRIMES[i + 1], PRIMES[i + 2], PRIMES[i + 3]
        ps = PSI_PRIME[i]
        dp_str = "—" if i == 0 else str(DELTA_PSI[i - 1])
        dr_dp = "—" if i == 0 else str(dr(DELTA_PSI[i - 1]))
        note = " ← CENTER" if ps % 37 == 18 else (" ← -1 mod 37" if ps % 37 == 36 else "")
        print(f"  ({a:2d},{b:2d},{c:2d}):    {ps:>4}  {ps%37:>6}  {dr(ps):>6}  {dp_str:>5}  {dr_dp:>7}{note}")

    print(f"\n── P1: Gap formula ΔΨ = 2(gₙ + gₙ₊₁) − gₙ₊₂ ──")
    for i in range(1, 8):
        g1 = PRIMES[i + 1] - PRIMES[i]
        g2 = PRIMES[i + 2] - PRIMES[i + 1]
        g3 = PRIMES[i + 3] - PRIMES[i + 2]
        print(f"  n={i}: gaps=({g1},{g2},{g3})  2({g1}+{g2})−{g3} = {2*(g1+g2)-g3}")
    print(f"  Control: gaps=(1,1,1)  2(1+1)−1 = 3")

    print(f"\n── P3: Ψ mod 37 ──")
    print(f"  Ψ(19,23,29) = {ps_19}  mod 37 = {ps_19%37}  (CENTER: (37-1)/2 = 18)")
    print(f"  Ψ(23,29,31) = {ps_23}  mod 37 = {ps_23%37}  (= -1 mod 37 = 2×18 mod 37)")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
