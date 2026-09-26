"""Self-supplying clusters of large primes (>= T): sets where every
q^e divides the product of sigma_2 of the OTHER members. These are the
only large primes a core cannot reach by read-off. Sizes 3 and 4."""
import sys, time
from math import isqrt
from sympy import primerange, factorint
from functools import lru_cache
T=250; M=10**12; B=M//60
@lru_cache(None)
def S(q,e): return (q**(2*(e+1))-1)//(q*q-1)
@lru_cache(None)
def F(q,e): return dict(factorint(S(q,e)))
def v(n,p):
    c=0
    while n%p==0: n//=p; c+=1
    return c
def powers(q,lim):
    out=[]; e=1; p=q
    while p<=lim: out.append((e,p)); e+=1; p*=q
    return out
t=time.time(); PR=list(primerange(T, isqrt(B)+2))
tri=[]; npairs=0
for i,q1 in enumerate(PR):
    if q1**3>B: break
    for e1,p1 in powers(q1,B):
        for q2 in PR[i+1:]:
            if p1*q2*q2>B: break
            for e2,p2 in powers(q2,B//(p1*q2)):
                npairs+=1
                pool=dict(F(q1,e1))
                for k,x in F(q2,e2).items(): pool[k]=pool.get(k,0)+x
                for q3,v3 in pool.items():
                    if q3<=q2: continue
                    for e3 in range(1,v3+1):
                        p3=q3**e3
                        if p1*p2*p3>B: break
                        if v(S(q2,e2)*S(q3,e3),q1)>=e1 and v(S(q1,e1)*S(q3,e3),q2)>=e2:
                            tri.append(((q1,e1),(q2,e2),(q3,e3)))
print(f"size 3: {npairs} (q1,q2) pairs scanned -> clusters: {tri}  ({time.time()-t:.0f}s)")
t=time.time(); quad=[]; ntrip=0
for i,q1 in enumerate(PR):
    if q1**4>B: break
    for j in range(i+1,len(PR)):
        q2=PR[j]
        if q1*q2**3>B: break
        for k in range(j+1,len(PR)):
            q3=PR[k]
            if q1*q2*q3*q3>B: break
            ntrip+=1
            pool={}
            for q in (q1,q2,q3):
                for a,x in F(q,1).items(): pool[a]=pool.get(a,0)+x
            for q4,v4 in pool.items():
                if q4<=q3 or q1*q2*q3*q4>B: continue
                prods=[S(q1,1),S(q2,1),S(q3,1),S(q4,1)]
                qs=[q1,q2,q3,q4]
                ok=all(v(eval('*'.join(str(prods[b]) for b in range(4) if b!=a)),qs[a])>=1 for a in range(4))
                if ok: quad.append((q1,q2,q3,q4))
print(f"size 4: {ntrip} triples scanned -> clusters: {quad}  ({time.time()-t:.0f}s)")
print("(size 4 at exponent 1 only: any exponent >= 2 on a prime >= 251 makes the")
print(" product exceed B, since 251^2 * 257 * 263 * 269 > 1.67e10)")
print(f"   check: 251^2*257*263*269 = {251**2*257*263*269:.3e}  vs  B = {B:.3e}")
