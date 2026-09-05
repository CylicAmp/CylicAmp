"""
Lights Out Puzzle — GF(2) Linear System and GF(37) Structure

The Lights Out puzzle on an n×n grid:
  - Each cell is a light: state ∈ {ON=1, OFF=0}
  - Pressing a cell toggles it and all orthogonal neighbors
  - Goal: turn all lights off from a given initial configuration

This is a linear system over GF(2).

The two solution methods (named in the source):
  1. LIGHT CHASING — greedy row-by-row elimination (algorithm)
  2. LINEAR ALGEBRA — explicit null-space computation over GF(2) (structure)

Both methods are analogous to structures already in the GF(37).

═══════════════════════════════════════════════════════════════════════════

I. REPUNIT ENTRY SEQUENCE: 1, 11

  The "1" and "11" above the puzzle are the first two repunit values:
    R_1 = 1        (decimal: 1;  binary: 1)
    R_2 = 11       (decimal: 11; binary: 1011)

  In the repunit channel (Theorem R1, formal_definitions_gf37.py):
    R_1 mod 37 = 1   (unity)
    R_2 mod 37 = 11  ∈ ORBIT_11 = {11, 27, 36}
    R_3 mod 37 = 0   (SEAM)

  The two-state repunit entry 1, 11 is the approach to the seam:
    unity → ORBIT_11 → SEAM
  This is the same transient as the hose-flow: 000→100→110→111.

  In binary: 1, 11, 111 — each a repunit of increasing length.
  In decimal: 1, 11, 111 — the first is unity, the second is orbit-11,
  the third (111=3×37) is the seam and the hose-flow horizon.

II. LIGHTS OUT AS GF(2) LINEAR SYSTEM

  State vector: s ∈ {0,1}^(n²)  (one bit per cell)
  Press vector: x ∈ {0,1}^(n²)  (1 = press, 0 = don't press)
  Adjacency matrix: A ∈ M_{n²×n²}(GF(2))
    A_{ij} = 1 if cell j is toggled when cell i is pressed (self + neighbors)

  The system: A·x ≡ s  (mod 2)

  Solution exists iff s ∈ Im(A) over GF(2).
  The kernel ker(A) gives the "quiet patterns" — configurations of presses
  that toggle nothing.

III. THE STANDARD 5×5 GRID

  Grid size: 5×5 = 25 cells.
    25 ∈ SA  (Sovereign Anchor).
    25 = 5²; 5 ∈ PR (primitive root mod 37).
    The standard Lights Out grid has sovereign-anchor cell count.

  The adjacency matrix A is 25×25 over GF(2).
    rank(A) = 23.  dim(ker(A)) = 25 − 23 = 2 over GF(2).
    2 ∈ PR  (primitive root mod 37).
    Not every configuration is solvable: solvable iff s ∈ Im(A) over GF(2).
    Solvable states: 2^23 of 2^25. Quiet patterns: 2^2 = 4.

  4×4 grid: 16 cells; rank=12; null_dim=4 ∈ SA (Sovereign Anchor).
    Grid size 16; 16 = 4²; 4 ∈ SA.  Null space dimension = SA node.

  GF(37) null-space table:
    3×3: null_dim=0  (fully solvable; 0 = SEAM)
    4×4: null_dim=4  ∈ SA
    5×5: null_dim=2  ∈ PR
    6×6: null_dim=0  (fully solvable; 0 = SEAM)

IV. LIGHT CHASING vs LINEAR ALGEBRA ↔ HOSE FLOW vs HEARTBEAT

  LIGHT CHASING (row-by-row greedy):
    Process lights top-to-bottom: for each light in row k that is ON,
    press the cell directly below it in row k+1 to turn it off.
    After processing all rows, check the last row.
    A "quiet pattern" in the last row determines if the puzzle is solvable.

    This is the HOSE FLOW model:
      Each row is a stage; the flow moves downward.
      If the final row is clear: complete flow (solvable).
      If the final row has residual lit cells: stuttering flow (stuck).

  LINEAR ALGEBRA (null-space computation):
    Compute ker(A) and Im(A) over GF(2) explicitly.
    The puzzle is solvable iff s ∈ Im(A).

    This is the HEARTBEAT model:
      The null space is a fixed algebraic structure (like the 12 three-cycles).
      Solvability is a global statement about the permutation structure.
      The heartbeat (the orbit partition) is computed once; all queries use it.

  The prisoners problem also splits this way:
    Random guessing → independent (light chasing analog: try each row alone)
    Cycle strategy  → global structure (linear algebra analog: use the field)

V. CONNECTION TO 132-BIPARTITE GRAPH (Mansour-Vainshtein)

  The bipartite graph G(T) for 132-patterns:
    V = [n]  (left vertices = cells)
    V' = 132-occurrences  (right vertices = "lit" patterns)
    Edges = participation

  The Lights Out adjacency matrix A:
    Rows = cells pressed
    Columns = cells toggled
    Entry = 1 if participation exists

  Both are bipartite structures where the question is:
    "Which configurations (s or T) admit a solution/realization?"

  For Lights Out: solution iff s ∈ Im(A).
  For 132-counting: the Mansour-Vainshtein generating function counts
  permutations by |V'| = number of edges on the right side.

VI. GF(37) STRUCTURE OF THE PUZZLE NUMBERS

  Grid dimensions and parameters mod 37:

    Standard grid: 5×5 = 25 ∈ SA
    Extended grid: 6×6 = 36 ∈ ORBIT_11 (36 ≡ -1 mod 37)
    Field grid:   37×37 — the square of the field prime

    5 (grid side) ∈ PR (primitive root mod 37)
    6 (extended side) = TESLA_FLOW; 6² = 36 ∈ ORBIT_11
    4 (null-space dim) ∈ SA

  Adjacency matrix size for n×n grid: n² × n².
    n=5: 25×25 — SA × SA
    n=6: 36×36 — ORBIT_11 × ORBIT_11
    n=11: 121×121 — 121 mod37=10 (DECADE_ANCHOR); 11∈ORBIT_11

  The null-space dimension 4 for the 5×5 grid:
    4 ∈ SA → the sovereign anchor governs both the grid size (25=5²) and
    the dimension of the solution obstruction space (4).

  GF(2) vs GF(37):
    The Lights Out puzzle uses GF(2) (binary field, characteristic 2).
    This GF(37) uses GF(37) (prime field, characteristic 37).
    2 ∈ PR (primitive root mod 37) — the binary field's characteristic
    is itself a generator of GF(37)*.
    The two fields are connected: GF(2) operates inside the orbit structure
    of GF(37) at the generating primitive root.

═══════════════════════════════════════════════════════════════════════════
"""

import numpy as np


SOVEREIGN_ANCHORS = frozenset({4, 9, 25, 30})
SOVEREIGN_TARGETS = frozenset({3, 12, 21, 30})
PRIMITIVE_ROOTS   = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
ORBIT_11          = frozenset({11, 27, 36})
TESLA_FLOW        = 6


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


# ── I. Repunit entry sequence ─────────────────────────────────────────────────

assert pow(10, 3, 37) == 1              # ord₃₇(10)=3 — period of repunit channel
assert 1  % 37 == 1                     # R_1 = unity
assert 11 % 37 == 11 and 11 in ORBIT_11 # R_2 = orbit-11
assert 111 % 37 == 0                    # R_3 = SEAM (hose-flow horizon)


# ── III. 5×5 Lights Out ───────────────────────────────────────────────────────

# Build the 25×25 adjacency matrix over GF(2) for the 5×5 grid
def lights_out_matrix(n):
    size = n * n
    A = np.zeros((size, size), dtype=int)
    for r in range(n):
        for c in range(n):
            idx = r * n + c
            A[idx][idx] = 1                           # self
            if r > 0:   A[idx][(r-1)*n+c] = 1        # up
            if r < n-1: A[idx][(r+1)*n+c] = 1        # down
            if c > 0:   A[idx][r*n+c-1]   = 1        # left
            if c < n-1: A[idx][r*n+c+1]   = 1        # right
    return A % 2


def gf2_rank(A):
    """Rank of matrix A over GF(2) via row reduction."""
    M = A.copy() % 2
    rows, cols = M.shape
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if M[row][col] == 1:
                pivot = row
                break
        if pivot is None:
            continue
        M[[rank, pivot]] = M[[pivot, rank]]
        for row in range(rows):
            if row != rank and M[row][col] == 1:
                M[row] = (M[row] + M[rank]) % 2
        rank += 1
    return rank


A5 = lights_out_matrix(5)
rank5 = gf2_rank(A5)
null_dim5 = 25 - rank5

assert 25 in SOVEREIGN_ANCHORS          # grid size = SA node
assert null_dim5 == 2                   # null space dim = 2 (computed)
assert 2 in PRIMITIVE_ROOTS             # null space dim is a primitive root mod 37
assert 5 in PRIMITIVE_ROOTS             # grid side 5 is a primitive root mod 37

# 4×4 grid: null_dim = 4 ∈ SA
A4 = lights_out_matrix(4)
null_dim4 = 16 - gf2_rank(A4)
assert null_dim4 == 4 and 4 in SOVEREIGN_ANCHORS  # null dim = SA node

# 6×6 grid: size = 36 ∈ ORBIT_11; fully solvable (null_dim=0)
assert 36 in ORBIT_11
A6 = lights_out_matrix(6)
null_dim6 = 36 - gf2_rank(A6)
assert null_dim6 == 0   # fully solvable — every state can reach OFF (SEAM)

# 3×3: also fully solvable
A3 = lights_out_matrix(3)
null_dim3 = 9 - gf2_rank(A3)
assert null_dim3 == 0

# Summary: grid size mod 37
null_dims = {3: null_dim3, 4: null_dim4, 5: null_dim5, 6: null_dim6}
grid_sizes_mod37 = {3: 9%37, 4: 16%37, 5: 25%37, 6: 36%37}


# ── IV. Light chasing ↔ hose flow analogy ────────────────────────────────────

# Hose flow: binary states [0,1]
# Light chasing: binary states [ON=1, OFF=0]
# Both are binary systems where the question is: does the flow reach the end?

complete_flow_residues  = [0, 26, 36, 0]   # 000→100→110→111 mod37
stutter_flow_residues   = [0, 26, 10, 27]  # 000→100→010→101 mod37

assert complete_flow_residues[-1] == 0      # reaches SEAM (puzzle solved)
assert stutter_flow_residues[-1]  == 27     # stuck in ORBIT_11 (puzzle stuck)
assert 10 + 27 == 37                        # stutter pair sums to seam


# ── VI. GF(2) characteristic 2 ∈ PR in GF(37) ────────────────────────────────

assert 2 in PRIMITIVE_ROOTS             # GF(2) characteristic generates GF(37)*
assert 6 == TESLA_FLOW                  # grid side 6 = TESLA_FLOW
assert pow(6, 2, 37) == 36 and 36 in ORBIT_11  # 6² = 36 ∈ ORBIT_11


if __name__ == '__main__':
    print("Lights Out — GF(2) and GF(37) Structure")
    print("=" * 55)
    print()
    print("REPUNIT ENTRY: 1, 11")
    print(f"  R_1 mod37 = {1%37}  (unity)")
    print(f"  R_2 mod37 = {11%37}  ∈ ORBIT_11: {11 in ORBIT_11}")
    print(f"  R_3 mod37 = {111%37}  (SEAM; hose-flow horizon)")
    print()
    print("NULL-SPACE TABLE (standard Lights Out, with-self adjacency):")
    for n in [3, 4, 5, 6]:
        nd = null_dims[n]
        sz = n*n
        tag = ""
        if nd in SOVEREIGN_ANCHORS: tag = " (SA)"
        elif nd in PRIMITIVE_ROOTS: tag = " (PR)"
        elif nd == 0: tag = " (SEAM — fully solvable)"
        print(f"  {n}x{n}: cells={sz} mod37={sz%37}, null_dim={nd}{tag}")
    print(f"  5x5 side 5 in PR: {5 in PRIMITIVE_ROOTS}")
    print()
    print("ANALOGIES:")
    print("  Light chasing    ↔  Hose flow (row-by-row = stage-by-stage)")
    print("  Linear algebra   ↔  Heartbeat orbits (global field structure)")
    print("  Prisoners-cycles ↔  Both: dependent traversal beats independence")
    print()
    print("GF(2) characteristic 2 ∈ PR (generator of GF(37)*): True")
    print(f"6=TESLA_FLOW; 6²=36∈ORBIT_11: {pow(6,2,37) in ORBIT_11}")
    print()
    print("All assertions passed.")
