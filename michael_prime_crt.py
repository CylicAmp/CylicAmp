#!/usr/bin/env python3
"""
michael_prime_crt -- the Michael primes (PM) through the CRT split 333 = 9 x 37, built from the owner's test file of
2026-11-19 (kept verbatim in owner_work/michael_prime_crt_tests_as_given.py; the run version is
tests/test_michael_prime_crt.py).

WHAT THE TESTS FIX, AND WHAT THIS MODULE TAKES FROM THEM
  * The ledger's 45 primes up to 10000 have digital root 1, 4 or 7 (they leave 1 by 3) and leave 6, 20 or 31 by 37,
    so they sit in nine classes by 333 (CRT): 31, 43, 94, 142, 154, 205, 253, 265, 316.
    A Michael prime here is a prime in one of those nine classes.
  * The mirror is the nines complement, 10^w - 1 - n (w = number of digits), so n + mirror = 99..9 and the test
    (mod_37 + mirror_mod_37) = (10^w - 1) by 37 is exact. Mirror roots: 9 - (1, 4, 7) = 8, 5, 2. For four digits
    9999 leaves 9 by 37, so the mirror leaves 9 - (6, 20, 31) = 3, 26, 15.
  * BRAID_981 is the six orderings of 1, 8, 9 (981 is one of them): total 3996 = 2 x 1998 = 108 x 37. Its two turn
    cycles 189 -> 891 -> 918 and 198 -> 981 -> 819 each add to 1998 = 6 x 333. Every ordering has root 9, so adding it
    never moves a root.
  * vireon_13_coupling = 13 x n by 37. 13 x 20 = 260 = 7 x 37 + 1, so the coupling is 1 exactly on the class 20 --
    2203 and 4201 (both 205 by 333) lock to 1. The tests fix only those two values; this definition is the reading used.

WHAT THE TESTS DO NOT SETTLE (asked)
  * The ledger leaves out 1759 and 2251. Both are prime and sit in the same classes (1759 = 5 x 333 + 94, the class
    of 1093; 2251 = 6 x 333 + 253, the class of 919 and 2917), and both pass every node test of the file. The rule
    above gives 47 primes up to 10000; no rule was found that keeps the 45 and removes those two.
  * Which orbit verify_crt_invariants is meant to check. It checks here: the CRT map is a bijection, the nine classes
    are exactly the product {1,4,7} x {6,20,31}, {1,4,7} is one orbit of x4 by 9, and the braid's two turn cycles.

    python3 michael_prime_crt.py            prints the ledger to 10000 and the audit of each node
"""
from itertools import permutations

DR_CLASSES = (1, 4, 7)                       # by 9
MOD37_CLASSES = (6, 20, 31)                  # by 37
DR_MIRRORS = tuple(sorted(9 - d for d in DR_CLASSES))                       # (2, 5, 8)
MOD37_MIRRORS = tuple(sorted((10 ** 4 - 1 - r) % 37 for r in MOD37_CLASSES))  # (3, 15, 26), four-digit mirrors
BRAID_981 = tuple(sorted(int("".join(p)) for p in permutations("981")))     # (189, 198, 819, 891, 918, 981)


def digital_root(n):
    n = abs(int(n))
    return 0 if n == 0 else 1 + (n - 1) % 9


def crt(a9, a37):
    """the unique x in 0..332 with x = a9 by 9 and x = a37 by 37"""
    return (a9 * 37 * pow(37, -1, 9) + a37 * 9 * pow(9, -1, 37)) % 333


RESIDUES_333 = tuple(sorted(crt(a, b) for a in DR_CLASSES for b in MOD37_CLASSES))


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    f = 3
    while f * f <= n:
        if n % f == 0:
            return False
        f += 2
    return True


def generate_michael_primes(lo, hi):
    """every prime p, lo <= p <= hi, in one of the nine classes by 333"""
    for p in range(max(lo, 2), hi + 1):
        if p % 333 in RESIDUES_333 and is_prime(p):
            yield p


def mirror(n):
    return 10 ** len(str(n)) - 1 - n


def audit_node(n):
    m = mirror(n)
    return {
        "n": n,
        "width": len(str(n)),
        "valid_pm": is_prime(n) and n % 333 in RESIDUES_333,
        "r_333": n % 333,
        "mod_9": n % 9,
        "dr": digital_root(n),
        "mod_37": n % 37,
        "mirror": m,
        "mirror_mod_37": m % 37,
        "mirror_dr": digital_root(m),
        "vireon_13_coupling": 13 * n % 37,
    }


def verify_crt_invariants():
    pairs = {(x % 9, x % 37) for x in range(333)}
    checks = [
        len(pairs) == 333,                                                     # CRT: 333 classes <-> 9 x 37 pairs
        all(crt(x % 9, x % 37) == x for x in range(333)),
        RESIDUES_333 == (31, 43, 94, 142, 154, 205, 253, 265, 316),
        {(r % 9, r % 37) for r in RESIDUES_333} == {(a, b) for a in DR_CLASSES for b in MOD37_CLASSES},
        {1 * 4 ** k % 9 for k in range(3)} == set(DR_CLASSES) and 4 ** 3 % 9 == 1,  # {1,4,7}: one orbit of x4 by 9
        sum(BRAID_981) == 3996 == 108 * 37,
        sum((189, 891, 918)) == sum((198, 981, 819)) == 1998 == 6 * 333,
        all(digital_root(b) == 9 for b in BRAID_981),
        13 * 20 % 37 == 1,
    ]
    return all(checks)


if __name__ == "__main__":
    ledger = list(generate_michael_primes(1, 10000))
    print(len(ledger), "Michael primes to 10000:", ledger)
    print("residues by 333:", RESIDUES_333, " invariants:", verify_crt_invariants())
    for p in ledger:
        a = audit_node(p)
        print(p, "r333", a["r_333"], "dr", a["dr"], "mod37", a["mod_37"], "mirror", a["mirror"], a["mirror_mod_37"],
              a["mirror_dr"], "13-coupling", a["vireon_13_coupling"])
