# CLASS: AUDIT
"""
Pasted audit of pages 11-13 of the manuscript "Haq & Song" (the TMC turmite / Langton's-ant image cipher), with a
script verify_pages_10_to_13.py, from another tool, relayed by the owner (2026-11-17). The manuscript and the module
verify_tmc_cipher.py it imports are not in the repository.

RIGHT:
  NIST SP 800-22 at alpha = 0.01 with 100 sequences: minimum pass proportion 0.99 - 3 sqrt(0.99 x 0.01 / 100) =
    0.9602 -> 0.96; raw fails Block Frequency (0.82), DFT (0.89), Serial-1 (0.95); totals 855 and 892 of 900, gain 37.
  Error bound: 1% noise x at most 5 bytes = 5% > 4.85% observed; a 128 x 128 occlusion is 16384 / 262144 = 6.25%.
  Steps: 2n + 4n + 8n = 14n; 917,504 / 3,670,016 / 14,680,064 steps; their roots 8, 5, 2 (forced: 14 -> 5 and the
    powers of 4 have roots 7, 1, 4 in turn, so 5 x 7 -> 8, 5 x 1 -> 5, 5 x 4 -> 2).
  Table 4 critical values (Wu-Noonan-Agaian, alpha = 0.05): NPCR 99.5893 / 99.5793 / 99.5581 / 99.5693 and the UACI
    pairs 33.3730-33.5541, 33.3276-33.5995, 33.2317-33.6954, 33.2824-33.6447 -- all right as values.
  Design law: highway onset 9977, period 104, +12 per period (langton_ant_highway_2026_10_14.py: onset step 9,976,
    Propp's 9977 counts the first step); |R_red| = 256 for m = 16 is the number of REDUCIBLE 16-colour rules, those
    repeating a word whose length divides 8: 2^8 = 256 (irreducible: 2^16 - 2^8 = 65,280; brute force at m = 8 gives
    2^4 = 16). That settles the "|R_red| = 256" asked about with the ledger's Lemma 11.

FAULTS THAT CHANGE A RESULT:
  1. The script's UACI formula is missing a factor F in the variance: it computes
     sigma^2 = (F+2)(F^2+2F+3) / (18 (F+1)^2 M N), which gives 32.0171-34.9100 at 512 x 512, so its own Table 4
     assertions FAIL. With sigma^2 = (F+2)(F^2+2F+3) / (18 (F+1)^2 M N F) (Wu, Noonan, Agaian) all four pairs match.
  2. "Encryption time scales linearly": the step count does (14n), but the paper's times grow 0.022 -> 0.118 -> 0.614 s,
     x5.36 and x5.20 for each x4 in pixels -- about n^1.2, not linear.
  3. "+37, the central prime": the 37 is the sum of per-test gains 1, 17, 2, -1, 8, 3, 5, 4, -2 over one run of
     100 sampled sequences per test (17 of it from Block Frequency); it moves with the keys and carries no
     structure. (999 = 27 x 37 is right, and so is Z/999 = Z/27 x Z/37.)
NOT CHECKABLE HERE: the 5-byte propagation test needs verify_tmc_cipher.py and Equation 3 / Proposition 8 from
  the manuscript -- missing.

FALSIFICATION: any assertion failing.
"""
import math
from itertools import product

from scipy.stats import norm

F = 255


def npcr_star(m, n, a=0.05):
    return round(100 * (F - norm.ppf(1 - a) * math.sqrt(F / (m * n))) / (F + 1), 4)


def uaci(m, n, a=0.05, with_F=True):
    mu = (F + 2) / (3 * F + 3)
    var = ((F + 2) * (F * F + 2 * F + 3)) / (18 * (F + 1) ** 2 * m * n * (F if with_F else 1))
    z = norm.ppf(1 - a / 2)
    return round(100 * (mu - z * math.sqrt(var)), 4), round(100 * (mu + z * math.sqrt(var)), 4)


table4 = {(512, 512): (99.5893, 33.3730, 33.5541), (303, 384): (99.5793, 33.3276, 33.5995),
          (200, 200): (99.5581, 33.2317, 33.6954), (256, 256): (99.5693, 33.2824, 33.6447)}
for (m, n), (ns, um, up) in table4.items():
    assert npcr_star(m, n) == ns and uaci(m, n) == (um, up)
    assert uaci(m, n, with_F=False) != (um, up)                     # the script's formula fails its own table
assert uaci(512, 512, with_F=False) == (32.0171, 34.91)

assert round(0.99 - 3 * math.sqrt(0.99 * 0.01 / 100), 4) == 0.9602
raw = [99, 82, 98, 100, 89, 97, 95, 96, 99]
tmc = [100, 99, 100, 99, 97, 100, 100, 100, 97]
assert sum(raw) == 855 and sum(tmc) == 892 and sum(tmc) - sum(raw) == 37
assert [t - r for r, t in zip(raw, tmc)] == [1, 17, 2, -1, 8, 3, 5, 4, -2]
assert [p < 96 for p in raw] == [False, True, False, False, True, False, True, False, False]
assert 999 == 27 * 37 and math.gcd(27, 37) == 1


def root(n):
    return 1 + (n - 1) % 9


steps = [14 * s * s for s in (256, 512, 1024)]
assert steps == [917504, 3670016, 14680064] and [root(x) for x in steps] == [8, 5, 2]
assert round(0.118 / 0.022, 2) == 5.36 and round(0.614 / 0.118, 2) == 5.2
assert round(math.log(0.614 / 0.022) / math.log(16), 2) == 1.2      # about n^1.2

assert 16384 / 262144 == 0.0625 and 4.85 < 5 * 1


def reducible(s):
    m = len(s)
    return any(s == s[:e] * (m // e) for e in range(1, m) if m % e == 0)


assert sum(reducible(s) for s in product("LR", repeat=8)) == 2 ** 4
assert 2 ** 8 == 256 and 2 ** 16 - 2 ** 8 == 65280

if __name__ == "__main__":
    print("pages 11-13: values right; script's UACI misses a factor F; times ~n^1.2; +37 is sampling; |R_red| = 2^8")
