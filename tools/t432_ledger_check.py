"""Executable checks for math/ledgers/t432_bases_66_83.json (supplied 2026-09-28,
corrected). Every assertion is recomputed from definitions; nothing is read back.
Definitions: ring Z/m, m = b - 1; carry map f(r) = 1 - r; island = proper nonzero
ideal (d), 1 < d < m, d | m (count tau(m) - 2)."""
import json, sys
from math import gcd
def order(a, m):
    if gcd(a, m) != 1: return None
    k, x = 1, a % m
    while x != 1: x = x * a % m; k += 1
    return k
def idem(m): return [x for x in range(m) if x * x % m == x]
def fixed(m): return [r for r in range(m) if (1 - r) % m == r]
def nil_index(x, m): return next(k for k in range(1, 64) if pow(x, k, m) == 0)
def islands(m): return [d for d in range(2, m) if m % d == 0]
def v3(x):
    if x == 0: return 99
    k = 0
    while x % 3 == 0: x //= 3; k += 1
    return k
checks = {
 "A01": sum(gcd(u, 65) == 1 for u in range(65)) == 48,
 "A02": sum(order(u, 65) == 12 for u in range(65) if gcd(u, 65) == 1) == 24,
 "A03": idem(65) == [0, 1, 26, 40],
 "A04": fixed(65) == [33],
 "A05": nil_index(10, 80) == 4,
 "A06": idem(80) == [0, 1, 16, 65],
 "A07": order(57, 80) == 4, "A08": order(37, 80) == 4,
 "A09": fixed(80) == [], "A10": fixed(81) == [41],
 "A11": all(v3((1 - r - 41) % 81) == v3((r - 41) % 81) for r in range(81) if r != 41),
 "A12": order(2, 41) == 20,
 "A13": sorted({2 * x % 82 for x in range(82)}) == list(range(0, 82, 2)) and sorted(x % 41 for x in range(0, 82, 2)) == list(range(41)),
 "A14": 405 % 81 == 81 % 81, "A15": 405 % 243 != 81 % 243,
 "A16": 405 % 37 == 35, "A17": 405 % 79 == 10,
 "A18": sum(range(1, 10)) == 45, "A19": 9 * 45 == 405, "A20": 405 - 81 == 4 * 81,
 "X01_islands_base81": len(islands(80)) == 8,
 "X02_max_unit_order_base83": max(order(u, 82) for u in range(82) if gcd(u, 82) == 1) == 40,
 "X03_idempotent_identities_mod65": all(40 * y % 65 == y for y in range(0, 65, 5)) and all(26 * y % 65 == y for y in range(0, 65, 13)),
}
bad = [k for k, v in checks.items() if not v]
print(f"{len(checks) - len(bad)}/{len(checks)} checks pass" + (f"; FAILED: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
