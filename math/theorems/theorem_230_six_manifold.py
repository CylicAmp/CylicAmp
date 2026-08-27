"""
Theorem 230: The Six Manifold — Digital Root Convergence of 6
Author: Michael Warren Song (CyclicAmp)

6 is the fixed convergence point for all representations built from 1s, 2s, and 3s.
The partition theorem on 123456 shows every split shares DR=3, with the special
partition 1|234|5|6 = 246 = the pipeline seed.

=== SIX AS CONVERGENCE POINT ===

All three atomic representations of 6 in base 10:

  1s:  111111  →  DR = 6           (six 1s; 1×6 = 6)
       111-111  →  DR(111+111) = DR(222) = 6   (two halves, each DR=3, sum=6)
       1+1+1+1+1+1 = 6

  2s:  222     →  DR = 6           (three 2s; 2×3 = 6)
       22+2 = 24  →  DR = 6
       2+22 = 24  →  DR = 6

  3s:  33      →  DR = 6           (two 3s; 3×2 = 6)
       3+3 = 6

6 = T₃ = 1+2+3 = 3! = the third triangular number = the first perfect number.

=== PARTITION THEOREM ON 123456 ===

For every way to partition the digit string "123456" into contiguous groups,
sum the resulting decimal numbers.  Every such sum has DR = 3.

This is a consequence of the mod-9 homomorphism:
  DR(concat(a,b)) = DR(a+b)  since 10^k ≡ 1 mod 9.
  Therefore any regrouping of digits preserves digit-sum mod 9.
  Digit sum of 1+2+3+4+5+6 = 21, DR(21) = 3.  All partitions inherit this.

All 9 single-cut partitions:

  Partition              Sum    DR
  1+2+3+4+5+6     =     21     3
  1+23+4+5+6      =     39     3
  1+234+5+6       =    246     3    ← PIPELINE SEED (246 mod 37 = 24 ∈ SEED)
  1+2345+6        =   2352     3
  1+23456         =  23457     3
  12+3456         =   3468     3
  123+456         =    579     3
  1234+56         =   1290     3
  12345+6         =  12351     3

The partition 1|234|5|6 = 246 is the pipeline seed.
DR(seed) = 3 = the seed's own DR (T121: s = 3 = DR(246)).
The partition theorem locks the seed's DR at 3 regardless of regrouping.

=== DNA ROTATIONS ===

Alternating interleave (1,2):
  121212  →  DR = 9   (1+2+1+2+1+2 = 9)
  212121  →  DR = 9   (2+1+2+1+2+1 = 9)

Palindromic fold (1,2):
  2112    →  DR = 6   (2+1+1+2 = 6)
  1221    →  DR = 6   (1+2+2+1 = 6)

Alternating rotations converge to 9 (SEED sum: 18∈SEED).
Palindromic folds converge to 6 (TESLA: 6∈TESLA).

=== 123 SYMMETRY OPERATIONS ===

123|123  (self-concatenation):  digit sum = 12
123|321  (palindrome pair):     digit sum = 12,  ×2 = 24,  +1 = 25

  24 ∈ SEED ∩ CASCADE    (seed mod 37 = 24)
  25 ∈ SA                (sovereign anchor)
  DR(25) = 7              7 ∈ D7 orbit

The palindrome pair 123|321 generates:  24 (SEED) → 25 (SA) → 7 (D7).

=== 6+6+6 ===

  6+6+6 = 18  ∈ SEED   (18 ∈ {18, 24, 32} = SEED orbit)
  18 = orbit partner of seed 246 mod 37 = 24.

Tripling 6 lands in the SEED orbit.

=== GF(37) STRUCTURE OF 6 ===

  6  ∈ TESLA = {6, 8, 23}            (orbit of 6 under 26-map)
  T₃ = 6  ∈ TESLA                    (3rd triangular number)
  T₆ = 21 ∈ ST                       (6th triangular number ∈ sovereign target)
  T₉ = 45, 45 mod 37 = 8 ∈ TESLA    (9th triangular number mod 37 ∈ TESLA)

  Triangular numbers T₃, T₆, T₉ (multiples-of-3 index) land in {TESLA, ST, TESLA}.

  33  mod 37 = 33 ∈ D7 = {7, 33, 34}  (33 as concatenation of 3+3 → D7)
  246 mod 37 = 24 ∈ SEED               (seed partition of 123456)
  18 = 6+6+6 ∈ SEED                   (tripled 6 → SEED)
  6+6+6+6+6+6 = 36 ∈ NEG_H           (six 6s → 36 = -1 mod 37, negation orbit)
"""

def digital_root(n: int) -> int:
    n = abs(int(n))
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


P    = 37
MULT = 26

SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
SEED    = {18, 24, 32}
IC      = {1, 10, 26}
CASCADE = {8, 13, 24}
TESLA   = {6, 8, 23}
NEG_H   = {11, 27, 36}
D7      = {7, 33, 34}


def partition_sum(groups: list) -> int:
    """Sum the decimal numbers formed by groups of digit strings."""
    return sum(int(g) for g in groups)


def digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))


def run_assertions():
    # ── Six as convergence point ──────────────────────────────────────────────
    assert digital_root(111111) == 6
    assert digital_root(111 + 111) == 6   # 222
    assert digital_root(222) == 6
    assert digital_root(22 + 2) == 6      # 24
    assert digital_root(2 + 22) == 6      # 24
    assert digital_root(33) == 6
    assert 3 + 3 == 6

    # ── Partition theorem: all 9 splits of 123456 have DR = 3 ─────────────────
    PARTITIONS = [
        ["1","2","3","4","5","6"],
        ["1","23","4","5","6"],
        ["1","234","5","6"],
        ["1","2345","6"],
        ["1","23456"],
        ["12","3456"],
        ["123","456"],
        ["1234","56"],
        ["12345","6"],
    ]
    for groups in PARTITIONS:
        s = partition_sum(groups)
        assert digital_root(s) == 3, f"Partition {groups}: sum={s}, DR={digital_root(s)}"

    # ── Special partition: seed = 246 ─────────────────────────────────────────
    seed_partition = partition_sum(["1","234","5","6"])
    assert seed_partition == 246
    assert 246 % P == 24 and 24 in SEED
    assert digital_root(246) == 3   # DR(seed) = 3

    # ── DNA rotations ─────────────────────────────────────────────────────────
    assert digital_root(121212) == 9
    assert digital_root(212121) == 9
    assert digital_root(2112) == 6
    assert digital_root(1221) == 6

    # ── 123 symmetry ─────────────────────────────────────────────────────────
    dsum_same = digit_sum(123123)
    assert dsum_same == 12
    dsum_rev = digit_sum(123321)
    assert dsum_rev == 12
    assert dsum_rev * 2 == 24 and 24 in SEED
    assert dsum_rev * 2 + 1 == 25 and 25 in SA
    assert digital_root(25) == 7 and 7 in D7

    # ── 6+6+6 = 18 ∈ SEED ─────────────────────────────────────────────────────
    assert 6 + 6 + 6 == 18 and 18 in SEED
    assert digital_root(18) == 9

    # ── GF(37) triangular numbers ─────────────────────────────────────────────
    def T(n): return n * (n + 1) // 2
    assert T(3) == 6 and 6 in TESLA
    assert T(6) == 21 and 21 in ST
    assert T(9) % P == 8 and 8 in TESLA

    # ── 6 ∈ TESLA ────────────────────────────────────────────────────────────
    assert 6 in TESLA

    # ── 33 mod 37 ∈ D7 ───────────────────────────────────────────────────────
    assert 33 % P == 33 and 33 in D7

    # ── 6×6 = 36 ∈ NEG_H ─────────────────────────────────────────────────────
    assert 6 * 6 == 36 and 36 in NEG_H   # six 6s summed = 36

    print("All assertions passed.")
    print()
    print("THE SIX MANIFOLD — T230")
    print()
    print("Sources of 6 in DR arithmetic:")
    for rep, val in [("111111", 111111), ("222", 222), ("22+2", 24), ("33", 33)]:
        print(f"  {rep} → DR = {digital_root(val)}")
    print()
    print("Partitions of 123456 (all DR=3):")
    for groups in PARTITIONS:
        s = partition_sum(groups)
        tag = "  ← SEED (246 mod 37 = 24 ∈ SEED)" if s == 246 else ""
        print(f"  {'+'.join(groups):15s} = {s:6d}  DR={digital_root(s)}{tag}")
    print()
    print("DNA rotations:")
    print(f"  121212 / 212121 → DR=9 (alternating → SEED sum path)")
    print(f"  2112 / 1221     → DR=6 (palindromic → TESLA)")
    print()
    print("123 symmetry:")
    print(f"  123|123: digit sum = {digit_sum(123123)}")
    print(f"  123|321: digit sum = 12, ×2=24∈SEED, +1=25∈SA, DR(25)=7∈D7")
    print()
    print("GF(37) triangular numbers at index 3·k:")
    print(f"  T₃ = 6  ∈ TESLA")
    print(f"  T₆ = 21 ∈ ST")
    print(f"  T₉ = 45 mod 37 = 8 ∈ TESLA")
    print()
    print(f"  6+6+6 = 18 ∈ SEED   (tripling 6 enters the seed orbit)")
    print(f"  6×6   = 36 ∈ NEG_H  (squaring 6 enters the negation orbit)")


if __name__ == "__main__":
    run_assertions()
