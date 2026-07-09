#!/usr/bin/env python3
"""
phase_gap_correlation_audit.py

Pearson correlation between prime-gap digital-root phases and raw gaps.
Sample: first 100 prime gaps (primes[1]−primes[0] through primes[100]−primes[99]).

Phase mapping: phase(gap) = (DR(gap) / 9) * 2π
DR(gap) is a positive linear rescaling of phase, so:
  r(phase, gap) = r(DR(gap), gap)  exactly (invariance under positive linear transform)

─────────────────────────────────────────────────────────────────
COPY-PASTE READY: run with  python3 phase_gap_correlation_audit.py
Requires: Python 3.6+, numpy
─────────────────────────────────────────────────────────────────
"""

import numpy as np

FAIL = []

def check(cond, label, actual=None, expected=None):
    if not cond:
        FAIL.append(f"  ✗  {label}  actual={actual!r}  expected={expected!r}")
    return cond

def generate_primes(n):
    sieve = [True] * (n * 10)
    sieve[0] = sieve[1] = False
    primes = []
    for i in range(2, len(sieve)):
        if sieve[i]:
            primes.append(i)
            if len(primes) >= n:
                break
            for j in range(i * i, len(sieve), i):
                sieve[j] = False
    return primes

def digital_root(n):
    return 0 if n == 0 else 1 + ((n - 1) % 9)

def run():
    print("\n" + "=" * 60)
    print("PHASE-GAP CORRELATION AUDIT")
    print("=" * 60)

    # ── PRIMES AND GAPS ──────────────────────────────────────────
    primes = generate_primes(1001)
    check(len(primes) >= 1001, "generate_primes(1001) yields >= 1001 primes",
          len(primes), 1001)
    check(primes[0] == 2, "first prime = 2", primes[0], 2)

    gaps_all = np.array([primes[i + 1] - primes[i] for i in range(1000)])
    gaps     = gaps_all[:100]

    # ── DR AND PHASE ─────────────────────────────────────────────
    dr_arr  = np.array([digital_root(int(g)) for g in gaps])
    phases  = dr_arr * (2 * np.pi / 9)

    # Verify phase = DR * (2π/9) for every cell
    for i in range(100):
        expected_phase = digital_root(int(gaps[i])) * (2 * np.pi / 9)
        check(abs(phases[i] - expected_phase) < 1e-12,
              f"phase[{i}] = DR({int(gaps[i])}) * 2π/9",
              phases[i], expected_phase)

    # ── FOLDED GAPS (DR(gap) ≠ gap) ──────────────────────────────
    print(f"\n  Gap range: min={int(gaps.min())}  max={int(gaps.max())}")
    folded = {g: digital_root(g) for g in sorted(set(int(g) for g in gaps))
              if digital_root(g) != g}
    print(f"  Gaps where DR(gap) ≠ gap (modular folding):")
    for g, dr in folded.items():
        count = int(np.sum(gaps == g))
        print(f"    gap={g:2d}  DR={dr}  (appears {count}× in first 100)")
    check(len(folded) > 0, "at least one gap > 9 exists (folding fires)", len(folded), ">0")

    # ── PEARSON r ────────────────────────────────────────────────
    r_phase = np.corrcoef(phases,  gaps)[0, 1]
    r_dr    = np.corrcoef(dr_arr,  gaps)[0, 1]

    # r(phase, gap) == r(DR, gap) to machine epsilon
    check(abs(r_phase - r_dr) < 1e-12,
          "r(phase,gap) == r(DR,gap) [positive linear invariance]",
          abs(r_phase - r_dr), 0.0)

    print(f"\n  Pearson r(phase, gap) = {r_phase:.6f}")
    print(f"  Pearson r(DR,    gap) = {r_dr:.6f}")
    print(f"  Difference:            {abs(r_phase - r_dr):.2e}  (machine epsilon)")

    if abs(r_phase) > 0.7:
        verdict = "Strong"
    elif abs(r_phase) > 0.3:
        verdict = "Moderate"
    else:
        verdict = "Weak"
    print(f"\n  Verdict: {verdict} linear correlation  (r = {r_phase:.6f})")

    # ── STRUCTURAL NOTES ─────────────────────────────────────────
    print(f"""
  Structural facts:
  1. phase = DR(gap) * (2π/9) — positive linear rescaling of DR.
     Pearson r is invariant under positive linear transforms:
     r(phase, gap) = r(DR, gap) exactly.

  2. DR folds {len(folded)} gap values in this sample: {list(folded.keys())}.
     Folding is non-linear: gap=10 → DR=1, gap=12 → DR=3, etc.
     This reduces r below what a pure linear gap→phase map would give.

  3. Phases span [2π/9, 2π] — less than one full revolution.
     Pearson is technically wrong for full circular data; here the
     circular distortion is bounded because no wrap-around occurs
     (DR ranges 1..9, never 0, so phase never returns to 0).

  4. r = {r_phase:.6f} ({verdict}). The non-linearity from DR folding
     is the reason r < 1; it is not a separate phenomenon.
""")

    # ── ASSERTIONS ───────────────────────────────────────────────
    print("=" * 60)
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f)
        import sys; sys.exit(1)
    else:
        print(f"ALL ASSERTIONS PASSED")

if __name__ == "__main__":
    run()
