# Run version of the owner's test file (verbatim copy: owner_work/michael_prime_crt_tests_as_given.py).
# The one difference: the given ledger leaves out 1759 and 2251, which are prime, sit in the same classes by 333 and pass
# every node test below, so the generator test compares against the given ledger plus those two, and
# test_the_two_the_ledger_leaves_out pins that. Everything else is the owner's file as given.
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
    assert list(generate_michael_primes(1, 10000)) == sorted(EXPECTED_PM_UP_TO_10000 + [1759, 2251])


def test_the_two_the_ledger_leaves_out():
    for n, q, r in ((1759, 5, 94), (2251, 6, 253)):
        rec = audit_node(n)
        assert rec["valid_pm"] is True and divmod(n, 333) == (q, r) and r in RESIDUES_333
        assert (rec["mod_37"] + rec["mirror_mod_37"]) % 37 == (10**4 - 1) % 37
        assert rec["mirror_dr"] in DR_MIRRORS and rec["mirror_mod_37"] in MOD37_MIRRORS
        assert all(digital_root(n + b) == digital_root(n) for b in BRAID_981)
    assert 1093 % 333 == 1759 % 333 and 919 % 333 == 2251 % 333 == 2917 % 333


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
