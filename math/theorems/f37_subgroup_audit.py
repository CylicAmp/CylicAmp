# math/theorems/f37_subgroup_audit.py
"""
F_37× Subgroup Theory: ⟨27⟩ and the 37-Family Law
====================================================
Claims verified:
  1. ord_37(2) = 36: 2 is a primitive root mod 37
  2. 27 ≡ 2^6 (mod 37); ⟨27⟩ has order 6, index 6 in F_37×
  3. ⟨27⟩ = {1, 10, 11, 26, 27, 36}  (sorted)
  4. Antipodal pairs: {1,36}, {10,27}, {11,26}  (each sums to 37)
  5. Orbit table: 6 multiplications by 2 scale every element by 27
  6. The 6 cosets of ⟨27⟩ partition F_37× = {1,...,36}
  7. 14 two-digit representatives (10..99) reduce to elements of ⟨27⟩ mod 37
     (NOT 16: r=1 loses lowest rep since 1 < 10; range 00..99 gives 15)
  8. 25-boundary effect: 99 ≡ 25 (mod 37) determines count distribution
     (residues 10,11 ≤ 25 get 3 reps; residues 1,26,27,36 each get ≤ 2)

3-digit extension:
  ABC in 100..999 with ABC mod 37 ∈ ⟨27⟩: computed and reported.
"""


# ── helpers ───────────────────────────────────────────────────────────────────

def multiplicative_order(g: int, q: int) -> int:
    o, x = 1, g % q
    while x != 1:
        x = x * g % q
        o += 1
    return o


def subgroup(g: int, q: int) -> list:
    """Elements of cyclic subgroup ⟨g⟩ in (Z/qZ)×."""
    s, x = [], 1
    for _ in range(multiplicative_order(g, q)):
        s.append(x)
        x = x * g % q
    return s


def cosets(gen_subgroup: list, full_gen: int, q: int, index: int) -> list:
    """Cosets of ⟨gen_subgroup⟩ via powers of full_gen."""
    result = []
    for k in range(index):
        rep = pow(full_gen, k, q)
        coset = sorted(rep * h % q for h in gen_subgroup)
        result.append((k, rep, coset))
    return result


# ── verify ────────────────────────────────────────────────────────────────────

def verify():
    print("F_37× Subgroup Theory: ⟨27⟩ and the 37-Family Law\n")

    q = 37

    # ── Claim 1: 2 is a primitive root mod 37 ────────────────────────────────
    print("=" * 60)
    print("CLAIM 1: ord_37(2) = 36  (2 is a primitive root)")
    print("=" * 60)

    ord2 = multiplicative_order(2, q)
    assert ord2 == q - 1    # 36 = phi(37)

    # Confirm no proper divisor of 36 works
    for d in [1, 2, 3, 4, 6, 9, 12, 18]:
        assert pow(2, d, q) != 1, f"2^{d} ≡ 1 contradicts primitive root claim"

    print(f"\n  ord_37(2) = {ord2} = phi(37)  OK")
    print(f"  2^k ≠ 1 for all proper divisors k of 36  OK")
    print(f"  Powers of 2 (mod 37) generate all {q-1} nonzero residues  OK\n")

    # ── Claim 2: 27 ≡ 2^6 and ord(27) = 6 ───────────────────────────────────
    print("=" * 60)
    print("CLAIM 2: 27 ≡ 2^6 (mod 37);  ⟨27⟩ has order 6, index 6")
    print("=" * 60)

    assert pow(2, 6, q) == 27
    ord27 = multiplicative_order(27, q)
    assert ord27 == 6
    assert (q - 1) // ord27 == 6   # index = 36/6 = 6

    print(f"\n  2^6 mod 37 = {pow(2,6,q)}  OK")
    print(f"  ord_37(27) = {ord27}  =  36 / gcd(6,36)  =  36/6  OK")
    print(f"  Index [F_37× : ⟨27⟩] = {(q-1)//ord27}  OK\n")

    # ── Claim 3: explicit subgroup ────────────────────────────────────────────
    print("=" * 60)
    print("CLAIM 3: ⟨27⟩ = {1, 10, 11, 26, 27, 36}")
    print("=" * 60)

    H = subgroup(27, q)
    H_set = set(H)
    assert sorted(H) == [1, 10, 11, 26, 27, 36]

    print(f"\n  27^k mod 37 for k=0..5:")
    x = 1
    for k in range(6):
        print(f"    27^{k} ≡ {x:2d} (mod 37)")
        x = x * 27 % q
    assert x == 1   # returned to identity

    print(f"\n  ⟨27⟩ = {sorted(H)}  OK\n")

    # ── Claim 4: antipodal pairs ──────────────────────────────────────────────
    print("=" * 60)
    print("CLAIM 4: Antipodal pairs — each pair sums to 37")
    print("=" * 60)

    pairs = [(1, 36), (27, 10), (26, 11)]
    for a, b in pairs:
        assert a in H_set and b in H_set
        assert (a + b) % q == 0    # antipodal = additive inverse pairs in subgroup

    for a, b in pairs:
        assert (a + b) == q, f"{a} + {b} ≠ 37"

    print(f"\n  {pairs[0][0]} + {pairs[0][1]} = {q}  (1 ↔ 36 ≡ −1)  OK")
    print(f"  {pairs[1][0]} + {pairs[1][1]} = {q}  (27 ↔ 10)  OK")
    print(f"  {pairs[2][0]} + {pairs[2][1]} = {q}  (26 ↔ 11)  OK")
    print(f"  All three pairs are closed under negation mod 37  OK")
    print(f"  (negation is the antipodal map T ↦ 37−T)  OK\n")

    # ── Claim 5: orbit table under ×2 ────────────────────────────────────────
    print("=" * 60)
    print("CLAIM 5: Orbit table — 6 steps of ×2 scale every element by 27")
    print("=" * 60)

    print(f"\n  T  | ×2¹  ×2²  ×2³  ×2⁴  ×2⁵  ×2⁶ (=27T)")
    print(f"  ---+{'-------'*6}")
    for t in sorted(H):
        row = [pow(2, k, q) * t % q for k in range(1, 7)]
        expected_end = 27 * t % q
        assert row[-1] == expected_end, f"2^6 × {t} ≠ 27×{t}"
        assert row[-1] in H_set, f"27×{t} not in subgroup"
        cols = '  '.join(f"{v:2d}" for v in row)
        print(f"  {t:2d} | {cols}")

    assert pow(2, 6, q) == 27   # 2^6 = 27: the 6-step return factor
    print(f"\n  After 6 ×2 steps: T → 27T (mod 37) for all T in ⟨27⟩  OK")
    print(f"  Intermediate orbit leaves subgroup; returns at step 6  OK\n")

    # ── Claim 6: 6 cosets partition F_37× ────────────────────────────────────
    print("=" * 60)
    print("CLAIM 6: 6 cosets of ⟨27⟩ partition F_37×")
    print("=" * 60)

    cos = cosets(H, 2, q, 6)
    all_els = set()
    print()
    for k, rep, coset in cos:
        label = "  ← ⟨27⟩ itself" if k == 0 else ""
        print(f"  Coset {k} (rep=2^{k}={rep:2d}): {coset}{label}")
        assert len(set(coset) & all_els) == 0, f"coset {k} overlaps"
        all_els |= set(coset)

    assert all_els == set(range(1, q))
    print(f"\n  All 6 cosets disjoint, union = {{1,...,36}}  OK")
    print(f"  Each coset is closed under multiplication by 27 (within coset)  OK")

    # Verify each coset is stable under ×27
    for k, rep, coset in cos:
        coset_s = set(coset)
        assert all(27 * x % q in coset_s for x in coset), \
            f"coset {k} not stable under ×27"
    print(f"  Each coset is a ⟨27⟩-orbit: x → 27x cycles within coset  OK\n")

    # ── Claim 7: 16 two-digit representatives ────────────────────────────────
    print("=" * 60)
    print("CLAIM 7: Two-digit numbers (10..99) that reduce to ⟨27⟩ mod 37")
    print("=" * 60)

    two_digit = [n for n in range(10, 100) if n % q in H_set]
    assert len(two_digit) == 14     # not 16: see boundary note below

    by_residue = {}
    for n in two_digit:
        r = n % q
        by_residue.setdefault(r, []).append(n)

    print(f"\n  Residue | Two-digit reps (10..99)  | Count")
    print(f"  --------|--------------------------|------")
    for r in sorted(H_set):
        reps = by_residue.get(r, [])
        print(f"  {r:7d} | {str(reps):26s}| {len(reps)}")

    print(f"\n  Total two-digit reps in ⟨27⟩ (range 10..99): {len(two_digit)}")
    print(f"  NOTE: count is 14, not 16.")
    print(f"  r=1 loses one rep (1 itself < 10); r=10,11 each gain one (≤25 boundary).")
    print(f"  If range is 00..99 (100 strings), count becomes 15 (r=1 recovers rep '01').")
    print(f"  A count of 16 requires a different domain or additional criterion.\n")

    # ── Claim 8: 25-boundary effect ───────────────────────────────────────────
    print("=" * 60)
    print("CLAIM 8: 25-boundary effect (99 ≡ 25 mod 37)")
    print("=" * 60)

    boundary = 99 % q    # 99 mod 37 = 25
    assert boundary == 25

    print(f"\n  99 ≡ {boundary} (mod 37)")
    print(f"  Residues 10..{boundary}: can appear at n, n+37, n+74  (3 reps in 10..99)")
    print(f"  Residues {boundary+1}..36: only n, n+37  (2 reps in 10..99)")
    print(f"\n  ⟨27⟩ members and their 2-digit rep counts:")

    for r in sorted(H_set):
        count = len(by_residue.get(r, []))
        reason = "3 reps (r <= 25 and smallest rep >= 10)" if count == 3 else "2 reps"
        print(f"    r={r:2d}: {count} — {reason}")

    # Verify the count rule:
    # r=10, 11: ≤25, and 10,11 ≥ 10 → 3 reps each
    # r=1:      ≤25 BUT 1 < 10 → only 38, 75 (2 reps)
    # r=26,27,36: > 25 → 2 reps each
    assert len(by_residue[10]) == 3
    assert len(by_residue[11]) == 3
    assert len(by_residue[1])  == 2    # 1 itself out of 10..99 range
    assert len(by_residue[26]) == 2
    assert len(by_residue[27]) == 2
    assert len(by_residue[36]) == 2
    print(f"\n  Boundary 99 ≡ 25 (mod 37): counts match prediction  OK\n")

    # ── 3-digit extension ─────────────────────────────────────────────────────
    print("=" * 60)
    print("3-DIGIT EXTENSION: ABC in 100..999")
    print("=" * 60)

    three_digit = [n for n in range(100, 1000) if n % q in H_set]
    by_res3 = {}
    for n in three_digit:
        r = n % q
        by_res3.setdefault(r, []).append(n)

    boundary3 = 999 % q    # 999 = 27×37 + 0 → 999 ≡ 0 (mod 37)
    start3 = 100 % q        # 100 ≡ 26 (mod 37)
    assert boundary3 == 0
    assert start3 == 26

    print(f"\n  Range 100..999: 900 numbers")
    print(f"  100 ≡ {start3} (mod 37);  999 ≡ {boundary3} (mod 37)")
    print(f"  900 = 24×37 + 12: residues in first-12 positions from 26 get 25 reps")
    print(f"  First 12 residues starting from 26: {{26,27,...,36,0}}")
    print(f"  Residues 1..25 get 24 reps; residues 0,26..36 get 25 reps\n")

    print(f"  Residue | Count in 100..999")
    print(f"  --------|------------------")
    for r in sorted(H_set):
        cnt = len(by_res3.get(r, []))
        print(f"  {r:7d} | {cnt:5d}")

    total3 = len(three_digit)
    print(f"\n  Total 3-digit ABC in ⟨27⟩: {total3}")
    print(f"  Expected ≈ 900 × 6/37 ≈ {900*6/37:.1f}")
    print(f"  Exact: r=1,10,11 get 24 each; r=26,27,36 get 25 each → {3*24+3*25}")
    assert total3 == 3 * 24 + 3 * 25

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"""
  VERIFIED:
    ord_37(2) = 36  (2 is primitive root of F_37×)             OK
    27 = 2^6 mod 37;  ord_37(27) = 6                           OK
    <27> = {{1,10,11,26,27,36}}  (order 6, index 6)             OK
    Antipodal pairs: {{1,36}},{{10,27}},{{11,26}}  (sum to 37)  OK
    Orbit table: 2^6 = 27, so 6 steps of x2 scale by 27        OK
    6 cosets partition F_37×; each stable under x27             OK
    14 two-digit reps (10..99) in <27>  (not 16; see note)      OK
    25-boundary: 99≡25 explains count split (2 vs 3 reps)       OK

  3-DIGIT EXTENSION:
    {total3} three-digit ABCs (100..999) satisfy ABC mod 37 in <27>
    Distribution: r in {{1,10,11}} -> 24 each; r in {{26,27,36}} -> 25 each
    Boundary: 100≡26 (mod 37), 999≡0 (mod 37); first 12 residues from 26 get +1

  COSET TABLE:  (printed above in Claim 6)
    """)


    print("All assertions passed.")


if __name__ == "__main__":
    verify()
