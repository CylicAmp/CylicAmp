# math/theorems/golden_path_sequence.py
"""
Golden Path Sequence — Eternal Rule.
Generates the result for any t >= 9 using the three 8-row digit cycles
(Red, Green, Blue) and a column wrap modulo 9.

Classification: Theorem
"""

# Complete digit patterns (row index 0–7)
RED   = {0: 1, 1: 1, 2: 8, 3: 1, 4: 9, 5: 8, 6: 9, 7: 8}
GREEN = {0: 9, 1: 1, 2: 1, 3: 9, 4: 1, 5: 1, 6: 9, 7: 1}
BLUE  = {0: 9, 1: 9, 2: 8, 3: 1, 4: 1, 5: 9, 6: 8, 7: 8}


def column_color(col_num):
    """Map column number (1–9) to 'red', 'green', or 'blue'."""
    mod = (col_num - 1) % 9
    if mod in (0, 3, 6):    # C1, C4, C7
        return "red"
    elif mod in (1, 4, 7):  # C2, C5, C8
        return "green"
    else:                   # C3, C6, C9
        return "blue"


def get_values(t):
    """Return (color, row_index, digit, column_number) for time t (t >= 9)."""
    col = ((t - 13) % 9) + 9
    if col > 9:
        col -= 9
    row = (t - 1) % 8
    color = column_color(col)
    if color == "red":
        digit = RED[row]
    elif color == "green":
        digit = GREEN[row]
    else:
        digit = BLUE[row]
    return color, row, digit, col


def calculate(t):
    """Compute the final value for time t using the eternal rule."""
    if t < 9:
        raise ValueError("Rule defined only for t >= 9")
    color, row, digit, col_num = get_values(t)
    offset = t - 8
    base = 400 + digit * 10 + offset
    result = base + 4
    return result, color, row, digit, offset, base, col_num


# --- Assertions ---

assert column_color(1) == "red"
assert column_color(2) == "green"
assert column_color(3) == "blue"
assert column_color(5) == "green"
assert column_color(6) == "blue"
assert column_color(9) == "blue"

# Row cycle = 8, column cycle = 9
assert all(get_values(t)[1] == get_values(t + 8)[1] for t in range(9, 50))
assert all(get_values(t)[3] == get_values(t + 9)[3] for t in range(9, 50))

# Spot checks
assert calculate(9)[0]   == 495
assert calculate(10)[0]  == 496
assert calculate(11)[0]  == 487
assert calculate(12)[0]  == 498
assert calculate(100)[0] == 506


if __name__ == "__main__":
    print(f"{'t':>3} {'Col':<6} {'Color':<6} {'Row':>3} {'Digit':>5} {'Offset':>6} {'Base':>6} {'Result':>6}")
    print("-" * 55)
    for t in range(9, 13):
        res, clr, row, digit, off, base, col_num = calculate(t)
        print(f"{t:3d} C{col_num:<5d} {clr:<6} {row:3d} {digit:5d} {off:6d} {base:6d} {res:6d}")

    t = 100
    res, clr, row, digit, off, base, col_num = calculate(t)
    print(f"\n--- t = {t} ---")
    print(f"Column: C{col_num} ({clr})")
    print(f"Row index: {row}")
    print(f"Digit: {digit}")
    print(f"Offset: {off}")
    print(f"Base: {base}")
    print(f"Final (+4): {res}")
    print()
    print("All assertions passed.")
