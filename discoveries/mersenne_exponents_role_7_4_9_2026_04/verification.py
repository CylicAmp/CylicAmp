def dr(n):
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

exponents = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127]

print("Mersenne Exponents Role Verification\n")
print(f"{'Exponent':<8} {'p % 9':<8} {'DR':<5} {'Fits Triad'}")
for p in exponents:
    mod9 = p % 9
    d = dr(p)
    fits = "YES" if d in [4, 7, 9] or mod9 in [4, 7, 0] else "no"
    print(f"{p:<8} {mod9:<8} {d:<5} {fits}")
