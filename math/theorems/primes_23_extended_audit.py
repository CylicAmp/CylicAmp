# math/theorems/primes_23_extended_audit.py
"""
{2,3}-Digit Prime Extended Audit
=================================
Extends primes_digits_23_audit.py with:
  1. Cross-check of the partial list from the exposition (corrects omissions)
  2. DR and mod-37 snapshot for all verified primes (L1–L7)
  3. Right-truncatable filter
  4. Length-8 enumeration
  5. Mod-37 sieve (classes ≡ 0,1,2,23 (mod 37) and full distribution)
"""

import itertools
import math


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, math.isqrt(n) + 1, 2):
        if n % i == 0:
            return False
    return True


def dr(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


def primes_23_length(length: int) -> list:
    return sorted(
        int("".join(d)) for d in itertools.product("23", repeat=length)
        if is_prime(int("".join(d)))
    )


def is_right_truncatable(n: int) -> bool:
    """All right-truncations of n are prime."""
    s = str(n)
    for end in range(len(s), 0, -1):
        if not is_prime(int(s[:end])):
            return False
    return True


# ── 1. Full enumeration L1–L8 ─────────────────────────────────────────────────

PRIMES_BY_LENGTH: dict[int, list] = {}
for _l in range(1, 9):
    PRIMES_BY_LENGTH[_l] = primes_23_length(_l)

ALL_PRIMES_L1_L7 = [p for l in range(1, 8) for p in PRIMES_BY_LENGTH[l]]

# Partial list from the exposition (claimed primes only — incomplete)
EXPOSITION_PRIMES = [
    2, 3,           # L1
    23,             # L2
    223, 233,       # L3
    2333, 3323,     # L4
    23333, 32233,   # L5  (missing: 32323, 33223)
    232333, 233323, # L6  (missing: 222323, 323233, 323333, 333233, 333323)
    2222333,        # L7  (missing: 12 more)
]

EXPOSITION_COMPOSITES = [22333, 322223, 2232233, 2233333]


def verify_cross_check():
    print("=" * 70)
    print("1. Cross-Check: Exposition vs Full Enumeration")
    print("=" * 70)

    # All exposition primes are genuine primes
    for p in EXPOSITION_PRIMES:
        assert is_prime(p), f"{p} claimed prime but is composite"

    # All exposition composites are genuinely composite
    for c in EXPOSITION_COMPOSITES:
        assert not is_prime(c), f"{c} claimed composite but is prime"
        # All digits in {2,3}?
        assert all(ch in "23" for ch in str(c)), f"{c} has digit outside {{2,3}}"

    # Find primes missing from the exposition
    missing_by_length = {}
    for l in range(1, 8):
        full = set(PRIMES_BY_LENGTH[l])
        expo = set(p for p in EXPOSITION_PRIMES if len(str(p)) == l)
        missing = sorted(full - expo)
        if missing:
            missing_by_length[l] = missing

    print(f"\n  Exposition lists {len(EXPOSITION_PRIMES)} primes; "
          f"full count is {len(ALL_PRIMES_L1_L7)}.")
    print(f"  Missing from exposition by length:")
    for l, m in missing_by_length.items():
        print(f"    L{l}: {m}")
    print(f"\n  Composites correctly identified: {EXPOSITION_COMPOSITES}  ✓")

    total_missing = sum(len(v) for v in missing_by_length.values())
    assert total_missing == len(ALL_PRIMES_L1_L7) - len(EXPOSITION_PRIMES)
    print(f"\n  Total omitted primes: {total_missing}")
    print()


# ── 2. DR and mod-37 snapshot ─────────────────────────────────────────────────

def verify_dr_mod37():
    print("=" * 70)
    print("2. DR and Mod-37 Snapshot (all L1–L7 primes)")
    print("=" * 70)

    drs    = [dr(p) for p in ALL_PRIMES_L1_L7]
    mod37s = [p % 37 for p in ALL_PRIMES_L1_L7]

    print(f"\n  {'Prime':>12}  L  DR  mod37")
    print(f"  {'-'*40}")
    for p in ALL_PRIMES_L1_L7:
        length = len(str(p))
        print(f"  {p:>12}  {length}   {dr(p)}  {p % 37:>3}")

    from collections import Counter
    dr_dist   = Counter(drs)
    mod37_dist = Counter(mod37s)

    print(f"\n  DR distribution:   {dict(sorted(dr_dist.items()))}")
    print(f"  Mod-37 values:     {sorted(mod37s)}")
    print(f"  Mod-37 unique:     {sorted(mod37_dist.keys())}")

    # Exposition claims "several ≡ 1, 2, 23 mod 37"
    for target in [1, 2, 23]:
        hits = [p for p in ALL_PRIMES_L1_L7 if p % 37 == target]
        print(f"  ≡ {target:>2} (mod 37): {hits}")

    # No fixed class: confirm residues are not all equal
    assert len(mod37_dist) > 1, "Unexpectedly uniform mod-37 class"
    print(f"\n  No single fixed mod-37 class  ✓")
    print()


# ── 3. Right-truncatable filter ───────────────────────────────────────────────

def verify_right_truncatable():
    print("=" * 70)
    print("3. Right-Truncatable {2,3}-Primes (L1–L7)")
    print("=" * 70)

    rt = [p for p in ALL_PRIMES_L1_L7 if is_right_truncatable(p)]
    print(f"\n  Right-truncatable primes: {rt}")
    print(f"  Count: {len(rt)}")

    # Main chain via first-digit-2: 2→23→233→2333→23333
    assert 2      in rt
    assert 23     in rt
    assert 233    in rt
    assert 2333   in rt
    assert 23333  in rt

    # Verify chain truncates correctly
    chain = [23333, 2333, 233, 23, 2]
    for i, p in enumerate(chain):
        assert is_prime(p), f"{p} not prime"
        if i + 1 < len(chain):
            assert int(str(p)[:-1]) == chain[i + 1]

    # Chain terminates: 233333 not in L6 primes (it's composite)
    assert not is_prime(233333)
    print(f"  Chain 2→23→233→2333→23333: all right-truncatable  ✓")
    print(f"  233333 (L6 extension) composite → chain terminates at L5  ✓")

    # 3 is right-truncatable but 3-started chain: 33 composite, so 3 only
    assert is_right_truncatable(3)
    assert not is_prime(33)
    print(f"  3 right-truncatable (1-member chain: 33 composite)  ✓")
    print()


# ── 4. Length-8 enumeration ───────────────────────────────────────────────────

def verify_length8():
    print("=" * 70)
    print("4. Length-8 Extension")
    print("=" * 70)

    L8 = PRIMES_BY_LENGTH[8]
    print(f"\n  L8 prime count: {len(L8)}")
    print(f"  L8 primes:")
    for p in L8:
        print(f"    {p}  DR={dr(p)}  mod37={p % 37}")

    # All end in 3 (even ending → divisible by 2)
    assert all(str(p)[-1] == "3" for p in L8 if p > 3)
    print(f"\n  All L8 primes end in 3  ✓")

    # Running totals
    counts = [len(PRIMES_BY_LENGTH[l]) for l in range(1, 9)]
    cumulative = [sum(counts[:i + 1]) for i in range(8)]
    print(f"\n  Count by length:   {counts}")
    print(f"  Cumulative totals: {cumulative}")
    print()


# ── 5. Mod-37 sieve (full distribution) ──────────────────────────────────────

def verify_mod37_sieve():
    print("=" * 70)
    print("5. Mod-37 Sieve (L1–L8)")
    print("=" * 70)

    all_primes = ALL_PRIMES_L1_L7 + PRIMES_BY_LENGTH[8]
    from collections import Counter
    dist = Counter(p % 37 for p in all_primes)

    print(f"\n  All {len(all_primes)} primes (L1–L8) by mod-37 residue:")
    for res in sorted(dist.keys()):
        ps = [p for p in all_primes if p % 37 == res]
        print(f"    ≡ {res:>2} (mod 37) [{len(ps):>2}]: {ps}")

    # Verify no complete coverage of all 37 residues
    assert len(dist) < 37
    print(f"\n  Distinct mod-37 classes covered: {len(dist)} of 37")
    print(f"  Uncovered residues: {sorted(set(range(37)) - set(dist.keys()))}")

    # 37 | p only if p = 37 itself (which is not a {2,3}-digit number)
    assert all(p % 37 != 0 for p in all_primes)
    print(f"  No prime ≡ 0 (mod 37)  ✓  (37 has digit 7, outside {{2,3}})")
    print()
    print("All assertions passed.")


def verify():
    verify_cross_check()
    verify_dr_mod37()
    verify_right_truncatable()
    verify_length8()
    verify_mod37_sieve()


if __name__ == "__main__":
    verify()
