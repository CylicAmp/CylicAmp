"""n = sum of squares of its k smallest divisors, for SOME k.
Every divisor used satisfies d_k^2 <= n, so only d <= sqrt(n) matter.
Segmented: add divisors in increasing order, test equality after each."""
import sys, time, numpy as np

def search(lo, hi, block=2_000_000, verbose=False):
    out=[]; n=lo
    while n < hi:
        top=min(n+block, hi); size=top-n
        vals=np.arange(n, top, dtype=np.int64)
        acc=np.zeros(size, dtype=np.int64)
        alive=np.ones(size, dtype=bool)
        dmax=int(top**0.5)+1
        for d in range(1, dmax+1):
            start=((n + d - 1)//d)*d
            if start>=top: continue
            idx=np.arange(start, top, d, dtype=np.int64)-n
            if idx.size==0: continue
            idx=idx[alive[idx]]
            if idx.size==0: continue
            acc[idx]+=d*d
            hit=idx[acc[idx]==vals[idx]]          # equality at this k
            for h in hit: out.append(int(vals[h]))
            alive[idx[acc[idx]>=vals[idx]]]=False # past n, or already counted
        if verbose: print(f"   ..{top}", flush=True)
        n=top
    return sorted(out)

if __name__=="__main__":
    lo,hi=int(sys.argv[1]),int(sys.argv[2])
    t=time.time(); r=search(lo,hi,verbose=(hi-lo>2_000_000))
    print(f"n in [{lo},{hi}): {r}   ({time.time()-t:.1f}s)")
