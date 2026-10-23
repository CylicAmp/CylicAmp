#!/usr/bin/env python3
"""
The owner's walk (tools/owner_engine.py) to a trillion and past, on every core at once.

The steps are the engine's: at each n, predict from n's place in 1 2 3 (place 3, or n = 2); act with the neighbours,
behind + yourself = 2n - 1 and yourself + right = 2n + 1; verify that both are prime. As in owner_walk_segmented.py,
2n - 1 is odd number n - 1 and 2n + 1 is odd number n (the k-th odd number is 2k + 1), and the table of odd numbers is
built piece by piece. Two changes for speed, neither changes an answer:
  - the multiples of 3, 5, 7, 11, 13, 17 are crossed out by copying one ready-made pattern (it repeats every
    3 x 5 x 7 x 11 x 13 x 17 = 255255 odd numbers) instead of one prime at a time;
  - the range 1 .. N is cut into as many parts as there are cores, each part walked by its own process
    (each n only reads odd numbers n - 1 and n, so the parts never need each other).

    python3 tools/owner_walk_parallel.py 1000000000000 records/owner_walk_1e12.json [workers]
"""
import json
import multiprocessing as mp
import os
import sys
import time

import numpy as np

SMALL = (3, 5, 7, 11, 13, 17)
PERIOD = 3 * 5 * 7 * 11 * 13 * 17          # 255255
PIECE = 200_000_000


def base_primes(limit):
    s = np.ones(limit + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return [int(p) for p in np.nonzero(s)[0] if p > 2]


def pattern(length):
    """pat[k] is False when 2k + 1 is a multiple of 3, 5, 7, 11, 13 or 17 (for k = 0 .. length - 1)"""
    pat = np.ones(length, dtype=bool)
    for p in SMALL:
        pat[(p - 1) // 2::p] = False                      # 2k + 1 = p, 3p, 5p, ...
    return pat


def odd_piece(k0, k1, base, pat):
    off = k0 % PERIOD
    T = pat[off:off + (k1 - k0)].copy()
    for p in SMALL:                                       # the small primes themselves are prime
        k = (p - 1) // 2
        if k0 <= k < k1:
            T[k - k0] = True
    if k0 == 0:
        T[0] = False                                      # 1 is not prime
    top, lo = 2 * k1 + 1, 2 * k0 + 1
    for p in base:
        if p <= 17:
            continue
        if p * p > top:
            break
        m = max(p * p, -(-lo // p) * p)
        if m % 2 == 0:
            m += p
        i = (m - 1) // 2 - k0
        if i < len(T):
            T[i::p] = False
    return T


def walk_part(args):
    s0, e0, base, marks, log = args
    pat = pattern(PIECE + 2 + PERIOD)
    pairs, missed, first, last = 0, 0, None, None
    per_billion, upto = {}, {}
    t0 = time.time()
    s = s0
    while s <= e0:
        e = min(s + PIECE - 1, e0)
        T = odd_piece(s - 1, e + 1, base, pat)            # odd numbers 2k + 1 for k = s - 1 .. e
        ns = np.nonzero(T[:-1] & T[1:])[0].astype(np.int64) + s
        if len(ns):
            pairs += len(ns)
            missed += int(((ns % 3 != 0) & (ns != 2)).sum())
            first = int(ns[0]) if first is None else first
            last = int(ns[-1])
            b = (ns - 1) // 10 ** 9
            for v, c in zip(*np.unique(b, return_counts=True)):
                per_billion[int(v)] = per_billion.get(int(v), 0) + int(c)
            for mk in marks:
                if s <= mk:
                    upto[mk] = upto.get(mk, 0) + int((ns <= mk).sum())
        if log:
            with open(log, "a") as f:
                f.write("%d %d %d %.0f\n" % (s0, e, pairs, time.time() - t0))
        s = e + 1
    return {"from": s0, "to": e0, "pairs": pairs, "missed": missed, "first_n": first, "last_n": last,
            "per_billion": per_billion, "upto": upto}


def smooth_25(limit):
    out, a = [], 1
    while a <= limit:
        b = a
        while b <= limit:
            out.append(b)
            b *= 5
        a *= 2
    return sorted(out)


def walk_parallel(N, workers=None, log=None):
    t0 = time.time()
    workers = workers or os.cpu_count() or 1
    base = base_primes(int((2 * N + 1) ** 0.5) + 2)
    marks = [5 * 10 ** j for j in range(0, 20) if 5 * 10 ** j <= N]
    cuts = [1 + (N * i // workers) for i in range(workers)] + [N + 1]
    jobs = [(cuts[i], cuts[i + 1] - 1, base, marks, log) for i in range(workers)]
    with mp.Pool(workers) as pool:
        parts = pool.map(walk_part, jobs)
    per_billion, upto = {}, {mk: 0 for mk in marks}
    for r in parts:
        for b, c in r["per_billion"].items():
            per_billion[b] = per_billion.get(b, 0) + c
        for mk, c in r["upto"].items():
            upto[mk] += c
    last = next(r["last_n"] for r in reversed(parts) if r["last_n"] is not None)
    S = set(smooth_25(N + 1))
    return {"N": N, "predicted": N // 3 + (1 if N >= 2 else 0), "pairs": sum(r["pairs"] for r in parts),
            "missed": sum(r["missed"] for r in parts), "last_n": last, "last_pair": [2 * last - 1, 2 * last + 1],
            "three_ends": sorted(n for n in (x + 1 for x in S) if 2 <= n <= N and (n + 1) in S),
            "per_billion": [per_billion.get(b, 0) for b in range(max(per_billion) + 1)],
            "pairs_up_to": {str(k): v for k, v in sorted(upto.items())},
            "workers": workers, "seconds": round(time.time() - t0, 1)}


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 12
    out = sys.argv[2] if len(sys.argv) > 2 else None
    W = int(sys.argv[3]) if len(sys.argv) > 3 else None
    log = (out + ".progress") if out else None
    if log and os.path.exists(log):
        os.remove(log)
    w = walk_parallel(N, W, log)
    print(json.dumps({k: w[k] for k in w if k != "per_billion"}))
    if out:
        with open(out, "w") as f:
            json.dump(w, f, indent=1)
