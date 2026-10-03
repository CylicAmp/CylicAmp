# CLASS: AUDIT
"""
Total correlation of an exchangeable two-component Bernoulli mixture (supplied
computation, 2026-09-28; reproduced and completed).

Model: a fair latent coin picks p in {0.9, 0.1}; X_1..X_n are then i.i.d.
Bernoulli(p). Every marginal is Bernoulli(q = 1/2).

VERIFIED
  * TC(X_1..X_n) = sum H(X_i) - H(X^n) = n - H(X^n) equals D(P || prod P_i) exactly
    (a general identity); the supplied numerical check agrees to <= 1e-11 at
    n = 1000 (floating-point accumulation over n + 1 terms).
ASYMPTOTICS (proved): the components become distinguishable exponentially fast,
  so H(X^n) = n h2(0.9) + H(latent) - o(1), hence
      TC(n) = n (1 - h2(0.9)) - 1 + o(1)      (bits),
  TC/n -> 1 - h2(0.9) = 0.531004, and the offset TC - 0.531004 n -> -1 bit (the
  entropy of the latent coin): -0.99731 (n = 10), -0.99999 (20), -1.00000 (50+).
"""
import math
pa, pb, q = 0.9, 0.1, 0.5
h2 = lambda p: 0.0 if p in (0, 1) else -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def tc(n):
    H = KL = 0.0
    for k in range(n + 1):
        mult = math.comb(n, k)
        ps = 0.5 * pa**k * (1 - pa)**(n - k) + 0.5 * pb**k * (1 - pb)**(n - k)
        if ps:
            H -= mult * ps * math.log2(ps)
            KL += mult * ps * math.log(ps / (q**k * (1 - q)**(n - k)))
    T = n * h2(q) - H
    return T, abs(KL - T * math.log(2))


LIM = 1 - h2(0.9)
assert abs(LIM - 0.531004) < 1e-6
for n in (10, 20, 50, 100, 250):
    T, err = tc(n)
    assert err < 1e-11
assert abs(tc(50)[0] - 50 * LIM + 1) < 1e-4 and abs(tc(250)[0] - 250 * LIM + 1) < 1e-9

if __name__ == "__main__":
    print("TC(n) = n(1 - h2(0.9)) - 1 + o(1); slope", round(LIM, 6))
