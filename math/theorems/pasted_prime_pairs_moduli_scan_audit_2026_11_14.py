# CLASS: AUDIT
"""
Pasted report "PRIME PAIRS IN ARITHMETIC PROGRESSIONS: LARGE-MODULI SCAN" (dated 2026-10-01, twin-prime
building-block thread; relayed by the owner 2026-11-14). Re-run here to 10^9 with a full odd sieve (2026-11-14).

COUNTS, RIGHT:  primes up to 10^9: 50,847,534; up to 10^9 + 8: 50,847,535 (the report's figure).
  twins: 3,424,506 bases up to 10^9 = OEIS A007508 = the owner's walk to 500,000,000
    (math/theorems/owner_engine_walk_1b_2026_10_23.py); 3,424,507 up to 10^9 + 8 -- the extra one is
    (1,000,000,007, 1,000,000,009), wholly above 10^9 (the report calls it "straddling").
  sexy (p, p + 6, any primes between): 6,849,047.
  cousins by 30: (1,5) 0 pairs, (7,11) 1,141,562, (13,17) 1,141,544, (19,23) 1,141,573 -- exactly the report's.
COUNT, WRONG:  cousins 3,424,681 -- it is 3,424,680 (to 10^9 and to 10^9 + 8 alike): the report's own three class
  counts add to 3,424,679, plus (3, 7) = 3,424,680.

CONNECTION TO THE OWNER'S WORK: the owner's twin chain race (owner_twin_chain_race_1e12_2026_10_26.py) splits twin
  pairs by the root of n into (5,7), (2,4), (8,1); those are exactly the three twin classes by 9 (base p = 2n - 1
  leaves 5, 2, 8 by 9). So the race is this report's modulus q = 9.

FALSIFICATION: any assertion failing.
"""
import json
import pathlib

rec = json.loads((pathlib.Path(__file__).resolve().parents[2] / "records" / "prime_pairs_1e9_counts.json").read_text())
c = rec["counts"]
assert (c["pi_1e9"], c["pi_1e9p8"]) == (50847534, 50847535)
assert (c["h2_base_le_1e9"], c["h2_base_le_1e9p8"]) == (3424506, 3424507)
assert c["h4_base_le_1e9"] == c["h4_base_le_1e9p8"] == 3424680 != 3424681
assert c["h6_base_le_1e9"] == 6849047
m = c["cousin_mod30"]
assert (m["1"], m["3"], m["7"], m["13"], m["19"]) == (0, 1, 1141562, 1141544, 1141573)
assert 1141562 + 1141544 + 1141573 == 3424679 and 3424679 + 1 == 3424680
# the race is q = 9: twin base p = 2n - 1 by 9, for n by 9 = 3, 6, 0
assert {n % 9: (2 * n - 1) % 9 for n in (3, 6, 9)} == {3: 5, 6: 2, 0: 8}
assert sorted(a for a in range(9) if a % 3 and (a + 2) % 3) == [2, 5, 8]
for n in range(3, 3000, 3):
    root = 1 + (n - 1) % 9
    assert {3: 5, 6: 2, 9: 8}[root] == (2 * n - 1) % 9

if __name__ == "__main__":
    print("scan counts right except cousins (3,424,680, not 3,424,681); the owner's chain race is the scan's q = 9")
