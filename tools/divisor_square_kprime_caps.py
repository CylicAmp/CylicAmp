"""Exponent caps for s with k distinct primes >= 5, no Wieferich-type pair.
For each x: 2 e_x <= 1 + (k-1) + sum_{y != x} v_x(2 e_y + 1)."""
from math import log
from sympy import primerange
def v(n,p):
    c=0
    while n%p==0: n//=p; c+=1
    return c
for k in range(1,13):
    M=1
    while 2*(M+1) <= k + (k-1)*log(2*(M+1)+1)/log(5): M+=1
    # caps: generic prime and small primes x <= 2M+1; iterate to fixed point
    xs=list(primerange(5,2*M+2))
    cap={x:M for x in xs}; gen=M
    for _ in range(50):
        top=max([gen]+list(cap.values()))
        new={}
        for x in xs:
            best=max(v(2*e+1,x) for e in range(1,top+1))
            new[x]=min(M,(1+(k-1)+(k-1)*best)//2)
        # the booster e_y must itself be allowed: recompute with allowed exponents
        allowed=set(range(1,max(list(new.values())+[(k)//2])+1))
        for x in xs:
            best=max([v(2*e+1,x) for e in allowed]+[0])
            new[x]=min(M,(1+(k-1)+(k-1)*best)//2)
        g=min(M,k//2)
        if new==cap and g==gen: break
        cap,gen=new,g
    print(f"k={k:2d}: M <= {M}; generic prime e <= {gen}; small primes: "+", ".join(f"e_{x}<={c}" for x,c in cap.items() if c>gen))
