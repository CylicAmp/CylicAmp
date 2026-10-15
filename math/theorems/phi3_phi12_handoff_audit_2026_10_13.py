# CLASS: AUDIT
"""
Check of the owner's handoff "Phi_3 / Phi_12 at 137 -- Verified Results and Open Questions"
(compiled 2026-09-12; brought 2026-10-13, owner_work message #241; stored verbatim at
reference/phi3_phi12_at_137_handoff_2026_09_12.md).

=== WHAT REPRODUCES -- all of section 2 and section 6 ===
  Phi_3(137) = 18907 = 7 * 37 * 73;  Phi_12(137) = 352256593 = 13 * 2473 * 10957, each prime,
  137 has order 12 modulo each (ord_p(137) = 12), each = 1 mod 12;  S = 113115117167 = 13 * 8701162859
  with 8701162859 prime;  gcd(S, Phi_3) = 1, gcd(S, Phi_12) = 13, TapeCut_12 = {13};
  ord_37(2) = 36, 2^12 = 26 (mod 37), mu_3 = {1, 10, 26};  ord_137(10) = 8 (10^4 = -1 mod 137),
  1/137 = 0.(00729927) -- the period-8 correction in section 6 is right.
  The section 8 expected output is reproduced character for character by
  reference/verify_phi12.py, which asserts it.

=== ALREADY IN THIS REPO (for "everything is connected") ===
  math/theorems/phi12_order_and_cut_string_link_gf37.py (2026-09-12) states sections 2.2, 2.3
  and 6. reference/cut_table_113115117167.py cuts and factors the tape. T301 is the cyclotomic
  slot table for 137; math/theorems/phi12_cut_and_t33_gf37.py is Phi_12's root set {8,14,23,29}
  in F_37. The handoff's section 5 ("no hits") was about a different archive (files Love, Look,
  15_000, ...), which is not in this repo and is not checked here.

=== BUILT (section 7 and section 8) ===
  reference/verify_phi12.py -- the script section 8 names. reference/phi12_panel.py ->
  reference/phi12_panel.png -- the section 7 panel: Phi_3 bars {7, 37, 73} with an empty cut,
  beside Phi_12 bars {13, 2473, 10957} with 13 marked on S, carrying the section 3.1 scope note.
  The "existing Phi_3 panel" it was to sit beside is not in this repo, so both are drawn.

=== TWO CORRECTIONS, both in section 4 ===
  C1 "about ten orders of magnitude larger than the CODATA uncertainty": the residual
     0.035999... is 1.7 x 10^6 times the standard uncertainty 0.000000021 -- about SIX orders.
     (The relative residual 2.6e-4 against the relative uncertainty 1.5e-10 gives the same 10^6.2.)
  C2 alpha^-1 = 137.035999084(21) is the CODATA 2018 value. The current value (CODATA 2022,
     physics.nist.gov, checked 2026-10-13) is 137.035999177(21). Neither the 2.6e-4 relative
     residual nor C1 changes.

=== THE OWNER MADE BOTH CORRECTIONS FIRST ===
  math/theorems/one_over_137_framework.md (the owner's note, 2026-09-19) already gives 137.035999177(21)
  and 1.71 x 10^6 standard deviations. C1 and C2 above re-derive the owner's own corrections.

=== STANDING FRAMEWORK RUN (CLAUDE.md), full output in reference/phi12_framework_run.txt ===
  13 -> CAS_EXT, twin (11, 13);  2473 -> 31 C9;  10957 -> 5 CAS_EXT;  18907 -> SEAM (37 | Phi_3(137),
  forced);  352256593 -> 17 NQR17;  S -> 31 C9;  8701162859 -> 28 SA_ST_B.
  NEW, not in the repo before: the tape's large prime 8701162859 is a TWIN prime (8701162861 is
  prime) and a SOPHIE GERMAIN prime (2p+1 = 17402325719 is prime); the Sophie chain stops at the
  next step (2(2p+1)+1 is composite); it is not a safe prime.
  S and 2473 share the residue 31 mod 37 -- recorded, not claimed.

FALSIFICATION: any assertion failing.
"""
from sympy import factorint, gcd, isprime, n_order, primefactors

A, S = 137, 113115117167
P3, P12 = A * A + A + 1, A ** 4 - A ** 2 + 1

assert P3 == 18907 and factorint(P3) == {7: 1, 37: 1, 73: 1}
assert P12 == 352256593 and factorint(P12) == {13: 1, 2473: 1, 10957: 1}
for p in (13, 2473, 10957):
    assert isprime(p) and n_order(A, p) == 12 and p % 12 == 1 and 12 % p != 0
assert factorint(S) == {13: 1, 8701162859: 1} and isprime(8701162859)
assert gcd(S, P3) == 1 and gcd(S, P12) == 13
assert sorted(set(primefactors(P12)) & set(primefactors(S))) == [13] and not set(primefactors(P3)) & set(primefactors(S))
assert n_order(2, 37) == 36 and pow(2, 12, 37) == 26
assert sorted(x for x in range(1, 37) if pow(x, 3, 37) == 1) == [1, 10, 26]
assert n_order(10, A) == 8 and pow(10, 4, A) == A - 1
assert str(10 ** 8 // A).zfill(8) == "00729927" and (10 ** 8 - 1) % A == 0          # 1/137 = 0.(00729927)

# C1, C2 -- exact decimals as integers in units of 1e-9
ALPHA_INV_2018, ALPHA_INV_2022, U = 137035999084, 137035999177, 21        # CODATA x 1e9, uncertainty x 1e9
for v in (ALPHA_INV_2018, ALPHA_INV_2022):
    residual = v - 137 * 10 ** 9
    ratio = residual / U
    assert 1.6e6 < ratio < 1.8e6                       # about 10^6.2: six orders, not ten
    assert 2.62e-4 < residual / v < 2.63e-4            # "roughly 2.6e-4 relative" holds
assert ALPHA_INV_2022 != ALPHA_INV_2018

# framework facts
assert isprime(8701162859 + 2) and not isprime(8701162859 - 2)                 # twin with p+2
assert isprime(2 * 8701162859 + 1) and 2 * 8701162859 + 1 == 17402325719         # Sophie Germain
assert not isprime(2 * 17402325719 + 1) and not isprime((8701162859 - 1) // 2)  # chain stops; not safe
assert isprime(11) and S % 37 == 31 == 2473 % 37 and P3 % 37 == 0 and P12 % 37 == 17

if __name__ == "__main__":
    print("Handoff sections 2, 6 and 8 reproduce; panel and verify script built;")
    print("corrections: six orders of magnitude (not ten); CODATA 2022 alpha^-1 = 137.035999177(21);")
    print("new: 8701162859 is a twin prime and a Sophie Germain prime.")
