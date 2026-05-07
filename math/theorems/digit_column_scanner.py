"""
Digit Column Scanner — Time-stepped digit pattern system

RED/GREEN/BLUE digit dictionaries indexed by row (0–7).
Columns C1–C9 cycle every 9 steps; rows cycle every 8 steps.
Formula: result = 400 + digit * 10 + (t - 8) + 4

Classification: Theorem
"""

# Complete digit patterns for each color (row index 0–7)
RED   = {0: 1, 1: 1, 2: 8, 3: 1, 4: 9, 5: 8, 6: 9, 7: 8}
GREEN = {0: 9, 1: 1, 2: 1, 3: 9, 4: 1, 5: 1, 6: 9, 7: 1}
BLUE  = {0: 9, 1: 9, 2: 8, 3: 1, 4: 1, 5: 9, 6: 8, 7: 8}


def column_color(col_num):
    """Return 'red', 'green', or 'blue' for column number (1–9)."""
    mod = (col_num - 1) % 9
    if mod in (0, 3, 6):    # C1, C4, C7
        return "red"
    elif mod in (1, 4, 7):  # C2, C5, C8
        return "green"
    else:                   # C3, C6, C9
        return "blue"


def get_values(t):
    """Return (color, row, digit, col_num) for a given time t (t >= 9)."""
    col_num = ((t - 13) % 9) + 9
    if col_num > 9:
        col_num -= 9
    row = (t - 1) % 8
    color = column_color(col_num)
    if color == "red":
        digit = RED[row]
    elif color == "green":
        digit = GREEN[row]
    else:
        digit = BLUE[row]
    return color, row, digit, col_num


def calculate(t):
    """Compute result for time step t >= 9."""
    if t < 9:
        raise ValueError("Rule defined only for t >= 9")
    color, row, digit, col_num = get_values(t)
    offset = t - 8
    base = 400 + digit * 10 + offset
    result = base + 4
    return result, color, row, digit, offset, base, col_num


# --- Assertions ---

# Column color assignments
assert column_color(1) == "red"
assert column_color(2) == "green"
assert column_color(3) == "blue"
assert column_color(4) == "red"
assert column_color(5) == "green"
assert column_color(6) == "blue"
assert column_color(7) == "red"
assert column_color(8) == "green"
assert column_color(9) == "blue"

# Row cycle period = 8, column cycle period = 9
assert all(get_values(t)[1] == get_values(t + 8)[1] for t in range(9, 50))
assert all(get_values(t)[3] == get_values(t + 9)[3] for t in range(9, 50))

# Spot checks against known output
assert calculate(9)[0]  == 495   # t9:  C5 green row0 digit9 offset1
assert calculate(10)[0] == 496   # t10: C6 blue  row1 digit9 offset2
assert calculate(11)[0] == 487   # t11: C7 red   row2 digit8 offset3
assert calculate(12)[0] == 498   # t12: C8 green row3 digit9 offset4
assert calculate(100)[0] == 506  # t100 forecast


if __name__ == "__main__":
    print(f"{'t':>3} {'Col':<6} {'Color':<6} {'Row':>3} {'Digit':>5} {'Offset':>6} {'Base':>6} {'Result':>6}")
    print("-" * 55)
    for t in range(9, 13):
        result, color, row, digit, offset, base, col_num = calculate(t)
        print(f"{t:3d} C{col_num:<5d} {color:<6} {row:3d} {digit:5d} {offset:6d} {base:6d} {result:6d}")

    t = 100
    result, color, row, digit, offset, base, col_num = calculate(t)
    print(f"\n--- t = {t} ---")
    print(f"Column: C{col_num} ({color})")
    print(f"Row index: {row}")
    print(f"Digit: {digit}")
    print(f"Offset: {offset}")
    print(f"Base: {base}")
    print(f"Final (+4): {result}")
    print()
    print("All assertions passed.")
