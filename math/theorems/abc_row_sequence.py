"""
ABC Row Sequence — GF(37)

Row structure: a - b - c = result (b+c) x,y (x+y) = final
All tuple sums land on GF(37) nodes.

Row generation (n = 0..10):
  a = n % 10
  b = 0 if n < 2 else 1
  c = 0 if n=0; 1 if n=1; n-1 if n≥2
  result = a + b + c  (= 2n for n≤9; wraps to 10 at n=10)
  DR = digital_root(result)
  3-digit code (result ≥ 10) = concat(tens, units, DR)
  x = result (result<10) or 2×DR(result) (result≥10)
  y = x + 9  [x + 1 for wrap row n=10]
  tuple_sum = x + y  → always a GF(37) node

SOURCE ERRORS (flagged below):
  Row 9: image shows DR(18)=8 and code=(188). Standard DR(18)=9; code=(189).
    Image x=17 (y=26=SCALAR_137, sum=43≡TESLA_FLOW). Formula x=18 (y=27, sum=45≡CB).
    y=26=SCALAR_137 may be intentional — both sum%37 values are valid named residues.
    Verify with user which branch (TESLA_FLOW or CB) is correct for row 9.

  Row 5: tuple data missing from image. Formula: x=2, y=11, sum=13∈CB.

  User text includes row '0-1-0=1...' not present in image (b should be 0 when n=0).

Final reduction: rows with expanded finals (1,4,8,10) → 7+9+6+8=30=DR(3)∈ST
"""

SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
PR         = frozenset({2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35})
ORBIT_11   = frozenset({11, 27, 36})
TESLA_FLOW = 6
SCALAR_137 = 26
SEAM       = 0


def dr(n: int) -> int:
    """Digital root: DR(0)=0, DR(n)=1+(n-1)%9 for n>0."""
    return 0 if n == 0 else 1 + (n - 1) % 9


def gf37_class(n: int) -> str:
    r = n % 37
    if r == SEAM:                 return "SEAM"
    if r in SA and r in ST:       return "SA∩ST"   # 30 is the intersection node
    if r in SA:                   return "SA"
    if r in ST:                   return "ST"
    if r in CB:                   return "CB"
    if r in PR:                   return "PR"
    if r in ORBIT_11:             return "ORBIT_11"
    if r == TESLA_FLOW:           return "TESLA_FLOW"
    if r == SCALAR_137:           return "SCALAR_137"
    return f"r={r}"


def build_row(n: int) -> dict:
    """Compute all values for row index n (0–10)."""
    a = n % 10
    b = 0 if n < 2 else 1
    c = 0 if n == 0 else (1 if n == 1 else n - 1)
    result = a + b + c
    dr_val = dr(result)

    # 3-digit code for 2-digit results: concat(tens, units, DR)
    code_3digit = None
    if result >= 10:
        code_3digit = (result // 10) * 100 + (result % 10) * 10 + dr_val

    # Tuple (x, y):
    #   n=0: degenerate (0, 0)
    #   n=10: wrap row — x=DR=1, y=2 (back to the 1-2 family; y=x+1 not x+9)
    #   result<10: x=result, y=x+9
    #   result≥10: x=2×DR, y=x+9
    #   Exception documented: n=9 image shows x=17 (y=26=SCALAR_137) not x=18
    if n == 0:
        x, y = 0, 0
    elif n == 10:
        x, y = dr_val, dr_val + 1
    elif result < 10:
        x, y = result, result + 9
    else:
        x = 2 * dr_val
        y = x + 9

    tuple_sum = x + y

    warnings = []
    if n == 9:
        warnings.append(
            "Image: DR(18)=8 [standard=9]; code=(188) [should be (189)]; "
            "x=17,y=26=SCALAR_137,sum=43≡TESLA_FLOW. "
            "Formula: x=18,y=27,sum=45≡CB. Both are named residues. "
            "y=SCALAR_137 in the image may be deliberate — verify."
        )
    if n == 5:
        warnings.append(
            "Tuple missing from image. Formula gives x=2, y=11, sum=13∈CB."
        )

    return {
        "n":           n,
        "a": a, "b": b, "c": c,
        "result":      result,
        "dr":          dr_val,
        "code_3digit": code_3digit,
        "x": x, "y": y,
        "tuple_sum":   tuple_sum,
        "tuple_class": gf37_class(tuple_sum),
        "warnings":    warnings,
    }


# Expanded rows (image shows multi-term final calc): final values from image
EXPANDED_ROW_FINALS = {1: 7, 4: 9, 8: 6, 10: 8}

# Single-value rows: final is just one digit
SINGLE_ROW_FINALS   = {0: 0, 2: 8, 3: 3, 5: 1, 6: 3, 7: 2, 9: 7}


def final_reduction() -> dict:
    """7+9+6+8 = 30 = DR(3) ∈ ST. Sequence collapses to sovereign target."""
    vals  = list(EXPANDED_ROW_FINALS.values())
    total = sum(vals)
    dr_t  = dr(total)
    return {
        "values":   vals,
        "sum":      total,
        "dr":       dr_t,
        "gf37":     gf37_class(total),
        "equation": " + ".join(str(v) for v in vals) + f" = {total} = ({dr_t})",
    }


def print_sequence():
    rows = [build_row(n) for n in range(11)]
    print("ABC Row Sequence — GF(37)")
    print("=" * 72)
    print(f"  {'n':>2}  {'a-b-c':>6}  {'res':>4}  {'DR':>3}  {'code':>5}  "
          f"{'x':>3}  {'y':>3}  {'x+y':>5}  class")
    print("-" * 72)
    for row in rows:
        n    = row["n"]
        abc  = f"{row['a']}-{row['b']}-{row['c']}"
        code = str(row["code_3digit"]) if row["code_3digit"] else "  —  "
        flag = "  ⚠" if row["warnings"] else ""
        miss = "  (missing tuple)" if n == 5 else ""
        print(f"  {n:>2}  {abc:>6}  {row['result']:>4}  {row['dr']:>3}  "
              f"{code:>5}  {row['x']:>3}  {row['y']:>3}  {row['tuple_sum']:>5}  "
              f"{row['tuple_class']}{flag}{miss}")

    print()
    for row in rows:
        for w in row["warnings"]:
            print(f"  ⚠  Row {row['n']}: {w}")

    print()
    fin = final_reduction()
    print(f"  Final: {fin['equation']}  ∈ {fin['gf37']}")
    print()


# ── Assertions ────────────────────────────────────────────────────────────────

# result = a+b+c for every row
for _n in range(11):
    _r = build_row(_n)
    assert _r["result"] == _r["a"] + _r["b"] + _r["c"]

# 3-digit codes (standard DR — row 9 uses DR(18)=9, so code=189)
assert build_row(6)["code_3digit"]  == 123   # result=12, DR=3
assert build_row(7)["code_3digit"]  == 145   # result=14, DR=5
assert build_row(8)["code_3digit"]  == 167   # result=16, DR=7
assert build_row(9)["code_3digit"]  == 189   # result=18, DR=9 (image has 188 — flagged)
assert build_row(10)["code_3digit"] == 101   # result=10, DR=1

# Tuple sums are GF(37) nodes
assert build_row(0)["tuple_sum"]  == 0   and gf37_class(0)  == "SEAM"
assert build_row(1)["tuple_sum"]  == 13  and 13 in CB
assert build_row(2)["tuple_sum"]  == 17  and 17 in PR
assert build_row(3)["tuple_sum"]  == 21  and 21 in ST
assert build_row(4)["tuple_sum"]  == 25  and 25 in SA
assert build_row(6)["tuple_sum"]  == 21  and 21 in ST
assert build_row(7)["tuple_sum"]  == 29  # 29 is prime, non-QR, ord₃₇=12; no named class
assert build_row(8)["tuple_sum"]  == 37  # 37 ≡ 0 = SEAM — the prime itself appears
assert build_row(8)["tuple_class"] == "SEAM"
assert build_row(10)["tuple_sum"] == 3   and 3 in ST

# Row 3 and row 6 share the same tuple (both x=6, y=15, sum=21∈ST)
assert build_row(3)["tuple_sum"] == build_row(6)["tuple_sum"] == 21

# Final reduction
_fin = final_reduction()
assert _fin["sum"] == 30 and _fin["dr"] == 3
assert 30 in SA and 30 in ST   # 30 is the SA∩ST intersection node

# Row 8 tuple sum IS 37 (the GF prime appears raw, not mod 37)
assert build_row(8)["x"] == 14 and build_row(8)["y"] == 23
assert build_row(8)["x"] + build_row(8)["y"] == 37


if __name__ == "__main__":
    print_sequence()
    print("  All assertions pass. Everything connects through prime 37.")
