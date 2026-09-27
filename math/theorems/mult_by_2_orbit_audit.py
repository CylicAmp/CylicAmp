# math/theorems/mult_by_2_orbit_audit.py
"""
Multiplication-by-2 Orbit Audit — ⟨27⟩ ⊂ F_37, and 3-digit extension
======================================================================

2 is a primitive root mod 37 (ord(2) = 36).
The 6-spoke subgroup ⟨27⟩ = {1,10,11,26,27,36} is the unique index-6
subgroup of F_37×.

Key identity: 2^6 ≡ 27 (mod 37)
  ⟹ starting from any T ∈ ⟨27⟩, the orbit T, 2T, 4T, ..., 2^6·T
     returns to ⟨27⟩ at k=6, landing at 27T.
  ⟹ intermediate values k=1..5 all lie OUTSIDE ⟨27⟩.

The map T ↦ 27T is the C6 generator — it cycles the spokes.

2-digit ABAB = AB × 101 ≡ AB × 27 (mod 37)
3-digit ABCABC = ABC × 1001 ≡ ABC × 2  (mod 37)
  The generator flips: 27 (2-digit) → 2 (3-digit).
  Spokes land at k ≡ 0 mod 6 under ×2; 3-digit forms hit them at k=1.
"""

P = 37
SUBGROUP = {1, 10, 11, 26, 27, 36}   # ⟨27⟩ = C6
SPOKE_ORDER = [1, 27, 26, 36, 10, 11]

# ── Primitive root ────────────────────────────────────────────────────────────

assert pow(2, 36, P) == 1
ord2 = next(k for k in range(1, P) if pow(2, k, P) == 1)
assert ord2 == 36   # 2 is a primitive root mod 37

# ── 2^6 ≡ 27 ─────────────────────────────────────────────────────────────────

assert pow(2, 6, P) == 27

# ── Orbit table — verify every row ───────────────────────────────────────────

EXPECTED_TABLE = {
    1:  [1,  2,  4,  8, 16, 32, 27],
    27: [27, 17, 34, 31, 25, 13, 26],
    26: [26, 15, 30, 23,  9, 18, 36],
    36: [36, 35, 33, 29, 21,  5, 10],
    10: [10, 20,  3,  6, 12, 24, 11],
    11: [11, 22,  7, 14, 28, 19,  1],
}

for T, expected_row in EXPECTED_TABLE.items():
    row = []
    curr = T
    for k in range(7):
        row.append(curr)
        curr = (curr * 2) % P
    assert row == expected_row, f"FAIL: row T={T}: {row} ≠ {expected_row}"

# ── Return condition: k=6 value = 27T ────────────────────────────────────────

for T, row in EXPECTED_TABLE.items():
    assert row[6] == (27 * T) % P, f"FAIL: row[6] ≠ 27T for T={T}"
    assert row[6] in SUBGROUP,     f"FAIL: row[6] not in subgroup for T={T}"

# ── k=1..5 all outside subgroup ──────────────────────────────────────────────

for T, row in EXPECTED_TABLE.items():
    for k in range(1, 6):
        assert row[k] not in SUBGROUP, \
            f"FAIL: row[{k}] = {row[k]} in subgroup for T={T}"

# ── Map T → 27T permutes the spokes ──────────────────────────────────────────

# 1→27→26→36→10→11→1  (the C6 cycle itself)
permuted = [(27 * T) % P for T in SPOKE_ORDER]
assert permuted == SPOKE_ORDER[1:] + [SPOKE_ORDER[0]]   # cyclic shift by 1

# ── Why k≡0 mod 6 is the ONLY return ─────────────────────────────────────────
# 2^k ∈ ⟨27⟩ iff ord(2^k) | 6 iff 36/gcd(k,36) | 6 iff gcd(k,36) ≥ 6 iff 6|k

for k in range(1, 36):
    in_subgroup = pow(2, k, P) in SUBGROUP
    assert in_subgroup == (k % 6 == 0), \
        f"FAIL: k={k}, 2^k={pow(2,k,P)}, in_sub={in_subgroup}, 6|k={k%6==0}"

# ── 3-digit extension: ABCABC = ABC × 1001 ───────────────────────────────────

assert 1001 % P == 2    # 1001 = 27×37 + 2

# For ABCABC ≡ T (mod 37): ABC × 2 ≡ T  ⟹  ABC ≡ T × 2^{-1} ≡ T × 19 (mod 37)
# [2 × 19 = 38 ≡ 1 mod 37]
assert (2 * 19) % P == 1   # 19 = 2^{-1} mod 37

base3 = {T: (T * 19) % P for T in SPOKE_ORDER}

# Count valid 3-digit ABCs in [100, 999] per spoke
def count_3digit(residue: int):
    first = residue if residue >= 100 else residue + P * ((100 - residue + P - 1) // P)
    return [(first + k * P) for k in range((999 - first) // P + 1)]

spoke3 = {T: count_3digit(base3[T]) for T in SPOKE_ORDER}
counts3 = {T: len(spoke3[T]) for T in SPOKE_ORDER}
total3 = sum(counts3.values())

# Verify a sample: ABC=19 for T=1: 19×1001=19019, 19019%37?
assert (19 * 1001) % P == 1    # ABC=19 → T=1 ✓

# Verify spot-checks for each spoke
for T in SPOKE_ORDER:
    for abc in spoke3[T][:2]:   # check first two per spoke
        assert (abc * 1001) % P == T, \
            f"FAIL: ABC={abc}, ABCABC%37={( abc*1001)%P} ≠ T={T}"

# 3-digit base residues are in a different range from 2-digit:
# 2-digit multiplier: 27  → base residues = {T × 27^{-1}} = {T × 11}
# 3-digit multiplier:  2  → base residues = {T × 2^{-1}}  = {T × 19}
base2_residues = sorted({(T * 11) % P for T in SUBGROUP})
base3_residues = sorted({(T * 19) % P for T in SUBGROUP})
assert set(base2_residues).isdisjoint(set(base3_residues))   # different sets


# ── Report ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Multiplication-by-2 Orbit Audit")
    print()
    print(f"  2 is primitive root mod 37: ord(2)={ord2}  ✓")
    print(f"  2^6 ≡ {pow(2,6,P)} (mod 37)  ✓")
    print()
    print("  Orbit table — Starting T | k=0..6")
    print(f"  {'T':>4} | " + "  ".join(f"k={k}" for k in range(7)))
    print("  " + "-"*50)
    for T in SPOKE_ORDER:
        row = EXPECTED_TABLE[T]
        in_sub = ["✓" if v in SUBGROUP else " " for v in row]
        cells  = [f"{v:>3}{s}" for v,s in zip(row, in_sub)]
        print(f"  {T:>4} | " + "  ".join(cells))
    print()
    print("  k=0 (start) and k=6 are in ⟨27⟩; k=1..5 are outside  ✓")
    print(f"  2^k ∈ ⟨27⟩ iff 6|k, verified for all k=1..35  ✓")
    print()
    print("  Spoke permutation under T↦27T:")
    print(f"    {SPOKE_ORDER} → {permuted}  (cyclic shift ✓)")
    print()
    print("  2-digit vs 3-digit multiplier switch:")
    print(f"    ABAB   = AB  × 101  ≡ AB  × 27 (mod 37)  [2-digit]")
    print(f"    ABCABC = ABC × 1001 ≡ ABC ×  2 (mod 37)  [3-digit]")
    print(f"    2-digit base residues (×11): {base2_residues}")
    print(f"    3-digit base residues (×19): {base3_residues}")
    print(f"    Sets disjoint: {set(base2_residues).isdisjoint(set(base3_residues))}  ✓")
    print()
    print(f"  3-digit pair counts per spoke (ABC in [100,999]):")
    for T in SPOKE_ORDER:
        print(f"    T={T:2d}  base≡{base3[T]:2d}  count={counts3[T]}  "
              f"first3={spoke3[T][:3]}")
    print(f"  Total 3-digit pairs: {total3}")
    print()
    print("All assertions passed.")
