# CLASS: COMPUTATION
"""
The owner's lines of #410 (2026-10-22): the 12 + 9 chain, 75.7%, "why not 2=2×2=4", the three
things (past, current, future), the bracket lines, the = key symbols, and the 1,2,3 substrate.
Process entry: owner_work/PROCESS.md, #410. The pasted blocks of the same message are audited in
pasted_signs_percent_equals_markov_audit_2026_10_22.py (and the repeated 1.137 paste in
pasted_1137_squared_running_sum_audit_2026_10_22.py).

THE OWNER'S LINES, verbatim (#410):
    so in other words 0.0
    12+9=21+2=23+7=30+6=36+9=4+5=9

    hmm

    75.7%×(−075.7%×(−1

    See if = means identical value why they not go 2=2×2=4

    I always do 3 things remember whats connected to whatever is current while predicting the
    future ..Than 1 action per registered action i can can than verify as i rinse and repeat...

    11,1)11,1)11-1)11,1)
    1,11(1,11(1,11(1,11(
    12(13(12(13(12
    1,2(1,2 (1,2 (1,2(
    1,3)1,3))1,3))1,3))

    12(13(12(13(12
    13)12)13)12)13

    11-
    22=
    33=
    33≈
    66≠
    66≡
    33≈
    33≠

    Okay, i'm just playing around with these things that are with the equal button, when you press
    it and hold it down on the keypad, which I have no idea what these things mean

    1,2,3,1,2 ,3,1,2,3,1,2,3

    creating a lineage of generations so even when not part of and individual or current actions a
    substrate of its

1. THE CHAIN
    cleaned: 12 + 9 = 21 -> 21 + 2 = 23 -> 23 + 7 = 30 -> 30 + 6 = 36 -> 36 + 9 = 45 -> 4 + 5 = 9
    right: every step.

2. 75.7%
    cleaned: 75.7% x (-75.7% x (-1)) -- the 0 in front of 075.7 changes nothing; the two closing
    brackets are added.
    -75.7% x (-1) = 75.7%  ->  75.7% x 75.7% = 0.757 x 0.757 = 0.573049 = 57.3049%
    right: 757 x 757 = 573049. 757 is prime; roots 7+5+7 = 19 -> 1 and 5+7+3+0+4+9 = 28 -> 1, 1 x 1 = 1.

3. "WHY NOT 2=2×2=4" -- two jobs for "=":
    the same value:  every piece of the chain is the same number, so 2 = 2 x 2 = 4 says 2 = 4
                     -> wrong that way
    carry forward:   each "=" passes the result on to the next step
                     2 -> 2 x 2 = 4 -> right that way
    The chain in 1 is the carry-forward kind: read as "the same value", 12+9 = 21+2 would say
    21 = 23. Written with arrows, nothing clashes. (CLAUDE.md, notation rule, #371.)

4. THE THREE THINGS: remember what is connected to the past, register the current, predict the
    future; one action per registered action; verify; repeat.
    past, current, future = behind, yourself, right of #405: n - 1, n, n + 1.
    Making the next from the one behind and the current one is a recurrence that looks back two:
      1 1 -> 1 + 1 = 2 -> 1 + 2 = 3 -> 2 + 3 = 5 -> 3 + 5 = 8 ...
    predict the next, take the step, check it, repeat.

5. THE BRACKET LINES
    each pair of lines is a flip of the other:
      11,1)  <->  1,11(       the pair read backwards, ) turned to (
      12(13(12(13(12  <->  13)12)13)12)13    12 and 13 swapped, ( turned to )
    brackets opened and closed, counted:
      lines 1 and 2:   4 )  and 4 (     -> they close each other
      12(... and 13)...: 4 ( and 4 )    -> they close each other
      lines 4 and 5:   4 (  and 7 )     -> 3 more closing than opening
    line 1 has 11-1) once where the other three have 11,1)

6. THE = KEY SYMBOLS
      =   the same value                 2 + 2 = 4
      ≠   not the same value             66 ≠ 33
      ≈   close, not the same            1 ÷ 3 ≈ 0.333
      ≡   two uses: the same remainder by a number named with it (10 ≡ 1 by 9: 10 = 9 + 1),
          or the same for every value (x + x ≡ 2x)
    the numbers in the list, 11 22 33 66, are 11 x 1, 2, 3, 6:
      by 11 all four leave 0, so 11 ≡ 22 ≡ 33 ≡ 66 by 11
      66 ≡ 33 by 33 and by 3 too;  66 ≠ 33;  roots 11 -> 2, 22 -> 4, 33 -> 6, 66 -> 12 -> 3

7. THE 1,2,3 SUBSTRATE
    1 2 3 1 2 3 1 2 3 1 2 3: every number has a place in it, acting or not -- n's place is the
    remainder of n by 3, with 3 for 0: 4 -> 1, 5 -> 2, 6 -> 3, 137 -> 2.
    behind, yourself, right (n - 1, n, n + 1) always land on 1, 2 and 3, once each, for every n.
    both ways: without zero 1 2 3, twelve terms add to 4 x 6 = 24 (root 6);
               with zero 0 1 2 (the remainders), twelve terms add to 4 x 3 = 12 (root 3).

RESIDUES mod 37 (gf37-audit): 757 -> 17 NQR17 (prime), 573049 -> 30 C3, 11 NEG_H (twin with 13,
Sophie Germain 23, safe from 5), 22 NQR17, 33 D7, 66 -> 29 C9, 12 SA_ST_A, 13 CAS_EXT, 24 SEED,
45 -> 8 TESLA.

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as F
from sympy import isprime


def root(n):
    while n > 9:
        n = sum(map(int, str(n)))
    return n


# 1. the chain, carried forward
steps, total = [9, 2, 7, 6, 9], 12
chain = [total]
for s in steps:
    total += s
    chain.append(total)
assert chain == [12, 21, 23, 30, 36, 45] and 4 + 5 == 9 == root(45)

# 2. 75.7%
p = F(757, 1000)
assert F("075.7") == F("75.7")
assert p * (-p * -1) == p * p == F(573049, 1000000) and 757 * 757 == 573049
assert p * p * 100 == F(573049, 10000)                      # 57.3049%
assert isprime(757) and root(757) == 1 and root(573049) == 1 and sum(map(int, "573049")) == 28

# 3. two jobs for "="
assert 2 != 2 * 2 and 2 * 2 == 4                             # same-value reading: 2 = 4 is wrong
assert 12 + 9 == 21 and 21 + 2 == 23 and 12 + 9 != 21 + 2     # same-value reading of the chain clashes

# 4. look back two: next = behind + current
seq = [1, 1]
for _ in range(4):
    seq.append(seq[-2] + seq[-1])
assert seq == [1, 1, 2, 3, 5, 8]

# 5. brackets
lines = ["11,1)11,1)11-1)11,1)", "1,11(1,11(1,11(1,11(", "12(13(12(13(12", "1,2(1,2 (1,2 (1,2( ",
         "1,3)1,3))1,3))1,3))", "13)12)13)12)13"]
opens, closes = [l.count("(") for l in lines], [l.count(")") for l in lines]
assert (closes[0], opens[1]) == (4, 4)
assert (opens[2], closes[5]) == (4, 4)
assert (opens[3], closes[4]) == (4, 7)
assert lines[5] == lines[2].replace("12", "#").replace("13", "12").replace("#", "13").replace("(", ")")
assert [g for g in ["11,1", "11,1", "11-1", "11,1"]] == lines[0].split(")")[:4]

# 6. symbols on 11 22 33 66
nums = [11, 22, 33, 66]
assert nums == [11 * k for k in (1, 2, 3, 6)] and all(n % 11 == 0 for n in nums)
assert 66 % 33 == 33 % 33 and 66 % 3 == 33 % 3 and 66 != 33
assert [root(n) for n in nums] == [2, 4, 6, 3] and 10 % 9 == 1

# 7. the 1,2,3 substrate
def place(n):
    return n % 3 or 3


assert [place(n) for n in range(1, 13)] == [1, 2, 3] * 4 and [place(n) for n in (4, 5, 6, 137)] == [1, 2, 3, 2]
assert all(sorted(place(m) for m in (n - 1, n, n + 1)) == [1, 2, 3] for n in range(1, 10000))
assert sum([1, 2, 3] * 4) == 24 and root(24) == 6 and sum([0, 1, 2] * 4) == 12 and root(12) == 3

# residues
assert [x % 37 for x in (757, 573049, 11, 22, 33, 66, 12, 13, 24, 45)] == [17, 30, 11, 22, 33, 29, 12, 13, 24, 8]

if __name__ == "__main__":
    print("#410: chain 12 21 23 30 36 45 -> 9 right; 75.7% x 75.7% = 57.3049% right; "
          "'=' as same value makes 2=2x2=4 say 2=4, as carry-forward it is 2 -> 2x2 = 4; "
          "past/current/future = behind/yourself/right; brackets 4/4, 4/4, 4/7; 11 22 33 66 all ≡ 0 by 11; "
          "n-1, n, n+1 always land on 1, 2, 3 once each")
