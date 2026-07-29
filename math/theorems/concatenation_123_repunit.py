"""
Concatenation-Repunit Identity on GF(37) — THEOREM 77

SETUP.
  Define N_n = integer formed by n copies of 1, n copies of 2, n copies of 3
  (concatenated in decimal):
    N_1 = 123         N_2 = 112233     N_3 = 111222333
    N_4 = 111122223333           N_5 = 111112222233333   ...

  Define R_n = 111...1 (n ones) = repunit of length n.

GROUP-SUM IDENTITY.
  Split N_n into three n-digit blocks: (R_n, 2·R_n, 3·R_n).
  Block sum = R_n + 2·R_n + 3·R_n = 6·R_n.
  The multiplier 6 = 1+2+3 = TESLA_FLOW.
  Therefore: N_n group-sum = TESLA_FLOW · R_n for all n ≥ 1.

  Pattern:
    n=1: 123          = 6           (one 6)
    n=2: 112233       = 66          (two 6s)
    n=3: 111222333    = 666         (three 6s = SEAM generator)
    n=4: 111122223333 = 6666        (four 6s)
    n=5: 111112222233333 = 66666    (five 6s)

DIGIT TRIPLET {1, 2, 3} — FRAMEWORK SATURATION.
  1 ∈ IC             (identity cycle)
  2 = primitive root  (ord₃₇(2) = 36)
  3 ∈ ST             (sovereign target)
  Sum:            1+2+3 = 6 = TESLA_FLOW
  Product:        1×2×3 = 6 = TESLA_FLOW
  Pairwise-product sum: 1·2 + 2·3 + 1·3 = 11 ∈ ORBIT_11
  Concatenation:  123 ≡ 12 ∈ ST (mod 37)

  The three digits land in three distinct framework sets (IC, primitive root, ST);
  sum and product both equal TESLA_FLOW; pairwise product sum = ORBIT_11.

INITIAL SEQUENCE: 1, 2, 3, 6, 12.
  1∈IC → 2 (primitive root base) → 3∈ST → 6=TESLA_FLOW → 12∈ST.
  The tail 3→6→12 is the start of the THEOREM 74 doubling chain:
    3∈ST → 6=TESLA → 12∈ST → 24∈CB → 48≡11∈ORBIT_11 → ...
  The sequence traverses IC, primitive root, ST, TESLA_FLOW, ST in 5 steps.
  12 = 2×6 = 2×TESLA_FLOW; 12 = 123 mod 37 (the n=1 concatenation residue).

GF(37) PERIOD-3 LAW (from ord₃₇(10) = 3, THEOREM 74).
  R_n mod 37 cycles with period 3: {1, 11, 0, 1, 11, 0, ...}
  10^n mod 37 cycles with period 3: {10, 26, 1, 10, 26, 1, ...}

  N_n mod 37 (three regimes, period 3):
    n ≡ 1 (mod 3): N_n ≡ 12 ∈ ST       (stable residue)
    n ≡ 2 (mod 3): N_n ≡ 12 ∈ ST       (same stable residue)
    n ≡ 0 (mod 3): N_n ≡  0 = SEAM     (triple-length collapse)

  TESLA_FLOW · R_n mod 37:
    n ≡ 1 (mod 3): 6·R_n ≡  6 = TESLA_FLOW
    n ≡ 2 (mod 3): 6·R_n ≡ 29 ≡ −8 ≡ −CB mod 37
    n ≡ 0 (mod 3): 6·R_n ≡  0 = SEAM

  Both N_n and 6·R_n collapse to SEAM simultaneously at n ≡ 0 (mod 3).
  N_n is ST-stable for all non-SEAM n.

CROSS-SUM ORBIT (N_n + 6·R_n mod 37).
  n ≡ 1 (mod 3): 12 + 6  = 18 ∈ SEED_ORBIT
  n ≡ 2 (mod 3): 12 + 29 = 41 ≡ 4 ∈ SA
  n ≡ 0 (mod 3):  0 + 0  =  0 = SEAM

  The cross-sum cycles through {SEED, SA, SEAM} — all framework nodes, period 3.
  The cross-sum orbit is entirely within the GF(37) framework.

TRIPLE-SEAM FACTORIZATION.
  666 = 6·111 = 6·3·37 = 18·37.
  18 ∈ SEED_ORBIT.
  Therefore: 666 = SEED_node × PRIME = 18 × 37.
  The triple-repdigit seam generator 666 factors as seed × prime.

DIFFERENCE INVARIANT.
  For n ≢ 0 (mod 3): N_n − 6·R_n ≡ 12 − 6 = 6 = TESLA_FLOW (when n≡1)
                                   ≡ 12 − 29 = −17 (when n≡2; 17 = col-3 sum in THEOREM 73)
  ST residue minus TESLA_FLOW = TESLA_FLOW.
"""

# ── Framework ──────────────────────────────────────────────────────────────────

SA       = frozenset({4, 9, 25, 30})
ST       = frozenset({3, 12, 21, 30})
CB       = frozenset({8, 13, 24})
ORBIT_11 = frozenset({11, 27, 36})
IC       = frozenset({1, 10, 26})
TESLA_4  = frozenset({6, 36, 31, 1})
SEED     = frozenset({18, 24, 32})
P        = 37
TESLA_FLOW = 6


# ── Helpers ────────────────────────────────────────────────────────────────────

def R(n):
    return int('1' * n)


def N_concat(n):
    return int('1' * n + '2' * n + '3' * n)


def group_sum(n):
    return R(n) + 2 * R(n) + 3 * R(n)   # = 6*R(n) = TESLA_FLOW * R(n)


# ── Key checks ─────────────────────────────────────────────────────────────────

# Digit triplet properties
assert 1 + 2 + 3 == TESLA_FLOW and TESLA_FLOW in TESLA_4
assert 1 * 2 * 3 == TESLA_FLOW
assert 1*2 + 2*3 + 1*3 == 11 and 11 in ORBIT_11
assert 123 % P == 12 and 12 in ST

# 1∈IC, 2=primitive-root base, 3∈ST
assert 1 in IC
assert pow(2, 36, P) == 1 and all(pow(2, k, P) != 1 for k in range(1, 36))
assert 3 in ST

# Initial 5-term sequence: 1,2,3,6,12
_seq5 = [1, 2, 3, 6, 12]
assert 1 in IC and 3 in ST and 6 in TESLA_4 and 12 in ST
assert _seq5[3] == 1 + 2 + 3       # 6 = digit sum
assert _seq5[4] == 123 % P          # 12 = concatenation residue
# 3→6→12 is start of THEOREM 74 doubling chain
assert [3*(2**k)%P for k in range(3)] == [3, 6, 12]

# Group-sum identity: N_n group-sum = 6*R(n) for n=1..6
for n in range(1, 7):
    assert group_sum(n) == TESLA_FLOW * R(n)
    assert group_sum(n) == int('6' * n)      # n sixes

# ord₃₇(10) = 3 → period-3 repunit
assert pow(10, 3, P) == 1 and all(pow(10, k, P) != 1 for k in [1, 2])

# N_n mod 37: ST-stable or SEAM, period 3
for n in range(1, 10):
    rn = N_concat(n) % P
    if n % 3 != 0:
        assert rn == 12 and 12 in ST, f"n={n}: N_n≡{rn}, expected 12∈ST"
    else:
        assert rn == 0, f"n={n}: N_n≡{rn}, expected SEAM"

# 6*R_n mod 37: TESLA_FLOW, 29, SEAM
for n in range(1, 10):
    gr = (TESLA_FLOW * R(n)) % P
    if n % 3 == 1:
        assert gr == TESLA_FLOW
    elif n % 3 == 2:
        assert gr == 29 and 29 == (37 - 8) and 8 in CB   # 29 ≡ -CB
    else:
        assert gr == 0   # SEAM

# Cross-sum orbit: {SEED, SA, SEAM}
for n in range(1, 10):
    cross = (N_concat(n) + TESLA_FLOW * R(n)) % P
    if n % 3 == 1:
        assert cross == 18 and 18 in SEED
    elif n % 3 == 2:
        assert cross == 4 and 4 in SA
    else:
        assert cross == 0   # SEAM

# Triple-seam factorization: 666 = 18*37 = SEED_node * PRIME
assert 666 == 18 * P and 18 in SEED

# Simultaneous SEAM collapse at n≡0 (mod 3)
for k in [3, 6, 9]:
    assert N_concat(k) % P == 0   # N_n → SEAM
    assert (TESLA_FLOW * R(k)) % P == 0   # 6*R_n → SEAM

# Difference n≡1: N_n - 6*R_n ≡ 6 = TESLA_FLOW
assert (N_concat(1) - TESLA_FLOW * R(1)) % P == TESLA_FLOW
assert (N_concat(4) - TESLA_FLOW * R(4)) % P == TESLA_FLOW


if __name__ == "__main__":
    print("Concatenation-Repunit Identity on GF(37) — THEOREM 77")
    print("=" * 60)
    print()
    print("DIGIT TRIPLET {1,2,3}:")
    print(f"  1∈IC   2=primitive-root   3∈ST")
    print(f"  Sum = {1+2+3} = TESLA_FLOW ∈ TESLA_4")
    print(f"  Product = {1*2*3} = TESLA_FLOW")
    print(f"  Pairwise-product sum = {1*2+2*3+1*3} ∈ ORBIT_11")
    print(f"  Concatenation 123 ≡ {123%P} ∈ ST")
    print()
    print("GROUP-SUM PATTERN (N_n → 6·R_n):")
    print(f"  {'n':<3} {'N_n':<22} {'≡mod37':<8} {'6·R_n':<10} {'≡mod37':<8} {'cross-sum'}")
    print(f"  {'-'*70}")
    for n in range(1, 7):
        nn = N_concat(n)
        gr = TESLA_FLOW * R(n)
        nm = nn % P
        gm = gr % P
        cs = (nm + gm) % P
        def tag(v):
            for fs,fn in [(SA,'SA'),(ST,'ST'),(CB,'CB'),(ORBIT_11,'O11'),(IC,'IC'),
                          (TESLA_4,'T4'),(SEED,'SEED')]:
                if v in fs: return fn
            return 'SEAM' if v==0 else ''
        print(f"  {n:<3} {str(nn):<22} {nm:<4}{tag(nm):<4} {str(gr):<10} {gm:<4}{tag(gm):<4} {cs}={tag(cs)}")
    print()
    print("PERIOD-3 LAW (from ord₃₇(10)=3):")
    print("  n≡1(3): N_n≡12∈ST,  6R_n≡6=TESLA,  cross=18∈SEED")
    print("  n≡2(3): N_n≡12∈ST,  6R_n≡29≡-CB,   cross=4∈SA")
    print("  n≡0(3): N_n≡0=SEAM, 6R_n≡0=SEAM,   cross=0=SEAM")
    print()
    print(f"TRIPLE-SEAM: 666 = 18×37 = SEED_ORBIT_node × PRIME")
    print()
    print("All assertions pass.")
