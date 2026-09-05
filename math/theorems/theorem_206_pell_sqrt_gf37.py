"""
Theorem 206: Pell Equation, Continued Fractions, and Square Roots in GF(37)
Author: Michael Warren Song (CyclicAmp)

CONTINUED FRACTION OF sqrt(37):
  sqrt(37) = [6; 12, 12, 12, ...] = [6; 12̄]  (period length 1)
  Period element: 12 ∈ ST (sovereign target).
  The SOLE periodic CF term is the ST element 12.
  Period 1 means the continued fraction is as simple as possible.

PELL EQUATION x^2 - 37y^2 = 1:
  Fundamental solution: (73, 12).
  73 mod37 = 36 ≡ -1 (mod 37).
  DR(73) = 1 (head-crash: 7+3=10, 1+0=1).
  12 ∈ ST (the denominator is sovereign).
  Verification: 73^2 - 37×12^2 = 5329 - 5328 = 1.

PELL y-VALUES MOD 37:
  Recurrence mod 37: y_{n+1} = 35y_n - y_{n-1} (since 146 mod37=35).
  [Trace of fundamental unit: 73+73=146≡35 mod37]
  Sovereign hits in Pell y-sequence mod37:
    y_0  = 0   [SEAM]
    y_1  = 12  [ST]   ← fundamental period element
    y_11 = 21  [ST]
    y_12 = 4   [SA]
    y_15 = 32  [SEED]
    y_16 = 30  [SA∩ST]
  All SA_ST_SEED classes appear in the Pell y-values mod37.

FRAMEWORK SQUARE ROOTS IN GF(37):
  For each SA_ST_SEED element v, sqrt(v) = {r : r^2 ≡ v (mod 37)}.
  (SA∪ST elements are QR; SEED elements are NQR — no sqrt exists for SEED.)

  GF(37) elements WITH another SA_ST_SEED element as sqrt:
    sqrt(9)  ∋ 3∈ST    [3^2=9∈SA: T199 squaring ST→SA]
    sqrt(12) ∋ 30∈SA∩ST [30^2=12∈ST: T199 squaring SA∩ST→ST]
    sqrt(21) ∋ 24∈SEED  [24^2=21∈ST: T199 squaring SEED→ST]
    sqrt(25) ∋ 32∈SEED  [32^2=25∈SA: T199 squaring SEED→SA]

  GF(37) elements whose square roots are OUTSIDE SA_ST_SEED:
    sqrt(3)  = {15,22} (both NQR g^7 and g^1)
    sqrt(4)  = {2,35}  (both non-sovereign)
    sqrt(30) = {17,20} (both NQR)

  SEED elements have NO square roots in GF(37) (all are NQR):
    18, 24, 32 ∈ NQR → no sqrt exists in GF(37).

SQRT INVERSE GRAPH — SOVEREIGN CONNECTIONS:
  The squaring map restricted to SA_ST_SEED:
    3(ST)  → 9(SA)      [T199: ST→SA]
    24(SEED)→ 21(ST)    [T199: SEED→ST]
    30(SA∩ST)→ 12(ST)  [T199: SA∩ST→ST]
    32(SEED)→ 25(SA)    [T199: SEED→SA]
  Taking sqrt (inverse): the 4 SA_ST_SEED elements {9,12,21,25} each have
  a SA_ST_SEED square root. The other 7 SA_ST_SEED elements ({3,4,18,24,30,32}
  and the SEAM connection) do not.

PELL PERIOD AND 12:
  12 appears in three independent roles:
    1. y_1 = 12 = fundamental Pell denominator.
    2. CF period: [6; 12̄] — sole period term.
    3. sqrt(12) ∋ 30 ∈ SA∩ST (the doubly-sovereign element is a sqrt of the Pell denominator).
    4. 12 + 25 = 0 (additive inverse; 25∈SA) [T205]
    5. 12 ∈ ST: DR(12) = 3 (ST signature).

73 ≡ -1 MOD 37:
  The Pell fundamental x-value 73 reduces to -1 mod37.
  73 = 2×37 - 1 = 2P - 1.
  This means in GF(37), the fundamental unit 73+12√37 ≡ -1+12√37.
  In the quotient ring GF(37)[X]/(X²-37): X≡0 so unit → -1 ≡ 36 ∈ g^6.
  36 = -1 is the element of order 2 in GF(37)*, sitting in g^6 = {11,27,36}.
"""

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED = {18, 24, 32}
SA_ST_SEED = SA | ST | SEED


def legendre(a, p):
    return pow(a, (p - 1) // 2, p)


def is_sovereign(x):
    x = x % P
    return x in SA or x in ST or x in SEED


def pell_y_mod(n):
    x, y = 1, 0
    for _ in range(n):
        x, y = 73 * x + 37 * 12 * y, 12 * x + 73 * y
    return y % P


def run_assertions():
    # 1. Fundamental Pell solution (73, 12)
    assert 73 ** 2 - 37 * 12 ** 2 == 1
    assert 73 % P == 36  # ≡ -1
    assert 12 in ST

    # 2. CF of sqrt(37) has period 1 with term 12
    # Verify: [6; 12] convergent = 73/12
    assert 6 * 12 + 1 == 73  # convergent numerator
    assert 12 in ST           # period term is ST

    # 3. Pell y-values sovereign hits
    assert pell_y_mod(0) == 0        # SEAM
    assert pell_y_mod(1) == 12 and 12 in ST
    assert pell_y_mod(11) == 21 and 21 in ST
    assert pell_y_mod(12) == 4 and 4 in SA
    assert pell_y_mod(15) == 32 and 32 in SEED
    assert pell_y_mod(16) == 30 and 30 in SA and 30 in ST

    # 4. GF(37) square roots
    # Elements with a SA_ST_SEED sqrt
    assert pow(3, 2, P) == 9 and 9 in SA     # sqrt(9)∋3∈ST
    assert pow(30, 2, P) == 12 and 12 in ST  # sqrt(12)∋30∈SA∩ST
    assert pow(24, 2, P) == 21 and 21 in ST  # sqrt(21)∋24∈SEED
    assert pow(32, 2, P) == 25 and 25 in SA  # sqrt(25)∋32∈SEED

    # 5. SEED elements are NQR — no sqrt in GF(37)
    assert all(legendre(s, P) == P - 1 for s in SEED)

    # 6. sqrt(3), sqrt(4), sqrt(30) have no SA_ST_SEED elements
    for v in [3, 4, 30]:
        roots = [r for r in range(1, P) if pow(r, 2, P) == v]
        assert not any(r in SA_ST_SEED for r in roots), f"sqrt({v})={roots} unexpectedly in SA_ST_SEED"

    # 7. Exactly 4 SA_ST_SEED elements have a SA_ST_SEED sqrt
    fw_with_fw_sqrt = [v for v in sorted(SA_ST_SEED)
                       if any(pow(r, 2, P) == v for r in SA_ST_SEED)]
    assert fw_with_fw_sqrt == [9, 12, 21, 25]

    # 8. Those 4 elements' SA_ST_SEED square roots
    fw_sqrt_map = {v: [r for r in sorted(SA_ST_SEED) if pow(r, 2, P) == v]
                   for v in fw_with_fw_sqrt}
    assert fw_sqrt_map[9] == [3]     # sqrt(9)∋3∈ST
    assert fw_sqrt_map[12] == [30]   # sqrt(12)∋30∈SA∩ST
    assert fw_sqrt_map[21] == [24]   # sqrt(21)∋24∈SEED
    assert fw_sqrt_map[25] == [32]   # sqrt(25)∋32∈SEED

    # 9. 12 appears in three roles: Pell denom, CF period, and 30=sqrt(12)∈SA∩ST
    assert 12 in ST
    assert 6 * 12 + 1 == 73          # Pell convergent
    assert pow(30, 2, P) == 12       # sqrt(12) ∋ 30∈SA∩ST
    assert (12 + 25) % P == 0        # additive inverse pair [T205]

    # 10. 73 ≡ -1 mod37; -1 = 36 has order 2 in GF(37)*
    assert 73 % P == 36
    assert 36 == P - 1  # ≡ -1
    assert pow(36, 2, P) == 1  # order 2

    # 11. Pell recurrence mod37: trace = 146 ≡ 35
    assert (73 + 73) % P == 35  # trace mod37

    # 12. All SA_ST_SEED classes appear in Pell y-values mod37
    pell_sectors = set()
    for n in range(40):
        ym = pell_y_mod(n)
        if ym in SA: pell_sectors.add('SA')
        if ym in ST: pell_sectors.add('ST')
        if ym in SEED: pell_sectors.add('SEED')
        if ym == 0: pell_sectors.add('SEAM')
    assert pell_sectors == {'SA', 'ST', 'SEED', 'SEAM'}

    print("All assertions passed.")
    print(f"GF(37) elements with SA_ST_SEED sqrt: {fw_sqrt_map}")


if __name__ == "__main__":
    run_assertions()
