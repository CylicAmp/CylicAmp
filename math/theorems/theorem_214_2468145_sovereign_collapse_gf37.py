"""
Theorem 214: Sovereign Collapse of 2,468,145 in GF(37)
Author: Michael Warren Song (CyclicAmp)

THE NUMBER: 2,468,145

GF(37) POSITION:
  2,468,145 mod 37 = 23.
  23 ∈ g^3 = {6, 8, 23} = SEED-gen coset.
  The number lands in the same coset as 8 (N, the phased array elements)
  and 6 (the imaginary unit i = √(-1) in GF(37)).
  23 is the largest element of the SEED-gen coset — and the cubing target
  of the SEED coset: 8^5 ≡ 23 (mod 37), meaning x³=23 for x∈SEED (T208).

DIGIT SUM SOVEREIGN HIT:
  Digits: 2+4+6+8+1+4+5 = 30.
  30 ∈ SA ∩ ST — the unique doubly sovereign element (the only element in
  both the anchor set and the target set simultaneously).
  This is the most distinguished element in the framework: it is the
  additive generator of the SA∪ST sum (T209: sum(SA∪ST)=30∈SA∩ST).

TWO-STEP SOVEREIGN COLLAPSE:
  2,468,145  →  digit sum = 30 ∈ SA∩ST  →  DR = 3 = ST signature.
  Step 1: The digit sum lands exactly on the doubly sovereign element.
  Step 2: DR of that element is 3, the universal DR signature of ALL ST elements
          (T210: every element of ST has DR=3).
  The number collapses through SA∩ST to the ST signature in two steps.

THE 2+4=6+6=12→3 CHAIN (T210 TRINITY TABLE):
  2 + 4 = 6:
    First two digits sum to the third digit (6). In GF(37): 2+4=6∈SEED-gen (imaginary unit coset).
  6 + 6 = 12 → DR = 3:
    This is entry (6,6) in the T210 DR-addition table: DR(6+6)=3 ✓ (trinity rule).
    12 ∈ ST; DR(12) = 3 = ST DR signature.
  1 + 2 + 3 = 6:
    The digits of 12 concatenated with 3 (i.e., "123") sum to 6.
    6 is the DR of 6 itself — the imaginary unit returns.
  The chain 6 → 12 → 3 → 6 is a cycle: 6 maps to 3 (by T210 doubling), and 3 maps
  back to 6 (by T210: DR(3+3)=6). The cycle {3,6} is the non-identity orbit of Z/3Z
  (the trinity group from T210, with identity=9).

DIGIT-BY-DIGIT GF(37) SECTORS:
  digit[0]=2: g^1 (primitive root coset)
  digit[1]=4: SA (sovereign anchor)
  digit[2]=6: g^3 = SEED-gen (imaginary unit)
  digit[3]=8: g^3 = SEED-gen (cascade element, N of phased array)
  digit[4]=1: <26> (137-map subgroup, kernel of cubing)
  digit[5]=4: SA (sovereign anchor — appears twice)
  digit[6]=5: g^11

  The digit sequence 2,4,6,8 is an arithmetic progression (step +2).
  In GF(37): these advance from g^1 → SA → SEED-gen → SEED-gen.
  The step of +2 in Z matches the twin prime gap and the DR-addition step (T212).

FACTORIZATION:
  2,468,145 = 3 × 5 × 17 × 9679.
  Factor 3 ∈ ST (the ST generator, L(2)=3, DR=3).
  3 divides 2,468,145 because DR(2,468,145)=3 (divisibility rule for 3).
  NOT divisible by 9: DR=3, not 9.

CONNECTIONS TO EXISTING THEOREMS:
  T208 (cubing map): cubing target of SEED (g^5) is 8^5=23∈SEED-gen. The number
       2,468,145 ≡ 23 mod 37 = exactly this cubing target.
  T210 (trinity): the chain 6→12→3→6 is the {3,6} orbit in Z/3Z under doubling.
  T209 (sum structure): digit sum=30∈SA∩ST matches the framework sum result.
  T207 (binomial): Row 11=P-26; sovereign C(11,k) all equal 18∈SEED.
       Digit[2]=6=i, digit[3]=8=N: both in SEED-gen, the coset feeding SEED cubing.

CUBING TARGET CLOSURE:
  2,468,145 ≡ 23 (mod 37).
  23 is the cubing target value: x³ ≡ 23 means x ∈ SEED = {18,24,32}.
  The seed orbit {18,24,32} (from seed=246 mod37=24) are the cube roots of 23.
  So: the seed orbit elements {18,24,32} are exactly the cube roots of
  (2,468,145 mod 37) in GF(37).
  The number 2,468,145 is a "cube attractor" for the seed orbit in GF(37).
"""

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED = {18, 24, 32}
SEED_GEN = {6, 8, 23}
SG26 = {1, 10, 26}
framework = SA | ST | SEED

N = 2468145


def ds(n):
    return sum(int(d) for d in str(abs(n)))


def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9


def run_assertions():
    # 1. GF(37) position
    assert N % P == 23
    assert 23 in SEED_GEN

    # 2. 23 is the cubing target of SEED (g^5): 8^5 mod37 = 23
    assert pow(8, 5, P) == 23 and 23 in SEED_GEN

    # 3. Seed orbit are cube roots of 23
    assert {x for x in range(1, P) if pow(x, 3, P) == 23} == SEED
    assert SEED == {18, 24, 32}

    # 4. Digit sum = 30 ∈ SA∩ST
    assert ds(N) == 30
    assert 30 in SA and 30 in ST

    # 5. DR = 3 = ST signature
    assert dr(N) == 3
    assert all(dr(x) == 3 for x in ST)  # universal ST DR signature

    # 6. Two-step sovereign collapse
    assert ds(N) == 30 and 30 in SA and 30 in ST   # step 1: digit sum ∈ SA∩ST
    assert dr(ds(N)) == 3                            # step 2: DR = ST signature

    # 7. 2+4=6 chain in Z and GF(37)
    assert 2 + 4 == 6
    assert 6 in SEED_GEN  # imaginary unit coset in GF(37)
    assert (2 + 4) % P == 6

    # 8. 6+6=12→3 is T210 trinity table entry
    assert 6 + 6 == 12 and 12 in ST and dr(12) == 3

    # 9. 1+2+3=6 (digits of "123" sum to 6, return to imaginary unit)
    assert 1 + 2 + 3 == 6

    # 10. Cycle {3,6} under T210 doubling: DR(3+3)=6, DR(6+6)=3
    assert dr(3 + 3) == 6
    assert dr(6 + 6) == 3

    # 11. Digit 2+4+6+8 arithmetic progression (step +2)
    digits_2468 = [2, 4, 6, 8]
    assert all(digits_2468[i+1] - digits_2468[i] == 2 for i in range(3))

    # 12. Digit sectors: 4∈SA (appears at positions 1 and 5), 6,8∈SEED-gen
    assert 4 in SA
    assert 6 in SEED_GEN and 8 in SEED_GEN

    # 13. Factor 3∈ST divides N (because DR=3)
    assert N % 3 == 0 and 3 in ST
    assert N % 9 != 0   # DR=3, not 9

    # 14. 30∈SA∩ST is the framework sum (T209: sum(SA∪ST) mod37=30)
    assert sum(SA | ST) % P == 30 and ds(N) == 30

    # 15. The cubing target 23: N≡23 means SEED={18,24,32} are cube roots of N mod37
    assert N % P == 23
    for s in SEED:
        assert pow(s, 3, P) == N % P   # each SEED element cubes to N mod37

    print("All assertions passed.")
    print(f"{N:,} mod 37 = {N%P} ∈ SEED-gen — cube attractor for seed orbit {{18,24,32}}")
    print(f"Digit sum = {ds(N)} ∈ SA∩ST (doubly sovereign)")
    print(f"DR = {dr(N)} = ST signature")
    print(f"Chain: 2+4=6∈SEED-gen → 6+6=12∈ST → DR(12)=3 → 1+2+3=6 (returns)")
    print(f"SEED cube roots of {N%P}: {sorted(x for x in range(1,P) if pow(x,3,P)==N%P)}")


if __name__ == "__main__":
    run_assertions()
