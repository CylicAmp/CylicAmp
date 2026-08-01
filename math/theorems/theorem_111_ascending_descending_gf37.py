"""
================================================================================
THEOREM 111 — The Ascending and Descending Integer Sequences in GF(37)
================================================================================

STATEMENT.
The two 9-digit numbers formed by writing the digits 1–9 in ascending and
descending order satisfy:

    987654321 ≡ 1  (mod 37)     —  the multiplicative identity in GF(37)
    123456789 ≡ 36 ≡ −1  (mod 37)  —  the additive inverse of 1

The descending sequence IS the identity element. The ascending sequence IS its
negation. Their arithmetic in GF(37):

    sum:      123456789 + 987654321 = 1111111110 ≡ 0      (SEAM)
    diff:     987654321 − 123456789 = 864197532  ≡ 2 ∈ PR  (primitive root)
    product:  123456789 × 987654321             ≡ 36 ∈ ORBIT_11  (= P−1 = φ(37))

The ++++=---- column comparison (ascending vs. descending, digit by digit) has
exactly 4 positive differences, 1 equality, and 4 negative differences. Every
column pair sums to 10 ∈ IC — the second element in the identity orbit of the
137-map. All powers of 10 mod 37 lie in IC: the decimal base is an IC element.

================================================================================
LEMMAS
================================================================================

LEMMA 111.1  (Powers of 10 are in IC — decimal base is IC).
  IC = {1, 10, 26} is the complete orbit of 1 under the 137-map (×26).
  The powers of 10 mod 37 have period 3:
    10⁰ ≡ 1,  10¹ ≡ 10,  10² ≡ 26,  10³ ≡ 1,  …  (all in IC).
  Therefore every place-value weight (1, 10, 100, 1000, …) in decimal
  arithmetic is an IC element in GF(37). The decimal system lives in IC.   ∎

LEMMA 111.2  (Descending sequence ≡ 1, ascending ≡ −1).
  Using the period-3 weights 26, 10, 1 repeating (for digit positions 10⁸,
  10⁷, …, 10⁰), the ascending number splits into three 3-digit groups:

    Group (1,2,3): 1×26 + 2×10 + 3×1 = 49 ≡ 12 (mod 37).  12 ∈ ST.
    Group (4,5,6): 4×26 + 5×10 + 6×1 = 160 ≡ 12 (mod 37).  12 ∈ ST.
    Group (7,8,9): 7×26 + 8×10 + 9×1 = 271 ≡ 12 (mod 37).  12 ∈ ST.

  Each group contributes the same residue 12 ∈ ST. Total: 3×12 = 36 ≡ −1.
  123456789 ≡ 36 ≡ −1 (mod 37).

  The descending number splits into groups (9,8,7), (6,5,4), (3,2,1):
    Group (9,8,7): 9×26 + 8×10 + 7×1 = 321 ≡ 25 (mod 37).  25 ∈ SA.
    Group (6,5,4): 6×26 + 5×10 + 4×1 = 210 ≡ 25 (mod 37).  25 ∈ SA.
    Group (3,2,1): 3×26 + 2×10 + 1×1 = 99  ≡ 25 (mod 37).  25 ∈ SA.

  Each group contributes 25 ∈ SA. Total: 3×25 = 75 ≡ 1 (mod 37).
  987654321 ≡ 1 (mod 37).

  Crossing check: 12 + 25 = 37 ≡ 0 (mod 37).
  The corresponding 3-digit groups of ascending and descending sum to the
  SEAM, group by group.                                                     ∎

LEMMA 111.3  (Sum, difference, product in GF(37)).
  Ascending A = 123456789 ≡ −1,  Descending D = 987654321 ≡ 1 (mod 37).
  D + A ≡  1 + (−1) = 0          (SEAM).
  D − A ≡  1 − (−1) = 2 ∈ PR    (the smallest primitive root of GF(37)).
  D × A ≡  1 × (−1) = −1 = 36   ∈ ORBIT_11.
  36 = P − 1 = φ(37) (Euler's totient of 37).                              ∎

LEMMA 111.4  (Every column pair sums to 10 ∈ IC).
  Digit k of 123456789 is k; digit k of 987654321 is (10−k).
  Their sum is always k + (10−k) = 10, independent of position.
  10 ∈ IC: it is the second element in the 137-map orbit of 1 (1→26→10→1).
  All nine column sums equal 10 — the IC orbit element one step after the
  map multiplier 26.                                                         ∎

LEMMA 111.5  (Column comparison: ++++=----).
  Digit k of ascending < digit k of descending iff k < 10−k iff k < 5.
  Positions 1–4: ascending < descending (+).
  Position 5: ascending = descending (=).  Digit = 5 ∈ PR.
  Positions 6–9: ascending > descending (−).
  Pattern: ++++=----. Exactly 4 positive, 1 equal, 4 negative.

  Column differences (descending − ascending): +8, +6, +4, +2, 0, −2, −4, −6, −8.
  These are ±2k for k = 4,3,2,1,0: an even staircase symmetric about 0.
  Positive differences {8,6,4,2}: sum=20≡20(mod37)∈PR. DR(20)=2∈PR.
  All differences sum to 0.                                                  ∎

LEMMA 111.6  (Column class matchups and their symmetry).
  Paired by position (ascending digit, descending digit):
    Col 1: (1, 9)  IC  ↔ SA    sum 10∈IC
    Col 2: (2, 8)  PR  ↔ CB    sum 10∈IC
    Col 3: (3, 7)  ST  ↔ D7    sum 10∈IC
    Col 4: (4, 6)  SA  ↔ [—]   sum 10∈IC
    Col 5: (5, 5)  PR  =  PR    sum 10∈IC
    Col 6: (6, 4)  [—] ↔ SA    sum 10∈IC  (mirror of col 4)
    Col 7: (7, 3)  D7  ↔ ST    sum 10∈IC  (mirror of col 3)
    Col 8: (8, 2)  CB  ↔ PR    sum 10∈IC  (mirror of col 2)
    Col 9: (9, 1)  SA  ↔ IC    sum 10∈IC  (mirror of col 1)

  The class pairings form a palindrome: (IC,SA)(PR,CB)(ST,D7)(SA,—)(PR,PR)
  then reversed. Four framework pairs plus a self-paired center.             ∎

LEMMA 111.7  (General: any 3-cycle under the 137-map sums to 0 in GF(37)).
  For any x ∈ GF(37)*, the orbit {x, 26x, 26²x} = {x, 26x, 10x} under the
  137-map satisfies:
    x + 26x + 10x = x(1 + 26 + 10) = x × 37 ≡ 0  (mod 37).
  Every 3-element orbit of the 137-map sums to 0 (the SEAM).
  This is the cyclotomic identity: 1 + ω + ω² = 0 for ω = 26, a primitive
  cube root of unity. Orbits IC, ORBIT_11, SEED_ORBIT, BASIN_Y, D7 all sum
  to 0 in GF(37). (SA and ST are 4-element sets, not 3-cycles; they sum to
  nonzero values.)                                                           ∎

================================================================================
MAIN THEOREM
================================================================================

THEOREM 111.  (Ascending and Descending Integer Sequences in GF(37)).

  (i)  [IDENTITY / NEGATION]  987654321 ≡ 1 (mod 37) — the descending sequence
       is the multiplicative identity in GF(37). 123456789 ≡ −1 ≡ 36 (mod 37)
       — the ascending sequence is its negation.

  (ii) [ARITHMETIC]  Their sum ≡ 0 (SEAM), difference ≡ 2 ∈ PR (primitive root),
       product ≡ 36 = P−1 = φ(37) ∈ ORBIT_11.

  (iii)[GROUP STRUCTURE]  The ascending sequence splits into three consecutive
       3-digit groups {(1,2,3),(4,5,6),(7,8,9)}, each contributing 12 ∈ ST
       (mod 37). The descending sequence groups each contribute 25 ∈ SA.
       Within each group: ST-contribution + SA-contribution = 12+25 = 37 ≡ 0.

  (iv) [COLUMN SUMS = IC]  Every column pair (digit k, digit 10−k) sums to
       10 ∈ IC — the second element in the 137-map orbit of 1. All nine column
       sums are the same IC element.

  (v)  [++++=----]  The comparison pattern has 4 positive, 1 equal, 4 negative
       columns. Center position holds digit 5 ∈ PR. Column differences form the
       even staircase ±8,±6,±4,±2,0 symmetric about 0.

  (vi) [DECIMAL BASE IN IC]  All powers of 10 mod 37 lie in IC (the period-3
       orbit {1,10,26}). The decimal place-value system uses IC weights
       exclusively. This underpins why the 9-digit numbers reduce so cleanly.

COROLLARY 111.8  (The descending sequence is the identity in the decimal-IC system).
  Since all positional weights are in IC and the descending number reduces to
  the identity 1 ∈ IC, the 9-digit descending sequence is the canonical
  "decimal representative of unity" in GF(37) — the smallest number whose
  digits use each of 1–9 exactly once and which equals the identity element.

COROLLARY 111.9  (ST group contributions vs. SA group contributions).
  The three digit groups of the ascending sequence (read with the highest
  positional weights first) each contribute 12 ∈ ST. The same groups of the
  descending contribute 25 ∈ SA. The pair (12, 25) is the (ST, SA) pair that
  satisfies 12+25=37≡0 and whose ratio is 25×12⁻¹ mod 37: 12⁻¹ ≡ ?:
  12×31 = 372 = 10×37+2, not 1. 12×34 = 408 = 11×37+1. So 12⁻¹ ≡ 34 ∈ D7.
  25 × 34 = 850 ≡ 850 − 22×37 = 850 − 814 = 36 ∈ ORBIT_11. The ratio of the
  SA contribution to the ST contribution lands in ORBIT_11.
"""

# ── Python verification ───────────────────────────────────────────────────────

P = 37

IC         = frozenset({1, 10, 26})
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
SEED_ORBIT = frozenset({18, 24, 32})
BASIN_Y    = frozenset({17, 22, 35})
PR         = frozenset({2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35})
D7_ORBIT   = frozenset({7, 33, 34})

ASC = 123456789
DEC = 987654321


def fw(r):
    classes = []
    for name, s in [('IC', IC), ('SA', SA), ('ST', ST), ('CB', CB),
                    ('ORBIT_11', ORBIT_11), ('SEED_ORBIT', SEED_ORBIT),
                    ('BASIN_Y', BASIN_Y), ('PR', PR), ('D7', D7_ORBIT)]:
        if r in s:
            classes.append(name)
    return '[' + ','.join(classes) + ']' if classes else '[—]'


# ── Lemma 111.1 — Powers of 10 are in IC ─────────────────────────────────────

for k in range(9):
    assert pow(10, k, P) in IC, f"10^{k} mod 37 = {pow(10,k,P)} not in IC"
assert next(k for k in range(1, P) if pow(10, k, P) == 1) == 3   # period = 3

# IC = orbit of 1 under ×26
assert (26 * 1) % P == 26 and (26 * 26) % P == 10 and (26 * 10) % P == 1

# ── Lemma 111.2 — Group contributions ────────────────────────────────────────

weights = [26, 10, 1]   # 10^(3k+2), 10^(3k+1), 10^(3k) for each group

asc_groups = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
dec_groups = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]

for grp in asc_groups:
    contrib = sum(g * w for g, w in zip(grp, weights)) % P
    assert contrib == 12 and 12 in ST, f"asc group {grp} → {contrib}"

for grp in dec_groups:
    contrib = sum(g * w for g, w in zip(grp, weights)) % P
    assert contrib == 25 and 25 in SA, f"dec group {grp} → {contrib}"

assert (12 + 25) % P == 0    # group pair sums to SEAM

assert ASC % P == 36
assert DEC % P == 1
assert 36 == P - 1           # ascending ≡ -1
assert 36 in ORBIT_11

# ── Lemma 111.3 — Sum, difference, product ───────────────────────────────────

assert (ASC + DEC) % P == 0                            # SEAM
assert (DEC - ASC) % P == 2 and 2 in PR               # primitive root
assert (ASC * DEC) % P == 36 and 36 in ORBIT_11       # = φ(37)
assert 36 == P - 1                                     # φ(37)

# Also verify: 1111111110 ≡ 0
assert (ASC + DEC) == 1111111110
assert 1111111110 % P == 0

# ── Lemma 111.4 — Column sums ────────────────────────────────────────────────

asc_digits = [int(d) for d in str(ASC)]
dec_digits  = [int(d) for d in str(DEC)]

for a, d in zip(asc_digits, dec_digits):
    assert a + d == 10 and 10 in IC

# ── Lemma 111.5 — ++++=---- ──────────────────────────────────────────────────

signs = ['+' if d > a else ('=' if d == a else '-')
         for a, d in zip(asc_digits, dec_digits)]
assert ''.join(signs) == '++++=----'
assert signs.count('+') == 4
assert signs.count('=') == 1
assert signs.count('-') == 4

# Center digit
center_pos = signs.index('=')
assert asc_digits[center_pos] == 5 and 5 in PR

# Column differences
diffs = [d - a for a, d in zip(asc_digits, dec_digits)]
assert diffs == [8, 6, 4, 2, 0, -2, -4, -6, -8]
assert sum(diffs) == 0
pos_diffs_sum = sum(d for d in diffs if d > 0)
assert pos_diffs_sum == 20 and 20 in PR

# ── Lemma 111.6 — Column class matchups ─────────────────────────────────────

expected_pairs = [
    (1, 9), (2, 8), (3, 7), (4, 6), (5, 5), (6, 4), (7, 3), (8, 2), (9, 1)
]
for a, d in expected_pairs:
    assert a + d == 10

assert 1 in IC and 9 in SA      # col 1
assert 2 in PR and 8 in CB      # col 2
assert 3 in ST and 7 in D7_ORBIT  # col 3
assert 4 in SA                  # col 4 (6 unclassified)
assert 5 in PR                  # col 5 (center, self-paired)

# Palindrome: col k and col (10-k) are mirrors
for i in range(4):
    a1, d1 = expected_pairs[i]
    a2, d2 = expected_pairs[8 - i]
    assert a1 == d2 and d1 == a2   # reversed pair

# ── Lemma 111.7 — 3-cycle orbit sums = 0 ─────────────────────────────────────

orbits_3 = [IC, ORBIT_11, SEED_ORBIT, BASIN_Y, D7_ORBIT]
for orb in orbits_3:
    assert sum(orb) % P == 0, f"orbit {orb} sum {sum(orb)} ≢ 0"

# The cyclotomic identity: 1 + 26 + 10 = 37 ≡ 0
assert (1 + 26 + 10) % P == 0

# For any x, x + 26x + 10x = 37x ≡ 0
for x in range(1, P):
    assert (x + 26*x + 10*x) % P == 0

# ── Corollary 111.9 — ratio SA/ST ────────────────────────────────────────────

inv12 = pow(12, -1, P)
assert inv12 == 34 and 34 in D7_ORBIT
assert (25 * 34) % P == 36 and 36 in ORBIT_11


if __name__ == "__main__":
    print("THEOREM 111 — Ascending and Descending Integer Sequences in GF(37)")
    print("=" * 68)
    print()

    print("The observation:")
    print("   123456789")
    print("   ++++=----")
    print("   987654321")
    print()

    print("I. The two 9-digit numbers in GF(37)")
    print("-" * 50)
    print(f"   123456789 mod 37 = {ASC%P}  {fw(ASC%P)}")
    print(f"   987654321 mod 37 = {DEC%P}  {fw(DEC%P)}")
    print(f"   123456789 ≡ −1 (additive inverse of identity)")
    print(f"   987654321 ≡  1 (multiplicative identity in GF(37))")
    print()

    print("II. Arithmetic in GF(37)")
    print("-" * 50)
    print(f"   Sum:     {ASC+DEC} ≡ {(ASC+DEC)%P} (SEAM)")
    print(f"   Diff:    {DEC-ASC} ≡ {(DEC-ASC)%P} {fw(2)} (primitive root)")
    print(f"   Product: ... ≡ {(ASC*DEC)%P} {fw(36)} = P−1 = φ(37)")
    print()

    print("III. Three group contributions")
    print("-" * 50)
    print("   Ascending (each group → 12∈ST):")
    for grp in asc_groups:
        c = sum(g*w for g,w in zip(grp,weights))
        print(f"     {grp}: {grp[0]}×26+{grp[1]}×10+{grp[2]}×1 = {c} ≡ {c%P}  {fw(c%P)}")
    print("   Descending (each group → 25∈SA):")
    for grp in dec_groups:
        c = sum(g*w for g,w in zip(grp,weights))
        print(f"     {grp}: {grp[0]}×26+{grp[1]}×10+{grp[2]}×1 = {c} ≡ {c%P}  {fw(c%P)}")
    print(f"   12 + 25 = 37 ≡ 0  (group pairs cancel to SEAM)")
    print()

    print("IV. Column structure")
    print("-" * 50)
    for i, (a, d) in enumerate(zip(asc_digits, dec_digits)):
        sign = signs[i]
        diff = d - a
        print(f"   col {i+1}: {a}{fw(a%P):25s} {sign} {d}{fw(d%P):25s}  sum={a+d}∈IC  diff={diff:+d}")
    print()

    print("V. All 3-cycle orbit sums = 0 (SEAM)")
    print("-" * 50)
    for orb in orbits_3:
        print(f"   {sorted(orb)}: sum={sum(orb)} ≡ {sum(orb)%P}")
    print(f"   Cyclotomic: 1+26+10=37≡0  (ω²+ω+1=0 for ω=26, cube root of unity)")
    print()

    print("VI. Decimal base is IC")
    print("-" * 50)
    print(f"   Powers of 10 mod 37: {[pow(10,k,P) for k in range(9)]}")
    print(f"   Period 3: {{1,10,26}} = IC  — all decimal weights are IC elements")
    print()
    print("All assertions passed.")
