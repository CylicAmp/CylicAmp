"""Directed supply cycles among primes >= T: x -> y when y | sigma_2(x^e).
Every member's unreachable large primes are reachable from such a cycle.
Enumerate all cycles with prod x^e <= B, from the smallest node q < B^(1/3)
(length-2 cycles with both exponents 1 are Vieta/Fibonacci, handled apart)."""
import sys, time
from math import isqrt
from functools import lru_cache
from sympy import primerange, factorint
T=250; B=int(float(sys.argv[1]))//60; QMAX=int(sys.argv[2]) if len(sys.argv)>2 else None
LMAX=int(sys.argv[3]) if len(sys.argv)>3 else 7
def icbrt(n):
    x=int(round(n**(1/3)))
    while x**3>n: x-=1
    while (x+1)**3<=n: x+=1
    return x
@lru_cache(None)
def S(x,e): return (x**(2*(e+1))-1)//(x*x-1)
@lru_cache(None)
def F(x,e): return tuple(sorted(factorint(S(x,e))))
cycles=set(); t0=time.time(); nodes=0
def dfs(q,path,prod):
    global nodes
    x,e=path[-1]; nodes+=1
    if len(path)>=2 and S(x,e)%q==0:            # close back to q
        cycles.add(tuple(path))
    if len(path)==LMAX: return
    for y in F(x,e):
        if y<=q or any(y==a for a,_ in path): continue
        f=1; p=y
        while prod*p<=B:
            dfs(q,path+[(y,f)],prod*p)
            f+=1; p*=y
top=QMAX or icbrt(B)
for q in primerange(T, top+1):
    e=1; p=q
    while p*q<=B:                               # room for at least one larger node
        dfs(q,[(q,e)],p); e+=1; p*=q
# length-2, exponents 1: q^2+r^2+1 = 3qr -> consecutive odd-index Fibonacci
a,b=1,2
fib2=[]
while a*b<=B:
    from sympy import isprime
    if a>=T and isprime(a) and isprime(b): fib2.append(((a,1),(b,1)))
    a,b=b,3*b-a
print(f"B={B:.3e} q<={top}: nodes {nodes}, cycles {len(cycles)}, Fibonacci 2-cycles >= {T}: {fib2}  ({time.time()-t0:.0f}s)")
import json; json.dump(sorted(cycles),open(f"cycles_{sys.argv[1]}.json","w"))
