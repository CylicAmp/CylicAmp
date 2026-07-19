"""
Twin prime lattice: recursive harmonic summation over T_pairs.

DR: Z>=0 -> {0,...,9}
f(n) = (137 * n) % 37
ANCHORS = {4, 9, 25, 30}
TARGETS  = {3, 12, 21, 30}

(29, 31): mid=30 in ANCHORS, f(30)=3 in TARGETS.
"""

ANCHORS = {4, 9, 25, 30}
TARGETS  = {3, 12, 21, 30}


def digital_root(n: int) -> int:
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


def recursive_harmonic_summation(p: int, q: int) -> dict:
    total = p + q
    mid   = total // 2

    n, chain = total, [total]
    while n >= 10:
        n = sum(int(d) for d in str(n))
        chain.append(n)

    return {
        "sum":         total,
        "dr_p":        digital_root(p),
        "dr_q":        digital_root(q),
        "dr_chain":    chain,
        "terminal_dr": chain[-1],
        "midpoint":    mid,
        "mid_dr":      digital_root(mid),
        "f_mid":       (137 * mid) % 37,
    }


def process_twin_prime_lattice(twin_pairs):
    results = {}
    for pair in twin_pairs:
        results[pair] = recursive_harmonic_summation(pair[0], pair[1])
    return results


T_pairs = [(11, 13), (17, 19), (29, 31), (41, 43), (59, 61), (71, 73)]
