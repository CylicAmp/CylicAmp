# CLASS: THEOREM
"""
Theorem 434: Fermat's Little Theorem, general and at p=37 -- the fact every
"divides 36" claim in this corpus already depends on
Author: Michael Warren Song (CyclicAmp)

=== THE THEOREM ===

For prime p and integer a with gcd(a, p) = 1:

    a^(p-1) = 1 (mod p)

Proof mechanism (Lagrange): (Z/pZ)* is a group of order p-1 under
multiplication; the order of every element divides the order of the group.
This is a fully proved classical theorem, not a conjecture, and it holds for
every prime -- it is Tier A in forced-check's sense, not a 37-specific fact.

=== AUDIT OF THE SUPPLIED FILE ===

Supplied as math/theorems/fermat_little.py: verify_fermat(a, p) =
pow(a, p-1, p) == 1, swept over 15 primes x 5 bases, skipping a % p == 0.
Checked directly: all 15 listed primes (2,3,5,7,11,13,17,19,23,29,31,97,
101,1009,104729) ARE prime, and 104729 is in fact the 10000th prime
(sympy.prime(10000)). The skip condition a % p == 0 is the right test for
gcd(a,p) != 1 when p is prime. No defect found in the supplied logic.

Renamed and renumbered to this corpus's convention (Txxx, CLASS header,
prior-art section, falsification criterion) rather than filed as a bare
fermat_little.py, and the pytest wrapper it proposed is dropped: this repo's
CI runs plain `pytest -v` with default discovery, which only collects files
named test_*.py/*_test.py, so a `def test_...` inside a theorem_*.py file is
never actually collected (checked: no file in math/theorems/ uses one). The
real runner for this corpus is tools/regression.py, which this file fits by
keeping `if __name__ == "__main__":`.

=== PRIOR ART ===

The p=37 instance is already in this corpus twice, neither as the general
theorem:
  math/primes/euler_totient.py -- asserts pow(2, 36, 37) == 1, phi(37) = 36,
    labelled "Fermat's little theorem" (one base, one prime).
  theorem_143_rsa_totient_twin_primes.py -- names FLT by this name as why
    RSA decryption recovers m over F_37 (e*d = 1 mod 36), does not verify it.
  ghost_kervaire_chain_gf37.py -- invokes FLT in the a^p = a form as a proof
    step for K(p) = 2^p - 2 = SEAM (mod p), general p, does not verify FLT
    itself either.
What is this file's own: the general statement checked across primes other
than 37, and the explicit dependency recorded below.

=== WHY THIS GOES THROUGH 37 (the dependency runs one way, not hunted) ===

Every orbit in this corpus has size exactly 3 because ord_37(26) = 3, and
that divides 36 only because 36 = phi(37) IS the order of (Z/37Z)* -- which
is exactly what this theorem supplies at p = 37. The 12-orbit partition, the
primitive-root-of-order-36 facts, and every other "divides 36" claim in the
corpus are downstream of this theorem at p=37, not parallel discoveries
alongside it. 37 is not singled out below; part (3) runs the identical check
against every prime, and 37 is simply included rather than exempted.

=== FALSIFICATION ===
Any prime p and a coprime to p with pow(a, p-1, p) != 1. None exists --
one would contradict Lagrange's theorem on finite groups.
"""
from sympy import isprime, prime


def verify_fermat(a: int, p: int) -> bool:
    return pow(a, p - 1, p) == 1


def mult_order(a: int, p: int) -> int:
    k, x = 1, a % p
    while x != 1:
        x = (x * a) % p
        k += 1
    return k


def run():
    # (1) The supplied sweep, reproduced and its hardcoded values checked.
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 97, 101, 1009, 104729]
    for p in primes:
        assert isprime(p), p
    assert prime(10000) == 104729

    bases = [2, 3, 5, 7, 10]
    checked = 0
    for p in primes:
        for a in bases:
            if a % p == 0:
                continue
            assert verify_fermat(a, p), (a, p)
            checked += 1

    # (2) The home case in full: every residue 1..36 at p=37, not a sample.
    P = 37
    for a in range(1, P):
        assert verify_fermat(a, P)

    # (3) The dependency this corpus relies on, tested at every prime in the
    # sweep above, 37 included without privilege: ord_p(a) | (p-1) for all a.
    for p in primes + [P]:
        for a in range(1, min(p, 50)):
            if a % p == 0:
                continue
            assert (p - 1) % mult_order(a, p) == 0

    return checked


if __name__ == "__main__":
    n = run()
    print(f"Fermat's Little Theorem: {n} (prime, base) pairs from the "
          f"supplied sweep, the complete p=37 residue set (36/36), and "
          f"order-divides-(p-1) at every prime tested -- all verified.")
