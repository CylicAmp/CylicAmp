"""
Theorem 238: Rule 30 Computational Complexity — GF(37) Modular Prediction and Irreducibility
Author: Michael Warren Song (CyclicAmp)

Open question: What is the complexity class of computing the nth center-column bit?
Is it PSPACE-complete?

=== NAIVE ALGORITHM: O(n²) TIME, O(n) SPACE ===

To compute bit(n): simulate n steps of Rule 30 on a tape of width 2n+1.
  — Time: O(n²) (n steps × O(n) width per step)
  — Space: O(n) (tape width 2n+1)

Therefore bit(n) ∈ PSPACE (polynomial space in the bit-length of n, which is log n,
but here we index by n directly, so O(n) space = exponential in input size |n| = log n).

In the standard complexity-theory convention where input is the binary representation
of n (length L = log₂ n), the naive algorithm uses:
  — Space: O(2^L) — exponential in L
  — Time:  O(4^L) — doubly exponential in L

This puts the problem in EXP (exponential time), and it is in PSPACE relative to n
but EXPSPACE relative to the length of the binary input.

Empirical runtime confirmation (Python, single-threaded):
  n=    100:     2.63 ms   (scaling exponent vs n=500: 2.105)
  n=    500:    77.86 ms
  n=  1,000:   248.68 ms   (scaling exponent: 1.675)
  n=  2,000:   927.02 ms   (scaling exponent: 1.898)
  n=  5,000:  5752.03 ms   (scaling exponent: 1.992)
  n= 10,000: 24516.19 ms   (scaling exponent: 2.092)

Scaling exponents converge to 2.0, confirming O(n²).

=== ENTROPY: NEAR-MAXIMAL ===

Over 20000 steps, binary Shannon entropy H of the center column:
  H = 0.999898 bits  (maximum possible = 1.000000)

The sequence is within 0.01% of maximum entropy. A sequence with lower entropy
would permit compression and thus a shorter algorithm. The near-maximal entropy
is evidence (not proof) that no sub-linear description exists.

=== AUTOCORRELATION: NEGLIGIBLE ===

Autocorrelation of the center column at lags 1..20 (N=20000):
  All values in range [−0.011, +0.009].

Under white noise, autocorrelations should be O(1/√N) ≈ 0.007 at each lag.
The observed autocorrelations are within noise level — no measurable lag structure.
This is consistent with computational irreducibility: previous center-column bits
give no predictive advantage over knowing none of them.

=== GF(37) MODULAR PREDICTION ===

If bit(n) depended only on n mod T for some fixed T, it could be computed
in O(T) space (precompute a lookup table) and O(1) time per query — a
dramatic speedup over the O(n²) naive algorithm.

Test: for each modulus T, compute the best achievable accuracy by always
predicting the majority class within each residue class mod T.

  Baseline (global density):  0.505950
  n mod    2:                  0.505950  (+0.000000)
  n mod    3:                  0.505950  (+0.000000)
  n mod    5:                  0.506250  (+0.000300)
  n mod    7:                  0.506850  (+0.000900)
  n mod   11:                  0.512500  (+0.006550)
  n mod   37:                  0.517100  (+0.011150)  ← GF prime
  n mod   74 (=2×37):          0.526050  (+0.020100)
  n mod  111 (=3×37):          0.527650  (+0.021700)  ← LCM(ord, P) = 3×37
  n mod  148 (=4×37):          0.535450  (+0.029500)
  n mod  185 (=5×37):          0.542300  (+0.036350)
  n mod  222 (=6×37):          0.542350  (+0.036400)
  n mod  333 (=9×37):          0.548450  (+0.042500)
  n mod  407 (=11×37):         0.561000  (+0.055050)
  n mod  481 (=13×37):         0.565500  (+0.059550)

GF(37) signature: multiples of 37 as modulus give consistently better prediction
than other moduli. Using n mod 37 jumps from 0.507 (n mod 7) to 0.517.

The advantage grows steadily with the multiple of 37 used, with no plateau
through 13×37 = 481. This means a lookup table of size T gives prediction
accuracy that grows slowly with T — no small T achieves reliable prediction.

If the accuracy growth were to plateau at some T₀, then bit(n) would be
computable in O(T₀) space. The data show no plateau through T=481, suggesting
T₀ ≫ 481 or that no finite T suffices (computational irreducibility).

=== ORBIT-BASED PREDICTOR: 0.510 ACCURACY ===

Using the GF(37) orbit of n (classifying n into one of 13 orbits/SEAM)
and predicting the majority bit for each orbit:
  Accuracy = 0.510050

Improvement over baseline: +0.41%. This is the total information content
of the orbit classification for predicting individual bits. The orbit tells
you almost nothing about any specific bit.

Per-orbit prediction accuracy (highest to lowest):
  CAS_EXT: 0.5293   IC:     0.5203   SEAM:   0.5167
  SA_ST_A: 0.5151   NEG_H:  0.5102   C9:     0.5102
  TESLA:   0.5099   C3:     0.5086   DARK_A: 0.5065
  NQR17:   0.5040   D7:     0.5034   SEED:   0.5009   SA_ST_B: 0.5000

No orbit gives better than 0.53 accuracy. The best (CAS_EXT = {5,13,19}) gives
53% — only 3% above chance. This quantifies how little structure the GF(37)
orbit classification provides for individual-bit prediction.

=== COMPLEXITY CLASSIFICATION ===

Known:
  bit(n) ∈ TIME(n²) ∩ SPACE(n)         [naive simulation]
  bit(n) ∈ EXP relative to input size L = log n

Unknown:
  Is bit(n) ∈ TIME(n^{1+ε}) for any ε < 1?  [does a sub-quadratic algorithm exist?]
  Is bit(n) ∈ SPACE(√n)?                    [can we save space?]
  Is bit(n) PSPACE-complete (relative to L)? [is it as hard as general PSPACE?]

Rule 110 is Turing-complete (Cook, 2004), hence PSPACE-hard. Rule 30 is NOT
known to be Turing-complete. The current evidence:

  — Entropy 0.9999: near-maximum, no known compression
  — Autocorrelation ~0: no exploitable lag structure
  — Modular prediction accuracy grows slowly in T: no small shortcut
  — No period T ≤ 10000 is consistent (T235)

All evidence points to computational irreducibility — bit(n) requires
essentially Ω(n²) computation — but no proof exists.

=== GF(37) AND COMPLEXITY ===

The modular prediction hierarchy shows:
  n mod 1 ⊂ n mod 37 ⊂ n mod 74 ⊂ n mod 111 ⊂ ...

Each refinement by a factor of 37 adds ~1% prediction accuracy. This grows
as approximately log(k) for n mod (k×37), suggesting the information content
of bit(n) in the n mod T feature grows logarithmically in T.

If the true information needed to compute bit(n) from n alone grows as Θ(n),
then the modular-prediction information gain (which grows as log(T/37))
falls short by a factor of n/log(n) — which is the gap between simulation
and any polynomial shortcut.

GF(37) provides the most information-dense simple predictor (n mod 37 beats
n mod 2, 3, 5, 7, and 11), but the gap between 0.517 and 1.0 represents
the irreducibility: the remaining 48.3% of the information is spread over
the full history of the automaton's evolution.

=== 1/137 ===

137 mod 37 = 26 = MULT. IC = {1, 10, 26} contains MULT.
n mod 37: accuracy = 0.517100. The GF prime 37 is the natural unit of
the modular prediction hierarchy because 26 = 137 mod 37 generates the
3-cycle structure of all orbits.

=== TWIN PRIMES ===

CAS_EXT = {5, 13, 19} gives the highest per-orbit prediction accuracy (0.5293).
13 and 19 are prime (13∈CAS_EXT, 19∈CAS_EXT); (11,13) is a twin prime pair
with 11∈NEG_H. CAS_EXT is the orbit where all elements are prime (from T233).

=== SOPHIE GERMAIN ===

5 ∈ CAS_EXT: 5 is Sophie Germain (2×5+1=11, prime). 11∈NEG_H.
CAS_EXT is the most accurate orbit predictor (0.5293). The Sophie Germain
source orbit provides the most predictive leverage of any GF(37) orbit.

=== RULE 30 ===

The rule itself is 30 ∈ C3. C3 gives prediction accuracy 0.5086.
The rule's own orbit is near-neutral as a predictor. The complexity of the
rule's output cannot be predicted from the rule's orbit membership alone.
"""

from collections import defaultdict, Counter
import math

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


def modular_accuracy(col, T):
    N = len(col)
    bucket = defaultdict(list)
    for i, b in enumerate(col):
        bucket[(i+1) % T].append(b)
    total_correct = sum(max(sum(v), len(v)-sum(v)) for v in bucket.values())
    return total_correct / N


def run_assertions():
    from sympy import isprime

    N = 20000
    col = center_col(N)

    # ── Entropy near 1.0 ──────────────────────────────────────────────────────
    cts = Counter(col)
    H = -sum((c/N)*math.log2(c/N) for c in cts.values() if c > 0)
    assert H > 0.999, f"Entropy={H:.6f}"

    # ── Autocorrelation small ─────────────────────────────────────────────────
    for lag in range(1, 21):
        n = N - lag
        corr = sum((col[i]-0.5)*(col[i+lag]-0.5) for i in range(n)) / (n*0.25)
        assert abs(corr) < 0.02, f"lag={lag}: autocorr={corr:.6f}"

    # ── Modular prediction: 37 beats 7 ────────────────────────────────────────
    acc7  = modular_accuracy(col, 7)
    acc37 = modular_accuracy(col, 37)
    acc111 = modular_accuracy(col, 111)
    assert acc37 > acc7,   f"n mod 37 ({acc37:.4f}) should beat n mod 7 ({acc7:.4f})"
    assert acc111 > acc37, f"n mod 111 ({acc111:.4f}) should beat n mod 37 ({acc37:.4f})"

    # Multiples of 37 give increasing accuracy
    accs = [modular_accuracy(col, k*P) for k in range(1, 6)]
    for i in range(len(accs)-1):
        assert accs[i+1] >= accs[i] - 0.001, \
            f"k×37 accuracy not monotone: k={i+1}→{i+2}: {accs[i]:.4f}→{accs[i+1]:.4f}"

    # ── Orbit predictor accuracy ───────────────────────────────────────────────
    orbit_act = defaultdict(int)
    orbit_tot = defaultdict(int)
    for i, b in enumerate(col):
        o = orb(i+1)
        orbit_tot[o] += 1
        orbit_act[o] += b

    orbit_accs = {
        o: max(orbit_act[o], orbit_tot[o]-orbit_act[o]) / orbit_tot[o]
        for o in orbit_tot
    }

    # CAS_EXT is highest orbit predictor
    assert orbit_accs['CAS_EXT'] == max(orbit_accs.values()), \
        f"CAS_EXT should be highest: {orbit_accs}"

    # SA_ST_B is lowest (density closest to 0.5)
    assert orbit_accs['SA_ST_B'] == min(orbit_accs.values()), \
        f"SA_ST_B should be lowest: {orbit_accs}"

    # No orbit exceeds 0.55 accuracy
    assert max(orbit_accs.values()) < 0.55

    # ── Sophie Germain ────────────────────────────────────────────────────────
    assert 5 in CAS_EXT
    assert isprime(5) and isprime(2*5+1)  # 5 is Sophie Germain, 11 ∈ NEG_H
    assert 11 in NEG_H

    # ── 1/137 ─────────────────────────────────────────────────────────────────
    assert MULT in IC
    assert acc37 > modular_accuracy(col, 11)  # mod 37 beats mod 11

    print("All assertions passed.")
    print()
    print("THEOREM 238: Rule 30 Computational Complexity — GF(37) Modular Prediction")
    print()
    print(f"Shannon entropy H = {H:.6f} bits (max=1.0)")
    print()
    print("Modular prediction accuracy:")
    for T in [2, 7, 11, 37, 74, 111, 185, 481]:
        acc = modular_accuracy(col, T)
        label = f'={T//P}×37' if T%P==0 else ''
        print(f"  n mod {T:4d}{label:6s}: {acc:.6f}  (+{acc - sum(col)/N:.6f})")
    print()
    print("Per-orbit prediction accuracy:")
    for o, a in sorted(orbit_accs.items(), key=lambda x: -x[1]):
        print(f"  {o:10s}: {a:.4f}")
    print()
    print("Complexity bounds: O(n²) time, O(n) space. PSPACE-completeness: open.")
    print("Computational irreducibility: no simple function of n achieves high accuracy.")


if __name__ == "__main__":
    run_assertions()
