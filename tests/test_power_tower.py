"""power_tower.py: exact digits, the limit, the contraction ln t, and the family across x."""
import importlib.util
import pathlib

spec = importlib.util.spec_from_file_location("pt", pathlib.Path(__file__).resolve().parent.parent / "power_tower.py")
pt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pt)
mp = pt.mp
Q = mp.mpf(1) / 4


def test_exact_digits_not_rounded():
    rows = {n: (d, s, r) for n, v, d, s, r in pt.up(Q, 3, 15)}
    assert rows[1][1:] == (7, 7)                                   # 0.25 -> 7
    assert rows[2] == ("707106781186547", 68, 5)                   # 1/sqrt2, truncated
    assert rows[3] == ("375214227246481", 58, 4)                   # 2^-sqrt2, truncated (not ...482 -> 59)


def test_limit_and_contraction():
    t = pt.fixed_point(Q)
    assert abs(t - mp.mpf(1) / 2) < mp.mpf(10) ** -60
    assert abs(t * mp.log(Q) + mp.log(2)) < mp.mpf(10) ** -60         # contraction = ln(1/2) = -ln 2
    roots = [r for _, _, _, _, r in pt.up(Q, 100, 15)][91:]
    assert roots == [5, 4, 5, 4, 5, 4, 5, 4, 5]                   # alternates forever: 0.5000.../0.4999...


def test_family_across_x():
    assert abs(pt.fixed_point(mp.sqrt(2)) - 2) < mp.mpf(10) ** -50
    assert pt.fixed_point(mp.mpf(1) / 27) is None                   # 1/27 < e^-e: 2-cycle
    assert abs(pt.fixed_point(mp.mpf(3) ** (mp.mpf(1) / 3)) - mp.mpf("2.47805268028830")) < mp.mpf(10) ** -12
    assert pt.fixed_point(2 * mp.e ** (1 / mp.e)) is None           # runs to infinity
    # (1/n)^n converges only for n = 2: |ln(1/n)| <= 1 forces n <= e
    assert [n for n in range(2, 10) if pt.fixed_point((mp.mpf(1) / n) ** n) is not None] == [2]
