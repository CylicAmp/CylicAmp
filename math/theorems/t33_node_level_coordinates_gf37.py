# CLASS: COMPUTATION
"""
Per-node (X,Y,Z) coordinate table for the T_33 three.js layout
Author: Michael Warren Song (CyclicAmp)

Resolves t33_orbit_invariance_and_transversal_gf37.py's transient-
ambiguity flag at node granularity rather than orbit granularity, so a
deterministic layout can assign one X value per vertex instead of a set.

RULE
    Y-axis: T_33(x), identical for every node in a coset (orbit-constant,
            proven in t33_orbit_invariance_and_transversal_gf37.py)
    Z-axis: orbit / coset identity (12 groups)
    X-axis: transient(x), computed PER NODE. On the six orbits touching
            C_6, the cycle member gets 0 and its two coset-mates get 1
            (they need exactly one more step, to the shared T_33 image,
            which is the cycle node). On the six non-touching orbits,
            X is uniform across the whole coset (2, 3, or 4).

All 36 values checked directly against transient(x) computed from first
principles (iterate T_33 until landing in C_6); zero mismatches.

FALSIFICATION
    Any assert below failing.
"""

P = 37
CYCLE = frozenset({6, 27, 32, 19, 10, 34})


def cube(x):
    return pow(x, 3, P)


def T33(x):
    return (cube(x) + 33) % P


def transient(x):
    k = 0
    while x not in CYCLE:
        x = T33(x)
        k += 1
    return k


# (orbit name, elements, T_33 value, {element: transient})
NODE_TABLE = [
    ("D7",      (7, 33, 34),   6,  {34: 0, 7: 1, 33: 1}),
    ("TESLA",   (6, 8, 23),    27, {6: 0, 8: 1, 23: 1}),
    ("NEG_H",   (11, 27, 36),  32, {27: 0, 11: 1, 36: 1}),
    ("SEED",    (18, 24, 32),  19, {32: 0, 18: 1, 24: 1}),
    ("CAS_EXT", (5, 13, 19),   10, {19: 0, 5: 1, 13: 1}),
    ("IC",      (1, 10, 26),   34, {10: 0, 1: 1, 26: 1}),
    ("C3",       (3, 4, 30),   23, {3: 2, 4: 2, 30: 2}),
    ("SA_ST_B",  (21, 25, 28), 7,  {21: 2, 25: 2, 28: 2}),
    ("DARK_A",   (2, 15, 20),  4,  {2: 3, 15: 3, 20: 3}),
    ("NQR17",    (17, 22, 35), 25, {17: 3, 22: 3, 35: 3}),
    ("SA_ST_A",  (9, 12, 16),  22, {9: 4, 12: 4, 16: 4}),
    ("C9",       (14, 29, 31), 2,  {14: 4, 29: 4, 31: 4}),
]


def run():
    seen = set()
    for name, elements, y_expected, assignment in NODE_TABLE:
        assert set(elements) == set(assignment)
        seen.update(elements)
        y_vals = {T33(x) for x in elements}
        assert y_vals == {y_expected}, (name, y_vals, y_expected)
        for x, claimed_x in assignment.items():
            assert transient(x) == claimed_x, (x, transient(x), claimed_x)

    assert seen == set(range(1, P))  # all 36 nonzero elements covered exactly once

    from collections import Counter
    dist = Counter(x for _, _, _, a in NODE_TABLE for x in a.values())
    assert dict(dist) == {0: 6, 1: 12, 2: 6, 3: 6, 4: 6}

    print("All assertions passed.\n")
    print(f"{'orbit':<9} {'element':>7} {'Y=T_33':>7} {'X=transient':>12}")
    for name, elements, y, assignment in NODE_TABLE:
        for x in elements:
            print(f"{name:<9} {x:>7} {y:>7} {assignment[x]:>12}")


if __name__ == "__main__":
    run()
