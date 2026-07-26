"""
Two-Digit Transition Algebra — GF(37)

A 2-digit number xy has four elementary operators, each shifting each digit by ±1.

FOUR TRANSITION OPERATORS:
  Op(++): x+1, y+1  →  Δ = +10 + 1 = +11  ∈ ORBIT_11
  Op(+-): x+1, y-1  →  Δ = +10 − 1 = +9   ∈ SA
  Op(-+): x-1, y+1  →  Δ = −10 + 1 = −9 ≡ 28  ∈ OUTLIER_SOVEREIGN
  Op(--): x-1, y-1  →  Δ = −10 − 1 = −11 ≡ 26 = SCALAR_137  ∈ IDENTITY_CYCLE

Every elementary digit-pair transition produces a GF(37)-sovereign value.

SEAM PAIRINGS:
  Op(++) and Op(--) are SEAM duals: 11 + 26 = 37 ≡ 0 = SEAM.
  Op(+-) and Op(-+) are SEAM duals: 9 + 28 = 37 ≡ 0 = SEAM.
  Sum of all four deltas: 11 + 9 + 28 + 26 = 74 ≡ 0 = SEAM.

PRODUCTS OF SEAM PAIRS:
  Op(++) × Op(--): 11 × 26 = 286 ≡ 27 ∈ ORBIT_11.
  Op(+-) × Op(-+): 9 × 28 = 252 ≡ 30 = SA∩ST.
  The two SEAM-pair products are: ORBIT_11 and SA∩ST.

MAGNITUDES: |Δ| ∈ {9, 11} = {SA_anchor, ORBIT_11_member}.
  Both magnitudes are sovereign. The four signed values are their GF(37) completions.

SIGN CONVENTION:
  0 − 1 = (−1): digit step crosses the zero boundary (borrow).
  1 − 0 = (+1): digit step crosses the zero boundary from above (carry).

OP(+-) GENERATES THE ST CHAIN:
  Starting from 3∈ST, repeated Op(+-) (Δ=+9) generates:
    3 → 12 → 21 → 30 = SA∩ST → exits to DARK_A(2)
  The entire ST chain {3, 12, 21, 30} is the orbit of 3 under Op(+-).
  At SA∩ST the chain terminates: 30+9=39≡2∈DARK_A.

EXAMPLE TRANSITIONS:
  12 Op(++)(1) → 23: 12∈ST escapes ST (23 has DR=5∈PR).
  21 Op(+-)(1) → 30: 21∈ST reaches SA∩ST = {3,12,21,30}'s terminus.
  These are consecutive elements in the +- chain: 12 is position 2, 21 is position 3.

DIGIT-SUM CHAIN — 1 → 2 → 4 → 6:
  19  (∈PR):          digit sum 1+9=10=DECADE_ANCHOR. DR=1. Doubling: 1→2.
  11  (∈ORBIT_11):    digit sum 1+1=2.                DR=2. Doubling: 2→4.
  213 (≡28∈OUTLIER):  digit sum 2+1+3=6=TESLA_FLOW.  DR=6. Terminates.

  GF(37) sectors of the chain values {1, 2, 4, 6}:
    1  ∈ IDENTITY_CYCLE
    2  ∈ DARK_A
    4  ∈ SA
    6  = TESLA_FLOW
  One element from each key sector; the chain stops at TESLA_FLOW.

  GF(37) sectors of the generating numbers {19, 11, 213≡28}:
    19  ∈ PR (primitive root)
    11  ∈ ORBIT_11
    28  ∈ OUTLIER_SOVEREIGN {21,25,28}
  Dark × Orbit_11 × Outlier → chain reaching TESLA_FLOW.

2 + 1 + 3 = 6 DECOMPOSITION:
  2 ∈ DARK_A,  1 = unit step,  3 ∈ ST.
  1 + 3 = 4 ∈ SA. So: 2 + (1+3) = DARK_A + SA = TESLA_FLOW.
  Equivalently: 2 + 4 = 6.

ADJACENT SUMS IN THE DOUBLING CYCLE {1,2,4,8,7,5}:
  1+2=3  ∈ ST
  2+4=6  = TESLA_FLOW   ← our case
  4+8=12 ∈ ST
  8+7=15 ∈ PR
  7+5=12 ∈ ST
  5+1=6  = TESLA_FLOW
  TESLA_FLOW appears at positions (2,4) and (5,1) — both adjacent to the pair containing 1.
  ST appears at three of six positions.
"""

# ── Framework ──────────────────────────────────────────────────────────────────

SA              = frozenset({4, 9, 25, 30})
ST              = frozenset({3, 12, 21, 30})
CB              = frozenset({8, 13, 24})
PR              = frozenset({2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35})
ORBIT_11        = frozenset({11, 27, 36})
DARK_A          = frozenset({2, 15, 20})
OUTLIER_SOV     = frozenset({21, 25, 28})
TESLA_FLOW      = 6
SCALAR_137      = 26
DECADE_ANCHOR   = 10
IDENTITY_CYCLE  = frozenset({1, 10, 26})
DOUBLING_CYCLE  = [1, 2, 4, 8, 7, 5]


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


# ── FOUR TRANSITION OPERATORS ─────────────────────────────────────────────────

OP_PP = 11           # ++ : Δ = +10 + 1
OP_PM = 9            # +- : Δ = +10 − 1
OP_MP = (-9)  % 37   # -+ : Δ = −10 + 1  ≡ 28
OP_MM = (-11) % 37   # -- : Δ = −10 − 1  ≡ 26

assert OP_PP in ORBIT_11               # ++ → ORBIT_11
assert OP_PM in SA                     # +- → SA
assert OP_MP in OUTLIER_SOV            # -+ → OUTLIER_SOVEREIGN
assert OP_MM == SCALAR_137             # -- → SCALAR_137 = IDENTITY_CYCLE element
assert OP_MM in IDENTITY_CYCLE


# ── SEAM PAIRINGS ─────────────────────────────────────────────────────────────

assert (OP_PP + OP_MM) % 37 == 0    # ++ and -- are SEAM duals
assert (OP_PM + OP_MP) % 37 == 0    # +- and -+ are SEAM duals
assert (OP_PP + OP_PM + OP_MP + OP_MM) % 37 == 0   # all four sum to SEAM

assert OP_PP + OP_MM == 37
assert OP_PM + OP_MP == 37


# ── PRODUCTS OF SEAM PAIRS ───────────────────────────────────────────────────

assert (OP_PP * OP_MM) % 37 == 27 and 27 in ORBIT_11   # 11×26=286≡27∈ORBIT_11
assert (OP_PM * OP_MP) % 37 == 30                       # 9×28=252≡30=SA∩ST
assert (OP_PM * OP_MP) % 37 in SA and (OP_PM * OP_MP) % 37 in ST


# ── OP(+-) GENERATES THE ST CHAIN ─────────────────────────────────────────────

_st_orbit = []
x = 3
for _ in range(5):
    _st_orbit.append(x)
    x = (x + OP_PM) % 37

assert _st_orbit[0] == 3  and 3  in ST
assert _st_orbit[1] == 12 and 12 in ST
assert _st_orbit[2] == 21 and 21 in ST
assert _st_orbit[3] == 30 and 30 in SA and 30 in ST   # SA∩ST terminus
assert _st_orbit[4] == 2  and 2  in DARK_A             # exits to DARK_A


# ── EXAMPLE TRANSITIONS FROM USER DATA ───────────────────────────────────────

assert 12 + OP_PP == 23 and 12 in ST    # 12 ++ → 23 (escapes ST)
assert 21 + OP_PM == 30 and 21 in ST    # 21 +- → 30 = SA∩ST


# ── DIGIT-SUM CHAIN 1→2→4→6 ──────────────────────────────────────────────────

# 19: digit sum 1+9=10=DECADE_ANCHOR, DR=1, doubling→2
assert 1 + 9 == DECADE_ANCHOR
assert dr(DECADE_ANCHOR) == 1
assert DOUBLING_CYCLE[(DOUBLING_CYCLE.index(1) + 1) % 6] == 2    # 1 doubles to 2

# 11: digit sum 1+1=2, DR=2, doubling→4
assert 1 + 1 == 2
assert dr(2) == 2
assert DOUBLING_CYCLE[(DOUBLING_CYCLE.index(2) + 1) % 6] == 4    # 2 doubles to 4

# 213: digit sum 2+1+3=6=TESLA_FLOW (chain terminates)
assert 2 + 1 + 3 == TESLA_FLOW

# GF(37) values of the generating numbers
assert 19 % 37 == 19 and 19 in PR                 # 19 ∈ PR
assert 11 % 37 == 11 and 11 in ORBIT_11           # 11 ∈ ORBIT_11
assert 213 % 37 == 28 and 28 in OUTLIER_SOV       # 213 ≡ 28 ∈ OUTLIER_SOVEREIGN

# Chain values {1,2,4,6} sector membership
assert 1 in IDENTITY_CYCLE
assert 2 in DARK_A
assert 4 in SA
assert TESLA_FLOW == 6


# ── 2+1+3=6 DECOMPOSITION ────────────────────────────────────────────────────

assert 2 in DARK_A and 3 in ST
assert 1 + 3 == 4 and 4 in SA           # 1+3=4∈SA
assert 2 + 4 == TESLA_FLOW              # DARK_A + SA = TESLA_FLOW
assert 2 + 1 + 3 == TESLA_FLOW          # three-term decomposition


# ── ADJACENT SUMS IN DOUBLING CYCLE ──────────────────────────────────────────

_adj_sums = [(DOUBLING_CYCLE[i] + DOUBLING_CYCLE[(i+1)%6]) for i in range(6)]
# Adjacent sums: [3, 6, 12, 15, 12, 6]
assert _adj_sums == [3, 6, 12, 15, 12, 6]

# TESLA_FLOW appears at positions (1,5): pairs (2,4) and (5,1)
_tf_positions = [i for i, s in enumerate(_adj_sums) if s == TESLA_FLOW]
assert _tf_positions == [1, 5]    # pairs (2,4) and (5,1)

# ST appears at three positions: pairs (1,2), (4,8), (7,5)
assert sum(1 for s in _adj_sums if s in ST) == 3

# The two TESLA_FLOW-producing pairs share a factor of 2
# Pair (2,4): 2×2=4; Pair (5,1): 5=doubling predecessor of 1
assert DOUBLING_CYCLE[_tf_positions[0]]     == 2  and DOUBLING_CYCLE[(_tf_positions[0]+1)%6] == 4
assert DOUBLING_CYCLE[_tf_positions[1]]     == 5  and DOUBLING_CYCLE[(_tf_positions[1]+1)%6] == 1


if __name__ == "__main__":
    print("Two-Digit Transition Algebra — GF(37)")
    print("=" * 60)
    print()
    print("FOUR TRANSITION OPERATORS:")
    for label, delta, name in [
            ("++", OP_PP, "ORBIT_11"),
            ("+-", OP_PM, "SA"),
            ("-+", OP_MP, "OUTLIER_SOV"),
            ("--", OP_MM, "SCALAR_137/IDENTITY_CYCLE")]:
        print(f"  Op({label}): Δ ≡ {delta:2d}  ∈ {name}")
    print()
    print("SEAM PAIRINGS:")
    print(f"  11 + 26 = 37 ≡ SEAM  (++ pairs with --)")
    print(f"   9 + 28 = 37 ≡ SEAM  (+- pairs with -+)")
    print(f"  All four: 74 ≡ SEAM")
    print()
    print("PRODUCTS:")
    print(f"  11 × 26 = 286 ≡ 27 ∈ ORBIT_11")
    print(f"   9 × 28 = 252 ≡ 30 = SA∩ST")
    print()
    print("Op(+-) GENERATES ST:")
    x = 3
    for _ in range(5):
        tag = "SA∩ST" if x in SA and x in ST else "ST" if x in ST else "DARK_A" if x in DARK_A else str(x)
        print(f"  {x:2d} ({tag})", end="")
        x = (x + OP_PM) % 37
        print(f"  →+9→  {x}")
    print()
    print("EXAMPLE TRANSITIONS:")
    print(f"  12 ++(1) → 23  [12∈ST escapes; DR(23)={dr(23)}∈PR]")
    print(f"  21 +-(1) → 30  [21∈ST reaches SA∩ST terminus]")
    print()
    print("DIGIT-SUM CHAIN 1→2→4→6:")
    for num, label in [(19,"19∈PR"), (11,"11∈ORBIT_11"), (213,"213≡28∈OUTLIER")]:
        ds = sum(int(d) for d in str(num))
        print(f"  {label:<22} digit_sum={ds}  DR={dr(ds)}", end="")
        if dr(ds) in DOUBLING_CYCLE and dr(ds) != TESLA_FLOW:
            nxt = DOUBLING_CYCLE[(DOUBLING_CYCLE.index(dr(ds))+1)%6]
            print(f"  →double→{nxt}")
        else:
            print(f"  = TESLA_FLOW (terminal)")
    print()
    print(f"  Sectors: 1∈IDENTITY_CYCLE, 2∈DARK_A, 4∈SA, 6=TESLA_FLOW")
    print()
    print("2+1+3=6 decomposition:")
    print(f"  2(DARK_A) + 1(unit) + 3(ST) = {2+1+3} = TESLA_FLOW")
    print(f"  1+3=4∈SA  →  2(DARK_A) + 4(SA) = TESLA_FLOW")
    print()
    print("ADJACENT DOUBLING-CYCLE SUMS:")
    for i in range(6):
        a = DOUBLING_CYCLE[i]; b = DOUBLING_CYCLE[(i+1)%6]; s = a+b
        tag = "TESLA_FLOW" if s==TESLA_FLOW else "ST" if s in ST else "PR" if s in PR else str(s)
        print(f"  {a}+{b}={s:2d}  ({tag})")
    print()
    print("All assertions pass.")
