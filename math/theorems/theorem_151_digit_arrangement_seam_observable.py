"""
Theorem 151: Digit Arrangement, the SEAM, and the Limits of Observable Structure

THE FIVE PATTERNS
==================

Consider five 4-digit strings:

    0000   1111   1234   1212   1221

Observable from digit count alone: five objects, each with 4 digits.
That is all N can see. The count carries no further information.

GF(37) ORBIT CLASSIFICATION
=============================

    Pattern   mod 37   Orbit            Structure
    ──────────────────────────────────────────────────
    0000           0   SEAM             null — no information
    1111           1   IC               uniform — all digits identical
    1234          13   NQR_5            ascending sequence
    1212          28   OUTLIER_ORB      alternating — period 2
    1221           0   SEAM             palindrome — exactly 33×37

THE TWO CRITICAL FINDINGS
===========================

I.  THE PALINDROME HITS THE SEAM EXACTLY

    1221 = 33 × 37

    The palindrome — the arrangement with perfect bilateral symmetry —
    is an exact multiple of 37. It maps to 0 mod 37. It hits the SEAM.
    Every element of the sequence that produced it is erased. Provenance
    collapses. The arrangement that looks most "complete" and "symmetric"
    is the one that loses everything.

    This is not a numerical coincidence selected after the fact. The
    question was: what orbit does the palindrome land in? The answer is
    SEAM, and the exact factorization 33×37 is the certificate.

II. THE UNIFORM PATTERN LANDS IN IC

    1111 ≡ 1 (mod 37)

    The arrangement in which all digits are identical — maximum uniformity,
    minimum internal variation — reduces to 1 mod 37. It lands in IC,
    the identity cluster {1, 10, 26}, the unique order-3 subgroup of F₃₇×.
    The thing that looks most like "just repeating one thing" is
    identified with the multiplicative identity.

THE INDISTINGUISHABILITY PROBLEM
==================================

1212 and 1221 share all aggregate observables:

    digit sum  = 6
    product    = 4
    digital root = 6

In any system that computes only aggregates, these two are the same object.
Their orbit destinations are not:

    1212  →  OUTLIER_ORB = {21, 28, 25}
    1221  →  SEAM  (total provenance collapse)

The difference between landing in OUTLIER_ORB and hitting the SEAM is
contained entirely in the arrangement — the internal order of the digits.
That information is invisible to any observable that only counts or sums.

CONNECTION TO N AND Nκ
========================

N (standard naturals) records only the value. For N, the digit string is
already gone; only the integer remains. 1212 and 1221 are distinct integers,
so N can tell them apart by value — but N cannot say WHY they differ, because
N carries no record of how they were formed.

Nκ (naturals with presence) carries κ: the genealogy, the arrangement, the
path taken. The arrangement IS κ here. The palindrome structure of 1221 is
part of its κ — and that κ is what places it on the SEAM.

If κ is not recorded, the arrangement is lost. The object enters the system
as a bare integer and its structural provenance cannot be recovered.

CONNECTION TO MEASUREMENT
===========================

The quantum measurement parallel: choosing to observe only digit count
is equivalent to choosing a measurement basis that destroys interference
information. The information not measured does not disappear — it determines
the orbit destination. The choice of what to measure is the choice of what
to lose.

The observer who sees only 4 digits cannot distinguish:
  - a pattern destined for IC from one destined for SEAM
  - a palindrome from an alternating sequence
  - a pattern carrying full provenance from one that erases it

The unobserved structure is not absent. It determines the outcome.
The peach was always a peach. The measurement did not make it one —
it only decided what you would know about it.

STRUCTURE SUMMARY
==================

  Five patterns, digit count 4 each. N sees five identical objects.

  0000  → SEAM              (trivially null)
  1111  → IC                (uniform → identity cluster; 1111 ≡ 1)
  1234  → NQR_5             (ascending; 1234 ≡ 13)
  1212  → OUTLIER_ORB       (alternating; 1212 ≡ 28)
  1221  → SEAM              (palindrome; 1221 = 33×37)

  1212 and 1221: equal digit sum, product, DR — different orbit destinations.
  The arrangement is the only carrier of the distinction.

  The palindrome collapses. The uniform pattern maps to identity.
  What you cannot see determines what happens.
"""

P = 37

ORBITS = {
    'IC':               frozenset({1, 10, 26}),
    'SOVEREIGN_SPIRAL': frozenset({3, 4, 30}),
    'D7':               frozenset({7, 33, 34}),
    'SA_ORB':           frozenset({9, 12, 16}),
    'ORBIT_11':         frozenset({11, 27, 36}),
    'OUTLIER_ORB':      frozenset({21, 25, 28}),
    'DARK_A':           frozenset({2, 15, 20}),
    'NQR_5':            frozenset({5, 13, 19}),
    'TESLA_ORB':        frozenset({6, 8, 23}),
    'NQR_14':           frozenset({14, 29, 31}),
    'NQR_17':           frozenset({17, 22, 35}),
    'SEED_ORB':         frozenset({18, 24, 32}),
}

PATTERNS = [
    ('0000', 0),
    ('1111', 1111),
    ('1234', 1234),
    ('1212', 1212),
    ('1221', 1221),
]


def orbit_of(v):
    v = v % P
    if v == 0:
        return 'SEAM'
    return next((name for name, s in ORBITS.items() if v in s), '?')


def dr(n):
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


def run_assertions():
    # GF(37) reductions
    assert 0    % P == 0
    assert 1111 % P == 1
    assert 1234 % P == 13
    assert 1212 % P == 28
    assert 1221 % P == 0

    # Orbit classifications
    assert orbit_of(0)    == 'SEAM'
    assert orbit_of(1111) == 'IC'
    assert orbit_of(1234) == 'NQR_5'
    assert orbit_of(1212) == 'OUTLIER_ORB'
    assert orbit_of(1221) == 'SEAM'

    # IC contains 1
    assert 1  in ORBITS['IC']
    # NQR_5 contains 13
    assert 13 in ORBITS['NQR_5']
    # OUTLIER_ORB contains 28
    assert 28 in ORBITS['OUTLIER_ORB']

    # Exact factorization: 1221 = 33 × 37
    assert 1221 == 33 * P

    # 1212 and 1221 share all aggregate observables
    def agg(label):
        d = [int(c) for c in label]
        s = sum(d)
        prod = 1
        for x in d:
            prod *= x
        return s, prod, dr(s)

    assert agg('1212') == agg('1221') == (6, 4, 6)

    # But different orbits
    assert orbit_of(1212) != orbit_of(1221)

    # Palindrome test
    assert list('1221') == list(reversed(list('1221')))
    assert list('1212') != list(reversed(list('1212')))

    # Uniform pattern
    assert len(set('1111')) == 1

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 151: Digit Arrangement, SEAM, Observable Limits")
    print("=" * 62)
    print()
    print(f"  {'Pattern':<8} {'mod 37':>6}  {'Orbit':<18}  Notes")
    print(f"  {'-------':<8} {'------':>6}  {'-----':<18}  -----")
    notes = {
        '0000': 'null',
        '1111': 'uniform → identity; 1111 ≡ 1',
        '1234': 'ascending',
        '1212': 'alternating, period 2',
        '1221': 'palindrome = 33×37',
    }
    for label, n in PATTERNS:
        r = n % P
        print(f"  {label:<8} {r:>6}  {orbit_of(n):<18}  {notes[label]}")
    print()
    print("  1212 vs 1221: digit_sum=6, product=4, DR=6 — identical aggregates")
    print("  1212 → OUTLIER_ORB    1221 → SEAM")
    print("  The arrangement is the only carrier of the distinction.")
    print()
    print("  The palindrome (1221) collapses. The uniform (1111) maps to IC.")
    print("  What you cannot see determines what happens.")


if __name__ == "__main__":
    run_assertions()
    summarise()
