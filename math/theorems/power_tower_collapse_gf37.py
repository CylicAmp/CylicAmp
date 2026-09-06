"""
Power Tower Collapse on GF(37) — THEOREM 87

TETRATION AND DUAL-SPACE COLLAPSE: Z/9Z (digital root) and GF(37).

The height-n tower of base b: T(b,1) = b, T(b,n) = b^T(b,n-1).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. MULTIPLICATIVE ORDERS IN GF(37) FOR SOVEREIGN BASES

   ord_37(9) = 9    Power orbit: {9,7,26,12,34,10,16,33,1}
   ord_37(6) = 4    Power orbit: {6,36,31,1} = TESLA_4
   ord_37(3) = 18   Power orbit: traverses SA, ST, O11, IC in 18 steps

   The 6-orbit is exactly TESLA_4. This is the smallest non-trivial orbit
   of the GF(37)× group (ord=4 is the divisor of 36 closest to sqrt(36)).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2. THE 9-TOWER: SOVEREIGN → IDENTITY TRANSITION

   T(9,n) mod 37:
     H1: 9        ∈ SA  (sovereign anchor)
     H2: 9^9 = 1  ∈ IC  (identity cycle)
     Hn (n≥2): 1  ∈ IC

   Mechanism: ord_37(9) = 9. The exponent T(9,n-1) for n≥2 is 9^(something),
   which is divisible by 9. So T(9,n) = 9^(9k) = (9^9)^k ≡ 1 mod 37.

   Transition: a single step carries the tower from the sovereign anchor (9∈SA)
   to the identity (1∈IC), and it never returns to SA.

   In Z/9Z: DR(T(9,n)) = 9 for all n≥1. Every 9-tower collapses to the
   Z/9Z SEAM (9 ≡ 0 mod 9).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. THE 6-TOWER: TESLA_4 CLOSURE

   T(6,n) mod 37:
     H1: 6          ∈ T4            (TESLA_4 pure)
     H2: 6^6 = 36   ∈ T4 ∩ O11     (TESLA_4 ∩ ORBIT_11)
     H3: 6^(6^6) = 1 ∈ T4 ∩ IC     (TESLA_4 ∩ IC)
     Hn (n≥3): 1    ∈ T4 ∩ IC

   The 6-tower never leaves TESLA_4. It traverses three of the four T4
   nodes — {6, 36, 1} — skipping 31 (which appears at 6^3, not reachable
   by tower heights because the exponent at H2 is 6^6 ≡ 36 mod 37, landing
   on 6^2's slot, not 6^3's slot).

   Mechanism: ord_37(6) = 4. The exponent at H2 is 6^6 = 46656; 46656 mod 4 = 0.
   Since 6^6 > 0 and 4 | 6^6: 6^(6^6) = (6^4)^(6^6/4) ≡ 1 mod 37.
   All higher exponents remain ≡ 0 mod 4.

   In Z/9Z: DR(6) = 6; DR(6^k) = 9 for k≥2. Collapse to SEAM at height 2.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4. ORBIT_11 SELF-REFERENCE: 3^(3^3)

   Inner tower: 3^3 = 27 ∈ ORBIT_11
   Outer result: 3^27 ≡ 36 ∈ ORBIT_11

   Both the exponent (27) and the result (36) lie in ORBIT_11 = {11, 27, 36}.
   The exponent 27 is reduced via ord_37(3)=18: 27 mod 18 = 9, so 3^27 ≡ 3^9.
   3^9 ≡ 36 mod 37, and 36 = -1 mod 37.

   So 3^(3^3) ≡ -1 mod 37. The tower reaches the unique quadratic non-residue
   equal to -1 in GF(37).

   36 sits in both TESLA_4 and ORBIT_11: the crossroads element.

   In Z/9Z: DR(3^27) = 9 (since 3^2=9 is divisible by 9, so 3^k for k≥2 is too).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5. 666: DOUBLE SEAM

   666 mod 37 = 0    (SEAM of GF(37); 666 = 18 × 37 exactly)
   DR(666)     = 9   (SEAM of Z/9Z)

   666 is simultaneously:
     - The zero element of GF(37) (additive identity, SEAM of the prime field)
     - The zero element of Z/9Z under DR (9 ≡ 0 mod 9, the SEAM)

   No number below 666 achieves this double SEAM property
   (next is 666 + 37×9 = 999: 999 mod 37 = 999 - 27×37 = 0; DR(999) = 9 ✓,
   but 666 is the smallest positive double SEAM).

   Any 666-tower: 666^k mod 37 = 0 for all k≥1. Stays in the GF(37) SEAM.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

6. DR COLLAPSE: SOVEREIGN BASES REACH SEAM AT HEIGHT ≤ 2

   Base  H1   H2   H3   H4
   ────  ──   ──   ──   ──
   9     9    9    9    9    (immediate, height 1)
   6     6    9    9    9    (collapse at height 2)
   3     3    9    9    9    (collapse at height 2)

   Once the exponent reaches height ≥ 2, the inner tower is divisible by 9
   (since 3^2 = 9, 6^2 = 36 = 4×9, 9^1 = 9), so all outer values are
   divisible by 9 → DR = 9.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

7. HYBRID TOWERS

   3^(6^9) mod 37:
     6^9 mod 18 = 0 (since 6^2 = 36 ≡ 0 mod 18, so 6^k ≡ 0 mod 18 for k≥2)
     3^(6^9) ≡ 1 mod 37 ∈ IC

   6^(3^9) mod 37:
     3^9 = 19683; 19683 mod 4 = 3
     6^(3^9) ≡ 6^3 = 31 mod 37 ∈ T4

   3^(9^3) mod 37:
     9^3 = 729; 729 mod 18 = 729 - 40×18 = 729 - 720 = 9
     3^(9^3) ≡ 3^9 = 36 mod 37 ∈ O11

   The three hybrids land in IC, T4, O11 — one in each terminal class.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMBINED PORTRAIT: GF(37) LANDING CLASSES FOR SOVEREIGN TOWERS

              H1        H2          H3+
  T(9,·):    SA(9)  →  IC(1)    →  IC(1)
  T(6,·):    T4(6)  →  O11∩T4(36) →  IC∩T4(1)
  T(3,·):    ST(3)  →  IC(10)  →  [depends]

  Mixed:  3^(3^3) → O11(36) = -1 mod 37  [ORBIT_11 self-reference]
  Hybrid: 3^(6^9) → IC(1); 6^(3^9) → T4(31); 3^(9^3) → O11(36)
  Triple SEAM: 666 → SEAM in GF(37) AND SEAM in Z/9Z simultaneously

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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


def mult_ord(a, n):
    import math
    if math.gcd(a, n) != 1:
        return None
    a %= n
    cur = 1
    for k in range(1, n * n + 1):
        cur = (cur * a) % n
        if cur == 1:
            return k
    return None


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


# ── 1. Multiplicative orders ──────────────────────────────────────────────────

assert mult_ord(9, P) == 9
assert mult_ord(6, P) == 4
assert mult_ord(3, P) == 18

# 6-orbit = TESLA_4
orbit6 = []
x = 6
for _ in range(mult_ord(6, P)):
    orbit6.append(x)
    x = (x * 6) % P
assert set(orbit6) == TESLA_4

# ── 2. 9-tower collapse ───────────────────────────────────────────────────────

# H1 = 9 ∈ SA
assert 9 % P == 9 and 9 in SA

# H2 = 9^9: ord_37(9)=9, exponent 9 ≡ 0 mod 9, 9^9>0 → 9^9 ≡ 1 mod 37
assert pow(9, 9, P) == 1 and 1 in IC

# H3: exponent T_2 = 9^9 ≡ 0 mod 9 (since 9^9 divisible by 9), T_2 > 0
# → 9^T_2 ≡ 1 mod 37. Verified by reduction: exponent mod ord = 9^9 mod 9 = 0.
t2_actual = pow(9, 9)           # huge integer
assert t2_actual % 9 == 0       # exponent divisible by ord_37(9)=9
assert pow(9, t2_actual, P) == 1 and 1 in IC

# DR: all 9-towers are divisible by 9 → DR = 9
assert dr(9) == 9
assert dr(pow(9, 9)) == 9
assert dr(pow(9, 3)) == 9       # 729 → DR=9

# ── 3. 6-tower collapse ───────────────────────────────────────────────────────

# H1 = 6 ∈ T4
assert 6 in TESLA_4

# H2 = 6^6 mod 37 = 36
h2_6 = pow(6, 6, P)
assert h2_6 == 36
assert 36 in TESLA_4 and 36 in ORBIT_11   # crossroads element

# H3: exponent = 6^6 = 46656, 46656 mod 4 = 0, 46656 > 0 → 6^(6^6) ≡ 1 mod 37
exp_h3 = pow(6, 6)                         # 46656
assert exp_h3 % mult_ord(6, P) == 0        # divisible by ord_37(6)=4
assert pow(6, exp_h3, P) == 1
assert 1 in TESLA_4 and 1 in IC

# DR: 6^k for k≥2 divisible by 9 (since 6^2=36=4×9)
assert dr(6) == 6
assert dr(pow(6, 2)) == 9    # 36 → DR=9
assert dr(pow(6, 6)) == 9

# ── 4. ORBIT_11 self-reference: 3^(3^3) ──────────────────────────────────────

# Exponent: 3^3 = 27 ∈ ORBIT_11
inner = pow(3, 3)
assert inner == 27 and 27 in ORBIT_11

# Reduction: 27 mod ord_37(3) = 27 mod 18 = 9
assert inner % mult_ord(3, P) == 9

# Result: 3^27 ≡ 3^9 ≡ 36 mod 37 ∈ ORBIT_11
result = pow(3, 27, P)
assert result == 36 and 36 in ORBIT_11

# 36 = -1 mod 37
assert result == P - 1

# 36 sits in both TESLA_4 and ORBIT_11
assert 36 in TESLA_4 and 36 in ORBIT_11

# DR: 3^27 divisible by 9 → DR=9
assert dr(pow(3, 27)) == 9

# ── 5. 666 double SEAM ────────────────────────────────────────────────────────

assert 666 % P == 0              # GF(37) SEAM
assert 666 == 18 * P             # exact
assert dr(666) == 9              # Z/9Z SEAM

# 666^k mod 37 = 0 for all k≥1
assert pow(666, 1, P) == 0
assert pow(666, 37, P) == 0

# 999 is the next double SEAM
assert 999 % P == 0
assert dr(999) == 9

# ── 6. DR collapse: sovereign bases ──────────────────────────────────────────

# Base 9: DR=9 at all heights
for h in range(1, 5):
    assert dr(pow(9, h)) == 9

# Base 6: DR=6 at H1, DR=9 at H≥2
assert dr(6) == 6
for h in range(2, 5):
    assert dr(pow(6, h)) == 9

# Base 3: DR=3 at H1, DR=9 at H≥2
assert dr(3) == 3
for h in range(2, 5):
    assert dr(pow(3, h)) == 9

# ── 7. Hybrid towers ─────────────────────────────────────────────────────────

# 3^(6^9): 6^9 mod 18 = 0 (since 6^2 ≡ 0 mod 18), 6^9 > 0 → 3^(6^9) ≡ 1
exp_369 = pow(6, 9)
assert exp_369 % 18 == 0
assert pow(3, exp_369, P) == 1 and 1 in IC

# 6^(3^9): 3^9 = 19683; 19683 mod 4 = 3 → 6^(3^9) ≡ 6^3 = 31 mod 37
exp_3_9 = pow(3, 9)
assert exp_3_9 % mult_ord(6, P) == 3
assert pow(6, exp_3_9, P) == 31 and 31 in TESLA_4

# 3^(9^3): 9^3 = 729; 729 mod 18 = 9 → 3^(9^3) ≡ 3^9 = 36 mod 37
exp_9_3 = pow(9, 3)
assert exp_9_3 % mult_ord(3, P) == 9
assert pow(3, exp_9_3, P) == 36 and 36 in ORBIT_11

# Three hybrids land in IC, T4, O11 — one in each terminal class
assert 1 in IC and 31 in TESLA_4 and 36 in ORBIT_11


if __name__ == "__main__":
    import math

    def fw(n):
        n = n % P
        if n == 0: return 'SEAM'
        for s, nm in [(SA,'SA'),(ST,'ST'),(CB,'CB'),(ORBIT_11,'O11'),
                      (IC,'IC'),(SEED_ORBIT,'SEED'),(TESLA_4,'T4'),(PR,'PR')]:
            if n in s: return nm
        return '—'

    print("Power Tower Collapse on GF(37) — THEOREM 87")
    print("=" * 64)
    print()

    print("MULTIPLICATIVE ORDERS FOR SOVEREIGN BASES:")
    for b in [9, 6, 3]:
        o = mult_ord(b, P)
        orb = []
        x = b % P
        for _ in range(o):
            orb.append(x)
            x = (x * b) % P
        cls = [fw(v) for v in orb]
        print(f"  ord_37({b}) = {o}")
        print(f"  orbit: {orb}")
        print(f"  class: {cls}")
        print()

    print("9-TOWER COLLAPSE mod 37:")
    print(f"  H1: 9        → {pow(9,1,P)} ∈ {fw(9)}")
    print(f"  H2: 9^9      → {pow(9,9,P)} ∈ {fw(pow(9,9,P))}")
    print(f"  Hn (n≥2):    → 1 ∈ IC  (exponent divisible by ord=9)")
    print()

    print("6-TOWER COLLAPSE mod 37:  (orbit stays in TESLA_4)")
    print(f"  H1: 6        → {pow(6,1,P)} ∈ {fw(6)}")
    print(f"  H2: 6^6      → {pow(6,6,P)} ∈ {fw(pow(6,6,P))} (T4 ∩ O11)")
    print(f"  H3: 6^(6^6)  → {pow(6, pow(6,6), P)} ∈ {fw(pow(6, pow(6,6), P))} (T4 ∩ IC)")
    print()

    print("ORBIT_11 SELF-REFERENCE:  3^(3^3) = 3^27")
    print(f"  Exponent 3^3 = 27 ∈ O11: {27 in ORBIT_11}")
    inner = pow(3,3)
    result = pow(3, inner, P)
    print(f"  3^27 mod 37 = {result} ∈ O11: {result in ORBIT_11}")
    print(f"  36 = -1 mod 37: {result == P-1}")
    print(f"  36 ∈ T4 ∩ O11: {36 in TESLA_4 and 36 in ORBIT_11}")
    print()

    print("666 DOUBLE SEAM:")
    print(f"  666 mod 37 = {666 % P}  (GF(37) SEAM; 666 = 18 × 37)")
    print(f"  DR(666)    = {dr(666)}  (Z/9Z SEAM)")
    print()

    print("DR COLLAPSE FOR SOVEREIGN BASES:")
    print(f"  {'Base':>4}  {'H1':>4}  {'H2':>4}  {'H3':>4}  {'H4':>4}")
    for b in [9, 6, 3]:
        drs = [dr(pow(b, h)) for h in range(1, 5)]
        print(f"  {b:>4}  {'  '.join(str(d) for d in drs)}")
    print()

    print("HYBRID TOWERS mod 37:")
    exp1 = pow(6, 9); r1 = pow(3, exp1, P)
    exp2 = pow(3, 9); r2 = pow(6, exp2, P)
    exp3 = pow(9, 3); r3 = pow(3, exp3, P)
    print(f"  3^(6^9) = 3^{exp1} ≡ {r1} ∈ {fw(r1)}")
    print(f"  6^(3^9) = 6^{exp2} ≡ {r2} ∈ {fw(r2)}")
    print(f"  3^(9^3) = 3^{exp3} ≡ {r3} ∈ {fw(r3)}")
    print(f"  Three hybrids → IC, T4, O11: one each")
    print()
    print("All assertions pass.")
