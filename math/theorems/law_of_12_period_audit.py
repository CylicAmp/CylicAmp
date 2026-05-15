# math/theorems/law_of_12_period_audit.py
"""
Law of 12 — Two Distinct Phenomena
====================================
Two sequences both have DR values in {3,6,9}, but different periods.

Phenomenon 1: dr(12·k) for k=1,2,3,...
  — defined in sovereign_dr_matrix_audit.py
  — period 3: [3,6,9,3,6,9,...]
  — reason: 12≡3 mod 9; dr(3k) cycles {3,6,9} with period 3

Phenomenon 2: dr(3·L_n) for Lucas numbers L_n
  — period 8: [6,3,9,3,3,6,9,6,6,3,9,3,3,6,9,6,...]
  — NOT period 3; residue classes mod 3 are non-constant

F_37 identity triplet {11, 48, 85}:
  — AP with step 37; all ≡ 11 mod 37
  — 3×{11,48,85} = {33,144,255}; DRs = {6,9,3} — one full {3,6,9} cycle
  — period 3; matches the period-3 formula

Claim under audit:
  CLAIM 1: period-3 formula x_n ∈ {3,6,9} cyclic — mathematically valid  → PASS
  CLAIM 2: formula matches F_37 triplet under 3× scaling               → PASS
  CLAIM 3: formula matches dr(3·L_n) Law of 12                         → FAIL (period 8)
"""

import math


def dr(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


def lucas_sequence(length: int) -> list:
    luc = [2, 1]
    while len(luc) < length:
        luc.append(luc[-1] + luc[-2])
    return luc[:length]


def find_period(seq: list) -> int | None:
    """Return smallest period p of seq, or None if not found within half length."""
    n = len(seq)
    for p in range(1, n // 2 + 1):
        if all(seq[i] == seq[i % p] for i in range(n)):
            return p
    return None


def verify():
    print("Law of 12 — Two Distinct Phenomena\n")

    # ── Phenomenon 1: dr(12·k), period 3 ────────────────────────────────────
    print("=" * 60)
    print("Phenomenon 1: dr(12·k)  (multiples of 12)")
    print("=" * 60)

    law12 = [dr(12 * k) for k in range(1, 49)]   # 48 terms = 16 full periods
    law12_prefix = law12[:8]
    assert law12_prefix == [3, 6, 9, 3, 6, 9, 3, 6]
    period1 = find_period(law12)
    assert period1 == 3
    assert all(v in {3, 6, 9} for v in law12)

    print(f"\n  First 24 terms: {law12[:24]}")
    print(f"  Period: {period1}  ✓")
    print(f"  All DRs ∈ {{3,6,9}}: {all(v in {3,6,9} for v in law12)}  ✓")
    print(f"  Reason: 12≡3 (mod 9); dr(3k) ∈ {{3,6,9}} with strict period 3  ✓")

    # ── Phenomenon 2: dr(3·L_n), period 8 ───────────────────────────────────
    print()
    print("=" * 60)
    print("Phenomenon 2: dr(3·L_n)  (3 × Lucas numbers)")
    print("=" * 60)

    L = lucas_sequence(96)   # 96 terms = 12 full periods of 8
    law12_lucas = [dr(3 * l) for l in L]
    law12_lucas_prefix = law12_lucas[:16]
    assert all(v in {3, 6, 9} for v in law12_lucas)

    period2 = find_period(law12_lucas)
    assert period2 == 8

    expected_prefix = [6, 3, 9, 3, 3, 6, 9, 6, 6, 3, 9, 3, 3, 6, 9, 6]
    assert law12_lucas_prefix == expected_prefix

    print(f"\n  First 24 terms: {law12_lucas[:24]}")
    print(f"  Period: {period2}  ✓")
    print(f"  All DRs ∈ {{3,6,9}}: {all(v in {3,6,9} for v in law12_lucas)}  ✓")

    # Residue classes mod 3 — must be NON-CONSTANT for period-3 formula to fail
    for r in range(3):
        subseq = [law12_lucas[n] for n in range(48) if n % 3 == r]
        is_constant = len(set(subseq)) == 1
        print(f"  n≡{r} mod 3: {subseq[:9]}...  constant={is_constant}")
        assert not is_constant, f"Residue class {r} is constant — period-3 formula might work"
    print(f"  No residue class mod 3 is constant → period-3 formula CANNOT match  ✓")

    # ── CLAIM 1: period-3 formula is mathematically valid ────────────────────
    print()
    print("=" * 60)
    print("CLAIM 1: Period-3 formula with DR ∈ {3,6,9} — mathematical validity")
    print("=" * 60)
    print()
    print("  x_n = a if n≡1, b if n≡2, c if n≡0 (mod 3)")
    print("  with (dr(a), dr(b), dr(c)) a cyclic permutation of (3,6,9)")
    print()
    # All 6 permutations generate valid period-3 sequences
    perms = [(3,6,9),(3,9,6),(6,3,9),(6,9,3),(9,3,6),(9,6,3)]
    for p in perms:
        a, b, c = p
        seq = [c if n%3==0 else a if n%3==1 else b for n in range(9)]
        assert all(v in {3,6,9} for v in seq)
        assert find_period(seq) in {1, 3}
    print(f"  All 6 permutations of (3,6,9) produce valid period-3 sequences  ✓")
    print(f"  STATUS: PASS")

    # ── CLAIM 2: matches F_37 identity triplet {11, 48, 85} ──────────────────
    print()
    print("=" * 60)
    print("CLAIM 2: Formula matches F_37 identity triplet {11, 48, 85}")
    print("=" * 60)

    triplet = [11, 48, 85]
    # All ≡ 11 mod 37
    assert all(t % 37 == 11 for t in triplet)
    # AP with step 37
    assert triplet[1] - triplet[0] == 37 and triplet[2] - triplet[1] == 37

    scaled = [3 * t for t in triplet]
    scaled_drs = [dr(v) for v in scaled]
    assert scaled == [33, 144, 255]
    assert scaled_drs == [6, 9, 3]
    assert set(scaled_drs) == {3, 6, 9}

    print(f"\n  Triplet: {triplet}  (all ≡ 11 mod 37, step = 37)  ✓")
    print(f"  3×triplet: {scaled}")
    print(f"  DRs: {scaled_drs}  = one full cycle of {{3,6,9}}  ✓")

    # Match to formula: c=6 (n≡0→6), a=9 (n≡1→9), b=3 (n≡2→3)
    # Under cyclic permutation (a,b,c)↦(c,a,b): [9,3,6]→[6,9,3] matches [6,9,3]
    formula_seq = [6 if n%3==0 else 9 if n%3==1 else 3 for n in range(9)]
    triplet_extended = scaled_drs * 3
    assert formula_seq == triplet_extended
    print(f"  Formula match (c=6,a=9,b=3): {formula_seq[:6]} = triplet cycle repeated  ✓")
    print(f"  Period: {find_period(formula_seq)}  ✓")
    print(f"  STATUS: PASS")

    # ── CLAIM 3: formula does NOT match dr(3·L_n) ────────────────────────────
    print()
    print("=" * 60)
    print("CLAIM 3: Formula vs dr(3·L_n)  — period mismatch")
    print("=" * 60)

    print(f"\n  Phenomenon 1 period: {period1}")
    print(f"  Phenomenon 2 period: {period2}")
    print(f"  Periods differ: {period1} ≠ {period2}  ✓")

    # Check all 6 permutations against the Lucas sequence
    print(f"\n  Testing all 6 permutations of (3,6,9) against dr(3·L_n):")
    any_match = False
    for a, b, c in perms:
        candidate = [c if n%3==0 else a if n%3==1 else b for n in range(48)]
        match = (candidate[:48] == law12_lucas[:48])
        print(f"    (a={a},b={b},c={c}): match = {match}")
        if match:
            any_match = True
    assert not any_match
    print(f"\n  No period-3 formula matches dr(3·L_n)  ✓")
    print(f"  STATUS: FAIL (as expected — period 8 ≠ period 3)")

    # ── Cross-connection: do the two sequences share structure? ───────────────
    print()
    print("=" * 60)
    print("Cross-connection between the two phenomena")
    print("=" * 60)

    # Both sequences have all DR ∈ {3,6,9}
    # Both are related to multiples of 3 (since 3×anything always has DR∈{3,6,9})
    # Phenomenon 1 period = 3; Phenomenon 2 period = 8; lcm = 24
    from math import gcd
    lcm_p = (period1 * period2) // gcd(period1, period2)
    print(f"\n  Both: all DR ∈ {{3,6,9}}  ✓")
    print(f"  Phenomenon 1 period = {period1}")
    print(f"  Phenomenon 2 period = {period2}")
    print(f"  LCM = {lcm_p}")
    print(f"  Note: period 24 (Fibonacci/Lucas DR period) = {lcm_p} × 3")
    # The Lucas DR period is 24; dr(3·L_n) has period 8 = 24/3
    assert 24 % period2 == 0
    assert 24 // period2 == 3
    print(f"  dr(3·L_n) period 8 = Fibonacci/Lucas period 24 ÷ 3  ✓")

    # Period-8 structure: 8 = 24/3 means every third position in the period-24
    # Lucas DR sequence gives a period-8 subsequence? Let's check.
    lucas_drs_24 = [dr(l) for l in lucas_sequence(24)]
    # The actual period-8 cycle is [6,3,9,3,3,6,9,6]
    period8_cycle = [6,3,9,3,3,6,9,6]
    assert law12_lucas[:8] == period8_cycle
    print(f"\n  Period-8 cycle: {period8_cycle}")
    # DR sum of one period-8 cycle
    cycle_sum = sum(period8_cycle)
    assert cycle_sum == 3+6+9+3+3+6+9+6
    print(f"  Sum of one period-8 cycle: {cycle_sum}")
    print(f"  DR({cycle_sum}) = {dr(cycle_sum)}")
    # 3+6+9+3+3+6+9+6 = 45; DR(45) = 9
    assert cycle_sum == 45 and dr(45) == 9
    print(f"  Cycle sum = 45 = 9×5;  DR = 9  ✓")

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"""
  Two distinct {'{3,6,9}'} phenomena:

  Phenomenon         Sequence        Period  Formula match  Source
  ─────────────────────────────────────────────────────────────────
  Multiples of 12    dr(12·k)           3     YES (trivial)  Law of 12
  Lucas ×3           dr(3·L_n)          8     NO             Lucas period

  F_37 triplet       3×{{11,48,85}}     3     YES            mod-37 AP

  Claims:
    CLAIM 1 (formula valid)              PASS  ✓
    CLAIM 2 (matches F_37 triplet)       PASS  ✓
    CLAIM 3 (matches Lucas Law of 12)    FAIL  ✗

  Connection:
    dr(3·L_n) period 8 = Lucas DR period 24 ÷ 3  ✓
    One period-8 cycle sums to 45; DR(45) = 9  ✓
    """)

    print("All assertions passed.")


if __name__ == "__main__":
    verify()
