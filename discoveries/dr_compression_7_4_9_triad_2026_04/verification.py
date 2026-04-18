def dr(n):
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

chains = {
    "Origin (162)": 162,
    "Prime Chain (97)": 97,
    "Symmetry Chain (25)": 25,
    "Expansion (94)": 94,
    "Simple Triple (13)": 13
}

print("Digital Root Compression Verification\n")
for name, value in chains.items():
    d = dr(value)
    mod9 = value % 9
    target = mod9 if mod9 != 0 else 9
    print(f"{name:20} → DR = {d} (mod 9 = {mod9}) → Target {target}")
