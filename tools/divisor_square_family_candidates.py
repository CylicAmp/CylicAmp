"""Family search in resumable chunks. Nodes with c < C0 are expanded in the
parent (checked + read-off there); every node with c >= C0 becomes an
independent item. Items run on 4 cores in order; progress is saved after
each result so a chunk can stop at a time budget and resume exactly."""
import sys, time, json, os
from multiprocessing import Pool
from collections import Counter
from sympy import primerange, isprime, factorint
from functools import lru_cache

M=int(float(sys.argv[1])); BUDGET=float(sys.argv[2]); T=250; DEPTH=5; C0=10**5
STATE=sys.argv[3]
from math import log
small=list(primerange(2,T))
tail=[1.0]*(len(small)+1)
tail[-1]=(1-T**-2)**-DEPTH*(1+1e-9)
for i in range(len(small)-1,-1,-1): tail[i]=tail[i+1]/(1-small[i]**-2)

@lru_cache(None)
def s2pe(q,e): return (q**(2*(e+1))-1)//(q*q-1)
@lru_cache(None)
def fac(x): return dict(factorint(x))

def check(m,s2,hits):
    if 2*s2>3*m*m and s2%m==0:
        q=s2//m-m
        if q>m//2 and q%2 and q%3: hits.add((m,q,int(isprime(q))))

@lru_cache(None)
def large(q,e): return frozenset(a for a in fac(s2pe(q,e)) if a>=T)

def big_ext(c,s2,L,hits):
    """L: primes >= T dividing sigma_2 of the current part. Only these can be
    read off; multiplicities are never used, so a set suffices."""
    seen=set()
    def ext(depth,m,s2m,L,chosen):
        if depth==DEPTH: return
        for q in L:
            if any(q==a for a,_ in chosen): continue
            pe=1; e=0
            while True:
                pe*=q; e+=1
                if m*pe>M: break
                key=chosen|{(q,e)}
                if key in seen: continue
                seen.add(key)
                S=s2pe(q,e); m2=m*pe; s22=s2m*S
                check(m2,s22,hits)
                ext(depth+1,m2,s22,L|large(q,e),frozenset(key))
    ext(0,c,s2,L,frozenset())

def node(j,c,s2,comps,hits,L=None):
    check(c,s2,hits)
    if s2/(c*c)*tail[-1]>=1.5:
        if L is None: L=frozenset().union(*(large(p,e) for p,e in comps))
        if L: big_ext(c,s2,L,hits)

def v(n,p):
    k=0
    while n%p==0: n//=p; k+=1
    return k
def feasible(jn,c,comps):
    """v2(m) must be supplied by v2(e+1) over odd p^e || m; v3(m) by v3(e+1)
    over p != 3. Future primes are >= p0; a unit of 2-supply costs >= p0,
    a unit of 3-supply needs e = 2 mod 3 so costs >= p0^2."""
    a=b=0; s2=s3=0
    for p,e in comps:
        if p==2: a=e
        else: s2+=v(e+1,2)
        if p==3: b=e
        else: s3+=v(e+1,3)
    p0=small[jn] if jn<len(small) else T
    R=M//c
    f2=int(log(R)/log(p0)+1e-9) if R>=p0 else 0
    return s2+f2>=a and s3+f2//2>=b

def children(j,c,s2,comps):
    r=s2/(c*c)
    for jj in range(j,len(small)):
        p=small[jj]
        if c*p>M or r*tail[jj]<1.5: break
        pe=1; e=0
        while True:
            pe*=p; e+=1
            if c*pe>M: break
            nc=comps+((p,e),)
            if feasible(jj+1,c*pe,nc): yield (jj+1,c*pe,s2*s2pe(p,e),nc)

def subtree(item):
    hits=set(); n=[0]
    def dfs(j,c,s2,comps,L):
        n[0]+=1; node(j,c,s2,comps,hits,L)
        for ch in children(j,c,s2,comps): dfs(*ch,L|large(*ch[3][-1]))
    dfs(*item,frozenset().union(*(large(p,e) for p,e in item[3])))
    return sorted(hits), n[0]

def build():
    items=[]; top=[]
    stack=[]
    for a in range(1,60):
        for b in range(1,40):
            c=2**a*3**b
            if c>M: break
            s2=s2pe(2,a)*s2pe(3,b)
            if s2/(c*c)*tail[2]<1.5: continue
            if not feasible(2,c,((2,a),(3,b))): continue
            stack.append((2,c,s2,((2,a),(3,b))))
    while stack:
        it=stack.pop()
        if it[1]>=C0: items.append(it); continue
        top.append(it)
        stack.extend(children(*it))
    items.sort(key=lambda x:(x[1],x[3]))
    return top,items

if __name__=="__main__":
    t0=time.time()
    top,items=build()
    st=json.load(open(STATE)) if os.path.exists(STATE) else {"next":0,"hits":[],"nodes":0,"top_done":False}
    hits=set(map(tuple,st["hits"]))
    if not st["top_done"]:
        for it in top:
            node(*it,hits); st["nodes"]+=1
        st["top_done"]=True
    i=st["next"]
    with Pool(4) as pool:
        for h,n in pool.imap(subtree, items[i:], chunksize=1):
            hits.update(map(tuple,h)); st["nodes"]+=n; i+=1
            if time.time()-t0>BUDGET: break
        pool.terminate()
    st["next"]=i; st["hits"]=sorted(hits)
    json.dump(st,open(STATE,"w"))
    print(f"M={M:.0e}: items {i}/{len(items)} done ({100*i/len(items):.1f}%), top nodes {len(top)}, "
          f"nodes so far {st['nodes']}, members so far {len(hits)}, this chunk {time.time()-t0:.0f}s")
