"""
infinity_proof_roadmap.py

Maps the set-theoretic landscape for proving |T| = ℵ₀ (TPC).

T = { (p, p+2) : p and p+2 both prime }

Evaluates four approaches:
  1. Euclid contradiction (construct new pair from known list)
  2. Injection f: N → T (equivalent to TPC, not simpler)
  3. Furstenberg topology (does not port to twin primes directly)
  4. Contradiction via DR structure (most tractable; precise gap identified)

Key finding:
  Set theory provides the LANGUAGE (infinite set, injection, partition).
  The proof requires NUMBER-THEORETIC content: a lower bound showing
  the twin prime count does not decay to zero.
  The DR framework sharpens the sieve constant but does not supply
  the lower bound.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'primes'))
from prime_engine import twin_prime_generator, is_prime, digital_root

# ---------------------------------------------------------------------------
# 1.  The set partition (already proven)
# ---------------------------------------------------------------------------
print("="*62)
print("1.  Set partition T = T₂₄ ∪ T₅₇ ∪ T₈₁")
print("="*62)
print("""
  T    = { (p, p+2) : p and p+2 prime, p > 3 }
  T₂₄  = { (p, p+2) ∈ T : DR(p) = 2 }
  T₅₇  = { (p, p+2) ∈ T : DR(p) = 5 }
  T₈₁  = { (p, p+2) ∈ T : DR(p) = 8 }

  PROVEN: T = T₂₄ ∪ T₅₇ ∪ T₈₁  (disjoint, exhaustive, p > 3)

  TPC ↔ |T| = ℵ₀
       ↔ at least one of |T₂₄|, |T₅₇|, |T₈₁| = ℵ₀

  Because: union of three finite sets is finite.
  So TPC ↔ ¬(|T₂₄| < ∞ ∧ |T₅₇| < ∞ ∧ |T₈₁| < ∞).

  The partition does NOT simplify the proof — proving one track
  infinite is equally hard as proving T infinite.
  But it gives a cleaner target: focus on ONE track (say T₅₇)
  and prove |T₅₇| = ℵ₀.
""")

counts = {(2,4):0,(5,7):0,(8,1):0}
for p,p2,_,_,dr1,dr2 in twin_prime_generator(5):
    if p > 10**6: break
    counts[(dr1,dr2)] += 1
total = sum(counts.values())
print(f"  Empirical counts to 10⁶:")
print(f"    |T₂₄ ∩ [1,10⁶]| = {counts[(2,4)]:,}")
print(f"    |T₅₇ ∩ [1,10⁶]| = {counts[(5,7)]:,}")
print(f"    |T₈₁ ∩ [1,10⁶]| = {counts[(8,1)]:,}")
print(f"    Total:             {total:,}")

# ---------------------------------------------------------------------------
# 2.  Euclid approach
# ---------------------------------------------------------------------------
print()
print("="*62)
print("2.  Euclid-style contradiction")
print("="*62)
print("""
  FOR PRIMES:
    Assume {p₁,...,pₖ} finite complete list.
    N = p₁·p₂·...·pₖ + 1
    N not divisible by any pᵢ  →  N has a new prime factor.  ∎

  FOR TWIN PRIMES (why it fails):
    Assume {(p₁,p₁+2),...,(pₖ,pₖ+2)} finite complete list.
    Need: M such that M and M+2 are both prime, M ∉ list.

    Attempt: N = p₁(p₁+2)·p₂(p₂+2)·...·pₖ(pₖ+2) + 1
      N is coprime to all pᵢ and all pᵢ+2 — so N is a new prime
      (or has new prime factors). But N-2 is NOT necessarily prime.
      The construction escapes ONE condition; we need BOTH.

    No known product construction produces a new TWIN prime pair.
    The Euclid mechanism is fundamentally single-prime.

  STATUS: BLOCKED — no known Euclid-type argument for twin primes.
""")

# ---------------------------------------------------------------------------
# 3.  Furstenberg topology
# ---------------------------------------------------------------------------
print("="*62)
print("3.  Furstenberg topology")
print("="*62)
print("""
  Furstenberg (1955): Define topology on Z with basis
    B(a,n) = { a + kn : k ∈ Z }   (a ∈ Z, n ≥ 1)
  Each B(a,n) is clopen (open AND closed).

  Z \\ {-1,1} = ⋃_{p prime} B(0,p)
  If only finitely many primes: RHS = finite union of closed sets
  → RHS is closed → its complement {-1,1} is open.
  But {-1,1} is not open (no AP fits inside it).  Contradiction. ∎

  PORTING TO TWIN PRIMES:
  Need: T expressed as complement of a finite union of APs.
  T = { p : p prime AND p+2 prime } — requires TWO primality conditions.
  No such AP expression is known.

  MODIFIED ATTEMPT:
  Let S = { n ≥ 5 : n ≡ 2,5,8 (mod 9) and (n or n+2 composite) }
        = complement of T in { n : DR(n) ∈ {2,5,8} }

  If S were a finite union of APs → T would have positive density.
  But this requires PROVING S has AP structure, which is harder than TPC.

  STATUS: DOES NOT PORT directly. The AP-complement trick requires
  expressing the twin prime condition as AP membership, which is unknown.
""")

# ---------------------------------------------------------------------------
# 4.  Contradiction via DR structure
# ---------------------------------------------------------------------------
print("="*62)
print("4.  Contradiction approach: assume T finite, exploit DR structure")
print("="*62)
print("""
  Assume T is finite. Let (p*, p*+2) be the largest twin prime pair.
  Then for all prime p > p*: p+2 is composite.

  Every such p has DR(p) ∈ {2,5,8} (forced by twin prime track structure).
  DR(p+2) = DR(DR(p)+2) ∈ {4,7,1} respectively.

  So for all p > p* with DR(p)=2:
    p+2 is composite with DR(p+2)=4.
    p+2 has a prime factor q ≤ √(p+2).
    DR(q) ∈ {1,2,4,5,7,8} (q is prime).

  WHAT THIS FORCES:
    The composites of the form {n : DR(n)=4, n>p*+2} all have
    small prime factors. This is a DENSITY statement about composites.

  WHY IT DOESN'T YET GIVE A CONTRADICTION:
    Composites CAN always have small factors — that's not unusual.
    To get a contradiction, we'd need the density of these composites
    to exceed 1 (impossible) or the structure to be self-contradictory.
    The DR arithmetic alone doesn't supply this.

  THE MISSING INGREDIENT:
    A lower bound on the "surviving" candidates after sieving.
    Specifically: how many n ≡ 2 (mod 9) in [N, 2N] survive
    after removing those divisible by small primes?
    This is the SIEVE LOWER BOUND — the hard part of TPC.
""")

# ---------------------------------------------------------------------------
# 5.  The precise gap stated as a math problem
# ---------------------------------------------------------------------------
print("="*62)
print("5.  The precise gap")
print("="*62)
print("""
  KNOWN (upper bound, proven by Brun sieve):
    |T ∩ [1,N]| ≤ C₁ · N / log²(N)    for all N

  KNOWN (conditional lower, Hardy-Littlewood conjecture):
    |T ∩ [1,N]| ~ 2C₂ · N / log²(N)   as N → ∞
    where C₂ = ∏_{p>2} p(p-2)/(p-1)² ≈ 0.6601...

  KNOWN (Zhang 2013): infinitely many prime pairs with gap < 70,000,000.
    First unconditional proof that prime gaps stay bounded — a landmark.
    Improved to gap ≤ 246 by Maynard-Tao / Polymath8b (2014).
    Conditional on Elliott-Halberstam: gap ≤ 16.
    Gap = 2 (TPC) remains OPEN. Parity problem is the key obstruction.

  TPC ↔ lim inf_{N→∞}  |T ∩ [1,N]| · log²(N) / N  >  0

  Set theory says: an infinite set has no maximum.
  To prove T infinite, show this liminf is positive.
  That requires ANALYTIC number theory — density estimates.

  ─────────────────────────────────────────────────────
  WHAT THE DR FRAMEWORK ADDS TO THE SIEVE:

  The standard sieve candidate set for twin primes is:
    C_std = { n : n ≡ ±1 (mod 6) }  (size ~ N/3)

  The DR pre-filter identifies:
    C_DR  = { n : DR(n) ∈ {2,5,8} }  (size ~ N/3, same)

  C_std = C_DR for twin prime candidates (equivalent filters).
  So the DR framework does NOT reduce the candidate count —
  it restates the same filter in DR language.

  However: the three-track partition DOES separate candidates
  by mod-9 residue, which could give refined singular series
  constants per track. This is a SHARPENING of existing bounds,
  not a new proof method.
  ─────────────────────────────────────────────────────
""")

# ---------------------------------------------------------------------------
# 6.  The most tractable next step
# ---------------------------------------------------------------------------
print("="*62)
print("6.  Most tractable next target")
print("="*62)
print("""
  The three-track partition gives a cleaner proof TARGET:
  Instead of proving |T| = ℵ₀, prove |T₅₇| = ℵ₀.

  T₅₇ = { (p, p+2) : p prime, DR(p)=5 }
       = { (p, p+2) : p prime, p ≡ 5 (mod 9) }

  This is a TWIN PRIME problem restricted to a single arithmetic
  progression (mod 9, residue 5). Proving this one is infinite
  proves TPC.

  What's needed: a lower bound
    |T₅₇ ∩ [N, 2N]| ≥ c · N / log²(N)  for infinitely many N

  This requires either:
    (a) Brun-type sieve with a positive lower bound (open)
    (b) A structural argument showing T₅₇ cannot terminate
    (c) Connection to an already-proven infinitude result

  For (b): the constellation theorem shows that when the
  6-element pattern {c±1, c±11, c±13} forms, ALL THREE tracks
  appear simultaneously. So if T₅₇ terminates at p*, then
  no constellation can exist with center > p*+1. But
  constellations are denser than single pairs — if constellations
  are infinite, all three tracks are forced to be infinite.
  This reduces TPC to: "are constellations infinite?" — a
  harder problem (prime 6-tuple), not simpler.

  CONCLUSION:
    Set theory frames the problem cleanly.
    The proof bottleneck is analytic: a positive lower bound
    for twin prime counts in a residue class.
    No purely set-theoretic or algebraic argument is known to
    supply this bound. Sieve theory or L-function methods are
    currently the only paths toward it.
""")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("="*62)
print("SUMMARY")
print("="*62)
print(f"""
  Approach                     Status
  --------------------------------------------------------
  Euclid contradiction         BLOCKED — no twin-prime analog
  Injection f: N → T           CIRCULAR — equivalent to TPC
  Furstenberg topology         DOES NOT PORT — needs AP structure
  DR contradiction             REACHES sieve gap, no contradiction
  Set partition (T₂₄,T₅₇,T₈₁) SIMPLIFIES TARGET, same difficulty
  Constellation recurrence     REDUCES to 6-tuple (harder, not simpler)

  WHAT SET THEORY CONTRIBUTES:
    Language: ℵ₀, injection, partition, complement, no-maximum.
    The partition T = T₂₄ ∪ T₅₇ ∪ T₈₁ is a real set-theoretic result.
    Proving any one track infinite proves TPC.

  WHAT SET THEORY CANNOT SUPPLY:
    The positive lower bound on |T ∩ [N,2N]|.
    That is the number-theoretic content of TPC.
    It requires sieve theory, L-functions, or a fundamentally new idea.

  THE HONEST DISTANCE:
    The DR framework has built the best possible MAP of where
    twin primes live. The proof needs an ENGINE that counts them.
    That engine does not yet exist in the mathematical literature.
    Building it is the problem.
""")
