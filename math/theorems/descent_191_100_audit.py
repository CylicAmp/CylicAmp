"""
descent_191_100_audit.py

The 10-value descent sequence from 1-9-1 to 1-0-0.

Construction:
  Row: 1-k-k for k = 8, 7, 6, 5, 4, 3, 2, 1, 0  (numbers 188 to 100)
  Top: 1-9-1 → 191  (prime; 19 → 191 via DR-append Layer 1)

Numbers: 191, 188, 177, 166, 155, 144, 133, 122, 111, 100

─────────────────────────────────────────────────────────────────
FACTORIZATIONS:
  191         prime        DR = 2
  188 = 2²×47             DR = 8
  177 = 3×59              DR = 6
  166 = 2×83              DR = 4
  155 = 5×31              DR = 2
  144 = 2⁴×3²             DR = 9   (12²)
  133 = 7×19              DR = 7
  122 = 2×61              DR = 5
  111 = 3×37              DR = 3
  100 = 2²×5²             DR = 1

DR sequence: [2, 8, 6, 4, 2, 9, 7, 5, 3, 1]

CLAIMS:
  (S1) The 10 DRs cover all 9 values {1..9} (DR=2 appears twice).
  (S2) DR formula for 1-k-k: DR(100+11k) = DR(1+2k)  for k=0..8.
       (Because 100≡1 and 11≡2 mod 9.)
  (S3) 191 is the unique prime. It is also Layer-1 result of 19→191
       in the DR-append chain.
  (S4) Bottom five DRs (144→100): 9,7,5,3,1 — arithmetic step −2.
─────────────────────────────────────────────────────────────────
"""

from sympy import isprime, factorint

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = n % 9
    return r if r else 9


# ── Sequence ───────────────────────────────────────────────────────────────────

VALUES = [191, 188, 177, 166, 155, 144, 133, 122, 111, 100]
ROWS   = [(1,9,1),(1,8,8),(1,7,7),(1,6,6),(1,5,5),(1,4,4),(1,3,3),(1,2,2),(1,1,1),(1,0,0)]

check(len(VALUES) == 10, "sequence length", len(VALUES), 10)
check(VALUES[0]  == 191, "first value", VALUES[0],  191)
check(VALUES[-1] == 100, "last value",  VALUES[-1], 100)


# ── Factorizations ─────────────────────────────────────────────────────────────

EXPECTED_FACTORS = {
    191: {191: 1},
    188: {2: 2, 47: 1},
    177: {3: 1, 59: 1},
    166: {2: 1, 83: 1},
    155: {5: 1, 31: 1},
    144: {2: 4, 3: 2},
    133: {7: 1, 19: 1},
    122: {2: 1, 61: 1},
    111: {3: 1, 37: 1},
    100: {2: 2, 5: 2},
}

for n, expected_f in EXPECTED_FACTORS.items():
    actual_f = factorint(n)
    check(actual_f == expected_f, f"factors({n})", actual_f, expected_f)


# ── S1: DR sequence covers all 9 values ───────────────────────────────────────

DR_SEQ = [dr(n) for n in VALUES]
check(DR_SEQ == [2, 8, 6, 4, 2, 9, 7, 5, 3, 1], "DR sequence", DR_SEQ, [2, 8, 6, 4, 2, 9, 7, 5, 3, 1])
check(set(DR_SEQ) == set(range(1, 10)), "S1 all 9 DRs covered", set(DR_SEQ), set(range(1, 10)))
check(DR_SEQ.count(2) == 2, "DR=2 appears twice", DR_SEQ.count(2), 2)


# ── S2: DR formula for 1-k-k rows ─────────────────────────────────────────────

# 100 ≡ 1 (mod 9), 11 ≡ 2 (mod 9) → DR(100+11k) = DR(1+2k)
for k in range(9):   # k = 0..8
    n = 100 + 11 * k
    check(
        dr(n) == dr(1 + 2 * k),
        f"S2 DR(100+11×{k})=DR(1+2×{k})",
        dr(n),
        dr(1 + 2 * k),
    )


# ── S3: 191 is the unique prime; 19 → 191 via DR-append ──────────────────────

primes_in_seq = [n for n in VALUES if isprime(n)]
check(primes_in_seq == [191], "S3 unique prime", primes_in_seq, [191])

# 19 → 19*10 + DR(19) = 190 + 1 = 191
check(19 * 10 + dr(19) == 191, "S3 DR-append: 19→191", 19 * 10 + dr(19), 191)
check(dr(19) == 1, "DR(19)=1", dr(19), 1)


# ── S4: bottom five DRs are 9,7,5,3,1 (step −2) ──────────────────────────────

bottom_dr = DR_SEQ[5:]   # 144 to 100
check(bottom_dr == [9, 7, 5, 3, 1], "S4 bottom five DRs", bottom_dr, [9, 7, 5, 3, 1])
diffs = [bottom_dr[i+1] - bottom_dr[i] for i in range(4)]
check(all(d == -2 for d in diffs), "S4 step −2", diffs, [-2, -2, -2, -2])


# ── 111 = 3×37, 100 = 2²×5², 144 = 12² ──────────────────────────────────────

check(111 == 3 * 37,   "111=3×37",    111, 3 * 37)
check(100 == 4 * 25,   "100=2²×5²",   100, 4 * 25)
check(144 == 12 ** 2,  "144=12²",     144, 144)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Descent Sequence Audit: 1-9-1 → 1-0-0")
    print("=" * 62)

    print(f"\n── Sequence ──")
    for (a, b, c), n in zip(ROWS, VALUES):
        f = EXPECTED_FACTORS[n]
        parts = [f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(f.items())]
        fac = "prime" if isprime(n) else "×".join(parts)
        print(f"  {a}-{b}-{c} → {n:4d}  DR={dr(n)}  {fac}")

    print(f"\n── S1: DR coverage ──")
    print(f"  DR sequence: {DR_SEQ}")
    print(f"  DR set:      {sorted(set(DR_SEQ))}")
    print(f"  All 9 values {'{1..9}'} covered: {set(DR_SEQ) == set(range(1,10))}")
    print(f"  DR=2 appears twice (rows 191 and 155)")

    print(f"\n── S2: formula DR(100+11k) = DR(1+2k) ──")
    print(f"  100 ≡ 1 (mod 9),  11 ≡ 2 (mod 9)")
    print(f"  Verified for k = 0..8")

    print(f"\n── S3: prime ──")
    print(f"  191 = prime (only prime in sequence)")
    print(f"  19 → 191 via DR-append: 19×10+DR(19) = 190+1 = 191")

    print(f"\n── S4: bottom five DRs ──")
    print(f"  144→133→122→111→100:  DRs {bottom_dr}  (step −2)")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
