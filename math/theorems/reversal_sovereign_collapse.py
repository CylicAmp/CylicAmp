"""
Reversal DR Collapse — Sovereign Fixed Point is Universal Attractor
=====================================================================

THEOREM 1 (REVERSAL COLLAPSE):
  For any positive integer n with rev(n) having the same number of digits
  and n ≠ rev(n):
    DR(|n − rev(n)|) = 9  (sovereign fixed point, always)

  Proof: digit sum is invariant under digit permutation.
    n ≡ digit_sum(n) (mod 9)
    rev(n) ≡ digit_sum(rev(n)) = digit_sum(n) (mod 9)
    → n ≡ rev(n) (mod 9)
    → n − rev(n) ≡ 0 (mod 9)
    → 9 | (n − rev(n)) → DR = 9 (sovereign fixed point)
  Zero violations over all integers — this is algebraic, not statistical.

  Emirp consequence: rev(p) − p ≡ 0 (mod 9) always.
  The mod-37 non-uniformity is the ONLY structure that survives after
  the sovereign collapse in DR algebra. GF(37) filters what 9 cannot see.

Verified pairs:
  |137−731| = 594  DR=9   |147−741| = 594  DR=9
  |175−571| = 396  DR=9   |157−751| = 594  DR=9
  |248−842| = 594  DR=9   |649−946| = 297  DR=9
  |715−517| = 198  DR=9   |571−175| = 396  DR=9

THEOREM 2 (6n SOVEREIGN LOCK):
  Every twin prime midpoint is 6n (for some positive integer n).
  DR(6n) is always in the sovereign set {3, 6, 9}.

  The mapping DR(n) → DR(6n):
    DR(n) ∈ {1,4,7}  →  DR(6n) = 6   [chi_{-3}(n) = +1]
    DR(n) ∈ {2,5,8}  →  DR(6n) = 3   [chi_{-3}(n) = -1]
    DR(n) ∈ {3,6,9}  →  DR(6n) = 9   [chi_{-3}(n) = 0]

  Equivalently: DR(6n) depends only on chi_{-3}(n).
    chi_{-3}(n) = +1  →  DR(6n) = 6  (sovereign)
    chi_{-3}(n) = −1  →  DR(6n) = 3  (sovereign)
    chi_{-3}(n) =  0  →  DR(6n) = 9  (sovereign fixed point)

  Every twin prime midpoint is locked in the sovereign set by multiplication
  by 6. The three sovereign values {3,6,9} appear with equal frequency
  (~33% each) in the twin prime midpoint DR distribution.

  Actual distribution over 8168 twin pairs up to 10^6:
    DR=3: 2651  (32.46%)   [chi_{-3}(n) = −1 → midpoints 6n with n ≡ 2 mod 3]
    DR=6: 2788  (34.13%)   [chi_{-3}(n) = +1 → midpoints 6n with n ≡ 1 mod 3]
    DR=9: 2729  (33.41%)   [chi_{-3}(n) =  0 → midpoints 6n with n ≡ 0 mod 3]

  The chi_{-3} value of the INDEX n determines which sovereign DR
  the MIDPOINT 6n carries. The midpoint itself is always sovereign.

142857 NOTE:
  142857 = 3³ × 11 × 13 × 37
  DR(142857) = 9  (sovereign, as expected: 1+4+2+8+5+7=27→9)
  142857 ≡ 0 (mod 37)  (37-null element)
  142857 ≡ 3 (mod 6)   (NOT a twin prime midpoint — wrong residue class)
  1/7 = 0.142857142857...  (cyclic number for 7)
  All six cyclic permutations of 142857 have DR=9:
    142857, 428571, 285714, 857142, 571428, 714285 — all DR=9.
"""


def dr(n: int) -> int:
    return (n - 1) % 9 + 1 if n > 0 else 0


def chi_m3(n: int) -> int:
    r = n % 3
    if r == 1:
        return 1
    if r == 2:
        return -1
    return 0


def rev_num(n: int) -> int:
    s = str(n)[::-1]
    return int(s) if s[0] != "0" else None


def sieve(limit: int):
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i :: i] = bytearray(len(is_p[i * i :: i]))
    return is_p


# ── THEOREM 1: REVERSAL COLLAPSE ─────────────────────────────────────────────

specific_pairs = [
    (137, 731), (147, 741), (175, 571), (157, 751),
    (248, 842), (649, 946), (751, 157), (715, 517), (571, 175),
]
for a, b in specific_pairs:
    assert dr(abs(a - b)) == 9, f"|{a}−{b}|={abs(a-b)}: DR should be 9"
    assert abs(a - b) % 9 == 0, f"|{a}−{b}| should be divisible by 9"

# Universal verification: all n from 10 to 10000
violations = 0
for n in range(10, 10001):
    r = rev_num(n)
    if r and len(str(r)) == len(str(n)) and n != r:
        diff = abs(n - r)
        if dr(diff) != 9:
            violations += 1
assert violations == 0, f"Reversal collapse violated {violations} times"

# ── THEOREM 2: 6n SOVEREIGN LOCK ─────────────────────────────────────────────

# DR(6n) depends only on chi_{-3}(n)
for n_dr in range(1, 10):
    result = dr(6 * n_dr)
    c = chi_m3(n_dr)
    if c == 1:
        assert result == 6, f"DR(6×{n_dr})={result}, expected 6 for chi=+1"
    elif c == -1:
        assert result == 3, f"DR(6×{n_dr})={result}, expected 3 for chi=-1"
    else:
        assert result == 9, f"DR(6×{n_dr})={result}, expected 9 for chi=0"

# DR(6n) is always sovereign
for n in range(1, 10001):
    assert dr(6 * n) in {3, 6, 9}, f"DR(6×{n}) not sovereign"

# Verify with actual twin prime midpoints
is_p = sieve(10 ** 6)
from collections import Counter
mid_drs = Counter(dr(p + 1) for p in range(5, 10 ** 6 - 1) if is_p[p] and is_p[p + 2])
assert set(mid_drs.keys()) == {3, 6, 9}, f"Midpoint DRs not all sovereign: {mid_drs}"

# Verify chi_{-3}(n) → DR(6n) mapping holds for all twin pairs
for p in range(5, 10 ** 6 - 1):
    if is_p[p] and is_p[p + 2]:
        mid = p + 1
        n = mid // 6  # midpoint = 6n
        assert mid == 6 * n
        expected = {1: 6, -1: 3, 0: 9}[chi_m3(n)]
        assert dr(mid) == expected, f"Midpoint {mid}: DR={dr(mid)}, expected {expected}"

# ── 142857 ────────────────────────────────────────────────────────────────────

assert 142857 == 3 ** 3 * 11 * 13 * 37
assert 142857 % 37 == 0
assert 142857 % 6 == 3  # not a twin prime midpoint
assert dr(142857) == 9

# All six cyclic permutations of 142857 have DR=9
cyclic_142857 = [142857, 428571, 285714, 857142, 571428, 714285]
assert all(dr(x) == 9 for x in cyclic_142857)
# All are multiples of 9?
assert all(x % 9 == 0 for x in cyclic_142857)


if __name__ == "__main__":
    print("REVERSAL DR COLLAPSE AND 6n SOVEREIGN LOCK")
    print("=" * 55)
    print()

    print("Theorem 1 — Reversal Collapse:")
    print("  n − rev(n) ≡ 0 (mod 9) → DR(|n − rev(n)|) = 9, always")
    print("  Proof: digit sum invariant under permutation → n ≡ rev(n) mod 9")
    print()
    print("  Specific pairs:")
    for a, b in specific_pairs:
        d = abs(a - b)
        print(f"    |{a}−{b}| = {d:>3}  = 9×{d//9}  DR={dr(d)}")
    print(f"  Universal check (n=10..10000): {violations} violations")
    print()

    print("Theorem 2 — 6n Sovereign Lock:")
    print("  DR(6n) depends only on chi_{-3}(n):")
    print("  chi_{-3}(n) | DR(6n) | Column")
    print("  ---------------------+--------+-------")
    print("       +1              |   6    | COL2 (sovereign)")
    print("       −1              |   3    | COL1 (sovereign)")
    print("        0              |   9    | COL3 (fixed point)")
    print()

    print("  DR map:")
    for dn in range(1, 10):
        c = chi_m3(dn)
        print(f"    DR(n)={dn}  chi={c:+d}  →  DR(6n)={dr(6*dn)}")
    print()

    total = sum(mid_drs.values())
    print(f"  Twin prime midpoint DR distribution ({total} pairs up to 10^6):")
    for k in [3, 6, 9]:
        v = mid_drs[k]
        print(f"    DR={k}: {v}  ({v/total*100:.2f}%)")
    print("  All sovereign — none in {1,2,4,5,7,8}")
    print()

    print("142857 = 3³ × 11 × 13 × 37:")
    print(f"  DR(142857) = {dr(142857)}  (sovereign fixed point)")
    print(f"  142857 mod 37 = {142857 % 37}  (37-null)")
    print(f"  142857 mod 6  = {142857 % 6}   (not a twin prime midpoint)")
    print("  Cyclic permutations and their DRs:")
    for x in cyclic_142857:
        print(f"    {x}  DR={dr(x)}  mod37={x%37}")
    print()
    print("All assertions passed.")
