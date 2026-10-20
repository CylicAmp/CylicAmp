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

---

## #372 (2026-10-20) — ones and zeros around the comma, 1314 and 1413

**As typed:** see `owner_work/messages/2026-10-20.txt`, #372 (quoted in full in the file below). The message ends on a bare "=".

**Cleaned:**

    1,000   → 1,0   → 1 + 1 = 2          one 1, one 0
    11,000  → 11,00 → 2 + 2 = 4          two 1s, two 0s
    111,000 → 3 + 3 = 6                  three 1s, three 0s
    111,000 = 1000 × 111   an even number of odds
    111,000 = 111 × 1000   an odd number of evens

    1,000      1 + 3 = 4   (with the comma 4 + 1 = 5)     → 1314
    10,000     2 + 3 = 5                                  → 2335
    100,000    3 + 3 = 6                                  → 3336
    1,000,000  (stops here)

    1314 → 1413                 13 | 14 swapped to 14 | 13
    1413 → 1+4 = 5, 1+3 = 4 → 5 4 → (1 2: step missing)
    1413 → 4 − 3 = 1 → 1 + 1 + 1 = 3
    14.13 → 14 | 13 → 5 + 4 = 9
    141 + 3 → 1+4+1+3 = 9   (141 + 3 = 144 → 1+4+4 = 9)
    1-4-1 → 141
    = (open)

**Process:**
1. Take 1 with zeros, 11 with zeros, 111 with zeros, and count the 1s and as many 0s: 1+1, 2+2, 3+3.
2. Read 111,000 two ways: 1000 copies of an odd number, or 111 copies of an even number.
3. Count the digits on each side of the comma: 1+3, 2+3, 3+3, and the comma itself as one more (4 | 1 = 5).
4. Write the counts as one number: 1314, 2335, 3336 (first digit = digits before the comma, second = digits after, last = all digits).
5. Swap the halves of 1314 → 1413, put a point between them (14.13), add inside each half (5 and 4), add those (9).
6. Split 1413 another way, 141 | 3: 1+4+1 = 6, 6+3 = 9, the same 9; 141 reads the same both ways.

**Checks:** steps 1, 2, 3, 5, 6 right; step 4: digits 1, 2 and 4 of each code right; the third digit (1, 3, 3) has no rule written yet — asked.
Also asked: the ends of "(2+335", "(3+3=6)+3336(" and the 1,000,000 line; the step "1--2"; the line "1-44-1-4"; what follows the last "=".
File: `math/theorems/owner_commas_1314_1413_2026_10_20.py`.

---

## #373 (2026-10-20) — 8 by halvings, a little Conway and a little of the owner's own

**As typed:** "8=44,2222,111,111,11 / 2442|31|31+21=5+2=7 / 248 / 24332 / 248= its also 24424884", with the owner's spoken explanation (quoted in the file).
The owner's earlier line on the same idea (2026-10-04): "1+7=8=44,2222,11111111=248=1+4=5".

**Cleaned:**

    8 = 4+4 = 2+2+2+2 = 1+1+1+1+1+1+1+1  →  44  2222  111 111 11
    44 → 24   2222 → 42   111 → 31   111 → 31   11 → 21        (count, then the digit)
    31 + 21 = 52 → 5 + 2 = 7
    two 4s, four 2s, eight 1s → 2 4 8
    group sizes 2 4 3 3 2 → 24332        (2+4+3+3+2 = 14 digits)
    2 4 8 → 24 42 48 84 → 24424884        (each neighbour pair and its flip; 2442 doubled = 4884)

**Process:**
1. Halve 8 down to ones: two 4s, four 2s, eight 1s, and write the 1s in comma groups of three (111,111,11).
2. Read every group by saying what is in it: two 4s → 24, four 2s → 42, three 1s → 31, three 1s → 31, two 1s → 21.
3. Add the last two readings: 31 + 21 = 52, and 5 + 2 = 7.
4. Count each digit over the whole line: 2, 4, 8 → 248.
5. Count each group's size: 2, 4, 3, 3, 2 → 24332.
6. From 248, write each neighbour pair with its flip: 24 42, 48 84 → 24424884.
7. Conway's look-and-say does step 2 without the commas: 44 2222 11111111 → 24 42 81 → 244281.

**Checks:** all seven right. 2442, 4884 and 24424884 are multiples of 37 (2442 = 66×37); 248 = 26 mod 37.
File: `math/theorems/owner_8_halvings_conway_248_2026_10_20.py`.

---

## #374 (2026-10-20) — the even one: 248 → 2442 4884 (adds to #373)

**As said:** "the one that's even, for example, if I got 2442, then I'm going, or I got 2248, right? I start with 248. What I'm doing there is I go,
I got 2442 4884."

**Cleaned:**

    248 → 24 → 2442      24 and its flip 42
        → 48 → 4884      48 and its flip 84

**Process:** start with 248; take each neighbour pair (24, 48); write it followed by its flip, which makes a four-digit mirror (2442, 4884).

**Checks:** right. Every four-digit mirror abba is a multiple of 11; when the inner digit is twice the outer (2442, 4884) it is a multiple of
1221 = 3×11×37: 2442 = 2×1221, 4884 = 4×1221 = 2×2442. "2248" in the dictation is read as "to 248". File: `math/theorems/owner_8_halvings_conway_248_2026_10_20.py`.

---

## #375 (2026-10-20) — reading back and forth, Conway out loud, 0.125 → 0.123

**As typed:** see the file below (quoted in full).

**Cleaned:**

    248 → 24 42 48 84                         read each pair, then read it back
    44 2222 1111|1111 → 24 42 81 → 244281     Conway, out loud: two 4s, four 2s, eight 1s
    2|8|1:  8 ÷ 2 = 4 → ÷ 2 = 2 → ÷ 2 = 1
    9 + 3 = 12 → 1 + 2 = 3
    9 + 6 = 15 → 1 + 5 = 6
    0.125 → take 2 from the 5 → 0.123
    11.123   0.333   11.222                   (step to these not written yet)

**Process:**
1. Read 248 back and forth: 24, 42, 48, 84.
2. Say the halving line out loud the way Conway does: two 4s, four 2s, eight 1s → 244281.
3. Halve 8 three times to reach 1 (the 2, the 8 and the 1 of "2|8|1").
4. Add 9 to 3 and to 6 and fold: the 9 disappears and 3 and 6 come back.
5. Take 0.125 (1 halved three times) and take 2 from its last digit: 0.123.
6. Then 11.123 and 11.222 (0.333 withdrawn by the owner in #376) — the step is explained in #376: the 2 taken from the 5 goes in front as 1 1.

**Checks:** steps 1–5 right. On step 6 the numbers show: 11.123 and 11.222 both add to 8 (1+1+1+2+3, 1+1+2+2+2); 0.333 adds to 9; .123 → .222
moves one from the 3 to the 1 (sum stays 6); .123 + .333 = .456. File: `math/theorems/owner_248_back_and_forth_0125_2026_10_20.py`.

---

## #376 (2026-10-20) — the last step of #375, explained by the owner

**As said:** "I started with a 5 at the end. And I took minus 2 from that 5. That's how I got the 1-1. ... I could have just put 2 right there ...
2, 1, 2, 3. But I decided to put a 1 and a 1 there. ... The 333 is not in there. ... So it's 11123 11222. Because I could just minus 1 from the 3.
And give it to the 1 in the front, and that's how I get the 222. Now, I can also have 323. ... But that's the best it's going to get."

**Cleaned:**

    0.125 → take 2 from the 5 → 0.123
          → put the 2 in front as 2    → 2.123
          → put the 2 in front as 1 1  → 11.123
    11.123 → take 1 from the 3, give it to the 1 in front of it → 11.222
    0.123 → give the 2 to the first digit → 0.323
    (0.333 is out: the owner's correction)

**Process:** start with 0.125; take 2 off the last digit; place those 2 somewhere else — whole (2), split (1 1), or onto another digit (3);
then move 1 more between neighbours (3 → 2, 1 → 2). Nothing is created or lost: every form adds to the 8 of 0.125.

**Checks:** right — 1+2+5 = 2+1+2+3 = 1+1+1+2+3 = 1+1+2+2+2 = 3+2+3 = 8. The value changes each time; the sum does not. 323 = 17×19, two twin primes.
File: `math/theorems/owner_248_back_and_forth_0125_2026_10_20.py`.

---

## #377 (2026-10-20) — take 2 from the 5, then take 3

**As typed:** "0.125 / 5-2 / 11.123 / 2.123 / 0.323 / 5-3 / 0.122 / 2.222"

**Cleaned:**

    0.125 → take 2 from the 5 → 11.123   2.123   0.323
    0.125 → take 3 from the 5 → 0.122 → 2 in front, 1 onto the first digit → 2.222

**Process:** the same move as #376 with a bigger piece: take 3 off the 5 (leaving 0.122), then put the 3 back elsewhere, here as 2 in front and 1 on the
first digit, so every digit becomes 2.

**Checks:** right — 0.122 adds to 5 while the 3 is out; 2.222 adds to 2+2+2+2 = 8, the four 2s of 8 = 2+2+2+2 (#373), and it is the only way to put the 3
back so all digits are equal. File: `math/theorems/owner_248_back_and_forth_0125_2026_10_20.py`.

---

## #378 (2026-10-20) — every form of 0.125, counted

**As typed:** "0.125 / 5-2 / 0.12311 / 0.1232 / 11.123 / 2.123 / 0.323 / 5-3 / 0.122 / 2.222 / 1.313", then: "You can make a bunch of different things from this
because you can reduce from any number or you can add to any number. You can add to the length of the number. You can add one way to the number, to the
left side or to the right side. And there's only a certain amount of things that you can do like that, and I would like the exact number."

**Cleaned:**

    0.125 → take 2 from the 5 → 0.123 → put the 2 on the right as 1 1 → 0.12311
                                       → put the 2 on the right as 2   → 0.1232
                                       → on the left as 1 1 → 11.123, as 2 → 2.123
                                       → onto the first digit → 0.323
    0.125 → take 3 from the 5 → 0.122 → 2.222, 1.313

**Process (the rule):** take units off any digit and put them back onto any digit or as new digits on either side; the length can grow; the 8 of 0.125
(1+2+5) is never lost.

**The exact number:** 576 — every way to write digits 1–9 that add to 8 (128 ways), with the point in each place that leaves a digit after it
(1×1 + 2×7 + 3×21 + 4×35 + 5×35 + 6×21 + 7×7 + 8×1 = 576). 704 if whole numbers with nothing after the point also count. Zeros are left out: they can be added
without end. All of the owner's examples are in the 576. File: `math/theorems/owner_0125_all_forms_count_2026_10_20.py`.
