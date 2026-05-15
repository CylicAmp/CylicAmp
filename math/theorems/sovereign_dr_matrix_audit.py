# math/theorems/sovereign_dr_matrix_audit.py
"""
Sovereign DR Matrix — Period-24 Fibonacci/Lucas DRs — Law of 12 — Checkerboard
================================================================================
Sections:
  A. 9×9 Sovereign DR matrix: M[i][j] = dr(i*j) for i,j ∈ {1..9}
  B. Fibonacci period-24 DR sequence (F0 adjusted: 0→DR 9)
  C. Lucas period-24 DR sequence
  D. Law of 12: multiples of 12 have DRs ∈ {3,6,9}
  E. Binary checkerboard ■□ row patterns (rows 1–9, alternating parity)
  F. 23/32 symmetry: digit operations and parity classification
"""

import math


def dr(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


# ── A. 9×9 Sovereign DR matrix ───────────────────────────────────────────────

SOVEREIGN = [
    [dr(i * j) for j in range(1, 10)]
    for i in range(1, 10)
]

SOVEREIGN_EXPECTED = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [2, 4, 6, 8, 1, 3, 5, 7, 9],
    [3, 6, 9, 3, 6, 9, 3, 6, 9],
    [4, 8, 3, 7, 2, 6, 1, 5, 9],
    [5, 1, 6, 2, 7, 3, 8, 4, 9],
    [6, 3, 9, 6, 3, 9, 6, 3, 9],
    [7, 5, 3, 1, 8, 6, 4, 2, 9],
    [8, 7, 6, 5, 4, 3, 2, 1, 9],
    [9, 9, 9, 9, 9, 9, 9, 9, 9],
]


# ── B. Fibonacci DR period-24 ─────────────────────────────────────────────────

def fib_sequence(length: int) -> list:
    f = [0, 1]
    while len(f) < length:
        f.append(f[-1] + f[-2])
    return f[:length]


# F0=0 has dr(0)=0; we replace 0 with 9 (convention: DR(9k)=9, DR(0)=9)
def fib_dr_adjusted(length: int) -> list:
    return [9 if dr(f) == 0 else dr(f) for f in fib_sequence(length)]


FIB_DR_PERIOD_24 = [9, 1, 1, 2, 3, 5, 8, 4, 3, 7, 1, 8, 9, 8, 8, 7, 6, 4, 1, 5, 6, 2, 8, 1]


# ── C. Lucas DR period-24 ─────────────────────────────────────────────────────

def lucas_sequence(length: int) -> list:
    luc = [2, 1]
    while len(luc) < length:
        luc.append(luc[-1] + luc[-2])
    return luc[:length]


LUCAS_DR_PERIOD_24 = [2, 1, 3, 4, 7, 2, 9, 2, 2, 4, 6, 1, 7, 8, 6, 5, 2, 7, 9, 7, 7, 5, 3, 8]


# ── D. Law of 12 ─────────────────────────────────────────────────────────────

def law_of_12_dr(count: int) -> list:
    return [dr(12 * k) for k in range(1, count + 1)]


LAW_OF_12_FIRST8 = [3, 6, 9, 3, 6, 9, 3, 6]


# ── E. Binary checkerboard ────────────────────────────────────────────────────

def checkerboard_row(length: int, start_odd: bool) -> str:
    row = []
    for k in range(length):
        is_odd = (k % 2 == 0) if start_odd else (k % 2 == 1)
        row.append("■" if is_odd else "□")
    return "".join(row)


# ── F. 23/32 symmetry ─────────────────────────────────────────────────────────

def digit_reverse(n: int) -> int:
    return int(str(n)[::-1])


def is_odd_number(n: int) -> bool:
    return n % 2 == 1


# 23 operations:
#   subtract 8: 23 - 8 = 15 (Odd)
#   21 - 3 = 18 (Even)
# 32: anchor, Even
# digit reversal: 23 ↔ 32


def verify():
    print("Sovereign DR Matrix — Period-24 DRs — Law of 12 — Checkerboard\n")

    # ── A. Sovereign DR matrix ────────────────────────────────────────────────
    print("=" * 70)
    print("A. 9×9 Sovereign DR matrix  M[i][j] = dr(i·j),  i,j ∈ {1..9}")
    print("=" * 70)

    assert SOVEREIGN == SOVEREIGN_EXPECTED, \
        f"Mismatch:\nComputed:\n{SOVEREIGN}\nExpected:\n{SOVEREIGN_EXPECTED}"

    print("\n  M[i][j] = dr(i·j):")
    print(f"  {'j':>3}", end="")
    for j in range(1, 10):
        print(f"{j:>4}", end="")
    print()
    print("  " + "-" * 39)
    for i in range(1, 10):
        row = SOVEREIGN[i - 1]
        print(f"  i={i} |", end="")
        for v in row:
            print(f"{v:>4}", end="")
        print()

    # Row 3: all multiples of 3 → DRs cycle {3,6,9}
    assert SOVEREIGN[2] == [3, 6, 9, 3, 6, 9, 3, 6, 9]
    # Row 6: same pattern
    assert SOVEREIGN[5] == [6, 3, 9, 6, 3, 9, 6, 3, 9]
    # Row 9: all 9s
    assert SOVEREIGN[8] == [9] * 9
    # Column 9 (j=9): all 9s
    assert [SOVEREIGN[i][8] for i in range(9)] == [9] * 9
    # Main diagonal: dr(i²) for i=1..9
    diag = [SOVEREIGN[i][i] for i in range(9)]
    assert diag == [dr((i + 1) ** 2) for i in range(9)]
    # Matrix is symmetric: dr(i·j) = dr(j·i)
    for i in range(9):
        for j in range(9):
            assert SOVEREIGN[i][j] == SOVEREIGN[j][i]

    print(f"\n  Row 3 (multiples of 3): {SOVEREIGN[2]}  (cycle 3,6,9)  ✓")
    print(f"  Row 9: {SOVEREIGN[8]}  (all 9)  ✓")
    print(f"  Column 9: {[SOVEREIGN[i][8] for i in range(9)]}  (all 9)  ✓")
    print(f"  Diagonal: {diag}  = [dr(i²)]  ✓")
    print(f"  Symmetric (dr(i·j)=dr(j·i))  ✓")

    # DR=9 positions: i=9 (all), j=9 (all), and wherever i*j ≡ 0 mod 9
    dr9_cells = [(i + 1, j + 1) for i in range(9) for j in range(9) if SOVEREIGN[i][j] == 9]
    # row 9 (9 cells) + col 9 (8 non-overlap) + {(3,3),(3,6),(6,3),(6,6)} = 21
    print(f"  DR=9 cells: {len(dr9_cells)}  "
          f"(row 9: 9, col 9: 8 new, (3,3)(3,6)(6,3)(6,6): 4 → 21)")
    assert len(dr9_cells) == 21

    # ── B. Fibonacci period-24 DR ─────────────────────────────────────────────
    print()
    print("=" * 70)
    print("B. Fibonacci period-24 DR  (F0 adjusted: dr(0)→9)")
    print("=" * 70)

    computed_fib_dr = fib_dr_adjusted(24)
    assert computed_fib_dr == FIB_DR_PERIOD_24, \
        f"Fib DR mismatch:\nGot:      {computed_fib_dr}\nExpected: {FIB_DR_PERIOD_24}"

    # Period-24: DRs repeat every 24 Fibonacci numbers
    fib_dr_48 = fib_dr_adjusted(48)
    assert fib_dr_48[:24] == fib_dr_48[24:48]
    print(f"\n  Period-24 DR sequence:")
    print(f"  {FIB_DR_PERIOD_24}")
    print(f"  Confirmed period = 24 (first 48 terms check)  ✓")

    # DR distribution within one period
    from collections import Counter
    fib_dist = Counter(FIB_DR_PERIOD_24)
    print(f"  DR distribution (one period): {dict(sorted(fib_dist.items()))}")
    # Each DR value 1–9 appears exactly 24/9... but 24 is not divisible by 9,
    # so distribution is not uniform. Verify actual counts.
    assert sum(fib_dist.values()) == 24
    print(f"  Total: 24 terms  ✓")

    # F0=0 is the only Fibonacci number equal to 0 in one period; DR(0)=0 → adjusted to 9
    raw_fib_drs = [dr(f) for f in fib_sequence(24)]
    assert raw_fib_drs[0] == 0          # F0=0 has DR=0
    assert FIB_DR_PERIOD_24[0] == 9     # adjusted to 9
    zero_positions = [i for i, v in enumerate(raw_fib_drs) if v == 0]
    assert zero_positions == [0]        # only F0=0 in first 24 terms
    adjusted_9_positions = [i for i, v in enumerate(FIB_DR_PERIOD_24) if v == 9]
    print(f"  Positions with DR=0 (raw): {zero_positions}  → adjusted to 9")
    print(f"  Positions with DR=9 (adjusted): {adjusted_9_positions}  ✓")

    # ── C. Lucas period-24 DR ─────────────────────────────────────────────────
    print()
    print("=" * 70)
    print("C. Lucas period-24 DR")
    print("=" * 70)

    lucas = lucas_sequence(24)
    computed_lucas_dr = [dr(l) for l in lucas]
    assert computed_lucas_dr == LUCAS_DR_PERIOD_24, \
        f"Lucas DR mismatch:\nGot:      {computed_lucas_dr}\nExpected: {LUCAS_DR_PERIOD_24}"

    # Period-24 for Lucas too
    lucas_48 = [dr(l) for l in lucas_sequence(48)]
    assert lucas_48[:24] == lucas_48[24:48]

    print(f"\n  Lucas L0..L23: {lucas}")
    print(f"  DR sequence:   {LUCAS_DR_PERIOD_24}")
    print(f"  Confirmed period = 24  ✓")

    lucas_dist = Counter(LUCAS_DR_PERIOD_24)
    print(f"  DR distribution: {dict(sorted(lucas_dist.items()))}")

    # Lucas vs Fibonacci: L_n = F_{n-1} + F_{n+1}
    fibs = fib_sequence(26)
    for n in range(1, 22):
        assert lucas[n] == fibs[n - 1] + fibs[n + 1], f"Lucas identity failed at n={n}"
    print(f"  L_n = F_{{n-1}} + F_{{n+1}} verified for n=1..21  ✓")

    # ── D. Law of 12 ──────────────────────────────────────────────────────────
    print()
    print("=" * 70)
    print("D. Law of 12: multiples of 12 have DR ∈ {3, 6, 9}")
    print("=" * 70)

    computed_law12 = law_of_12_dr(8)
    assert computed_law12 == LAW_OF_12_FIRST8, \
        f"Law of 12 mismatch: {computed_law12} vs {LAW_OF_12_FIRST8}"

    # Verify for all k=1..100
    for k in range(1, 101):
        assert dr(12 * k) in {3, 6, 9}, f"12×{k}={12*k} has DR={dr(12*k)} not in {{3,6,9}}"

    # Why: dr(12) = 3; dr(12k) = dr(3k) since 12≡3 (mod 9); dr(3k) ∈ {3,6,9}
    assert dr(12) == 3
    assert all(dr(12 * k) == dr(3 * k) for k in range(1, 101))
    assert all(dr(3 * k) in {3, 6, 9} for k in range(1, 101))

    print(f"\n  First 8 multiples of 12 and their DRs:")
    for k in range(1, 9):
        print(f"    12×{k} = {12*k:>4}  DR = {dr(12*k)}")
    print(f"\n  All k=1..100: DR(12k) ∈ {{3,6,9}}  ✓")
    print(f"  Reason: dr(12)=3; 12≡3 (mod 9); DR(3k)∈{{3,6,9}} always  ✓")

    # Period of DR(12k): cycles [3,6,9] with period 3
    law12_period3 = [dr(12 * k) for k in range(1, 10)]
    assert law12_period3 == [3, 6, 9, 3, 6, 9, 3, 6, 9]
    print(f"  Period-3 cycle: {law12_period3}  ✓")

    # ── E. Binary checkerboard ────────────────────────────────────────────────
    print()
    print("=" * 70)
    print("E. Binary checkerboard ■□ row patterns  (■=Odd, □=Even)")
    print("=" * 70)

    print(f"\n  Ascending (rows 1–9, length = row number):")
    rows_asc = []
    for length in range(1, 10):
        start_odd = True   # odd-length rows: (i+j+1)%2 pattern, row i=length starts ■
        row = checkerboard_row(length, start_odd=True)
        rows_asc.append(row)
        label = f"    row {length} (len {length}): {row}"
        print(label)

    # Verify alternation: each row strictly alternates ■ and □
    for row in rows_asc:
        for k in range(len(row) - 1):
            assert row[k] != row[k + 1], f"Row {row} not strictly alternating"
    print(f"  All rows strictly alternating  ✓")

    # Row 9 starts ■ (odd), ends ■ (9 is odd-length)
    assert rows_asc[8] == "■□■□■□■□■"
    assert len(rows_asc[8]) == 9

    print(f"\n  Descending mirror (rows 9→1):")
    for length in range(9, 0, -1):
        row = checkerboard_row(length, start_odd=True)
        print(f"    row {length} (len {length}): {row}")

    # ■□ parity map: ■ = 1 (Odd), □ = 0 (Even)
    # Row length k: starts ■ → [1,0,1,0,...] with k entries
    # Odd-length rows: first=last=■; even-length rows: first=■, last=□
    for length in range(1, 10):
        row = checkerboard_row(length, start_odd=True)
        if length % 2 == 1:
            assert row[0] == row[-1] == "■", f"Odd-length row {length} start/end mismatch"
        else:
            assert row[0] == "■" and row[-1] == "□", f"Even-length row {length} end mismatch"
    print(f"  Odd-length rows: first=last=■  ✓")
    print(f"  Even-length rows: first=■, last=□  ✓")

    # ── F. 23/32 symmetry ─────────────────────────────────────────────────────
    print()
    print("=" * 70)
    print("F. 23/32 symmetry: digit operations and parity")
    print("=" * 70)

    # Core pair
    assert digit_reverse(23) == 32
    assert digit_reverse(32) == 23
    assert dr(23) == 5
    assert dr(32) == 5
    print(f"\n  23 ↔ 32 digit reversal  (both DR=5)  ✓")

    # 23 operations
    op1 = 23 - 8          # = 15, Odd
    op2 = 21 - 3          # = 18, Even
    assert op1 == 15 and is_odd_number(15)
    assert op2 == 18 and not is_odd_number(18)
    print(f"  23 − 8 = {op1}  (Odd)  ✓")
    print(f"  21 − 3 = {op2}  (Even)  ✓")

    # 32 anchor: Even
    assert not is_odd_number(32)
    print(f"  32 anchor: Even  ✓")

    # Digit operations on 23: place-value decomposition
    assert int("2") * 10 + int("3") == 23
    assert int("3") * 10 + int("2") == 32
    d_tens_23, d_units_23 = 2, 3
    d_tens_32, d_units_32 = 3, 2
    assert d_tens_23 + d_units_23 == 5 == dr(23)
    assert d_tens_32 + d_units_32 == 5 == dr(32)
    print(f"  Digit sum: 2+3=5=DR(23)  ✓;  3+2=5=DR(32)  ✓")

    # 23 in AP {5,14,23,32}: step=9, DR=5, third member
    AP = [5, 14, 23, 32]
    assert 23 in AP and 32 in AP
    assert AP.index(23) == 2 and AP.index(32) == 3
    print(f"  AP {{5,14,23,32}}: 23 is member 3, 32 is member 4 (last)  ✓")

    # Parity of AP members
    parity_AP = ["Odd" if x % 2 == 1 else "Even" for x in AP]
    assert parity_AP == ["Odd", "Even", "Odd", "Even"]
    print(f"  AP parity: {list(zip(AP, parity_AP))}  (alternating)  ✓")

    # Binary representation: 23=10111, 32=100000
    assert bin(23) == "0b10111"
    assert bin(32) == "0b100000"
    print(f"  23 = {bin(23)}  (5 bits)  ✓")
    print(f"  32 = {bin(32)}  (6 bits, power of 2)  ✓")
    assert 32 == 2 ** 5
    print(f"  32 = 2^5  ✓")

    # 0-1 / 00-11 / 000-111 bit ranges
    ranges = {
        1: (0, 1),    # 1-bit: [0,1]
        2: (0, 3),    # 2-bit: [0,3]
        3: (0, 7),    # 3-bit: [0,7]
        4: (0, 15),   # 4-bit: [0,15]
        5: (0, 31),   # 5-bit: [0,31]
    }
    for bits, (lo, hi) in ranges.items():
        assert lo == 0 and hi == 2 ** bits - 1
    print(f"\n  Bit-length ranges: { {b: f'[0,{2**b-1}]' for b in range(1,6)} }  ✓")
    # 23 fits in 5 bits (0..31); 32 requires 6 bits (0..63)
    assert 0 <= 23 <= 31
    assert 0 <= 32 <= 63
    print(f"  23 ∈ [0,31] (5-bit range)  ✓;  32 ∈ [0,63] (6-bit range)  ✓")

    print()
    print("All assertions passed.")


if __name__ == "__main__":
    verify()
