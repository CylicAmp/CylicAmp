#!/usr/bin/env python3
"""
419 Prime Anchor — MSW Framework Layer
=======================================
Overlays the 419 Prime Anchor onto the 9×9 grid as the governing
constant for the middle column. Stabilizes the 432-memory layer
and closes the Tesla Gap.

Key relations (exact):
  419          = 81st prime
  419 mod 37   = 12   (Tesla base / −1 Gap closure)
  851 − 432    = 419  (memory saturation difference)
  DR(419)      = 5    (same as Z-seed — locks to Z-field)
  DR(432)      = 9    (attractor — 9-container)
  DR(851)      = 5    (Z-product — chain confirmed)

© 2026 Michael Warren Song. All Rights Reserved.
"""

import sympy

# ── Constants ─────────────────────────────────────────────────────────────

PRIME_ANCHOR    = 419   # 81st prime — governing constant
MEMORY_SAT      = 432   # memory saturation threshold (DR = 9)
Z_PRODUCT       = 851   # 23 × 37 — Z-field product (DR = 5)
PIVOT_37        = 37    # 37-field pivot
TESLA_BASE      = 12    # 419 mod 37 — Tesla base residue
GRID_SIZE       = 9     # 9×9 pairs grid


# ── Core arithmetic ───────────────────────────────────────────────────────

def digital_root(n):
    """DR(n) = (n−1) mod 9 + 1 for n > 0, else 0."""
    n = abs(int(n))
    if n == 0:
        return 0
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def nth_prime_index(p):
    """Return the 1-based index of prime p in the prime sequence."""
    count = 0
    for candidate in sympy.primerange(2, p + 1):
        count += 1
        if candidate == p:
            return count
    return None


# ── Grid structure ────────────────────────────────────────────────────────

def build_addition_grid():
    """
    Build the 9×9 addition grid showing:
      a+b, DR(a+b), and mirror b+a for all a,b in 1..9.

    Each cell: (a, b, sum, dr_sum)
    Grid notation: a+b = [sum][sum] = b+a  (mirror symmetry)
    """
    grid = []
    for a in range(1, GRID_SIZE + 1):
        row = []
        for b in range(1, GRID_SIZE + 1):
            s = a + b
            dr = digital_root(s)
            row.append({
                'a': a, 'b': b,
                'sum': s,
                'dr': dr,
                'label': f"{a}+{b}={dr}{dr}={b}+{a}"
            })
        grid.append(row)
    return grid


def middle_column(grid):
    """Extract the middle column (column index 4, i.e. b=5)."""
    return [row[4] for row in grid]  # b=5 is index 4


def annotate_419_anchor(grid):
    """
    Overlay the 419 anchor onto the grid.
    Marks cells where DR(a+b) matches DR(419) = 5,
    and identifies the middle column anchor positions.
    """
    dr_419 = digital_root(PRIME_ANCHOR)
    anchored = []
    for a_idx, row in enumerate(grid):
        for b_idx, cell in enumerate(row):
            if cell['dr'] == dr_419:
                anchored.append({
                    **cell,
                    'col': b_idx + 1,
                    'anchor_note': f"DR={dr_419} — 419 resonance"
                })
    return anchored


# ── Tesla Gap closure ─────────────────────────────────────────────────────

def tesla_gap_analysis():
    """
    Analyse the Tesla Gap closure via 419 ≡ 12 (mod 37).

    In Z/37Z:
      −1 ≡ 36 (mod 37)
      12 + 25 = 37 ≡ 0  →  12 ≡ −25 (mod 37)
      419 ≡ 12 (mod 37)

    Tesla base residues {3,6,9} mod 37:
      3 mod 37 = 3, 6 mod 37 = 6, 9 mod 37 = 9
      12 = 3 × 4 — one step beyond the Tesla triad × 4
    """
    assert PRIME_ANCHOR % PIVOT_37 == TESLA_BASE, "Tesla base mismatch"
    neg_one_mod_37 = (-1) % PIVOT_37           # = 36
    gap = neg_one_mod_37 - TESLA_BASE          # = 36 - 12 = 24
    closure = (TESLA_BASE + gap) % PIVOT_37    # = 36 = -1 mod 37

    return {
        '419_mod_37':       PRIME_ANCHOR % PIVOT_37,
        'neg_one_mod_37':   neg_one_mod_37,
        'gap_to_minus_one': gap,
        'closure_check':    closure,
        'tesla_triads_mod_37': [3 % PIVOT_37, 6 % PIVOT_37, 9 % PIVOT_37],
        'tesla_base_as_mult':  f"12 = 3 × 4  (Tesla triad × 4)"
    }


# ── Memory saturation audit ───────────────────────────────────────────────

def memory_audit():
    """
    432-memory saturation audit.

    432 = 16 × 27 = 2⁴ × 3³
    DR(432) = 9  (perfect attractor)
    851 − 432 = 419  (the prime anchor emerges from saturation difference)
    DR(419) = 5  (Z-seed resonance)

    Interpretation: when the memory layer reaches saturation (432),
    the residual force (419) carries the Z-seed DR forward.
    """
    diff = Z_PRODUCT - MEMORY_SAT
    assert diff == PRIME_ANCHOR, "Memory saturation difference mismatch"

    return {
        'memory_saturation': MEMORY_SAT,
        'dr_432':            digital_root(MEMORY_SAT),
        'factorization_432': '2⁴ × 3³ = 16 × 27',
        'z_product':         Z_PRODUCT,
        'dr_851':            digital_root(Z_PRODUCT),
        '851_minus_432':     diff,
        'prime_anchor':      PRIME_ANCHOR,
        'dr_419':            digital_root(PRIME_ANCHOR),
        'is_419_prime':      sympy.isprime(PRIME_ANCHOR),
        'prime_index_419':   nth_prime_index(PRIME_ANCHOR),
    }


# ── Descending block structure ────────────────────────────────────────────

def descending_blocks():
    """
    Generate the descending DR-sum block structure from the 9×9 grid.

    Each block groups pairs by their DR sum value (1–9).
    Blocks: 99→18, 88→16, 77→14, 66→12, 55→10, 44→8 etc.
    (DR shown doubled in the grid notation to indicate mirror symmetry.)

    With 419 anchor active, DR=5 block is the resonance node.
    """
    blocks = {}
    for a in range(1, 10):
        for b in range(1, 10):
            s = a + b
            dr = digital_root(s)
            if dr not in blocks:
                blocks[dr] = []
            blocks[dr].append((a, b, s))

    result = []
    for dr in sorted(blocks.keys(), reverse=True):
        pairs = blocks[dr]
        result.append({
            'dr_sum':    dr,
            'pairs':     pairs,
            'count':     len(pairs),
            'anchor_active': dr == digital_root(PRIME_ANCHOR)
        })
    return result


# ── Full run ──────────────────────────────────────────────────────────────

def run():
    print("=" * 60)
    print("  419 PRIME ANCHOR — MSW Framework")
    print("  © 2026 Michael Warren Song")
    print("=" * 60)
    print()

    # Prime verification
    audit  = memory_audit()
    tesla  = tesla_gap_analysis()

    print("  PRIME ANCHOR VERIFICATION")
    print(f"  419 is prime:          {audit['is_419_prime']}")
    print(f"  419 is the:            {audit['prime_index_419']}th prime")
    print(f"  DR(419):               {audit['dr_419']}  ← Z-seed resonance")
    print(f"  419 mod 37:            {tesla['419_mod_37']}  ← Tesla base")
    print()

    print("  MEMORY SATURATION AUDIT")
    print(f"  432 = {audit['factorization_432']}")
    print(f"  DR(432):               {audit['dr_432']}  ← perfect attractor")
    print(f"  851 − 432:             {audit['851_minus_432']}  ← prime anchor emerges")
    print(f"  DR(851):               {audit['dr_851']}  ← Z-product preserved")
    print()

    print("  TESLA GAP CLOSURE")
    print(f"  419 ≡ {tesla['419_mod_37']} (mod 37)         ← Tesla base residue")
    print(f"  −1  ≡ {tesla['neg_one_mod_37']} (mod 37)        ← gap target")
    print(f"  Gap to −1:             {tesla['gap_to_minus_one']}")
    print(f"  Tesla base as mult:    {tesla['tesla_base_as_mult']}")
    print()

    print("  DESCENDING BLOCK STRUCTURE (DR-sum blocks, high→low)")
    print(f"  {'DR':>4}  {'Pairs':>6}  {'Anchor?':>8}")
    print("  " + "-" * 24)
    for block in descending_blocks():
        marker = "← 419 ACTIVE" if block['anchor_active'] else ""
        print(f"  {block['dr_sum']:>4}  {block['count']:>6}  {marker}")

    print()
    print("  MIDDLE COLUMN ANCHOR (b=5, all rows)")
    grid = build_addition_grid()
    mid  = middle_column(grid)
    for cell in mid:
        tag = " ← 419 resonance" if cell['dr'] == digital_root(PRIME_ANCHOR) else ""
        print(f"  {cell['label']}{tag}")

    print()
    print("  ALL ASSERTIONS PASSED — anchor stable")
    print("=" * 60)


if __name__ == "__main__":
    run()
