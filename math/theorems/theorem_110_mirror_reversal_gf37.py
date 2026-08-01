"""
================================================================================
THEOREM 110 — Mirror Reversal of 3-Digit Numbers in GF(37)
================================================================================

STATEMENT.
For any 3-digit number ABC, the reversal formula ABC − CBA = 99(A−C) gives
differences that are multiples of 99. In GF(37): 99 ≡ 25 ∈ SA (mod 37) — the
reversal constant is a Sovereign Anchor element. Equivalently: 99 ≡ 26 − 1
(mod 37), the distance from the identity to the 137-map multiplier.

From this central fact, five further results follow for the series with A=1:

  (i)   The 8 differences 99k (k=1..8) hit classes SA, CB, IC, IC, —, PR,
        ORBIT_11, PR in sequence. The fourth multiple 99×4 ≡ 26 ∈ IC — the
        137-map multiplier itself.

  (ii)  The inner 2-digit digit-sum staircase is {5,7,9,11,13,15,17} — seven
        consecutive odd integers, centered on 11 ∈ ORBIT_11. Every symmetric
        pair sums to 22 ∈ BASIN_Y ∩ PR.

  (iii) The first reversal pair sums to 123+321 = 444 = 12×37. The sum is
        exactly 12 times the prime; 12 ∈ ST.

  (iv)  The six permutations of the digits {1,2,3} all have digit-sum 6 (DR=6).
        Their three reversal pairs yield differences in SA and CB, and sums in
        {SEAM, SA∩ST, D7}.

  (v)   The nine single digits partition into three multiplicative DR families:
          {1,5,7}: sum 13 ∈ CB,   product mod 37 = 35 ∈ BASIN_Y (forbidden twin prime residue)
          {2,4,8}: sum 14,        product mod 37 = 27 ∈ ORBIT_11
          {3,6,9}: sum 18 ∈ SEED_ORBIT, product mod 37 = 14

================================================================================
DEFINITIONS
================================================================================

  ABC: the 3-digit number 100A + 10B + C, digits A,B,C ∈ {1,…,9} (A≠0).
  CBA: the reversal 100C + 10B + A.
  Inner pair: the 2-digit number BC from ABC and its reversal CB.
  Digit-sum staircase: the sequence of digit sums of the inner pairs (BC) for
    the A=1 series with B+C increasing.
  DR: digital root — iterative digit sum to single digit. DR(n) = ((n−1)%9)+1.
  Multiplicative DR families: partition of {1,…,9} by the orbit structure of
    repeated doubling in Z/9Z: {1,2,4,8,7,5} (main chain) and {3,6,9} (trinity).
    Sub-families: {1,5,7} (odd-prime subcycle), {2,4,8} (powers of 2), {3,6,9}.

================================================================================
LEMMAS
================================================================================

LEMMA 110.1  (Reversal formula).
  ABC − CBA = (100A+10B+C) − (100C+10B+A) = 99(A−C).
  The middle digit B cancels. The difference depends only on the first and
  last digits. The digital root of any nonzero such difference is 9, since
  DR(99k) = 9 for all nonzero k (99 = 9×11, and DR(9k)=9).              ∎

LEMMA 110.2  (99 ≡ 25 ∈ SA, the Sovereign Anchor).
  99 = 2×37 + 25.   99 ≡ 25 (mod 37).   25 ∈ SA.
  Equivalently: 99 = 100 − 1. 100 mod 37 = 26 ∈ IC (the 137-map multiplier).
  Therefore 99 ≡ 26 − 1 ≡ multiplier − identity (mod 37).
  Every mirror difference ABC − CBA ≡ 25(A−C) (mod 37).                 ∎

LEMMA 110.3  (The 8 multiples of 99 hit five named classes).
  For k=1..8, the residues 99k mod 37 are:
    k=1: 25 ∈ SA                   (Sovereign Anchor)
    k=2: 13 ∈ CB ∩ PR              (Cascade Base, Metonic orbit {5,13,19})
    k=3: 1  ∈ IC                   (multiplicative identity)
    k=4: 26 ∈ IC                   (the 137-map multiplier)
    k=5: 14                        (unclassified)
    k=6: 2  ∈ PR                   (primitive root, primitive root of GF(37))
    k=7: 27 ∈ ORBIT_11             (orbit-11 element)
    k=8: 15 ∈ PR                   (primitive root)
  Five of eight residues land in named framework classes. The sequence
  SA → CB → identity → multiplier in k=1..4 is a descent through sovereignty,
  cascade base, and the IC orbit to the map's own coefficient.             ∎

LEMMA 110.4  (Inner digit-sum staircase: center at ORBIT_11, edges at BASIN_Y).
  For the A=1 series, the inner pair BC (last two digits of 1BC) has digit sum
  B+C. The distinct values as C steps through 3,2,3,4,5,6,7,8,9 are:
      {5, 7, 9, 11, 13, 15, 17}  — seven consecutive odd integers.
  Center: 11 ∈ ORBIT_11.
  Symmetric pairs:
      5  + 17 = 22 ∈ BASIN_Y ∩ PR
      7  + 15 = 22 ∈ BASIN_Y ∩ PR
      9  + 13 = 22 ∈ BASIN_Y ∩ PR
  Every symmetric pair about the center 11 sums to 22 ∈ BASIN_Y ∩ PR.
  Sum of all seven: 77 ≡ 3 (mod 37) ∈ ST.  DR(77) = 5 ∈ PR.
  The staircase contains the lower elements of three twin prime pairs:
    5 (lower of (5,7)), 11 (lower of (11,13)), 17 (lower of (17,19)).    ∎

LEMMA 110.5  (123+321 = 444 = 12×37, a SEAM multiple).
  123 + 321 = 444.  444 / 37 = 12.  444 ≡ 0 (mod 37).
  The sum of the first mirror pair is exactly 12 times the prime.
  12 ∈ ST (Sovereign Target).                                              ∎

LEMMA 110.6  (Permutations of {1,2,3}).
  The six permutations of {1,2,3} as 3-digit numbers are 123, 132, 213, 231,
  312, 321. All have digit-sum 1+2+3=6, hence DR=6.

  The three reversal pairs and their framework classes:
    Pair (123, 321): |diff| = 198 ≡ 13 ∈ CB.  Sum = 444 ≡ 0 (SEAM).
    Pair (132, 231): |diff| = 99  ≡ 25 ∈ SA.  Sum = 363 ≡ 30 ∈ SA ∩ ST.
    Pair (213, 312): |diff| = 99  ≡ 25 ∈ SA.  Sum = 525 ≡ 7  ∈ D7_ORBIT.

  Differences land in CB and SA. Sums land in SEAM, SA∩ST, D7_ORBIT —
  one from each of the three "boundary" structures.                        ∎

LEMMA 110.7  (Three multiplicative DR families of single digits).
  Under the DR-doubling map (d ↦ DR(2d)), the nine single digits partition as:
    {1,2,4,8,7,5}: main 6-cycle under ×2 mod 9.
    {3,6,9}: trinity, fixed under +multiples of 3.

  Further sub-partition:
    {1,5,7}: odd elements of the 6-cycle (complement of {2,4,8} within it).
    {2,4,8}: powers of 2 (2¹=2, 2²=4, 2³=8).
    {3,6,9}: multiples of 3.

  Framework arithmetic of the three families:
    {1,5,7}: sum = 13 ∈ CB ∩ PR.
             product = 35 ≡ 35 (mod 37) ∈ BASIN_Y ∩ PR  =  the forbidden
             twin prime residue (p ≡ 35 → p+2 ≡ 0, blocked; Theorem 108).
    {2,4,8}: sum = 14  (unclassified).
             product = 64 ≡ 27 (mod 37) ∈ ORBIT_11.
    {3,6,9}: sum = 18 ∈ SEED_ORBIT ∩ PR.
             product = 162 ≡ 14 (mod 37)  (unclassified).

  The families {1,5,7} and {3,6,9} connect to CB and SEED_ORBIT — the same
  two classes containing the seed residue 24 (CB ∩ SEED_ORBIT).           ∎

LEMMA 110.8  (DR of n×4 visits all nine digital roots).
  gcd(4,9) = 1, so the map n ↦ 4n mod 9 is a permutation of Z/9Z.
  For n=1..9 the digital root of 4n visits every digit root 1..9 exactly once:
    n:   1 2 3 4 5 6 7 8 9
    4n:  4 8 12 16 20 24 28 32 36
    DR:  4 8  3  7  2  6  1  5  9
  This is the same permutation structure as multiplication by 26 in GF(37)
  (ord₃₇(26)=3 permutes a subset of residues). In Z/9Z, ×4 has order 3:
  4¹≡4, 4²≡7, 4³≡1 (mod 9) — matching DR(4)=4, DR(16)=7, DR(64)=1.       ∎

================================================================================
MAIN THEOREM
================================================================================

THEOREM 110.  (Mirror Reversal — GF(37) Structure).

  (i)  [REVERSAL CONSTANT]  For any 3-digit integer ABC:
       ABC − CBA = 99(A−C),  and  99 ≡ 25 ∈ SA (mod 37).
       Equivalently: 99 ≡ (137-map multiplier) − 1  (mod 37).
       Every nonzero mirror difference has digital root 9.

  (ii) [STAIRCASE SYMMETRY]  The inner 2-digit digit-sum staircase for the A=1
       series is {5,7,9,11,13,15,17}, centered on 11 ∈ ORBIT_11. Every pair
       symmetric about the center sums to 22 ∈ BASIN_Y. Sum of all seven ≡ 3
       ∈ ST (mod 37). Three consecutive twin prime lower elements are contained:
       5 (→(5,7)), 11 (→(11,13)), 17 (→(17,19)).

  (iii)[SEAM PRODUCT]  The first mirror sum: 123+321 = 444 = 12×37, with 12∈ST.
       The first reversal pair's sum is a Sovereign-Target multiple of the prime.

  (iv) [PERMUTATIONS OF {1,2,3}]  All six permutations have DR=6. Reversal
       pair differences land in CB and SA; sums land in SEAM, SA∩ST, D7.

  (v)  [THREE FAMILIES]  The nine digits split into {1,5,7} (sum=13∈CB,
       product≡35∈BASIN_Y), {2,4,8} (product≡27∈ORBIT_11), {3,6,9}
       (sum=18∈SEED_ORBIT). The forbidden twin prime residue 35 is the
       product of the odd prime-subcycle family {1,5,7}.

COROLLARY 110.9  (The 99 descent: SA → CB → identity → multiplier).
  Successive multiples of the reversal constant 99 ≡ 25 (mod 37) trace:
    99×1 ≡ 25 ∈ SA     — Sovereign Anchor
    99×2 ≡ 13 ∈ CB     — Cascade Base (Metonic orbit element)
    99×3 ≡  1 ∈ IC     — multiplicative identity
    99×4 ≡ 26 ∈ IC     — the 137-map multiplier
  Starting from a Sovereign Anchor element, repeated application of the
  reversal constant descends through cascade base and identity to the map's
  own coefficient in four steps.

COROLLARY 110.10  (Twin prime structure in the staircase).
  The digit sums 5,11,17 (positions 1,4,7 in the staircase) are each the
  lower element of a twin prime pair: (5,7), (11,13), (17,19). These are
  spaced 6 apart — the same gap as the period of Fermat residues mod 37
  (THEOREM 106). The staircase records twin prime structure at the level of
  inner digit sums.
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


def dr(n):
    if n == 0: return 9
    return ((n - 1) % 9) + 1


def fw(r):
    classes = []
    for name, s in [('IC', IC), ('SA', SA), ('ST', ST), ('CB', CB),
                    ('ORBIT_11', ORBIT_11), ('SEED_ORBIT', SEED_ORBIT),
                    ('BASIN_Y', BASIN_Y), ('PR', PR), ('D7', D7_ORBIT)]:
        if r in s:
            classes.append(name)
    return '[' + ','.join(classes) + ']' if classes else '[—]'


# ── Lemma 110.1 — Reversal formula ───────────────────────────────────────────

for A in range(1, 10):
    for B in range(0, 10):
        for C in range(0, 10):
            if C == 0 and A == 0: continue
            n = 100*A + 10*B + C
            rev = 100*C + 10*B + A
            assert n - rev == 99 * (A - C)
            if A != C:
                assert dr(abs(n - rev)) == 9   # always DR=9

# ── Lemma 110.2 — 99 ≡ 25 ∈ SA ───────────────────────────────────────────────

assert 99 % P == 25 and 25 in SA
assert 100 % P == 26 and 26 in IC             # 100 ≡ map multiplier
assert (100 - 1) % P == 25                    # 99 ≡ multiplier - identity

# ── Lemma 110.3 — 8 multiples of 99 mod 37 ───────────────────────────────────

expected = [25, 13, 1, 26, 14, 2, 27, 15]
for k, r in enumerate(expected, 1):
    assert (99 * k) % P == r, f"k={k}: expected {r}, got {(99*k)%P}"
assert expected[0] in SA                   # k=1 → SA
assert expected[1] in CB and expected[1] in PR  # k=2 → CB
assert expected[2] in IC                   # k=3 → identity
assert expected[3] in IC                   # k=4 → multiplier
assert expected[5] in PR                   # k=6 → PR
assert expected[6] in ORBIT_11             # k=7 → ORBIT_11
assert expected[7] in PR                   # k=8 → PR

# ── Lemma 110.4 — Staircase ──────────────────────────────────────────────────

staircase = [5, 7, 9, 11, 13, 15, 17]
assert staircase[3] == 11 and 11 in ORBIT_11   # center in ORBIT_11

for i in range(3):
    s = staircase[i] + staircase[6 - i]
    assert s == 22 and 22 in BASIN_Y and 22 in PR

total = sum(staircase)
assert total == 77
assert total % P == 3 and 3 in ST
assert dr(total) == 5 and 5 in PR

# Three twin prime lower elements
def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    return all(n % i != 0 for i in range(3, int(n**0.5) + 1, 2))

assert is_prime(5) and is_prime(7)   # (5,7) twin prime
assert is_prime(11) and is_prime(13) # (11,13) twin prime
assert is_prime(17) and is_prime(19) # (17,19) twin prime
# lower elements in staircase
assert 5 in staircase and 11 in staircase and 17 in staircase

# ── Lemma 110.5 — 123+321 = 444 = 12×37 ─────────────────────────────────────

assert 123 + 321 == 444
assert 444 % P == 0 and 444 // P == 12
assert 12 in ST

# ── Lemma 110.6 — Permutations of {1,2,3} ────────────────────────────────────

from itertools import permutations as _perms
perm_nums = [100*a + 10*b + c for a, b, c in _perms([1, 2, 3])]
assert all(sum(int(d) for d in str(n)) == 6 for n in perm_nums)

# Three reversal pairs
pair_diffs = {(123, 321): 198, (132, 231): 99, (213, 312): 99}
for (a, b), expected_diff in pair_diffs.items():
    assert abs(a - b) == expected_diff
assert 198 % P == 13 and 13 in CB
assert  99 % P == 25 and 25 in SA

assert (123 + 321) % P == 0             # SEAM
assert (132 + 231) % P == 30 and 30 in SA and 30 in ST   # SA∩ST
assert (213 + 312) % P == 7  and 7  in D7_ORBIT           # D7

# ── Lemma 110.7 — Three digit families ───────────────────────────────────────

f_odd   = [1, 5, 7]
f_pow2  = [2, 4, 8]
f_trin  = [3, 6, 9]

assert sum(f_odd)  == 13 and 13 in CB and 13 in PR
assert sum(f_pow2) == 14
assert sum(f_trin) == 18 and 18 in SEED_ORBIT and 18 in PR

prod_odd  = 1 * 5 * 7
prod_pow2 = 2 * 4 * 8
prod_trin = 3 * 6 * 9

assert prod_odd  % P == 35 and 35 in BASIN_Y and 35 in PR   # forbidden twin prime residue
assert prod_pow2 % P == 27 and 27 in ORBIT_11
assert prod_trin % P == 14                                    # unclassified

# {1,5,7} and {3,6,9} connect to CB and SEED_ORBIT (same classes as seed 24)
assert 24 in CB and 24 in SEED_ORBIT
assert 13 in CB      # {1,5,7} sum → CB
assert 18 in SEED_ORBIT  # {3,6,9} sum → SEED_ORBIT

# ── Lemma 110.8 — DR of n×4 permutation ─────────────────────────────────────

from math import gcd
assert gcd(4, 9) == 1
dr_4n = [dr(4 * n) for n in range(1, 10)]
assert sorted(dr_4n) == list(range(1, 10))   # all 9 DRs covered

# ord of 4 mod 9: 4^1=4, 4^2=16→7, 4^3=64→1 mod 9
assert pow(4, 1, 9) == 4
assert pow(4, 2, 9) == 7
assert pow(4, 3, 9) == 1   # order 3 in Z/9Z (matching ord₃₇(26)=3)

# ── Corollary 110.9 — The 99 descent ────────────────────────────────────────

assert (99*1)%P == 25 and 25 in SA
assert (99*2)%P == 13 and 13 in CB
assert (99*3)%P ==  1 and  1 in IC
assert (99*4)%P == 26 and 26 in IC   # the 137-map multiplier

# ── Corollary 110.10 — Staircase spacing ────────────────────────────────────

twin_lower = [5, 11, 17]
for i in range(len(twin_lower) - 1):
    assert twin_lower[i+1] - twin_lower[i] == 6   # spacing = 6 = Fermat period (Thm 106)


if __name__ == "__main__":
    print("THEOREM 110 — Mirror Reversal of 3-Digit Numbers in GF(37)")
    print("=" * 68)
    print()

    print("I. Reversal constant")
    print("-" * 50)
    print(f"   ABC - CBA = 99(A-C)  [middle digit cancels]")
    print(f"   99 mod 37 = {99%P}  {fw(25)}")
    print(f"   99 = 100 - 1 = {100%P}(IC/multiplier) - 1(identity)  mod 37")
    print()

    print("II. A=1 series — mirror pairs")
    print("-" * 50)
    pairs_data = [
        (123,321),(132,231),(143,341),(154,451),
        (165,561),(176,671),(187,781),(198,891),(119,911)
    ]
    for n, rev in pairs_data:
        diff = abs(n-rev)
        k = diff//99
        inner = n % 100
        ds = (inner//10)+(inner%10)
        print(f"   {n}-{rev}: |diff|=99×{k}  mod37={(diff)%P}{fw(diff%P)}  inner={inner} dsum={ds}")
    print()

    print("III. Staircase {5,7,9,11,13,15,17}")
    print("-" * 50)
    for i in range(3):
        a, b = staircase[i], staircase[6-i]
        print(f"   {a} + {b} = 22  {fw(22)}")
    print(f"   center: 11  {fw(11)}")
    print(f"   sum 77 ≡ 3(mod 37){fw(3)}, DR={dr(77)}{fw(5)}")
    print(f"   twin prime lower elements: 5→(5,7), 11→(11,13), 17→(17,19)  [spacing 6]")
    print()

    print("IV. First mirror sum: 444 = 12×37")
    print("-" * 50)
    print(f"   123+321=444=12×37.  12∈ST: {12 in ST}")
    print(f"   132+231=363≡30{fw(30)}.  30∈SA∩ST: {30 in SA and 30 in ST}")
    print(f"   213+312=525≡7{fw(7)}.   7∈D7: {7 in D7_ORBIT}")
    print()

    print("V. Three digit families")
    print("-" * 50)
    for name, fam, s, p in [
        ("{1,5,7}", f_odd,  sum(f_odd),  prod_odd),
        ("{2,4,8}", f_pow2, sum(f_pow2), prod_pow2),
        ("{3,6,9}", f_trin, sum(f_trin), prod_trin),
    ]:
        print(f"   {name}: sum={s}{fw(s%P if s<P else s%P)}  prod mod37={p%P}{fw(p%P)}")
    print()

    print("VI. 99 descent: SA → CB → identity → multiplier")
    print("-" * 50)
    for k in range(1, 5):
        r = (99*k) % P
        print(f"   99×{k} = {99*k:4d} ≡ {r:2d} {fw(r)}")
    print()

    print("VII. DR of n×4: full permutation of {1..9}")
    print("-" * 50)
    print(f"   n:  {list(range(1,10))}")
    print(f"   DR: {dr_4n}")
    print(f"   ord₉(4) = 3  (4³≡1 mod 9, same as ord₃₇(26)=3)")
    print()
    print("All assertions passed.")
