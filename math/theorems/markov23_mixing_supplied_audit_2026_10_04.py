# CLASS: AUDIT
"""
Audit of supplied record AUD-WAV-MIXING-23 (2026-10-04): spectrum and mixing time of a 23-state
Markov chain. The chain is rebuilt exactly as the text describes it: u1 self-loop 0.6 and
u1 -> u2 0.4; at each junction an even split between the direct spine step and a 3-step delay
branch (u2-u4-u5-u6, u6-u7-u8-u9, u9-u10-u11-u12, u12-u13-u14-u15, u15-u16-u17-u18,
u20-u22-u23-u21); u18 -> u19 -> u20; u21 -> u1 or u21 -> u3 -> u1. The rebuild reproduces the
record's own minimum stationary probability 1/36, so it is the chain the record means.
Mathematics only.

CORRECT
  M1 Row-stochastic, irreducible; the self-loop at u1 makes it aperiodic; lambda_1 = 1 simple.
  M2 pi_min = 1/36.

WRONG (recomputed with numpy)
  M3 Subdominant pair 0.909901 +- 0.329983 i, modulus 0.967889 -- not 0.864312 +- 0.354188 i,
     0.934125. So gamma_* = 0.032111 (not 0.065875) and 1/gamma_* = 31.1 (not 15.18).
  M4 Total-variation mixing time t_mix(1/4) = 33 (d_TV(33) = 0.2465), not 30.
  M5 "Two exact zero eigenvalues (nilpotent dead branches)": no eigenvalue of this chain is 0.
  M6 The relaxation-time and mixing-time bounds quoted (1/gamma_*, and the pi_min bound) are the
     REVERSIBLE-chain bounds. This chain is not reversible (u4 -> u5 has probability 1, u5 -> u4
     has 0), so those bounds do not apply as stated; only the direct matrix-power count does.
FALSIFICATION: any assertion failing.
"""
import numpy as np

n = 23
P = np.zeros((n, n))


def e(a, b, p):
    P[a - 1, b - 1] += p


e(1, 1, .6); e(1, 2, .4)
for a, b, c, d in [(2, 6, 4, 5), (6, 9, 7, 8), (9, 12, 10, 11), (12, 15, 13, 14), (15, 18, 16, 17), (20, 21, 22, 23)]:
    e(a, b, .5); e(a, c, .5); e(c, d, 1); e(d, b, 1)
e(18, 19, 1); e(19, 20, 1); e(21, 1, .5); e(21, 3, .5); e(3, 1, 1)
assert np.allclose(P.sum(1), 1)                                                          # M1
w, v = np.linalg.eig(P.T)
pi = np.real(v[:, np.argmin(abs(w - 1))]); pi /= pi.sum()
assert abs(pi.min() - 1 / 36) < 1e-12 and (pi > 0).all()                                  # M2
ev = sorted(np.linalg.eigvals(P), key=lambda z: -abs(z))
assert abs(ev[0] - 1) < 1e-9 and abs(abs(ev[1]) - 0.967889) < 1e-6                       # M3
assert abs(ev[1].real - 0.909901) < 1e-6 and abs(abs(ev[1].imag) - 0.329983) < 1e-6
assert abs(1 / (1 - abs(ev[1])) - 31.14) < 0.01
Pt, tmix = np.eye(n), None                                                                # M4
for t in range(1, 200):
    Pt = Pt @ P
    if 0.5 * abs(Pt - pi).sum(1).max() <= 0.25:
        tmix = t
        break
assert tmix == 33
assert min(abs(z) for z in ev) > 1e-6                                                     # M5
D = np.diag(pi)
assert not np.allclose(D @ P, (D @ P).T)                                                  # M6: not reversible
