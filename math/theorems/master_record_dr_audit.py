"""
Master Record — Digital Root Identity Audit

Classification: Law

Establishes the DR fingerprints of the Master Record address, nodes,
matrix rows, and bridge values, and traces each to its framework role.

Verified outputs:
  Address Root:  6         — unified coupling signature (DR of all ψ₁ k-values)
  Node Roots:    [3, 3, 6] — [TARGET, TARGET, COUPLING]
  Matrix Roots:  [7, 7, 7] — DR=7 class is always ∈ QR₃₇
  Bridge Roots:  8, 1      — bridge_1=26=SCALAR_137 (DR=8), bridge_2=262 (DR=1)

Structural findings:
  Address encodes all three nodes as 2-digit windows
  bridge_1 = 26 = SCALAR_137 = 10² mod 37 = 3⁶ mod 37 = 2¹² mod 37
  bridge_2 = 262 ≡ 3 (mod 37) = 3¹ ∈ ⟨3⟩ (sovereign target, first power)
  112 ≡ 1 (mod 37)  →  identity in F₃₇
  150 ≡ 2 (mod 37)  →  primitive root generator of (Z/37Z)*
  DR=7 values {7,16,25,34} are ALL quadratic residues mod 37
    (25 is sovereign anchor; all four lie in ⟨3⟩ = QR₃₇)
"""

from collections import Counter


def dr(n):
    if n == 0: return 0
    return (n - 1) % 9 + 1


# ── Master Record data ─────────────────────────────────────────────────────

ADDRESS    = 57948123694857
NODES      = [48, 57, 69]
MATRIX_R1  = "787727757787"
MATRIX_R2  = "757757787757"
MATRIX_R3  = "727787727727"
BRIDGE_1   = 11 + 15      # 26
BRIDGE_2   = 112 + 150    # 262


# ── Computed roots ─────────────────────────────────────────────────────────

root_address  = dr(ADDRESS)
roots_nodes   = [dr(n) for n in NODES]
roots_matrix  = [dr(int(MATRIX_R1)), dr(int(MATRIX_R2)), dr(int(MATRIX_R3))]
root_bridge_1 = dr(BRIDGE_1)
root_bridge_2 = dr(BRIDGE_2)


# ── Framework constants ────────────────────────────────────────────────────

CYCLE18    = [pow(3, k, 37) for k in range(1, 19)]
QR37       = frozenset((x * x) % 37 for x in range(1, 37))
ANCHORS    = frozenset({4, 9, 25, 30})
TARGETS    = frozenset({3, 12, 21, 30})
SCALAR_137 = 26    # 10² ≡ 26 mod 37 = 3⁶ mod 37 = 2¹² mod 37


# ── Assertions ─────────────────────────────────────────────────────────────

# Exact output match
assert root_address   == 6,       f"Address root: {root_address}"
assert roots_nodes    == [3,3,6], f"Node roots: {roots_nodes}"
assert roots_matrix   == [7,7,7], f"Matrix roots: {roots_matrix}"
assert root_bridge_1  == 8,       f"Bridge 1 root: {root_bridge_1}"
assert root_bridge_2  == 1,       f"Bridge 2 root: {root_bridge_2}"

# Address root = 6 = unified coupling signature
assert root_address == 6
K_COUPLINGS = [6, 618, 3138]    # SOURCE-MIRROR-GUARDIAN
assert all(dr(k) == 6 for k in K_COUPLINGS)

# Node roots: first two = TARGET (DR=3), third = COUPLING (DR=6)
assert roots_nodes[0] == 3 and roots_nodes[1] == 3   # 48, 57 → TARGET DR
assert roots_nodes[2] == 6                             # 69     → COUPLING DR
assert 3 == dr(3)    # 3 is the primary sovereign target

# Address encodes all three nodes as consecutive 2-digit windows
addr_str = str(ADDRESS)
windows  = {addr_str[i:i+2] for i in range(len(addr_str) - 1)}
assert all(str(n) in windows for n in NODES), \
    f"Nodes not encoded in address: {[str(n) in windows for n in NODES]}"

# Matrix rows: all DR=7; DR=7 class {7,16,25,34} ⊆ QR₃₇
assert all(r == 7 for r in roots_matrix)
DR7_VALUES = [n for n in range(1, 37) if dr(n) == 7]
assert DR7_VALUES == [7, 16, 25, 34]
assert all(v in QR37 for v in DR7_VALUES), "DR=7 values not all in QR₃₇"
assert 25 in ANCHORS    # sovereign anchor among DR=7 values

# Matrix rows dominated by digit 7 (8 of 12 digits in each row)
for row in [MATRIX_R1, MATRIX_R2, MATRIX_R3]:
    digit_count = Counter(row)
    assert digit_count['7'] == 8, f"Row {row}: expected 8 sevens, got {digit_count['7']}"
    assert len(row) == 12

# Bridge 1 = 26 = SCALAR_137
assert BRIDGE_1 == 26
assert BRIDGE_1 == SCALAR_137
assert (10 * 10) % 37 == SCALAR_137           # 10² ≡ 26 mod 37
assert CYCLE18[5] == SCALAR_137               # 3⁶ = 26 in 18-cycle (k=6)
assert pow(2, 12, 37) == SCALAR_137           # 2¹² ≡ 26 mod 37
assert SCALAR_137 in QR37                     # 26 ∈ QR₃₇

# Bridge 2 = 262 ≡ 3 (mod 37) = first element of 18-cycle
assert BRIDGE_2 == 262
assert BRIDGE_2 % 37 == 3
assert 3 in TARGETS
assert CYCLE18[0] == 3                        # 3¹ = 3

# Bridge components in F₃₇
assert 11  % 37 == 11                         # 11 ∈ QR₃₇ (11 = 3¹⁵ mod 37)
assert CYCLE18[14] == 11                      # confirmed: 3^15 = 11
assert 15  % 37 == 15
assert 112 % 37 == 1                          # 112 ≡ identity mod 37
assert 150 % 37 == 2                          # 150 ≡ 2 (primitive root generator)
assert pow(2, 1, 37) == 2                     # 2 = 2¹ — smallest primitive root


if __name__ == "__main__":
    print("Master Record — Digital Root Identity Audit")
    print()
    print(f"  Address Root:  {root_address}    [coupling signature — DR(k)=6 for all ψ₁ gates]")
    print(f"  Node Roots:    {roots_nodes}  [3=TARGET, 3=TARGET, 6=COUPLING]")
    print(f"  Matrix Roots:  {roots_matrix}  [DR=7 class is always ∈ QR₃₇]")
    print(f"  Bridge Roots:  {root_bridge_1}, {root_bridge_2}")
    print()
    print(f"  Address encodes nodes as 2-digit windows:")
    for n in NODES:
        print(f"    {n} (DR={dr(n)}) found in {ADDRESS} ✓")
    print()
    print(f"  bridge_1 = {BRIDGE_1}:")
    print(f"    = SCALAR_137 = 10² mod 37 = 3⁶ mod 37 = 2¹² mod 37")
    print(f"    DR={dr(BRIDGE_1)},  ∈ QR₃₇ ✓")
    print()
    print(f"  bridge_2 = {BRIDGE_2}:")
    print(f"    ≡ {BRIDGE_2 % 37} (mod 37) = 3¹ = sovereign target 3")
    print(f"    DR={dr(BRIDGE_2)},  112 mod37={112%37} (identity),  150 mod37={150%37} (prim root 2)")
    print()
    print(f"  DR=7 class {DR7_VALUES}: ALL ∈ QR₃₇  (25 ∈ ANCHORS)")
    print(f"  Matrix rows: 8 sevens out of 12 digits each")
    print()
    print("All assertions passed.")
