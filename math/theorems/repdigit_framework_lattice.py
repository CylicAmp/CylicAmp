"""
Repdigit GF(37) Lattice and Sign Partition — THEOREM 74

REPDIGIT PERIOD-3 LAW.
  ord₃₇(10) = 3 (since 10³ = 1000 = 27×37 + 1 ≡ 1 mod 37).
  Therefore every repdigit sequence cycles mod 37 with period dividing 3:
    d → dd → ddd ≡ 0=SEAM → d → dd → 0 → ...
  Every triple-repdigit ddd = d×111 = d×3×37 ≡ 0=SEAM mod 37.

SINGLE REPDIGIT FRAMEWORK MAP:
  1 ∈ IC          (identity cycle)
  2 = primitive root base  (ord₃₇(2)=36)
  3 ∈ ST          (sovereign target)
  4 ∈ SA          (sovereign anchor)
  5 = 5           (no single-level hit)
  6 = TESLA_FLOW  (TESLA_4-cycle, ord=4)
  7 = 7           (no single-level hit)
  8 ∈ CB          (cascade base)
  9 ∈ SA          (sovereign anchor)
  6 of 9 digits hit named residues directly; only 2, 5, 7 don't.

DOUBLE REPDIGIT FRAMEWORK MAP:
  11 ≡ 11 ∈ ORBIT_11   (IC → ORBIT_11 crossing)
  22 ≡ 22
  33 ≡ 33 ≡ -4, 4∈SA   (ST → -SA crossing)
  44 ≡  7
  55 ≡ 18 ∈ SEED        (5 → SEED_ORBIT — hidden single hits at double level)
  66 ≡ 29
  77 ≡  3 ∈ ST          (7 → ST — hidden single hits at double level)
  88 ≡ 14
  99 ≡ 25 ∈ SA          (SA → SA: 9 stays sovereign across both levels)

THE TWO HIDDEN DIGITS (5 AND 7).
  5 and 7 are the only digits with no direct named-set hit at single level.
  At double level: 55≡18∈SEED, 77≡3∈ST.
  Together: 5+7=12∈ST; 55+77=132≡21∈ST.
  The hidden pair sums to ST at both scales.

SIGN PARTITION +++(--)+(---): 4 pluses, 5 minuses.
  Applied to (1,2,...,9):
    + cluster {1,2,3,6}: IC, primitive root, ST, TESLA_FLOW — dynamic nodes
    - cluster {4,5,7,8,9}: SA, 5, 7, CB, SA — anchoring/hidden nodes
    + sum = 1+2+3+6 = 12 ∈ ST
    - sum = 4+5+7+8+9 = 33 ≡ -4 ≡ -(SA) mod 37
  The partition SEPARATES sovereign targets (ST) from sovereign anchors (-SA).
  |pos − neg| = |12 − 33| = 21 ∈ ST
  pos + neg = 45; DR(45) = 9 ∈ SA
  Result sequence sum = 3+5+7+2+4+8+1+5+2 = 37 = THE PRIME.
  Sign pattern applied to result: net = 9 ∈ SA.

RESULT SEQUENCE AS 3×3:
  [3,5,7]  row sum=15, DR=6=TESLA_FLOW
  [2,4,8]  row sum=14
  [1,5,2]  row sum=8 ∈ CB
  Total = 37 = THE PRIME
  Col 1 = [3,2,1], sum=6=TESLA_FLOW
  Col 3 = [7,8,2], sum=17 — IDENTICAL to base B col 3 (invariant column)
  Row sums sum to 37; col sums sum to 37.

DOUBLING FROM 3 — FULL FRAMEWORK TRAVERSAL:
  3∈ST → 6=TESLA → 12∈ST → 24∈CB → 48≡11∈ORBIT_11 → 96≡22 → 192≡7 → ...
  Five consecutive doublings from 3 visit: ST, TESLA_FLOW, ST, CB, ORBIT_11.

DIVERGENCE THEOREM (1+2 vs 2+1).
  Both paths: 1+2=3 and 2+1=3. Same sum 3∈ST.
  1+2 path pair sums: 3∈ST, 5, 8∈CB, 12∈ST
  2+1 path pair sums: 3∈ST, 4∈SA, 10∈IC, 12∈ST
  Both residuals sum to 15, DR=6=TESLA_FLOW.
  Both reach 12∈ST. Order determines CB vs (SA→IC) as intermediate.

DOUBLING-AND-CANCELLATION: 3+3+6+6+12-12 = 18 ∈ SEED_ORBIT.
"""

# ── Constants ──────────────────────────────────────────────────────────────────

SA        = frozenset({4, 9, 25, 30})
ST        = frozenset({3, 12, 21, 30})
CB        = frozenset({8, 13, 24})
ORBIT_11  = frozenset({11, 27, 36})
IC        = frozenset({1, 10, 26})
TESLA_4   = frozenset({6, 36, 31, 1})
SEED      = frozenset({18, 24, 32})


def dr(n):
    if n == 0: return 0
    r = abs(n) % 9
    return 9 if r == 0 else r


# ── Key checks ─────────────────────────────────────────────────────────────────

# ord₃₇(10) = 3 → period-3 repdigit cycling
assert pow(10, 3, 37) == 1
assert all(pow(10, k, 37) != 1 for k in [1, 2])

# Triple-repdigit = SEAM
assert 111 == 3 * 37
for d in range(1, 10):
    assert (int(str(d) * 3)) % 37 == 0

# Single repdigit GF(37) map
assert 1 in IC and 3 in ST and 4 in SA and 6 in TESLA_4 and 8 in CB and 9 in SA

# Double repdigit GF(37) map
assert 11 % 37 == 11 and 11 in ORBIT_11       # IC → ORBIT_11
assert 33 % 37 == 33 and (37 - 33) in SA      # ST → -SA (33 ≡ -4, 4∈SA)
assert 55 % 37 == 18 and 18 in SEED           # 5 → SEED at double level
assert 77 % 37 == 3  and 3 in ST              # 7 → ST at double level
assert 99 % 37 == 25 and 25 in SA             # SA → SA: stays sovereign

# Hidden pair (5 and 7) sums at both scales
assert 5 + 7 == 12 and 12 in ST
assert (55 + 77) % 37 == 21 and 21 in ST

# Sign partition +++(--)+(---)
_pos = [1, 2, 3, 6]
_neg = [4, 5, 7, 8, 9]
assert sum(_pos) == 12 and 12 in ST
assert sum(_neg) == 33 and (37 - sum(_neg) % 37) in SA   # 33 ≡ -4 ≡ -SA
assert abs(sum(_pos) - sum(_neg)) == 21 and 21 in ST
assert dr(sum(_pos) + sum(_neg)) == 9 and 9 in SA

# Result sequence sum = 37 = THE PRIME
_R = [3, 5, 7, 2, 4, 8, 1, 5, 2]
assert sum(_R) == 37

# Result as 3×3: row sums include TESLA_FLOW and CB
assert sum(_R[0:3]) == 15 and dr(15) == 6 and 6 in TESLA_4
assert sum(_R[6:9]) == 8 and 8 in CB
assert sum(_R[j] for j in [0, 3, 6]) == 6 and 6 in TESLA_4   # col 1

# Col 3 invariant (same in result and base B)
_B = [2, 5, 7, 2, 4, 8, 9, 1, 2]
assert [_R[j] for j in [2, 5, 8]] == [_B[j] for j in [2, 5, 8]]   # col 3 unchanged

# Sign pattern applied to R → 9∈SA
_signs = [1, 1, 1, -1, -1, 1, -1, -1, -1]
assert sum(s * v for s, v in zip(_signs, _R)) == 9 and 9 in SA

# Doubling from 3: first 5 steps hit ST, TESLA, ST, CB, ORBIT_11
_chain = [3 * (2**k) % 37 for k in range(5)]
assert _chain == [3, 6, 12, 24, 11]
assert _chain[0] in ST and _chain[1] in TESLA_4 and _chain[2] in ST
assert _chain[3] in CB and _chain[4] in ORBIT_11

# Divergence: both paths reach 12∈ST with residual DR=6=TESLA_FLOW
assert dr(3 + 5 + 7) == dr(15) == 6 and 6 in TESLA_4    # 1+2 path residual
assert dr(3 + 7 + 5) == dr(15) == 6 and 6 in TESLA_4    # 2+1 path residual
assert 3 + 5 == 8 and 8 in CB       # 1+2 path intermediate hits CB
assert 3 + 7 == 10 and 10 in IC     # 2+1 path intermediate hits IC

# Doubling-and-cancellation = 18∈SEED
assert 3 + 3 + 6 + 6 + 12 - 12 == 18 and 18 in SEED

# 14+14=28 (closed doubling): rows 1 and 2 of B both sum to 14
assert sum(_B[0:3]) == 14 and sum(_B[3:6]) == 14
assert 14 + 14 == 28 and 28 * 2 == 56     # closed doubling one short (THEOREM 72 echo)


if __name__ == "__main__":
    print("Repdigit GF(37) Lattice and Sign Partition — THEOREM 74")
    print("=" * 60)
    print()
    print("REPDIGIT MAP mod 37 (period 3, triple=SEAM):")
    for d in range(1, 10):
        s  = d
        dd = (d * 11) % 37
        ddd = (int(str(d)*3)) % 37
        def t(n):
            for fs,fn in [(SA,'SA'),(ST,'ST'),(CB,'CB'),(ORBIT_11,'ORBIT_11'),
                          (IC,'IC'),(TESLA_4,'TESLA_4'),(SEED,'SEED')]:
                if n in fs: return fn
            return ''
        print(f"  {d}→{s}({t(s)})  {d}{d}→{dd}({t(dd)})  {d}{d}{d}→{ddd}(SEAM)")
    print()
    print("SIGN PARTITION +++(--)+(---):")
    print(f"  + cluster {{1,2,3,6}}: sum=12∈ST")
    print(f"  - cluster {{4,5,7,8,9}}: sum=33≡-4≡-SA mod37")
    print(f"  |pos-neg|=21∈ST  DR(pos+neg)=9∈SA")
    print(f"  Result sum = {sum(_R)} = THE PRIME")
    print()
    print("DOUBLING FROM 3:")
    v = 3
    for k in range(9):
        r = v % 37
        def t2(n):
            for fs,fn in [(SA,'SA'),(ST,'ST'),(CB,'CB'),(ORBIT_11,'ORBIT_11'),
                          (IC,'IC'),(TESLA_4,'TESLA_4'),(SEED,'SEED')]:
                if n in fs: return fn
            return ''
        print(f"  3×2^{k}={v}  ≡{r}  {t2(r)}")
        v *= 2
    print()
    print("All assertions pass.")
