"""plug.py: number pairs written both ways, and lines written both ways round."""
import importlib.util
import pathlib

spec = importlib.util.spec_from_file_location("plug", pathlib.Path(__file__).resolve().parent.parent / "plug.py")
plug = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plug)


def test_flip_pairs_from_the_owners_drip_example():
    nums, _ = plug.numbers_by_line("1\n12\n\n1\n21\n\n2\n12\n\n2\n21\n")
    assert nums == [1, 12, 21, 2]
    assert plug.flip_pairs(nums) == [(12, 21)]


def test_trailing_zero_is_not_a_flip():
    assert plug.flip_pairs([20, 2]) == []


def test_lines_both_ways_round():
    _, by_line = plug.numbers_by_line("2+4=6\n4+2=6\n2÷11\n11÷2\n4+8+8\n8+4+4\n")
    groups = [[line for _, line, _ in g] for g in plug.lines_both_ways(by_line)]
    assert ["2+4=6", "4+2=6"] in groups and ["2÷11", "11÷2"] in groups
    assert not any("4+8+8" in g for g in groups)   # different numbers: 4,8,8 vs 8,4,4
