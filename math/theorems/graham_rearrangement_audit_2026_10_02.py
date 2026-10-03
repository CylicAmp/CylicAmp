# CLASS: AUDIT
"""
Audit of a supplied summary (2026-10-02) of arXiv:2409.07403,
B. Bedert and N. Kravitz, "Graham's rearrangement conjecture beyond the
rectification barrier" (v1 11 Sep 2024, v2 7 Jan 2025).  Checked against the
paper's text (v2), not the abstract alone.

Conjecture (Graham 1971; Erdos-Graham 1980): every A in F_p \\ {0} has an
ordering whose partial sums a_1, a_1+a_2, ..., a_1+...+a_k are all distinct
("valid").  s_0 = 0 is not one of the sums compared.

CORRECT IN THE SUMMARY
 - The conjecture, the authors' bound and the previous bound: Theorem 1.2
   proves it for |A| <= e^{c (log p)^{1/4}}, any c > 0, p large; the previous
   bound was log p / log log p.
 - Dissociated: all 2^|S| subset sums distinct.  The paper defines it by
   eps in {-1,0,1}^r, eps != 0 => sum != 0, and states the equivalence
   (asserted below).

INCORRECT OR NOT IN THE PAPER
 1. Where the old bound came from.  The summary: "algebraic methods,
    polynomial method variants, or basic additive energy".  The paper:
    Kravitz [8] used "a simple RECTIFICATION argument" (dilate A into
    (-p/|A|, p/|A|) so sums do not wrap, then order positives before negatives
    in Z); W. Sawin had a comparable bound in a 2015 MathOverflow post.  That
    is the "rectification barrier" in the title.
 2. "Trivial for |A| <= c log log p".  Not in the paper.  Before 2024 the
    published record was |A| <= 12 (a constant).
 3. The mechanism.  The summary describes a dichotomy in which A without
    large dissociated sets is forced by Freiman / Chang-type inverse theorems
    into a generalized arithmetic progression.  The paper does not do that.
    Theorem 3.4 PARTITIONS A = D_1 u ... u D_s u E: each D_j dissociated of
    size ~ R, and a residual E that, after one dilation, lies in a short
    interval around 0 (rectifiable).  The ordering is: positive part of E,
    then the dissociated sets, then the negative part of E.  The dissociated
    sets are ordered RANDOMLY: a random order of a dissociated set of size R
    has its first-k sum spread over C(R,k) values, so hitting a forbidden
    value is unlikely.  The text cites Bourgain for the decomposition; there
    is no Bohr set, Fourier analysis, additive energy, Ruzsa distance or
    Nullstellensatz in it (word counts: 0 each); "Freiman" appears only as
    "Freiman-isomorphic" and in a reference title.
 4. "Sub-exponential in log p".  The paper's own word is quasi-polynomial:
    e^{c (log p)^{1/4}} exceeds every power of log p and is below every power
    of p.  A naive random version already reaches (log p)^{3/2}.
 5. Lean 4 requirements.  Since the proof uses rectification, dissociated
    sets and elementary probability, the listed prerequisites (Bohr sets,
    Ruzsa distance, Freiman's theorem, Fourier-analytic machinery) are not
    what a formalization of THIS proof needs.

COMPUTED BELOW
 A. The conjecture holds for every A in F_p \\ {0}, all primes p <= 13
    (exhaustive; every subset, 4095 at p = 13; p = 17 by this plain
    depth-first search takes minutes, so it is left out).
 B. The integer step of rectification: every A in Z \\ {0} drawn from
    [-7, 7], |A| <= 6, has a TWO-SIDED valid ordering with all positives
    first (no proper nonempty interval sums to 0).
 C. The dissociated-set equivalence, exhaustively in F_p, p <= 13.

FALSIFICATION: any assertion failing.
"""
from itertools import combinations, permutations, product

from sympy import primerange


def has_valid(A, p):
    A = list(A); k = len(A)
    used = [False] * k

    def dfs(s, seen, depth):
        if depth == k:
            return True
        for i in range(k):
            if not used[i]:
                t = (s + A[i]) % p
                if t not in seen:
                    used[i] = True; seen.add(t)
                    if dfs(t, seen, depth + 1):
                        return True
                    used[i] = False; seen.discard(t)
        return False
    return dfs(0, set(), 0)


counts = {}
for p in primerange(2, 14):                                                   # A
    nz = range(1, p)
    n = 0
    for k in range(1, p):
        for A in combinations(nz, k):
            assert has_valid(A, p), (p, A)
            n += 1
    counts[p] = n
assert counts[13] == 2 ** 12 - 1


def two_sided(seq):
    t = len(seq)
    for i in range(t):
        s = 0
        for j in range(i, t):
            s += seq[j]
            if s == 0 and (i, j) != (0, t - 1):
                return False
    return True


pool = [x for x in range(-7, 8) if x]
nB = 0
for k in range(1, 7):                                                         # B
    for A in combinations(pool, k):
        P = [a for a in A if a > 0]; N = [a for a in A if a < 0]
        assert any(two_sided(list(x) + list(y)) for x in permutations(P) for y in permutations(N)), A
        nB += 1


def dissoc_pm(S, p):
    return all(sum(e * s for e, s in zip(E, S)) % p for E in product((-1, 0, 1), repeat=len(S)) if any(E))


def dissoc_01(S, p):
    sums = [sum(e * s for e, s in zip(E, S)) % p for E in product((0, 1), repeat=len(S))]
    return len(set(sums)) == len(sums)


for p in primerange(3, 14):                                                   # C
    for k in range(1, 5):
        for S in combinations(range(1, p), k):
            assert dissoc_pm(S, p) == dissoc_01(S, p)

if __name__ == "__main__":
    print("Graham rearrangement audit: all subsets valid for p <= 13", counts,
          "| two-sided integer check on", nB, "sets | dissociated equivalence ok")
