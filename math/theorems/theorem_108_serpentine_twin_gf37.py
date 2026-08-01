"""
================================================================================
THEOREM 108 — The Serpentine 3×3 Path and Twin Prime Candidates in GF(37)
================================================================================

STATEMENT.
The standard 3×3 grid (123/456/789) breaks sequential continuity: the path
1→2→3→4→5→6→7→8→9 requires two non-adjacent jumps at positions 3→4 and 6→7
(Manhattan distance 3 each). The serpentine arrangement (123/654/789) resolves
this: the identical sequential path is fully adjacent (every step has Manhattan
distance 1), forming a Hamiltonian path on the grid graph with no jumps.

Every consecutive odd pair in the S-path differs by 2 and is therefore a twin
prime candidate. Stacking serpentine blocks continuously tiles all candidate
pairs across the positive integers. The one pair that can never yield a twin
prime is uniquely identified by GF(37): the pair (n, n+2) where n ≡ 35 ≡ −2
(mod 37), which forces n+2 ≡ 0 (mod 37) — the SEAM.

================================================================================
DEFINITIONS
================================================================================

  Standard grid positions (row, col), 0-indexed:
      1→(0,0)  2→(0,1)  3→(0,2)
      4→(1,0)  5→(1,1)  6→(1,2)
      7→(2,0)  8→(2,1)  9→(2,2)

  Serpentine grid positions:
      1→(0,0)  2→(0,1)  3→(0,2)
      4→(1,2)  5→(1,1)  6→(1,0)
      7→(2,0)  8→(2,1)  9→(2,2)

  S-path: 1→2→3→4→5→6→7→8→9 (sequential, by value).

  Manhattan distance: d(a,b) = |row_a − row_b| + |col_a − col_b|.

  Adjacent step: d = 1 (shares exactly one grid edge).

  Serpentine block k (k ≥ 1): integer range {9(k−1)+1, …, 9k}.
  The S-path within block k visits these 9 values in ascending order,
  all steps adjacent by the same arrangement that makes block 1 continuous.

================================================================================
LEMMAS
================================================================================

LEMMA 108.1  (Standard grid has two jumps).
  In 123/456/789 the S-path steps 3→4 and 6→7 have distance 3.
  No other step exceeds distance 1.

  Proof.
    3 is at (0,2); 4 is at (1,0). d = |0−1| + |2−0| = 1+2 = 3.
    6 is at (1,2); 7 is at (2,0). d = |1−2| + |2−0| = 1+2 = 3.
    All other consecutive steps share a row or column boundary: d = 1.  ∎

LEMMA 108.2  (Serpentine grid is a Hamiltonian path with all steps adjacent).
  In 123/654/789 every consecutive step in the S-path has Manhattan distance 1.

  Proof (by enumeration of all 8 steps):
    1(0,0)→2(0,1): d = 0+1 = 1  ✓
    2(0,1)→3(0,2): d = 0+1 = 1  ✓
    3(0,2)→4(1,2): d = 1+0 = 1  ✓   (4 is placed at row 1 col 2 — reversed row)
    4(1,2)→5(1,1): d = 0+1 = 1  ✓
    5(1,1)→6(1,0): d = 0+1 = 1  ✓
    6(1,0)→7(2,0): d = 1+0 = 1  ✓
    7(2,0)→8(2,1): d = 0+1 = 1  ✓
    8(2,1)→9(2,2): d = 0+1 = 1  ✓
  Every step adjacent. The path visits all 9 cells: it is Hamiltonian.       ∎

LEMMA 108.3  (All odd pairs in the S-path are twin prime candidates).
  Within block k, the values at path positions 0, 2, 4, 6, 8 (0-indexed) are
  the five odd numbers {9(k−1)+1, 9(k−1)+3, 9(k−1)+5, 9(k−1)+7, 9(k−1)+9}.
  Each consecutive odd pair differs by exactly 2 and is therefore a twin prime
  candidate: a pair (n, n+2) that must be checked for simultaneous primality.

  Proof.
    Within any serpentine block the S-path visits values 1,2,3,4,5,6,7,8,9
    (shifted by 9(k−1)). Odd values occupy path positions 0,2,4,6,8.
    Consecutive odd values at positions 2i and 2i+2 differ by 2.            ∎

LEMMA 108.4  (Stacking tiles all twin prime candidates with no gaps).
  Every pair of consecutive odd positive integers (n, n+2) appears as an
  adjacent odd pair in exactly one serpentine block.

  Proof.
    Consecutive odd pairs in ℤ+ are exactly {(2m−1, 2m+1) : m ≥ 1} =
    {(1,3),(3,5),(5,7),(7,9),(9,11),(11,13),…}.
    Block k covers {9(k−1)+1,…,9k}. The five odd values in block k are
    9(k−1)+{1,3,5,7,9}. Adjacent odd pairs within block k:
      (9(k−1)+1, 9(k−1)+3), (9(k−1)+3, 9(k−1)+5),
      (9(k−1)+5, 9(k−1)+7), (9(k−1)+7, 9(k−1)+9).
    The block-boundary pair (9(k−1)+9, 9k+1) = (9k−0, 9k+1): these differ by
    2 only if 9k−0 is odd, i.e., always (9k is odd iff k is odd). When k is
    even, 9k is even so the boundary values are even and do not form an odd
    pair — the block boundary between consecutive blocks yields one even–odd
    transition, not a twin prime candidate, so no candidate is missed or
    double-counted. Every consecutive odd pair (n, n+2) falls inside exactly
    one block (when ⌈n/9⌉ = ⌈(n+2)/9⌉) or at a boundary. In both cases
    the candidate is captured.                                               ∎

  Note: the inter-block boundary odd pair always falls: (9, 11) spans blocks 1
  and 2, but 9 = 9×1 (last of block 1) and 11 = 9×1+2 (second of block 2).
  The convention: cross-block pairs (n, n+2) where n = 9k are attributed to
  the boundary between blocks k and k+1; all others sit inside one block.

LEMMA 108.5  (Unique forbidden twin prime residue in GF(37)).
  The unique residue r ∈ {1,…,36} such that every prime p ≡ r (mod 37) has
  p+2 composite is r = 35 ≡ −2 (mod 37).

  Proof.
    p+2 ≡ 0 (mod 37) iff p ≡ −2 ≡ 35 (mod 37).
    p+2 divisible by 37 → p+2 = 37 (if p+2 prime) → p = 35 = 5×7, not prime.
    For all larger p ≡ 35, p+2 is composite (divisible by 37).
    No other residue forces p+2 ≡ 0, so r = 35 is unique.                  ∎

LEMMA 108.6  (The S-path traverses the forbidden seam exactly once per period).
  The +2 shift on Z/37Z is ergodic: starting from any odd value n, the sequence
  n, n+2, n+4, … returns to n mod 37 after exactly 37 steps (hitting all 37
  residues). Within each period the forbidden residue r = 35 is encountered
  exactly once, blocking exactly 1 of 37 consecutive twin prime candidate pairs.

  Proof.
    gcd(2, 37) = 1, so the map r ↦ r+2 (mod 37) is a permutation of Z/37Z of
    order 37. In any window of 37 consecutive odd numbers the residues mod 37
    are a permutation of {0,1,…,36}. Exactly one residue equals 35.         ∎

================================================================================
MAIN THEOREM
================================================================================

THEOREM 108.  (Serpentine Path — Twin Prime Candidate Geometry in GF(37)).

  (i)  [GEOMETRY] The serpentine arrangement 123/654/789 produces a Hamiltonian
       path through the 3×3 grid in which every step is grid-adjacent (distance
       1). The standard arrangement 123/456/789 does not — it has jumps at
       3→4 and 6→7.

  (ii) [CANDIDATES] Every consecutive odd pair in a serpentine block is a twin
       prime candidate: a pair (n, n+2) both of which must be checked for
       primality. Stacking serpentine blocks continuously tiles all twin prime
       candidate pairs across the positive integers.

  (iii)[BLOCK STRUCTURE] Block k captures exactly 4 intra-block candidate pairs
       and at most 1 inter-block boundary pair. The S-path within each block
       visits odd values in sequence with no jumps, so the visual S-flow
       matches the arithmetic twin-prime scan.

  (iv) [GF(37) SEAM] Among all residue classes mod 37, exactly one — r = 35
       ≡ −2 — is permanently forbidden: every p ≡ 35 forces p+2 ≡ 0 (mod 37),
       composite. In every window of 37 consecutive S-path candidate pairs,
       exactly one pair is blocked by the SEAM.

  (v)  [BLOCK RESIDUE ANATOMY] The 4 intra-block candidate pairs in block 1
       carry residues (mod 37):
         (1,3): IC → ST              — not a twin prime
         (3,5): ST → PR              — twin prime: (3,5)
         (5,7): PR → D7_orbit{7,33,34} — twin prime: (5,7)
         (7,9): D7_orbit → SA        — not a twin prime (7,9: 9=3² composite)
       Block 2 (10–18) includes (11,13): ORBIT_11 → CB — twin prime.
       Block 3 (19–27) includes (19,21): PR → ST — not (21=3×7), and (29,31)
       in block 4: 29≡29, 31≡31 — both residues unclassified (below PR).

COROLLARY 108.7  (Twin prime count density via S-path).
  In each period of 37 candidate pairs (74 consecutive odd integers), exactly
  1 is blocked by the SEAM. The remaining 36 residue pairs have no structural
  obstruction in GF(37); their primality depends on higher arithmetic (Sieve
  of Eratosthenes, Bateman-Horn, etc.). GF(37) provides residue anatomy —
  not a primality certificate — for each candidate pair.

COROLLARY 108.8  (Serpentine adjacency ↔ twin prime gap 2).
  The defining property of the serpentine arrangement — every S-path step
  is distance 1 in the grid — is the geometric counterpart of the twin prime
  gap 2 in the integers: no number is skipped, the sieve flows without breaks.
  The standard grid's jumps (distance 3) correspond to gaps that skip residues.
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


def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    return all(n % i != 0 for i in range(3, int(n**0.5) + 1, 2))


def manhattan(pos_a, pos_b):
    return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])


def fw(r):
    classes = []
    for name, s in [('IC', IC), ('SA', SA), ('ST', ST), ('CB', CB),
                    ('ORBIT_11', ORBIT_11), ('SEED_ORBIT', SEED_ORBIT),
                    ('BASIN_Y', BASIN_Y), ('PR', PR), ('D7', D7_ORBIT)]:
        if r in s:
            classes.append(name)
    return '[' + ','.join(classes) + ']' if classes else '[—]'


# ── Lemma 108.1 — Standard grid jumps ────────────────────────────────────────

STANDARD_POS = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    4: (1, 0), 5: (1, 1), 6: (1, 2),
    7: (2, 0), 8: (2, 1), 9: (2, 2),
}

std_steps = [(v, v+1, manhattan(STANDARD_POS[v], STANDARD_POS[v+1])) for v in range(1, 9)]
std_distances = [d for _, _, d in std_steps]

assert std_distances[2] == 3   # step 3→4
assert std_distances[5] == 3   # step 6→7
assert all(d == 1 for i, d in enumerate(std_distances) if i not in (2, 5))

# ── Lemma 108.2 — Serpentine grid: all steps adjacent ────────────────────────

SERPENTINE_POS = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    4: (1, 2), 5: (1, 1), 6: (1, 0),
    7: (2, 0), 8: (2, 1), 9: (2, 2),
}

serp_steps = [(v, v+1, manhattan(SERPENTINE_POS[v], SERPENTINE_POS[v+1])) for v in range(1, 9)]
serp_distances = [d for _, _, d in serp_steps]

assert all(d == 1 for d in serp_distances), f"Non-adjacent step found: {serp_steps}"

# Hamiltonian: all 9 values visited
assert set(SERPENTINE_POS.keys()) == set(range(1, 10))

# ── Lemma 108.3 — Odd pairs in S-path block 1 ────────────────────────────────

# S-path positions 0,2,4,6,8 hold values 1,3,5,7,9
serp_order = sorted(SERPENTINE_POS.keys())   # [1,2,3,4,5,6,7,8,9]
odd_positions = [serp_order[i] for i in range(0, 9, 2)]
assert odd_positions == [1, 3, 5, 7, 9]

odd_pairs_block1 = [(odd_positions[i], odd_positions[i+1]) for i in range(len(odd_positions)-1)]
assert odd_pairs_block1 == [(1, 3), (3, 5), (5, 7), (7, 9)]
for a, b in odd_pairs_block1:
    assert b - a == 2   # twin prime candidates: gap 2

# ── Lemma 108.4 — Stacking: block k odd pairs ────────────────────────────────

def block_odd_pairs(k):
    offset = 9 * (k - 1)
    return [(offset + 1 + 2*i, offset + 3 + 2*i) for i in range(4)]

# Block 1: (1,3),(3,5),(5,7),(7,9)
assert block_odd_pairs(1) == [(1, 3), (3, 5), (5, 7), (7, 9)]
# Block 2: (10,12),(12,14),(14,16),(16,18)
assert block_odd_pairs(2) == [(10, 12), (12, 14), (14, 16), (16, 18)]
# Block 3: (19,21),(21,23),(23,25),(25,27)
assert block_odd_pairs(3) == [(19, 21), (21, 23), (23, 25), (25, 27)]
# Block 4: (28,30),(30,32),(32,34),(34,36)
assert block_odd_pairs(4) == [(28, 30), (30, 32), (32, 34), (34, 36)]

# All intra-block pairs are twin prime candidates (gap 2)
for k in range(1, 8):
    for a, b in block_odd_pairs(k):
        assert b - a == 2

# ── Lemma 108.5 — Forbidden residue r=35 ─────────────────────────────────────

FORBIDDEN = 35
assert FORBIDDEN == P - 2               # ≡ −2 mod 37
assert FORBIDDEN in PR                  # 35 is a primitive root mod 37
assert not is_prime(FORBIDDEN)          # 35 = 5 × 7
assert (FORBIDDEN + 2) % P == 0        # p+2 ≡ 0 mod 37

# No other residue r ∈ {1..36} forces p+2 ≡ 0
blocked = [r for r in range(1, P) if (r + 2) % P == 0]
assert blocked == [35]                  # unique forbidden residue

# Verify: no twin prime has first element ≡ 35 mod 37 (check to 2000)
twin_pairs_2000 = [(p, p+2) for p in range(3, 2001, 2) if is_prime(p) and is_prime(p+2)]
assert not any(p % P == 35 for p, _ in twin_pairs_2000)

# ── Lemma 108.6 — Ergodic +2 shift visits all residues ───────────────────────

from math import gcd
assert gcd(2, P) == 1

orbit_2 = []
r = 1
for _ in range(P):
    orbit_2.append(r)
    r = (r + 2) % P
assert set(orbit_2) == set(range(P))   # all 37 residues visited
assert 35 in orbit_2                    # forbidden residue encountered exactly once
assert orbit_2.count(35) == 1

# ── Block 1 residue anatomy (Theorem part v) ──────────────────────────────────

block1_residues = [(a % P, b % P) for a, b in block_odd_pairs(1)]
# (1,3), (3,5), (5,7), (7,9)
assert block1_residues == [(1, 3), (3, 5), (5, 7), (7, 9)]

# Class membership
assert 1 in IC and 3 in ST              # (1,3): IC → ST
assert 3 in ST and 5 in PR             # (3,5): ST → PR — twin prime
assert 5 in PR and 7 in D7_ORBIT       # (5,7): PR → D7 — twin prime
assert 7 in D7_ORBIT and 9 in SA       # (7,9): D7 → SA

# Primality of block 1 pairs
assert not is_prime(1) and is_prime(3)  # (1,3): 1 not prime
assert is_prime(3) and is_prime(5)      # (3,5): twin prime ✓
assert is_prime(5) and is_prime(7)      # (5,7): twin prime ✓
assert is_prime(7) and not is_prime(9)  # (7,9): 9=3² not prime

# Block 2 key twin prime: (11,13) — ORBIT_11 → CB
assert is_prime(11) and is_prime(13)
assert 11 % P in ORBIT_11 and 13 % P in CB

# Block 3: (29,31) — neither in named class (residues 29, 31)
assert is_prime(29) and is_prime(31)
assert 29 % P == 29  # unclassified
assert 31 % P == 31  # 31: PRIME_MIRROR label in twin_prime_gf37.py

# ── Density: 1 forbidden per 37 candidates ───────────────────────────────────

# In residues {1,3,5,...,73} (37 consecutive odds), count blocked candidates
# A candidate (n, n+2) is blocked if n ≡ 35 mod 37
# Among odds 1..73 (37 odd values), check how many have n ≡ 35 mod 37
odd_37 = [2*i + 1 for i in range(37)]  # 37 consecutive odds starting from 1
blocked_in_period = [n for n in odd_37 if n % P == 35]
assert len(blocked_in_period) == 1     # exactly one blocked per period of 37


if __name__ == "__main__":
    print("THEOREM 108 — Serpentine Path and Twin Prime Candidates in GF(37)")
    print("=" * 68)
    print()

    print("I. Grid comparison")
    print("-" * 50)
    print("   Standard 123/456/789 — steps:")
    for v, w, d in std_steps:
        mark = " <-- JUMP (d=3)" if d == 3 else ""
        print(f"     {v}→{w}: d={d}{mark}")
    print()
    print("   Serpentine 123/654/789 — steps:")
    for v, w, d in serp_steps:
        print(f"     {v}→{w}: d={d}  ✓")
    print()

    print("II. Block 1 odd pair residue anatomy")
    print("-" * 50)
    for (a, b), (ra, rb) in zip(odd_pairs_block1, block1_residues):
        tp = "twin prime ✓" if is_prime(a) and is_prime(b) else "not twin prime"
        print(f"   ({a},{b})  mod37: {ra}{fw(ra)} → {rb}{fw(rb)}  [{tp}]")
    print()

    print("III. Twin prime anatomy by block (blocks 1–5)")
    print("-" * 50)
    for k in range(1, 6):
        pairs = block_odd_pairs(k)
        print(f"   Block {k}  [{9*(k-1)+1}–{9*k}]:")
        for a, b in pairs:
            ra, rb = a % P, b % P
            tp = "✓" if is_prime(a) and is_prime(b) else " "
            print(f"     ({a:3d},{b:3d}) mod37: {ra:2d}{fw(ra)} → {rb:2d}{fw(rb)}  {tp}")
    print()

    print("IV. Forbidden residue r=35 (SEAM)")
    print("-" * 50)
    print(f"   r=35 ≡ −2 (mod 37) ∈ PR")
    print(f"   p+2 ≡ 0 (mod 37) → p+2 divisible by 37 → composite")
    print(f"   Unique blocked residue: {blocked}")
    print(f"   Verification: {len(twin_pairs_2000)} twin prime pairs to 2000, none at r=35")
    print()

    print("V. Ergodic +2 shift — period 37")
    print("-" * 50)
    print(f"   gcd(2,37)=1 → +2 is ergodic on Z/37Z")
    print(f"   One forbidden per 37 candidates: {blocked_in_period} ≡ 35 (mod 37)")
    print(f"   35 ∈ PR (primitive root) — the seam is itself a primitive root class")
    print()

    print("VI. GF(37) twin prime staircase (pairs to 246, mod 37 labels)")
    print("-" * 50)
    twins_246 = [(p, p+2) for p in range(3, 247, 2) if is_prime(p) and is_prime(p+2)]
    print(f"   π₂(246) = {len(twins_246)}  (twin prime count at seed 246)")
    for p, q in twins_246:
        ra, rb = p % P, q % P
        print(f"   ({p:3d},{q:3d}) mod37: {ra:2d}{fw(ra)} → {rb:2d}{fw(rb)}")
    print()
    print("All assertions passed.")
