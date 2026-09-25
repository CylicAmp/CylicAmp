"""n = m*q, q prime > 43 so q does not divide the smooth m.
Divisors of n are divs(m) merged with q*divs(m). Merge lazily and stop the
moment the running sum passes n -- most pairs die in a handful of steps."""
import sys, time
from sympy import primerange, factorint

def smooth(primes, M):
    out=[1]
    for p in primes:
        new=[]
        for m in out:
            v=m
            while v<=M: new.append(v); v*=p
        out=new
    return sorted(x for x in out if x>1)

def divs_of(m):
    d=[1]
    for p,e in factorint(m).items(): d=[x*p**i for x in d for i in range(e+1)]
    return sorted(d)

def test(A, m, q):
    """A = sorted divisors of m; lazily merge A and q*A, prefix-sum to n=m*q"""
    n=m*q; s=0; i=j=0; k=0; la=len(A); dk=0
    while i<la or j<la:
        if j>=la or (i<la and A[i] <= q*A[j]):
            d=A[i]; i+=1
        else:
            d=q*A[j]; j+=1
        s+=d*d; k+=1; dk=d
        if s==n: return k, dk
        if s>n: return None
    return None

def run(M, QMAX, primes, verbose=True):
    t=time.time(); ms=smooth(primes,M); qs=[q for q in primerange(47,QMAX+1)]
    if verbose: print(f"  {len(ms)} smooth m <= {M}, {len(qs)} primes 47..{QMAX}", flush=True)
    hits=[]; pairs=0
    for m in ms:
        A=divs_of(m)
        for q in qs:
            if q>m: break
            pairs+=1
            r=test(A,m,q)
            if r:
                k,dk=r
                hits.append((m*q,k,m,q,q<=dk))
    if verbose: print(f"  {pairs} pairs  ({time.time()-t:.0f}s)")
    return sorted(set(hits))

if __name__=="__main__":
    M,QMAX=int(sys.argv[1]),int(sys.argv[2])
    P=[2,3,5,7,11,13,17,19,23,29,31,37,41,43]
    for n,k,m,q,inside in run(M,QMAX,P):
        print(f"  n={n:>22} k={k:<5} m={m:<14} q={q:<9} q inside prefix: {inside}")
