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

THE VARIANCE LAW, RE-RUN (records/prime_pairs_1e9_moduli_scan.json: 4,938 / 4,938 / 4,940 moduli, all q to 2000 and
  primes to 30,000), RIGHT within the moduli-set difference (report: 4,928):
    twins   mean z -14.15 (report -14.18), sd 8.12 (8.10), |z| > 3 in 4,661 (4,661); kappa = 0.220 + 1.163 r,
            R^2 0.778 (0.224 + 1.155 r, 0.773); slope-1 constant c = 5.92 (5.92); binned 0.412 0.569 0.669 0.768
            (0.422 0.569 0.669 0.768)
    cousins mean z -14.16 (-14.19), c = 5.88 (5.89);   sexy mean z -15.51 (-15.53), c = 5.56 (5.56), R^2 0.782 (0.808)
  where kappa = chi^2/df, r = log q / log x. q = 9 at 10^9: kappa 0.408 against the law's 0.392.

THE RESIDUAL CLAIM, WRONG (section 6: "|z_res| > 3: 6/4928 ... the law + sampling noise accounts for essentially
  everything; no modulus stands out"): the 6 comes back only by measuring against the plain multinomial spread
  sqrt(2/df). If counts vary kappa times the multinomial -- the report's own law -- the spread of kappa is
  kappa x sqrt(2/df) (simulated at q = 25013: 0.0070), and then 134 twin moduli are beyond 3 (13 expected).
  Where the excess is: for primes q from 20,000 to 30,000 the scatter equals sampling noise (0.0071 against 0.0070);
  below 2000, prime moduli sit above the law and composites below (+0.035 / -0.027 twins, +0.031 / -0.030 cousins,
  +0.025 / -0.019 sexy) -- far beyond noise (means over 301 and 1,694 moduli). Adding S(q) = sum of log p/(p - 1)
  over the primes p dividing q fits c(q) = 6.27 - 1.16 S(q) (twins), 6.24 - 1.17 S(q) (cousins), 5.77 - 0.69 S(q)
  (sexy) and shrinks the twin prime/composite gap from 0.062 to 0.014; outliers remain (171 / 106 / 68 beyond 3),
  so the law still misses structure. (A sum over p | q of log p/(p - 1) is recalled from the lower-order term of
  the Hooley / Friedlander-Goldston variance for primes; that paper's text was not reached to confirm it. Related:
  Goldston and Yildirim, Canad. J. Math. 50 (1998), total variance under a twin-prime hypothesis.)

THE OWNER'S RACE AGAINST THE LAW (q = 9, x = 2N, kappa_law = (log 9 + 6.27 - 1.16 S(9))/log x):
  n up to 10^9: chi^2 = 2.65, kappa 1.33 against 0.37 -- more spread than the law (high tail p = 0.027);
  n up to 10^12: chi^2 = 0.006, kappa 0.003 against 0.28 -- more even than the law (low tail p = 0.011), the
  "3,744 apart" of the race file; the other checkpoints ordinary. Seven cumulative looks, so neither tail decides.

FALSIFICATION: any assertion failing.
"""
import math

import numpy as np
from scipy import stats
from sympy import factorint, isprime
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

root_dir = pathlib.Path(__file__).resolve().parents[2]
scan = json.loads((root_dir / "records" / "prime_pairs_1e9_moduli_scan.json").read_text())
lx = math.log(1e9)


def analyse(rows):
    a = np.array(rows, dtype=float)
    q, chi2, df = a[:, 0], a[:, 1], a[:, 2]
    kap = chi2 / df
    z = (chi2 - df) / np.sqrt(2 * df)
    c = float(np.mean(kap * lx - np.log(q)))
    law = (np.log(q) + c) / lx
    S = np.array([sum(math.log(p) / (p - 1) for p in factorint(int(x))) for x in q])
    (c0, beta), *_ = np.linalg.lstsq(np.vstack([np.ones_like(S), S]).T, kap * lx - np.log(q), rcond=None)
    pr = np.array([isprime(int(x)) for x in q])
    small = q < 2000
    res = kap - law
    return dict(n=len(q), mean_z=z.mean(), c=c, z3=int((abs(z) > 3).sum()),
                unscaled=int((abs((kap - law) / np.sqrt(2 / df)) > 3).sum()),
                scaled=int((abs((kap - law) / (law * np.sqrt(2 / df))) > 3).sum()),
                prime=res[small & pr].mean(), comp=res[small & ~pr].mean(), c0=c0, beta=beta, q=q, kap=kap, df=df)


tw = analyse(scan["twins"])
assert tw["n"] == 4938 and round(tw["mean_z"], 2) == -14.15 and round(tw["c"], 2) == 5.92 and tw["z3"] == 4661
assert tw["unscaled"] == 6 and tw["scaled"] == 134                      # the report's 6 needs the unscaled spread
assert tw["prime"] > 0.03 and tw["comp"] < -0.025                       # primes above the law, composites below
assert round(tw["c0"], 2) == 6.27 and round(tw["beta"], 2) == -1.16
big = tw["q"] >= 20000
A = np.vstack([np.ones(big.sum()), np.log(tw["q"][big])]).T
coef, *_ = np.linalg.lstsq(A, tw["kap"][big], rcond=None)
detr = (tw["kap"][big] - A @ coef).std(ddof=1)
noise = math.sqrt(float(np.mean((tw["kap"][big].mean() * np.sqrt(2 / tw["df"][big])) ** 2)))
assert abs(detr - noise) < 0.0005                                        # large primes: scatter = sampling noise
co, sx = analyse(scan["cousins"]), analyse(scan["sexy"])
assert round(co["c"], 2) == 5.88 and round(sx["c"], 2) == 5.56 and round(sx["mean_z"], 2) == -15.51

# the owner's race against the law, q = 9
race = json.loads((root_dir / "records" / "owner_race_1e12.json").read_text())["checkpoints"]
S9 = math.log(3) / 2
tails = {}
for N, cts in race.items():
    N = int(N)
    e = sum(cts) / 3
    chi2 = sum((x - e) ** 2 / e for x in cts)
    k = (math.log(9) + 6.27 - 1.16 * S9) / math.log(2 * N)
    tails[N] = (stats.chi2.sf(chi2 / k, 2), stats.chi2.cdf(chi2 / k, 2))
assert round(tails[10 ** 9][0], 3) == 0.027 and round(tails[10 ** 12][1], 3) == 0.011
assert all(min(t) > 0.1 for N, t in tails.items() if N not in (10 ** 9, 10 ** 12))

if __name__ == "__main__":
    print("scan counts right except cousins (3,424,680, not 3,424,681); the owner's chain race is the scan's q = 9")
    print("variance law reproduced (c = 5.92); its residual claim needs the unscaled spread: 134 moduli beyond 3, "
          "primes above / composites below; the race at 10^12 is more even than the law (p = 0.011)")
