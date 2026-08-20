# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 241: Hydrogen Orbital Structure and GF(37) Sovereign Classification
================================================================================

USER OBSERVATION:
  Hydrogen atomic orbitals are exact solutions to the Schrodinger equation.
  From the simple sphere of 1s to the multi-lobed 6f, every surface shows
  where an electron is most likely to be found, with phase signs (+/-).
  Radial nodes: n-l-1. Angular nodes: l. Total nodes: n-1.
  The same geometry underpins molecular orbitals, laser transitions, MRI,
  quantum dots, and topological materials.

STRUCTURE:

A. PRIME SHELLS AND SA:
  The first three prime principal quantum numbers n = 2, 3, 5 have orbital
  counts n^2 that land exactly in SA = {4, 9, 25, 30}:
    n=2: 4 orbitals  -> 4  in SA
    n=3: 9 orbitals  -> 9  in SA
    n=5: 25 orbitals -> 25 in SA
  These are three of the four SA elements. The missing SA element is 30,
  which appears at n=17 (twin prime): 17^2 = 289 mod 37 = 30 in SA AND ST.

B. SOVEREIGN LANDMARKS:
  n=1:  1 orbital  -> 1  in H (identity; 1s is the ground state)
  n=2:  4 orbitals -> 4  in SA
  n=3:  9 orbitals -> 9  in SA
  n=5: 25 orbitals -> 25 in SA
  n=6: 36 orbitals -> 36 = -1 (antipode; shell 6 is the antipodal shell)
  n=7: 49 orbitals -> 12 in ST
  n=17: 289 orbitals -> 30 in SA AND ST (double-sovereign; 17 = twin prime)

C. CUMULATIVE ORBITALS AND SEED ORBIT:
  Orbitals through n=4: 1+4+9+16 = 30 mod 37 = 30 in SA AND ST (double-sovereign).
  Orbitals through n=5: 1+4+9+16+25 = 55 mod 37 = 18 in SEED_ORBIT = {18,24,32}.
  The five-shell cumulation lands in the 137-map orbit of seed 246.

D. NODAL STRUCTURE:
  Total nodes for shell n = n-1.
  n=1: 0 nodes -> 0 mod 37 = SEAM (37 | 0)
  n=2: 1 node  -> 1 in H  (prime shell, identity)
  n=4: 3 nodes -> 3 in ST (sovereign target)
  n=5: 4 nodes -> 4 in SA (prime shell, sovereign anchor)

E. MAGNETIC QUANTUM NUMBERS AND SOVEREIGN SETS:
  The count of magnetic states for subshell l is 2l+1.
  l=0 (s): 2l+1=1  in H   QR=+1  [spherical, single lobe]
  l=1 (p): 2l+1=3  in ST  QR=+1  [three lobes, sovereign target]
  l=2 (d): 2l+1=5         QR=-1  [five lobes, non-residue]
  l=3 (f): 2l+1=7         QR=+1  [7 = anchor prime]
  l=4 (g): 2l+1=9  in SA  QR=+1  [sovereign anchor]

  The s and p subshells (the chemistry-driving subshells) land in H and ST.
  The g subshell (l=4) lands in SA.

F. PHASE SIGN AND QR/NQR:
  Wavefunctions carry phase signs (+/-) that determine interference and bonding.
  In GF(37), the Legendre symbol classifies residues as QR (+1) or NQR (-1).
  l=0 (s): QR=+1; l=1 (p): QR=+1; l=2 (d): QR=-1; l=3 (f): QR=+1.
  The d subshell is the only NQR among the standard (s,p,d,f) subshells.
  DR(5) = 5 = prime seed.

G. THE TWIN PRIME CONNECTION:
  n=17 gives 30 in SA AND ST -- the double-sovereign element, the only element
  in both SA and ST simultaneously.
  17 is one of the twin prime pair (17, 19). DR(17)+DR(19) = 8+1 = 9.
  17+19 = 36 = -1 mod 37 = antipode.
  The twin prime shell is the double-sovereign shell.
================================================================================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
H_SET = {1, 10, 26}
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED_ORBIT = {18, 24, 32}


def dr(n):
    n = abs(n)
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True


def legendre(a, p):
    r = pow(a, (p-1)//2, p)
    return 0 if r == 0 else (-1 if r == p-1 else 1)


def run():
    print("=" * 70)
    print("THEOREM 241: HYDROGEN ORBITAL STRUCTURE AND GF(37) CLASSIFICATION")
    print("=" * 70)

    # A: Prime shells and SA
    print("\nA. PRIME SHELLS AND SA:")
    prime_shells = [(2, 4), (3, 9), (5, 25)]
    for n, orb in prime_shells:
        assert is_prime(n)
        assert orb == n*n
        assert orb % P in SA
        print(f"  n={n} (prime): {n}^2={orb} mod{P}={orb%P} in SA  check")
    assert {(n*n)%P for n,_ in prime_shells} == {4, 9, 25}
    print(f"  {{4,9,25}} are three of the four SA elements {{4,9,25,30}}  check")

    # n=17 completes SA
    n = 17
    r = (n*n) % P
    assert is_prime(n) and r in SA and r in ST
    print(f"  n={n} (twin prime): {n}^2={n*n} mod{P}={r} in SA AND ST (double-sovereign)  check")
    print(f"  All four SA elements accounted for by prime shells  check")

    # B: Sovereign landmarks
    print(f"\nB. SOVEREIGN LANDMARKS:")
    cases = [
        (1, "H: ground state identity"),
        (2, "SA"),
        (3, "SA"),
        (5, "SA"),
        (6, "-1 = antipode"),
        (7, "ST"),
        (17, "SA AND ST: double-sovereign, twin prime"),
    ]
    for n, label in cases:
        orb = n*n
        r = orb % P
        flags = []
        if r in H_SET: flags.append("H")
        if r in SA:    flags.append("SA")
        if r in ST:    flags.append("ST")
        if r == P-1:   flags.append("-1")
        print(f"  n={n}: {n}^2={orb} mod{P}={r} [{','.join(flags) or '-'}]  [{label}]")

    assert (1*1)%P in H_SET
    assert (6*6)%P == P-1
    assert (7*7)%P in ST
    assert (17*17)%P in SA and (17*17)%P in ST

    # C: Cumulative orbitals
    print(f"\nC. CUMULATIVE ORBITALS AND SEED ORBIT:")
    total = 0
    for n in range(1, 8):
        total += n*n
        r = total % P
        flags = []
        if r in H_SET:     flags.append("H")
        if r in SA:        flags.append("SA")
        if r in ST:        flags.append("ST")
        if r in SEED_ORBIT: flags.append("SEED")
        if r == 0:         flags.append("SEAM")
        print(f"  n=1..{n}: sum={total} mod{P}={r} DR={dr(total)} [{','.join(flags) or '-'}]")

    cum4 = sum(n*n for n in range(1, 5))
    cum5 = sum(n*n for n in range(1, 6))
    assert cum4 % P in SA and cum4 % P in ST
    assert cum5 % P in SEED_ORBIT
    print(f"  n=1..4 cumulative = {cum4} mod{P}={cum4%P} in SA AND ST  check")
    print(f"  n=1..5 cumulative = {cum5} mod{P}={cum5%P} in SEED_ORBIT  check")

    # D: Nodal structure
    print(f"\nD. NODAL STRUCTURE (total nodes = n-1):")
    nodal_cases = [(1, "SEAM"), (2, "H"), (4, "ST"), (5, "SA")]
    for n, label in nodal_cases:
        nodes = n - 1
        r = nodes % P
        flags = []
        if r == 0:      flags.append("SEAM")
        if r in H_SET:  flags.append("H")
        if r in SA:     flags.append("SA")
        if r in ST:     flags.append("ST")
        print(f"  n={n}: nodes={nodes} mod{P}={r} [{','.join(flags)}]  [{label}]")

    assert (1-1)%P == 0
    assert (2-1)%P in H_SET
    assert (4-1)%P in ST
    assert (5-1)%P in SA

    # E: Magnetic quantum numbers
    print(f"\nE. MAGNETIC QUANTUM NUMBERS (2l+1):")
    names = ["s", "p", "d", "f", "g", "h", "i"]
    for l in range(7):
        m = 2*l+1
        r = m % P
        qr = legendre(r, P)
        flags = []
        if r in H_SET: flags.append("H")
        if r in SA:    flags.append("SA")
        if r in ST:    flags.append("ST")
        print(f"  l={l} ({names[l]}): 2l+1={m} mod{P}={r} DR={dr(m)} QR={qr:+d} [{','.join(flags) or '-'}]")

    assert (2*0+1)%P in H_SET        # s in H
    assert (2*1+1)%P in ST            # p in ST
    assert (2*4+1)%P in SA            # g in SA
    assert legendre((2*2+1)%P, P) == -1  # d is NQR
    print(f"  s in H, p in ST, g in SA  check")
    print(f"  d subshell (l=2) is the only NQR among s,p,d,f  check")

    # F: Phase / QR connection
    print(f"\nF. PHASE SIGN AND QR/NQR:")
    print(f"  d subshell: QR={legendre(5,P):+d}  DR(5)={dr(5)} = prime seed  check")
    assert legendre(5, P) == -1 and dr(5) == 5

    # G: Twin prime
    print(f"\nG. TWIN PRIME CONNECTION:")
    print(f"  n=17 (twin prime): 17^2=289 mod{P}={289%P} in SA AND ST  check")
    print(f"  DR(17)+DR(19) = {dr(17)}+{dr(19)} = {dr(17)+dr(19)} = 9  check")
    print(f"  17+19 = {17+19} = -1 mod {P} = antipode  check")
    assert 289 % P in SA and 289 % P in ST
    assert dr(17) + dr(19) == 9
    assert (17 + 19) % P == P - 1

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
