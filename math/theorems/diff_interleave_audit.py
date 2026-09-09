"""
diff_interleave_audit.py

Difference-interleaving sequence from seed S₀ = (1, 2, 3).

RULE:
  Given S = (a₁, …, aₖ), compute D = (|a₁-a₂|, …, |aₖ₋₁-aₖ|).
  S' = (a₁, d₁, a₂, d₂, …, d_{k-1}, aₖ)  [interleave S with D]

─────────────────────────────────────────────────────────────────
ITERATIONS (verified):

  S₀ = (1, 2, 3)
  D₀ = (1, 1)
  S₁ = (1, 1, 2, 1, 3)

  D₁ = (0, 1, 1, 2)
  S₂ = (1, 0, 1, 1, 2, 1, 1, 2, 3)

  D₂ = (1, 1, 0, 1, 1, 0, 1, 1)
  S₃ = (1, 1, 0, 1, 1, 0, 1, 1, 2, 1, 1, 0, 1, 1, 2, 1, 3)

  D₃ = (0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 2)
  S₄ = (1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 2, 1, 1, 0,
         1, 1, 0, 1, 1, 0, 1, 1, 2, 1, 1, 2, 3)

NOTE: The submitted S₄ contained 17 element errors.
The submitted tuple (1,0,1,1,0,1,0,1,1,0,…) diverges from the
correct interleaving of S₃ with D₃ at positions 6, 7 and onwards.
S₁–S₃ and D₀–D₃ are all correct.

STRUCTURAL INVARIANTS (all hold for all n ≥ 0):
  (I1) S_n[0] = 1   (first element fixed)
  (I2) S_n[-1] = 3  (last element fixed)
  (I3) max(S_n) = 3
  (I4) S_n[-2] = 2 if n even, 1 if n odd

CONVERGENCE CLAIM CORRECTION:
  The submitted text claims the sequence eventually reaches (0,…,0,1)
  then (0,…,0). This is FALSE for seed (1,2,3):
  — I1 forces first element = 1 ≠ 0 for all n.
  — I2 forces last element = 3 ≠ 0 for all n.
  — sum(S_n) is strictly increasing (sum(D_n) > 0 for all n).
  The all-zero fixed point is reachable only from the all-zero seed.

LENGTH:
  L_n = 2^(n+1) + 1   (L₀=3, L₁=5, L₂=9, L₃=17, L₄=33, …)

ZERO DENSITY:
  zeros(S_n) / L_n → 1/3 as n → ∞.
  Interior converges toward the period-3 pattern (1, 1, 0)ω.

  n=0:  0/3   = 0.0000
  n=1:  0/5   = 0.0000
  n=2:  1/9   ≈ 0.1111
  n=3:  3/17  ≈ 0.1765
  n=4:  8/33  ≈ 0.2424
  n=8:  166/513 ≈ 0.3236  → 1/3

SUM:
  sum(S_n) grows as (4^(⌊n/2⌋+1))/3 + O(n).
  sum increments = sum(D_n): 2, 4, 6, 12, 22, 44, 86, 172, …
  where a(2k) = (4^(k+1)+2)/3  and  a(2k+1) = 2(4^(k+1)+2)/3.
─────────────────────────────────────────────────────────────────
"""

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


# ── Rule implementation ────────────────────────────────────────────────────────

def diff_step(S):
    D = [abs(S[i] - S[i + 1]) for i in range(len(S) - 1)]
    result = []
    for i in range(len(S) - 1):
        result.append(S[i])
        result.append(D[i])
    result.append(S[-1])
    return result, D


# ── Generate through iteration 8 ──────────────────────────────────────────────

S0 = [1, 2, 3]
sequences = [S0]
diff_seqs = []
S = S0
for _ in range(8):
    S_new, D = diff_step(S)
    sequences.append(S_new)
    diff_seqs.append(D)
    S = S_new


# ── Verify S₁–S₃ and D₀–D₃ ───────────────────────────────────────────────────

check(sequences[1] == [1, 1, 2, 1, 3],
      "S1", sequences[1], [1, 1, 2, 1, 3])

check(diff_seqs[0] == [1, 1],
      "D0", diff_seqs[0], [1, 1])

check(diff_seqs[1] == [0, 1, 1, 2],
      "D1", diff_seqs[1], [0, 1, 1, 2])

check(sequences[2] == [1, 0, 1, 1, 2, 1, 1, 2, 3],
      "S2", sequences[2], [1, 0, 1, 1, 2, 1, 1, 2, 3])

check(diff_seqs[2] == [1, 1, 0, 1, 1, 0, 1, 1],
      "D2", diff_seqs[2], [1, 1, 0, 1, 1, 0, 1, 1])

check(sequences[3] == [1, 1, 0, 1, 1, 0, 1, 1, 2, 1, 1, 0, 1, 1, 2, 1, 3],
      "S3", sequences[3], [1, 1, 0, 1, 1, 0, 1, 1, 2, 1, 1, 0, 1, 1, 2, 1, 3])

check(diff_seqs[3] == [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 2],
      "D3", diff_seqs[3], [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 2])

CORRECT_S4 = [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 2,
              1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 2, 1, 1, 2, 3]
check(sequences[4] == CORRECT_S4, "S4 correct", sequences[4], CORRECT_S4)

# The submitted S4 (17 element errors; included for reference only)
SUBMITTED_S4 = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 2,
                1, 1, 0, 1, 1, 0, 1, 1, 2, 1, 2, 1, 2, 3]
s4_errors = [(i, CORRECT_S4[i], SUBMITTED_S4[i])
             for i in range(len(CORRECT_S4))
             if CORRECT_S4[i] != SUBMITTED_S4[i]]
check(len(s4_errors) == 17, "S4 error count", len(s4_errors), 17)


# ── Length formula: L_n = 2^(n+1) + 1 ────────────────────────────────────────

for n, seq in enumerate(sequences):
    expected = 2 ** (n + 1) + 1
    check(len(seq) == expected, f"L_{n}", len(seq), expected)


# ── Structural invariants ──────────────────────────────────────────────────────

for n, seq in enumerate(sequences):
    check(seq[0]  == 1, f"I1 first n={n}", seq[0],  1)
    check(seq[-1] == 3, f"I2 last n={n}",  seq[-1], 3)
    check(max(seq) == 3, f"I3 max n={n}",  max(seq), 3)

for n, seq in enumerate(sequences):
    expected_penult = 2 if n % 2 == 0 else 1
    check(seq[-2] == expected_penult, f"I4 penult n={n}", seq[-2], expected_penult)


# ── Sum strictly increases ────────────────────────────────────────────────────

sums = [sum(s) for s in sequences]
EXPECTED_SUMS = [6, 8, 12, 18, 30, 52, 96, 182, 354]

for n, (s, e) in enumerate(zip(sums, EXPECTED_SUMS)):
    check(s == e, f"sum n={n}", s, e)

for n in range(len(sums) - 1):
    check(sums[n + 1] > sums[n], f"sum increasing n={n}", sums[n + 1], f"> {sums[n]}")


# ── Sum increments: a(2k) = (4^(k+1)+2)/3 ────────────────────────────────────

increments = [sums[n + 1] - sums[n] for n in range(len(sums) - 1)]
EXPECTED_INCREMENTS = [2, 4, 6, 12, 22, 44, 86, 172]

for n, (inc, e) in enumerate(zip(increments, EXPECTED_INCREMENTS)):
    check(inc == e, f"increment n={n}", inc, e)

# a(2k) = (4^(k+1)+2)/3
for k in range(4):
    a_2k = (4 ** (k + 1) + 2) // 3
    check(increments[2 * k] == a_2k, f"a(2×{k})=(4^{k+1}+2)/3", increments[2*k], a_2k)

# a(2k+1) = 2*(4^(k+1)+2)/3
for k in range(4):
    a_2k1 = 2 * (4 ** (k + 1) + 2) // 3
    check(increments[2 * k + 1] == a_2k1, f"a(2×{k}+1)", increments[2*k+1], a_2k1)


# ── Zero density increases toward 1/3 ────────────────────────────────────────

EXPECTED_ZEROS = [0, 0, 1, 3, 8, 18, 39, 81, 166]

for n, (seq, ez) in enumerate(zip(sequences, EXPECTED_ZEROS)):
    check(seq.count(0) == ez, f"zeros n={n}", seq.count(0), ez)

# Density at n=8 is closer to 1/3 than at n=4
d4 = sequences[4].count(0) / len(sequences[4])
d8 = sequences[8].count(0) / len(sequences[8])
check(abs(d8 - 1/3) < abs(d4 - 1/3), "density converging to 1/3", True, True)


# ── Convergence claim is FALSE for seed (1,2,3) ──────────────────────────────

# First element is always 1 ≠ 0; sum is strictly increasing (never zero)
for seq in sequences:
    check(seq[0] != 0, "first ≠ 0 (no all-zero)", seq[0], "!=0")
    check(sum(seq) > 0, "sum > 0 (no all-zero)", sum(seq), ">0")

# All-zero IS a fixed point (for the all-zero seed)
def is_fixed_point(S):
    S_new, _ = diff_step(S)
    return S_new == S + [0] * (len(S) - 1)   # grows in length but all zeros → no

zeros_3 = [0, 0, 0]
all_zero_step, _ = diff_step(zeros_3)
check(all(x == 0 for x in all_zero_step), "all-zero maps to all-zero", all(x==0 for x in all_zero_step), True)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Difference-Interleave Audit: seed (1, 2, 3)")
    print("=" * 62)

    for n in range(5):
        seq = sequences[n]
        zeros = seq.count(0)
        print(f"\n  S{n} = {seq}")
        print(f"       len={len(seq)}  sum={sums[n]}  DR(sum)={dr(sums[n])}  zeros={zeros}")
        if n < len(diff_seqs):
            print(f"  D{n} = {diff_seqs[n]}")

    print(f"\n── Structural invariants ──")
    print(f"  First element: always 1   (I1)")
    print(f"  Last element:  always 3   (I2)")
    print(f"  Max value:     always 3   (I3)")
    print(f"  Penultimate:   2 if n even, 1 if n odd  (I4)")

    print(f"\n── Length formula: L_n = 2^(n+1) + 1 ──")
    for n in range(9):
        print(f"  n={n}: {2**(n+1)+1}")

    print(f"\n── Zero density → 1/3 ──")
    for n, (seq, z) in enumerate(zip(sequences, EXPECTED_ZEROS)):
        d = z / len(seq)
        print(f"  n={n}: {z:>4}/{len(seq):<4} = {d:.4f}  (|d - 1/3| = {abs(d-1/3):.4f})")

    print(f"\n── Sum increments: a(2k)=(4^(k+1)+2)/3 ──")
    for n, inc in enumerate(increments):
        print(f"  D{n} sum = {inc}")

    print(f"\n── S4 error report ──")
    print(f"  Submitted S4 has {len(s4_errors)} errors vs correct interleaving of S3 with D3.")
    print(f"  First error at position {s4_errors[0][0]}: correct={s4_errors[0][1]}, submitted={s4_errors[0][2]}")
    print(f"  Correct S4 = {CORRECT_S4}")

    print(f"\n── Convergence claim correction ──")
    print(f"  Claim: sequence reaches (0,…,0,1) then (0,…,0).")
    print(f"  FALSE for seed (1,2,3): first=1 and last=3 are invariant.")
    print(f"  sum is strictly increasing; the sequence never contains all zeros.")
    print(f"  The all-zero fixed point is reachable only from the all-zero seed.")
    print(f"  Correct description: interior converges to period-3 pattern (1,1,0).")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
