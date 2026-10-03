#!/usr/bin/env python3
"""Census the shapes that actually occur, so a hand tree can be diffed.

    python3 census.py --divisor-shapes 5 300000
"""
import math
import sys
from collections import Counter


def divisors(n):
    d = []
    for i in range(1, math.isqrt(n) + 1):
        if n % i == 0:
            d.append(i)
            if i != n // i:
                d.append(n // i)
    return sorted(d)


def factor(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def shape(n, k):
    """Symbolic form of the k smallest divisors, primes named p<q<r<..."""
    primes = sorted(factor(n))
    name = {p: "pqrstuvw"[i] if i < 8 else "?" for i, p in enumerate(primes)}
    out = []
    for d in divisors(n)[:k]:
        if d == 1:
            out.append("1")
            continue
        parts = []
        for b, e in sorted(factor(d).items()):
            nm = name.get(b, "?")
            parts.append(nm if e == 1 else "%s^%d" % (nm, e))
        out.append("".join(parts))
    return " ".join(out)


def census(k, bound):
    c = Counter()
    for n in range(2, bound + 1):
        if len(divisors(n)) < k:
            continue
        c[shape(n, k)] += 1
    print("shapes of the %d smallest divisors, n <= %d" % (k, bound))
    for s, cnt in c.most_common():
        print("   %-34s %d" % (s, cnt))
    print("   DISTINCT SHAPES: %d" % len(c))
    print("\n   diff this against your hand tree. Every shape here that your")
    print("   tree does not list is an unexamined branch.")
    return c


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 3 and a[0] == "--divisor-shapes":
        census(int(a[1]), int(a[2]))
    else:
        print(__doc__)
