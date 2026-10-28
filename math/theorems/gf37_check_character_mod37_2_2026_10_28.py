# CLASS: COMPUTATION
"""
An application of the GF(37) arithmetic: the check character ISO/IEC 7064 MOD 37-2 (exports/check37.py), built
2026-10-28 as the first of the applications offered (check character, safe primes, Rule 30).

THE STANDARD: the 37 symbols 0-9, A-Z, * are 0 .. 36; total -> 2 x total + symbol, by 37; a code is right when its
total leaves 1; the check character is 1 - 2 x total, by 37.

WHAT MAKES IT WORK IS IN THE REPO ALREADY: 2 has order 36 by 37 (CLAUDE.md, "2 is a primitive root mod 37").
  one wrong symbol moves the total by (difference) x 2^k -- never 0 by 37, so always caught;
  a swap d apart moves it by (a - b) x 2^k x (2^d - 1) -- 0 by 37 only when 36 | d, because 2 has order 36;
  so every swap in a code of up to 36 symbols (check character included) is caught, and 36 apart is the first miss.

CHECKED HERE:
  the tool's own --test (python-stdnum's values, every single error, every swap under 36 apart, every aa -> bb,
    the 36-apart miss, 1 in 37 random strings pass);
  2^d = 1 by 37 for d = 1 .. 72 exactly at d = 36, 72;
  every single error in every position of every code of length 1 and 2 over all 36 symbols (exhaustive), and three
    codes of length 3.
Cross-checked outside CI against python-stdnum on 200,000 random codes of length 1 .. 40: 0 mismatches (2026-10-28).

FALSIFICATION: any assertion failing.
"""
import itertools
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "exports"))
import check37 as C  # noqa: E402

assert C.run_tests()
assert [d for d in range(1, 73) if pow(2, d, 37) == 1] == [36, 72]

letters = C.SYMBOLS[:36]
codes = ["".join(t) for L in (1, 2) for t in itertools.product(letters, repeat=L)] + ["A7Z", "000", "K9K"]
for code in codes:
    good = C.add_check(code)
    assert C.is_right(good)
    for i in range(len(good)):
        for ch in (C.SYMBOLS if i == len(good) - 1 else letters):
            if ch != good[i]:
                assert not C.is_right(good[:i] + ch + good[i + 1:])

if __name__ == "__main__":
    print("MOD 37-2: every single error and every swap under 36 apart caught; 2 has order 36 by 37")
