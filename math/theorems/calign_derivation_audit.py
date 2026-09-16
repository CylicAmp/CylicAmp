# math/theorems/calign_derivation_audit.py
"""
C_Align Derivation Audit — Is √5 − 1/13 derivable from existing structure?
============================================================================
The √5 term: traceable (2φ−1 = √5).
The −1/13 term: no derivation supplied in any prior material.

This file exhaustively checks every structural role of 13 in this codebase
and tests whether any of them naturally produces 1/13 as a correction to √5.

Sections:
  A. Confirm √5 = 2φ−1 (established)
  B. All roles of 13 in existing work
  C. Test each as a candidate source of 1/13
  D. Verdict
"""

import math
from collections import defaultdict


def dr(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


def mul_order(base: int, m: int) -> int | None:
    if math.gcd(base, m) != 1:
        return None
    k, val = 1, base % m
    while val != 1:
        val = (val * base) % m
        k += 1
        if k > m:
            return None
    return k


PHI = (1 + math.sqrt(5)) / 2


def verify():
    print("C_Align Derivation Audit\n")

    # ── A. √5 = 2φ−1 ─────────────────────────────────────────────────────────
    print("=" * 60)
    print("A. √5 = 2φ−1  (traceable)")
    print("=" * 60)

    sqrt5 = math.sqrt(5)
    assert abs(2 * PHI - 1 - sqrt5) < 1e-12
    print(f"\n  φ = (1+√5)/2  →  2φ−1 = √5 = {sqrt5:.10f}  ✓")
    print(f"  Source: golden ratio, period-18 of prime 19, Fibonacci/Lucas")
    print(f"  Connection to existing work: established")

    # ── B. All roles of 13 in this codebase ──────────────────────────────────
    print()
    print("=" * 60)
    print("B. Every structural role of 13 in existing work")
    print("=" * 60)

    # B1. 13 divides 191919919191
    N = 191919919191
    assert N % 13 == 0
    cofactor_13 = N // 13
    print(f"\n  B1. 13 | {N}  ✓")
    print(f"      N/13 = {cofactor_13}")

    # B2. 13 divides 10101 = 3×7×13×37
    assert 10101 % 13 == 0
    assert 10101 == 3 * 7 * 13 * 37
    print(f"\n  B2. 13 | 10101 = 3×7×13×37  ✓")

    # B3. ord_13(10) = multiplicative order of 10 mod 13
    ord13 = mul_order(10, 13)
    assert ord13 == 6
    print(f"\n  B3. ord_13(10) = {ord13}  ✓")
    print(f"      Powers: {[pow(10, i, 13) for i in range(7)]}")

    # B4. 13 as index: 37th prime = 157; what is the 13th prime?
    def primes_up_to(n):
        return [x for x in range(2, n+1) if all(x % d != 0 for d in range(2, x))]
    primes = primes_up_to(200)
    p13 = primes[12]   # 0-indexed
    assert p13 == 41
    print(f"\n  B4. 13th prime = {p13}")

    # B5. 13 mod 9 = DR(13)
    assert dr(13) == 4
    print(f"\n  B5. DR(13) = {dr(13)}")

    # B6. 13 in QR context (used in node_verification_matrix_audit.py)
    # QR shift = n mod 13
    for r in range(13):
        pass   # the QR_shift(n) = n mod 13 was used as a probe
    print(f"\n  B6. n mod 13 used as QR-shift probe in node verification")

    # B7. 13 and the group order: |G|=12, |G|+1=13
    G_order = 12
    assert G_order + 1 == 13
    print(f"\n  B7. |G| = ⟨row_cycle,σ_p,σ_a⟩ = {G_order};  {G_order}+1 = 13")

    # B8. 13 in the period of mod-13 powers: ord_13(10)=6 → period 6 block sum
    blocks_10101 = [int(str(10101)[i:i+2]) for i in range(0, 4, 2)]
    print(f"\n  B8. 10101 = {10101}; 2-digit blocks: {blocks_10101}")
    print(f"      sum = {sum(blocks_10101)};  sum mod 13 = {sum(blocks_10101) % 13}")

    # ── C. Test each as source of 1/13 ────────────────────────────────────────
    print()
    print("=" * 60)
    print("C. Test: does any role of 13 produce 1/13 as correction to √5?")
    print("=" * 60)

    print(f"\n  Target: √5 − C_Align = 1/13 = {1/13:.10f}")
    print(f"  √5 = {sqrt5:.10f}")

    tests = [
        ("1/13 (direct)", 1/13),
        ("1/ord_13(10) = 1/6", 1/6),
        ("1/|G| = 1/12", 1/12),
        ("1/(|G|+1) = 1/13", 1/13),
        ("DR(13)/13 = 4/13", 4/13),
        ("13/(10101/13) = 13/777 ≈ 1/59.8", 13/(10101//13)),
        ("(p13−37)/p13 = (41−37)/41 = 4/41", (41-37)/41),
        ("1/p13 = 1/41", 1/41),
    ]

    target = 1/13
    print()
    for label, val in tests:
        match = abs(val - target) < 1e-9
        print(f"  {label:40s} = {val:.8f}  {'← MATCH' if match else ''}")

    print()
    # C1. |G|+1 = 13 gives 1/(|G|+1) = 1/13 — this IS 1/13
    # but is there a structural reason to use this as a correction?
    print(f"  C1. |G|+1=13 → 1/13 is 1/(group_order+1). No known structural")
    print(f"      justification for subtracting 1/(|G|+1) from √5.")

    # C2. ord_13(10)=6: the period of 10-powers mod 13.
    # Does 1/13 arise as a residual from period-6 structure? Check:
    # 1/ord_13(10) = 1/6 ≠ 1/13
    print(f"\n  C2. ord_13(10)=6 → 1/6 ≠ 1/13. Period-6 structure does not")
    print(f"      produce 1/13 directly.")

    # C3. 10101 = 3×7×13×37: the generator node factor. 1/13 as a cofactor ratio?
    # 10101/13 = 777. 1/777 ≠ 1/13.
    print(f"\n  C3. 10101/13 = {10101//13}. Ratio 13/{10101//13} = {13/777:.6f} ≠ 1/13.")

    # C4. Check if 1/13 appears anywhere in the Fibonacci/Lucas period-24 DR
    # as a frequency: 24 terms, DR=? appears how many times?
    from collections import Counter

    def fib_seq(n):
        f = [0, 1]
        while len(f) < n:
            f.append(f[-1] + f[-2])
        return f[:n]

    fib_drs = [9 if dr(f) == 0 else dr(f) for f in fib_seq(24)]
    fib_counts = Counter(fib_drs)
    # Does any DR appear exactly 24/13 times? No, 24/13 is not integer.
    print(f"\n  C4. Fibonacci period-24 DR counts: {dict(sorted(fib_counts.items()))}")
    print(f"      24/13 = {24/13:.4f} (not integer). No 1/13 frequency.")

    # C5. Does 1/13 appear as a natural normalization in the P(n) structure?
    # P-values sum = 165 = 3×5×11. 165/13 = 12.69... not integer.
    # max P = 25. 25/13 = 1.923...
    # 37/13 ≈ 2.846...  None close to 1/13.
    print(f"\n  C5. P(n) context: sum=165, 165 mod 13 = {165 % 13}. No 1/13 connection.")

    # C6. Check directly: was C_Align = 2φ−1−1/13 stated with a derivation
    #     in any prior material, or just asserted?
    print(f"\n  C6. Origin trace:")
    print(f"      C_Align appeared in 'Complete Master Framework' (Dec 2025)")
    print(f"      as a row in a constants table: '2.1592 / 2φ-1-1/13 / Network efficiency'.")
    print(f"      No derivation was supplied in that document.")
    print(f"      That document was audited as containing unfounded claims.")
    print(f"      The −1/13 term is not derivable from any other structure in this codebase.")

    # ── D. Verdict ────────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("D. Verdict")
    print("=" * 60)
    print(f"""
  √5 = 2φ−1: derived, traceable.  ✓

  −1/13: no derivation exists in any material in this codebase.

  Every structural role of 13 tested:
    13 | 191919919191             → no 1/13 correction
    13 | 10101                    → no 1/13 correction
    ord_13(10) = 6                → gives 1/6, not 1/13
    |G| = 12, |G|+1 = 13         → numerical coincidence only
    DR(13) = 4                    → no 1/13 correction
    period-24 Fibonacci DR        → no 1/13 frequency
    P(n) structure                → no 1/13 connection

  Origin of the expression: the AI-generated 'master framework' document
  (already flagged). No supporting derivation was ever supplied.

  RECOMMENDATION:
    Drop −1/13.  The defensible constant from this work is √5 = 2φ−1.
    If a correction term is needed, it requires an explicit structural
    derivation before being added to the framework.

  C_Align (clean) = √5  ≈ {sqrt5:.10f}
    """)

    print("All assertions passed.")


if __name__ == "__main__":
    verify()
