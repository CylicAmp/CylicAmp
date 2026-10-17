# CLASS: AUDIT
"""
The neighbor-difference sequence of 43 against the 45-digit seed (owner_work #308, 2026-10-17).

PASTED (another tool's text, relayed by the owner with no words of their own; not the owner's claims):
    "Starting number . 45 digits  123456789012345678910123456789012345678901234
     Length after one transformation: 89 digits.  Original digit sum: 193.
     compare your 45-digit seed with the original 43 sequence using the same neighbor-difference rule ...
     full comparison through 48 steps"

FAULT FIRST: the digit sum of that seed is 191, not 193. The seed has 45 digits and 2 x 45 - 1 = 89 is right.

THE RULE IS NOT DEFINED IN THE PASTE. Used here: between every two neighbouring digits a, b insert |a - b|
(43 -> 413 -> 43123 -> 413211213 ...); one step takes n digits to 2n - 1, as the paste says (45 -> 89). A variant,
(a - b) mod 10, also gives 2n - 1; it is checked at the end. If the earlier "43 sequence" used another rule, the
results below are for |a - b| only.

EXACT METHOD: the digit counts after k steps follow from the counts of neighbouring pairs, which obey one fixed
rule (the pair (a,b) becomes (a,d) and (d,b), d = |a-b|). Checked against writing the digits out for k <= 9. Every
number below is exact (big integers) up to k = 100; 2^48 + 1 digits are never written out.

RESULTS for |a - b|
  Length: L_k = 2^k + 1 for 43; 44 x 2^k + 1 for the seed.
  43, closed forms (hold for every k from 0 to 100; not proved for all k):
      #4 = 1,  #3 = floor(k/2) + 1,  #2 = floor(k^2/4),  #1 = 2 x #0 + C(k,2) + (k mod 2),
      #0 = (2^k + 1 - C(k,2) - (k mod 2) - floor(k^2/4) - floor(k/2) - 2) / 3.
      Only the 0s and 1s grow exponentially; the 2s grow like k^2/4 and the 3s like k/2; the 4 never comes back.
  Digit frequencies in the limit (what separates the two starts):
      zeros 1/3 and the sum-ratio S_k / S_(k-1) -> 2 are the same for every start (here: all 99 digit pairs
      and 20 random seeds). The nonzero digits are not: a neighbouring pair (a, b) ends up as zeros and g = gcd(a, b)
      in the ratio 1 : 2, so the frequency of a nonzero digit g is (2/3) x (share of neighbouring pairs with gcd g).
      43:    0 -> 1/3, 1 -> 2/3.   mean digit 2/3.
      seed:  0 -> 1/3, 1 -> 41/66, 9 -> 1/22 (the three 9-0 neighbours of the seed keep the 9s alive; gcd(9,0) = 9).
             mean digit 34/33.
  Digital root of the digit sum, dr(S_k): periodic from k = 0 with period 18 for 43 (784928151922427925 ...) and
      54 for the seed (254188499562474774 ...); dr(S_k) = 9 first at k = 3, 9, 15, ... for 43 and k = 7, 8, 26, 28 ...
      for the seed. dr of the digit sum is the number's own digital root (digit sums add mod 9).
  Variant (a - b) mod 10 (NOT in the paste): both starts converge to the same distribution,
      0 -> 1/18, 1 3 7 9 -> 5/36 each, 2 4 6 8 -> 5/72 each, 5 -> 1/9. There the limit does not depend on the start.

ANSWER to "universal or does it depend on the initial digits": with |a - b| the zeros (1/3), the doubling of the digit
sum and the exponential growth of 0s and 1s are universal; which nonzero digits survive, and the mean digit, depend on the
gcds of the neighbouring digits of the start.

FALSIFICATION: any assertion failing.
"""
from collections import Counter
from fractions import Fraction
from math import comb, gcd
import random

SEED = "123456789012345678910123456789012345678901234"


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def absd(a, b):
    return abs(a - b)


def mod10(a, b):
    return (a - b) % 10


def write_out(s, k, rule):
    d = [int(c) for c in s]
    for _ in range(k):
        out = [d[0]]
        for a, b in zip(d, d[1:]):
            out += [rule(a, b), b]
        d = out
    return d


def start(s):
    return Counter((int(a), int(b)) for a, b in zip(s, s[1:])), Counter(int(c) for c in s)


def step(P, C, rule):
    P2, C2 = Counter(), Counter(C)
    for (a, b), n in P.items():
        d = rule(a, b)
        P2[(a, d)] += n
        P2[(d, b)] += n
        C2[d] += n
    return P2, C2


def counts_by_step(s, K, rule=absd):
    P, C = start(s)
    out = [dict(C)]
    for _ in range(K):
        P, C = step(P, C, rule)
        out.append(dict(C))
    return out


def total(C):
    return sum(C.values())


def digit_sum(C):
    return sum(x * n for x, n in C.items())


# the pasted block
assert len(SEED) == 45 and sum(map(int, SEED)) == 191 != 193 and len(write_out(SEED, 1, absd)) == 89 == 2 * 45 - 1
assert write_out("43", 1, absd) == [4, 1, 3] and write_out("43", 2, absd) == [4, 3, 1, 2, 3] and write_out("43", 3, absd) == [4, 1, 3, 2, 1, 1, 2, 1, 3]
# pair-count method = writing the digits out
for rule in (absd, mod10):
    for s in ("43", SEED):
        by = counts_by_step(s, 9, rule)
        for k in range(10):
            d = write_out(s, k, rule)
            assert Counter(d) == Counter({x: n for x, n in by[k].items() if n}), (rule.__name__, s, k)
R43, RSEED = counts_by_step("43", 100), counts_by_step(SEED, 100)
assert all(total(R43[k]) == 2 ** k + 1 and total(RSEED[k]) == 44 * 2 ** k + 1 for k in range(101))
# closed forms of the 43 sequence
for k in range(101):
    c = R43[k]
    n2, n3, n4 = c.get(2, 0), c.get(3, 0), c.get(4, 0)
    assert n4 == 1 and n3 == k // 2 + 1 and n2 == k * k // 4, k
    assert c.get(1, 0) == 2 * c.get(0, 0) + comb(k, 2) + k % 2, k
    z = 2 ** k + 1 - comb(k, 2) - k % 2 - k * k // 4 - k // 2 - 2
    assert z % 3 == 0 and c.get(0, 0) == z // 3, k
    assert set(c) <= {0, 1, 2, 3, 4}
# limits
assert abs(R43[100][0] / total(R43[100]) - 1 / 3) < 1e-9 and abs(R43[100][1] / total(R43[100]) - 2 / 3) < 1e-9
for x, f in ((0, Fraction(1, 3)), (1, Fraction(41, 66)), (9, Fraction(1, 22))):
    assert abs(RSEED[100].get(x, 0) / total(RSEED[100]) - float(f)) < 1e-9
assert abs(digit_sum(RSEED[100]) / total(RSEED[100]) - 34 / 33) < 1e-9 and abs(digit_sum(R43[100]) / total(R43[100]) - 2 / 3) < 1e-9
assert Counter(gcd(int(a), int(b)) for a, b in zip(SEED, SEED[1:])) == {1: 41, 9: 3}
assert abs(digit_sum(R43[100]) / digit_sum(R43[99]) - 2) < 1e-9 and abs(digit_sum(RSEED[100]) / digit_sum(RSEED[99]) - 2) < 1e-9
for a in range(10):
    for b in range(10):
        if (a, b) != (0, 0):
            C = counts_by_step(f"{a}{b}", 60)[60]
            g = gcd(a, b)
            assert abs(C.get(0, 0) / total(C) - 1 / 3) < 1e-6 and abs(C.get(g, 0) / total(C) - 2 / 3) < 1e-6, (a, b)
random.seed(1)
for _ in range(20):
    s = "".join(random.choice("0123456789") for _ in range(random.randint(5, 60)))
    C = counts_by_step(s, 70)[70]
    n = len(s) - 1
    pairs = Counter(gcd(int(x), int(y)) for x, y in zip(s, s[1:]))
    zeros = pairs.pop(0, 0)
    pred = Counter({0: Fraction(zeros, n) + Fraction(1, 3) * Fraction(n - zeros, n)})
    for g, m in pairs.items():
        pred[g] += Fraction(2, 3) * Fraction(m, n)
    assert max(abs(C.get(x, 0) / total(C) - float(pred.get(x, 0))) for x in range(10)) < 1e-9
# digital roots of the digit sum
S43, SS = [digit_sum(R43[k]) for k in range(101)], [digit_sum(RSEED[k]) for k in range(101)]
assert "".join(str(dr(s)) for s in S43[:36]) == "784928151922427925" * 2
assert [k for k in range(40) if dr(S43[k]) == 9] == [3, 9, 15, 21, 27, 33, 39]
assert "".join(str(dr(s)) for s in SS[:18]) == "254188499562474774" and all(dr(SS[k]) == dr(SS[k + 54]) for k in range(47))
assert [k for k in range(30) if dr(SS[k]) == 9] == [7, 8, 26, 28] and not any(all(dr(SS[k]) == dr(SS[k + p]) for k in range(46)) for p in range(1, 54))
assert not any(all(dr(S43[k]) == dr(S43[k + p]) for k in range(80)) for p in range(1, 18))
# the variant, not in the paste
V43, VSEED = counts_by_step("43", 200, mod10), counts_by_step(SEED, 200, mod10)      # slower convergence: k = 200
want = [Fraction(2, 36), Fraction(5, 36), Fraction(5, 72), Fraction(5, 36), Fraction(5, 72), Fraction(4, 36), Fraction(5, 72), Fraction(5, 36), Fraction(5, 72), Fraction(5, 36)]
assert sum(want) == 1
for R in (V43, VSEED):
    assert max(abs(R[200].get(x, 0) / total(R[200]) - float(want[x])) for x in range(10)) < 1e-8

if __name__ == "__main__":
    print("seed digit sum is 191 (not 193); |a-b| rule: zeros 1/3 and sum ratio 2 are universal, nonzero digits follow gcds;")
    print("43: #4=1, #3=floor(k/2)+1, #2=floor(k^2/4); dr(S_k) period 18 for 43, 54 for the seed")
