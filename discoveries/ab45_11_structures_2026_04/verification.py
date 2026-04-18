print("AB45=11 Structures – All 24 Valid Versions\n")

pairs = [(2,9),(3,8),(4,7),(5,6)]
structures = []

for outer in pairs:
    for inner in pairs:
        if inner != outer:
            x, w = outer
            y, z = inner
            structures.append(f"{x}{y}{z}{w}")

for outer in [(9,2),(8,3),(7,4),(6,5)]:
    for inner in pairs:
        if inner != outer:
            x, w = outer
            y, z = inner
            structures.append(f"{x}{y}{z}{w}")

for i, s in enumerate(structures, 1):
    print(f"{i:2}. {s}")

print(f"\nTotal: {len(structures)}")
