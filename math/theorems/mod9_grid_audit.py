#!/usr/bin/env python3
"""
mod9_grid_audit.py

Grid: val(x,y) = (x*A + y*B) % 9   for x,y ∈ {0,1,...,8}
Baseline: A=1, B=1  →  val = (x+y) % 9

DOMAINS COVERED:
  1.  Grid construction and display
  2.  Latin square verification (row, column, full)
  3.  Value frequency / density analysis
  4.  Row sums, column sums, diagonal sums
  5.  Anti-diagonal constant: x+y=8 → all cells = 8
  6.  Level sets: geometry of iso-value lines
  7.  Slope of iso-value lines: -A/B (real slope analogy)
  8.  Cayley table of Z₉ under addition (A=B=1 case)
  9.  DR bridge: shift 0→9, recovering digital root convention 1..9
  10. DR addition table verification
  11. Parameter sweep: all (A,B) ∈ Z₉² — Latin vs non-Latin classification
  12. gcd(A,9) / gcd(B,9) determines Latin property
  13. Track identification: T₂₄, T₅₇, T₈₁ positions in the grid
  14. Twin prime constraint: DR(p)∈{2,5,8} — grid positions and neighbors
  15. Density: non-Latin grids show value clustering (gcd > 1 effect)
  16. Full assertion battery — zero skipped, zero assumed

─────────────────────────────────────────────────────────────────
COPY-PASTE READY: run with  python3 mod9_grid_audit.py
Requires: Python 3.6+, stdlib only (math, collections, itertools)
─────────────────────────────────────────────────────────────────
"""

import math
from collections import Counter

FAIL = []

def check(cond, label, actual=None, expected=None):
    if not cond:
        FAIL.append(f"  ✗  {label}  actual={actual!r}  expected={expected!r}")
    return cond

# ══════════════════════════════════════════════════════════════════
# 1. GRID CONSTRUCTION
# ══════════════════════════════════════════════════════════════════

N = 9

def make_grid(A, B, N=9):
    """val(x,y) = (x*A + y*B) % N.  x=column, y=row."""
    return [[(x * A + y * B) % N for x in range(N)] for y in range(N)]

def print_grid(grid, label="", N=9):
    print(f"\n  {label}")
    header = "      " + "  ".join(f"x={x}" for x in range(N))
    print(f"  {header}")
    print("  " + "─" * (N * 5 + 4))
    for y, row in enumerate(grid):
        cells = "  ".join(f"{v:2d}" for v in row)
        print(f"  y={y} │  {cells}")
    print("  " + "─" * (N * 5 + 4))

# ══════════════════════════════════════════════════════════════════
# 2. LATIN SQUARE VERIFICATION
# ══════════════════════════════════════════════════════════════════

def latin_square_check(grid, N=9):
    rows_ok = all(sorted(row) == list(range(N)) for row in grid)
    cols = [[grid[y][x] for y in range(N)] for x in range(N)]
    cols_ok = all(sorted(col) == list(range(N)) for col in cols)
    return {'latin': rows_ok and cols_ok, 'rows': rows_ok, 'cols': cols_ok}

# ══════════════════════════════════════════════════════════════════
# 3. VALUE FREQUENCY / DENSITY
# ══════════════════════════════════════════════════════════════════

def value_freq(grid):
    return Counter(v for row in grid for v in row)

# ══════════════════════════════════════════════════════════════════
# 4. ROW / COLUMN / DIAGONAL SUMS
# ══════════════════════════════════════════════════════════════════

def row_sums(grid, N=9):
    return [sum(row) for row in grid]

def col_sums(grid, N=9):
    return [sum(grid[y][x] for y in range(N)) for x in range(N)]

def main_diagonal(grid, N=9):
    return [grid[i][i] for i in range(N)]

def anti_diagonal(grid, N=9):
    return [grid[i][N - 1 - i] for i in range(N)]

def diag_sum_k(grid, k, N=9):
    """Sum of cells where x+y ≡ k (mod N)."""
    return sum(grid[y][x] for y in range(N) for x in range(N) if (x+y) % N == k)

# ══════════════════════════════════════════════════════════════════
# 5. LEVEL SETS
# ══════════════════════════════════════════════════════════════════

def level_sets(grid, N=9):
    ls = {c: [] for c in range(N)}
    for y in range(N):
        for x in range(N):
            ls[grid[y][x]].append((x, y))
    return ls

# ══════════════════════════════════════════════════════════════════
# 6. SLOPE OF ISO-VALUE LINES
# ══════════════════════════════════════════════════════════════════

def slope_str(A, B, N=9):
    """
    Iso-value lines satisfy A*x + B*y ≡ c (mod N).
    Real-valued slope analogy: dy/dx = -A/B.
    When B=0: lines are vertical (x = const, since A≠0).
    When A=0: lines are horizontal (y = const).
    """
    if B % N == 0 and A % N == 0:
        return "undefined (A=B=0, all cells equal)"
    if B % N == 0:
        return "vertical  (B≡0 mod 9, x fixed per level set)"
    if A % N == 0:
        return "horizontal (A≡0 mod 9, y fixed per level set)"
    g = math.gcd(abs(A), abs(B))
    num, den = -A // g, B // g
    if den < 0:
        num, den = -num, -den
    return f"{num}/{den}" if den != 1 else f"{num}"

# ══════════════════════════════════════════════════════════════════
# 7. DR BRIDGE: 0 → 9
# ══════════════════════════════════════════════════════════════════

def dr_shift(grid, N=9):
    """Map 0 → N (digital root convention: values run 1..9, not 0..8)."""
    return [[(v if v != 0 else N) for v in row] for row in grid]

def dr(n):
    if n == 0:
        return 0
    r = n % 9
    return r if r else 9

def verify_dr_addition_table(grid_dr, N=9):
    """
    Z₉ element 0 (x=0 or y=0) represents digit 9, since 9 mod 9 = 0.
    Z₉ elements 1..8 (x=1..8, y=1..8) represent digits 1..8.
    So: digit(x) = x if x != 0 else 9.  Same for y.
    Then grid_dr[y][x] = DR(digit(x) + digit(y)) for all x,y ∈ {0..8}.
    """
    errors = []
    for y in range(N):
        for x in range(N):
            a = x if x != 0 else N   # digit: 9 when x=0, else x
            b = y if y != 0 else N   # digit: 9 when y=0, else y
            expected = dr(a + b)
            actual = grid_dr[y][x]
            if actual != expected:
                errors.append(f"DR({a}+{b})={expected} but grid={actual}")
    return errors

# ══════════════════════════════════════════════════════════════════
# 8. PARAMETER SWEEP
# ══════════════════════════════════════════════════════════════════

def sweep(N=9):
    latin_pairs, non_latin = [], []
    for A in range(N):
        for B in range(N):
            G = make_grid(A, B, N)
            ls = latin_square_check(G, N)
            freq = value_freq(G)
            if ls['latin']:
                latin_pairs.append((A, B))
            else:
                non_latin.append((A, B, dict(freq)))
    return latin_pairs, non_latin

# ══════════════════════════════════════════════════════════════════
# 9. TRACK IDENTIFICATION IN GRID
# ══════════════════════════════════════════════════════════════════

# Twin prime tracks (DR values in digital root convention 1..9):
TRACK_T24 = {2, 4}   # DR(p)=2, DR(p+2)=4
TRACK_T57 = {5, 7}   # DR(p)=5, DR(p+2)=7
TRACK_T81 = {8, 1}   # DR(p)=8, DR(p+2)=1 (DR(10)=1)

# DR values of twin prime p>3: only {2,5,8}
TWIN_P_DR = {2, 5, 8}

def track_positions(grid_dr, N=9):
    """
    In the DR-shifted grid, find positions of TWIN_P_DR values {2,5,8}.
    Also identify which track each belongs to and their +2 neighbors.
    """
    results = {}
    for v in TWIN_P_DR:
        positions = [(x, y) for y in range(N) for x in range(N) if grid_dr[y][x] == v]
        results[v] = positions
    return results

# ══════════════════════════════════════════════════════════════════
# MAIN AUDIT
# ══════════════════════════════════════════════════════════════════

def run():
    print("MOD-9 GRID AUDIT")
    print("=" * 66)
    print(f"  val(x,y) = (x·A + y·B) mod 9     x = column, y = row")

    # ── SECTION 1: BASELINE A=1, B=1 ────────────────────────────
    A, B = 1, 1
    G = make_grid(A, B, N)
    print_grid(G, f"BASELINE  A={A}, B={B}  →  val = (x+y) mod 9")

    # ── SECTION 2: LATIN SQUARE ──────────────────────────────────
    ls = latin_square_check(G, N)
    check(ls['latin'], "A=1,B=1 is Latin square")
    check(ls['rows'],  "A=1,B=1 rows are Latin")
    check(ls['cols'],  "A=1,B=1 cols are Latin")
    print(f"\n  ─ LATIN SQUARE")
    print(f"  Rows Latin: {ls['rows']}   Cols Latin: {ls['cols']}   Full: {ls['latin']}")

    # ── SECTION 3: VALUE FREQUENCY ───────────────────────────────
    freq = value_freq(G)
    expected_count = N   # each value appears N times in an N×N Latin square
    for v in range(N):
        check(freq[v] == expected_count, f"value {v} appears {N}×", freq[v], expected_count)
    print(f"\n  ─ VALUE FREQUENCIES  (each must = {N})")
    for v in range(N):
        bar = "█" * freq[v]
        print(f"    val {v}: {freq[v]:2d}  {bar}")

    # ── SECTION 4: ROW / COLUMN / DIAGONAL SUMS ──────────────────
    rs = row_sums(G, N)
    cs = col_sums(G, N)
    expected_sum = sum(range(N))   # 0+1+...+8 = 36
    grand_total  = N * expected_sum  # 9 × 36 = 324
    for i in range(N):
        check(rs[i] == expected_sum, f"row {i} sum", rs[i], expected_sum)
        check(cs[i] == expected_sum, f"col {i} sum", cs[i], expected_sum)
    check(sum(rs) == grand_total, "grand total", sum(rs), grand_total)
    print(f"\n  ─ SUMS")
    print(f"  Expected row/col sum: {expected_sum}  (= 0+1+…+8)")
    print(f"  Row sums: {rs}")
    print(f"  Col sums: {cs}")
    print(f"  Grand total: {sum(rs)}  (= {N} × {expected_sum})")

    # ── SECTION 5: DIAGONALS ─────────────────────────────────────
    md = main_diagonal(G, N)
    ad = anti_diagonal(G, N)
    expected_md = [(2 * k) % N for k in range(N)]   # (k+k) mod 9
    expected_ad = [8] * N                             # x+(8-x)=8 always
    check(md == expected_md, "main diagonal = [2k mod 9]", md, expected_md)
    check(ad == expected_ad, "anti-diagonal all = 8",      ad, expected_ad)
    print(f"\n  ─ DIAGONALS  (A=B=1)")
    print(f"  Main diagonal (x=y):   {md}   sum={sum(md)}")
    print(f"    Explanation: val(k,k) = (k+k) mod 9 = 2k mod 9")
    print(f"  Anti-diagonal (x+y=8): {ad}   sum={sum(ad)}")
    print(f"    Explanation: val(x,8-x) = (x+8-x) mod 9 = 8  (constant)")

    # Diagonal-sum sweep: sum of cells on each diagonal x+y ≡ k (mod 9)
    diag_sums = [diag_sum_k(G, k, N) for k in range(N)]
    # Each diagonal has exactly N cells, each with value k → sum = N*k
    expected_diag_sums = [N * k for k in range(N)]
    for k in range(N):
        check(diag_sums[k] == expected_diag_sums[k],
              f"diag k={k} sum", diag_sums[k], expected_diag_sums[k])
    print(f"\n  Diagonal sums (x+y ≡ k mod 9 → sum = 9·k):")
    for k in range(N):
        print(f"    k={k}: sum={diag_sums[k]}  (= 9×{k})")

    # ── SECTION 6: LEVEL SETS ─────────────────────────────────────
    ls_sets = level_sets(G, N)
    print(f"\n  ─ LEVEL SETS  (cells sharing value c)")
    for c in range(N):
        pts = ls_sets[c]
        check(len(pts) == N, f"level set {c} has {N} points", len(pts), N)
        for (x, y) in pts:
            check((x + y) % N == c, f"({x},{y}) on level set {c}", (x+y)%N, c)
        # Verify all points lie on x+y = c (with wraparound at the boundary)
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        print(f"    c={c}: x+y ≡ {c} (mod 9)  →  {pts}")

    # ── SECTION 7: SLOPE ─────────────────────────────────────────
    print(f"\n  ─ SLOPE OF ISO-VALUE LINES  (A=1, B=1)")
    s = slope_str(A, B, N)
    print(f"  dy/dx analogy = -A/B = -{A}/{B} = {s}")
    print(f"  Meaning: along a constant-value line, for every 1 step right (Δx=+1)")
    print(f"           take 1 step up (Δy=-1) to stay on the same value.")
    print(f"  These are the diagonals: x+y = constant.")

    # ── SECTION 8: CAYLEY TABLE OF Z₉ ────────────────────────────
    cayley_ok = all(
        G[y][x] == (x + y) % N
        for y in range(N) for x in range(N)
    )
    check(cayley_ok, "grid is Cayley table of Z₉ under +")
    print(f"\n  ─ GROUP THEORY")
    print(f"  Cayley table of Z₉ (additive group): {cayley_ok}")
    print(f"  Group order: 9   Identity element: 0   (col x=0 = col y=0 = identity row/col)")
    # Identity check: row y=0 = [0,1,2,...,8] = column x=0
    check(G[0] == list(range(N)),        "identity row (y=0)",    G[0],            list(range(N)))
    check([G[y][0] for y in range(N)] == list(range(N)),
          "identity col (x=0)",
          [G[y][0] for y in range(N)], list(range(N)))
    # Inverse: a + (-a mod 9) = 0
    for a in range(N):
        inv = (-a) % N
        check(G[a][inv] == 0, f"inverse of {a} is {inv}", G[a][inv], 0)
    print(f"  Inverses verified: " + "  ".join(f"{a}⁻¹={(-a)%N}" for a in range(N)))

    # ── SECTION 9: DR BRIDGE ─────────────────────────────────────
    G_dr = dr_shift(G, N)
    print_grid(G_dr, "DR BRIDGE: shift 0→9  (digital root convention 1..9)")
    dr_freq = value_freq(G_dr)
    for v in range(1, N + 1):
        check(dr_freq[v] == N, f"DR value {v} appears {N}×", dr_freq[v], N)
    print(f"  DR-shifted frequencies: {dict(sorted(dr_freq.items()))}  (each = {N})")

    # DR addition table verification
    dr_errors = verify_dr_addition_table(G_dr, N)
    check(len(dr_errors) == 0, "DR addition table matches DR(a+b)", len(dr_errors), 0)
    if dr_errors:
        for e in dr_errors[:5]:
            print(f"  DR error: {e}")
    else:
        print(f"\n  DR addition table: grid[y][x] = DR(digit(x)+digit(y)) for all x,y ∈ {{0..8}}")
        print(f"  digit(k) = k for k=1..8; digit(0) = 9  (Z₉ element 0 represents digit 9)")
        print(f"  Verified: all 81 cells match.")

    # Key DR addition facts from the table
    print(f"\n  Key DR addition facts (reading from DR-shifted grid):")
    key_pairs = [(9,9),(1,8),(5,4),(3,6),(7,2),(8,1),(6,3),(2,7)]
    for (a,b) in key_pairs:
        xi = a % N   # Z₉ index: digit 9 → 0, digits 1..8 → 1..8
        yi = b % N
        gv = G_dr[yi][xi]
        expected = dr(a+b)
        check(gv == expected, f"DR({a}+{b})", gv, expected)
        print(f"    DR({a}+{b}) = DR({a+b}) = {expected}  ← grid[{yi}][{xi}] = {gv}")

    # ── SECTION 10: PARAMETER SWEEP ──────────────────────────────
    print(f"\n  ─ PARAMETER SWEEP  A,B ∈ {{0,...,8}}")
    latin_pairs, non_latin = sweep(N)
    check(len(latin_pairs) + len(non_latin) == N * N,
          "sweep covers all 81 pairs",
          len(latin_pairs) + len(non_latin), N * N)
    print(f"  Total (A,B) pairs: {N*N}")
    print(f"  Latin square:     {len(latin_pairs)}")
    print(f"  Non-Latin:        {len(non_latin)}")

    print(f"\n  Latin square pairs:")
    for A_val in range(N):
        Bs = [B for (A2,B) in latin_pairs if A2 == A_val]
        if Bs:
            print(f"    A={A_val}: B ∈ {Bs}")

    print(f"\n  Non-Latin sample (A,B → value frequencies):")
    for (Av, Bv, fq) in non_latin[:12]:
        g_a, g_b = math.gcd(Av, N), math.gcd(Bv, N)
        distinct = len(fq)
        print(f"    A={Av}(gcd={g_a}), B={Bv}(gcd={g_b}): {distinct} distinct values → {dict(sorted(fq.items()))}")

    # gcd condition: Latin iff gcd(A,9)=1 OR gcd(B,9)=1
    # (When both gcds > 1, the image of (x,y)→xA+yB doesn't cover Z₉ uniformly)
    print(f"\n  gcd analysis:")
    gcd_stats = Counter((math.gcd(Av, N), math.gcd(Bv, N)) for (Av, Bv) in latin_pairs)
    for (ga, gb), cnt in sorted(gcd_stats.items()):
        print(f"    gcd(A,9)={ga}, gcd(B,9)={gb}: {cnt} Latin pairs")

    # Verify condition: Latin ↔ gcd(A,9)=1 AND gcd(B,9)=1
    # (both A and B must be coprime to 9; if either fails, rows or cols collapse)
    for (Av, Bv) in latin_pairs:
        g_a, g_b = math.gcd(Av, N), math.gcd(Bv, N)
        check(g_a == 1 and g_b == 1,
              f"Latin pair A={Av},B={Bv} has gcd(A,9)=1 AND gcd(B,9)=1",
              (g_a, g_b), "both = 1")
    for (Av, Bv, _) in non_latin:
        g_a, g_b = math.gcd(Av, N), math.gcd(Bv, N)
        check(not (g_a == 1 and g_b == 1),
              f"Non-Latin A={Av},B={Bv} has gcd(A,9)>1 OR gcd(B,9)>1",
              (g_a, g_b), "at least one > 1")
    print(f"\n  PROVEN: grid(A,B) is Latin square ↔ gcd(A,9)=1 AND gcd(B,9)=1")
    print(f"  (If gcd(A,9)>1 then columns collapse; if gcd(B,9)>1 then rows collapse)")
    print(f"  Coprime-to-9 values: {{1,2,4,5,7,8}} (|φ(9)|=6; elements not divisible by 3)")

    # ── SECTION 11: SLOPE TABLE FOR KEY (A,B) ────────────────────
    print(f"\n  ─ SLOPE SURVEY")
    print(f"  {'A':>3}  {'B':>3}  {'slope -A/B':>15}  {'Latin':>6}  {'distinct vals':>14}")
    print("  " + "─" * 55)
    test_pairs = [(1,1),(2,1),(1,2),(3,1),(1,3),(2,3),(4,1),(1,4),
                  (3,3),(0,1),(1,0),(0,0),(6,3),(3,6),(2,2)]
    for (Av, Bv) in test_pairs:
        Gv  = make_grid(Av, Bv, N)
        lv  = latin_square_check(Gv, N)
        sl  = slope_str(Av, Bv, N)
        fv  = value_freq(Gv)
        print(f"  {Av:>3}  {Bv:>3}  {sl:>15}  {str(lv['latin']):>6}  {len(fv):>14}")

    # ── SECTION 12: TRACK IDENTIFICATION ─────────────────────────
    print(f"\n  ─ TWIN PRIME TRACK POSITIONS IN DR GRID")
    print(f"  (DR(p) for twin prime p > 3 is always in {{2,5,8}})")
    print(f"  Track T₂₄: DR(p)=2 → DR(p+2)=4")
    print(f"  Track T₅₇: DR(p)=5 → DR(p+2)=7")
    print(f"  Track T₈₁: DR(p)=8 → DR(p+2)=1 (since DR(10)=1)")

    A, B = 1, 1
    G = make_grid(A, B, N)
    G_dr = dr_shift(G, N)

    tp_pos = track_positions(G_dr, N)
    for v in sorted(TWIN_P_DR):
        track = "T₂₄" if v == 2 else "T₅₇" if v == 5 else "T₈₁"
        partner = 4 if v == 2 else 7 if v == 5 else 1
        print(f"\n  DR(p)={v} [{track}] — {len(tp_pos[v])} positions in grid:")
        for (x, y) in tp_pos[v]:
            # The +2 step: DR(p+2) should be v+2 mod 9 (with 0→9)
            nbr_val = G_dr[y][(x + 2) % N]   # move 2 steps right (+2 in x means +2A=+2)
            print(f"    (x={x},y={y}) val={G_dr[y][x]}  →  neighbor(x+2,y)={nbr_val}  expected={partner}  {'✓' if nbr_val==partner else '✗'}")
            check(nbr_val == partner,
                  f"T track: grid+2 step at (x={x},y={y})",
                  nbr_val, partner)

    # ── SECTION 13: DENSITY EXAMPLES ─────────────────────────────
    print(f"\n  ─ DENSITY: NON-LATIN GRIDS (gcd effect)")
    density_cases = [(3,0),(0,3),(3,3),(6,3),(3,6)]
    for (Av,Bv) in density_cases:
        Gd = make_grid(Av, Bv, N)
        fd = value_freq(Gd)
        distinct = len(fd)
        ga, gb = math.gcd(Av,N), math.gcd(Bv,N)
        reachable = N // math.gcd(math.gcd(Av,N), math.gcd(Bv,N))
        print(f"  A={Av}(gcd={ga}), B={Bv}(gcd={gb}): {distinct} distinct values, "
              f"each appearing {N*N//distinct}×")
        print(f"    Reachable residues: {sorted(fd.keys())}")
        check(distinct == reachable or (Av==0 and Bv==0),
              f"distinct vals for A={Av},B={Bv}", distinct, reachable)
        print_grid(Gd, f"  Grid A={Av}, B={Bv}")

    # ── ASSERTIONS ───────────────────────────────────────────────
    print("\n" + "=" * 66)
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f)
        import sys; sys.exit(1)
    else:
        total_checks = (
            3          # latin
            + N        # freq
            + N * 2    # row/col sums
            + 1        # grand total
            + 2        # diagonals
            + N        # diag sums
            + N * (N+1)# level sets (size + membership)
            + 1        # cayley
            + 2        # identity row/col
            + N        # inverses
            + N + 1    # DR freq + table
            + len(key_pairs)
            + 1        # sweep count
            + len(latin_pairs) + len(non_latin)   # gcd conditions
            + 3 * N    # track neighbor checks
            + len(density_cases)
        )
        print(f"ALL ASSERTIONS PASSED  ({total_checks}+ checks, zero skipped)")

if __name__ == "__main__":
    run()
