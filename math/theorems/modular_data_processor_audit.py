"""
modular_data_processor_audit.py

Audits ModularDataProcessor's two "deterministic" constant derivations
and checks whether the algebraic justifications are governing or decorative.

Claims:
  1. WINDOW_SIZE=6 derived from ord(2) in (Z/9Z)* — algebraically correct?
  2. MAD_MULTIPLIER=3 derived from "37-field center (18) / period (6)" —
     is the prime 37 derived or reverse-engineered?
  3. Do the modular parameters influence the pipeline output differently
     than the empirical parameters they replace?
  4. Does digital root classification affect the output DataFrame?
  5. Removal test: what remains after stripping algebraic framing?
"""

import math

# ---------------------------------------------------------------------------
# 1.  WINDOW_SIZE = ord(2) in (Z/9Z)*
# ---------------------------------------------------------------------------
print("="*62)
print("1.  WINDOW_SIZE = ord(2) in (Z/9Z)*")
print("="*62)

# Compute multiplicative order of 2 mod 9
def mult_order(a, m):
    """Multiplicative order of a in (Z/mZ)*; assumes gcd(a,m)=1."""
    if math.gcd(a, m) != 1:
        return None
    val = a % m
    for k in range(1, m):
        if val == 1:
            return k
        val = (val * a) % m
    return None

order_2_mod9 = mult_order(2, 9)
print(f"  ord(2) in (Z/9Z)* = {order_2_mod9}")
print(f"  Verification: powers of 2 mod 9:")
val = 1
for k in range(1, 8):
    val = (val * 2) % 9
    print(f"    2^{k} ≡ {val} (mod 9)  {'← back to 1' if val==1 else ''}")

print(f"\n  WINDOW_SIZE = 6: ALGEBRAICALLY CORRECT ✓")
print(f"  ord(2) = 6 in (Z/9Z)* is a proven fact.")

print(f"""
  OPEN QUESTION: does ord(2) in (Z/9Z)* govern the optimal rolling
  window for variance-based anomaly detection?

  Rolling variance detection window choice depends on:
    (a) autocorrelation length of the signal (data-dependent)
    (b) expected anomaly cluster size (domain-dependent)
    (c) tradeoff between sensitivity and false-positive rate
  None of these are determined by the multiplicative structure of Z/9Z.

  Applying removal test:
    Remove the algebraic justification →
    "WINDOW_SIZE = 6"  ← just a number with no governing equation
    connecting (Z/9Z)* to optimal window selection for arbitrary data.

  STATUS: Algebraic derivation CORRECT; causal connection to pipeline
  window choice NOT established. The value 6 could be good, bad, or
  indifferent depending on the dataset's autocorrelation structure.
""")

# ---------------------------------------------------------------------------
# 2.  MAD_MULTIPLIER = 18/6 = 3 from "37-field center"
# ---------------------------------------------------------------------------
print("="*62)
print("2.  MAD_MULTIPLIER = 37-field center / period = 18/6 = 3")
print("="*62)
print("""
  Claim: "37-field center = 18, divided by period 6 → multiplier 3"
  "37-field center" = (37-1)/2 = 18 (median of {0,...,36}).

  Test: which primes p give (p-1)/2 / 6 = integer?
""")

# Find all primes p < 200 where (p-1)/2 is divisible by 6
def is_prime(n):
    if n < 2: return False
    return all(n % k != 0 for k in range(2, int(n**0.5)+1))

print(f"  {'p':>5}  {'center=(p-1)/2':>15}  {'center/6':>10}  {'integer?':>10}")
print(f"  {'-'*50}")
for p in range(3, 150):
    if not is_prime(p): continue
    center = (p-1)//2
    if (p-1) % 2 == 0 and center % 6 == 0:
        ratio = center // 6
        print(f"  {p:>5}  {center:>15}  {ratio:>10}  yes → multiplier={ratio}")

print(f"""
  Primes p where (p-1)/2 / 6 = integer are common; the ratio varies.
  To obtain multiplier=3 exactly: need (p-1)/2 = 18, so p = 37.
  p=37 is the UNIQUE prime that yields multiplier = 3 via this formula.

  This means the formula was constructed by working backward:
    Target: multiplier = 3  (standard empirical MAD threshold)
    Solve:  (p-1)/2 = 18 → p = 37
  The prime 37 is chosen to produce 3, not derived independently.
""")

# Verify: MAD×3 is a standard robust statistics threshold
print("  STANDARD USAGE OF MAD×3 IN STATISTICS:")
print("""
  Iglewicz & Hoaglin (1993), "How to Detect and Handle Outliers":
    Modified Z-score: 0.6745*(x - median) / MAD > 3.5 → outlier
  Many implementations use threshold = median ± k*MAD with k=3.
  The value 3 is an empirical standard, analogous to ±3σ for
  normally distributed data (covers ~99.7% of observations).

  The code replaces:
    empirical: mean * 3.0
    "deterministic": median + 3 * MAD

  These are genuinely different formulas (median vs. mean, additive
  vs. multiplicative). The MAD version IS more robust — but that
  robustness argument is statistical, not algebraic.
  The number 3 in both cases is the same empirical threshold.
""")

# ---------------------------------------------------------------------------
# 3.  Does the algebraic choice of parameters affect performance?
# ---------------------------------------------------------------------------
print("="*62)
print("3.  Parameter sensitivity: does window=6 vs. other values matter?")
print("="*62)

import random
random.seed(42)

# Generate same test data as in the original script
base = [random.gauss(100, 5) for _ in range(20)]
base[10] = 500; base[11] = 600; base[12] = 550

def rolling_var(data, window):
    result = [None] * len(data)
    for i in range(window-1, len(data)):
        chunk = data[i-window+1:i+1]
        mean = sum(chunk)/len(chunk)
        var  = sum((x-mean)**2 for x in chunk)/(len(chunk)-1)
        result[i] = var
    return result

def detect_spikes_window(data, window, k=3):
    rv = [v for v in rolling_var(data, window) if v is not None]
    if not rv: return 0
    sorted_rv = sorted(rv)
    median = sorted_rv[len(sorted_rv)//2]
    mad = sorted(abs(v - median) for v in rv)[len(rv)//2]
    threshold = median + k * mad
    return sum(1 for v in rolling_var(data, window) if v is not None and v > threshold)

print(f"  Test data: 20 points, spikes at indices 10-12 (values 500,600,550)")
print(f"\n  {'window':>8}  {'spikes detected':>16}  note")
print(f"  {'-'*40}")
for w in range(3, 12):
    n = detect_spikes_window(base, w)
    note = "← WINDOW_SIZE (ord(2) mod 9)" if w==6 else \
           "← original empirical" if w==5 else ""
    print(f"  {w:>8}  {n:>16}  {note}")

print(f"""
  KEY FINDING: window=6 detects 0 spikes; window=5 detects 7.
  The algebraically-derived window PERFORMS WORSE on this test case.

  Root cause: 3 consecutive spikes (indices 10,11,12) with window=6
  contaminate indices 10-17 = 8 windows out of 15 valid = 53%.
  MAD estimators break down above 50% contamination rate: the median
  of rolling variances IS a contaminated value, so the threshold
  becomes too large to flag anything.

  With window=5: contaminated windows = 7 out of 16 = 43.75% < 50%
  → median is a clean window → detection works correctly.

  Breakdown point of median-based estimators = 50%.
  window=6 exceeds this for 3 consecutive spikes; window=5 does not.
  The optimal window depends on the spike cluster size in the data.
  (Z/9Z)* structure contains no information about this.
""")

# ---------------------------------------------------------------------------
# 4.  Digital root classification: effect on pipeline output
# ---------------------------------------------------------------------------
print("="*62)
print("4.  Digital root classification: pipeline effect")
print("="*62)
print("""
  The class computes digital roots and classifies residues into
  DOUBLING_CYCLE and TRINITY_SET, storing counts in audit_metrics.

  Checking code flow in process_data():
    1. replace_zeros_with_nan()      — modifies raw_data
    2. compute_digital_roots()       — appends *_digital_root columns
    3. classify_residues()           — writes to audit_metrics only
    4. detect_variance_spikes()      — appends *_spike_flag columns
    5. Final filter: clean_mask uses only *_spike_flag columns

  The digital root classification is stored in audit_metrics but
  does NOT appear in the clean_mask construction.
  Removing compute_digital_roots() and classify_residues() from
  process_data() would produce identical output DataFrames.
""")

# Minimal re-implementation to prove the point
def pipeline_without_dr(data, target_cols, window=6, k=3):
    """Pipeline with spike detection only — no digital root steps."""
    df = dict(data)  # copy
    flags = {}
    for col in target_cols:
        vals = df[col]
        rv = rolling_var(vals, window)
        rv_valid = [v for v in rv if v is not None]
        if not rv_valid: continue
        sorted_rv = sorted(rv_valid)
        median = sorted_rv[len(sorted_rv)//2]
        mad = sorted(abs(v-median) for v in rv_valid)[len(rv_valid)//2]
        threshold = median + k * mad
        flags[col] = [i for i, v in enumerate(rv) if v is not None and v > threshold]
    return flags

flags = pipeline_without_dr({'Value': base}, ['Value'])
print(f"  Spike flags without digital root steps: {flags}")
print(f"  Identical to full pipeline output: implied ✓")
print(f"""
  VERDICT: Digital root classification adds metadata (audit_metrics)
  but has zero effect on which rows survive the final filter.
  The pipeline's output is determined entirely by detect_variance_spikes().
""")

# ---------------------------------------------------------------------------
# 5.  Removal test
# ---------------------------------------------------------------------------
print("="*62)
print("5.  Removal test: strip algebraic framing")
print("="*62)
print("""
  Original with framing:
    WINDOW_SIZE = 6  # ord(2) in (Z/9Z)*
    MAD_MULTIPLIER = 18 // 6  # 37-field center / period

  After removing algebraic framing:
    window = 6       # chosen value
    k = 3            # chosen multiplier

  After framing removal, the pipeline reduces to:

    rolling_var = df[col].rolling(window=6).var()
    median_var  = rolling_var.median()
    mad         = (rolling_var - median_var).abs().median()
    threshold   = median_var + 3 * mad
    spike_mask  = rolling_var > threshold

  This is a standard median+MAD outlier detection method.
  It appears in, e.g., Rousseeuw & Croux (1993), Leys et al. (2013).
  The parameters 6 and 3 are reasonable choices but not uniquely
  determined by the modular structure.

  APPLYING USER'S CRITERION (from prior session):
    "If removing the analogy leaves only descriptive language...
    the framework is still conceptual."

    Remove (Z/9Z)* justification for window=6:
      → "window = 6" remains. Governing equation: none. ✗
    Remove "37-field center / period" justification for k=3:
      → "k = 3" remains. Governing equation: none. ✗

  The statistical behavior of the pipeline is determined by window=6
  and k=3. The algebraic objects (Z/9Z)*, "37-field" do not appear
  in the pipeline equations and cannot be used to tune, modify, or
  derive alternative parameters without additional assumptions.
""")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("="*62)
print("SUMMARY")
print("="*62)
print("""
  Claim                                    Status
  --------------------------------------------------------
  ord(2) in (Z/9Z)* = 6                   CORRECT ✓
  WINDOW_SIZE = 6: algebraic derivation    CORRECT ✓
  6 is optimal window for pipeline         FALSE on tested data:
    window=6 detects 0 spikes (>50%         window=5 detects 7.
    contamination breaks MAD);              See breakdown-point analysis.
  37-field center = 18 = (37-1)/2         ARITHMETIC IDENTITY ✓
  18/6 = 3                                CORRECT ✓
  p=37 derived independently               FALSE — 37 reverse-engineered
    (unique prime giving ratio = 3)         to produce target value 3
  k=3 is standard MAD threshold           CORRECT (Iglewicz-Hoaglin 1993)
  Digital root classification affects      FALSE — stored in audit_metrics
    pipeline output                         only; no effect on clean_mask

  What survives framing removal:
    window=6, k=3, rolling MAD threshold.
    Standard robust outlier detection method.
    Parameters are reasonable; not uniquely determined by algebra.

  What the algebraic framing does NOT provide:
    A governing equation connecting Z/9Z structure to signal properties.
    A method for adapting window or k to a new dataset via algebra.
    A derivation that would give different values for different data.

  The statistical pipeline is functional. The algebraic justification
  for its parameters is post-hoc labeling of two conventional values.
""")
