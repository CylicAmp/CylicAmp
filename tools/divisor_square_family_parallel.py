"""fam_full2 split into independent subtrees rooted at 2^a * 3^b, run on
all cores. Every member has 2 | m and 3 | m (without 2 the ceiling on
sigma_2/m^2 is 1.234, without 3 it is 1.462, both below 3/2), so these
roots cover the whole family."""
import sys, time
from multiprocessing import Pool
import divisor_square_family_uncapped as F
from sympy import primerange, isprime, factorint
from collections import Counter

M=int(float(sys.argv[1])); T=int(sys.argv[2])
small=list(primerange(2,T))
tail=[1.0]*(len(small)+1)
tail[-1]=(1-T**-2)**-2*(1+1e-9)
for i in range(len(small)-1,-1,-1): tail[i]=tail[i+1]/(1-small[i]**-2)

def work(root):
    a,b=root
    hits=set(); comp={}; nodes=[0]
    s2pe=F.s2pe; fac=F.fac
    def check(m,s2):
        if 2*s2>3*m*m and s2%m==0:
            q=s2//m-m
            if q>m//2 and isprime(q): hits.add((m,q))
    def big_ext(c,s2,comps):
        C=Counter()
        for k in comps: C.update(comp[k])
        L=[(q,v) for q,v in C.items() if q>=T]
        for q,v in L:
            pe=1
            for e in range(1,v+1):
                pe*=q
                if c*pe>M: break
                check(c*pe,s2*s2pe(q,e))
        for qa,va in L:
            pa=1
            for ea in range(1,va+1):
                pa*=qa
                if c*pa*T>M: break
                Sa=s2pe(qa,ea); C2=C.copy(); C2.update(fac(Sa))
                for qb,vb in C2.items():
                    if qb<T or qb==qa: continue
                    pb=1
                    for eb in range(1,vb+1):
                        pb*=qb
                        if c*pa*pb>M: break
                        check(c*pa*pb,s2*Sa*s2pe(qb,eb))
    def dfs(j,c,s2,comps):
        nodes[0]+=1
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
    c=2**a*3**b; s2=s2pe(2,a)*s2pe(3,b)
    comp[(2,a)]=fac(s2pe(2,a)); comp[(3,b)]=fac(s2pe(3,b))
    if s2/(c*c)*tail[2]>=1.5:
        dfs(2,c,s2,((2,a),(3,b)))
    return hits,nodes[0]

if __name__=="__main__":
    t=time.time()
    roots=[(a,b) for a in range(1,60) for b in range(1,40) if 2**a*3**b<=M]
    roots.sort(key=lambda r:2**r[0]*3**r[1])      # biggest subtrees first
    allh=set(); tot=0
    with Pool(4) as pool:
        for h,n in pool.imap_unordered(work,roots,chunksize=1):
            allh|=h; tot+=n
    c=Counter()
    for m,q in allh:
        tau=1
        for e in factorint(m).values(): tau*=e+1
        c[tau]+=1
    print(f"m<={M:.0e} T={T}: {len(roots)} roots, {tot} nodes, {len(allh)} members, {time.time()-t:.0f}s")
    print(" tau:",dict(sorted(c.items())))
    open(f"par_{sys.argv[1]}.txt","w").write("\n".join(f"{m} {q}" for m,q in sorted(allh))+"\n")
