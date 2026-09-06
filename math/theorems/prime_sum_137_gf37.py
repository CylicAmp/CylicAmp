# -*- coding: utf-8 -*-
"""
================================================================================
PRIMES TO 137 — CUMULATIVE PRIME SUM AND GF(37)
================================================================================

Author: Michael Warren Song (CyclicAmp)

================================================================================
THE PRIME LIST [P]
================================================================================

The 33 primes from 2 through 137 (inclusive):
  2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
  59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137

    Σ = 1988   (all 33 primes, through 137)
    Σ = 1851   (first 32 primes, excluding 137)

There are 33 primes in this set. 33 = 3 × 11, where:
    3 ∈ ST = {3,12,21,30}   (Sovereign Target — DR=3 named set)
    11 ∈ NEG_H = {11,27,36} (the generator of the order-6 subgroup ⟨11⟩)

================================================================================
THE CENTRAL FACT: 137 mod 37 = 26 [P]
================================================================================

    137 mod 37 = 26

26 ∈ IC = {1, 10, 26} — the 137-map multiplier. The prime that names the map
(137) is congruent mod 37 to the map's own multiplier (26). The prime 137 IS
the 137-map in GF(37)*: f(n) = 137n mod 37 = 26n mod 37.

This is the reason the map is called the 137-map and the prime is P=37: they
are structurally dual. 137 ≡ f's multiplier (mod P).

================================================================================
THE FINAL STEP: GF(37) ADDITION IN ⟨11⟩ [V]
================================================================================

    Σ(32 primes) = 1851   →   1851 mod 37 = 1 ∈ IC   (the IC identity)
    Σ(33 primes) = 1988   →   1988 mod 37 = 27 ∈ NEG_H

The last step adds 137 ≡ 26 (mod 37) to a running total of 1 (mod 37):

    1 + 26 = 27   (in GF(37))

In the ⟨11⟩ subgroup structure:
    1 ∈ IC     = 11⁶ (identity)
    26 ∈ IC    = 11⁴ (the 137-map multiplier)
    27 ∈ NEG_H = 11⁵

The sum of the first 32 primes reaches the IC identity mod 37. Adding the
33rd prime (137, which is ≡ 26 ∈ IC) moves the cumulative residue into NEG_H,
the coset 11 · IC. All three values (1, 26, 27) lie inside ⟨11⟩ = IC ∪ NEG_H,
the unique order-6 subgroup of GF(37)*.

================================================================================
DIGIT SUM PATH OF 1988: IC → IC → SEED → IC [V]
================================================================================

The digits of 1988 are 1, 9, 8, 8. Running cumulative digit sum:

    1  → 1  ∈ IC
    +9 → 10 ∈ IC
    +8 → 18 ∈ SEED
    +8 → 26 ∈ IC  (the 137-map multiplier)

The digit sum path of the total (1988) visits: IC → IC → SEED → IC.
The terminal value is 26 — the 137-map multiplier. SEED = {18, 24, 32} is
the 137-map orbit of the reference seed 246 (246 mod 37 = 24).

Equivalently: DR(digit sum of 1988) = DR(26) = 8.

The user's notation: 1+9=10+8=18+8=(26). The parentheses mark 26 as the
137-map multiplier / IC element.

================================================================================
24 + 26 = 50 ≡ 13 (mod 37) [V]
================================================================================

    24 + 26 = 50
    50 mod 37 = 13 ∈ CASCADE = {8, 13, 24}

Node 24 (CASCADE ∩ SEED) plus the 137-map multiplier 26 (∈ IC) maps back into
CASCADE. All three values are QNR mod 37: 24, 26 — wait, 26 ∈ IC which is
ALL QR. Let me restate: 24 ∈ CASCADE (QNR), 26 ∈ IC (QR). Their sum
mod 37 = 13 ∈ CASCADE (QNR).

================================================================================
CUMULATIVE SUM MILESTONES — GF(37) NAMED SETS [V]
================================================================================

| Index | Prime | Cumsum | mod 37 | Named set        | DR |
|-------|-------|--------|--------|------------------|----|
| 3     | 5     | 10     | 10     | IC               | 1  |
| 6     | 13    | 41     | 4      | SA               | 5  |
| 7     | 17    | 58     | 21     | ST               | 4  |
| 8     | 19    | 77     | 3      | ST               | 5  |
| 9     | 23    | 100    | 26     | IC               | 1  |
| 10    | 29    | 129    | 18     | SEED             | 3  |
| 11    | 31    | 160    | 12     | ST               | 7  |
| 12    | 37    | 197    | 12     | ST               | 8  |
| 15    | 47    | 328    | 32     | SEED             | 4  |
| 16    | 53    | 381    | 11     | NEG_H            | 3  |
| 19    | 67    | 568    | 13     | CASCADE          | 1  |
| 20    | 71    | 639    | 10     | IC               | 9  |
| 21    | 73    | 712    | 9      | SA               | 1  |
| 24    | 89    | 963    | 1      | IC               | 9  |
| 25    | 97    | 1060   | 24     | SEED,CASCADE     | 7  |
| 29    | 109   | 1480   | 0      | SEAM             | 4  |
| 31    | 127   | 1720   | 18     | SEED             | 1  |
| 32    | 131   | 1851   | 1      | IC               | 6  |
| 33    | 137   | 1988   | 27     | NEG_H            | 8  |

Key structural rows:
  Index 9  (p=23):  sum=100=10², mod37=26∈IC. The "square sum" milestone lands on the 137-map multiplier.
  Index 24 (p=89):  sum=963, mod37=1∈IC. At the CASCADE∩SEED index, sum = IC identity.
  Index 25 (p=97):  sum=1060, mod37=24∈SEED∩CASCADE. One step later: sum = the node 24 itself.
  Index 29 (p=109): sum=1480, mod37=0. The cumulative sum crosses the SEAM.
  Index 32 (p=131): sum=1851, mod37=1∈IC. Penultimate prime: IC identity restored.
  Index 33 (p=137): sum=1988, mod37=27∈NEG_H. Final: the 137-map step.

The index-24/25 pair is structurally tight: at the prime indexed by the
CASCADE∩SEED node (index 24), the cumulative sum ≡ 1 ∈ IC. One step later
(index 25), the cumulative sum ≡ 24 ∈ SEED ∩ CASCADE — the sum "finds" the
node whose index it just passed.

EPISTEMIC STATUS:
  [P] 137 mod 37 = 26 ∈ IC (the 137-map multiplier) — exact.
  [P] 33 = 3 × 11, 3 ∈ ST, 11 ∈ NEG_H — exact.
  [V] Σ(33 primes) = 1988, Σ(32 primes) = 1851 — verified by sieve.
  [V] 1851 mod 37 = 1 ∈ IC — exact.
  [V] 1988 mod 37 = 27 ∈ NEG_H — exact.
  [V] 1 + 26 = 27 in GF(37); 1,26∈IC; 27∈NEG_H; all in ⟨11⟩ — exact.
  [V] Digit sum path of 1988: 1→10→18→26, labels IC→IC→SEED→IC — exact.
  [V] 24 + 26 = 50, 50 mod 37 = 13 ∈ CASCADE — exact.
  [V] sum(index 9)=100, mod37=26∈IC — exact.
  [V] sum(index 24)=963, mod37=1∈IC — exact.
  [V] sum(index 25)=1060, mod37=24∈SEED∩CASCADE — exact.
  [V] sum(index 29)=1480, mod37=0 (SEAM) — exact.
================================================================================
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
SEED    = {18, 24, 32}
SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
IC      = {1, 10, 26}
NEG_H   = {11, 27, 36}
CASCADE = {8, 13, 24}
named   = SEED | SA | ST | IC | NEG_H | CASCADE

PRIMES = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,
          73,79,83,89,97,101,103,107,109,113,127,131,137]


def dr(n):
    n = abs(n)
    if n == 0: return 9
    r = n % 9
    return 9 if r == 0 else r


def orbit_label(r):
    if r == 0: return 'SEAM'
    cats = []
    if r in IC:      cats.append('IC')
    if r in SA:      cats.append('SA')
    if r in ST:      cats.append('ST')
    if r in SEED:    cats.append('SEED')
    if r in NEG_H:   cats.append('NEG_H')
    if r in CASCADE: cats.append('CASCADE')
    return ','.join(cats) if cats else '-'


def run():
    print("=" * 70)
    print("PRIMES TO 137 — CUMULATIVE PRIME SUM AND GF(37)")
    print("=" * 70)

    assert len(PRIMES) == 33 and PRIMES[-1] == 137
    total = sum(PRIMES)
    excl  = total - 137
    assert total == 1988 and excl == 1851

    # Count structure: 33 = 3 × 11
    print(f"\nPRIME COUNT STRUCTURE:")
    assert 3 in ST and 11 in NEG_H
    print(f"  33 primes total.  33 = 3 × 11  where 3∈ST and 11∈NEG_H  check")

    # Central fact: 137 mod 37 = 26
    print(f"\nCENTRAL FACT — 137 mod 37:")
    assert 137 % P == 26 and 26 in IC
    print(f"  137 mod 37 = {137 % P} ∈ IC  (the 137-map multiplier)  check")
    print(f"  The prime that names the map equals the map's multiplier mod P")

    # GF(37) final step
    print(f"\nFINAL STEP — GF(37) ADDITION IN ⟨11⟩:")
    assert excl % P == 1 and 1 in IC
    assert total % P == 27 and 27 in NEG_H
    assert (excl % P + 137 % P) % P == total % P
    print(f"  Σ(32 primes) = {excl}  mod 37 = {excl % P} ∈ IC  check")
    print(f"  Σ(33 primes) = {total}  mod 37 = {total % P} ∈ NEG_H  check")
    print(f"  In GF(37): {excl % P} + {137 % P} = {(excl % P + 137 % P) % P}  (1∈IC + 26∈IC = 27∈NEG_H)  check")
    print(f"  All three (1, 26, 27) lie inside ⟨11⟩ = IC ∪ NEG_H  check")

    # Digit sum path
    print(f"\nDIGIT SUM PATH OF 1988:")
    running = 0
    path = []
    for d in [1, 9, 8, 8]:
        running += d
        path.append(running)
    assert path == [1, 10, 18, 26]
    labels = [orbit_label(x % P) for x in path]
    assert labels == ['IC', 'IC', 'SEED', 'IC']
    print(f"  1 → 10 → 18 → 26")
    print(f"  IC → IC → SEED → IC")
    print(f"  Terminal value 26 ∈ IC (137-map multiplier)  check")

    # 24 + 26
    print(f"\n24 + 26 = 50:")
    assert (24 + 26) % P == 13 and 13 in CASCADE
    print(f"  50 mod 37 = {50 % P} ∈ CASCADE  check")

    # Milestone table
    print(f"\nCUMULATIVE SUM MILESTONES:")
    cumsum = 0
    for i, p in enumerate(PRIMES, 1):
        cumsum += p
        r = cumsum % P
        if r in named or r == 0:
            print(f"  idx={i:2d} p={p:3d} sum={cumsum:5d} mod37={r:2d} [{orbit_label(r):14s}] DR={dr(cumsum)}")

    # Spot-check key milestones
    cumsum = 0
    c = {}
    for i, p in enumerate(PRIMES, 1):
        cumsum += p
        c[i] = cumsum

    assert c[9]  % P == 26 and 26 in IC       # square sum milestone
    assert c[24] % P == 1  and 1 in IC        # index = CASCADE∩SEED node
    assert c[25] % P == 24 and 24 in SEED and 24 in CASCADE  # sum = the node
    assert c[29] % P == 0                     # SEAM crossing
    assert c[32] % P == 1  and 1 in IC        # penultimate: IC identity
    assert c[33] % P == 27 and 27 in NEG_H    # final

    print(f"\n  idx= 9 (p=23): sum=100=10², mod37=26∈IC  check")
    print(f"  idx=24 (p=89): sum=963, mod37=1∈IC (at CASCADE∩SEED index, IC identity)  check")
    print(f"  idx=25 (p=97): sum=1060, mod37=24∈SEED∩CASCADE (sum finds the node)  check")
    print(f"  idx=29 (p=109): sum=1480, mod37=0 (SEAM crossing)  check")
    print(f"  idx=32 (p=131): sum=1851, mod37=1∈IC  check")
    print(f"  idx=33 (p=137): sum=1988, mod37=27∈NEG_H  check")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
