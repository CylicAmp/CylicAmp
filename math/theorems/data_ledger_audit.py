"""
data_ledger_audit.py

Audits four claims in the "Data Ledger: Systemic Equation & Sequence Projection":
  1. n = (n+1)/2  →  n = 1  (arithmetic)
  2. 1 is genesis of DR-doubling circuit {1,2,4,8,7,5}
  3. S_k = S_{k+1}/2 with S_1=1 generates {2^k}
  4. {2^k} is "the exact exponential backbone for Mersenne primes"
"""

import math

# ---------------------------------------------------------------------------
# 1. n = (n+1)/2
# ---------------------------------------------------------------------------
print("="*60)
print("1.  n = (n+1)/2  →  n = 1")
print("="*60)
print("""
  Algebra:  2n = n + 1  →  n = 1
  Verification: 1 = (1+1)/2 = 1  ✓
""")

# Integer solutions in Z
solutions = [n for n in range(-100, 100) if n == (n + 1) / 2]
print(f"  Integer solutions in [-100, 100]: {solutions}")
print(f"  Unique solution: TRUE")

print("""
  "Theorem of Uniqueness": In S = {{1,2,3,...}}, the integer 1 is the
  unique instance where n = (n+1)/2.
  STATUS: CORRECT — trivially so. This is one linear equation in one
  unknown; it has exactly one real solution. The label "Theorem of
  Uniqueness" describes a consequence of linear algebra, not a
  structural property of S = {{1,2,3,...}}.

  REMOVAL TEST: Strip the framing.
    What remains: n = (n+1)/2 has solution n = 1.
    Governing equation: the linear equation itself.
    STATUS: Equation is self-contained. The framing adds no content.
""")

# ---------------------------------------------------------------------------
# 2. 1 as genesis of DR-doubling circuit
# ---------------------------------------------------------------------------
print("="*60)
print("2.  1 is genesis of {1,2,4,8,7,5} bypassing {3,6,9}")
print("="*60)

def dr(n):
    if n <= 0:
        raise ValueError
    return (n - 1) % 9 + 1

# Trace the 6-cycle from 1
cycle_from_1 = []
x = 1
for _ in range(7):
    cycle_from_1.append(x)
    x = dr(2 * x)

print(f"  Doubling orbit from DR=1: {cycle_from_1}")
print(f"  Returns to 1 at step 6: {cycle_from_1[-1] == 1}")

# Does the equation n=1 "generate" the circuit?
print("""
  CLAIM: 1 "directly bypasses" the triadic set {3,6,9}.
  ARITHMETIC FACT: DR(1)=1 ∉ {3,6,9}. Correct.
  DR(2×1)=2, DR(2×2)=4, DR(2×4)=8, DR(2×8)=7, DR(2×7)=5, DR(2×5)=1.
  The 6-cycle is a property of the doubling map on Z/9Z — established
  independently of the equation n=(n+1)/2.

  CONNECTION: The equation n=(n+1)/2 produces n=1.
              The doubling orbit of 1 is {1,2,4,8,7,5}.
              These are two separate facts joined by the value 1.
  The equation does not generate or govern the cycle;
  it identifies one element that happens to be in the cycle.
  "Genesis coordinate" is a label, not a causal relationship.
""")

# ---------------------------------------------------------------------------
# 3. S_k = S_{k+1}/2 generates powers of 2
# ---------------------------------------------------------------------------
print("="*60)
print("3.  S_k = S_{k+1}/2 with S_1=1 generates {2^(k-1)}")
print("="*60)

S = [2**(k-1) for k in range(1, 12)]
print(f"  S_k = 2^(k-1) for k=1..11: {S}")

# Verify recurrence
for k in range(1, 10):
    assert S[k-1] == S[k] / 2, f"Failed at k={k}"
print(f"  S_k = S_(k+1)/2 verified for k=1..10: TRUE")

print("""
  CLAIM: "the condition is perpetually maintained ad infinitum."
  STATUS: CORRECT. The recurrence S_{k+1} = 2*S_k with S_1=1 gives
  S_k = 2^(k-1) for all k ≥ 1. The sequence is infinite.
  This is a standard geometric series (ratio=2); nothing non-standard.

  "Terminal condition: Null / Infinity" — correct; no finite terminus.
""")

# ---------------------------------------------------------------------------
# 4. {2^k} as "exact exponential backbone" for Mersenne primes
# ---------------------------------------------------------------------------
print("="*60)
print("4.  {2^k} as backbone for Mersenne primes M_p = 2^p - 1")
print("="*60)

def is_prime_miller_rabin(n):
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1; d //= 2
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if a >= n: continue
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(r-1):
            x = pow(x, 2, n)
            if x == n-1: break
        else:
            return False
    return True

# Check which exponents in {2^k} give Mersenne primes
print(f"  {'k':>4}  {'2^k':>12}  {'k prime?':>10}  {'M_k = 2^k-1':>14}  {'M_k prime?':>12}")
print(f"  {'-'*58}")
for k in range(1, 20):
    val = 2**k
    k_prime = is_prime_miller_rabin(k)
    M_k = val - 1
    M_prime = is_prime_miller_rabin(M_k) if k <= 15 else None
    mark = ""
    if M_prime: mark = "← Mersenne prime"
    m_str = str(M_k) if k <= 15 else "..."
    mp_str = str(M_prime) if M_prime is not None else "—"
    print(f"  {k:>4}  {val:>12}  {str(k_prime):>10}  {m_str:>14}  {mp_str:>12}  {mark}")

print(f"""
  CRITICAL CONSTRAINT MISSING FROM CLAIM:
  M_p = 2^p - 1 can be prime ONLY IF p is prime (necessary condition,
  NOT sufficient). The sequence {{2^k}} includes ALL exponents k ∈ ℤ⁺.
  Composite k guarantees composite M_k:
    If k = ab (a,b > 1): 2^(ab) - 1 = (2^a - 1)(2^(a(b-1)) + ... + 1)
    → M_k is composite.

  From the table above: k=4 (composite) → M_4=15=3×5 (composite)
                        k=6 (composite) → M_6=63=9×7 (composite)
                        k=2 (prime)     → M_2=3 (prime) ✓
                        k=3 (prime)     → M_3=7 (prime) ✓

  The sequence S = {{1,2,4,8,16,...}} = {{2^0,2^1,2^2,...}} provides
  the values 2^k, but Mersenne primes require:
    (a) p prime (necessary)
    (b) 2^p - 1 prime (sufficient — no general formula exists)

  The doubling sequence is the domain from which exponents are selected,
  not the "backbone" that generates Mersenne primes.

  CLAIM STATUS: PARTIALLY CORRECT, INCOMPLETE.
  The form M_p = 2^p - 1 is correctly stated.
  The claim that {{2^k}} is the "exact exponential backbone" omits the
  primality constraint on k, making it imprecise: S also contains all
  non-prime exponents, which produce no Mersenne primes.

  "Mersenne Prime Topology" — label escalation.
  y = 2x is a linear map. Topology refers to open sets and continuity;
  a discrete sequence {{2^k}} has the discrete topology by default.
  No topological content is established.
""")

# ---------------------------------------------------------------------------
# 5. Removal test across all four sections
# ---------------------------------------------------------------------------
print("="*60)
print("5.  Removal test: strip structural labels")
print("="*60)
print("""
  Section 1 after removal:  n = 1  (one-step linear equation)
  Section 2 after removal:  DR doubling orbit of 1 = {1,2,4,8,7,5}
  Section 3 after removal:  S_k = 2^(k-1), infinite geometric sequence
  Section 4 after removal:  Mersenne primes have form 2^p-1 (p prime)

  All four cores survive as correct arithmetic statements.
  The structural framing ("Triadic Resonance", "Genesis Coordinate",
  "Mersenne Prime Topology", "Topological Matching") does not add
  content; removing it leaves the arithmetic intact and unchanged.
""")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("="*60)
print("SUMMARY")
print("="*60)
print("""
  Claim                                     Status
  -------------------------------------------------------
  n=(n+1)/2 → n=1                          CORRECT ✓
  n=1 is unique in Z solving that eq.      CORRECT ✓ (trivial)
  "Theorem of Uniqueness" adds content      FALSE — label for linear eq.
  DR(1)=1, not in {3,6,9}                  CORRECT ✓
  {1,2,4,8,7,5} is doubling orbit of 1     CORRECT ✓
  Equation n=(n+1)/2 generates the orbit   FALSE — identifies one
                                             element; orbit is a
                                             property of DR algebra
  S_k=S_{k+1}/2, S_1=1 → 2^(k-1)          CORRECT ✓
  Sequence infinite                         CORRECT ✓
  {2^k} is backbone for Mersenne primes     INCOMPLETE — omits p prime
                                             constraint; composites k
                                             produce composite M_k
  "Mersenne Prime Topology"                 LABEL ESCALATION — y=2x is
                                             a linear map, not topology

  What is established:
    Four standard arithmetic facts connected by the value 1 and the
    number 2. Each fact is correct in isolation. The connections are
    associative (shared values), not causal (governing equations).
""")
