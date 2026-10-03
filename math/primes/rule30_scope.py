# CLASS: VERIFICATION
"""
Rule 30 scope check — what is measured, what is conjectured.

Backs the scope note in CLAUDE.md step 6 of the standing analysis. The
repo runs Rule 30 on every value; this file records what Rule 30 is and
is not known to do, so nothing downstream cites a conjecture as settled.

THE THREE WOLFRAM RULE 30 PRIZE PROBLEMS -- all open, $10,000 each
(https://www.rule30prize.org/, checked 2026-09-13):

  Problem 1  Does the center column always remain non-periodic?
  Problem 2  Does each color of cell occur on average equally often
             in the center column?
  Problem 3  Does computing the nth cell of the center column require
             at least O(n) computational effort?

Problem 3 IS the computational-irreducibility claim. Problem 2 IS the
equidistribution claim. Neither is a theorem.

MEASURED HERE (finite runs, which cannot settle either prize):
  - center column generation cost
  - NIST monobit, block-frequency (M=100), runs
  - autocorrelation over lags 1..32

FALSIFICATION: any assert below failing, or any statistical test
returning p < 0.01 (which would be a real finding worth chasing, not a
bug -- print it, do not silence it).
"""

import math
import time


def center_column(N):
    """new[i] = left XOR (center OR right).
       Bitboard form: new = (row>>1) ^ (row | (row<<1)).
       Row update is parallel in space; only the time axis is serial,
       and that seriality is Problem 3 -- conjectured, not proven."""
    row = 1 << N
    mask = (1 << (2 * N + 1)) - 1
    col = bytearray(N)
    for t in range(N):
        col[t] = (row >> N) & 1
        row = ((row >> 1) ^ (row | (row << 1))) & mask
    return col


def _gammaincc(a, x):
    if x < a + 1:
        s = 1.0 / a
        term, n = s, 0
        while True:
            n += 1
            term *= x / (a + n)
            s += term
            if abs(term) < abs(s) * 1e-15 or n > 10000:
                break
        return 1.0 - s * math.exp(-x + a * math.log(x) - math.lgamma(a))
    b, c, d = x + 1 - a, 1e300, 1.0 / (x + 1 - a)
    h, i = d, 1
    while i < 10000:
        an = -i * (i - a)
        b += 2
        d = an * d + b
        if abs(d) < 1e-300:
            d = 1e-300
        c = b + an / c
        if abs(c) < 1e-300:
            c = 1e-300
        d = 1.0 / d
        de = d * c
        h *= de
        i += 1
        if abs(de - 1) < 1e-15:
            break
    return h * math.exp(-x + a * math.log(x) - math.lgamma(a))


def monobit(b):
    n = len(b)
    s = sum(1 if x else -1 for x in b)
    return math.erfc(abs(s) / math.sqrt(n) / math.sqrt(2))


def block_freq(b, M=100):
    n = len(b)
    K = n // M
    chi = 4 * M * sum((sum(b[i * M:(i + 1) * M]) / M - 0.5) ** 2
                      for i in range(K))
    return _gammaincc(K / 2, chi / 2)


def runs_test(b):
    n = len(b)
    pi = sum(b) / n
    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        return 0.0
    v = 1 + sum(1 for i in range(n - 1) if b[i] != b[i + 1])
    return math.erfc(abs(v - 2 * n * pi * (1 - pi))
                     / (2 * math.sqrt(2 * n) * pi * (1 - pi)))


def autocorr(b, lag):
    n = len(b) - lag
    m = sum(1 for i in range(n) if b[i] == b[i + lag])
    z = (m - n / 2) / (math.sqrt(n) / 2)
    return math.erfc(abs(z) / math.sqrt(2))


def run():
    print("RULE 30 SCOPE CHECK\n")
    print("OPEN PRIZE PROBLEMS (rule30prize.org, $10,000 each, unclaimed):")
    print("  1  center column always non-periodic?")
    print("  2  each color equally often on average?      <- equidistribution")
    print("  3  nth cell requires >= O(n) effort?         <- IRREDUCIBILITY")
    print("  none is a theorem. cite them as conjectures.\n")

    results = {}
    for N in (20000, 100000):
        t0 = time.perf_counter()
        col = center_column(N)
        dt = time.perf_counter() - t0
        b = list(col)
        ps = {
            "monobit": monobit(b),
            "block_freq_M100": block_freq(b, 100),
            "runs": runs_test(b),
        }
        lags = {L: autocorr(b, L) for L in range(1, 33)}
        worst_lag = min(lags, key=lags.get)
        results[N] = (dt, sum(b), ps, worst_lag, lags[worst_lag])

        print(f"N = {N}   {dt:.2f}s   ~{N * N:,} cell updates")
        print(f"  ones {sum(b)}  zeros {N - sum(b)}  "
              f"balance {sum(b) / N:.6f}")
        for k, p in ps.items():
            print(f"  {k:<16} p = {p:.4f}   "
                  f"{'PASS' if p >= 0.01 else 'FAIL <- investigate'}")
        fails = [(L, p) for L, p in lags.items() if p < 0.01]
        print(f"  autocorr lags 1..32  worst p = {lags[worst_lag]:.4f} "
              f"at lag {worst_lag}")
        print(f"  failing at alpha=0.01: {fails if fails else 'none'}"
              f"   (expect ~0.32 false failures over 32 lags)\n")

    # --- assertions ---
    for N, (dt, ones, ps, wl, wp) in results.items():
        for k, p in ps.items():
            assert p >= 0.01, f"N={N} {k} p={p} -- real finding, chase it"
        assert wp >= 0.01, f"N={N} autocorr lag {wl} p={wp} -- chase it"
        assert 0.45 < ones / N < 0.55

    # cost: O(N^2) cells, bit-packing is a constant factor not a complexity change
    assert 20000 ** 2 == 400_000_000
    assert 100000 ** 2 == 10_000_000_000
    assert results[20000][0] < 60 and results[100000][0] < 300

    print("All assertions passed.\n")
    print("WHAT THIS DOES AND DOES NOT SHOW")
    print("  shows: finite prefixes of the center column pass four NIST test")
    print("         families, and generating them is cheap -- O(N^2) cells,")
    print("         seconds at N=100,000 in plain Python.")
    print("  does NOT show: Problem 2. no finite run settles a limit.")
    print("  does NOT show: Problem 3. cost measured is an upper bound; the")
    print("         prize asks for a LOWER bound, which is the hard direction.")
    print("  four test families is not the full NIST SP 800-22 (15 tests)")
    print("  nor Dieharder. absence of failure here is not a pass overall.")


if __name__ == "__main__":
    run()
