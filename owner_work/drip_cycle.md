# Drip cycle (owner's term)

## The owner's example, verbatim (owner_work #228, 2026-10-12)

```
1
12

1
21

2
12

2
21
```

"That right there is just a fucking small example. That is not all of them. Find all of them."

## How it is run (`drip_cycle.py`)

The shape of the example: each digit of the number set against every ordering of the digits.
Run at every length -- every pair of the number's digits (both orders, as in the example) and
every ordering of all of its digits -- and every number produced goes through the frameworks.

```
python3 drip_cycle.py 246
```

## 246 (owner_work #252, 2026-10-13: "run my full drip cycle on 246")

```
===== DRIP CYCLE: 246 =====
--- length 2: 12 drip lines over 6 arrangements ---
2
24

2
42

4
24

4
42

2
26

2
62

6
26

6
62

4
46

4
64

6
46

6
64

     n mod37    orbit  dr  prime  twin    SG  x137%37  %137
    24    24     SEED   6  False False False       32    24
    42     5  CAS_EXT   6  False False False       19    42
    26    26       IC   8  False False False       10    26
    62    25  SA_ST_B   8  False False False       21    62
    46     9  SA_ST_A   1  False False False       12    46
    64    27    NEG_H   1  False False False       36    64

--- length 3: 18 drip lines over 6 arrangements ---
2
246

2
264

2
426

2
462

2
624

2
642

4
246

4
264

4
426

4
462

4
624

4
642

6
246

6
264

6
426

6
462

6
624

6
642

     n mod37    orbit  dr  prime  twin    SG  x137%37  %137
   246    24     SEED   3  False False False       32   109
   264     5  CAS_EXT   3  False False False       19   127
   426    19  CAS_EXT   3  False False False       13    15
   462    18     SEED   3  False False False       24    51
   624    32     SEED   3  False False False       18    76
   642    13  CAS_EXT   3  False False False        5    94

```

### What the run shows

- **The six orderings of 246 split three and three.** 246, 462, 624 are SEED; 264, 426, 642 are
  CAS_EXT, the antipodal orbit. Both halves are forced:
  - a cyclic rotation of a 3-digit number multiplies it by 10 mod 37 (1000 = 1 mod 37), and 10 is
    in IC, so rotation never leaves the orbit;
  - the digits 2, 4, 6 are in arithmetic progression, so n + reverse(n) = 222 x (middle digit)
    = 6 x 37 x 4: 246 + 642 = 888 = 24 x 37. The reversal is the negative mod 37, which is the
    antipodal orbit. (888 as a SEAM value is already in theorem_190, Axiom 6.)
- **Pairs:** 24 SEED / 42 CAS_EXT are antipodal too -- forced because 4 = 2 x 2
  (42 + 26 x 24 = 666 = 18 x 37). 26 IC / 62 SA_ST_B and 46 SA_ST_A / 64 NEG_H are not.
- All six 3-digit orderings have digital root 3 (2+4+6 = 12); the pairs have 6 (24, 42),
  8 (26, 62), 1 (46, 64). Every ordering is even, so none is prime, twin or Sophie Germain.

## 0.25 (owner_work #255, 2026-10-13)

### The owner's lines, verbatim

```
run my full drip cycle on 0.25


01
00=23/6
0=+1
00=23/6
0=+1
00=23/6
0=+1
00=23/6



0
00=36
0+1 
00=66
0+1
00=99
0+1=
12


6+1=7
6+1=7
6+1=7
9+3=12+21=(3+4=7)

36+66=102
9+12=21
```

### The drip cycle on 0.25 (digits as written: 0, 2, 5)

```
===== DRIP CYCLE: 0.25 =====
--- length 2: 12 drip lines over 6 arrangements ---
0
02

0
20

2
02

2
20

0
05

0
50

5
05

5
50

2
25

2
52

5
25

5
52

as written      n mod37    orbit  dr  prime  twin    SG  x137%37  %137
        02      2     2   DARK_A   2   True False  True       15     2
        20     20    20   DARK_A   2  False False False        2    20
        05      5     5  CAS_EXT   5   True  True  True       19     5
        50     50    13  CAS_EXT   5  False False False        5    50
        25     25    25  SA_ST_B   7  False False False       21    25
        52     52    15   DARK_A   7  False False False       20    52

--- length 3: 18 drip lines over 6 arrangements ---
0
025

0
052

0
205

0
250

0
502

0
520

2
025

2
052

2
205

2
250

2
502

2
520

5
025

5
052

5
205

5
250

5
502

5
520

as written      n mod37    orbit  dr  prime  twin    SG  x137%37  %137
       025     25    25  SA_ST_B   7  False False False       21    25
       052     52    15   DARK_A   7  False False False       20    52
       205    205    20   DARK_A   7  False False False        2    68
       250    250    28  SA_ST_B   7  False False False       25   113
       502    502    21  SA_ST_B   7  False False False       28    91
       520    520     2   DARK_A   7  False False False       15   109

```

- Every 3-digit ordering has digital root 7 (0 + 2 + 5 = 7) -- the 7 of the owner's
  `6+1=7` lines and of 0.25 itself (2 + 5 = 7).
- The orderings split SA_ST_B {025, 250, 502} (rotations of each other: x10 mod 37) and
  DARK_A {052, 205, 520} (rotations of the reversal). Unlike 246, the reversal is not the
  opposite orbit: 0, 2, 5 are not in equal steps (025 + 520 = 545, not a multiple of 37).
- 02 -> 2 and 05 -> 5 are prime: 2 is a Sophie Germain prime; 5 is a twin and Sophie Germain prime.

### The owner's equations, checked

| line | holds |
|---|---|
| `6+1=7` (three times) | yes |
| `9+3=12` | yes |
| `12+21` (in `9+3=12+21=`) | = 33 |
| `(3+4=7)` | yes |
| `36+66=102` | yes |
| `9+12=21` | yes -- the digit sums of 36 and 66; and 1+0+2 = 3 = 2+1 |

Open: `00=23/6` -- 23 divided by 6 (3.8333...), or 2 x 3 = 6, which then gives the `6+1=7`
lines? Asked of the owner 2026-10-13.

### Frameworks on the owner's numbers

- 23 and 6 are in the same orbit, TESLA {6, 8, 23}: under the 137-map 6 -> 8 -> 23.
  23 is a Sophie Germain prime and a safe prime.
- SA_ST_B {21, 25, 28} holds 25 (0.25's digits), 1/4 (= 28 mod 37), 99 (= 25), 21, and 102
  (= 28): 36 + 66 = 102 lands on 1/4 mod 37 (102 x 4 = 408 = 11 x 37 + 1).
- 7: D7, twin prime, safe prime. 3: C3, twin, Sophie Germain. 36: NEG_H. 66: C9 (29).
  12: SA_ST_A. 9: SA_ST_A. 33: D7. 4: C3. 1: IC.
- Full six-register and GF(37) run: owner_work/plugged/2026-10-13T171551Z.txt.
