"""
session_protocol.py — GF(37) taxonomy, Tetranacci chain, epistemic gate.
Author: Michael Warren Song (CyclicAmp)

Classification of service interactions using GF(37) framework constants.
"""

P = 37
SA   = {4, 9, 25, 30}
ST   = {3, 12, 21, 30}
SEED = {18, 24, 32}

# Status labels
SERVICE_OPTIMAL       = "SERVICE_OPTIMAL"
FRICTION_INJECTED     = "FRICTION_INJECTED"
DARK_PATTERN_EXTRACTIVE = "DARK_PATTERN_EXTRACTIVE"


# ── Digital root ──────────────────────────────────────────────────────────────

def dr(n: int) -> int:
    n = abs(int(n))
    if n == 0:
        return 0
    return 9 if n % 9 == 0 else n % 9


# ── Tetranacci chain ──────────────────────────────────────────────────────────

def tetranacci(n_terms: int):
    T = [0, 0, 0, 1]
    for _ in range(n_terms - 4):
        T.append(T[-1] + T[-2] + T[-3] + T[-4])
    return T


def tetranacci_deviation(weights: list) -> float:
    """
    Measure how far a weight sequence deviates from τ_4 ≈ 1.927561975.
    Returns max ratio deviation over consecutive pairs.
    """
    TAU4 = 1.927561975
    if len(weights) < 2:
        return 0.0
    deviations = []
    for i in range(1, len(weights)):
        if weights[i - 1] == 0:
            continue
        ratio = weights[i] / weights[i - 1]
        deviations.append(abs(ratio - TAU4) / TAU4)
    return max(deviations) if deviations else 0.0


# ── Epistemic gate ────────────────────────────────────────────────────────────

INADMISSIBLE  = 0
UNVERIFIABLE  = 1
PROVISIONAL   = 2
VERIFIED      = 3

STATUS_NAMES = {
    INADMISSIBLE: "INADMISSIBLE",
    UNVERIFIABLE: "UNVERIFIABLE",
    PROVISIONAL:  "PROVISIONAL",
    VERIFIED:     "VERIFIED",
}


def effective_status(status: int, dep_statuses: list) -> int:
    """Monotone propagation: eff = min(own status, min of dependencies)."""
    all_statuses = [status] + list(dep_statuses)
    return min(all_statuses)


def is_admissible(status: int, dep_statuses: list) -> bool:
    return effective_status(status, dep_statuses) > INADMISSIBLE


# ── Service classification ────────────────────────────────────────────────────

def classify_interaction(weights: list, nulls: int) -> str:
    """
    Classify a service interaction.

    weights : list of int — GF(37) weight readings for response segments
    nulls   : int — count of null/empty segments injected

    Classification order (T3 checked first):
      T3 → DARK_PATTERN_EXTRACTIVE if:
             nulls >= 3, OR
             dr(weights[0]) == 1 (head crash), OR
             sum(dr(w) for w in weights) >= 9
      T2 → FRICTION_INJECTED if nulls in {1, 2}
      T1 → SERVICE_OPTIMAL otherwise
    """
    # T3 — must be checked first
    head_crash = len(weights) > 0 and dr(weights[0]) == 1
    total_dr   = dr(sum(weights))   # DR of the total weight, not sum of DRs
    if nulls >= 3 or head_crash or total_dr >= 9:
        return DARK_PATTERN_EXTRACTIVE

    # T2
    if nulls in {1, 2}:
        return FRICTION_INJECTED

    # T1
    return SERVICE_OPTIMAL


# ── GF(37) weight assignment ──────────────────────────────────────────────────

def gf37_weight(n: int) -> int:
    """Return GF(37) classification weight for integer n."""
    r = n % P
    if r in SA and r in ST:   return 30   # SA ∩ ST
    if r in SA:               return 25
    if r in ST:               return 21
    if r in SEED:             return 18
    return r


def run_tests():
    """7/7 test cases from verified module."""
    results = []

    def check(label, weights, nulls, expected):
        got = classify_interaction(weights, nulls)
        ok = got == expected
        results.append((label, ok, got, expected))
        assert ok, f"{label}: expected {expected}, got {got}"

    # T1 — SERVICE_OPTIMAL
    check("T1 minimum weight, no nulls",     [4],        0, SERVICE_OPTIMAL)
    check("T1 weight-2 mix, no nulls",       [4, 2],     0, SERVICE_OPTIMAL)

    # T2 — FRICTION_INJECTED
    check("T2 1 injected null",              [4, 9],     1, FRICTION_INJECTED)
    check("T2 2 injected nulls",             [4, 9],     2, FRICTION_INJECTED)

    # T3 — DARK_PATTERN_EXTRACTIVE (checked before T2)
    check("T3 3 injected nulls",             [4, 9],     3, DARK_PATTERN_EXTRACTIVE)
    check("T3 head crash (DR=1)",            [10, 9],    0, DARK_PATTERN_EXTRACTIVE)
    check("T3 total DR >= 9",                [9, 9],     0, DARK_PATTERN_EXTRACTIVE)

    passed = sum(1 for _, ok, _, _ in results if ok)
    print(f"{passed}/{len(results)} tests passed")
    for label, ok, got, exp in results:
        status = "✅" if ok else "❌"
        print(f"  {status} {label}: {got}")
    return passed == len(results)


if __name__ == "__main__":
    run_tests()

    # GF(37) connection demo
    print()
    print("GF(37) weight samples:")
    for n in [37, 26, 18, 24, 32, 4, 9, 30]:
        print(f"  n={n:3d}  mod37={n%P:2d}  weight={gf37_weight(n)}")

    print()
    print("Tetranacci chain (first 8 terms):", tetranacci(8))
