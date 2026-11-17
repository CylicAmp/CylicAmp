# CLASS: AUDIT
"""
Pasted ledger table (2026-11-17), from another tool, relayed by the owner: rows 1-9 as before, plus Lemmas 10-12.
Rows 1-9 were audited in pasted_v6_ledger_lemmas_audit_2026_11_17.py and pasted_unified_handoff_ledger_audit_
2026_11_17.py; this table still marks Lemma 1 PROVEN while writing "C+ = {10, ..., 17}; 11 not in C+" (11 is in
that set: 2 + 9), and Lemma 2 PROVEN for "31 -> 10" (not derived).

LEMMA 10: W8(12) + W8(34) = W8(46) -- right (12 + 34 = 46, no carries; every cut adds the same way,
  owner_3333_cuts_and_repeats_2026_11_17.py). "Phi_8 = 73 x 101 x 137" -- WRONG: Phi_8(x) = x^4 + 1, so
  Phi_8(10) = 10001 = 73 x 137. 73 x 101 x 137 = 1010101 = Phi_4(10) x Phi_8(10) = 101 x 10001, the factor that turns
  ab into abababab.
LEMMA 11: P = 104 and +12 black cells per period -- right, Langton's ant highway (langton_ant_highway_2026_10_14.py,
  proved there for the all-white start; the +12 is 23 white-to-black flips minus 11 black-to-white). "58 - 46" as
  the source of the 12 and "|R_red| = 256" are not defined anywhere in the paste or the repo -- missing.
  104 is also the single-digit total of the owner's sequence (12 + 28 + 12 + 40 + 12); the table sets the two side
  by side, nothing derives one from the other.
LEMMA 12: 3 + 5 = 8, 7 + 1 = 8, 8 + 8 = 16 -> 7 -- right. "7 <-> 8 involution" is not shown: 7 -> 8 goes by +10 then
  the digit sum (Lemma 5), 8 -> 7 by doubling then the digit sum; two different maps, so no single map is shown to
  undo itself.

FALSIFICATION: any assertion failing.
"""
import sympy as sp

x = sp.symbols("x")
assert sp.expand(sp.cyclotomic_poly(8, x) - (x ** 4 + 1)) == 0
assert sp.cyclotomic_poly(8, 10) == 10001 == 73 * 137 and 73 * 101 * 137 == 1010101 != 10001
assert sp.cyclotomic_poly(4, 10) * sp.cyclotomic_poly(8, 10) == 1010101
assert 12121212 + 34343434 == 46464646 and all(n == ab * 1010101 for ab, n in ((12, 12121212), (34, 34343434), (46, 46464646)))

assert 23 - 11 == 12 == 58 - 46 and 12 + 28 + 12 + 40 + 12 == 104

assert 3 + 5 == 8 == 7 + 1 and 8 + 8 == 16 and 1 + 6 == 7
assert 7 + 10 == 17 and 1 + 7 == 8                                  # 7 -> 8 (Lemma 5's map)
assert 1 + (2 * 8 - 1) % 9 == 7 and 1 + (7 + 10 - 1) % 9 == 8         # two different maps

C = {a + b for a in range(1, 10) for b in range(1, 10) if a < b and a + b >= 10}
assert C == set(range(10, 18)) and 11 in C

if __name__ == "__main__":
    print("lemma 10: W8 sum right, Phi_8(10) = 10001 = 73 x 137 (not x 101); lemma 11: 104 and +12 right; lemma 12 right")
