#!/usr/bin/env python3
"""
The owner's walk (tools/owner_engine.py) for large ranges: 1 to N with N up to a billion and more.

At each n: predict from n's place in 1 2 3 (place 3, or n = 2); act with the neighbours, behind + yourself = 2n - 1
and yourself + right = 2n + 1; verify that both are prime. The same steps as the engine.

The trick that makes a billion fit: 2n - 1 and 2n + 1 are odd, and the k-th odd number is 2k + 1. So one table
"is 2k + 1 prime?" for k = 0 .. N answers every step: 2n - 1 is entry n - 1 and 2n + 1 is entry n. For N = 10^9
that table has 10^9 + 1 entries (1 GB), and the walk is entry n - 1 and entry n, side by side.

    python3 tools/owner_walk_big.py 1000000000
"""
import sys
import time

import numpy as np


def odd_sieve(N):
    """P[k] is True exactly when 2k + 1 is prime, k = 0 .. N"""
    P = np.ones(N + 1, dtype=bool)
    P[0] = False                                   # 1 is not prime
    k = 1
    while (2 * k + 1) ** 2 <= 2 * N + 1:
        if P[k]:
            p = 2 * k + 1
            P[(p * p - 1) // 2::p] = False         # p x p, p x p + 2p, ... in the odd table
        k += 1
    return P


def ends_mask(n):
    """n x n / (n x n - 1) ends (no loop) exactly when n x n - 1 is made of 2s and 5s"""
    q = n * n - 1
    r = q // (q & -q)                              # every 2 taken out
    out = r == 1
    c = np.nonzero(r % 5 == 0)[0]
    s = r[c]
    while s.size:
        s = s // 5
        done = s == 1
        out[c[done]] = True
        keep = (s % 5 == 0) & ~done
        c, s = c[keep], s[keep]
    return out


def walk_big(N, block=50_000_000):
    t0 = time.time()
    P = odd_sieve(N)
    hits, predicted, missed, three_ends = [], 0, 0, []
    for s in range(1, N + 1, block):
        e = min(s + block - 1, N)
        n = np.arange(s, e + 1, dtype=np.int64)
        hit = P[s - 1:e] & P[s:e + 1]              # 2n - 1 and 2n + 1 both prime
        guess = (n % 3 == 0) | (n == 2)
        predicted += int(guess.sum())
        missed += int((hit & ~guess).sum())
        hits.append(n[hit])
        m = n[n >= 2]
        three_ends += m[ends_mask(m)].tolist()
    pairs = np.concatenate(hits)
    return {"N": N, "predicted": predicted, "missed": missed, "pairs": pairs, "three_ends": three_ends,
            "seconds": round(time.time() - t0, 1)}


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 9
    w = walk_big(N)
    p = w["pairs"]
    print("walk 1 to %d: predicted %d, twin pairs %d, missed %d, last n = %d (%d, %d), 3-step ends %s, %.1f s"
          % (N, w["predicted"], len(p), w["missed"], p[-1], 2 * p[-1] - 1, 2 * p[-1] + 1, w["three_ends"], w["seconds"]))
