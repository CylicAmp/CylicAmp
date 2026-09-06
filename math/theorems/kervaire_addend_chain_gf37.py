"""
Kervaire Addend Chain — SEAM Landing and Digital Root Structure on GF(37) — THEOREM 83

USER INPUT: Chain [2, 4, 8, 16, 32, 12, 4, 2] → cumulative sum 80.
  First five addends are powers of 2 (2^1, 2^2, 2^3, 2^4, 2^5).
  Last three: 12, 4, 2.

PARTIAL SUMS.
  Step | Addend | Cumsum | Mod 37 | GF(37)
  ─────────────────────────────────────────────
    1  |   2    |    2   |   2    | PR
    2  |   4    |    6   |   6    | TESLA_4 (= TESLA_FLOW)
    3  |   8    |   14   |  14    | — (CB⁻¹: 8×14≡1)
    4  |  16    |   30   |  30    | SA∩ST
    5  |  32    |   62   |  25    | SA
    6  |  12    |   74   |   0    | SEAM  (74 = 2×37)
    7  |   4    |   78   |   4    | SA
    8  |   2    |   80   |   6    | TESLA_4 (= TESLA_FLOW)

KERVAIRE IDENTIFICATION.
  The first five partial sums ARE the first five Kervaire dimensions:
    [2, 6, 14, 30, 62] = {2^j − 2 : j = 2, 3, 4, 5, 6}
  The chain builds the Kervaire sequence by cumulating the first differences:
    2^j − 2^{j-1} = 2^{j-1}, for j = 2,...,6: giving addends 2, 4, 8, 16, 32.

GHOST STEP AT j=7.
  Correct 7th addend: 2^6 = 64 ≡ 27 ∈ ORBIT_11 (would give cumsum 126 ≡ 15 ∈ PR).
  Ghost 7th addend: 12 ∈ ST (cumsum 74 = 2×37 = SEAM).
  Difference: 64 − 12 = 52 ≡ 15 ∈ PR.
  The ghost step uses 12∈ST instead of 64≡27∈ORBIT_11, trading the 6th Kervaire
  dimension (126≡15∈PR) for a direct SEAM landing at the double-prime 2×37.

GHOST TAIL.
  [12, 4, 2]: sum = 18 ∈ SEED_ORBIT.
  The ghost tail sums to the SEED anchor — same as the sum of ALL Kervaire dims mod 37
  (THEOREM 81: ∑dims = 240 ≡ 18 ∈ SEED_ORBIT).
  After the SEAM: +4 → 78 ≡ 4 ∈ SA; then +2 → 80 ≡ 6 = TESLA_FLOW.

OUTER/INNER DECOMPOSITION.
  Outer left:  2 + 4 =  6 = TESLA_FLOW.
  Outer right: 4 + 2 =  6 = TESLA_FLOW.
  Inner: [8, 16, 32, 12]; sum = 68 ≡ 31 ∈ TESLA_4.
  31 + 6 = 37 = PRIME → SEAM.   (PRIME_MIRROR + TESLA_FLOW = PRIME)
  Total: 6 + 68 + 6 = 80 ≡ 6 = TESLA_FLOW.

DIGITAL ROOT (DR) SEQUENCE.
  DR(2) = 2,   DR(6) = 6,  DR(14) = 5,  DR(30) = 3,
  DR(62) = 8,  DR(74) = 2, DR(78) = 6,  DR(80) = 8.
  DR sequence: [2, 6, 5, 3, 8, 2, 6, 8].

  SEAM-MIRROR PROPERTY.
    Step 6 (SEAM landing): DR = 2 = DR at step 1.
    Step 7 (first post-SEAM): DR = 6 = DR at step 2.
    Step 8 (return to TESLA_FLOW): DR = 8 = DR at step 5.
    The SEAM landing mirrors the start of the sequence in digital root.

FIRST FOUR DIGITAL ROOTS: [2, 6, 5, 3].
  These are the DRs of the first four Kervaire dimensions (2, 6, 14, 30).
  Sum:     2 + 6 + 5 + 3 = 16 = 2^4  (the 4th addend in the chain).
  Product: 2 × 6 × 5 × 3 = 180 ≡ 32 ∈ SEED_ORBIT (mod 37).
  GF(37): 2∈PR, 6∈TESLA_4, 5∈PR, 3∈ST.

ALL-DR STATISTICS.
  Sum of all DR:     2+6+5+3+8+2+6+8 = 40 ≡ 3 ∈ ST (mod 37).
  Product of all DR: 2×6×5×3×8×2×6×8 = 138240 ≡ 8 ∈ CB (mod 37).
  [Sum lands in ST; product lands in CB — mirroring the gauge/cascade split.]
"""

# ── Constants ──────────────────────────────────────────────────────────────────

SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
IC         = frozenset({1, 10, 26})
SEED_ORBIT = frozenset({18, 24, 32})
TESLA_4    = frozenset({6, 36, 31, 1})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
P          = 37
TESLA_FLOW = 6

import math

# ── Chain and partial sums ────────────────────────────────────────────────────

ADDENDS  = [2, 4, 8, 16, 32, 12, 4, 2]
PARTIALS = []
s = 0
for a in ADDENDS:
    s += a
    PARTIALS.append(s)

assert PARTIALS == [2, 6, 14, 30, 62, 74, 78, 80]

# Mod 37 residues
MODS = [x % P for x in PARTIALS]
assert MODS == [2, 6, 14, 30, 25, 0, 4, 6]

# ── Kervaire identification ───────────────────────────────────────────────────

KERVAIRE_DIMS = [2**j - 2 for j in range(2, 8)]   # [2, 6, 14, 30, 62, 126]
assert PARTIALS[:5] == KERVAIRE_DIMS[:5]            # first 5 partial sums = Kervaire dims

# First differences of Kervaire dims = powers of 2
_kdiffs = [KERVAIRE_DIMS[i] - KERVAIRE_DIMS[i-1] for i in range(1, 5)]
_kdiffs = [KERVAIRE_DIMS[0]] + _kdiffs   # [2, 4, 8, 16, 32]
assert _kdiffs == ADDENDS[:5]             # Kervaire first diffs = chain prefix

# ── Mod-37 GF(37) membership ───────────────────────────────────────────────

assert MODS[0] == 2 and 2 in PR               # step 1: PR
assert MODS[1] == 6 == TESLA_FLOW and 6 in TESLA_4  # step 2: TESLA_FLOW
# step 3: 14 = CB⁻¹ (8×14≡1 mod 37, from THEOREM 81)
assert MODS[2] == 14 and (8 * 14) % P == 1
assert MODS[3] == 30 and 30 in SA and 30 in ST  # step 4: SA∩ST junction
assert MODS[4] == 25 and 25 in SA               # step 5: SA
assert MODS[5] == 0                              # step 6: SEAM (74 = 2×37)
assert PARTIALS[5] == 2 * P == 74               # explicit double-prime
assert MODS[6] == 4 and 4 in SA                 # step 7: SA
assert MODS[7] == 6 == TESLA_FLOW               # step 8: TESLA_FLOW (closes)

# ── Ghost step ───────────────────────────────────────────────────────────────

# Correct 7th addend: 2^6=64≡27∈ORBIT_11 (would give 6th Kervaire dim 126)
assert pow(2, 6, P) == 27 and 27 in ORBIT_11
assert (62 + 64) == 126 and 126 % P == 15 and 15 in PR  # 6th Kervaire dim

# Ghost: 12∈ST → SEAM
assert ADDENDS[5] == 12 and 12 in ST
assert 62 + 12 == 74 == 2 * P                   # SEAM landing
assert (64 - 12) % P == 15 and 15 in PR         # ghost difference ∈ PR

# ── Ghost tail ───────────────────────────────────────────────────────────────

GHOST_TAIL = ADDENDS[5:]    # [12, 4, 2]
assert GHOST_TAIL == [12, 4, 2]
assert sum(GHOST_TAIL) == 18 and 18 in SEED_ORBIT    # ghost tail sum = SEED
assert sum(KERVAIRE_DIMS) % P == 18                  # matches ∑Kervaire dims (T81)

# ── Outer/inner decomposition ─────────────────────────────────────────────────

outer_L = ADDENDS[0] + ADDENDS[1]     # 2+4=6
outer_R = ADDENDS[-1] + ADDENDS[-2]   # 2+4=6
inner   = ADDENDS[2:-2]               # [8, 16, 32, 12]

assert outer_L == outer_R == TESLA_FLOW               # both outer pairs = TESLA_FLOW
assert sum(inner) == 68 and 68 % P == 31 and 31 in TESLA_4  # inner ≡ PRIME_MIRROR∈T4
assert (68 % P + TESLA_FLOW) == P                     # PRIME_MIRROR + TESLA_FLOW = PRIME
assert sum(ADDENDS) == 80 and 80 % P == TESLA_FLOW    # total ≡ TESLA_FLOW

# ── Digital root sequence ─────────────────────────────────────────────────────

def dr(n):
    while n >= 10:
        n = sum(int(c) for c in str(n))
    return n

DR_SEQ = [dr(ps) for ps in PARTIALS]
assert DR_SEQ == [2, 6, 5, 3, 8, 2, 6, 8]

# SEAM-mirror property
assert DR_SEQ[5] == DR_SEQ[0] == 2    # step 6 (SEAM) mirrors step 1
assert DR_SEQ[6] == DR_SEQ[1] == 6    # step 7 mirrors step 2
assert DR_SEQ[7] == DR_SEQ[4] == 8    # step 8 mirrors step 5

# ── First four DR: [2, 6, 5, 3] ──────────────────────────────────────────────

DR4 = DR_SEQ[:4]
assert DR4 == [2, 6, 5, 3]
assert 2 in PR and 6 in TESLA_4 and 5 in PR and 3 in ST

# Sum of first four DR = 2^4 (the 4th addend)
assert sum(DR4) == 16 == 2**4 == ADDENDS[3]

# Product of first four DR ≡ 32 ∈ SEED_ORBIT
assert math.prod(DR4) == 180 and 180 % P == 32 and 32 in SEED_ORBIT

# ── All-DR statistics ─────────────────────────────────────────────────────────

# Sum of all DR ≡ 3 ∈ ST
assert sum(DR_SEQ) == 40 and 40 % P == 3 and 3 in ST

# Product of all DR ≡ 8 ∈ CB
_prod_dr = math.prod(DR_SEQ)
assert _prod_dr == 138240 and _prod_dr % P == 8 and 8 in CB


if __name__ == "__main__":
    print("Kervaire Addend Chain — SEAM Landing and Digital Root Structure on GF(37) — THEOREM 83")
    print("=" * 80)
    print()
    print("CHAIN: [2, 4, 8, 16, 32, 12, 4, 2] → cumulative sum 80")
    print()

    fw_map = [(SA,'SA'),(ST,'ST'),(CB,'CB'),(ORBIT_11,'O11'),
              (IC,'IC'),(SEED_ORBIT,'SEED'),(TESLA_4,'T4'),(PR,'PR')]
    def fw(n):
        n = n % P
        if n == 0: return 'SEAM'
        for s,nm in fw_map:
            if n in s: return nm
        return '—'

    print(f"{'Step':>4} | {'Addend':>6} | {'CumSum':>6} | {'Mod37':>5} | GF(37)")
    print("-" * 50)
    for i, (a, ps) in enumerate(zip(ADDENDS, PARTIALS)):
        print(f"  {i+1:>2} | {a:>6} | {ps:>6} | {ps%P:>5} | {fw(ps)}")
    print()
    print(f"First 5 partial sums = Kervaire dims {PARTIALS[:5]}")
    print(f"Step 6: 62+12=74=2×37 ≡ 0 = SEAM  [ghost step: 12∈ST, not 64≡27∈ORBIT_11]")
    print(f"Step 7: +4 → 78 ≡ 4 ∈ SA")
    print(f"Step 8: +2 → 80 ≡ 6 = TESLA_FLOW  [return]")
    print()
    print(f"GHOST TAIL [12,4,2] sum = 18 ∈ SEED_ORBIT = ∑Kervaire dims mod 37 (T81)")
    print(f"OUTER PAIRS: 2+4=6=TESLA_FLOW (left), 4+2=6=TESLA_FLOW (right)")
    print(f"INNER [8,16,32,12] sum = 68 ≡ 31 ∈ TESLA_4 (PRIME_MIRROR); 31+6=37=PRIME")
    print()
    print(f"DIGITAL ROOT SEQUENCE: {DR_SEQ}")
    print(f"First four DR: {DR4}")
    print(f"  Sum     = {sum(DR4)} = 2^4 = 4th addend")
    print(f"  Product = {math.prod(DR4)} ≡ {math.prod(DR4)%P} ∈ SEED_ORBIT (mod 37)")
    print(f"SEAM-mirror: DR[step 6]={DR_SEQ[5]}=DR[step 1]; DR[step 7]={DR_SEQ[6]}=DR[step 2]; DR[step 8]={DR_SEQ[7]}=DR[step 5]")
    print()
    print(f"All-DR sum  = 40 ≡ 3 ∈ ST")
    print(f"All-DR prod = 138240 ≡ 8 ∈ CB")
    print()
    print("All assertions pass.")
