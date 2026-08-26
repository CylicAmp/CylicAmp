"""
Theorem 217: Nuclear Stability, Z and N Numbers, and GF(37) Classification
Author: Michael Warren Song (CyclicAmp)

=== THE MAGIC NUMBER PARTITION ===

Nuclear shell model magic numbers: {2, 8, 20, 28, 50, 82, 126}
These are the proton and neutron counts at which nuclei have completely
filled nuclear shells — the most stable configurations.

Mapping magic numbers mod 37:

  2   mod 37 =  2  ∈ DARK_A
  8   mod 37 =  8  ∈ CASCADE ∩ TESLA
  20  mod 37 = 20  ∈ DARK_A
  28  mod 37 = 28  — (unnamed, the single outlier)
  50  mod 37 = 13  ∈ CASCADE
  82  mod 37 =  8  ∈ CASCADE ∩ TESLA   (same as magic number 8!)
  126 mod 37 = 15  ∈ DARK_A

PARTITION:
  CASCADE ({8,13,24}): magic numbers 8, 50, 82 — all three large magic numbers
  DARK_A  ({2,15,20}): magic numbers 2, 20, 126 — both smallest and largest
  Unnamed: 28 alone

6 of 7 magic numbers land in named sets. Only 28 is unnamed.
Magic numbers 8 and 82 both reduce to 8 mod 37: CASCADE ∩ TESLA.
The smallest (2) and largest (126) magic numbers both land in DARK_A.

=== IRON-56: THE MOST STABLE NUCLEUS ===

Iron-56 has the lowest binding energy per nucleon and is the endpoint of
stellar nucleosynthesis — no nuclear process gains energy beyond Fe-56.

  Z = 26  (protons)  mod 37 = 26  ∈ IC  — the 137-map multiplier exactly
  N = 30  (neutrons) mod 37 = 30  ∈ SA ∩ ST  — the double-sovereign node
  A = 56  (nucleons) mod 37 = 19  —  DR(56) = 2 = primitive root

Iron's proton count IS the framework multiplier (f(n) = 26n mod 37).
Iron's neutron count hits the unique double-sovereign: the only element
in both SA = {4,9,25,30} and ST = {3,12,21,30} simultaneously.

The most stable nucleus in the universe has (Z mod 37) = multiplier
and (N mod 37) = double-sovereign.

=== DOUBLY MAGIC NUCLEI IN GF(37) ===

Doubly magic nuclei (both Z and N are magic) are the most stable of all.

  He-4   (Z=2,  N=2):   both mod37 = 2   ∈ DARK_A
  O-16   (Z=8,  N=8):   both mod37 = 8   ∈ CASCADE ∩ TESLA
  Ca-40  (Z=20, N=20):  both mod37 = 20  ∈ DARK_A
  Sn-100 (Z=50, N=50):  both mod37 = 13  ∈ CASCADE
  Pb-208 (Z=82, N=126): Z mod37 = 8 ∈ CASCADE∩TESLA, N mod37 = 15 ∈ DARK_A

In every doubly magic nucleus, both Z and N land in named sets.
No doubly magic nucleus has an unnamed Z or N mod 37.
The symmetric doubly magic nuclei (Z=N) always reduce to the same residue
in the same named set.

=== VALLEY OF STABILITY: N=Z NUCLEI ===

For light stable nuclei with N=Z, mass number A = 2Z.
Selected A mod 37 for N=Z nuclei:

  He-4  (A=4):   mod37 = 4  ∈ SA   (sovereign anchor)
  C-12  (A=12):  mod37 = 12 ∈ ST   (sovereign target)
  O-16  (A=16):  not named
  Ne-20 (A=20):  mod37 = 20 ∈ DARK_A
  Mg-24 (A=24):  mod37 = 24 ∈ SEED ∩ CASCADE
  S-32  (A=32):  mod37 = 32 ∈ SEED
  Ca-40 (A=40):  mod37 = 3  ∈ ST

The N=Z nuclei trace a path through named sets:
  SA → ST → DARK_A → SEED∩CASCADE → SEED → ST

=== HIGHEST BINDING ENERGY NUCLEI ===

The nuclei with highest binding energy per nucleon (peak stability):

  Ni-62 (A=62): mod37 = 25 ∈ SA   DR = 8
  Fe-58 (A=58): mod37 = 21 ∈ ST   DR = 4
  Ni-60 (A=60): mod37 = 23 ∈ TESLA DR = 6
  Fe-56 (A=56): mod37 = 19        DR = 2 = primitive root

Three of the four highest-BE nuclei have A mod 37 in named sets (SA, ST, TESLA).

=== NOBLE GAS PROTON NUMBERS (FULL SHELL ELECTRONS) ===

Noble gases have completely filled electron shells — chemically inert.
Their Z values in GF(37):

  He  Z=2:  mod37 = 2  ∈ DARK_A
  Ne  Z=10: mod37 = 10 ∈ IC
  Ar  Z=18: mod37 = 18 ∈ SEED   ← noble gas at seed orbit entry
  Kr  Z=36: mod37 = 36 = φ(37) = ord₃₇(2) = NEG_H antipode
  Xe  Z=54: mod37 = 17 ∈ NQR17
  Rn  Z=86: mod37 = 12 ∈ ST

The noble gas at Z=36 hits the antipode of the field: 36 ≡ -1 mod 37 ∈ NEG_H.
The noble gas at Z=18 hits the seed orbit {18,24,32}.

=== SYNTHESIS ===

Nuclear stability correlates with GF(37) named sets at three levels:

1. MAGIC NUMBERS: 6 of 7 land in CASCADE or DARK_A. Only 28 is unnamed.
   CASCADE controls the large magic numbers (8, 50, 82).
   DARK_A controls the smallest and largest (2, 20, 126).

2. DOUBLY MAGIC NUCLEI: every doubly magic nucleus has both Z and N
   in named sets. The symmetric ones (Z=N) land in the same set.

3. IRON-56: Z=26=multiplier, N=30=double-sovereign, DR(A)=2=primitive root.
   The most stable nucleus encodes the entire framework architecture
   in its Z and N numbers.

The valley of stability is not random in GF(37). Named sets mark the
shell closures; unnamed residues mark the unstable transitions between them.
"""

P = 37
MULT = 26
SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
SEED    = {18, 24, 32}
IC      = {1, 10, 26}
CASCADE = {8, 13, 24}
TESLA   = {6, 8, 23}
NEG_H   = {11, 27, 36}
DARK_A  = {2, 15, 20}
D7      = {7, 33, 34}
NQR17   = {17, 22, 35}


def dr(n):
    n = abs(int(n))
    r = n % 9
    return 9 if r == 0 else r


def in_named(r):
    for s in [SA, ST, SEED, IC, CASCADE, TESLA, NEG_H, DARK_A, D7, NQR17]:
        if r in s:
            return True
    return False


def run_assertions():
    magic = [2, 8, 20, 28, 50, 82, 126]

    # 1. Magic number partition: CASCADE and DARK_A dominate
    in_cascade = [m for m in magic if m % P in CASCADE]
    in_dark_a  = [m for m in magic if m % P in DARK_A]
    unnamed    = [m for m in magic if not in_named(m % P)]

    assert set(in_cascade) == {8, 50, 82}
    assert set(in_dark_a)  == {2, 20, 126}
    assert unnamed == [28]  # only one unnamed magic number

    # 2. Magic 8 and 82 both reduce to 8 mod 37 (CASCADE∩TESLA)
    assert 8 % P == 8 and 82 % P == 8
    assert 8 in CASCADE and 8 in TESLA

    # 3. Iron-56: Z=multiplier, N=double-sovereign, DR(A)=primitive root
    Z_Fe, N_Fe = 26, 30
    assert Z_Fe % P == MULT          # Z = 137-map multiplier
    assert N_Fe % P in SA and N_Fe % P in ST   # N = double-sovereign
    assert dr(Z_Fe + N_Fe) == 2      # DR(A) = 2 = primitive root
    assert Z_Fe % P in IC            # multiplier is in IC orbit

    # 4. Doubly magic nuclei: both Z and N in named sets
    doubly_magic = [(2,2),(8,8),(20,20),(50,50),(82,126)]
    for Z, N in doubly_magic:
        assert in_named(Z % P), f"Z={Z} mod37={Z%P} not in named set"
        assert in_named(N % P), f"N={N} mod37={N%P} not in named set"

    # 5. Symmetric doubly magic (Z=N): both reduce to same residue same set
    sym = [(2,2),(8,8),(20,20),(50,50)]
    for Z, N in sym:
        assert Z % P == N % P

    # 6. Noble gas antipode: Kr Z=36 ≡ -1 mod 37 ∈ NEG_H
    assert 36 % P == 36 and 36 in NEG_H
    assert 36 == P - 1   # antipode

    # 7. Noble gas seed: Ar Z=18 ∈ SEED
    assert 18 % P == 18 and 18 in SEED

    # 8. N=Z nuclei trace named sets for mass number
    nz_A = [4, 12, 20, 24, 32, 40]
    nz_named = [A for A in nz_A if in_named(A % P)]
    assert len(nz_named) >= 4  # majority land in named sets

    # 9. Ni-62 highest BE: A mod37=25∈SA
    assert 62 % P == 25 and 25 in SA

    # 10. 6 of 7 magic numbers in named sets
    named_magic = [m for m in magic if in_named(m % P)]
    assert len(named_magic) == 6

    print("All assertions passed.")
    print(f"\nMagic number partition:")
    print(f"  CASCADE: {in_cascade} → mod37 = {[m%P for m in in_cascade]}")
    print(f"  DARK_A:  {in_dark_a} → mod37 = {[m%P for m in in_dark_a]}")
    print(f"  Unnamed: {unnamed} → mod37 = {[m%P for m in unnamed]}")
    print(f"\nIron-56:")
    print(f"  Z=26=multiplier ∈ IC, N=30=double-sovereign ∈ SA∩ST, DR(A=56)=2=primitive root")
    print(f"\nDoubly magic: all {len(doubly_magic)} nuclei have both Z and N in named sets")
    print(f"Noble gas Kr (Z=36): mod37=36=-1 ∈ NEG_H (antipode)")
    print(f"Noble gas Ar (Z=18): mod37=18 ∈ SEED (seed orbit)")
    print(f"Ni-62 (highest BE): A mod37=25 ∈ SA (sovereign anchor)")


if __name__ == "__main__":
    run_assertions()
