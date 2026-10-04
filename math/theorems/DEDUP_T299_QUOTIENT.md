# Dedup pass — T299, then the quotient cluster

Prior art run before recording. Same rule as the negation cluster (`24f302a`).

## T299 — Two Maps Out of Phi_3

Two operations on one polynomial, not two proofs of one fact.

| | Use 1 — evaluate | Use 2 — quotient |
|---|---|---|
| object | Phi_3 in Z[x] | Z[x]/(Phi_3) = Z[omega] |
| output | Phi_3(137) = 18907 = 7×37×73; mu_3 = {1,10,26} | traces of y^2 = x^3+a; 4·37 = 11^2+27 |
| needs | factorization of 18907 | a curve and 4p = L^2+27M^2 |

Use 1 is T292, later packaged as L1 of T304 (three lists meet at 37). Use 2 does not factor 18907. Sharing a reduction of omega does not make one map the other.

What is forced, and is not a curve fact: F_37* is cyclic of order 36, so it has exactly one subgroup of each order dividing 36. The reduced unit group, the sixth powers, and <11> are three descriptions of that unique order-6 subgroup {1,10,11,26,27,36}. Re-checked: one subgroup per divisor of 36.

The 2026-09-16 scope upgrade already in the file — n | (p-1) collapses the coincidence to p = n^2+1 — is a second route to T300 Tier C and T301's closure n in {2,4,6}, not a new list. Re-checked below 20000: n=6 hits [37], n=4 hits [17], n=2 hits [5]. Honest sentence remains: 37 is to j=0 what 17 is to j=1728.

`connection_map.py` asserting 6^2+1^2 = 37 is Fermat two-square. Same integer, different content: there the 6 is not forced.

## Quotient cluster

One result, four statements. T276 is not in it.

| file | what it actually states | status |
|---|---|---|
| T118 | cosets of H_3 = IC are the 12 orbits of the 137-map; H_9 cosets are unions of three orbits; named-class membership | earliest coset=orbit identification. No priority note in the file. Own: the H_9 layer |
| T138 Part III | (Z/37Z)*/IC ≅ Z/12Z, DARK_A generates, dlog mod 12 | first file that names the quotient group. Own besides that: the DR subtraction law, and 3-6-9 products miss only 20 |
| T200 | sovereign cosets as g^2, g^3, g^4, g^5, g^10 inside that quotient | uses the quotient; does not originate it. Own: KEY/SEED arithmetic and the dlog-vs-dlog-mod-12 resolution for i=6 |
| T285 | results 1–3 restate T138/T200 | already cites both (2026-09-16). Own: antipodal = +6, inverse pairing n ↔ 12-n, TESLA↔C9 the one pair where they coincide because 6^2 ≡ -1 |
| T339 | index table byte-identical to T285's n=0..11 sequence; negation is j → j+6 | already cites T138 and T285. Own: safe-prime forced exclusions, semiprime split, prime-square confinement to even index, and the grading that the index is definitional |

T276 (Kolakoski gaps {2,3,4}) uses the orbit names as labels. log_2(3) = 26 is 2^26 ≡ 3 (mod 37), which is the multiplier sitting in IC, not a theorem about the quotient. Do not fold it in.

Re-checked independently: 12 cosets of {1,10,26}, identical to the orbit partition; unique subgroup per divisor of 36.

Asserted: `dedup_t299_quotient_check.py` (2026-10-02) runs every check in this note.
