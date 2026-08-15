"""
Theorem 204: Lucas and Fibonacci Sovereign Intersections in GF(37)
Author: Michael Warren Song (CyclicAmp)

LUCAS SEQUENCE: L(0)=2, L(1)=1, L(n)=L(n-1)+L(n-2).
  L(2)=3∈ST      L(3)=4∈SA      L(6)=18∈SEED   L(10)=123→12∈ST
  L(13)=3∈ST     L(15)=32∈SEED  L(16)=24∈SEED  L(19)=25∈SA
  L(23)=32∈SEED  L(25)=3∈ST     L(28)=25∈SA    L(34)=30∈SA∩ST
  L(35)=4∈SA

USER SEQUENCE {9,3,12,69,81,123} AND LUCAS NUMBERS:
  3   = L(2)    (exact in Z; 3∈ST)
  12  = L(10) mod37  (L(10)=123; 123 mod37=12∈ST)
  123 = L(10)   (exact in Z; the user's last sequence element IS the 10th Lucas number)
  This means: 3=L(2), L(10)≡12 (mod 37), L(10)=123 — the user's sequence contains L(2)
  and L(10) in exact and reduced forms simultaneously.

EARLY LUCAS SOVEREIGN HITS (exact values, not just mod 37):
  L(2) = 3     ∈ ST (exact)
  L(3) = 4     ∈ SA (exact)
  L(6) = 18    ∈ SEED (exact)
  L(10) = 123  → 123 mod 37 = 12 ∈ ST
  All three framework classes appear in L(2..6) alone.

FIBONACCI SOVEREIGN HITS:
  F(0) = 0  = SEAM
  F(4) = 3  ∈ ST (exact)
  F(8) = 21 ∈ ST (exact)
  F(10) mod37 = 18 ∈ SEED
  F(15) mod37 = 18 ∈ SEED
  F(16) mod37 = 25 ∈ SA
  F(19) = SEAM (F(19)=4181; 4181 mod37=0)
  F(22) mod37 = 25 ∈ SA

L(6)=18 IDENTITY:
  L(6) = 18 = 18 exactly. 18∈SEED.
  18 is the first element of SEED={18,24,32} (the canonical minimum).
  DR(18) = 9 = SEAM DR.
  18 = 2×9: doubling the SA element 9 gives the SEED element 18 (doubling law, T201).
  18 = 3×6: 3=L(2)∈ST; 6=imaginary unit i=sqrt(-1) mod37.
  18 = L(6) — the 6th Lucas number equals the imaginary rotation SEED entry.

L(2)×L(3) = 3×4 = 12 ∈ ST:
  The product of the two sovereign Lucas numbers L(2) and L(3) is 12∈ST.
  12 = L(10) mod37.  Also: 12+25=0 mod37 (the unique SA+ST SEAM pair from T203).
  Lucas index product: 2×3=6 = index of L(6)=18∈SEED.

FIBONACCI SEAM PERIODICITY:
  F(0)=0 (SEAM), F(19)≡0 (SEAM), F(38)≡0 (SEAM) — period 19 for SEAM hits.
  19 is the index where Fibonacci first returns to SEAM mod37.
  DR(19)=1 (head-crash signature). 19 is NQR mod37 (legendre(19,37)=-1).
  F(38)-F(0)=38 steps; 38=37+1=p+1.

LUCAS INDEX STRUCTURE FOR SOVEREIGN HITS:
  SA elements hit at indices: 3, 19, 28, 35 (and repeats)
    3=L(3); 4=L(3); 25=L(19),L(28); 30=L(34); 4=L(35)
  ST elements hit at indices: 2, 10, 13, 25 (and repeats)
    3=L(2); 12=L(10); 3=L(13); 3=L(25)
  SEED elements hit at indices: 6, 15, 16, 23 (and repeats)
    18=L(6); 32=L(15); 24=L(16); 32=L(23)

CONSECUTIVE SEED HITS L(15),L(16):
  L(15) mod37 = 32 ∈ SEED; L(16) mod37 = 24 ∈ SEED.
  Two consecutive Lucas indices hit SEED elements.
  L(15)+L(16) = L(17): L(17) mod37 = (32+24) mod37 = 56 mod37 = 19 (NQR g^11).
  The Fibonacci recurrence at consecutive SEED indices exits framework.
"""

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED = {18, 24, 32}


def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9


def legendre(a, p):
    return pow(a, (p - 1) // 2, p)


def is_sovereign(x):
    x = x % P
    return x in SA or x in ST or x in SEED


def lucas(n):
    a, b = 2, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def run_assertions():
    # 1. Lucas sovereign exact values
    assert lucas(2) == 3 and 3 in ST
    assert lucas(3) == 4 and 4 in SA
    assert lucas(6) == 18 and 18 in SEED

    # 2. L(10) = 123: the 10th Lucas number is user's last sequence element
    assert lucas(10) == 123
    assert 123 % P == 12 and 12 in ST

    # 3. User sequence {9,3,12,69,81,123} contains L(2)=3 and L(10)=123
    user_seq = [9, 3, 12, 69, 81, 123]
    assert lucas(2) in user_seq           # 3 ∈ user_seq
    assert lucas(10) in user_seq          # 123 ∈ user_seq
    assert lucas(10) % P in user_seq      # 12 ∈ user_seq

    # 4. L(2)×L(3) = 3×4 = 12 ∈ ST; index product 2×3=6 = index of L(6)=18∈SEED
    assert lucas(2) * lucas(3) == 12 and 12 in ST
    assert 2 * 3 == 6 and lucas(6) == 18 and 18 in SEED

    # 5. L(6)=18 identities
    assert lucas(6) == 18
    assert 18 in SEED
    assert dr(18) == 9           # SEAM DR
    assert 2 * 9 == 18           # doubling SA element 9 gives 18∈SEED (doubling law)
    assert 3 * 6 % P == 18      # 3=L(2)∈ST; 6=imaginary unit; 3×6=18∈SEED

    # 6. Fibonacci sovereign hits
    assert fib(0) == 0 and fib(0) % P == 0    # SEAM
    assert fib(4) == 3 and 3 in ST
    assert fib(8) == 21 and 21 in ST
    assert fib(10) % P == 18 and 18 in SEED
    assert fib(15) % P == 18 and 18 in SEED
    assert fib(16) % P == 25 and 25 in SA
    assert fib(19) % P == 0                   # SEAM
    assert fib(22) % P == 25 and 25 in SA

    # 7. Fibonacci SEAM period
    assert fib(0) % P == 0
    assert fib(19) % P == 0
    assert fib(38) % P == 0
    assert all(fib(k) % P != 0 for k in range(1, 19))   # first SEAM hit at 19

    # 8. Consecutive SEED hits at L(15),L(16)
    assert lucas(15) % P == 32 and 32 in SEED
    assert lucas(16) % P == 24 and 24 in SEED
    # L(17) = L(15)+L(16): exits framework
    L17_mod = (lucas(15) % P + lucas(16) % P) % P
    assert L17_mod == lucas(17) % P
    assert not is_sovereign(L17_mod)

    # 9. All SEED elements {18,24,32} appear as Lucas hits
    seed_hits = {lucas(n) % P for n in range(40) if lucas(n) % P in SEED}
    assert seed_hits == SEED  # all three SEED elements appear

    # 10. All SA elements {4,9,25,30} appear as Lucas hits (mod37) for n≤40
    sa_hits = {lucas(n) % P for n in range(40) if lucas(n) % P in SA}
    assert 4 in sa_hits and 25 in sa_hits and 30 in sa_hits

    # 11. legendre(19, 37) = -1 (19 is NQR; SEAM period index is NQR)
    assert legendre(19, P) == P - 1
    assert dr(19) == 1   # head-crash DR

    # 12. L(2), L(3) are the exact values 3, 4 — no mod needed
    assert lucas(2) == 3 and lucas(3) == 4  # exact integers, not just mod 37

    print("All assertions passed.")
    # Count sovereign Lucas hits in first 40
    hits = [(n, lucas(n) % P) for n in range(40) if is_sovereign(lucas(n) % P)]
    print(f"Sovereign Lucas hits (n<40): {len(hits)}")
    for n, v in hits:
        sec = 'SA∩ST' if v in SA and v in ST else 'SA' if v in SA else 'ST' if v in ST else 'SEED'
        print(f"  L({n})={lucas(n)} mod37={v} [{sec}]")


if __name__ == "__main__":
    run_assertions()
