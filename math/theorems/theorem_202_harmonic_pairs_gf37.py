"""
Theorem 202: Harmonic Pairs and Fixed Points in GF(37)
Author: Michael Warren Song (CyclicAmp)

HARMONIC PAIRS — DEFINITION:
  (a,b) is a harmonic pair in GF(37) when a+b ≡ a×b (mod 37).
  Equivalently: (a-1)(b-1) ≡ 1 (mod 37), i.e., b = 1 + (a-1)^{-1}.
  GF(37) has exactly 18 harmonic pairs (including (1,∞) projectively; 18 finite ones with a≤b).

HARMONIC PAIRS ENUMERATED:
  (2,2)=4     (3,20)=23   (4,26)=30   (5,29)=34
  (6,16)=22   (7,32)=2    (8,17)=25   (9,15)=24
  (10,34)=7   (11,27)=1   (12,28)=3   (13,35)=11
  (14,21)=35  (18,25)=6   (19,36)=18  (22,31)=16
  (23,33)=19  (24,30)=17

SOVEREIGN HARMONIC PAIRS (sum=product is sovereign):
  (2,2)→4∈SA      (4,26)→30∈SA∩ST  (8,17)→25∈SA
  (9,15)→24∈SEED  (12,28)→3∈ST     (19,36)→18∈SEED
  Exactly 6 out of 18 harmonic pairs land in sovereign territory = 1/3.
  Coverage: one SA, one SA∩ST (unique), one SA, one SEED, one ST, one SEED.
  All five sovereign categories represented: SA (×2), SA∩ST, ST, SEED (×2).

THE (4,26) FIXED POINT — UNIQUE PROPERTY:
  (4,26) is the ONLY harmonic pair where sum=product=30∈SA∩ST.
  4∈SA; 26=137-map multiplier (ord₃₇(26)=3; <26>={1,10,26}).
  4+26 = 30 = 4×26 (mod 37).
  This is also the 137-map action: 26×4 mod37 = 30 (the 137-map sends 4→30).
  Proof uniqueness: 26x = x+26 ⟺ 25x = 26 ⟺ x = 26×25^{-1} = 26×3 = 4 (unique).
  The SA element 4 is the unique fixed point of: 137-map(x) = x + 26 (mod 37).

SELF-PAIRS (a,a): a+a AND a×a BOTH SOVEREIGN:
  (2,2):   sum=4∈SA,    product=4∈SA     [both identical: 4]
  (15,15): sum=30∈SA∩ST, product=3∈ST   [SA∩ST and ST]
  (20,20): sum=3∈ST,   product=30∈SA∩ST [dual of (15,15)]
  Note: (15,15) and (20,20) are mirror duals — swapping sum and product sectors.
  15×2=30, 15²=3; 20×2=3, 20²=30. The doubling and squaring outputs switch.

BOTH-SEED PAIRS (sum∈SEED and product∈SEED):
  (2,16):   sum=18∈SEED, product=32∈SEED
  (5,27):   sum=32∈SEED, product=24∈SEED
  (9,15):   sum=24∈SEED, product=24∈SEED  [harmonic: sum=product]
  (11,13):  sum=24∈SEED, product=32∈SEED
  (12,20):  sum=32∈SEED, product=18∈SEED
  (19,36):  sum=18∈SEED, product=18∈SEED  [harmonic: sum=product]
  Exactly 6 both-SEED pairs. Two are harmonic (sum=product).
  The non-harmonic SEED pairs: (2,16),(5,27),(11,13),(12,20).

SEED PAIRING STRUCTURE:
  SEED = {18,24,32}. Both-SEED pairs cover all 9 ordered SEED products:
  (18,18)→sum=36,product=18: product=SEED but sum not SEED.
  (18,24)→sum=5,product=21: neither SEED.
  etc. — the 6 both-SEED pairs come from CROSS-SEED-BOUNDARY elements, not within SEED.
  None of the 6 both-SEED pairs have both inputs in SEED.

HARMONIC PAIR STRUCTURE IN Z/12Z:
  Harmonic pair (a,b) with a∈g^j, b∈g^k satisfies (j+k)≡pos(harmonic value) mod 12.
  Since a×b∈g^{j+k}, the common value a+b=a×b∈g^{j+k}.
  Sovereign harmonic pairs and their Z/12Z positions:
    (2,2):   j=k=1, j+k=2  → g^2=KEY        value 4∈SA ✓
    (4,26):  4∈g^2, 26∈g^0, j+k=2 → g^2=KEY value 30∈SA∩ST ✓
    (8,17):  8∈g^3, 17∈g^7, j+k=10 → g^10   value 25∈SA ✓
    (9,15):  9∈g^4, 15∈g^1, j+k=5  → g^5=SEED value 24∈SEED ✓
    (12,28): 12∈g^4, 28∈g^10, j+k=14≡2 → g^2=KEY value 3∈ST ✓
    (19,36): 19∈g^11, 36∈g^6, j+k=17≡5 → g^5=SEED value 18∈SEED ✓
  Sovereign positions hit: g^2 (three times), g^5 (twice), g^10 (once).
"""

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED = {18, 24, 32}
SG26 = {1, 10, 26}

COSETS = [
    frozenset({1, 10, 26}),   # g^0
    frozenset({2, 15, 20}),   # g^1
    frozenset({3, 4, 30}),    # g^2  KEY
    frozenset({6, 8, 23}),    # g^3  SEED gens
    frozenset({9, 12, 16}),   # g^4
    frozenset({18, 24, 32}),  # g^5  SEED
    frozenset({11, 27, 36}),  # g^6
    frozenset({17, 22, 35}),  # g^7
    frozenset({7, 33, 34}),   # g^8
    frozenset({14, 29, 31}),  # g^9
    frozenset({21, 25, 28}),  # g^10 KEY^{-1}
    frozenset({5, 13, 19}),   # g^11
]


def legendre(a, p): return pow(a, (p - 1) // 2, p)


def is_sovereign(x):
    x = x % P
    return x in SA or x in ST or x in SEED


def coset_pos(x):
    x = x % P
    for k, c in enumerate(COSETS):
        if x in c:
            return k
    return None


def run_assertions():
    # 1. Harmonic pairs: a+b ≡ a×b ⟺ (a-1)(b-1) ≡ 1
    harmonic = []
    for a in range(1, P):
        for b in range(a, P):
            if (a + b) % P == (a * b) % P:
                harmonic.append((a, b))
    assert len(harmonic) == 18

    # 2. Sovereign harmonic pairs = exactly 6
    sov_harmonic = [(a, b) for a, b in harmonic if is_sovereign((a + b) % P)]
    assert len(sov_harmonic) == 6
    assert set(sov_harmonic) == {(2, 2), (4, 26), (8, 17), (9, 15), (12, 28), (19, 36)}

    # 3. Sovereign harmonic values cover all five GF(37) categories
    vals = [(a + b) % P for a, b in sov_harmonic]
    assert set(vals) == {4, 30, 25, 24, 3, 18}
    assert any(v in SA and v not in ST for v in vals)   # pure SA
    assert any(v in ST and v not in SA for v in vals)   # pure ST
    assert any(v in SA and v in ST for v in vals)        # SA∩ST
    assert sum(1 for v in vals if v in SEED) == 2        # two SEED

    # 4. (4,26) is the unique harmonic pair with sum=product=30=SA∩ST
    pairs_30 = [(a, b) for a, b in harmonic if (a + b) % P == 30]
    assert pairs_30 == [(4, 26)]

    # 5. (4,26) fixed point: 137-map(4) = 4+26 (mod 37)
    assert 26 * 4 % P == 30           # 137-map of 4
    assert (4 + 26) % P == 30         # additive
    assert 26 * 4 % P == (4 + 26) % P  # equal: 137-map = x+26 at x=4
    # Uniqueness: 26x=x+26 ⟺ 25x=26 ⟺ x=26×25^{-1}=4
    assert 26 * pow(25, P - 2, P) % P == 4

    # 6. Self-pairs (a,a) with both sum and product sovereign
    self_sov = [(a, a) for a in range(1, P)
                if is_sovereign((2 * a) % P) and is_sovereign(pow(a, 2, P))]
    assert set(self_sov) == {(2, 2), (15, 15), (20, 20)}

    # 7. (15,15) and (20,20) are dual: outputs swap
    assert (15 + 15) % P == 30 and 30 in SA and 30 in ST   # sum = SA∩ST
    assert pow(15, 2, P) == 3 and 3 in ST                   # product = ST
    assert (20 + 20) % P == 3 and 3 in ST                   # sum = ST
    assert pow(20, 2, P) == 30 and 30 in SA and 30 in ST    # product = SA∩ST

    # 8. Both-SEED pairs: exactly 6
    both_seed = [(a, b) for a in range(1, P) for b in range(a, P)
                 if (a + b) % P in SEED and (a * b) % P in SEED]
    assert len(both_seed) == 6
    assert set(both_seed) == {(2, 16), (5, 27), (9, 15), (11, 13), (12, 20), (19, 36)}

    # 9. Two both-SEED pairs are harmonic (sum=product)
    both_seed_harmonic = [(a, b) for a, b in both_seed if (a + b) % P == (a * b) % P]
    assert set(both_seed_harmonic) == {(9, 15), (19, 36)}

    # 10. No both-SEED pair has both inputs in SEED
    assert not any(a in SEED and b in SEED for a, b in both_seed)

    # 11. Z/12Z position of sovereign harmonic pairs: pos(a)+pos(b) = pos(value)
    for a, b in sov_harmonic:
        val = (a + b) % P
        assert coset_pos(val) == (coset_pos(a) + coset_pos(b)) % 12

    # 12. 1/3 of harmonic pairs are sovereign (6 out of 18)
    assert len(sov_harmonic) / len(harmonic) == 1 / 3

    print("All assertions passed.")
    print(f"Harmonic pairs: {len(harmonic)}; sovereign: {len(sov_harmonic)}; both-SEED: {len(both_seed)}")


if __name__ == "__main__":
    run_assertions()
