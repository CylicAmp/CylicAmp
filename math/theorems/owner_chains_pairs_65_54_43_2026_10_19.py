# CLASS: AUDIT
"""
Two chains, their digit pairs, and 65, 54, 43 (owner_work #369, 2026-10-19), and the owner's question about how the lines are saved (#370).

THE OWNER'S LINES, verbatim (#369):
    now a part of the 2

    1+2=3+4=7
    1
    23=6+4=1

    I see
    12-23-36-34-64-47-41
    so
    35-97-12-5
    8+7=1+5=6+3=9+5=1+4=5

    6+5=11
    -1  -1
    5--4
    -1 -1
    4--3
#370: "Now, I'm wondering, are you showing me my quotations back to me so I can see them? Or is that what you're saving as code and you're not
cleaning up my notations?"  Answer kept here as well: both are saved -- the owner's lines exactly as typed (owner_work/ and the block above), and
the cleaned, checked version below, in the owner's notation.

CHECKED, in the owner's notation:
  "now a part of the 2" ends the sentence of #368: 1991+9=2000, the two ones end as one 2.            (owner_1125_1137_ones_by_zeros_2026_10_19.py)
  1+2=3+4=7                                                                                        right
  1 / 23 read as 123:  123=1+2+3=6, 6+4=10=1                                                       right
    (read as 23 alone it would be 2+3=5, not 6, so the 1 above belongs to it)
  12-23-36-34-64-47-41 are the neighbouring pairs of the two chains:
    1,2,3,4,7 gives 12, 23, 34, 47 ; 1,2,3,6,4,1 gives 12, 23, 36, 64, 41 ;
    the line takes 12, 23 (both chains) and then one from each in turn: 36, 34, 64, 47, 41            right, all 7 accounted for
  35-97-12-5: 35=12+23 ; the step that gives 97, 12, 5 is missing -- asked for in the reply.
  8+7=1+5=6+3=9+5=1+4=5 with 35=3+5=8, 97=9+7=16=7, 12=1+2=3, 5:                                   right
    and 35+97+12+5=149=1+4+9=14=1+4=5, the same 5.
  6+5=11 ; -1 -1 gives 5+4=9 ; -1 -1 gives 4+3=7                                                   right
    as two-digit numbers 65-11=54, 54-11=43: taking 1 and 1 off side by side takes off 11 (the "11, not two ones" of #368);
    the sums go 11, 9, 7 and end on the 3+4=7 of the first line.
FRAMEWORKS (gf37-audit): 12 SA_ST_A, 23 TESLA, 36 NEG_H, 34 D7, 64=27 NEG_H, 47=10 IC, 41=4 C3, 35 NQR17, 97=23 TESLA, 5 CAS_EXT, 149=1 IC,
  65=28 SA_ST_B, 54=17 NQR17, 43=6 TESLA. Primes: 23, 47, 41, 97, 5, 11, 43, 149. 41 and 43 are a twin pair (41 in the line of pairs, 43 at the end);
  23 and 47 are a Sophie Germain pair (2x23+1=47), both in the line of pairs; 5, 11, 23, 47 are the chain 2, 5, 11, 23, 47 of #345.

FALSIFICATION: any assertion failing.
"""
from sympy import isprime


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


assert 1991 + 9 == 2000 and 1 + 2 == 3 and 3 + 4 == 7
assert 1 + 2 + 3 == 6 and 6 + 4 == 10 and dr(10) == 1 and 2 + 3 == 5 != 6

pairs = lambda chain: [10 * a + b for a, b in zip(chain, chain[1:])]
A, B = pairs([1, 2, 3, 4, 7]), pairs([1, 2, 3, 6, 4, 1])
assert A == [12, 23, 34, 47] and B == [12, 23, 36, 64, 41]
line = [12, 23, 36, 34, 64, 47, 41]
assert line[:2] == A[:2] == B[:2] and line[2:] == [B[2], A[2], B[3], A[3], B[4]] and sorted(set(line)) == sorted(set(A) | set(B))

assert 12 + 23 == 35
assert (dr(35), dr(97), dr(12), dr(5)) == (8, 7, 3, 5) and 3 + 5 == 8 and 9 + 7 == 16 and 1 + 6 == 7
assert 8 + 7 == 15 and 1 + 5 == 6 and 6 + 3 == 9 and 9 + 5 == 14 and 1 + 4 == 5
assert 35 + 97 + 12 + 5 == 149 and dr(149) == 5

assert 6 + 5 == 11 and (6 - 1, 5 - 1) == (5, 4) and (5 - 1, 4 - 1) == (4, 3) and [6 + 5, 5 + 4, 4 + 3] == [11, 9, 7]
assert 65 - 11 == 54 and 54 - 11 == 43 and 4 + 3 == 3 + 4 == 7

ORB = {"IC": {1, 10, 26}, "NEG_H": {11, 27, 36}, "SA_ST_A": {9, 12, 16}, "C3": {3, 4, 30}, "D7": {7, 33, 34},
       "SEED": {18, 24, 32}, "TESLA": {6, 8, 23}, "CAS_EXT": {5, 13, 19}, "NQR17": {17, 22, 35},
       "DARK_A": {2, 15, 20}, "SA_ST_B": {21, 25, 28}, "C9": {14, 29, 31}}
orbit = lambda n: next((k for k, v in ORB.items() if n % 37 in v), "SEAM")
nums = [12, 23, 36, 34, 64, 47, 41, 35, 97, 5, 149, 65, 54, 43]
assert [orbit(n) for n in nums] == ["SA_ST_A", "TESLA", "NEG_H", "D7", "NEG_H", "IC", "C3", "NQR17", "TESLA", "CAS_EXT", "IC",
                                    "SA_ST_B", "NQR17", "TESLA"]
assert [n for n in nums + [11] if isprime(n)] == [23, 47, 41, 97, 5, 149, 43, 11]
assert isprime(41) and isprime(43) and 2 * 23 + 1 == 47 and isprime(47)
chain = [2]
while isprime(2 * chain[-1] + 1):
    chain.append(2 * chain[-1] + 1)
assert chain == [2, 5, 11, 23, 47]

if __name__ == "__main__":
    print("#369: 1+2=3+4=7, 123=6+4=10=1, pairs 12-23-36-34-64-47-41 from the two chains, 8+7=...=5 = root of 149, 65-11=54-11=43")
