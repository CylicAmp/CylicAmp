"""Uncapped, any exponent, at most two large primes (>= T). No per-core
enumeration: every large prime is read off a sigma_2 factorisation, except
mutual pairs (neither divides sigma_2(core)), which depend only on the
pair and are precomputed once."""
import sys, time
from math import isqrt
from sympy import primerange, isprime, factorint
from collections import Counter
from functools import lru_cache

@lru_cache(None)
def fac(x): return dict(factorint(x))
def s2pe(q,e): return (q**(2*(e+1))-1)//(q*q-1)

def run(M,T,CMIN=60):
    small=list(primerange(2,T))
    tail=[1.0]*(len(small)+1)
    tail[-1]=(1-T**-2)**-2*(1+1e-9)   # two primes >= T lift sigma_2/m^2 by < this
    for i in range(len(small)-1,-1,-1): tail[i]=tail[i+1]/(1-small[i]**-2)
    # mutual pairs: q2^e2 | s2(q1^e1) and q1^e1 | s2(q2^e2)
    mutual=[]; B=M//CMIN
    for q1 in primerange(T, isqrt(B)+2):
        e1=1; p1=q1
        while p1*q1<=B:
            S1=s2pe(q1,e1)
            for q2,v2 in fac(S1).items():
                if q2<=q1 or q2<T: continue
                e2=1; p2=q2
                while e2<=v2 and p1*p2<=B:
                    if s2pe(q2,e2)%p1==0: mutual.append((p1*p2, s2pe(q1,e1)*s2pe(q2,e2)))
                    e2+=1; p2*=q2
            e1+=1; p1*=q1
    hits=set(); nodes=0
    def check(m,s2):
        if 2*s2>3*m*m and s2%m==0:
            q=s2//m-m
            if q>m//2 and isprime(q): hits.add((m,q))
    comp={}
    def big_ext(c,s2,comps):
        F=Counter()
        for k in comps: F.update(comp[k])
        L=[(q,v) for q,v in F.items() if q>=T]
        for q,v in L:                                   # one large prime
            pe=1
            for e in range(1,v+1):
                pe*=q
                if c*pe>M: break
                check(c*pe, s2*s2pe(q,e))
        for qa,va in L:                                  # two, qa read off core
            pa=1
            for ea in range(1,va+1):
                pa*=qa
                if c*pa*T>M: break
                Sa=s2pe(qa,ea); F2=F.copy(); F2.update(fac(Sa))
                for qb,vb in F2.items():
                    if qb<T or qb==qa: continue
                    pb=1
                    for eb in range(1,vb+1):
                        pb*=qb
                        if c*pa*pb>M: break
                        check(c*pa*pb, s2*Sa*s2pe(qb,eb))
        for mm,ss in mutual:                             # two, neither off core
            if c*mm<=M: check(c*mm, s2*ss)
    def dfs(j,c,s2,comps):
        nonlocal nodes; nodes+=1
        check(c,s2)
        r=s2/(c*c)
        if r*tail[-1]>=1.5: big_ext(c,s2,comps)
        for jj in range(j,len(small)):
            p=small[jj]
            if c*p>M or r*tail[jj]<1.5: break
            pe=1; sp=1; e=0
            while True:
                pe*=p; e+=1
                if c*pe>M: break
                sp+=pe*pe
                if (p,e) not in comp: comp[(p,e)]=fac(sp)
                dfs(jj+1,c*pe,s2*sp,comps+((p,e),))
    dfs(0,1,1,())
    return sorted(hits),nodes,len(mutual)

if __name__=="__main__":
    M=int(float(sys.argv[1])); T=int(sys.argv[2]); t=time.time()
    h,nodes,nm=run(M,T)
    c=Counter()
    for m,q in h:
        tau=1
        for e in factorint(m).values(): tau*=e+1
        c[tau]+=1
    print(f"m<={M:.0e} T={T}: {nodes} nodes, {nm} mutual pairs, {len(h)} members, {time.time()-t:.0f}s")
    print(" tau:",dict(sorted(c.items())))
    open(f"full2_{sys.argv[1]}.txt","w").write("\n".join(f"{m} {q}" for m,q in h)+"\n")
