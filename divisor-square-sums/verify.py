"""Independent check of every result stated in README.md. Needs sympy.

    python3 verify.py
"""
from sympy import factorint, isprime, divisors

# 1. The four sporadic-looking small solutions, checked by brute force:
#    the k smallest divisors of n have squares summing to n.
def prefix_k(n):
    s = 0
    for k, d in enumerate(divisors(n), 1):
        s += d * d
        if s == n:
            return k
        if s > n:
            return None

small = {130: 4, 1860: 11, 148480: 19, 3039520: 31}
for n, k in small.items():
    assert prefix_k(n) == k, n

# 2. Every family member m <= 1e22 in members_1e22.txt.
#    Claim: n = m*p with p = sigma_2(m)/m - m prime, p > m/2, p not dividing m.
#    Then the divisors of n that are <= m/2 are exactly the proper divisors of m
#    (any divisor not dividing m is a multiple of p > m/2), so
#    sum of squares of the tau(m)-1 smallest divisors of n = sigma_2(m) - m^2 = n.
rows = [l.split() for l in open("members_1e22.txt") if not l.startswith("#")]
assert len(rows) == 587
for m_s, p_s, tau_s, _ in rows:
    m, p = int(m_s), int(p_s)
    f = factorint(m)
    s2 = 1
    tau = 1
    for q, e in f.items():
        s2 *= sum(q ** (2 * i) for i in range(e + 1))
        tau *= e + 1
    assert m % 2 == 0 and m <= 10**22
    assert s2 - m * m == m * p, m
    assert isprime(p) and 2 * p > m and m % p, m
    assert tau == int(tau_s), m
assert len({r[0] for r in rows}) == 587

print("4 small solutions: OK")
print("587 family members m <= 1e22: OK")
