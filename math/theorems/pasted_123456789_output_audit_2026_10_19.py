# CLASS: AUDIT
"""
A pasted output about 123456789 (owner_work #354, 2026-10-19). The message is the printed lines of a script and a
"Step-by-Step Output Derivation" written in another tool's style; the script itself is not in the message.
Nothing below is put in the owner's mouth.

THE PASTED LINES, and what each was checked against:
  [3, 3, 3607, 3803]                    RIGHT   123456789 = 3x3x3607x3803
  8 987654312                           RIGHT   8x123456789 = 987654312
  9 1111111101                          RIGHT   9x123456789 = 1111111101
  123456790012345679                    WRONG as labelled: the derivation says 111111111**2, which is 12345678987654321.
                                        123456790012345679 = 12345679 x 10000000001 = 37x101x3541x27961x333667
  1 123456789 9 45 9                    RIGHT   length 9, digit sum 45, root 9
  2 12469135679012345 17 81 9           WRONG   the printed number has length 17, digit sum 68, root 5
  3 123580246790123456789 21 81 9       WRONG   length 21, digit sum 92, root 2
  4 123469135790123456789012345 25 117 9  WRONG length 27, digit sum 110, root 2
        A number is divisible by 9 exactly when its root is 9. The three numbers leave 5, 2, 2 on division by 9,
        so no definition of N(k) can make these numbers have root 9: the numbers and the printed lengths, sums and
        roots did not come from one run. "base sum evaluates to 11335577890011223 ..." in the derivation is not a
        definition. I CAN'T CHECK what N(k) is: the code is not in the paste.
  1368 18, 1566, odds evens 25 20      RIGHT   123+456+789=1368=1+3+6+8+... 1+3+6+8=18 ; 123+654+789=1566, 1+5+6+6=18=9 ;
                                                1+3+5+7+9=25, 2+4+6+8=20
  123456790                             RIGHT   (10^10-10)//81 = 123456790, and 123456790 - 1 = 123456789
  12345688                              CAN'T CHECK: 12345688 is not 123456790-1, not 12345678 (= sum d x 10^(8-d), d = 1..8,
                                        12345678+10 = 12345688); the line it belongs to is not in the paste.
  123456789                             RIGHT   sum of d x 10^(9-d), d = 1..9
  the derivation's note that 111111111^2 "is not the standard palindrome 12345678987654321": WRONG, it is.

CONNECTIONS (the owner's lines and files):
  123+456+789 = 1368 = 1369-1 = 37x37-1 = 36x38. 1000 = 1 mod 999, so 123456789 = 1368 = 369 mod 999 and
    123456789 = 36 mod 37 (369 = 370-1 = 10x37-1): the owner's 369 (#268), NEG_H 36.
  8x123456789+9 = 987654321 and 9x123456789+10 = 1111111111 (987654312+9, 1111111101+10).
  123456789 + 1 = 123456790 is the repeating block of 10/81 = 0.123456790 123456790 ...; the owner's +1 "to begin again".
  1/81 = 0.012345679 012345679 ... has no 8 (the 8 is 10-2); 1/9801 has no 98; 1/998001 has no 998 (math/theorems/
    repetend_998001_audit_2026_10_19.py): 1/(10^k-1)^2 skips 10^k-2 for k = 1, 2, 3 (long division below).

FALSIFICATION: any assertion failing.
"""
from sympy import factorint


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


n = 123456789
assert factorint(n) == {3: 2, 3607: 1, 3803: 1} and 9 * 3607 * 3803 == n
assert (8 * n, 9 * n) == (987654312, 1111111101) and 8 * n + 9 == 987654321 and 9 * n + 10 == 1111111111
assert sum(d * 10 ** (9 - d) for d in range(1, 10)) == n

T3 = 123456790012345679
assert 111111111 ** 2 == 12345678987654321 and T3 != 111111111 ** 2
assert T3 == 12345679 * (10 ** 10 + 1) and factorint(T3) == {37: 1, 101: 1, 3541: 1, 27961: 1, 333667: 1}
assert 12345679 == (10 ** 9 - 1) // 81 == 37 * 333667 and 12345679 * 9 == 111111111

printed = {2: (12469135679012345, 17, 81, 9), 3: (123580246790123456789, 21, 81, 9), 4: (123469135790123456789012345, 25, 117, 9)}
actual = {k: (len(str(v)), sum(map(int, str(v))), dr(v)) for k, (v, *_rest) in printed.items()}
assert actual == {2: (17, 68, 5), 3: (21, 92, 2), 4: (27, 110, 2)}
assert all(actual[k] != printed[k][1:] for k in printed)
assert all(printed[k][0] % 9 != 0 for k in printed) and all(dr(printed[k][0]) != 9 for k in printed)
assert (len(str(n)), sum(map(int, str(n))), dr(n)) == (9, 45, 9)

assert 123 + 456 + 789 == 1368 and 1 + 3 + 6 + 8 == 18 and dr(1368) == 9
assert 123 + 654 + 789 == 1566 and 1 + 5 + 6 + 6 == 18 and dr(1566) == 9
assert sum(range(1, 10, 2)) == 25 and sum(range(2, 10, 2)) == 20
assert (10 ** 10 - 10) // 81 == 123456790 and (10 ** 10 - 10) % 81 == 0 and 123456790 - 1 == n
assert 12345688 != 123456790 - 1 and 12345688 != 12345678 and sum(d * 10 ** (8 - d) for d in range(1, 9)) == 12345678

# connections
assert 1368 == 37 * 37 - 1 == 36 * 38 and n % 999 == 369 == 1368 - 999 and n % 37 == 36 and 369 == 10 * 37 - 1 and 369 == 3 * 123 == 9 * 41
assert 10 ** 6 % 999 == 1 and n == 999 * 123580 + 369


def repetend(num, den):
    r, digs, seen = num, "", {}
    while r not in seen:
        seen[r] = len(digs)
        r *= 10
        digs += str(r // den)
        r %= den
    return digs[seen[r]:]


assert repetend(10, 81) == "123456790" and repetend(1, 81) == "012345679"
for k in (1, 2, 3):
    N = (10 ** k - 1) ** 2
    digs = repetend(1, N)
    blocks = [digs[j:j + k] for j in range(0, len(digs), k)]
    missing = sorted(set(f"{i:0{k}d}" for i in range(10 ** k)) - set(blocks))
    assert missing == [str(10 ** k - 2)] and len(digs) == k * (10 ** k - 1)

if __name__ == "__main__":
    print("123456789 output: factor, 8x, 9x, sums, 123456790 right; 111111111**2 label wrong (T3 = 12345679x(10^10+1)); "
          "N(k) lines 2-4 contradict themselves (digit sums 68, 92, 110, roots 5, 2, 2); 1368 = 37x37-1, 123456789 = 369 mod 999")
