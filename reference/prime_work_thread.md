```
================================================================================
PRIME WORK FROM THIS THREAD
================================================================================
Scope: cyclotomic factorization of Φ₃(137), F₃₇ orbits, zeta-floor
labels, CM side-conditions, Maynard–Tao / Polymath variational problem.
Not included: local-model economics, IEEE 754, ISO/GB number-system
notes, Bunch–Kaufman / rook / Woodbury / BFGS.
================================================================================


0. THE PUZZLE THAT STARTED IT
--------------------------------------------------------------------------------
7 (30) 37 (36) 73 (?)

As an isolated sequence: gaps 37−7=30, 73−37=36, next gap 42,
so 73+42=115. That parse is internally consistent and better than a −1 rule.

It is the wrong reading of what the numbers are.

7, 37, 73 are the complete prime factorization of
    Φ₃(137) = 137² + 137 + 1 = 18907 = 7 × 37 × 73.
T292: that set is exhaustive. There is no fourth term. The sequence
terminates by theorem.

115 = 5×23 does not divide 18907 and is not a candidate.

Why the gaps look patterned
  Every admissible prime dividing n²+n+1 satisfies p ≡ 1 (mod 3)
  (so a cube root of unity exists mod p) and is odd, so any two differ
  by a multiple of 6. Thus 30=6×5 and 36=6×6 were forced. The only
  free observation is that the multipliers are consecutive (5 then 6).
  That pattern does not recur. For n<60 with n²+n+1 having ≥3 prime
  factors, 0 of 7 cases show a uniform +6 in the gaps
    n=16  273   [3,7,13]    gaps [4,6]
    n=25  651   [3,7,31]    gaps [4,24]
    n=49  2451  [3,19,43]   gaps [16,24]
    n=55  3081  [3,13,79]   gaps [10,66]


1. CYCLOTOMIC FACTS USED
--------------------------------------------------------------------------------
Φ₃(x) = x² + x + 1.
p | Φ_d(a)  ⇒  ord_p(a) = d, unless p | d
  (exception: p is then the largest prime factor of d).

Φ_d(137) for d=1..12 was computed; every prime factor of Φ_d(137)
had ord_p(137)=d except the p|d cases, which checked out.
Every prime p<2000, p≠137, lands in exactly one row: Φ_{ord_p(137)}(137).

d=3 row: Φ₃(137)=18907=7×37×73.
37 is one of three primes in that slot. The slot is not special;
it is the slot the later F₃₇ framework happens to use.

Admissible primes for orbit size k = factors of Φ_k(137) with
ord_p(137)=k. Choosing k=3 was not forced by the cyclotomic table;
it is forced only by 137 ≡ 26 (mod 37) being a cube root of unity.

What this is not
  Not a closed form for primes. Φ_n(a) is often composite.
  Not a proof of RH, and not a derivation of 1/137.
  Not CM. The same ω with ω²+ω+1=0 appears in ℤ[ω] as an
  endomorphism of j=0 curves. That is a second use of Φ₃,
  not a corollary of the cyclotomic plate.


2. TWO USES OF Φ₃  (KEEP SEPARATE)
--------------------------------------------------------------------------------
Use A — cyclotomic / field
  Φ₃(x)=x²+x+1 in ℤ[x].
  p | Φ₃(a) ⇒ ord_p(a)=3 (unless p|3).
  Splitting of x²+x+1 in F_p is the existence of a primitive
  cube root of unity in F_p, i.e. 3 | (p−1).

Use B — CM endomorphism ring
  ℤ[ω], ω²+ω+1=0, ring of integers of ℚ(√−3), j=0 curves
  E: y² = x³ + a.
  End(E) contains ℤ[ω]. Unit group has order 6.
  Traces of Frobenius at p come from 4p = L² + 27 M².
  Twists by sixth powers: a'/a ∈ (F*)⁶.

Same polynomial, two theories. The plate's μ₃-action on F₃₇ˣ is Use A.
The j=0 trace list is Use B. Neither implies the other.


3. F₃₇ˣ / μ₃   ORBITS
--------------------------------------------------------------------------------
F₃₇ˣ is cyclic of order 36. Primitive root 2.
μ₃ = {1, 10, 26} ⊂ F₃₇ˣ.
  10² ≡ 26, 10³ ≡ 1
  26² ≡ 10, 26³ ≡ 1
  10²+10+1 ≡ 0, 26²+26+1 ≡ 0
  ⟨10⟩ = ⟨26⟩ = μ₃. Order 3, not 9.
  137 ≡ 26 (mod 37).  26⁻¹ ≡ 10 (mod 37).

12 orbits of F₃₇ˣ / ⟨1,10,26⟩, least representatives:

  O01  {1, 10, 26}     cube-root subgroup itself
  O02  {2, 15, 20}
  O03  {3, 4, 30}
  O04  {5, 13, 19}
  O05  {6, 8, 23}
  O06  {7, 33, 34}
  O07  {9, 12, 16}
  O08  {11, 27, 36}
  O09  {14, 29, 31}
  O10  {17, 22, 35}
  O11  {18, 24, 32}
  O12  {21, 25, 28}

Plus SEAM: 0 (mod 37).
Check: 12×3 + 1 = 37.

Action on a nonzero residue:  x ↦ 26x ↦ 10x ↦ x.
(The posted plate that wrote x ↦ 26x ↦ 18x ↦ x is wrong.)

Named labels used later in the thread (same 12 sets):
  IC={1,10,26}  DARK_A={2,15,20}  C3={3,4,30}  CAS_EXT={5,13,19}
  TESLA={6,8,23}  D7={7,33,34}  SA_ST_A={9,12,16}  NEG_H={11,27,36}
  C9={14,29,31}  NQR17={17,22,35}  SEED={18,24,32}  SA_ST_B={21,25,28}

These names are labels, not theorems.

Subgroup lattice of C₃₆
  Divisors of 36: 1,2,3,4,6,9,12,18,36  (9 subgroups).
  Those containing μ₃ (order divisible by 3): 3,6,9,12,18,36  (6 of 9).
  T286's lattice is the sublattice above μ₃, not the whole subgroup lattice.

Sixth powers in F₃₇ˣ equal ⟨27⟩, order 6, the H_2 lattice element.
That is a Z/36Z fact. It does not predict CM traces.


4. 137, DIGITAL ROOTS
--------------------------------------------------------------------------------
137 ≡ 26 (mod 37) = MULT
26⁻¹ ≡ 10 ∈ IC
38 ≡ 1 (mod 37)
65 ≡ 28 (mod 37)
19 ≡ 19 (mod 37)

DR(n) = n mod 9, except multiples of 9 give 9 (n>0).
DR(137)=2  because 137 ≡ 2 (mod 9).
So DR(n·137)=4  iff  n ≡ 2 (mod 9).
That is a mod-9 fact, independent of the F₃₇ geometry.

DR(18907)=7.
Two derivations:
  (a) DR(7)=7, DR(37)=1, DR(73)=1, so DR(7·37·73)=7.
      37 and 73 are invisible mod 9.
  (b) 137 ≡ 2 (mod 9) ⇒ n²+n+1 at n≡2 (mod 9) is 4+2+1=7.

"DR = smallest prime factor" is not a law.
mod 9 and mod 7 are independent by CRT.
Empirical: among n=2..3000, DR(n²+n+1) lying in the prime-factor
set of n²+n+1 is common, not rare. n=137 is one of many.


5. ZETA FLOORS  floor(γ_n) mod 37
--------------------------------------------------------------------------------
First 20 ordinates (LMFDB), floor, residue, orbit:

   n     γ            floor   mod 37   orbit
   1   14.134725        14      14     O09
   2   21.022040        21      21     O12
   3   25.010858        25      25     O12
   4   30.424876        30      30     O03
   5   32.935062        32      32     O11
   6   37.586178        37       0     SEAM
   7   40.918719        40       3     O03
   8   43.327073        43       6     O05
   9   48.005151        48      11     O08
  10   49.773832        49      12     O07
  11   52.970321        52      15     O02
  12   56.446248        56      19     O04
  13   59.347044        59      22     O10
  14   60.831779        60      23     O05
  15   65.112544        65      28     O12
  16   67.079811        67      30     O03
  17   69.546402        69      32     O11
  18   72.067158        72      35     O10
  19   75.704691        75       1     O01
  20   77.144840        77       3     O03

20 zeros over 13 bins (12 orbits + SEAM).
Expected 20/13 ≈ 1.54 each.
χ² ≈ value consistent with uniform (χ²/df near 1, p well above 0.05).
The table is correct. The distribution at n=20 carries no signal.

Standouts that were labelled, not proved:
  38 = 2×19.  38 ≡ 1 (mod 37) ∈ μ₃.
  19 ∈ O04 = {5,13,19}; floor(γ₁₂) ≡ 19.
  38×137 and 65×137 both have digital root 4.
  floor(γ₁₅)=65.

None of this is a proof of RH or a derivation of 1/137.


6. T299  /  CM UNIT CONDITION
--------------------------------------------------------------------------------
Condition:  n · gcd(n, p−1) = p−1,
where n = #units of the CM ring.

If n | (p−1) this collapses to p−1 = n², i.e. p = n²+1,
and that prime is unique for each n.

  ring          j      n    p=n²+1   prime?   n|(p−1)?
  ℤ (generic)   any    2       5       yes       yes
  ℤ[i]         1728    4      17       yes       yes
  ℤ[ω]            0    6      37       yes       yes

Exhaustive search of primes < 100000: those three are the only hits
for n=2,4,6.

Direct check, units vs n-th powers:
  p=5,  n=2: units {1,4}           = squares
  p=17, n=4: units {1,16,i,−i}     = 4th powers   (i²≡−1)
  p=37, n=6: units {±1,±ω,±ω²}     = 6th powers   (ω=26)

Near-miss, unrelated: 17 | (137−1) because 137 ≡ 1 (mod 17).
That is a fact about 137, not about Gaussian CM.

j=0 traces from 4p = L²+27M², p=37: L=11, M=1
  traces {±1, ±10, ±11}.
j=1728 traces from p = L²+M²: different list.
Nothing in Z/36Z predicts that trace 1 exists. That is the only
place the F₃₇ picture touches something outside itself (CM / GLV).


7. DIGIT-PREFIX SEQUENCE  2, 24, 246, 2468, 24680
--------------------------------------------------------------------------------
  n       mod 37   orbit
  2           2    DARK_A
  24         24    SEED
  246        24    SEED     (collision)
  2468       26    IC
  24680      20    DARK_A

246 − 24 = 222 = 6×37. Appending digit e to n is invisible mod 37
iff 9n+e ≡ 0 (mod 37). For base 24 that digit is 6, which is why
24 and 246 share a residue.

2468 ≡ 26 ≡ 137 (mod 37), the multiplier's own residue.
cls-additivity (T215 style) held on the checked example
  cls(2)+cls(123) ≡ cls(246) (mod 12).

This is modular arithmetic of appending decimal digits.
It is not a law of primes and not a cyclotomic generator.


8. MAYNARD–TAO SIEVE WEIGHTS
--------------------------------------------------------------------------------
Admissible k-tuple H={h₁,…,hₖ}, level R = N^{θ/2−ε}.

  w_n = ( ∑_{dᵢ | n+hᵢ} λ_{d₁,…,dₖ} )²

λ vanishes unless each dᵢ is squarefree, the dᵢ are pairwise coprime,
(dᵢ,W)=1, and ∏ dᵢ ≤ R.

Smooth choice: with F supported on the simplex
  Δ_k = { xᵢ ≥ 0, ∑ xᵢ ≤ 1 },

  λ_{d₁,…,dₖ} = (∏ μ(dᵢ)) F(log d₁ / log R, …, log dₖ / log R).

GPY is the special case F(x)=g(∑ xᵢ) (one-dimensional, product of
the shifts). Maynard–Tao is every F on Δ_k.

The square is Selberg positivity. The simplex is ∏ dᵢ ≤ R after
xᵢ = log dᵢ / log R. Weights are not a model of Φ_n and not a
partition of F_pˣ.


9. VARIATIONAL PROBLEM
--------------------------------------------------------------------------------
  I(F)  = ∫_{Δ_k} F(x)² dx
  y^{(i)}(x̂ᵢ) = ∫_0^{1−|x̂ᵢ|₁} F(x) dxᵢ
  Jᵢ(F) = ∫_{Δ_{k−1}} (y^{(i)})² d x̂ᵢ

  M_k = sup_{F ≢ 0}  (∑_{i=1}^k Jᵢ(F)) / I(F)

Level of distribution θ gives m+1 primes in an admissible k-tuple
i.o. once M_k > 2m/θ.
Unconditionally θ=1/2, so two primes need M_k > 4.

A maximizer exists (compact slice operator). Symmetric F is enough.
Large k: M_k ∼ log k.
Upper comparison: M_k ≤ (k/(k−1)) log k.

Only the comparison M_k > 2/θ is arithmetic. I and Jᵢ are analysis
on Δ_k.


10. RADIAL ANSATZ  — CORRECTION
--------------------------------------------------------------------------------
One-parameter family F(x) = (1−∑ xᵢ)^r  on Δ_k:

  ∑ Jᵢ / I  =  2k(2r+1) / ((r+1)(k+2r+1))

For every finite k the max over r is strictly less than 4.
As k,r → ∞ the value approaches 4 from below and never crosses it.

  k=3    r≈0.37   M≈1.61     (asymp 1.65)
  k=10   r≈1.08   M≈2.31     (asymp 2.56)
  k=50   r≈3.04   M≈3.07     (asymp 3.99)
  k=105  r≈4.62   M≈3.32     (asymp 4.70)
  k=500  r≈10.68  M≈3.66     (asymp 6.23)

RETRACTED: "that already gives M_105>4."
That sentence is false for this family. GPY's F=g(∑ xᵢ) is the same
lock: M_k → 4, not ∞.

What actually produces M_105>4 is non-radial symmetric F
(products ∏ g(xᵢ) cut off to Δ_k, or symmetric polynomials).
Those are the functions with M_k ∼ log k.


11. TWO-PARAMETER PERTURBATION  (COMPUTED)
--------------------------------------------------------------------------------
  F(x) = (1−∑ xᵢ)^r ( 1 + c ∑_{i<j} xᵢ xⱼ )

c=0 recovers the closed form to 10^{−14}.
At k=105 a scan in (r,c) peaked near

  r≈4.6,  c≈−1,   M_105≈3.40.

Not over 4. One extra quadratic term is not enough.

  g(∑ xᵢ) or (1−∑ xᵢ)^r              M_105 ≈ 3.32    lim = 4
  times (1 + c ∑_{i<j} xᵢ xⱼ)        M_105 ≈ 3.40    still < 4
  high-degree symmetric polynomials  M_105 > 4       ∼ log k


12. OPTIMIZING F  /  POLYMATH8b EIGENVALUE METHOD
--------------------------------------------------------------------------------
Restrict F to a span b₁,…,b_n of symmetric functions on Δ_k.
Then I(F)=aᵀ A a and ∑ Jᵢ(F)=aᵀ B a, with Gram matrices
of Beta / Dirichlet integrals of the basis (exact rationals).

Generalized eigenproblem  B a = λ A a.
λ_max on that span is a lower bound for M_k.
Numerically: Cholesky A=LLᵀ, ordinary eigensolve of
L⁻¹ B L⁻ᵀ, recover a = L⁻ᵀ v.

Two bases used by Polymath8b:
  (i) (1−P_{(1)})^a P_α with α even, degree ≤ d.
      M_54 > 4.00238 at d=23.
  (ii) Krylov  bᵢ = L^{i−1} 1, Hankel Gram matrices.
      Cheaper; produced the table sitting just under
      (k/(k−1)) log k.

Enlarged simplex ∑ xᵢ ≤ 1+ε, paid as a slightly smaller
effective θ:
  M_{50, 1/25} > 4.00124   (d=25)
  M_{51, 1/50} > 4.00156   (d=22)

With a short admissible 50-tuple this is the gap 246.

Selected Polymath lower bounds vs (k/(k−1)) log k:
  k=2     1.38593    1.38630
  k=5     2.00714    2.01180
  k=10    2.54547    2.55843
  k=50    3.93586    3.99187
  k=54    4.00223    4.06425
  k=100   4.46424    4.65169

Maynard's published 600 used a coarser explicit F and k=105
in the non-radial class, not the radial family of §10.


13. WHAT WAS NOT CLAIMED
--------------------------------------------------------------------------------
  The 12 orbits and the μ₃ action are theorems in F₃₇.
  The zeta-floor table is a correct labelling; n=20 is consistent
  with uniform, not a signal.
  Φ₃(137)=7×37×73 is a complete factorization.
  T299's three primes 5,17,37 are n²+1 for n=2,4,6.
  M_k ∼ log k for non-radial F is Maynard; M_54>4 is Polymath8b.
  None of this is a proof of RH.
  None of this is a derivation of α ≈ 1/137.
  The two uses of Φ₃ stay separate.
================================================================================
END COPY
================================================================================
```

---

Verification note (added on copy, not part of the original text)

Checked before commit; everything below held except one item.

Confirmed:
- Φ₃(137) = 18907 = 7 × 37 × 73, complete
- the four n<60 cases in §0 (n=16, 25, 49, 55) and their gap lists
- 12 orbits of F₃₇ˣ under μ₃, exactly as listed; 12×3+1 = 37
- x ↦ 26x ↦ 10x ↦ x (the 18x form is indeed wrong)
- 137 ≡ 2 (mod 9), DR(137)=2; 18907 ≡ 7 (mod 9), DR(18907)=7
- all 20 rows of the §5 zeta-floor table — γ, floor, residue and orbit,
  0 mismatches against computed zeta zeros
- §5 χ²: counts give χ² = 8.60 on df = 12, χ²/df = 0.717, consistent
  with uniform as stated (expected counts are ≈1.5, so the χ²
  approximation is itself weak here — the "no signal" reading stands)
- 246 − 24 = 222 = 6×37; 2468 ≡ 26 (mod 37)
- §10 radial closed form 2k(2r+1)/((r+1)(k+2r+1)): the r-maxima
  reproduce 1.61, 2.31, 3.07, 3.32, 3.66 at k = 3, 10, 50, 105, 500,
  all strictly below 4
- §12 comparison column (k/(k−1))log k: 1.38630, 2.01180, 2.55843,
  3.99187, 4.06425, 4.65169

One discrepancy:
- §7 lists 24680 → 20 → DARK_A. Computed: 24680 = 37×667 + 1, so
  24680 ≡ 1 (mod 37), which is IC/O01, not 20/DARK_A. The other four
  rows of that table (2, 24, 246, 2468) are correct as written.
