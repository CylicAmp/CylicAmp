# CLASS: AUDIT
"""
Pasted "Sharpened Core: The Stripped Mathematical Engine" on V = [6, 10, 12, 12, 99] (2026-11-28). Audit on arrival.

RIGHT:
  paths: 139 = p_34, 31 = p_11, 13; each -> 4 (forced: a sum, its digit sum and its sum by 9 share the root).
  34 - 11 = 23 = p_9, and I AM = 9 + 1 + 13 = 23 (pasted_unified_handoff_ledger_audit_2026_11_17.py).
  V by 37 = [6, 10, 12, 12, 25]; ord(10) = 3, ord(25) = 18.
  product 6 x 10 x 12 x 12 x 25 = 216000 = 216 x 1000; 1000 leaves 1 by 37, so the product leaves 216 -> 31.
    That it equals Path B's 31 is a match of values (one is a product by 37, the other a digit sum), not an identity.
  phi(31) = 30 -> 3, phi(139) = 138 -> 12 -> 3. Forced: both primes have root 4, so p - 1 has root 3.
WRONG (each changes a value):
  ord_37(6) = 4, not 36 (6 x 6 = 36 leaves -1, so 6^4 leaves 1);  ord_37(12) = 9, not 36 (12^3 leaves 26, 12^9 leaves 1).
  tau(75) = 12 again: tau(75) = 6 (pasted_phi_inversion_ledger_correction_2026_11_28.py).
STILL ASKED: the t983 matrix; the "19 primes <-> period 104" row names no link to check.

FALSIFICATION: any assertion failing.
"""
from sympy import divisor_count, n_order, prime, totient

V = [6, 10, 12, 12, 99]
dr = lambda n: 1 + (n - 1) % 9
assert sum(V) == 139 == prime(34) and sum(int(c) for v in V for c in str(v)) == 31 == prime(11) and sum(v % 9 for v in V) == 13
assert dr(139) == dr(31) == dr(13) == 4 and 34 - 11 == 23 == prime(9) and 9 + 1 + 13 == 23
assert [v % 37 for v in V] == [6, 10, 12, 12, 25]
assert [n_order(a, 37) for a in (6, 10, 12, 25)] == [4, 3, 9, 18]                     # paste: 36, 3, 36, 18
assert 6 * 10 * 12 * 12 * 25 == 216000 == 216 * 1000 and pow(10, 3, 37) == 1 and 216000 % 37 == 216 % 37 == 31
assert (60 % 37, 144 % 37, 23 * 33 % 37, 19 * 25 % 37) == (23, 33, 19, 31)
assert (int(totient(31)), int(totient(139))) == (30, 138) and dr(30) == dr(138) == 3 and 31 % 9 == 139 % 9 == 4
assert divisor_count(75) == 6

if __name__ == "__main__":
    print("sharpened core: sums, 23, product 31 right; ord(6) = 4 and ord(12) = 9 (not 36); tau(75) = 6")
