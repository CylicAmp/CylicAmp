"""CASE C, fast: n = m*q1*q2, m 43-smooth, 47 <= q1 <= q2 prime.
Manual 4-pointer merge over A, q1A, q2A, q1q2A with early exit, plus a
reachability prune: the prefix can only use divisors <= sqrt(n), so if the
sum of squares of ALL divisors <= sqrt(n) is below n, skip the triple."""
import sys, time
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

def hit(A, m, q1, q2):
    n=m*q1*q2; root=int(n**0.5)
    la=len(A)
    # reachability: sum of squares of all divisors <= sqrt(n)
    tot=0
    for a in A:
        if a<=root: tot+=a*a
        if q1*a<=root: tot+=(q1*a)**2
        if q2*a<=root: tot+=(q2*a)**2
        if q1*q2*a<=root: tot+=(q1*q2*a)**2
    if tot<n: return None
    i=j=l=t=0; s=0; k=0
    while True:
        c=[]
        if i<la: c.append((A[i],0))
        if j<la: c.append((q1*A[j],1))
        if l<la: c.append((q2*A[l],2))
        if t<la: c.append((q1*q2*A[t],3))
        if not c: return None
        d,w=min(c)
        if w==0: i+=1
        elif w==1: j+=1
        elif w==2: l+=1
        else: t+=1
        s+=d*d; k+=1
        if s==n: return k
        if s>n: return None

def run(M,QMAX):
    t0=time.time(); ms=smooth(M); qs=list(primerange(47,QMAX+1))
    hits=[]; trip=0
    for m in ms:
        A=divs_of(m)
        for a,q1 in enumerate(qs):
            if q1>m: break
            for q2 in qs[a:]:
                trip+=1
                r=hit(A,m,q1,q2)
                if r: hits.append((m*q1*q2,r,m,q1,q2))
    return sorted(set(hits)), trip, time.time()-t0

if __name__=="__main__":
    M,Q=int(sys.argv[1]),int(sys.argv[2])
    h,trip,el=run(M,Q)
    print(f"CASE C  m smooth <= {M}, primes 47..{Q}")
    for n,k,m,q1,q2 in h: print(f"   n = {n:>20}  k={k:<5} m={m} q1={q1} q2={q2}")
    print(f"   {len(h)} solutions from {trip} triples  ({el:.0f}s)")
