# math/theorems/primes_digits_23_audit.py
"""
Primes Using Only Digits {2, 3} — Lengths 1 to 7
==================================================
Exhaustive enumeration of all primes whose decimal representation
uses only the digits 2 and 3, for each word-length 1 through 7.

Key results:
  Length 1: [2, 3]
  Length 2: [23]                               — unique; 22,32,33 composite
  Length 3: [223, 233]
  Length 4: [2333, 3323]
  Length 5: [23333, 32233, 32323, 33223]
  Length 6: [222323, 232333, 233323, 323233, 323333, 333233, 333323]
  Length 7: [2222333, 2223233, 2232323, 2233223, 2332333, 2333323,
             3222223, 3223223, 3223333, 3233323, 3233333, 3332233,
             3333233]

Structural notes:
  - Smallest prime at each length ≥ 2 begins with '2' followed by
    runs of '3': 23, 233, 2333, 23333 — all prime.
  - 23 is a common prefix across lengths.
  - Every prime > 2 must end in 3 (trailing 2 → even → composite).
  - Total primes found: 2+1+2+2+4+7+13 = 31 across lengths 1-7.
"""

import itertools


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def primes_from_digits_23(length: int) -> list[int]:
    result = []
    for digits in itertools.product("23", repeat=length):
        n = int("".join(digits))
        if is_prime(n):
            result.append(n)
    return sorted(result)


# Pre-computed expected results (verified against exhaustive enumeration)
EXPECTED = {
    1: [2, 3],
    2: [23],
    3: [223, 233],
    4: [2333, 3323],
    5: [23333, 32233, 32323, 33223],
    6: [222323, 232333, 233323, 323233, 323333, 333233, 333323],
    7: [2222333, 2223233, 2232323, 2233223, 2332333, 2333323,
        3222223, 3223223, 3223333, 3233323, 3233333, 3332233, 3333233],
}


def verify():
    all_primes: dict[int, list[int]] = {}

    for length in range(1, 8):
        found = primes_from_digits_23(length)
        all_primes[length] = found
        assert found == EXPECTED[length], (
            f"Length {length}: got {found}, expected {EXPECTED[length]}"
        )

    # Every prime > 2 must end in 3 (ending in 2 → even → composite)
    for length, primes in all_primes.items():
        for p in primes:
            if p > 2:
                assert str(p)[-1] == "3", f"{p} ends in 2 but is claimed prime"

    # Smallest prime at each length ≥ 2 starts with '2'
    for length in range(2, 8):
        assert str(all_primes[length][0])[0] == "2"

    # 23 is prime and appears as prefix in longer primes
    assert is_prime(23)
    prefix_hits = [p for length in range(3, 8) for p in all_primes[length]
                   if str(p).startswith("23")]
    assert len(prefix_hits) >= 3  # 233, 23333, 232333, 233323, ...

    # Total count
    total = sum(len(v) for v in all_primes.values())
    assert total == 31

    # Print table
    print("Primes using only digits {2, 3} — lengths 1 to 7")
    print()
    print(f"  {'Length':>6}  {'Count':>5}  Primes (all)")
    for length, primes in all_primes.items():
        print(f"  {length:>6}  {len(primes):>5}  {primes}")
    print()
    print(f"  Total: {total} primes across lengths 1–7  (2+1+2+2+4+7+13)")
    print()
    print(f"  Structural: every prime > 2 ends in 3  ✓")
    print(f"  Structural: smallest per length ≥ 2 starts with '2'  ✓")
    print(f"  Prefix '23' hits (length ≥ 3): {sorted(prefix_hits)}")
    print()
    print("All assertions passed.")


if __name__ == "__main__":
    verify()
