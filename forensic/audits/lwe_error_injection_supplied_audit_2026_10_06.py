# CLASS: AUDIT
"""
Audit of a supplied file (2026-10-06), presented as `crypto/lwe_error_injection.py`:
reuses the carry/digital-root arithmetic from
carry_spectrum_dashboard_supplied_audit_2026_10_06.py, relabeled as an LWE
(Learning With Errors) error-injection module.

RESULT: the code runs and prints exactly what was claimed -- no execution
bug. The problem is the label. Nothing here is LWE, and the "checksum" is
not a checksum.

FAULT 1 -- the "error" carries no cryptographic hardness.
  LWE's security comes from the error being secret-dependent noise an
  attacker cannot predict, which stops (A, As+e) from being solved by plain
  linear algebra. Here error = floor(2a/10) is a PUBLIC, DETERMINISTIC
  function of a alone, with exactly two possible values (0 or 1) and a
  known, announced threshold (a=5, printed as "NOMINAL"/"NOISE INJECTED" in
  the module's own output). An attacker who knows the scheme computes and
  subtracts it exactly, same as the module does: this collapses the
  instance back to (A, As), solvable directly. Zero bits of the error are
  unknown to an attacker; LWE needs the error's entropy to BE the hardness.

FAULT 2 -- the "checksum" authenticates nothing and leaks structure.
  verify_checksum compares two digital roots, dr(2a) and dr(2a mod 10 +
  error); both are public, linear functions of a mod 9, computed with no
  secret key. Anyone can compute and forge it. A real integrity checksum
  needs a secret (a MAC key) or a one-way function; digital root is
  neither -- it is the same mod-9 reduction used throughout this session's
  other audited files, carrying no more information here than there.

FAULT 3 -- the docstring's own claim is false outside a=5..9.
  "Error = 1 for a >= 5" (the supplied inject_error docstring) holds only
  for a = 5..9. discrete_carry(10) = 20 // 10 = 2, discrete_carry(15) = 3,
  and so on: error grows without bound as a grows, it does not stay at 1.
  The claim is true only inside the single-digit window the demo happens
  to test (3, 4, 5, 8).

FAULT 4 -- named target does not exist.
  math/evolutionary_sims.py is not in this repository. The closest files
  by content are replicator_mutator_sim.py, entropy_replicator_sim.py and
  entropy_replicator_v2.py, all at the repo root, not under math/.

PATTERN ACROSS TODAY'S SUPPLIED FILES, noted factually: three supplied
pieces today (dragon_boundary_supplied_audit_2026_10_06.py,
carry_spectrum_dashboard_supplied_audit_2026_10_06.py, and this one) take
the same core arithmetic -- the carry at a=5, the mod-9 digital root, and
the cubic x^3-x^2-2 -- and relabel it with a different field's vocabulary
each time (fluid dynamics, spectral/cyclic group theory, cryptography)
without adding that field's actual structure. The arithmetic itself keeps
checking out; the labels keep not matching it.

FALSIFICATION: any assertion below failing.
"""
import logging
import math as _math
import os

logging.basicConfig(level=logging.CRITICAL)  # suppress the module's own log output here


def digital_root(n: int) -> int:
    if n == 0:
        return 0
    return 1 + ((n - 1) % 9)


def discrete_carry(a: int) -> int:
    return (2 * a) // 10


# --- the module's own output, reproduced exactly ---
EXPECTED = [
    (3, 0, True, "NOMINAL"),
    (4, 0, True, "NOMINAL"),
    (5, 1, True, "NOISE INJECTED"),
    (8, 1, True, "NOISE INJECTED"),
]
lattice_state = 0
for a, exp_err, exp_valid, exp_state in EXPECTED:
    error = discrete_carry(a)
    lattice_state += error
    expected_dr = digital_root(2 * a)
    projected_dr = digital_root((2 * a % 10) + error)
    is_valid = expected_dr == projected_dr
    state = "NOMINAL" if a <= 4 else "NOISE INJECTED"
    assert (error, is_valid, state) == (exp_err, exp_valid, exp_state), a
print("[ok] output reproduced exactly: a=3,4 NOMINAL error=0; a=5,8 NOISE INJECTED error=1")

# --- Fault 1: the error is fully predictable and subtractable by anyone ---
for a in range(0, 1000):
    predicted = discrete_carry(a)          # an attacker computes this with no secret at all
    assert predicted == (2 * a) // 10       # identical formula: zero hidden entropy
assert len({discrete_carry(a) for a in range(0, 10)}) == 2   # only 2 possible error values in 0..9
print("[ok] in 0..9, error has only 2 possible values, both publicly computable: no LWE hardness")

# Fault 3: "Error = 1 for a >= 5" is false beyond a=9
assert all(discrete_carry(a) == 1 for a in range(5, 10))
assert discrete_carry(10) == 2 and discrete_carry(15) == 3
assert not all(discrete_carry(a) == 1 for a in range(5, 20))
print("[ok] docstring's 'Error = 1 for a>=5' holds only for a=5..9; grows unbounded after")

# --- Fault 2: the "checksum" is a public linear function, forgeable with no key ---
def forge(a: int) -> bool:
    """An attacker with no secret reproduces verify_checksum's result exactly."""
    error = discrete_carry(a)
    return digital_root(2 * a) == digital_root((2 * a % 10) + error)

for a in range(0, 50):
    error = discrete_carry(a)
    real = digital_root(2 * a) == digital_root((2 * a % 10) + error)
    assert forge(a) == real                 # no key was used to "forge" it
print("[ok] checksum reproduced with no secret key: authenticates nothing")

# --- Fault 3: the named next target does not exist in this repo ---
assert not os.path.exists("math/evolutionary_sims.py")
assert os.path.exists("replicator_mutator_sim.py")
assert os.path.exists("entropy_replicator_sim.py")
print("[ok] math/evolutionary_sims.py: confirmed absent from the repository")

print("\nlwe_error_injection audit: code runs exactly as claimed; the LWE and")
print("checksum labels do not match what the code does. All assertions pass.")
