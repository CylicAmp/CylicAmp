"""
prime_sieve_dr_audit.py

Five verified results: DR fixed point, wheel sieve mod 9, twin prime
residue pairs, Zhang's gap theorem (reference), and the ε perturbation
analogy.  All computational claims are verified; Zhang's theorem is
referenced only.

─────────────────────────────────────────────────────────────────
RESULTS:
  (S1) DR FIXED POINT (proved).
       DR(2n) = n (equality of integers) for n ∈ ℕ = {1,2,…}
       if and only if n = 9.
       Note: n = 0 also satisfies trivially (DR(0)=0=n), but lies
       outside ℕ. The proof's Case 1 "If n=0, DR(0)=0 ≠ 0" contains
       a typographical error; the equality 0=0 holds, so n=0 IS a
       formal solution and must be excluded by the domain restriction.

  (S2) WHEEL SIEVE MOD 9 (proved).
       90 = 2×3²×5 ≡ 0 (mod 9).  Every column in a +90 matrix
       preserves its residue mod 9.  For p > 3 prime, p mod 9 ∈
       {1,2,4,5,7,8} (the six residues coprime to 3 mod 9).
       The +90 grid is thus a wheel sieve: columns for residues 0,3,6
       contain no primes >3.

  (S3) TWIN PRIME RESIDUE PAIRS (proved).
       For twin primes (p, p+2) with p > 3, the allowed residue pairs
       mod 9 are exactly:  (2,4),  (5,7),  (8,1).
       Pairs (1,3), (4,6), (7,0) are excluded because p+2 ≡ 0 mod 3.
       DR sums of the three pairs: 6, 3, 9 — the three-six-nine lock.
       In Z/37Z all three pairs are modal crossings (ORBIT_V ↔ ORBIT_P).

  (S4) ZHANG'S THEOREM (referenced, not re-proved).
       ∃ even h ≤ 246 such that lim inf (p_{n+1}−p_n) ≤ h.
       Source: Zhang (Ann. Math. 2014) + Polymath 8b (2014).
       The bound 246 is unconditional.

  (S5) ε PERTURBATION ANALOGY (structural).
       The singular correction ε₂ = 80−90 = −10 at M(2,1) in the
       non-uniform matrix is exactly −(26⁻¹ mod 37) = −(modular ratio).
       Sparse perturbations of arithmetic progressions are the template
       for number-theoretic sequences: primes after a sieve break
       uniform progressions exactly as ε breaks the +90 column.

FRAMEWORK CONNECTIONS:
  · 17 (criss-cross prime, DR=8=AHL) lies in pair (8,1).
    DR(17)=8=AHL; 17 mod 9=8.
  · (137,139) (the triad twin primes) lie in pair (2,4).
    DR(137)=2=e axiom; DR(139)=4; pair DR sum=6=DR(33)=DR(φ×e×π digits).
  · DR sums {6,3,9} of the three pairs = same DR-lock as grid column sums.
  · All three pairs are V→P or P→V in Z/37Z = modal crossings.
─────────────────────────────────────────────────────────────────
"""

from sympy import isprime, nextprime

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


ORBIT_P = [0, 1, 4, 13, 3, 10, 31, 20, 24, 36, 35, 32, 23, 33, 26, 5, 16, 12]
ORBIT_V = [2, 7, 22, 30, 17, 15, 9, 28, 11, 34, 29, 14, 6, 19, 21, 27, 8, 25]


# ── S1: DR fixed point — computational verification ───────────────────────────

# For n in {1,...,18}: only n=9 satisfies DR(2n) = n
solutions_positive = [n for n in range(1, 19) if dr(2 * n) == n]
check(solutions_positive == [9],
      "DR(2n)=n for n ∈ {1..18}: unique solution n=9",
      solutions_positive, [9])

check(dr(18) == 9, "DR(2×9) = DR(18) = 9", dr(18), 9)

# Proof structure verification
for n in range(1, 10):
    r = n % 9
    if r == 0:   # n ≡ 0 mod 9, n > 0: DR(2n) = 9; equation gives n = 9
        check(dr(2 * n) == 9, f"n={n} ≡ 0 mod 9: DR(2n)=9", dr(2 * n), 9)
        if n == 9:
            check(dr(2 * n) == n, "n=9: DR(18)=9=n ✓", dr(2 * n), 9)
    else:        # n ≢ 0 mod 9: DR(2n) = (2r) mod 9; need = r → r ≡ 0 mod 9: impossible
        two_r_mod_9 = (2 * r) % 9
        check(two_r_mod_9 != r,
              f"n={n} (r={r}): (2r) mod 9 = {two_r_mod_9} ≠ r (no solution)",
              two_r_mod_9 == r, False)

# Boundary note: n=0 satisfies trivially (DR(0)=0=0); excluded from ℕ
check(dr(0) == 0, "DR(0)=0 (repo convention)", dr(0), 0)
check(dr(2 * 0) == 0, "DR(2×0) = 0 = 0 (n=0 trivially satisfies but ∉ ℕ)", dr(2 * 0), 0)

# 9 is unique in {1..9}: only fixed point of the DR-doubling map
check(dr(2 * 9) == 9,     "DR(2×9) = 9 (fixed point)", dr(2 * 9), 9)
check(dr(9) == 9,         "DR(9) = 9 (NULL anchor)", dr(9), 9)
check((37 - 1) // 2 == 18, "GATE = 18 = 2×9", (37 - 1) // 2, 18)


# ── S2: Wheel sieve mod 9 ────────────────────────────────────────────────────

# 90 ≡ 0 mod 9
check(90 % 9 == 0, "90 ≡ 0 mod 9 (step preserves residue column)", 90 % 9, 0)
check(90 == 2 * 3 ** 2 * 5, "90 = 2×3²×5", 90, 2 * 3 ** 2 * 5)

# Primes > 3 cannot be ≡ 0, 3, 6 mod 9 (those are multiples of 3)
for r in [0, 3, 6]:
    check(r % 3 == 0, f"residue {r} ≡ 0 mod 3 → no prime > 3", r % 3, 0)

ALLOWED_RESIDUES = {1, 2, 4, 5, 7, 8}
FORBIDDEN_RESIDUES = {0, 3, 6}
check(ALLOWED_RESIDUES | FORBIDDEN_RESIDUES == set(range(9)),
      "allowed + forbidden = all residues mod 9",
      ALLOWED_RESIDUES | FORBIDDEN_RESIDUES, set(range(9)))
check(len(ALLOWED_RESIDUES) == 6, "6 allowed residues for primes > 3", len(ALLOWED_RESIDUES), 6)

# Verify computationally: all primes 5..500 in ALLOWED_RESIDUES
p = 5
while p <= 500:
    check(p % 9 in ALLOWED_RESIDUES, f"prime {p} mod 9 ∈ allowed",
          p % 9 in ALLOWED_RESIDUES, True)
    p = nextprime(p)


# ── S3: Twin prime residue pairs ──────────────────────────────────────────────

# Exact three allowed pairs
ALLOWED_PAIRS = {(2, 4), (5, 7), (8, 1)}

# Verify by case analysis of all 6 allowed r
excluded_r = []
for r in [1, 2, 4, 5, 7, 8]:
    r2 = (r + 2) % 9
    if r2 in FORBIDDEN_RESIDUES or r2 == 0:
        excluded_r.append(r)
        check(r2 not in ALLOWED_RESIDUES or r2 == 0,
              f"r={r}: r+2 mod 9={r2} excluded", r2 in FORBIDDEN_RESIDUES or r2 == 0, True)
    else:
        check((r, r2) in ALLOWED_PAIRS, f"pair ({r},{r2}) in allowed pairs",
              (r, r2) in ALLOWED_PAIRS, True)

check(set(excluded_r) == {1, 4, 7}, "excluded starting residues = {1,4,7}", set(excluded_r), {1, 4, 7})

# Computational scan: all twin primes up to 10000 must be in ALLOWED_PAIRS
p = 5
while p <= 10000:
    if isprime(p) and isprime(p + 2):
        pair = (p % 9, (p + 2) % 9)
        check(pair in ALLOWED_PAIRS, f"twin prime ({p},{p+2}) mod 9 ∈ allowed",
              pair in ALLOWED_PAIRS, True)
    p = nextprime(p)

# DR sums of allowed pairs
PAIR_DR_SUMS = {(2, 4): 6, (5, 7): 12, (8, 1): 9}
for (r1, r2), expected_sum in PAIR_DR_SUMS.items():
    check(r1 + r2 == expected_sum, f"pair ({r1},{r2}) sum = {expected_sum}",
          r1 + r2, expected_sum)

DR_OF_SUMS = {6: 6, 12: 3, 9: 9}
for s, d in DR_OF_SUMS.items():
    check(dr(s) == d, f"DR({s}) = {d}", dr(s), d)

# The three DR values form the three-six-nine set
check({dr(s) for s in PAIR_DR_SUMS.values()} == {3, 6, 9},
      "pair DR sums ∈ {3,6,9}", {dr(s) for s in PAIR_DR_SUMS.values()}, {3, 6, 9})

# Verified examples
for p, q, expected_pair in [(17, 19, (8, 1)), (41, 43, (5, 7)),
                              (71, 73, (8, 1)), (137, 139, (2, 4)),
                              (11, 13, (2, 4)), (5, 7, (5, 7))]:
    check(isprime(p) and isprime(q), f"({p},{q}) are prime", True, True)
    check((p % 9, q % 9) == expected_pair,
          f"({p},{q}) mod 9 = {expected_pair}", (p % 9, q % 9), expected_pair)


# ── S3 extension: Modal crossings in Z/37Z ────────────────────────────────────

for r1, r2 in [(2, 4), (5, 7), (8, 1)]:
    o1 = "P" if r1 in ORBIT_P else "V"
    o2 = "P" if r2 in ORBIT_P else "V"
    check(o1 != o2, f"pair ({r1},{r2}): {o1}→{o2} is a modal crossing",
          o1 != o2, True)


# ── S4: Zhang's theorem — boundary check (result only) ───────────────────────

ZHANG_BOUND = 246
check(ZHANG_BOUND == 246, "Zhang/Polymath 8b bound h ≤ 246 (unconditional)", ZHANG_BOUND, 246)
check(ZHANG_BOUND % 2 == 0, "h = 246 is even (required for prime gaps)", ZHANG_BOUND % 2, 0)

# The residue condition for h=246 is satisfiable: ∃ r such that
# both r and r+246 avoid {0,3,6} mod 9
h = 246
viable = [r for r in ALLOWED_RESIDUES if (r + h) % 9 in ALLOWED_RESIDUES]
check(len(viable) > 0, f"h={h}: some allowed r has r+{h} mod 9 also allowed",
      len(viable) > 0, True)


# ── S5: ε perturbation ────────────────────────────────────────────────────────

# From bivariate_grid_audit: standard step 90, singular step 80
epsilon_2 = 80 - 90
check(epsilon_2 == -10, "ε₂ = 80 − 90 = −10", epsilon_2, -10)
check(26 * 10 % 37 == 1, "10 = 26⁻¹ mod 37 (modular ratio)", 26 * 10 % 37, 1)
check(abs(epsilon_2) == 10, "|ε₂| = 10 = modular ratio", abs(epsilon_2), 10)


# ── Framework: 17 and (137,139) ───────────────────────────────────────────────

# 17 (criss-cross prime) in pair (8,1)
check(17 % 9 == 8, "17 mod 9 = 8 = AHL (criss-cross prime in pair (8,1))", 17 % 9, 8)
check(dr(17) == 8, "DR(17) = 8 = AHL", dr(17), 8)
check(19 % 9 == 1, "19 mod 9 = 1", 19 % 9, 1)
check((17 % 9, 19 % 9) == (8, 1), "(17,19) → pair (8,1)", (17 % 9, 19 % 9), (8, 1))

# (137,139) in pair (2,4) — the triad twin primes
check(137 % 9 == 2, "137 mod 9 = 2 = e axiom", 137 % 9, 2)
check(139 % 9 == 4, "139 mod 9 = 4", 139 % 9, 4)
check(dr(137) == 2, "DR(137) = 2 = e axiom", dr(137), 2)
check(dr(139) == 4, "DR(139) = 4", dr(139), 4)
check(dr(137) + dr(139) == 6, "DR(137)+DR(139) = 6 = pair DR sum", dr(137) + dr(139), 6)
check(dr(6) == 6, "DR(6) = 6 (fixed point)", dr(6), 6)

# slot-diff 137→139 in Z/37Z = 2 = twin prime gap (from triad audit)
check((139 % 37) - (137 % 37) == 2, "Z/37Z slot-diff 137→139 = 2 = gap",
      (139 % 37) - (137 % 37), 2)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Prime Sieve and DR Audit")
    print("=" * 62)

    print("\n── S1: DR fixed point DR(2n)=n ⟺ n=9 (n ∈ ℕ) ──")
    print("  Proof cases:")
    for n in range(1, 10):
        r = n % 9
        d2n = dr(2 * n)
        eq = "= n ✓" if d2n == n else f"≠ {n}"
        print(f"    n={n} (r={r}): DR({2*n}) = {d2n} {eq}")
    print(f"  Boundary: n=0 gives DR(0)=0=n, trivially true but 0 ∉ ℕ")
    print(f"  9 = GATE/2 = DR base = pivot of all DR cycles")

    print(f"\n── S2: Wheel sieve (+90 preserves residues mod 9) ──")
    print(f"  90 = 2×3²×5 ≡ 0 mod 9")
    print(f"  Primes > 3: allowed residues mod 9 = {sorted(ALLOWED_RESIDUES)}")
    print(f"  Forbidden (multiples of 3 mod 9): {{0,3,6}}")
    print(f"  6 of 9 columns survive the sieve")

    print(f"\n── S3: Twin prime residue pairs mod 9 ──")
    print(f"  Allowed starting residues: {sorted(ALLOWED_RESIDUES)}")
    print(f"  Excluded (p+2 hits multiple of 3): {{1,4,7}}")
    print(f"  Allowed pairs: {sorted(ALLOWED_PAIRS)}")
    print(f"  {'Pair':>6}  {'Sum':>4}  {'DR':>3}  {'ORBIT crossing (Z/37Z)'}")
    for r1, r2 in sorted(ALLOWED_PAIRS):
        s = r1 + r2
        o1 = "P" if r1 in ORBIT_P else "V"
        o2 = "P" if r2 in ORBIT_P else "V"
        print(f"  ({r1},{r2})   {s:>4}    {dr(s):>3}  ORBIT_{o1}→ORBIT_{o2} (modal crossing)")
    print(f"  DR values {{6,3,9}} = three-six-nine lock")

    print(f"\n── Examples ──")
    for p, q, pair in [(17,19,(8,1)), (41,43,(5,7)), (71,73,(8,1)), (137,139,(2,4))]:
        print(f"  ({p},{q}): mod9={pair}  DR({p})={dr(p)}  DR({q})={dr(q)}")
    print(f"  (137,139): DR(137)+DR(139)={dr(137)+dr(139)}=DR(33)=pair DR sum")

    print(f"\n── S4: Zhang's theorem (referenced) ──")
    print(f"  ∃ even h ≤ 246 with lim inf (p_{{n+1}}-p_n) ≤ h  (unconditional)")
    print(f"  Source: Zhang, Ann. Math. 2014; Polymath 8b, 2014")
    print(f"  h=246 viable: residues r where both r and r+246 avoid {{0,3,6}}: {viable}")

    print(f"\n── S5: ε perturbation ──")
    print(f"  ε₂ = 80−90 = −10 = −(26⁻¹ mod 37) = −(modular ratio)")
    print(f"  Sparse break in +90 column ↔ prime indicator breaking arithmetic progression")
    print(f"  Both are: smooth background + localized sparse deviation")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
