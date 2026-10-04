"""Proper-divisor family, fast. Small primes (< T) enumerated by DFS with the
exact ratio cut. Large primes (T <= q < P, exponent 1, at most two) are NOT
enumerated: a first-power prime q of m divides sigma_2(m/q), since
sigma_2(q) = 1 + q^2 = 1 (mod q). So q is read off the factors of sigma_2 of
the smaller part. A core can only take large primes if its own ratio is
already within a hair of 3/2, which kills almost every core."""
import sys, time
from sympy import primerange, isprime, factorint
from collections import Counter
from functools import lru_cache

@lru_cache(None)
def pfac(x): return tuple(sorted(factorint(x)))

def run(M,T,P):
    small=list(primerange(2,T)); big=list(primerange(T,P))
    big_tail=1.0
    for q in big: big_tail/= (1-q**-2)
    big_tail*=(1+4.0/P)
    tail=[big_tail]*(len(small)+1)
    for i in range(len(small)-1,-1,-1): tail[i]=tail[i+1]/(1-small[i]**-2)
    hits=set(); nodes=0
    def check(m,s2):
        if 2*s2>3*m*m and s2%m==0:
            q=s2//m-m
            if q>m//2 and isprime(q): hits.add((m,q))
    comp={}                                  # factor sets of sigma_2 components
    def dfs(j,c,s2,comps):
        nonlocal nodes; nodes+=1
        check(c,s2)
        r=s2/(c*c)
        if r*(1+T**-2)**2*1.0000001>=1.5:    # only near-threshold cores take big primes
            ps=set()
            for key in comps: ps.update(comp[key])
            for q in ps:                      # one big prime: q | sigma_2(core)
                if T<=q<P and c*q<=M: check(c*q, s2*(1+q*q))
            for q1 in big:                    # two big primes q1 < q2
                if c*q1*q1>M: break
                s1=s2*(1+q1*q1)
                cand=set(ps)|set(pfac(1+q1*q1))
                for q2 in cand:
                    if q1<q2<P and q2>=T and c*q1*q2<=M:
                        check(c*q1*q2, s1*(1+q2*q2))
        for jj in range(j,len(small)):
            p=small[jj]
            if c*p>M: break
            if r*tail[jj]<1.5: break
            pe=1; sp=1; e=0
            while True:
                pe*=p; e+=1
                if c*pe>M: break
                sp+=pe*pe
                key=(p,e)
                if key not in comp: comp[key]=pfac(sp)
                dfs(jj+1,c*pe,s2*sp,comps+(key,))
    dfs(0,1,1,())
    return sorted(hits),nodes

if __name__=="__main__":
    M=int(float(sys.argv[1])); T=int(sys.argv[2]); P=int(sys.argv[3]); t=time.time()
    h,nodes=run(M,T,P)
    print(f"m <= {M:.0e}  small primes < {T}  big primes [{T},{P}) exp 1, <=2 of them")
    print(f"   {nodes} nodes, {len(h)} members  ({time.time()-t:.0f}s)")
    c=Counter()
    for m,q in h:
        tau=1
        for e in factorint(m).values(): tau*=e+1
        c[tau]+=1
        print(f"   m={m:<16} tau={tau:<6} p={q}")
    print("   tau distribution:", dict(sorted(c.items())))
