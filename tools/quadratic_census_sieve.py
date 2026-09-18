import sys, time
N   = 10_000_000          # n < N
B   = 3_000_000           # sieve bound

def primes_upto(m):
    s = bytearray([1])*(m+1); s[0]=s[1]=0
    for i in range(2,int(m**0.5)+1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(2,m+1) if s[i]]

def sqrt_mod(a,p):
    a%=p
    if a==0: return 0
    if pow(a,(p-1)//2,p)!=1: return None
    if p%4==3: return pow(a,(p+1)//4,p)
    q,s=p-1,0
    while q%2==0: q//=2; s+=1
    z=2
    while pow(z,(p-1)//2,p)!=p-1: z+=1
    m,c,t,r=s,pow(z,q,p),pow(a,q,p),pow(a,(q+1)//2,p)
    while t!=1:
        i,t2=0,t
        while t2!=1: t2=t2*t2%p; i+=1
        b=pow(c,1<<(m-i-1),p); m=i; c=b*b%p; t=t*c%p; r=r*b%p
    return r

def mr(n):
    # the small-prime pre-check is LOAD-BEARING: if the value is itself one
    # of the bases then that base is 0 mod n and the test wrongly rejects a
    # genuine prime. Dropping it undercounted A by 1 (7), B by 2 (5, 17)
    # and C by 2 (3, 13) at every mark in the 10^8 run.
    if n<2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37,41):
        if n%p==0: return n==p
    d,s=n-1,0
    while d%2==0: d//=2; s+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37,41):
        x=pow(a,d,n)
        if x==1 or x==n-1: continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True

FORMS = {'A':(4,2,1), 'B':(4,0,1), 'C':(4,-2,1)}
t0=time.time()
PR = primes_upto(B)
print("primes to %d: %d  (%.0fs)"%(B,len(PR),time.time()-t0), flush=True)

MARKS = (10_000, 500_000, 1_000_000, 5_000_000, 10_000_000)
results = {}
for name,(a,b,c) in FORMS.items():
    f = lambda n,a=a,b=b,c=c: a*n*n+b*n+c
    alive = bytearray([1])*N
    disc = b*b-4*a*c
    inv8 = None
    for p in PR:
        if p==2: continue                      # all values are odd
        d = disc % p
        if d==0:
            inv2a = pow(2*a % p, p-2, p)
            roots = [(-b)*inv2a % p]
        else:
            s = sqrt_mod(d,p)
            if s is None: continue
            inv2a = pow(2*a % p, p-2, p)
            roots = {((-b+s)*inv2a)%p, ((-b-s)*inv2a)%p}
        for r in roots:
            if r<N:
                alive[r::p] = bytearray(len(alive[r::p]))
            # restore n where f(n) == p itself
            for n in (r, r+p):
                if n<N and f(n)==p: alive[n]=1
    surv = [n for n in range(N) if alive[n]]
    print("%s: survivors after sieve %d (%.0fs)"%(name,len(surv),time.time()-t0), flush=True)
    cnt=0; marks={}
    mi=0
    for n in surv:
        while mi<len(MARKS) and n>=MARKS[mi]:
            marks[MARKS[mi]]=cnt; mi+=1
        if f(n)>1 and mr(f(n)): cnt+=1
    while mi<len(MARKS): marks[MARKS[mi]]=cnt; mi+=1
    results[name]=marks
    print("%s: %s  (%.0fs)"%(name,marks,time.time()-t0), flush=True)

print()
print("  k            A          B          C        A>C")
for k in MARKS:
    A,Bc,C = results['A'][k],results['B'][k],results['C'][k]
    print("  %-11d %-10d %-10d %-10d %s"%(k,A,Bc,C,A>C))
print("total %.0fs"%(time.time()-t0))
