# math/theorems/spoke_enumeration_ab_audit.py
"""
Spoke Enumeration Audit — Valid AB Pairs per Spoke in ⟨27⟩ ⊂ F_37
====================================================================

Two formulas produce two valid but DISTINCT enumerations.

Formula A  (mirror table, earlier audit):
    val_A = (AB × 101) % 37 = (AB × 27) % 37
    Filter: val_A ∈ {1, 10, 11, 26, 27, 36}
    Result: 14 pairs  (distribution: 3,2,2,2,2,3)

Formula B  (user's spoke table):
    val_B = (AB × 101 × 18) % 37 = (AB × 5) % 37
    Filter: val_B ∈ {1, 10, 11, 26, 27, 36}
    Result: 16 pairs  (distribution: 3,2,3,3,2,3)

These answer different questions:
    Formula A: where does ABAB sit in F_37 directly?
    Formula B: what is the "fraction value" ABAB/12800 in F_37?
               (18 = modular inverse of 12800 ≡ −2 mod 37)

The 16 vs 14 difference is NOT a filter issue — it is the difference
between multiplying by 27 vs multiplying by 5 before the membership
test. The base residues (and therefore the AB sets) are completely
disjoint between the two formulas.

Antipodal symmetry (Formula B): Spoke T ↔ Spoke (−T mod 37).
The base residues are also antipodal: base(T) + base(−T) ≡ 0 (mod 37).
"""

P = 37

SUBGROUP = {1, 10, 11, 26, 27, 36}    # ⟨27⟩ ⊂ F_37×
SPOKE_ORDER = [1, 27, 26, 36, 10, 11]  # C6 cycle order

USER_SPOKES = {
    1:  [15, 52, 89],
    27: [35, 72],
    26: [20, 57, 94],
    36: [22, 59, 96],
    10: [39, 76],
    11: [17, 54, 91],
}


# ── Verify the two multipliers ────────────────────────────────────────────────

assert 101 % P == 27                    # ABAB = AB × 101, so 101 ≡ 27
assert (27 * 18) % P == 5              # Formula B multiplier: 27 × 18 = 5 mod 37
assert (18 * (-2)) % P == 1           # 18 = (−2)^{-1} mod 37
assert (5 * pow(27, -1, P)) % P == 18  # 5 = 27 × 18,  so 5/27 = 18 = inv(12800)


# ── Enumerate both formulas ───────────────────────────────────────────────────

formula_a = {}   # val_A = AB×27 % 37,  filter ∈ subgroup
formula_b = {}   # val_B = AB×5  % 37,  filter ∈ subgroup

for ab in range(10, 100):
    va = (ab * 27) % P
    vb = (ab * 5)  % P
    if va in SUBGROUP:
        formula_a.setdefault(va, []).append(ab)
    if vb in SUBGROUP:
        formula_b.setdefault(vb, []).append(ab)

assert sum(len(v) for v in formula_a.values()) == 14
assert sum(len(v) for v in formula_b.values()) == 16

# The two AB sets are completely disjoint
set_a = {ab for lst in formula_a.values() for ab in lst}
set_b = {ab for lst in formula_b.values() for ab in lst}
assert set_a.isdisjoint(set_b), "FAIL: expected disjoint AB sets"


# ── Verify user's enumeration (Formula B) ────────────────────────────────────

for T, expected in USER_SPOKES.items():
    calc = formula_b.get(T, [])
    assert calc == expected, f"FAIL: Spoke T={T}: expected {expected}, got {calc}"

# Total count
assert sum(len(v) for v in USER_SPOKES.values()) == 16


# ── Verify antipodal symmetry ─────────────────────────────────────────────────

# T ↔ −T are antipodal pairs in the subgroup
antipodal = [(1, 36), (27, 10), (26, 11)]

for T1, T2 in antipodal:
    assert (T1 + T2) % P == 0          # T values are antipodal

    base1 = USER_SPOKES[T1][0] % P     # base residue of spoke T1
    base2 = USER_SPOKES[T2][0] % P     # base residue of spoke T2
    assert (base1 + base2) % P == 0, \
        f"FAIL: base residues not antipodal for ({T1},{T2}): {base1}+{base2}"

    # All AB pairs in each spoke share the same residue mod 37
    for ab in USER_SPOKES[T1]:
        assert ab % P == USER_SPOKES[T1][0] % P
    for ab in USER_SPOKES[T2]:
        assert ab % P == USER_SPOKES[T2][0] % P


# ── Why 14 vs 16: count per spoke ────────────────────────────────────────────
# Each spoke's count = number of integers ≡ base (mod 37) in [10, 99].
# = 3 if base ∈ [10, 25], else 2  (since base+74 ≤ 99 iff base ≤ 25)
# EXCEPT: if base < 10, the smallest representative is base+37.

def count_in_window(base_residue: int) -> int:
    first = base_residue if base_residue >= 10 else base_residue + P
    return len([first + k*P for k in range(3) if 10 <= first + k*P <= 99])

# Formula A base residues: {11:11, 27:1, 26:27, 36:26, 10:36, 11base:10}
# (the T→base map under ×27^{-1} = ×11)
for T, pairs in formula_a.items():
    base = pairs[0] % P
    assert count_in_window(base) == len(pairs)

# Formula B base residues under ×5^{-1} = ×15
for T, pairs in formula_b.items():
    base = pairs[0] % P
    assert count_in_window(base) == len(pairs)

# The 16−14=2 extra pairs in Formula B are because Formula B's base
# residues include {20,22} (both ≤25) giving 3 pairs, while Formula A's
# corresponding residues {27,26} (both >25) give only 2.
b_counts = sorted(len(v) for v in formula_b.values())
a_counts = sorted(len(v) for v in formula_a.values())
assert b_counts == [2, 2, 3, 3, 3, 3]
assert a_counts == [2, 2, 2, 2, 3, 3]


# ── Report ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Spoke Enumeration Audit — AB pairs per spoke")
    print()
    print(f"  Formula A  (AB×27 % 37 ∈ subgroup):  {sum(len(v) for v in formula_a.values())} pairs")
    for T in SPOKE_ORDER:
        print(f"    T={T:2d}  base≡{formula_a[T][0]%P:2d}  {formula_a[T]}")
    print()
    print(f"  Formula B  (AB×5 % 37 ∈ subgroup):   {sum(len(v) for v in formula_b.values())} pairs")
    for i, T in enumerate(SPOKE_ORDER):
        pairs = formula_b[T]
        base  = pairs[0] % P
        print(f"    Spoke {i}  T={T:2d}  base≡{base:2d}  {pairs}")
    print()
    print(f"  AB sets disjoint: {set_a.isdisjoint(set_b)}  ✓")
    print()
    print("  Antipodal base-residue pairs (Formula B):")
    for T1, T2 in antipodal:
        b1 = USER_SPOKES[T1][0] % P
        b2 = USER_SPOKES[T2][0] % P
        print(f"    T={T1:2d}↔T={T2:2d}:  base {b1:2d}+{b2:2d}={b1+b2} ≡ 0 (mod 37)  ✓")
    print()
    print("  Count difference (16−14=2):")
    print(f"    Formula A per-spoke counts: {a_counts}  (four '2's)")
    print(f"    Formula B per-spoke counts: {b_counts}  (two  '2's)")
    print(f"    Root cause: Formula A bases {{26,27,36,1}} include residues >25,")
    print(f"    giving only 2 pairs each. Formula B bases {{15,17,20,22}} are ≤25,")
    print(f"    giving 3 pairs each. Not a filter — genuinely different multiplier.")
    print()
    print("All assertions passed.")
