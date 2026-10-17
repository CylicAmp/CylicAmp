#!/usr/bin/env python3
"""The zeta-zero parity engine of the MWS handoff, section 4 (owner_work #272), built to run.

The owner's engine: for each zero gamma_n, take its digits, count odd minus even digits in the first N
(D_N), fit the slope alpha of log|D_N| against log N, and test the prediction "odd-indexed zero -> D_N > 0,
even-indexed -> D_N < 0". This keeps that logic. It fixes three places where the pasted code broke:
  1. a zero with fewer digits than the smallest depth left d_n_vals empty and d_n_vals[-1] crashed;
  2. alpha silently became 0.5 when it could not be fitted -- it is now None, with the reason;
  3. zetazeros.txt is not in the repository -- zeros come from mpmath.zetazero at the needed precision,
     or from a file (one zero per line) when a path is given.
"Digits" = the digits of the zero as written, integer part included (14.1347... starts 1, 4, 1, 3, 4, 7 ...),
as in the owner's code.

    python3 tools/zeta_parity_engine.py                  first 20 zeros, depths 100 and 1000
    python3 tools/zeta_parity_engine.py --zeros 10 --depths 100 1000
    python3 tools/zeta_parity_engine.py --file zetazeros.txt
"""
import argparse
import math
import sys

import numpy as np


def digits_of(text):
    return "".join(c for c in text.strip() if c.isdigit())


def zeros_from_mpmath(count, digits):
    import mpmath as mp
    mp.mp.dps = digits + 20
    for n in range(1, count + 1):
        yield mp.nstr(mp.zetazero(n).imag, digits + 10, strip_zeros=False)


def zeros_from_file(path, count):
    with open(path) as f:
        for i, line in enumerate(f):
            if i >= count:
                break
            yield line


def analyze_stream(lines, depths):
    results = []
    for idx, line in enumerate(lines):
        digits = digits_of(line)
        if not digits:
            continue
        zero_index = idx + 1
        valid = [n for n in depths if n <= len(digits)]
        d_vals = []
        for n in valid:
            odds = sum(1 for ch in digits[:n] if int(ch) % 2 == 1)
            d_vals.append(odds - (n - odds))
        pts = [(n, abs(d)) for n, d in zip(valid, d_vals) if d != 0]
        if len(pts) > 1:
            alpha, alpha_note = float(np.polyfit(np.log([n for n, _ in pts]), np.log([d for _, d in pts]), 1)[0]), f"{len(pts)}-point slope"
        else:
            alpha, alpha_note = None, "fewer than 2 depths with D_N != 0"
        if d_vals:
            predicted = (d_vals[-1] > 0) if zero_index % 2 == 1 else (d_vals[-1] < 0)
        else:
            predicted = None
        results.append({"zero_idx": zero_index, "depths": valid, "d_n": d_vals, "d_n_final": d_vals[-1] if d_vals else None,
                        "alpha_slope": alpha, "alpha_note": alpha_note, "predicted_sign_match": predicted})
    return results


def binomial_two_sided(k, n):
    """Exact two-sided p-value against a fair coin (sum of the probabilities no larger than P(k))."""
    probs = [math.comb(n, i) / 2 ** n for i in range(n + 1)]
    return min(1.0, sum(p for p in probs if p <= probs[k] + 1e-15))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zeros", type=int, default=20)
    ap.add_argument("--depths", type=int, nargs="+", default=[100, 1000])
    ap.add_argument("--file")
    a = ap.parse_args()
    lines = zeros_from_file(a.file, a.zeros) if a.file else zeros_from_mpmath(a.zeros, max(a.depths))
    res = analyze_stream(lines, a.depths)
    print(f"{'zero':>4}  {'D_N at ' + '/'.join(map(str, a.depths)):<22} {'alpha':>8}  predicted sign")
    for r in res:
        al = "None" if r["alpha_slope"] is None else f"{r['alpha_slope']:.3f}"
        print(f"{r['zero_idx']:>4}  {str(r['d_n']):<22} {al:>8}  {r['predicted_sign_match']}")
    scored = [r["predicted_sign_match"] for r in res if r["predicted_sign_match"] is not None]
    k, n = sum(scored), len(scored)
    print(f"\nsign matches {k} of {n}; fair-coin baseline {n / 2:.1f}; exact two-sided binomial p = {binomial_two_sided(k, n):.4f}")
    print(f"alpha is a {len(a.depths)}-depth slope: with 2 or 3 depths it is a 2 to 3 point fit, not a Hurst exponent estimate")
    return 0


if __name__ == "__main__":
    sys.exit(main())
