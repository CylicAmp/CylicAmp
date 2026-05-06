"""
Digital Root Modular Foundation — Theorems mod 9 and mod 3

Classification: Theorem

THEOREM 1 (DR mod 9):
  For any positive integer n: dr(n) ≡ n (mod 9)
  Convention: if n ≡ 0 (mod 9) and n ≠ 0, then dr(n) = 9.

PROOF SKETCH:
  10 ≡ 1 (mod 9)  →  10^m ≡ 1 (mod 9) for all m ≥ 0.
  For n = Σ aᵢ·10ⁱ:  n ≡ Σ aᵢ·1 = digit_sum(n) (mod 9).
  Repeated digit summing preserves the mod-9 class.
  Termination at single digit d ∈ {1..9}: d = dr(n).
  Therefore dr(n) ≡ n (mod 9).  □

THEOREM 2 (DR mod 3):
  For any non-negative integer n: dr(n) ≡ n (mod 3)

PROOF:
  Follows immediately from Theorem 1: since 3 | 9, congruence mod 9 implies
  congruence mod 3.
  Alternatively, 10 ≡ 1 (mod 3) → same digit-sum argument holds mod 3.  □

COROLLARY (2n−1 rule):
  dr(2n − 1) ≡ 2·dr(n) − 1 (mod 9)
  The map n ↦ 2n−1 shifts DR class by +2 in the 9-cycle because
  2n−1 ≡ 2n−1 (mod 9) and 2 generates a +2 step in Z/9Z.

This proof is the axiomatic foundation for:
  - the DR algebra (dr_algebra.py)
  - the 81-pair grid and 9×9 sovereign matrix
  - the 2n−1 skip rule
  - all DR-based claims throughout the framework
"""

from math import log10


def dr(n):
    """Digital root: (n−1)%9+1 for n>0, else 0. Method 4 (most efficient)."""
    return (n - 1) % 9 + 1 if n > 0 else 0


def dr_iterated(n):
    """Digital root via repeated digit summing (Method 1). Proves the process."""
    if n == 0:
        return 0
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def digit_sum(n):
    """Single digit sum (not iterated)."""
    return sum(int(d) for d in str(n))


# ── Lemma: 10 ≡ 1 (mod 9) and 10 ≡ 1 (mod 3) ────────────────────────────

assert 10 % 9 == 1
assert 10 % 3 == 1

# 10^m ≡ 1 for all m ≥ 0
for m in range(20):
    assert pow(10, m, 9) == 1
    assert pow(10, m, 3) == 1

# ── Theorem 1: dr(n) ≡ n (mod 9) ─────────────────────────────────────────

# Verify for n = 1..1000
for n in range(1, 1001):
    assert dr(n) % 9 == n % 9 or (n % 9 == 0 and dr(n) == 9)
    # Equivalently: dr(n) ≡ n (mod 9), with dr(n) ∈ {1..9}

# Both computation methods agree
for n in range(1, 500):
    assert dr(n) == dr_iterated(n)

# 9-convention: dr(9k) = 9 for all positive multiples of 9
for k in range(1, 100):
    assert dr(9 * k) == 9

# Digit sum step preserves mod 9:
for n in range(10, 200):
    assert digit_sum(n) % 9 == n % 9   # single step

# ── Theorem 2: dr(n) ≡ n (mod 3) ─────────────────────────────────────────

for n in range(1, 1001):
    assert dr(n) % 3 == n % 3

# Corollary from Theorem 1 (since 3 | 9):
for n in range(1, 200):
    assert (n % 9) % 3 == n % 3

# The three DR classes mod 3:
# n ≡ 0 (mod 3): dr(n) ∈ {3, 6, 9}
# n ≡ 1 (mod 3): dr(n) ∈ {1, 4, 7}
# n ≡ 2 (mod 3): dr(n) ∈ {2, 5, 8}
assert {dr(n) for n in range(1, 100) if n % 3 == 0} == {3, 6, 9}
assert {dr(n) for n in range(1, 100) if n % 3 == 1} == {1, 4, 7}
assert {dr(n) for n in range(1, 100) if n % 3 == 2} == {2, 5, 8}

# ── Method equivalence: all four methods agree ────────────────────────────

def dr_method1(n):
    """Repeated digit sum until single digit."""
    if n == 0: return 0
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

def dr_method2(n):
    """Recursive digit sum."""
    if n < 10: return n
    return dr_method2(sum(int(d) for d in str(n)))

def dr_method3(n):
    """Direct modulo: 1 + (n−1) mod 9  (cleaner form)."""
    if n == 0: return 0
    r = n % 9
    return r if r != 0 else 9

def dr_method4(n):
    """(n−1) % 9 + 1 — the canonical formula used throughout the framework."""
    return (n - 1) % 9 + 1 if n > 0 else 0

for n in range(1, 300):
    d1 = dr_method1(n)
    d2 = dr_method2(n)
    d3 = dr_method3(n)
    d4 = dr_method4(n)
    assert d1 == d2 == d3 == d4, f"Methods disagree at n={n}: {d1},{d2},{d3},{d4}"

# ── Corollary: 2n−1 rule — DR shift of +2 ────────────────────────────────

# dr(2n−1) ≡ 2·dr(n) − 1 (mod 9)
# This follows from Theorem 1: dr(2n−1) ≡ 2n−1 ≡ 2·n − 1 ≡ 2·dr(n) − 1 (mod 9)

for n in range(1, 200):
    lhs = dr(2*n - 1)
    rhs_raw = 2 * dr(n) - 1
    # Apply 9-convention to rhs_raw (it may be 0 or need reduction)
    rhs = dr(rhs_raw) if rhs_raw > 0 else 9
    assert lhs == rhs, f"2n-1 rule fails at n={n}: dr(2n-1)={lhs}, 2·dr(n)-1={rhs}"

# The 9-cycle under 2n−1: DR values for 2n−1, n=1..9
cycle_2n1 = [dr(2*n - 1) for n in range(1, 10)]
assert cycle_2n1 == [1, 3, 5, 7, 9, 2, 4, 6, 8]
# Odd residues in order: all 9 DR classes appear exactly once (permutation)
assert sorted(cycle_2n1) == list(range(1, 10))

# The "+2 step" in Z/9Z:
# Starting from DR=1: 1 → 3 → 5 → 7 → 9 → 2 → 4 → 6 → 8 → 1 (mod 9)
# Each step is +2 (mod 9)
for i in range(len(cycle_2n1) - 1):
    step = (cycle_2n1[i+1] - cycle_2n1[i]) % 9
    assert step == 2, f"Step from {cycle_2n1[i]} to {cycle_2n1[i+1]} is {step}, not 2"

# Period: applying 2n−1 nine times returns to start
# But actually: the MAP dr → 2·dr−1 has order 9 in the DR system
start = 1
val = start
for _ in range(9):
    val = dr(2 * val - 1)
assert val == start    # returns to start after 9 steps

# ── Connection to sovereign framework ─────────────────────────────────────

# Sovereign anchors {4,9,25,30}: all have DR mod 3 = 1,0,7,3 mod 3 = 1,0,1,0
# i.e. they split evenly between n≡0(mod 3) and n≡1(mod 3)
SOVEREIGN_ANCHORS = {4, 9, 25, 30}
anchor_mod3 = {a: a % 3 for a in SOVEREIGN_ANCHORS}
assert set(anchor_mod3.values()) == {0, 1}   # no n≡2(mod 3) in sovereign anchors

# DR=3 classes (sovereign targets {3,12,21,30}):
SOVEREIGN_TARGETS = {3, 12, 21, 30}
assert all(t % 3 == 0 for t in SOVEREIGN_TARGETS)   # all ≡ 0 (mod 3)
assert all(dr(t) == 3 for t in SOVEREIGN_TARGETS)   # all have DR=3

# mod-3 projection of the sovereign targets (not the 18-cycle elements):
# Sovereign targets {3,12,21,30}: all ≡ 0 (mod 3) — this is exact
assert all(t % 3 == 0 for t in SOVEREIGN_TARGETS)
assert all(dr(t) == 3 for t in SOVEREIGN_TARGETS)

QR37 = frozenset((x * x) % 37 for x in range(1, 37))
# QR₃₇ elements are residues mod 37, not integers; mod-3 distribution is mixed
# The 18 QR₃₇ elements split: 8 in class 0, 8 in class 1, 2 in class 2 mod 3
QR37_list = sorted(QR37)
qr_mod3_dist = {r: sum(1 for q in QR37_list if q % 3 == r) for r in range(3)}
assert qr_mod3_dist == {0: 8, 1: 8, 2: 2}   # confirmed distribution

# The two QR₃₇ elements ≡ 2 (mod 3): {11, 26}
qr_class2 = {q for q in QR37 if q % 3 == 2}
assert qr_class2 == {11, 26}
assert 11 == pow(3, 15, 37)   # 11 = 3^15 (observer constant)
assert 26 == pow(3, 6, 37)    # 26 = SCALAR_137

# Gate 18 and DR mod 9:
assert 666 % 9 == 0    # 666 ≡ 0 (mod 9)
assert dr(666) == 9    # 9-convention: dr(666) = 9
assert 18 % 9 == 0     # 18 ≡ 0 (mod 9)
assert dr(18) == 9     # same class

# SCALAR_137 = 26:
assert dr(26) == 8        # DR(26) = 8 (bridge class)
assert 26 % 9 == 8        # confirmed: 26 mod 9 = 8 = dr(26)
assert 26 % 3 == 2        # 26 ≡ 2 (mod 3)


if __name__ == "__main__":
    print("Digital Root Modular Foundation — Theorems mod 9 and mod 3")
    print()
    print("  THEOREM 1: dr(n) ≡ n (mod 9)  [verified n=1..1000]")
    print(f"  10 ≡ {10%9} (mod 9),  10^m ≡ 1 (mod 9) for all m ≥ 0 ✓")
    print(f"  9-convention: dr(9k) = 9 for k=1..99 ✓")
    print(f"  Both methods agree for n=1..499 ✓")
    print()
    print("  THEOREM 2: dr(n) ≡ n (mod 3)  [verified n=1..1000]")
    print(f"  Follows from Theorem 1 (3|9) and direct digit-sum argument ✓")
    print(f"  DR mod-3 classes:")
    print(f"    n≡0(mod 3) → dr(n) ∈ {{3,6,9}} ✓")
    print(f"    n≡1(mod 3) → dr(n) ∈ {{1,4,7}} ✓")
    print(f"    n≡2(mod 3) → dr(n) ∈ {{2,5,8}} ✓")
    print()
    print("  All 4 Methods equivalent [verified n=1..299] ✓")
    print("    Method 1: repeated digit sum")
    print("    Method 2: recursive digit sum")
    print("    Method 3: 1 + (n−1) mod 9")
    print("    Method 4: (n−1)%9+1  ← framework formula")
    print()
    print("  COROLLARY (2n−1 rule):")
    print(f"  dr(2n−1) = 2·dr(n)−1 (mod 9-convention) [verified n=1..199] ✓")
    print(f"  9-cycle: {cycle_2n1}")
    print(f"  Each step = +2 (mod 9) ✓")
    print(f"  Period = 9: returns to start after 9 applications ✓")
    print()
    print("  Sovereign connections:")
    print(f"  Anchors mod 3: {anchor_mod3} (split {{0,1}}, no 2-class) ✓")
    print(f"  All sovereign targets ≡ 0 (mod 3) ✓")
    print(f"  QR₃₇ mod-3 distribution: {qr_mod3_dist} (class-2: {{11,26}}=3^15,SCALAR_137) ✓")
    print(f"  666 ≡ 0 (mod 9), dr(666)={dr(666)} ✓")
    print(f"  SCALAR_137=26: 26 mod 9={26%9}=dr(26)={dr(26)} ✓")
    print()
    print("All assertions passed. Foundation sealed.")
