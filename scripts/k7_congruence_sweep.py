#!/usr/bin/env python3
"""O(1)-per-v search for k=7's four two-prime Level-2 shapes.

For each shape, (L) on the v-part of lcm(V) gives a CONGRUENCE
    v^a | P(u)
and (M) on u gives a DIVISIBILITY
    u | Q(v),   Q = F1 * F2  with each Fi a cyclotomic-type factor.
u is prime, so u | F1 or u | F2.  Writing F = u*d:
  * if u < v^a, the congruence class of u mod v^a pins u to ONE value;
  * if u > F/v^a then d = F/u < v^a, and d = F * u^{-1} is pinned mod v^a,
    so d is ONE value too.
Either way O(1) candidates per v, with no factorisation of F at all.
"""
import sys
from sympy.ntheory.residue_ntheory import sqrt_mod
from math import gcd, isqrt

def sieve(N):
    b=bytearray([1])*(N+1); b[0]=b[1]=0
    for i in range(2,isqrt(N)+1):
        if b[i]: b[i*i::i]=bytearray(len(b[i*i::i]))
    return [i for i in range(3,N+1) if b[i]]

def isp(n):
    if n<2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%p==0: return n==p
    d=n-1; r=0
    while d%2==0: d//=2; r+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(r-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True

def lcm_of(vs):
    o=1
    for x in vs: o=o*x//gcd(o,x)
    return o

def smallest_divisors(n,k):
    d=[]
    for i in range(1,isqrt(n)+1):
        if n%i==0: d.append(i); d.append(n//i)
    return sorted(set(d))[:k]

def roots_quartic_mod_v(v):
    """Roots of x^4+x^2+1 = (x^2+x+1)(x^2-x+1) mod v, in O(1)."""
    out=set()
    w=sqrt_mod(-3, v, all_roots=True) or []
    inv2=pow(2,-1,v)
    for y in w:
        out.add((-1+y)*inv2 % v)      # x^2+x+1 = 0
        out.add(( 1+y)*inv2 % v)      # x^2-x+1 = 0
    return sorted(out)

def hensel(poly, dpoly, v, a, base):
    """Lift roots mod v to roots mod v^a.  O(1) per simple root."""
    rs=list(base)
    for k in range(2,a+1):
        mk=v**k; mk1=v**(k-1); new=[]
        for r in rs:
            d=dpoly(r)%v
            if d:
                inv=pow(d,-1,mk)
                new.append((r - poly(r)*inv) % mk)
            else:
                new += [(r+j*mk1)%mk for j in range(v)
                        if poly((r+j*mk1)%mk)%mk==0]
        rs=sorted(set(new))
    return rs

def roots_mod(poly, v, a, dpoly=None, base=None):
    if base is None:
        base=[x for x in range(v) if poly(x)%v==0]
    if a==1: return sorted(set(base))
    if dpoly is None:
        dpoly=lambda x: (poly(x+1)-poly(x-1))  # not used for our shapes
    return hensel(poly, dpoly, v, a, base)

SHAPES={}
# shape 1: {1,v,u,v^2,uv,v^3,v^4};  a=4; P(u)=u^2+1; Q=Phi5*Phi10
SHAPES[1]=dict(
    name="{1, v, u, v^2, uv, v^3, v^4}", a=4,
    P=lambda u: u*u+1,
    facs=lambda v: [v**4+v**3+v**2+v+1, v**4-v**3+v**2-v+1],
    elems=lambda v,u: [1,v,u,v*v,u*v,v**3,v**4],
    umin=lambda v: v*v)
# shape 2: {1,v,u,v^2,uv,v^3,uv^2}; a=3; P=u^2+1; Q=(1+v^2)(1+v^4)
SHAPES[2]=dict(
    name="{1, v, u, v^2, uv, v^3, uv^2}", a=3,
    P=lambda u: u*u+1,
    facs=lambda v: [v*v+1, v**4+1],
    elems=lambda v,u: [1,v,u,v*v,u*v,v**3,u*v*v],
    umin=lambda v: v)
# shape 3: {1,v,u,v^2,uv,u^2,v^3}; a=3; P depends on v; Q=(1+v^2)(1+v^4)
SHAPES[3]=dict(
    name="{1, v, u, v^2, uv, u^2, v^3}", a=3,
    P=None,
    facs=lambda v: [v*v+1, v**4+1],
    elems=lambda v,u: [1,v,u,v*v,u*v,u*u,v**3],
    umin=lambda v: v)
# shape 4: {1,v,u,v^2,uv,u^2,uv^2}; a=2; P=u^4+u^2+1; Q=(v^2+v+1)(v^2-v+1)
SHAPES[4]=dict(
    name="{1, v, u, v^2, uv, u^2, uv^2}", a=2,
    P=lambda u: u**4+u*u+1,
    facs=lambda v: [v*v+v+1, v*v-v+1],
    elems=lambda v,u: [1,v,u,v*v,u*v,u*u,u*v*v],
    umin=lambda v: v)

def verify(sh, v, u):
    """Full check: distinct, in-box forcing, lcm | n, prefix."""
    if u<2 or not isp(u) or u==v: return None
    V=sorted(set(sh['elems'](v,u)))
    if len(V)!=7: return None
    M=max(V)
    # in-box forced non-members, per shape
    forced={1:[u*v*v], 2:[u*v**3], 3:[u*u*v, u*v*v], 4:[u*u*v]}[sh['key']]
    if any(f<=M for f in forced): return None
    n=sum(d*d for d in V); L=lcm_of(V)
    if n%L: return None
    if smallest_divisors(n,7)!=V: return None
    return (v,u,n)

def run(key, VMAX, report=True):
    sh=SHAPES[key]; sh['key']=key; a=sh['a']
    hits=[]; cand=0; vok=0
    for v in sieve(VMAX):
        if key in (1,2):
            if v%4!=1: continue              # -1 must be a QR mod v
            rs=sqrt_mod(-1, v**a, all_roots=True)
            if not rs: continue
        elif key==4:
            if v!=3 and v%3!=1: continue     # -3 must be a QR mod v
            base=roots_quartic_mod_v(v)
            if not base: continue
            rs=roots_mod(lambda x: x**4+x*x+1, v, a,
                         dpoly=lambda x: 4*x**3+2*x, base=base)
        else:
            if v!=3 and v%3!=1: continue
            base=roots_quartic_mod_v(v)       # mod v the poly reduces to this
            if not base: continue
            P3=lambda x,v=v: x**4+x*x*v*v+x*x+v*v+1
            rs=roots_mod(P3, v, a,
                         dpoly=lambda x,v=v: 4*x**3+2*x*v*v+2*x, base=base)
        vok+=1; Mp=v**a
        for F in sh['facs'](v):
            for r in rs:
                if r==0: continue
                # case A: u < v^a, pinned to r itself
                if sh['umin'](v) < r < Mp and F % r == 0:
                    cand+=1
                    h=verify(sh,v,r)
                    if h: hits.append(h)
                # case B: d = F/u < v^a, pinned
                if gcd(r,Mp)!=1: continue
                d=(F % Mp) * pow(r,-1,Mp) % Mp
                if d and d<Mp and F % d == 0:
                    u=F//d
                    if u>sh['umin'](v):
                        cand+=1
                        h=verify(sh,v,u)
                        if h: hits.append(h)
    if report:
        print(f"  shape {key} {sh['name']:33s} v<{VMAX}: "
              f"{vok} live v, {cand} candidates, hits={hits if hits else 'NONE'}")
    return hits, cand, vok

if __name__=="__main__":
    VMAX=int(sys.argv[1])
    print(f"k=7 two-prime Level-2 shapes, O(1)-per-v sweep to v < {VMAX}\n")
    for k in (1,2,3,4):
        run(k,VMAX)
