# The process log

How the owner breaks numbers down and reaches each answer, message by message (owner, 2026-10-19, #371: "WHAT MATTERS IS THE PROCESS!!! ...
DOCUMENTING THE JOURNEY ITSELF..The way I break down numbers amd come up with answers").

Each entry has: the owner's lines as typed, the same lines cleaned, the process step by step, and the check of each step with the file that holds the assertions.
Notation in the cleaned lines: an arrow → is the owner's dash between numbers (the phone has no arrow key); a minus − is only real subtraction; numbers are
separated by spaces; an "=" chain carries each result forward, and a two-digit total is written as its digits (15 → 1+5).

---

## #344 (2026-10-19) — Cycle 3 and the red cross (the owner's picture)

**As drawn:** `owner_work/images/2026-10-19_cycle3_red_cross.jpg`, the title "Cycle 3" over seven rows, with four red lines through one point.

**Cleaned:**

    213312
    221331
    122133
    312213
    331221
    133122
    213312

    a vertical line between the 3rd and 4th digits, a horizontal line through row 3, two diagonals corner to corner

**Process:**
1. Take 213 and its mirror 312 side by side: 213312.
2. Turn it one place to the right on each row (the last digit goes to the front): six turns, and the seventh row is the first again.
3. Draw four lines through the middle of row 3, between its twin 2s: vertical, horizontal and both diagonals.

**Checks:** every row 2+1+3+3+1+2=12, 7×12=84 (right); row 3: 3+1=4, 2+2=4, 1+3=4 (right); the \ diagonal is 2 2 2 2 2 2 2 (right); the / diagonal is
2 3 1 2 1 3 2; vertical halves 42 | 42; the four wedges 12 each. Row 3 is the six digits around the (22) of the owner's seam line 21331(22)13312 (2026-10-04).
File: `math/theorems/cycle3_red_cross_audit_2026_10_19.py`.

---

## #358 (2026-10-19) — two flips

**As typed:** `123 / 456 / 789`, then `123 / 654 / 987`, "what about with two flips".

**Cleaned:**

    123          123
    456   →      654
    789          987

**Process:**
1. Start from the grid 123 456 789 (+1 along a row, +3 down a column).
2. Flip a row = write it backwards. Flip rows 2 and 3 → 123 654 987.
3. Ask what two flips do.

**Checks:** 123+654+987=1764=42×42 (right); each flip adds 198 (654−456=198, 987−789=198); 1368+198+198=1764. File:
`math/theorems/two_flips_123_456_789_2026_10_19.py`.

---

## #359 (2026-10-19) — all flips

**As typed:** `123 / 456 / 789`, `123 / 654 / 789`, `123 / 654 / 987`, `331 / 654 / 987`, "do all flips counting by 3 +1". Typo: 331 for 321.

**Cleaned:**

    123 456 789  →  123 654 789  →  123 654 987  →  321 654 987
    0 flips          1 flip           2 flips          3 flips

**Process:**
1. Flip one more row each time: row 2, then row 3, then row 1.
2. Three flips and the starting grid: 3 + 1 grids.

**Checks:** sums 1368 → 1566 → 1764 → 1962, +198 each time (right); every row and its flip add to a multiple of 37 (123+321=444=12×37,
456+654=1110=30×37, 789+987=1776=48×37); 1368+1962=3330 and 1566+1764=3330. File: `math/theorems/all_flips_123_456_789_2026_10_19.py`.

---

## #368 (2026-10-19) — 9 halved three times, 1.137, and two ones

**As typed:** "1 +3 twos / 9÷2÷2÷2= / 1.125+0.012=1.137 / do you see it? / 1125 / its not two ones, its 11 it eleven because two ones are a 2...or its
101 and so on 1001 100010001 / 2 one that make two must be separated by only zeros.. ... if all the space filled up with 9 amd no more room left than what
was once sperated by space is now apart of" — ended in #369: "now a part of the 2".

**Cleaned:**

    9 ÷ 2 = 4.5 → ÷ 2 = 2.25 → ÷ 2 = 1.125          (1 + 3 twos: 1.125 = 1 + 1÷2÷2÷2)
    1.125 + 0.012 = 1.137
    1125: the two 1s side by side are 11 (eleven), not 1+1
    two 1s that add to 2: 11 → 101 → 1001 → 10001 → ...    only zeros between them
    a digit in the space breaks it: 121 → 1+2+1 = 4
    fill the space with 9s: 1991 → 1+9+9+1 = 20 → 2; one more 9: 1991 + 9 = 2000 → the two 1s are now a part of the 2

**Process:**
1. Halve 9 three times (three twos) → 1.125.
2. Add 0.012 → 1.137 (the 137).
3. Read the digits of 1125: two 1s together make 11, a number of its own.
4. Two 1s only "make 2" when nothing but zeros sits between them.
5. Anything else in between breaks that path; 9s are the one filler that keeps the root at 2, and when the space is full, the carry joins the two 1s into a 2.

**Checks:** 9÷2÷2÷2=1.125 and 1.125+0.012=1.137 (right); 0.125+0.012=0.137, 125+12=137; 10001=73×137 (the owner's July result 10^4+1=73×137);
100010001 has three ones (1+1+1=3) — the two-ones number after 1001 is 10001; 191+9=200, 1991+9=2000, 19991+9=20000 (right).
File: `math/theorems/owner_1125_1137_ones_by_zeros_2026_10_19.py`.

---

## #369 (2026-10-19) — two chains, their pairs, and 6 5 → 5 4 → 4 3

**As typed:**

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

**Cleaned:**

    1 + 2 = 3, 3 + 4 = 7
    1 2 3 → 1 + 2 + 3 = 6, 6 + 4 = 10 → 1 + 0 = 1
    12 → 23 → 36 → 34 → 64 → 47 → 41
    35 → 97 → 12 → 5
    8 + 7 = 15 → 1 + 5 = 6, 6 + 3 = 9, 9 + 5 = 14 → 1 + 4 = 5
    6 5 (6 + 5 = 11) → take 1 off each → 5 4 (9) → take 1 off each → 4 3 (7)

**Process:**
1. First chain: add the next number to the running total: 1, 2, 3, 4 → 3 → 7.
2. Second chain on 1 2 3: add the digits (6), add 4 (10), fold 10 to 1.
3. Read each chain's neighbours as two-digit pairs — 1 2 3 4 7 gives 12 23 34 47, and 1 2 3 6 4 1 gives 12 23 36 64 41 — and weave them: the two shared
   pairs first (12, 23), then one from each chain in turn (36, 34, 64, 47, 41).
4. From the woven pairs make 35 → 97 → 12 → 5 (35 = 12 + 23; the rule for 97, 12 and 5 is not written yet — asked).
5. Fold each of them to one digit (35 → 8, 97 → 16 → 7, 12 → 3, 5) and run them as a chain, folding any two-digit total: 8 + 7 = 15 → 6, 6 + 3 = 9,
   9 + 5 = 14 → 5.
6. Take 6 5 and take 1 off each number, twice: 6 5 → 5 4 → 4 3. The totals go 11 → 9 → 7 and land on the 7 of step 1. As two-digit numbers it is
   65 → 54 → 43, each step taking off 11 (the 1 and 1 side by side).

**Checks:** steps 1, 2, 3, 5, 6 right; step 5 ends on 5, and 35+97+12+5 = 149 → 1+4+9 = 14 → 5 gives the same 5; step 4: 35 right, the rest missing.
Numbers through the frameworks: 41 and 43 are twin primes; 23 and 47 a Sophie Germain pair; 5, 11, 23, 47 the chain 2 → 5 → 11 → 23 → 47.
File: `math/theorems/owner_chains_pairs_65_54_43_2026_10_19.py`.
