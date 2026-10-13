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
