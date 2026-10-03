# CLASS: AUDIT
"""
Audit of supplied "Thread 5: Leibniz triangle row 37" (2026-09-28). No prior Leibniz
file in the corpus.

Row n = 36 of the Leibniz harmonic triangle has denominators D(36,k) = 37 * C(36,k),
k = 0..36 (37 entries).

VERIFIED
  * Centre: 37 * C(36,18) = 335,780,006,100 = 2^2 * 3 * 5^2 * 7 * 11 * 19 * 23 * 29
    * 31 * 37. Kummer carry counts for 18 + 18: base 2: 2, base 3: 1, base 5: 2,
    base 7: 1, base 11: 1, base 13: 0, base 17: 0; primes 19..31 once each.
  * 37 = 1 (mod 9), so dr(37 X) = dr(X) for every X: FORCED.
  * v_3(C(36,18)) = 1 forces dr = 3 or 6; it is 6, and k = 18 is the ONLY dr-6
    entry.
  * Row spectrum: dr 9 x 28; dr 3 x 4 (k = 3, 6, 30, 33); dr 6 x 1 (k = 18);
    dr 1 x 2 (k = 0, 36); dr 4 x 2 (k = 9, 27). No 2, 5, 7, 8.
  * Mechanism: 36 = 1100_3; v_3(C(36,k)) = (S_3(k) + S_3(36-k) - S_3(36))/2 is the
    base-3 carry count (Kummer). v_3 >= 2 gives dr 9; v_3 = 1 at k in
    {3,6,18,30,33}; v_3 = 0 at k in {0,9,27,36}.
CORRECTED
  * The stated reason "18 < 2p implies no carry" for p = 13, 17 is wrong: p = 11
    also has 18 < 22 yet carries (v_11 = 1). The correct test for m + m in base p
    with m < p^2 is the low digit: a carry iff 2 (m mod p) >= p. 18 mod 13 = 5,
    18 mod 17 = 1: no carry; 18 mod 11 = 7: carry.
RECONCILIATION NOTES (supplied "all five threads closed")
  * Thread 1 is out of date: the family search is COMPLETE at m <= 1e22 (587
    members; T245) -- not "conditionally verified at 1e16".
  * Thread 3: the +-2 (mod 9) clustering is not a sample-selection artifact. It is
    inherited from the candidate construction q = sigma_2(m)/m - m, derived exactly
    in T245 (q = eps * tau(u)/3^b * prod C - m mod 9; 71% of candidates at 1e12).
  * Thread 4 checks: 11 * 26 = 286 = 27 (mod 37); 11 in -mu_3, 26 in mu_3, product
    in -mu_3. Syracuse 37 -> 7 -> 11 (3*37+1 = 112 = 16*7; 3*7+1 = 22 = 2*11).
  * Thread 2 (Collatz on twin centres) is not reproduced here.

CROSS-THREAD STATUS (certification rule adopted 2026-09-28: a thread is VERIFIED
only when its result reproduces from the stated domain and generation rules and
every inference used for exhaustiveness is independently checked):
  Thread 5  VERIFIED (this file).
  Thread 4  VERIFIED (assertions above).
  Thread 3  VERIFIED, re-run 2026-09-28 from the committed tool
            tools/divisor_square_family_candidates.py 1e12 (clean state):
            552 candidates (m | sigma_2(m), ratio > 3/2, q > m/2, gcd(q,6) = 1),
            394 = 71.4% with q = +-2 (mod 9), 26 with q prime. The concentration
            precedes prime filtering; mechanism derived and checked 552/552 in T245
            (q = eps * tau(u)/3^b * prod C - m mod 9).
            SCOPE: a property of this generator at 1e12, not a universal theorem;
            T245 shows the share varies with v3(m) (e.g. 95% at v3 = 3 but 31% at
            v3 = 4, both at 1e14).
  Thread 1  VERIFIED TO m <= 1e22 (587 members; completed 2026-09-28). Artifacts:
            T245 ("COMPLETE AT m <= 1e22"), t245_family_members_1e22.txt (all 587
            re-verified), t245_supply_cycles_1e22.json (106 cycles, 122 seeds),
            tools/rust_family (validated by identical node counts vs Python at
            1e12..1e18). Exhaustiveness rests on the read-off + supply-cycle
            argument written out in T245. Four members at 1e22 contain supply
            cycles (4817^2 and 8101^2 two-cycle junctions) and are found only by
            the seeded runs.
  Thread 2  UNVERIFIED here.
"""
from math import comb
from collections import Counter
from sympy import factorint


import sys as _sys, pathlib as _pl
_sys.path.append(str(next(p for p in _pl.Path(__file__).resolve().parents if (p / "functions.py").exists())))
from functions import dr9_signed as dr


def v3(n):
    c = 0
    while n % 3 == 0:
        n //= 3
        c += 1
    return c


def carries(a, b, p):
    c = n = 0
    while a or b or c:
        t = a % p + b % p + c
        c = 1 if t >= p else 0
        n += c
        a //= p
        b //= p
    return n


def s3(n):
    s = 0
    while n:
        s += n % 3
        n //= 3
    return s


N = 37 * comb(36, 18)
assert N == 335780006100
assert factorint(N) == {2: 2, 3: 1, 5: 2, 7: 1, 11: 1, 19: 1, 23: 1, 29: 1, 31: 1, 37: 1}
assert {p: carries(18, 18, p) for p in (2, 3, 5, 7, 11, 13, 17)} == {2: 2, 3: 1, 5: 2, 7: 1, 11: 1, 13: 0, 17: 0}
assert {p: 2 * (18 % p) >= p for p in (11, 13, 17)} == {11: True, 13: False, 17: False}
row = {k: dr(37 * comb(36, k)) for k in range(37)}
assert Counter(row.values()) == Counter({9: 28, 3: 4, 6: 1, 1: 2, 4: 2})
assert [k for k, v in row.items() if v == 6] == [18]
assert [k for k, v in row.items() if v == 3] == [3, 6, 30, 33]
assert [k for k, v in row.items() if v == 1] == [0, 36] and [k for k, v in row.items() if v == 4] == [9, 27]
assert all(v3(comb(36, k)) == (s3(k) + s3(36 - k) - s3(36)) // 2 for k in range(37))
assert all((v3(comb(36, k)) >= 2) == (row[k] == 9) for k in range(37))
assert 11 * 26 % 37 == 27 and (3 * 37 + 1) == 16 * 7 and 3 * 7 + 1 == 2 * 11

if __name__ == "__main__":
    print("Leibniz row 37: centre", N, "dr", dr(N), "; spectrum", dict(Counter(row.values())))
