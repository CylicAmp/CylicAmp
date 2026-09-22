"""
mod4_1_sequence_audit.py

Arithmetic progression aₙ = 4n + 1, n = 0..250.
Complete residue class ≡ 1 (mod 4) from 1 to 1001.

─────────────────────────────────────────────────────────────────
Key structure:
  - 251 terms, range 1..1001
  - 80 primes (31.9%)
  - All primes are sums of two squares (Fermat's theorem)
  - 37-field anchors (37, 137, 142857) live IN this class
  - Seal numbers (191, 919, 787, 111) live in 4k+3

Framework values split:
  4k+1: 37, 137, 17, 13, 142857
  4k+3: 191, 919, 111, 787, 113183, 1395, 23, 19, 7, 11

37-field intersection:
  37  ≡ 0 (mod 37)  →  37-field zero      a_9
  149 ≡ 1 (mod 37)  →  37-field unity     prime
  593 ≡ 1 (mod 37)  →  37-field unity     prime
  137 ≡ 26 (mod 37) →  modular ratio 10⁻¹  a_34
  241 ≡ 19 (mod 37) →  19-center          prime

Terms ≡ 0 (mod 37): [37, 185, 333, 481, 629, 777, 925]
─────────────────────────────────────────────────────────────────
"""

import math
from collections import Counter
from fractions import Fraction
from sympy import isprime

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = abs(n) % 9
    return r if r else 9


def sum_of_two_squares(p):
    for a in range(1, int(math.sqrt(p)) + 1):
        b2 = p - a * a
        if b2 >= 0:
            b = int(math.sqrt(b2))
            if b * b == b2:
                return (a, b)
    return None


# ── Sequence construction ─────────────────────────────────────────────────────

sequence = [1 + 4 * n for n in range(251)]

check(len(sequence) == 251, "sequence length = 251", len(sequence), 251)
check(sequence[0] == 1,    "a_0 = 1",                sequence[0], 1)
check(sequence[250] == 1001, "a_250 = 1001",          sequence[250], 1001)
check(all(x % 4 == 1 for x in sequence),
      "all terms ≡ 1 (mod 4)", True, True)

# 1001 = 7 × 11 × 13
check(1001 == 7 * 11 * 13, "1001 = 7 × 11 × 13", 1001, 7 * 11 * 13)


# ── Position lookups ──────────────────────────────────────────────────────────

check(sequence[9] == 37,  "a_9  = 37",  sequence[9], 37)
check(sequence[34] == 137, "a_34 = 137", sequence[34], 137)
check(sequence[4] == 17,  "a_4  = 17",  sequence[4], 17)
check(sequence[3] == 13,  "a_3  = 13",  sequence[3], 13)


# ── Prime count ───────────────────────────────────────────────────────────────

primes_in_seq = [x for x in sequence if isprime(x)]

check(len(primes_in_seq) == 80, "80 primes in sequence", len(primes_in_seq), 80)

# First and last primes
check(primes_in_seq[0] == 5,   "first prime = 5",   primes_in_seq[0], 5)
check(primes_in_seq[-1] == 997, "last prime = 997", primes_in_seq[-1], 997)


# ── Fermat: primes ≡ 1 mod 4 are sums of two squares ─────────────────────────

TWO_SQ = {
    5:   (1, 2),
    13:  (2, 3),
    17:  (1, 4),
    29:  (2, 5),
    37:  (1, 6),
    41:  (4, 5),
    53:  (2, 7),
    61:  (5, 6),
    73:  (3, 8),
    89:  (5, 8),
    97:  (4, 9),
    101: (1, 10),
    109: (3, 10),
    113: (7, 8),
    137: (4, 11),
}

for p, (a, b) in TWO_SQ.items():
    check(a * a + b * b == p,
          f"{p} = {a}² + {b}²", a * a + b * b, p)

# Every prime in sequence has a two-square representation
for p in primes_in_seq:
    rep = sum_of_two_squares(p)
    check(rep is not None,
          f"prime {p} ≡ 1 (mod 4) is sum of two squares", rep is not None, True)
    if rep:
        a, b = rep
        check(a * a + b * b == p,
              f"{p} = {a}² + {b}²", a * a + b * b, p)


# ── 37-field residues ──────────────────────────────────────────────────────────

check(37 % 37 == 0,   "37  ≡ 0 (mod 37) — 37-field zero",      37 % 37, 0)
check(149 % 37 == 1,  "149 ≡ 1 (mod 37) — 37-field unity",     149 % 37, 1)
check(593 % 37 == 1,  "593 ≡ 1 (mod 37) — 37-field unity",     593 % 37, 1)
check(137 % 37 == 26, "137 ≡ 26 (mod 37) — modular ratio 10⁻¹", 137 % 37, 26)
check(241 % 37 == 19, "241 ≡ 19 (mod 37) — 19-center",         241 % 37, 19)

# 26 = 10⁻¹ mod 37
check(10 * 26 % 37 == 1, "10 × 26 ≡ 1 (mod 37)", 10 * 26 % 37, 1)

# Primality of 37-field unity primes
check(isprime(149), "149 is prime", isprime(149), True)
check(isprime(593), "593 is prime", isprime(593), True)
check(isprime(241), "241 is prime", isprime(241), True)

# Both unity primes in sequence
check(149 in sequence, "149 in sequence", 149 in sequence, True)
check(593 in sequence, "593 in sequence", 593 in sequence, True)

primes_1_mod_37 = [p for p in primes_in_seq if p % 37 == 1]
check(primes_1_mod_37 == [149, 593],
      "primes in sequence ≡ 1 (mod 37)", primes_1_mod_37, [149, 593])


# ── Terms ≡ 0 (mod 37) ────────────────────────────────────────────────────────

# 4n+1 ≡ 0 (mod 37)  →  4n ≡ -1 ≡ 36 (mod 37)  →  n ≡ 9 (mod 37)
terms_0_mod37 = [x for x in sequence if x % 37 == 0]
check(terms_0_mod37 == [37, 185, 333, 481, 629, 777, 925],
      "terms ≡ 0 (mod 37)", terms_0_mod37, [37, 185, 333, 481, 629, 777, 925])

# 37 is the only prime in that list
check(sum(1 for x in terms_0_mod37 if isprime(x)) == 1,
      "37 is the only prime ≡ 0 (mod 37) in sequence",
      sum(1 for x in terms_0_mod37 if isprime(x)), 1)

# DR(37) = 1, so DR(37×k) = DR(k) — DRs follow the cofactor
# cofactors in sequence: 1,5,9,13,17,21,25 → DR 1,5,9,4,8,3,7
TERMS_DR = [dr(v) for v in terms_0_mod37]
check(TERMS_DR == [1, 5, 9, 4, 8, 3, 7],
      "DR values of terms ≡ 0 (mod 37)", TERMS_DR, [1, 5, 9, 4, 8, 3, 7])
# cofactors are themselves the first 7 terms of the 4k+1 sequence
cofactors = [v // 37 for v in terms_0_mod37]
check(cofactors == [1, 5, 9, 13, 17, 21, 25],
      "cofactors of 37-zero terms are first 7 terms of 4k+1",
      cofactors, [1, 5, 9, 13, 17, 21, 25])

# 333 = 9 × 37 — joint period of scale-2 orbit
check(333 == 9 * 37, "333 = 9 × 37 in terms ≡ 0 (mod 37)", 333, 9 * 37)
check(dr(333) == 9,  "DR(333) = 9 = NULL", dr(333), 9)


# ── Near-uniform distribution mod 37 ─────────────────────────────────────────

# 251 terms, 251 = 6×37 + 29 → 29 residues get 7 terms, 8 residues get 6 terms
mod37_counts = Counter(x % 37 for x in sequence)
count_values = sorted(set(mod37_counts.values()))
check(set(count_values) == {6, 7},
      "mod-37 distribution uses only counts 6 and 7",
      set(count_values), {6, 7})
check(sum(mod37_counts.values()) == 251,
      "total term count = 251", sum(mod37_counts.values()), 251)


# ── Framework values mod 4 split ──────────────────────────────────────────────

IN_4K1  = [37, 137, 17, 13]          # ≡ 1 mod 4
IN_4K3  = [191, 919, 111, 787, 113183, 1395, 23, 19, 7, 11]  # ≡ 3 mod 4
# 142857: 142857 % 4 = 1, but 142857 % 4 computation:
check(142857 % 4 == 1, "142857 ≡ 1 (mod 4)", 142857 % 4, 1)
# (out of sequence range 1..1001, but same residue class)

for v in IN_4K1:
    check(v % 4 == 1, f"{v} ≡ 1 (mod 4) — in 4k+1 class", v % 4, 1)

for v in IN_4K3:
    check(v % 4 == 3, f"{v} ≡ 3 (mod 4) — in 4k+3 class", v % 4, 3)


# ── DR values for key sequence elements ───────────────────────────────────────

check(dr(37)  == 1, "DR(37) = 1",  dr(37),  1)
check(dr(137) == 2, "DR(137) = 2", dr(137), 2)
check(dr(17)  == 8, "DR(17) = 8",  dr(17),  8)
check(dr(13)  == 4, "DR(13) = 4",  dr(13),  4)
check(dr(149) == 5, "DR(149) = 5", dr(149), 5)
check(dr(593) == 8, "DR(593) = 8", dr(593), 8)
check(dr(241) == 7, "DR(241) = 7", dr(241), 7)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Arithmetic Progression aₙ = 4n+1 (n = 0..250) — Sequence Audit")
    print("=" * 66)

    print(f"\n── Sequence ──")
    print(f"  Terms: {len(sequence)}    Range: {sequence[0]}..{sequence[-1]}")
    print(f"  1001 = 7 × 11 × 13 ✓")
    print(f"  All terms ≡ 1 (mod 4): ✓")

    print(f"\n── Positions ──")
    print(f"  a_9  = 37    (37-field zero)")
    print(f"  a_34 = 137   (modular ratio 10⁻¹ mod 37)")
    print(f"  a_4  = 17")
    print(f"  a_3  = 13")

    print(f"\n── Primes ──")
    print(f"  Count: {len(primes_in_seq)} / 251 = {len(primes_in_seq)/251*100:.1f}%")
    print(f"  All are sums of two squares (Fermat's theorem): ✓")

    print(f"\n── Two-square representations ──")
    for p, (a, b) in sorted(TWO_SQ.items()):
        print(f"  {p:3d} = {a}² + {b}² = {a**2} + {b**2}")

    print(f"\n── 37-field residues ──")
    print(f"  37  ≡  0 (mod 37) — 37-field zero    DR={dr(37)}")
    print(f"  149 ≡  1 (mod 37) — 37-field unity   DR={dr(149)}  prime")
    print(f"  593 ≡  1 (mod 37) — 37-field unity   DR={dr(593)}  prime")
    print(f"  137 ≡ 26 (mod 37) — modular ratio 10⁻¹  DR={dr(137)}")
    print(f"  241 ≡ 19 (mod 37) — 19-center        DR={dr(241)}  prime")
    print(f"  10 × 26 ≡ {10*26%37} (mod 37)  →  26 = 10⁻¹ mod 37 ✓")
    print(f"  Primes ≡ 1 (mod 37): {primes_1_mod_37}")

    print(f"\n── Terms ≡ 0 (mod 37) ──")
    print(f"  {terms_0_mod37}")
    print(f"  4n+1 ≡ 0 (mod 37)  →  n ≡ 9 (mod 37)")
    print(f"  333 = 9 × 37  DR(333) = {dr(333)} = NULL ✓")

    print(f"\n── Mod-37 distribution ──")
    print(f"  Count values: {sorted(set(mod37_counts.values()))}"
          f"  (near-uniform; 251 = 6×37+29)")

    print(f"\n── Framework values mod 4 split ──")
    print(f"  IN 4k+1: 37, 137, 17, 13, 142857")
    print(f"  IN 4k+3: 191, 919, 111, 787, 113183, 1395, 23, 19, 7, 11")
    print(f"  37-field anchors sit in 4k+1; seal numbers in 4k+3")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
