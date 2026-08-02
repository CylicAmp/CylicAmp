def dr(n):
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n if n != 0 else 9

print("Mersenne Exponents – 7-4-9 Triad Alignment\n")

exponents = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127]

print(f"{'p':<6} {'DR(p)':<8} {'In {4,7,9}?'}")
for p in exponents:
    d = dr(p)
    flag = "yes" if d in [4, 7, 9] else "no"
    print(f"{p:<6} {d:<8} {flag}")

aligned = [p for p in exponents if dr(p) in [4, 7, 9]]
print(f"\nAligned: {aligned}")
print(f"Count: {len(aligned)} of {len(exponents)}")
