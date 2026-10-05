# CLASS: AUDIT
"""
Thread 2 (Collatz trajectories on twin centres) -- reproduced 2026-10-05.
audit_leibniz_row37.py left Thread 2 unreproduced; the owner's ledger
(owner_words_2026-09-06_to_2026-10-03.txt, 2026-09-28) states it as:
  "Formalized under S(n) and c_odd; 27.2 sample-dependent; v_3 = 3 elongation
   refuted; 3077 identified as global trunk without twin enrichment."
Source runs: same file, 2026-09-26 21:02 (centres 108, 432, 462, 570, 660).

REPRODUCED (twin centre c: c-1 and c+1 both prime):
  1. 108, 432, 462, 570, 660 are twin centres and the largest ODD value on each
     Syracuse orbit is 3077 = 17 x 181. 3077 lies on the trajectory of 27, so
     every start that reaches 27 passes it.
  2. "Global trunk without twin enrichment": below 200,000, 37.98% of the 2159
     twin centres pass 3077 against 39.11% of all multiples of 6 -- no excess.
  3. "v_3 = 3 elongation refuted": twin centres with 3^3 || c average 110.1
     steps (160 of them); multiples of 6 with 3^3 || c average 109.3 -- no
     elongation beyond the baseline.
  4. "27.2 sample-dependent": the mean number of odd steps over twin centres
     moves with the range -- 13.9 (c < 1000), 24.1 (< 10^4), 32.1 (< 10^5),
     34.8 (< 2x10^5) -- so any single value such as 27.2 belongs to its sample.
     S(n) and c_odd are not defined anywhere in the corpus; the check uses the
     plain step count and odd-step count.
CORRECTION to the 2026-09-26 source text: it lists the full Collatz run of 108
  as "Length: 51, Max: 1780, 3077 in sequence: False". Wrong: 108 -> 54 -> 27
  -> ... takes 113 steps, peaks at 9232 and passes 3077 (the odd-only Syracuse
  listing in the same block is right).
STATUS: Thread 2 VERIFIED (2026-10-05), with the correction above.

FALSIFICATION: any assertion below failing.
"""
import statistics as st
from sympy import isprime

def coll(n):
    t = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        t.append(n)
    return t

def v3(n):
    k = 0
    while n % 3 == 0:
        n //= 3
        k += 1
    return k

c108 = coll(108)
assert len(c108) - 1 == 113 and max(c108) == 9232 and 3077 in c108 and 27 in c108
assert 3077 == 17 * 181 and 3077 in coll(27)
for c in (108, 432, 462, 570, 660):
    assert isprime(c - 1) and isprime(c + 1)
    assert max(x for x in coll(c) if x % 2) == 3077

N = 200000
TC = [c for c in range(6, N, 6) if isprime(c - 1) and isprime(c + 1)]
M6 = list(range(6, N, 6))
T = {c: coll(c) for c in M6}
assert len(TC) == 2159
via_t = sum(3077 in set(T[c]) for c in TC) / len(TC)
via_m = sum(3077 in set(T[c]) for c in M6) / len(M6)
assert round(via_t, 4) == 0.3798 and round(via_m, 4) == 0.3911
a = [len(T[c]) - 1 for c in TC if v3(c) == 3]
b = [len(T[c]) - 1 for c in M6 if v3(c) == 3]
assert len(a) == 160 and round(st.mean(a), 1) == 110.1 and round(st.mean(b), 1) == 109.3
odd = lambda c: sum(1 for x in T[c][:-1] if x % 2)
means = [round(st.mean(odd(c) for c in TC if c < hi), 1) for hi in (1000, 10000, 100000, 200000)]
assert means == [13.9, 24.1, 32.1, 34.8]

if __name__ == "__main__":
    print("Thread 2 reproduced; all assertions pass")
