"""The 'all proper divisors of m' family: n = m*p, prefix = proper divisors of m.
Needs m | sigma_2(m) and p = sigma_2(m)/m - m prime with p > m/2.
Search it directly and record tau(m) for every member."""
import sys, time, numpy as np
from sympy import isprime
from collections import Counter
N=int(sys.argv[1]); t=time.time()
spf=np.zeros(N+1,dtype=np.int64)
for i in range(2,int(N**0.5)+1):
    if spf[i]==0:
        spf[i*i::i][spf[i*i::i]==0]=i
spf_list=spf.tolist()
def fac(m):
    f={}
    while m>1:
        p=spf_list[m] or m
        e=0
        while m%p==0: m//=p; e+=1
        f[p]=e
    return f
fam=[]; tried=0
for m in range(6,N+1,6):          # 2|m and 3|m are forced by sum 1/d^2 > 3/2
    f=fac(m); s2=1; tau=1
    for p,e in f.items():
        s2*= (p**(2*(e+1))-1)//(p*p-1); tau*=e+1
    if 2*s2 <= 3*m*m: continue    # need sigma_2/m^2 > 3/2
    tried+=1
    if s2 % m: continue           # need m | sigma_2(m)
    q = s2//m - m
    if q > m//2 and isprime(q):
        fam.append((m,q,tau,f))
print(f"m <= {N}, m = 0 mod 6: {tried} passed sum(1/d^2)>3/2, {len(fam)} family members  ({time.time()-t:.0f}s)")
for m,q,tau,f in fam:
    fs=" * ".join(f"{p}^{e}" if e>1 else str(p) for p,e in sorted(f.items()))
    print(f"   m={m:>9}  tau={tau:>4}  p={q:>10}  m = {fs}")
print("tau distribution:", dict(Counter(t for _,_,t,_ in fam)))
