# CLASS: AUDIT
"""
Check of the pasted claim table on negation, the cosets of <10> and T283 / T331 / T332 (owner_work #314, 2026-10-17).
The paste is another tool's text, relayed by the owner with no words of their own. It says the T283-T345 files "aren't in this
environment"; in this repository they are: math/lemmas/theorem_283_negation_antipodal_gf37.py,
math/theorems/theorem_331_orbit_sum_37_74_negation_gf37.py, math/theorems/theorem_332_six_six_forced_inversion_closed_gf37.py,
and the owner's 2026-07-26 file math/theorems/orbit_negation_duality_gf37.py.

EVERY ROW OF THE TABLE HOLDS (recomputed below):
  0 is the only fixed point of negation in Z/37Z; negation is free on the 36 nonzero elements (18 pairs); <10> = {1, 10, 26}
  (10^3 = 1000 = 1, 10^2 = 100 = 26 mod 37); -1 = 36 is not in <10>, so no coset is self-negating: 12 cosets, 6 dual pairs;
  the multiples of 37 in [6, 105] are 37 and 74 (the bound is T331's: three distinct residues sum to between 1+2+3 = 6 and
  34+35+36 = 105); 666 = 18 x 37 = 6 x 111 = 1 + ... + 36; 37a + 74(12 - a) = 666 gives a = 6 (T332); exactly two cosets are
  inversion-closed, {1, 10, 26} (IC) and {11, 27, 36} (NEG_H = -IC); negation moves the coset index by 6 in Z/12Z
  (dlog 2 of -1 is 18, and 18 = 6 mod 12), inversion sends the index k to -k, whose fixed points are 0 and 6.
  The repository files say the same: T331 lines 81-92 and 183-186 (the [6, 105] bound), T332 lines 82-105 (IC and NEG_H, 6/6),
  T283 Part 5 (0 is the unique fixed point of negation).

ONE POINT THAT DOES NOT MATCH THE FILES: the paste's order "T283 sets up the involution, T331 gives the bound, T332 uses it" is
  not the order the files cite. T283 says its Parts 1-4 and 6 are a restatement of orbit_negation_duality_gf37.py (owner, 2026-07-26)
  and that T331 and T332 cite that earlier file, not T283; only T283's Part 5 (the fixed point 0, the fixed-point-free involution)
  is its own. And T332 uses T331's result "every orbit sums to 37 or 74" with the total 666, not the [6, 105] bound directly.

FALSIFICATION: any assertion failing.
"""
import pathlib

P = 37
neg = lambda x: (-x) % P
inv = lambda x: pow(x, -1, P)
assert [x for x in range(P) if neg(x) == x] == [0] and len({frozenset((x, neg(x))) for x in range(1, P)}) == 18
H = sorted({pow(10, k, P) for k in range(3)})
assert H == [1, 10, 26] and 10 ** 3 == 1000 and 1000 % P == 1 and 100 % P == 26 and 36 not in H
cosets = {frozenset(x * h % P for h in H) for x in range(1, P)}
assert len(cosets) == 12 and not [c for c in cosets if frozenset(map(neg, c)) == c]
assert len({frozenset((c, frozenset(map(neg, c)))) for c in cosets}) == 6
assert [n for n in range(6, 106) if n % P == 0] == [37, 74] and 1 + 2 + 3 == 6 and 34 + 35 + 36 == 105 and 111 > 105
assert 666 == 18 * 37 == 6 * 111 == sum(range(1, 37))
assert sorted(sum(c) for c in cosets) == [37] * 6 + [74] * 6
assert [a for a in range(13) if 37 * a + 74 * (12 - a) == 666] == [6]
closed = [c for c in cosets if frozenset(map(inv, c)) == c]
assert sorted(sorted(c) for c in closed) == [[1, 10, 26], [11, 27, 36]] and frozenset((36, 27, 11)) == frozenset(map(neg, H))
dlog = {pow(2, k, P): k for k in range(36)}
assert dlog[36] == 18 and 18 % 12 == 6 and [k for k in range(12) if (-k) % 12 == k] == [0, 6]
assert all(dlog[x] % 12 == dlog[y] % 12 for c in cosets for x in c for y in c)          # the coset index is dlog 2 mod 12
assert {(dlog[x] % 12 + 6) % 12 for x in H} == {dlog[x] % 12 for x in map(neg, H)} == {6}
root = pathlib.Path(__file__).resolve().parent.parent
for f in ("lemmas/theorem_283_negation_antipodal_gf37.py", "theorems/theorem_331_orbit_sum_37_74_negation_gf37.py",
          "theorems/theorem_332_six_six_forced_inversion_closed_gf37.py", "theorems/orbit_negation_duality_gf37.py"):
    assert (root / f).exists(), f

if __name__ == "__main__":
    print("every row of the pasted table holds; two inversion-closed cosets IC and NEG_H; 6 dual pairs; a = 6; T331/T332 cite the 07-26 file, not T283")
