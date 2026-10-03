"""SIZE TEST.  P = product of the distinct primes of the shape divides n, so
n >= P.  n = sum of nine divisor squares, each <= d_9, with d_1 = 1 < d_9, so
n < 9 d_9^2.  For any two distinct primes u,v of the shape, uv | n; if uv is
NOT one of the nine tokens then uv > d_9.  With m the least such non-token
product, d_9 < m and therefore

        P <= n < 9 d_9^2 < 9 m^2      i.e.   P < 9 m^2

is NECESSARY.  A shape for which no admissible prime assignment satisfies it
is empty for all values -- no search, no bound."""
import sys, itertools
from sympy import primerange
PR=list(primerange(5,4000))
def parse(sh):
    toks=sh.split(); syms=[]; tokset=set()
    for tk in toks:
        if tk=="1": tokset.add(()); continue
        d={}
        for part in tk.split("*"):
            b,e=(part.split("^")+["1"])[:2]; d[b]=int(e)
        tokset.add(tuple(sorted(d.items())))
        for b in d:
            if b!="3" and b not in syms: syms.append(b)
    order=["3"]+[s for s in "pqrst" if s in syms]
    return toks,tokset,order
def feasible(sh,LIM=40):
    """is P < 9 m^2 satisfiable for ANY admissible assignment of the free primes?"""
    toks,tokset,order=parse(sh)
    free=order[1:]
    best=None
    for combo in itertools.combinations(PR[:LIM],len(free)):
        v={"3":3}
        for s,x in zip(free,combo): v[s]=x
        vals=[]
        ok=True
        for tk in toks:
            if tk=="1": vals.append(1); continue
            x=1
            for part in tk.split("*"):
                b,e=(part.split("^")+["1"])[:2]; x*=v[b]**int(e)
            vals.append(x)
        if sorted(vals)!=vals or len(set(vals))!=len(vals): continue
        d9=vals[-1]
        P=1
        for b in order: P*=v[b]
        m=None
        for u,w in itertools.combinations(order,2):
            prod=v[u]*v[w]
            if prod not in vals:
                m=prod if m is None else min(m,prod)
        if m is None: continue
        if P < 9*m*m:
            return True,(dict(v),P,m,d9)
    return False,None
if __name__=="__main__":
    fn=sys.argv[1]; LIM=int(sys.argv[2]) if len(sys.argv)>2 else 40
    dead=[]; alive=0
    L=[l.rstrip() for l in open(fn) if l.strip()]
    for l in L:
        f,_=feasible(l,LIM)
        if f: alive+=1
        else: dead.append(l)
    print("%s : %d shapes ; size test KILLS %d ; %d survive"%(fn,len(L),len(dead),alive))
    open(fn.replace(".txt","_sizedead.txt"),"w").write("\n".join(dead)+"\n")
