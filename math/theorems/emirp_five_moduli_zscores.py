"""
emirp_five_moduli_zscores.py

Multi-modulus digit-aware Z-scores for m in {29, 31, 37, 41, 43}.
Tests specificity: 37|999 (ord10=3) vs four non-resonant moduli.

If the 37 Z-curve grows while all others stay near zero, the case for
a genuine emirp/reversal-residue coupling is considerably stronger.
"""

import random
import math
import numpy as np

# ---------------------------------------------------------------------------
# Sieve up to 1,000,000
# ---------------------------------------------------------------------------
LIMIT = 1_000_001
sieve = bytearray([1]) * (LIMIT + 1)
sieve[0] = sieve[1] = 0
for i in range(2, int(LIMIT**0.5) + 1):
    if sieve[i]:
        sieve[i*i::i] = bytearray(len(sieve[i*i::i]))

def is_prime(n): return bool(sieve[n]) if 0 <= n <= LIMIT else False
def rev_int(n):  return int(str(n)[::-1])

def is_emirp(p):
    if not is_prime(p) or str(p).endswith('0'): return False
    r = rev_int(p)
    return r != p and is_prime(r)

def sample_digit_prime(p, rng, max_tries=60):
    digits = list(str(p))
    for _ in range(max_tries):
        rng.shuffle(digits)
        if digits[0] == '0': continue
        n = int(''.join(digits))
        if is_prime(n): return n
    return None

def chi2_r(counts, mod):
    c = counts[1:]
    s = sum(c)
    if s == 0: return 0.0
    exp = s / (mod - 1)
    return sum((x - exp)**2 / exp for x in c)

def null_ensemble(emirps, mod, S=200, seed=0):
    rng = random.Random(seed)
    results = []
    for _ in range(S):
        counts = [0] * mod
        for p in emirps:
            q = sample_digit_prime(p, rng)
            if q is not None:
                counts[q % mod] += 1
        results.append(chi2_r(counts, mod))
    return np.array(results)

def obs_chi2(emirps, mod):
    counts = [0] * mod
    for p in emirps:
        counts[p % mod] += 1
    return chi2_r(counts, mod)

# ---------------------------------------------------------------------------
# Precompute all emirps up to 10^6
# ---------------------------------------------------------------------------
ALL_EMIRPS = [p for p in range(2, LIMIT) if is_emirp(p)]
print(f"Total emirps in [2, {LIMIT-1:,}]: {len(ALL_EMIRPS):,}")

MODULI = [29, 31, 37, 41, 43]

# ord10 and 999-divisibility (computed above)
ORD10 = {29: 28, 31: 15, 37: 3, 41: 5, 43: 21}
DIV999 = {m: (999 % m == 0) for m in MODULI}

# ---------------------------------------------------------------------------
# 1.  Single scale X = 10^6 — all five moduli
# ---------------------------------------------------------------------------
print()
print("=" * 66)
print("1.  Five-modulus digit-aware Z-scores  (X=10^6, N=11,241)")
print("=" * 66)
print(f"  {'m':>3}  {'ord10':>6}  {'999|m':>6}  {'χ²_obs':>8}  "
      f"{'μ_null':>8}  {'σ_null':>7}  {'Z_ens':>7}  verdict")
print(f"  {'-'*66}")

z_scores_1M = {}
for mod in MODULI:
    c2_obs = obs_chi2(ALL_EMIRPS, mod)
    null   = null_ensemble(ALL_EMIRPS, mod, S=200, seed=mod * 100)
    mu, sig = null.mean(), null.std(ddof=1)
    Z = (c2_obs - mu) / (sig + 1e-10)
    z_scores_1M[mod] = Z
    verdict = "SIGNAL" if Z > 2.0 else ("borderline" if Z > 1.5 else "null")
    print(f"  {mod:>3}  {ORD10[mod]:>6}  {str(DIV999[mod]):>6}  "
          f"{c2_obs:>8.2f}  {mu:>8.2f}  {sig:>7.3f}  {Z:>+7.3f}  {verdict}")

print()
print(f"  Only m=37 has 37|999 (ord10=3). Others have 29∤999, 31∤999, 41∤999, 43∤999.")
print(f"  If 37 is the only persistent positive Z, the coupling is specific to ord10=3.")


# ---------------------------------------------------------------------------
# 2.  Scaling trajectory for all five moduli
# ---------------------------------------------------------------------------
print()
print("=" * 66)
print("2.  Scaling trajectory  Z(X)  — all five moduli")
print("=" * 66)

X_VALUES = [10**4, 30_000, 100_000, 300_000, 10**6]
S_SCALE  = 150

header = "  {:>8}  {:>5}".format("X", "N")
for m in MODULI:
    header += f"  Z_{m:>2}"
print(header)
print(f"  {'-'*56}")

traces = {m: [] for m in MODULI}
logX   = []

for X in X_VALUES:
    em_X = [p for p in ALL_EMIRPS if p <= X]
    N_X  = len(em_X)
    row  = f"  {X:>8,}  {N_X:>5}"
    logX.append(math.log10(X))
    for mod in MODULI:
        c2 = obs_chi2(em_X, mod)
        nl = null_ensemble(em_X, mod, S=S_SCALE, seed=mod + X)
        Z  = (c2 - nl.mean()) / (nl.std(ddof=1) + 1e-10)
        traces[mod].append(Z)
        row += f"  {Z:>+5.2f}"
    print(row)

print()
slopes = {}
for m in MODULI:
    slopes[m] = float(np.polyfit(logX, traces[m], 1)[0])
print(f"  Slopes dZ/d(log10 X):")
for m in MODULI:
    flag = "  ← 37|999" if m == 37 else ""
    print(f"    m={m}: {slopes[m]:>+7.3f}{flag}")


# ---------------------------------------------------------------------------
# 3.  Summary table
# ---------------------------------------------------------------------------
print()
print("=" * 66)
print("3.  Summary: Specificity Test")
print("=" * 66)
print(f"""
  Prediction: m=37 (37|999, ord10=3) → Z_ens growing positive.
              m∈{{29,31,41,43}} (none divide 999) → Z_ens near zero.

  Result:
    m=37: Z(10^6)={z_scores_1M[37]:+.3f}, slope={slopes[37]:+.3f}
    m=29: Z(10^6)={z_scores_1M[29]:+.3f}, slope={slopes[29]:+.3f}
    m=31: Z(10^6)={z_scores_1M[31]:+.3f}, slope={slopes[31]:+.3f}
    m=41: Z(10^6)={z_scores_1M[41]:+.3f}, slope={slopes[41]:+.3f}
    m=43: Z(10^6)={z_scores_1M[43]:+.3f}, slope={slopes[43]:+.3f}

  The algebraic coupling p−rev(p) ≡ 25(a−c) mod 37 is SPECIFIC to 37|999.
  Digit-aware Z-score separates 37 from its neighbors iff the emirp filter
  creates residue bias beyond digit content.

  Decision rule:
    slope(37) > 2 × max(slope for m≠37) → coupling confirmed, specific.
    slope(37) ≤ 2 × max(others)          → coupling not uniquely isolated yet.

  Ratio slope(37) / max(other slopes): {slopes[37] / max(slopes[m] for m in MODULI if m!=37):.2f}
""")
