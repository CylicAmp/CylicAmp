"""Prime factors >= 250 of sigma_2(p^e) for every prime p < 250 with p^e <= MAXM.
One line per (p, e): 'p e f1 f2 ...'. Consumed by the Rust search."""
import sys, time
from sympy import primerange, factorint
MAXM=int(float(sys.argv[1])) if len(sys.argv)>1 else 10**22
T=250; t=time.time(); n=0
with open("small_table.txt","w") as f:
    for p in primerange(2,T):
        e=1; pe=p
        while pe<=MAXM:
            S=(p**(2*(e+1))-1)//(p*p-1)
            fs=sorted(q for q in factorint(S) if q>=T)
            f.write(f"{p} {e} "+" ".join(map(str,fs))+"\n"); n+=1
            e+=1; pe*=p
print(f"{n} entries, {time.time()-t:.0f}s")
