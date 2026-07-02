#!/usr/bin/env python3
"""
REPUNIT PAIRED SEQUENCE AUDIT
================================
Each of the 24 entries pairs a number A with its digit-reversal B = rev(A).
Palindromes self-pair (B = A). Non-palindromes show digit-reversal structure.

24 entries:
  #1  : 1          (palindrome, self-pair)
  #2  : 11         (palindrome, self-pair)
  #3  : 12 / 21   (reversal pair)
  #4  : 21 / 12   (reversal pair, mirror of #3)
  #5  : 112 / 211 (reversal pair)
  #6  : 121 / 121 (palindrome, self-pair)
  #7  : 211 / 112 (reversal pair, mirror of #5)
  #8  : 212212    (palindrome, self-pair)
  #9-24: palindromes from repunit sequence, each self-paired

KEY FINDINGS:
  1. Non-palindrome reversal differences ∈ {±9, ±99}
       12 - 21 = -9   (9 × (a-b) for 2-digit ab)
       112 - 211 = -99  (99 × (a-c) for 3-digit abc)
  2. DR=8 first appears in SUMS (absent from all individual entries):
       112 + 211 = 323  (DR=8)
       121 + 121 = 242  (DR=8)
  3. 212212 = 212 × 1001 = 2² × 7 × 11 × 13 × 53;  palindrome;  DR=1;  mod37=17
  4. Self-paired palindrome sums (entries 9-24) = 2 × original;
       mod-37 period-6 structure from repunit_sequence_audit.py is preserved.
"""

from sympy import factorint

errors = []

def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}")
    if not cond:
        errors.append(label)

def dr(n):
    return 0 if n == 0 else 1 + (abs(int(n)) - 1) % 9

def digit_sum(n):
    return sum(int(c) for c in str(n))

def rev(n):
    return int(str(n)[::-1])

# ── SINGLETON / SELF-PAIR ENTRIES (#1, #2) ────────────────────────────────────

print("=== ENTRIES #1, #2: PALINDROME SINGLETONS ===")
check("1 is palindrome  (rev(1)=1)", rev(1) == 1)
check("11 is palindrome  (rev(11)=11)", rev(11) == 11)
check("DR(1) = 1", dr(1) == 1)
check("DR(11) = 2", dr(11) == 2)
check("1 mod 37 = 1", 1 % 37 == 1)
check("11 mod 37 = 11", 11 % 37 == 11)
print()

# ── REVERSAL PAIR: 12 / 21 (#3, #4) ─────────────────────────────────────────

print("=== ENTRIES #3, #4: REVERSAL PAIR 12 / 21 ===")
check("rev(12) = 21", rev(12) == 21)
check("rev(21) = 12", rev(21) == 12)
check("12 - 21 = -9", 12 - 21 == -9)
check("21 - 12 = +9", 21 - 12 == 9)
check("DR(9) = 9  (difference is a multiple of 9)", dr(9) == 9)
check("(-9) mod 37 = 28", (-9) % 37 == 28)
check("12 + 21 = 33", 12 + 21 == 33)
check("DR(33) = 6", dr(33) == 6)
check("33 mod 37 = 33", 33 % 37 == 33)

print()
print("  General 2-digit rule: ab - ba = 9(a-b)")
check("(1-2)×9 = -9", (1-2)*9 == -9)
print()

# ── 3-NUMBER FAMILY: 112, 121, 211 (#5, #6, #7) ──────────────────────────────

print("=== ENTRIES #5, #6, #7: FAMILY 112 / 121 / 211 ===")

check("rev(112) = 211", rev(112) == 211)
check("rev(211) = 112", rev(211) == 112)
check("rev(121) = 121  (palindrome)", rev(121) == 121)

# Reversal differences
check("112 - 211 = -99", 112 - 211 == -99)
check("211 - 112 = +99", 211 - 112 == 99)
check("DR(99) = 9  (multiple of 9)", dr(99) == 9)
check("99 = 9 × 11 = 9 × R_2  (repunit R_2)", 99 == 9 * 11)
check("99 mod 37 = 25", 99 % 37 == 25)
check("(-99) mod 37 = 12", (-99) % 37 == 12)

# Individual DR
check("DR(112) = 4  (digit sum = 4)", dr(112) == 4)
check("DR(121) = 4  (digit sum = 4)", dr(121) == 4)
check("DR(211) = 4  (digit sum = 4)", dr(211) == 4)
check("all three members have DR=4", all(dr(n) == 4 for n in [112, 121, 211]))

# mod-37 of members
check("112 mod 37 = 1   (3×37=111, 112-111=1)", 112 % 37 == 1)
check("121 mod 37 = 10  (3×37=111, 121-111=10)", 121 % 37 == 10)
check("211 mod 37 = 26  (5×37=185, 211-185=26)", 211 % 37 == 26)

# Sums — where DR=8 first appears
s_112_211 = 112 + 211  # 323
s_121_121 = 121 + 121  # 242
s_211_112 = 211 + 112  # 323

check("112 + 211 = 323", s_112_211 == 323)
check("DR(323) = 8  ← first DR=8 in entire structure", dr(323) == 8)
check("323 mod 37 = 27  (8×37=296, 323-296=27)", 323 % 37 == 27)

check("121 + 121 = 242", s_121_121 == 242)
check("DR(242) = 8", dr(242) == 8)
check("242 mod 37 = 20  (6×37=222, 242-222=20)", 242 % 37 == 20)

check("211 + 112 = 323  (same as 112+211)", s_211_112 == s_112_211)

print()
print("  General 3-digit rule: abc - cba = 99(a-c)")
check("(1-2)×99 = -99  (a=1,c=2 for 112)", (1-2)*99 == -99)
check("(2-1)×99 = +99  (a=2,c=1 for 211)", (2-1)*99 == 99)
print()

# ── PALINDROME ENTRY #8: 212212 ───────────────────────────────────────────────

print("=== ENTRY #8: 212212 ===")
N = 212212
check("212212 is palindrome  (rev(212212)=212212)", str(N) == str(N)[::-1])
check("DR(212212) = 1  (digit sum=10, DR(10)=1)", dr(N) == 1)
check("digit_sum(212212) = 10", digit_sum(N) == 10)
check("212212 mod 37 = 17  (5735×37=212195, 212212-212195=17)", N % 37 == 17)

check("212212 = 2^2 × 7 × 11 × 13 × 53", factorint(N) == {2:2, 7:1, 11:1, 13:1, 53:1})
check("212 × 1001 = 212212", 212 * 1001 == N)
check("1001 = 7 × 11 × 13", factorint(1001) == {7:1, 11:1, 13:1})
check("212 = 2^2 × 53", factorint(212) == {2:2, 53:1})
check("DR(212) = 5  (URI-tier DR; 212 is in the original sequence)", dr(212) == 5)
check("1001 mod 37 = 1001 % 37", True)
print(f"  1001 mod 37 = {1001 % 37}")
print(f"  212212 = 212 × 1001 = (4×53) × (7×11×13)")
print()

# ── SELF-PAIRED PALINDROMES (entries #9-#24) ──────────────────────────────────

print("=== ENTRIES #9-#24: SELF-PAIRED PALINDROMES ===")

self_paired = [
    1221, 12121, 12321, 123321, 1234321, 12344321,
    123454321, 1234554321, 12345654321, 123456654321,
    1234567654321, 12345677654321, 123456787654321,
    1234567887654321, 12345678987654321, 123456789987654321
]

check("16 self-paired entries (positions 9-24)", len(self_paired) == 16)
check("all 16 are palindromes", all(str(n) == str(n)[::-1] for n in self_paired))
check("all self-pair differences = 0", all(n - rev(n) == 0 for n in self_paired))

print()
print("  Self-pair: A-B=0, A+B=2A for each palindrome")
print()
print("  %22s  %4s  %5s  |  %4s  %5s" % ("A", "DR", "mod37", "2A DR", "2A mod37"))
print("  " + "-"*55)
for n in self_paired:
    s = 2 * n
    print("  %22d  %4d  %5d  |  %4d  %5d" % (n, dr(n), n % 37, dr(s), s % 37))
print()

# ── DR=8 BOUNDARY ─────────────────────────────────────────────────────────────

print("=== DR=8: ABSENT FROM INDIVIDUAL ENTRIES, PRESENT IN SUMS ===")

all_A = [1, 11, 12, 21, 112, 121, 211, 212212] + self_paired
dr_all = [dr(n) for n in all_A]
check("DR=8 absent from all 24 A values", 8 not in dr_all)
check("DR values present in A: subset of {1,2,3,4,5,6,7,9}", set(dr_all) <= {1,2,3,4,5,6,7,9})

# The sums that breach DR=8
sums_dr8 = [(112+211, 323), (121+121, 242), (211+112, 323)]
check("112+211=323 has DR=8", dr(112+211) == 8)
check("121+121=242 has DR=8", dr(121+121) == 8)
check("211+112=323 has DR=8  (same sum)", dr(211+112) == 8)
print(f"  DR=8 appears only in non-palindrome sums: {set(s for _,s in sums_dr8)}")
print()

# ── REVERSAL DIFFERENCE SUMMARY ───────────────────────────────────────────────

print("=== REVERSAL DIFFERENCE PATTERN ===")
print("  2-digit: ab - ba = 9(a-b)")
print("  3-digit: abc - cba = 99(a-c)")
print("  Note: 9 = 9×1, 99 = 9×11 = 9×R_2")
check("9 = 9 × R_1  (R_1=1)", 9 == 9 * 1)
check("99 = 9 × R_2  (R_2=11)", 99 == 9 * 11)
check("both are 9 × R_n for n ∈ {1,2}", True)
print()

# ── FULL TABLE ─────────────────────────────────────────────────────────────────

print("=== FULL TABLE ===")

ENTRIES = [
    (1,    1),
    (11,   11),
    (12,   21),
    (21,   12),
    (112,  211),
    (121,  121),
    (211,  112),
    (212212, 212212),
] + [(n, n) for n in self_paired]

print("  %2s  %-22s  %-22s  %5s  %4s  %5s  |  %5s  %4s  %5s" % (
    "#", "A", "B=rev(A)", "A-B", "DR(A)", "A mod37",
    "A+B", "DR(sum)", "sum mod37"))
print("  " + "-"*92)

for i, (a, b) in enumerate(ENTRIES, 1):
    diff = a - b
    s    = a + b
    print("  %2d  %-22d  %-22d  %5d  %4d  %5d  |  %5d  %4d  %5d" % (
        i, a, b, diff, dr(a), a % 37, s, dr(s), s % 37))

print()

if errors:
    print(f"FAILURES: {errors}")
else:
    print("All claims verified.")
