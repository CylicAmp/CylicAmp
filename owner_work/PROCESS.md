# The process log

How the owner breaks numbers down and reaches each answer, message by message (owner, 2026-10-19, #371: "WHAT MATTERS IS THE PROCESS!!! ...
DOCUMENTING THE JOURNEY ITSELF..The way I break down numbers amd come up with answers").

Each entry has: the owner's lines as typed, the same lines cleaned, the process step by step, and the check of each step with the file that holds the assertions.

**Standing parts of the owner's process** (apply to every entry):
- **Count both ways — with and without.** Every count is given with zero and without zero, as with the comma and without the comma (#269: "no comma count
  should be explored also because it creates a better understanding of the bigger picture"; #379: "very good with zero amd without ... so totals are for
  both"). Both totals are written down, every time.
- **The calculator's last digit is rounded.** The last digit a calculator shows can be rounded up, and the same division in two orders can end differently
  (#385: 0.0004166667 ends in a rounded 7; #394: 1% ÷ 1 ÷ 2 ÷ 3 ÷ 4 ends …668 and 1% ÷ 4 ÷ 3 ÷ 2 ÷ 1 ends …666, the true digits being 6 for ever). A digit chain is run
  on the exact digits (a fraction, or the repeating block), or on the digits before the last one shown.
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

---

## #379 (2026-10-20) — totals with zero and without

**As typed:** "very good with zero amd without... / seeing on how I covered this already before and either not saved or not made into part of the process of
how I do.. / so totals are for both"

**The rule, now in the standing parts above:** every count is given with and without (zero, or the comma).

**Totals for #378, both ways:**

    without zero:  1 + 14 + 63 + 140 + 175 + 126 + 49 + 8 = 576         (704 with whole numbers)
    with zero:     1 + 17 + 117 + 525 + 1815 + 5247 + 13299 + 30459 = 51480   up to 8 digits

With zero there is no last length (another 0 always fits), so the with-zero total is given by number of digits; up to 8 digits, the longest form without
zero, it is 51480. Example for 2 digits: 08 17 26 35 44 53 62 71 80 → 0.08 … 0.80 (9) and 1.7 … 8.0 (8) → 17.
File: `math/theorems/owner_0125_all_forms_count_2026_10_20.py`.

---

## #380 (2026-10-20) — the same with 0.137

**As typed:** "now do the same with 0.137"

**Cleaned:**

    0.137 → 1+3+7 = 11 is the total kept
    0.137 → take 2 from the 7 → 0.135 → 2.135   11.135   0.1352   0.13511   0.335      (each adds to 11)

**Process:** the moves of #376–#378 started from 0.137 instead of 0.125; the total kept is 11 instead of 8.

**Totals, both ways:**

    without zero:  0 + 8 + 45 + 120 + 210 + 252 + 210 + 120 + 45 + 10 + 1 = 1021 digit strings
                   with the point: 2x8 + 3x45 + 4x120 + 5x210 + 6x252 + 7x210 + 8x120 + 9x45 + 10x10 + 11x1 = 6139   (7160 with whole numbers)
    with zero:     0 + 16 + 191 + 1185 + 5308 + 19292 + 60297 + 167791 + 425429 + 999091 + 2199945 = 3878545   up to 11 digits

**What is new against 0.125:** a digit stops at 9, so 11 can't be one digit and 10 + 1 can't be two: 2x2x2x2x2x2x2x2x2x2 = 1024, minus those 3 = 1021.
1021 is prime, twin with 1019. File: `math/theorems/owner_0137_all_forms_count_2026_10_20.py`.

---

## #381 (2026-10-20) — where 0.125 came from; 12 apart; 0.253

**As typed:** "0.125 i got by dividing what times what? Its a important detail. / because / 0125+ / 0.012=0137 are exactly 12 apart / 0.253 all prime building blocks"

**Cleaned:**

    9 ÷ 2 = 4.5 → ÷ 2 = 2.25 → ÷ 2 = 1.125        (#368: 9 divided by 2 three times = 9 ÷ 8)
    1.125 = 1 + 0.125, and 0.125 = 1 ÷ 2 ÷ 2 ÷ 2 = 1 ÷ 8
    0.125 + 0.012 = 0.137 → 137 − 125 = 12
    0.253 → 2 5 3, all prime

**Process:** the start of the 0.125 work is the halving: 9 ÷ 2 ÷ 2 ÷ 2 (#368). Adding 0.012 reaches 0.137, 12 thousandths further on.

**Checks:** right — 9 ÷ 8 = 1.125; 0.125 + 0.012 = 0.137; 2, 5, 3 prime; also 253 = 11 × 23 (two primes, 2×11+1 = 23) and 253 = 125 + 128.
Open: how 0.253 is made — asked. File: `math/theorems/owner_0125_origin_12_apart_0253_2026_10_20.py`.

---

## #382 (2026-10-20) — odds make evens; 5 is two sevens; 20 is 8 sevens

**As typed:** "2 made from odd odd =even / or 4 odds even / 1÷2=0.5 +0.5 / 2=1+1=0.5×4=2.0 or 0.20 im not sure / 4 × 5 =20 / 5=2 number sevens / because /
5÷2=2.5+2.5 / so 20 equal 5555 / thats 8 sevens"

**Cleaned:**

    1 + 1 = 2                      two odds → even
    5 + 5 + 5 + 5 = 20             four odds → even
    1 ÷ 2 = 0.5 → 0.5 + 0.5 = 1
    2 = 1 + 1 = 0.5 × 4 = 2.0      (not 0.20)
    4 × 5 = 20
    5 ÷ 2 = 2.5 → 2.5 + 2.5 = 5,  2.5 → 2 + 5 = 7  → 5 is two sevens
    20 = 5 5 5 5 = 8 × 2.5         → 8 sevens

**Process:** split a number into halves, read each half by its digits (2.5 → 7), and count how many halves make the whole: 5 = two halves = two 7s;
20 = four 5s = eight halves = eight 7s.

**Checks:** all right except "0.20": 0.5 × 4 = 2.0; 0.20 is 0.5 × 0.4. Both ways with zero: 2.0 = 2 (a 0 at the end changes nothing); 0.20 = 0.2 (a 0 in front
moves the 2 down a place). The roots agree: 7 + 7 = 14 → 5; 8 × 7 = 56 → 11 → 2 = 2 + 0. Halving again and again walks the doubling roots backwards:
5 → 7 → 8 → 4 → 2 → 1 → 5 (2.5, 1.25, 0.625, 0.3125, 0.15625, 0.078125). File: `math/theorems/owner_halves_sevens_20_5555_2026_10_20.py`.

---

## #383 (2026-10-20) — 20 as 55|55 and 77|77|77|77; halving 7

**As typed:** "20 is made from 55|55 even odds / 20 is made from 77|77|77|77 / 7÷2=3.5+3.5=7 / so / 8 sevens = / 7 × 3.5+3.5 / or 7x7=4+9=1-3=4"

**Cleaned:**

    20 = 5 + 5 | 5 + 5                          four odds, an even count
    20 = 7 7 | 7 7 | 7 7 | 7 7                  eight halves of 5 (2.5 → 7)
    7 ÷ 2 = 3.5 → 3.5 + 3.5 = 7,  3.5 → 3 + 5 = 8
    8 sevens = 7 × 3.5 + 3.5   (reading asked)
    or 7 × 7 = 49 → 4 + 9 = 13 → 1 + 3 = 4

**Process:** write 20 as its odd pieces (four 5s), then as their halves read by digits (eight 7s); halve 7 the same way (two 3.5s, each read 8).

**Checks:** right — 5+5+5+5 = 20; 8 × 2.5 = 20 and 8 × 7 = 56 → 11 → 2 = 2+0; 3.5 + 3.5 = 7 and 8 + 8 = 16 → 7. "7 × 3.5 + 3.5" as written is 28 = 8 × 3.5
(eight halves of 7); with brackets it is 7 × 7 = 49 → 4, which is seven sevens — eight sevens is 8 × 7 = 56 → 2. Asked which is meant.
File: `math/theorems/owner_halves_sevens_20_5555_2026_10_20.py`.

---

## #384 (2026-10-20) — 3.5 and 5.3 read 8; 1.6 and 6.1

**As typed:** "3.5=8 / 3.5=8+8=(1+6=7) / 6=6.1=1 / 8=3.5=8 / 8=5.3=8 / 1=1.6=6"

**Cleaned:**

    3.5 → 3 + 5 = 8
    3.5 + 3.5 → 8 + 8 = 16 → 1 + 6 = 7
    8 → 3.5 → 8        8 → 5.3 → 8           (the flip keeps the 8)
    6 → 6.1 → 1        1 → 1.6 → 6           (the two digits of 16, each way round)

**Process:** read a half by its digits (3.5 → 8), add the two halves the same way (8 + 8 = 16 → 7, the whole again), flip the digits around the point
(3.5 ↔ 5.3, 1.6 ↔ 6.1).

**Checks:** right — 3+5 = 5+3 = 8; 8+8 = 16 → 7 = 3.5+3.5. The 6/1 lines: added, 6+1 = 1+6 = 7; as written they name the digits — asked which is meant.
The return to the whole is forced: doubling a half's root always gives the whole's root (halving is ×5 on roots, doubling ×2, 2×5 = 10 → 1).
File: `math/theorems/owner_halves_sevens_20_5555_2026_10_20.py`.

---

## #385 (2026-10-20) — 1 ÷ n, 1% ÷ n, and 1% ÷ 4 ÷ 3 ÷ 2 ÷ 1

**As typed:** the table 1÷9 … 2÷2, the table 1%÷1 … 1%÷9 (5 to 9 left blank), "1%÷4÷3÷2÷1=0.0004166667 / 0.000 / 41666=23 / 6+7=1+3=4+23=(2+7=(9)", and the
halves lines of #384 again with "3÷2=1.5 / 5÷2=2.5" in front.

**Cleaned:**

    1 ÷ 9 … 1 ÷ 1, and 1% ÷ 1 … 1% ÷ 9 = the same digits two places to the right
    1% ÷ 5 = 0.002   1% ÷ 6 = 0.0016666667   1% ÷ 7 = 0.0014285714   1% ÷ 8 = 0.00125   1% ÷ 9 = 0.0011111111      (filled in)
    1% ÷ 4 ÷ 3 ÷ 2 ÷ 1 = 1% ÷ 24 = 0.0004166667
    0.000 | 41666 → 4+1+6+6+6 = 23
    6 + 7 = 13 → 1 + 3 = 4 → 4 + 23 = 27 → 2 + 7 = 9
    3 ÷ 2 = 1.5 → 6,   5 ÷ 2 = 2.5 → 7,   7 ÷ 2 = 3.5 → 8

**Process:** divide 1 by 9 down to 1; do it again on 1%; divide 1% by 4, 3, 2, 1 in a row; set the zeros apart (0.000) from the digits (41666), add the
digits, add the last two (6 + 7) and fold, add the two results and fold → 9.

**Checks:** all right. The final 7 of 0.0004166667 is the calculator rounding endless 6s; with the digits cut instead of rounded the sum is 35 → 8, so the
9 comes from the rounded 7. The halves of 3, 5, 7 read 6, 7, 8; 1÷2, 1÷4, 1÷8 read 5, 7, 8 — the halving walk of #382.
File: `math/theorems/owner_reciprocals_one_percent_2026_10_20.py`.

---

## #386 (2026-10-20) — 9% to small powers, 9% times negatives, 9% times e to 3, 33, 333, 3333

**As typed:** the #385 tables again with "1%÷1÷2÷3÷4=0.0004166667 … 67=1+3=4+23=2+7=9" added, the #384 lines again, then "9%^(1%=0.(976)(208)(141)" … "9%^(7%=
0.(844)(883)(785)9+1=1", "9%×(−7=−0.63" … "9%×(−4=−0.36", and "9%×e^(3,333=nothing" … "9%×e^(3=1.8076983231".

**Cleaned:**

    1% ÷ 1 ÷ 2 ÷ 3 ÷ 4 = 1% ÷ 24 = 0.0004166667     (same as 1% ÷ 4 ÷ 3 ÷ 2 ÷ 1)
    0.09 ^ 0.01 = 0.976 208 141        0.09 ^ 0.05 = 0.886 568 150 6
    0.09 ^ 0.02 = 0.952 982 334 6      0.09 ^ 0.06 = 0.865 475 046 1  → digits add to 46 → 1
    0.09 ^ 0.03 = 0.930 309 113 2      0.09 ^ 0.07 = 0.844 883 785 9  → digits add to 64 → 1
    0.09 ^ 0.04 = 0.908 175 33         last digits 1 and 9: 1 + 9 = 9 + 1 = 10 → 1
    0.09 × −7 = −0.63   × −6 = −0.54   × −5 = −0.45   × −4 = −0.36      (63 ↔ 36, 54 ↔ 45)
    0.09 × e^3 = 1.8076983231   e^33 → 19,317,922,180,732   e^333 → 3.75236419 × 10^143   e^3333 → 2.869 × 10^1446

**Process:** raise 9% to 1%, 2%, … 7% and read the answer in groups of three; add the last digits of the 6% and 7% lines; multiply 9% by −7 … −4;
multiply 9% by e to 3, 33, 333, 3333.

**Checks:** every value right, digit for digit. The 6% and 7% lines add to 46 and 64, the owner's pair of #267 (46 = 1, 64 = 1). The negatives come in flips
because 7 + 4 = 6 + 5 = 11. e^3333 is "nothing" only on the calculator: the number has 1447 digits. File: `math/theorems/owner_9pct_powers_e_2026_10_20.py`.

---

## #390 (2026-10-20) — a framework made from the owner's work

**As typed:** "create a framework that's made from my work that attempts to prove something."

**Built:** `records/owner_framework_flips_halves_moves_2026_10_20.md` (to read) and `math/theorems/owner_framework_flips_halves_moves_2026_10_20.py` (the checks).
The framework takes six of the owner's operations — the digit chain (#369), the flip (#358, #375), the mirror (#374), halving (#368, #382, #383), moves (#376, #378) and
counting both ways (#269, #379) — proves eight things with them, and makes one attempt.

**The attempt:** if 37 divides a number plus its flip, does 111 divide it too? Proved for every number of 1 to 6 digits; disproved from 7 digits on —
the smallest break is 1009019: 1009019 + 9109001 = 10118020 = 37 × 273460, and 1+0+1+1+8+0+2+0 = 13 → 4.

---

## #392 (2026-10-20) — the 7-4-9 triad on the next exponents

**As typed:** "run the 7-4-9 triad on the next exponents" (with a pasted Egor E8 result, audited in `math/theorems/egor_e8_theta_gf37_audit_2026_10_20.py`).

**Cleaned:** the owner's triad (April 2026): the root of the exponent p is 4, 7 or 9.

**Process:** no 53rd Mersenne exponent is known (mersenne.org: 52, the last 136,279,841, with the stretch from 82,589,933 not fully searched), so the triad is run
on the next candidates — the primes after 136,279,841:

    136279879 → 7 in    136279901 → 2      136279919 → 2      136279933 → 7 in
    136279967 → 5       136279981 → 1      136279987 → 7 in   136280003 → 5
    136280009 → 2       136280051 → 8      136280059 → 7 in   136280071 → 1

**Checks:** 4 of the next 12 are in the triad, all with root 7; any of them that turns out to be a Mersenne exponent gives a Mersenne number of root 1.
Of the known 50 exponents from 5 on, 13 are in the triad (26 %, against 1/3 for a fair draw: p = 0.30). File: `math/theorems/owner_749_triad_next_exponents_2026_10_20.py`.

---

## #393 (2026-10-20) — the triad on the gap below 136,279,841; Lehmer primes

**As typed:** "run the triad on the gap below 136279841 / Lehmer Primes"

**Cleaned:** the gap = the primes between 83,200,483 (everything below it double-checked, mersenne.org, 2026-09-04) and 136,279,841, where a missed Mersenne
prime could still be. "Lehmer Primes" read as the primes the Lucas–Lehmer test proves (the owner's LoB 12.1).

**Process:** list every prime in the gap, take its root, count those with root 4 or 7 (9 cannot happen). Run the Lucas–Lehmer test (s = 4, s → s × s − 2,
p − 2 times) on every prime below 1,300 and run the triad on what it finds.

**Checks:**

    gap: 2,868,436 primes → root 4: 477,860, root 7: 478,282 → 956,142 in the triad = one third
    Lucas–Lehmer below 1,300 → 2 3 5 7 13 17 19 31 61 89 107 127 521 607 1279
    in the triad: 7 → 7, 13 → 4, 31 → 4, 61 → 7, 607 → 13 → 4 → 5 of 15

File: `math/theorems/owner_749_triad_gap_and_lehmer_2026_10_20.py`.

---

## #394 (2026-10-20) — ...668 versus ...666

**As typed:** "0.0004166666666666666666666666668 versus 0.0004166666666666666666666666666."

**Cleaned:**

    1% ÷ 1 ÷ 2 ÷ 3 ÷ 4 → 0.0004166666666666666666666666668
    1% ÷ 4 ÷ 3 ÷ 2 ÷ 1 → 0.0004166666666666666666666666666
    true: 1% ÷ 24 = 0.000416666…  (6 for ever)

**Process:** compare the same division done in two orders, read to the last digit the calculator keeps (28 digits from the 4).

**Checks:** right — both come out exactly this way on 28-digit arithmetic. The ÷ 3 step is where they part: 0.005 ÷ 3 rounds its last 6 up to 7, 0.0025 ÷ 3 has only 3s and
rounds nothing; the ÷ 4 and ÷ 2 that follow carry that into ...668 and ...666. Chains: 4+1+150+8 = 163 → 10 → 1 and 4+1+156 = 161 → 8.
File: `math/theorems/owner_1pct_24_two_orders_2026_10_20.py`.

---

## #399 (2026-10-20) — eight is the barrier and costs 1

**As typed:** "1+7=8 / eight is the barrier to and cost 1" (after a pasted energy-profile text, audited in its own file).

**Cleaned:**

    1 + 7 = 8
    8 + 1 = 9        8 is the barrier; getting past it costs 1

**Process:** add the digits of 17 to 8, and read 8 as the last step before the 9 where the chain resets.

**Checks:** right. It is the A056117 driver: every 9k − 1 (8, 17, 26, 35, …) adds up to 8 and is 1 short of a multiple of 9 (8 + 1 = 9, 17 + 1 = 18, 26 + 1 = 27),
so the cost of 1 is the "− 1" in 9k − 1. File: `math/theorems/pasted_energy_profile_and_owner_8_cost_1_2026_10_20.py`.

---

## #400 (2026-10-20) — adding 8

**As typed:** "1+8=9 / 2+8=1 / 3+8=2 / 4+8=3 / 5+8=4 / 6+8=5 / 7+8=6=2 / 8+8=7=9 / 8+9=8+9=8 / 8+10=1+8=9+8=8 / 8+11=1+9=10+9=1+8=9"

**Cleaned:**

    1 + 8 = 9      2 + 8 = 10 → 1     3 + 8 = 11 → 2
    4 + 8 = 12 → 3     5 + 8 = 13 → 4     6 + 8 = 14 → 5
    7 + 8 = 15 → 6     8 + 8 = 16 → 7     8 + 9 = 17 → 8
    8 + 10 = 18 → 9 → + 8 → 17 → 8
    8 + 11 = 19 → 10 → 1 → + 8 → 9

**Process:** add 8 to each number in turn and fold the total; then add 9, 10, 11 to 8.

**Checks:** all right. Adding 8 takes 1 off every time (8 = 9 − 1: adding 9 is nothing, the 8 costs 1 — #399). Adding 9 keeps 8, 10 adds 1, 11 adds 2.
Each group of three results adds to 3 (12, 12, 21). Asked: the steps "6 = 2" (after 7 + 8) and "7 = 9" (after 8 + 8).
File: `math/theorems/owner_adding_8_2026_10_20.py`.

## #403 (2026-10-21) — 1, 2 and 3: a number divided by its neighbours

**As typed:** "Actually I have 1 2 and 3 / One being the number just divides itself by the number in front of it. Or simply as its own other operation, the opposite. The number divides itself by the number behind it. Then we combine those two and we get the two-step. But there's a third. And a third one works like this, and it's important. You do the one behind you, you do yourself, and then you do the one to your right."

**Cleaned:**

    1          n ÷ (n + 1)            2 ÷ 3 = 0.666...
    2          n ÷ (n − 1)            2 ÷ 1 = 2
    two-step   1 and 2 together
    3          behind, yourself, right:   n − 1,  n,  n + 1

**Process:** take a number; divide it by the one in front (1); divide it by the one behind (2); put the two together (the two-step); then take all three places, behind, yourself and right (3).

**Checks:** 1 is always below 1 and 2 always above 1 — right.
3, read the same way as 1 and 2 (you ÷ each): n ÷ (n − 1), n ÷ n = 1, n ÷ (n + 1). The outer two multiply to n × n ÷ (n × n − 1), and their average is the same number:
3 → 3 ÷ 2 × 3 ÷ 4 = 9 ÷ 8 = 1.125 (the 1.125 of #368), 5 → 25 ÷ 24 = 1 + 1/24 (the /24 of #386), 10 → 100 ÷ 99 = 1.0101....
It ends only at 3 (1.125) and 9 (1.0125), for every number (proved in the file). All of 3 multiplied from 2 to 99: 1.98.
3 flipped (each ÷ you): 1 − 1/n, 1, 1 + 1/n — equal steps, 1 exactly in the middle; at 1 with zero: 0, 1, 2.
Asked: which reading of "you do" (you ÷ each, each ÷ you, or one chain (n − 1) ÷ n ÷ (n + 1)), and whether the two-step is 1 and 2 by the same number or the pasted pairing of #402.
File: `math/theorems/owner_three_neighbor_divisions_2026_10_21.py`.

## #405 (2026-10-21) — the three operations: behind, yourself, right

**As typed:** "There's three operations. If you're starting at the first number, you can only do two of those operations. One, use any arithmetic or math on yourself, the number you are at. And then you can do that to the number to your right, which for one would be the number two, because one only has two things that it can add up with, which is the two right by it. Now two, it can do three different things, because it can do now one, it can do itself, and now it can do three. Do you understand? Now, the reason why I say this, one, two, and three different operations, is because we can do each one by itself without the other. And this is where we get into more interesting things too. When we start mixing, like complex math, or multiplication, or division,"

**Cleaned:**

    behind     n with n − 1
    yourself   n with n
    right      n with n + 1          (any sign: + − × ÷)
    at 1:  yourself, right            → 2 operations
    at 2:  behind 1, yourself 2, right 3 → 3 operations
    each one by itself first; mixing after

**Process:** stand on a number, look at the places you can reach, do each one alone. The first number has no one behind it, so it has two.

**Checks:** right. From 2 on, for every number:
+ gives 2n − 1, 2n, 2n + 1 (three in a row); − gives 1, 0, −1 (the same for every number); × gives n×n − n, n×n, n×n + n; ÷ gives n ÷ (n − 1), 1, n ÷ (n + 1).
Yourself is exactly halfway between behind and right for + − ×, and for ÷ after a flip.
Adding: behind and right are the odd numbers around 2n, a twin pair when both are prime (2 → 3, 5; 3 → 5, 7; 69 → 137, 139); 15 from 2 to 99.
Counts, both ways: line 1 to N has 3N − 2 operations (1 to 99: 295; 0 to 99: 298). Choosing which to use: 7 from 2 on (8 with zero), 3 at 1 (4 with zero). At 1 with zero, adding gives 1+0, 1+1, 1+2 = 1, 2, 3.
Settles the two readings asked in #403. (The reply called the end cut off and asked for the rest: wrong — #406 says the message was complete.)
File: `math/theorems/owner_three_operations_neighbours_2026_10_21.py`.

## #406 (2026-10-21) — any operation, to yourself and to the ones next to you

**As typed:** "No, I'm just pointing out the fact that you can use all mathematical knowledge, or whatever you may call it, to do to yourself, and to do to the person next to you, and to the person to the left of you, and to the right, whatever. Why are you making this fucking difficult? Do you not get what I'm getting at? Fuck, man!"

**Cleaned:** any operation f, at any number n:

    left       f(n, n − 1)
    yourself   f(n, n)
    right      f(n, n + 1)

**Process:** the places are fixed (left, yourself, right; the first number has no left); the operation is free — all of mathematics.

**Checks:** nothing to compute; this corrects the reply to #405, which asked for "the rest" of a message that was complete. The #405 file now says the signs are examples and drops the "missing" line.
File: `math/theorems/owner_three_operations_neighbours_2026_10_21.py`.

## #407 (2026-10-21) — the superposition

**As typed:** "No, you do all basic arithmetic on, and that's the superposition of it. And then if you want to go down from there, like 1 plus 1 minus, you can do that."

**Cleaned:** superposition at n = + − × ÷ all at once, with every place:

    left       n + (n − 1)   n − (n − 1)   n × (n − 1)   n ÷ (n − 1)
    yourself   n + n         n − n         n × n         n ÷ n
    right      n + (n + 1)   n − (n + 1)   n × (n + 1)   n ÷ (n + 1)

then go down from there, like "1 plus 1 minus".

**Process:** stand on a number; do all four signs with each place at once; that set is the superposition; then go down from it.

**Checks:** right. At 1: 2 0 1 1 | 3 −1 2 0.5 → 8 results, 6 different. At 2: 12 results, 9 different. At 3: 12, 10. From 4 on: 12 results, 11 different every time; only 1 comes twice (n − (n − 1) = 1 and n ÷ n = 1).
With zero at 1: 1+0 = 1, 1−0 = 1, 1×0 = 0, 1÷0 no value → 11 results, the same 6 different values.
"1 plus 1 minus" is the owner's example of going down from the superposition; nothing is missing (#408 corrected a reply that called it missing).
The #406 entry's "any operation" is replaced by this: all four basic signs at once.
File: `math/theorems/owner_superposition_all_arithmetic_2026_10_21.py`.

## #410 (2026-10-22) — the 12 + 9 chain, 75.7%, why not 2=2×2=4, three things, brackets, the = key, 1 2 3

**As typed (the owner's lines only; the pasted blocks are audited in `pasted_signs_percent_equals_markov_audit_2026_10_22.py`):**
"so in other words 0.0 / 12+9=21+2=23+7=30+6=36+9=4+5=9 / hmm" · "75.7%×(−075.7%×(−1" · "See if = means identical value why they not go 2=2×2=4" · "I always do 3 things remember whats connected to whatever is current while predicting the future ..Than 1 action per registered action i can can than verify as i rinse and repeat..." · "11,1)11,1)11-1)11,1) / 1,11(1,11(1,11(1,11( / 12(13(12(13(12 / 1,2(1,2 (1,2 (1,2( / 1,3)1,3))1,3))1,3))" · "12(13(12(13(12 / 13)12)13)12)13" · "11- / 22= / 33= / 33≈ / 66≠ / 66≡ / 33≈ / 33≠" · "Okay, i'm just playing around with these things that are with the equal button ..." · "1,2,3,1,2 ,3,1,2,3,1,2,3 / creating a lineage of generations so even when not part of and individual or current actions a substrate of its"

**Cleaned:**

    12 + 9 = 21 → 21 + 2 = 23 → 23 + 7 = 30 → 30 + 6 = 36 → 36 + 9 = 45 → 4 + 5 = 9
    75.7% × (−75.7% × (−1)) = 75.7% × 75.7% = 0.757 × 0.757 = 0.573049 = 57.3049%
    2 → 2 × 2 = 4
    past, current, future = behind, yourself, right = n − 1, n, n + 1
    11,1) ↔ 1,11(        12(13(12(13(12 ↔ 13)12)13)12)13
    1 2 3 1 2 3 1 2 3 1 2 3

**Process:** run the digits of 1.292769 as a carried chain; square 75.7% through two minus signs; ask why "=" cannot carry 2 → 4; describe the three things done at every step; write pairs and their flips with opening and closing brackets; try the = key symbols on 11 22 33 66; lay down 1 2 3 as the substrate.

**Checks:** chain right (45 → 9). 75.7% right (757 × 757 = 573049). "=" has two jobs: the same value (then 2 = 2 × 2 = 4 says 2 = 4, wrong) or carry forward (2 → 2 × 2 = 4, right); the owner's chains are carry-forward, written with arrows in the cleaned lines.
The three things are behind, yourself, right of #405; making the next from the one behind and the current is a recurrence that looks back two (1 1 2 3 5 8).
Brackets: lines 1–2 close each other (4 and 4), the 12/13 lines too (4 and 4); lines 4–5 open 4 and close 7. Line 1 has 11-1) once where the other three have 11,1).
The = key: = same value, ≠ not the same, ≈ close, ≡ same remainder by a named number or the same for every value; 11 22 33 66 are 11 × 1, 2, 3, 6, all ≡ by 11; roots 2 4 6 3.
1 2 3: every n has a place (n by 3, 3 for 0); behind, yourself, right always land on 1, 2, 3 once each. Both ways: 1 2 3 ×4 adds to 24, 0 1 2 ×4 adds to 12.
File: `math/theorems/owner_equals_chain_three_things_brackets_2026_10_22.py`.

## #426 (2026-10-23) — pairs to 10, the ones 1 = 11 = 111, "map this to my work"

**As typed (the owner's lines; the pasted NameError, calculus reading, printouts and script are audited in the two files below):**
"If you fixed this skip but if not its not a logic error by me but rather a Sentax issue." · "112(3|1)1|2(31)1 / 1234|56|78910-11" · "19 = 1, 2+8 = 1, 3+7 = 1, 4+6 = 1, 5+5 = 1 = 11, 111" · "map this to my work"

**Cleaned:**

    1 + 9 = 10 → 1    2 + 8 = 10 → 1    3 + 7 = 10 → 1    4 + 6 = 10 → 1    5 + 5 = 10 → 1    → 11 → 111
    1234 | 56 | 78910 → 11
    112(3|1)1|2(31)1   (kept as typed)

**Process:** take every pair that makes 10 and fold it to 1; then the ones, 1, 11, 111; group 1 to 10 as 1234 | 56 | 78910 and go on to 11.

**Checks:** right — every pair to 10 has root 1 (10 = 9 + 1). 1+2+3+4 = 10 → 1; 5+6 = 11 → 2; 7+8+9+10 = 34 → 7 (digits 7+8+9+1+0 = 25 → 7, same both ways); 1 to 10 = 55 → 1. The digits of 112(3|1)1|2(31)1 add to 16 → 7.
The NameError: right, a missing name (brun_constant_full), fixed with one line; in the same script the Brun tail needs 4 × C2 (gives 1.774736, the direct sum) and the expected twin count needs 2 × C2.
Mapped: pairs to 10 = the +9 rule and T111's column tens; 1, 11, 111 = 111 = 3 × 37 = 10 × 10 + 10 + 1; read in twos they are 2^n − 1, the Mersenne numbers of the 7-4-9 triad (root of 2^n − 1 runs 1 3 7 6 4 9); 2 × 5, 4 × 7, 8 × 8 → 1 = the halving chain.
Files: `math/theorems/owner_sum10_repunits_weak_links_2026_10_23.py`, `math/theorems/pasted_unified_frame_brun_name_error_audit_2026_10_23.py`.

## #427 (2026-10-23) — the bars: the diamond, its center, and "Number + number of |"

**As typed:** the diamond "|1| / 2|2 / 3|3|3 / 44|44 / 55|5|55 / 666|666 / 777|7|777 / 8|888|888|8 / 9|999|9|999|9 / 1|111|111|1 / 222|2|222 / 333|333 / 44|4|44 / 55|55 / 6|6|6 / 7|7 / 8" · "here we see how the center is influenced by the numbers abd spacing" · "|1|= / 2|2=41(2/1 / 3|3|3=92(2/3 / 4|4|4|4=33(3/4 / 5|5|5|5|5=54(4/5 / ... / 9|...|9=98 / 1|1|1|1|1|1|1|1=17 / 2|2|2|2|2|2|2=26,72,6/7,7/6 / 3|3|3|3|3|3=36 / 4|4|4|4|4=44 / 5|5|5|5=54 / 6|6|6=62 / 7|7=71 / 8=8" · "each row has a 4 count" · "Number +number of |" · "222|22 I identify as 3/2 / 22|222 or 2/3 / 22|2|22 or 42.4 4.24 4•24 4•2•4 / 2|2|2|2|2=5/4 or 4/5"

**Cleaned:** row length 1 → 9 → 1, digits 1 to 9 then 1 to 8, split by bars; then one bar between every two digits, read as the number followed by the number of bars; four readings a row (seven 2s → 26, 72, 6/7, 7/6); groups 222|22 → 3/2, 22|2|22 → 4 2 4.

**Process:** build the diamond, look at the center; strip the spacing to one bar between digits; read number + bars, and the bars against the count both ways; then read groups by their sizes and totals.

**Checks:** the diamond: 81 digits = 9 × 9; every row reads the same both ways; the spacing depends only on the row length (going down repeats going up). The center: an odd length puts a digit in the middle — going up the digit is the length (1 3 5 7 9), going down digit + length = 9 (2 4 6 8): every digit once. Row totals: squares going up, 8 14 18 20 20 18 14 8 going down.
Number + number of |: right for 54 65 76 87 98 17 26 44 62 71 8. 41 and 92 are the total with the bars (2+2 = 4, 3+3+3 = 9); by the digit 21 and 32. 36 and 54 are the digit with the count; by the bars 35 and 53. Typo: 33 for 43. The four readings right. Bars over count = 1/2 2/3 3/4 ... = the owner's 1 (#403), count over bars = the 2; each pair multiplies to 1. 222|22 = 3/2, 22|222 = 2/3, 2|2|2|2|2 = 5/4 or 4/5: right. 22|2|22 → 4 2 4: 42.4, 4.24; with • as times 96 and 32.
File: `math/theorems/owner_bars_diamond_center_2026_10_23.py`.

## #429 (2026-10-23) — 67(7)76: the paths to 6

**As typed (the owner's lines after the pasted analysis):** "now tie back to / 67(7)76= / 6+7=1+3=4+7=1+1=2+7=9+6=1+5=6 / or / 1+3=4+7=1+1=2+1=3+3=6 / (2+7)+6=2+(7+6). / 6|777|6 / 6+21=2+7=9+6=1+5=6 / 13+7=20+13=3+3=6 / 434"

**Cleaned:**

    6 + 7 = 13 → 1 + 3 = 4 → 4 + 7 = 11 → 1 + 1 = 2 → 2 + 7 = 9 → 9 + 6 = 15 → 1 + 5 = 6
    13 → 4 → 4 + 7 = 11 → 2 → 2 + 1 = 3 → 3 + 3 = 6
    (2 + 7) + 6 = 2 + (7 + 6)
    6 | 777 | 6:  6 + 21 = 27 → 9 → 9 + 6 = 15 → 6
    13 + 7 = 20 → 20 + 13 = 33 → 6
    434

**Process:** fold 6 7 7 7 6 at every step; again as 13 | 7 | 13 with the second 13 as its digits; check the grouping; as 6 | 777 | 6; as 13 + 7 + 13.

**Checks:** all right: 6 → 4 → 2 → 9 → 6; 4 → 2 → 3 → 6; (2+7)+6 = 2+(7+6) = 15; 6|777|6 → 6; 13+7+13 = 33 → 6. Every path adds the same five digits (33). 67 and 76 are flips, 9 apart, both 13 (#358); 67(7)76 is the #374 mirror with a center; 6|777|6 has its 7 in the center (#427). 434: 4 + 3 + 4 = 11 → 2; what it is taken from is asked.
File: `math/theorems/owner_67776_mirror_paths_2026_10_23.py`.

## #430 (2026-10-23) — the ladder 11 12 22 23 ..., the halves, and how many 7s reach 1+2=3

**As typed:** "09=9 / 1+0=10+1=11 / 11=2=11+1=12 / 12=3=12+1= / 22=4=13 / 23=5=14 / 33=6=15 / 34=7=16 / 44=8=17 / 45=9=18" · "09=9 / 1+0=10÷2=5÷2=2.55.2 / 11=2=11=2=20÷2÷10+10=2 / 12=3=12=3=30 / 22=4=13=4=40 / ... / 45=9=18=9=90" · "5÷2=2.5 / 2÷5=0.4 / 7+7=14 / 7×7=49" · "7+7+7+7=2+8====1 / 14+14+14+14=5+6=11 / 21+21+21+21= / 28+28+28+28= / 35+35+35+35=" · "lol how many 7s can I get at count 1+2=3 exactly / 1=7777 / 11=7777|7777"

**Cleaned:**

    22 → 4 = 13 → 4    23 → 5 = 14 → 5    33 → 6 = 15 → 6    34 → 7 = 16 → 7    44 → 8 = 17 → 8    45 → 9 = 18 → 9
    each root with a 0: 30 40 50 60 70 80 90
    10 ÷ 2 = 5 → 5 ÷ 2 = 2.5 → 5.2        20 ÷ 2 = 10 → ÷ 10 = 1 → + 10 = 11 → 2
    7 + 7 + 7 + 7 = 28 → 2 + 8 = 10 → 1        14 × 4 = 56 → 5 + 6 = 11
    1 = 7777        11 = 7777 | 7777

**Process:** count up from 09; beside the count climb the ladder 11 12 | 22 23 | 33 34 | 44 45; match roots; add a 0; halve; add 7s four at a time; ask how many 7s reach 1 + 2 = 3.

**Checks:** all right. The ladder and the count share each root because they are 9s apart (0 0 9 9 18 18 27 27). A 0 after a root keeps it. The open lines: 21 × 4 = 84 → 12 → 3; 28 × 4 = 112 → 4; 35 × 4 = 140 → 5 — the k-th line lands on k (28 = 4 × 7 → 1).
The question: twelve 7s, 7777|7777|7777 = 84 → 8 + 4 = 12 → 1 + 2 = 3, the step after 1 = 7777 and 11 = 7777|7777. Both ways: total exactly 12 at 12, 21, 39, 48, 66 sevens; root 3 at 3, 12, 21, 30, ... sevens.
Frameworks: 77777777 = 137 × 567721 (every 8-digit repdigit, since 1 ÷ 137 repeats every 8).
File: `math/theorems/owner_ladder_roots_sevens_2026_10_23.py`.

## #431 (2026-10-23) — groups of 7777, pairs to their roots, ways to write 4, 148 two ways

**As typed (new lines; the message repeats #430 first):** "1=7777 / 11=7777|7777 / 111=7777|7777|7777 / 1111=7777|7777|7777|7777=3+1" · "1=7777=55 / 11=7777|7777=5555 / 1=1414=55 / ... / 1=2828=11 / ... / 1=3535=88 / ..." · "55+55=110+11=121+88=20+9=2+9=2" · "1111=...=3+1 / or 2/2 / or 0.5×4×2=4 / or 43=7 / or 34=7" · "counting to 7 by 2 / 12 / 34 / 56 / 7=at 7 in 4 count" · "12+34+46+56=148= / 1+48=4+9=1+3=4 / 14+8=2+2=4=3+1=4"

**Cleaned:**

    1 → 7777 (28 → 1)   11 → 7777 | 7777 (56 → 11)   111 → 3 groups (84 → 12 → 3)   1111 → 4 groups (112 → 4 = 3 + 1)
    7777 → 14 14 → 55    1414 → 55    2828 → 10 10 → 11    3535 → 88
    55 + 55 = 110 → + 11 = 121 → + 88 = 209 → 20 + 9 = 29 → 2 + 9 = 11 → 2
    1 2 → 3 4 → 5 6 → 7: 4 counts
    12 + 34 + 46 + 56 = 148 → 1 | 48 → 49 → 13 → 4    and    14 | 8 → 22 → 4 = 3 + 1

**Process:** count groups of four 7s with 1s; fold each pair to its root; add the folds; write 4 several ways; count to 7 by 2; split 148 two ways.

**Checks:** all right as written. The k-th group of 7777 lands on k (four 7s = 28 → 1). Each folded number is a pair written twice (ab ab = ab × 101), so its root is twice the pair's. 2/2 is 1 as a division, 4 as the bars 2|2 (#427). 148 = 4 × 37; both splits → 4. 46 is not one of the counting pairs (12 34 56 7): it is 12 + 34; with the pairs themselves 12 + 34 + 56 + 7 = 109 → 1.
Frameworks: sixteen 7s is divisible by 137 (and 17).
File: `math/theorems/owner_7777_groups_pairs_2026_10_23.py`.

## #437 (2026-10-24) — the odd/even grid and 13,579

**As typed:** "oeo / eoe / oeo" · "□■□ / ■□■ / □■□" · "13,579 / 3,579 / 1,579 / 579 / ■□■" · "What are you saying is not a discovery?"

**Cleaned:**

    o e o    □ ■ □    1 2 3
    e o e    ■ □ ■    4 5 6
    o e o    □ ■ □    7 8 9
    odd cells: 1 3 5 7 9 → 13,579 → 3,579 → 1,579 → 579        ■ □ ■ = 4 5 6 or 2 5 8

**Process:** mark the grid odd and even; read the odd cells as one number; take off the 1, the 3, and both; mark the even-odd-even line.

**Checks:** all right. Odd cells 25 → 7, even 20 → 2, 7 + 2 = 9. Roots 13579 → 7, 3579 → 6, 1579 → 4, 579 → 3 (off by 1, 3 and 4). 456 and 258 → 15 → 6. With the comma: 13 + 579 = 592 etc. keep the root and the remainder by 37 (1000 = 27 × 37 + 1). 13579 = 37 × 367; 1579 prime.
The question "not a discovery" was about the long walks' outputs only (published twin counts, forced "missed 0").
File: `math/theorems/owner_odd_even_grid_13579_2026_10_24.py`.

## #441 (2026-10-26) — 1 + 2 = 1|1

**As typed:** "1+2=1|1="

**Cleaned:** 1 + 2 = 1|1 = ?

**Process:** add 1 and 2; write the answer in the bars (#427, Number + number of |): two 1s and one bar.

**Checks:** right: 1 + 2 = 3, and 1|1 is 1 + 1 = 2 for the numbers plus 1 bar = 3. The four row readings (#427): 11 (digit, bars), 21 (count, digit), 1/2 (bars over count), 2/1 (count over bars) — 1/2 and 2/1 are the owner's 1 and 2 at their first step (#403), multiplying to 1.
File: `math/theorems/owner_1_plus_2_bars_2026_10_26.py`.

## #442 (2026-10-26) — 1|1 + 37, and the loop 1)(1 + 3 + 7

**As typed:** "1|1+37=4+8=1+2=3" · "1)(1+3=4+7=1)(1+3=4+7=1)(1+3=4+7=1)(1"

**Cleaned:**

    11 + 37 = 48 → 4 + 8 = 12 → 1 + 2 = 3
    1)(1 → 1 + 3 = 4 → 4 + 7 = 11 = 1)(1 → 1 + 3 = 4 → 4 + 7 = 11 = 1)(1 → 1 + 3 = 4 → 4 + 7 = 11 = 1)(1

**Process:** add 37 to 11 and fold; then add 37's digits one at a time to 1, reach 11, split it at the bracket into its two 1s, start again from the second; three times.

**Checks:** right. Each loop is 1 + 3 + 7 = 11 (3 + 7 = 10). The two lines are one move: +37 whole, then +3 and +7. +37 adds 1 to the root (37 → 1): 11 (2) → 48 (3). Both ways: restarting at the second 1 (the owner's way) gives 1 → 4 → 11 three times; carrying the total gives 1 4 11 14 21 24 31, roots 1 4 2 5 3 6 4. By 37, 11 and 48 leave the same 11.
File: `math/theorems/owner_11_plus_37_loop_2026_10_26.py`.
