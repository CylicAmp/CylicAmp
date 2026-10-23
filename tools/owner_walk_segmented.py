#!/usr/bin/env python3
"""
The owner's walk (tools/owner_engine.py) for very large ranges -- ten billion and more -- in pieces.

The steps are the engine's: at each n, predict from n's place in 1 2 3 (place 3, or n = 2); act with the neighbours,
behind + yourself = 2n - 1 and yourself + right = 2n + 1; verify that both are prime.

As in tools/owner_walk_big.py, the k-th odd number is 2k + 1, so 2n - 1 is odd number n - 1 and 2n + 1 is odd number n.
Here the table of odd numbers is built one piece at a time (50,000,000 odd numbers per piece), crossing out the
multiples of every prime up to the square root of 2N + 1, so memory stays under 2 GB at any N.

The 3-step n x n / (n x n - 1) ends exactly when n - 1 and n + 1 are both made of 2s and 5s (owner_work #403). Every
number up to N + 1 made of 2s and 5s is listed (a few hundred of them), so every n up to N is checked, none skipped.

    python3 tools/owner_walk_segmented.py 10000000000 records/owner_walk_1e10.json
"""
import json
import sys
import time

import numpy as np


def small_primes(limit):
    s = np.ones(limit + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.nonzero(s)[0]


def odd_piece(k0, k1, base):
    """T[i] is True exactly when 2(k0 + i) + 1 is prime, for k0 + i in [k0, k1)"""
    T = np.ones(k1 - k0, dtype=bool)
    if k0 == 0:
        T[0] = False                                         # 1 is not prime
    top = 2 * k1 + 1
    lo = 2 * k0 + 1
    for p in base:
        p = int(p)
        if p == 2:
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


def smooth_25(limit):
    out = []
    a = 1
    while a <= limit:
        b = a
        while b <= limit:
            out.append(b)
            b *= 5
        a *= 2
    return sorted(out)


def walk_segmented(N, piece=50_000_000, report=None):
    t0 = time.time()
    base = small_primes(int((2 * N + 1) ** 0.5) + 2)
    total_pairs, missed, last = 0, 0, None
    per_block = {}                                          # pairs per 10^9 of n
    upto = {}                                               # pairs with n <= 5 x 10^j (the A007508 checkpoints)
    marks = [5 * 10 ** j for j in range(0, 20) if 5 * 10 ** j <= N]
    # odd numbers 2k + 1 for k = s - 1 .. e, so that n = s .. e reads entries n - 1 and n
    s = 1
    while s <= N:
        e = min(s + piece - 1, N)
        T = odd_piece(s - 1, e + 1, base)                   # k = s - 1 .. e
        hit = T[:-1] & T[1:]                                # n = s .. e
        idx = np.nonzero(hit)[0]
        ns = idx.astype(np.int64) + s
        total_pairs += len(ns)
        missed += int(((ns % 3 != 0) & (ns != 2)).sum())
        if len(ns):
            last = int(ns[-1])
        for b in np.unique((ns - 1) // 10 ** 9):
            per_block[int(b)] = per_block.get(int(b), 0) + int(((ns - 1) // 10 ** 9 == b).sum())
        for mk in marks:
            if s <= mk:
                upto[mk] = upto.get(mk, 0) + int((ns <= mk).sum())
        if report:
            report(e, total_pairs, time.time() - t0)
        s = e + 1
    for mk in marks:
        upto.setdefault(mk, 0)
    predicted = N // 3 + (1 if N >= 2 else 0)               # n = 3, 6, 9, ... and n = 2
    S = set(smooth_25(N + 1))
    three_ends = sorted(n for n in (x + 1 for x in S) if 2 <= n <= N and (n + 1) in S)
    return {"N": N, "predicted": predicted, "pairs": total_pairs, "missed": missed, "last_n": last,
            "last_pair": [2 * last - 1, 2 * last + 1] if last else None, "three_ends": three_ends,
            "per_billion": [per_block.get(b, 0) for b in range(max(per_block) + 1)] if per_block else [],
            "pairs_up_to": {str(k): v for k, v in sorted(upto.items())}, "seconds": round(time.time() - t0, 1)}


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 10
    out = sys.argv[2] if len(sys.argv) > 2 else None
    w = walk_segmented(N, report=lambda e, t, sec: print("  n up to %d: %d pairs, %.0f s" % (e, t, sec), flush=True)
                       if e % 1_000_000_000 == 0 else None)
    print(json.dumps(w, indent=1))
    if out:
        with open(out, "w") as f:
            json.dump(w, f, indent=1)
