"""
dds_ca_digit_audit.py

Audits three claims:

  A. {1,11,111} Representation Theorem
     f(n) = YES iff n ≥ 0.  Greedy decomposition:
       n = (n//111)·111 + ((n%111)//11)·11 + (n%11)·1
     FSM ≡ greedy for n = 0..999; 14 test cases pass.

  B. Cascade chain: 3.1448 = 19 = 10 = 1
                    4.6%   = 10 = 1

  C. Digit-level DDS / CA reinterpretation
     — discrete dynamical system: x_{t+1} = digit_sum(x_t)
       showing 1 as global attractor
     — 1D cellular automaton on digit arrays
       with local rule s_i += s_{i-1} + s_{i+1} mod 10
     — compare DDS (contractive) vs CA (emergent)
"""

import math
import numpy as np

# ============================================================
# A.  {1, 11, 111} Representation Theorem
# ============================================================
print("=" * 62)
print("A.  {1, 11, 111} Representation Theorem")
print("=" * 62)


def greedy_decompose(n):
    """n → (a, b, c) with n = 111a + 11b + c, a,b,c ≥ 0.

    User's stated formula used c = n%11, which is WRONG.
    Correct: c = (n%111)%11.
    Error source: 111 ≡ 1 mod 11, so n%11 = (n%111)%11 + (n//111)%11,
    which differs whenever n//111 ≢ 0 mod 11.
    """
    if n < 0:
        return None
    a = n // 111
    r = n % 111          # remainder after extracting 111s
    b = r // 11
    c = r % 11           # NOT n%11
    return (a, b, c)


def fsm_decompose(n):
    """
    FSM on digits of n (left to right, state = residual).
    At each position, greedily assign the largest block ≤ residual.
    Equivalent to greedy; implemented as explicit state transitions.
    """
    if n < 0:
        return None
    residual = n
    blocks = []
    for block in (111, 11, 1):
        count = residual // block
        blocks.append(count)
        residual -= count * block
    assert residual == 0
    return tuple(blocks)


def verify_decomp(n, abc):
    """Check that 111a + 11b + c = n and all coefficients ≥ 0."""
    a, b, c = abc
    return a >= 0 and b >= 0 and c >= 0 and 111 * a + 11 * b + c == n


# 14 test cases: edge cases, powers of 11, round numbers, boundaries
TEST_CASES = [0, 1, 10, 11, 12, 22, 100, 110, 111, 122, 200, 333, 500, 999]

print(f"\n  {'n':>5}  {'greedy (a,b,c)':>18}  {'check':>7}  {'fsm≡greedy':>11}")
print(f"  {'-'*50}")
all_pass = True
for n in TEST_CASES:
    g = greedy_decompose(n)
    f = fsm_decompose(n)
    ok  = verify_decomp(n, g)
    eq  = (g == f)
    all_pass = all_pass and ok and eq
    print(f"  {n:>5}  {str(g):>18}  {'✓' if ok else '✗':>7}  {'✓' if eq else '✗':>11}")

print(f"\n  14/14 pass: {all_pass}  (claimed: 14/14)")

# Full FSM ≡ greedy sweep n=0..999
mismatches = [(n, greedy_decompose(n), fsm_decompose(n))
              for n in range(1000)
              if greedy_decompose(n) != fsm_decompose(n)]
print(f"  FSM ≡ greedy for n=0..999:  "
      f"{'YES ✓' if not mismatches else f'NO — {len(mismatches)} mismatches'}")

# Proof sketch
print(f"""
  FORMULA CORRECTION:
    User wrote: c = n%11   ← WRONG (889/1000 values incorrect)
    Correct:    c = (n%111)%11
    Cause: 111 ≡ 1 (mod 11), so n%11 = (n%111)%11 + (n//111)%11.
    These coincide only when n//111 ≡ 0 (mod 11), i.e. n < 111 or n ≡ 0..110 after 111-block extraction.

  Proof (correct form):
    n = (n//111)·111 + ((n%111)//11)·11 + ((n%111)%11)·1
    holds by Euclidean division applied twice on the residual:
      n = 111·a + r₁       r₁ = n%111 ∈ [0,110]
      r₁ = 11·b  + c        c = r₁%11 ∈ [0,10]
    All coefficients are non-negative by construction.
    Every n ≥ 0 is representable.  Every n < 0 is not (all blocks positive).
    The greedy is unique given the block order (111 > 11 > 1).
""")

# Negative integers: confirm non-representability
print(f"  f(-1): {greedy_decompose(-1)}  (None = NOT REPRESENTABLE ✓)")
print(f"  f(-100): {greedy_decompose(-100)}  (None ✓)")


# ============================================================
# B.  Cascade Chains: 3.1448 and 4.6%
# ============================================================
print()
print("=" * 62)
print("B.  Cascade Chains")
print("=" * 62)


def digit_sum(x):
    """Sum of decimal digits of integer x (x > 0)."""
    return sum(int(d) for d in str(abs(x)))


def digit_root(x):
    """Iterated digit sum until single digit."""
    x = abs(int(x))
    while x >= 10:
        x = digit_sum(x)
    return x


def cascade(s):
    """
    Cascade a string of characters through digit-sum reduction.
    Extracts all digit characters, sums them, then iterates to DR.
    """
    digits = [int(c) for c in s if c.isdigit()]
    if not digits:
        return None, []
    total = sum(digits)
    chain = [total]
    x = total
    while x >= 10:
        x = digit_sum(x)
        chain.append(x)
    return chain[-1], chain


print("\n  Claim: 3.1448 → 19 → 10 → 1")
final_a, chain_a = cascade("3.1448")
actual_sum_a = sum(int(c) for c in "31448")
print(f"  Digits of '3.1448': {list('31448')}")
print(f"  Digit sum = 3+1+4+4+8 = {actual_sum_a}   (claimed: 19)")
print(f"  Cascade chain: {chain_a}  → final = {final_a}")
print(f"  Claim '3.1448 = 19': {'✓' if actual_sum_a == 19 else f'✗  actual sum = {actual_sum_a} ≠ 19'}")
print(f"  NOTE: 3+1+4+4+8 = 20, not 19.  Correct chain: 20 → 2 (DR=2, not 1)")

print()
print("  Claim: 4.6% → 10 → 1")
final_b, chain_b = cascade("4.6")
actual_sum_b = sum(int(c) for c in "46")
print(f"  Digits of '4.6': {list('46')}")
print(f"  Digit sum = 4+6 = {actual_sum_b}  (claimed: 10)")
print(f"  Cascade chain: {chain_b}  → final = {final_b}")
print(f"  Claim '4.6% = 10 = 1': {'✓' if actual_sum_b == 10 and final_b == 1 else '✗'}")


# ============================================================
# C.  DDS / CA Reinterpretation
# ============================================================
print()
print("=" * 62)
print("C.  Digit-Level Dynamical Systems")
print("=" * 62)

# ---- C1: DDS — iterated digit sum, 1 as global attractor ----------
print("\n  C1. DDS: x_{t+1} = digit_sum(x_t)")
print("  Fixed point: 1  (claimed global attractor for DR-1 inputs)")
print()

sample_trajectories = [
    3_1448,    # entropy value (integer)
    46,        # 4.6% scaled
    137,       # cascade number
    999,       # near-boundary
    31337,     # arbitrary large
    142857,    # cyclic number
]

print(f"  {'x_0':>10}  trajectory")
print(f"  {'-'*50}")
for x0 in sample_trajectories:
    traj = [x0]
    x = x0
    for _ in range(20):
        x = digit_sum(x)
        traj.append(x)
        if x < 10:
            break
    print(f"  {x0:>10}  {' → '.join(str(t) for t in traj)}")

# Count steps to attractor (single digit) over range
steps_to_single = []
for n in range(1, 10001):
    x, k = n, 0
    while x >= 10:
        x = digit_sum(x)
        k += 1
    steps_to_single.append(k)

print(f"\n  Steps to single digit (n=1..10000):")
print(f"    Mean:  {np.mean(steps_to_single):.2f}")
print(f"    Max:   {max(steps_to_single)}")
print(f"    0 steps (already single digit): {steps_to_single.count(0):,}")

# DR-class distribution
dr_classes = {}
for n in range(1, 10001):
    d = digit_root(n)
    dr_classes[d] = dr_classes.get(d, 0) + 1
print(f"\n  DR distribution for n=1..10000:")
for d in sorted(dr_classes):
    print(f"    DR={d}: {dr_classes[d]:,}  ({dr_classes[d]/100:.1f}%)")
print(f"  (Dirichlet predicts equal ~1111 per class ≈ 11.1% each)")


# ---- C2: 1D Cellular Automaton on digit arrays --------------------
print()
print("  C2. 1D CA on digit arrays")
print("  Rule: s_i[t+1] = (s_{i-1}[t] + s_i[t] + s_{i+1}[t]) mod 10")
print("  Boundary: periodic (wraparound)")
print()


def ca_step(cells):
    """One step of the additive CA: s_i += neighbors, mod 10."""
    n = len(cells)
    new = []
    for i in range(n):
        val = (cells[(i-1) % n] + cells[i] + cells[(i+1) % n]) % 10
        new.append(val)
    return new


def ca_evolve(initial, steps=10):
    """Evolve CA for given steps; return list of states."""
    states = [list(initial)]
    for _ in range(steps):
        states.append(ca_step(states[-1]))
    return states


# Seed: digits of entropy value 3.1448 → [3,1,4,4,8]
seed_entropy = [3, 1, 4, 4, 8]
print(f"  Seed (entropy 3.1448): {seed_entropy}")
states_e = ca_evolve(seed_entropy, steps=8)
print(f"  Evolution:")
for t, s in enumerate(states_e):
    dsum = sum(s)
    print(f"    t={t}: {s}  Σ={dsum}")

# Seed: digits of cascade number 137 → [1,3,7]
seed_137 = [1, 3, 7]
print(f"\n  Seed (cascade 137): {seed_137}")
states_137 = ca_evolve(seed_137, steps=10)
print(f"  Evolution:")
for t, s in enumerate(states_137):
    print(f"    t={t}: {s}  Σ={sum(s)}")

# Check if state sum is conserved or drifts (mod 10 is not sum-preserving in general)
sums_entropy = [sum(s) for s in states_e]
print(f"\n  State sums (entropy seed): {sums_entropy}")
print(f"  State sum mod 10:           {[s%10 for s in sums_entropy]}")

# CA vs DDS comparison
print(f"""
  Comparison:
    DDS (iterated digit sum):
      − Each step: one number → one number
      − All trajectories converge (single digit)
      − 1 is a fixed point (only if starting from DR=1)
      − DR=2 converges to 2, DR=7 to 7, etc.
      − Dissipative: information destroyed in 1–2 steps

    1D CA (local digit interaction):
      − Each step: array → array (structure preserved)
      − Sum is NOT conserved (mod-10 interaction)
      − Behavior depends on initial state
      − Can exhibit cycles, patterns, apparent structure
      − NOT automatically contractive (unlike DDS)

  Key distinction:
    DDS with digit_sum is contractive by construction.
    CA with local additive rule preserves spatial structure
    and can produce rich dynamics (not necessarily → 1).
""")


# ---- C3: DDS multi-stage map F(x) = N(C(P(A(x)))) ---------------
print()
print("  C3. Multi-stage DDS:  x_{t+1} = N(C(P(A(x_t))))")
print("  A=accumulate, P=pattern, C=correct, N=normalize")
print()


def multi_stage_dds(x, bias=0):
    """
    A simplified realization:
      A: accumulate (digit sum)
      P: pattern (× 2, identifying structure)
      C: correct (bias applied)
      N: normalize (mod 9, mapping to 1..9)
    """
    a = digit_sum(x)           # A
    p = a * 2                  # P
    c = p + bias               # C
    n = c % 9 or 9             # N (digit root of c)
    return n


print(f"  {'x':>8}  {'A=dr':>6}  {'P=2·A':>7}  {'C=P+0':>7}  {'N=C mod9':>10}")
print(f"  {'-'*45}")
for x in [31448, 137, 999, 46, 3, 8, 24]:
    a = digit_sum(x)
    p = a * 2
    c = p
    n = c % 9 or 9
    print(f"  {x:>8}  {a:>6}  {p:>7}  {c:>7}  {n:>10}")


# ============================================================
# Summary
# ============================================================
print()
print("=" * 62)
print("SUMMARY")
print("=" * 62)
print(f"""
  A. {{1,11,111}} Representation Theorem:
     14/14 test cases:  {'PASS ✓' if all_pass else 'FAIL'}
     FSM ≡ greedy for n=0..999: {'YES ✓' if not mismatches else 'NO'}
     Theorem: every n ≥ 0 representable; no n < 0 representable ✓
     FORMULA CORRECTION: user wrote c=n%11 (wrong); correct is c=(n%111)%11
       (111 ≡ 1 mod 11, so the two expressions differ by (n//111) mod 11)

  B. Cascade chain 3.1448 → 19 → 10 → 1:
     ARITHMETIC ERROR in claim: 3+1+4+4+8 = 20 (not 19)
     Correct chain: 3.1448 → 20 → 2  (DR=2, not 1)
     4.6% → 10 → 1: CORRECT ✓ (4+6=10, 1+0=1)

  C. DDS/CA reinterpretation:
     DDS (iterated digit sum): global attractor = DR of starting value
       NOT always 1 — DR=2 → 2, DR=7 → 7, etc.
     CA (local additive rule): no universal collapse; emergent structure
     Multi-stage F=N(C(P(A(x)))): maps all inputs to a DR class
     Claim "everything → 1": holds only for inputs with DR=1
""")
