# CLASS: AUDIT
"""
The comma sliding through four digits, the 12 taken both ways, and the pairs (owner_work #267, 2026-10-13).

THE OWNER'S LINES, verbatim:
    0,------000=1+3=4
    00,------00=2+2=4
    000,------0=3+1=4

    4×3=12
    3×4=12==(2+4=6)
    7×7=4+9=(1+3=4)

    6+4=10
    24+13=3+7=(10+1)=11


    12=3
    21=3


    34=7
    43=7

    46=1
    64=1

    33=6
    77=5
    11=2

EVERY LINE HOLDS.

THE COMMA THROUGH FOUR DIGITS
  The comma after digit 1, 2, 3 of a four-digit set: 1+3, 2+2, 3+1, each 4 (the comma sets of #265,
  now with the comma at every place). Each line has six dashes between the comma and the digits after it.
  4×3 = 12: three places for the comma, four digits each.

THE 12 BOTH WAYS
  4×3 = 12 and 3×4 = 12; the two 12s together are 24, and (2+4 = 6) is its digit sum -- the
  parenthesis as in #263 ("6x2=(1+2=3)"). 24 is written out two lines down.
  7×7 = 49, 4+9 = 13, 1+3 = 4.

THE TWO SUMS
  6+4 = 10 adds the 6 and the 4 just made. 24+13 adds the numbers they came from: 24+13 = 37,
  3+7 = 10 -- the same 10, because 24+13 has no carry. (10+1) = 11 is the +1 "to begin again" (#264).
  24+13 = 14+23 (the tens swap): the 14+23 = 37 of #263 (halving_strings_and_chain_2026_10_13.py).

THE PAIRS
  12 = 3, 21 = 3;  34 = 7, 43 = 7;  46 = 1, 64 = 1 (4+6 = 10 -> 1).
  12+34 = 46 and 21+43 = 64: the third pair is the first two added, and its root 1 is 3+7 = 10 -> 1.
  33 = 12+21, 77 = 34+43; 46+64 = 110. 33 = 6, 77 = 5 (14 -> 5), 11 = 2; 110 is also 2, and 33+77 = 110.
  A two-digit number plus its reversal is 11 x its digit sum: 33 = 11x3, 77 = 11x7, 110 = 11x10.

#268 (2026-10-13): the owner sent #267 again with this added, verbatim:
    0,
    00,
    000,

    this section goes by 369
    like this
    23
    123
    1123

    when we count the comma


    also with a comma we get 369

    ,000=3
    ,000=6
    ,000=9=18
    1+8=9
    and if we add the commas
    =18+3=21
    =9+3=12

  ,000 THREE TIMES -- holds: each ,000 adds three digits, 3, 6, 9; 3+6+9 = 18; 1+8 = 9; three commas:
  18+3 = 21 and 9+3 = 12 -- 21 and 12 both ways round, both root 3, the pair of #267.
  THE LEADS -- 369 = 3 x 123 (1, 2, 3 each times 3, no carries). 23 -> 123 -> 1123 each puts a 1 in
  front (+100, +1000). Their digit sums 5, 6, 7 are the characters of 0,000 / 00,000 / 000,000
  counting the comma (4+1, 5+1, 6+1). Open: how 23, 123, 1123 go by 3, 6, 9 -- asked.

FRAMEWORKS (#268): 3 C3 (twin with 5, Sophie Germain -> 7); 6 TESLA; 9 SA_ST_A; 18 SEED; 21 SA_ST_B;
  12 SA_ST_A; 23 TESLA, prime, Sophie Germain (47) and safe (11); 123 = 3 x 41 SA_ST_A;
  1123 prime -> 13 CAS_EXT, not twin, not Sophie Germain (2247 = 3 x 7 x 107); 369 = 3^2 x 41 -> 36 NEG_H.

#269 (2026-10-13): the owner sent #268 again with this added after "1123", verbatim:
    because
    123
    112233

    10-20-30
    11-22-33
    3---6--9+3 zeros =1+2=3
  and at the end:
    no comma count should be explored also because it creates a better understanding of the bigger picture..

    I look at one from the other as
    1=1 thats i view as something like integers vs primes or odds and even or positive or negative... I'm pretty sure it's a fairly new concept. Because I've never heard of what I'm telling you, and I just made the s*** up inside my head. But it makes sense to me. So that's why I keep going forward. Do you understand what I'm saying? It is not actually positive and negative odds or evens or indigenous or primes. It might have its own category. That's what we should figure out
  (typo: "indigenous" for "integers", as in the line before.)

  123 -> 112233: each digit written twice; 112233 = 11 x 10203 = 3 x 11 x 19 x 179.
  10-20-30 is 1, 2, 3 with a zero; 11-22-33 is 1, 2, 3 written twice. Down each column:
  10 over 11, 20 over 22, 30 over 33 add to 21, 42, 63 -- digit sums 1+0+1+1 = 3, 2+0+2+2 = 6,
  3+0+3+3 = 9: the 3, 6, 9. 3+6+9 = 18 -> 9; with the 3 zeros of 10-20-30: 9+3 = 12, 1+2 = 3 --
  the same step as "=9+3=12" with the 3 commas in #268.
  112233 is 12 mod 37, like 123 and 12333 (112233 - 123 = 37 x 3030) -- recorded, not claimed.

FRAMEWORKS (#269): 10 IC; 20 DARK_A; 30 C3; 11 NEG_H, prime, twin (11, 13), Sophie Germain with
  2 x 11 + 1 = 23 -- the 23 of "23 / 123 / 1123" (so 23 is safe); 22 NQR17; 33 D7; 42 CAS_EXT; 63 IC;
  112233 -> 12 SA_ST_A.

FALSIFICATION: any assertion failing.
"""


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


for s, k in (("0,------000", (1, 3)), ("00,------00", (2, 2)), ("000,------0", (3, 1))):
    lead, rest = s.split(",")
    assert (len(lead), len(rest.replace("-", ""))) == k and sum(k) == 4 and rest.count("-") == 6
assert 4 * 3 == 3 * 4 == 12 and 12 + 12 == 24 and 2 + 4 == 6
assert 7 * 7 == 49 and 4 + 9 == 13 and 1 + 3 == 4
assert 24 + 13 == 14 + 23 == 37
assert 6 + 4 == 10 and 24 + 13 == 37 and 3 + 7 == 10 and 10 + 1 == 11
assert dr(24) + dr(13) == 10 and (24 % 10 + 13 % 10) < 10                       # no carry
for a, b, r in ((12, 21, 3), (34, 43, 7), (46, 64, 1)):
    assert dr(a) == dr(b) == r and int(str(a)[::-1]) == b
assert 12 + 34 == 46 and 21 + 43 == 64 and dr(3 + 7) == 1
assert 12 + 21 == 33 and 34 + 43 == 77 and 46 + 64 == 110 and 33 + 77 == 110
assert (dr(33), dr(77), dr(11), dr(110)) == (6, 5, 2, 2) and 7 + 7 == 14 and 1 + 4 == 5
for n in (12, 34, 46):
    assert n + int(str(n)[::-1]) == 11 * sum(map(int, str(n)))

# 268
run = [3 * k for k in (1, 2, 3)]
assert run == [3, 6, 9] and sum(run) == 18 and 1 + 8 == 9 and 18 + 3 == 21 and 9 + 3 == 12
assert dr(21) == dr(12) == 3 and str(21)[::-1] == "12"
assert 369 == 3 * 123 and [3 * d for d in (1, 2, 3)] == [3, 6, 9]
assert 123 - 23 == 100 and 1123 - 123 == 1000
for n, sset in ((23, "0,000"), (123, "00,000"), (1123, "000,000")):
    assert sum(map(int, str(n))) == len(sset) == len(sset.replace(",", "")) + 1
from sympy import factorint, isprime
assert isprime(23) and isprime(47) and isprime(11) and isprime(1123) and not isprime(2247)
assert factorint(369) == {3: 2, 41: 1} and factorint(2247) == {3: 1, 7: 1, 107: 1}
assert [n % 37 for n in (18, 21, 12, 23, 123, 1123, 369)] == [18, 21, 12, 23, 12, 13, 36]

# 269
assert int("".join(d * 2 for d in "123")) == 112233 == 11 * 10203 and factorint(112233) == {3: 1, 11: 1, 19: 1, 179: 1}
tens, twins = [10, 20, 30], [11, 22, 33]
assert [a + b for a, b in zip(tens, twins)] == [21, 42, 63]
assert [sum(map(int, f"{a}{b}")) for a, b in zip(tens, twins)] == [3, 6, 9] == [dr(a + b) for a, b in zip(tens, twins)]
assert "".join(map(str, tens)).count("0") == 3 and 3 + 6 + 9 == 18 and 9 + 3 == 12 and 1 + 2 == 3
assert 112233 % 37 == 123 % 37 == 12333 % 37 == 12 and 112233 - 123 == 37 * 3030
assert isprime(11) and isprime(13) and 2 * 11 + 1 == 23

if __name__ == "__main__":
    print("every line of #267, #268 and #269 checked holds; columns 10/11, 20/22, 30/33 -> 3, 6, 9; 369 = 3 x 123; 12+34 = 46, 21+43 = 64; 12+21 = 33, 34+43 = 77, 46+64 = 110 = 33+77")
