"""Proper-divisor family, searched by DFS over factorisations instead of a sieve.
m is built prime by prime in increasing order. A branch is pruned when even
adding every remaining prime at unbounded exponent cannot lift
sigma_2(m)/m^2 above 3/2. Exact integer arithmetic throughout."""
import sys, time
from sympy import primerange, isprime
from collections import Counter

def run(M, P):
    ps=list(primerange(2,P))
    tail=[1.0]*(len(ps)+1)
    for i in range(len(ps)-1,-1,-1):
        tail[i]=tail[i+1]/(1-ps[i]**-2)
    tail=[t*(1+4.0/P) for t in tail]       # safe over-estimate for primes >= P
    hits=[]; nodes=0
    def check(m,s2,f):
        if 2*s2>3*m*m and s2%m==0:
            q=s2//m-m
            if q>m//2 and isprime(q): hits.append((m,q,dict(f)))
    def dfs(i,m,s2,f):
        nonlocal nodes
        nodes+=1
        check(m,s2,f)
        for j in range(i,len(ps)):
            p=ps[j]
            if m*p>M: break
            if (s2/(m*m))*tail[j]<1.5: break     # no prime >= p can rescue it
            pe=1; sp=1
            while True:
                pe*=p
                if m*pe>M: break
                sp+=pe*pe
                f[p]=f.get(p,0)+1
                dfs(j+1,m*pe,s2*sp,f)
            f.pop(p,None)
    dfs(0,1,1,{})
    return hits,nodes

if __name__=="__main__":
    M=int(float(sys.argv[1])); P=int(sys.argv[2]); t=time.time()
    h,nodes=run(M,P)
    print(f"m <= {M:.0e}, primes in m < {P}:  {nodes} nodes, {len(h)} members  ({time.time()-t:.0f}s)")
    for m,q,f in sorted(h):
        fs=" * ".join(f"{p}^{e}" if e>1 else str(p) for p,e in sorted(f.items()))
        tau=1
        for e in f.values(): tau*=e+1
        print(f"   m={m:<16} tau={tau:<6} p={q:<16} m = {fs}")
    c=Counter()
    for m,q,f in h:
        t2=1
        for e in f.values(): t2*=e+1
        c[t2]+=1
    print("tau distribution:", dict(sorted(c.items())))
