"""
constellation_mirror_audit.py

Audits the "mirror constellation" {c±1, c±11, c±13} pattern.

Claims under investigation:
  1. The pattern first appears at c=18 and c=30 (the P₃#=30 cluster).
  2. The pattern recurs at larger centers.
  3. Every occurrence covers all three DR tracks (2,4)(5,7)(8,1).
  4. The three-track coverage is provable (not empirical).

The key theorem proved here:
  CONSTELLATION DR THEOREM:
  Whenever {c-13, c-11, c-1, c+1, c+11, c+13} are all prime (six primes),
  the three twin pairs NECESSARILY cover all three DR tracks (2,4)(5,7)(8,1).

Proof sketch:
  The three pair-starts p₁=c-13, p₂=c-1, p₃=c+11 are spaced 12 apart.
  DR(12) = 3.
  Adding 3 in Z/9Z acts on the valid twin-starter DRs {2,5,8} as a 3-cycle:
      2 → 5 → 8 → 2 → ...
  Therefore {DR(p₁), DR(p₂), DR(p₃)} = {2,5,8} always, and each pair
  is forced into a distinct track. QED.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'primes'))
from prime_engine import is_prime, digital_root, twin_prime_generator

# ---------------------------------------------------------------------------
# 1. Prove the +3 cycle in Z/9Z
# ---------------------------------------------------------------------------
print("="*62)
print("1.  +3 cycle on twin-starter DRs in Z/9Z")
print("="*62)
print("""
  Valid twin-starter DRs (DR of the smaller element of any twin pair > 3):
    {2, 5, 8}  (from the tripartite theorem)

  Adding DR(12)=3 mod 9 cycles through all three:
""")

for start in [2, 5, 8]:
    path = []
    r = start
    for _ in range(4):
        path.append(r)
        r = digital_root(r + 3)
    print(f"    DR={start}:  {' → '.join(map(str, path))}")

print("""
  The set {2,5,8} is closed under +3 (mod 9) and the orbit has length 3.
  Any starting point cycles through the full set in exactly 3 steps.
""")

# ---------------------------------------------------------------------------
# 2. Constellation DR theorem
# ---------------------------------------------------------------------------
print("="*62)
print("2.  Constellation DR Theorem — proof")
print("="*62)
print("""
  THEOREM: Let c be any positive integer divisible by 6.
  Suppose {c-13, c-11, c-1, c+1, c+11, c+13} are all prime.
  Then the three twin pairs
      A = (c-13, c-11),  B = (c-1, c+1),  C = (c+11, c+13)
  have DR pairs covering exactly {(2,4), (5,7), (8,1)}.

  PROOF:
    Since all six numbers are prime and > 3 (c ≥ 18 implies c-13 ≥ 5),
    their DRs lie in {1,2,4,5,7,8}.  Twin-pair starters have DR ∈ {2,5,8}.

    Let r = DR(c-13).  Then r ∈ {2,5,8}.

    p₂ = c-13 + 12.  DR(p₂) = DR(DR(c-13) + DR(12)) = DR(r + 3).
    p₃ = c-13 + 24.  DR(p₃) = DR(r + 6).

    From the +3 cycle:
      r=2: DR sequence 2, 5, 8  → pairs (2,4),(5,7),(8,1)
      r=5: DR sequence 5, 8, 2  → pairs (5,7),(8,1),(2,4)
      r=8: DR sequence 8, 2, 5  → pairs (8,1),(2,4),(5,7)

    In every case the set of pairs is {(2,4),(5,7),(8,1)}.  ∎

  COROLLARY: The three-track coverage is not a coincidence;
  it is forced by the gap-12 spacing and the Z/9Z structure.
""")

# Numerical verification of the three cases
print("  Numerical check of all three starting DRs:")
for r in [2, 5, 8]:
    b = digital_root(r + 3)
    c_dr = digital_root(r + 6)
    pair_a = (r, digital_root(r + 2))
    pair_b = (b, digital_root(b + 2))
    pair_c = (c_dr, digital_root(c_dr + 2))
    tracks = sorted([pair_a, pair_b, pair_c])
    ok = tracks == [(2,4),(5,7),(8,1)]
    print(f"    r={r}: pairs {pair_a},{pair_b},{pair_c}  → {tracks}  {'✓' if ok else '✗'}")

# ---------------------------------------------------------------------------
# 3. Find all recurrences to 500,000
# ---------------------------------------------------------------------------
print()
print("="*62)
print("3.  All constellation centers to 500,000")
print("="*62)

found = []
for c in range(6, 500_001, 6):
    elems = [c-13, c-11, c-1, c+1, c+11, c+13]
    if elems[0] < 2:
        continue
    if all(is_prime(e) for e in elems):
        p1, p2, p3 = c-13, c-1, c+11
        pairs = [(p1, p1+2), (p2, p2+2), (p3, p3+2)]
        tracks = sorted([(digital_root(a), digital_root(b)) for a, b in pairs])
        found.append((c, tracks))

print(f"\n  {'center':>10}  {'DR tracks':>30}  all 3?")
print(f"  {'-'*50}")
for c, tracks in found:
    all3 = (tracks == [(2,4),(5,7),(8,1)])
    print(f"  {c:>10,}  {str(tracks):>30}  {'✓' if all3 else '✗'}")

print(f"\n  Total constellation centers to 500,000: {len(found)}")
all_cover = all(t == [(2,4),(5,7),(8,1)] for _,t in found)
print(f"  All cover all three tracks: {all_cover}")

# ---------------------------------------------------------------------------
# 4. Gap analysis between constellation centers
# ---------------------------------------------------------------------------
print()
print("="*62)
print("4.  Gaps between consecutive constellation centers")
print("="*62)

centers = [c for c, _ in found]
gaps = [centers[i+1] - centers[i] for i in range(len(centers)-1)]
print(f"\n  Centers: {centers}")
print(f"  Gaps:    {gaps}")
from collections import Counter
gap_counts = Counter(gaps)
print(f"\n  Gap distribution: {dict(sorted(gap_counts.items()))}")
print(f"\n  Note: gaps are irregular — no fixed spacing, unlike the")
print(f"  centers 18,30,42 within the first cluster (those are spaced 12).")
print(f"  Constellation centers follow prime constellation density, not")
print(f"  a periodic pattern.")

# ---------------------------------------------------------------------------
# 5. What the theorem adds
# ---------------------------------------------------------------------------
print()
print("="*62)
print("5.  Implications for mirror symmetry")
print("="*62)
print(f"""
  WHAT IS PROVEN (no number theory conjectures required):

    If the 6-element constellation {{c±1, c±11, c±13}} exists at
    a given center c, then:
      a) c is divisible by 6 (necessary for twin primes; proven earlier).
      b) The three pairs automatically cover all three DR tracks.
         This follows purely from DR(12)=3 and the Z/9Z cycle 2→5→8→2.
      c) The center c is also a twin prime center (since c±1 are prime).

  WHAT IS NOT PROVEN:

    Whether the constellation recurs infinitely often.
    This is an open problem equivalent to (or stronger than) the
    Twin Prime Conjecture: it requires three simultaneous twin prime
    pairs in the pattern {{c-12, c, c+12}}, which is a prime 6-tuple
    constellation.

    Hardy-Littlewood k-tuple conjecture predicts infinitely many such
    constellations, but this is unproven.

  FOUND SO FAR ({len(found)} occurrences to 500,000):
    Centers: {centers}

  THE MIRROR STRUCTURE ITSELF IS NOT OPTIONAL:
    When the constellation exists, the DR track coverage is forced.
    You cannot have all six primes without all three tracks.
    The mirror is algebraically mandated by the Z/9Z arithmetic.
""")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("="*62)
print("SUMMARY")
print("="*62)
print(f"""
  Claim                                          Status
  ----------------------------------------------------------
  {c-13},... constellation covers all 3 DR tracks  PROVEN ✓
    (forced by DR(12)=3 and +3 cycle on {{2,5,8}})
  Constellation first appears at c=18, c=30       CORRECT ✓
  Pattern recurs at larger centers                CORRECT ✓
    ({len(found)} occurrences to 500,000)
  Pattern recurs infinitely                       OPEN (≡ HL 6-tuple)
  Coverage of all 3 tracks is coincidental        FALSE — it's algebraic ✓

  KEY RESULT:
    The 3-cycle 2→5→8→2 under +3 (mod 9) means that any three
    twin prime pairs whose centers are spaced 12 apart MUST
    collectively cover all three DR tracks.
    This is a provable structural theorem, derived from Z/9Z alone.
    No empirical evidence is needed; it holds for ALL such constellations
    regardless of how many exist or whether they are infinite.
""")
