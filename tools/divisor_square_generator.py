"""Smooth-m generator with CORRECT verification.

gen3 assumed n/m was prime when it was not smooth, built the divisor list
from that assumption, and checked the candidate against its own wrong list.
4 of 5 sampled hits were false. Here every candidate is factored for real
and its true divisor list rebuilt before it is accepted."""
import sys, time
from sympy import factorint

def smooth(primes, M):
    out=[1]
    for p in primes:
        new=[]
        for m in out:
            v=m
            while v<=M: new.append(v); v*=p
        out=new
    return sorted(out)

def divisors_from(f):
    d=[1]
    for p,e in f.items(): d=[x*p**i for x in d for i in range(e+1)]
    return sorted(d)

def verify(n):
    """ground truth: factor n, build all divisors, test every prefix"""
    D=divisors_from(factorint(n))
    s=0
    for k,d in enumerate(D,1):
        s+=d*d
        if s==n: return k
        if s>n: return None
    return None

def run(primes, M, verbose=True):
    t=time.time(); ms=smooth(primes,M)
    if verbose: print(f"  {len(ms)} smooth m <= {M}", flush=True)
    cand=0; hits=[]
    for m in ms:
        if m<2: continue
        D=divisors_from(factorint(m))
        s=0
        for k,d in enumerate(D,1):
            s+=d*d
            if s<=m or s%m: continue
            cand+=1
            kk=verify(s)
            if kk: hits.append((s,kk,m))
    if verbose: print(f"  {cand} candidates factored, {len(set(hits))} verified  ({time.time()-t:.0f}s)")
    return sorted(set(hits))

if __name__=="__main__":
    M=int(sys.argv[1])
    P=[2,3,5,7,11,13,17,19,23,29,31,37,41,43]
    for n,k,m in run(P,M):
        print(f"  n = {n:>22}  k = {k:<5} m = {m}")
