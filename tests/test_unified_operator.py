"""Unified Operator Module: restart-safe, no partial steps, one failing operator does not stop the rest."""
import importlib.util
import json
import pathlib

spec = importlib.util.spec_from_file_location("uo", pathlib.Path(__file__).resolve().parent.parent / "unified_operator.py")
uo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(uo)

KEYS = ("step", "used", "frontier", "covered", "seen")


def test_restart_resumes_to_the_same_state(tmp_path):
    whole = uo.run([246], budget=6000, width=10, steps=8, path=tmp_path / "a.json")
    cp = tmp_path / "b.json"
    uo.run([246], budget=6000, width=10, steps=3, path=cp)          # "restart" after step 3
    assert json.loads(cp.read_text())["step"] == 3
    resumed = uo.run([246], budget=6000, width=10, steps=8, path=cp)
    assert all(whole[k] == resumed[k] for k in KEYS)


def test_refused_step_changes_nothing():
    z = uo.initial_state([1, 2, 12, 21], budget=10, width=12)
    before = json.dumps(z, sort_keys=True)
    z = uo.recurse(z)
    assert z["stopped"].startswith("INSUFFICIENT_COMPUTE")
    z["stopped"] = None
    assert json.dumps(z, sort_keys=True) == before


def test_one_failing_operator_does_not_stop_the_others():
    uo.UNARY["broken"] = lambda n: 1 // 0
    try:
        z = uo.initial_state([246], budget=1000, width=5)
        z = uo.recurse(z)
        assert z["log"][-1]["errors"] and "broken" in z["log"][-1]["errors"][0]
        assert {"642", "888", "248"} <= set(z["seen"])                # flip, flip-sum, twin-up still ran
    finally:
        del uo.UNARY["broken"]


def test_drip_example_joins_both_ways():
    z = uo.run([1, 2], budget=100, width=4, steps=1)
    assert z["seen"]["12"]["op"] in ("join", "join-back") and "21" in z["seen"]


def test_miller_rabin_agrees_with_trial_division_and_the_known_pseudoprime():
    assert [n for n in range(2, 5000) if uo.is_prime(n)] == [n for n in range(2, 5000) if uo.G.is_prime(n)]
    assert not uo.is_prime(318665857834031151167461)                # 399165290221 x 798330580441
