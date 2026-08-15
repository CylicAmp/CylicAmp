"""
Theorem 211: {1,3,7} Permutation Diamond and 11-Ladder in GF(37)
Author: Michael Warren Song (CyclicAmp)

DISCOVERY ENGINE: script explorer.py runs three analyses.
This theorem records the GF(37) framework connections found in each.

=== ANALYSIS 1: {1,3,7} PERMUTATION DIAMOND ===

Six permutations of digits {1,3,7}: 137, 173, 317, 371, 713, 731.
Every permutation has digit sum 11 and DR = 2.
  11 = P - 26 = P - multiplier  (from T207: row 11 = P-mult)
  DR = 2 = DR of the primitive root g=2 mod37.

System aggregate sum: 137+173+317+371+713+731 = 2442.
  2442 = 66 × 37 = 66 × P ≡ 0 (mod 37): SEAM.
  digit_sum(2442) = 12 ∈ ST; DR(2442) = 3 = ST DR signature.
  2442 is a palindrome of {2,4}: digits are the primitive root 2 and SA element 4.

PRIMALITY STRATIFIES BY GF(37) COSET:
  PRIMES: 137, 173, 317 — their residues mod 37:
    137 ≡ 26  (the 137-map multiplier itself)
    173 ≡ 25  ∈ SA
    317 ≡ 21  ∈ ST
  COMPOSITES: 371, 713, 731 — their residues mod 37:
    371 ≡ 1   ∈ <26> (identity, kernel of cubing)
    713 ≡ 10  ∈ <26> (second element of <26>={1,10,26})
    731 ≡ 28  ∈ g^10 = KEY^{-1} coset {21,25,28}

  The 3 primes reduce to {multiplier, SA element, ST element}.
  Two composites reduce to elements of <26> — the 137-map subgroup, kernel of cubing.
  One composite reduces to KEY^{-1}=g^10.
  PRIMALITY PARTITIONS EXACTLY ALONG THE <26>-KERNEL vs FRAMEWORK/MULTIPLIER LINE.

137 IS THE MAP ITSELF:
  The prime 137 generates the entire framework through f(n) = 137n mod 37 = 26n mod 37.
  137 ≡ 26 (mod 37): the prime is its own multiplier mod P.
  DR(137) = 2 = DR of primitive root. digit_sum(137) = 11 = P-multiplier.

12→3 CONVERGENCE:
  Aggregate 2442 → digit_sum = 12 ∈ ST → DR = 3 = ST signature.
  The intermediate sum 12 is sovereign (ST); the digital root 3 is the defining DR of ST.
  This matches: DR(12)=3, DR(21)=3, DR(3)=3, DR(30)=3 — all ST elements have DR=3.

=== ANALYSIS 2: 11-LADDER (11×18 DOWN TO 11×9) ===

11 = P - multiplier. The ladder multiplies 11 by k ∈ {9,10,...,18}.
Range bounds: 9∈SA (bottom), 18∈SEED (top).
The ladder descends from 11×18 to 11×9: SEED index down to SA index.

DR SEQUENCE OF THE LADDER (descending k=18..9):
  DRs: 9, 7, 5, 3, 1, 8, 6, 4, 2, 9
  This is the COMPLETE TRAVERSAL of Z/9Z via the orbit of 9 under step -2.
  Each descent of 11 subtracts DR(11)=2 from the running DR in Z/9Z.
  The 10 terms cover all 9 digital roots, returning to 9.

11-LADDER GF(37) RESIDUES:
  11×18 = 198  ≡ 13  (cascade element! {8,13,24} from T201)
  11×17 = 187  ≡ 2   (primitive root)
  11×16 = 176  ≡ 28  ∈ g^10 (KEY^{-1})
  11×15 = 165  ≡ 17  ∈ g^7
  11×14 = 154  ≡ 6   ∈ g^3 (imaginary unit i = SEED-gen)
  11×13 = 143  ≡ 32  ∈ SEED
  11×12 = 132  ≡ 21  ∈ ST
  11×11 = 121  ≡ 10  ∈ <26>
  11×10 = 110  ≡ 36  = -1 (g^6, order 2)
  11×9  = 99   ≡ 25  ∈ SA

  Ladder hits in GF(37): 13∈cascade; 32∈SEED; 21∈ST; 25∈SA; 6=imaginary unit.
  Endpoint: 11×9=99≡25∈SA; start: 11×18=198≡13∈cascade {8,13,24}.
  11×13=143≡32∈SEED: the half-multiplier (13) times (P-mult) = SEED element.

=== ANALYSIS 3: BIRTHDAY PROBLEM ON 9 STATES ===

N=9 states = the 9 digital root values {1,...,9} = Z/9Z*.
Birthday threshold (first n with P(collision) > 50%): n = 4.
  4 ∈ SA: the birthday threshold is a sovereign anchor.
  At n=4: P(unique) ≈ 46.09%, P(collision) ≈ 53.91%.

n=2 case: P(unique) = 8/9 ≈ 88.89%.
  8 ∈ g^3 (SEED-gen coset). 8 = number of phased array elements.
  8/9: the probability is the ratio of (SEED-gen element)/(SA element).

n=9 (saturation): P(unique) = 1/9! × 9! × 1 → ≈0.09%; effectively guaranteed collision.
  9∈SA: at n=9 elements in a 9-state space, saturation is complete. The SA element
  is simultaneously the state count AND the saturation threshold.
"""

import itertools
from math import isqrt

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED = {18, 24, 32}
SG26 = {1, 10, 26}
KEYINV = frozenset({21, 25, 28})
CASCADE = {8, 13, 24}
framework = SA | ST | SEED


def is_prime(n):
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0 or n % 3 == 0: return False
    for i in range(5, isqrt(n) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0: return False
    return True


def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9


def digit_sum(n):
    return sum(int(d) for d in str(abs(n)))


def run_assertions():
    # 1. {1,3,7} permutations
    perms = sorted(set(int("".join(map(str, p)))
                       for p in itertools.permutations((1, 3, 7))))
    assert perms == [137, 173, 317, 371, 713, 731]

    # 2. All have digit sum 11 = P-multiplier and DR=2
    assert all(digit_sum(n) == 11 for n in perms)
    assert all(dr(n) == 2 for n in perms)
    assert 11 == P - 26   # P - multiplier

    # 3. Aggregate = 2442 = 66×P = SEAM
    assert sum(perms) == 2442
    assert 2442 % P == 0         # SEAM
    assert 2442 == 66 * P
    assert digit_sum(2442) == 12 and 12 in ST
    assert dr(2442) == 3 and all(dr(x) == 3 for x in ST)

    # 4. Primality vs GF(37) coset
    primes = [n for n in perms if is_prime(n)]
    composites = [n for n in perms if not is_prime(n)]
    assert primes == [137, 173, 317]
    assert composites == [371, 713, 731]

    # 5. Prime residues: {multiplier, SA, ST}
    prime_residues = {n % P for n in primes}
    assert prime_residues == {26, 25, 21}
    assert 26 not in framework  # multiplier (not framework)
    assert 25 in SA
    assert 21 in ST

    # 6. Composite residues: two in <26>, one in KEY^{-1}
    comp_residues = {n % P for n in composites}
    assert comp_residues == {1, 10, 28}
    assert {1, 10} <= SG26          # two elements of <26>
    assert 28 in KEYINV             # KEY^{-1} coset

    # 7. 137 ≡ 26 = multiplier
    assert 137 % P == 26
    assert dr(137) == 2             # DR = primitive root DR
    assert digit_sum(137) == 11     # digit sum = P - multiplier

    # 8. 12→3 convergence: ST intermediate, ST DR
    assert digit_sum(2442) == 12 and 12 in ST
    assert dr(12) == 3

    # 9. 11-Ladder DR traversal: complete Z/9Z via step -2
    ladder = [11 * k for k in range(18, 8, -1)]
    ladder_drs = [dr(v) for v in ladder]
    assert set(ladder_drs) == set(range(1, 10))   # all 9 DR values
    # Each step changes DR by -DR(11) = -2 in Z/9Z
    assert dr(11) == 2
    for i in range(len(ladder_drs) - 1):
        expected = (ladder_drs[i] - 2) % 9 or 9
        assert ladder_drs[i + 1] == expected

    # 10. 11-Ladder GF(37) residues: key framework hits
    ladder_residues = {11 * k % P for k in range(9, 19)}
    assert 13 in ladder_residues and 13 in CASCADE    # cascade hit at 11×18
    assert 32 in ladder_residues and 32 in SEED       # SEED hit at 11×13
    assert 21 in ladder_residues and 21 in ST         # ST hit at 11×12
    assert 25 in ladder_residues and 25 in SA         # SA hit at 11×9 (endpoint)
    assert 6 in ladder_residues                       # imaginary unit at 11×14

    # 11. Specific ladder anchors
    assert 11 * 18 % P == 13 and 13 in CASCADE
    assert 11 * 13 % P == 32 and 32 in SEED           # half-mult × (P-mult) = SEED
    assert 11 * 12 % P == 21 and 21 in ST
    assert 11 * 9 % P == 25 and 25 in SA              # endpoint = SA
    assert 11 * 14 % P == 6                           # imaginary unit

    # 12. 11 = P - multiplier; 11 ∈ g^6 = {11,27,36}
    assert 11 == P - 26
    assert 11 in frozenset({11, 27, 36})              # g^6: cube roots of -1

    # 13. Birthday problem: threshold n=4 ∈ SA
    p = 1.0
    for n in range(1, 5):
        p *= (9 - (n - 1)) / 9
    assert p < 0.5   # at n=4 unique probability < 50% → collision > 50%
    p_3 = (9/9) * (8/9) * (7/9)
    assert p_3 > 0.5  # at n=3 unique probability > 50%
    assert 4 in SA   # birthday threshold is SA element

    # 14. n=2 unique probability = 8/9; 8∈g^3
    assert abs((8/9) - (9/9)*(8/9)) < 1e-10
    assert 8 in frozenset({6, 8, 23})   # g^3 SEED-gen

    # 15. State count N=9 ∈ SA
    assert 9 in SA

    print("All assertions passed.")
    print(f"Primes {[137,173,317]} ≡ {[n%P for n in [137,173,317]]} (mod 37) = multiplier, SA, ST")
    print(f"Composites {[371,713,731]} ≡ {[n%P for n in [371,713,731]]} (mod 37) = <26>×2 + KEY^{{-1}}")
    print(f"2442 = {2442//P}×P ≡ 0 (SEAM); digit_sum→12∈ST; DR→3=ST signature")
    print(f"11-Ladder DRs: {[dr(11*k) for k in range(18,8,-1)]} — complete Z/9Z")
    print(f"Birthday threshold n=4∈SA in 9-state (DR) space")


if __name__ == "__main__":
    run_assertions()
