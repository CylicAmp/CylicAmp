# CLASS: THEOREM
"""
Concentric square shells grow by exactly 8k, and the shells tile (2k+1)^2
Author: Michael Warren Song (CyclicAmp)

STATEMENT
    For a square grid of odd side 2k+1 centred on one cell, the k-th
    concentric ring contains exactly 8k cells:

        S(k) = (2k+1)^2 - (2k-1)^2 = 8k          for k >= 1,   S(0) = 1

    and the shells partition the grid:

        1 + sum_{j=1..k} 8j  =  1 + 8*k(k+1)/2  =  (2k+1)^2

PROOF
    (2k+1)^2 - (2k-1)^2 = (4k^2+4k+1) - (4k^2-4k+1) = 8k.
    Summing, 1 + 8*(k(k+1)/2) = 1 + 4k^2 + 4k = (2k+1)^2.  QED

    Both are polynomial identities in k, so they hold for every k, not just
    the checked range. The assertions below check k = 0..999 as a guard
    against transcription error, not as the proof.

SHELL SIZES AND THE 137-MAP
    Shell sizes are 8k, so their residues mod 37 are 8k mod 37. Since
    gcd(8,37) = 1, k -> 8k is a bijection on Z/37Z: over any 37 consecutive
    shells every residue appears exactly once, and each of the 12 orbits is
    hit exactly 3 times, with SEAM once (k = 0 mod 37, i.e. k = 37, 74, ...).
    That distribution is forced by the bijection and carries no information
    beyond it.

    The first three shells are the grids this repository already uses:
        k=1   8 cells    3x3    8 in TESLA
        k=2  16 cells    5x5   16 in SA_ST_A
        k=3  24 cells    7x7   24 in SEED       (= seed 246 mod 37)

FALSIFICATION
    Any k with (2k+1)^2 - (2k-1)^2 != 8k, or any k where the shells fail to
    sum to (2k+1)^2.
"""

P = 37
MULT = 26
ORBITS = {
    'IC': {1, 10, 26},      'DARK_A': {2, 15, 20},  'C3': {3, 4, 30},
    'CAS_EXT': {5, 13, 19}, 'TESLA': {6, 8, 23},    'D7': {7, 33, 34},
    'SA_ST_A': {9, 12, 16}, 'NEG_H': {11, 27, 36},  'C9': {14, 29, 31},
    'NQR17': {17, 22, 35},  'SEED': {18, 24, 32},   'SA_ST_B': {21, 25, 28},
}


def orbit_of(n):
    r = n % P
    if r == 0:
        return 'SEAM'
    for name, s in ORBITS.items():
        if r in s:
            return name
    raise AssertionError(r)


def shell(k):
    """Cells in the k-th concentric ring of an odd square grid."""
    return 1 if k == 0 else (2 * k + 1) ** 2 - (2 * k - 1) ** 2


def run():
    for k in range(1, 1000):
        assert shell(k) == 8 * k, k
    for k in range(0, 1000):
        assert 1 + sum(shell(j) for j in range(1, k + 1)) == (2 * k + 1) ** 2, k

    # 8 is a unit mod 37, so k -> 8k is a bijection on the residues
    assert len({(8 * k) % P for k in range(P)}) == P
    from collections import Counter
    c = Counter(orbit_of(8 * k) for k in range(1, P + 1))
    assert c['SEAM'] == 1
    assert all(v == 3 for o, v in c.items() if o != 'SEAM'), c

    print("All assertions passed.\n")
    print("  k   side   shell = 8k   total = (2k+1)^2   shell mod 37   orbit")
    for k in range(0, 9):
        s = shell(k)
        print(f"  {k}   {2*k+1:4d}   {s:9d}   {(2*k+1)**2:14d}   {s % P:11d}   {orbit_of(s)}")
    print()
    print("  over 37 consecutive shells, orbit counts:", dict(c))
    print("  (3 per orbit + 1 SEAM, forced because gcd(8,37) = 1)")


if __name__ == "__main__":
    run()
