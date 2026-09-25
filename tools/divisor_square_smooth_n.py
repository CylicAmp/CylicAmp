"""Two cases the earlier runs did not cover.

CASE A  n fully 43-smooth. This is exactly the q <= 43 gap: if the extra
        prime is small, n has no large prime at all. Enumerate smooth n
        directly and test the prefix.

CASE C  n = m * q1 * q2 with m smooth and q1 <= q2 primes > 43 (q1 == q2
        allowed, covering a large prime squared). Divisors of n are the
        four-way merge of A, q1*A, q2*A, q1*q2*A with A = divs(m).
"""
import sys, time, heapq
from sympy import primerange, factorint

SMALL=[2,3,5,7,11,13,17,19,23,29,31,37,41,43]

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

def prefix_hit(D, n):
    s=0
    for k,d in enumerate(D,1):
        s+=d*d
        if s==n: return k
        if s>n: return None
    return None

def caseA(M):
    hits=[]
    for n in smooth(SMALL, M):
        k=prefix_hit(divs_of(n), n)
        if k: hits.append((n,k))
    return hits

def merged(lists):
    """lazy k-way merge of sorted lists"""
    return heapq.merge(*lists)

def caseC(M, QMAX):
    hits=[]; pairs=0
    ms=smooth(SMALL,M); qs=list(primerange(47,QMAX+1))
    for m in ms:
        A=divs_of(m)
        for i,q1 in enumerate(qs):
            if q1*q1>m*q1*qs[-1]: pass
            if q1>m: break
            for q2 in qs[i:]:
                n=m*q1*q2
                if q1>int(n**0.5): break
                pairs+=1
                if q1==q2:
                    L=[A,[q1*a for a in A],[q1*q1*a for a in A]]
                else:
                    L=[A,[q1*a for a in A],[q2*a for a in A],[q1*q2*a for a in A]]
                s=0; k=0; hit=None
                for d in merged(L):
                    s+=d*d; k+=1
                    if s==n: hit=k; break
                    if s>n: break
                if hit: hits.append((n,hit,m,q1,q2))
    return hits, pairs

if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="A":
        M=int(sys.argv[2]); t=time.time()
        r=caseA(M)
        print(f"CASE A: n fully 43-smooth, n <= {M}")
        for n,k in r: print(f"   n = {n:>18}  k = {k}")
        print(f"   {len(r)} solutions  ({time.time()-t:.0f}s)")
    else:
        M,Q=int(sys.argv[2]),int(sys.argv[3]); t=time.time()
        r,pairs=caseC(M,Q)
        print(f"CASE C: n = m*q1*q2, m smooth <= {M}, primes 47..{Q}")
        for n,k,m,q1,q2 in sorted(set(r)):
            print(f"   n = {n:>20}  k = {k:<5} m={m} q1={q1} q2={q2}")
        print(f"   {len(set(r))} solutions from {pairs} triples  ({time.time()-t:.0f}s)")
