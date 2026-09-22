def dr(n):
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n if n != 0 else 9

print("9x9 State Matrix [11, 99] Verification\n")

diagonal = [11,22,33,44,55,66,77,88,99]
print("Fixed diagonal DRs:")
for d in diagonal:
    print(f"{d:2} → DR = {dr(d)}")

chain = [89,98,99]
mods = [x % 37 for x in chain]
print("\nChain [89-99] mod 37:")
for x, m in zip(chain, mods):
    print(f"{x:2} ≡ {m:2} (mod 37)")

print("\nDifferential persistence:")
print("25 - 15 =", 25-15)
print("24 - 15 =", 24-15)
print("25 - 24 =", 25-24)

print("\nCompletion Constant check:")
print("575 % 37 =", 575 % 37)
print("DR(7) + DR(4) + DR(9) =", dr(7) + dr(4) + dr(9))
