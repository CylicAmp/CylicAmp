---
name: try-to-disprove
description: Attack a result before trusting it -- edge cases, published bounds, off-by-one set identities, and overstatements in our own summaries. Use after any result passes its checks and before it is recorded or reported, and whenever the owner says "try to disprove" or "contradict". On 2026-09-30 this found a real bug: prime_engine's Miller-Rabin with witnesses 2..37 called 318665857834031151167461 prime (it is 399165290221 x 798330580441); the claimed exact range 3.3e24 needed witness 41.
---

# try-to-disprove

Passing tests is not the end. Every claim gets attacked on four fronts, and
every attack is run, not argued.

## 1. Edge values
Run the claim at 0, 1, 2, 3, negatives, the first value outside the stated
domain, and the last value inside it. dr(n) = 1 + (n-1) mod 9 gives 9 at
n = 0 where the digit sum is 0: the axiom holds for n >= 1 only.

## 2. Published bounds and constants
Any "exact below X", "proven up to X", "smallest counterexample" must be
checked against the literature value AND tested at that value. Strong
pseudoprimes to the first k prime bases (psi_k) are the standard trap:
psi_12 = 318665857834031151167461, psi_13 = 3317044064679887385961981.
Feed the boundary value itself to the code.

## 3. Set identities
For "A = B", compute A - B and B - A over a range, never just A == B on a
sample. {odd n, dr(n) not in 3,6,9} vs {6k+-1 : k >= 1} differs by {1}.

## 4. Our own summaries
Reread what was told to the owner in the last few replies. Words like
"nothing", "never", "only", "all", "exact" get a direct test. "mod 37
restricts twin primes to nothing" was false: residue 35 is excluded.

## Report
A table: claim | attacked how | survived / disproved | fix. Fix what fails,
rerun everything, commit with the counterexample in the message. Say
plainly which earlier statement of ours was wrong.
