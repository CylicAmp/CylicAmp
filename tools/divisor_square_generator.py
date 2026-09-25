"""Blocked divisor sieve over m; every candidate verified against its own prefix."""
import sys, time

def verify(n, kmax=400):
    D=[]; s=0; d=1
    lim=int(n**0.5)+1
    while d<=lim and len(D)<kmax:
        if n%d==0:
            D.append(d); s+=d*d
            if s==n: return len(D)
            if s>n: return None
        d+=1
    return None

def search(M, block=100_000, verbose=True):
    hits=[]; t=time.time()
    lo=2
    while lo<=M:
        hi=min(lo+block, M+1)
        divs=[[] for _ in range(hi-lo)]
        for d in range(1, hi):
            start=max(d, ((lo+d-1)//d)*d)
            for m in range(start, hi, d):
                divs[m-lo].append(d)
        for i,D in enumerate(divs):
            m=lo+i
            s=0
            for k,d in enumerate(D,1):
                s+=d*d
                if s<=m or s%m: continue
                if verify(s): hits.append((s,k,m))
        if verbose: print(f"   m<{hi}  ({time.time()-t:.0f}s)  hits so far {len(hits)}", flush=True)
        lo=hi
    return sorted(set(hits))

if __name__=="__main__":
    M=int(sys.argv[1])
    for n,k,m in search(M):
        print(f"  n = {n:>20}  k = {k:<4} from m = {m}")
