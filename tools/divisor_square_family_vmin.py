from sympy import primerange
def v(n,p):
    k=0
    while n%p==0:n//=p;k+=1
    return k
P=list(primerange(5,200))
TYPES=[e for e in range(1,27) if v(e+1,2) or v(e+1,3)]
def minm(a,b):
    n2=a-v(b+1,2); n3=b-v(a+1,3)          # supply still owed by primes >= 5
    if n2<0 or n3<0: return None,None
    best=[None,None]
    def rec(start,r2,r3,exps):
        if r2==0 and r3==0:
            prod=2**a*3**b
            for p,e in zip(P,exps): prod*=p**e
            if best[0] is None or prod<best[0]: best[0]=prod; best[1]=list(exps)
            return
        for k in range(start,len(TYPES)):
            e=TYPES[k]; d2,d3=v(e+1,2),v(e+1,3)
            if d2>r2 or d3>r3 or (exps and e>exps[-1]): continue
            rec(k,r2-d2,r3-d3,exps+[e])
    TYPES.sort(reverse=True)
    rec(0,n2,n3,[])
    return best
for b in (3,4):
    for a in range(1,14):
        mm,ex=minm(a,b); j=a+v(a+1,2)-v(b+1,2)
        print(f"v3={b} a={a} j={j}  min m = {mm:.3e}  exponents on 5,7,11,...: {ex}" if mm else f"v3={b} a={a} j={j}: impossible (3 over-supplies 2)")
