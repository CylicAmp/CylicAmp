"""
twin_prime_markov_audit.py

Markov transition analysis of twin prime DR tracks.

─────────────────────────────────────────────────────────────────
SETUP:
  Twin prime pairs (p, p+2) with p > 3 fall into exactly three
  DR tracks (proven in twin_prime_tripartite_audit.py):

    Track A:  DR(p) = 2,  DR(p+2) = 4
    Track B:  DR(p) = 5,  DR(p+2) = 7
    Track C:  DR(p) = 8,  DR(p+2) = 1

  This file asks: given the current twin pair is in track X,
  what is the track of the NEXT twin pair?

CLAIMS UNDER TEST:
  (M1) The 3×3 transition matrix is approximately doubly stochastic.
  (M2) The stationary distribution converges to (1/3, 1/3, 1/3).
  (M3) Mutual information I(Xn ; Xn+1) is near zero and decreases
       with N — tracks are nearly independent.
  (M4) Diagonal entries of P are slightly < 1/3 (weak anti-persistence).
  (M5) MI(N ≤ 10^4) ≈ 0.103, MI(N ≤ 10^5) ≈ 0.007, MI(N ≤ 10^6) ≈ 0.004
       — consistent with MI → 0 as N → ∞.

EMPIRICAL RESULTS (N ≤ 10^6):
  Twin pairs (p > 3):  8 168   (excludes (3,5) whose DR(3) = 3 ∉ {2,5,8})
  Track A:  2 651  (32.46%)
  Track B:  2 788  (34.13%)
  Track C:  2 729  (33.41%)

  Transition matrix P[i][j] = P(next = j | current = i):
             A       B       C
    A:  [0.3067, 0.3663, 0.3270]
    B:  [0.3226, 0.3053, 0.3721]
    C:  [0.3441, 0.3536, 0.3023]

  Stationary distribution:  A = 0.3246,  B = 0.3413,  C = 0.3341
  H(X) = 1.5847 bits  (uniform max = log₂3 = 1.5850 bits)
  I(Xn ; Xn+1) = 0.003820 bits  (0.24% of H(X))

  MI vs bound:
    N ≤ 10^4:  204 pairs   MI = 0.102882 bits
    N ≤ 10^5: 1 223 pairs  MI = 0.006720 bits
    N ≤ 10^6: 8 168 pairs  MI = 0.003820 bits
─────────────────────────────────────────────────────────────────
"""

from math import isqrt, log2
from collections import Counter

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


# ── Sieve ─────────────────────────────────────────────────────────────────────

def sieve(n):
    ip = bytearray([1]) * (n + 1)
    ip[0] = ip[1] = 0
    for i in range(2, isqrt(n) + 1):
        if ip[i]:
            ip[i * i :: i] = bytearray(len(ip[i * i :: i]))
    return ip


def dr(n):
    if n == 0:
        return 0
    r = n % 9
    return r if r else 9


BOUND = 10 ** 6
IP = sieve(BOUND)

twins = sorted(
    (p, p + 2)
    for p in range(5, BOUND - 1)
    if IP[p] and p + 2 <= BOUND and IP[p + 2]
)

check(len(twins) == 8168, "twin count (p>3, N≤10^6)", len(twins), 8168)
check(twins[0]  == (5, 7),             "first twin", twins[0],  (5, 7))
check(twins[-1] == (999959, 999961),   "last twin",  twins[-1], (999959, 999961))


# ── Track assignment ───────────────────────────────────────────────────────────

def track(p):
    d = dr(p)
    if d == 2: return 0   # A
    if d == 5: return 1   # B
    if d == 8: return 2   # C
    return -1             # only (3,5) hits this


tracks = [track(p) for p, _ in twins]

tc = Counter(tracks)
check(tc[0] == 2651, "Track A count", tc[0], 2651)
check(tc[1] == 2788, "Track B count", tc[1], 2788)
check(tc[2] == 2729, "Track C count", tc[2], 2729)
check(sum(tc[i] for i in range(3)) == 8168, "tracks sum", sum(tc[i] for i in range(3)), 8168)


# ── Transition matrix ──────────────────────────────────────────────────────────

trans = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
for i in range(len(tracks) - 1):
    a, b = tracks[i], tracks[i + 1]
    if a >= 0 and b >= 0:
        trans[a][b] += 1

row_sums = [sum(r) for r in trans]

check(trans[0] == [813, 971, 867],  "row A counts", trans[0], [813, 971, 867])
check(trans[1] == [899, 851, 1037], "row B counts", trans[1], [899, 851, 1037])
check(trans[2] == [939, 965, 825],  "row C counts", trans[2], [939, 965, 825])

prob = [
    [trans[i][j] / row_sums[i] for j in range(3)]
    for i in range(3)
]

# M4: Diagonal entries all < 1/3
for i, label in enumerate("ABC"):
    check(
        prob[i][i] < 1 / 3,
        f"anti-persistence P({label}→{label}) < 1/3",
        round(prob[i][i], 4),
        f"< {1/3:.4f}",
    )

# Row-stochastic sanity
for i in range(3):
    check(
        abs(sum(prob[i]) - 1.0) < 1e-12,
        f"row {i} sums to 1",
        sum(prob[i]),
        1.0,
    )


# ── Stationary distribution (power iteration) ─────────────────────────────────

pi = [1 / 3, 1 / 3, 1 / 3]
for _ in range(2000):
    pi2 = [sum(pi[k] * prob[k][j] for k in range(3)) for j in range(3)]
    s = sum(pi2)
    pi = [x / s for x in pi2]

# Stationary should be close to empirical frequencies
for i, label in enumerate("ABC"):
    emp = tc[i] / 8168
    check(abs(pi[i] - emp) < 0.01, f"π_{label} ≈ empirical", round(pi[i], 4), round(emp, 4))

H_stat = -sum(x * log2(x) for x in pi if x > 0)
H_max  = log2(3)
check(abs(H_stat - H_max) < 0.01, "H near log₂3", round(H_stat, 4), round(H_max, 4))


# ── Mutual information ────────────────────────────────────────────────────────

pairs = [
    (tracks[i], tracks[i + 1])
    for i in range(len(tracks) - 1)
    if tracks[i] >= 0 and tracks[i + 1] >= 0
]
M = len(pairs)

joint = [[0] * 3 for _ in range(3)]
for a, b in pairs:
    joint[a][b] += 1
joint = [[joint[i][j] / M for j in range(3)] for i in range(3)]

marg_r = [sum(joint[i]) for i in range(3)]
marg_c = [sum(joint[i][j] for i in range(3)) for j in range(3)]

MI = sum(
    joint[i][j] * log2(joint[i][j] / (marg_r[i] * marg_c[j]))
    for i in range(3)
    for j in range(3)
    if joint[i][j] > 0
)

check(abs(MI - 0.003820) < 1e-4, "MI(N=10^6)", round(MI, 6), 0.003820)
check(MI / H_stat < 0.003, "MI / H < 0.3%", round(MI / H_stat, 4), "< 0.003")


# ── MI vs N scaling (M5) ──────────────────────────────────────────────────────

def mi_at_bound(bound, ip_arr):
    tw = sorted(
        (p, p + 2)
        for p in range(5, bound - 1)
        if ip_arr[p] and p + 2 <= bound and ip_arr[p + 2]
    )
    tr = [track(p) for p, _ in tw]
    ps = [(tr[i], tr[i + 1]) for i in range(len(tr) - 1) if tr[i] >= 0 and tr[i + 1] >= 0]
    Mb = len(ps)
    if Mb == 0:
        return 0.0
    jt = [[0] * 3 for _ in range(3)]
    for a, b in ps:
        jt[a][b] += 1
    jt = [[jt[i][j] / Mb for j in range(3)] for i in range(3)]
    mr = [sum(jt[i]) for i in range(3)]
    mc = [sum(jt[i][j] for i in range(3)) for j in range(3)]
    return sum(
        jt[i][j] * log2(jt[i][j] / (mr[i] * mc[j]))
        for i in range(3) for j in range(3) if jt[i][j] > 0
    )


mi_1e4 = mi_at_bound(10 ** 4, IP)
mi_1e5 = mi_at_bound(10 ** 5, IP)

check(abs(mi_1e4 - 0.102882) < 0.001, "MI(N=10^4)", round(mi_1e4, 6), 0.102882)
check(abs(mi_1e5 - 0.006720) < 0.0002, "MI(N=10^5)", round(mi_1e5, 6), 0.006720)
check(mi_1e5 < mi_1e4, "MI decreasing: 10^5 < 10^4", round(mi_1e5, 6), f"< {round(mi_1e4, 6)}")
check(MI    < mi_1e5, "MI decreasing: 10^6 < 10^5", round(MI, 6),    f"< {round(mi_1e5, 6)}")


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Twin Prime DR Track Markov Audit")
    print("=" * 62)

    print(f"\nBound N ≤ {BOUND:,}")
    print(f"  Twin pairs (p > 3): {len(twins):,}")
    print(f"  First: {twins[0]}   Last: {twins[-1]}")

    print(f"\n── Track distribution ──")
    for i, label in enumerate("ABC"):
        d_lo = [2, 5, 8][i]
        d_hi = [4, 7, 1][i]
        print(f"  Track {label} (DR {d_lo}→{d_hi}): {tc[i]:>4}  ({100*tc[i]/8168:.2f}%)")

    print(f"\n── Transition matrix P[i][j] ──")
    print(f"       {'A':>7}  {'B':>7}  {'C':>7}")
    for i, label in enumerate("ABC"):
        row = "  ".join(f"{prob[i][j]:.4f}" for j in range(3))
        print(f"  {label}: {row}")

    print(f"\n── Stationary distribution ──")
    for i, label in enumerate("ABC"):
        print(f"  π_{label} = {pi[i]:.4f}")
    print(f"  H(X) = {H_stat:.6f} bits  (log₂3 = {H_max:.6f})")

    print(f"\n── Anti-persistence (M4) ──")
    for i, label in enumerate("ABC"):
        print(f"  P({label}→{label}) = {prob[i][i]:.4f}  < 1/3 = {1/3:.4f}:  "
              f"{'YES' if prob[i][i] < 1/3 else 'NO'}")
    print("  Interpretation: consecutive identical tracks are slightly suppressed.")

    print(f"\n── Mutual information ──")
    print(f"  I(Xn ; Xn+1) = {MI:.6f} bits")
    print(f"  MI / H(X)    = {MI/H_stat:.4%}  (near-zero → tracks nearly independent)")

    print(f"\n── MI vs N (M5) ──")
    for bound, mi_val in [(10**4, mi_1e4), (10**5, mi_1e5), (BOUND, MI)]:
        print(f"  N ≤ {bound:>7,}: MI = {mi_val:.6f} bits")
    print("  Trend: MI → 0 as N → ∞  (consistent with equidistribution)")

    print(f"\n── Connection to Hardy–Littlewood ──")
    print("  The H-L conjecture B implies π_{A,B,C}(N) ~ N / (3 log N)² each.")
    print("  Near-uniform track weights confirmed empirically.")
    print("  H-L constant C₂ = 0.6601618... governs total twin prime density;")
    print("  relative track weights are controlled by equidistribution (not C₂).")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
