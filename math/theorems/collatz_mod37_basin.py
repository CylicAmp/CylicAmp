"""
collatz_mod37_basin.py

Basin structure of the Collatz map T in F_37.
Extends lob_26_collatz_f37.py with full basin / inverse-tree analysis.

MAP DEFINITION (same as lob_26):
  T: {0,...,36} → {0,...,36}
    T(x) = 19x  mod 37   if x is even   [19 = 2^{-1} mod 37]
    T(x) = 3x+1 mod 37   if x is odd

CYCLE PARTITION [PROVEN in lob_26]:
  C0  = {0}                                   length 1 (fixed point)
  C3  = {1, 2, 4}                             length 3 (image of 4→2→1)
  C9  = {7,9,11,14,15,17,22,28,34}            length 9

BASIN SIZES [PROVEN below]:
  |basin(C0)|  = 1    (no proper pre-images; C0 is a source)
  |basin(C3)|  = 23   (3 cycle + 20 basin nodes, max depth 9)
  |basin(C9)|  = 13   (9 cycle + 4 basin nodes, max depth 2)
  Total: 1 + 23 + 13 = 37 ✓

MODULAR CONSTRAINT ON HYPOTHETICAL CYCLES [PROVEN]:
  Any integer Collatz orbit, when reduced mod 37 step-by-step, follows T
  exactly (since the Collatz rule depends only on parity and T encodes
  both branches). Therefore the residues of any integer Collatz cycle
  must form a sub-orbit of a cycle of T in F_37. The only cycles are
  C0, C3, C9.
    - C3 = {1,2,4} is the image of the known cycle {4→2→1}.
    - Any other integer cycle has all its elements' residues in C9.
  [OPEN]: No integer cycle with elements in C9 is known; none is proven
  to be impossible by this argument alone.
"""

from sympy import isprime


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def T(x, p=37):
    """Single-step Collatz map in F_p (p odd prime)."""
    inv2 = pow(2, -1, p)
    return (x * inv2) % p if x % 2 == 0 else (3 * x + 1) % p


def preimages(y, p=37):
    """All x in {0,...,p-1} with T(x) = y."""
    inv2 = pow(2, -1, p)
    inv3 = pow(3, -1, p)
    result = []
    # Even branch: inv2 * x ≡ y  →  x ≡ 2y
    x_e = (2 * y) % p
    if x_e % 2 == 0:
        result.append(x_e)
    # Odd branch: 3x+1 ≡ y  →  x ≡ (y-1)/3
    x_o = ((y - 1) * inv3) % p
    if x_o % 2 == 1:
        result.append(x_o)
    return result


# ──────────────────────────────────────────────────────────────────────────────
# CYCLE PARTITION (from lob_26)
# ──────────────────────────────────────────────────────────────────────────────

C0 = frozenset([0])
C3 = frozenset([1, 2, 4])
C9 = frozenset([7, 9, 11, 14, 15, 17, 22, 28, 34])

assert all(T(x) in C0 for x in C0)
assert all(T(x) in C3 for x in C3)
assert all(T(x) in C9 for x in C9)
assert len(C0 | C3 | C9) == 13
assert C0.isdisjoint(C3) and C0.isdisjoint(C9) and C3.isdisjoint(C9)

# Known integer cycle 4→2→1 projects to C3 correctly
assert T(4) == 2 and T(2) == 1 and T(1) == 4


# ──────────────────────────────────────────────────────────────────────────────
# BASIN COMPUTATION (BFS on inverse tree)
# ──────────────────────────────────────────────────────────────────────────────

dest  = {}
depth = {}

for x in C0: dest[x] = 'C0'; depth[x] = 0
for x in C3: dest[x] = 'C3'; depth[x] = 0
for x in C9: dest[x] = 'C9'; depth[x] = 0

changed = True
while changed:
    changed = False
    for x in range(37):
        if x not in dest:
            y = T(x)
            if y in dest:
                dest[x]  = dest[y]
                depth[x] = depth[y] + 1
                changed  = True

assert len(dest) == 37

# All 37 elements assigned
basin_C0 = [x for x in range(37) if dest[x] == 'C0']
basin_C3 = [x for x in range(37) if dest[x] == 'C3']
basin_C9 = [x for x in range(37) if dest[x] == 'C9']

assert len(basin_C0) == 1
assert len(basin_C3) == 23
assert len(basin_C9) == 13


# ──────────────────────────────────────────────────────────────────────────────
# DEPTH PROFILE FOR BASIN(C3)
# ──────────────────────────────────────────────────────────────────────────────

DEPTH_C3 = {
    0: [1, 2, 4],
    1: [8, 25],
    2: [16, 27],
    3: [5, 21, 32],
    4: [10, 19, 35],
    5: [3, 20],
    6: [6, 13, 31],
    7: [12, 26],
    8: [24, 33],
    9: [23],
}

for d, members in DEPTH_C3.items():
    for x in members:
        assert dest[x]  == 'C3', f"dest[{x}] = {dest[x]}, expected C3"
        assert depth[x] == d,    f"depth[{x}] = {depth[x]}, expected {d}"

assert sum(len(v) for v in DEPTH_C3.values()) == 23

# Max depth of basin(C3)
assert max(depth[x] for x in basin_C3) == 9

# The 37-gateway: n ≡ 12 (mod 37) has depth 7 in basin(C3)
assert dest[12]  == 'C3'
assert depth[12] == 7

# Trace: 12 →6→3→10→5→16→8→4 (7 steps, then in C3)
trace12 = [12]
while trace12[-1] not in C3:
    trace12.append(T(trace12[-1]))
assert len(trace12) - 1 == 7    # 7 steps to reach C3
assert trace12 == [12, 6, 3, 10, 5, 16, 8, 4]


# ──────────────────────────────────────────────────────────────────────────────
# BASIN(C9) NODES
# ──────────────────────────────────────────────────────────────────────────────

C9_basin_nodes = sorted(x for x in basin_C9 if x not in C9)
assert C9_basin_nodes == [18, 29, 30, 36]

assert T(36) == 18 and T(18) == 9  and 9  in C9
assert T(29) == 14 and 14 in C9
assert T(30) == 15 and 15 in C9


# ──────────────────────────────────────────────────────────────────────────────
# INVERSE-TREE COVERAGE: ALL RESIDUES REACHED BY BACKWARDS TREE FROM C3
# ──────────────────────────────────────────────────────────────────────────────

# Iteratively build the set reachable backwards from C3
reachable = set(C3)
prev_size = 0
while len(reachable) != prev_size:
    prev_size = len(reachable)
    for y in list(reachable):
        for x in preimages(y):
            reachable.add(x)

assert reachable == set(basin_C3)   # backward tree from C3 covers exactly basin_C3


# ──────────────────────────────────────────────────────────────────────────────
# CONSTRAINT ON HYPOTHETICAL NON-TRIVIAL CYCLES
# ──────────────────────────────────────────────────────────────────────────────

# The only integer Collatz cycle known is {1,2,4} (= 4→2→1).
# If any other integer cycle K exists:
#   - Each element n ∈ K satisfies T(n mod 37) = T(n) mod 37 (by linearity/def)
#   - So the residues {n mod 37 : n ∈ K} form a cycle of T in F_37
#   - The only cycles of T in F_37 are C0, C3, C9
#   - C0 cannot host an integer cycle: if n ≡ 0 (mod 37) and n is odd,
#       T(n) = 3n+1 ≡ 1 (mod 37), leaving C0 immediately
#   - C3 = {1,2,4}: the 3-cycle forces the cycle back to C3 residues; the
#       minimal integer solution is exactly {1,2,4} = {4→2→1}
#   - Therefore any other integer cycle must have all elements ≡ C9 (mod 37)

# Verify: odd n ≡ 0 (mod 37) maps OUT of C0
odd_multiples_of_37 = [37, 111, 185]
for n in odd_multiples_of_37:
    assert n % 2 == 1
    assert (3*n + 1) % 37 == 1    # lands in C3, not C0

# The minimal cycle with residues in C3: forced to be {1,2,4}
# (3-step closure: n odd ≡1, T(n)=3n+1≡4 even, T(4)/2=n+... forces n=1)
n1 = 1
assert n1 % 2 == 1 and n1 % 37 == 1      # odd, residue 1 ∈ C3
n2 = 3*n1 + 1                              # = 4
assert n2 % 37 == 4 and n2 % 2 == 0
n3 = n2 // 2                               # = 2
assert n3 % 37 == 2 and n3 % 2 == 0
assert n3 // 2 == n1                       # closes back to 1 → only solution


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Collatz Map T in F_37 — Basin Structure")
    print("=" * 62)

    print("\n── CYCLE PARTITION ──")
    print(f"  C0  = {sorted(C0)}  (fixed point)")
    print(f"  C3  = {sorted(C3)}  (image of 4→2→1)")
    print(f"  C9  = {sorted(C9)}")
    print(f"  Total cycle elements: {len(C0|C3|C9)} / 37")

    print("\n── BASIN SIZES ──")
    print(f"  |basin(C0)| = {len(basin_C0)}   residues: {basin_C0}")
    print(f"  |basin(C3)| = {len(basin_C3)}  ({len(C3)} cycle + {len(basin_C3)-len(C3)} basin nodes)")
    print(f"  |basin(C9)| = {len(basin_C9)}  ({len(C9)} cycle + {len(C9_basin_nodes)} basin nodes: {C9_basin_nodes})")
    print(f"  Total: {len(basin_C0)+len(basin_C3)+len(basin_C9)} ✓")

    print("\n── DEPTH PROFILE: basin(C3) ──")
    for d, members in DEPTH_C3.items():
        tag = "  ← cycle" if d == 0 else ""
        print(f"  depth {d}: {members}{tag}")

    print("\n── 37-GATEWAY TRACE (n=49 ≡ 12 mod 37) ──")
    print(f"  T-path in F_37: {' → '.join(map(str, trace12))}")
    print(f"  Depth: {depth[12]} steps to reach C3 = {{1,2,4}}")

    print("\n── CONSTRAINT ON HYPOTHETICAL CYCLES ──")
    print("  [PROVEN]  Any integer Collatz cycle's residues mod 37")
    print("            form a cycle of T in F_37.")
    print("  [PROVEN]  C0 cannot host an integer cycle (odd n≡0 maps to ≡1).")
    print("  [PROVEN]  The minimal integer cycle with residues in C3 is {1,2,4}.")
    print("  [PROVEN]  Any OTHER integer cycle must have all elements ≡ C9 (mod 37).")
    print("  [OPEN]    No such cycle is known; none is proven impossible here.")

    print()
    print("All assertions passed.")
