"""Self-supplying clusters of primes >= T with product <= B, sizes 2..5, any
exponent. The largest member q^e must divide sigma_2 of the others, so the
smaller members are enumerated and the largest is READ OFF their pool."""
import sys, time
from math import isqrt
from sympy import primerange, factorint
from functools import lru_cache
T=250; B=int(float(sys.argv[1]))//60; SMAX=int(sys.argv[2])
@lru_cache(None)
def S(q,e): return (q**(2*(e+1))-1)//(q*q-1)
@lru_cache(None)
def F(q,e): return factorint(S(q,e))
def v(n,p):
    c=0
    while n%p==0: n//=p; c+=1
    return c
PR=list(primerange(T, isqrt(B)+2))
found=[]; scanned=[0]*(SMAX+1)
def rec(start,mem,prod,pool):
    k=len(mem)
    if k>=1:                                    # try closing with a read-off largest
        qmax=mem[-1][0]
        for q,vq in pool.items():
            if q<=qmax: continue
            for e in range(1,vq+1):
                p=q**e
                if prod*p>B: break
                full=mem+[(q,e)]
                if all(v(eval_prod(full,i),a)>=b for i,(a,b) in enumerate(full)):
                    found.append(tuple(full))
    if k+1>=SMAX: return
    for i in range(start,len(PR)):
        q=PR[i]
        if prod*q*q>B: break                    # room for this and ONE larger member
        e=1; p=q
        while prod*p*q<=B:
            scanned[k+1]+=1
            np_=dict(pool)
            for a,x in F(q,e).items(): np_[a]=np_.get(a,0)+x
            rec(i+1,mem+[(q,e)],prod*p,np_)
            e+=1; p*=q
def eval_prod(full,skip):
    r=1
    for j,(a,b) in enumerate(full):
        if j!=skip: r*=S(a,b)
    return r
t=time.time()
rec(0,[],1,{})
print(f"B = {B:.3e}, sizes 2..{SMAX}: prefix tuples scanned by size {scanned[1:]}")
print(f"clusters found: {found}  ({time.time()-t:.0f}s)")
