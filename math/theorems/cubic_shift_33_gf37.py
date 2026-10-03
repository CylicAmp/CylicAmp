# CLASS: THEOREM
"""
T_33(x) = x^3+33 mod 37: fibers of the cube map, the single 6-cycle, and
where the birthday residues land in it
Author: Michael Warren Song (CyclicAmp)

THE CUBE MAP IS NEVER A PERMUTATION ON F_37
    gcd(3, 36) = 3, so x -> x^3 is 3-to-1 onto an image of size 36/3 = 12,
    plus the fixed image of 0, for 13 image values total. Every fiber of
    a nonzero image value is a coset of mu_3 = {1,10,26} (the kernel of
    the cubing map, T292/T299's unit group).

    mu_3 is exactly the fiber of 1 -- not a separate object from what is
    already on the board, the same order-3 subgroup viewed as a fiber.

T_33(x) = x^3 + 33 (mod 37): ONE 6-CYCLE, WHOLE-FIELD BASIN
    Image (13 values): {2,4,6,7,10,19,22,23,25,27,32,33,34}
    Unique cycle:  6 -> 27 -> 32 -> 19 -> 10 -> 34 -> 6      (length 6)
    Every one of the 37 starting points reaches this cycle in at most 4
    iterations -- verified exhaustively, not sampled.

    Other shifts T_b(x) = x^3+b are NOT all single whole-field attractors:
        b=0:   four attractors  {0}, {1}, {36}, {6,31}
        b=8:   one fixed point  {14}, whole field
        b=26:  one 4-cycle      (0,26,27,25)
        b=33:  the 6-cycle above
    T_33's basin structure is a property of b=33 specifically, not generic
    to the cube map with a shift.

BIRTHDAY RESIDUES UNDER T_33
    Each of the eight date residues from CLAUDE.md's biographical anchor,
    followed until it reaches the cycle:

        3  -> 23 -> 27                  (2 steps, lands on 27)
        6                                (already on-cycle)
        9  -> 22 -> 25 -> 7 -> 6         (4 steps, lands on 6)
        33 -> 6                          (1 step, lands on 6)
        28 -> 7 -> 6                     (2 steps, lands on 6)
        8  -> 27                         (1 step, lands on 27)
        7  -> 6                          (1 step, lands on 6)
        25 -> 7 -> 6                     (2 steps, lands on 6)

    33 (the Easter-gap / T268-shift value) enters the cycle in one step,
    at 6. 3 (month/day) enters at 27, in two steps. Six of the eight
    residues eventually land on 6; only 3 and 8 land on 27.

WHERE 33 CAME FROM, AND WHERE THE ADDITIVE ANTIPODE ACTUALLY IS
    T268's shift constant 33 traces to MICHAEL's letters reduced to
    digital roots and summed: 4+9+3+8+1+5+3 = 33 (a route record, scheme-
    dependent, not a forced identity -- see CLAUDE.md).
    D7 <-> C3 (T265) is a named orbit-taxonomy pairing, distinct from the
    additive antipode in Z/37Z: 3's true additive antipode is 34
    (3+34=37), not 33 (3+33=36, one short of 37). Both facts are recorded
    so they are not conflated.

FALSIFICATION
    Any assert below failing.
"""

from math import gcd

P = 37


def cube(x):
    return pow(x, 3, P)


def T(b):
    return lambda x: (cube(x) + b) % P


def find_cycles(f):
    """All distinct cycles of f on Z/PZ, by iterating from every start."""
    seen_global = set()
    cycles = []
    for x in range(P):
        path, local = [], {}
        cur = x
        while cur not in local and cur not in seen_global:
            local[cur] = len(path)
            path.append(cur)
            cur = f(cur)
        if cur in local:
            cyc = path[local[cur]:]
            if frozenset(cyc) not in (frozenset(c) for c in cycles):
                cycles.append(cyc)
        seen_global.update(path)
    return cycles


def steps_to_cycle(f, cyc, x):
    cyc = set(cyc)
    k = 0
    while x not in cyc:
        x = f(x)
        k += 1
        if k > 4 * P:
            raise AssertionError("did not converge")
    return k


def fibers_of_cube():
    f = {}
    for x in range(P):
        f.setdefault(cube(x), []).append(x)
    return f


BIRTHDAY_RESIDUES = [3, 6, 9, 33, 28, 8, 7, 25]


def run():
    assert gcd(3, 36) == 3
    fib = fibers_of_cube()
    assert len(fib) == 13
    assert fib[1] == [1, 10, 26]                    # mu_3 as a fiber

    f33 = T(33)
    img33 = sorted({f33(x) for x in range(P)})
    assert img33 == [2, 4, 6, 7, 10, 19, 22, 23, 25, 27, 32, 33, 34]

    cycles33 = find_cycles(f33)
    assert len(cycles33) == 1
    assert cycles33[0] == [6, 27, 32, 19, 10, 34]

    max_steps = max(steps_to_cycle(f33, cycles33[0], x) for x in range(P))
    assert max_steps == 4

    expected_tails = {
        3: ([3, 23, 27], 27), 6: ([6], 6), 9: ([9, 22, 25, 7, 6], 6),
        33: ([33, 6], 6), 28: ([28, 7, 6], 6), 8: ([8, 27], 27),
        7: ([7, 6], 6), 25: ([25, 7, 6], 6),
    }
    cyc_set = set(cycles33[0])
    for s, (path, land) in expected_tails.items():
        p = [s]
        if s not in cyc_set:
            while p[-1] not in cyc_set:
                p.append(f33(p[-1]))
        assert p == path, (s, p, path)
        assert p[-1] == land

    # other shifts
    assert find_cycles(T(0)) and sorted(map(sorted, find_cycles(T(0)))) == \
        sorted(map(sorted, [[0], [1], [36], [6, 31]]))
    assert find_cycles(T(8)) == [[14]]
    c26 = find_cycles(T(26))
    assert len(c26) == 1 and set(c26[0]) == {0, 26, 27, 25}

    assert (3 + 34) % P == 0 and (3 + 33) % P == 36  # antipode correction

    print("All assertions passed.\n")
    print(f"Cube map: gcd(3,36)={gcd(3,36)}, image size {len(fib)}, mu_3 = fiber(1) = {fib[1]}\n")
    print(f"T_33 image ({len(img33)}): {img33}")
    print(f"T_33 cycle: {' -> '.join(map(str, cycles33[0] + [cycles33[0][0]]))}")
    print(f"max steps to reach cycle from any of 37 starts: {max_steps}\n")
    print("Birthday residues under T_33:")
    for s in BIRTHDAY_RESIDUES:
        path, land = expected_tails[s]
        route = " -> ".join(map(str, path))
        print(f"  {s:3d}: {route:<24} lands on {land}")
    print()
    print("Other shifts (measured, not generic):")
    print("  b=0:  four attractors {0},{1},{36},{6,31}")
    print("  b=8:  one fixed point {14}")
    print("  b=26: one 4-cycle (0,26,27,25)")
    print("  b=33: the 6-cycle above")


if __name__ == "__main__":
    run()
