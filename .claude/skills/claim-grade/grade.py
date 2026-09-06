#!/usr/bin/env python3
"""
The four cuts of T305, runnable.

    python3 grade.py                 the checklist, blank
    python3 grade.py --examples      the graded claims
    python3 grade.py --check-eca 30  is elementary rule N the GF(2) Laplacian?
    python3 grade.py --axes          assert the three axes stay independent
"""
import sys
import itertools

N = 8                                   # ring size for exhaustive ECA checks

CUTS = [
    ("1  literal / structural",
     "Same object (or a defined discretization) on both sides, or only the",
     "same ROLE? Look for the literal object first — if it exists and is a",
     "different object, the claim is decided, not a matter of taste."),
    ("2  level 1 / 2 / 3",
     "1 role named | 2 map Phi specified and a named relation survives it |",
     "3 proved implication with hypotheses, conclusion, and the failure mode",
     "when a hypothesis is dropped."),
    ("3  native / correspondence",
     "Is the strength being claimed for the target theory on its own ground,",
     "or for the identification? A mature target does not upgrade the map.",
     ""),
    ("4  Phi / functor",
     "Both live at Level 2. A functor needs C, D and preservation of",
     "identities and composition. 'Functorial' without them is still Level 1.",
     ""),
]

# (claim, tier A/B/C, correspondence level, can the test come back negative)
GRADED = [
    ('ord_37(27)=6, six 6-cycles',          'C', 3, True),
    ('"that 6-cycle is discrete curl"',     'C', 1, False),
    ('antipodal pairing exists',            'A', 3, True),
    ('"DARK_A occupancy is neg. divergence"', 'C', 1, False),
    ('m != +-1 mod p for twin midpoints',   'A', 3, True),
    ('ord_p(137)=3 => p in {7,37,73}',      'B', 3, True),
    ('"Sigma verification is Stokes"',      'A', 1, False),
    ('rule 90 = Delta over GF(2)',          'A', 3, True),
    ('"rule 30 is the discrete Laplacian"', 'A', 1, True),
    ('37 unique with ord_p(10)=3',          'C', 3, True),
    ('"security is a functor to ext. calc"', 'A', 1, False),
    ('p = n^2+1 for CM unit count n',       'C', 3, True),
]


def eca(num):
    return lambda l, c, r: (num >> (l * 4 + c * 2 + r)) & 1


def step(f, s):
    n = len(s)
    return tuple(f(s[(i - 1) % n], s[i], s[(i + 1) % n]) for i in range(n))


def laplacian_mod2(s):
    n = len(s)
    return tuple((s[(i - 1) % n] - 2 * s[i] + s[(i + 1) % n]) % 2
                 for i in range(n))


def is_linear(num):
    f = eca(num)
    if f(0, 0, 0):
        return False
    return all(step(f, tuple(x ^ y for x, y in zip(a, b)))
               == tuple(x ^ y for x, y in zip(step(f, a), step(f, b)))
               for a in itertools.product((0, 1), repeat=4)
               for b in itertools.product((0, 1), repeat=4))


def check_eca(num):
    states = list(itertools.product((0, 1), repeat=N))
    matches = all(step(eca(num), s) == laplacian_mod2(s) for s in states)
    all_hits = [r for r in range(256)
                if all(step(eca(r), s) == laplacian_mod2(s) for s in states)]
    lin = [r for r in range(256) if is_linear(r)]
    print(f"rule {num}: local table "
          f"{[eca(num)(*b) for b in itertools.product((0,1),repeat=3)]}")
    print(f"  over GF(2), u[i-1] - 2u[i] + u[i+1] = u[i-1] + u[i+1]  (-2 = 0)")
    print(f"  equals that on all {len(states)} states of an {N}-cell ring: {matches}")
    print(f"  exhaustive over all 256 ECA, the rules that do: {all_hits}")
    print(f"  GF(2)-linear ECA: {lin}")
    print(f"  rule {num} linear: {is_linear(num)}")
    print()
    if matches:
        print(f"  CUT 1: LITERAL. Rule {num} is the discrete Laplacian over GF(2).")
    elif all_hits:
        print(f"  CUT 1: FAILS. The literal object exists and is rule {all_hits[0]},")
        print(f"         a different rule. Not a taste call — decided.")
        if not is_linear(num):
            print(f"         Rule {num} is not GF(2)-linear, so the role (linear")
            print(f"         second difference) is not shared either.")
    print("  SCOPE: nearest-neighbour ECA on a line or cycle, over GF(2).")
    print("         Not the Hodge Laplacian d.delta+delta.d, not Delta over R.")
    return matches


def check_axes():
    tier = [c[1] for c in GRADED]
    lvl = [c[2] for c in GRADED]
    fals = [c[3] for c in GRADED]

    def determines(x, y):
        m = {}
        for a, b in zip(x, y):
            if m.setdefault(a, b) != b:
                return False
        return True

    named = (('tier', tier), ('level', lvl), ('falsifiable', fals))
    for na, a in named:
        for nb, b in named:
            if na == nb:
                continue
            assert not determines(a, b), \
                f"{na} determines {nb} — the axes have collapsed"
            print(f"  {na:<12} does NOT determine {nb}")
    assert any(t == 'A' and l == 1 for _, t, l, _ in GRADED), \
        "need a Tier A claim that is only Level 1"
    assert any(t == 'C' and l == 3 for _, t, l, _ in GRADED), \
        "need a Tier C claim that is Level 3"
    assert any(f and l == 1 for _, _, l, f in GRADED), \
        "need a falsifiable claim that is still Level 1"
    print("\n  witnesses present: Tier A at Level 1, Tier C at Level 3,")
    print("  and a falsifiable claim that is still Level 1.")
    return True


def show_examples():
    print(f"  {'claim':<40}{'tier':<6}{'level':<7}test can fail")
    for name, t, l, f in GRADED:
        print(f"  {name:<40}{t:<6}L{l:<6}{f}")
    print("\n  weakest cut governs:")
    print('    "rule 30 is the discrete Laplacian"  fails Cut 1')
    print('    "DARK_A occupancy is neg. divergence" L1; fails L2 until a')
    print("                                          discrete div is defined")
    print('    "Sigma verification is Stokes"        L1; fails Cut 3')
    print('    "security is a functor to ext. calc"  fails Cut 4; not even L2')


def checklist():
    print(__doc__.strip())
    print()
    for head, *lines in CUTS:
        print(f"CUT {head}")
        for l in lines:
            if l:
                print(f"     {l}")
        print()
    print("Then: state the SCOPE, and report the weakest cut. That is the grade.")
    print("Do not substitute a Tier (forced-check) or a p-value (miss-test)")
    print("for a level. The three axes are independent — see --axes.")


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        checklist()
    elif a[0] == '--examples':
        show_examples()
    elif a[0] == '--axes':
        check_axes()
    elif a[0] == '--check-eca':
        check_eca(int(a[1]))
    else:
        print(__doc__)
        sys.exit(1)
