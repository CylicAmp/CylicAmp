#!/usr/bin/env python3
"""
Rule 30 random numbers -- one file, plain Python 3, nothing to install. Runs on a phone, an online Python, any computer.

    python3 rule30_random.py                         10 random numbers from 1 to 100 (fresh seed, printed so you can repeat it)
    python3 rule30_random.py --seed 246 --count 20 --range 1 6     20 dice rolls from seed 246 (same seed, same rolls)
    python3 rule30_random.py --seed 246 --bits 64    64 random bits
    python3 rule30_random.py --center 100            the first 100 cells of Rule 30's center column
    python3 rule30_random.py --test                  every check below, PASS or FAIL

RULE 30: a row of cells, each 0 or 1; each step every cell becomes   left XOR (center OR right).
  Start from one black cell and the column under it runs 1 1 0 1 1 1 0 0 1 1 0 0 0 1 0 ... (OEIS A051023).
  Wolfram used that center column for random integers in Mathematica (A New Kind of Science, p. 317).

THE GENERATOR: a ring of 1024 cells (the ends join), filled from your seed (SHA-256 of the seed, stretched to 1024
  bits), run 1024 steps to mix, then one bit per step is read from the middle cell -- Wolfram's way, one fixed cell.
  From the bits: dice rolls and numbers in any range (no bias: draws past the range are thrown back), bytes, and
  decimals between 0 and 1.

WHAT IT IS GOOD FOR: simulations, games, sampling, Monte Carlo -- anything that needs numbers that look random and
  can be repeated from a seed.
WHAT IT IS NOT FOR: passwords, keys, money. Meier and Staffelbach (EUROCRYPT 1991) showed how to recover the cells
  from the output of a Rule 30 generator; for those uses take os.urandom or Python's secrets module.

WHAT IS PROVED AND WHAT IS NOT: nobody has proved Rule 30 is random. All three Wolfram Rule 30 Prize problems are open
  (rule30prize.org): is the center column never periodic, are 0s and 1s equally common in it, does its nth cell need
  about n steps of work. A ring of 1024 cells is finite, so it must repeat some day; how long that takes is not known
  (small rings repeat fast -- --test shows it). Passing the tests below means no fault was seen, not that none exists.
"""
import hashlib
import math
import os
import sys

WIDTH = 1024
CENTER_SHA256_100000 = "f216025979f959fd49ff944fff3ba6b6365c143e1a79e1d52dc787da055a6aa0"   # OEIS A051023, n = 0 .. 99999
CENTER_FIRST_256_HEX = "dcc593ae756195abf0f15c12c71b6808fba71d7064679f81fd96e0b1b18ed95f"


def rule30(left, center, right):
    return left ^ (center | right)


def center_column(n):
    """the first n cells of the center column, starting from one black cell on an endless row"""
    row = 1 << n
    mask = (1 << (2 * n + 1)) - 1
    col = bytearray(n)
    for t in range(n):
        col[t] = (row >> n) & 1
        row = ((row >> 1) ^ (row | (row << 1))) & mask      # bit i takes bit i+1 (left) and bit i-1 (right)
    return col


class Rule30Random:
    """Rule 30 on a ring of `width` cells, one bit per step from the middle cell"""

    def __init__(self, seed=None, width=WIDTH, warmup=None):
        if seed is None:
            seed = os.urandom(16).hex()
        self.seed = seed
        self.width = width
        self.mask = (1 << width) - 1
        self.mid = width // 2
        data = seed if isinstance(seed, bytes) else str(seed).encode()
        stretched, counter = b"", 0
        while len(stretched) * 8 < width:
            stretched += hashlib.sha256(data + counter.to_bytes(4, "big")).digest()
            counter += 1
        self.row = int.from_bytes(stretched, "big") & self.mask
        if self.row in (0, self.mask):                       # all 0s stays 0; all 1s turns to all 0s
            self.row ^= 1
        for _ in range(width if warmup is None else warmup):
            self.step()

    def step(self):
        r, w = self.row, self.width
        left = (r >> 1) | ((r & 1) << (w - 1))               # bit i takes bit i+1, joined round the ring
        right = ((r << 1) & self.mask) | (r >> (w - 1))      # bit i takes bit i-1
        self.row = left ^ (r | right)
        if self.row == 0:
            raise RuntimeError("the ring died out (all cells 0) -- use another seed")

    def bit(self):
        self.step()
        return (self.row >> self.mid) & 1

    def getrandbits(self, k):
        x = 0
        for _ in range(k):
            x = (x << 1) | self.bit()
        return x

    def randbelow(self, n):
        """0 .. n-1, every value equally likely (draws of n or more are thrown back)"""
        if n <= 0:
            raise ValueError("n must be positive")
        k = max(1, (n - 1).bit_length())
        while True:
            x = self.getrandbits(k)
            if x < n:
                return x

    def randint(self, a, b):
        return a + self.randbelow(b - a + 1)

    def random(self):
        return self.getrandbits(53) / (1 << 53)

    def randbytes(self, n):
        return bytes(self.getrandbits(8) for _ in range(n))


# ---- tests (NIST SP 800-22 statistics, written out) ----

def igamc(a, x):
    """regularized upper incomplete gamma Q(a, x)"""
    if x <= 0:
        return 1.0
    if x < a + 1:
        s = term = 1.0 / a
        n = 0
        while abs(term) > abs(s) * 1e-15 and n < 100000:
            n += 1
            term *= x / (a + n)
            s += term
        return 1.0 - s * math.exp(-x + a * math.log(x) - math.lgamma(a))
    b, c, d = x + 1 - a, 1e300, 1.0 / (x + 1 - a)
    h = d
    for i in range(1, 100000):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        d = 1e-300 if abs(d) < 1e-300 else d
        c = b + an / c
        c = 1e-300 if abs(c) < 1e-300 else c
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1) < 1e-15:
            break
    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


def monobit(b):
    s = abs(2 * sum(b) - len(b)) / math.sqrt(len(b))
    return math.erfc(s / math.sqrt(2))


def block_frequency(b, M=128):
    N = len(b) // M
    chi2 = 4 * M * sum((sum(b[i * M:(i + 1) * M]) / M - 0.5) ** 2 for i in range(N))
    return igamc(N / 2, chi2 / 2)


def runs(b):
    n = len(b)
    pi = sum(b) / n
    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        return 0.0
    v = 1 + sum(b[i] != b[i + 1] for i in range(n - 1))
    return math.erfc(abs(v - 2 * n * pi * (1 - pi)) / (2 * math.sqrt(2 * n) * pi * (1 - pi)))


def serial(b, m=3):
    n = len(b)

    def psi2(k):
        if k <= 0:
            return 0.0
        ext = list(b) + list(b[:k - 1])
        counts = [0] * (1 << k)
        x = 0
        for i in range(k - 1):
            x = (x << 1) | ext[i]
        for i in range(k - 1, n + k - 1):
            x = ((x << 1) | ext[i]) & ((1 << k) - 1)
            counts[x] += 1
        return (1 << k) / n * sum(c * c for c in counts) - n

    p_m, p_m1, p_m2 = psi2(m), psi2(m - 1), psi2(m - 2)
    return igamc(2 ** (m - 2), (p_m - p_m1) / 2), igamc(2 ** (m - 3), (p_m - 2 * p_m1 + p_m2) / 2)


def autocorrelation(b, d):
    n = len(b) - d
    a = sum(b[i] ^ b[i + d] for i in range(n))
    return math.erfc(abs(2 * (a - n / 2) / math.sqrt(n)) / math.sqrt(2))


def byte_spread(data):
    counts = [0] * 256
    for x in data:
        counts[x] += 1
    e = len(data) / 256
    return igamc(255 / 2, sum((c - e) ** 2 / e for c in counts) / 2)


def run_tests():
    results = []

    def claim(name, ok):
        results.append(bool(ok))
        print(("PASS  " if ok else "FAIL  ") + name)

    table = {(l, c, r): rule30(l, c, r) for l in (0, 1) for c in (0, 1) for r in (0, 1)}
    claim("left XOR (center OR right) is rule number 30 (00011110 in binary)",
          sum(v << (4 * l + 2 * c + r) for (l, c, r), v in table.items()) == 30)

    col = center_column(100000)
    s = "".join(map(str, col))
    claim("center column, first 256 cells = OEIS A051023", "%064x" % int(s[:256], 2) == CENTER_FIRST_256_HEX)
    claim("center column, first 100,000 cells = OEIS A051023 (SHA-256 of the b-file terms)",
          hashlib.sha256(s.encode()).hexdigest() == CENTER_SHA256_100000)
    claim("center column: %d ones in 100,000 (50,098 in OEIS)" % s.count("1"), s.count("1") == 50098)

    # Each statistic runs on six seeds, 1 .. 6 (fixed, not picked). A perfect generator falls below 0.01 on one seed
    # 1 time in 17 and on two or more about 1 time in 700, so a statistic passes when at most one seed is below 0.01.
    # (A single fixed seed fails a perfect generator 1% of the time per statistic: the first version of this file did
    # that and two of fifteen came back low; over 50 seeds the p-values were evenly spread -- see the theorem file.)
    stats = {"monobit": [], "block frequency (128)": [], "runs": [], "serial (3-bit), first": [],
             "serial (3-bit), second": [], "bytes over 256 values (12,800)": [], "dice (30,000 rolls)": []}
    lag_fails = 0
    first_bits = None
    for seed in range(1, 7):
        g = Rule30Random(seed=seed)
        bits = [g.bit() for _ in range(100000)]
        if first_bits is None:
            first_bits = bits
        stats["monobit"].append(monobit(bits))
        stats["block frequency (128)"].append(block_frequency(bits))
        stats["runs"].append(runs(bits))
        s1, s2 = serial(bits)
        stats["serial (3-bit), first"].append(s1)
        stats["serial (3-bit), second"].append(s2)
        lag_fails += sum(autocorrelation(bits, d) < 0.01 for d in range(1, 33))
        stats["bytes over 256 values (12,800)"].append(byte_spread(g.randbytes(12800)))
        rolls = [g.randint(1, 6) for _ in range(30000)]
        chi2 = sum((rolls.count(k) - 5000) ** 2 / 5000 for k in range(1, 7))
        stats["dice (30,000 rolls)"].append(igamc(2.5, chi2 / 2))
    for name, ps in stats.items():
        low = sum(p < 0.01 for p in ps)
        claim("ring, 6 seeds: %s, p = %s" % (name, " ".join("%.3f" % p for p in ps)), low <= 1)
    claim("ring, 6 seeds: autocorrelation lags 1..32: %d of 192 below 0.01 (1.9 expected by chance)" % lag_fails,
          lag_fails <= 6)

    g2 = Rule30Random(seed=1)
    claim("same seed, same numbers", [g2.bit() for _ in range(1000)] == first_bits[:1000])
    g3 = Rule30Random(seed=2)
    diff = sum(a != g3.bit() for a in first_bits[:10000])
    claim("seed 2 vs seed 1: %d of 10,000 bits differ (about half expected)" % diff, 4800 < diff < 5200)

    g5 = Rule30Random(seed=1, width=64, warmup=0)
    g5.row = g5.mask
    try:
        g5.step()
        stopped = False
    except RuntimeError:
        stopped = True
    claim("all 1s turns to all 0s in one step (and all 0s stays 0s); the generator stops there instead of "
          "giving 0s forever", rule30(0, 0, 0) == 0 and rule30(1, 1, 1) == 0 and stopped)

    def cycle(width, seed):
        g = Rule30Random(seed=seed, width=width, warmup=0)
        seen = {}
        for t in range(1 << 20):
            if g.row in seen:
                return t - seen[g.row]
            seen[g.row] = t
            g.step()
        return None

    lengths = [cycle(16, s) for s in range(20)]
    claim("a ring of 16 cells repeats: cycle lengths up to %d steps over 20 seeds (65,536 states; finite rings "
          "always repeat, so the width matters)" % max(lengths), all(x is not None for x in lengths))
    return all(results)


def main(args):
    if args and args[0] == "--test":
        return 0 if run_tests() else 1
    opts = {}
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--range":
            opts["range"] = (int(args[i + 1]), int(args[i + 2]))
            i += 3
        elif a in ("--seed", "--count", "--bits", "--center"):
            opts[a[2:]] = args[i + 1]
            i += 2
        else:
            print(__doc__)
            return 1
    if "center" in opts:
        print("".join(map(str, center_column(int(opts["center"])))))
        return 0
    g = Rule30Random(seed=opts.get("seed"))
    if "bits" in opts:
        print("".join(str(g.bit()) for _ in range(int(opts["bits"]))))
    else:
        lo, hi = opts.get("range", (1, 100))
        print(" ".join(str(g.randint(lo, hi)) for _ in range(int(opts.get("count", 10)))))
    if "seed" not in opts:
        print("seed:", g.seed, "(use --seed to get the same numbers again)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
