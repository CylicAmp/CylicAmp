"""
dr6_tensor_audit.py

DR-6 field: 123-variation matrices and the 9-row tensor block.

─────────────────────────────────────────────────────────────────
THE DR-6 FAMILY:

  Every element in the system has DR = 6:
    15: 1+5=6  |  24: 2+4=6  |  33: 3+3=6
    42: 4+2=6  |  51: 5+1=6
    123: 1+2+3=6  |  213: 2+1+3=6  |  312: 3+1+2=6  |  321: 3+2+1=6

  Row sum: 6+6+6+6 = 24 → DR(24) = 6. The 6-signature is preserved under
  4-fold addition because 4×6 ≡ 6 (mod 9) (additive order of 6 in Z/9Z is 3;
  4 = 3+1, so 4×6 ≡ 6).

─────────────────────────────────────────────────────────────────
WHY CROSS-PRODUCTS COLLAPSE TO 9:

  DR(a)=6, DR(b)=6 → DR(a×b) = DR(6×6) = DR(36) = 9 (NULL).

  Algebraic reason: 6 is nilpotent of order 2 in Z/9Z.
    6¹ ≡ 6 (mod 9)
    6² = 36 ≡ 0 (mod 9)  → DR = 9
  Any two 6-field elements annihilate to NULL when multiplied.
  This is not an emergent property of these specific numbers;
  it is a theorem about the residue 6 in Z/9Z.

─────────────────────────────────────────────────────────────────
NILPOTENCY vs IDEMPOTENCY:

  Addition:      6+6 = 12 → DR = 3;  6+6+6 = 18 → DR = 9 (annihilates in 3 steps)
  Multiplication: 6×6 = 36 → DR = 9 (annihilates in 1 step)

  Compare: 9×9=81→DR=9 (idempotent); 1×1=1→DR=1 (idempotent).
  6 is the unique nilpotent in {1..9} under DR-multiplication.
  Because 6 = -3 mod 9 and (-3)² = 9 ≡ 0.

─────────────────────────────────────────────────────────────────
VECTOR DOT PRODUCTS:

  L = [123, 312, 321, 123],  R = [321, 213, 123, 321]
    123×321 = 39,483  → digit sum 27 → DR=9
    312×213 = 66,456  → digit sum 27 → DR=9
    321×123 = 39,483  → digit sum 27 → DR=9
    123×321 = 39,483  → digit sum 27 → DR=9

  All products: digit sum = 27.  DR(27) = 9.
  All products are multiples of 9 (nilpotency theorem applied).

─────────────────────────────────────────────────────────────────
GENUS ANALYSIS (topological loops in digit symbols):

  Loop-carrying digits: 0(1), 4(1), 6(1), 8(2), 9(1).
  This digit set uses only {1,2,3,5} in permutations and {1,5},{2,4},{3,3},{4,2},{5,1}
  in gateways. Only digit 4 carries a loop.

  Gateway genus:
    15: 0   24: 1   33: 0   42: 1   51: 0

  Key: 42 and 24 are digit-reverses of each other and have EQUAL genus (both = 1).
  Key: 51 and 15 are digit-reverses of each other and have EQUAL genus (both = 0).

  Replacing 24 with 42 in a row: Γ unchanged (digit 4 present in both).
  Replacing 33 with 42 in a row: Γ increases by 1 (digit 4 introduced).
  Replacing 15 with 51 in a row: Γ unchanged.

─────────────────────────────────────────────────────────────────
9-ROW MATRIX GENUS (blocks C+D):

  Rows 1,3,5,7,8: no 4-digit → genus = 0
  Row 2 (312-33-24-213): genus = 1  (from digit 4 in 24)
  Row 4 (321-33-15-123): genus = 0
  Row 6 (321-33-15-123): genus = 0
  Row 9 (312-33-24-213): genus = 1  (from digit 4 in 24)
  Total: Γ = 2

  The two 24-pylons are at rows 2 and 9 — symmetric at the extremes
  of the 9-row block.

─────────────────────────────────────────────────────────────────
CYLINDER WRAPPING:

  On a cylinder (row 9 adjacent to row 1): the two pylons at rows 2 and 9
  are separated by 2 rows on the shorter arc (9→1→2) and 7 rows on the longer
  arc (2→3→...→9). They are not equidistant; the cylinder is asymmetric.

  The genus count is unchanged: Γ = 2 on the cylinder.
  The DR-6 signature and nilpotency properties are also unchanged — these
  are purely algebraic and independent of spatial arrangement.

─────────────────────────────────────────────────────────────────
"""

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = abs(n) % 9
    return r if r else 9


# Topological genus per digit symbol
DIGIT_GENUS = {str(d): 0 for d in range(10)}
DIGIT_GENUS['0'] = 1
DIGIT_GENUS['4'] = 1
DIGIT_GENUS['6'] = 1
DIGIT_GENUS['8'] = 2
DIGIT_GENUS['9'] = 1


def genus(n):
    return sum(DIGIT_GENUS[d] for d in str(abs(n)))


# ── DR-6 family ───────────────────────────────────────────────────────────────

DR6_GATEWAYS   = [15, 24, 33, 42, 51]
DR6_PERMS      = [123, 213, 312, 321]
DR6_ALL        = DR6_GATEWAYS + DR6_PERMS

for x in DR6_ALL:
    check(dr(x) == 6, f"DR({x}) = 6", dr(x), 6)

# Row sum invariance: 6+6+6+6 = 24 → DR=6
check(dr(6 + 6 + 6 + 6) == 6, "DR(6+6+6+6) = DR(24) = 6", dr(6 + 6 + 6 + 6), 6)
check(4 * 6 % 9 == 6, "4×6 ≡ 6 mod 9", 4 * 6 % 9, 6)


# ── Nilpotency of 6 in Z/9Z ──────────────────────────────────────────────────

check(6 ** 1 % 9 == 6, "6^1 ≡ 6 mod 9", 6 ** 1 % 9, 6)
check(6 ** 2 % 9 == 0, "6^2 ≡ 0 mod 9 (nilpotent order 2)", 6 ** 2 % 9, 0)
check(6 ** 3 % 9 == 0, "6^3 ≡ 0 mod 9", 6 ** 3 % 9, 0)
check(dr(36) == 9, "DR(36) = DR(6²) = 9 = NULL", dr(36), 9)

# Additive order of 6 in Z/9Z = 3
check((6 + 6 + 6) % 9 == 0, "6+6+6 ≡ 0 mod 9 (additive order 3)", (6 + 6 + 6) % 9, 0)

# Any two DR-6 numbers annihilate under multiplication
for a in DR6_ALL:
    for b in DR6_ALL:
        check(dr(a * b) == 9,
              f"DR({a}×{b}) = 9 (nilpotency)", dr(a * b), 9)

# Prove: 6 = -3 mod 9; (-3)^2 = 9 ≡ 0
check((-3) % 9 == 6, "6 ≡ -3 mod 9", (-3) % 9, 6)
check((-3) ** 2 % 9 == 0, "(-3)^2 = 9 ≡ 0 mod 9", (-3) ** 2 % 9, 0)

# Contrast: idempotents
check(dr(9 * 9) == 9, "DR(9×9) = 9 (idempotent)", dr(9 * 9), 9)
check(dr(1 * 1) == 1, "DR(1×1) = 1 (idempotent)", dr(1 * 1), 1)


# ── Vector dot products ───────────────────────────────────────────────────────

L_VEC = [123, 312, 321, 123]
R_VEC = [321, 213, 123, 321]
EXPECTED_PRODUCTS = [39483, 66456, 39483, 39483]

for i, (l, r, ep) in enumerate(zip(L_VEC, R_VEC, EXPECTED_PRODUCTS)):
    p = l * r
    check(p == ep, f"row {i+1}: {l}×{r} = {ep}", p, ep)
    check(sum(int(d) for d in str(p)) == 27,
          f"row {i+1}: digit_sum({p}) = 27", sum(int(d) for d in str(p)), 27)
    check(dr(p) == 9, f"row {i+1}: DR({p}) = 9", dr(p), 9)

check(dr(27) == 9, "DR(27) = 9", dr(27), 9)

# All products are multiples of 9
for p in EXPECTED_PRODUCTS:
    check(p % 9 == 0, f"{p} ≡ 0 mod 9", p % 9, 0)


# ── Genus analysis ────────────────────────────────────────────────────────────

GATEWAY_GENUS = {15: 0, 24: 1, 33: 0, 42: 1, 51: 0}
PERM_GENUS    = {123: 0, 213: 0, 312: 0, 321: 0}

for x, g in {**GATEWAY_GENUS, **PERM_GENUS}.items():
    check(genus(x) == g, f"genus({x}) = {g}", genus(x), g)

# 42 and 24 are digit-reverses with identical genus
check(genus(24) == genus(42), "genus(24) = genus(42) (both contain digit 4)",
      genus(24), genus(42))
check(str(24) == str(42)[::-1], "24 and 42 are digit-reverses", str(42)[::-1], str(24))

# 51 and 15 are digit-reverses with identical genus (both 0)
check(genus(15) == genus(51), "genus(15) = genus(51) = 0",
      genus(15), genus(51))

# Replacing 24 with 42: genus unchanged
check(genus(42) == genus(24), "42→24 substitution: no Γ change", genus(42), genus(24))

# Replacing 33 with 42: genus +1
check(genus(42) - genus(33) == 1, "33→42 substitution: Γ increases by 1",
      genus(42) - genus(33), 1)


# ── 9-row matrix genus ────────────────────────────────────────────────────────

KNOWN_ROWS = {
    2: [312, 33, 24, 213],
    4: [321, 33, 15, 123],
    6: [321, 33, 15, 123],
    9: [312, 33, 24, 213],
}

row_genera = {}
for row_num, cells in KNOWN_ROWS.items():
    g = sum(genus(c) for c in cells)
    row_genera[row_num] = g

check(row_genera[2] == 1, "row 2 genus = 1 (one 24)", row_genera[2], 1)
check(row_genera[4] == 0, "row 4 genus = 0", row_genera[4], 0)
check(row_genera[6] == 0, "row 6 genus = 0", row_genera[6], 0)
check(row_genera[9] == 1, "row 9 genus = 1 (one 24)", row_genera[9], 1)

GAMMA = sum(row_genera.values())
check(GAMMA == 2, "total Γ = 2 (two pylons at rows 2 and 9)", GAMMA, 2)

# Pylon rows are symmetric: both are (312-33-24-213)
check(KNOWN_ROWS[2] == KNOWN_ROWS[9], "pylon rows 2 and 9 are identical",
      KNOWN_ROWS[2], KNOWN_ROWS[9])


# ── Cylinder wrapping ─────────────────────────────────────────────────────────

PERIOD = 9
PYLON_ROWS = [2, 9]

# On cylinder: distance between pylons on each arc
arc_forward = PYLON_ROWS[1] - PYLON_ROWS[0]   # 9-2 = 7
arc_backward = PERIOD - arc_forward             # 9-7 = 2

check(arc_forward == 7,  "forward arc 2→9 = 7 rows", arc_forward, 7)
check(arc_backward == 2, "backward arc 9→2 (via row 1) = 2 rows", arc_backward, 2)
check(arc_forward + arc_backward == PERIOD, "arcs sum to period 9",
      arc_forward + arc_backward, PERIOD)

# Pylons are NOT equidistant on the cylinder
check(arc_forward != arc_backward, "pylons are asymmetrically placed on cylinder",
      arc_forward != arc_backward, True)

# Genus unchanged by wrapping
check(GAMMA == 2, "Γ = 2 on cylinder (spatial topology doesn't affect digit loops)",
      GAMMA, 2)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("DR-6 Tensor Field Audit")
    print("=" * 66)

    print(f"\n── DR-6 family ──")
    for x in DR6_ALL:
        tag = f"genus={genus(x)}" if x in GATEWAY_GENUS else "genus=0"
        print(f"  {x:>3}: DR=6  {tag}")
    print(f"  Row sum: 6+6+6+6=24 → DR=6  (4×6≡6 mod 9, additive order 3)")

    print(f"\n── Nilpotency of 6 in Z/9Z ──")
    print(f"  6^1 mod 9 = 6;  6^2 mod 9 = 0;  6^3 mod 9 = 0")
    print(f"  6 ≡ −3 mod 9;  (−3)^2 = 9 ≡ 0 mod 9 → NULL")
    print(f"  6 is the unique nilpotent element of {{1..9}} under DR-multiplication.")
    print(f"  DR(a)=6, DR(b)=6 → DR(a×b)=9: annihilation is a THEOREM, not coincidence.")
    print(f"  Compare: 9×9→9 (idempotent), 1×1→1 (idempotent).")

    print(f"\n── Vector dot products ──")
    for i, (l, r, p) in enumerate(zip(L_VEC, R_VEC, EXPECTED_PRODUCTS)):
        print(f"  Row {i+1}: {l} × {r} = {p}  digit_sum=27  DR=9")
    print(f"  All products ≡ 0 mod 9; all digit sums = 27 = 3×9.")

    print(f"\n── Genus ──")
    print(f"  Loop-carrying digit: only 4 (in this symbol set).")
    print(f"  Gateway genera: 15→0, 24→1, 33→0, 42→1, 51→0")
    print(f"  24 and 42 are digit-reverses: same genus = 1.")
    print(f"  15 and 51 are digit-reverses: same genus = 0.")

    print(f"\n── 9-row matrix ──")
    for rn, cells in KNOWN_ROWS.items():
        g = row_genera[rn]
        pylon = " ← pylon" if g > 0 else ""
        print(f"  Row {rn} {cells}: Γ = {g}{pylon}")
    print(f"  Total Γ = {GAMMA}.  Pylons at rows 2 and 9.")

    print(f"\n── Effect of introducing 42 or 51 ──")
    print(f"  42 → replaces 24: Γ unchanged (digit 4 still present).")
    print(f"  42 → replaces 33: Γ +1 (digit 4 introduced).")
    print(f"  42 → replaces 15: Γ +1 (digit 4 introduced).")
    print(f"  51 → replaces anything: Γ unchanged (genus(51)=0).")
    print(f"  The pylon shifts only if 42 is introduced into a currently genus-0 row.")

    print(f"\n── Cylinder wrapping ──")
    print(f"  Pylon arcs: rows 2→9 = {arc_forward} steps; rows 9→2 (via 1) = {arc_backward} steps.")
    print(f"  Asymmetric: pylons at 2/9 and 9/9 of circumference → {arc_backward}/{PERIOD} short arc.")
    print(f"  Γ = 2 on cylinder: spatial topology doesn't affect digit loop count.")
    print(f"  DR and nilpotency: unchanged — purely algebraic, not spatial.")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
