"""
AHL-17 Grid Structure
Absolute Harmonic Location = 8 = DR(17)

Results:

1. IDENTITY
   DR(17) = 8 = AHL
   17 is the carrier of AHL in the natural numbers.

2. DOUBLING ORBIT SHIFT
   17 + 17 = 34    DR(34) = 7    (orbit shifts -1 from AHL)
   Chain to recover AHL: 7+7=14, 14+6=20, 20+6=26  →  DR(26) = 8
   Two applications of the twin prime period (6) restore AHL.

3. 9-PRESERVATION (fixed-point absorption)
   9 is the fixed point of DR. Adding 9 never changes DR:
     17 + 9  = 26   DR(26) = 8  ✓
     26 + 9  = 35   DR(35) = 8  ✓
     35 + 9  = 44   DR(44) = 8  ✓
   DR(17 + 9k) = 8 for all k ≥ 0.

4. ALTERNATING 1,7 SEQUENCE
   Build a string by repeating the digits of 17 (1 and 7):
     9  digits: 1 7 1 7 1 7 1 7 1  →  DS = 33, DR = 6   (ends MATCH: 1 … 1)
     10 digits: 1 7 1 7 1 7 1 7 1 7  →  DS = 40, DR = 4  (ends OPPOSE: 1 … 7)
   At 10 digits the endpoints are {1,7} — exactly the digits of 17.
   DR(40) = 4 = (1+7)/2 — the mean of the digit pair.

5. STACKED-17 GRID (down vs across)
   Stack two copies of 17 vertically:
       1  7
       1  7
   Operations:
     Column (down):   left  1+1=2,  right 7+7=14 → DR=5
     Diagonal (across): 1+7=8  (AHL recovered)

   Result: cross-addition (diagonal) recovers AHL; column does not.

6. FULL GRID WITH TOP/BOTTOM ROW
   Top row:  8+2  or  2+8  (switchable — addition is commutative, sum=10, DR=1)
   Middle:   columns give 1+1=2,  diagonal gives 1+7=8
   Bottom:   FIXED at 2+8  (left=column result=2, right=diagonal result=8)

   Top is free; bottom is locked by the order produced in the middle.
   You can swap middle-row digit order (1+7 vs 7+1) but cannot change
   that the column operation determines the left value and the diagonal
   determines the right value — so bottom is always 2+8.

7. PALINDROME DR CHAIN (from grid explorations)
   5-5-5       DS=15  DR=6
   5-77-5      DS=24  DR=6  (cascade base 24)
   32-1616-32  DS=24  DR=6  (cascade base preserved)
   4224        DS=12  DR=3  (sovereign target: 2^28 mod 37 = 12)
   48282848    DS=44  DR=8  (returns to AHL)
"""


def dr(n: int) -> int:
    return (n - 1) % 9 + 1 if n > 0 else 0


def ds(digits) -> int:
    return sum(int(d) for d in str(digits) if d.isdigit())


# 1. Identity
assert dr(17) == 8, "DR(17) must equal 8 (AHL)"

# 2. Doubling orbit shift and recovery
assert dr(34) == 7, "DR(34) must equal 7"
# chain: 7+7=14, 14+6=20, 20+6=26
recovery_chain = [14, 20, 26]
assert dr(26) == 8, "Chain must recover DR=8"

# 3. 9-preservation
for k in range(20):
    assert dr(17 + 9 * k) == 8, f"9-preservation failed at k={k}"

# 4. Alternating 1,7 sequence
seq9  = [1, 7, 1, 7, 1, 7, 1, 7, 1]
seq10 = [1, 7, 1, 7, 1, 7, 1, 7, 1, 7]
ds9   = sum(seq9)   # 33
ds10  = sum(seq10)  # 40
assert ds9 == 33 and dr(33) == 6
assert ds10 == 40 and dr(40) == 4
assert seq9[0]  == seq9[-1],  "9-digit ends must match"
assert seq10[0] != seq10[-1], "10-digit ends must oppose"

# 5. Column vs diagonal
left_col  = 1 + 1  # 2
right_col = 7 + 7  # 14 → DR=5
diagonal  = 1 + 7  # 8 = AHL
assert dr(diagonal) == 8, "Diagonal must recover AHL"
assert dr(right_col) == 5, "Right column DR must equal 5"

# 6. Grid bottom fixed at 2+8
bottom_left  = left_col   # 2
bottom_right = diagonal   # 8
assert bottom_left == 2 and bottom_right == 8

# 7. Palindrome chain
palindromes = {
    "5-5-5":       (15, 6),
    "5-77-5":      (24, 6),
    "32-1616-32":  (24, 6),
    "4224":        (12, 3),
    "48282848":    (44, 8),
}
for name, (expected_ds, expected_dr) in palindromes.items():
    assert dr(expected_ds) == expected_dr, f"Palindrome {name} failed"


if __name__ == "__main__":
    print("AHL-17 GRID STRUCTURE")
    print("=" * 40)
    print(f"DR(17) = {dr(17)} = AHL")
    print()
    print("Doubling orbit shift:")
    print(f"  17+17 = 34   DR(34) = {dr(34)}")
    print(f"  Recovery chain: 14 → 20 → 26   DR(26) = {dr(26)}")
    print()
    print("9-preservation (first 5 steps):")
    for k in range(5):
        n = 17 + 9 * k
        print(f"  17 + 9×{k} = {n:>3}   DR = {dr(n)}")
    print()
    print("Alternating 1,7 sequence:")
    print(f"   9 digits: DS={ds9}  DR={dr(ds9)}  ends: {seq9[0]}…{seq9[-1]} (match)")
    print(f"  10 digits: DS={ds10} DR={dr(ds10)}  ends: {seq10[0]}…{seq10[-1]} (oppose = digits of 17)")
    print()
    print("Grid (down vs across):")
    print("  1  7")
    print("  1  7")
    print(f"  Column:   2  {right_col}={dr(right_col)} DR")
    print(f"  Diagonal: 1+7={diagonal} → DR={dr(diagonal)} (AHL)")
    print()
    print("Bottom row fixed: 2+8")
    print()
    print("Palindrome DR chain:")
    for name, (d, r) in palindromes.items():
        print(f"  {name:>12}  DS={d:>2}  DR={r}")
    print()
    print("All assertions passed.")
