# CLASS: THEOREM
"""
T432 — The carry map and the digital-root ring Z/(b-1)

Definitions. s_b(x) = base-b digit sum. dr_b(x) = the digital root (x mod b-1 with
0 -> b-1 for x > 0). CARRY MAP C_b(x, y) = number of carries when adding x + y in
base b.

(1) KUMMER'S IDENTITY (proved). C_b(x,y) = (s_b(x) + s_b(y) - s_b(x+y)) / (b-1).
    Each carry replaces a column sum b by digit 0 plus 1 carried: the digit sum
    drops by exactly b - 1. Hence s_b(x) + s_b(y) and s_b(x+y) lie in the same coset
    of (b-1)Z, and C_b counts the coset steps between them. This is WHY digital
    roots are additive mod b-1: carries are invisible modulo b-1.

(2) BOUNDARY CARRIES (proved). If D + d = b^k with D, d >= 1 and v = v_b(D) (trailing
    zeros), then v_b(d) = v and C_b(D, d) = k - v exactly: below position v both
    digits are 0 (no carry); at position v the digits sum to b; above, each column
    is (b-1) + carry = b, up to position k-1. Therefore
        s_b(D) + s_b(d) = 1 + (b-1)(k - v),
    and dr_b(D) + dr_b(d) = b (the supplied "absolute invariant", which needs
    D, d >= 1; it fails at d = 0). The carry DEPTH is k - v, unbounded in k.

(3) THE DIGITAL-ROOT RING R_b = Z/(b-1). With n = b - 1 = prod p_i^a_i:
      units          phi(n), group = prod (Z/p_i^a_i)^x  (cyclic iff n in {1,2,4,p^a,2p^a})
                     (the table lists these prime-power factors, e.g. n=35 prints
                      C4xC6 = (Z/5)^x (Z/7)^x, which is C2xC12 in invariant factors)
      idempotents    2^omega(n)      (one per CRT splitting)
      nilpotents     n / rad(n)
      zero divisors  n - phi(n) - 1  (nonzero non-units)
      2 invertible   iff n odd       iff b even  (the midpoint inverse b/2)
    CLASS: FIELD if n prime; LOCAL if n a prime power; MIXED if omega(n) >= 2.

(4) BASE 13: R_13 = Z/12 = Z/4 x Z/3, MIXED. Units {1,5,7,11} = C2 x C2 (not
    cyclic: every unit squares to 1). Idempotents {0,1,4,9}. Nilpotents {0,6}. Zero
    divisors {2,3,4,6,8,9,10}. 2 not invertible (13 odd). Digit ring Z/13 = F_13,
    primitive roots {2,6,7,11}.

(5) GF(37). Base 38 is the base whose digital-root ring IS GF(37) (38 - 1 = 37):
    in base 38 casting out 37s is dr, and the 137-map (x -> 26x) acts on digital
    roots. Base 37 (the prime itself) has R_37 = Z/36 = Z/4 x Z/9, MIXED, units
    C2 x C6 (order 12), 4 idempotents, 6 nilpotents; 2 not invertible (37 odd).
    Recorded as structure; no claim that base 38 is otherwise distinguished.

(6) BASE 37 (m = 36 = 2^2 * 3^2, MIXED). Seven proper islands (2),(3),(4),(6),
    (9),(12),(18); nilradical (6) = {0,6,12,18,24,30}; idempotents {0,1,9,28}
    (9 = (1,0), 28 = (0,1) under Z/4 x Z/9); 12 units, orders 1,2,3,6 (C2 x C6).
    CARRY COMPLEMENT f(r) = 1 - r: NO fixed point (36 even), so two parts with
    D + d = 37^k never share a digital root. f sends every island I onto 1 + I; a
    coset a + (d) is preserved iff 2a = 1 (mod d), possible only for odd d:
    a = 2 for (3), a = 5 for (9); no coset of an even-index island is preserved.
    DOUBLING x2: not a permutation (image = (2), 18 elements). Every orbit reaches
    the ideal (4) within 2 steps (the Z/4 component dies), and (4) = Z/9 via
    x -> x mod 9. On it x2 is EXACTLY base 10's picture: unit cycle
    (4 8 16 32 28 20) = (4 8 7 5 1 2) mod 9, island cycle (12 24) = (3 6), fixed 0
    (the 9 class). Base 37 doubling = transient collapse onto base 10's 3-6-9 ring.
    DIGITAL-ROOT RING = DISCRETE-LOG RING. 2 is primitive mod 37, so dlog_2:
    GF(37)* -> Z/36 is an isomorphism and the base-37 digital-root ring is the
    exponent ring of GF(37)*. The 137-map x -> 26x has dlog_2(26) = 12, so it is
    translation by 12 on Z/36 and its 12 orbits are the cosets of the island (12).
    PRIOR ART: the Z/12 orbit quotient is T138 (also T200, T285, T339, "dlog mod
    12"). New here only: that quotient is Z/36 modulo the ideal (12) of the
    base-37 digital-root ring. dr_37(137) = 29, a unit of order 6.

(7) BASE 38 (m = 37: the root ring IS GF(37), a FIELD). Dual of base 37: the
    digit ring Z/38 = Z/2 x Z/19 is mixed while the root ring is a field (base 37
    had digit field F_37 and mixed root ring Z/36). Each carry lowers the digit sum
    by 37, so s_38(x) = x (mod 37): the base-38 digital root is reduction in GF(37).
    No proper islands (ideals); nilradical {0}; idempotents {0,1}; x2 is a single
    36-cycle on units (2 primitive mod 37) plus fixed 0.
    CARRY COMPLEMENT f(r) = 1 - r: exactly one fixed point, r = 19 = b/2 = 2^-1,
    and 19 lies in CAS_EXT = {5,13,19}. For D + d = 38^k (D, d >= 1) the digital
    roots sum to 38 and coincide only when both are 19.
    THEOREM: f maps NO coset xH of any subgroup H of GF(37)* with |H| = d >= 2
    onto a coset. Proof: sum_{h in H} h = 0 (the d-th roots of unity), so
    1 - xH = yH would give d = 0 in GF(37), impossible for d <= 36. In particular
    no 137-orbit (coset of <26>) maps to an orbit. f fixes 19 and swaps the
    primitive sixth roots 11 <-> 27 (roots of r^2 - r + 1), both in NEG_H;
    f(NEG_H) = {2, 11, 27}.
    The 12 x 12 incidence #{x in O_i : 1 - x in O_j} is the order-12 cyclotomic
    number matrix of p = 37 (Gauss/Dickson) -- standard, recorded not claimed.

FALSIFICATION: any assertion below failing.
"""
import random
from math import gcd
from sympy import factorint, totient, primitive_root, is_primitive_root


def digits(x, b):
    out = []
    while x:
        out.append(x % b)
        x //= b
    return out


def s(x, b):
    return sum(digits(x, b))


def carries(x, y, b):
    c = n = 0
    while x or y or c:
        t = x % b + y % b + c
        c = 1 if t >= b else 0
        n += c
        x //= b
        y //= b
    return n


def dr(x, b):
    return 0 if x == 0 else 1 + (x - 1) % (b - 1)


def vb(x, b):
    v = 0
    while x % b == 0:
        x //= b
        v += 1
    return v


# (1) Kummer's identity
random.seed(432)
for _ in range(20000):
    b = random.randint(2, 40)
    x = random.randint(0, 10**12)
    y = random.randint(0, 10**12)
    assert (s(x, b) + s(y, b) - s(x + y, b)) == (b - 1) * carries(x, y, b)

# (2) boundary carries
for b in range(2, 30):
    for k in range(1, 6):
        N = b**k
        for D in range(1, N, max(1, N // 300)):
            d = N - D
            v = vb(D, b)
            assert vb(d, b) == v
            assert carries(D, d, b) == k - v
            assert s(D, b) + s(d, b) == 1 + (b - 1) * (k - v)
            assert dr(D, b) + dr(d, b) == b


# (3) the ring Z/n, n = b - 1
def elementary_divisors_units(n):
    out = []
    for p, a in factorint(n).items():
        if p == 2:
            if a == 2:
                out.append(2)
            elif a >= 3:
                out += [2, 2 ** (a - 2)]
        else:
            out.append((p - 1) * p ** (a - 1))
    return sorted(x for x in out if x > 1)


def ring_profile(n):
    U = [x for x in range(n) if gcd(x, n) == 1]
    idem = [x for x in range(n) if x * x % n == x]
    nil = [x for x in range(n) if pow(x, n, n) == 0]  # x^n = 0 iff nilpotent
    zd = [x for x in range(1, n) if gcd(x, n) > 1]
    om = len(factorint(n))
    kind = "FIELD" if om == 1 and max(factorint(n).values()) == 1 else ("LOCAL" if om == 1 else "MIXED")
    rad = 1
    for p in factorint(n):
        rad *= p
    # closed forms
    assert len(U) == totient(n)
    assert len(idem) == 2**om
    assert len(nil) == n // rad
    assert len(zd) == n - totient(n) - 1
    # unit-group structure: element-order census matches the elementary divisors
    ed = elementary_divisors_units(n)
    cyclic = any(is_primitive_root(g, n) for g in U) if n > 2 else True
    assert cyclic == (len(ed) <= 1)
    return dict(n=n, kind=kind, units=len(U), unit_group=ed or [1], cyclic=cyclic,
                idempotents=idem, nilpotents=nil, zero_divisors=len(zd), two_inv=gcd(2, n) == 1)


TABLE = {b: ring_profile(b - 1) for b in range(3, 41)}
for b, r in TABLE.items():
    assert r["two_inv"] == (b % 2 == 0)

# (4) base 13
r13 = TABLE[13]
assert r13["kind"] == "MIXED" and r13["unit_group"] == [2, 2] and not r13["cyclic"]
assert r13["idempotents"] == [0, 1, 4, 9] and r13["nilpotents"] == [0, 6]
assert [x for x in range(1, 12) if gcd(x, 12) > 1] == [2, 3, 4, 6, 8, 9, 10]
assert all(u * u % 12 == 1 for u in (1, 5, 7, 11))
assert [g for g in range(1, 13) if is_primitive_root(g, 13)] == [2, 6, 7, 11]

# (5) GF(37)
r38 = TABLE[38]
assert r38["kind"] == "FIELD" and r38["units"] == 36 and r38["cyclic"]
r37 = TABLE[37]
assert r37["kind"] == "MIXED" and r37["unit_group"] == [2, 6] and len(r37["idempotents"]) == 4
assert len(r37["nilpotents"]) == 6 and not r37["two_inv"]
assert primitive_root(37) == 2

# (6) base 37: carry map coset structure on Z/36
m = 36
assert [d for d in range(2, m) if m % d == 0] == [2, 3, 4, 6, 9, 12, 18]
assert [x for x in range(m) if pow(x, m, m) == 0] == [0, 6, 12, 18, 24, 30]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 9, 28]
assert not [r for r in range(m) if (1 - r) % m == r]
pres = {d: [a for a in range(d) if (1 - a) % d == a] for d in (2, 3, 4, 6, 9, 12, 18)}
assert pres == {2: [], 3: [2], 4: [], 6: [], 9: [5], 12: [], 18: []}
assert len({2 * x % m for x in range(m)}) == 18
assert all(any((x * 2**k) % 4 == 0 for k in range(3)) for x in range(m))
cyc = [4, 8, 16, 32, 28, 20]
assert all(cyc[(i + 1) % 6] == 2 * cyc[i] % m for i in range(6))
assert [x % 9 for x in cyc] == [4, 8, 7, 5, 1, 2] and [12 % 9, 24 % 9] == [3, 6]
assert sorted(x % 9 for x in range(0, m, 4)) == list(range(9))
DLOG = {pow(2, k, 37): k for k in range(36)}
assert len(DLOG) == 36 and DLOG[26] == 12
ORB = {frozenset({x, 26 * x % 37, 26 * 26 * x % 37}) for x in range(1, 37)}
assert len(ORB) == 12 and all(len({DLOG[y] % 12 for y in o}) == 1 for o in ORB)
assert 137 % 36 == 29

# (7) base 38: root ring GF(37)
p = 37
assert [r for r in range(p) if (1 - r) % p == r] == [19] and 2 * 19 % p == 1
CAS_EXT = {5, 13, 19}
assert 19 in CAS_EXT
assert sorted((1 - x) % p for x in (11, 27, 36)) == [2, 11, 27]
assert [r for r in range(p) if (r * r - r + 1) % p == 0] == [11, 27]
assert all(pow(2, k, p) != 1 for k in range(1, 36))
for d in (2, 3, 4, 6, 9, 12, 18, 36):
    H = {pow(2, 36 // d * i, p) for i in range(d)}
    assert sum(H) % p == 0
    cos = {frozenset(x * h % p for h in H) for x in range(1, p)}
    assert not any(frozenset((1 - x) % p for x in c) in cos for c in cos)

if __name__ == "__main__":
    print("T432 carry map + digital-root rings")
    print("  (1) Kummer C_b = (s(x)+s(y)-s(x+y))/(b-1): 20000 random checks, b = 2..40")
    print("  (2) D + d = b^k: carries = k - v_b(D); s(D)+s(d) = 1+(b-1)(k-v); dr sum = b")
    print(f"  {'b':>3} {'n=b-1':>6} {'class':>6} {'|U|':>4} {'U structure':>14} "
          f"{'#idem':>5} {'#nil':>4} {'#zd':>4} {'2^-1':>5}")
    for b, r in TABLE.items():
        ug = "x".join(f"C{x}" for x in r["unit_group"])
        print(f"  {b:>3} {r['n']:>6} {r['kind']:>6} {r['units']:>4} {ug:>14} "
              f"{len(r['idempotents']):>5} {len(r['nilpotents']):>4} {r['zero_divisors']:>4} "
              f"{'yes' if r['two_inv'] else 'no':>5}")
    cls = {}
    for b, r in TABLE.items():
        cls.setdefault(r["kind"], []).append(b)
    for k, v in cls.items():
        print(f"  {k}: bases {v}")
