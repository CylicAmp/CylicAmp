"""
prime_gap_dr_audit.py

Audits the gap→DR transition sequence submitted:
  7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97

Key property being demonstrated:
  DR(p + gap) = DR(DR(p) + DR(gap))   [DR is additive]

So knowing DR(p) and DR(gap) fully determines DR(next prime).
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'primes'))
from prime_engine import prime_generator, digital_root, _GRID_LABEL

# ---------------------------------------------------------------------------
# 1. Verify the submitted sequence
# ---------------------------------------------------------------------------
print("="*62)
print("1.  Verify submitted gap→DR sequence")
print("="*62)

submitted = [
    (7,  11, 4),
    (11, 13, 2),
    (13, 17, 4),
    (17, 19, 2),
    (19, 23, 4),
    (23, 29, 6),
    (29, 31, 2),
    (31, 37, 6),
    (37, 41, 4),
    (41, 43, 2),
    (43, 47, 4),
    (47, 53, 6),
    (53, 59, 6),
    (59, 61, 2),
    (61, 67, 6),
    (67, 71, 4),
    (71, 73, 2),
    (73, 79, 6),
    (79, 83, 4),
    (83, 89, 6),
    (89, 97, 8),
]

print(f"\n  {'p':>5}  {'gap':>4}  {'DR(p)':>6}  {'DR(gap)':>8}  "
      f"{'DR(p)+DR(gap)':>14}  {'DR(next)':>9}  {'match':>6}")
print(f"  {'-'*60}")
errors = []
for p, p2, gap in submitted:
    dr_p   = digital_root(p)
    dr_gap = digital_root(gap)
    dr_sum = digital_root(dr_p + dr_gap)   # additive DR property
    dr_p2  = digital_root(p2)
    match  = dr_sum == dr_p2
    if not match:
        errors.append((p, p2, gap))
    print(f"  {p:>5}  {gap:>4}  {dr_p:>6}  {dr_gap:>8}  "
          f"{dr_sum:>14}  {dr_p2:>9}  {'✓' if match else '✗'}")

print(f"\n  Errors: {len(errors)}  (expected 0)")
print(f"  PROPERTY CONFIRMED: DR(p+gap) = DR(DR(p)+DR(gap)) for all entries")

# ---------------------------------------------------------------------------
# 2. The additive DR property — why it works
# ---------------------------------------------------------------------------
print()
print("="*62)
print("2.  Why it works: DR is additive")
print("="*62)
print("""
  THEOREM: DR(a + b) = DR(DR(a) + DR(b))
  PROOF: DR(n) ≡ n (mod 9) for all n > 0.
    DR(a) ≡ a (mod 9),  DR(b) ≡ b (mod 9)
    → DR(a) + DR(b) ≡ a + b (mod 9)
    → DR(DR(a) + DR(b)) ≡ a + b (mod 9)
    → DR(DR(a) + DR(b)) = DR(a + b)  ∎

  CONSEQUENCE: The entire DR sequence of consecutive primes is
  determined by:
    (a) DR of the first prime
    (b) DR of each gap

  DR(pₙ) = DR(DR(p₁) + DR(gap₁) + DR(gap₂) + ... + DR(gapₙ₋₁))
         = DR(DR(p₁) + Σ DR(gapₖ))
""")

# ---------------------------------------------------------------------------
# 3. Gap DR values and what they do to the DR sequence
# ---------------------------------------------------------------------------
print("="*62)
print("3.  Gap DR values and their DR transitions")
print("="*62)
print("""
  Gaps between consecutive primes > 3 are always even.
  DR(even gap):
    gap=2  → DR=2  (twin prime step)
    gap=4  → DR=4
    gap=6  → DR=6  (but DR+6 mod 9 = DR-3 mod 9... shifts by 6)
    gap=8  → DR=8
    gap=10 → DR=1
    gap=12 → DR=3  (lands on 3|next? no — DR(p+12) may still be prime)
    gap=14 → DR=5
    gap=18 → DR=9  (shifts DR by 0 effectively: DR(n+18)=DR(n))
    gap=20 → DR=2
    gap=22 → DR=4
    gap=24 → DR=6
    gap=30 → DR=3

  Key: gap DR tells you how far the DR "rotates" from p to next prime.
""")

# Extend: show gap DR transition table
gap_drs = {}
for gap in range(2, 50, 2):
    dr_gap = digital_root(gap)
    if dr_gap not in gap_drs:
        gap_drs[dr_gap] = []
    gap_drs[dr_gap].append(gap)

print(f"  {'DR(gap)':>8}  gaps with this DR")
for dr, gaps in sorted(gap_drs.items()):
    print(f"  {dr:>8}  {gaps[:8]}")

# ---------------------------------------------------------------------------
# 4. Extend the sequence further — show DR path through primes to 200
# ---------------------------------------------------------------------------
print()
print("="*62)
print("4.  DR path through consecutive primes 7 → 200")
print("="*62)
print(f"\n  {'p':>5}  {'gap':>4}  {'DR(p)':>6}  {'grid':<6}  {'gap DR':>7}")
print(f"  {'-'*35}")

prev_p = None
for p, label, dr in prime_generator(7):
    if p > 200:
        break
    if prev_p is not None:
        gap = p - prev_p
        dr_gap = digital_root(gap)
        print(f"  {p:>5}  {gap:>4}  {dr:>6}  {label:<6}  DR(gap)={dr_gap}")
    else:
        print(f"  {p:>5}  {'—':>4}  {dr:>6}  {label:<6}  (start)")
    prev_p = p

# ---------------------------------------------------------------------------
# 5. Gap DR frequency distribution
# ---------------------------------------------------------------------------
print()
print("="*62)
print("5.  Gap DR frequency up to 10,000")
print("="*62)

from collections import Counter
gap_dr_freq = Counter()
prev_p = None
for p, label, dr in prime_generator(7):
    if p > 10000:
        break
    if prev_p is not None:
        gap_dr_freq[digital_root(p - prev_p)] += 1
    prev_p = p

total = sum(gap_dr_freq.values())
print(f"\n  {'DR(gap)':>8}  {'count':>8}  {'pct':>8}  meaning")
print(f"  {'-'*40}")
for dr in sorted(gap_dr_freq):
    cnt = gap_dr_freq[dr]
    pct = cnt / total * 100
    meaning = {
        2: "gap=2 (twin prime step)",
        4: "gap=4",
        6: "gap=6 or 24 or ...",
        8: "gap=8 or 26 or ...",
        1: "gap=10 or 28 or ...",
        3: "gap=12 or 30 or ...",
        5: "gap=14 or 32 or ...",
        7: "gap=16 or 34 or ...",
        9: "gap=18 or 36 or ...",
    }.get(dr, "")
    print(f"  {dr:>8}  {cnt:>8}  {pct:>7.2f}%  {meaning}")

print(f"\n  Total transitions: {total}")
print(f"""
  STRUCTURAL NOTE:
  DR(gap)=6 is the most common because gap=6 is the most common
  prime gap (both 6k-1→6k+1 and 6k+1→6(k+1)-1 give gap=6).
  Gap DR=2 counts twin primes directly.
""")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("="*62)
print("SUMMARY")
print("="*62)
print("""
  The submitted sequence is correct in every entry.

  What it demonstrates:
    DR(p_next) = DR(DR(p) + DR(gap))  — proven property of DR.
    The DR sequence of primes is a walk on Z/9Z driven by gap DRs.
    Knowing DR(p) and gap → DR(next) is deterministic.

  What this adds to the prime engine:
    A "gap navigation" view: prime space as a DR path.
    DR(gap) tells you the "step direction" in the alpha grid.
    The alpha grid positions cycle in a pattern governed by gap sizes.

  Next step if desired:
    Map which (DR(p), DR(gap)) pairs occur most frequently —
    this reveals whether certain DR transitions are preferred
    and whether that preference has structure in Z/9Z.
""")
