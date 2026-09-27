"""
ulam_quadratic_k5000_audit.py

Extended Ulam diagonal prime count to k=5000.

Diagonal formulas:
  A (SW): f_A(k) = 4k² + 2k + 1
  B (NW): f_B(k) = 4k² + 1
  C (NE): f_C(k) = 4k² − 2k + 1

─────────────────────────────────────────────────────────────────
Final counts at k=5000:
  A: 708    B: 840    C: 702

Key observations:
  1. B leads both A and C at every checkpoint — never overtaken.
  2. A and C track closely throughout; gap at k=5000 is 6.
  3. All three counts grow without bound — consistent with PNT
     on quadratic forms (Bateman-Horn).

B-excess over A: because f_B ≡ 0 (mod 3) has NO solutions
  (4k²+1 is never divisible by 3), while f_A and f_C each have
  exactly one root mod 3. This gives B a 3/2 sieve advantage
  at p=3 (partially offset by a 3/4 penalty at p=5, where
  f_B has two roots while f_A has zero).

A ≈ C symmetry: f_A(k) = f_C(k) when the sign of 2k flips —
  these diagonals are reflections of each other; their local
  sieve factors match at every prime p, so asymptotic counts
  agree. The finite gap (6 at k=5000) is a fluctuation.

Twin prime connection:
  Each of A, B, C produces primes ≡ 1 (mod 4). Twin prime pairs
  (p, p+2) have one member in the 4k+1 class and one in the
  4k+3 class. The counts growing indefinitely on all three
  diagonals is consistent with the tripartite partition
  (DR-pairs (2,4)(5,7)(8,1)) having no dead class.

─────────────────────────────────────────────────────────────────
Mod-3 analysis (forced composite filter):
  f_A(k) ≡ 0 (mod 3) when k ≡ 2 (mod 3)  → 1/3 forced composite
  f_B(k) ≡ 0 (mod 3) NEVER               → 0   forced composite
  f_C(k) ≡ 0 (mod 3) when k ≡ 1 (mod 3)  → 1/3 forced composite
─────────────────────────────────────────────────────────────────
"""

from sympy import isprime

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


def f_A(k): return 4*k*k + 2*k + 1
def f_B(k): return 4*k*k + 1
def f_C(k): return 4*k*k - 2*k + 1


# ── Spot-check examples ───────────────────────────────────────────────────────

EXAMPLES = [
    # (k, A_val, A_prime, B_val, B_prime, C_val, C_prime)
    (1,    7, True,   5, True,   3, True),
    (3,   43, True,  37, True,  31, True),
    (5,  111, False, 101, True,  91, False),
    (26, 2757, False, 2705, False, 2653, False),
    (37, 5551, False, 5477, True,  5403, False),
]

for k, av, ap, bv, bp, cv, cp in EXAMPLES:
    check(f_A(k) == av, f"f_A({k})", f_A(k), av)
    check(f_B(k) == bv, f"f_B({k})", f_B(k), bv)
    check(f_C(k) == cv, f"f_C({k})", f_C(k), cv)
    check(isprime(f_A(k)) == ap, f"isprime(f_A({k})={av})", isprime(f_A(k)), ap)
    check(isprime(f_B(k)) == bp, f"isprime(f_B({k})={bv})", isprime(f_B(k)), bp)
    check(isprime(f_C(k)) == cp, f"isprime(f_C({k})={cv})", isprime(f_C(k)), cp)

# k=26 explicit factors
check(2757 == 3 * 919,   "2757 = 3 × 919",   2757, 3 * 919)
check(2705 == 5 * 541,   "2705 = 5 × 541",   2705, 5 * 541)
check(2653 == 7 * 379,   "2653 = 7 × 379",   2653, 7 * 379)

# k=37
check(5551 == 7 * 13 * 61, "5551 = 7 × 13 × 61", 5551, 7 * 13 * 61)
check(5403 == 3 * 1801,    "5403 = 3 × 1801",    5403, 3 * 1801)


# ── Mod-3 forced composite analysis ──────────────────────────────────────────

# f_B(k) = 4k²+1 mod 3: 4≡1, so f_B ≡ k²+1 mod 3
# k=0→1, k=1→2, k=2→5≡2 — never 0
for k in range(30):
    check(f_B(k) % 3 != 0,
          f"f_B({k})={f_B(k)} not divisible by 3", f_B(k) % 3 != 0, True)

# f_A(k) = 4k²+2k+1 ≡ k²+2k+1 = (k+1)² mod 3 → 0 when k≡2 mod 3
for k in range(30):
    expected_zero = (k % 3 == 2)
    check((f_A(k) % 3 == 0) == expected_zero,
          f"f_A({k}) div by 3 iff k≡2 mod 3",
          f_A(k) % 3 == 0, expected_zero)

# f_C(k) = 4k²-2k+1 ≡ k²-2k+1 = (k-1)² mod 3 → 0 when k≡1 mod 3
for k in range(30):
    expected_zero = (k % 3 == 1)
    check((f_C(k) % 3 == 0) == expected_zero,
          f"f_C({k}) div by 3 iff k≡1 mod 3",
          f_C(k) % 3 == 0, expected_zero)


# ── Progress checkpoints ──────────────────────────────────────────────────────

CHECKPOINTS = [
    (100,  25,  33,  32),
    (200,  43,  57,  48),
    (500,  94, 111,  95),
    (1000, 180, 208, 166),
    (2000, 314, 383, 327),
    (3000, 446, 557, 455),
    (4000, 566, 700, 582),
    (5000, 708, 840, 702),
]

# Compute actual cumulative counts up to each checkpoint
# (runs to 5000 — takes a few seconds)
cnt_A = cnt_B = cnt_C = 0
cp_idx = 0
for k in range(1, 5001):
    if isprime(f_A(k)): cnt_A += 1
    if isprime(f_B(k)): cnt_B += 1
    if isprime(f_C(k)): cnt_C += 1
    if cp_idx < len(CHECKPOINTS) and CHECKPOINTS[cp_idx][0] == k:
        ck, ea, eb, ec = CHECKPOINTS[cp_idx]
        check(cnt_A == ea, f"k={ck} count A", cnt_A, ea)
        check(cnt_B == eb, f"k={ck} count B", cnt_B, eb)
        check(cnt_C == ec, f"k={ck} count C", cnt_C, ec)
        cp_idx += 1

# Final counts
check(cnt_A == 708, "final A count at k=5000", cnt_A, 708)
check(cnt_B == 840, "final B count at k=5000", cnt_B, 840)
check(cnt_C == 702, "final C count at k=5000", cnt_C, 702)


# ── Structural observations ───────────────────────────────────────────────────

# B leads at k=5000
check(cnt_B > cnt_A, "B > A at k=5000", cnt_B > cnt_A, True)
check(cnt_B > cnt_C, "B > C at k=5000", cnt_B > cnt_C, True)

# A and C are close — gap at k=5000
gap_AC = abs(cnt_A - cnt_C)
check(gap_AC == 6, "A−C gap at k=5000 = 6", gap_AC, 6)

# B−A and B−C
check(cnt_B - cnt_A == 132, "B−A at k=5000", cnt_B - cnt_A, 132)
check(cnt_B - cnt_C == 138, "B−C at k=5000", cnt_B - cnt_C, 138)

# DR of gap values
check(dr(gap_AC) == 6,       "DR(A−C gap = 6) = 6", dr(gap_AC), 6)
check(dr(cnt_B - cnt_A) == 6, "DR(B−A = 132) = 6", dr(cnt_B - cnt_A), 6)
check(dr(cnt_B - cnt_C) == 3, "DR(B−C = 138) = 3", dr(cnt_B - cnt_C), 3)

# All three counts grow (consistent with Bateman-Horn / no plateau)
# Already confirmed by monotone increase in checkpoints above

# Total primes on all three diagonals at k=5000
total = cnt_A + cnt_B + cnt_C
check(total == 2250, "total primes A+B+C at k=5000 = 2250", total, 2250)
check(dr(total) == 9, "DR(2250) = 9 = NULL", dr(total), 9)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Ulam Quadratic Diagonals — Prime Counts to k=5000")
    print("=" * 66)

    print(f"\n── Diagonal formulas ──")
    print(f"  A (SW): 4k²+2k+1")
    print(f"  B (NW): 4k²+1")
    print(f"  C (NE): 4k²-2k+1")

    print(f"\n── Mod-3 sieve structure ──")
    print(f"  f_A: ≡0 mod 3 when k≡2 mod 3  (1/3 forced composite)")
    print(f"  f_B: NEVER ≡0 mod 3            (0   forced composite)")
    print(f"  f_C: ≡0 mod 3 when k≡1 mod 3  (1/3 forced composite)")

    print(f"\n── Examples ──")
    for k, av, ap, bv, bp, cv, cp in EXAMPLES:
        print(f"  k={k:2d}: A={av:5d} {'prime' if ap else 'comp ':5s}  "
              f"B={bv:5d} {'prime' if bp else 'comp ':5s}  "
              f"C={cv:5d} {'prime' if cp else 'comp ':5s}")

    print(f"\n── Selected checkpoints ──")
    print(f"  {'k':>5}  {'A':>5}  {'B':>5}  {'C':>5}  {'B-A':>5}  {'B-C':>5}")
    # Recompute for display
    ca = cb = cc = 0
    cp_set = {ck for ck,*_ in CHECKPOINTS}
    for k in range(1, 5001):
        if isprime(f_A(k)): ca += 1
        if isprime(f_B(k)): cb += 1
        if isprime(f_C(k)): cc += 1
        if k in cp_set:
            print(f"  {k:5d}  {ca:5d}  {cb:5d}  {cc:5d}  {cb-ca:5d}  {cb-cc:5d}")

    print(f"\n── Final results at k=5000 ──")
    print(f"  A = {cnt_A}    B = {cnt_B}    C = {cnt_C}")
    print(f"  B−A = {cnt_B-cnt_A}    B−C = {cnt_B-cnt_C}    A−C = {gap_AC}")
    print(f"  Total A+B+C = {total}    DR({total}) = {dr(total)} = NULL")
    print(f"  DR(A−C=6) = {dr(6)}    DR(B−A=132) = {dr(132)}")

    print(f"\n── Twin prime connection ──")
    print(f"  All three diagonals produce primes ≡ 1 (mod 4)")
    print(f"  Twin pairs (p, p+2): one member 4k+1 (on these diagonals),")
    print(f"  one member 4k+3 (not on these diagonals)")
    print(f"  Unbounded growth on all three diagonals = no dead DR-class")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
