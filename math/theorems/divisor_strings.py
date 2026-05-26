"""
DIVISOR STRINGS: Proper-Divisor-String Palindromes in 11–99
=========================================================================

Definition:
  The "proper divisor string" of n is the concatenation of all proper
  divisors of n (divisors < n) in sorted order, written as a string.

  Example: n=93, proper divisors = {1, 3, 31}
           string = "1" + "3" + "31" = "1331"  ← palindrome

Verified results:
  - 22 of the 89 integers in [11, 99] have palindromic proper divisor strings
  - 21 of the 22 are primes (proper divisors = {1} → string "1", trivially palindromic)
  - 1 composite: n=93 = 3 × 31, string "1331" (palindrome ✓)

The "111" pattern:
  The claim that "all 9 multiples of 11 in 11–99 contain '111'" is FALSE
  under this definition. Only n=11 gives string "1". The number 111 = 3×37
  appears in the cascade framework (k=5 step: 13+21+24+32+37=127 is nearby;
  111 is a cascade element at step k=5). The connection is structural, not
  string-containment.

Connection to mod-37 framework:
  - 37 itself is one of the 22 palindromes (prime → string "1")
  - 93 = 3 × 31; 93 mod 37 = 19 ∈ QNR_37
  - "1331" = 11³; 11 is in the cascade and in the orbit
"""


def proper_divisors(n: int) -> list:
    return sorted(d for d in range(1, n) if n % d == 0)


def divisor_string(n: int) -> str:
    return ''.join(str(d) for d in proper_divisors(n))


def is_palindrome(s: str) -> bool:
    return bool(s) and s == s[::-1]


def find_palindromes(lo: int = 11, hi: int = 99) -> list:
    """Return all n in [lo, hi] with palindromic proper divisor string."""
    return [(n, divisor_string(n)) for n in range(lo, hi + 1)
            if is_palindrome(divisor_string(n))]


def classify(n: int) -> str:
    pd = proper_divisors(n)
    if pd == [1]:
        return "prime"
    return f"composite ({' × '.join(str(p) for p in pd[1:])})"


# =============================================================================
# Summary
# =============================================================================

def summarise():
    print("=" * 60)
    print("DIVISOR STRINGS: Palindromes in [11, 99]")
    print("=" * 60)

    palins = find_palindromes()
    total = len(list(range(11, 100)))

    print(f"\nDefinition: concat of proper divisors (sorted) as string")
    print(f"Range: 11–99  ({total} integers)")
    print(f"Palindromes: {len(palins)}/{total}")

    primes   = [(n, s) for n, s in palins if classify(n) == "prime"]
    comps    = [(n, s) for n, s in palins if classify(n) != "prime"]

    print(f"\nAll {len(palins)} palindromes:")
    print(f"  Primes ({len(primes)}): {[n for n,_ in primes]}")
    for n, s in comps:
        print(f"  Composite: n={n} = {classify(n)}, string='{s}' ✓")

    print(f"\nNote: '1331' = 11³  (11 appears in cascade and orbit)")
    print(f"  11³ = {11**3}")
    print(f"  93 mod 37 = {93 % 37}")

    qr37 = set(pow(3, k, 37) for k in range(1, 19))
    print(f"  37 mod 37 = 0  (cascade zero element)")
    print(f"  37 ∈ palindromes: {37 in [n for n,_ in palins]}")

    print(f"\nMultiples of 11 in [11, 99] — proper divisor strings:")
    for n in range(11, 100, 11):
        s = divisor_string(n)
        print(f"  n={n:3d}: '{s}'  palindrome={is_palindrome(s)}")

    print(f"\nCorrected claim: 22/89 palindromes (21 primes + n=93)")
    print(f"Retracted claim: 'all multiples of 11 contain 111' — FALSE under this definition")


if __name__ == "__main__":
    summarise()
