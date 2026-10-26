#!/usr/bin/env python3
"""
The race of the owner's three twin chains -- one file, plain Python 3, nothing to install, nothing else needed.
Runs on a phone, an online Python, or any other assistant's computer.

    python3 twin_chain_race.py            walk n = 1 .. 10,000,000 (a few seconds)
    python3 twin_chain_race.py 100000000  walk to 100,000,000 (a minute or two, about 100 MB of memory)

THE WALK (Michael Warren Song's): at each n, behind + yourself = 2n - 1 and yourself + right = 2n + 1; a twin pair when
both are prime. After (3, 5) every pair has n at place 3 of 1 2 3, and the root of n picks the chain:
    root 3 -> (5, 7)      root 6 -> (2, 4)      root 9 -> (8, 1)
The lead is the chain with the most pairs so far (on a tie, the first of 3, 6, 9); a lead change is counted each time
it passes to another chain.

The table: the k-th odd number is 2k + 1, so "is 2k + 1 prime?" for k = 0 .. N answers every n:
2n - 1 is entry n - 1 and 2n + 1 is entry n.

It prints the counts and checks them against the numbers found by the C version (tools/owner_race_fast.c, run to a
trillion on 2026-10-26): PASS or FAIL for each checkpoint it reaches.
"""
import sys

KNOWN = {  # n up to: (root 3, root 6, root 9)
    10 ** 6: (4979, 4978, 4913),
    10 ** 7: (35876, 35811, 35719),
    10 ** 8: (271509, 271038, 270823),
    10 ** 9: (2131202, 2127929, 2128909),
}
KNOWN_LEAD = {10 ** 6: (56, 998544), 10 ** 7: (496, 8648940), 10 ** 8: (496, 8648940)}   # (changes, last change at n)


def odd_prime_table(N):
    """P[k] = 1 exactly when 2k + 1 is prime, k = 0 .. N"""
    P = bytearray([1]) * (N + 1)
    P[0] = 0
    k = 1
    while (2 * k + 1) ** 2 <= 2 * N + 1:
        if P[k]:
            p = 2 * k + 1
            start = (p * p - 1) // 2
            P[start::p] = bytes(len(range(start, N + 1, p)))
        k += 1
    return bytes(P)


def race(N):
    P = odd_prime_table(N)
    counts = [0, 0, 0]
    at = {}
    lead, changes, last_change = -1, 0, 0
    marks = sorted(m for m in KNOWN if m <= N)
    mi = 0
    i = P.find(b"\x01\x01")
    while i != -1:
        n = i + 1                                   # entries n - 1 = i and n = i + 1
        if n > N:
            break
        while mi < len(marks) and n > marks[mi]:
            at[marks[mi]] = tuple(counts)
            mi += 1
        if n > 2:
            idx = {3: 0, 6: 1, 0: 2}[n % 9]
            counts[idx] += 1
            best = 0
            if counts[1] > counts[best]:
                best = 1
            if counts[2] > counts[best]:
                best = 2
            if lead < 0:
                lead = best
            elif best != lead:
                changes += 1
                last_change = n
                lead = best
        i = P.find(b"\x01\x01", i + 1)
    while mi < len(marks):
        at[marks[mi]] = tuple(counts)
        mi += 1
    return counts, at, changes, last_change, lead


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 7
    counts, at, changes, last_change, lead = race(N)
    names = ["root 3 (5,7)", "root 6 (2,4)", "root 9 (8,1)"]
    print("walk n = 1 .. %d" % N)
    print("  %s: %d   %s: %d   %s: %d" % (names[0], counts[0], names[1], counts[1], names[2], counts[2]))
    print("  lead changes: %d, last at n = %d, leading now: %s" % (changes, last_change, names[lead]))
    ok = True
    for m in sorted(at):
        good = at[m] == KNOWN[m]
        ok &= good
        print("  %s  n up to %d: %s" % ("PASS" if good else "FAIL", m, at[m]))
    if N in KNOWN_LEAD:
        good = (changes, last_change) == KNOWN_LEAD[N]
        ok &= good
        print("  %s  lead changes and last change at %d" % ("PASS" if good else "FAIL", N))
    sys.exit(0 if ok else 1)
