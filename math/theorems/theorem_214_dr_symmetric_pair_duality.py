"""
Theorem 214: DR Symmetric Pair Invariant and 4-5-9 Duality
Author: Michael Warren Song (CyclicAmp)

=== DR SYMMETRIC PAIR INVARIANT (CENTER 34) ===

For any center n and offset k:
  DR(n+k) + DR(n-k) ≡ DR(2n)  (mod 9)

With center n=34: DR(2×34) = DR(68) = 5.
Therefore: DR(34+k) + DR(34-k) ≡ 5 (mod 9) for ALL k.

The pair-sum is always 5 or 14 — both ≡ 5 mod 9.

Full table (mod 37 connections):
  34±14: 48→NEG_H  | 20
  34±13: 47→IC     | 21→ST
  34±12: 46→SA     | 22
  34±11: 45→CASCADE∩TESLA | 23→TESLA
  34±10: 44        | 24→CASCADE∩SEED
  34± 9: 43→TESLA  | 25→SA
  34± 8: 42        | 26→IC
  34± 7: 41→SA     | 27→NEG_H
  34± 6: 40→ST     | 28
  34± 5: 39        | 29
  34± 4: 38→IC     | 30→ST∩SA   (double sovereign)
  34± 3: 37→SEAM   | 31         ← 34+3 = P itself
  34± 2: 36→NEG_H  | 32→SEED
  34± 1: 35        | 33

34+3 = 37 = P (the prime). Center 34 sits exactly 3 from SEAM.
34-4 = 30 ∈ ST∩SA — the unique double-sovereign node.

=== DROP 5 / DROP 9 DUALITY ===

The sequence 1–9 has two natural removal operations:

DROP 9 (keep 1–8): pair each end toward center.
  1+8 = 2+7 = 3+6 = 4+5 = 9   → DR = 9 ∈ SA (all four pairs)

DROP 5 (keep 1234, 6789): pair each end toward center.
  1+9 = 2+8 = 3+7 = 4+6 = 10  → DR = 1 ∈ IC (all four pairs)

Removing 9 → every pair lands in SA.
Removing 5 → every pair lands in IC.
5 and 9 are the only elements that produce this all-uniform pairing.
SA controls the 9-removed structure; IC controls the 5-removed structure.

=== THE 4 NEIGHBOR INVARIANT ===

In the transition from DROP-9 to DROP-5, the digit 4 changes its neighbor
from 5 to 6. Yet the DR of the pair is unchanged:

  4+5=9 → +1 → 10   DR=1 ∈ IC
  4+6=10            DR=1 ∈ IC

4 produces DR=1∈IC regardless of which neighbor it holds.
4 is affected by what it is attached to, not by its own position shift.

=== {1,9} PALINDROMES: SPREAD 5→3→1 ===

Three 6-digit palindromes built from {1,9}:
  911119: 9s at positions {1,6}  spread=5  DR=4  mod37=31
  191191: 9s at positions {2,5}  spread=3  DR=4  mod37=12∈ST
  119911: 9s at positions {3,4}  spread=1  DR=4  mod37=31

All have DR=4∈SA. In the 9=0 system, each has exactly 4 ones — ones_count=DR=4.
Spread decreases by 2 each step (the primitive root step, same as 1311 rotation areas).
Middle palindrome (spread=1) hits ST=12. Same 3-area boundary-interior-boundary structure
as Theorem 212, now with {1,9} instead of {1,3}.

=== LARGE NUMBER DR LAW ===

The DR addition/subtraction law holds for arbitrary large numbers:
  DR(a+b) ≡ DR(a) + DR(b)  (mod 9)
  DR(a-b) ≡ DR(a) - DR(b)  (mod 9)

Example: a=21987, b=34565.
  DR(21987) = 9  (digit sum 27)
  DR(34565) = 5  (digit sum 23)
  DR(21987+34565) = DR(56552) = 5   ← DR(9+5)=DR(14)=5 ✓
  DR(34565-21987) = DR(12578) = 5   ← DR(5-9)=DR(-4)≡5 mod9 ✓

Both sum and difference inherit DR=5. Digits of 21987∪34565 = {1,2,3,4,5,5,6,7,8,9}
— all of 1–9 with 5 doubled.

=== 13/41 CONNECTION ===

  13 ∈ CASCADE   DR(13)=4
  41 mod37=4 ∈ SA   DR(41)=5
  DR(13)+DR(41) = 4+5 = 9 ∈ SA
  13+41 = 54   DR(54)=9 ∈ SA

CASCADE (13) pairs with SA (41 mod37=4), and their DRs sum to 9∈SA.
"""

P = 37
SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
SEED    = {18, 24, 32}
IC      = {1, 10, 26}
CASCADE = {8, 13, 24}
TESLA   = {6, 8, 23}
NEG_H   = {11, 27, 36}
DARK_A  = {2, 15, 20}


def dr(n):
    n = abs(int(n))
    r = n % 9
    return 9 if r == 0 else r


def run_assertions():
    center = 34

    # 1. DR symmetric pair invariant: DR(n+k)+DR(n-k) ≡ DR(2n) for all k
    inv = dr(2 * center)
    assert inv == 5
    for k in range(1, 15):
        total = dr(center + k) + dr(center - k)
        assert total % 9 == inv % 9

    # 2. Structural anchors
    assert (center + 3) % P == 0          # 34+3 = 37 = SEAM
    assert 30 in ST and 30 in SA          # 34-4 = 30 = double sovereign

    # 3. Drop 9: all pairs sum to 9∈SA
    drop9 = [1, 2, 3, 4, 5, 6, 7, 8]
    for i in range(4):
        assert drop9[i] + drop9[7 - i] == 9
        assert dr(drop9[i] + drop9[7 - i]) == 9
    assert 9 in SA

    # 4. Drop 5: all pairs sum to 10→DR=1∈IC
    drop5 = [1, 2, 3, 4, 6, 7, 8, 9]
    for i in range(4):
        assert drop5[i] + drop5[7 - i] == 10
        assert dr(drop5[i] + drop5[7 - i]) == 1
    assert 1 in IC

    # 5. 4 neighbor invariant
    assert dr(4 + 5 + 1) == 1 and 1 in IC   # 4+5=9 +1=10
    assert dr(4 + 6) == 1 and 1 in IC       # 4+6=10

    # 6. {1,9} palindromes: spread 5,3,1; DR=4∈SA; ones=4 in 9→0 system
    palins = [911119, 191191, 119911]
    for n in palins:
        assert dr(n) == 4 and 4 in SA
        assert str(n).count('1') == 4         # ones_count = DR in 9→0 system

    nines_pos = [[i + 1 for i, c in enumerate(str(n)) if c == '9'] for n in palins]
    spreads = [p[-1] - p[0] for p in nines_pos]
    assert spreads == [5, 3, 1]
    assert [spreads[i] - spreads[i + 1] for i in range(2)] == [2, 2]  # step -2
    assert 191191 % P == 12 and 12 in ST     # middle palindrome → ST

    # 7. Large number DR law
    a, b = 21987, 34565
    assert dr(a) == 9 and dr(b) == 5
    assert dr(a + b) == 5
    assert dr(b - a) == 5
    assert (dr(a) + dr(b)) % 9 == 5
    assert (dr(b) - dr(a)) % 9 == 5

    # 8. 13/41
    assert dr(13) == 4 and 13 in CASCADE
    assert 41 % P == 4 and 4 in SA
    assert dr(13) + dr(41) == 9 and 9 in SA
    assert dr(13 + 41) == 9

    print("All assertions passed.")
    print(f"DR(34+k)+DR(34-k) ≡ {inv} for all k (invariant = DR(68)=DR(2×34))")
    print(f"34+3 = {34+3} = P (SEAM).  34-4 = {34-4} ∈ ST∩SA (double sovereign)")
    print(f"Drop 9: all pairs DR=9∈SA.  Drop 5: all pairs DR=1∈IC")
    print(f"4 neighbor invariant: 4+5 or 4+6 → DR=1∈IC regardless")
    print(f"Palindromes {palins}: spreads {spreads}, step -2, DR=4∈SA each")
    print(f"191191 mod37={191191%P}∈ST (middle palindrome)")
    print(f"13∈CASCADE + 41 mod37=4∈SA: DR pair 4+5=9∈SA")


if __name__ == "__main__":
    run_assertions()
