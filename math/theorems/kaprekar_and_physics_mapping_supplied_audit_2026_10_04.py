# CLASS: AUDIT
"""
Audit of supplied blocks (2026-10-04): Kaprekar numbers 9, 45, 99; and a "physics mapping" of
the grid results. (The repeated "formal blueprint" block is audited in
formal_blueprint_supplied_audit_2026_10_04.py.) Mathematics only.

KAPREKAR -- CORRECT, with what the text left out
  K1 9^2 = 81, 8 + 1 = 9; 45^2 = 2025, 20 + 25 = 45; 99^2 = 9801, 98 + 01 = 99. These are
     Kaprekar numbers (a d-digit n whose square splits into a left part and a right part of d
     digits that add back to n).
  K2 The full list below 1000 is 1, 9, 45, 55, 99, 297, 703, 999 (OEIS A006886) -- 55 sits
     next to 45: 55^2 = 3025, 30 + 25 = 55.
  K3 Forced pieces: every all-nines number 10^d - 1 is Kaprekar, because
     (10^d - 1)^2 = (10^d - 2) * 10^d + 1, and (10^d - 2) + 1 = 10^d - 1. And the list pairs up
     to powers of ten: 45 + 55 = 100, 297 + 703 = 1000 (n and 10^d - n), for these entries.
  K4 Kaprekar's CONSTANT 6174 (the text's source [1]) is a different object: the fixed point of
     "sort digits descending minus ascending" for 4-digit numbers.
  K5 The script's print line for 99 shows 9**2 instead of 99**2 (display only; the check is right).

PHYSICS MAPPING -- not established, and partly wrong
  P1 "Global totals 23,328 and 89,100": 23,328 is on record (the 81-pair seed total); 89,100
     appears in no file in this repository.
  P2 "Net drift 0" in the script is (12 - 10) + (8 - 10) = 0, i.e. 12 + 8 = 2 x 10: four 3s plus
     four 2s is 20. Arithmetic, not a momentum law.
  P3 "Fission: the two fragments add back to the parent with no mass missing": physically
     false -- fission products weigh LESS than the parent; the missing mass is the energy
     released (E = mc^2). Nucleon number and charge are what is conserved.
  P4 "The digit sum 10 at 82 is the discharge threshold": 81 + 1 = 82 has no carry
     (rotation_3223_and_82_boundary_supplied_audit_2026_10_04.py).
  P5 "The anti-diagonal split proves a magnetic or structural alignment": the anti-diagonal of a
     left-rotation stack is four copies of the base row's last entry
     (fixed_grip_and_disproof_tests_supplied_audit_2026_10_04.py) -- a property of the
     construction, not evidence about any physical system.
FALSIFICATION: any assertion failing.
"""


def kaprekar(n):
    d = len(str(n))
    left, right = divmod(n * n, 10 ** d)
    return right > 0 and left + right == n or n == 1


ks = [n for n in range(1, 1000) if kaprekar(n)]
assert ks == [1, 9, 45, 55, 99, 297, 703, 999]                                        # K2
assert (81 // 10 + 81 % 10, 2025 // 100 + 2025 % 100, 9801 // 100 + 9801 % 100) == (9, 45, 99)  # K1
assert all((10 ** d - 1) ** 2 == (10 ** d - 2) * 10 ** d + 1 and kaprekar(10 ** d - 1) for d in range(1, 9))  # K3
assert 45 + 55 == 100 and 297 + 703 == 1000
assert int("".join(sorted("6174", reverse=True))) - int("".join(sorted("6174"))) == 6174   # K4
assert (12 - 10) + (8 - 10) == 0 and 4 * 3 + 4 * 2 == 2 * 10                             # P2
