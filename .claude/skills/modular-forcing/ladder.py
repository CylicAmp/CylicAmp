#!/usr/bin/env python3
"""The 2-adic ladder, run on a sum-of-squares expression.

    python3 ladder.py --divisor-sum 6      # the k=6 layer of T245
    python3 ladder.py --parity-lemma 3 9   # which k are forced, k=3..9
"""
import sys


def parity_lemma(kmin, kmax):
    print("n = 1 + (k-1) squares, every divisor odd:")
    print("  k    1+(k-1) odd terms    n parity    p=2 forced?")
    out = {}
    for k in range(kmin, kmax + 1):
        par = (1 + (k - 1)) % 2
        forced = (par == 0)
        out[k] = forced
        print("  %-4d %-20d %-11s %s" % (k, k, "even" if par == 0 else "odd",
                                         "YES" if forced else "no"))
    print("\n  forced exactly when k is even. Odd layers need another tool.")
    return out


def divisor_sum(k):
    """The mod-4 rung for n = 1 + 4 + (k-2 squares), i.e. after p=2."""
    if k % 2:
        print("k=%d is ODD: parity forces nothing. Ladder will not fire." % k)
        return
    m = k - 2                      # terms after 1 and 2^2
    print("k=%d: p=2 forced, so n = 5 + %d squares." % (k, m))
    print("  mod 4: n = 1 + a (mod 4), a = #odd among the %d terms." % m)
    live = []
    for a in range(m + 1):
        r = (1 + a) % 4
        odd = r % 2 == 1
        tag = "n odd -> excluded (n is even)" if odd else "LIVE, n = %d (mod 4)" % r
        print("    a=%-2d -> n = %d (mod 4)   %s" % (a, r, tag))
        if not odd:
            live.append((a, r))
    print("  surviving: %s" % [a for a, _ in live])
    print("\n  mod 8 on each: odd squares are 1 (mod 8), so the residue is")
    print("  exact and you get a divisibility. Then you MUST convert it into")
    print("  an ordering contradiction -- see SKILL.md, failure mode 1.")
    return live


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "--parity-lemma":
        parity_lemma(int(a[1]), int(a[2]))
    elif a[0] == "--divisor-sum":
        divisor_sum(int(a[1]))
    else:
        print(__doc__)
