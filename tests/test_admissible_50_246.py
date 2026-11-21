"""Admissibility assertions for the minimal 50-tuple (diameter 246) and its 39-suffix (diameter 182), every prime p <= 53,
and every number of the pasted request of 2026-11-21 (math/primes/admissible_50_246.py, records/evidence_ledger_...)."""
import importlib.util
import json
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("adm", ROOT / "math" / "primes" / "admissible_50_246.py")
A = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A)
PRIMES_53 = A.primes_upto(53)


@pytest.mark.parametrize("p", PRIMES_53)
def test_admissible_at_every_prime_up_to_53(p):
    assert len(A.occupied(A.H50, p)) < p and len(A.occupied(A.H39, p)) < p


def test_sizes_diameters_and_least_possible():
    assert (len(A.H50), A.H50[-1], len(set(A.H50))) == (50, 246, 50)
    assert (len(A.H39), A.H39[-1], A.SHIFT) == (39, 182, 64) and 246 - 182 == 64 == 2 ** 6
    assert A.A008407[50] == 246 and A.A008407[39] == 182 and A.A008407[38] == 176    # OEIS A008407


def test_excluded_residues_small_primes_as_pasted():
    want = {2: [1], 3: [2], 5: [2], 7: [5], 11: [10], 13: [11]}
    assert {p: A.excluded(A.H50, p) for p in want} == want
    assert all(len(A.occupied(A.H50, p)) == p - 1 for p in want)
    # the suffix, shifted down by 64, excludes the same classes moved by 64
    assert {p: A.excluded(A.H39, p) for p in want} == {p: [(r - 64) % p] for p, (r,) in want.items()}


def test_gap_architecture_as_pasted():
    assert dict(A.gaps(A.H50)) == {4: 14, 2: 12, 10: 3, 14: 1, 6: 15, 8: 4}
    assert dict(A.gaps(A.H39)) == {6: 15, 8: 4, 4: 11, 2: 8}
    assert [round(100 * c / 49, 1) for c in (12, 14, 15, 4, 3, 1)] == [24.5, 28.6, 30.6, 8.2, 6.1, 2.0]
    assert [round(100 * c / 38, 1) for c in (8, 11, 15, 4)] == [21.1, 28.9, 39.5, 10.5]
    assert sum(A.gaps(A.H50)[g] for g in (2, 4, 6)) == 41 and round(41 / 49, 4) == 0.8367
    assert sum(A.gaps(A.H39)[g] for g in (2, 4, 6)) == 34 and round(34 / 38, 4) == 0.8947
    assert max(A.gaps(A.H39)) == 8                                   # every step of 10 or 14 sits in the first 11 gaps


def test_sub_182_windows_and_greedy():
    assert A.windows(A.H50, 39) == [204, 206, 208, 200, 190, 192, 192, 188, 190, 182, 184, 182]
    assert min(A.windows(A.H50, 39)) == 182                          # two windows reach 182 (from h = 58 and h = 64)
    greedy = {d: len(A.greedy_sieve(d)) for d in (176, 178, 180)}
    assert greedy == {176: 37, 178: 37, 180: 36} and all(A.admissible(A.greedy_sieve(d)) for d in greedy)


def test_ledger_matches_recomputation():
    assert json.loads(A.LEDGER.read_text()) == json.loads(json.dumps(A.ledger()))
