# CLASS: THEOREM
"""
Theorem 314: 12 is the unique number closed under both readings of "n + 9"
Author: Michael Warren Song (CyclicAmp)

=== THE RESULT ===

    An expression like "9 + 12" admits two readings:

        READING A (reduce the operand)   9 + dr(n)
        READING B (take it literally)    9 + n

    Ask which n are returned or reversed by their own reading:

        A closes when  9 + dr(n) = n      -- solutions: 10..18   (9 of them)
        B closes when  n + 9 = rev(n)     -- solutions: the a-b=-1
                                             diagonal 12,23,...,89 (8 of them)

    The two sets intersect in exactly one number:

        {10,...,18} INTERSECT {12,23,34,45,56,67,78,89} = {12}

    12 is the unique n for which BOTH readings close:
        literal   12 + 9 = 21 = rev(12)
        reduced   9 + dr(12) = 9 + 3 = 12

=== MECHANISM -- both sides derived, neither counted ===

    A.  9 + dr(n) = n  <=>  n - dr(n) = 9.
        n - dr(n) = 9 * floor((n-1)/9) for every n, so the difference is
        9 exactly when floor((n-1)/9) = 1, i.e. 10 <= n <= 18.
        Nine solutions, and they are the nine consecutive integers of one
        digit-root block -- the block is the solution set.

    B.  n + 9 = rev(n) on two digits: n = 10a+b gives 9a + 9 = 9b, so
        b = a+1, the a-b = -1 diagonal. Eight solutions (T313).

    A is a statement about which BLOCK n sits in. B is a statement about
    which DIAGONAL its digits sit on. They are independent conditions --
    one modular, one positional -- which is why the intersection is small.
    12 is block 2 (10..18) and diagonal rung a=1. Both at once, once.

=== THE TWO READINGS CANNOT DISAGREE ON THE ROOT ===

    9 = 0 (mod 9), so both readings preserve dr(n):
        dr(9 + dr(n)) = dr(n) = dr(9 + n)     for every n.
    Zero exceptions, n = 1..2999. For n = 12 the two answers are 12 and 21
    -- different numbers, same root 3, and reverses of each other.

    This is the formal content of "which is 3 regardless": the ambiguity
    in how you read the operand is invisible mod 9. It is a theorem about
    the reading, not about the number.

=== WHY REDUCING EARLY IS LEGITIMATE ===

    dr is a homomorphism Z -> Z/9Z, so reduce-then-add equals
    add-then-reduce:
        12 + 12  reduced first  ->  3 + 3  = 6
        12 + 12  added first    ->  24     -> dr 6
    Zero exceptions over all 199 x 199 ordered pairs. The practice of
    collapsing a numeral to its digit sum mid-calculation is sound for
    + and x; it is NOT sound for - when the result is taken as a bare
    integer rather than a residue, nor for any predicate that depends on
    the numeral (primality, reversal, digit count). Recorded as the scope.

=== THE ZERO TALLY (protocol 12) ===

    0 -> 1, 00 -> 2, running total 3. The cumulative column is T_k:
    T_1 = 1, T_2 = 3. Three routes land on 3 here -- the token (1+2),
    both answers (dr 12 = dr 21 = 3), and the tally (1+2). The first two
    are the same fact twice (dr(12) = 3 either way); the third is
    unrelated arithmetic on a different sequence. Two routes, not three.

=== GF(37) ===

    3 (C3), 12 (SA_ST_A), 21 (SA_ST_B) are three of the four sovereign
    targets ST = {3,12,21,30}. All three appear in the six lines; 30 does
    not. Recorded as an observation. It is close to vacuous: ST is the
    DR=3 set below 37, and every quantity here has dr 3 by the forcing
    above, so any small DR=3 value had to land in ST. Not evidence.

=== FALSIFICATION ===
    Any assert below failing.

SCOPE (added after mutation audit, tools/mutation_audit.py): TIER A, and here
that IS a mislabel. This file has ZERO assertions referencing 37 or P. Every
claim in it -- 9 + dr(n) = n on the block {10..18}, n + 9 = rev(n) on the
a-b = -1 diagonal, and their intersection {12} -- is base-10 and mod-9
arithmetic. The only GF(37) content is placing 12 and 21 in ST, which the
section above already calls near-vacuous. The filename ends _gf37 and this is
not a GF(37) theorem. The mathematics is correct and stands; the claim the name
makes does not. Left in place rather than renamed, per this repo's rule that
corrections are recorded where the error was made.
"""

P = 37


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def tri(k):
    return k * (k + 1) // 2


def rev(n):
    return int(str(n)[::-1])


BLOCK = list(range(10, 19))
DIAG = [12, 23, 34, 45, 56, 67, 78, 89]


def run():
    # --- reading A closes on exactly 10..18 ---
    A = [n for n in range(1, 10000) if 9 + dr(n) == n]
    assert A == BLOCK
    assert len(A) == 9
    for n in range(1, 10000):
        assert n - dr(n) == 9 * ((n - 1) // 9)
        assert (9 + dr(n) == n) == (10 <= n <= 18)

    # --- reading B closes on exactly the a-b=-1 diagonal ---
    B = [n for n in range(10, 100) if n + 9 == rev(n)]
    assert B == DIAG
    assert len(B) == 8
    for n in range(10, 100):
        a, b = n // 10, n % 10
        assert (n + 9 == rev(n)) == (a - b == -1)

    # --- THE RESULT: they meet in exactly one place ---
    both = sorted(set(A) & set(B))
    assert both == [12]
    assert len(both) == 1
    assert 12 + 9 == 21 == rev(12)
    assert 9 + dr(12) == 12 and dr(12) == 3

    # 12 is block 2 and diagonal rung a=1 -- independent coordinates
    assert (12 - 1) // 9 == 1                 # block index
    assert 12 // 10 - 12 % 10 == -1           # diagonal index

    # --- neither reading can move the root ---
    assert not [n for n in range(1, 3000) if dr(9 + dr(n)) != dr(9 + n)]
    assert not [n for n in range(1, 3000) if dr(9 + n) != dr(n)]
    assert dr(12) == dr(21) == 3
    assert 9 % 9 == 0

    # --- dr is a homomorphism: reduce early is safe for + ---
    assert not [(a, b) for a in range(1, 200) for b in range(1, 200)
                if dr(a + b) != dr(dr(a) + dr(b))]
    assert not [(a, b) for a in range(1, 200) for b in range(1, 200)
                if dr(a * b) != dr(dr(a) * dr(b))]
    assert dr(3 + 3) == dr(12 + 12) == 6
    # and the recorded failure of scope: it is NOT safe for the numeral
    assert dr(13) == dr(4) and _isprime(13) and not _isprime(4)
    assert rev(12) != rev(dr(12))

    # --- the six lines, each as written ---
    assert 9 + dr(12) == 12                   # line 1  (starred)
    assert 9 + 1 + 1 == 11 and 11 + 1 == 12   # line 4
    assert 9 + 12 == 21                       # line 3
    assert 9 + 11 == 20 and 20 + 1 == 21      # line 5
    assert 9 + 1 == 10 and 10 + 11 == 21      # line 6
    assert 1 + 2 == 3                         # the token, 12 and 1.2 alike

    # --- zero tally ---
    assert tri(1) == 1 and tri(2) == 3

    # --- ST placement ---
    ST = {3, 12, 21, 30}
    assert {3, 12, 21} < ST and 30 not in {3, 12, 21}
    assert all(dr(t) == 3 for t in ST)        # near-vacuous, see docstring

    print("All assertions passed.\n")
    print("TWO READINGS OF  9 + n")
    print(f"  {'n':>4} {'9+dr(n)':>8} {'9+n':>5} {'rev(n)':>7} "
          f"{'A closes':>9} {'B closes':>9}")
    for n in range(10, 19):
        a_ok = (9 + dr(n) == n)
        b_ok = (n + 9 == rev(n))
        print(f"  {n:>4} {9 + dr(n):>8} {9 + n:>5} {rev(n):>7} "
              f"{str(a_ok):>9} {str(b_ok):>9}"
              f"{'   <-- BOTH' if a_ok and b_ok else ''}")
    print(f"\n  A = {A}   ({len(A)})   block 10..18, forced by n-dr(n)=9")
    print(f"  B = {B}   ({len(B)})   diagonal a-b=-1, forced by b=a+1")
    print(f"  A and B = {both}   ({len(both)})\n")

    print("12, BOTH WAYS")
    print(f"  literal   12 + 9 = {12 + 9} = rev(12) = {rev(12)}")
    print(f"  reduced   9 + dr(12) = 9 + {dr(12)} = {9 + dr(12)}")
    print(f"  the two answers are reverses, and share dr {dr(12)}.")
    print(f"  neither reading can move the root: 9 = 0 mod 9.\n")

    print("REDUCE-EARLY IS SOUND FOR + AND x")
    print(f"  12+12 reduced first 3+3 = {3 + 3}   added first 24 -> dr "
          f"{dr(24)}   same: {3 + 3 == dr(24)}")
    print(f"  0 exceptions over 199x199 pairs, for both + and x.")
    print(f"  NOT sound for numeral predicates: dr(13)=dr(4)={dr(13)} but")
    print(f"  13 is prime and 4 is not. that is the scope boundary.")


def _isprime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


if __name__ == "__main__":
    run()
