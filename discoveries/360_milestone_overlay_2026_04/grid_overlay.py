def dr(n):
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n if n != 0 else 9

print("9×9 DR Grid with 360 Milestone Overlay\n")

print("Grid (row i, col j → DR(i+j)):\n")
header = "    " + "  ".join(f"{j}" for j in range(1,10))
print(header)
for i in range(1, 10):
    row = f"{i}  "
    for j in range(1, 10):
        val = dr(i+j)
        if (i,j) in [(3,6),(6,3)]:
            row += f" ★"
        elif (i,j) == (4,4):
            row += f" ◆"
        else:
            row += f" {val}"
    print(row)

print("\nDR=9 coordinate pairs (a+b=9):")
pairs = [(a, 9-a) for a in range(1,9)]
for p in pairs:
    print(f"  {p}")

print("\n360 Milestone jump sequence:")
print("360 → 384 (+24) → 396 (+12) → 432 (+36)")
print(f"360 mod 81 = {360 % 81}")
print(f"360 mod 37 = {360 % 37}")
print(f"Gap to 432: {432-360} = 8×9 = {8*9}")
