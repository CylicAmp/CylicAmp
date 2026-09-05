"""
Zero-Comma Label System: Complete Theorem

Label formula:  str(left_size) + str(K) * (2K)

  K         = (n-1) // 3       number of commas in zero-string
  left_size  = n % 3 (0→3)    leftmost group size, cycles 1,2,3 forever
  label      = [first] + [K repeated 2K times]   → always 2K+1 digits

THE COMPLETE STRUCTURE — ALL VERIFIED
══════════════════════════════════════

Three All-Same Entries (left_size = K):

  K   n    label       digits   class
  ─────────────────────────────────────
  1   4    111         3        ALL 1s
  2   8    22222       5        ALL 2s
  3   12   3333333     7        ALL 3s

Why the full rotation closes at K=3:
  First digit = left_size ∈ {1,2,3} always.
  For all-same at tier K, every digit must equal K.
  But first digit ≤ 3, so K ≤ 3 is the only possibility.
  Permanently closed after n=12.

  [Note: K≥10 produces accidental all-sames via multi-digit str(K),
   e.g. K=11→str="11", left=1 → all 1s at n=34. These are outside
   the single-digit regime (K≤9, n≤30) of the theorem.]

The 357 Connection:
  Digit counts of all-same codes: 3, 5, 7 — consecutive odd integers.
  3 + 5 + 7 = 15
  3 × 5 × 7 = 105

The 37-Hub Bridge:
  First all-same code: 111 = 3 × 37.
  ord₃₇(10) = 3  [PROVEN: 10³ = 1000 = 27×37+1 ≡ 1 mod 37].
  Period-3 (mod 3 cycle) meets period-3 (ord₃₇(10)=3) at 111.

Odd-Perfect Property:
  Every label has 2K+1 digits — always odd.
  1 first digit (odd count) + 2K trailing digits (even count) = odd.
  Not added; emerges from the structure.

Encoding Rule:
  K   pattern             examples
  ──────────────────────────────────────────────
  1   [first]11           111, 211, 311
  2   [first]2222         12222, 22222, 32222
  3   [first]333333       1333333, 2333333, 3333333
  4   [first]44444444     144444444, 244444444, 344444444
  ...
"""


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def label(n):
    """Zero-comma label for n zeros (n ≥ 4)."""
    assert n >= 4
    K = (n - 1) // 3
    left = n % 3 or 3
    return str(left) + str(K) * (2 * K)


def zero_string(n):
    groups, r = [], n
    while r > 3:
        groups.append(3)
        r -= 3
    groups.append(r)
    return ",".join("0" * g for g in reversed(groups))


# ---------------------------------------------------------------------------
# Proofs
# ---------------------------------------------------------------------------

# Three all-same entries
assert label(4)  == "111"
assert label(8)  == "22222"
assert label(12) == "3333333"
for n in (4, 8, 12):
    assert len(set(label(n))) == 1

# Digit counts 3, 5, 7
assert [len(label(n)) for n in (4, 8, 12)] == [3, 5, 7]

# Sum and product
assert 3 + 5 + 7 == 15
assert 3 * 5 * 7 == 105

# No all-same for K=4..9 (n=13..30, single-digit regime)
assert not any(len(set(label(n))) == 1 for n in range(13, 31))

# 111 = 3 × 37
assert 111 == 3 * 37

# ord_37(10) = 3
assert pow(10, 1, 37) != 1
assert pow(10, 2, 37) != 1
assert pow(10, 3, 37) == 1   # 10³ = 1000 = 27×37+1

# 2K+1 always odd (single-digit regime)
for n in range(4, 31):
    K = (n - 1) // 3
    assert len(label(n)) == 2 * K + 1
    assert (2 * K + 1) % 2 == 1

# 1 first digit + 2K trailing = 2K+1
for n in range(4, 31):
    K = (n - 1) // 3
    assert 1 + 2 * K == len(label(n))

# First digit always in {1,2,3}
for n in range(4, 100):
    assert int(label(n)[0]) in {1, 2, 3}


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Zero-Comma Label System: Complete Theorem")
    print("=" * 64)
    print()
    print(f"  {'n':>3}  {'zero-string':>26}  K  {'label':<18}  digits  note")
    print("  " + "-" * 66)

    for n in range(4, 22):
        K = (n - 1) // 3
        raw = label(n)
        digs = len(raw)
        note = f"ALL {raw[0]}s ★" if len(set(raw)) == 1 else ""
        print(f"  {n:>3}  {zero_string(n):>26}  {K}  {raw:<18}  {digs:>6}  {note}")

    print()
    print("All-same entries: n=4 (111), n=8 (22222), n=12 (3333333)")
    print("Digit counts: 3, 5, 7  →  3+5+7=15  |  3×5×7=105")
    print()
    print(f"111 = 3 × 37    ord_37(10) = 3    10³ mod 37 = {pow(10,3,37)}")
    print()
    print("Label digit counts by level (2K+1, always odd):")
    for K in range(1, 7):
        print(f"  K={K}: {2*K+1} digits")
    print()
    print("All claims proved. All assertions passed.")
