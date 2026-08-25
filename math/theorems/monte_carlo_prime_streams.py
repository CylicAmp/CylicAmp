# -*- coding: utf-8 -*-
"""
================================================================================
MONTE CARLO — PRIME STREAM DISTRIBUTION
================================================================================

Author: Michael Warren Song (CyclicAmp)

Measures:
  1. Stream distribution (chi-squared uniformity test)
  2. Mirror pair balance (1↔8, 2↔7, 4↔5)
  3. Chebyshev bias (QNR streams {2,5,8} vs QR streams {1,4,7})
  4. GF(37) named-set hit rate per stream
  5. Large prime sampling via Miller-Rabin
================================================================================
"""

import random
import math
from collections import defaultdict

P = 37
F_CLASS = {1, 2, 4, 5, 7, 8}

SEED_S  = {18, 24, 32}
SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
IC      = {1, 10, 26}
NEG_H   = {11, 27, 36}
CASCADE = {8, 13, 24}
DARK_A  = {2, 15, 20}
NQR_17  = {17, 22, 35}
named   = SEED_S | SA | ST | IC | NEG_H | CASCADE | DARK_A | NQR_17

QNR_STREAMS = {2, 5, 8}   # lower twin prime DRs
QR_STREAMS  = {1, 4, 7}   # upper twin prime DRs

MIRROR_PAIRS = [(1, 8), (2, 7), (4, 5)]
CROSS_CURRENTS = [(2, 5), (4, 7), (8, 8)]


def dr(n):
    n = abs(n)
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def is_prime_miller_rabin(n, k=12):
    if n < 2: return False
    if n in (2, 3, 5, 7, 11, 13): return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for a in witnesses:
        if a >= n: continue
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else:
            return False
    return True


def sieve(limit):
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(limit**0.5) + 1):
        if is_p[i]:
            is_p[i*i::i] = bytearray(len(is_p[i*i::i]))
    return [i for i in range(2, limit+1) if is_p[i]]


def chi_squared_uniform(counts, n_bins):
    total = sum(counts.values())
    expected = total / n_bins
    return sum((c - expected)**2 / expected for c in counts.values())


def run():
    print("=" * 70)
    print("MONTE CARLO — PRIME STREAM DISTRIBUTION")
    print("=" * 70)

    # ── PHASE 1: Sieve up to 10^7 (full census) ──────────────────────────
    print("\n── PHASE 1: Sieve census (primes ≤ 10,000,000) ──")
    primes = sieve(10_000_000)
    stream_counts = defaultdict(int)
    gf37_hits = defaultdict(int)
    for p in primes:
        if p <= 3: continue
        d = dr(p)
        stream_counts[d] += 1
        r = p % P
        if r in named:
            gf37_hits[d] += 1

    total_f = sum(stream_counts[d] for d in F_CLASS)
    print(f"\nTotal primes in F-class: {total_f:,}")
    print(f"\n{'Stream':>7} {'Count':>8} {'Pct':>7} {'Expected':>9} {'GF37 hits':>10} {'Hit%':>6}")
    expected_pct = 100 / 6
    for d in sorted(F_CLASS):
        c = stream_counts[d]
        pct = 100 * c / total_f
        hits = gf37_hits[d]
        hit_pct = 100 * hits / c if c else 0
        print(f"  DR={d}   {c:>8,}  {pct:>6.2f}%  {expected_pct:>8.2f}%  {hits:>10,}  {hit_pct:>5.1f}%")

    chi2 = chi_squared_uniform(stream_counts, 6)
    print(f"\nChi-squared (6 streams, df=5): {chi2:.4f}")
    print(f"  (critical value at p=0.05: 11.07; >11.07 = non-uniform)")

    # Mirror pair balance
    print(f"\n── Mirror pair balance ──")
    for a, b in MIRROR_PAIRS:
        ca, cb = stream_counts[a], stream_counts[b]
        ratio = ca / cb if cb else float('inf')
        print(f"  Stream {a} ↔ Stream {b}: {ca:,} vs {cb:,}  ratio={ratio:.4f}  (ideal=1.0000)")

    # Chebyshev bias: QNR vs QR streams
    qnr_total = sum(stream_counts[d] for d in QNR_STREAMS)
    qr_total  = sum(stream_counts[d] for d in QR_STREAMS)
    bias = qnr_total - qr_total
    print(f"\n── Chebyshev bias ──")
    print(f"  QNR streams {{2,5,8}}: {qnr_total:,}")
    print(f"  QR  streams {{1,4,7}}: {qr_total:,}")
    print(f"  Bias toward QNR: {bias:+,}  ({'QNR leads' if bias > 0 else 'QR leads'})")

    # ── PHASE 2: Monte Carlo — random large primes ────────────────────────
    print("\n── PHASE 2: Monte Carlo large prime sampling ──")
    ranges = [
        (10**12, 10**12 + 10**8, "10^12 range"),
        (10**15, 10**15 + 10**8, "10^15 range"),
        (10**18, 10**18 + 10**8, "10^18 range"),
    ]
    N_SAMPLE = 200_000

    for lo, hi, label in ranges:
        mc_counts = defaultdict(int)
        found = 0
        attempts = 0
        while found < 600:
            n = random.randint(lo, hi)
            attempts += 1
            if is_prime_miller_rabin(n):
                d = dr(n)
                if d in F_CLASS:
                    mc_counts[d] += 1
                    found += 1

        mc_total = sum(mc_counts.values())
        mc_chi2 = chi_squared_uniform(mc_counts, 6)
        qnr_mc = sum(mc_counts[d] for d in QNR_STREAMS)
        qr_mc  = sum(mc_counts[d] for d in QR_STREAMS)
        print(f"\n  {label} (n={mc_total} primes, {attempts} candidates):")
        for d in sorted(F_CLASS):
            c = mc_counts[d]
            pct = 100 * c / mc_total
            mark = " ←" if d in QNR_STREAMS else ""
            print(f"    DR={d}: {c:>4}  ({pct:>5.1f}%){mark}")
        print(f"    Chi²={mc_chi2:.3f}  QNR bias: {qnr_mc-qr_mc:+d}")

    # ── PHASE 3: Cross-current verification ──────────────────────────────
    print("\n── Phase 3: Cross-current collision (group law) ──")
    print("  Sampling 10,000 prime pairs, verifying DR(p×q) mod 9 = DR(p)×DR(q) mod 9")
    sample_primes = random.sample(primes[10:], 500)
    violations = 0
    tests = 0
    for i in range(len(sample_primes)):
        for j in range(i, min(i+20, len(sample_primes))):
            p, q = sample_primes[i], sample_primes[j]
            dp, dq = dr(p), dr(q)
            dpq = dr(p * q)
            expected_dr = dr(dp * dq)
            if dpq != expected_dr:
                violations += 1
            tests += 1
    print(f"  Tests: {tests:,}  Violations: {violations}  (0 expected — group law)")

    print(f"\nAll done.")


if __name__ == "__main__":
    run()
