# CLASS: THEOREM
"""
Theorem 429: the 3x3 digit grid is the transversality of two triple-partitions
of {1..9}, the six permutations of a digit triple hit two complete GF(37)
orbits because {100,10,1} = H, and four triples break that rule

Supplied as a reversal-block observation:

    block 1   187 781 718 817 871 178      all permutations of {1,7,8}
    middle    178 246 359
    block 2   123 321 547 745 869 968      three reversal pairs

  and the reconstruction that the middle numbers are the ROWS and block 2
  the COLUMNS of

        1 7 8          rows     178, 246, 359
        2 4 6          columns  123, 745, 869   (745 = reverse of 547)
        3 5 9

  Both halves verified below. What follows separates what the grid IS from
  what is merely true of it.

PRIOR ART.  cipher_123_1234.py has 1234 mod 37 and the Z/9Z trinity/doubling
partition; T382 (coset_step_alignment) and T386 (penrose_tiktok) use the
cyclic-rotation coset fact. The transversality characterisation and the
84-triple census below are not in the corpus.

================================================================================
1. WHAT THE GRID IS -- TRANSVERSALITY, AND NOTHING MORE
================================================================================

  The two digit-partitions in play are

      A = {1,7,8} {2,4,6} {3,5,9}       the middle triple's digit sets
      B = {1,2,3} {4,5,7} {6,8,9}       block 2's digit sets

  and every block of A meets every block of B in exactly ONE digit.  That
  property -- transversality -- is precisely the condition for two partitions
  of a 9-set into triples to be the rows and columns of a 3x3 array.  So the
  grid is not an additional object: it IS the statement that A and B are
  transversal, rewritten as a picture.  Asking what the grid is, is asking
  what those two partitions are to each other, and the answer is this.

  IT IS SELECTIVE, so the miss-test passes.  Of the 280 partitions of {1..9}
  into three unordered triples, exactly 36 are transversal to A -- 12.9%.
  A property satisfied by one partition in eight is a real constraint, not
  a tautology.  (36 = 6 x 3! : choose the bijection row->column position
  freely, then the 3! orderings, which is the count of ways to read columns
  off a fixed grid.)

  IT IS NOT A MAGIC SQUARE and not a Latin square.  Row sums 16, 12, 17;
  column sums 6, 16, 23; diagonals 14 and 15.  Nothing is equal to anything.

================================================================================
2. FORCED -- THE SIX PERMUTATIONS ALWAYS HIT TWO COMPLETE ORBITS
================================================================================

  Block 1's six residues are

      187->2   718->15  871->20     DARK_A = {2,15,20}
      178->30  781->4   817->3      C3     = {3,4,30}

  two orbits, complete, each hit exactly once per element.  This looks like
  a find about {1,7,8}.  It is not.

      100a + 10b + c  =  26a + 10b + c   (mod 37)

  and {26, 10, 1} is H = IC itself.  Cyclic rotation of the digits is
  multiplication by 10, and ord_37(10) = 3, so the six permutations split
  into two cyclic classes of three, each of the form {v, 10v, 26v} = v*H.
  An H-coset is exactly one of the twelve named orbits.  So "two complete
  orbits" is FORCED for a digit triple; only WHICH two is contingent.

  FOUR EXCEPTIONS, and they are exactly the seam.  A class collapses when
  v = 0, i.e. when some permutation is divisible by 37:

      {1,4,8}  -> NEG_H + SEAM       {1,5,8}  -> IC + SEAM
      {2,5,9}  -> NEG_H + SEAM       {2,6,9}  -> IC + SEAM

  80 of the 84 triples give two complete orbits; these four give one orbit
  and the seam.  185 = 5 x 37 is the witness for {1,5,8}.

  This is recorded as a correction to a first pass of this same file, which
  asserted the rule for all 84 and was wrong on four.

================================================================================
3. GF(37), SEPARATING THE EXACT HIT FROM THE CLASSIFICATION
================================================================================

      row  178 -> 30  C3        col  123 -> 12  SA_ST_A
      row  246 -> 24  SEED      col  745 ->  5  CAS_EXT
      row  359 -> 26  IC        col  869 -> 18  SEED

  Two of these are exact numeric identities and worth naming:

      246 IS the pipeline's reference seed (CLAUDE.md, seed mod 37 = 24)
      359 = 26 (mod 37), and 26 = 137 mod 37 is the 137-map multiplier

  Everything else in that table is classification, and classification is
  nearly free: every residue lies in some orbit, so "the row lands in SEED"
  carries at most log2(12) = 3.6 bits and three rows landing in three named
  orbits is guaranteed.  The content here is the integer 246, not its orbit.

  FALSIFICATION.  Any of: A and B failing transversality; a transversal
  count other than 36 of 280; a digit triple outside the four listed whose
  permutations fail to cover two complete orbits; or 246 mod 37 != 24.
"""

import sys
from itertools import combinations

P = 37
ORBITS = {
    "IC": {1, 10, 26}, "DARK_A": {2, 15, 20}, "C3": {3, 4, 30},
    "CAS_EXT": {5, 13, 19}, "TESLA": {6, 8, 23}, "D7": {7, 33, 34},
    "SA_ST_A": {9, 12, 16}, "NEG_H": {11, 27, 36}, "C9": {14, 29, 31},
    "NQR17": {17, 22, 35}, "SEED": {18, 24, 32}, "SA_ST_B": {21, 25, 28},
}


def orbit_of(x):
    r = x % P
    return "SEAM" if r == 0 else next(k for k, v in ORBITS.items() if r in v)


def perms3(t):
    return [100 * a + 10 * b + c for a in t for b in t for c in t
            if len({a, b, c}) == 3]


def triple_partitions():
    out = []

    def rec(rem, cur):
        if not rem:
            out.append(tuple(cur))
            return
        m = min(rem)
        for pair in combinations(sorted(rem - {m}), 2):
            block = {m} | set(pair)
            rec(rem - block, cur + [block])
    rec(set(range(1, 10)), [])
    return out


def main():
    G = [[1, 7, 8], [2, 4, 6], [3, 5, 9]]
    print("=" * 78)
    print("THEOREM 429: TRANSVERSAL TRIPLE-PARTITIONS AND THE DIGIT GRID")
    print("=" * 78)

    print("\nPart 1: the reconstruction is correct")
    rows = [int("".join(map(str, r))) for r in G]
    cols = [int("".join(str(G[i][j]) for i in range(3))) for j in range(3)]
    print("   rows    %s" % rows)
    print("   columns %s   (745 is the reverse of block 2's 547)" % cols)
    assert rows == [178, 246, 359]
    assert cols == [123, 745, 869]
    assert sorted(d for r in G for d in r) == list(range(1, 10))
    rs = [sum(r) for r in G]
    cs = [sum(G[i][j] for i in range(3)) for j in range(3)]
    print("   row sums %s, col sums %s, diagonals %d and %d -> not magic"
          % (rs, cs, G[0][0] + G[1][1] + G[2][2], G[0][2] + G[1][1] + G[2][0]))
    assert len(set(rs + cs)) > 1

    print("\nPart 2: the grid IS the transversality of two partitions")
    A = [{1, 7, 8}, {2, 4, 6}, {3, 5, 9}]
    B = [{1, 2, 3}, {4, 5, 7}, {6, 8, 9}]
    assert all(len(x & y) == 1 for x in A for y in B)
    print("   every block of A meets every block of B in exactly one digit ✓")
    PS = triple_partitions()
    tr = [q for q in PS if all(len(x & y) == 1 for x in A for y in q)]
    print("   partitions of {1..9} into 3 triples: %d" % len(PS))
    print("   transversal to A: %d  (%.1f%%)" % (len(tr), 100 * len(tr) / len(PS)))
    assert len(PS) == 280 and len(tr) == 36
    assert B in [list(q) for q in tr] or any(
        sorted(map(sorted, q)) == sorted(map(sorted, B)) for q in tr)
    print("   B is among them ✓ -- selective at 1 in 8, so the miss-test passes")

    print("\nPart 3: two complete orbits is FORCED, with four exceptions")
    print("   100a+10b+c = 26a+10b+c (mod 37), and {26,10,1} = H = IC.")
    print("   rotation is x -> 10x, ord_37(10) = 3, so the six permutations")
    print("   are two cyclic classes {v,10v,26v} = v*H, i.e. two orbits.")
    assert {100 % P, 10 % P, 1} == ORBITS["IC"]
    assert pow(10, 3, P) == 1
    bad = []
    for t in combinations(range(1, 10), 3):
        pr = perms3(t)
        os = sorted({orbit_of(n) for n in pr})
        ok = len(os) == 2 and all(
            len({n % P for n in pr if orbit_of(n) == o}) == 3 for o in os)
        if not ok:
            bad.append((t, os))
    print("   triples with two COMPLETE orbits: %d of 84" % (84 - len(bad)))
    for t, os in bad:
        print("      exception %s -> %s" % (list(t), os))
    assert len(bad) == 4
    assert [t for t, _ in bad] == [(1, 4, 8), (1, 5, 8), (2, 5, 9), (2, 6, 9)]
    assert 185 % P == 0 and 185 == 5 * 37
    print("   the exceptions are exactly the seam cases (185 = 5 x 37) ✓")
    b1 = perms3((1, 7, 8))
    assert sorted(b1) == sorted([187, 781, 718, 817, 871, 178])
    assert {n % P for n in b1} == ORBITS["DARK_A"] | ORBITS["C3"]
    print("   block 1 = all six permutations of {1,7,8} -> DARK_A + C3 ✓")

    print("\nPart 4: the exact hits, kept apart from the classification")
    for n in rows + cols:
        print("   %-4d mod 37 = %-3d %s" % (n, n % P, orbit_of(n)))
    assert 246 % P == 24 and orbit_of(246) == "SEED"
    assert 359 % P == 26 and 137 % P == 26
    print("   246 IS the pipeline reference seed; 359 = 26 = 137 mod 37.")
    print("   the orbit labels are near-free (every residue has one); the")
    print("   content is the integer 246, not its classification.")

    print("\n" + "=" * 78)
    print("ALL ASSERTIONS PASS")
    print("=" * 78)


if __name__ == "__main__":
    sys.exit(main())
