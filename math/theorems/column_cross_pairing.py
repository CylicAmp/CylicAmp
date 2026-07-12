"""
Column Cross-Pairing Theorem
Column groups of the 3×3 grid: COL1=(1,4,7), COL2=(2,5,8), COL3=(3,6,9)

Results:

1. SEQUENTIAL ACCUMULATION RULE
   Summing a group's elements one-by-one always converges to that group's DR.
   COL2: 2+5=7, 7+8=15, DR=6 = DR(COL2). Holds for all rows and columns.

2. CROSS-PAIRING TOTALS
   COL1×COL1 = 24   DR=6  (cascade base)
   COL1×COL2 = 27   DR=9  (fixed point)
   COL1×COL3 = 30   DR=3  (sovereign bridge)
   COL2×COL2 = 30   DR=3  (sovereign bridge)
   COL2×COL3 = 33   DR=6
   COL3×COL3 = 36   DR=9

3. SOVEREIGN BRIDGE 30 IS STRUCTURALLY FORCED
   30 appears at COL1×COL3, COL2×COL2, and DIAG1×DIAG2 — three independent paths.
   DR(30) = 3 (sovereign).

4. PURE SOVEREIGN OUTPUT
   COL1×COL2 pair DRs = {3,9,6} — the complete sovereign+fixed set.
   COL3×COL3 pair DRs = {6,3,9} — the DR orbit of 3 (self-referential).

5. 842 AND 963
   842 = 8→4→2 (halving descent from AHL=8).
   963 = 9,6,3 = COL3 reversed. 963 = 9×107, DR(107)=8=AHL.
   DR(842)=5, DR(963)=9 (fixed point absorber).
   DR(842+963) = DR(842): adding any multiple of 9 preserves DR.

6. FIXED-POINT ABSORPTION
   If DR(b) = 9 (b is a multiple of 9), then DR(a+b) = DR(a) for all a.
   963 is such an absorber. So is 369 (DS=18=2×9), 9, 18, 27, ...

7. TOTALS CYCLE
   All column cross-pairing totals: {24,27,30,33,36} = 3×{8,9,10,11,12}
   DRs of those totals: {6,9,3,6,9} — only sovereign and fixed point values.
"""


def dr(n: int) -> int:
    return (n - 1) % 9 + 1 if n > 0 else 0


COL1, COL2, COL3 = [1, 4, 7], [2, 5, 8], [3, 6, 9]
DIAG1, DIAG2 = [1, 5, 9], [3, 5, 7]


def pair_sums(A, B):
    return [a + b for a, b in zip(A, B)]


def pair_total(A, B):
    return sum(pair_sums(A, B))


def pair_sum_dr(A, B):
    return dr(pair_total(A, B))


# 1. Sequential accumulation
assert dr(sum(COL2)) == 6
running = 0
for x in COL2:
    running += x
assert dr(running) == 6  # final step matches

# 2. Cross-pairing totals
assert pair_total(COL1, COL1) == 24 and pair_sum_dr(COL1, COL1) == 6
assert pair_total(COL1, COL2) == 27 and pair_sum_dr(COL1, COL2) == 9
assert pair_total(COL1, COL3) == 30 and pair_sum_dr(COL1, COL3) == 3
assert pair_total(COL2, COL2) == 30 and pair_sum_dr(COL2, COL2) == 3
assert pair_total(COL2, COL3) == 33 and pair_sum_dr(COL2, COL3) == 6
assert pair_total(COL3, COL3) == 36 and pair_sum_dr(COL3, COL3) == 9

# 3. Sovereign bridge from diagonals
assert pair_total(DIAG1, DIAG2) == 30 and pair_sum_dr(DIAG1, DIAG2) == 3

# 4. Pure sovereign output
c12_drs = sorted([dr(s) for s in pair_sums(COL1, COL2)])
assert c12_drs == [3, 6, 9]
c33_drs = [dr(s) for s in pair_sums(COL3, COL3)]
assert c33_drs == [6, 3, 9]  # orbit of 3

# 5. 842 and 963
assert dr(842) == 5  # halving descent: 8,4,2
assert dr(963) == 9  # COL3 reversed; 963 = 9×107
assert dr(107) == 8  # AHL
assert 963 == 9 * 107
assert dr(842 + 963) == dr(842)  # fixed-point absorption

# 6. Fixed-point absorption: DR(b)=9 → DR(a+b)=DR(a)
for a in [1, 17, 41, 123, 842]:
    for b_factor in [1, 107, 369 // 9 if 369 % 9 == 0 else None]:
        if b_factor:
            b = 9 * b_factor
            assert dr(a + b) == dr(a), f"Absorption failed: a={a}, b={b}"

# 7. All cross-pairing totals in {24,27,30,33,36}
all_totals = [pair_total(A, B)
              for A in [COL1, COL2, COL3]
              for B in [COL1, COL2, COL3]]
unique_totals = sorted(set(all_totals))
assert unique_totals == [24, 27, 30, 33, 36]
assert all(dr(t) in {3, 6, 9} for t in unique_totals)


if __name__ == "__main__":
    print("COLUMN CROSS-PAIRING THEOREM")
    print("=" * 45)
    print()
    print("Sequential accumulation:")
    for name, G in [("COL2", COL2), ("ROW2", [4,5,6]), ("ROW1", [1,2,3])]:
        running = 0
        steps = []
        for x in G:
            running += x
            steps.append(running)
        print(f"  {name}: steps={steps}  DR={dr(running)} = DR(group)")
    print()

    print("Cross-pairing totals:")
    labels = {"COL1": COL1, "COL2": COL2, "COL3": COL3}
    for na, A in labels.items():
        for nb, B in labels.items():
            if na <= nb:
                ps = pair_sums(A, B)
                t = sum(ps)
                print(f"  {na}×{nb}: pair_sums={ps}  DRs={[dr(s) for s in ps]}  "
                      f"total={t}  DR={dr(t)}")
    print()

    print("Diagonal cross:")
    ps = pair_sums(DIAG1, DIAG2)
    t = sum(ps)
    print(f"  DIAG1(1,5,9)×DIAG2(3,5,7): pair_sums={ps}  DRs={[dr(s) for s in ps]}  "
          f"total={t}  DR={dr(t)}")
    print()

    print("842 and 963:")
    print(f"  842=8→4→2 (halving from AHL), DR={dr(842)}")
    print(f"  963=9×107, DR(107)={dr(107)}=AHL, DR(963)={dr(963)}")
    print(f"  842+963={842+963}, DR={dr(842+963)} (preserved)")
    print()

    print(f"All unique totals: {unique_totals}")
    print(f"Their DRs: {[dr(t) for t in unique_totals]} ∈ {{3,6,9}}")
    print()
    print("All assertions passed.")
