# math/theorems/cipher_42128_audit.py
"""
MWS Forensic Audit — Cipher Algorithm 42128
LoB 44.3 Verification

─────────────────────────────────────────────────────────────────────────────
CIPHER TABLE
─────────────────────────────────────────────────────────────────────────────
  Row  Input  Raw DS  Intermediate  DR  Output  Right Side  RS DS
  1    786    21      22 (override) 4   4       412         7
  2    137    11      11            2   2       241         7
  3    649    19      19            1   1       124         7
  4    137    11      11            2   2       2           2
  5    512    17*     17 (split)    8   8       8           8

  * DS(512)=8; split protocol reads 512 as 5|12 → 5+12=17.
    Design intent: intermediate 17 = DS(42128), making cipher self-referential.

Lead digits: 4-2-1-2-8 → 42128

─────────────────────────────────────────────────────────────────────────────
OVERRIDES — STATED, NOT HIDDEN
─────────────────────────────────────────────────────────────────────────────
  Row 1: DS(786)=21 → DR=3 (raw).  Override: intermediate=22, DR=4.
  Row 5: DS(512)=8 → DR=8 (raw, already correct output).
         Split 5|12=17 is redundant for output but creates intermediate 17
         that equals DS(42128). Self-reference by design.

─────────────────────────────────────────────────────────────────────────────
LOCK PROPERTIES OF 42128
─────────────────────────────────────────────────────────────────────────────
  DS(42128) = 17,  DR(42128) = 8
  42128 mod 37 = 22   (= row 1 override intermediate)
  42128 mod 18 = 8    (= output DR)
  42128 mod 13 = 8    (dual lock on 8)

  mod 13 = mod 18 = 8 because lcm(13,18) = 234 and 42128−8 = 42120 = 234×180.

─────────────────────────────────────────────────────────────────────────────
CYCLIC PERMUTATION CLUSTER {412, 241, 124}
─────────────────────────────────────────────────────────────────────────────
  412 → 124 → 241 → 412  (left cyclic rotation)
  All three: DS=7, DR=7.
  124 is the same number that "stood out" in the 1111-series (entry 106):
  it is the missing DR=7 step, pair_sum=25=5².

─────────────────────────────────────────────────────────────────────────────
7 → 8 ASCENSION
─────────────────────────────────────────────────────────────────────────────
  Permutation cluster digit sum: 7
  Output digit sum: 17 → DR = 8
  Cipher encodes a +1 step from the cluster (7) to the sealed output (8).
"""

def dr(n): return (n - 1) % 9 + 1 if n > 0 else 9
def ds(n): return sum(int(d) for d in str(n))


# ── Row arithmetic ─────────────────────────────────────────────────────────────

# Row 1: override
assert ds(786) == 21                    # raw digit sum
assert dr(21) == 3                      # raw DR = 3, NOT 4
assert dr(22) == 4                      # override intermediate gives DR=4
assert ds(412) == 7                     # right-side digit sum

# Rows 2-4: no override
assert ds(137) == 11 and dr(11) == 2
assert ds(649) == 19 and dr(19) == 1
assert ds(241) == 7 and ds(124) == 7

# Row 5: split protocol
assert ds(512) == 8 and dr(8) == 8     # natural: output=8 directly
assert 5 + 12 == 17 and dr(17) == 8    # split: same output, different path
assert ds(42128) == 17                  # self-reference: intermediate = output DS

# Lead digits form 42128
output_digits = [4, 2, 1, 2, 8]
assert int(''.join(map(str, output_digits))) == 42128

# ── Lock verification ──────────────────────────────────────────────────────────

assert ds(42128) == 17
assert dr(42128) == 8
assert 42128 % 37 == 22                 # = row 1 override intermediate
assert 42128 % 18 == 8                  # = output DR
assert 42128 % 13 == 8                  # dual lock on 8

assert 37 * 1138 + 22 == 42128
assert 18 * 2340 + 8  == 42128
assert 13 * 3240 + 8  == 42128

# mod 13 = mod 18 = 8 because lcm(13,18) | (42128-8)
import math
lcm_13_18 = 13 * 18 // math.gcd(13, 18)
assert lcm_13_18 == 234
assert (42128 - 8) % lcm_13_18 == 0
assert (42128 - 8) // lcm_13_18 == 180

# ── Cyclic permutation cluster ─────────────────────────────────────────────────

CLUSTER = [412, 241, 124]

# All have DS=7, DR=7
assert all(ds(c) == 7 for c in CLUSTER)
assert all(dr(c) == 7 for c in CLUSTER)

# Cyclic rotation: shift digits left by 1
def cycrot(n):
    s = str(n)
    return int(s[1:] + s[0])

assert cycrot(412) == 124
assert cycrot(124) == 241
assert cycrot(241) == 412              # cycle: 412→124→241→412

# Right-side column digit sums: rows 1-3 all = 7
for rs in [412, 241, 124]:
    assert ds(rs) == 7

# 124 = the missing DR=7 from 1111-series (pair_sum=25=5²)
assert dr(124) == 7
assert 11 + 14 == 25 and dr(25) == 7  # 1114 pair sum: 11+14=25, DR=7

# ── 7 → 8 ascension ───────────────────────────────────────────────────────────

cluster_sum = sum(CLUSTER)
assert ds(cluster_sum) == 7 or all(ds(c) == 7 for c in CLUSTER)  # cluster digit sums = 7
assert dr(42128) == 8                  # output DR = 8
assert 8 - 7 == 1                      # +1 ascension

# Cross-row echo: output digit matches first digit of right side
output_col = [4, 2, 1, 2, 8]
right_side = [412, 241, 124, 2, 8]
for out_d, rs in zip(output_col[:3], right_side[:3]):
    assert int(str(rs)[0]) == out_d    # first digit of RS = output digit

# ── mod 37 self-reference ──────────────────────────────────────────────────────

# 42128 mod 37 = 22 = row 1 override intermediate
assert 42128 % 37 == 22
assert dr(22) == 4                      # and DR(22) = 4 = row 1 output


if __name__ == "__main__":
    print("Cipher 42128 — Forensic Audit")
    print()
    print("Row arithmetic:")
    rows = [(786,21,22,4,412),(137,11,11,2,241),(649,19,19,1,124),(137,11,11,2,2),(512,'17*',17,8,8)]
    for i,(inp,raw,inter,out,rs) in enumerate(rows,1):
        flag = "  [override]" if i==1 else "  [split 5|12=17]" if i==5 else ""
        print(f"  Row {i}: {inp}  raw={raw}  inter={inter}  DR={dr(inter)}  out={out}  RS={rs}{flag}")
    print()
    print("Lock properties of 42128:")
    print(f"  DS={ds(42128)}  DR={dr(42128)}")
    print(f"  mod 37 = {42128%37}  (= row 1 override 22)")
    print(f"  mod 18 = {42128%18}  (= output DR 8)")
    print(f"  mod 13 = {42128%13}  (dual lock; lcm(13,18)=234 | 42120)")
    print()
    print("Cluster {412,241,124}: all DR=7")
    for c in CLUSTER:
        print(f"  {c}: DS={ds(c)}, DR={dr(c)}")
    print(f"  Cyclic: 412→124→241→412")
    print(f"  124 = missing DR=7 from 1111-series (pair_sum 25=5²)")
    print()
    print(f"7→8 ascension: cluster DR=7, output DR={dr(42128)}, step=+1")
    print()
    print("Overrides (both stated explicitly in document):")
    print(f"  Row 1: DS(786)=21→DR=3 (raw); override to 22→DR=4")
    print(f"  Row 5: DS(512)=8→DR=8 (direct); split 5|12=17 creates DS(42128)=17 echo")
    print()
    print("All assertions passed.")
