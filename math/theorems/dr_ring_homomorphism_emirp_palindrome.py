"""
DR Ring Homomorphism, Emirp Invariance, Palindromic Prime Sovereign Exclusion
==============================================================================

1. DR IS A RING HOMOMORPHISM
   DR: Z → Z/9Z*  where Z/9Z* = {1,2,...,9} with 9 acting as 0.
   DR(a + b) = DR(DR(a) + DR(b))    (additive)
   DR(a × b) = DR(DR(a) × DR(b))    (multiplicative)

   This is "casting out nines" formalized: any arithmetic computation
   can be shadow-checked by reducing operands to their DR and re-computing.
   The result's DR must match.

   Examples:
     17×23=391:  DR(8×5)=DR(40)=4  =  DR(391)  ✓
     12×13=156:  DR(3×4)=DR(12)=3  =  DR(156)  ✓
      9× 9= 81:  DR(9×9)=DR(81)=9  =  DR(81)   ✓
     37×73=2701: DR(1×1)=DR(1) =1  =  DR(2701) ✓

   The reversal collapse (DR(|n-rev(n)|)=9) is a corollary:
     DR(n) = DR(rev(n)) always (digit sum permutation-invariant)
     → DR(n - rev(n)) = DR(DR(n) - DR(n)) = DR(0 mod 9) = 9

2. EMIRP DR INVARIANCE
   For any emirp pair (p, rev(p)):
     DR(p) = DR(rev(p))  — always, zero exceptions.
   And: DR(|p - rev(p)|) = 9  — always, zero exceptions.

   Consequence: DR algebra is BLIND to emirp pairs.
   p and rev(p) are indistinguishable in DR space.
   The mod-37 non-uniformity (Z = +2.93) is entirely invisible to DR.

   The two number-theoretic filters are ORTHOGONAL:
     DR algebra:  collapses (p, rev(p)) to a single point
     Mod-37:      separates (p, rev(p)) via 25(c-a) mod 37

   DR of emirp pairs (first 15):
     (13,31)  DR=4  diff=18  DR(diff)=9   chi_{-3}=+1  [COL1]
     (17,71)  DR=8  diff=54  DR(diff)=9   chi_{-3}=-1  [COL2, AHL]
     (37,73)  DR=1  diff=36  DR(diff)=9   chi_{-3}=+1  [COL1]
     (79,97)  DR=7  diff=18  DR(diff)=9   chi_{-3}=+1  [COL1]
     (107,701) DR=8  diff=594 DR(diff)=9  chi_{-3}=-1  [COL2, AHL]
     (157,751) DR=4  diff=594 DR(diff)=9  chi_{-3}=+1  [COL1]

   Note: AHL pair (17,71) and (107,701) both have DR=8.
   DR=8 emirps are enriched at residue r=8 mod 37 (the AHL residue).

3. PALINDROMIC PRIME SOVEREIGN EXCLUSION
   A palindromic prime is a prime p with rev(p) = p (same digits).
   Palindromic primes are NOT emirps (rev(p)=p, not a distinct prime).

   Theorem: all palindromic primes > 3 have DR ∈ {1,2,4,5,7,8}
            (the doubling orbit, sovereign-free).

   Proof: any palindromic prime > 3 must be coprime to 3.
     If 3 | p, then p = 3 (since 3 is prime). For p > 3:
     3 ∤ p  →  digit_sum(p) ≢ 0 (mod 3)  →  DR(p) ∉ {3,6,9}.

   The only palindromic prime with DR ∈ {3,6,9} is 3 itself (DR=3).

   Even-digit palindromic primes: only 11 exists.
   Proof: a 2k-digit palindrome (k ≥ 2) is divisible by 11 (alternating
   digit sum = 0 for palindromes → 11 | palindrome). So 11 is the lone
   even-digit palindromic prime.

   DR distribution (113 palindromic primes up to 10^6):
     DR=1: 18   DR=2: 22   DR=3:  1 (only the prime 3)
     DR=4: 17   DR=5: 18   DR=6:  0
     DR=7: 20   DR=8: 17   DR=9:  0
     COL2 (2,5,8): 57   COL1 (1,4,7): 55   COL3 (3,6,9): 1

   chi_{-3} distribution (palindromic primes > 3):
     chi = −1: 56  [COL2]   chi = +1: 55  [COL1]   chi = 0: 0
   Near-equal split: palindromic primes distribute across both chi classes
   with no bias (unlike twin primes which are structurally locked).

4. SUMMARY: HIERARCHY OF FILTERS
   DR (mod 9):     Collapses n and rev(n) to the same value.
                   Emirp pairs are invisible. Reversal → sovereign DR=9.
   Mod 37:         Separates n and rev(n) via digit position weighting.
                   Emirp non-uniformity Z=+2.93. Source: ord10(37)=3.
   Chi_{-3} (mod 3): Partitions all integers into COL1/COL2/COL3.
                   Twin prime structure locked (-1, 0, +1). Palindromic
                   primes avoid COL3. Emirp pairs share chi value.
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
    return int(str(n)[::-1])


def is_palindrome(n: int) -> bool:
    return str(n) == str(n)[::-1]


def sieve(limit: int):
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i :: i] = bytearray(len(is_p[i * i :: i]))
    return is_p


# ── 1. DR ring homomorphism (casting out nines) ───────────────────────────────

ring_checks = [
    (17, 23, 391),
    (12, 13, 156),
    (9, 9, 81),
    (37, 73, 2701),
    (496, 31, 15376),
    (8, 17, 136),
]
for a, b, prod in ring_checks:
    assert a * b == prod
    assert dr(dr(a) * dr(b)) == dr(prod), f"Homomorphism failed: {a}×{b}={prod}"
    assert dr(dr(a) + dr(b)) == dr(a + b), f"Additive failed: {a}+{b}={a+b}"

# ── 2. Emirp DR invariance ────────────────────────────────────────────────────

is_p = sieve(10 ** 6)
emirp_dr_violations = 0
emirp_diff_violations = 0
for p in range(13, 10 ** 6):
    if is_p[p]:
        rp = rev_num(p)
        if len(str(rp)) == len(str(p)) and is_p[rp] and p != rp:
            if dr(p) != dr(rp):
                emirp_dr_violations += 1
            if dr(abs(p - rp)) != 9:
                emirp_diff_violations += 1

assert emirp_dr_violations == 0, f"DR(p)≠DR(rev(p)) in {emirp_dr_violations} cases"
assert emirp_diff_violations == 0, f"DR(|p-rev(p)|)≠9 in {emirp_diff_violations} cases"

# AHL emirp pairs (DR=8)
ahl_pairs = [(p, rev_num(p)) for p in range(13, 10000)
             if is_p[p] and is_p[rev_num(p)] and len(str(rev_num(p))) == len(str(p))
             and p != rev_num(p) and dr(p) == 8 and p < rev_num(p)]
assert all(dr(p) == 8 and dr(rp) == 8 for p, rp in ahl_pairs)
assert (17, 71) in ahl_pairs
assert (107, 701) in ahl_pairs

# ── 3. Palindromic prime sovereign exclusion ──────────────────────────────────

pal_primes = [p for p in range(2, 10 ** 6 + 1) if is_p[p] and is_palindrome(p)]

# Only 3 has DR in sovereign set
assert [p for p in pal_primes if dr(p) in {3, 6, 9}] == [3]

# Only 11 has even digit count
even_digit_pals = [p for p in pal_primes if len(str(p)) % 2 == 0]
assert even_digit_pals == [11]

# All palindromic primes > 3 are sovereign-free (DR in doubling orbit)
doubling_orbit = {1, 2, 4, 5, 7, 8}
assert all(dr(p) in doubling_orbit for p in pal_primes if p > 3)

# chi_{-3}: no palindromic prime > 3 has chi=0
assert all(chi_m3(p) != 0 for p in pal_primes if p > 3)

# Near-equal chi split (within 5%)
chi_counts = {1: sum(1 for p in pal_primes if p > 3 and chi_m3(p) == 1),
             -1: sum(1 for p in pal_primes if p > 3 and chi_m3(p) == -1)}
assert abs(chi_counts[1] - chi_counts[-1]) < 10, "Palindromic prime chi split too asymmetric"

# ── 4. Orthogonality: DR blind to mod-37 emirp signal ────────────────────────

# 3-digit emirp pairs: DR(p)=DR(rev(p)) but 25(c-a) mod 37 varies
three_digit_emirp_pairs = [
    (p, rev_num(p)) for p in range(100, 1000)
    if is_p[p] and is_p[rev_num(p)] and p != rev_num(p) and p < rev_num(p)
]
assert len(three_digit_emirp_pairs) > 0
# All share DR; their mod-37 difference 25(c-a) takes multiple values
diff_37_values = set()
for p, rp in three_digit_emirp_pairs:
    a, c = int(str(p)[0]), int(str(p)[2])
    diff_37_values.add((25 * (c - a)) % 37)
# Actual emirp pairs only cover a subset of the 9 theoretically possible differences;
# the full 9 arise from all (a,c) ∈ {1,3,7,9}² — see emirp_mod37_nonuniformity.py
theoretical_diffs = {(25 * (c - a)) % 37 for a in (1, 3, 7, 9) for c in (1, 3, 7, 9)}
assert len(theoretical_diffs) == 9, f"Expected 9 theoretical mod-37 differences"
assert diff_37_values <= theoretical_diffs, "Actual diffs not a subset of theoretical"
# But all DR differences are 9
assert all(dr(rp - p) == 9 for p, rp in three_digit_emirp_pairs)


if __name__ == "__main__":
    from collections import Counter

    print("DR RING HOMOMORPHISM, EMIRP INVARIANCE, PALINDROMIC PRIMES")
    print("=" * 60)
    print()

    print("1. CASTING OUT NINES (DR ring homomorphism)")
    for a, b, prod in ring_checks:
        print(f"   {a}×{b}={prod}:  "
              f"DR({dr(a)})×DR({dr(b)})=DR({dr(a)*dr(b)})={dr(dr(a)*dr(b))}  "
              f"=  DR({prod})={dr(prod)}  ✓")
    print()

    print("2. EMIRP DR INVARIANCE")
    print(f"   Violations DR(p)≠DR(rev(p)) in [13,10^6]: {emirp_dr_violations}")
    print(f"   Violations DR(|p-rev(p)|)≠9 in [13,10^6]: {emirp_diff_violations}")
    print()
    print("   First 12 emirp pairs (p < rev(p)):")
    first12 = [(p, rev_num(p)) for p in range(13, 1000)
               if is_p[p] and is_p[rev_num(p)] and len(str(rev_num(p)))==len(str(p))
               and p != rev_num(p) and p < rev_num(p)][:12]
    for p, rp in first12:
        a, c = int(str(p)[0]), int(str(p)[-1])
        d37 = (25*(c-a))%37 if len(str(p))==3 else "—"
        ahl = " ← AHL" if dr(p) == 8 else ""
        print(f"   ({p:>4},{rp:>4})  DR={dr(p)}  |diff|={rp-p}  DR(diff)={dr(rp-p)}  "
              f"chi={chi_m3(p):+d}  mod37diff={d37}{ahl}")
    print()
    print(f"   AHL (DR=8) emirp pairs up to 10^4: {ahl_pairs}")
    print()

    print("3. PALINDROMIC PRIME SOVEREIGN EXCLUSION")
    print(f"   Total palindromic primes up to 10^6: {len(pal_primes)}")
    print(f"   With DR in {{3,6,9}}: {[p for p in pal_primes if dr(p) in {3,6,9}]}")
    print(f"   Even-digit palindromic primes: {even_digit_pals}")
    print()
    dr_dist = Counter(dr(p) for p in pal_primes)
    print("   DR distribution:")
    for col, members in [("COL1", [1,4,7]), ("COL2", [2,5,8]), ("COL3", [3,6,9])]:
        total_col = sum(dr_dist[d] for d in members)
        vals = " ".join(f"DR={d}:{dr_dist[d]}" for d in members)
        print(f"   {col}: {vals}  (total={total_col})")
    print()
    print(f"   chi_{{-3}} split (palindromic primes > 3):")
    print(f"     chi=+1: {chi_counts[1]}   chi=-1: {chi_counts[-1]}   chi=0: 0")
    print()

    print("4. ORTHOGONALITY SUMMARY")
    print("   DR algebra:   DR(p) = DR(rev(p)) → emirp pairs collapse to 1 point")
    print("   Mod-37:       25(c-a) mod 37 → 9 distinct values → Z=+2.93 signal")
    print("   Chi_{-3}:     palindromic primes avoid kernel; twin primes lock (-1,0,+1)")
    print()
    print("   The three filters operate on independent number-theoretic tracks.")
    print("   Z/9Z sees: palindromes. Z/37Z sees: digit reversals. Z/3Z sees: columns.")
    print()
    print("All assertions passed.")
