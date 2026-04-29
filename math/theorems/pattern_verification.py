# Raw computational verification of user-provided patterns
# No narrative. Only operators and results.

from itertools import permutations

print("="*60)
print("PATTERN VERIFICATION")
print("="*60)

# Pattern 1: Doubling chain
print("\n1. DOUBLING CHAIN")
print("-"*40)
chain = [(1, 1, 2), (2, 2, 4), (4, 4, 8)]
for a, b, expected in chain:
    result = a + b
    print(f"  {a}+{b}={result} {'✓' if result == expected else '✗'}")

# Pattern 2: 6x4 grid
print("\n2. 6x4 GRID")
print("-"*40)

grid = [
    [4, 2, 2, 2, 2, 4],
    [2, 4, 2, 2, 4, 2],
    [2, 2, 4, 4, 2, 2],
    [4, 2, 2, 2, 2, 4],
]

print("  Grid:")
for i, row in enumerate(grid):
    row_sum = sum(row)
    print(f"    Row {i+1}: {'-'.join(map(str, row))} = {row_sum}")

total = sum(sum(row) for row in grid)
print(f"\n  Total sum: {total}")
print(f"  6+4=10 reference: {6+4}")

# Pattern 3: 88+66
print("\n3. 88+66")
print("-"*40)
result_154 = 88 + 66
print(f"  88+66 = {result_154}")
print(f"  Addend digit sum:  8+8+6+6 = {8+8+6+6}")
print(f"  Result digit sum:  1+5+4   = {sum(int(d) for d in str(result_154))}")

# Pattern 4: 1-2-8 permutations
print("\n4. 1-2-8 PERMUTATIONS")
print("-"*40)

perms = set(permutations([1, 2, 8]))
for p in sorted(perms):
    s = sum(p)
    print(f"  {'-'.join(map(str, p))} = {s}")

# Pattern 5: 123/321 mirror
print("\n5. 123/321 MIRROR (recall)")
print("-"*40)
print(f"  123+321 = {123+321}")
print(f"  321+123 = {321+123}")
print(f"  123+321+123+321 = {123+321+123+321}")

print("\n" + "="*60)
