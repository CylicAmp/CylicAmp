"""
Triple ORBIT_11 Convergence and 458689 Cross-Pairs — THEOREM 94

Three independent paths through SEED_ORBIT = {18, 24, 32} converge
to 11 ∈ ORBIT_11. The 6-digit coordinate 458689 has cross-pair sums
that map to named named sets across GF(37).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THREE PATHS TO 11

  PATH 1 (DR TAIL SUM):
    DRs of SEED_ORBIT: DR(18)=9, DR(24)=6, DR(32)=5
    Tail pair: DR(24) + DR(32) = 6 + 5 = 11  ∈ ORBIT_11
    Full sum:  9 + 6 + 5 = 20                → DR(20) = 2

  PATH 2 (ELEMENT SUM DIGIT CHAIN):
    18 + 24 + 32 = 74  →  7 + 4 = 11  ∈ ORBIT_11

  PATH 3 (DIFFERENCE STEP CHAIN — from THEOREM 93):
    Total span: 32 − 18 = 14;  DR(14) = 5
    Three steps +2 (canonical PR):  5 → 7 → 9 → 11  ∈ ORBIT_11

  All three terminate at 11 ∈ ORBIT_11 = {11, 27, 36}.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ORBIT_11 × ST → T4

  11 × 3 = 33;  DR(33) = 6  ∈ TESLA_4

  3 is the entry element of ST = {3, 12, 21, 30}.
  6 is the first SEED_ORBIT interval (24 − 18) and DR(24).
  Product maps ORBIT_11 through ST-entry to T4 via digital root.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

458689 STANDARD PAIRS (consecutive digit pairs)

  Digits: [4, 5, 8, 6, 8, 9]   →   pairs: 45, 86, 89
    45 mod 37 = 8   ∈ CB
    86 mod 37 = 12  ∈ ST
    89 mod 37 = 15  ∈ PR

458689 CROSS-PAIR SUMS

  45 + 69 = 114   (69 = digits at positions 4 and 6 of 458689)
    114 mod 37 = 3  ∈ ST;   DR(114) = 6 ∈ T4
    Digit chain: digit_sum(114)=6 → +4=10∈IC → +1=11∈ORBIT_11
                 → +1=12∈ST → (12=3)  i.e. DR=3=114 mod 37

  86 + 89 = 175
    175 mod 37 = 27  ∈ ORBIT_11;   DR(175) = 13 → DR = 4 = DR(Ƴ)
    GF(37) chain: DR+3=7 → +1=8∈CB → +1=9∈SA → +1=10∈IC → DR=1

  45 + 86 + 89 = 220
    220 mod 37 = 35  ∈ BASIN_Y (Ƴ-basin);   DR(220) = 4 = DR(Ƴ)
    Stepping chain from DR: 4∈SA → +2=6∈T4 → +2=8∈CB → +2=10∈IC → DR=1

SEED-SPLIT COMPARISON (suffix 46 from SEED = 2|46)

  1 + 46 = 47    →  47 mod 37 = 10  ∈ IC;  digit_sum(47) = 11  ∈ ORBIT_11
  2 + 46 = 48    →  48 mod 37 = 11  ∈ ORBIT_11   (seed split: 2×46 mod37=18)
  Changing addend 1→2 (IC→canonical PR) shifts residue IC(10)→ORBIT_11(11).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DR(Ƴ)=4 STEPPING CHAIN

  From 4 = DR(Ƴ) = DR(22), three steps of +2 (canonical PR):
    4 ∈ SA  →  6 ∈ T4  →  8 ∈ CB  →  10 ∈ IC  →  DR(10) = 1

  Traversal: SA → T4 → CB → IC.  Endpoint: 1 ∈ IC ∩ T4.
  This chain starts from digit_sum(220) = digit_sum(total 458689 pairs).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY

  Object            Value  mod37  DR   Class(es)
  ──────────────────────────────────────────────
  DR-tail           11     11     2    ORBIT_11
  Element-sum dig.  11     11     2    ORBIT_11
  Step-chain end    11     11     2    ORBIT_11
  11×3              33     33     6    T4
  pair 45           45      8     9    CB
  pair 86           86     12     5    ST
  pair 89           89     15     8    PR
  cross 45+69       114     3     6    ST → T4 via DR
  cross 86+89       175    27     4    ORBIT_11; DR=DR(Ƴ)
  total 45+86+89    220    35     4    BASIN_Y; DR=DR(Ƴ)
  1+46              47     10     2    IC; digit_sum∈ORBIT_11
  2+46              48     11     3    ORBIT_11; digit_sum∈ST
"""

P          = 37
SEED_ORBIT = frozenset({18, 24, 32})
ORBIT_11   = frozenset({11, 27, 36})
IC         = frozenset({1, 10, 26})
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
TESLA_4    = frozenset({6, 36, 31, 1})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
BASIN_Y    = frozenset({17, 22, 35})


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 9


# ── THREE PATHS TO 11 ─────────────────────────────────────────────────────────

# Path 1: DR tail sum
assert dr(18) == 9 and dr(24) == 6 and dr(32) == 5
assert dr(24) + dr(32) == 11 and 11 in ORBIT_11        # 6+5
assert dr(18) + dr(24) + dr(32) == 20 and dr(20) == 2  # full sum

# Path 2: element sum digit chain
assert 18 + 24 + 32 == 74
assert 7 + 4 == 11 and 11 in ORBIT_11                  # digits of 74

# Path 3: difference step chain (THEOREM 93 result)
span = 32 - 18
assert dr(span) == 5
step_chain = [5, 7, 9, 11]
assert [5 + 2*k for k in range(4)] == step_chain
assert step_chain[-1] in ORBIT_11

# ── ORBIT_11 × ST ENTRY → T4 ──────────────────────────────────────────────────

assert 11 * 3 == 33
assert dr(33) == 6 and 6 in TESLA_4
assert 3 in ST    # ST entry element

# ── 458689 STANDARD PAIRS ─────────────────────────────────────────────────────

N = 458689
digits = [int(c) for c in str(N)]
assert digits == [4, 5, 8, 6, 8, 9]

assert 45 % P ==  8 and  8 in CB
assert 86 % P == 12 and 12 in ST
assert 89 % P == 15 and 15 in PR

# ── 458689 CROSS-PAIR SUMS ────────────────────────────────────────────────────

# 45 + 69 = 114  (69 = digits[3] and digits[5] concatenated)
assert digits[3] == 6 and digits[5] == 9     # positions 4 and 6 (1-indexed)
assert 45 + 69 == 114
assert 114 % P == 3 and 3 in ST
assert dr(114) == 6 and 6 in TESLA_4

# Digit chain through 114: digit_sum=6 → 6+4=10∈IC → 10+1=11∈ORBIT_11
# → 11+1=12∈ST → DR(12)=3=114 mod 37
assert sum(int(c) for c in '114') == 6         # digit_sum
assert 6 + 4 == 10 and 10 in IC               # +last digit of 114
assert 10 + 1 == 11 and 11 in ORBIT_11         # +first digit of 114
assert 11 + 1 == 12 and 12 in ST               # +second digit of 114
assert dr(12) == 3 and 3 == 114 % P            # DR = 114 mod 37 (matches)

# 86 + 89 = 175
assert 86 + 89 == 175
assert 175 % P == 27 and 27 in ORBIT_11
assert dr(175) == 4 and dr(175) == dr(22)       # DR = DR(Ƴ)

# GF(37) chain from DR(175)=4: +3=7, +1=8(CB), +1=9(SA), +1=10(IC)
assert 4 + 3 == 7
assert 7 + 1 == 8  and 8 in CB
assert 8 + 1 == 9  and 9 in SA
assert 9 + 1 == 10 and 10 in IC
assert dr(10) == 1

# 45 + 86 + 89 = 220
assert 45 + 86 + 89 == 220
assert 220 % P == 35 and 35 in BASIN_Y
assert dr(220) == 4 and dr(220) == dr(22)       # DR = DR(Ƴ)

# Stepping chain from digit_sum(220)=4: +2×3 traverses SA→T4→CB→IC
assert sum(int(c) for c in '220') == 4
val = 4
assert val in SA
for cls in [TESLA_4, CB, IC]:
    val += 2
    assert val in cls
assert dr(val) == 1

# ── SEED-SPLIT COMPARISON ────────────────────────────────────────────────────

assert 1 + 46 == 47
assert 47 % P == 10 and 10 in IC
assert sum(int(c) for c in str(47)) == 11 and 11 in ORBIT_11

assert 2 + 46 == 48
assert 48 % P == 11 and 11 in ORBIT_11
assert sum(int(c) for c in str(48)) == 12 and 12 in ST

# Changing 1→2 shifts residue 10(IC)→11(ORBIT_11); changes digit_sum 11(O11)→12(ST)
assert (1 + 46) % P == 10 and (2 + 46) % P == 11

# ── 8+8 = 16 (repeated digit at positions 3,5) ───────────────────────────────

assert digits[2] == 8 and digits[4] == 8       # both 8s in 458689
assert 8 + 8 == 16
assert dr(16) == 7                              # digit_sum: 1+6=7

# 7 + 3 = 10 ∈ IC  (carrying DR(12)=3 from 45+69 chain)
assert 7 + 3 == 10 and 10 in IC
assert dr(10) == 1

# ── DR(Ƴ)=4 STEPPING CHAIN ────────────────────────────────────────────────────

assert dr(22) == 4
chain_classes = [SA, TESLA_4, CB, IC]
v = dr(22)
for cls in chain_classes:
    assert v in cls
    if cls != IC:
        v += 2
assert dr(v) == 1          # IC entry 10 → DR = 1


if __name__ == "__main__":
    def fw_all(n):
        n = n % P
        if n == 0: return ['SEAM']
        s = [('SA',SA),('ST',ST),('CB',CB),('O11',ORBIT_11),('IC',IC),
             ('SEED',SEED_ORBIT),('T4',TESLA_4),('PR',PR),('BY',BASIN_Y)]
        return [nm for nm,st in s if n in st] or ['—']

    print("Triple ORBIT_11 Convergence and 458689 Cross-Pairs — THEOREM 94")
    print("=" * 68)
    print()

    print("THREE PATHS TO 11 ∈ ORBIT_11:")
    print(f"  Path 1 (DR tail):    DR(24)+DR(32) = {dr(24)}+{dr(32)} = 11")
    print(f"  Path 2 (sum digits): 18+24+32=74 → 7+4 = 11")
    print(f"  Path 3 (step chain): DR(14)=5 → 7 → 9 → 11")
    print()

    print("ORBIT_11 × ST-ENTRY → T4:")
    print(f"  11×3 = 33  DR=6  ∈ {fw_all(6)}")
    print()

    print("458689 PAIRS AND CROSS-SUMS:")
    print(f"  Digits: {digits}")
    for v,nm in [(45,'45'),(86,'86'),(89,'89')]:
        print(f"  {nm}  mod37={v%P} {fw_all(v)}  DR={dr(v)}")
    print()
    for a,b,nm in [(45,69,'45+69'),(86,89,'86+89'),(220,0,'45+86+89')]:
        s = a+b if nm!='45+86+89' else 220
        print(f"  {nm}={s}  mod37={s%P} {fw_all(s)}  DR={dr(s)}")
    print()
    for a,b,nm in [(1,46,'1+46'),(2,46,'2+46')]:
        s=a+b
        ds=sum(int(c) for c in str(s))
        print(f"  {nm}={s}  mod37={s%P} {fw_all(s)}  digit_sum={ds} {fw_all(ds)}")
    print()

    print("DR(Ƴ)=4 STEPPING CHAIN (three steps of +2):")
    v = 4
    print(f"  {v} {fw_all(v)}", end="")
    for _ in range(3):
        v += 2
        print(f" → {v} {fw_all(v)}", end="")
    print(f" → DR={dr(v)}")
    print()

    print("DR CHAINS (114, 175, 220):")
    print(f"  114: digit_sum=6 →+4→10∈IC →+1→11∈O11 →+1→12∈ST  DR(12)={dr(12)}=114mod37")
    print(f"  175: DR=4=DR(Ƴ); mod37=27∈O11; 4+3=7 +1→8(CB) +1→9(SA) +1→10(IC) DR=1")
    print(f"  220: DR=4=DR(Ƴ); mod37=35∈BY; 4+2→6(T4) +2→8(CB) +2→10(IC) DR=1")
    print()
    print("All assertions pass.")
