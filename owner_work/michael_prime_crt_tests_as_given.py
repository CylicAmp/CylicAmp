# The owner's test file for michael_prime_crt, 2026-11-19, kept verbatim (not collected by pytest: the name does not start
# with test_). The run version, with the one difference, is tests/test_michael_prime_crt.py.
import pytest
from michael_prime_crt import (
    BRAID_981,
    MOD37_MIRRORS,
    DR_MIRRORS,
    RESIDUES_333,
    audit_node,
    digital_root,
    generate_michael_primes,
    verify_crt_invariants,
)

EXPECTED_PM_UP_TO_10000 = [
    31, 43, 487, 709, 919, 1093, 1153, 1597, 2029, 2203, 2473, 2647, 2707, 2917,
    3313, 3361, 3373, 3583, 4027, 4201, 4261, 4423, 4483, 5581, 6037, 6199, 6247,
    6421, 6469, 6481, 6691, 6703, 7309, 7369, 7591, 7753, 8419, 8467, 8641, 8689,
    8863, 8923, 9133, 9811, 9973,
]


def test_crt_bijection_and_orbit():
    assert verify_crt_invariants() is True


def test_generator_matches_known_ledger():
    assert list(generate_michael_primes(1, 10000)) == EXPECTED_PM_UP_TO_10000


@pytest.mark.parametrize("pm", EXPECTED_PM_UP_TO_10000)
def test_node_invariants_and_width_dependent_mirror_duality(pm):
    record = audit_node(pm)
    width = len(str(pm))
    expected_mod37_sum = (10**width - 1) % 37

    assert record["valid_pm"] is True
    assert record["r_333"] in RESIDUES_333
    assert (record["mod_37"] + record["mirror_mod_37"]) % 37 == expected_mod37_sum
    assert record["mirror_dr"] in DR_MIRRORS
    if width == 4:
        assert record["mirror_mod_37"] in MOD37_MIRRORS


def test_vireon_unity_locks():
    for unity_node in (2203, 4201):
        rec = audit_node(unity_node)
        assert rec["r_333"] == 205
        assert rec["vireon_13_coupling"] == 1


def test_braid_group_and_perturbation():
    assert sum(BRAID_981) == 3996
    assert sum(BRAID_981) % 37 == 0
    assert sum((189, 891, 918)) == 1998 == 6 * 333
    assert sum((198, 981, 819)) == 1998 == 6 * 333
    for pm in EXPECTED_PM_UP_TO_10000:
        for b in BRAID_981:
            assert digital_root(pm + b) == digital_root(pm)
