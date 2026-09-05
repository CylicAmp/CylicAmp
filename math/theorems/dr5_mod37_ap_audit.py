# math/theorems/dr5_mod37_ap_audit.py
"""
DR=5 Arithmetic Progression in mod-37 — Range 5 to 32
======================================================
The DR=5 residues mod 37 are exactly those r ∈ [0,36] with dr(r)=5:
    {5, 14, 23, 32}  — arithmetic progression, common difference 9.

Notation: 5–14–(23–32)
  First pair:   {5, 14}   (span 9)
  Second pair:  {23, 32}  (span 9, grouped)
  Full span:    32 − 5 = 27 = 3 × 9

Every DR class has exactly 4 representatives mod 37 (since 9 × 4 = 36 = φ(37)).
These form cosets of the subgroup ⟨9⟩ = {0,9,18,27,36} in Z_37... but 37 is prime
and 9 is not a subgroup generator of Z_37×; the spacing of 9 is a coincidence of
the DR=5 residue slice.

Connection to prior work:
  - ord_37(10) = 3; positional weights cycle [1, 10, 26] mod 37.
  - 23 ≡ 23 (mod 37): the prime 23 and its extension 23333 both land here.
  - 14 ≡ 14 (mod 37): five {2,3}-primes land here (all L7-L8).
  - Distribution across the AP: {5:1, 14:5, 23:5, 32:1} — palindromic.
"""

import itertools, math
from collections import defaultdict


def dr(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


def is_prime(n: int) -> bool:
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, math.isqrt(n) + 1, 2):
        if n % i == 0: return False
    return True


def primes_23_length(length: int) -> list:
    return sorted(
        int("".join(d)) for d in itertools.product("23", repeat=length)
        if is_prime(int("".join(d)))
    )


ALL_PRIMES = [p for l in range(1, 9) for p in primes_23_length(l)]  # L1–L8


def verify():
    print("DR=5 Arithmetic Progression in mod-37\n")

    # ── AP structure ──────────────────────────────────────────────────────────
    AP = [r for r in range(37) if dr(r) == 5]
    assert AP == [5, 14, 23, 32]
    assert AP[1] - AP[0] == AP[2] - AP[1] == AP[3] - AP[2] == 9
    assert AP[-1] - AP[0] == 27 == 3 * 9
    assert len(AP) == 4      # every DR class has exactly 4 reps in [0,36]

    print(f"  AP = {AP}")
    print(f"  Common difference: 9")
    print(f"  Full span: {AP[-1]}−{AP[0]} = {AP[-1]-AP[0]} = 3×9  ✓")
    print(f"  Notation: {AP[0]}–{AP[1]}–({AP[2]}–{AP[3]})")
    print(f"    First pair  {AP[:2]}: span {AP[1]-AP[0]}")
    print(f"    Second pair {AP[2:]}: span {AP[3]-AP[2]}")

    # All 9 DR classes have 4 representatives each in [0,36]
    for r in range(1, 10):
        reps = [x for x in range(37) if dr(x) == r]
        assert len(reps) == 4
    print(f"\n  Every DR class 1–9 has exactly 4 representatives in [0,36]  ✓")

    # ── {2,3}-prime distribution across the AP ────────────────────────────────
    dist: dict[int, list] = {r: [] for r in AP}
    for p in ALL_PRIMES:
        if p % 37 in dist:
            dist[p % 37].append(p)

    counts = [len(dist[r]) for r in AP]
    print(f"\n  {'{2,3}'}-prime hits per AP residue (L1–L8):")
    for r in AP:
        ps = dist[r]
        lengths = [len(str(p)) for p in ps]
        print(f"    ≡{r:>2} mod 37 [{len(ps)}]: {ps}  lengths={lengths}")

    # Distribution is palindromic: [1, 5, 5, 1]
    assert counts == [1, 5, 5, 1]
    assert counts == counts[::-1]
    print(f"\n  Count distribution: {counts}  (palindromic)  ✓")

    # ── Key anchors ───────────────────────────────────────────────────────────
    # The prime 23 itself has DR=5 and lands at ≡23 mod 37
    assert is_prime(23) and dr(23) == 5 and 23 % 37 == 23
    assert 23 in dist[23]

    # 23333 (the length-5 right-truncatable extension of 23) also ≡23 mod 37
    assert is_prime(23333) and dr(23333) == 5 and 23333 % 37 == 23
    assert 23333 in dist[23]

    print(f"\n  Anchor: 23 mod 37 = 23  (prime, DR=5)  ✓")
    print(f"  Anchor: 23333 mod 37 = 23  (extension, DR=5)  ✓")
    print(f"  Both anchors share residue class ≡23 — the AP's third member.")

    # ── AP in relation to ord_37(10) = 3 ─────────────────────────────────────
    # Positional weights: 10^0=1, 10^1=10, 10^2=26 (then repeats)
    # DR=5 residues {5,14,23,32} and the weight cycle {1,10,26}:
    weights = [pow(10, i, 37) for i in range(6)]
    assert weights[:3] == [1, 10, 26]
    # 5 ≡ 5 mod 37;  10-5=5;  14-5=9;  23-5=18=2×9;  32-5=27=3×9
    # Differences from 5: 0, 9, 18, 27 — multiples of 9
    diffs = [r - AP[0] for r in AP]
    assert diffs == [0, 9, 18, 27]
    print(f"\n  Differences from first element: {diffs}  (multiples of 9)  ✓")
    print(f"  Block-sum weight cycle mod 37: {weights[:3]}  (period 3)  ✓")

    # ── Full DR-class × mod-37 map for all {2,3}-primes ─────────────────────
    print(f"\n  Full DR × mod-37 for all {len(ALL_PRIMES)} {'{2,3}'}-primes (L1–L8):")
    by_dr: dict = defaultdict(list)
    for p in ALL_PRIMES:
        by_dr[dr(p)].append((p % 37, p))

    for d in sorted(by_dr):
        entries = sorted(by_dr[d])
        res = sorted({r for r, _ in entries})
        print(f"    DR{d} [{len(entries):>2} primes]: mod-37 residues = {res}")

    print()
    print("All assertions passed.")


if __name__ == "__main__":
    verify()
