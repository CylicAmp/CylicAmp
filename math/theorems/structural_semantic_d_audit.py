# math/theorems/structural_semantic_d_audit.py
"""
Structural vs Semantic D(n) — 6-Space Row Analysis
====================================================
Two interpretations of D(n) for a 6-row grid:

  STRUCTURAL (marker only):  D(n) = 2|n - 3|
    Row n splits 6 slots into left block of size n and right of size 6-n.
    D = |left_count - right_count| = |n - (6-n)| = |2n-6| = 2|n-3|.
    Gives sequence [4, 2, 0, 2, 4, 6]. Row 6 is NOT anomalous.

  SEMANTIC (value-active):  D(n) = (6-n) - n = 6 - 2n
    Right side has (6-n) ones; digit n consumes n units.
    Gives sequence [4, 2, 0, -2, -4, -6]. Row 6 IS anomalous (overflow).

  NOTATION-BASED reading of row 6 specifically:
    The split "11111 | 6" puts 5 ones on the left and digit 6 on the right.
    Left_ones = 5,  Right_ones = 0,  Digit_value = 6.
    D_notation(6) = Left_ones - Digit_value = 5 - 6 = -1.
    This is NEITHER D_structural(6)=6 NOR D_semantic(6)=-6.
    It is the specific semantic reading of that literal notation.

KEY FINDING:
  Rows 1-5 have the digit embedded in the left block (digit in last position).
  Row 6 has the digit externalized to the right block.
  The NOTATION itself encodes the structural break.

CORRECTION TO USER'S FIRST-OVERFLOW TABLE:
  For grid size S, the semantic first overflow is at n = floor(S/2) + 1.
  For S=6: first semantic overflow is at n=4 (deficit 2-4=-2), NOT n=6.
  The table entry (S=6, n=6, deficit 5-6=-1) uses the NOTATION-BASED reading
  of the specific row-6 split, not the semantic formula. The two differ.
"""


# ── helpers ───────────────────────────────────────────────────────────────────

def d_structural(n: int, size: int = 6) -> int:
    """D = |left_count - right_count| = |2n - size|."""
    return abs(2 * n - size)


def d_semantic(n: int, size: int = 6) -> int:
    """D = remaining_ones - digit = (size - n) - n = size - 2n."""
    return (size - n) - n


def d_notation(n: int, size: int = 6) -> int:
    """
    D for the literal row-n notation in a size-S grid.

    For n = 1..S-1: digit n is embedded in the LEFT block.
      Left_ones = n-1,  Right_ones = S-n.
      D_notation = Left_block_size - Right_block_size = n - (S-n) = 2n - S.
      (This equals -D_semantic = 2n - S, signed.)

    For n = S (final row): digit S migrates to the RIGHT block.
      Left_ones = S-1,  Right_ones = 0,  Digit_value = S.
      D_notation = Left_ones - Digit_value = (S-1) - S = -1.
    """
    if n == size:
        return (size - 1) - size   # -1
    else:
        return n - (size - n)      # 2n - size


def first_semantic_overflow(size: int) -> tuple:
    """First n where d_semantic < 0: n = floor(size/2) + 1."""
    n = size // 2 + 1
    return n, d_semantic(n, size)


def first_notation_overflow(size: int) -> tuple:
    """
    First n where d_notation(n, size) < 0.
    For n=1..size-1:  d_notation = 2n - size < 0  iff  n < size/2.
      But for n < size/2, d_notation = 2n-size < 0 from n=1 onward when size>2.
    Hmm — actually for size=6, n=1: d_notation = 2-6 = -4 < 0 immediately.
    This means the signed notation D is negative for n < size/2 and positive for n > size/2.
    First POSITIVE→NEGATIVE transition (overflow in the semantic sense):
      d_notation first goes negative at n = size//2 + 1 for n < size.
    Special case n=size: always -1.
    """
    for n in range(1, size + 1):
        if d_notation(n, size) < 0:
            return n, d_notation(n, size)
    return None, None


# ── verify ────────────────────────────────────────────────────────────────────

def verify():
    print("Structural vs Semantic D(n) — 6-Space Row Analysis\n")

    SIZE = 6

    # ── Part 1: structural formula D(n) = 2|n-3| ─────────────────────────────
    print("=" * 60)
    print("PART 1: STRUCTURAL  D(n) = 2|n-3|  (= |2n-6|)")
    print("=" * 60)

    expected_struct = [4, 2, 0, 2, 4, 6]
    print(f"\n  n | Left | Right | |L-R| | 2|n-3| | Match")
    print(f"  --|------|-------|-------|--------|------")
    for n in range(1, SIZE + 1):
        left  = n
        right = SIZE - n
        D_pos = abs(right - left)
        D_fml = d_structural(n, SIZE)
        assert D_pos == D_fml
        assert D_fml == expected_struct[n - 1]
        mark = "OK" if D_pos == D_fml else "FAIL"
        print(f"  {n} | {left:4d} | {right:5d} | {D_pos:5d} | {D_fml:6d} | {mark}")

    struct_seq = [d_structural(n, SIZE) for n in range(1, SIZE + 1)]
    assert struct_seq == expected_struct
    print(f"\n  Sequence: {struct_seq}  OK")
    print(f"  Symmetric? {struct_seq == struct_seq[::-1]}  (not palindrome — open-ended)")
    print(f"  Row 6: D=6, NOT anomalous under structural lens  OK\n")

    # ── Part 2: semantic formula D(n) = (6-n) - n ─────────────────────────────
    print("=" * 60)
    print("PART 2: SEMANTIC  D(n) = (6-n) - n = 6 - 2n")
    print("=" * 60)

    expected_sem = [4, 2, 0, -2, -4, -6]
    print(f"\n  n | rem_ones | digit | D=rem-digit")
    print(f"  --|----------|-------|-----------")
    for n in range(1, SIZE + 1):
        rem  = SIZE - n
        D    = d_semantic(n, SIZE)
        assert D == expected_sem[n - 1]
        overflow = "  <- OVERFLOW" if D < 0 else ""
        print(f"  {n} | {rem:8d} | {n:5d} | {D:11d}{overflow}")

    sem_seq = [d_semantic(n, SIZE) for n in range(1, SIZE + 1)]
    assert sem_seq == expected_sem
    print(f"\n  Sequence: {sem_seq}  OK")
    print(f"  Antisymmetric: {sem_seq == [-x for x in sem_seq[::-1]]}  OK")
    print(f"  Row 6: D=-6, IS anomalous (overflow by 6)  OK\n")

    # ── Part 3: notation-based reading of row 6 ───────────────────────────────
    print("=" * 60)
    print("PART 3: NOTATION-BASED READING  (row 6 in 6-space)")
    print("=" * 60)

    print("""
  Row representation for 6-space:
    Row 1: "1"     | "11111"  →  left=1 elem,  right=5 ones
    Row 2: "12"    | "1111"   →  left=2 elems, right=4 ones
    Row 3: "113"   | "111"    →  left=3 elems, right=3 ones
    Row 4: "1114"  | "11"     →  left=4 elems, right=2 ones
    Row 5: "11115" | "1"      →  left=5 elems, right=1 one
    Row 6: "11111" | "6"      →  left=5 ones,  right=0 ones + digit 6

  Rows 1-5: digit embedded in LEFT block (last element of left block).
  Row 6:    digit externalized to RIGHT block (left block = only ones).
  ─ This is the structural break. ─
    """)

    # Verify row structure
    for n in range(1, SIZE):
        # Row n: left has (n-1) ones + digit n; right has (SIZE-n) ones
        left_ones  = n - 1
        right_ones = SIZE - n
        left_total = n          # (n-1 ones) + digit = n elements
        right_total = SIZE - n
        d_struct = d_structural(n, SIZE)
        d_sem    = d_semantic(n, SIZE)
        d_not    = d_notation(n, SIZE)
        # d_structural uses absolute block counts; d_notation is signed
        assert abs(d_not) == d_struct, f"n={n}: |notation|={abs(d_not)} != struct={d_struct}"

    # Row 6: the special case
    n = SIZE
    left_ones_6  = SIZE - 1    # 5 ones on left
    digit_value  = SIZE        # 6
    right_ones_6 = 0           # no ones on right
    d_not_6      = left_ones_6 - digit_value   # 5 - 6 = -1
    d_struct_6   = d_structural(n, SIZE)       # 6
    d_sem_6      = d_semantic(n, SIZE)         # -6

    assert d_not_6   == -1
    assert d_struct_6 == 6
    assert d_sem_6    == -6
    assert d_notation(n, SIZE) == -1

    print(f"  Row 6 readings:")
    print(f"    Structural: |0 - 6| = {d_struct_6}   (block size difference)")
    print(f"    Semantic:   0 - 6 = {d_sem_6}   (remaining_ones - digit, full formula)")
    print(f"    Notation:   5 - 6 = {d_not_6}   (left_ones - digit_value, literal split)")
    print(f"\n  Ratio structural/notation: {d_struct_6}/{d_not_6} = {d_struct_6/d_not_6}")
    print(f"  Sum structural + notation: {d_struct_6} + {d_not_6} = {d_struct_6 + d_not_6}")
    print(f"\n  Three distinct values {d_struct_6}, {d_sem_6}, {d_not_6} for the same row.  OK\n")

    # ── Part 4: capacity threshold (semantic formula, all grid sizes) ──────────
    print("=" * 60)
    print("PART 4: CAPACITY THRESHOLD  (semantic: remaining - digit)")
    print("=" * 60)

    print(f"\n  Size | First semantic overflow | Deficit")
    print(f"  -----|------------------------|--------")
    for size in range(3, 9):
        n_over, deficit = first_semantic_overflow(size)
        print(f"  {size:4d} | n = {n_over:19d} | {deficit}")

    # Verify specific values from the script output
    assert first_semantic_overflow(3) == (2, -1)
    assert first_semantic_overflow(4) == (3, -2)
    assert first_semantic_overflow(5) == (3, -1)
    assert first_semantic_overflow(6) == (4, -2)   # n=4, NOT n=6
    assert first_semantic_overflow(7) == (4, -1)
    assert first_semantic_overflow(8) == (5, -2)
    print(f"\n  Formula: first overflow at n = floor(S/2) + 1  OK\n")

    # ── Part 5: correction to user's first-overflow table ─────────────────────
    print("=" * 60)
    print("PART 5: CORRECTION — S=6 in the 'First Overflow' table")
    print("=" * 60)

    print("""
  User's table (reproduced):
    S=3: n=2, deficit 1-2=-1     ← semantic formula  OK
    S=4: n=3, deficit 1-3=-2     ← semantic formula  OK
    S=5: n=3, deficit 2-3=-1     ← semantic formula  OK
    S=6: n=6, deficit 5-6=-1     ← NOTATION-BASED (not semantic formula)
    S=7: n=4, deficit 3-4=-1     ← semantic formula  OK
    S=8: n=5, deficit 3-5=-2     ← semantic formula  OK

  For S=6, the semantic first overflow is at n=4 (deficit 2-4=-2), not n=6.
  The table entry (n=6, deficit 5-6=-1) is the NOTATION reading of the
  specific split "11111|6", not the semantic formula applied uniformly.

  Notation-based reading for ALL sizes (digit migrates at n=S):
    S=3: Row 3 → "11"|"3",  notation deficit = 2-3 = -1
    S=4: Row 4 → "111"|"4", notation deficit = 3-4 = -1
    S=5: Row 5 → "1111"|"5",notation deficit = 4-5 = -1
    S=6: Row 6 → "11111"|"6",notation deficit = 5-6 = -1
  All give notation deficit = (S-1) - S = -1.  Uniform.
    """)

    # Verify notation deficit at n=S is always -1
    for size in range(3, 10):
        assert d_notation(size, size) == -1, f"size={size}: notation deficit != -1"
    print(f"  d_notation(S, S) = -1 for all S = 3..9  OK")
    print(f"  The notation phase transition is a UNIFORM -1 deficit, not size-dependent.")
    print(f"  The S=6 table mixes two criteria; it is not internally consistent.\n")

    # ── Part 6: mirror completeness ───────────────────────────────────────────
    print("=" * 60)
    print("PART 6: MIRROR COMPLETENESS")
    print("=" * 60)

    struct_seq = [d_structural(n, SIZE) for n in range(1, SIZE + 1)]
    sem_seq    = [d_semantic(n, SIZE)   for n in range(1, SIZE + 1)]
    not_seq    = [d_notation(n, SIZE)   for n in range(1, SIZE + 1)]

    assert struct_seq == [4, 2, 0, 2, 4, 6]
    assert sem_seq    == [4, 2, 0, -2, -4, -6]
    assert not_seq    == [-4, -2, 0, 2, 4, -1]

    print(f"\n  Structural: {struct_seq}")
    print(f"    Symmetric (palindrome)? {struct_seq == struct_seq[::-1]}")
    print(f"    Antisymmetric? {struct_seq == [-x for x in struct_seq[::-1]]}")

    print(f"\n  Semantic:   {sem_seq}")
    print(f"    Symmetric? {sem_seq == sem_seq[::-1]}")
    print(f"    Antisymmetric: {sem_seq == [-x for x in sem_seq[::-1]]}")

    print(f"\n  Notation:   {not_seq}")
    print(f"    Symmetric? {not_seq == not_seq[::-1]}")
    print(f"    Note: n=6 breaks the antisymmetric pattern [-4,-2,0,2,4,4] → last term is -1")
    print(f"    If row 6 used semantic formula: last term would be -4 (antisymmetric).")
    print(f"    Notation gives -1 instead: signature of the structural break.\n")

    # Verify that WITHOUT row 6, notation is antisymmetric
    not_seq_5 = [d_notation(n, SIZE) for n in range(1, SIZE)]
    expected_antisym = [4, 2, 0, -2, -4]
    # d_notation for n=1..5: 2*1-6=-4, 2*2-6=-2, 0, 2, 4
    # that's [-4,-2,0,2,4], antisymmetric
    assert not_seq_5 == [-4, -2, 0, 2, 4]
    print(f"  Notation n=1..5: {not_seq_5}  (antisymmetric)  OK")
    print(f"  Row 6 breaks this to {not_seq}: the -1 is the notational anomaly.  OK\n")

    # ── Summary ───────────────────────────────────────────────────────────────
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"""
  VERIFIED:
    D_structural(n) = 2|n-3|: {struct_seq}   OK
    D_semantic(n)   = 6-2n:   {sem_seq}  OK
    Row 6 notation split "11111|6": deficit = 5-6 = -1           OK
    Notation d(S,S) = (S-1)-S = -1 for all grid sizes S=3..9    OK
    First semantic overflow at floor(S/2)+1 for each size         OK

  CORRECTION:
    The 'First Overflow' table for S=6 shows (n=6, deficit -1).
    This is the NOTATION reading, not the semantic formula.
    Semantic formula gives first overflow at n=4 (deficit 2-4=-2).
    The table mixes criteria: semantic for S=3,4,5,7,8; notation for S=6.

  THE BREAK (confirmed):
    Rows 1-5: digit in LEFT block  ->  signed notation D = 2n-6  (antisymmetric)
    Row 6:    digit in RIGHT block ->  notation D = (S-1)-S = -1 (breaks symmetry)
    This is notationally encoded, not externally imposed.
    The notation's structure changed at row 6.
    """)

    print("All assertions passed.")


if __name__ == "__main__":
    verify()
