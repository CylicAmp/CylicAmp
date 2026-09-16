import json
from sympy import isprime

def rev(n): return int(str(n)[::-1])

def ord10(p):
    if p in (2, 5): return None
    o, c = 1, 10 % p
    while c != 1: c = (c*10) % p; o += 1
    return o

def emirp_stats(X, m, lo=1000):
    counts = [0]*m
    for p in range(lo, X):
        if isprime(p):
            rp = rev(p)
            if len(str(rp)) == len(str(p)) and isprime(rp):
                counts[p % m] += 1
    # restricted: exclude residue 0
    r = counts[1:]
    tr = sum(r)
    valid = m - 1
    exp = tr / valid
    chi2_r = sum((c - exp)**2 / exp for c in r)
    df = valid - 1
    # standardized effect size: Z = (chi2 - df) / sqrt(2 df)
    Z = (chi2_r - df) / (2*df)**0.5
    return {"mod": m, "ord10": ord10(m), "999_div": 999 % m == 0,
            "N": tr, "chi2_r": round(chi2_r,1), "df": df, "Z": round(Z,2)}

X = 10**6
rows = [emirp_stats(X, m) for m in (31, 37, 41, 43)]
print(json.dumps({"bound": X, "rows": rows}, indent=2))
