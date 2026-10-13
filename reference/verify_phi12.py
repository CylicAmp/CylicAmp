#!/usr/bin/env python3
"""verify_phi12.py -- the reproduction script for the owner's handoff
reference/phi3_phi12_at_137_handoff_2026_09_12.md (owner_work message #241, 2026-10-13).

The handoff names this script and gives its expected output (section 8) but the script itself
was not in the repo. Built 2026-10-13 to print exactly that output; it asserts its own output
against section 8, line for line, so any drift fails loudly.

    pip install sympy
    python3 reference/verify_phi12.py
"""
import io
import pathlib
from contextlib import redirect_stdout

from sympy import factorint, gcd, isprime, n_order, primefactors

A = 137
S = 113115117167


def phi3(x):
    return x * x + x + 1


def phi12(x):
    return x ** 4 - x ** 2 + 1


def report():
    p3, p12 = phi3(A), phi12(A)
    print(f"Phi_3(137)  = {p3} {factorint(p3)}")
    print(f"Phi_12(137) = {p12} {factorint(p12)}")
    print()
    for p in primefactors(p12):
        print(f"  p={p:<6} prime={isprime(p)}  ord_p(137)={n_order(A, p)}  p mod 12 = {p % 12}")
    print()
    print(f"S = {S} = {factorint(S)}")
    print(f"gcd(S, Phi_3)  = {gcd(S, p3)}")
    print(f"gcd(S, Phi_12) = {gcd(S, p12)}")
    print(f"P_12(137) cap PrimeDiv(S) = {sorted(set(primefactors(p12)) & set(primefactors(S)))}")
    print()
    print(f"ord_37(2) = {n_order(2, 37)}")
    print(f"2^12 mod 37 = {pow(2, 12, 37)}")
    print(f"mu_3 in F_37^x = {sorted(x for x in range(1, 37) if pow(x, 3, 37) == 1)}")
    print()
    print(f"ord_137(10) = {n_order(10, A)}  -> 1/137 repeating block length")


EXPECTED = """Phi_3(137)  = 18907 {7: 1, 37: 1, 73: 1}
Phi_12(137) = 352256593 {13: 1, 2473: 1, 10957: 1}

  p=13     prime=True  ord_p(137)=12  p mod 12 = 1
  p=2473   prime=True  ord_p(137)=12  p mod 12 = 1
  p=10957  prime=True  ord_p(137)=12  p mod 12 = 1

S = 113115117167 = {13: 1, 8701162859: 1}
gcd(S, Phi_3)  = 1
gcd(S, Phi_12) = 13
P_12(137) cap PrimeDiv(S) = [13]

ord_37(2) = 36
2^12 mod 37 = 26
mu_3 in F_37^x = [1, 10, 26]

ord_137(10) = 8  -> 1/137 repeating block length
"""

buf = io.StringIO()
with redirect_stdout(buf):
    report()
assert buf.getvalue() == EXPECTED, "output differs from section 8 of the handoff"

# the handoff's own section 8 text, read from the stored document, must be the same block
_doc = (pathlib.Path(__file__).resolve().parent / "phi3_phi12_at_137_handoff_2026_09_12.md").read_text(encoding="utf-8")
assert EXPECTED.strip() in _doc

if __name__ == "__main__":
    print(buf.getvalue(), end="")
