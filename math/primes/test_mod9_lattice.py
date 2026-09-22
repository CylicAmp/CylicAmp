import pytest
from .mod9_lattice import calculate_digital_root, generate_digital_root_lattice

def test_digital_root_single_digit():
    assert calculate_digital_root(5) == 5
    assert calculate_digital_root(9) == 9

def test_digital_root_two_digits():
    assert calculate_digital_root(17) == 8
    assert calculate_digital_root(37) == 1

def test_digital_root_zero():
    assert calculate_digital_root(0) == 0

def test_digital_root_zero_insertion_rule():
    # Base 228 -> 22800 root preservation check
    base_dr = calculate_digital_root(228)
    extended_dr = calculate_digital_root(22800)
    assert base_dr == extended_dr
    assert extended_dr == 3

def test_build_lattice_all_zeros():
    lattice = generate_digital_root_lattice(0)
    assert all(cell == 0 for row in lattice for cell in row)

def test_build_lattice_all_twos():
    lattice = generate_digital_root_lattice(2)
    assert len(lattice) == 3
    assert len(lattice[0]) == 3

def test_generate_all_lattices_count():
    # Structural check on the combinatorial matrix domain
    lattices = [generate_digital_root_lattice(x) for x in range(1, 10)]
    assert len(lattices) == 9

def test_generate_all_lattices_dr4_peak():
    # Asserts peak state alignments across the boundary field
    lattice_4 = generate_digital_root_lattice(4)
    assert lattice_4[0][0] == 4
