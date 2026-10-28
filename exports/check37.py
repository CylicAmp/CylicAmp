#!/usr/bin/env python3
"""
Check character on 37 -- one file, plain Python 3, nothing to install. Runs on a phone, an online Python, any computer.

    python3 check37.py CYLICAMP              adds the check character:  CYLICAMPF
    python3 check37.py --check CYLICAMPF     right or wrong
    python3 check37.py --test                runs every check below, PASS or FAIL

This is the international standard ISO/IEC 7064 MOD 37-2, the check for codes made of letters and digits (part numbers,
serial numbers, IDs). It is the arithmetic of GF(37):

  THE 37 SYMBOLS:  0 1 2 ... 9 are 0 .. 9,  A B C ... Z are 10 .. 35,  and * is 36.  (10 + 26 + 1 = 37)
  THE TOTAL:       go left to right; each step, total -> 2 x total + symbol, and keep what is left by 37.
  THE RULE:        a code is right when the total of the whole code (check character included) leaves 1.
  THE CHECK:       the check character is  1 - 2 x (total of the code), by 37.

WHY IT CATCHES MISTAKES -- each line is tested by --test:
  one wrong symbol:   the total moves by (the difference) x a power of 2; 37 is prime, so that is never 0 by 37 --
                      every single wrong symbol is caught.
  two symbols swapped, d places apart:  the total moves by (a - b) x (a power of 2) x (2^d - 1). 2 runs through all
                      36 remainders before it comes back to 1 (2 has order 36 by 37), so 2^d - 1 is a multiple of 37
                      only when d is a multiple of 36 -- every swap in a code of up to 36 symbols (check
                      character included) is caught, neighbours or not. Two symbols exactly 36 apart can swap
                      unseen; that needs a code of 37 or more, and --test shows one.
  a doubled symbol mistyped (aa -> bb):  moves the total by 3 x (a - b) x (a power of 2), never 0 -- caught.
  anything else (two or more random mistakes): slips through 1 time in 37, about 2.7%.
"""
import sys

SYMBOLS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ*"
M = 37


def total(code):
    t = 0
    for ch in code:
        t = (2 * t + SYMBOLS.index(ch)) % M
    return t


def check_character(code):
    """the one symbol to put at the end"""
    code = code.upper()
    if not code or any(ch not in SYMBOLS[:36] for ch in code):
        raise ValueError("use letters A-Z and digits 0-9 only")
    return SYMBOLS[(1 - 2 * total(code)) % M]


def add_check(code):
    return code.upper() + check_character(code)


def is_right(code_with_check):
    s = code_with_check.upper()
    return len(s) >= 2 and all(ch in SYMBOLS for ch in s[:-1]) and "*" not in s[:-1] and total(s) == 1


# reference values from python-stdnum (stdnum.iso7064.mod_37_2), computed 2026-10-28; G123498654321 -> H is the
# example in stdnum's own documentation
KNOWN = {"G123498654321": "H", "5": "S", "W2N": "O", "SX6TI": "5", "ORS935Q4": "Z", "YINRN2XDWQ40": "E",
         "0WN4E1KMXA10DJEW": "4", "J2IHDU9DH3SS6Z0HF5S8": "C", "LM1694AWFXIU1BYI8D7ARXY0MH43EAPSK4C5": "W",
         "CYLICAMP": "F", "GF37": "6", "A1B2C3": "8", "0000": "1", "ZZZZ": "O"}


def run_tests():
    results = []

    def claim(name, ok):
        results.append(ok)
        print(("PASS  " if ok else "FAIL  ") + name)

    claim("matches python-stdnum on %d codes" % len(KNOWN), all(check_character(c) == k for c, k in KNOWN.items()))
    claim("every code with its check character is right", all(is_right(c + k) for c, k in KNOWN.items()))
    claim("2 has order 36 by 37", [d for d in range(1, 37) if pow(2, d, M) == 1] == [36])

    letters = SYMBOLS[:36]
    singles = missed = 0
    for code in KNOWN:
        good = add_check(code)
        for i in range(len(good)):
            for ch in (SYMBOLS if i == len(good) - 1 else letters):
                if ch != good[i]:
                    singles += 1
                    missed += is_right(good[:i] + ch + good[i + 1:])
    claim("every single wrong symbol caught (%d tried)" % singles, missed == 0)

    swaps = missed = 0
    far = []
    for code in KNOWN:
        good = add_check(code)
        for i in range(len(good)):
            for j in range(i + 1, len(good)):
                if good[i] != good[j]:
                    s = list(good)
                    s[i], s[j] = s[j], s[i]
                    if j - i < 36:
                        swaps += 1
                        missed += is_right("".join(s))
                    else:
                        far.append(is_right("".join(s)))
    claim("every swap of two different symbols less than 36 apart caught (%d tried)" % swaps, missed == 0)
    claim("the limit is real: a swap exactly 36 apart slips through (%d of %d)" % (sum(far), len(far)),
          len(far) > 0 and all(far))

    twins = missed = 0
    for a in letters:
        for b in letters:
            if a != b:
                for pre in ("", "Q7", "ABC123"):
                    good = add_check(pre + a + a + "X")
                    bad = pre + b + b + "X" + good[-1]
                    twins += 1
                    missed += is_right(bad)
    claim("every doubled symbol mistyped aa -> bb caught (%d tried)" % twins, missed == 0)

    right_pairs = sum(is_right(a + b) for a in letters for b in SYMBOLS)
    claim("random two-symbol strings: exactly 1 in 37 pass (%d of %d)" % (right_pairs, 36 * 37), right_pairs == 36)
    return all(results)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "--test":
        sys.exit(0 if run_tests() else 1)
    if args[0] == "--check":
        for c in args[1:]:
            print(c.upper(), "right" if is_right(c) else "wrong")
    else:
        for c in args:
            print(add_check(c))
