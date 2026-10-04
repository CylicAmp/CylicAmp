# CLASS: AUDIT
"""
Audit of supplied text (2026-10-04): "10 columns were an error; the true ceiling is 8
columns (99,999,999) under the fives filter and 9 under the nines filter". Mathematics only.

CORRECT
  E1 3 x 33,333,333 = 99,999,999; digit sum 72, root 9; 72 = 45 + 27 (one full 45-container,
     27 left). Adding 1 gives 100,000,000: 8 carries, all eight columns to 0, digit sum
     72 + 1 - 9*8 = 1 (T432, Kummer's identity). In the owner's drain notation that is one
     drain recorded by the leading 1 (casting_out_tens_drain_system.py).

WRONG
  E2 "999,999,999 has digit sum 27 -> 9": nine nines sum to 81 (root 9), not 27.
  E3 "The lopsided 1,980 vs 3,960 node split found in the audit": no audit in this repository
     reports those numbers. The mod-5 node counts actually recorded
     (grip_81_and_one_x_supplied_audit_2026_10_04.py, T4) are 504 / 1,656 / 1,008.
  E4 "Adding a 9th and 10th column makes the mod-5 counts fracture": a number's remainder mod 5
     depends only on its last digit, so the number of columns cannot change it. The 4 + 4
     high/low split is the owner's labelling of 8 digits, not a mod-5 property.
FALSIFICATION: any assertion failing.
"""
ds = lambda n: sum(map(int, str(n)))
n = 99_999_999
assert 3 * 33_333_333 == n and ds(n) == 72 and 72 % 9 == 0 and 72 == 45 + 27               # E1
assert n + 1 == 10 ** 8 and ds(n + 1) == ds(n) + 1 - 9 * 8 == 1
assert ds(999_999_999) == 81 != 27                                                         # E2
assert all(m % 5 == (m % 10) % 5 for m in (12345678, 912345678, 1234567890, 99_999_999))   # E4
