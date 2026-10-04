"""
adjacent_pair_sum_audit.py

For a 3-digit number ABC:
  p1 = A+B          (raw digit sum of first pair)
  p2 = DR(B+C)      (digital root of second pair)
  S  = p1 + p2
  result = [d1][d2][d1+d2]  where d1,d2 are digits of S

VERIFIED CASES:
  357: p1=3+5=8,  p2=DR(5+7)=DR(12)=3, S=11 → 112  (1+1=2)
  573: p1=5+7=12, p2=DR(7+3)=DR(10)=1, S=13 → 134  (1+3=4)
  224: p1=2+2=4,  p2=DR(2+4)=6,         S=10 → 101  (1+0=1)
  481: p1=4+8=12, p2=DR(8+1)=9,         S=21 → 213  (2+1=3)
  815: p1=8+1=9,  p2=DR(1+5)=6,         S=15 → 156  (1+5=6)
  152: p1=1+5=6,  p2=DR(5+2)=7,         S=13 → 134  (1+3=4)

CORRECTIONS:
  235 → 234: p1=5, p2=DR(7)=7, S=12 → 123  (original 235 gives S=13 → 134)
  724 → 824: p1=10, p2=DR(6)=6, S=16 → 167  (724 gives p1=9, S=15 → 156)
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
    r = n % 9
    return r if r else 9


def pair_result(abc):
    """p1=A+B (raw), p2=DR(B+C), S=p1+p2, result=[d1][d2][d1+d2]."""
    a, b, c = abc // 100, (abc // 10) % 10, abc % 10
    p1 = a + b
    p2 = dr(b + c)
    S = p1 + p2
    assert S >= 10, f"S={S} < 10, rule requires two-digit sum"
    d1, d2 = S // 10, S % 10
    return d1 * 100 + d2 * 10 + (d1 + d2), p1, p2, S


CASES = [
    (357, 112),
    (573, 134),
    (224, 101),
    (481, 213),
    (815, 156),
    (152, 134),
    (234, 123),
    (824, 167),
]

for inp, expected in CASES:
    result, p1, p2, S = pair_result(inp)
    check(result == expected, f"{inp}→{result}", result, expected)

# Original errors confirmed
result_235, p1_235, p2_235, S_235 = pair_result(235)
check(result_235 == 134, "235→134 (not 123)", result_235, 134)

result_724, p1_724, p2_724, S_724 = pair_result(724)
check(result_724 == 156, "724→156 (not 167)", result_724, 156)

# Last digit always = d1+d2
for inp, expected in CASES:
    result, p1, p2, S = pair_result(inp)
    d1, d2 = S // 10, S % 10
    check(result % 10 == d1 + d2, f"{inp} last digit check", result % 10, d1 + d2)

if __name__ == "__main__":
    print("Adjacent Pair Sum Audit — 3-digit numbers")
    print("=" * 62)
    print(f"\n  Rule: p1=A+B (raw), p2=DR(B+C), S=p1+p2, result=[d1][d2][d1+d2]")
    print(f"\n  {'input':>6}  {'p1':>4}  {'p2':>4}  {'S':>4}  {'result':>7}  note")
    print("  " + "-" * 52)
    for inp, expected in CASES:
        result, p1, p2, S = pair_result(inp)
        rev = int(str(result)[::-1])
        rev_str = str(rev) if rev != result else "palindrome"
        note = "← corrected" if inp in (234, 824) else ""
        print(f"  {inp:>6}  {p1:>4}  {p2:>4}  {S:>4}  {result}={rev_str}  {note}")
    print(f"\n  235→134 (original showed 123; input should be 234)")
    print(f"  724→156 (original showed 167; input should be 824)")
    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
