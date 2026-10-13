"""drip_cycle.py: the owner's example shape, and the 246 run."""
import importlib.util
import pathlib

spec = importlib.util.spec_from_file_location("drip", pathlib.Path(__file__).resolve().parent.parent / "drip_cycle.py")
drip = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drip)


def test_owners_example_is_reproduced():
    (k, lines), = drip.drip(12)
    assert k == 2 and lines == [("1", "12"), ("1", "21"), ("2", "12"), ("2", "21")]


def test_246():
    levels = dict(drip.drip(246))
    assert len(levels[2]) == 12 and len(levels[3]) == 18
    orbit = {a: drip.frame(a)["orbit"] for _, a in levels[3]}
    assert {a for a, o in orbit.items() if o == "SEED"} == {"246", "462", "624"}
    assert {a for a, o in orbit.items() if o == "CAS_EXT"} == {"264", "426", "642"}
    assert 246 + 642 == 888 == 24 * 37 and 42 + 26 * 24 == 666 == 18 * 37
