"""sigma_3(n) mod 37 segmented sieve (vectorised; verified: 188742 zeros <= 1e6).
Usage: python3 tools/sigma3_mod37_sieve.py LIM [checkpoints...]
Exponent of each p <= sqrt(LIM) by numpy masks; sigma_3(p^e) mod 37 by table; the
residual after all p <= sqrt(LIM) is 1 or ONE prime > sqrt(LIM). Checkpoint
snapshots count only the prefix of the segment up to the checkpoint; per-residue
zero counts AND class sizes are both kept."""
import numpy as np, math, sys, time
from sympy import primerange
LIM=int(float(sys.argv[1])); B=2_000_000
CK=sorted(int(float(c)) for c in sys.argv[2:]) if len(sys.argv)>2 else [LIM]
snap={}
primes=list(primerange(2,math.isqrt(LIM)+1))
zero_by_res=np.zeros(37,np.int64); n_by_res=np.zeros(37,np.int64); nonzero=0
t0=time.time()
for lo in range(1,LIM+1,B):
    hi=min(lo+B,LIM+1)
    val=np.arange(lo,hi,dtype=np.int64); sig=np.ones(hi-lo,np.int64)
    for p in primes:
        if p>=hi: break
        st=((lo+p-1)//p)*p-lo
        idx=np.arange(st,hi-lo,p)
        vv=val[idx]; e=np.zeros(len(idx),np.int64)
        m=vv%p==0
        while m.any():
            vv[m]//=p; e[m]+=1; m=vv%p==0
        val[idx]=vv
        r=pow(p,3,37); S=[1]; pw=1
        for _ in range(64): pw=pw*r%37; S.append((S[-1]+pw)%37)
        sig[idx]=sig[idx]*np.array(S,np.int64)[e]%37
    big=val>1                                  # residual: 1 or ONE prime > sqrt(LIM)
    sig[big]=sig[big]*((1+(val[big]%37)**3)%37)%37
    z=sig==0; res=np.arange(lo,hi)%37
    zero_by_res+=np.bincount(res[z],minlength=37); n_by_res+=np.bincount(res,minlength=37)
    for c in CK:                               # snapshot only the part of the segment up to c
        if lo<=c<hi:
            u=c-lo+1
            snap[c]=(nonzero+int((~z[:u]).sum()),
                     zero_by_res-np.bincount(res[u:][z[u:]],minlength=37),
                     n_by_res-np.bincount(res[u:],minlength=37))
    nonzero+=int((~z).sum())
for c in CK:
    nz,zr,nr=snap[c]; print(f"x={c:.0e}: nonzero {nz} density {nz/c:.9f}; max class density spread {float(np.ptp(1-zr[1:]/nr[1:])):.6f}")
print(f"LIM={LIM:.0e}: zeros {LIM-nonzero}, nonzero density {nonzero/LIM:.6f}, {time.time()-t0:.1f}s")
print("zeros by residue (first 6):",zero_by_res[:6].tolist()," counts:",n_by_res[:6].tolist())
