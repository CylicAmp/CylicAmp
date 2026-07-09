#!/usr/bin/env python3
"""
phase_gap_correlation_audit.py

Pearson correlation between prime-gap digital-root phases and raw gaps.
Phase mapping: phase(gap) = (DR(gap) / 9) * 2π

CONNECTIONS TO EXISTING FRAMEWORK:
  1. mod9_grid_audit.py  — gcd(2,9)=1 Latin property governs which DR
     residues are reachable from even gaps. DR(2k) cycles through all
     9 residues with period 9 because gcd(2,9)=1.
  2. twin_prime_dr_sum_audit.py — gap DR directly reads the twin prime
     track. DR(p) + DR(2) = DR(p+2) on the DR addition table gives
     T₂₄ (2→4), T₅₇ (5→7), T₈₁ (8→1).
  3. mod9_grid_audit.py Cayley table — the gap of 2 is a +2 step in Z₉,
     moving p to its twin partner within the track.

STRUCTURAL FINDING:
  r starts at 1.000 when all gaps ≤ 9 (DR(gap)=gap, no folding).
  r decreases as larger gaps fold back via DR, converging toward ~0.22
  as ~33% of gaps exceed 9 and trigger modular reduction.

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

    # ── CONNECTION 1: gcd(2,9)=1 — Latin property ───────────────
    import math
    check(math.gcd(2, 9) == 1, "gcd(2,9)=1 — even gaps reach all 9 DR residues",
          math.gcd(2, 9), 1)
    dr_period = [digital_root(2 * k) for k in range(1, 10)]
    check(sorted(dr_period) == list(range(1, 10)),
          "DR(2k) for k=1..9 covers all of {1..9}",
          sorted(dr_period), list(range(1, 10)))
    print(f"\n  gcd(2,9) = 1  →  DR(2k) hits all 9 residues with period 9")
    print(f"  DR(2k), k=1..9: {dr_period}")
    print(f"  Same Latin property proven in mod9_grid_audit (gcd(A,9)=1 → bijection).")

    # ── CONNECTION 2: twin prime tracks via DR addition table ────
    print(f"\n  Twin prime track: DR(p) + DR(gap=2) = DR(p+2)")
    twin_p_drs = {2: "T₂₄", 5: "T₅₇", 8: "T₈₁"}
    for dr_p, track in twin_p_drs.items():
        dr_p2 = digital_root(dr_p + 2)
        check(dr_p2 == {2: 4, 5: 7, 8: 1}[dr_p],
              f"DR({dr_p})+DR(2)=DR(p+2) [{track}]", dr_p2, {2:4,5:7,8:1}[dr_p])
        print(f"    DR(p)={dr_p}  +  DR(2)=2  →  DR(p+2)={dr_p2}   [{track}]")
    print(f"  Gap DR=2 is the +2 step in Z₉ moving p to its twin within the track.")

    # ── CONNECTION 3: r convergence as folded fraction grows ─────
    print(f"\n  r(phase,gap) vs sample size — r tracks folding fraction:")
    print(f"  {'n':>6}  {'r':>10}  {'folded%':>9}")
    gaps_full = np.array([primes[i+1] - primes[i] for i in range(1000)])
    for n in [10, 25, 50, 100, 200, 500, 1000]:
        g_sl = gaps_full[:n]
        dr_sl = np.array([digital_root(int(g)) for g in g_sl])
        ph_sl = dr_sl * (2 * np.pi / 9)
        r_n = np.corrcoef(ph_sl, g_sl)[0, 1]
        fold_pct = 100 * sum(1 for g in g_sl if g > 9) / n
        print(f"  {n:>6}  {r_n:>10.6f}  {fold_pct:>8.1f}%")
    # r=1 at n=10,25 (no gaps>9 yet); drops sharply when folding begins
    g10 = gaps_full[:10]
    dr10 = np.array([digital_root(int(g)) for g in g10])
    r10 = np.corrcoef(dr10 * (2*np.pi/9), g10)[0,1]
    check(abs(r10 - 1.0) < 1e-10,
          "r=1.000 when all gaps ≤ 9 (no DR folding)", r10, 1.0)

    # ── STRUCTURAL NOTES ─────────────────────────────────────────
    print(f"""
  Structural facts:
  1. phase = DR(gap) * (2π/9) — positive linear rescaling of DR.
     r(phase, gap) = r(DR, gap) exactly (invariance under positive scale).

  2. DR folds {len(folded)} distinct gap values in this sample: {list(folded.keys())}.
     gcd(2,9)=1 guarantees all 9 DR residues are reachable from even gaps.
     Same coprimality condition as Latin square proof in mod9_grid_audit.

  3. r starts at 1 (no folding), decreases as folded-gap fraction grows,
     converging toward ~0.22 as ~33% of gaps exceed 9.

  4. Twin prime tracks are the +2 step on the DR addition table.
     DR(p) ∈ {{2,5,8}} + DR(2)=2 → DR(p+2) ∈ {{4,7,1}}: T₂₄, T₅₇, T₈₁.
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
