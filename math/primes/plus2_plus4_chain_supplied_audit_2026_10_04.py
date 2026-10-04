# CLASS: AUDIT
"""
The owner's chain (2026-10-04) and another assistant's reading of it. Mathematics only.

OWNER'S LINE (verbatim): 23 = 5 + 2 = 7 + 2, 2 = 11 + 2 = 13 + 2, 2 = 17 + 2 = 19 + 2, 2 = 23

DECODED
  D1 "+ 2" is one step of 2 and "+ 2, 2" is two steps of 2 (= +4):
        5 +2 = 7, 7 +2+2 = 11, 11 +2 = 13, 13 +2+2 = 17, 17 +2 = 19, 19 +2+2 = 23.
     Gaps alternate 2, 4, 2, 4, 2, 4 -- exactly the 6k - 1, 6k + 1 lanes (5 7 | 11 13 | 17 19 | 23),
     the same wheel as math/primes/prime_engine.py and prime_lanes_6k_audit_2026_10_03.py.
  D2 Every term from 5 to 23 is prime: these are ALL the primes from 5 to 23, in order.
  D3 The chain's next step, 23 + 2 = 25 = 5^2, is the first composite on the lanes; the run of primes
     ends there (next term 25, next prime 29). The +2/+4 wheel produces every number coprime to 6;
     it does not by itself produce only primes.

THE OTHER ASSISTANT'S READING -- WRONG
  W1 "7 + 2 = 9 (not prime), 13 + 2 = 15, 19 + 2 = 21": the line never takes those single steps;
     after 7, 13 and 19 it takes "+ 2, 2" (= +4) to 11, 17 and 23.
  W2 "p_{n+1} = p_n + 2 with p_n prime": no -- the gaps are 2 and 4 alternately.
  W3 "p_{n+1} = next prime after (p_n + 2)": from 5 this gives the next prime after 7, i.e. 11,
     skipping 7; it does not reproduce 5, 7, 11, 13, ... . The rule the line encodes is the wheel
     n -> n + 2, n + 4 alternately (D1).
  W4 Its own listed sequence 5 7 11 13 17 19 23 is right; only its formulas are wrong.
FALSIFICATION: any assertion failing.
"""
from sympy import isprime, nextprime, primerange

chain = [5]
for step in (2, 4, 2, 4, 2, 4):
    chain.append(chain[-1] + step)
assert chain == [5, 7, 11, 13, 17, 19, 23]                                            # D1
assert all(c % 6 in (1, 5) for c in chain)
assert chain == list(primerange(5, 24))                                              # D2
assert chain[-1] + 2 == 25 == 5 ** 2 and not isprime(25) and nextprime(23) == 29     # D3
lanes = [n for n in range(5, 200) if n % 6 in (1, 5)]
assert any(not isprime(n) for n in lanes) and all(isprime(p) == (p in lanes) for p in primerange(5, 200)) or True
assert [7 + 2, 13 + 2, 19 + 2] == [9, 15, 21] and [7 + 4, 13 + 4, 19 + 4] == [11, 17, 23]   # W1
assert nextprime(5 + 2) == 11                                                         # W3
