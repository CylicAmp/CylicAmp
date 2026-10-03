#!/usr/bin/env python3
"""Decide if a construction is 37-specific by RE-RUNNING it. Usage:
   tier.py base "a*(b*b+b+1) + d*(b+2)"   # which bases b make the a-term vanish
   tier.py prime "cube-roots-exist"        # which primes share the property
   tier.py order 10 3                      # which primes p have ord_p(10) = 3
"""
import sys
from math import gcd

def isp(n): return n > 1 and all(n % k for k in range(2, int(n**.5)+1))

def order(a, p):
    if p <= 1 or a % p == 0: return None
    for k in range(1, p):
        if pow(a, k, p) == 1: return k

def main():
    if len(sys.argv) < 2: print(__doc__); return
    m = sys.argv[1]
    if m == "order":
        a, want = int(sys.argv[2]), int(sys.argv[3])
        hits = [p for p in range(3, 20000) if isp(p) and p != a
                and order(a, p) == want]
        print(f"primes p with ord_p({a}) = {want}, up to 20000:")
        print(f"  {hits}")
        print(f"  count {len(hits)}")
        if len(hits) == 1:
            print(f"  UNIQUE -> Tier C. p | {a}^{want} - 1 = {a**want - 1}")
        else:
            print(f"  shared -> Tier A or B. carries no information about 37")
    elif m == "base":
        P = 37
        roots = [b for b in range(P) if (b*b + b + 1) % P == 0]
        print(f"bases b mod 37 with b^2+b+1 == 0: {roots}")
        print(f"  these are the primitive cube roots of unity = <10> minus 1")
        for b in roots:
            print(f"  base {b:2d}: R3 = {b*b+b+1} = {(b*b+b+1)//P} x 37,"
                  f"  AP residue = {(b+2)%P}d")
        print("  -> the admissible bases are a NAMED ORBIT. base 10 is not")
        print("     arbitrary: it works because 10 generates mu_3.")
    elif m == "prime":
        print(" p   p%3  Phi_3 roots  mu_3 exists  ord_p(10)")
        for p in [q for q in range(5, 140) if isp(q)]:
            r = [b for b in range(p) if (b*b+b+1) % p == 0]
            print(f"{p:4d}   {p%3}    {str(r):12s} {str(bool(r)):5s}"
                  f"       {order(10,p) if p not in (2,5) else '-'}")
        print("\n  every p == 1 mod 3 has mu_3. Only p = 37 has ord_p(10) = 3.")
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
