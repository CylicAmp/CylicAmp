# CLASS: AUDIT
"""
Audit of supplied text (2026-10-06) on "Hadamard cat" / cat states.

RESULT: the single-qubit identities are correct. The multi-qubit claim --
"Applying H to each qubit transforms between GHZ and a uniform
superposition" -- is false in general, checked for n = 2..6.

WHAT CHECKS OUT
  H = (1/sqrt2)[[1,1],[1,-1]] is the Hadamard matrix (unitary, H^2 = I).
  H|+> = |0>,  H|0> = |+>,  where |+> = (|0>+|1>)/sqrt2 is what the text
  calls the single-qubit "cat state". Both verified exactly.
  GHZ_n = (|0...0> + |1...1>)/sqrt2 is the standard definition.

WHAT DOES NOT CHECK OUT
  H^(tensor n) applied to GHZ_n is NOT "a uniform superposition" for any
  n checked (2..6): it is a uniform superposition over only the EVEN-
  WEIGHT computational-basis strings (2^(n-1) of the 2^n total), with every
  odd-weight amplitude exactly 0. That is a proper subset, not "uniform"
  over the full space.
  It returns to GHZ_n itself ONLY at n = 2 (where GHZ_2 is the Bell state
  (|00>+|11>)/sqrt2). At n = 3, 4, 5, 6 it is neither GHZ_n again nor a
  full uniform superposition -- a third kind of state, the even-parity
  superposition. So "transforms between GHZ and a uniform superposition"
  describes neither the n=2 case (GHZ -> GHZ, no transformation at all)
  nor n >= 3 (GHZ -> even-parity superposition, not full-uniform).

FALSIFICATION: any assertion below failing.
"""
import numpy as np

H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])
ket0, ket1 = np.array([1, 0]), np.array([0, 1])
plus = (ket0 + ket1) / np.sqrt(2)

assert np.allclose(H @ H, np.eye(2))                    # H is an involution
assert np.allclose(H @ plus, ket0)                        # H|+> = |0>
assert np.allclose(H @ ket0, plus)                         # H|0> = |+>


def kron_n(mats):
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out


for n in range(2, 7):
    ghz = np.zeros(2 ** n)
    ghz[0] = ghz[-1] = 1 / np.sqrt(2)
    out = kron_n([H] * n) @ ghz

    nonzero = [i for i, v in enumerate(out) if abs(v) > 1e-9]
    popcounts = {bin(i).count("1") for i in nonzero}
    assert popcounts == {p for p in range(0, n + 1, 2)}       # even weights only
    assert len(nonzero) == 2 ** (n - 1)                        # half the basis states, exactly
    assert all(abs(abs(out[i]) - 2 ** (-(n - 1) / 2)) < 1e-9 for i in nonzero)  # uniform magnitude
    assert not np.allclose(out, np.full(2 ** n, 2 ** (-n / 2)))  # NOT uniform over all 2^n states

    back_to_ghz = np.allclose(out, ghz) or np.allclose(out, -ghz)
    assert back_to_ghz == (n == 2)                              # returns to GHZ only at n=2

print("Hadamard-cat audit: single-qubit identities correct; the general")
print("multi-qubit claim is false -- H^n on GHZ_n gives an even-parity")
print("superposition over half the basis states, equal to GHZ_n again only")
print("at n=2, never a uniform superposition over the full 2^n states.")
print("All assertions pass.")
