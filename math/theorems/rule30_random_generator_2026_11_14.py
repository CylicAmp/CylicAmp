# CLASS: COMPUTATION
"""
The Rule 30 random number generator (exports/rule30_random.py), built 2026-11-14: the third of the applications
offered on 2026-10-28 (check character, safe primes, Rule 30). Builds on math/primes/rule30_scope.py, which already
measured the center column (monobit, block frequency, runs, autocorrelation) and records that all three Rule 30 Prize
problems are open.

THE GENERATOR: Rule 30 (each cell -> left XOR (center OR right)) on a ring of 1024 cells, seeded by SHA-256 of the
seed, 1024 mixing steps, then one bit per step from the middle cell -- Wolfram's way (A New Kind of Science, p. 317:
Mathematica's Random[Integer] took the center cell of Rule 30). Numbers in a range by throwing back draws past it.
NOT for keys or passwords: Meier and Staffelbach (EUROCRYPT 1991) recover the cells from the output.

CHECKED HERE (CI):
  the program's own --test: the rule is number 30; the center column equals OEIS A051023 for 100,000 cells
    (SHA-256 of the b-file terms, 50,098 ones); on six fixed seeds 1 .. 6, monobit, block frequency, runs, serial,
    bytes, dice and autocorrelation; same seed same numbers; all-1s dies; a 16-cell ring repeats;
  the statistics against NIST SP 800-22's own worked examples (monobit 0.527089, block frequency 0.801252, runs
    0.147232, serial 0.808792 / 0.670320) and the gamma function against scipy;
  dice p-values over 10 seeds spread evenly (Kolmogorov-Smirnov against uniform).

FOUND WHILE BUILDING (2026-11-14): the first version tested one fixed seed per statistic; two of fifteen came back
  below 0.01 (bytes after 200,000 bits on seed 246, p = 0.002; 60,000 dice rolls on seed "dice", p = 0.0003). Over
  50 seeds (1000 .. 1049) beside Python's Mersenne Twister on the same tests: dice 1 of 50 below 0.01 (0.5 expected),
  p-values even (KS p = 0.38); bytes 0 of 50; the twister 0 and 0. Seed "dice" over 600,000 rolls: p = 0.15. So the two
  were chance lows; one fixed seed fails a perfect generator 1% of the time per statistic, and the test now uses six.
  The guessed bound for the 16-cell ring (5000) was wrong too: it repeats within 6016 steps over 20 seeds.

FALSIFICATION: any assertion failing.
"""
import pathlib
import sys

from scipy.special import gammaincc
from scipy.stats import chisquare, kstest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "exports"))
import rule30_random as R  # noqa: E402

assert R.run_tests()


def b(s):
    return [int(c) for c in s]


assert round(R.monobit(b("1011010101")), 6) == 0.527089
assert round(R.block_frequency(b("0110011010"), M=3), 6) == 0.801252
assert round(R.runs(b("1001101011")), 6) == 0.147232
assert tuple(round(p, 6) for p in R.serial(b("0011011101"), m=3)) == (0.808792, 0.670320)
for a, x in ((2.5, 11.7), (127.5, 150.0), (0.5, 0.3), (32, 20), (2, 7.1), (5, 0.01)):
    assert abs(R.igamc(a, x) - gammaincc(a, x)) < 1e-9

ps = []
for seed in range(100, 110):
    g = R.Rule30Random(seed=seed)
    rolls = [g.randint(1, 6) for _ in range(20000)]
    ps.append(chisquare([rolls.count(k) for k in range(1, 7)]).pvalue)
assert kstest(ps, "uniform").pvalue > 0.01 and sum(p < 0.01 for p in ps) <= 1

if __name__ == "__main__":
    print("Rule 30 generator: center column = OEIS A051023, NIST statistics match NIST's examples, six seeds pass")
