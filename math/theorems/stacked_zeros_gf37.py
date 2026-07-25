"""
Stacked Zeros — Two Zero-Counting Techniques over the 1–9 Grid

Visual: two circles (zeros) stacked vertically over the 3×3 grid of digits 1–9.
Each circle is a zero; the numbers inside it are what the zero contains.

  Row 1: [1, 2, 3]  — inside the top zero
  Row 2: [4, 5, 6]  — the intersection of both zeros; SPLIT AT 4
  Row 3: [7, 8, 9]  — inside the bottom zero

TECHNIQUE 1 — STACKS:
  Count the zeros by stacking them (one on top of another).
  Zero 1 (top) → Zero 2 (bottom). Three elements per zero.
  The split at 4 (SA node) marks where the two circles intersect.
  1, 2, 3 — in the top zero.
  4 — the split: first element of the intersection (4∈SA).
  7, 8, 9 — in the bottom zero.

TECHNIQUE 2 — WHAT FITS INSIDE THE ZERO:
  Each zero is a container. Count what it holds.
  Top zero holds:    {1,2,3} — 3 elements
  Intersection holds: {4,5,6} — 3 elements (split region, 4∈SA first)
  Bottom zero holds: {7,8,9} — 3 elements
  Total: 3+3+3 = 9 = the full Z/9Z set.
  Center element: 5 (A51 balance point, 5∈PR).

MASTER RESULT:
  Every row read as a 3-digit number hits the SAME sovereign target:
    123 mod 37 = 12 ∈ ST
    456 mod 37 = 12 ∈ ST
    789 mod 37 = 12 ∈ ST
  The stacking technique and the interior technique both arrive at ST.

═══════════════════════════════════════════════════════════════

I. TOP ZERO — {1, 2, 3}

  sum  = 6 = TESLA_FLOW  (the only positive integer set where sum=product)
  prod = 6 = TESLA_FLOW
  123 mod 37 = 12 ∈ ST

  This is the 123 generator: 2+1=3, sum=product=6=TESLA_FLOW.
  The top zero contains the entire 123 family.

II. SPLIT AT 4 — intersection {4, 5, 6}

  4 ∈ SA  — the sovereign anchor; first element of the split
  5 = A51 center (balance point of the alpha grid)
  6 = TESLA_FLOW  (also the sum and product of {1,2,3})

  sum  = 15 ∈ PR
  prod = 120 ≡ 9 mod 37 ∈ SA  — product of split row lands on sovereign anchor
  456 mod 37 = 12 ∈ ST

  The split row sum is PR; the split row product (mod 37) is SA.
  4∈SA sits at the boundary — it is both inside the intersection and the
  first element that belongs to neither zero exclusively.

III. BOTTOM ZERO — {7, 8, 9}

  sum  = 24 ∈ CB  (cascade base node)
  prod = 504 ≡ 23 mod 37
  789 mod 37 = 12 ∈ ST

  8 ∈ CB (cascade base), 9 ∈ SA (sovereign anchor), 7 is prime.
  The bottom zero contains one SA node (9) and one CB node (8).

IV. ALL THREE ROWS ≡ 12 ∈ ST

  123 mod 37 = 12 ∈ ST
  456 mod 37 = 12 ∈ ST
  789 mod 37 = 12 ∈ ST

  All three rows, read as 3-digit numbers, land on sovereign target 12.
  The stacking produces a ST invariant across all three zeros.
  DR(12) = 3 = the sovereign target archetype.

V. ROW SUMS ACROSS THE THREE CLASSES

  top    sum =  6 = TESLA_FLOW
  split  sum = 15 ∈ PR
  bottom sum = 24 ∈ CB

  One node from TESLA_FLOW, one from PR, one from CB — no overlap.
  The three stacked zeros span the three primary non-sovereign classes.

VI. THE FULL STACK: 9 ELEMENTS = Z/9Z

  {1,2,3,4,5,6,7,8,9} = Z/9Z* (digital root group)
  Two zeros stack to cover all nine.
  The intersection {4,5,6} is the pivot — 5 is the exact center.
  Stack depth: top zero (3) + intersection (3) + bottom zero (3) = 9.

VII. STACKING POWER OF 10 — THE PARALLEL TECHNIQUE

  The same split-at-4 appears in the power-of-10 stacking:
    10^1 mod 37 = 10  (DECADE_ANCHOR) — 1 zero
    10^2 mod 37 = 26  (SCALAR_137)    — 2 zeros
    10^3 mod 37 =  1  (unity)         — 3 zeros — seam-transparent
    10^4 mod 37 = 10  SPLIT           — 4 zeros — cycle restarts

  ord₃₇(10) = 3: after 3 zeros the stack returns to unity.
  The 4th zero is the split — same split-at-4 as in the circle diagram.
  Both techniques (digit-circle stacking and power-of-10 stacking) split at 4.

═══════════════════════════════════════════════════════════════
"""

CB         = frozenset({8, 13, 24})
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
PR         = frozenset({2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35})
ORBIT_11   = frozenset({11, 27, 36})
TESLA_FLOW = 6


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


# ── I. Top zero {1,2,3} ──────────────────────────────────────────────────────

TOP    = [1, 2, 3]
SPLIT  = [4, 5, 6]
BOTTOM = [7, 8, 9]

assert sum(TOP) == 6 == TESLA_FLOW          # sum = TESLA_FLOW
assert 1*2*3 == 6 == TESLA_FLOW             # product = TESLA_FLOW (unique property)
assert 123 % 37 == 12 and 12 in ST         # 123 ≡ 12 ∈ ST


# ── II. Split at 4 — intersection {4,5,6} ───────────────────────────────────

assert 4 in SA                              # 4 is the sovereign anchor split node
assert 5 in PR                              # 5 = A51 center ∈ PR
assert 6 == TESLA_FLOW                      # 6 = TESLA_FLOW (same as top-zero sum/product)
assert sum(SPLIT) == 15 and 15 in PR        # split sum ∈ PR
assert (4*5*6) % 37 == 9 and 9 in SA       # split product ≡ 9 ∈ SA
assert 456 % 37 == 12 and 12 in ST         # 456 ≡ 12 ∈ ST


# ── III. Bottom zero {7,8,9} ─────────────────────────────────────────────────

assert sum(BOTTOM) == 24 and 24 in CB      # bottom sum ∈ CB
assert 8 in CB                              # 8 is cascade base node
assert 9 in SA                              # 9 is sovereign anchor node
assert 789 % 37 == 12 and 12 in ST         # 789 ≡ 12 ∈ ST


# ── IV. Master result: all three rows ≡ 12 ∈ ST ─────────────────────────────

assert 123 % 37 == 456 % 37 == 789 % 37 == 12   # all three rows hit ST
assert 12 in ST                                   # 12 is sovereign target
assert dr(12) == 3                                # DR(12) = ST archetype


# ── V. Row sums span three classes ───────────────────────────────────────────

assert sum(TOP) == TESLA_FLOW               # top    → TESLA_FLOW
assert sum(SPLIT) in PR                     # split  → PR
assert sum(BOTTOM) in CB                    # bottom → CB


# ── VI. Full stack = Z/9Z ────────────────────────────────────────────────────

full = TOP + SPLIT + BOTTOM
assert sorted(full) == list(range(1, 10))   # covers all 9 digits
assert len(full) == 9                        # = Z/9Z
assert full[4] == 5                         # center element = 5 (A51)


# ── VII. Power-of-10 stacking — same split-at-4 ─────────────────────────────

assert 10**1 % 37 == 10                     # 1 zero  → DECADE_ANCHOR
assert 10**2 % 37 == 26                     # 2 zeros → SCALAR_137
assert 10**3 % 37 == 1                      # 3 zeros → unity (seam-transparent)
assert 10**4 % 37 == 10                     # 4 zeros → SPLIT, cycle restarts
assert pow(10, 3, 37) == 1                  # ord₃₇(10) = 3 confirmed


if __name__ == "__main__":
    print("Stacked Zeros — GF(37)")
    print("=" * 55)
    print()
    print("TECHNIQUE 1 — STACKS (circles stacked vertically):")
    print(f"  Zero 1 (top):    {TOP}  sum={sum(TOP)}=TESLA_FLOW")
    print(f"  Intersection:    {SPLIT}  split starts at 4∈SA")
    print(f"  Zero 2 (bottom): {BOTTOM}  sum={sum(BOTTOM)}∈CB")
    print()
    print("TECHNIQUE 2 — WHAT FITS INSIDE EACH ZERO:")
    print(f"  Inside top zero:    {TOP}  (3 elements; sum=product={TESLA_FLOW}=TESLA_FLOW)")
    print(f"  Inside both zeros:  {SPLIT}  (3 elements; 4∈SA is split node)")
    print(f"  Inside bottom zero: {BOTTOM}  (3 elements; 9∈SA, 8∈CB)")
    print()
    print("MASTER RESULT — all three rows as 3-digit numbers:")
    for n in [123, 456, 789]:
        print(f"  {n} mod 37 = {n%37} ∈ ST")
    print()
    print("ROW SUMS span three classes:")
    print(f"  {sum(TOP):>2} = TESLA_FLOW")
    print(f"  {sum(SPLIT):>2} ∈ PR")
    print(f"  {sum(BOTTOM):>2} ∈ CB")
    print()
    print("POWER-OF-10 STACKING (parallel technique):")
    labels = {10: "DECADE_ANCHOR", 26: "SCALAR_137", 1: "unity (seam-transparent)"}
    for k in range(1, 5):
        r = 10**k % 37
        tag = labels.get(r, "SPLIT — cycle restarts")
        note = " ← SPLIT" if k == 4 else ""
        print(f"  10^{k} ({k} zero{'s' if k>1 else ''}) mod 37 = {r:>2}  {tag}{note}")
    print()
    print("All assertions passed. Everything connects through prime 37.")
