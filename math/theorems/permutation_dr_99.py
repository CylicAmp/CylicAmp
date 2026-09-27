"""
permutation_dr_99.py

For any 3-digit number N = 100a + 10b + c with reverse R = 100c + 10b + a:

  N - R = 99(a - c)

Since 99 = 9 × 11, all differences are divisible by 9.
When a ≠ c (non-palindrome), |N - R| ≥ 99 and dr(|N-R|) = 9.
When a = c (palindrome), N - R = 0 and dr(0) = 0.

Permutation invariant: all permutations of the same digit set share
the same digit sum and digital root (digit sum is invariant under permutation).
"""

from itertools import permutations

def dr(n): return 0 if n == 0 else 1+(n-1)%9

# ── PERMUTATION INVARIANCE ────────────────────────────────────────────────────

perms_123 = [int(''.join(map(str,p))) for p in permutations([1,2,3])]
assert all(sum(int(d) for d in str(v)) == 6 for v in perms_123)
assert all(dr(v) == 6 for v in perms_123)
assert all(v % 9 == 6 for v in perms_123)

# ── DIFFERENCE FORMULA ────────────────────────────────────────────────────────

# Algebraic proof:
# N - R = (100a+10b+c) - (100c+10b+a) = 99a - 99c = 99(a-c)
for N in range(100, 1000):
    s = str(N)
    a, c = int(s[0]), int(s[2])
    R = int(s[::-1])
    assert N - R == 99 * (a - c)
    if a != c:
        assert dr(abs(N - R)) == 9

# ── PALINDROME CASE ───────────────────────────────────────────────────────────

for N in [121, 353, 787, 999]:
    assert str(N) == str(N)[::-1]   # palindrome
    assert N - int(str(N)[::-1]) == 0
    assert dr(0) == 0

# ── SPECIFIC PERMUTATION PAIRS ────────────────────────────────────────────────

assert 321 - 123 == 99 * 2 and dr(198) == 9
assert 312 - 213 == 99 * 1 and dr(99)  == 9
assert 231 - 132 == 99 * 1 and dr(99)  == 9

# ── OUTPUT ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Permutation DR and N-R=99(a-c)")
    print("=" * 50)
    print("  Permutations of {1,2,3}: all DR=6")
    print("  N-R = 99(a-c)  for any 3-digit N")
    print("  a≠c → |N-R| = 99|a-c| ≥ 99 → dr=9")
    print("  a=c → N-R = 0 → dr=0  (palindrome)")
    print("  Verified over all 900 three-digit integers.")
    print()
    print("All assertions passed.")
