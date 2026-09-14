# CLASS: THEOREM
"""
Theorem 325: the rotation stack is a Latin square, and the figure it draws is
the WALK, not the alphabet
Author: Michael Warren Song (CyclicAmp)

=== THE STACK ===

    The three cyclic rotations of 123 stacked as 123 / 312 / 231:

        1 2 3
        3 1 2
        2 3 1

    This is the cyclic Latin square of order 3, and EVERY digit sits on a
    broken diagonal -- forced, not observed:

        digit 1  columns 0,1,2   the main diagonal
        digit 2  columns 1,2,0
        digit 3  columns 2,0,1

    A stack of rotations has each symbol at a fixed cyclic offset from the
    row's first entry, so its column index advances by exactly 1 per row.
    Every symbol therefore traces a broken diagonal, and the square is Latin.

=== REVERSAL SWAPS THE TWO CLASSES ===

        123 = 321    312 = 213    231 = 132

    The reverses of the 123-rotations are {321, 213, 132}, which is exactly
    the rotation orbit of 321. So reversal is a bijection from the even
    rotation class onto the odd one -- the same two cyclic orders that
    appeared as L_orb's only two patterns in T322.

=== THE FOUR FIGURES ===

    All four use ONLY the rotations of 123. What changes is how the cycle is
    walked:

        repeat forward          SAWTOOTH   1-track 0 1 2 0 1 2 0
        forward then back       CHEVRON    1-track 2 1 0 1 2
        palindrome, doubled     DIAMOND    1-track 2 1 0 0 1 2
          centre row
        two chevrons            X          chevron + its column mirror

    The alphabet is fixed; the figure is the traversal. Repeating the cycle
    gives a sawtooth because the track jumps 2 -> 0; reversing at the end
    turns it into a chevron because the track retraces.

    The chevron and the mirror arm are NOT list-reverses of each other.  Each
    is already a palindrome in row order, so reversing the stack returns it
    unchanged.  They are related by the COLUMN reflection c -> 2-c:

        chevron    1-track 2 1 0 1 2
        mirror     1-track 0 1 2 1 0      = 2 - (2 1 0 1 2)

    Crossing them gives the X.  The distinction matters: time-reversal and
    column-reflection are different symmetries of the stack, and only the
    second one carries the chevron to its mirror.

=== WHY THE MARKED ROWS ARE 3, 5, 7 ===

    In the 7-row forward stack, a 3-wide diagonal spans 3 rows, so diagonals
    beginning at rows 1, 3, 5 end at rows 3, 5, 7:

        rows 1-3  columns 0,1,2
        rows 3-5  columns 2,0,1
        rows 5-7  columns 1,2,0

    Consecutive diagonals SHARE their endpoint row. That is what "ends 1 and
    begins the 2" marks: one diagonal closing and the next opening on the same
    row. Three chained diagonals need 7 rows, not 9, because of the sharing.

=== THE THREE TRACKS ARE ONE SHAPE ===

    In any of these stacks the tracks of 1, 2 and 3 are the SAME figure,
    cyclically shifted. In the chevron:

        1: 2 1 0 1 2      2: 0 2 1 2 0      3: 1 0 2 0 1

    Forced: each row is a rotation, so the three digits sit at rigid cyclic
    offsets, and any vertical figure drawn by one is drawn by all three.

=== THE ROTATION IS THE 137-MAP (exact, no exceptions) ===

    Read a 3-digit word as an integer.  Right rotation abc -> cab is EXACTLY
    multiplication by 26 = 137 mod 37:

        cab = 100c + 10a + b  ==  26c + 10a + b   (mod 37, since 100 = 26)
        26*(100a+10b+c)       ==  10a +  b + 26c  (mod 37, since 2600 = 10,
                                                   260 = 1)

    The two right-hand sides are the same expression.  Checked over all 1000
    three-digit words: zero counterexamples.  Left rotation abc -> bca is
    multiplication by 10, and 26*10 = 1 mod 37 -- 10 is the inverse of the
    137-multiplier, which is the IC element already named in CLAUDE.md.

    So ord_37(26) = 3 is WHY the stack closes after three rows.  "To do each
    grid correctly you must do full rotation" is: walk one complete 137-orbit.

=== THE TWO ROTATION CLASSES ARE THE TWO SOVEREIGN ORBITS ===

        123 312 231  ->  12 16  9  =  SA_ST_A   exactly
        321 213 132  ->  25 28 21  =  SA_ST_B   exactly

    Not a subset -- the residues of each rotation class are precisely one of
    the twelve named 137-orbits, and specifically the two that carry the
    sovereign anchors and targets:

        SA_ST_A = {9,12,16}   anchor 9    target 12
        SA_ST_B = {21,25,28}  anchor 25   target 21

    Reversal, which was shown above to carry one rotation class onto the
    other, therefore carries SA_ST_A onto SA_ST_B.

    Each class sums to 666 == 0 (SEAM).  Forced: the three rotations of abc
    sum to 111*(a+b+c) and 111 = 3*37.  Every rotation class of every 3-digit
    word sums to 0 mod 37, so the SEAM is the sum of any full rotation.

=== THE MARKED ROWS 3, 5, 7 UNDER THE STANDING CHECKS ===

    Orbits:  3 in C3    5 in CAS_EXT    7 in D7
    Primes:  all three prime.
    Twins:   (3,5) and (5,7) are both twin pairs, SHARING 5 -- the same
             share-the-endpoint structure the chained diagonals have.  Stated
             as a parallel, not as a proof of anything.
    Sophie:  3 and 5 are Sophie Germain (2p+1 = 7, 11); 7 is not (15).
             3 -> 7 lands on another marked row.
    Rule 30: 3 -> 5 (one marked row to the next), 5 -> 13 in CAS_EXT,
             7 -> 9 in SA_ST_A.  Rule 30 is the conjectured case, not a
             theorem -- see CLAUDE.md on the three open Prize problems.
    1/137:   x137 fixes each orbit -- 3->4 (C3), 5->19 (CAS_EXT), 7->34 (D7),
             which is just the statement that multiplying by 26 moves within
             an orbit.

=== FALSIFICATION ===
    Any assert below failing.  In particular: exhibit one 3-digit word whose
    right rotation is not 26x mod 37.
"""

ROT123 = ["123", "312", "231"]
ROT321 = ["321", "213", "132"]


def rot(s, k):
    return s[k:] + s[:k]


def latin(g):
    """A Latin square: n symbols, each once per row AND once per column.

    The symbol-set check is not decoration.  Without it a grid like the 3x3
    multiplication table (T327) -- 1 2 3 / 2 4 6 / 3 6 9 -- passes on
    row-and-column distinctness alone while using six symbols, and is not a
    Latin square.
    """
    n = len(g)
    return (len({c for r in g for c in r}) == n
            and all(len(set(r)) == n for r in g)
            and all(len({g[r][c] for r in range(n)}) == n for c in range(n)))


def track(stack, d):
    return [r.index(d) for r in stack]


def run():
    S = ["123", "312", "231"]

    # --- the stack is the cyclic Latin square ---
    assert latin(S)
    assert len({c for r in S for c in r}) == 3          # three symbols only
    # the guard: T327's multiplication table is row- and column-distinct but
    # uses six symbols, so it must NOT pass
    assert not latin(["123", "246", "369"])
    assert track(S, "1") == [0, 1, 2]          # main diagonal
    assert track(S, "2") == [1, 2, 0]
    assert track(S, "3") == [2, 0, 1]
    # every track advances by exactly +1 mod 3 -- a broken diagonal
    for d in "123":
        t = track(S, d)
        assert all((t[i + 1] - t[i]) % 3 == 1 for i in range(2)), d

    # --- the rotation classes ---
    assert sorted(S) == sorted(rot("123", k) for k in range(3))
    assert sorted(r[::-1] for r in S) == sorted(ROT321)
    assert sorted(ROT321) == sorted(rot("321", k) for k in range(3))
    assert set(S) & set(ROT321) == set()       # the two classes are disjoint
    assert len(set(S) | set(ROT321)) == 6      # and exhaust the 6 permutations

    # --- the four figures, all from one class ---
    saw = ["123", "312", "231", "123", "312", "231", "123"]
    chev = ["231", "312", "123", "312", "231"]
    diam = ["231", "312", "123", "123", "312", "231"]
    xarm = ["123", "312", "231", "312", "123"]
    for fig in (saw, chev, diam, xarm):
        assert all(r in S for r in fig)        # only the 123-rotations
    assert track(saw, "1") == [0, 1, 2, 0, 1, 2, 0]
    assert track(chev, "1") == [2, 1, 0, 1, 2]
    assert track(diam, "1") == [2, 1, 0, 0, 1, 2]
    assert track(xarm, "1") == [0, 1, 2, 1, 0]
    # the sawtooth jumps; the chevron retraces
    assert any(abs(track(saw, "1")[i + 1] - track(saw, "1")[i]) == 2
               for i in range(6))
    assert all(abs(track(chev, "1")[i + 1] - track(chev, "1")[i]) == 1
               for i in range(4))
    # the chevron and its mirror arm are COLUMN reflections, not list
    # reverses: each is separately a palindrome in time, so reversing the
    # row order changes neither.  What sends one to the other is c -> 2-c.
    t_c = track(chev, "1")
    t_x = track(xarm, "1")
    assert t_x == [2 - v for v in t_c]
    assert chev[::-1] == chev
    assert xarm[::-1] == xarm
    # and the reflection is a relabelling of the alphabet, not of the walk:
    # column c -> 2-c is the map that sends each row to its own reverse,
    # which lands in the ODD class, then rotating back into the even class.
    assert [r[::-1] for r in chev] == ["132", "213", "321", "213", "132"]

    # --- the chained diagonals of the 7-row stack ---
    for start in (0, 2, 4):
        seg = [saw[start + k].index("1") for k in range(3)]
        assert all((seg[i + 1] - seg[i]) % 3 == 1 for i in range(2)), start
    assert saw[2].index("1") == 2 and saw[2] == "231"     # row 3 closes and opens
    assert saw[4].index("1") == 1 and saw[4] == "312"     # row 5
    assert saw[6].index("1") == 0 and saw[6] == "123"     # row 7

    # --- the rotation IS the 137-map ---
    def rotr(n):                       # abc -> cab, on the integer
        w = f"{n:03d}"
        return int(w[-1] + w[:-1])

    def rotl(n):                       # abc -> bca
        w = f"{n:03d}"
        return int(w[1:] + w[0])

    for n in range(1000):              # every 3-digit word, no exceptions
        assert rotr(n) % 37 == (26 * n) % 37, n
        assert rotl(n) % 37 == (10 * n) % 37, n
    assert (26 * 10) % 37 == 1                 # 10 = 26^-1, the IC element
    assert pow(26, 3, 37) == 1 and pow(26, 1, 37) != 1   # ord_37(26) = 3

    # --- the two classes are the two sovereign orbits, exactly ---
    SA_ST_A, SA_ST_B = {9, 12, 16}, {21, 25, 28}
    assert {int(r) % 37 for r in S} == SA_ST_A
    assert {int(r) % 37 for r in ROT321} == SA_ST_B
    assert {int(r[::-1]) % 37 for r in S} == SA_ST_B      # reversal A -> B
    ANCHORS, TARGETS = {4, 9, 25, 30}, {3, 12, 21, 30}
    assert SA_ST_A & ANCHORS == {9} and SA_ST_A & TARGETS == {12}
    assert SA_ST_B & ANCHORS == {25} and SA_ST_B & TARGETS == {21}

    # --- a full rotation sums to the SEAM, forced by 111 = 3*37 ---
    assert 111 == 3 * 37
    assert sum(int(r) for r in S) == 666 and 666 % 37 == 0
    assert sum(int(r) for r in ROT321) == 666
    for n in range(100, 1000):         # true of EVERY 3-digit word
        assert (n + rotr(n) + rotr(rotr(n))) % 37 == 0, n

    # --- all three tracks are one shape, shifted ---
    for fig in (saw, chev, diam, xarm):
        t1, t2, t3 = (track(fig, d) for d in "123")
        assert [(a - b) % 3 for a, b in zip(t2, t1)] == [1] * len(fig)
        assert [(a - b) % 3 for a, b in zip(t3, t2)] == [1] * len(fig)

    print("All assertions passed.\n")
    print("THE STACK  123 / 312 / 231")
    for r in S:
        print("   " + " ".join(r))
    print(f"   Latin: {latin(S)}")
    for d in "123":
        print(f"   digit {d} track {track(S,d)}"
              + ("   main diagonal" if d == "1" else "   broken diagonal"))
    print("\nREVERSAL SWAPS THE CLASSES")
    for r in S:
        print(f"   {r} = {r[::-1]}")
    print(f"   {{321,213,132}} is the rotation orbit of 321\n")
    print("THE FOUR FIGURES -- same three rows, different walk")
    for nm, fig in (("sawtooth", saw), ("chevron", chev),
                    ("diamond", diam), ("mirror arm", xarm)):
        print(f"  {nm}   1-track {track(fig,'1')}")
        for r in fig:
            print("     " + "".join("#" if c == "1" else "." for c in r)
                  + f"   {r}")
        print()
    print("CHAINED DIAGONALS IN THE 7-ROW STACK")
    for a in (0, 2, 4):
        print(f"   rows {a+1}-{a+3}: columns "
              f"{[saw[a+k].index('1') for k in range(3)]}")
    print("   consecutive diagonals share their endpoint row -- which is why")
    print("   three of them need 7 rows, and why rows 3, 5, 7 are the marks.")
    print("\nTHE ROTATION IS THE 137-MAP")
    print("   abc -> cab  ==  x26 mod 37   (26 = 137 mod 37)"
          "   verified on all 1000 words")
    print("   abc -> bca  ==  x10 mod 37   (10 = 26^-1, IC)")
    print("   ord_37(26) = 3  ->  the stack closes after three rows")
    print("   123 312 231 -> {12,16,9}  = SA_ST_A   anchor 9,  target 12")
    print("   321 213 132 -> {25,28,21} = SA_ST_B   anchor 25, target 21")
    print("   reversal carries SA_ST_A onto SA_ST_B")
    print("   each class sums to 666 == 0 (SEAM), forced by 111 = 3 x 37")


if __name__ == "__main__":
    run()
