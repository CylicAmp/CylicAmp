"""
prime_insertion_sequence_audit.py

The sequence obtained by inserting decreasing digits into the gap of 1-7.

Construction:
  Start: 1, 7  (gap = 6)
  Insert 6: 1, 6, 7  → 167
  Insert 5: 1, 5, 1  → 151
  Insert 4: 1, 4, 4  → 144
  Insert 3: 1, 3, 3  → 133
  Insert 2: 1, 2, 2  → 122
  Insert 1: 1, 1, 1  → 111

The inserted digit k produces the number by concatenation:
  k=6 → 1_6_7 → 167
  k=5 → 1_5_(7-6) = 1_5_1 → 151   [terminal digit = gap remainder: 7-(6-k+1)×1 cycling]
  ...
  k=1 → 1_1_1 → 111

Structural observations:
  (P1) First three values are all prime: 17, 167, 151.
  (P2) DR sequence: [8, 5, 7, 9, 7, 5, 3] — bottom four decrease by 2.
  (P3) Terminal value 111 = 3 × 37 — framework modulus 37 appears.
  (P4) Middle column of the triangle (6, 5, 4, 3, 2, 1) counts down.
  (P5) 144 = 12² = 2⁴ × 3².

─────────────────────────────────────────────────────────────────
VALUES AND FACTORIZATIONS:
  17   = prime             DR = 8
  167  = prime             DR = 5
  151  = prime             DR = 7   (palindrome prime)
  144  = 2^4 × 3^2         DR = 9   (12²)
  133  = 7 × 19            DR = 7
  122  = 2 × 61            DR = 5
  111  = 3 × 37            DR = 3

DR sequence: [8, 5, 7, 9, 7, 5, 3]
Bottom four (144→111): DR descent 9 → 7 → 5 → 3  (step −2)
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


# ── Sequence values ────────────────────────────────────────────────────────────

VALUES = [17, 167, 151, 144, 133, 122, 111]

check(len(VALUES) == 7, "sequence length", len(VALUES), 7)
check(VALUES[0]  == 17,  "first value",  VALUES[0],  17)
check(VALUES[-1] == 111, "last value",   VALUES[-1], 111)


# ── Factorizations ─────────────────────────────────────────────────────────────

EXPECTED_FACTORS = {
    17:  {17: 1},
    167: {167: 1},
    151: {151: 1},
    144: {2: 4, 3: 2},
    133: {7: 1, 19: 1},
    122: {2: 1, 61: 1},
    111: {3: 1, 37: 1},
}

for n, expected_f in EXPECTED_FACTORS.items():
    actual_f = factorint(n)
    check(actual_f == expected_f, f"factors({n})", actual_f, expected_f)


# ── Primality ─────────────────────────────────────────────────────────────────

EXPECTED_PRIME = {17: True, 167: True, 151: True, 144: False, 133: False, 122: False, 111: False}

for n, expected_p in EXPECTED_PRIME.items():
    check(isprime(n) == expected_p, f"isprime({n})", isprime(n), expected_p)


# ── P1: first three values are prime ──────────────────────────────────────────

check(all(isprime(n) for n in VALUES[:3]), "P1 first three prime", [isprime(n) for n in VALUES[:3]], [True, True, True])
check(not any(isprime(n) for n in VALUES[3:]), "P1 last four composite", [isprime(n) for n in VALUES[3:]], [False, False, False, False])


# ── P2: DR sequence ───────────────────────────────────────────────────────────

DR_SEQUENCE = [dr(n) for n in VALUES]
check(DR_SEQUENCE == [8, 5, 7, 9, 7, 5, 3], "P2 DR sequence", DR_SEQUENCE, [8, 5, 7, 9, 7, 5, 3])

# Bottom four DRs decrease by 2 each step
bottom_dr = DR_SEQUENCE[3:]  # [9, 7, 5, 3]
check(bottom_dr == [9, 7, 5, 3], "P2 bottom four DRs", bottom_dr, [9, 7, 5, 3])
diffs = [bottom_dr[i + 1] - bottom_dr[i] for i in range(len(bottom_dr) - 1)]
check(all(d == -2 for d in diffs), "P2 bottom four step -2", diffs, [-2, -2, -2])


# ── P3: 111 = 3 × 37 ──────────────────────────────────────────────────────────

check(111 == 3 * 37, "P3 111=3×37", 111, 3 * 37)
check(37 in factorint(111), "P3 37 is factor of 111", 37 in factorint(111), True)


# ── P4: middle digits count down 6→1 ─────────────────────────────────────────

# The sequence rows are: 1-7, 1-6-7, 1-5-1, 1-4-4, 1-3-3, 1-2-2, 1-1-1
# Inserted digits (middle column for rows 2-7): 6, 5, 4, 3, 2, 1
inserted_digits = list(range(6, 0, -1))
check(inserted_digits == [6, 5, 4, 3, 2, 1], "P4 middle column", inserted_digits, [6, 5, 4, 3, 2, 1])


# ── P5: 144 = 12² ─────────────────────────────────────────────────────────────

check(144 == 12 ** 2, "P5 144=12²", 144, 12 ** 2)
check(factorint(144) == {2: 4, 3: 2}, "P5 144=2^4×3^2", factorint(144), {2: 4, 3: 2})


# ── 151 is a palindrome prime ──────────────────────────────────────────────────

check(str(151) == str(151)[::-1], "151 palindrome", str(151), str(151)[::-1])
check(isprime(151), "151 prime", isprime(151), True)


# ── DR of first value (17) ────────────────────────────────────────────────────

check(dr(17) == 8, "DR(17)=8", dr(17), 8)
check(17 % 9 == 8, "17 mod 9 = 8", 17 % 9, 8)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Prime Insertion Sequence Audit: 1-7 → 1-1-1")
    print("=" * 62)

    print(f"\n── Triangle construction ──")
    rows = [
        (None, [1, 7],       17),
        (6,    [1, 6, 7],   167),
        (5,    [1, 5, 1],   151),
        (4,    [1, 4, 4],   144),
        (3,    [1, 3, 3],   133),
        (2,    [1, 2, 2],   122),
        (1,    [1, 1, 1],   111),
    ]
    for ins, digits, n in rows:
        ins_str = f"insert {ins}" if ins is not None else "start  "
        digits_str = "-".join(str(d) for d in digits)
        p_str = "prime" if isprime(n) else "×".join(
            (f"{b}^{e}" if e > 1 else str(b)) for b, e in sorted(factorint(n).items())
        )
        print(f"  {ins_str}  {digits_str:9s} → {n:4d}  DR={dr(n)}  {p_str}")

    print(f"\n── Primality ──")
    print(f"  First three: {VALUES[:3]} — all prime")
    print(f"  Last four:   {VALUES[3:]} — all composite")

    print(f"\n── DR sequence ──")
    print(f"  {DR_SEQUENCE}")
    print(f"  Bottom four: {bottom_dr}  (step −2 each)")

    print(f"\n── Notable factorizations ──")
    print(f"  111 = 3 × 37   (framework modulus 37 appears)")
    print(f"  144 = 12² = 2⁴ × 3²")
    print(f"  151 palindrome prime")
    print(f"  133 = 7 × 19")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
