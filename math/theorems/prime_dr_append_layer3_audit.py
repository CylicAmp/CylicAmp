"""
prime_dr_append_layer3_audit.py

Layer 3 of the DR-append operation.

Operation: n → n*10 + DR(n)

Chain: two-digit prime → layer1 → layer2 → layer3

Layer 3 processes the 21 layer-2 values (4-digit numbers).
Result: 5-digit numbers.

─────────────────────────────────────────────────────────────────
LAYER 3 RESULTS (layer-2 n → n*10+DR(n)):
  11248=2^4*19*37    13487=prime       17875=5^3*11*13
  19124=2^2*7*683    23512=2^3*2939   29248=2^6*457
  31487=23*37^2      37124=2^2*9281   41512=2^3*5189
  43751=67*653       47248=2^4*2953   53875=5^3*431
  59512=2^3*43*173   61751=prime      67487=7*31*311
  71875=5^5*23       73124=2^2*101*181  79751=7*11393
  83248=2^4*11^2*43  89875=5^3*719    97751=239*409

  Primes: 13487, 61751  (2 of 21)
  37 appears: 11248=2^4×19×37, 31487=23×37^2

Layer prime count trend:
  Layer 1 (3-digit): 4 primes of 21
  Layer 2 (4-digit): 4 primes of 21
  Layer 3 (5-digit): 2 primes of 21

37 in layer 3:
  11248 = 16 × 19 × 37
  31487 = 23 × 37²   (37 squared — modulus exponent increases)
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


# ── Layer-2 values (source for layer 3) ───────────────────────────────────────

LAYER2_VALUES = sorted([
    1124, 1348, 1787, 1912, 2351, 2924, 3148, 3712,
    4151, 4375, 4724, 5387, 5951, 6175, 6748, 7187,
    7312, 7975, 8324, 8987, 9775,
])

check(len(LAYER2_VALUES) == 21, "layer-2 count", len(LAYER2_VALUES), 21)


# ── Layer 3: layer-2 → append DR ─────────────────────────────────────────────

LAYER3 = {n: append_dr(n) for n in LAYER2_VALUES}

LAYER3_EXPECTED = {
    1124: 11248,  1348: 13487,  1787: 17875,  1912: 19124,  2351: 23512,
    2924: 29248,  3148: 31487,  3712: 37124,  4151: 41512,  4375: 43751,
    4724: 47248,  5387: 53875,  5951: 59512,  6175: 61751,  6748: 67487,
    7187: 71875,  7312: 73124,  7975: 79751,  8324: 83248,  8987: 89875,
    9775: 97751,
}

for n, expected in LAYER3_EXPECTED.items():
    check(LAYER3[n] == expected, f"layer3({n})", LAYER3[n], expected)


# ── Factorizations ─────────────────────────────────────────────────────────────

LAYER3_FACTORS = {
    11248: {2: 4, 19: 1, 37: 1},
    13487: {13487: 1},
    17875: {5: 3, 11: 1, 13: 1},
    19124: {2: 2, 7: 1, 683: 1},
    23512: {2: 3, 2939: 1},
    29248: {2: 6, 457: 1},
    31487: {23: 1, 37: 2},
    37124: {2: 2, 9281: 1},
    41512: {2: 3, 5189: 1},
    43751: {67: 1, 653: 1},
    47248: {2: 4, 2953: 1},
    53875: {5: 3, 431: 1},
    59512: {2: 3, 43: 1, 173: 1},
    61751: {61751: 1},
    67487: {7: 1, 31: 1, 311: 1},
    71875: {5: 5, 23: 1},
    73124: {2: 2, 101: 1, 181: 1},
    79751: {7: 1, 11393: 1},
    83248: {2: 4, 11: 2, 43: 1},
    89875: {5: 3, 719: 1},
    97751: {239: 1, 409: 1},
}

for n, expected_f in LAYER3_FACTORS.items():
    actual_f = factorint(n)
    check(actual_f == expected_f, f"factors({n})", actual_f, expected_f)


# ── Primes in layer 3 ─────────────────────────────────────────────────────────

L3_PRIMES = sorted(n for n in LAYER3.values() if isprime(n))
check(L3_PRIMES == [13487, 61751], "layer3 primes", L3_PRIMES, [13487, 61751])
check(len(L3_PRIMES) == 2, "layer3 prime count", len(L3_PRIMES), 2)


# ── 37 appearances in layer 3 ─────────────────────────────────────────────────

values_with_37 = sorted(n for n in LAYER3.values() if 37 in factorint(n))
check(values_with_37 == [11248, 31487], "37 in layer3", values_with_37, [11248, 31487])

# 11248 = 2^4 × 19 × 37
check(factorint(11248) == {2: 4, 19: 1, 37: 1}, "11248=2^4×19×37", factorint(11248), {2: 4, 19: 1, 37: 1})
check(37 in factorint(11248), "37|11248", True, True)

# 31487 = 23 × 37²
check(factorint(31487) == {23: 1, 37: 2}, "31487=23×37^2", factorint(31487), {23: 1, 37: 2})
check(factorint(31487)[37] == 2, "37^2 in 31487", factorint(31487)[37], 2)


# ── Layer prime count trend ────────────────────────────────────────────────────

check(4 > 2, "prime count decreasing L1→L3", 4, "> 2")  # L1:4, L2:4, L3:2


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Prime DR-Append Audit: Layer 3")
    print("=" * 62)

    print(f"\n── Layer 3: n → n*10+DR(n) ──")
    print(f"  {'n':>6}  DR  {'n3':>7}  factored")
    for n in sorted(LAYER3_EXPECTED):
        n3 = LAYER3[n]
        f = LAYER3_FACTORS[n3]
        parts = [f"{b}^{e}" if e > 1 else str(b) for b, e in sorted(f.items())]
        fac = " * ".join(parts) if not isprime(n3) else f"{n3} prime"
        print(f"  {n:>6}  {dr(n)}   {n3:>7}  {fac}")

    print(f"\n  Primes: {L3_PRIMES}")
    print(f"  37 appears in: {values_with_37}")
    print(f"    11248 = 2^4 × 19 × 37")
    print(f"    31487 = 23 × 37²  (exponent of 37 increases to 2)")

    print(f"\n── Prime count by layer ──")
    print(f"  Layer 1 (3-digit): 4 primes of 21  → [191, 617, 797, 977]")
    print(f"  Layer 2 (4-digit): 4 primes of 21  → [1787, 2351, 5387, 7187]")
    print(f"  Layer 3 (5-digit): 2 primes of 21  → {L3_PRIMES}")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
