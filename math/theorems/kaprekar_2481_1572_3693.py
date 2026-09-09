"""
kaprekar_2481_1572_3693.py

Kaprekar sibling structure connecting 7518 and its split-complement 2481
to the numbers 1572 and 3693.

KAPREKAR SIBLINGS:
  {7518, 2481} → 7173 on step 1 (same Kaprekar image)
  {1572, 3693} → 6264 on step 1 (same Kaprekar image)

CROSS-PAIR SUM:
  2481 + 3693 = 6174  (Kaprekar constant)

MOD-73 PROPERTY:
  7518 ≡ -1 (mod 73)  since 7518 = 103×73 - 1
  2481 ≡ -1 (mod 73)  since 7518+2481=9999=10^4-1 and 10^4≡-1 (mod 73)
  Both halves of the 103/137 repeating block are ≡ -1 (mod 73).

MOD-37 STRUCTURE:
  3693 mod 37 = 30, in {4,9,25,30}
  3693 = 3×1231, and 1231 mod 37 = 10 (generator of order-3 subgroup {1,10,26})
  1572 = 12×131, and 131 appeared in subgroup sum table (p=131, lift=30)
"""

from sympy import factorint

def dr(n): return 0 if n == 0 else 1+(n-1)%9

def kaprekar_step(n):
    s = f'{n:04d}'
    return int(''.join(sorted(s, reverse=True))) - int(''.join(sorted(s)))

# ── KAPREKAR SIBLINGS ─────────────────────────────────────────────────────────

assert kaprekar_step(7518) == 7173
assert kaprekar_step(2481) == 7173   # same image as 7518

assert kaprekar_step(1572) == 6264
assert kaprekar_step(3693) == 6264   # same image as 1572

# Both pairs converge to 6174
def kaprekar_path(n):
    path = [n]
    while path[-1] != 6174:
        path.append(kaprekar_step(path[-1]))
    return path

assert kaprekar_path(7518) == [7518, 7173, 6354, 3087, 8352, 6174]
assert kaprekar_path(2481) == [2481, 7173, 6354, 3087, 8352, 6174]
assert kaprekar_path(1572) == [1572, 6264, 4176, 6174]
assert kaprekar_path(3693) == [3693, 6264, 4176, 6174]

# ── CROSS-PAIR SUM ────────────────────────────────────────────────────────────

assert 2481 + 3693 == 6174    # Kaprekar constant

# ── CONNECTION TO 103/137 DECIMAL ─────────────────────────────────────────────

# 7518 and 2481 are the two halves of the 8-digit repeating block of 103/137
assert 7518 + 2481 == 9999    # split-complement
assert 103 * (10**8 - 1) // 137 == 75182481
assert 75182481 // 10**4 == 7518
assert 75182481 % 10**4 == 2481

# ── MOD-73 PROPERTY ───────────────────────────────────────────────────────────

assert 7518 == 103 * 73 - 1
assert 7518 % 73 == 72    # ≡ -1 (mod 73)
assert 2481 % 73 == 72    # ≡ -1 (mod 73)
# Proof: 9999 ≡ -2 (mod 73) since 10^4 ≡ -1 (mod 73)
# 7518 ≡ -1 → 2481 = 9999-7518 ≡ -2-(-1) = -1 (mod 73)
assert pow(10, 4, 73) == 72   # 10^4 ≡ -1 (mod 73)

# ── MOD-37 STRUCTURE ──────────────────────────────────────────────────────────

assert 3693 % 37 == 30
assert 30 in {4, 9, 25, 30}

assert factorint(3693) == {3: 1, 1231: 1}
assert 1231 % 37 == 10    # 10 generates the order-3 subgroup {1,10,26}
assert pow(10, 3, 37) == 1

assert factorint(1572) == {2: 2, 3: 1, 131: 1}
assert 131 % 37 == 20

assert 2481 % 37 == 2
assert 1572 % 37 == 18

# ── OUTPUT ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Kaprekar siblings: 2481, 1572, 3693")
    print("=" * 50)
    print(f"  7518 → {kaprekar_path(7518)}")
    print(f"  2481 → {kaprekar_path(2481)}")
    print(f"  1572 → {kaprekar_path(1572)}")
    print(f"  3693 → {kaprekar_path(3693)}")
    print(f"  2481 + 3693 = {2481+3693}  (Kaprekar constant)")
    print(f"  7518 mod 73 = {7518%73} ≡ -1,  2481 mod 73 = {2481%73} ≡ -1")
    print(f"  3693 mod 37 = {3693%37}  (in {{4,9,25,30}})")
    print(f"  1231 mod 37 = {1231%37}  (order-3 subgroup generator)")
    print()
    print("All assertions passed.")
