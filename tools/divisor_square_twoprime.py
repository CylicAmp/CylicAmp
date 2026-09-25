"""r=2 pushed: n = m*q1*q2, m 43-smooth, 47 <= q1 <= q2 prime.

The reachability prune used to scan all of divs(m) four times per triple.
Precomputing prefix sums of a^2 turns each of the four terms into one
binary search, so the prune costs O(log|A|) instead of O(|A|).
Only triples that survive it are merged."""
import sys, time
from bisect import bisect_right
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

def run(M,QMAX,verbose=True):
    t0=time.time(); ms=smooth(M); qs=list(primerange(47,QMAX+1))
    hits=[]; trip=0; merged=0
    for m in ms:
        A=divs_of(m); la=len(A)
        P=[0]*(la+1)                       # P[i] = sum of squares of A[:i]
        for i,a in enumerate(A): P[i+1]=P[i]+a*a
        def cap(lim):                      # sum of a^2 over a <= lim
            return P[bisect_right(A,lim)]
        for ai,q1 in enumerate(qs):
            if q1>m: break
            for q2 in qs[ai:]:
                trip+=1
                n=m*q1*q2; R=int(n**0.5)
                tot = cap(R) + q1*q1*cap(R//q1) + q2*q2*cap(R//q2)
                if q1*q2<=R: tot += (q1*q2)**2 * cap(R//(q1*q2))
                if tot<n: continue
                merged+=1
                i=j=l=t=0; s=0; k=0; ok=None
                while True:
                    best=None
                    if i<la: best=(A[i],0)
                    if j<la:
                        v=q1*A[j]
                        if best is None or v<best[0]: best=(v,1)
                    if l<la:
                        v=q2*A[l]
                        if best is None or v<best[0]: best=(v,2)
                    if t<la:
                        v=q1*q2*A[t]
                        if best is None or v<best[0]: best=(v,3)
                    if best is None: break
                    d,w=best
                    if w==0: i+=1
                    elif w==1: j+=1
                    elif w==2: l+=1
                    else: t+=1
                    s+=d*d; k+=1
                    if s==n: ok=k; break
                    if s>n: break
                if ok: hits.append((n,ok,m,q1,q2))
    return sorted(set(hits)), trip, merged, time.time()-t0

if __name__=="__main__":
    M,Q=int(sys.argv[1]),int(sys.argv[2])
    h,trip,mg,el=run(M,Q)
    print(f"r=2  m smooth <= {M}, primes 47..{Q}")
    for n,k,m,q1,q2 in h: print(f"   n={n}  k={k}  m={m} q1={q1} q2={q2}")
    print(f"   {len(h)} solutions | {trip} triples, {mg} survived the prune ({100*mg/max(trip,1):.1f}%) | {el:.0f}s")
