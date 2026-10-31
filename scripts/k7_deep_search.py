import random, sys
from math import gcd, isqrt
def mr(n):
    if n<2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%p==0: return n==p
    d=n-1;s=0
    while d%2==0: d//=2;s+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True
def rho(n):
    if n%2==0: return 2
    while True:
        x=random.randrange(2,n); y=x; c=random.randrange(1,n); d=1
        while d==1:
            x=(x*x+c)%n; y=(y*y+c)%n; y=(y*y+c)%n
            d=gcd(abs(x-y),n)
        if d!=n: return d
def factor(n, out=None):
    if out is None: out=set()
    if n==1: return out
    if mr(n): out.add(n); return out
    d=rho(n)
    factor(d,out); factor(n//d,out)
    return out
def lcm_of(vs):
    o=1
    for x in vs: o=o*x//gcd(o,x)
    return o
def smallest(n,k):
    d=[]
    for i in range(1,isqrt(n)+1):
        if n%i==0: d.append(i); d.append(n//i)
    return sorted(set(d))[:k]
def primes_upto(n):
    s=bytearray([1])*(n+1); s[0:2]=b"\x00\x00"
    for i in range(2,isqrt(n)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(n+1) if s[i]]

VMAX=int(sys.argv[1]) if len(sys.argv)>1 else 30000
P=[p for p in primes_upto(VMAX) if p>=3]
JOBS=[
 ("{1,v,u,v^2,uv,v^3,v^4}", lambda v,u:[1,v,u,v*v,u*v,v**3,v**4],
   lambda v:[v**4+v**3+v*v+v+1, v**4-v**3+v*v-v+1]),
 ("{1,v,u,v^2,uv,v^3,uv^2}", lambda v,u:[1,v,u,v*v,u*v,v**3,u*v*v],
   lambda v:[1+v*v, 1+v**4]),
 ("{1,v,u,v^2,uv,u^2,v^3}", lambda v,u:[1,v,u,v*v,u*v,u*u,v**3],
   lambda v:[1+v*v, 1+v**4]),
 ("{1,v,u,v^2,uv,u^2,uv^2}", lambda v,u:[1,v,u,v*v,u*v,u*u,u*v*v],
   lambda v:[v*v+v+1, v*v-v+1]),
]
print(f"DEEP EXHAUSTIVE SEARCH, two-prime shapes, v prime up to {VMAX:,}")
print("Pollard rho factoring of the cyclotomic pieces; u ranges over their")
print("prime factors, which is the complete candidate set by the mod-p rule.\n")
for name,mk,fac in JOBS:
    hits=[]; cand=0
    for v in P:
        us=set()
        for part in fac(v):
            us |= factor(part)
        for u in us:
            if u==v or u<3: continue
            V=mk(v,u)
            if len(set(V))<7: continue
            cand+=1
            n=sum(d*d for d in V)
            if n%lcm_of(V): continue
            if sorted(V)!=smallest(n,7): continue
            hits.append((v,u,n))
    print(f"  {name:<30} {cand:>8} candidates   {hits if hits else 'NONE'}")
print(f"\n  v primes tested: {len(P):,}")
