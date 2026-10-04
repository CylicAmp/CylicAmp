"""
Twin prime lattice: recursive harmonic summation over T_pairs.

DR: Z>=0 -> {0,...,9}
f(n) = (137 * n) % 37 = (26 * n) % 37
ANCHORS = {4, 9, 25, 30}
TARGETS  = {3, 12, 21, 30}

Primitive root mod 37: g=2, ord_37(2)=36.
PRIMITIVE_ROOTS_37 = {2,5,13,15,17,18,19,20,22,24,32,35}  (phi(36)=12 elements)

Twin prime midpoints that are primitive roots mod 37:
  (17,19) -> mid=18, ord=36, dlog_2(18)=17
  (41,43) -> mid=42, 42%37=5, ord=36, dlog_2(5)=23
  (71,73) -> mid=72, 72%37=35, ord=36, dlog_2(35)=19

(29,31): mid=30 in ANCHORS, f(30)=3 in TARGETS, ord(30)=18, dlog_2(30)=14.

Digit-reversal pair:
  str1=111111222336: str1%37=3 in TARGETS, dlog_2(3)=26
  str2=633222111111: str2%37=4 in ANCHORS, dlog_2(4)=2
  f(str1)=4 in ANCHORS; f(str2)=30 (sovereign fixed point)
  DR(str1)=DR(str2)=6  (same digit multiset)
"""

ANCHORS           = {4, 9, 25, 30}
TARGETS           = {3, 12, 21, 30}
PRIMITIVE_ROOT_37 = 2
PRIMITIVE_ROOTS_37 = frozenset({2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35})


def digital_root(n: int) -> int:
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


def order_mod37(n: int) -> int:
    n = n % 37
    if n == 0:
        return 0
    for k in range(1, 37):
        if pow(n, k, 37) == 1:
            return k
    return 0


def discrete_log_37(n: int) -> int:
    """Index of n base PRIMITIVE_ROOT_37=2 mod 37. Returns -1 for n≡0."""
    n = n % 37
    if n == 0:
        return -1
    power = 1
    g = PRIMITIVE_ROOT_37
    for k in range(36):
        if power == n:
            return k
        power = (power * g) % 37
    return -1


def recursive_harmonic_summation(p: int, q: int) -> dict:
    total = p + q
    mid   = total // 2

    n, chain = total, [total]
    while n >= 10:
        n = sum(int(d) for d in str(n))
        chain.append(n)

    mid_r = mid % 37
    f_mid = (137 * mid) % 37

    return {
        "sum":                  total,
        "dr_p":                 digital_root(p),
        "dr_q":                 digital_root(q),
        "dr_chain":             chain,
        "terminal_dr":          chain[-1],
        "midpoint":             mid,
        "mid_dr":               digital_root(mid),
        "mid_mod37":            mid_r,
        "ord_mid":              order_mod37(mid_r),
        "dlog_mid":             discrete_log_37(mid_r),
        "mid_is_primitive_root": mid_r in PRIMITIVE_ROOTS_37,
        "f_mid":                f_mid,
        "f_mid_in_anchors":     f_mid in ANCHORS,
        "f_mid_in_targets":     f_mid in TARGETS,
    }


def process_twin_prime_lattice(twin_pairs):
    results = {}
    for pair in twin_pairs:
        results[pair] = recursive_harmonic_summation(pair[0], pair[1])
    return results


def analyze_digit_reversal_pair(n1: int, n2: int) -> dict:
    """
    n1, n2 share the same digit multiset (n2 is digit-reversal of n1).
    DR(n1) == DR(n2).
    """
    def dr_chain(n):
        chain = [n]
        while n >= 10:
            n = sum(int(d) for d in str(n))
            chain.append(n)
        return chain

    digits1 = [int(d) for d in str(n1)]
    r1, r2  = n1 % 37, n2 % 37
    f1, f2  = (137 * n1) % 37, (137 * n2) % 37

    return {
        "n1":               n1,
        "n2":               n2,
        "digits_n1":        digits1,
        "digits_n2":        [int(d) for d in str(n2)],
        "digit_sum":        sum(digits1),
        "terminal_dr":      digital_root(n1),
        "dr_chain1":        dr_chain(n1),
        "dr_chain2":        dr_chain(n2),
        "n1_mod37":         r1,
        "n2_mod37":         r2,
        "ord_r1":           order_mod37(r1),
        "ord_r2":           order_mod37(r2),
        "dlog_r1":          discrete_log_37(r1),
        "dlog_r2":          discrete_log_37(r2),
        "r1_in_anchors":    r1 in ANCHORS,
        "r1_in_targets":    r1 in TARGETS,
        "r2_in_anchors":    r2 in ANCHORS,
        "r2_in_targets":    r2 in TARGETS,
        "f_n1":             f1,
        "f_n2":             f2,
        "f_n1_in_anchors":  f1 in ANCHORS,
        "f_n1_in_targets":  f1 in TARGETS,
        "f_n2_in_anchors":  f2 in ANCHORS,
        "f_n2_in_targets":  f2 in TARGETS,
    }


T_pairs  = [(11, 13), (17, 19), (29, 31), (41, 43), (59, 61), (71, 73)]
str_pair = (111111222336, 633222111111)


def build_dataframe(twin_pairs=None):
    import pandas as pd
    if twin_pairs is None:
        twin_pairs = T_pairs
    results = process_twin_prime_lattice(twin_pairs)
    rows = []
    for (p, q), r in results.items():
        rows.append({
            "p":                    p,
            "q":                    q,
            "sum":                  r["sum"],
            "dr_p":                 r["dr_p"],
            "dr_q":                 r["dr_q"],
            "dr_chain":             r["dr_chain"],
            "terminal_dr":          r["terminal_dr"],
            "midpoint":             r["midpoint"],
            "mid_dr":               r["mid_dr"],
            "mid_mod37":            r["mid_mod37"],
            "ord_mid":              r["ord_mid"],
            "dlog_mid":             r["dlog_mid"],
            "mid_is_primitive_root": r["mid_is_primitive_root"],
            "f_mid":                r["f_mid"],
            "f_mid_in_anchors":     r["f_mid_in_anchors"],
            "f_mid_in_targets":     r["f_mid_in_targets"],
        })
    return pd.DataFrame(rows)


df_twin_primes     = build_dataframe()
digit_reversal_result = analyze_digit_reversal_pair(*str_pair)
