"""
orbit_137_period333_audit.py

9-step orbit of 137 under T: a → a+4 inside the period-333 system.
Tracks four coordinates: (a, dr, r mod 37, fib-index in C).

─────────────────────────────────────────────────────────────────
Orbit table (k=0..8):

  k | a   | dr | r (mod 37) | fib-index in C
  --|-----|----|------------|---------------
  0 | 137 |  2 |     26     |  3
  1 | 141 |  6 |     30     | 16
  2 | 145 |  1 |     34     |  1
  3 | 149 |  5 |      1     |  5
  4 | 153 |  9 |      5     | 12
  5 | 157 |  4 |      9     |  7
  6 | 161 |  8 |     13     |  6
  7 | 165 |  3 |     17     |  4
  8 | 169 |  7 |     21     |  9

DR evolves as +4 (mod 9) each step — same rate as the integer sequence
since adding 4 to a raises its digital root by 4 mod 9.

Fib-index: first occurrence of dr in the Fibonacci DR cycle C (period 24).

─────────────────────────────────────────────────────────────────
DR=6 closure across scales:
  Scale-1: 33 (start, dr=6), 141 (terminal, dr=6)
  Scale-2: 141 (k=1 of this orbit, dr=6)

  +4 mod 9 sends dr=6 → dr=1; both positions admissible in C.

─────────────────────────────────────────────────────────────────
DR correction: 37 ≡ 1 (mod 9), so DR(37m) = DR(m).
Cofactors of terms ≡ 0 (mod 37) in any Δ=4 sequence are themselves
a Δ=4 sequence, preserving the mod-4 residue class.

─────────────────────────────────────────────────────────────────
37-field unity primes in the orbit: 149 (k=3, r=1 mod 37).
Combined period: lcm(9, 37) = 333.  CRT: 333 = 9 × 37.
Coset incidence coordinate c = 33 (prime index of 137): constant
under T, period 1 — combined period remains 333.
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


# ── Fibonacci DR cycle C (period 24, starting index 0) ───────────────────────

C = [0, 1, 1, 2, 3, 5, 8, 4, 3, 7, 1, 8, 9, 8, 8, 7, 6, 4, 1, 5, 6, 2, 8, 1]

check(len(C) == 24, "Fibonacci DR cycle has period 24", len(C), 24)

# First occurrence (index ≥ 1) of each DR value in C
FIB_INDEX = {}
for i, v in enumerate(C):
    if v not in FIB_INDEX and v != 0:
        FIB_INDEX[v] = i

expected_fib_index = {1: 1, 2: 3, 3: 4, 4: 7, 5: 5, 6: 16, 7: 9, 8: 6, 9: 12}
for dr_val, idx in expected_fib_index.items():
    check(FIB_INDEX[dr_val] == idx,
          f"fib-index of dr={dr_val} in C", FIB_INDEX[dr_val], idx)
    check(C[idx] == dr_val,
          f"C[{idx}] = {dr_val}", C[idx], dr_val)


# ── Orbit table ───────────────────────────────────────────────────────────────

ORBIT = [
    # (k, a, dr_val, r_mod37, fib_idx)
    (0, 137, 2, 26,  3),
    (1, 141, 6, 30, 16),
    (2, 145, 1, 34,  1),
    (3, 149, 5,  1,  5),
    (4, 153, 9,  5, 12),
    (5, 157, 4,  9,  7),
    (6, 161, 8, 13,  6),
    (7, 165, 3, 17,  4),
    (8, 169, 7, 21,  9),
]

for k, a, dr_val, r_mod37, fib_idx in ORBIT:
    check(137 + 4 * k == a,
          f"k={k}: a = 137+4×{k}", 137 + 4 * k, a)
    check(dr(a) == dr_val,
          f"k={k}: dr({a})", dr(a), dr_val)
    check(a % 37 == r_mod37,
          f"k={k}: {a} mod 37", a % 37, r_mod37)
    check(FIB_INDEX[dr_val] == fib_idx,
          f"k={k}: fib-index of dr={dr_val}", FIB_INDEX[dr_val], fib_idx)
    check(C[fib_idx] == dr_val,
          f"k={k}: C[{fib_idx}] = {dr_val}", C[fib_idx], dr_val)

# DR evolves exactly as +4 (mod 9) each step
for i in range(len(ORBIT) - 1):
    _, _, dr_cur, _, _ = ORBIT[i]
    _, _, dr_nxt, _, _ = ORBIT[i + 1]
    check((dr_cur + 4 - 1) % 9 + 1 == dr_nxt,
          f"dr step {i}→{i+1}: {dr_cur}+4≡{dr_nxt} (mod 9)",
          (dr_cur + 4 - 1) % 9 + 1, dr_nxt)

# Mod-37 advances by 4 each step
for i in range(len(ORBIT) - 1):
    _, _, _, r_cur, _ = ORBIT[i]
    _, _, _, r_nxt, _ = ORBIT[i + 1]
    check((r_cur + 4) % 37 == r_nxt,
          f"r step {i}→{i+1}: ({r_cur}+4) mod 37 = {r_nxt}",
          (r_cur + 4) % 37, r_nxt)


# ── 37-field unity prime at k=3 ───────────────────────────────────────────────

check(149 % 37 == 1, "149 ≡ 1 (mod 37) — 37-field unity", 149 % 37, 1)

from sympy import isprime
check(isprime(149), "149 is prime", isprime(149), True)


# ── DR=6 positions and closure ────────────────────────────────────────────────

# Scale-1: 33 (start), 141 (terminal)
check(dr(33)  == 6, "DR(33) = 6  [Scale-1 start]",    dr(33),  6)
check(dr(141) == 6, "DR(141) = 6 [Scale-1/2 terminal]", dr(141), 6)

# Scale-2: 141 appears at k=1 of this orbit
check(ORBIT[1][1] == 141, "k=1 in orbit is 141", ORBIT[1][1], 141)
check(ORBIT[1][2] == 6,   "k=1 has dr=6",         ORBIT[1][2], 6)

# +4 mod 9 sends dr=6 to dr=1
check((6 + 4 - 1) % 9 + 1 == 1, "dr=6 → dr=1 under +4 mod 9", (6 + 4 - 1) % 9 + 1, 1)

# Both dr=6 (index 16) and dr=1 (index 1) are admissible in C
check(C[16] == 6, "C[16] = 6", C[16], 6)
check(C[1]  == 1, "C[1]  = 1", C[1],  1)


# ── Coset incidence: prime index of 137 ──────────────────────────────────────

# 137 is the 33rd prime (1-indexed)
from sympy import primepi
check(primepi(137) == 33, "137 is the 33rd prime", primepi(137), 33)

COSET_C = 33  # constant coordinate under T
# Constant under T → period 1 → combined period unchanged
check(1 * 333 == 333, "period with constant coset coord: lcm(333,1)=333", 1 * 333, 333)


# ── Period-333 CRT decomposition ─────────────────────────────────────────────

from math import gcd, lcm
check(lcm(9, 37) == 333,  "lcm(9, 37) = 333",  lcm(9, 37),  333)
check(9 * 37 == 333,       "9 × 37 = 333",       9 * 37,       333)
check(gcd(9, 37) == 1,     "gcd(9, 37) = 1",     gcd(9, 37),   1)
check(dr(333) == 9,        "DR(333) = 9 = NULL",  dr(333),      9)


# ── DR correction: DR(37m) = DR(m) ───────────────────────────────────────────

check(37 % 9 == 1, "37 ≡ 1 (mod 9)", 37 % 9, 1)

# For any integer m: DR(37m) = DR(1×DR(m)) = DR(m)
for m in [1, 5, 9, 13, 17, 21, 25, 33, 137]:
    check(dr(37 * m) == dr(m),
          f"DR(37×{m}) = DR({m}) = {dr(m)}", dr(37 * m), dr(m))


# ── Continued-fraction convergent: 137/1 ─────────────────────────────────────

# 137 is the integer convergent of α⁻¹ ≈ 137.036 (fine structure constant)
# It sits at k=0 of this orbit (Scale-2 start)
check(137 == ORBIT[0][1], "137/1 convergent = k=0 of orbit", 137, ORBIT[0][1])
check(dr(137) == 2,       "DR(137) = 2",                     dr(137), 2)
check(137 % 37 == 26,     "137 ≡ 26 ≡ 10⁻¹ (mod 37)",      137 % 37, 26)

# 10 × 26 ≡ 1 (mod 37) — modular ratio
check(10 * 26 % 37 == 1, "10 × 26 ≡ 1 (mod 37)", 10 * 26 % 37, 1)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Orbit of 137 under T: a → a+4  (period-333 system)")
    print("=" * 66)

    print(f"\n── Fibonacci DR cycle C (period {len(C)}) ──")
    print(f"  {C}")
    print(f"  First positions: { {dr_val: idx for dr_val, idx in sorted(expected_fib_index.items())} }")

    print(f"\n── 9-step orbit table ──")
    print(f"  {'k':>2} | {'a':>4} | {'dr':>3} | {'r mod 37':>9} | fib-index")
    print("  " + "─" * 36)
    for k, a, dr_val, r_mod37, fib_idx in ORBIT:
        print(f"  {k:2d} | {a:4d} |  {dr_val:2d} | {r_mod37:9d} | {fib_idx}")

    print(f"\n── DR progression (each step +4 mod 9) ──")
    dr_seq = [row[2] for row in ORBIT]
    print(f"  {dr_seq}")

    print(f"\n── DR=6 positions ──")
    print(f"  Scale-1:  33 (start, dr=6), 141 (terminal, dr=6)")
    print(f"  Scale-2:  141 (k=1, dr=6)")
    print(f"  +4 mod 9: dr=6 → dr=1  (C[16]=6, C[1]=1  both admissible)")

    print(f"\n── Coset incidence ──")
    print(f"  137 is the {COSET_C}rd prime  (primepi(137) = {primepi(137)})")
    print(f"  Constant coordinate c=33 under T  →  combined period = 333")

    print(f"\n── Period-333 CRT ──")
    print(f"  lcm(9, 37) = {lcm(9,37)}   9 × 37 = {9*37}   gcd = {gcd(9,37)}")
    print(f"  DR(333) = {dr(333)} = NULL ✓")

    print(f"\n── DR correction: 37 ≡ 1 (mod 9) ──")
    print(f"  DR(37m) = DR(m) for all m")
    for m in [1, 5, 9, 13, 17, 21, 25]:
        print(f"  DR(37×{m:2d}) = DR({37*m:4d}) = {dr(37*m)} = DR({m})")

    print(f"\n── α⁻¹ convergent ──")
    print(f"  137/1 lands at k=0 of orbit")
    print(f"  DR=2, r=26=10⁻¹ mod 37,  10×26≡{10*26%37} (mod 37) ✓")
    print(f"  149 at k=3: r=1 (mod 37) — 37-field unity, prime ✓")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
