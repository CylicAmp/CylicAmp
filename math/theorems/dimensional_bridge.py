# CLASS: COMPUTATION
"""
37phi Dimensional Bridge — computational verification.

Finds the smallest N such that sum of first N primes exceeds 37*phi
AND is divisible by 7.

Verified result: N=8, sum=77=7×11
"""

import math

PHI = (1 + math.sqrt(5)) / 2
COHERENCE_TARGET = 37 * PHI  # 59.867258...


import sys as _sys, pathlib as _pl
_sys.path.append(str(next(p for p in _pl.Path(__file__).resolve().parents if (p / "functions.py").exists())))
from functions import dr_signed as digital_root


import sys as _sys, pathlib as _pl
_sys.path.append(str(next(p for p in _pl.Path(__file__).resolve().parents if (p / "functions.py").exists())))
from functions import primes_upto as sieve


primes = sieve(200)

# Find smallest N where sum of first N primes > 37phi AND sum % 7 == 0
result_n = None
result_sum = None
for n in range(1, len(primes) + 1):
    s = sum(primes[:n])
    if s > COHERENCE_TARGET and s % 7 == 0:
        result_n = n
        result_sum = s
        break

if __name__ == "__main__":
    print(f"37 × φ = {COHERENCE_TARGET:.6f}")
    print()
    print(f"First {result_n} primes: {primes[:result_n]}")
    print(f"Sum: {result_sum}")
    print(f"Sum > 37φ: {result_sum} > {COHERENCE_TARGET:.3f}  ✓")
    print(f"Sum mod 7: {result_sum % 7}  ✓")
    print(f"Factorization: {result_sum} = 7 × {result_sum // 7}")
    print()
    print("Digital roots:")
    drs = [digital_root(p) for p in primes[:result_n]]
    for p, dr in zip(primes[:result_n], drs):
        print(f"  {p:>2} → DR={dr}")
    print(f"  DR sum: {sum(drs)} → DR={digital_root(sum(drs))}")
    print(f"  dr({result_sum}) = {digital_root(result_sum)}")
    print()
    assert result_n == 8
    assert result_sum == 77
    assert result_sum % 7 == 0
    assert result_sum > COHERENCE_TARGET
    print("All assertions passed.")
