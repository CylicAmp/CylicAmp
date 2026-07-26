"""
Palindrome Structure in GF(37) — THEOREM 56

GENERAL COEFFICIENT RULE:
  An n-digit palindrome has pairs (position k, position n-1-k) for k < n//2,
  and a center digit if n is odd.

  pair_coeff(k, n) = (10^k + 10^(n-1-k)) mod 37

  The exponents k and n-1-k fall into power classes mod 3:
    class 0: 10^k ≡ 1  (k ≡ 0 mod 3)
    class 1: 10^k ≡ 10  (k ≡ 1 mod 3)
    class 2: 10^k ≡ 26  (k ≡ 2 mod 3)

  RULE: if k and (n-1-k) are in DIFFERENT power classes →
            pair_coeff ∈ ORBIT_11 = {11, 27, 36}
        if k and (n-1-k) are in the SAME power class →
            pair_coeff ∈ DARK_A = {2, 15, 20}

  Center position (n odd, position k=n//2): coeff = 10^k mod 37 ∈ {1, 10, 26}

DARK_A CYCLE: {2, 15, 20}
  2 = 1+1       (class 0 + class 0)
  15 = 10+5≡10+10+10+10+10=... actually: 10+10-1... no: 10^1+10^1=20 nope
  Direct: 10^0+10^0=2, 10^1+10^1=20, 10^2+10^2=52≡15 (mod 37)
  So: same class 0 → 2; same class 1 → 20; same class 2 → 15
  All three: 2+15+20=37≡SEAM (mod 37).
  These are dark (NQR): χ(2)=-1, χ(15)=-1, χ(20)=-1.

PALINDROME COEFFICIENTS BY LENGTH:

  3-digit ABA:
    pair(0,2): classes 0,2 → different → 1+26=27∈ORBIT_11
    center(1):                            10=DECADE_ANCHOR
    ABA ≡ 27A + 10B (mod 37)

  4-digit ABBA:
    pair(0,3): classes 0,0 → same class 0 → 1+1=2∈DARK_A
    pair(1,2): classes 1,2 → different → 10+26=36∈ORBIT_11
    ABBA ≡ 2A + 36B (mod 37)

  5-digit ABCBA:
    pair(0,4): classes 0,1 → different → 1+10=11∈ORBIT_11
    pair(1,3): classes 1,1 → same class 1 → 10+10=20... wait
    Actually n=5: pair(1,3): k=1 class 1, n-1-k=3 class 0 → different → 10+1=11∈ORBIT_11
    center(2): class 2 → 26=SCALAR_137
    ABCBA ≡ 11A + 11B + 26C (mod 37) ≡ 11(A+B) + 26C (mod 37)

  6-digit ABCCBA:
    pair(0,5): k=0 class 0, n-1-k=5 class 2 → different → 1+26=27∈ORBIT_11
    pair(1,4): k=1 class 1, n-1-k=4 class 1 → same class 1 → 10+10=20∈DARK_A
    pair(2,3): k=2 class 2, n-1-k=3 class 0 → different → 26+1=27∈ORBIT_11
    ABCCBA ≡ 27A + 20B + 27C (mod 37) ≡ 27(A+C) + 20B (mod 37)

  7-digit ABCDCBA:
    pair(0,6): k=0 class 0, n-1-k=6 class 0 → same class 0 → 1+1=2∈DARK_A
    pair(1,5): k=1 class 1, n-1-k=5 class 2 → different → 10+26=36∈ORBIT_11
    pair(2,4): k=2 class 2, n-1-k=4 class 1 → different → 26+10=36∈ORBIT_11
    center(3): class 0 → 1
    ABCDCBA ≡ 2A + 36B + 36C + D (mod 37)

  8-digit ABCDDCBA:
    pair(0,7): k=0 class 0, n-1-k=7 class 1 → different → 1+10=11∈ORBIT_11
    pair(1,6): k=1 class 1, n-1-k=6 class 0 → different → 10+1=11∈ORBIT_11
    pair(2,5): k=2 class 2, n-1-k=5 class 2 → same class 2 → 26+26=52≡15∈DARK_A
    pair(3,4): k=3 class 0, n-1-k=4 class 1 → different → 1+10=11∈ORBIT_11
    ABCDDCBA ≡ 11A + 11B + 15C + 11D (mod 37)

SEAM CONDITIONS (palindrome ≡ 0 mod 37):

  ABBA ≡ 2A + 36B ≡ 2A − B (mod 37).
    ≡ 0 iff B ≡ 2A (mod 37). For single digits: (A,B)=(1,2),(2,4),(3,6),(4,8).
    Connection: B=2A invokes the Z/9Z DOUBLING CYCLE (THEOREM 54).

  ABCBA ≡ 11(A+B) + 26C (mod 37).
    ≡ 0 iff 26C ≡ −11(A+B) ≡ 26(A+B) (mod 37) iff C ≡ A+B (mod 37).
    For single digits: C=A+B (exact integer when A+B ≤ 9).
    Connection: C=A+B is the SOVEREIGN STAIRCASE rule (THEOREM 55).

  ABCCBA ≡ 27(A+C) + 20B (mod 37).
    ≡ 0 iff 27(A+C) ≡ −20B ≡ 17B (mod 37).
    27 and 17: 27×17=459=12×37+15 ≠ 1; check: 27×11=297≡297-8×37=1. So 27⁻¹=11.
    A+C ≡ 11×17×B = 187B ≡ 187-5×37=2 → A+C ≡ 2B (mod 37).
    For single digits: A+C=2B (B is the average of A and C).

STAIRCASE SEAM PALINDROMES:
  1221:  A=1, B=2=2×1 → SEAM.  (ABBA, B=2A)
  2442:  A=2, B=4=2×2 → SEAM.
  12321: A=1,B=2,C=3=1+2 → SEAM.  (ABCBA, C=A+B)
  123321: A=1,B=2,C=3; A+C=4=2×2=2B → SEAM.  (ABCCBA, A+C=2B)
  These three form a "staircase": 1221, 12321, 123321 each ≡ SEAM.

SQUARED REPUNIT CYCLE:
  R(n) = (10^n − 1)/9 = 111...1 (n ones).
  R(1)²=1; R(2)²=121≡10=DECADE; R(3)²=12321≡0=SEAM.
  Cycle {1, 10, 0} = {IDENTITY_CYCLE_MEMBER, DECADE_ANCHOR, SEAM} with period 3.
  Equivalently: R(n)² mod 37 follows ord₃₇(10)=3 exactly.
  R(n)² = R(n)×R(n): since R(3)≡0 (mod 37), R(3k)≡0 for all k.

  R(1)=1, R(2)=11∈ORBIT_11, R(3)≡0=SEAM.
  R(1)²=1, R(2)²=121≡10, R(3)²=12321≡0.
"""

# ── Framework ──────────────────────────────────────────────────────────────────

SA           = frozenset({4, 9, 25, 30})
ST           = frozenset({3, 12, 21, 30})
CB           = frozenset({8, 13, 24})
PR           = frozenset({2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35})
ORBIT_11     = frozenset({11, 27, 36})
DARK_A       = frozenset({2, 15, 20})   # same-class palindrome coefficients
TESLA_FLOW   = 6
SCALAR_137   = 26
DECADE_ANCHOR = 10


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def chi(n, p=37):
    n = n % p
    if n == 0: return 0
    return 1 if pow(n, (p - 1) // 2, p) == 1 else -1


def pair_coeff(k, n):
    return (pow(10, k, 37) + pow(10, n - 1 - k, 37)) % 37


def power_class(k):
    return k % 3


# ── GENERAL COEFFICIENT RULE ──────────────────────────────────────────────────

# Same-class pairs → DARK_A; different-class pairs → ORBIT_11
for n in range(3, 12):
    for k in range(n // 2):
        c = pair_coeff(k, n)
        if power_class(k) == power_class(n - 1 - k):
            assert c in DARK_A, f"n={n} k={k}: same-class {c} not in DARK_A"
        else:
            assert c in ORBIT_11, f"n={n} k={k}: diff-class {c} not in ORBIT_11"

# Same-class coefficients: class 0→2, class 1→20, class 2→15
assert (pow(10, 0, 37) + pow(10, 0, 37)) % 37 == 2   # 1+1
assert (pow(10, 1, 37) + pow(10, 1, 37)) % 37 == 20  # 10+10
assert (pow(10, 2, 37) + pow(10, 2, 37)) % 37 == 15  # 26+26≡52≡15

# DARK_A triple sum = SEAM
assert 2 + 15 + 20 == 37   # sum = 37 ≡ 0 = SEAM

# DARK_A elements are all dark (NQR)
for d in DARK_A:
    assert chi(d) == -1


# ── SPECIFIC PALINDROME LENGTHS ───────────────────────────────────────────────

# 3-digit ABA: pair(0,2)=27∈ORBIT_11, center=10=DECADE_ANCHOR
assert pair_coeff(0, 3) == 27 and 27 in ORBIT_11
assert pow(10, 1, 37) == DECADE_ANCHOR

for A in range(10):
    for B in range(10):
        aba = A * 100 + B * 10 + A
        assert aba % 37 == (27 * A + DECADE_ANCHOR * B) % 37

# 4-digit ABBA: pair(0,3)=2∈DARK_A, pair(1,2)=36∈ORBIT_11
assert pair_coeff(0, 4) == 2  and 2  in DARK_A
assert pair_coeff(1, 4) == 36 and 36 in ORBIT_11

for A in range(10):
    for B in range(10):
        abba = A * 1000 + B * 100 + B * 10 + A
        assert abba % 37 == (2 * A + 36 * B) % 37

# 5-digit ABCBA: pairs=11,11 both∈ORBIT_11, center=26=SCALAR_137
assert pair_coeff(0, 5) == 11 and 11 in ORBIT_11
assert pair_coeff(1, 5) == 11 and 11 in ORBIT_11
assert pow(10, 2, 37) == SCALAR_137

for A in range(10):
    for B in range(10):
        for C in range(10):
            abcba = A * 10000 + B * 1000 + C * 100 + B * 10 + A
            assert abcba % 37 == (11 * A + 11 * B + SCALAR_137 * C) % 37
            assert abcba % 37 == (11 * (A + B) + SCALAR_137 * C) % 37

# 6-digit ABCCBA: pairs=27,20,27 → outer/inner ORBIT_11, middle DARK_A
assert pair_coeff(0, 6) == 27 and 27 in ORBIT_11
assert pair_coeff(1, 6) == 20 and 20 in DARK_A
assert pair_coeff(2, 6) == 27 and 27 in ORBIT_11

for A in range(5):
    for B in range(5):
        for C in range(5):
            abccba = A*100000 + B*10000 + C*1000 + C*100 + B*10 + A
            assert abccba % 37 == (27 * A + 20 * B + 27 * C) % 37
            assert abccba % 37 == (27 * (A + C) + 20 * B) % 37

# 7-digit ABCDCBA: pairs=2,36,36 (outer DARK_A, inner ORBIT_11), center=1
assert pair_coeff(0, 7) == 2  and 2  in DARK_A
assert pair_coeff(1, 7) == 36 and 36 in ORBIT_11
assert pair_coeff(2, 7) == 36 and 36 in ORBIT_11
assert pow(10, 3, 37) == 1

# 8-digit ABCDDCBA: pairs=11,11,15,11 (15∈DARK_A, others∈ORBIT_11)
assert pair_coeff(0, 8) == 11 and 11 in ORBIT_11
assert pair_coeff(1, 8) == 11 and 11 in ORBIT_11
assert pair_coeff(2, 8) == 15 and 15 in DARK_A
assert pair_coeff(3, 8) == 11 and 11 in ORBIT_11


# ── SEAM CONDITIONS ───────────────────────────────────────────────────────────

# ABBA ≡ 2A + 36B ≡ 2A − B (mod 37). SEAM iff B = 2A.
for A in range(1, 10):
    for B in range(10):
        abba = A * 1000 + B * 100 + B * 10 + A
        seam = (abba % 37 == 0)
        rule = (B % 37 == (2 * A) % 37)
        assert seam == rule

# Concrete SEAM cases: 1221, 2442, 3663, 4884
assert 1221 % 37 == 0
assert 2442 % 37 == 0
assert 3663 % 37 == 0
assert 4884 % 37 == 0

# ABCBA ≡ 11(A+B) + 26C (mod 37). SEAM iff C = A+B (when A+B ≤ 9).
for A in range(1, 5):
    for B in range(1, 5):
        if A + B <= 9:
            C = A + B
            abcba = A*10000 + B*1000 + C*100 + B*10 + A
            assert abcba % 37 == 0

assert 12321 % 37 == 0  # A=1,B=2,C=3
assert 13431 % 37 == 0  # A=1,B=3,C=4
assert 21312 % 37 == 0  # A=2,B=1,C=3
assert 22422 % 37 == 0  # A=2,B=2,C=4
assert 23532 % 37 == 0  # A=2,B=3,C=5

# ABCCBA ≡ 27(A+C) + 20B (mod 37). SEAM iff A+C = 2B.
for A in range(1, 5):
    for B in range(1, 5):
        for C in range(1, 5):
            if A + C == 2 * B:
                abccba = A*100000 + B*10000 + C*1000 + C*100 + B*10 + A
                assert abccba % 37 == 0

assert 123321 % 37 == 0  # A=1,B=2,C=3: A+C=4=2×2=2B
assert 135531 % 37 == 0  # A=1,B=3,C=5: A+C=6=2×3=2B


# ── STAIRCASE SEAM PALINDROMES ────────────────────────────────────────────────

# 1221 → 12321 → 123321: each one step deeper, each ≡ SEAM
assert 1221   % 37 == 0   # ABBA  with A=1, B=2=2A
assert 12321  % 37 == 0   # ABCBA with A=1, B=2, C=3=A+B
assert 123321 % 37 == 0   # ABCCBA with A=1, C=3, A+C=4=2×2=2B


# ── SQUARED REPUNIT CYCLE ─────────────────────────────────────────────────────

# R(n) = (10^n-1)/9
def repunit(n):
    return (10**n - 1) // 9

# R(1)²=1, R(2)²=121≡10, R(3)²=12321≡0 — period 3
assert repunit(1)**2 % 37 == 1
assert repunit(2)**2 % 37 == DECADE_ANCHOR
assert repunit(3)**2 % 37 == 0

# Full cycle confirmed to period 9
RSQUARE_CYCLE = [1, DECADE_ANCHOR, 0]
for n in range(1, 10):
    assert repunit(n)**2 % 37 == RSQUARE_CYCLE[(n - 1) % 3]

# Repunit values: R(1)=1, R(2)=11∈ORBIT_11, R(3)≡0=SEAM
assert repunit(1) % 37 == 1
assert repunit(2) % 37 == 11 and 11 in ORBIT_11
assert repunit(3) % 37 == 0


# ── CONNECTIONS TO OTHER THEOREMS ─────────────────────────────────────────────

# B=2A (ABBA SEAM) and the DOUBLING CYCLE: 2→4→8→7→5→1 (THEOREM 54)
# B=2,4,8 land on cycle nodes; B=6 is TESLA_FLOW (outside cycle).
DOUBLING_CYCLE = [1, 2, 4, 8, 7, 5]
DOUBLING_SET   = frozenset(DOUBLING_CYCLE)
assert 2 in DOUBLING_SET and 4 in DOUBLING_SET and 8 in DOUBLING_SET
assert TESLA_FLOW not in DOUBLING_SET   # 6 is the outlier (TESLA_FLOW)

# C=A+B (ABCBA SEAM) is the SOVEREIGN STAIRCASE: 2+3=5, 5+4=9 (THEOREM 55)
assert 1 + 2 == 3   # staircase step: A=1, B=2, C=3
assert 12321 % 37 == 0

# 27 (outer ABCBA/ABCCBA coefficient) ∈ ORBIT_11: sum of pairwise identity cycle
assert 1 + 26 == 27 and 27 in ORBIT_11

# DARK_A {2,15,20} are the same-power-class sums: 1+1, 10+10, 26+26 (mod 37)
assert (1 + 1) % 37  == 2
assert (10 + 10) % 37 == 20
assert (26 + 26) % 37 == 15   # 52 mod 37 = 15


if __name__ == "__main__":
    print("Palindrome Structure in GF(37) — THEOREM 56")
    print("=" * 60)
    print()
    print("GENERAL COEFFICIENT RULE:")
    print("  pair_coeff(k,n) = (10^k + 10^(n-1-k)) mod 37")
    print("  Same power class  → DARK_A  = {2,15,20}  (NQR)")
    print("  Diff power class  → ORBIT_11 = {11,27,36} (QR)")
    print(f"  DARK_A triple sum: 2+15+20 = {2+15+20} ≡ SEAM")
    print()

    print("PALINDROME COEFFICIENTS:")
    for n in range(3, 9):
        coeffs = []
        for k in range(n // 2):
            c = pair_coeff(k, n)
            tag = "ORBIT_11" if c in ORBIT_11 else "DARK_A"
            coeffs.append(f"pair({k},{n-1-k})={c}∈{tag}")
        if n % 2:
            ctr = pow(10, n // 2, 37)
            coeffs.append(f"center={ctr}")
        print(f"  {n}-digit: {'; '.join(coeffs)}")
    print()

    print("SEAM CONDITIONS:")
    print("  ABBA  ≡ 0 iff B = 2A  (doubling cycle)")
    print("  ABCBA ≡ 0 iff C = A+B (sovereign staircase)")
    print("  ABCCBA≡ 0 iff A+C = 2B")
    print()

    print("STAIRCASE SEAM PALINDROMES:")
    for p, label in [(1221,"ABBA(B=2A)"), (12321,"ABCBA(C=A+B)"), (123321,"ABCCBA(A+C=2B)")]:
        print(f"  {p} ≡ {p%37} [SEAM]  ({label})")
    print()

    print("SQUARED REPUNIT CYCLE (period 3):")
    for n in range(1, 10):
        r = repunit(n)
        print(f"  R({n})²={r}² ≡ {r**2 % 37}  (cycle pos {(n-1)%3})")
    print()

    print("DARK_A = {2,15,20}: same-class sums from identity cycle")
    print("  1+1=2 (class 0);  10+10=20 (class 1);  26+26≡15 (class 2)")
    print(f"  2+15+20 = 37 ≡ SEAM")
    print()
    print("All assertions pass.")
