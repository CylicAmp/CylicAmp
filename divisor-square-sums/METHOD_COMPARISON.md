# How the problem was attacked: published vs this repo

Problem: n equal to the sum of the squares of its first k divisors (OEIS A185584).

| | Published (OEIS A185584) | This repo |
|---|---|---|
| **What is searched over** | Every integer n in turn. For each n, add squares of its divisors in increasing order and stop when the total reaches or passes n (Mathematica and PARI programs in the entry). | The prefix instead of n: a number m whose proper divisors are the first k divisors of n. Then n = m·p is forced, with p = σ₂(m)/m − m. |
| **How far it reaches** | The programs in the entry run to 5·10⁶ and 10⁷. Terms up to 9.3·10¹⁸ were added by contributors (2011–2014, one in 2026); their method is not stated in the entry. | Complete for the family up to m ≤ 10²², i.e. n up to about 6·10⁴³. A separate sieve over all n to 10⁹. |
| **Why it can reach that far** | Cost grows with n; every n is tested. | Only m with σ₂(m)/m² > 3/2 can work, which forces 6 \| m and prunes almost everything. Each large prime of m must divide σ₂ of the rest of m, so primes are read off rather than guessed. Loops of large primes that supply each other are listed and searched separately. |
| **What structure is stated** | None beyond the definition and examples. | The lemma: if p = σ₂(m)/m − m is prime, p > m/2, p ∤ m, then m·p is a solution. It explains 10 of the 19 published terms. |
| **Found by the published side and not the repo** | 5 non-family terms between 10⁹ and 10¹⁹: 4172437680, 5788838100, 38341734200, 343869932366333100, 5447947283895097800. | — |
| **Found by the repo and not published** | — | 577 family members beyond 9.3·10¹⁸. The m-sequence (60, 286650, 308700, …) is not in OEIS. |

The two approaches cover different ground. Testing every n finds every
solution but cannot go far. Searching over m goes very far but only finds one
shape of solution.
