"""
THEOREM 115 — Primitive Roots mod 37 in the Heegner–Rabinowitsch Difference Set

NOTATION
    D       = |a - b| ∈ ℤ                  (exact integer difference)
    D mod 37 ∈ {0,…,36}                     (residue class in ℤ/37ℤ)
    These coincide if and only if 0 ≤ D < 37.

PRIMITIVE ROOTS MODULO 37
    g is a primitive root mod 37 iff ord₃₇(g) = φ(37) = 36.
    The multiplicative group (ℤ/37ℤ)× is cyclic of order 36.
    There are exactly φ(36) = 12 primitive roots:

        {2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35}

SETS
    R = {2, 3, 5, 11, 17, 41}                    (Rabinowitsch primes)
    H = {3, 4, 7, 8, 11, 19, 43, 67, 163}        (Heegner absolute values)

EXACT DIFFERENCES < 37 THAT ARE PRIMITIVE ROOTS
    Nine exact differences D = |a−b| < 37 drawn from pairs in R ∪ H
    have D ∈ PR:

        D =  2:  |4−2|, |5−3|, |7−5|, |19−17|, |43−41|   (cross / R&H / cross / cross / cross)
        D =  5:  |7−2|, |8−3|                               (cross / R&H)
        D = 13:  |17−4|                                      (cross: 17∈R, 4∈H)
        D = 15:  |17−2|, |19−4|                             (R-R, H-H)
        D = 17:  |19−2|                                      (cross)
        D = 22:  |41−19|                                     (cross)
        D = 24:  |41−17|, |43−19|, |67−43|                 (R-R, H-H, H-H)
        D = 32:  |43−11|                                     (R&H)
        D = 35:  |43−8|                                      (H-H)

    The overlap is exactly {2, 5, 13, 15, 17, 22, 24, 32, 35} — nine elements.

    Note on 13: the classifier in Theorem 114 labels D=13 as [CB] (cascade base
    {8,13,24}) because CB is checked first. But 13 is simultaneously a primitive
    root. ord₃₇(13) = 36 is verified below.

DOUBLE-MEMBERSHIP OF PRIMITIVE ROOTS IN OTHER NAMED CLASSES
    Six of the twelve primitive roots also belong to other named framework sets:

        13  ∈ CB         ∩ PR
        17  ∈ BASIN_Y    ∩ PR
        18  ∈ SEED_ORBIT ∩ PR
        22  ∈ BASIN_Y    ∩ PR
        24  ∈ CB ∩ SEED_ORBIT ∩ PR
        32  ∈ SEED_ORBIT ∩ PR
        35  ∈ BASIN_Y    ∩ PR

    The remaining six primitive roots {2, 5, 15, 19, 20} have no additional
    named-class membership.

PRIMITIVE ROOTS ABSENT FROM THE DIFFERENCE SET
    Three primitive roots do not appear as any exact difference < 37
    among pairs in R ∪ H:

        {18, 19, 20}

    They are absent from both the within-list and cross-list tables.
"""

P = 37

SA         = {4, 9, 25, 30}
ST         = {3, 12, 21, 30}
IC         = {1, 10, 26}
CB         = {8, 13, 24}
ORBIT_11   = {11, 27, 36}
SEED_ORBIT = {18, 24, 32}
BASIN_Y    = {17, 22, 35}
D7         = {7, 33, 34}
PR         = {2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35}

R = [2, 3, 5, 11, 17, 41]
H = [3, 4, 7, 8, 11, 19, 43, 67, 163]


def multiplicative_order(g, p):
    g = g % p
    if g == 0:
        return None
    o, x = 1, g
    while x != 1:
        x = (x * g) % p
        o += 1
    return o


def run():
    print("=" * 70)
    print("THEOREM 115 — PRIMITIVE ROOTS mod 37 IN THE H–R DIFFERENCE SET")
    print("=" * 70)

    # ---------------------------------------------------------------
    # PART 1 — Verify the complete list of primitive roots mod 37
    # ---------------------------------------------------------------
    print("\n--- Part 1: Primitive roots mod 37 ---")
    prim_roots = [g for g in range(1, P) if multiplicative_order(g, P) == P - 1]
    assert prim_roots == sorted(PR), f"Mismatch: {prim_roots}"
    assert len(prim_roots) == 12

    # phi(36) = phi(4) * phi(9) = 2 * 6 = 12
    from sympy import totient
    assert totient(36) == 12

    print(f"  Primitive roots: {prim_roots}")
    print(f"  Count: {len(prim_roots)} = φ(36) = {totient(36)}")

    # Verify orders
    for g in prim_roots:
        assert multiplicative_order(g, P) == 36, f"ord₃₇({g}) ≠ 36"
    # Verify non-primitive-roots have order < 36
    for g in range(1, P):
        if g not in prim_roots:
            assert multiplicative_order(g, P) < 36, f"{g} should not be primitive root"
    print(f"  All 36 multiplicative orders verified.")

    # ---------------------------------------------------------------
    # PART 2 — All exact differences < 37 from R ∪ H
    # ---------------------------------------------------------------
    print("\n--- Part 2: Exact differences D < 37 from pairs in R ∪ H ---")
    universe = sorted(set(R + H))

    diff_sources = {}
    for i, a in enumerate(universe):
        for b in universe[i + 1:]:
            d = abs(b - a)
            if d < P:
                in_r_a = a in R; in_h_a = a in H
                in_r_b = b in R; in_h_b = b in H
                if in_r_a and in_r_b and not in_h_a and not in_h_b:
                    src = 'R-R'
                elif in_h_a and in_h_b and not in_r_a and not in_r_b:
                    src = 'H-H'
                elif (in_r_a and in_h_a) or (in_r_b and in_h_b):
                    src = 'R∩H'
                else:
                    src = 'cross'
                diff_sources.setdefault(d, []).append((a, b, src))

    all_exact_diffs = set(diff_sources.keys())
    print(f"  Distinct exact values D < 37: {sorted(all_exact_diffs)}")

    # ---------------------------------------------------------------
    # PART 3 — Overlap with primitive roots
    # ---------------------------------------------------------------
    print("\n--- Part 3: Exact differences D < 37 that are primitive roots ---")
    overlap = sorted(all_exact_diffs & set(prim_roots))
    assert overlap == [2, 5, 13, 15, 17, 22, 24, 32, 35], \
        f"Overlap mismatch: {overlap}"

    for d in overlap:
        srcs = diff_sources[d]
        pairs_str = ', '.join(f"|{b}-{a}|({s})" for a, b, s in srcs)
        print(f"  D={d:>2}  ord₃₇({d})={multiplicative_order(d,P)}  pairs: {pairs_str}")

    # D=13 special note
    assert 13 in CB and 13 in PR, "13 ∈ CB ∩ PR"
    assert multiplicative_order(13, P) == 36, "ord₃₇(13) = 36"
    print(f"\n  Note: D=13 is labeled [CB] by the Theorem 114 classifier (CB checked first)")
    print(f"        but ord₃₇(13)={multiplicative_order(13,P)} — 13 is simultaneously in CB ∩ PR.")

    # ---------------------------------------------------------------
    # PART 4 — Double membership of primitive roots
    # ---------------------------------------------------------------
    print("\n--- Part 4: Primitive roots with double class membership ---")
    named_classes = [('IC', IC), ('SA', SA), ('ST', ST), ('CB', CB),
                     ('ORBIT_11', ORBIT_11), ('SEED_ORBIT', SEED_ORBIT),
                     ('BASIN_Y', BASIN_Y), ('D7', D7)]
    double = {}
    for g in prim_roots:
        extra = [nm for nm, cls in named_classes if g in cls]
        double[g] = extra

    double_members = {g: v for g, v in double.items() if v}
    pure_pr        = {g: v for g, v in double.items() if not v}

    assert double_members == {
        13: ['CB'],
        17: ['BASIN_Y'],
        18: ['SEED_ORBIT'],
        22: ['BASIN_Y'],
        24: ['CB', 'SEED_ORBIT'],
        32: ['SEED_ORBIT'],
        35: ['BASIN_Y'],
    }, f"Double-member mismatch: {double_members}"

    for g, tags in sorted(double_members.items()):
        print(f"  {g:>2}  ∈ {' ∩ '.join(tags)} ∩ PR")

    print(f"\n  Primitive roots with no other named-class membership:")
    print(f"    {sorted(pure_pr.keys())}")

    # ---------------------------------------------------------------
    # PART 5 — Primitive roots absent from the difference set
    # ---------------------------------------------------------------
    print("\n--- Part 5: Primitive roots absent from all exact differences < 37 ---")
    absent = sorted(set(prim_roots) - all_exact_diffs)
    assert absent == [18, 19, 20], f"Absent mismatch: {absent}"
    for g in absent:
        extra = double[g]
        tag   = f"∈ {extra[0]}" if extra else "(pure PR)"
        print(f"  {g}  {tag}  — not a difference of any pair in R ∪ H")

    # ---------------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------------
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  12 primitive roots mod 37: {prim_roots}")
    print(f"  9 appear as exact D < 37: {overlap}")
    print(f"  3 absent from difference set: {absent}")
    print(f"  6 primitive roots have double class membership")
    print(f"  D=13 (CB ∩ PR) was obscured by classifier priority in Theorem 114")
    print()
    print("All assertions passed. THEOREM 115 verified.")


if __name__ == "__main__":
    run()
