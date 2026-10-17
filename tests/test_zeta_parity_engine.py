"""Fast checks of tools/zeta_parity_engine.py (the owner's section-4 engine, handoff #272)."""
import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("zeta_parity_engine", ROOT / "tools" / "zeta_parity_engine.py")
zpe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(zpe)


def test_known_d_n():
    # 8 digits: 1 3 5 7 9 1 3 5 are all odd, then 2 4 6 8 are even -> D_4 = 4, D_8 = 8 - 0 = 8 for the odd run
    r = zpe.analyze_stream(["13572468"], [4, 8])[0]
    assert r["d_n"] == [4, 0] and r["d_n_final"] == 0
    r = zpe.analyze_stream(["1111.2222"], [4, 8])[0]
    assert r["d_n"] == [4, 0] and r["alpha_slope"] is None and "fewer than 2" in r["alpha_note"]


def test_short_zero_does_not_crash():
    r = zpe.analyze_stream(["12.5"], [100, 1000])[0]
    assert r["d_n"] == [] and r["d_n_final"] is None and r["predicted_sign_match"] is None


def test_sign_prediction_follows_index_parity():
    # zero 1 (odd index) wants D > 0, zero 2 (even index) wants D < 0, zero 3 wants D > 0
    res = zpe.analyze_stream(["111", "111", "222"], [3])
    assert [r["d_n_final"] for r in res] == [3, 3, -3]
    assert [r["predicted_sign_match"] for r in res] == [True, False, False]


def test_first_zero_digits():
    first = next(zpe.zeros_from_mpmath(1, 40))
    assert zpe.digits_of(first).startswith("141347251417346937904572519835624702707")


def test_binomial():
    assert abs(zpe.binomial_two_sided(10, 20) - 1.0) < 1e-12
    assert zpe.binomial_two_sided(20, 20) < 1e-5
