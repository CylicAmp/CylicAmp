"""
Cut table for the 12-digit string 113115117167 — verification

A pasted table cut the string at each position k (left = first k digits,
right = the remaining 12-k) and labelled both halves prime / composite.
This file reproduces the cuts, recomputes primality and factorization,
and asserts the pasted labels.

RESULT: 21 of 22 labels correct. One correction:

    k=1 left = 1 was labelled "composite". 1 is a unit — neither prime
    nor composite. Every other label, including the two explicit
    factorizations given (3 * 1038372389 at k=2 right, 7 * 283 * 571 at
    k=7 left), is exactly right.

GF(37) placement is computed for all 22 pieces. Three land on named
values (11311 = 26 = MULT, 1131151 = 24 = seed residue, 7167 = 26 again),
but 22 values over 13 bins expects ~1.7 per bin, so those hits are inside
noise, and decimal-prefix cuts are base-10 rendering in the sense of
forced-check. They are recorded, not claimed.

FALSIFICATION: any label below failing its assert, or the whole-string
factorization 113115117167 = 13 * 8701162859 being wrong.
"""

S = "113115117167"
P = 37
MULT = 26

ORBITS = {
    'IC': {1, 10, 26},        'DARK_A': {2, 15, 20},  'C3': {3, 4, 30},
    'CAS_EXT': {5, 13, 19},   'TESLA': {6, 8, 23},    'D7': {7, 33, 34},
    'SA_ST_A': {9, 12, 16},   'NEG_H': {11, 27, 36},  'C9': {14, 29, 31},
    'NQR17': {17, 22, 35},    'SEED': {18, 24, 32},   'SA_ST_B': {21, 25, 28},
}


def orbit_of(n):
    r = n % P
    if r == 0:
        return 'SEAM'
    for name, s in ORBITS.items():
        if r in s:
            return name
    raise AssertionError(f"{r} in no orbit")


def factor(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def status(n):
    """'unit' for 1, else 'prime' or 'composite'."""
    if n < 2:
        return 'unit'
    f = factor(n)
    return 'prime' if sum(f.values()) == 1 else 'composite'


def fstr(n):
    return "*".join(f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(factor(n).items()))


# (k, expected left status, expected right status) — as verified here,
# with k=1 left corrected from the pasted "composite" to "unit".
EXPECTED = [
    (1,  'unit',      'prime'),
    (2,  'prime',     'composite'),
    (3,  'prime',     'composite'),
    (4,  'composite', 'composite'),
    (5,  'prime',     'composite'),
    (6,  'composite', 'prime'),
    (7,  'composite', 'prime'),
    (8,  'composite', 'composite'),
    (9,  'composite', 'prime'),
    (10, 'composite', 'prime'),
    (11, 'composite', 'prime'),
]


def run():
    assert len(S) == 12
    assert factor(int(S)) == {13: 1, 8701162859: 1}, "whole-string factorization"

    for k, el, er in EXPECTED:
        L, R = int(S[:k]), int(S[k:])
        assert status(L) == el, f"k={k} left {L}: {status(L)} != {el}"
        assert status(R) == er, f"k={k} right {R}: {status(R)} != {er}"

    # the two factorizations stated explicitly in the pasted table
    assert factor(int(S[2:])) == {3: 1, 1038372389: 1}
    assert factor(int(S[:7])) == {7: 1, 283: 1, 571: 1}

    # 1 is a unit, not composite — the one correction
    assert status(1) == 'unit'

    print("All assertions passed.\n")
    print(f"string = {S}  =  {fstr(int(S))}   mod 37 = {int(S) % P} in {orbit_of(int(S))}\n")
    print(" k  left          right         left        right       left mod37    right mod37")
    for k, _, _ in EXPECTED:
        L, R = int(S[:k]), int(S[k:])
        print(f"{k:2d}  {S[:k]:<12}  {S[k:]:<12}  {status(L):<10}  {status(R):<10}"
              f"  {L % P:2d} {orbit_of(L):<9} {R % P:2d} {orbit_of(R)}")
    print()
    print("Factorizations of the composite pieces:")
    for k, _, _ in EXPECTED:
        for side, n in (('left', int(S[:k])), ('right', int(S[k:]))):
            if status(n) == 'composite':
                print(f"  k={k:2d} {side:<5} {n:<12} = {fstr(n)}")
    print()
    print(f"Named-value hits (recorded, not claimed): 11311 = {11311 % P} = MULT, "
          f"1131151 = {1131151 % P} = seed 246 mod 37, 7167 = {7167 % P} = MULT")


if __name__ == "__main__":
    run()
