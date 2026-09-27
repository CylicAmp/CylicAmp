"""
prime_dr_append_audit.py

Operation: take each two-digit prime p, append DR(p) as the last digit.
n = p * 10 + DR(p)

Layers:
  Layer 1: two-digit primes → append DR → 3-digit numbers
  Layer 2: layer-1 results  → append DR → 4-digit numbers

Every factorization is computed and hardcoded. Every claim is asserted.
Nothing is taken on faith.

─────────────────────────────────────────────────────────────────
LAYER 1 RESULTS (p → p*10+DR(p)):
  112=2^4*7  134=2*67  178=2*89  191=prime
  235=5*47   292=2^2*73  314=2*157  371=7*53
  415=5*83   437=19*23   472=2^3*59  538=2*269
  595=5*7*17  617=prime  674=2*337  718=2*359
  731=17*43  797=prime  832=2^6*13  898=2*449
  977=prime

  Primes: 191, 617, 797, 977  (4 of 21)
  Fold-back (factors in original two-digit prime list):
    437  = 19 × 23
    731  = 17 × 43

LAYER 2 RESULTS (layer-1 n → n*10+DR(n)):
  1124=2^2*281   1348=2^2*337  1787=prime    1912=2^3*239
  2351=prime     2924=2^2*17*43  3148=2^2*787  3712=2^7*29
  4151=7*593     4375=5^4*7    4724=2^2*1181  5387=prime
  5951=11*541    6175=5^2*13*19  6748=2^2*7*241  7187=prime
  7312=2^4*457   7975=5^2*11*29  8324=2^2*2081  8987=11*19*43
  9775=5^2*17*23

  Primes: 1787, 2351, 5387, 7187  (4 of 21)
  Fold-back (factors in original two-digit prime list):
    2924 = 4 × 17 × 43
    3712 = 128 × 29
    5951 = 11 × 541
    6175 = 25 × 13 × 19
    7975 = 25 × 11 × 29
    8987 = 11 × 19 × 43
    9775 = 25 × 17 × 23
─────────────────────────────────────────────────────────────────
"""

from sympy import isprime, factorint

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = n % 9
    return r if r else 9


def append_dr(n):
    return n * 10 + dr(n)


def factors_set(n):
    return set(factorint(n).keys())


# ── Two-digit primes ──────────────────────────────────────────────────────────

TWO_DIGIT_PRIMES = [
    11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
    47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
]

check(len(TWO_DIGIT_PRIMES) == 21, "two-digit prime count", len(TWO_DIGIT_PRIMES), 21)
check(all(isprime(p) for p in TWO_DIGIT_PRIMES), "all are prime", True, True)
check(TWO_DIGIT_PRIMES[0]  == 11, "first", TWO_DIGIT_PRIMES[0],  11)
check(TWO_DIGIT_PRIMES[-1] == 97, "last",  TWO_DIGIT_PRIMES[-1], 97)

TWO_DIGIT_SET = set(TWO_DIGIT_PRIMES)


# ── DR values ─────────────────────────────────────────────────────────────────

EXPECTED_DR = {
    11:2, 13:4, 17:8, 19:1, 23:5, 29:2, 31:4, 37:1, 41:5, 43:7,
    47:2, 53:8, 59:5, 61:7, 67:4, 71:8, 73:1, 79:7, 83:2, 89:8, 97:7,
}

for p, expected in EXPECTED_DR.items():
    check(dr(p) == expected, f"DR({p})", dr(p), expected)


# ── Layer 1: p → p*10+DR(p) ──────────────────────────────────────────────────

LAYER1 = {p: append_dr(p) for p in TWO_DIGIT_PRIMES}

LAYER1_EXPECTED = {
    11: 112,  13: 134,  17: 178,  19: 191,  23: 235,
    29: 292,  31: 314,  37: 371,  41: 415,  43: 437,
    47: 472,  53: 538,  59: 595,  61: 617,  67: 674,
    71: 718,  73: 731,  79: 797,  83: 832,  89: 898,
    97: 977,
}

for p, expected in LAYER1_EXPECTED.items():
    check(LAYER1[p] == expected, f"layer1({p})", LAYER1[p], expected)

# Factorizations — computed and hardcoded, both must agree
LAYER1_FACTORS = {
    112: {2: 4, 7: 1},
    134: {2: 1, 67: 1},
    178: {2: 1, 89: 1},
    191: {191: 1},
    235: {5: 1, 47: 1},
    292: {2: 2, 73: 1},
    314: {2: 1, 157: 1},
    371: {7: 1, 53: 1},
    415: {5: 1, 83: 1},
    437: {19: 1, 23: 1},
    472: {2: 3, 59: 1},
    538: {2: 1, 269: 1},
    595: {5: 1, 7: 1, 17: 1},
    617: {617: 1},
    674: {2: 1, 337: 1},
    718: {2: 1, 359: 1},
    731: {17: 1, 43: 1},
    797: {797: 1},
    832: {2: 6, 13: 1},
    898: {2: 1, 449: 1},
    977: {977: 1},
}

for n, expected_f in LAYER1_FACTORS.items():
    actual_f = factorint(n)
    check(actual_f == expected_f, f"factors({n})", actual_f, expected_f)

# Primes in layer 1
L1_PRIMES = [n for n in LAYER1.values() if isprime(n)]
check(sorted(L1_PRIMES) == [191, 617, 797, 977], "layer1 primes", sorted(L1_PRIMES), [191, 617, 797, 977])

# Fold-back: factors inside two-digit prime list
check(factors_set(437) == {19, 23}, "437=19×23 fold", factors_set(437), {19, 23})
check(factors_set(731) == {17, 43}, "731=17×43 fold", factors_set(731), {17, 43})
check(19 in TWO_DIGIT_SET and 23 in TWO_DIGIT_SET, "19,23 in source", True, True)
check(17 in TWO_DIGIT_SET and 43 in TWO_DIGIT_SET, "17,43 in source", True, True)


# ── Layer 2: layer-1 results → append DR → factorize ─────────────────────────

LAYER2 = {n: append_dr(n) for n in sorted(LAYER1.values())}

LAYER2_EXPECTED = {
    112: 1124,  134: 1348,  178: 1787,  191: 1912,  235: 2351,
    292: 2924,  314: 3148,  371: 3712,  415: 4151,  437: 4375,
    472: 4724,  538: 5387,  595: 5951,  617: 6175,  674: 6748,
    718: 7187,  731: 7312,  797: 7975,  832: 8324,  898: 8987,
    977: 9775,
}

for n, expected in LAYER2_EXPECTED.items():
    check(LAYER2[n] == expected, f"layer2({n})", LAYER2[n], expected)

LAYER2_FACTORS = {
    1124: {2: 2, 281: 1},
    1348: {2: 2, 337: 1},
    1787: {1787: 1},
    1912: {2: 3, 239: 1},
    2351: {2351: 1},
    2924: {2: 2, 17: 1, 43: 1},
    3148: {2: 2, 787: 1},
    3712: {2: 7, 29: 1},
    4151: {7: 1, 593: 1},
    4375: {5: 4, 7: 1},
    4724: {2: 2, 1181: 1},
    5387: {5387: 1},
    5951: {11: 1, 541: 1},
    6175: {5: 2, 13: 1, 19: 1},
    6748: {2: 2, 7: 1, 241: 1},
    7187: {7187: 1},
    7312: {2: 4, 457: 1},
    7975: {5: 2, 11: 1, 29: 1},
    8324: {2: 2, 2081: 1},
    8987: {11: 1, 19: 1, 43: 1},
    9775: {5: 2, 17: 1, 23: 1},
}

for n, expected_f in LAYER2_FACTORS.items():
    actual_f = factorint(n)
    check(actual_f == expected_f, f"factors({n})", actual_f, expected_f)

# Primes in layer 2
L2_PRIMES = [n for n in LAYER2.values() if isprime(n)]
check(sorted(L2_PRIMES) == [1787, 2351, 5387, 7187], "layer2 primes", sorted(L2_PRIMES), [1787, 2351, 5387, 7187])

# Fold-back in layer 2
check(factors_set(2924) == {2, 17, 43},     "2924=4×17×43",    factors_set(2924), {2, 17, 43})
check(factors_set(6175) == {5, 13, 19},     "6175=25×13×19",   factors_set(6175), {5, 13, 19})
check(factors_set(8987) == {11, 19, 43},    "8987=11×19×43",   factors_set(8987), {11, 19, 43})
check(factors_set(9775) == {5, 17, 23},     "9775=25×17×23",   factors_set(9775), {5, 17, 23})
check(factors_set(7975) == {5, 11, 29},     "7975=25×11×29",   factors_set(7975), {5, 11, 29})


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Prime DR-Append Audit: Layer 1 and Layer 2")
    print("=" * 62)

    print(f"\n── Layer 1: p → p*10+DR(p) ──")
    print(f"  {'p':>4}  DR  {'n':>5}  factored")
    for p in TWO_DIGIT_PRIMES:
        n = LAYER1[p]
        f = LAYER1_FACTORS[n]
        parts = [f"{b}^{e}" if e > 1 else str(b) for b, e in sorted(f.items())]
        fac = " * ".join(parts) if not isprime(n) else f"{n} prime"
        print(f"  {p:>4}  {dr(p)}   {n:>5}  {fac}")

    print(f"\n  Primes: {sorted(L1_PRIMES)}")
    print(f"  Fold-back: 437=19×23, 731=17×43  (factors from source list)")

    print(f"\n── Layer 2: n → n*10+DR(n) ──")
    print(f"  {'n':>5}  DR  {'n2':>6}  factored")
    for n in sorted(LAYER2_EXPECTED):
        n2 = LAYER2[n]
        f = LAYER2_FACTORS[n2]
        parts = [f"{b}^{e}" if e > 1 else str(b) for b, e in sorted(f.items())]
        fac = " * ".join(parts) if not isprime(n2) else f"{n2} prime"
        print(f"  {n:>5}  {dr(n)}   {n2:>6}  {fac}")

    print(f"\n  Primes: {sorted(L2_PRIMES)}")
    print(f"  Fold-back (two-digit prime factors):")
    fold2 = {n2: factors_set(n2) & TWO_DIGIT_SET
             for n2 in LAYER2.values()
             if factors_set(n2) & TWO_DIGIT_SET}
    for n2, folds in sorted(fold2.items()):
        print(f"    {n2} ← {sorted(folds)}")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
