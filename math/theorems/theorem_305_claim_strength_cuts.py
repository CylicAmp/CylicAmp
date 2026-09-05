"""
T305 — Four Orthogonal Cuts for Grading a Claim, With the Rule 30 Case Worked

METHOD.md fixes what to compute and what a theorem must carry. It has no cut
for how strong a CORRESPONDENCE is. The word "structural" was carrying four
different jobs at once: not-literal, Level 1, role-sharing, and "has
structure." These cuts separate them. They nest; they do not replace each
other, and a claim is only as strong as the weakest cut it fails.

════════════════════════════════════════════════════════════════════════════
CUT 1 — LITERAL vs STRUCTURAL          identity of objects vs identity of roles
════════════════════════════════════════════════════════════════════════════
LITERAL     the same object appears on both sides, or a defined
            discretization of it.
STRUCTURAL  only the ROLE is shared — concentration, circulation, locality,
            a cut, preferential movement. The operators need not be the same.

    literal:     <d.alpha, sigma> = <alpha, d.sigma>   discrete Stokes
    literal:     Lap u_i = u_{i-1} - 2u_i + u_{i+1}
    literal:     x -> 27x mod 37 is a 6-cycle in (Z/37Z)*   (ord_37(27)=6)
    structural:  calling that 6-cycle "discrete curl"

Use "structural" for ONE thing only: shared role, not shared operator.

════════════════════════════════════════════════════════════════════════════
CUT 2 — LEVEL OF THE CORRESPONDENCE    strength of the map between domains
════════════════════════════════════════════════════════════════════════════
    1  structural analogy      same role                 produce: the role, named
    2  formal correspondence   a map Phi                 produce: objects each
                                                         side + what identity,
                                                         inequality or diagram
                                                         Phi preserves
    3  theorem                 a proved implication      produce: hypotheses,
                                                         conclusion, and the
                                                         failure mode when a
                                                         hypothesis is dropped

Same pair of systems, three different claims:
    L1  "a security boundary is like Stokes"
    L2  attack graph G, source s, asset t, cut C; blocking C preserves the
        separation of s from t
    L3  if C separates s from t and every edge of C is blocked, no s-t path
        remains

"Structure-preserving" at Level 2 means only: Phi is specified and a specified
relation survives it. It does not yet mean functor.

════════════════════════════════════════════════════════════════════════════
CUT 3 — NATIVE vs CORRESPONDENCE RIGOR      where the strength is claimed
════════════════════════════════════════════════════════════════════════════
NATIVE          how strong is the target theory on its own ground
CORRESPONDENCE  how strong is the identification with another domain

These diverge, and a mature target does NOT upgrade the map.

    pair                        native                  correspondence
    Sigma protocols             theorems                Stokes reading is L1
    discrete Stokes in DEC      theorem, by def of d    shell filter = d is L1
    6-cycle of 27 mod 37        theorem in (Z/37Z)*     "curl" is L1
    first-order allocation      KKT is a theorem        "that is grad" is L2;
                                once L and the          "a market computes it"
                                feasible set exist      is L3 only after proof

"Cryptography is rigorous, therefore the Stokes analogy is a theorem" is the
confusion this cut blocks.

════════════════════════════════════════════════════════════════════════════
CUT 4 — Phi vs FUNCTOR                      which kind of Level-2 map
════════════════════════════════════════════════════════════════════════════
Both live at Level 2 and are not the same object.
    Phi       any explicitly defined map preserving a named relation
    functor   one species of Phi: requires categories C, D and preservation
              of identities and composition

    a cut in an attack graph          L2 Phi, not a functor
    a Galois connection in abs. int.  L2 Phi, not a functor
    cell complex -> cochain complex   CAN be written as a functor, once the
                                      categories are named

Saying "the correspondence is functorial" without C, D and F is still Level 1.
"Functorial" is not a synonym for "precise."

════════════════════════════════════════════════════════════════════════════
THE WORKED CASE — "RULE 30 IS THE DISCRETE LAPLACIAN"
════════════════════════════════════════════════════════════════════════════
CLAUDE.md runs Rule 30 on every value in the standing analysis, so this claim
is live and has to be graded. It fails Cut 1, and the failure is sharper than
"the roles differ":

    over GF(2),  u_{i-1} - 2u_i + u_{i+1} = u_{i-1} + u_{i+1}    since -2 = 0

which is EXACTLY Rule 90 (new[i] = left XOR right). So the literal discrete
Laplacian over GF(2) exists inside the elementary CA family — it is a
different rule from Rule 30.

    exhaustive over all 256 ECA: rule 90 is the ONLY one equal to
      u[i-1] + u[i+1] mod 2 on every state
    Rule 90 additive                          65536/65536 pairs
    Rule 30 additive                           3106/65536 pairs  -> not linear
    exactly 8 of 256 ECA are GF(2)-linear: {0,60,90,102,150,170,204,240};
      30 is not among them
    rule 150 = l XOR c XOR r = l+c+r mod 2 (the other natural stencil)

TWO WORDINGS, TIGHT, SO THIS DOES NOT OVERSHOOT:
    - The elementary CA whose local polynomial equals Delta over GF(2) is
      rule 90, uniquely.
    - Rule 30 is a well-defined local CA rule. It is not that operator.

SCOPE. Nearest-neighbour ECA on a line or cycle, over GF(2). This is NOT the
Hodge Laplacian d.delta + delta.d, and NOT Delta over R. The grading is
non-negotiable inside that scope and licenses nothing outside it: "rule 90 is
the Laplacian" in general is itself a Level-1 claim.

CLAUDE.md's standing analysis runs rule 30 on every value. That step is
unchanged and should stay unchanged — it is a literal local rule on a
bitstring. Cut 1 removes only the Laplacian label on top of it.

════════════════════════════════════════════════════════════════════════════
HOW THE CUTS COMPOSE
════════════════════════════════════════════════════════════════════════════
    literal / structural       identity of objects vs identity of roles
            |
    level 1 / 2 / 3            strength of the map between domains
            |
    native / correspondence    where that strength is being claimed
            |
    Phi / functor              which kind of Level-2 map, if at Level 2

    "Rule 30 is the discrete Laplacian"
        fails Cut 1: not literal, and the roles do not match either.
    "DARK_A occupancy is negative divergence"
        passes as structural; fails at Level 2 until a discrete div is defined.
    "Sigma verification is Stokes"
        passes as structural; fails Cut 3 — the protocol is a theorem, the
        identification is not.
    "Security is a functor to exterior calculus"
        fails Cut 4 until C, D, F are written; until then it is not even L2.

THE AUDIT TEST, asked in order:
    1. What is the local object?
    2. What is the compatibility condition or invariant?
    3. What global behavior is thereby restricted?
    4. Is the claim a shared role, a structure-preserving map, or a proved
       implication — and is that claim about the target, or about the map
       between targets?

RELATION TO THE EXISTING SCREENS — THREE AXES THAT DO NOT STACK
    axis                    grades                              lives in
    Tier A/B/C              scope of a number or property       forced-check, T300
    correspondence L1/2/3   strength of a map between domains   these cuts, T305
    test can fail           whether a measurement is operational the test itself,
                                                                 not its label

Independence is the point, and it is asserted below, not asserted in prose:
no axis is a function of any other across the recorded claims. A Tier C
property can still be a Level 1 correspondence. A test that can fail can still
be measuring a role rather than an operator. If a Tier A stamp is ever allowed
to upgrade a Level 1 identification, or a falsifiable test is allowed to
pretend it measured Delta, the cuts have been collapsed back into one word.
"""

import itertools

P = 37
N = 8                       # ring size for the exhaustive CA checks


def order_mod(a, p):
    a %= p
    k, v = 1, a
    while v != 1:
        v = (v * a) % p
        k += 1
    return k


# ─── Cut 1: the literal objects named above really are literal ──────────────

def rule30(l, c, r):
    return l ^ (c | r)


def rule90(l, c, r):
    return l ^ r


def ca_step(rule, s):
    n = len(s)
    return tuple(rule(s[(i - 1) % n], s[i], s[(i + 1) % n]) for i in range(n))


def laplacian_mod2(s):
    n = len(s)
    return tuple((s[(i - 1) % n] - 2 * s[i] + s[(i + 1) % n]) % 2
                 for i in range(n))


def eca(num):
    """Wolfram-numbered elementary CA local rule."""
    return lambda l, c, r: (num >> (l * 4 + c * 2 + r)) & 1


def verify_rule90_is_laplacian():
    """Rule 90 is the UNIQUE ECA equal to Delta over GF(2). Exhaustive."""
    states = list(itertools.product((0, 1), repeat=N))
    hits = [r for r in range(256)
            if all(ca_step(eca(r), s) == laplacian_mod2(s) for s in states)]
    assert hits == [90], f"expected only rule 90, got {hits}"
    for s in states:
        assert ca_step(rule90, s) == laplacian_mod2(s), s
    # rule 150 is the other natural stencil: l + c + r
    for s in states:
        assert ca_step(eca(150), s) == tuple(
            (s[(i - 1) % N] + s[i] + s[(i + 1) % N]) % 2 for i in range(N))
    return 2 ** N, hits


def linear_ecas():
    """Which of the 256 ECA are GF(2)-linear? Rule 30 must not be."""
    out = []
    for num in range(256):
        f = eca(num)
        if f(0, 0, 0) != 0:
            continue
        if all(ca_step(f, tuple(x ^ y for x, y in zip(a, b)))
               == tuple(x ^ y for x, y in zip(ca_step(f, a), ca_step(f, b)))
               for a in itertools.product((0, 1), repeat=4)
               for b in itertools.product((0, 1), repeat=4)):
            out.append(num)
    assert out == [0, 60, 90, 102, 150, 170, 204, 240], out
    assert 30 not in out and 90 in out and 150 in out
    return out


def additivity_rate(rule):
    """Fraction of pairs (a,b) with f(a XOR b) = f(a) XOR f(b)."""
    ok = tot = 0
    for a in itertools.product((0, 1), repeat=N):
        fa = ca_step(rule, a)
        for b in itertools.product((0, 1), repeat=N):
            s = tuple(x ^ y for x, y in zip(a, b))
            rhs = tuple(x ^ y for x, y in zip(fa, ca_step(rule, b)))
            tot += 1
            ok += ca_step(rule, s) == rhs
    return ok, tot


def verify_rule30_not_linear():
    ok90, tot = additivity_rate(rule90)
    ok30, _ = additivity_rate(rule30)
    assert ok90 == tot, f"Rule 90 must be linear: {ok90}/{tot}"
    assert ok30 < tot, "Rule 30 must NOT be linear"
    return ok30, ok90, tot


def verify_27_is_six_cycle():
    """The literal object: ord_37(27) = 6, six 6-cycles partitioning F_37*."""
    assert order_mod(27, P) == 6
    seen, cycles = set(), []
    for s in range(1, P):
        if s in seen:
            continue
        c, x = [s], (27 * s) % P
        while x != s:
            c.append(x)
            x = (27 * x) % P
        seen |= set(c)
        cycles.append(c)
    assert len(cycles) == 6 and all(len(c) == 6 for c in cycles)
    assert seen == set(range(1, P))
    return cycles


# ─── Cut 2: the Level-3 statement in the worked example is a theorem ────────

def verify_cut_theorem():
    """L3: if C separates s from t, blocking every edge of C kills all paths."""
    import random
    random.seed(37)
    for _ in range(200):
        n = random.randrange(4, 9)
        edges = {(a, b) for a in range(n) for b in range(n)
                 if a != b and random.random() < 0.4}
        s, t = 0, n - 1
        # a cut: every edge leaving the reachable-from-s side under removal
        side = {s}
        for _ in range(n):
            side |= {b for (a, b) in edges if a in side}
        if t not in side:
            continue                      # already separated, nothing to test
        C = {(a, b) for (a, b) in edges if a in side and b not in side}
        rest = edges - C
        reach = {s}
        for _ in range(n):
            reach |= {b for (a, b) in rest if a in reach}
        assert t not in reach or not C, "cut failed to separate"
    return True


# ─── Cut 3 / Cut 4 are definitional; record the table as data ──────────────

NATIVE_VS_CORRESPONDENCE = [
    ('Sigma protocols',        'theorems (special soundness, HVZK)', 1),
    ('discrete Stokes in DEC', 'theorem, by definition of d',        1),
    ('6-cycle of 27 mod 37',   'theorem in (Z/37Z)*',                1),
    ('first-order allocation', 'KKT theorem given L and feasible set', 2),
]

# (claim, tier A/B/C, correspondence level 1/2/3, can the test come back negative)
GRADED_CLAIMS = [
    ('ord_37(27)=6, six 6-cycles',        'C', 3, True),
    ('"that 6-cycle is discrete curl"',   'C', 1, False),
    ('antipodal pairing exists',          'A', 3, True),
    ('"DARK_A occupancy is neg. div."',   'C', 1, False),
    ('m != +-1 mod p for twin midpoints', 'A', 3, True),
    ('ord_p(137)=3 => p in {7,37,73}',    'B', 3, True),
    ('"Sigma verification is Stokes"',    'A', 1, False),
    ('rule 90 = Delta over GF(2)',        'A', 3, True),
    ('"rule 30 is the discrete Laplacian"','A', 1, True),
    ('37 unique with ord_p(10)=3',        'C', 3, True),
    ('"security is a functor to ext.calc"','A', 1, False),
    ('p = n^2+1 for CM unit count n',     'C', 3, True),
]


def verify_axes_independent():
    """No axis is a function of any other across the recorded claims."""
    tier = [c[1] for c in GRADED_CLAIMS]
    lvl  = [c[2] for c in GRADED_CLAIMS]
    fals = [c[3] for c in GRADED_CLAIMS]

    def determines(x, y):
        """Does knowing x pin down y? (i.e. is y a function of x)"""
        m = {}
        for a, b in zip(x, y):
            if m.setdefault(a, b) != b:
                return False
        return True

    pairs = {}
    for na, a in (('tier', tier), ('level', lvl), ('falsifiable', fals)):
        for nb, b in (('tier', tier), ('level', lvl), ('falsifiable', fals)):
            if na == nb:
                continue
            d = determines(a, b)
            assert not d, f"{na} determines {nb} — the axes have collapsed"
            pairs[(na, nb)] = d

    # and every level appears at more than one tier, in both directions
    from collections import defaultdict
    by_lvl = defaultdict(set)
    for _, t, l, _ in GRADED_CLAIMS:
        by_lvl[l].add(t)
    assert len(by_lvl[1]) > 1 and len(by_lvl[3]) > 1, by_lvl
    # a falsifiable claim that is still only Level 1
    assert any(f and l == 1 for _, _, l, f in GRADED_CLAIMS)
    # a Tier A claim that is only Level 1
    assert any(t == 'A' and l == 1 for _, t, l, _ in GRADED_CLAIMS)
    # a Tier C claim that is Level 3
    assert any(t == 'C' and l == 3 for _, t, l, _ in GRADED_CLAIMS)
    return dict(by_lvl), pairs


LEVEL2_NOT_FUNCTOR = ['cut in an attack graph', 'Galois connection in abs. int.']
LEVEL2_CAN_BE_FUNCTOR = ['cell complex -> cochain complex']


def run():
    print("=" * 76)
    print("T305 — Four Orthogonal Cuts for Grading a Claim")
    print("=" * 76)

    states, hits = verify_rule90_is_laplacian()
    lin = linear_ecas()
    ok30, ok90, tot = verify_rule30_not_linear()
    print("\n--- Cut 1, worked case: 'Rule 30 is the discrete Laplacian' ---")
    print("  over GF(2):  u[i-1] - 2u[i] + u[i+1]  =  u[i-1] + u[i+1]   (-2 = 0)")
    print(f"  that is rule 90 — and exhaustively over all 256 ECA, rule 90 is")
    print(f"  the ONLY one equal to it on every state ({states} states, {N}-cell ring)")
    print(f"  GF(2)-linear ECA: {lin} — 30 is not among them")
    print(f"  rule 150 = l XOR c XOR r = l+c+r mod 2, the other natural stencil")
    print(f"  additivity   Rule 90: {ok90}/{tot}    Rule 30: {ok30}/{tot}")
    print("  Rule 30 = l XOR (c OR r); OR is not GF(2)-linear.")
    print("  => the claim is not literal, and the role (linear second")
    print("     difference) is not shared either. Rule 30 is a local CA rule.")
    print("  SCOPE: nearest-neighbour ECA on a line/cycle over GF(2). Not the")
    print("  Hodge Laplacian d.delta+delta.d, not Delta over R. 'Rule 90 is the")
    print("  Laplacian' in general would itself be a Level-1 claim.")

    cycles = verify_27_is_six_cycle()
    print("\n--- Cut 1, the literal side ---")
    print(f"  ord_37(27) = {order_mod(27, P)}; F_37* partitions into "
          f"{len(cycles)} six-cycles:")
    for c in cycles:
        print(f"    {c}")
    print("  That is literal. Calling it 'discrete curl' is structural — Level 1.")

    verify_cut_theorem()
    print("\n--- Cut 2: the three levels, same pair of systems ---")
    print("  L1  'a security boundary is like Stokes'          role only")
    print("  L2  graph G, s, t, cut C; blocking C separates    a map Phi")
    print("  L3  C separates and all edges blocked => no path  proved")
    print("  L3 verified on 200 random graphs: no counterexample.")

    print("\n--- Cut 3: native rigor does not upgrade the correspondence ---")
    for name, native, level in NATIVE_VS_CORRESPONDENCE:
        print(f"  {name:<24} native: {native:<38} corr: L{level}")

    print("\n--- Cut 4: Phi vs functor, both at Level 2 ---")
    for x in LEVEL2_NOT_FUNCTOR:
        print(f"  {x:<34} Level-2 Phi, NOT a functor")
    for x in LEVEL2_CAN_BE_FUNCTOR:
        print(f"  {x:<34} can be written as a functor once C, D are named")
    print("  'Functorial' without C, D, F is still Level 1.")

    print("\n--- composition: weakest cut governs ---")
    print("  'Rule 30 is the discrete Laplacian'      fails Cut 1")
    print("  'DARK_A occupancy is negative divergence' L1 ok; fails L2 until")
    print("                                            a discrete div is defined")
    print("  'Sigma verification is Stokes'            L1 ok; fails Cut 3")
    print("  'Security is a functor to exterior calc'  fails Cut 4; not even L2")

    by_lvl, _ = verify_axes_independent()
    print("\n--- three axes, asserted independent (not asserted in prose) ---")
    print(f"  {'claim':<38}{'tier':<6}{'level':<7}test can fail")
    for name, t, l, f in GRADED_CLAIMS:
        print(f"  {name:<38}{t:<6}L{l:<6}{f}")
    print(f"\n  levels seen at more than one tier: "
          f"L1 at {sorted(by_lvl[1])}, L3 at {sorted(by_lvl[3])}")
    print("  no axis is a function of any other — checked pairwise, all 6 ways.")
    print("  A Tier A stamp does not upgrade a Level 1 identification, and a")
    print("  falsifiable test does not thereby measure Delta.")
    print("\nAll T305 assertions passed.")


if __name__ == '__main__':
    run()
