"""General divisor-shape solver: pin each prime by the divisibility it forces."""
import math,re,sys
from sympy import primerange, factorint
SYM="pqrs"
def parse(tok):
    """token -> exponent dict over p,q,r,s"""
    if tok=="1": return {}
    e={}
    for m in re.finditer(r"([pqrs])(?:\^(\d+))?", tok):
        e[m.group(1)]=e.get(m.group(1),0)+int(m.group(2) or 1)
    if not e: raise ValueError(tok)
    return e
def val(e,vals):
    v=1
    for s,k in e.items(): v*=vals[s]**k
    return v
def verify(n,v,primes):
    if any(n%x for x in v): return False
    L=v[-1]; c=n; exps={}
    for pr in primes:
        k=0
        while c%pr==0: c//=pr; k+=1
        exps[pr]=k
    small={1}
    for pr,k in exps.items():
        small={d*pr**j for d in small for j in range(k+1) if d*pr**j<=L}
    if c>1:
        lim=min(L,math.isqrt(c)); d=2
        while d<=lim:
            if c%d==0: return False
            d+=1 if d==2 else 2
        if c<=L: return False
    K=len(v)
    return sorted(small)[:K]==v and len([x for x in small if x<=L])==K
def solve(shape, bounds, cap=10**15):
    toks=[parse(t) for t in shape.split()]
    used=[s for s in SYM if any(s in e for e in toks)]
    K=len(toks); hits=[]; cand=0; skip=0; nmax=0
    PRS={s:[x for x in primerange(3,bounds[s])] for s in used}
    def rec(i, vals):
        nonlocal cand,skip,nmax
        if i==len(used):
            vv=[val(e,vals) for e in toks]
            if sorted(vv)!=vv or len(set(vv))!=K: return
            n=sum(x*x for x in vv)
            if any(n%vals[s] for s in used): return
            cand+=1; nmax=max(nmax,n)
            if verify(n,vv,[vals[s] for s in used]): hits.append((dict(vals),n))
            return
        s=used[i]
        if i < len(used)-1:
            # NOT the last prime: it cannot be pinned, because the condition
            # s | n involves tokens carrying the primes not yet chosen.
            lo = vals[used[i-1]] if i else 0
            for x in PRS[s]:
                if x>lo: rec(i+1, {**vals, s:x})
        else:
            # the LAST prime CAN be pinned: every token free of it uses only
            # primes already fixed, so C is a definite integer.
            C=sum(val(e,{**vals,s:0})**2 for e in toks if s not in e)
            if C<=1 or C>cap: skip+=1; return
            prev=vals[used[i-1]] if i else 0
            for x in sorted(factorint(C)):
                if x>prev: rec(i+1, {**vals, s:x})
    rec(0,{})
    return cand,skip,nmax,hits
if __name__=="__main__":
    sh=sys.argv[1]
    b={"p":int(sys.argv[2]),"q":int(sys.argv[3]),"r":int(sys.argv[3]),"s":int(sys.argv[3])}
    c,sk,nm,h=solve(sh,b)
    print("%-32s cand %-7d skip %-5d n<=%.1e  %s"%(sh,c,sk,nm,("HIT %s"%h) if h else "EMPTY"))
