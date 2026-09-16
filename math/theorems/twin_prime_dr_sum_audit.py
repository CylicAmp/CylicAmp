"""
twin_prime_dr_sum_audit.py

For a twin prime pair (p, p+2) with p > 3:
  DR(p + (p+2)) = DR(2p+2) ∈ {3, 6, 9}

PROOF:
  p > 3 prime → p ≢ 0 (mod 3)
  p+2 prime → p ≢ 1 (mod 3)  [else p+2 ≡ 0 mod 3]
  Therefore p ≡ 2 (mod 3) for all twin primes p > 3.
  → p+1 ≡ 0 (mod 3) → sum = 2(p+1) ≡ 0 (mod 3)
  → DR(sum) ∈ {3, 6, 9}

MAPPING TO TRACK FRAMEWORK:
  DR(p) = 2 → 2p+2 ≡ 6 (mod 9) → DR(sum) = 6
  DR(p) = 5 → 2p+2 ≡ 3 (mod 9) → DR(sum) = 3
  DR(p) = 8 → 2p+2 ≡ 0 (mod 9) → DR(sum) = 9

  The {3,6,9} in the sum is the image of {2,5,8} in DR(p)
  under the map p → 2p+2. Same partition, different view.

EXCEPTION:
  (3, 5): 3+5=8, DR=8. p=3 is the only prime ≡ 0 (mod 3).
  Singular entry point. All pairs after (3,5) are locked in {3,6,9}.

WHAT THIS PROVES:
  Necessary condition — twin primes cannot produce DR(sum) outside {3,6,9}.
  The {3,6,9} constraint set is infinite.
  Attaching to an infinite set via necessary condition does NOT prove
  twin primes are infinite. That requires a density lower bound (open).
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


TWIN_PRIMES = [
    (3, 5), (5, 7), (11, 13), (17, 19), (29, 31),
    (41, 43), (59, 61), (71, 73), (101, 103), (107, 109),
    (137, 139), (149, 151), (179, 181), (191, 193), (197, 199),
    (227, 229), (239, 241), (269, 271), (281, 283), (311, 313),
]

# (3,5) exception
p, q = 3, 5
check(dr(p + q) == 8, "DR(3+5)=8", dr(p + q), 8)

# All pairs (p,p+2) with p > 3: DR(sum) ∈ {3,6,9}
for p, q in TWIN_PRIMES:
    if p == 3:
        continue
    s = p + q
    d = dr(s)
    check(d in {3, 6, 9}, f"DR({p}+{q})={d} ∈ {{3,6,9}}", d, "∈{3,6,9}")

# Track mapping: DR(p) → DR(sum)
TRACK_MAP = {2: 6, 5: 3, 8: 9}
for p, q in TWIN_PRIMES:
    if p == 3:
        continue
    dp = dr(p)
    ds = dr(p + q)
    check(dp in {2, 5, 8}, f"DR({p}) ∈ {{2,5,8}}", dp, "∈{2,5,8}")
    check(ds == TRACK_MAP[dp], f"DR({p})={dp} → DR(sum)={ds}", ds, TRACK_MAP[dp])

# Modular proof: p ≡ 2 (mod 3) for all twin p > 3
for p, q in TWIN_PRIMES:
    if p == 3:
        continue
    check(p % 3 == 2, f"{p} ≡ 2 mod 3", p % 3, 2)
    check((p + q) % 3 == 0, f"sum {p+q} ≡ 0 mod 3", (p + q) % 3, 0)

if __name__ == "__main__":
    print("Twin Prime DR(sum) Audit")
    print("=" * 62)
    print(f"\n  {'pair':>12}  {'sum':>6}  {'DR(sum)':>7}  {'DR(p)':>5}  {'track_check':>11}")
    print("  " + "-" * 50)
    for p, q in TWIN_PRIMES:
        s = p + q
        d = dr(s)
        dp = dr(p) if p > 3 else "—"
        note = "ENTRY" if p == 3 else ""
        print(f"  ({p},{q}){'':<6}  {s:>6}  {d:>7}  {str(dp):>5}  {note}")
    print(f"\n  Rule: p > 3 twin prime → p ≡ 2 (mod 3) → DR(sum) ∈ {{3,6,9}}")
    print(f"  Track map: DR(p)=2→6, DR(p)=5→3, DR(p)=8→9")
    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
