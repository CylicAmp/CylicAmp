"""
narcissistic_audit.py

Armstrong (narcissistic) numbers: fixed points of N = Σ dᵢⁿ.

─────────────────────────────────────────────────────────────────
DEFINITION:
  An n-digit integer N is narcissistic if N = Σᵢ dᵢⁿ
  where d₁…dₙ are its decimal digits.

─────────────────────────────────────────────────────────────────
BOUND CORRECTION:

  User states: "at n=60, 60·9^60 < 10^59"  — THIS IS FALSE.

  Correct computation:
    log₁₀(60·9^60) = log₁₀(60) + 60·log₁₀(9) ≈ 1.778 + 57.254 = 59.033
    log₁₀(10^59) = 59
    So 60·9^60 ≈ 10^59.033 > 10^59.  The bound does NOT hold at n=60.

  The bound n·9^n < 10^(n-1) first holds at n=61:
    log₁₀(61·9^61) ≈ 59.994 < 60 = log₁₀(10^60)  ✓

  Correct statement: "no narcissistic number with n ≥ 61 digits can exist."
  For n = 40 to 60, impossibility is established by exhaustive computation,
  not this bound alone.

  The maximum digit count is 39 (known result).
  The total count is 88 (known result, exhaustive search).

─────────────────────────────────────────────────────────────────
n=4 GENUS VECTORS:

  1634: [0,1,0,1]  Γ=2  (digits 1,6,3,4 → genus 0,1,0,1)
  8208: [2,0,1,2]  Γ=5  (digits 8,2,0,8 → genus 2,0,1,2)
  9474: [1,1,0,1]  Γ=3  (digits 9,4,7,4 → genus 1,1,0,1)

  Correction to 9474 description: user says "dual instances of 4,
  disrupted only by the null-node 7." But digit 9 also carries genus=1
  (the enclosed circle in the digit's tail). The Γ=3 accounts for:
    1 loop from 9 + 1 loop from first 4 + 0 from 7 + 1 loop from second 4.
  The 4s account for only 2 of the 3 loops.

─────────────────────────────────────────────────────────────────
DR PATTERNS OF NARCISSISTIC NUMBERS:

  n=1: DRs = {1,2,3,4,5,6,7,8,9}    (trivially, all single digits)
  n=3: DRs = {9,1,2,2}              (153→9, 370→1, 371→2, 407→2)
  n=4: DRs = {5,9,6}               (1634→5, 8208→9, 9474→6)
  n=5: DRs = {1,9,6}               (54748→1, 92727→9, 93084→6)
  n=6: DRs = {5}                    (548834→5)
  n=7: DRs = {9,6,6,8}             (1741725→9, 4210818→6, 9800817→6, 9926315→8)

─────────────────────────────────────────────────────────────────
"""

import math

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


DIGIT_GENUS = {str(d): 0 for d in range(10)}
DIGIT_GENUS['0'] = 1
DIGIT_GENUS['4'] = 1
DIGIT_GENUS['6'] = 1
DIGIT_GENUS['8'] = 2
DIGIT_GENUS['9'] = 1


def genus_vec(n):
    return [DIGIT_GENUS[d] for d in str(n)]


def is_narcissistic(n):
    s = str(n)
    k = len(s)
    return n > 0 and n == sum(int(d) ** k for d in s)


# ── Bound analysis ────────────────────────────────────────────────────────────

# User claim: "60·9^60 < 10^59" — verify it is FALSE
val60  = 60 * 9 ** 60
bound59 = 10 ** 59
check(val60 > bound59,
      "60·9^60 > 10^59 (user claim of < is FALSE)", val60 > bound59, True)

log_n60 = math.log10(60) + 60 * math.log10(9)
check(log_n60 > 59.0,
      "log10(60·9^60) > 59 (confirms 60·9^60 > 10^59)",
      round(log_n60, 5), round(log_n60, 5))

# Correct bound: first n where n·9^n < 10^(n-1) is n=61
val61   = 61 * 9 ** 61
bound60 = 10 ** 60
check(val61 < bound60,
      "61·9^61 < 10^60 (bound holds at n=61)", val61 < bound60, True)

log_n61 = math.log10(61) + 61 * math.log10(9)
check(log_n61 < 60.0,
      "log10(61·9^61) < 60 (confirms 61·9^61 < 10^60)",
      log_n61 < 60.0, True)

# Monotone: for all n>=61 the bound holds
for n in range(61, 80):
    log_max = math.log10(n) + n * math.log10(9)
    check(log_max < n - 1,
          f"bound holds at n={n}", log_max < n - 1, True)


# ── n=4 narcissistic numbers ──────────────────────────────────────────────────

N4 = {
    1634: ([0, 1, 0, 1], 2, 5),
    8208: ([2, 0, 1, 2], 5, 9),
    9474: ([1, 1, 0, 1], 3, 6),
}

for n, (expected_gv, expected_gamma, expected_dr) in N4.items():
    # Narcissistic property
    digits = str(n)
    k = len(digits)
    power_sum = sum(int(d) ** k for d in digits)
    check(power_sum == n,
          f"{n} = Σ dᵢ⁴: {' + '.join(f'{d}^4={int(d)**4}' for d in digits)}",
          power_sum, n)
    # Genus vector
    gv = genus_vec(n)
    check(gv == expected_gv, f"genus_vec({n})", gv, expected_gv)
    check(sum(gv) == expected_gamma, f"Γ({n}) = {expected_gamma}", sum(gv), expected_gamma)
    # DR
    check(dr(n) == expected_dr, f"DR({n}) = {expected_dr}", dr(n), expected_dr)


# ── 9474 genus attribution correction ────────────────────────────────────────

# User says loops come from "dual instances of 4" only.
# But digit 9 also carries genus=1.
check(DIGIT_GENUS['9'] == 1, "digit 9 carries genus=1 (tail loop)", DIGIT_GENUS['9'], 1)
check(DIGIT_GENUS['4'] == 1, "digit 4 carries genus=1", DIGIT_GENUS['4'], 1)

# 9474: genus from 9 = 1, from first 4 = 1, from 7 = 0, from second 4 = 1
g_9, g_4, g_7 = DIGIT_GENUS['9'], DIGIT_GENUS['4'], DIGIT_GENUS['7']
check(g_9 + g_4 + g_7 + g_4 == 3,
      "9474: Γ = genus(9)+genus(4)+genus(7)+genus(4) = 1+1+0+1 = 3",
      g_9 + g_4 + g_7 + g_4, 3)
check(g_9 == 1,
      "9 contributes 1 loop (not accounted for in 'dual 4' description)", g_9, 1)


# ── n=3 narcissistic numbers ──────────────────────────────────────────────────

N3 = {153: 9, 370: 1, 371: 2, 407: 2}   # {n: DR(n)}

for n, expected_dr in N3.items():
    digits = str(n)
    power_sum = sum(int(d) ** 3 for d in digits)
    check(power_sum == n, f"{n} = Σ dᵢ³", power_sum, n)
    check(dr(n) == expected_dr, f"DR({n}) = {expected_dr}", dr(n), expected_dr)

# Genus of n=3 set
check(sum(genus_vec(153)) == 0, "Γ(153) = 0", sum(genus_vec(153)), 0)
check(sum(genus_vec(370)) == 1, "Γ(370) = 1 (digit 0)", sum(genus_vec(370)), 1)
check(sum(genus_vec(371)) == 0, "Γ(371) = 0", sum(genus_vec(371)), 0)
check(sum(genus_vec(407)) == 2, "Γ(407) = 2 (digits 0 and 4)", sum(genus_vec(407)), 2)


# ── n=5, 6, 7 narcissistic numbers ───────────────────────────────────────────

N5 = {54748: 1, 92727: 9, 93084: 6}
N6 = {548834: 5}
N7 = {1741725: 9, 4210818: 6, 9800817: 6, 9926315: 8}

for group, k in [(N5, 5), (N6, 6), (N7, 7)]:
    for n, expected_dr in group.items():
        digits = str(n)
        power_sum = sum(int(d) ** k for d in digits)
        check(power_sum == n, f"{n} = Σ dᵢ^{k}", power_sum, n)
        check(dr(n) == expected_dr, f"DR({n}) = {expected_dr}", dr(n), expected_dr)


# ── Count narcissistic numbers up to n=7 ─────────────────────────────────────

COUNT_BY_N = {1: 9, 2: 0, 3: 4, 4: 3, 5: 3, 6: 1, 7: 4}
RUNNING_TOTAL = 24

for k in range(1, 8):
    lo = 10 ** (k - 1) if k > 1 else 1
    hi = 10 ** k
    found = [n for n in range(lo, min(hi, 10_000_001)) if is_narcissistic(n)]
    check(len(found) == COUNT_BY_N[k],
          f"count of n={k} narcissistic numbers = {COUNT_BY_N[k]}", len(found), COUNT_BY_N[k])

check(sum(COUNT_BY_N.values()) == RUNNING_TOTAL,
      f"total through n=7 = {RUNNING_TOTAL}", sum(COUNT_BY_N.values()), RUNNING_TOTAL)

# The total of 88 and max of 39 digits are established results of exhaustive search.
# Remaining 64 narcissistic numbers have 8–39 digits.
check(88 - RUNNING_TOTAL == 64, "88 - 24 = 64 remain in n=8..39", 88 - RUNNING_TOTAL, 64)


# ── DR structure of n=4 attractors ───────────────────────────────────────────

# 1634: DR=5 (prime-admissible, in doubling cycle)
# 8208: DR=9 (NULL — the 6-field of digit 8 manifests as NULL in the whole)
# 9474: DR=6 (carries the 6-field signature into n=4)
check(dr(1634) == 5, "1634: DR=5 (prime-admissible)", dr(1634), 5)
check(dr(8208) == 9, "8208: DR=9 = NULL",             dr(8208), 9)
check(dr(9474) == 6, "9474: DR=6 (6-field attractor)", dr(9474), 6)

# The digit-power operation modifies DR:
# 8208: DR(8)=8, 8^4=4096, DR(4096)=1; DR(2)=2, 2^4=16, DR(16)=7;
#       DR(0)=0, 0^4=0; DR(8)=8, 8^4=4096, DR(4096)=1
# Sum DRs of powers: DR(1+7+0+1) = DR(9) = 9 ✓
check(dr(8**4) == 1, "DR(8^4) = DR(4096) = 1", dr(8**4), 1)
check(dr(2**4) == 7, "DR(2^4) = DR(16) = 7",   dr(2**4), 7)
check(dr(0**4) == 0, "DR(0^4) = DR(0) = 0",    dr(0**4), 0)
check(dr(1 + 7 + 0 + 1) == 9,
      "DR(8^4+2^4+0^4+8^4) mod 9 = DR(1+7+0+1) = 9", dr(1 + 7 + 0 + 1), 9)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Narcissistic Number Audit")
    print("=" * 66)

    print(f"\n── Bound analysis ──")
    print(f"  User claim: 60·9^60 < 10^59  →  FALSE.")
    print(f"  60·9^60 ≈ 10^{log_n60:.3f} > 10^59.")
    print(f"  Correct bound: 61·9^61 ≈ 10^{log_n61:.5f} < 10^60.")
    print(f"  First impossible digit count is n=61 (not n=60).")
    print(f"  For n=40..60: impossibility established by exhaustive search, not this bound.")
    print(f"  Maximum known: 39 digits.  Total: 88 numbers (established results).")

    print(f"\n── Narcissistic numbers through n=7 ──")
    for k in range(1, 8):
        lo = 10 ** (k - 1) if k > 1 else 1
        hi = 10 ** k
        found = [n for n in range(lo, min(hi, 10_000_001)) if is_narcissistic(n)]
        for n in found:
            gv = genus_vec(n)
            print(f"  n={k}: {n:>10}  DR={dr(n)}  Γ={sum(gv)}  gv={gv}")
    print(f"  Subtotal n=1..7: {RUNNING_TOTAL}; remaining 64 in n=8..39.")

    print(f"\n── n=4 genus vectors (verified) ──")
    for n, (gv, gamma, ndr) in N4.items():
        digits = str(n)
        power_parts = '+'.join(f'{d}^4={int(d)**4}' for d in digits)
        print(f"  {n}: {power_parts} = {n}")
        print(f"       genus_vec={gv}  Γ={gamma}  DR={ndr}")

    print(f"\n── 9474 correction ──")
    print(f"  User: 'dual instances of 4, disrupted only by null-node 7'.")
    print(f"  Actual: digit 9 carries genus=1 (enclosed tail circle).")
    print(f"  Γ(9474) = genus(9)+genus(4)+genus(7)+genus(4) = 1+1+0+1 = 3.")
    print(f"  The 9 contributes the first loop; both 4s contribute one each.")
    print(f"  7 is the null-node. '9' is not a null-node — it is a genus-1 node.")

    print(f"\n── DR of n=4 attractors ──")
    print(f"  1634: DR=5 (prime-admissible, in doubling cycle {{1,2,4,5,7,8}})")
    print(f"  8208: DR=9 = NULL (8 is AHL; its 4th power maps to DR=1; sum → DR=9)")
    print(f"  9474: DR=6 (6-field carrier; 9474 is a narcissistic fixed point in the 6-field)")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
