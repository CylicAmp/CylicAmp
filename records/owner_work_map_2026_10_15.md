# How your work fits together -- October lines and your own earlier files

Michael Warren Song's work. Each row: your recent line (owner_work #n), the earlier file of yours it
continues, and what is the same. Found by searching the repository and confirmed by running the files
(2026-10-14/15). "Forced" means the match would happen for any numbers -- recorded, but not a discovery.

## Counting the commas (#265-#269)

| Your October line | Your earlier work | What is the same |
|---|---|---|
| #265 "or 11323 count commas with out" | `math/theorems/zero_comma_label_system.py` (2026-07-04 import) | Your July zero-comma labels number each comma among the commas and each group as 3: "1323" (2 commas), "13233343" (4 commas). Your October "with out" count is 1 followed by the July label: 11323, and for 4 commas 113233343 -- digit for digit. **The "with out" count is your own July label system.** |
| #270 "0=(o=1)", "00=eo" -- the "own category" question of #269 | `math/theorems/odd_perfect_zero_system.py` (2026-07-04) | July marks each group odd or even with C for the comma: 0,000,000 is O C O C O, the same five pieces as 1 1 3 2 3. #270's o / eo is that marking. |
| #265 "0,000 / 00,000 / 000,000"; #268 "0, / 00, / 000," | `math/theorems/triangular_partition_audit.py` (2026-07-04) | The same 0 / 00 / 000 rows with the same before-comma / after-comma split. |
| #269 "123 / 112233", "11-22-33" | `math/theorems/concatenation_123_repunit.py` (T77, 2026-07-29) | 112233 is your T77's N_2 (each digit of 123 written twice), split 11 / 22 / 33. T77 proves N_n = 12 mod 37 whenever 3 does not divide n -- so 112233 = 123 = 12 (mod 37) is your July theorem. |

## Doubling, halving and 181 (#263, #264, #270)

| Your October line | Your earlier work | What is the same |
|---|---|---|
| #270 "1248 / 751", "AT THE 7 NUMBER I GET MY SECOND 1" | `math/theorems/cipher_123_1234.py` (2026-07-16) | Trinity {3,6,9} / doubling {1,2,4,5,7,8}, unity pairs (3,7), (6,4), (9,1) -- all reappear in #267-#270 (`continuity_cipher_123_to_2026_10_13.py`). |
| #270 "124 / 875", 124 + 875 = 999 | `math/theorems/digits_137_and_7.py`, your SPLIT-COMPLEMENT THEOREM: 142 + 857 = 999 | The same law: a 6-step cycle whose half-way step is -1 splits into halves adding to 999. 124 + 875 = 248 + 751 = 142 + 857 = 999 (forced by 2^3 = -1 mod 9, as 10^3 = -1 mod 7). |
| #270 "1248 / 751" | `math/theorems/prime_dr_append_layer3_audit.py` (July) | Your July append tables write the doubling cycle digit by digit: 11 -> 112 -> 1124 -> 11248 (= 2^4 x 19 x 37, in the July table). |
| #270 "see that 181?" | your line in #227 (2026-10-12): "1+1=2÷11(0.181\|818\|181\|8)" | The same 1, 8, 1, 8 run: 2/11 = 0.181818..., and column 1 of 124 / 875 / 1. Different operations, both alternate by the mirror x -> 9 - x. |
| #263 halving strings; #270 "10÷2=5", "1÷2=0.5+0.5=1" | `math/theorems/five_six_orbit.py` (2026-07-26): "11÷2 = 5.5 ... flanking 5 and 6", HALVING CHAIN | The #263 halving run on 11 gives levels [6,5], [3,3,3,2] -- your July chain 11 -> {5,6}, 5 -> {2,3}, 6 -> 3. |
| #270 "OEO / 123 / 246" | `math/theorems/theorem_215_246_equals_2x123_gf37.py` | 246 = 2 x 123 digit by digit, roots 6 -> 3. |

## Grids and both-ways pairs (#259-#262)

| Your October line | Your earlier work | What is the same |
|---|---|---|
| #259 "(3x7=12 and 21)" | your line in #227 (2026-10-12): "3x7=12 and 21 at different scales" | Word for word. |
| #259 "(2)2(2)2(2)=3 twos or 2 thress" (typo: thress) | `math/theorems/theorem_230_six_manifold.py` (2026-08-27): "Three twos: 2+2+2 = 6" | The same phrase and operation. |
| #259 bar grid "1---\|23 / 45--\|6" | `math/theorems/theorem_231_236_permutations.py` (2026-08-27), {2, 3, 6} permutations | The same digit set {2,3,6} and the same 23 \| 6 split. |
| #261 "159-7 ... 7-951" | `math/theorems/theorem_320_ag23_lift_geometry_gf37.py` (2026-09-14), grid 7 159 483 | The block's left parts are grid 7's rows. |

## The drip cycle and the power tower

| Your recent work | Your earlier work | What is the same |
|---|---|---|
| drip cycle on 246 (#252) | `math/theorems/theorem_129_digit_rotation_orbit.py` (2026-08-05) | Rotation of 246 is the 137-map: {246, 624, 462} -> {24, 32, 18}, {642, 426, 264} -> {13, 19, 5}. |
| 1/4 power tower (#257) | `math/theorems/nine_tower_dr_invariant.py` (2026-07-24) | Same recursion b^T. Your integer towers (3, 6, 9) lock to root 9 by height 2; the 1/4 tower never locks -- it alternates 4 and 5 (0.4999... / 0.5000...). |
| drip cycle on 137's digits | the Phi_3(137) primes 7, 37, 73 and 13 | All of them appear in the drip of 137. Among primes below 100,000, 137 is the only one whose Phi_3 primes all lie in its own drip. Recorded, not claimed (base-10 rendering). |

## Phi_3 / Phi_12 at 137 (#241)

| | Your earlier work | What is the same |
|---|---|---|
| every number in the #241 handoff | `math/theorems/phi12_order_and_cut_string_link_gf37.py` (2026-09-12) and `reference/cut_table_113115117167.py` (2026-09-11) | The handoff is the portable copy of your own files. |
| the two corrections in `phi3_phi12_handoff_audit_2026_10_13.py` (six orders, CODATA 2022) | `math/theorems/one_over_137_framework.md`, your note of 2026-09-19 | **You made both corrections first**: 137.035999177(21) and 1.71 x 10^6 standard deviations. |
| 1/137 period 8, block 00729927 | `math/theorems/digits_137_and_7.py` (July) | Your July result: 0072 + 9927 = 9999, 10^4 + 1 = 73 x 137. |

## Collatz

| | Your earlier work | What is the same |
|---|---|---|
| Thread 2: the twin centres' orbits top out at 3077 | `collatz_v2_equidistribution.py` (2026-07-04), Syracuse orbit of 27 | 3077 is the top of the orbit of 27; all five twin-centre orbits join it. |
| T271 fixed point 18 of 3x+1 mod 37 | LoB 20 gate 18 (2026-04-23), `cascade_constants_audit.py` | The same 18 = -2^-1 mod 37. |
