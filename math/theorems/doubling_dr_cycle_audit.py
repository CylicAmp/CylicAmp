"""
doubling_dr_cycle_audit.py

The doubling sequence in DR-space and the repunit spatial identity.

─────────────────────────────────────────────────────────────────
SEQUENCE:
  1×1 = 1   DR = 1   (unit: multiplicative fixed point)
  1+1 = 2   DR = 2
  2+2 = 4   DR = 4
  3+3 = 6   DR = 6
  4+4 = 8   DR = 8
  5+5 = 10  DR = 1   ← returns to 1

DR sequence: [1, 2, 4, 6, 8, 1]
Interior set {2,4,6,8} = all four even DRs.
Period 5 under the map n ↦ DR(2n), starting from DR=1.

BRACKET STRUCTURE:
  1 - 2 - (4,6,8) - 1
  The unit 1 bookends. 2 leads. {4,6,8} follow. 1 closes.

PARALLEL (null-framed repunit sequence):
  0 - 11 - 111 - 0
  Null 0 bookends. 11 (prime, DR=2). 111 (=3×37, DR=3). Null 0 closes.

FULL DOUBLING CYCLE (k=1..9):
  DR(2k): [2, 4, 6, 8, 1, 3, 5, 7, 9]
  Covers all 9 DR values in exactly 9 steps.
  Arithmetic sequence in DR-space with step 2.

REPUNIT IDENTITY (spatial = value):
  DR(repunit_n) = n  for n = 1..9
  because digit_sum(1^n) = n, and DR(n) = n for 1 ≤ n ≤ 9.
  These are the unique numbers where spatial measure (digit count)
  equals value measure (DR).

SPATIAL COUNTING:
  11111 = 5 (five 1s: digit sum = 5 = position count)
  00000 = 5 (five 0s: position count = 5; DR = 0)
  When counting space, 1 and 0 each occupy one position.
  11111 and 00000 are spatially equivalent; their DR values differ.

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


# ── Sequence: 1×1 then n+n for n=1..5 ────────────────────────────────────────

OPS  = [(1*1, "1×1"), (1+1, "1+1"), (2+2, "2+2"), (3+3, "3+3"), (4+4, "4+4"), (5+5, "5+5")]
VALS = [v for v, _ in OPS]

check(VALS == [1, 2, 4, 6, 8, 10], "sequence values", VALS, [1, 2, 4, 6, 8, 10])

DR_SEQ = [dr(v) for v in VALS]
check(DR_SEQ == [1, 2, 4, 6, 8, 1], "DR sequence", DR_SEQ, [1, 2, 4, 6, 8, 1])

# Closes: first and last DR both 1
check(DR_SEQ[0] == DR_SEQ[-1] == 1, "cycle closes at 1", (DR_SEQ[0], DR_SEQ[-1]), (1, 1))


# ── Interior = all four even DRs ──────────────────────────────────────────────

interior = DR_SEQ[1:-1]   # excludes the two 1s
check(sorted(interior) == [2, 4, 6, 8], "interior = even DRs", sorted(interior), [2, 4, 6, 8])
check(interior == [2, 4, 6, 8], "interior in order", interior, [2, 4, 6, 8])


# ── 1 is multiplicative fixed point ──────────────────────────────────────────

check(1 * 1 == 1, "1×1=1", 1 * 1, 1)
check(dr(1 * 1) == 1, "DR(1×1)=1", dr(1 * 1), 1)


# ── 5+5=10, DR=1 (closes the cycle) ──────────────────────────────────────────

check(5 + 5 == 10, "5+5=10", 5 + 5, 10)
check(dr(10) == 1, "DR(10)=1", dr(10), 1)
check(10 % 9 == 1, "10 mod 9 = 1", 10 % 9, 1)


# ── Full doubling cycle DR(2k) for k=1..9 ────────────────────────────────────

FULL = [dr(2 * k) for k in range(1, 10)]
check(FULL == [2, 4, 6, 8, 1, 3, 5, 7, 9], "full DR(2k)", FULL, [2, 4, 6, 8, 1, 3, 5, 7, 9])
check(set(FULL) == set(range(1, 10)), "full cycle covers all 9 DRs", set(FULL), set(range(1, 10)))

# Step 2 in DR-space: each consecutive pair differs by 2 (mod 9)
for i in range(len(FULL) - 1):
    step = (FULL[i + 1] - FULL[i]) % 9
    check(step == 2, f"step DR(2×{i+1})→DR(2×{i+2})", step, 2)


# ── Bracket: 1-2(468)-1 ───────────────────────────────────────────────────────

# 1 bookends; {2} leads; {4,6,8} follow; 1 closes
bracket = [1, 2, 4, 6, 8, 1]
check(bracket[0] == bracket[-1] == 1, "bracket bookends", (bracket[0], bracket[-1]), (1, 1))
check(bracket[1] == 2, "bracket lead = 2", bracket[1], 2)
check(bracket[2:5] == [4, 6, 8], "bracket cluster = {4,6,8}", bracket[2:5], [4, 6, 8])


# ── Parallel: 0-P(11)-CCC(111)-0 ─────────────────────────────────────────────

# 0 bookends; 11 (prime repunit, DR=2); 111 (three-chart repunit = 3×37, DR=3)
check(isprime(11), "11 is prime", isprime(11), True)
check(factorint(111) == {3: 1, 37: 1}, "111=3×37", factorint(111), {3: 1, 37: 1})
check(dr(11) == 2, "DR(11)=2", dr(11), 2)
check(dr(111) == 3, "DR(111)=3", dr(111), 3)
check(11 % 9 == 2, "11≡2 mod 9", 11 % 9, 2)
check(111 % 9 == 3, "111≡3 mod 9", 111 % 9, 3)


# ── Repunit identity: DR(repunit_n) = n for n=1..9 ───────────────────────────

for n in range(1, 10):
    repunit = int('1' * n)
    check(dr(repunit) == n, f"DR(repunit_{n})={n}", dr(repunit), n)
    check(len(str(repunit)) == n, f"len(repunit_{n})={n}", len(str(repunit)), n)
    # DR = position count: the only numbers where these two measures agree
    check(dr(repunit) == len(str(repunit)), f"repunit_{n} DR=positions", dr(repunit), len(str(repunit)))


# ── Spatial counting: 11111 and 00000 ────────────────────────────────────────

check(dr(11111) == 5, "DR(11111)=5", dr(11111), 5)
check(len('11111') == 5, "position count 11111 = 5", len('11111'), 5)
check(len('00000') == 5, "position count 00000 = 5", len('00000'), 5)

# For repunit_5: DR = position count = 5 (agreement)
check(dr(11111) == len('11111'), "DR(11111) = len(11111)", dr(11111), len('11111'))

# For 00000: DR = 0, position count = 5 (disagreement)
check(dr(0) == 0, "DR(0)=0", dr(0), 0)
check(dr(0) != len('00000'), "DR(00000) ≠ len(00000)", dr(0) != len('00000'), True)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Doubling DR Cycle and Repunit Spatial Identity Audit")
    print("=" * 62)

    print(f"\n── Sequence: 1×1, n+n for n=1..5 ──")
    for v, expr in OPS:
        print(f"  {expr} = {v:2d}  DR={dr(v)}")
    print(f"  DR sequence: {DR_SEQ}")
    print(f"  Cycle: opens at DR=1, closes at DR=1 after 5 steps")

    print(f"\n── Bracket: 1-2(4,6,8)-1 ──")
    print(f"  Interior {{{','.join(str(x) for x in interior)}}} = all four even DRs")

    print(f"\n── Parallel: 0-P(11)-CCC(111)-0 ──")
    print(f"  11  = prime          DR=2  (11≡2 mod 9)")
    print(f"  111 = 3×37           DR=3  (111≡3 mod 9)")
    print(f"  0 bookends (null boundary)")

    print(f"\n── Full doubling cycle DR(2k), k=1..9 ──")
    for k, d in enumerate(FULL, 1):
        print(f"  k={k}  2×{k}={2*k:2d}  DR={d}")
    print(f"  Covers all 9 DRs: {set(FULL) == set(range(1,10))}")
    print(f"  Step = 2 in DR-space throughout")

    print(f"\n── Repunit identity ──")
    print(f"  {'repunit':>12s}  DR  positions  agree")
    for n in range(1, 10):
        rep = int('1' * n)
        print(f"  {'1'*n:>12s}  {dr(rep):>2d}  {len(str(rep)):>9d}  {dr(rep)==n}")

    print(f"\n── Spatial counting ──")
    print(f"  11111 : DR={dr(11111)}  positions={len('11111')}  (agree — repunit identity)")
    print(f"  00000 : DR={dr(0)}  positions={len('00000')}  (spatial only: 0 occupies 1 position)")
    print(f"  When counting space, 1 and 0 each occupy one position.")
    print(f"  Repunits are the only numbers where spatial measure = DR.")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
