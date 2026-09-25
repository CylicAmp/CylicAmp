"""n = m * q1 * q2 * q3 ... with m 43-smooth and r large primes (r >= 3).
Divisors are divs(m) times every subset product of the q's: 2^r sorted
streams merged lazily. Reachability prune first -- if the squares of ALL
divisors below sqrt(n) do not reach n, the merge is never started."""
import sys, time, itertools, heapq
from sympy import primerange, factorint

SMALL=[2,3,5,7,11,13,17,19,23,29,31,37,41,43]

def smooth(M):
    out=[1]
    for p in SMALL:
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

def subset_products(Q):
    out=[1]
    for q in Q: out += [x*q for x in out]
    return sorted(out)

def check(A, m, Q):
    n=m
    for q in Q: n*=q
    root=int(n**0.5)
    mult=subset_products(Q)
    tot=0
    for c in mult:
        if c>root: continue
        for a in A:
            v=c*a
            if v>root: break
            tot+=v*v
    if tot<n: return None
    streams=[[c*a for a in A] for c in mult]
    s=0;k=0
    for d in heapq.merge(*streams):
        s+=d*d;k+=1
        if s==n: return k
        if s>n: return None
    return None

def run(M, QMAX, r):
    t=time.time(); ms=smooth(M); qs=list(primerange(47,QMAX+1))
    hits=[]; tried=0; pruned=0
    for m in ms:
        A=divs_of(m)
        for Q in itertools.combinations(qs, r):
            if Q[0]>m: break
            tried+=1
            res=check(A,m,list(Q))
            if res: hits.append((m*Q[0]*Q[1]*Q[2] if r==3 else None, res, m, Q))
    return sorted(set(hits)), tried, time.time()-t

if __name__=="__main__":
    M,Q,r=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
    h,tried,el=run(M,Q,r)
    print(f"n = m * {r} large primes,  m smooth <= {M}, primes 47..{Q}")
    for n,k,m,qq in h: print(f"   n = {n}  k={k}  m={m}  Q={qq}")
    print(f"   {len(h)} solutions from {tried} combinations  ({el:.0f}s)")
