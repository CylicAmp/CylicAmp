from math import log
from sympy import primerange, isprime
def v(n,p):
    k=0
    while n%p==0: n//=p; k+=1
    return k
def s2(x,e): return (x**(2*(e+1))-1)//(x*x-1)
C=(5,7,41)
def bounds(p,r):
    wp=v(pow(r,p-1,p**12)-1 or p**12,p); wr=v(pow(p,r-1,r**12)-1 or r**12,r)
    al=int(p in C); be=int(r in C); a=b=10**6
    for _ in range(60):
        a=int((al+wp+log(2*b+1)/log(p))/2); b=int((be+wr+log(2*a+1)/log(r))/2)
    return wp,wr,a,b
def check(p,r,res):
    wp,wr,A,B=bounds(p,r)
    for a in range(2,A+1):
        Sa=s2(p,2*a)
        for b in range(1,B+1):
            if (1435*Sa*s2(r,2*b))%(p**(2*a)*r**(2*b))==0: res.append((p,a,r,b))
    return A,B
res=[]; pairs=0; maxA=maxB=0
# branch 1: w_p >= 2  (r^(p-1) = 1 mod p^2), p <= 1000, r <= 1e7
for p in primerange(5,1001):
    m=p*p; roots={pow(k,p,m) for k in range(1,p)}
    for w in roots:
        for r in range(w if w>p else w+m*((p-w)//m+1), 10**7, m):
            if r>p and isprime(r):
                pairs+=1; A,B=check(p,r,res); maxA=max(maxA,A); maxB=max(maxB,B)
print(f"branch w_p>=2 (p<=1000, r<1e7): {pairs} pairs, max a-bound {maxA}, max b-bound {maxB}, solutions {res}")
res2=[]; pairs2=0
# branch 2: w_r >= 2 (p^(r-1) = 1 mod r^2), all p < r <= 3e4
for r in primerange(7,30001):
    m=r*r
    for p in primerange(5,r):
        if pow(p,r-1,m)==1:
            pairs2+=1; check(p,r,res2)
print(f"branch w_r>=2 (p<r<=3e4): {pairs2} pairs, solutions {res2}")
