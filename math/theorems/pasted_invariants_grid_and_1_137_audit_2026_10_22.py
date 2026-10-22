# CLASS: AUDIT
"""
The pasted "exact arithmetic and algebraic check of those invariants" (dual digital-root cycles,
a Manhattan spiral, concatenated rows and 37, a mod 11 signature, the cross differences 441 and
529, the order of 33 mod 37) and the pasted 1/137 block (period 00729927, Midy, the fine-structure
constant) -- owner_work #411, 2026-10-22. Audit on arrival.

THE PASTE: text from another tool, relayed by the owner. The first block appears twice, word for
word. Nothing below puts a claim of the paste in the owner's mouth.

PRIOR ART: 1/137 = 0.00729927..., 137 x 729927 = 99999999 -- repetend_998001_audit_2026_10_19.py,
digits_137_and_7.py, one_over_137_framework.md. 33 = 2^20 by 37 -- CLAUDE.md, generator walk.

THE GRID the first block checks is not in the paste and not in owner_work/. Three checks need it:
the Manhattan distances 15 13 11 9 7 5 3 1, the "chain" whose roots are 9 3 6, and what the
"cross differences" are.

RIGHT (re-run):
  9 + 1 = 3 + 7 = 6 + 4 = 10 -> 1
  N = 10000a + 100(a + d) + (a + 2d) = 10101a + 102d
  111111 = 37 x 3003;  1000 = 27 x 37 + 1, so 10^4 leaves 10 and 10^5 leaves 26 by 37
  (1, -1, 0) adds to 0, so a row with those column remainders adds to a multiple of 11
  441 = 21 x 21, 529 = 23 x 23 (21 and 23 are consecutive odd numbers; 529 - 441 = 88)
  no number has order 37 by 37 (orders divide 36); a primitive root has order 36
  33 leaves -4: (-4)^2 = 16, (-4)^3 = -64 -> 10, (-4)^4 = 256 -> 34 = -3, (-4)^9 -> 1
  -> 33 has order 9 (because (-4)^9 -> 1 and (-4)^3 -> 10, not 1); 33 = 2^20 by 37, 36 / 4 = 9
  stepping by 33 reaches all 37 remainders (33 and 37 share no factor)
  1/137 = 0.00729927 00729927 ... loop of 8
  0072 + 9927 = 9999 (0+9, 0+9, 7+2, 2+7); 0+0+7+2+9+9+2+7 = 36 -> 9; 72 + 27 = 99
  729 = 9 x 9 x 9 = 27 x 27

WRONG:
  1. "Duality / 9-Complements": the pairs add to 10 (9+1, 3+7, 6+4), so they are 10-complements;
     9-complements add to 9.
     And the two cycles are forced by the step: a step of 33 moves the root by 6, so the roots go
     round three values of one kind by 3 -- {3, 6, 9}, {1, 4, 7} or {2, 5, 8} -- whatever the start.
  2. "projecting every concatenated row to the identical residue class N ≡ 22": the 10101a part
     always drops out (10101 = 37 x 273), but what is left depends on the steps inside the row.
     For a row a, a + p, a + q the remainder by 37 is 26 x p + q, for every a.
       uniform step d (the paste's own formula): 102d -> 28 x d by 37; this is 22 only for d = 14
         12 13 14 -> 121314 -> 28, not 22
         10 24 38 -> 102438 -> 22
       steps 9 and 10 (rows 1 10 11, 12 21 22, ... 89 98 99): 26 x 9 + 10 = 244 = 6 x 37 + 22 -> 22
     So "every row -> 22" is right only for rows whose inner steps give 26p + q -> 22; the paste's
     uniform-step algebra does not give it.
  3. "They agree to four significant figures (0.00729...)": 0.00729 is three significant figures
     (7, 2, 9). The fourth differs: 1/137 = 0.0072992..., alpha = 0.0072973... (9 against 7).
  4. "the high-precision CODATA value 137.035999084": that is the 2018 value. NIST's current
     value (2022 CODATA, read 2026-10-22 at physics.nist.gov/cgi-bin/cuu/Value?alphinv):
       1/alpha = 137.035 999 177(21),  alpha = 0.0072973525643...
     (the paste's alpha 0.0072973525693 is the 2018 one too). The three-figure agreement is the
     same with either.

WHAT FITS THE PASTE'S OWN NUMBERS: the rows 1 10 11, 12 21 22, 23 32 33, ..., 89 98 99 (each column
  up 11 per row) give every claim of sections 1 (rows), 3 and 4 at once: columns leave 1, 10, 0 by
  11; row sums 22 55 88 121 ... step 33; their roots 4 1 7 4 1 7 ...; each row concatenated
  leaves 22 by 37; and 21 and 23 are in it. Whether this is the grid the paste had is not shown.

RESIDUES mod 37 (gf37-audit): 111 -> 0, 10101 -> 0, 3003 -> 6 TESLA, 55 -> 18 SEED, 56 -> 19
  CAS_EXT, 22 NQR17, 441 -> 34 D7, 529 -> 11 NEG_H, 729 -> 26 IC (729 and 137 both leave 26:
  729 - 137 = 592 = 16 x 37).

FALSIFICATION: any assertion failing.
"""
from decimal import Decimal, getcontext


def root(n):
    while n > 9:
        n = sum(map(int, str(n)))
    return n


def concat(row):
    return int("".join(f"{v:02d}" for v in row))


# --- RIGHT ---
assert 9 + 1 == 3 + 7 == 6 + 4 == 10 and root(10) == 1
for a in range(10, 60):
    for d in range(0, 14):
        assert 10000 * a + 100 * (a + d) + (a + 2 * d) == 10101 * a + 102 * d
assert 111111 == 37 * 3003 and 1000 == 27 * 37 + 1
assert pow(10, 4, 37) == 10 and pow(10, 5, 37) == 26 and pow(10, 2, 37) == 26
assert (1 + (-1) + 0) % 11 == 0
assert 21 * 21 == 441 and 23 * 23 == 529 and 529 - 441 == 88
assert all(36 % pow_ord == 0 for pow_ord in
           [next(k for k in range(1, 37) if pow(g, k, 37) == 1) for g in range(1, 37)])
assert 33 % 37 == 37 - 4 and pow(-4, 2, 37) == 16 and pow(-4, 3, 37) == 10 and pow(-4, 4, 37) == 34
assert pow(33, 9, 37) == 1 and pow(33, 3, 37) == 10 and next(k for k in range(1, 37) if pow(33, k, 37) == 1) == 9
assert pow(2, 20, 37) == 33 and 36 // 4 == 9
assert sorted({33 * k % 37 for k in range(37)}) == list(range(37))
block = str(10 ** 8 // 137).zfill(8)
assert block == "00729927" and pow(10, 8, 137) == 1 and all(pow(10, k, 137) != 1 for k in (1, 2, 4))
assert int(block[:4]) + int(block[4:]) == 9999 and all(int(x) + int(y) == 9 for x, y in zip(block[:4], block[4:]))
assert sum(map(int, block)) == 36 and root(36) == 9 and 72 + 27 == 99
assert 729 == 9 ** 3 == 27 ** 2

# --- WRONG 1 ---
assert all(x + y == 10 != 9 for x, y in ((9, 1), (3, 7), (6, 4)))
for start in range(1, 200):
    roots = {root(start + 33 * k) for k in range(30)}
    assert len(roots) == 3 and len({r % 3 for r in roots}) == 1

# --- WRONG 2 ---
assert 10101 == 37 * 273
for a in range(10, 70):
    for p in range(0, 15):
        for q in range(p, 29):
            if a + q < 100:
                assert concat((a, a + p, a + q)) % 37 == (26 * p + q) % 37
assert (102 % 37) == 28 and pow(28, -1, 37) == 4 and (22 * 4) % 37 == 14
assert concat((12, 13, 14)) == 121314 and 121314 % 37 == 28
assert concat((10, 24, 38)) == 102438 and 102438 % 37 == 22
assert (26 * 9 + 10) == 244 == 6 * 37 + 22

# --- WRONG 3 and 4 ---
getcontext().prec = 30
inv_alpha_2022, inv_alpha_2018 = Decimal("137.035999177"), Decimal("137.035999084")
alpha_2022, alpha_2018, frac = 1 / inv_alpha_2022, 1 / inv_alpha_2018, Decimal(1) / 137
assert str(alpha_2022).startswith("0.0072973525643") and str(alpha_2018).startswith("0.0072973525692")
assert str(frac).startswith("0.0072992700")


def sig(x, n):
    s = str(x).split(".")[1].lstrip("0")
    return s[:n]


for al in (alpha_2022, alpha_2018):
    assert sig(frac, 3) == sig(al, 3) == "729" and sig(frac, 4) == "7299" != sig(al, 4) == "7297"

# --- WHAT FITS ---
rows = [(1 + 11 * k, 10 + 11 * k, 11 + 11 * k) for k in range(9)]
assert rows[0] == (1, 10, 11) and rows[1] == (12, 21, 22) and rows[-1] == (89, 98, 99)
assert all((r[0] % 11, r[1] % 11, r[2] % 11) == (1, 10, 0) for r in rows)
sums = [sum(r) for r in rows]
assert sums[:4] == [22, 55, 88, 121] and all(sums[i + 1] - sums[i] == 33 for i in range(8))
assert [root(s) for s in sums] == [4, 1, 7] * 3
assert all(concat(r) % 37 == 22 for r in rows)
assert any(21 in r for r in rows) and any(23 in r for r in rows)

# --- RESIDUES ---
assert [x % 37 for x in (111, 10101, 3003, 55, 56, 22, 441, 529, 729)] == [0, 0, 6, 18, 19, 22, 34, 11, 26]
assert 137 % 37 == 26 and 729 - 137 == 592 == 16 * 37

if __name__ == "__main__":
    print("#411: arithmetic right (10101a + 102d, 111111 = 37 x 3003, ord(33) = 9, 1/137 = 0.(00729927), "
          "0072 + 9927 = 9999); wrong: '9-complements' (they add to 10), 'every row -> 22' (26p + q depends "
          "on the steps; uniform d gives 28d), 'four significant figures' (three), CODATA 2018 value quoted "
          "(2022: 137.035999177)")
