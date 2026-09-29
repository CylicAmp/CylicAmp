# Numbers equal to the sum of the squares of their smallest divisors

Michael Song

## The question

Find every n whose k smallest divisors 1 = d₁ < d₂ < … < d_k satisfy

    d₁² + d₂² + … + d_k² = n

for some k.

Example: 130 has smallest divisors 1, 2, 5, 10, and 1 + 4 + 25 + 100 = 130.

## Known solutions below 10⁹ (all k)

| n | k | factorization |
|---|---|---|
| 130 | 4 | 2 · 5 · 13 |
| 1860 | 11 | 2² · 3 · 5 · 31 |
| 148480 | 19 | 2¹⁰ · 5 · 29 |
| 3039520 | 31 | 2⁵ · 5 · 11² · 157 |

An exhaustive sieve over every k finds exactly these four below 10⁹. That
sieve is in the working file (see *Sources*) and is not re-run by
`verify.py`, which checks the four values directly.

## Two easy facts

**k = 2 is impossible.** d₂ is the smallest prime factor q of n, so
n = 1 + q². Then q divides n and q², so q divides 1. Contradiction.

**At most one prime of n lies above the prefix.** Let r be the part of n made
of primes larger than d_k, and m = n / r. Every d_i ≤ d_k has all its prime
factors ≤ d_k, so it divides m. Hence m has at least k divisors, so m ≥ k.
Also n ≤ k·d_k². So r = n/m ≤ d_k². Two primes above d_k, or one squared,
would give r > d_k². So r is 1 or a single prime.

## The proper-divisor family

The largest group of solutions has a single shape: the prefix is **all the
proper divisors of some m**, and n = m·p with p prime.

**Lemma.** Let m be even, and p = σ₂(m)/m − m (σ₂ = sum of squares of
divisors). If p is a prime with p > m/2 and p ∤ m, then n = m·p is a solution
with k = τ(m) − 1.

*Proof.* A divisor of n that does not divide m is a multiple of p, so it
exceeds m/2. So the divisors of n that are ≤ m/2 are exactly the divisors of
m that are ≤ m/2, which are the proper divisors of m because m is even.
Their squares sum to σ₂(m) − m² = m·p = n. ∎

1860 = 60 · 31 is the smallest member. The next are 286650 · 143909 and
308700 · 175303.

### Complete count up to m ≤ 10²²

**There are exactly 587 members with m ≤ 10²².** All are listed in
`members_1e22.txt`, one per line: m, p, τ(m) and the factorization of m.

How completeness is established:

1. **Primes of m above 250.** m ≥ 60, so m ≤ 10²² leaves room for at most
   eight of them (10²²/60 < 250⁹). The search builds m prime by prime and
   reads each large prime directly off σ₂ of the part already built. It
   stops a branch as soon as the required ratio σ₂(m)/m² > 3/2 can no longer
   be reached.
2. **Supply cycles.** A large prime can also be forced by a loop of large
   primes that divide σ₂ of each other's powers. Every such loop that fits
   was listed separately (106 loops, plus 16 disjoint pairs of loops that
   fit together), and each was searched on its own.
3. **Counts.** The main search found 583 members. The loop searches found 4
   more that the main search cannot reach:

   ```
   277226850795071720400  = 2^4·3^2·5^2·11·13·1291·4817^2·17977
   1702491146631682328952 = 2^3·3^2·17^2·19·8011·8101^2·8191
   3099271808728883001312 = 2^5·3^3·7^2·17·8011·8101^2·8191
   4033972830409022319168 = 2^6·3·7·17·41·8011·8101^2·8191
   ```

The search program was checked against an independent Python version. Both
give identical node counts at 10¹², 10¹⁴, 10¹⁶ and 10¹⁸.

The largest member is m = 9933475307461748064000, with τ(m) = 103680.

## What is open

- **Whether the family is finite.** No finite search can settle this.
- **How many solutions lie outside the family.** Below 10⁹ three of the
  four solutions (130, 148480, 3039520) are not family members.
- **One sub-case needs a statement of odd-perfect-number type.** Some members
  would have m = 108·s², with gcd(s, 6) = 1. Such members exist only if
  s² divides 1435·σ₂(s²). The case where s is a power of a single prime is
  proved impossible, and so is s = p·r^b with p < r. Nothing else is proved. No such s
  exists with m ≤ 10²².

## Checking it yourself

    pip install sympy
    python3 verify.py

This checks the four small solutions by brute force, and all 587 family
members through the lemma above. It runs in under a second.

## Sources

- Working file, with the full derivations, corrections and search history:
  `math/theorems/theorem_245_n130_divisor_square_sum_gf37.py`
- Search programs: `tools/rust_family/`, `tools/divisor_square_*.py`
