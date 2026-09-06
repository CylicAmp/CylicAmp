"""
T303 — The Decimal-Block Map Is Multiplication by 27, and Its Cycles Are the
        Antipodal Pairs

Found by feeding decimal blocks back into gf37-audit as inputs: 1 -> 27 ->
729 -> 702 -> 972 -> 270 -> 297 -> 1. That path closes, and the reason is
exact.

════════════════════════════════════════════════════════════════════════════
block(k) = 27k, EXACTLY
════════════════════════════════════════════════════════════════════════════
    1/37 = 27/999,  so  k/37 = 27k/999.

The repeating 3-digit block of k/37 is therefore the integer 27k, and since
27 x 36 = 972 < 1000 there is no wraparound for any k in 1..36. Verified for
all 36 residues, zero counterexamples.

    block(1)=027   block(10)=270   block(26)=702
    block(11)=297  block(27)=729   block(36)=972

Consequence: feeding a block back as input is multiplication by 27 mod 37.

    B(k) = 27k  (mod 37)

════════════════════════════════════════════════════════════════════════════
27 = -10, SO B IS NEGATION COMPOSED WITH THE DECIMAL SHIFT
════════════════════════════════════════════════════════════════════════════
    -10 mod 37 = 27.

T302 established that x10 is the decimal shift with ord_37(10) = 3, and T283
that x(-1) is the antipodal map with order 2. B is their composite:

    B = (x -1) o (x 10),   ord_37(27) = lcm(3, 2) = 6.

Both factors already had names in GF(37). B is the first object that
needs both.

════════════════════════════════════════════════════════════════════════════
<27> IS THE OPERATOR GROUP, AGAIN
════════════════════════════════════════════════════════════════════════════
    <27> = {1, 10, 11, 26, 27, 36} = <11> = IC u NEG_H

which is, from earlier theorems, all of the following:
    the operator group                      (T284)
    the sixth powers of F_37*               (T299)
    the reduction of the units of Z[omega]  (T299)
    the order-6 rotation subgroup H_2       (T296)

and now also: the orbit of 1 under the decimal-block map.

════════════════════════════════════════════════════════════════════════════
THE SIX CYCLES ARE THE SIX ANTIPODAL PAIRS
════════════════════════════════════════════════════════════════════════════
B partitions F_37* into 6 cycles of length 6. Each cycle is exactly one
antipodal pair of orbits, and it alternates between them:

    [ 1, 27, 26, 36, 10, 11]   IC / NEG_H
    [ 2, 17, 15, 35, 20, 22]   DARK_A / NQR17
    [ 3,  7,  4, 34, 30, 33]   C3 / D7
    [ 5, 24, 19, 32, 13, 18]   CAS_EXT / SEED
    [ 6, 14,  8, 31, 23, 29]   TESLA / C9
    [ 9, 21, 12, 28, 16, 25]   SA_ST_A / SA_ST_B

The alternation is forced: 27 is in NEG_H and 27^2 = 26 is in IC, so odd
powers land in NEG_H and even powers in IC.

These cycles are simultaneously:
    the cosets of <11> in F_37*                     (T284)
    the 6 antipodal orbit pairs                     (T283)
    the 6 isomorphism classes of y^2 = x^3 + a      (T288)
    the 3 quadratic twist pairs, doubled            (T289)
Verified equal to the coset list by direct comparison.

════════════════════════════════════════════════════════════════════════════
WHAT IS AND IS NOT FORCED
════════════════════════════════════════════════════════════════════════════
block(k) = 27k is a genuine computation about base 10 and the value 37 —
it is where the content is. Everything after it is forced: once B = x27 is
known, ord_37(27) = 6, <27> = <11>, and the cycles being cosets all follow
from group theory with no further input.

The general form is B_p = x((10^d - 1)/p) where d = ord_p(10). Nothing here
claims what that multiplier equals for other p; at p = 7 it is 142857, which
reduces to 1 mod 7, making the map trivial there. The p = 37 case is not
asserted to be typical.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..',
                                '.claude', 'skills'))
import gf37 as G

P = G.P
B_MULT = 27          # = 999/37 = (10^3 - 1)/37


def block_int(k):
    """The 3-digit repeating block of k/37, as an integer."""
    return (k % P) * 1000 // P % 1000


# ─── Part 1: block(k) = 27k exactly ─────────────────────────────────────────

def verify_block_is_27k():
    assert 999 // P == 27 and 999 == 27 * P
    for k in range(1, P):
        assert block_int(k) == 27 * k, f"k={k}: {block_int(k)} != {27*k}"
    assert 27 * 36 == 972 < 1000          # no wraparound
    assert G.block(1) == '027' and G.block(36) == '972'
    return True


# ─── Part 2: 27 = -10, B = negation o shift ─────────────────────────────────

def verify_composite():
    assert (-10) % P == 27
    assert G.order_mod(10, P) == 3        # decimal shift, T302
    assert G.order_mod(P - 1, P) == 2     # negation, T283
    assert G.order_mod(27, P) == 6        # lcm(3,2)
    for k in range(1, P):
        assert (27 * k) % P == (-(10 * k)) % P
    return True


# ─── Part 3: <27> is the operator group ─────────────────────────────────────

def verify_operator_group():
    g27 = {pow(27, i, P) for i in range(6)}
    g11 = {pow(11, i, P) for i in range(6)}
    sixth = {pow(x, 6, P) for x in range(1, P)}
    assert g27 == g11 == sixth == G.ORBITS['IC'] | G.ORBITS['NEG_H']
    assert sorted(g27) == [1, 10, 11, 26, 27, 36]
    return sorted(g27)


# ─── Part 4: the six cycles are the six antipodal pairs ────────────────────

def block_cycles():
    seen, cycles = set(), []
    for s in range(1, P):
        if s in seen:
            continue
        c, x = [s], (B_MULT * s) % P
        while x != s:
            c.append(x)
            x = (B_MULT * x) % P
        seen |= set(c)
        cycles.append(c)
    return cycles


def verify_cycles():
    cycles = block_cycles()
    assert len(cycles) == 6 and all(len(c) == 6 for c in cycles)

    # each cycle is exactly one antipodal pair, alternating
    for c in cycles:
        orbs = [G.orbit(v) for v in c]
        a, b = orbs[0], orbs[1]
        assert G.antipode(a) == b, f"{a} / {b} not antipodal"
        assert orbs == [a, b] * 3, f"not alternating: {orbs}"

    # cycles == cosets of <11>
    og = {1, 10, 11, 26, 27, 36}
    cos, cov = [], set()
    for a in range(1, P):
        if a in cov:
            continue
        s = sorted({(a * g) % P for g in og})
        cos.append(s)
        cov |= set(s)
    assert sorted(map(sorted, cycles)) == sorted(cos)
    return cycles


# ─── Part 5: the audit chain that found it ──────────────────────────────────

def verify_found_chain():
    """1 -> 27 -> 729 -> 702 -> 972 -> 270 -> 297 -> 1"""
    chain, n = [], 1
    for _ in range(7):
        chain.append(n)
        n = block_int(n)
    assert chain == [1, 27, 729, 702, 972, 270, 297]
    assert block_int(297) == 27          # closes
    residues = sorted({v % P for v in chain})
    assert residues == [1, 10, 11, 26, 27, 36]
    return chain


def run():
    print("=" * 76)
    print("T303 — The Decimal-Block Map Is x27; Its Cycles Are the Antipodal Pairs")
    print("=" * 76)

    verify_block_is_27k()
    print("\n--- Part 1: block(k) = 27k, exactly ---")
    print(f"  1/37 = 27/999, so k/37 = 27k/999 and block(k) = 27k")
    print(f"  27 x 36 = {27*36} < 1000, so no wraparound. Checked all 36 k.")
    for k in (1, 10, 11, 26, 27, 36):
        print(f"    block({k:>2}) = {G.block(k)} = 27 x {k}")

    verify_composite()
    print("\n--- Part 2: 27 = -10, so B = negation o decimal shift ---")
    print(f"  -10 mod 37 = {(-10)%P}")
    print(f"  ord(10) = {G.order_mod(10,P)} (shift, T302);  "
          f"ord(-1) = {G.order_mod(P-1,P)} (antipodal, T283)")
    print(f"  ord(27) = {G.order_mod(27,P)} = lcm(3,2)")
    print("  B is the first GF(37) object requiring both factors.")

    g = verify_operator_group()
    print("\n--- Part 3: <27> is the operator group, again ---")
    print(f"  <27> = {g}")
    print("  = <11> (T284) = the sixth powers (T299) = reduced Z[omega]* (T299)")
    print("  = the order-6 rotation subgroup H_2 (T296)")
    print("  and now also the orbit of 1 under the block map.")

    cycles = verify_cycles()
    print("\n--- Part 4: six cycles = six antipodal pairs ---")
    for c in cycles:
        a, b = G.orbit(c[0]), G.orbit(c[1])
        print(f"  {str(c):<26} {a} / {b}")
    print("  Each cycle alternates a pair, forced by 27 in NEG_H and 27^2 in IC.")
    print("  Verified identical to the cosets of <11> — hence also the 6 j=0")
    print("  isomorphism classes (T288) and the 3 twist pairs doubled (T289).")

    chain = verify_found_chain()
    print("\n--- Part 5: the chain that found it ---")
    print(f"  {' -> '.join(map(str, chain))} -> 27  (closed)")
    print(f"  residues {sorted({v%P for v in chain})} = <11>")

    print("\n--- forced vs found ---")
    print("  block(k) = 27k is the content: a fact about base 10 and 37.")
    print("  Everything after is forced by group theory once B = x27 is known.")
    print("  General form B_p = x((10^d-1)/p), d = ord_p(10). At p=7 that")
    print("  multiplier is 142857 = 1 mod 7, so the map is trivial there.")
    print("  No claim that p=37 is typical.")

    print("\nAll T303 assertions passed.")


if __name__ == '__main__':
    run()
