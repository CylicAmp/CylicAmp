from sympy import primerange, factorint, isprime
from sympy.ntheory import sqrt_mod
def s2(x): return x**4+x*x+1
hits=[]; tried=0; Q=10**6
for q in primerange(7,Q):
    for r in factorint(s2(q)):
        if r<=q: continue
        if r in (7,41):
            ps=[p for p in primerange(5,q)]
        else:
            t=sqrt_mod(-3%r,r,all_roots=True) or []
            inv2=pow(2,-1,r)
            ps=sorted({x for u in t for x in ((-1+u)*inv2%r,(1+u)*inv2%r)})
            ps=[x for x in ps if 5<=x<q and isprime(x)]
        for p in ps:
            tried+=1; s=p*q*r
            if (1435*s2(p)*s2(q)*s2(r))%(s*s)==0: hits.append((p,q,r))
print(f"q < {Q}: triples meeting the r-condition: {tried}; full solutions: {hits}")
