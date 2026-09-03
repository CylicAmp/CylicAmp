"""
Theorem 237: Rule 30 Normality — Block Frequency Convergence and GF(37) Extremes
Author: Michael Warren Song (CyclicAmp)

Normality (stronger than Problem 3): for every k, each k-bit block appears
in the center column with frequency approaching exactly 1/2^k.

Problem 3 only requires eventual appearance. Normality requires that the
frequency converges to the uniform value. This theorem measures the convergence
and classifies the extremes in GF(37).

=== CHI-SQUARED CONVERGENCE TO UNIFORMITY ===

For each k, the chi-squared statistic measures deviation from the uniform
distribution over 2^k blocks. Under true normality, chi2/df → 1 as N → ∞.
(df = 2^k − 1; the null expectation is chi2 = df.)

N = 20000 steps:

  k= 1: chi2=    2.83  df=     1  ratio=2.832   all-ones: 1.012x  all-zeros: 0.988x
  k= 2: chi2=    6.47  df=     3  ratio=2.157   all-ones: 1.018x  all-zeros: 0.970x
  k= 3: chi2=   10.54  df=     7  ratio=1.505   all-ones: 1.020x  all-zeros: 0.958x
  k= 4: chi2=   15.78  df=    15  ratio=1.052   all-ones: 1.038x  all-zeros: 0.947x
  k= 5: chi2=   33.97  df=    31  ratio=1.096   all-ones: 1.091x  all-zeros: 0.930x
  k= 6: chi2=   78.69  df=    63  ratio=1.249   all-ones: 1.191x  all-zeros: 0.954x
  k= 7: chi2=  151.76  df=   127  ratio=1.195   all-ones: 1.229x  all-zeros: 0.992x
  k= 8: chi2=  286.32  df=   255  ratio=1.123   all-ones: 1.216x  all-zeros: 0.999x
  k= 9: chi2=  530.26  df=   511  ratio=1.038   all-ones: 1.255x  all-zeros: 1.050x
  k=10: chi2= 1040.31  df=  1023  ratio=1.017   all-ones: 1.025x  all-zeros: 0.922x

The ratio chi2/df decreases from 2.83 at k=1 toward 1.017 at k=10.
Trend: the sequence is approaching uniformity at larger block lengths.
At k=4, ratio reaches ≈1.05 and then oscillates close to 1 for k≥4.

This is strong evidence (not proof) that the center column is normal.

=== ALL-ONES PERSISTENT OVER-REPRESENTATION ===

The all-ones block (1^k) is over-represented at every k from 1 to 10.
The all-zeros block (0^k) is under-represented for most k.

This is consistent with the orbit-level density finding (T235): the density
at N=20000 is 0.5060 (ones slightly over-represented at this cutoff).
Density oscillates: at N=5000 it was 0.494, at N=20000 it is 0.506.

The persistent over-representation of all-ones runs indicates the center
column has positive autocorrelation at short lags — runs of 1s are
slightly longer than expected under independence.

=== RUN-LENGTH ANALYSIS ===

Under normality (fair coin flips), run lengths follow a geometric distribution
with mean 2 for both 0-runs and 1-runs.

Observed (N = 20000 steps):
  Runs of 1s: count=5032, mean=2.0109, max=13
  Runs of 0s: count=5032, mean=1.9636, max=14

Both means are within 2% of the theoretical 2.000. The number of 1-runs
and 0-runs are exactly equal (5032 each), as required by a binary sequence
that alternates between runs. Max run lengths of 13 and 14 are consistent
with what an approximately fair coin would produce over 20000 trials
(expected max run ≈ log2(20000) ≈ 14.3).

Run-length distribution matches normality prediction closely.

=== EXTREME BLOCKS: GF(37) ANALYSIS ===

Most over-represented k=10 block:
  509 = 0111111101  mod37=28 ∈ SA_ST_B
  509 is prime. 509 is Sophie Germain: 2×509+1=1019 (prime), 1019∈IC (1019 mod37=26∈IC).
  509 × 137 mod 37 = 25 ∈ SA_ST_B (137-map keeps 509's orbit: 28→25→21→28 = SA_ST_B).
  SA_ST_B is ACTIVE-biased (T235: ratio 0.5037). The most over-represented block
  has its binary value in the most active-biased regular orbit.

Least frequent k=10 block:
  211 = 0011010011  mod37=26 ∈ IC
  211 is prime. Not Sophie Germain (2×211+1=423=3×141, not prime).
  211 × 137 mod 37 = 10 ∈ IC (137-map fixes IC: 26→10→1→26 = IC 3-cycle).
  IC = {1,10,26} is ACTIVE-biased (T235: ratio 0.5320). Despite IC being
  active-biased at the step level, the specific bit-pattern 0011010011
  is under-represented. Step-level bias and block-pattern frequency are distinct.

Most over-represented k=9 block:
  91 = 001011011  mod37=17 ∈ NQR17
  91 = 7 × 13: 7∈D7 (INACTIVE-biased), 13∈CAS_EXT (near-neutral).
  91 × 137 mod 37 = 35 ∈ NQR17 (137-map keeps NQR17: 17→35→22→17 = NQR17).

=== NORMALITY VS ORBIT BIAS ===

T235 showed that step indices classified by GF(37) orbit have measurable
active-bit density bias (IC=0.532, DARK_A=0.456). If the sequence were
strictly normal (independent fair coin flips), all orbit densities would
converge to 0.5 with no systematic orbit preference.

The persistent orbit bias (T235) is therefore evidence against strict normality
under the assumption of independence. However, normality does not require
independence — it only requires frequency convergence. A biased sequence
at the orbit level can still be normal if the biases exactly cancel in the
block frequency statistics.

The chi-squared ratio converging to 1 supports normality at the block level
even while orbit-level bias persists. These are compatible: the orbit bias
may encode long-range correlation structure that does not affect finite-block
frequencies.

=== DENSITY OSCILLATION ===

  N= 1000: density=0.480  (−0.020 from 0.5)
  N= 5000: density=0.494  (−0.006)
  N=20000: density=0.506  (+0.006)

The density oscillates through 0.5 with decreasing amplitude, consistent
with convergence toward 0.5 (Problem 2). The oscillation means both the
all-ones and all-zeros biases reverse as N increases.

=== 1/137 ===

509 (most over-represented k=10 block): 509 is Sophie Germain. Safe prime 1019.
  1019 mod 37 = 1019 − 27×37 = 1019 − 999 = 20 ∈ DARK_A.
  (DARK_A is the most INACTIVE-biased orbit from T235.)
  The safe prime 1019 of the over-represented block's Sophie Germain source
  lands in the most inactive-biased orbit.

211 × 137 mod 37 = 10 ∈ IC. IC is fixed by the 137-map.
509 × 137 mod 37 = 25 ∈ SA_ST_B. The orbit cycles within SA_ST_B.

=== TWIN PRIMES ===

509: not a twin prime (509+2=511=7×73, 509−2=507=3×169).
211: not a twin prime (211+2=213=3×71, 211−2=209=11×19).
91 = 7×13: not prime. But its factors 7∈D7 and 13∈CAS_EXT are from distinct orbits.

=== SOPHIE GERMAIN ===

509 is Sophie Germain: 2×509+1=1019 (prime). Chain: 509∈SA_ST_B → 1019∈DARK_A.
  Sophie map connects the most over-represented block (SA_ST_B) to the most
  inactive-biased orbit (DARK_A). Sophie Germain structure bridges active and
  inactive extremes.

=== RULE 30 ===

If the center column is normal, every computable statistical test passes —
including chi-squared, autocorrelation, spectral tests. The orbit-density
bias (T235) would then be a finite-N artifact that vanishes in the limit.
If the orbit bias persists as N→∞, normality fails.

The chi-squared evidence (ratio → 1) supports normality. The orbit bias
evidence (T235) provides a concrete candidate falsification: if orbit-level
density bias can be shown to persist for all N, the sequence is not normal.
"""

from collections import Counter
from statistics import mean

P    = 37
MULT = 26

IC      = {1, 10, 26}
DARK_A  = {2, 15, 20}
C3      = {3, 4, 30}
CAS_EXT = {5, 13, 19}
TESLA   = {6, 8, 23}
D7      = {7, 33, 34}
SA_ST_A = {9, 12, 16}
NEG_H   = {11, 27, 36}
C9      = {14, 29, 31}
NQR17   = {17, 22, 35}
SEED    = {18, 24, 32}
SA_ST_B = {21, 25, 28}

ORBITS = {
    'IC': IC, 'DARK_A': DARK_A, 'C3': C3, 'CAS_EXT': CAS_EXT,
    'TESLA': TESLA, 'D7': D7, 'SA_ST_A': SA_ST_A, 'NEG_H': NEG_H,
    'C9': C9, 'NQR17': NQR17, 'SEED': SEED, 'SA_ST_B': SA_ST_B,
}


def orb(n):
    r = n % P
    if r == 0: return 'SEAM'
    for name, s in ORBITS.items():
        if r in s: return name


def rule30_step(row):
    w = len(row)
    return [((30 >> (4*row[(i-1)%w] + 2*row[i] + row[(i+1)%w])) & 1) for i in range(w)]


def center_col(n_steps):
    W = 2*n_steps + 1
    row = [0]*W
    row[n_steps] = 1
    col = []
    for _ in range(n_steps):
        row = rule30_step(row)
        col.append(row[n_steps])
    return col


def run_assertions():
    from sympy import isprime

    N = 20000
    col = center_col(N)

    # ── Chi-squared ratios converge toward 1 ──────────────────────────────────
    ratios = {}
    for k in range(1, 11):
        n_windows = N - k + 1
        counts = Counter(tuple(col[i:i+k]) for i in range(n_windows))
        expected = n_windows / (2**k)
        chi2 = sum(
            (counts.get(tuple((n>>(k-1-j))&1 for j in range(k)), 0) - expected)**2 / expected
            for n in range(2**k)
        )
        ratios[k] = chi2 / (2**k - 1)

    # Ratio at k=10 should be close to 1 (within 5%)
    assert ratios[10] < 1.05, f"k=10 ratio={ratios[10]:.4f}"
    # Ratio at k=1 should be > 1 (non-normal at small k under finite N)
    assert ratios[1] > 1.5

    # ── All-ones over-represented for k=1..9 ──────────────────────────────────
    for k in range(1, 10):
        n_windows = N - k + 1
        counts = Counter(tuple(col[i:i+k]) for i in range(n_windows))
        expected = n_windows / (2**k)
        ones_block = tuple([1]*k)
        assert counts.get(ones_block, 0) > expected, \
            f"k={k}: all-ones block not over-represented"

    # ── Run-length analysis ────────────────────────────────────────────────────
    runs_1, runs_0 = [], []
    cur, cnt = col[0], 1
    for b in col[1:]:
        if b == cur:
            cnt += 1
        else:
            (runs_1 if cur == 1 else runs_0).append(cnt)
            cur, cnt = b, 1
    (runs_1 if cur == 1 else runs_0).append(cnt)

    mean_1 = mean(runs_1)
    mean_0 = mean(runs_0)
    # Both means should be within 5% of 2.0 (geometric p=0.5 mean)
    assert abs(mean_1 - 2.0) < 0.15, f"Mean run of 1s = {mean_1:.4f}"
    assert abs(mean_0 - 2.0) < 0.15, f"Mean run of 0s = {mean_0:.4f}"
    # Equal number of runs
    assert abs(len(runs_1) - len(runs_0)) <= 1

    # ── Extreme block analysis ─────────────────────────────────────────────────
    # k=10: most over = 509, least = 211
    n_windows_10 = N - 9
    counts_10 = Counter(tuple(col[i:i+10]) for i in range(n_windows_10))
    all_10 = [tuple((n>>(9-j))&1 for j in range(10)) for n in range(1024)]
    sorted_10 = sorted(all_10, key=lambda b: counts_10.get(b, 0))

    least_val = int(''.join(map(str, sorted_10[0])), 2)
    most_val  = int(''.join(map(str, sorted_10[-1])), 2)
    assert least_val == 211
    assert most_val  == 509

    # 509 mod 37 = 28 ∈ SA_ST_B
    assert 509 % P == 28 and 28 in SA_ST_B
    # 509 is Sophie Germain
    assert isprime(509) and isprime(2*509+1)
    # 137-map keeps SA_ST_B
    assert (509 % P * MULT) % P == 25 and 25 in SA_ST_B

    # 211 mod 37 = 26 ∈ IC
    assert 211 % P == 26 and 26 in IC
    assert isprime(211)
    # 137-map keeps IC
    assert (211 % P * MULT) % P == 10 and 10 in IC

    # 1019 = safe prime of 509; 1019 mod 37 ∈ DARK_A
    assert isprime(1019)
    assert 1019 % P == 20 and 20 in DARK_A

    # ── Density at N=20000 ────────────────────────────────────────────────────
    density = sum(col) / len(col)
    # Should be within 2% of 0.5
    assert abs(density - 0.5) < 0.02, f"Density = {density:.4f}"

    print("All assertions passed.")
    print()
    print("THEOREM 237: Rule 30 Normality — Block Frequency Convergence and GF(37) Extremes")
    print()
    print(f"Density at N={N}: {density:.6f}")
    print(f"Mean run of 1s: {mean_1:.4f}  (expected 2.0)")
    print(f"Mean run of 0s: {mean_0:.4f}  (expected 2.0)")
    print()
    print("Chi-squared ratio (chi2/df):")
    for k, r in sorted(ratios.items()):
        print(f"  k={k:2d}: {r:.4f}")
    print()
    print(f"k=10 most over-represented: 509 mod37=28 ∈ SA_ST_B (Sophie Germain; safe prime 1019 ∈ DARK_A)")
    print(f"k=10 least frequent:        211 mod37=26 ∈ IC      (137-map fixes IC)")
    print()
    tie_correction()


# ══════════════════════════════════════════════════════════════════════════════
# TIE CORRECTION (added after independent re-verification)
# ══════════════════════════════════════════════════════════════════════════════
#
# The measured quantities above re-verify exactly: density 0.5060 at N=20000,
# mean runs 2.011/1.964, max runs 13/14, chi2/df = 1.0168 at k=10, and the full
# chi2 table. Those stand.
#
# The EXTREME-BLOCK ORBIT INFERENCE does not. At k=10 the maximum count (33) is
# a THREE-WAY TIE, and the minimum count (7) is a TWO-WAY TIE:
#
#   k=10 max, count 33:   183 -> 35 ∈ NQR17
#                         409 ->  2 ∈ DARK_A
#                         509 -> 28 ∈ SA_ST_B      <- the one originally reported
#
#   k=10 min, count  7:   211 -> 26 ∈ IC          <- the one originally reported
#                         521 ->  3 ∈ C3
#
# The original claim — "the most over-represented block has its binary value in
# the most active-biased regular orbit" — selected 509 from a three-way tie.
# The tie also contains DARK_A, which this same theorem identifies as the MOST
# INACTIVE-biased orbit. The tie therefore spans both ends of the bias scale,
# so the orbit assignment of the maximum carries no information. Under T282 this
# is post-hoc label-fit: no possible outcome could have counted as a miss,
# because a tie member exists in orbits on both sides of the hypothesis.
#
# STATUS CHANGE:
#   k=10 max orbit inference  ->  WITHDRAWN (selection from an unbroken tie)
#   k=10 min orbit inference  ->  WITHDRAWN (selection from an unbroken tie)
#   k=9  max (91 -> NQR17)    ->  STANDS. Verified as a genuine 1-way maximum.
#   k=8  max                  ->  2-way tie (117->TESLA, 157->SA_ST_A); no claim made.
#   chi2 / density / runs     ->  STAND. Re-verified to 3-4 decimals.
#
# The arithmetic about 509 and 211 is all correct and stays: 509 is prime and
# Sophie Germain (1019 prime), 211 is prime and is not. What is withdrawn is
# only the inference that their ORBITS explain their block frequencies.
#
# Separate note on a 0-bit statement: "the 137-map keeps 509's orbit SA_ST_B"
# and "the 137-map fixes IC" are true but forced — EVERY orbit is preserved by
# the 137-map, since that is what makes it an orbit. These sentences describe
# the definition, not a property of 509 or 211.

def center_col_fast(n_steps):
    """Bitwise Rule 30 center column. Same convention as center_col():
    the value is recorded AFTER each step."""
    W = 2 * n_steps + 5
    mask = (1 << W) - 1
    c = W // 2
    row = 1 << c
    col = bytearray(n_steps)
    for i in range(n_steps):
        row = ((row << 1) ^ (row | (row >> 1))) & mask
        col[i] = (row >> c) & 1
    return col


def tie_correction(col=None):
    """Recompute the k=8,9,10 extremes and report the FULL tie sets."""
    if col is None:
        col = center_col_fast(20000)
    print("TIE CORRECTION — full extreme sets (not single representatives):")
    for k in (8, 9, 10):
        m = (1 << k) - 1
        cnt = {}
        v = 0
        for idx in range(len(col)):
            v = ((v << 1) | col[idx]) & m
            if idx >= k - 1:
                cnt[v] = cnt.get(v, 0) + 1
        freq = {b: cnt.get(b, 0) for b in range(1 << k)}
        mx, mn = max(freq.values()), min(freq.values())
        top = sorted(b for b in freq if freq[b] == mx)
        bot = sorted(b for b in freq if freq[b] == mn)
        print(f"  k={k}: max={mx} ({len(top)}-way tie) "
              f"{[(b, b % 37, orb(b)) for b in top]}")
        print(f"       min={mn} ({len(bot)}-way tie) "
              f"{[(b, b % 37, orb(b)) for b in bot[:4]]}"
              f"{' ...' if len(bot) > 4 else ''}")
    print()
    print("  k=10 max and min are BOTH ties -> orbit inferences WITHDRAWN.")
    print("  k=9 max (91 -> NQR17) is a genuine 1-way maximum -> STANDS.")


if __name__ == "__main__":
    run_assertions()
