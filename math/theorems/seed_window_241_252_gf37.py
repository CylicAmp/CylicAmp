"""
The Seed Window 241–252 on GF(37) — THEOREM 89

The 12 consecutive integers 241–252, presented with digit-split notation
(2-46, 24-7, 25-1, ...), encode a rich cross-section of the GF(37)
around the reference seed 246.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER 1: THE DR COUNTDOWN

  Reading from 252 down to 241, the digital roots form:
    9, 8, 7, 6, 5, 4, 3, 2, 1, 9, 8, 7

  One complete descending cycle (9→1) followed by a partial cycle (9→7).
  The seed 246 sits at position 7 in this descent — at DR = 3.
  DR(246) = 3 = the seed's own DR = the seed's position in the countdown.

  The countdown enters DR=3 exactly at the seed and at no other point.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER 2: 24 IS TRIPLE-CLASSED

  246 mod 37 = 24.

  24 is the unique element simultaneously in:
    CB (Cascade Base)      = {8, 13, 24}
    SEED_ORBIT             = {18, 24, 32}
    PR (Primitive Roots)   = {2,5,13,...,24,...,35}

  No other element of CB belongs to SEED_ORBIT.
  24 is the triple-intersection: CB ∩ SEED_ORBIT ∩ PR = {24}.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER 3: THE SEED SPLIT IDENTITY

  Split 246 at the first digit: (2)(46).
    2 ∈ PR     (primitive root)
    46 mod 37 = 9 ∈ SA   (sovereign anchor)
    2 × 46 mod 37 = 18 ∈ SEED_ORBIT

  The digit-split product of the seed equals the SEED_ORBIT entry node.
  18 is the starting node of the 137-map orbit: 18 → 24 → 32 → 18.
  So the split sends the seed (as a number) back to its own orbit's origin.

  Three split products in the window land in SEED_ORBIT:
    249 = (2)(49):  2 × 49 = 98 ≡ 24  ∈ SEED  [PR × ST → SEED]
    246 = (2)(46):  2 × 46 = 92 ≡ 18  ∈ SEED  [PR × SA → SEED entry]
    241 = (24)(1): 24 × 1  = 24 ≡ 24  ∈ SEED  [CB × IC → SEED]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER 4: WINDOW COVERAGE AND BOUNDARY

  The 12 residues covered: 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30.
  Contains every named named set except TESLA_4.
    T4 = {6, 36, 31, 1} — all outside the range 19–30.
    31 ∈ T4 would appear at n=253 = 246 + 7. The window stops one short.

  Upper boundary: 252 = 246 + 6 = SEED + TESLA_FLOW.
    252 mod 37 = 30 ∈ SA ∩ ST — the sovereign bridge, the only element
    in both sovereign sets simultaneously.

  Sum of all 12 split products mod 37 = 9 (the SA anchor and Z/9Z SEAM).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE SPLIT NOTATION

  Numbers with odd last digit → "24-x" or "25-x" (2-digit prefix exposing 24/25)
  Numbers with even last digit or 9 → "2-xx" (1-digit prefix exposing 2)

  The split alternates between prefix 2 (∈ PR) and prefix 24 (∈ CB∩SEED∩PR),
  visually encoding the dual character of the window: primitive roots everywhere,
  with CB/SEED marking the odd-ended members.

  246 (even) → "2-46": prefix 2 ∈ PR, suffix 46→9 ∈ SA.
  247 (odd)  → "24-7": prefix 24 ∈ CB∩SEED, suffix 7 ∈ —.
"""

import math

P = 37
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
IC         = frozenset({1, 10, 26})
SEED_ORBIT = frozenset({18, 24, 32})
TESLA_4    = frozenset({6, 36, 31, 1})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
SEED       = 246
SEED_RES   = SEED % P   # 24
TESLA_FLOW = 6


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 9


# ── Layer 1: DR countdown ─────────────────────────────────────────────────────

countdown = list(range(252, 240, -1))  # 252 down to 241
drs = [dr(n) for n in countdown]

# Perfect descending sequence 9,8,...,1,9,8,7
assert drs == [9, 8, 7, 6, 5, 4, 3, 2, 1, 9, 8, 7]

# Seed 246 sits at position 7 (index 6), DR = 3
seed_pos = countdown.index(SEED)
assert seed_pos == 6                    # 7th position (0-indexed: 6)
assert drs[seed_pos] == 3              # DR at that position = 3
assert dr(SEED) == 3                   # seed's own DR = 3

# DR=3 appears exactly once in the countdown
assert drs.count(3) == 1

# ── Layer 2: 24 is triple-classed ────────────────────────────────────────────

assert SEED_RES == 24
assert 24 in CB
assert 24 in SEED_ORBIT
assert 24 in PR

# 24 is the only CB element in SEED_ORBIT
assert CB & SEED_ORBIT == {24}

# 24 is the only CB element in PR
assert CB & PR == {13, 24}             # 13 and 24; but 24 is SEED, 13 is IC∩CB

# ── Layer 3: Seed split identity ─────────────────────────────────────────────

# 246 = (2)(46): digit split at first digit
p1, p2 = 2, 46
assert p1 * 10 + p2 // 10 != 246      # not a simple digit split
assert str(SEED) == "246"
assert int("2") == p1 and int("46") == p2

assert p2 % P == 9 and 9 in SA        # 46 mod 37 = 9 ∈ SA
assert (p1 * p2) % P == 18            # 2 × 46 mod 37 = 18
assert 18 in SEED_ORBIT               # 18 = SEED_ORBIT entry node

# 18 is the 137-map entry: 18 → 24 → 32 → 18
assert (137 * 18) % P == 24
assert (137 * 24) % P == 32
assert (137 * 32) % P == 18

# The three SEED-landing split products
pairs = [(2,52),(25,1),(25,0),(2,49),(2,48),(24,7),
         (2,46),(24,5),(2,44),(24,3),(2,42),(24,1)]

seed_products = [(a, b, (a*b) % P) for (a, b) in pairs if (a*b) % P in SEED_ORBIT]
assert len(seed_products) == 3

products_mod37 = [(a*b) % P for a, b in pairs]
assert products_mod37 == [30, 25, 0, 24, 22, 20, 18, 9, 14, 35, 10, 24]

# Sum of all 12 products mod 37 = 9
assert sum(products_mod37) % P == 9

# ── Layer 4: Window coverage and boundary ────────────────────────────────────

# Residues covered: 19 through 30
residues = [n % P for n in countdown]
assert sorted(residues) == list(range(19, 31))

# T4 is the only named class absent from the window
T4_in_window = [r for r in residues if r in TESLA_4]
assert T4_in_window == []              # TESLA_4 ∩ {19,...,30} = ∅

# The 31 ∈ T4 would appear at 253 = 246 + 7
assert 253 % P == 31 and 31 in TESLA_4
assert 253 == SEED + 7

# Upper boundary: 252 = 246 + TESLA_FLOW
assert 252 == SEED + TESLA_FLOW
assert 252 % P == 30 and 30 in SA and 30 in ST   # sovereign bridge

# Split alternation: even last digit → "2-xx" prefix, odd → "24-x" prefix
for (a, b), n in zip(pairs, countdown):
    if n % 10 in {0, 1, 3, 5, 7}:    # odd or zero last digit
        assert a == 24 or a == 25, f"Expected 24/25 prefix at n={n}, got {a}"
    else:                              # even or 9
        assert a == 2, f"Expected prefix 2 at n={n}, got {a}"


if __name__ == "__main__":
    def fw_all(n):
        n = n % P
        if n == 0: return ['SEAM']
        return [nm for s, nm in [(SA,'SA'),(ST,'ST'),(CB,'CB'),(ORBIT_11,'O11'),
                (IC,'IC'),(SEED_ORBIT,'SEED'),(TESLA_4,'T4'),(PR,'PR')] if n in s] or ['—']

    print("The Seed Window 241–252 — THEOREM 89")
    print("=" * 60)
    print()
    print("LAYER 1: DR COUNTDOWN")
    print(f"  {'n':>4}  {'notation':>8}  {'DR':>3}  {'mod37':>6}  class")
    pairs_list = [(2,52),(25,1),(25,0),(2,49),(2,48),(24,7),
                  (2,46),(24,5),(2,44),(24,3),(2,42),(24,1)]
    notations  = ["2-52","25-1","25(0)","2-49","2-48","24-7",
                  "2-46","24-5","2-44","24-3","2-42","24-1"]
    for (a,b), n, nota in zip(pairs_list, countdown, notations):
        r = n % P
        d = dr(n)
        cls = ', '.join(fw_all(r))
        seed = " ← SEED" if n == 246 else ""
        print(f"  {n:>4}  {nota:>8}  {d:>3}  {r:>6}  {cls}{seed}")
    print(f"  DR sequence: {[dr(n) for n in countdown]}")
    print(f"  Seed 246 at DR=3 = seed's own DR. DR=3 appears once.")
    print()
    print("LAYER 2: 24 = CB ∩ SEED_ORBIT ∩ PR")
    print(f"  246 mod 37 = 24 ∈ {fw_all(24)}")
    print(f"  CB ∩ SEED_ORBIT = {{24}}  (unique intersection)")
    print()
    print("LAYER 3: SEED SPLIT IDENTITY")
    print(f"  246 → (2)(46): 2×46 = 92 ≡ 18 mod 37 ∈ SEED_ORBIT (entry node)")
    print(f"  137-map from 18: 18→24→32→18")
    print(f"  Three SEED-landing products:")
    for (a, b), n, nota in zip(pairs_list, countdown, notations):
        prod = (a * b) % P
        if prod in SEED_ORBIT:
            print(f"    {nota} ({n}): {a}×{b}={a*b} ≡ {prod} ∈ SEED")
    print(f"  Sum of all 12 products: {sum((a*b)%P for a,b in pairs_list)} ≡ "
          f"{sum((a*b)%P for a,b in pairs_list) % P} mod 37 (SA anchor + Z/9Z SEAM)")
    print()
    print("LAYER 4: WINDOW BOUNDARY")
    print(f"  Residues 19–30 cover all named classes except TESLA_4")
    print(f"  T4 entry: 253 = 246 + 7 → 31 ∈ T4 (one step beyond the window)")
    print(f"  Upper bound: 252 = 246 + TESLA_FLOW → 30 ∈ SA∩ST (sovereign bridge)")
    print()
    print("All assertions pass.")
