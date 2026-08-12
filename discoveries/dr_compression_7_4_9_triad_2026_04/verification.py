def dr(n):
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n if n != 0 else 9

print("DR Compression – 7-4-9 Triad Verification\n")

chains = {
    "Origin (162)": 162,
    "Prime Chain (97)": 97,
    "Symmetry Chain (25)": 25,
    "Expansion (94)": 94,
    "Simple Triple (13)": 13
}

for name, val in chains.items():
    print(f"{name}: DR({val}) = {dr(val)}")

print("\n7-4-9 Triad check:")
print(f"DR(7) = {dr(7)}")
print(f"DR(4) = {dr(4)}")
print(f"DR(9) = {dr(9)}")
print(f"Sum = {dr(7)+dr(4)+dr(9)}")
