# CLASS: LEMMA
"""
Owner's nine-row digit ladder (image, 2026-10-04):
    12312 23514 34716 45918 56220 67422 78624 89826 91128

RULE (fits all 9 rows, verified below): row a = 1..9 is the concatenation
    a | DR(a+1) | DR(2a+1) | 2a+10
where DR is the digital root. The reduction is DR, not mod 10:
  - row 5..8 middle digit is 2,4,6,8 = DR(11..17); mod 10 would give 1,3,5,7;
  - row 9 second digit is 1 = DR(10); mod 10 would give 0.
With no reduction at all, only rows 1-4 match (row 5 would be 561120).

FORCED CONSEQUENCES (proved, not observed):
  - DR(row a) = DR(6a+3): every column contributes a, a+1, 2a+1, 2a+1 mod 9.
    So DR runs 9,6,3 with period 3, and every row is divisible by 3.
  - Last digit is even, so every row is divisible by 6.
  - Consecutive difference is 11202 = 10000+1000+200+2 while no column wraps.
    Middle wraps between rows 4 and 5 (9 -> 2, i.e. -900 vs no wrap): 10302.
    Second and middle both wrap between rows 8 and 9 (-9000, -900): 1302.

FALSIFICATION: any assertion below failing.
"""
N = [12312, 23514, 34716, 45918, 56220, 67422, 78624, 89826, 91128]

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def row(a):
    return int(f"{a}{dr(a + 1)}{dr(2 * a + 1)}{2 * a + 10}")

assert [row(a) for a in range(1, 10)] == N
assert [int(f"{a}{(a+1)%10}{(2*a+1)%10}{2*a+10}") for a in range(1, 10)] != N
assert [int(f"{a}{a+1}{2*a+1}{2*a+10}") for a in range(1, 10)][:4] == N[:4]
assert [int(f"{a}{a+1}{2*a+1}{2*a+10}") for a in range(1, 10)][4] == 561120

assert [dr(n) for n in N] == [dr(6 * a + 3) for a in range(1, 10)] == [9, 6, 3] * 3
assert all(n % 6 == 0 for n in N)

diffs = [N[i + 1] - N[i] for i in range(8)]
assert diffs == [11202, 11202, 11202, 10302, 11202, 11202, 11202, 1302]
assert 11202 - 900 == 10302 and 11202 - 9000 - 900 == 1302

FACTORS = {12312: "2^3*3^4*19", 23514: "2*3*3919", 34716: "2^2*3*11*263",
           45918: "2*3^2*2551", 56220: "2^2*3*5*937", 67422: "2*3*17*661",
           78624: "2^5*3^3*7*13", 89826: "2*3*11*1361", 91128: "2^3*3*3797"}
for n, f in FACTORS.items():
    v = 1
    for t in f.split("*"):
        p, _, e = t.partition("^")
        v *= int(p) ** int(e or 1)
    assert v == n, n

if __name__ == "__main__":
    for a, n in enumerate(N, 1):
        print(a, n, f"= {a}|{dr(a+1)}|{dr(2*a+1)}|{2*a+10}", "DR", dr(n), FACTORS[n])
    print("diffs", diffs)
    print("all assertions pass")
