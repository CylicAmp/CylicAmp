"""
Tripling Map and Six-Orbit Cycle — GF(37)

TRIPLING MAP: multiplication by 3 in GF(37)*.

KEY PROPERTIES OF 3:
  ord₃₇(3) = 18.  <3> = QR subgroup of order 18 (elements n with chi(n)=1).
  3 is itself a QR: 3^18 ≡ 1 (mod 37), 3^9 ≡ 36 ≡ −1.
  3^6 ≡ 26 = SCALAR_137.  So ×3^6 = ×26 = the 137-map.
  The 137-map (inner 3-cycles) is the 6th power of the tripling map.

QR SUBGROUP VIA POWERS OF 3:
  3^0 = 1    3^1 = 3    3^2 = 9    3^3 = 27   3^4 = 7    3^5 = 21
  3^6 = 26   3^7 = 4    3^8 = 12   3^9 = 36   3^10= 34   3^11= 28
  3^12= 10   3^13= 30   3^14= 16   3^15= 11   3^16= 33   3^17= 25
  All 18 QR elements, generated in order.

THE SIX-ORBIT CYCLE — QR ORBITS UNDER ×3:
  {3,  4, 30}  ×3→  {9, 12, 16}  ×3→  {11, 27, 36}  ×3→
  {7, 33, 34}  ×3→  {21, 25, 28} ×3→  { 1, 10, 26}  ×3→  {3, 4, 30}

  Step 1: {3,4,30}    = canonical sovereign spiral   (ST→SA→SA∩ST)
  Step 2: {9,12,16}   = second sovereign orbit        (SA,ST + interior)
  Step 3: {11,27,36}  = ORBIT_11                     (negation of IDENTITY_CYCLE)
  Step 4: {7,33,34}   = anti-sovereign               (negation of step 1)
  Step 5: {21,25,28}  = OUTLIER_SOV                  (negation of step 2)
  Step 6: {1,10,26}   = IDENTITY_CYCLE               (order-3 subgroup)

  Negation duality: step k and step k+3 are negation-dual (each pair sums to SEAM×3).
  After 6 steps, 3^6=26=SCALAR_137 maps each orbit to itself (the inner 137-map).

THE SIX-ORBIT CYCLE — NQR ORBITS UNDER ×3:
  {2, 15, 20}  ×3→  { 6,  8, 23}  ×3→  {18, 24, 32}  ×3→
  {17, 22, 35} ×3→  {14, 29, 31}  ×3→  { 5, 13, 19}  ×3→  {2, 15, 20}

  Step 1: {2,15,20}   = DARK_A
  Step 2: {6,8,23}    = TESLA_FLOW orbit (contains TESLA_FLOW=6 and CB-element 8)
  Step 3: {18,24,32}  = SEED_ORBIT (137-orbit of seed 246)
  Step 4: {17,22,35}  = negation-dual of DARK_A
  Step 5: {14,29,31}  = negation-dual of {6,8,23}; contains PRIME_MIRROR=31
  Step 6: {5,13,19}   = negation-dual of SEED_ORBIT

SUM INVARIANT:
  Elements [7, 9, 5, 2, 3, 1, 8, 6, 6] sum to 47 ≡ 10 = DECADE_ANCHOR (mod 37).
  These elements sample the ×3 chain: 1=3^0, 3=3^1, 9=3^2, 7=3^4 (QR chain, steps 1,2,4,6).
  The NQR subset {2,5,8,6,6} covers DARK_A(2), {5,13,19}(5), and three from {6,8,23}.

FIBONACCI–GF(37) INTERSECTIONS:
  F(n) = nth Fibonacci number mod 37.
  F(6)  = 8   ∈ CB = {8, 13, 24}        (Cascade Base)
  F(8)  = 21  ∈ ST = {3, 12, 21, 30}    (Sovereign Target)
  F(12) = 33  ∈ {7, 33, 34}             (anti-sovereign orbit)

THREE-CHAIN (decoded from data stream):
  [1,1,2,8] row  → F(1)=1, F(2)=1, F(3)=2, F(6)=8
             F(3) + F(6)  = 2 + 8 = 10 = DECADE_ANCHOR; DR=1. (IDENTITY_CYCLE member)

  [3,8,1,1] row  → F(4)=3, F(6)=8, F(1)=1, F(2)=1
             F(4) × (F(6) − F(1)×F(2)) = 3 × 7 = 21 ∈ ST; DR=3. (SA_anchor=4∈SA paired)

  [3,8,2,2] row  → F(4)=3, F(6)=8, F(3)=2, F(3)=2
             F(4) × F(6) / F(3)² = 3×8/4 = 6 = TESLA_FLOW.
             Equivalently: SA(4) + DARK_A_min(2) = 6 = TESLA_FLOW.
             +4 ∈ SA; +(1 + DECADE_ANCHOR = 11 ∈ ORBIT_11). [doubly starred: touches SA, ORBIT_11]

F(6)=8 IS THE ANCHOR: all three rows use F(6)=8∈CB to reach DECADE_ANCHOR, ST, TESLA_FLOW.
"""

# ── Constants ──────────────────────────────────────────────────────────────────

SA             = frozenset({4, 9, 25, 30})
ST             = frozenset({3, 12, 21, 30})
CB             = frozenset({8, 13, 24})
ORBIT_11       = frozenset({11, 27, 36})
DARK_A         = frozenset({2, 15, 20})
SEED_ORBIT     = frozenset({18, 24, 32})
OUTLIER_SOV    = frozenset({21, 25, 28})
IDENTITY_CYCLE = frozenset({1, 10, 26})
TESLA_FLOW     = 6
SCALAR_137     = 26
DECADE_ANCHOR  = 10
PRIME_MIRROR   = 31


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def chi(n, p=37):
    n = n % p
    if n == 0: return 0
    return 1 if pow(n, (p - 1) // 2, p) == 1 else -1


def ord37(n):
    n = n % 37
    for k in range(1, 37):
        if pow(n, k, 37) == 1:
            return k


# ── KEY PROPERTIES OF 3 ──────────────────────────────────────────────────────

assert ord37(3) == 18                     # 3 has order 18 in GF(37)*
assert chi(3) == 1                        # 3 is a QR
assert pow(3, 6, 37) == SCALAR_137        # 3^6 = 26 = 137-map multiplier
assert pow(3, 9, 37) == 36               # 3^9 = −1

# <3> is the QR subgroup of order 18
QR_SUBGROUP_3 = frozenset(pow(3, k, 37) for k in range(18))
QR_SUBGROUP   = frozenset(n for n in range(1, 37) if pow(n, 18, 37) == 1)
assert QR_SUBGROUP_3 == QR_SUBGROUP
assert len(QR_SUBGROUP) == 18


# ── QR SIX-ORBIT CYCLE ────────────────────────────────────────────────────────

QR_ORBITS_ORDERED = [
    frozenset({3,  4, 30}),   # step 1: canonical sovereign
    frozenset({9, 12, 16}),   # step 2: second sovereign
    frozenset({11,27, 36}),   # step 3: ORBIT_11
    frozenset({7, 33, 34}),   # step 4: anti-sovereign
    frozenset({21,25, 28}),   # step 5: OUTLIER_SOV
    frozenset({1, 10, 26}),   # step 6: IDENTITY_CYCLE
]

# ×3 maps each orbit to the next
for i in range(6):
    this_orb = QR_ORBITS_ORDERED[i]
    next_orb = QR_ORBITS_ORDERED[(i + 1) % 6]
    assert frozenset((x * 3) % 37 for x in this_orb) == next_orb

# All QR orbits are covered
assert set(frozenset(o) for o in QR_ORBITS_ORDERED) == {
    frozenset({1,10,26}), frozenset({3,4,30}), frozenset({7,33,34}),
    frozenset({9,12,16}), frozenset({11,27,36}), frozenset({21,25,28})
}

# Negation duality: steps k and k+3 are negation-dual
for i in range(3):
    orb_a = QR_ORBITS_ORDERED[i]
    orb_b = QR_ORBITS_ORDERED[i + 3]
    assert frozenset((37 - x) % 37 for x in orb_a) == orb_b


# ── NQR SIX-ORBIT CYCLE ───────────────────────────────────────────────────────

NQR_ORBITS_ORDERED = [
    frozenset({2, 15, 20}),   # step 1: DARK_A
    frozenset({6,  8, 23}),   # step 2: TESLA_FLOW orbit
    frozenset({18,24, 32}),   # step 3: SEED_ORBIT
    frozenset({17,22, 35}),   # step 4: neg-dual of DARK_A
    frozenset({14,29, 31}),   # step 5: neg-dual of TESLA_FLOW orbit; contains PRIME_MIRROR
    frozenset({5, 13, 19}),   # step 6: neg-dual of SEED_ORBIT
]

for i in range(6):
    this_orb = NQR_ORBITS_ORDERED[i]
    next_orb = NQR_ORBITS_ORDERED[(i + 1) % 6]
    assert frozenset((x * 3) % 37 for x in this_orb) == next_orb

# Negation duality in NQR cycle
for i in range(3):
    orb_a = NQR_ORBITS_ORDERED[i]
    orb_b = NQR_ORBITS_ORDERED[i + 3]
    assert frozenset((37 - x) % 37 for x in orb_a) == orb_b

# PRIME_MIRROR in NQR step 5 (negation-dual of TESLA_FLOW orbit)
assert PRIME_MIRROR in NQR_ORBITS_ORDERED[4]


# ── SUM INVARIANT ─────────────────────────────────────────────────────────────

ELEMENTS = [7, 9, 5, 2, 3, 1, 8, 6, 6]
assert sum(ELEMENTS) == 47
assert sum(ELEMENTS) % 37 == DECADE_ANCHOR   # 47 ≡ 10 = DECADE_ANCHOR

# QR elements in ELEMENTS and their 3-power positions
assert 1 in QR_SUBGROUP_3 and pow(3, 0, 37) == 1    # 3^0
assert 3 in QR_SUBGROUP_3 and pow(3, 1, 37) == 3    # 3^1
assert 9 in QR_SUBGROUP_3 and pow(3, 2, 37) == 9    # 3^2
assert 7 in QR_SUBGROUP_3 and pow(3, 4, 37) == 7    # 3^4


# ── FIBONACCI–GF(37) INTERSECTIONS ───────────────────────────────────────────

def fib_mod37(n):
    a, b = 1, 1
    if n == 1 or n == 2: return 1
    for _ in range(n - 2): a, b = b, (a + b) % 37
    return b

assert fib_mod37(6)  == 8  and 8  in CB         # F(6)=8∈CB
assert fib_mod37(8)  == 21 and 21 in ST          # F(8)=21∈ST
assert fib_mod37(12) == 33 and 33 in frozenset({7,33,34})  # F(12)=33 anti-sovereign

# THREE-CHAIN decoded:
assert fib_mod37(3) + fib_mod37(6) == DECADE_ANCHOR   # 2+8=10; DR=1
assert dr(DECADE_ANCHOR) == 1

assert fib_mod37(4) * (fib_mod37(6) - fib_mod37(1) * fib_mod37(2)) == 21  # 3×7=21∈ST
assert 21 in ST and dr(21) == 3
assert 4 in SA   # SA_anchor paired with ST(21) in the canonical orbit

assert fib_mod37(4) * fib_mod37(6) // fib_mod37(3)**2 == TESLA_FLOW  # 3×8//4=6
assert 4 + 2 == TESLA_FLOW   # SA(4) + DARK_A_min(2) = TESLA_FLOW
assert 4 in SA and 2 in DARK_A
assert 1 + DECADE_ANCHOR == 11 and 11 in ORBIT_11   # (1+10=11∈ORBIT_11)


if __name__ == "__main__":
    print("Tripling Map and Six-Orbit Cycle — GF(37)")
    print("=" * 60)
    print(f"\nord₃₇(3) = {ord37(3)}  (generates QR subgroup, order 18)")
    print(f"3^6 = {pow(3,6,37)} = SCALAR_137 = 137-map multiplier")
    print(f"3^9 = {pow(3,9,37)} = −1")
    print()
    print("QR subgroup (powers of 3):")
    print(" ", [pow(3,k,37) for k in range(18)])
    print()
    print("QR SIX-ORBIT CYCLE under ×3:")
    for i, orb in enumerate(QR_ORBITS_ORDERED):
        labels = []
        for x in sorted(orb):
            if x in SA and x in ST: labels.append(f"{x}(SA∩ST)")
            elif x in SA: labels.append(f"{x}(SA)")
            elif x in ST: labels.append(f"{x}(ST)")
            else: labels.append(str(x))
        print(f"  step {i+1}: {{{', '.join(labels)}}}", end="")
        if i < 5: print(" →×3→")
        else: print(" →×3→ [cycle]")
    print()
    print("NQR SIX-ORBIT CYCLE under ×3:")
    for i, orb in enumerate(NQR_ORBITS_ORDERED):
        print(f"  step {i+1}: {sorted(orb)}", end="")
        if i < 5: print(" →×3→")
        else: print(" →×3→ [cycle]")
    print()
    print(f"SUM: {ELEMENTS} → {sum(ELEMENTS)} ≡ {sum(ELEMENTS)%37} = DECADE_ANCHOR")
    print()
    print("FIBONACCI intersections:")
    print(f"  F(6) = 8 ∈ CB   F(8) = 21 ∈ ST   F(12) = 33 ∈ {{7,33,34}}")
    print()
    print("THREE-CHAIN (F(6)=8 as anchor):")
    print(f"  F(3)+F(6) = 2+8 = {fib_mod37(3)+fib_mod37(6)} = DECADE_ANCHOR, DR=1")
    print(f"  F(4)×(F(6)-1) = 3×7 = {fib_mod37(4)*(fib_mod37(6)-1)} ∈ ST, DR=3; 4∈SA")
    print(f"  F(4)×F(6)/F(3)² = 3×8/4 = {fib_mod37(4)*fib_mod37(6)//fib_mod37(3)**2} = TESLA_FLOW")
    print(f"    = SA(4)+DARK_A(2): 4+2={4+2}; +(1+10=11∈ORBIT_11)")
    print()
    print("All assertions pass.")
