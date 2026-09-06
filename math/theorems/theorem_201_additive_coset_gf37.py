"""
Theorem 201: Additive Coset Structure in GF(37) — Sum Factorization and Coset Displacement
Author: Michael Warren Song (CyclicAmp)

COSET POSITION TABLE (Z/12Z):
  g^0  = {1,10,26}   — identity/<26>
  g^1  = {2,15,20}   — doubling generator
  g^2  = {3,4,30}    — KEY (ST+SA+SA∩ST)
  g^3  = {6,8,23}    — SEED generators (NQR)
  g^4  = {9,12,16}   — SA+ST+free
  g^5  = {18,24,32}  — SEED (all primitive roots)
  g^6  = {11,27,36}  — free (36=-1)
  g^7  = {17,22,35}  — NQR
  g^8  = {7,33,34}   — free
  g^9  = {14,29,31}  — NQR
  g^10 = {21,25,28}  — KEY^{-1} (ST+SA+free)
  g^11 = {5,13,19}   — NQR

MULTIPLICATION DISPLACEMENT LAW (exact):
  For any a ∈ g^j and b ∈ g^k: a×b ∈ g^{j+k mod 12}.
  This is the Z/12Z quotient group law: coset positions add under multiplication.

DOUBLING LAW (special case):
  For any x ∈ g^k: x+x = 2x ∈ g^{k+1 mod 12}.
  Proof: x = 2^k × h for h ∈ <26>, so 2x = 2^{k+1} × h ∈ g^{k+1}.
  2 ∈ g^1, so multiplication by 2 always shifts coset position by +1.

SUM FACTORIZATION THEOREM:
  When a+b = c×d (in GF(37)), the sum a+b lands in g^{pos(c)+pos(d) mod 12}.
  Equivalently: factor the sum, then add coset positions.

USER EQUATIONS FACTORED:
  3+6  = 3×(1+2) = 3×3  = 9:  pos=2+2=4 → g^4 (SA+ST coset) ✓
  3+15 = 3×(1+5) = 3×6  = 18: pos=2+3=5 → g^5 (SEED)        ✓
  15+15= 15×(1+1)= 15×2 = 30: pos=1+1=2 → g^2 (KEY)          ✓
  6+6  = 6×(1+1) = 6×2  = 12: pos=3+1=4 → g^4 (SA+ST)        ✓
  9+3  = 3×(3+1) = 3×4  = 12: pos=2+2=4 → g^4 (SA+ST)        ✓
  6+3  = 3×(2+1) = 3×3  = 9:  pos=2+2=4 → g^4 (SA+ST)        ✓

ALL USER EQUATIONS:
  Every user equation sum factors as a product of elements in g^{≤3}.
  Sums land at positions {2, 4, 5} — all sovereign positions (KEY, SA+ST, SEED).
  No user equation sum lands outside the sovereign cosets.

DUAL SOVEREIGNTY — SUM AND PRODUCT BOTH SOVEREIGN:
  (3,6):   sum 3+6=9∈SA (g^4);     product 3×6=18∈SEED (g^5)  → BOTH SOVEREIGN
  (3,15):  sum 3+15=18∈SEED (g^5); product 3×15=8∈g^3 (SEED gen) → SEED + SEED gen
  (15,15): sum 15+15=30∈SA∩ST(g^2); product 15²=225 mod37=3∈KEY(g^2) → BOTH KEY
  (6,6):   sum 6+6=12∈ST (g^4);    product 6²=36∈g^6 (free, -1) → sum sovereign only
  (9,3):   sum 9+3=12∈ST (g^4);    product 9×3=27∈g^6 (free)    → sum sovereign only

PURE DUAL-SOVEREIGN PAIRS (both sum ∈ SA∪ST∪SEED and product ∈ SA∪ST∪SEED):
  Enumerated over all pairs (a,b) with a,b ∈ SA∪ST∪SEED:
  [computed in run_assertions]

POSITION ARITHMETIC — USER SEQUENCE:
  Sovereign positions used: g^2(KEY), g^4(SA+ST), g^5(SEED), g^10(KEY^{-1})
  Additive operations between them all land in sovereign positions.
  This exhausts the user's equation set {3+6, 3+15, 15+15, 6+6, 9+3, 6+3}.
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

SOVEREIGN_POSITIONS = {2, 4, 5, 10}  # KEY, SA+ST, SEED, KEY^{-1}


def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9


def legendre(a, p):
    return pow(a, (p - 1) // 2, p)


def sector(r):
    if r == 0: return 'SEAM'
    if r in SA and r in ST: return 'SA∩ST'
    if r in SA: return 'SA'
    if r in ST: return 'ST'
    if r in SEED: return 'SEED'
    if legendre(r, P) == P - 1: return 'NQR'
    return 'free'


def coset_pos(x):
    for k, c in enumerate(COSETS):
        if x % P in c:
            return k
    return None


def is_sovereign(x):
    x = x % P
    return x in SA or x in ST or x in SEED


def run_assertions():
    # 1. Full coset table covers all of GF(37)*
    all_elements = set()
    for c in COSETS:
        all_elements |= c
    assert all_elements == set(range(1, P))

    # 2. Each coset is a <26>-coset: {x, 10x, 26x} mod 37
    for k, c in enumerate(COSETS):
        rep = next(iter(c))
        assert frozenset(rep * h % P for h in SG26) == c

    # 3. Multiplication displacement law: pos(a*b) = pos(a)+pos(b) mod 12
    for j, cj in enumerate(COSETS):
        for k, ck in enumerate(COSETS):
            a = next(iter(cj))
            b = next(iter(ck))
            assert coset_pos(a * b % P) == (j + k) % 12

    # 4. Doubling law: x+x = 2x ∈ g^{pos(x)+1 mod 12}
    for k, c in enumerate(COSETS):
        for x in c:
            assert coset_pos(2 * x % P) == (k + 1) % 12

    # 5. User equation sums: all land in sovereign positions
    user_sums = [
        (3, 6),    # 3+6=9
        (3, 15),   # 3+15=18
        (15, 15),  # 15+15=30
        (6, 6),    # 6+6=12
        (9, 3),    # 9+3=12
        (6, 3),    # 6+3=9
    ]
    for a, b in user_sums:
        s = (a + b) % P
        assert is_sovereign(s), f"{a}+{b}={s} not sovereign"
        assert coset_pos(s) in SOVEREIGN_POSITIONS, f"pos {coset_pos(s)} not sovereign"

    # 6. Sum factorization verification
    # 3+6 = 3×3 → pos 2+2=4
    assert 3 + 6 == 3 * 3 and coset_pos(9) == 4
    # 3+15 = 3×6 → pos 2+3=5
    assert 3 + 15 == 3 * 6 and coset_pos(18) == 5
    # 15+15 = 2×15 → pos 1+1=2
    assert 15 + 15 == 2 * 15 and coset_pos(30) == 2
    # 6+6 = 2×6 → pos 1+3=4
    assert 6 + 6 == 2 * 6 and coset_pos(12) == 4
    # 9+3 = 3×4 → pos 2+2=4
    assert 9 + 3 == 3 * 4 and coset_pos(12) == 4
    # 6+3 = 3×3 → pos 2+2=4
    assert 6 + 3 == 3 * 3 and coset_pos(9) == 4

    # 7. Dual-sovereign pairs: sum AND product both sovereign, over all GF(37)*
    dual_sovereign = []
    for a in range(1, P):
        for b in range(a, P):
            s = (a + b) % P
            pr = (a * b) % P
            if is_sovereign(s) and is_sovereign(pr):
                dual_sovereign.append((a, b, s, pr))

    # Known dual-sovereign pairs from user equations
    assert (3, 6, 9, 18) in dual_sovereign   # 3+6=9∈SA, 3×6=18∈SEED
    assert (15, 15, 30, 3) in dual_sovereign  # 15+15=30∈SA∩ST, 15²=3∈ST

    # 8. User equation products and their positions
    # (3,6): product 3×6=18∈g^5=SEED; 2+3=5 ✓
    assert coset_pos(3 * 6 % P) == (coset_pos(3) + coset_pos(6)) % 12 == 5
    # (15,15): product 15²=225 mod37=225-6×37=225-222=3∈g^2; 1+1=2 ✓
    assert 15 * 15 % P == 3 and coset_pos(3) == 2
    assert coset_pos(15 * 15 % P) == (coset_pos(15) + coset_pos(15)) % 12 == 2

    # 9. The factor (1+2)=3 is itself in g^2=KEY; (1+5)=6 in g^3=SEED gen
    assert 1 + 2 == 3 and coset_pos(3) == 2    # factor for 3+6
    assert 1 + 5 == 6 and coset_pos(6) == 3    # factor for 3+15
    assert 1 + 1 == 2 and coset_pos(2) == 1    # factor for doublings

    # 10. Sovereign positions sum ≡ 9 mod 12 (SEAM, consistent with T200)
    assert sum(SOVEREIGN_POSITIONS) % 12 == 9

    print(f"Dual-sovereign pairs: {len(dual_sovereign)}")
    for a, b, s, pr in dual_sovereign:
        print(f"  ({a},{b}): sum={s}[{sector(s)}] product={pr}[{sector(pr)}]")
    print("All assertions passed.")


if __name__ == "__main__":
    run_assertions()
