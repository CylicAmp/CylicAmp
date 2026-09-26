import json, sys
from sympy import factorint, isprime, divisors
hits=json.load(open(sys.argv[1]))['hits']
ok=0
for m,p in hits:
    n=m*p
    assert isprime(p)
    ds=divisors(n)          # sorted, from sympy's own factorization of n
    s=0; k=None
    for i,d in enumerate(ds):
        s+=d*d
        if s==n: k=i+1; break
        if s>n: break
    good = k is not None and ds[k-1]==m//2 and m%2==0 and k==len(divisors(m))-1 and ds[k]==min(m,p)
    ok+=good
    print(m, p, "n=",n, "k=",k, "tau(m)=",len(divisors(m)), "OK" if good else "FAIL")
print(ok,"/",len(hits))
