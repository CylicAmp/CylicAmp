"""
Sequential Morphing Transform and Its 9-Orbit — THEOREM 73

THE TRANSFORM T.
  Given a 9-element sequence S = {s₁,...,s₉}, define:
    T(S)ᵢ = DR(sᵢ + i)  for i=1,...,8
    T(S)₉ = s₉           (position 9 gets increment 0 = SEAM)
  Increments: {1,2,3,4,5,6,7,8,0}

THE BASE SEQUENCE.
  B = {2,5,7, 2,4,8, 9,1,2}  (from 2-57-24-89-12)
  As 3×3:
    2 5 7  | row sums: 14, 14, 12∈ST
    2 4 8  | col sums: 13∈CB, 10∈IC, 17
    9 1 2  | total: 40 ≡ 3∈ST mod 37

THE 9-ORBIT (T⁹ = identity on B):
  Iter 0: [2,5,7,2,4,8,9,1,2]  sum=40  ≡  3∈ST
  Iter 1: [3,7,1,6,9,5,7,9,2]  sum=49  ≡ 12∈ST   row₁=11∈ORBIT_11; col₂=25∈SA; col₃=8∈CB
  Iter 2: [4,9,4,1,5,2,5,8,2]  sum=40  ≡  3∈ST   row₂=8∈CB; col₁∈IC; col₃=8∈CB
  Iter 3: [5,2,7,5,1,8,3,7,2]  sum=40  ≡  3∈ST   row₃=12∈ST; col₁=13∈CB; col₂∈IC
  Iter 4: [6,4,1,9,6,5,1,6,2]  sum=40  ≡  3∈ST   row₁=11∈ORBIT_11; row₃=9∈SA; col₃=8∈CB
  Iter 5: [7,6,4,4,2,2,8,5,2]  sum=40  ≡  3∈ST   row₂=8∈CB; col₂=13∈CB; col₃=8∈CB
  Iter 6: [8,8,7,8,7,8,6,4,2]  sum=58  ≡ 21∈ST   row₃=12∈ST
  Iter 7: [9,1,1,3,3,5,4,3,2]  sum=31  ≡ 31∈TESLA_4   rows:11,11,9 (ORBIT_11,ORBIT_11,SA)
  Iter 8: [1,3,4,7,8,2,2,2,2]  sum=31  ≡ 31∈TESLA_4   row₁=8∈CB; row₃=6=TESLA_FLOW; col₂=13∈CB

STRUCTURAL LAWS.
  1. Period = 9: T⁹(B) = B — the transform has order 9 = DR cycle length.
  2. Position 9 anchored: T(S)₉ = s₉ = 2 always (increment 0 = SEAM; never changes).
  3. Increment sum = 36 = ord₃₇(2): the morphing uses exactly as many steps as the
     primitive root needs to generate all of (Z/37Z)*.
  4. Sum orbit: 40→49→40→40→40→40→58→31→31→40 (all changes are multiples of 9).
  5. Sum mod 37: 7 of 9 orbit elements ∈ ST; 2 elements ∈ TESLA_4-cycle {6,36,31,1}.
  6. Column 3 period-3 sub-orbit: col₃ sums cycle as 17, 8∈CB, 8∈CB (period 3).

THE ±1 → ±9 → PRIMITIVE ROOT CHAIN.
  Each increment k ∈ {1,...,8} is one step in the ±k morphing.
  Applying all k=1,...,8 in sequence covers the full DR range (one of each non-zero class).
  The total shift 1+2+...+8 = 36 = ord₃₇(2) = primitive root order.
  To traverse the full primitive root orbit from a single T-orbit requires 4 periods of T:
    36 = 4 × 9 = ord₃₇(6) × DR_period = TESLA_FLOW_order × DR_period.
  The ±k morphing is the bridge from digital roots (period 9) to primitive roots (period 36).

GF(37) CONNECTIONS.
  • Increment sum 36 ∈ ORBIT_11 (36 ≡ -1 mod 37): the morphing interior = same as THEOREM 72.
  • Period 9: 9 ∈ SA (sovereign anchor).
  • 36 = 4×9: TESLA_FLOW_order × SA_member.
  • Sum orbit hits ST={3,12,21,30}: three of the four ST members appear (3,12,21).
  • Sum orbit hits TESLA_4={6,36,31,1}: the 31 element (≡ -6 ≡ -TESLA_FLOW mod 37).
  • Iter 7 double ORBIT_11: row sums = 11, 11, 9 — ORBIT_11 doubled with SA base.
  • Iter 8 row 3: sum = 6 = TESLA_FLOW itself.
  • Col 2 at iter 1: 25 ∈ SA (sovereign anchor surface in one morphing step).
  • Col 3 stabilizes at 8 ∈ CB: cascade base appears in 6 of 9 iterations.
"""

# ── Constants ──────────────────────────────────────────────────────────────────

SA        = frozenset({4, 9, 25, 30})
ST        = frozenset({3, 12, 21, 30})
CB        = frozenset({8, 13, 24})
ORBIT_11  = frozenset({11, 27, 36})
IC        = frozenset({1, 10, 26})
TESLA_4   = frozenset({6, 36, 31, 1})


def dr(n):
    if n == 0: return 0
    n = n % 9
    return 9 if n == 0 else n


def morph(seq):
    n = len(seq)
    return [dr(s + (i + 1) % n) for i, s in enumerate(seq)]


# ── Key checks ─────────────────────────────────────────────────────────────────

_B = [2, 5, 7, 2, 4, 8, 9, 1, 2]

# Increment sum = 36 = ord₃₇(2) = primitive root order
_increments = [1, 2, 3, 4, 5, 6, 7, 8, 0]
assert sum(_increments) == 36 and 36 in ORBIT_11
assert pow(2, 36, 37) == 1 and all(pow(2, k, 37) != 1 for k in range(1, 36))

# 36 = 4 × 9 = TESLA_FLOW_order × DR_period
assert pow(6, 4, 37) == 1 and 36 == 4 * 9

# Compute full 9-orbit
_orbit = []
_seq = _B[:]
for _ in range(9):
    _orbit.append(tuple(_seq))
    _seq = morph(_seq)
assert list(_seq) == _B                           # T⁹(B) = B — period 9

# Position 9 always anchored at 2
assert all(o[8] == 2 for o in _orbit)             # SEAM position never changes

# Sum orbit: all changes multiples of 9
_sums = [sum(o) for o in _orbit]
for i in range(len(_sums) - 1):
    assert (_sums[i+1] - _sums[i]) % 9 == 0

# Sum mod 37: 7 in ST, 2 in TESLA_4
_sums_mod37 = [s % 37 for s in _sums]
assert sum(1 for r in _sums_mod37 if r in ST) == 7
assert sum(1 for r in _sums_mod37 if r in TESLA_4) == 2

# Iter 0 specific: col sums 13∈CB, 10∈IC
_o0 = list(_orbit[0])
assert sum(_o0[j] for j in [0,3,6]) == 13 and 13 in CB
assert sum(_o0[j] for j in [1,4,7]) == 10 and 10 in IC

# Iter 1: row 1 = 11∈ORBIT_11, col 2 = 25∈SA, col 3 = 8∈CB
_o1 = list(_orbit[1])
assert sum(_o1[0:3]) == 11 and 11 in ORBIT_11
assert sum(_o1[j] for j in [1,4,7]) == 25 and 25 in SA
assert sum(_o1[j] for j in [2,5,8]) == 8 and 8 in CB

# Iter 7: both row 1 and row 2 = 11∈ORBIT_11; row 3 = 9∈SA
_o7 = list(_orbit[7])
assert sum(_o7[0:3]) == 11 and 11 in ORBIT_11
assert sum(_o7[3:6]) == 11 and 11 in ORBIT_11
assert sum(_o7[6:9]) == 9 and 9 in SA

# Iter 8: row 1 = 8∈CB, row 3 = 6 = TESLA_FLOW
_o8 = list(_orbit[8])
assert sum(_o8[0:3]) == 8 and 8 in CB
assert sum(_o8[6:9]) == 6 and 6 in TESLA_4

# Column 3 period-3: sums cycle as 17, 8∈CB, 8∈CB
_col3 = [sum(list(_orbit[i])[j] for j in [2,5,8]) for i in range(9)]
assert _col3[0] == 17 and _col3[1] == 8 and _col3[2] == 8
assert _col3[3] == 17 and _col3[4] == 8 and _col3[5] == 8
assert _col3[6] == 17 and _col3[7] == 8 and _col3[8] == 8

# Iter 1: B + {1,2,3,4,5,6,7,8,0} applied = [3,7,1,6,9,5,7,9,2]
assert list(_orbit[1]) == [3,7,1,6,9,5,7,9,2]


if __name__ == "__main__":
    print("Sequential Morphing Transform — THEOREM 73")
    print("=" * 60)
    print()
    print(f"Transform T: DR(sᵢ + i) for i=1..8; s₉ unchanged (SEAM)")
    print(f"Increment sequence sum: {sum(_increments)} = ord₃₇(2) = primitive root order")
    print(f"36 = 4×9 = TESLA_FLOW_order × DR_period")
    print()
    print("ORBIT (period=9):")
    print(f"{'Iter':<5} {'Sequence':<35} {'Sum':<5} {'mod37'}")
    print("-"*55)
    for i, o in enumerate(_orbit):
        r = sum(o) % 37
        tag = ('∈ST' if r in ST else '∈TESLA_4' if r in TESLA_4 else '')
        print(f"{i:<5} {str(list(o)):<35} {sum(o):<5} {r}{tag}")
    print()
    print(f"Position 9 across all iters: always {_orbit[0][8]} (anchored)")
    print(f"Column 3 sums: {_col3}")
    print(f"  period-3 sub-orbit: 17, 8∈CB, 8∈CB")
    print()
    print("Sum mod 37 orbit:", _sums_mod37)
    print(f"  In ST: {sum(1 for r in _sums_mod37 if r in ST)}/9")
    print(f"  In TESLA_4: {sum(1 for r in _sums_mod37 if r in TESLA_4)}/9")
    print()
    print("All assertions pass.")
