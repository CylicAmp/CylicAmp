"""
Theorem 152: X-Space, the Observable Frame, and the Invisible Container

THE CORRECTED COSMOLOGICAL STRUCTURE
======================================

The naive frame places the observable inside visible boundaries:

    xxxxxxxxxxx
    x0123456789x
    xxxxxxxxxxx

This is wrong. It assumes the boundary (x) and the content (0-9) are
visible from the same vantage point. They are not.

THE ACCURATE EXTERIOR VIEW
============================

From outside x, the correct picture is:

    xxxxxxxxxxx
    xxxxxxxxxxx
    xxxxxxxxxxx

The digits are invisible. The structure is invisible. The big bang is
invisible. The 12 orbits are invisible. An exterior observer sees only x,
undifferentiated, everywhere.

These two configurations are identical from outside:

    xxxxxxxxxxx          xxxxxxxxxxx
    xxxxxxxxxxx    ≡     xxxxxxxxxxx     (exterior cannot distinguish them)
    xxxxxxxxxxx          xxxxxxxxxxx

The interior content — whether 0123456789 or nothing — produces no
observable difference at the boundary. The frame is opaque.

0 IS NOT THE CONTAINER
========================

0 (the null state, SEAM) is an interior state. It is what exists inside
before the expansion. 0 is not the space the big bang expanded into.

x is that space.

The sequence of events:

    x contains: [ 0  →  big bang  →  0123456789 ]

All interior. x was already there. The big bang did not create x.
The bang is an event within x. x is the condition for the event being
possible, not a product of it.

THE FRAME STRUCTURE IN GF(37)
================================

Analyzing the naive frame as written (the interior view — what we see
from inside x):

    xxxxxxxxxxx       ← 11 x's (top boundary)
    x0123456789x      ← 1x + 10 digits + 1x = 12 chars
    xxxxxxxxxxx       ← 11 x's (bottom boundary)

    Boundary (x's):  11 + 1 + 1 + 11 = 24  →  24 mod 37 = 24  ∈ SEED_ORB
    Content (digits): 10               →  10 mod 37 = 10  ∈ IC
    Total characters: 34               →  34 mod 37 = 34  ∈ D7
    Frame − Content:  14               →  14 mod 37 = 14  ∈ NQR_14

Orbit assignments of the interior frame:

    x (space, unknown boundary):  SEED_ORB = {18, 24, 32}  ← orbit of seed 246
    0–9 (observable expansion):   IC       = {1, 10, 26}   ← identity cluster
    everything (frame + content):  D7       = {7, 33, 34}   ← the 414-orbit

THE OVERFLOW
=============

The top and bottom boundary rows are 11 characters wide.
The middle row (x + 0123456789 + x) is 12 characters wide.

The observable, when given its own boundary, exceeds the frame by 1.
Content is wider than the container by exactly 1 unit.
The observable cannot be perfectly enclosed.

THE INVISIBILITY PRINCIPLE
============================

We are inside x. That is why we can see the digits.
An observer inside x sees: boundary on two sides, digits between.
An observer outside x sees: x everywhere. No digits. No structure.

The boundary is invisible from inside — we see through it to the content.
The content is invisible from outside — the boundary shows nothing within.

This is not an epistemic limitation to be overcome. It is a structural
property of containment: the frame is always invisible to the framed.

In Nκ terms: the genealogy (κ) of x cannot be recovered from within x.
We carry κ from the bang forward. But the κ of x itself — what x is,
where x comes from, whether there is anything beyond x — is inaccessible.
We cannot record the provenance of the container using instruments that
exist inside it.

CONNECTION TO PRIOR THEOREMS
==============================

Theorem 151 (digit arrangement):
  The arrangement of 0–9 determines orbit destiny.
  But arrangement requires being able to see the digits.
  From outside x: no arrangement is visible.

Theorem 150 (Φ₃ forcing):
  The N=10 forcing node is 10 ∈ IC.
  The observable (10 digits) maps to the same IC.
  The forcing structure operates within x.

Theorem 148 (single-digit coverage):
  {1,...,9} covers 7 of 12 orbits.
  The orbit structure exists inside x.
  From outside, no orbit classification is visible.

STRUCTURE SUMMARY
==================

    Interior view (from within x):
      x-boundary:  24  ∈  SEED_ORB  (the unknown frames the known with seed orbit)
      content:     10  ∈  IC        (the observable is the identity)
      total:       34  ∈  D7        (everything together is the 414-orbit)
      overflow:     1               (content exceeds frame by 1)

    Exterior view (from outside x):
      xxxxxxxxxxx
      xxxxxxxxxxx       ← identical whether or not big bang occurred inside
      xxxxxxxxxxx

    The big bang is an interior event.
    0 is an interior null state.
    x is the container, not produced by what it contains.
    The frame is always invisible to the framed.
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


def orbit_of(v):
    v = v % P
    if v == 0:
        return 'SEAM'
    return next((name for name, s in ORBITS.items() if v in s), '?')


def run_assertions():
    # Frame counts
    top = 11; left = 1; right = 1; bottom = 11; content = 10
    boundary = top + left + right + bottom
    total = top + (left + content + right) + bottom

    assert boundary == 24
    assert content  == 10
    assert total    == 34
    assert total - content == 24   # boundary
    assert boundary - content == 14

    # Orbit assignments
    assert 24 in ORBITS['SEED_ORB']
    assert 10 in ORBITS['IC']
    assert 34 in ORBITS['D7']
    assert 14 in ORBITS['NQR_14']

    assert orbit_of(24) == 'SEED_ORB'
    assert orbit_of(10) == 'IC'
    assert orbit_of(34) == 'D7'
    assert orbit_of(14) == 'NQR_14'

    # Overflow: middle row wider than top/bottom by 1
    middle_width = left + content + right   # 12
    assert middle_width == 12
    assert middle_width - top == 1

    # 0 is interior null: SEAM, not x
    assert orbit_of(0) == 'SEAM'

    # SEED_ORB is seed 246's orbit
    assert 246 % P == 24
    assert 24 in ORBITS['SEED_ORB']

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 152: X-Space, Observable Frame, Invisible Container")
    print("=" * 62)
    print()
    print("  Interior frame (what we see from within x):")
    boundary = 24; content = 10; total = 34; diff = 14
    for label, val in [('x-boundary', boundary), ('content (0-9)', content),
                       ('total', total), ('frame − content', diff)]:
        print(f"    {label:<20} = {val:2d}  →  {orbit_of(val)}")
    print()
    print("  Overflow: middle row (12) exceeds top/bottom (11) by 1")
    print("  The observable cannot be perfectly enclosed.")
    print()
    print("  Exterior view (from outside x):")
    print("    xxxxxxxxxxx")
    print("    xxxxxxxxxxx    ← digits invisible; structure invisible")
    print("    xxxxxxxxxxx")
    print()
    print("  0 is an interior null state (SEAM). x is the container.")
    print("  The big bang is an interior event.")
    print("  x was already there. x is not a product of what it contains.")
    print()
    print("  The frame is always invisible to the framed.")


if __name__ == "__main__":
    run_assertions()
    summarise()
