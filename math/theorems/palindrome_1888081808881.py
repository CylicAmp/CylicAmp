"""
Palindrome Analysis: 1888081808881

13-digit palindrome with center digit 1.
Base = 188808; full number = base + "1" + reverse(base).
"""

from sympy import factorint, isprime


N    = 1888081808881
BASE = 188808


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


# ---------------------------------------------------------------------------
# Palindrome structure
# ---------------------------------------------------------------------------

s = str(N)
assert s == s[::-1],               "N must be a palindrome"
assert len(s) == 13
assert s[6] == "1",                "center digit = 1"
assert s[:6]  == "188808"
assert s[6:]  == "1808881"
assert s[:7]  == "1888081",        "left half (0-6) = 1888081"
assert s[6:]  == "1808881",        "right half (6-12) = 1808881"

base_s = s[:6]
assert base_s[::-1] == "808881"
assert base_s + s[6] + base_s[::-1] == s, "reconstruction matches"

# ---------------------------------------------------------------------------
# Base 188808 analysis
# ---------------------------------------------------------------------------

digits   = [int(d) for d in str(BASE)]
dsum     = sum(digits)          # 1+8+8+8+0+8 = 33  [NOT 25]
assert digits == [1, 8, 8, 8, 0, 8]
assert dsum == 33
assert dr(dsum) == 6            # DR(33)=6, NOT 7

# [ERRATA]: user output shows "Digit sum: 33 = 25, dr(25)=7"
# The 25 comes from 1+8+8+0+8=25, which OMITS one 8 from the triple.
# Correct digit sum = 33; correct DR = 6.

assert BASE % 37 == 34
assert BASE %  9 ==  6         # consistent with DR(dsum)=6
assert abs(BASE / 111 - 1700.973) < 0.001

factors = factorint(BASE)
assert factors == {2: 3, 3: 1, 7867: 1}   # 8 × 3 × 7867
assert isprime(7867)
assert 2**3 * 3 * 7867 == BASE

# ---------------------------------------------------------------------------
# 188808 in terms of 37
# ---------------------------------------------------------------------------

assert 51 * 37 + 1 == 1888              # 1888 ≡ 1 (mod 37)
assert (51 * 37 + 1) * 100 + 8 == BASE  # = 5100×37 + 108
assert 5100 * 37 + 108 == BASE
assert 108 % 37 == 34                   # so BASE ≡ 34 (mod 37) ✓

# ---------------------------------------------------------------------------
# Full number N mod 37
# ---------------------------------------------------------------------------

assert N == 51029238077 * 37 + 32
assert N % 37 == 32
assert 32 == 37 - 5                      # N ≡ -5 (mod 37)
assert N + 5 == 1888081808886
assert 1888081808886 % 37 == 0
assert 1888081808886 // 37 == 51029238078
assert 37 * 51029238078 == 1888081808886

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Palindrome: 1888081808881")
    print("=" * 56)
    s = str(N)
    print(f"  N           = {N}")
    print(f"  Palindrome  = {s == s[::-1]}")
    print(f"  Digits      = {len(s)}")
    print()
    print(f"  Left  (0-6) = {s[:7]}")
    print(f"  Center      = {s[6]}")
    print(f"  Right (6-12)= {s[6:]}")
    print()
    print(f"  Base          = {s[:6]}")
    print(f"  Base reversed = {s[:6][::-1]}")
    print(f"  Reconstruction: {s[:6]+s[6]+s[:6][::-1]} ✓")
    print()
    print(f"Base {BASE} analysis:")
    print(f"  Digits       = {[int(d) for d in str(BASE)]}")
    print(f"  Pattern      = 1, (8,8,8), 0, 8")
    print(f"  Digit sum    = 33  →  DR = {dr(33)}")
    print(f"  [ERRATA: '33=25, dr=7' in source — 25 omits one 8 from triple]")
    print(f"  mod 37  = {BASE % 37}")
    print(f"  mod  9  = {BASE % 9}")
    print(f"  / 111   = {BASE/111:.3f}")
    print(f"  Factors = {factorint(BASE)}  (7867 prime: {isprime(7867)})")
    print()
    print(f"188808 via 37:")
    print(f"  1888 = 51×37 + 1  ≡ 1 (mod 37)")
    print(f"  188808 = 5100×37 + 108,  108 mod 37 = {108%37}")
    print()
    print(f"N mod 37:")
    print(f"  N = 51029238077 × 37 + 32")
    print(f"  N ≡ 32 ≡ -5 (mod 37)  [32 = 37-5]")
    print(f"  N + 5 = {N+5} = 37 × 51029238078  ✓")
    print()
    print("All assertions passed.")
