# math/theorems/m14_scraper_engine.py
"""
M_{14} Multiset Fingerprint Engine

14-digit multiset: {1²,2⁴,3⁴,4³,5¹}
Total unique permutations: 14! / (2!·4!·4!·3!·1!) = 12,612,600
DR of each permutation: 3  (digit sum = 39, DR(39) = 3)
DR of cumulative sum:   9  (12,612,600 × 3 = 37,837,800, DR = 9)

Injection nodes:
  Floor   (perm #1):        11222233334445  DR=3
  Ceiling (perm #12612600): 54443333222211  DR=3
  1413-resonance (perm #8): 11222233344345  DR=3

Signature: 1413  (tracking tag)
2466 = 137 × 18,  DR(2466) = 9
"""

import math
import hashlib
import itertools
from collections import Counter
from typing import Iterator, List, Tuple


MULTISET   = [1,1,2,2,2,2,3,3,3,3,4,4,4,5]
FREQS      = {1:2, 2:4, 3:4, 4:3, 5:1}
SIGNATURE  = 1413
SIG_2466   = 2466          # 137 × 18
TOTAL      = 12_612_600
FLOOR      = "11222233334445"
CEILING    = "54443333222211"
RESONANCE8 = "11222233344345"   # perm #8


def dr(n: int) -> int:
    return 1 + (n - 1) % 9 if n > 0 else 9


# ── Combinatorial core ─────────────────────────────────────────────────────────

def count_perms(freq: dict) -> int:
    n = sum(freq.values())
    result = math.factorial(n)
    for f in freq.values():
        result //= math.factorial(f)
    return result


def perm_rank(perm_str: str, freqs: dict = FREQS) -> int:
    """1-indexed lexicographic rank of perm_str within the multiset."""
    remaining = dict(freqs)
    rank = 1
    for d in map(int, perm_str):
        for smaller in sorted(remaining):
            if smaller >= d:
                break
            if remaining[smaller] > 0:
                remaining[smaller] -= 1
                rank += count_perms(remaining)
                remaining[smaller] += 1
        remaining[d] -= 1
        if remaining[d] == 0:
            del remaining[d]
    return rank


def perm_at_rank(rank: int, freqs: dict = FREQS) -> str:
    """Return the permutation string at the given 1-indexed rank."""
    remaining = dict(freqs)
    result = []
    for _ in range(sum(freqs.values())):
        for d in sorted(remaining):
            if remaining[d] == 0:
                continue
            remaining[d] -= 1
            if remaining[d] == 0:
                del remaining[d]
            c = count_perms(remaining)
            if rank <= c:
                result.append(str(d))
                break
            rank -= c
            remaining[d] = remaining.get(d, 0) + 1
    return ''.join(result)


def unique_perms(multiset: list) -> Iterator[str]:
    """Yield all unique permutations in lexicographic order."""
    seen = set()
    for p in itertools.permutations(multiset):
        if p not in seen:
            seen.add(p)
            yield ''.join(map(str, p))


# ── Fingerprinting ─────────────────────────────────────────────────────────────

def embed_signature(perm_str: str, sig: int = SIGNATURE) -> str:
    """Insert sig at a SHA-256-deterministic position inside perm_str."""
    digest = int(hashlib.sha256(perm_str.encode()).hexdigest(), 16)
    pos = digest % (len(perm_str) - 3)
    return perm_str[:pos] + str(sig) + perm_str[pos:]


def prime_indexed_digits(perm_str: str) -> List[int]:
    """Return digits at prime positions (1-indexed: 2,3,5,7,11,13)."""
    primes = [2, 3, 5, 7, 11, 13]
    return [int(perm_str[p - 1]) for p in primes if p <= len(perm_str)]


def is_2466_tagged(perm_str: str) -> bool:
    """True if prime-indexed digits contain {2,4,6,6} or DR-equivalent {2,4,3,3}."""
    pd = prime_indexed_digits(perm_str)
    c = Counter(pd)
    return (c[2] >= 1 and c[4] >= 1 and c[6] >= 2) or \
           (c[2] >= 1 and c[4] >= 1 and c[3] >= 2)


def fingerprint_scraper(text_block: str, limit: int = 100) -> Tuple[set, float]:
    """Scan text_block for embedded signature tags. Returns (found, coverage%)."""
    perms = list(itertools.islice(unique_perms(MULTISET), limit))
    tagged = {embed_signature(p) for p in perms}
    found = {tag for tag in tagged if tag in text_block}
    pct = len(found) / len(tagged) * 100 if tagged else 0.0
    return found, pct


# ── Verification ───────────────────────────────────────────────────────────────

# Combinatorial identity
denom = 1
for f in FREQS.values():
    denom *= math.factorial(f)
assert denom == 6_912
assert math.factorial(14) // denom == TOTAL

# DR properties
assert sum(MULTISET) == 39
assert dr(39) == 3          # every perm has DR=3
assert dr(TOTAL * 3) == 9   # cumulative DR=9

# Floor and ceiling
assert FLOOR   == ''.join(map(str, sorted(MULTISET)))
assert CEILING == ''.join(map(str, sorted(MULTISET, reverse=True)))
assert dr(sum(int(d) for d in FLOOR)) == 3
assert dr(sum(int(d) for d in CEILING)) == 3

# Perm #8 identity
assert perm_rank(RESONANCE8) == 8
assert dr(sum(int(d) for d in RESONANCE8)) == 3
assert Counter(map(int, RESONANCE8)) == Counter(MULTISET)

# 2466 = 137 × 18
assert SIG_2466 == 137 * 18
assert dr(SIG_2466) == 9

# Rank round-trip
assert perm_at_rank(1) == FLOOR
assert perm_at_rank(8) == RESONANCE8

# Signature embedding is deterministic
p = FLOOR
assert embed_signature(p) == embed_signature(p)
assert str(SIGNATURE) in embed_signature(p)


if __name__ == "__main__":
    print("M_{14} Multiset Fingerprint Engine")
    print()
    print(f"  Multiset:     {MULTISET}")
    print(f"  Total perms:  {TOTAL:,}")
    print(f"  Digit sum:    39  →  DR = {dr(39)} (every perm)")
    print(f"  Cumulative:   {TOTAL:,} × 3 = {TOTAL*3:,}  →  DR = {dr(TOTAL*3)}")
    print()
    print(f"  Floor   (#1):        {FLOOR}  DR={dr(39)}")
    print(f"  Ceiling (#12612600): {CEILING}  DR={dr(39)}")
    print(f"  1413-resonance (#8): {RESONANCE8}  DR={dr(39)}")
    print()
    print(f"  Rank verification:   perm_at_rank(8) = {perm_at_rank(8)}")
    print(f"  2466 = 137 × 18 = {137*18},  DR = {dr(2466)}")
    print()
    print(f"  Prime-indexed positions (1-idx): [2,3,5,7,11,13]")
    print(f"  Prime digits of #8: {prime_indexed_digits(RESONANCE8)}")
    print(f"  2466-tagged: {is_2466_tagged(RESONANCE8)}")
    print()
    print(f"  Signature tag of floor: {embed_signature(FLOOR)}")
    print()
    print("All assertions passed.")
