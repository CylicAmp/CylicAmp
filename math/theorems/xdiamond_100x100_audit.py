# 100x100 BOUNDED X-DIAMOND MATRIX
# Spine: cols 50-51 (1-indexed)
# Top half (rows 1-50): outer diagonals at col r and col 101-r; values swap roles
# Bottom half (rows 51-100): outer diagonals at col 101-r and col r; values swap roles
# Center reflection at rows 50-51: diagonals displaced to cols 49, 52 when they land on spine


def get_value(r, c):
    """Return matrix value at row r, col c (1-indexed). 0 = empty."""
    if r <= 50:
        spine_val = ((r - 1) % 5) + 1
        diag_val  = 5 - ((r - 1) % 5)
        left_diag = r
        right_diag = 101 - r
    else:
        spine_val = 5 - ((r - 1) % 5)
        diag_val  = ((r - 1) % 5) + 1
        left_diag = 101 - r
        right_diag = r

    # Center reflection: when diagonals land on spine cols 50 or 51, displace to 49 and 52
    if left_diag == 50:  # implies right_diag == 51
        left_diag  = 49
        right_diag = 52

    if c in (50, 51):
        return spine_val
    if c == left_diag or c == right_diag:
        return diag_val
    return 0


def verify():
    # All active positions from the specification, with expected values
    expected = {
        1:   {1: 5, 50: 1, 51: 1, 100: 5},
        2:   {2: 4, 50: 2, 51: 2,  99: 4},
        3:   {3: 3, 50: 3, 51: 3,  98: 3},
        4:   {4: 2, 50: 4, 51: 4,  97: 2},
        5:   {5: 1, 50: 5, 51: 5,  96: 1},
        48:  {48: 3, 50: 3, 51: 3,  53: 3},
        49:  {49: 2, 50: 4, 51: 4,  52: 2},
        50:  {49: 1, 50: 5, 51: 5,  52: 1},
        51:  {49: 1, 50: 5, 51: 5,  52: 1},
        52:  {49: 2, 50: 4, 51: 4,  52: 2},
        53:  {48: 3, 50: 3, 51: 3,  53: 3},
        96:  {5: 1,  50: 5, 51: 5,  96: 1},
        97:  {4: 2,  50: 4, 51: 4,  97: 2},
        98:  {3: 3,  50: 3, 51: 3,  98: 3},
        99:  {2: 4,  50: 2, 51: 2,  99: 4},
        100: {1: 5,  50: 1, 51: 1, 100: 5},
    }

    errors = []
    for r, col_vals in sorted(expected.items()):
        # Check active cells
        for c, ev in col_vals.items():
            av = get_value(r, c)
            if av != ev:
                errors.append(f"  Row {r:3d} Col {c:3d}: expected {ev}, got {av}")
        # Check all other cols are empty
        for c in range(1, 101):
            if c not in col_vals:
                av = get_value(r, c)
                if av != 0:
                    errors.append(f"  Row {r:3d} Col {c:3d}: expected 0, got {av}")

    return errors


def active_cells_per_row():
    """Return dict: row -> list of (col, value) for non-empty cells."""
    result = {}
    for r in range(1, 101):
        cells = [(c, get_value(r, c)) for c in range(1, 101) if get_value(r, c)]
        result[r] = cells
    return result


def count_by_value():
    """Count occurrences of each value 1-5 across the full matrix."""
    counts = {v: 0 for v in range(1, 6)}
    for r in range(1, 101):
        for c in range(1, 101):
            v = get_value(r, c)
            if v:
                counts[v] += 1
    return counts


if __name__ == '__main__':
    print("=== 100x100 BOUNDED X-DIAMOND MATRIX ===")
    print()

    errors = verify()
    if errors:
        print("VERIFICATION ERRORS:")
        for e in errors:
            print(e)
    else:
        print("All boundary checks PASS (16 rows, 64 cells verified)")
    print()

    cells = active_cells_per_row()
    total_active = sum(len(v) for v in cells.values())
    print(f"Total non-empty cells: {total_active}")
    print()

    counts = count_by_value()
    print("Value distribution across full matrix:")
    for v, n in sorted(counts.items()):
        print(f"  Value {v}: {n} cells")
    print(f"  Total : {sum(counts.values())} cells")
    print()

    print("Active cells by row (non-empty only):")
    for r in range(1, 101):
        row_cells = cells[r]
        if row_cells:
            pairs = '  '.join(f"c{c}={v}" for c, v in row_cells)
            print(f"  Row {r:3d}: {pairs}")
