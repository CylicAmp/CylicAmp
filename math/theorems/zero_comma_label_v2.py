"""
Zero-Comma Label System v2: Uniform Suffix

Label formula:  left_size + str(K) * (2K)

  K        = number of commas  = (n-1) // 3
  left_size = leftmost group   = n % 3  (0 → 3)
  label     = str(left_size) + str(K) * (2*K)   → always 2K+1 digits

Each level K contains exactly 3 zero-strings (left_size = 1, 2, 3).
Within a level the suffix is entirely uniform (all Ks); only the
first digit changes.

ALL-SAME entries (left_size = K → every digit identical):
  K=1 → n=4  → "111"       (3 digits)
  K=2 → n=8  → "22222"     (5 digits)
  K=3 → n=12 → "3333333"   (7 digits)
  IMPOSSIBLE for K ≥ 4: left_size ∈ {1,2,3}, K ≥ 4 → left_size < K always.

All-same labels have digit counts 3, 5, 7 — the 357 anti-diagonal.
They occur at n = 4K (K = 1,2,3 only):  n = 4, 8, 12.

Additional structural facts:
  • Label digit count = 2K+1 is ALWAYS ODD  (OddPerfect property)
  • 111 = 3 × 37   (37-hub connection)
  • 2K+1 for K=1,2,3 gives {3, 5, 7} — prime, and the 357 constant
  • left_size cycles 1→2→3→1→2→3→... forever; K grows without bound
  • After K=3, the all-same condition left_size=K is never satisfied again
"""


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def comma_groups(n):
    groups, r = [], n
    while r > 3:
        groups.append(3)
        r -= 3
    groups.append(r)
    return list(reversed(groups))


def zero_string(n):
    return ",".join("0" * g for g in comma_groups(n))


def label(n):
    """Uniform-suffix label for n zeros (n ≥ 4)."""
    assert n >= 4
    K = (n - 1) // 3
    left = n % 3 or 3
    return str(left) + str(K) * (2 * K)


# ---------------------------------------------------------------------------
# Assertions — verify all published examples
# ---------------------------------------------------------------------------

_examples = {
    4:  "111",
    5:  "211",
    6:  "311",
    7:  "12222",
    8:  "22222",
    9:  "32222",
    10: "1333333",
    11: "2333333",
    12: "3333333",
    13: "144444444",
    14: "244444444",
    15: "344444444",
    16: "15555555555",
}

for n, expected in _examples.items():
    got = label(n)
    assert got == expected, f"n={n}: got {got!r}, expected {expected!r}"

# Label length = 2K+1 (always odd) — valid while K is single digit (n ≤ 30)
for n in range(4, 31):
    K = (n - 1) // 3
    assert len(label(n)) == 2 * K + 1,  f"n={n} K={K} len={len(label(n))}"
    assert (2 * K + 1) % 2 == 1

# First digit = left_size = n%3 (0→3), cycles 1,2,3,1,2,3,...
for n in range(4, 31):
    left = n % 3 or 3
    assert int(label(n)[0]) == left

# Suffix all = K (single-digit K only)
for n in range(4, 31):
    K = (n - 1) // 3
    assert all(c == str(K) for c in label(n)[1:])

# ALL-SAME entries: exactly n=4,8,12 (search up to K≤9 i.e. n≤30)
all_same = [n for n in range(4, 31) if len(set(label(n))) == 1]
assert all_same == [4, 8, 12], f"all-same: {all_same}"

# All-same digit counts = 3, 5, 7
assert [len(label(n)) for n in all_same] == [3, 5, 7]

# 111 = 3 × 37
assert 111 == 3 * 37

# All-same at n = 4K (K=1,2,3)
for i, n in enumerate(all_same, start=1):
    assert n == 4 * i


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Zero-Comma Label System v2")
    print("=" * 64)
    print("  formula: left_size + K*(2K)   [label has 2K+1 digits, always odd]")
    print()
    print(f"  {'n':>3}  {'zero-string':>26}  K  {'label':<18}  note")
    print("  " + "-" * 62)

    for n in range(4, 22):
        K = (n - 1) // 3
        raw = label(n)
        note = "ALL %s  ← 3×37" % raw[0] if raw[0] == str(K) and len(set(raw)) == 1 and K <= 3 else (
               "all %s" % raw[0] if len(set(raw)) == 1 else "")
        print(f"  {n:>3}  {zero_string(n):>26}  {K}  {raw:<18}  {note}")

    print()
    print("ALL-SAME entries (left_size = K, impossible for K ≥ 4):")
    for n in [4, 8, 12]:
        K = (n - 1) // 3
        raw = label(n)
        print(f"  n={n:>2}  K={K}  label={raw:<10}  {len(raw)} digits  "
              f"DR={dr(sum(int(c) for c in raw))}")

    print()
    print("Digit counts of all-same labels: 3, 5, 7  ← 357 anti-diagonal")
    print("111 = 3 × 37  ← 37-hub")
    print()
    print("Label digit counts by level:")
    for K in range(1, 7):
        n0 = 3 * K + 1
        print(f"  K={K}: {2*K+1} digits (odd)  — zero-string n={n0}..{n0+2}")
    print()
    print("All assertions passed.")
