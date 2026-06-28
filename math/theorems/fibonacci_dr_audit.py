"""
fibonacci_dr_audit.py

Fibonacci digital-root period and the Scale-2 orbit under step 4 mod 37.

─────────────────────────────────────────────────────────────────
FIBONACCI DR PERIOD:

  The Pisano period π(9) = 24: F(n + 24) ≡ F(n) mod 9 for all n ≥ 0.

  DR sequence is NOT strictly periodic at n = 0:
    DR(F(0))  = DR(0) = 0    (repo convention: dr(0) = 0)
    DR(F(24)) = DR(46368) = 9  (46368 > 0; 4+6+3+6+8 = 27, DR = 9)

  For n ≥ 1: F(n) > 0 always, so DR(F(n+24)) = DR(F(n)) exactly.
  The check `fib_dr[:24] == fib_dr[24:48]` is False for exactly one
  position (index 0, value 0 vs 9). This is correct given dr(0) = 0.

  The 24-term Fibonacci DR cycle (n = 0..23):
    [0, 1, 1, 2, 3, 5, 8, 4, 3, 7, 1, 8, 9, 8, 8, 7, 6, 4, 1, 5, 6, 2, 8, 1]

  DR distribution within the cycle:
    DR = 0: position [0]                       — 1 occurrence (F(0)=0 only)
    DR = 1: positions [1, 2, 10, 18, 23]       — 5 occurrences
    DR = 2: positions [3, 21]                  — 2 occurrences
    DR = 3: positions [4, 8]                   — 2 occurrences
    DR = 4: positions [7, 17]                  — 2 occurrences
    DR = 5: positions [5, 19]                  — 2 occurrences
    DR = 6: positions [16, 20]                 — 2 occurrences (6 arrives latest)
    DR = 7: positions [9, 15]                  — 2 occurrences
    DR = 8: positions [6, 11, 13, 14, 22]      — 5 occurrences
    DR = 9: position [12]                      — 1 occurrence (F(12)=144)

  1 and 8 each appear 5 times (1+8=9; null-pair).
  0 and 9 each appear once (boundary pair).
  All others appear exactly twice.

─────────────────────────────────────────────────────────────────
SCALE-2 ORBIT: a₀ = 133, step = 4.

  133 = 7 × 19.  DR(133) = 7.  133 mod 37 = 22.

  The orbit {133 + 4k : k ≥ 0} has two independent periods:

  DR period = 9.
    (133 + 4k) mod 9 = (7 + 4k) mod 9.
    gcd(4, 9) = 1 → step 4 generates all of ℤ/9ℤ additively.
    DR orbit over k = 0..8: [7, 2, 6, 1, 5, 9, 4, 8, 3] — permutation of 1..9.
    Every nonzero DR value appears exactly once per 9 steps.

  mod 37 period = 37.
    gcd(4, 37) = 1, 37 prime → orbit traverses all of ℤ/37ℤ in 37 steps.

  Joint period = lcm(9, 37) = 333.   (gcd(9, 37) = 1)
    DR(333) = 9 = NULL.   333 = 9 × 37.

─────────────────────────────────────────────────────────────────
FIB_POS MAPPING (first occurrence of each DR in the 24-cycle):

  k orbit step → DR value → first Fibonacci position carrying that DR.

  k=0: DR=7 → F( 9) = 34        fib_pos = 9
  k=1: DR=2 → F( 3) = 2         fib_pos = 3
  k=2: DR=6 → F(16) = 987       fib_pos = 16   ← 6 arrives latest
  k=3: DR=1 → F( 1) = 1         fib_pos = 1
  k=4: DR=5 → F( 5) = 5         fib_pos = 5
  k=5: DR=9 → F(12) = 144       fib_pos = 12
  k=6: DR=4 → F( 7) = 13        fib_pos = 7
  k=7: DR=8 → F( 6) = 8         fib_pos = 6
  k=8: DR=3 → F( 4) = 3         fib_pos = 4

  Sorted fib_pos: [1, 3, 4, 5, 6, 7, 9, 12, 16]
  These are exactly the first-occurrence positions for DR = 1..9 in the
  24-cycle (position 0 carries DR = 0, absent from the orbit).

─────────────────────────────────────────────────────────────────
"""

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = abs(n) % 9
    return r if r else 9


# ── Fibonacci DR sequence ─────────────────────────────────────────────────────

fibs = []
a, b = 0, 1
for _ in range(49):
    fibs.append(a)
    a, b = b, a + b

FIB_DR = [dr(f) for f in fibs]

EXPECTED_CYCLE = [0, 1, 1, 2, 3, 5, 8, 4, 3, 7, 1, 8, 9, 8, 8, 7, 6, 4, 1, 5, 6, 2, 8, 1]
check(FIB_DR[:24] == EXPECTED_CYCLE,
      "Fibonacci DR cycle (n=0..23)", FIB_DR[:24], EXPECTED_CYCLE)


# ── Pisano period π(9) = 24 ───────────────────────────────────────────────────

# F(n + 24) ≡ F(n) mod 9 for all n ≥ 0
for n in range(25):
    check(fibs[n + 24] % 9 == fibs[n] % 9,
          f"F({n+24}) ≡ F({n}) mod 9 (Pisano period 24)", fibs[n + 24] % 9, fibs[n] % 9)

# Programmatic period detection: first k ≥ 1 with F(k)≡0 and F(k+1)≡1 mod 9
pisano_9 = next(k for k in range(1, 100) if fibs[k] % 9 == 0 and fibs[k + 1] % 9 == 1)
check(pisano_9 == 24, "π(9) = 24", pisano_9, 24)


# ── Why `fib_dr[:24] == fib_dr[24:48]` is False ──────────────────────────────

F24 = fibs[24]
check(F24 == 46368, "F(24) = 46368", F24, 46368)
check(F24 % 9 == 0, "F(24) ≡ 0 mod 9", F24 % 9, 0)
check(F24 > 0, "F(24) > 0", F24 > 0, True)
check(dr(F24) == 9, "DR(F(24)) = 9 (positive multiple of 9)", dr(F24), 9)
check(dr(fibs[0]) == 0, "DR(F(0)) = DR(0) = 0 (repo convention)", dr(fibs[0]), 0)

# Exactly one index where the two windows differ
diff_indices = [i for i in range(24) if FIB_DR[i] != FIB_DR[i + 24]]
check(diff_indices == [0],
      "Only index 0 differs between cycle windows", diff_indices, [0])
check(FIB_DR[0] == 0 and FIB_DR[24] == 9,
      "FIB_DR[0]=0 vs FIB_DR[24]=9", (FIB_DR[0], FIB_DR[24]), (0, 9))

# For n ≥ 1: period holds exactly
for n in range(1, 24):
    check(FIB_DR[n] == FIB_DR[n + 24],
          f"n={n}: DR(F(n+24)) = DR(F(n)) for n≥1", FIB_DR[n], FIB_DR[n + 24])


# ── DR distribution within the 24-term cycle ─────────────────────────────────

EXPECTED_DIST = {
    0: [0],
    1: [1, 2, 10, 18, 23],
    2: [3, 21],
    3: [4, 8],
    4: [7, 17],
    5: [5, 19],
    6: [16, 20],
    7: [9, 15],
    8: [6, 11, 13, 14, 22],
    9: [12],
}

for val, expected_positions in EXPECTED_DIST.items():
    actual_positions = [i for i, d in enumerate(EXPECTED_CYCLE) if d == val]
    check(actual_positions == expected_positions,
          f"DR={val} positions in cycle", actual_positions, expected_positions)

# 1 and 8 appear 5 times each (null-pair: 1+8=9)
check(len(EXPECTED_DIST[1]) == 5, "DR=1 appears 5 times", len(EXPECTED_DIST[1]), 5)
check(len(EXPECTED_DIST[8]) == 5, "DR=8 appears 5 times", len(EXPECTED_DIST[8]), 5)
# 0 and 9 appear once each (boundary pair)
check(len(EXPECTED_DIST[0]) == 1, "DR=0 appears once (only F(0)=0)", len(EXPECTED_DIST[0]), 1)
check(len(EXPECTED_DIST[9]) == 1, "DR=9 appears once (only F(12)=144)", len(EXPECTED_DIST[9]), 1)
# All mid-values appear twice
for v in range(2, 8):
    check(len(EXPECTED_DIST[v]) == 2, f"DR={v} appears twice", len(EXPECTED_DIST[v]), 2)
# Total = 24
total = sum(len(v) for v in EXPECTED_DIST.values())
check(total == 24, "Total positions = 24", total, 24)

# DR=6 arrives latest: first occurrence at position 16 (last of all DR=1..9)
first_occurrences = {v: EXPECTED_DIST[v][0] for v in range(1, 10)}
check(first_occurrences[6] == max(first_occurrences.values()),
      "DR=6 has the latest first-occurrence (pos 16)", first_occurrences[6], 16)


# ── Scale-2 orbit: a₀ = 133, step = 4 ───────────────────────────────────────

A0 = 133
STEP = 4

check(A0 == 7 * 19, "133 = 7 × 19", A0, 7 * 19)
check(dr(A0) == 7, "DR(133) = 7", dr(A0), 7)
check(A0 % 37 == 22, "133 mod 37 = 22", A0 % 37, 22)

# DR orbit over k=0..8 (one full DR period)
ORBIT_DR = [dr(A0 + STEP * k) for k in range(9)]
EXPECTED_ORBIT_DR = [7, 2, 6, 1, 5, 9, 4, 8, 3]
check(ORBIT_DR == EXPECTED_ORBIT_DR,
      "DR orbit k=0..8", ORBIT_DR, EXPECTED_ORBIT_DR)
check(sorted(ORBIT_DR) == list(range(1, 10)),
      "DR orbit is permutation of 1..9", sorted(ORBIT_DR), list(range(1, 10)))


# ── DR period = 9 ────────────────────────────────────────────────────────────

# gcd(4, 9) = 1 → step 4 generates all of ℤ/9ℤ additively → period = 9
from math import gcd
check(gcd(STEP, 9) == 1, "gcd(4,9)=1 → 4 generates ℤ/9ℤ additively", gcd(STEP, 9), 1)
check(gcd(STEP, 37) == 1, "gcd(4,37)=1 → orbit spans all of ℤ/37ℤ", gcd(STEP, 37), 1)

# Verify period 9 directly
for k in range(9):
    check(dr(A0 + STEP * k) == dr(A0 + STEP * (k + 9)),
          f"DR orbit period 9: k={k} matches k+9", dr(A0 + STEP * k), dr(A0 + STEP * (k + 9)))

# mod 37 period = 37
for k in range(37):
    check((A0 + STEP * k) % 37 == (A0 + STEP * (k + 37)) % 37,
          f"mod37 period 37: k={k}", (A0 + STEP * k) % 37, (A0 + STEP * (k + 37)) % 37)

# mod 37 orbit traverses all residues 0..36
mod37_orbit = [(A0 + STEP * k) % 37 for k in range(37)]
check(sorted(mod37_orbit) == list(range(37)),
      "mod37 orbit is all of ℤ/37ℤ", sorted(mod37_orbit), list(range(37)))


# ── Joint period = 333 = lcm(9, 37) ─────────────────────────────────────────

from math import lcm
JOINT_PERIOD = lcm(9, 37)
check(JOINT_PERIOD == 333, "lcm(9, 37) = 333", JOINT_PERIOD, 333)
check(333 == 9 * 37, "333 = 9 × 37", 333, 9 * 37)
check(dr(333) == 9, "DR(333) = 9 = NULL", dr(333), 9)

# Verify joint period
check((A0 + STEP * JOINT_PERIOD) % 37 == A0 % 37,
      "mod37 returns after 333 steps", (A0 + STEP * JOINT_PERIOD) % 37, A0 % 37)
check(dr(A0 + STEP * JOINT_PERIOD) == dr(A0),
      "DR returns after 333 steps", dr(A0 + STEP * JOINT_PERIOD), dr(A0))


# ── fib_pos mapping ───────────────────────────────────────────────────────────

# fib_pos(d) = first index i in the 24-cycle where FIB_DR[i] = d
def fib_pos(d):
    return next(i for i, v in enumerate(FIB_DR[:24]) if v == d)

EXPECTED_FIB_POS = [
    (0, 7,  9),
    (1, 2,  3),
    (2, 6, 16),
    (3, 1,  1),
    (4, 5,  5),
    (5, 9, 12),
    (6, 4,  7),
    (7, 8,  6),
    (8, 3,  4),
]

for k, expected_dr, expected_pos in EXPECTED_FIB_POS:
    val = A0 + STEP * k
    d = dr(val)
    pos = fib_pos(d)
    check(d == expected_dr, f"k={k}: DR({val}) = {expected_dr}", d, expected_dr)
    check(pos == expected_pos, f"k={k}: fib_pos(DR={d}) = {expected_pos}", pos, expected_pos)

# Sorted fib_pos values = first-occurrence positions for DR=1..9
sorted_fps = sorted(fib_pos(d) for d in range(1, 10))
check(sorted_fps == [1, 3, 4, 5, 6, 7, 9, 12, 16],
      "sorted fib_pos = first-occurrence positions for DR=1..9",
      sorted_fps, [1, 3, 4, 5, 6, 7, 9, 12, 16])

# DR=6 maps to fib_pos=16 (latest of all)
check(fib_pos(6) == 16, "DR=6 → fib_pos=16 (latest first occurrence)", fib_pos(6), 16)

# Position 0 (DR=0) is excluded: no k in 0..8 gives DR=0
check(0 not in ORBIT_DR, "DR=0 absent from orbit (A0+4k never ≡ 0 mod 9)", 0 not in ORBIT_DR, True)
check(dr(A0) % 9 == 7, "133 mod 9 = 7 → DR=0 never reached by step 4", dr(A0) % 9, 7)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Fibonacci DR Period and Scale-2 Orbit Audit")
    print("=" * 66)

    print(f"\n── Fibonacci DR cycle (n=0..23) ──")
    print(f"  {EXPECTED_CYCLE}")
    print(f"  Length: 24  (Pisano period π(9) = {pisano_9})")
    print(f"  F(24) = {F24}; DR(F(24)) = 9 ≠ DR(F(0)) = 0")
    print(f"  `fib_dr[:24] == fib_dr[24:48]` → False (n=0 boundary only)")
    print(f"  For n ≥ 1: DR(F(n+24)) = DR(F(n)) exactly.")

    print(f"\n── DR distribution within the 24-cycle ──")
    for val, positions in EXPECTED_DIST.items():
        marker = " ← 5×" if len(positions) == 5 else (" ← 1×" if len(positions) == 1 else "")
        print(f"  DR={val}: positions={positions}{marker}")
    print(f"  DR=1 and DR=8 each appear 5× (1+8=9, null-pair).")
    print(f"  DR=0 and DR=9 each appear 1× (boundary pair).")
    print(f"  DR=6 first appears at position 16 — last of all DR=1..9.")

    print(f"\n── Scale-2 orbit: a₀=133, step=4, over k=0..8 (one DR period) ──")
    print(f"  {'k':>2}  {'val':>5}  mod37  mod9  DR  fib_pos")
    for k, expected_dr, expected_pos in EXPECTED_FIB_POS:
        val = A0 + STEP * k
        print(f"  {k:>2}  {val:>5}   {val%37:>3}    {val%9}   {expected_dr}    {expected_pos}")
    print(f"  DR orbit: {EXPECTED_ORBIT_DR} — permutation of 1..9")

    print(f"\n── Periods ──")
    print(f"  DR period   = 9   (gcd(4,9)=1; 4 generates ℤ/9ℤ additively)")
    print(f"  mod37 period = 37  (gcd(4,37)=1; 37 prime; full traversal)")
    print(f"  Joint period = lcm(9,37) = 333 = 9×37; DR(333) = 9 = NULL")

    print(f"\n── fib_pos: DR values mapped to first Fibonacci position ──")
    print(f"  Sorted positions: {sorted_fps}")
    print(f"  These are the 9 first-occurrence indices for DR=1..9 in the 24-cycle.")
    print(f"  DR=6 → position 16 (latest); DR=9 → position 12; DR=0 not in orbit.")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
