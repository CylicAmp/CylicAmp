# CLASS: AUDIT
"""
Audit of the pasted "sharpened theorem" for the neighbor-difference transformation (owner_work #310, 2026-10-17).
Continues math/theorems/neighbor_difference_43_vs_seed45_2026_10_17.py. The paste is another tool's text, relayed
by the owner with no words of their own; it is checked, not attributed to the owner.

THE RULE: the paste states it -- T(a_1..a_L) = (a_1, |a_1-a_2|, a_2, ..., |a_(L-1)-a_L|, a_L). This is the |a - b| rule
used in the 43 comparison, so that open question is answered by the paste.

FAULTS FIRST (formulas lost in the paste are not guessed)
  F1  "S_(n+1) = 2 S_n + sum |a_i - a_(i+1)|" is wrong. The new sequence holds each old digit once plus the inserted
      differences, so  S_(n+1) = S_n + D_n  with D_n = sum of |a_i - a_(i+1)|. Check: 43 -> 413: 7 + 1 = 8, not 15.
      The paste's sentence "this explains why the sum approaches doubling when the average adjacent difference becomes small"
      does not follow: S_(n+1)/S_n = 1 + D_n/S_n tends to 2 exactly when D_n/S_n tends to 1.
  F2  The 1212121 closed forms are wrong. Their counts do not add up to their own length: 0s + 1s + 2s = 9 x 2^(n-2) + 1 but
      L = 12 x 2^(n-2) + 1. True forms (seed at n = 0, valid for every n >= 0):
        L_n = 6 x 2^n + 1,  N_2 = 3,  N_1 = 2^(n+2) + 2 (n mod 2),  N_0 = 2^(n+1) - 2 - 2 (n mod 2),
        S_n = 2^(n+2) + 6 + 2 (n mod 2).
      Proved for all n by a linear-recurrence argument (below), not only measured.
  F3  The pasted S_48 = 3 x 2^48 + 4 = 844,424,930,131,972 is wrong: the true value is S_48 = 2^50 + 6 = 1,125,899,906,842,630
      (seed at n = 0). Counting the seed as step 1, "step 48" is n = 47: S_47 = 2^49 + 8 = 562,949,953,421,320. Neither is the pasted number.
  F4  The numbering is inconsistent: the text puts the seed at n = 0, but L_n = 6 x 2^(n-1) + 1 and the 123 table both
      put the seed at step 1.

HOLDS
  length L_(n+1) = 2 L_n - 1; the bounded alphabet; the 123-ten-times table (all 8 rows, with Step = n + 1);
  N_3 = 10 for every n (the 3s are never created or lost) -- PROVED: only pair types (0,1) (1,0) (1,1) (1,2) (1,3) (2,1) (2,3)
  (3,1) (3,2) ever occur, none has difference 3; likewise N_2 = 3 for 1212121 (pair types (0,1) (1,0) (1,1) (1,2) (2,1)).
  The pair-count matrix claim is right.

PROOF TOOL (for the closed forms): with P possible pair types the pair counts v_n obey v_(n+1) = M v_n, so by Cayley-Hamilton every
  digit count N_x(n) = (linear in v_n) + (a constant: the first digit never changes) satisfies a linear recurrence of order P + 1.
  A closed form built from 2^n, 1, (-1)^n and polynomials satisfies one of order r. Their difference satisfies one of order
  P + 1 + r, so agreement on that many consecutive n gives agreement for all n. This also turns the closed forms for the 43
  sequence (previous file: #3 = floor(k/2) + 1, #2 = floor(k^2/4), ...), checked there for k <= 100, into proved identities.

NOT PROVED: the gcd law for the limiting frequencies (previous file), measured exactly for all digit pairs and random seeds.
  What it predicts for "which seeds keep a positive share of digits other than 0 and 1": exactly the seeds with a neighbouring
  pair of gcd >= 2 (a pair (a, 0) with a >= 2 counts, gcd(a, 0) = a). 123 ten times has none, so its limit is 0: 1/3, 1: 2/3.

FALSIFICATION: any assertion failing.
"""
from collections import Counter
from fractions import Fraction
from math import comb, gcd

DIGITS = lambda s: [int(c) for c in s]


def absd(a, b):
    return abs(a - b)


def write_out(s, k):
    d = DIGITS(s)
    for _ in range(k):
        out = [d[0]]
        for a, b in zip(d, d[1:]):
            out += [absd(a, b), b]
        d = out
    return d


def counts_by_step(s, K):
    P, C = Counter(zip(DIGITS(s), DIGITS(s)[1:])), Counter(DIGITS(s))
    out = [dict(C)]
    for _ in range(K):
        P2, C2 = Counter(), Counter(C)
        for (a, b), n in P.items():
            d = absd(a, b)
            P2[(a, d)] += n
            P2[(d, b)] += n
            C2[d] += n
        P, C = P2, C2
        out.append(dict(C))
    return out


def pair_types(s):
    types = set(zip(DIGITS(s), DIGITS(s)[1:]))
    todo = list(types)
    while todo:
        a, b = todo.pop()
        d = absd(a, b)
        for t in ((a, d), (d, b)):
            if t not in types:
                types.add(t)
                todo.append(t)
    return types


total = lambda c: sum(c.values())
dsum = lambda c: sum(x * n for x, n in c.items())
SEED_123, SEED_12 = "123" * 10, "1212121"

# F1: S_(n+1) = S_n + D_n, not 2 S_n + D_n
d = DIGITS("43")
for n in range(6):
    D = sum(absd(a, b) for a, b in zip(d, d[1:]))
    nxt = write_out("".join(map(str, d)), 1)
    assert sum(nxt) == sum(d) + D and sum(nxt) != 2 * sum(d) + D
    d = nxt
assert sum(write_out("43", 1)) == 8 and 2 * 7 + 1 == 15
# the length and the alphabet
for s in ("43", SEED_12, SEED_123):
    for k in range(8):
        w = write_out(s, k)
        assert len(w) == 2 ** k * (len(s) - 1) + 1 and max(w) <= max(DIGITS(s))
# F2/F3/F4: 1212121 true closed forms (seed at n = 0)
R12 = counts_by_step(SEED_12, 200)
for n in range(201):
    c, m = R12[n], n % 2
    assert total(c) == 6 * 2 ** n + 1 and c.get(2, 0) == 3 and set(c) <= {0, 1, 2}
    assert c.get(1, 0) == 2 ** (n + 2) + 2 * m and c.get(0, 0) == 2 ** (n + 1) - 2 - 2 * m and dsum(c) == 2 ** (n + 2) + 6 + 2 * m
assert dsum(R12[48]) == 2 ** 50 + 6 == 1125899906842630 and dsum(R12[47]) == 2 ** 49 + 8 == 562949953421320
assert 3 * 2 ** 48 + 4 == 844424930131972 not in (dsum(R12[48]), dsum(R12[47]))
for n in range(2, 8):                                    # the pasted forms contradict themselves
    pasted = (3 * 2 ** (n - 2) - 3) + (3 * 2 ** (n - 1) + 1) + 3
    assert pasted == 9 * 2 ** (n - 2) + 1 != 6 * 2 ** (n - 1) + 1 and total(R12[n - 1]) == 6 * 2 ** (n - 1) + 1
# proof by recurrence order: window of agreement must be at least P + 1 + r terms
P12 = len(pair_types(SEED_12))
assert P12 == 5 and pair_types(SEED_12) == {(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)}
assert all(absd(a, b) != 2 for a, b in pair_types(SEED_12))            # N_2 constant for all n (proof)
assert P12 + 1 + 3 <= 201                                              # recurrence order 9 <= 201 agreeing terms: proved for all n
# the 123 table (Step = n + 1) and N_3 = 10 for ever
R123 = counts_by_step(SEED_123, 12)
PASTED = {1: (30, 60, 0, 10, 10, 10), 2: (59, 98, 0, 30, 19, 10), 3: (117, 156, 10, 68, 29, 10), 4: (233, 252, 39, 146, 38, 10),
          5: (465, 426, 107, 300, 48, 10), 6: (929, 754, 252, 610, 57, 10), 7: (1857, 1392, 552, 1228, 67, 10), 8: (3713, 2648, 1161, 2466, 76, 10)}
for step, row in PASTED.items():
    c = R123[step - 1]
    assert (total(c), dsum(c), c.get(0, 0), c.get(1, 0), c.get(2, 0), c.get(3, 0)) == row
T123 = pair_types(SEED_123)
assert T123 == {(0, 1), (1, 0), (1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)} and all(absd(a, b) != 3 for a, b in T123)
R123L = counts_by_step(SEED_123, 100)
assert all(R123L[n].get(3, 0) == 10 for n in range(101))
# the 43 closed forms: P = reachable pair types, order P + 1 + 5, window 101 terms: proved for all k
P43 = len(pair_types("43"))
assert P43 + 1 + 5 <= 101
R43 = counts_by_step("43", 100)
for k in range(101):
    c = R43[k]
    z = (2 ** k + 1 - comb(k, 2) - k % 2 - k * k // 4 - k // 2 - 2) // 3
    assert c.get(4, 0) == 1 and c.get(3, 0) == k // 2 + 1 and c.get(2, 0) == k * k // 4 and c.get(0, 0) == z
    assert c.get(1, 0) == 2 * z + comb(k, 2) + k % 2
# the gcd law's prediction for 123 ten times
n_pairs = len(SEED_123) - 1
assert all(gcd(a, b) == 1 for a, b in zip(DIGITS(SEED_123), DIGITS(SEED_123)[1:])) and n_pairs == 29
assert abs(R123L[100][0] / total(R123L[100]) - 1 / 3) < 1e-9 and abs(R123L[100][1] / total(R123L[100]) - 2 / 3) < 1e-9

if __name__ == "__main__":
    print("pasted theorem audited: S recurrence is S_n + D_n; 1212121 true forms L = 6*2^n+1, S = 2^(n+2) + 6 + 2(n mod 2), proved;")
    print("N_3 = 10 for 123x10 proved; the 43 closed forms are now proved; the pasted 1212121 forms and S_48 are wrong")
