def dr(n):
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n if n != 0 else 9

def mod9(n):
    m = n % 9
    return m if m != 0 else 9

print("Mod-9 Digit-Pair Transition System Verification\n")
print("Base chain check:")
chain = [11,12,21,22,23,32,33,34,43,44,45,54,55]
for i in range(len(chain)-1):
    a, b = divmod(chain[i], 10)
    next_expected = [chain[i]+1, int(str(b)+str(a))]
    status = "(valid)" if chain[i+1] in next_expected else "(INVALID)"
    print(f"{chain[i]:2} → {chain[i+1]:2}  {status}")

print("\nCompletion Constant 20:")
print("7+4=11+9=20 → DR =", dr(20))
print("9+1+1+9=20 → DR =", dr(20))

print("\nKey clusters collapse to same residue:")
print("9+1+1+9=20 →", dr(20))
print("9+11+9=29 →", dr(29))

print("\nGlobal invariant classes (sample):")
samples = [11,22,33,44,55,66,77,88,99,67,76,89,98]
for n in samples:
    print(f"{n:2} → DR={dr(n)}  mod9={mod9(n)}")
