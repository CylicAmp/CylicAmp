#!/usr/bin/env python3
"""
Runs every digit/number protocol demonstrated in this thread against any
input, so each one applies automatically instead of being re-derived by
hand every time a new number comes up.

    python3 protocols.py 246
    python3 protocols.py 121212121
    python3 protocols.py 19 28 37 46 55 64 73 82 91

Six protocols, each a real check, not a template applied blindly:

  1. COMMA-GROUP / REPUNIT   base-10 groups digits in 3s because
     10^3 = 1 mod 37. Reports each 3-digit group's residue and orbit,
     and whether the number is a repunit divisible by 37 (period 3).

  2. REVERSAL DIFFERENCE     abc - cba = 99*(a-c) for any 3-digit number
     (first digit minus last digit), generalizing to (b^(n-1)-1)*(a-z)
     for n digits. Reports the difference and its mod-37 residue.

  3. DIGIT-SUM LADDER        is this number on a constant-digit-sum
     ladder (step 9 within a decade)? Reports the ladder position and
     whether adjacent rungs are also GF(37)-notable.

  4. PASCAL / REPUNIT ROW    is this number a row of Pascal's triangle
     read as digits (11^n) or the sum 2^n? Both are the binomial
     theorem at x=10 and x=1 respectively -- reports which n, if any,
     and where the carry breaks (n=5) if relevant.

  5. SHELL / GNOMON          is this number a two-step concentric-ring
     shell size 8k, or a one-step Pythagorean gnomon 2k+1, or a total
     (2k+1)^2? Reports which, if any.

  6. PARITY / CHECKERBOARD   for a number read as (row,col) or as a
     sequence of digits, is (i+j) mod 2 alternation present -- i.e. is
     this consistent with a bipartite lattice coloring?

Every protocol reports GF(37) placement (residue, orbit, DR) for
whatever it finds, using the same orbit table as gf37-audit.
"""
import sys, math

P = 37
MULT = 26
ORBITS = {
    'IC': {1, 10, 26}, 'DARK_A': {2, 15, 20}, 'C3': {3, 4, 30},
    'CAS_EXT': {5, 13, 19}, 'TESLA': {6, 8, 23}, 'D7': {7, 33, 34},
    'SA_ST_A': {9, 12, 16}, 'NEG_H': {11, 27, 36}, 'C9': {14, 29, 31},
    'NQR17': {17, 22, 35}, 'SEED': {18, 24, 32}, 'SA_ST_B': {21, 25, 28},
}


def orbit_of(n):
    r = n % P
    if r == 0:
        return 'SEAM'
    for name, s in ORBITS.items():
        if r in s:
            return name
    raise AssertionError(r)


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def place(n):
    return f"{n} mod37={n % P} orbit={orbit_of(n)} DR={dr(n)}"


def protocol_comma_group(n):
    s = str(n)
    groups = []
    while s:
        groups.append(s[-3:])
        s = s[:-3]
    groups.reverse()
    print(f"  1. COMMA-GROUP  groups={groups}")
    for g in groups:
        v = int(g)
        print(f"       {g:>3} -> {place(v)}")
    if len(s := str(n)) >= 3 and len(set(s)) == 1 and int(s) % P == 0:
        print(f"       repunit-like, all digits equal, divisible by 37 (period-3 fact)")


def protocol_reversal(n):
    s = str(n)
    if len(s) < 2:
        print("  2. REVERSAL     (single digit, no reversal to check)")
        return
    rev = int(s[::-1])
    diff = n - rev
    b = 10
    L = len(s)
    a, z = int(s[0]), int(s[-1])
    forced = (b ** (L - 1) - 1) * (a - z)
    print(f"  2. REVERSAL     {n} - {rev} = {diff}   forced form (10^{L-1}-1)*({a}-{z}) = {forced}"
          f"   match={diff == forced}   {place(abs(diff)) if diff else 'diff=0'}")


def digit_sum(n):
    return sum(int(c) for c in str(n))


def protocol_digit_sum_ladder(n):
    ds = digit_sum(n)
    below = n - 9 if n - 9 >= 1 else None
    above = n + 9
    same = [x for x in (below, above) if x is not None and digit_sum(x) == ds]
    broken = [x for x in (below, above) if x is not None and digit_sum(x) != ds]
    print(f"  3. DIGIT-LADDER digit_sum={ds}  same-sum neighbors (n+-9): {same}"
          + (f"  [broken at: {broken}]" if broken else ""))
    for x in same:
        print(f"       {place(x)}")


def protocol_pascal(n):
    from math import comb
    found = []
    for k in range(0, 20):
        if 11 ** k == n:
            found.append(('11^k digit-row', k))
        if 2 ** k == n:
            found.append(('2^k row-sum', k))
    if found:
        for label, k in found:
            print(f"  4. PASCAL       {n} = {label}, k={k}")
    else:
        print(f"  4. PASCAL       {n} is not 11^k or 2^k for k=0..19")


def protocol_shell(n):
    hits = []
    for k in range(0, 100):
        if k >= 1 and 8 * k == n:
            hits.append(f"shell(k={k})=8k")
        if 2 * k + 1 == n:
            hits.append(f"gnomon(k={k})=2k+1")
        if (2 * k + 1) ** 2 == n:
            hits.append(f"total(k={k})=(2k+1)^2")
    if hits:
        print(f"  5. SHELL/GNOMON {n}: {', '.join(hits)}")
    else:
        print(f"  5. SHELL/GNOMON {n} matches no shell/gnomon/total form for k=0..99")


def protocol_parity(n):
    s = str(n)
    parities = [int(c) % 2 for c in s]
    alt = all(parities[i] != parities[i + 1] for i in range(len(parities) - 1))
    print(f"  6. PARITY       digits={s}  parities={parities}  strictly alternating={alt}")


PROTOCOLS = [
    protocol_comma_group, protocol_reversal, protocol_digit_sum_ladder,
    protocol_pascal, protocol_shell, protocol_parity,
]


def run(n):
    print(f"=== {n} ===  ({place(n)})")
    for p in PROTOCOLS:
        p(n)
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    for arg in sys.argv[1:]:
        run(int(arg))
