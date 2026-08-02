from cylicamp.core import build_full_lattice, digital_root, generate_all_lattices


def run(d1=1, d2=2, d3=3, d4=4):
    """Print a lattice and its center digital root."""
    lattice, center = build_full_lattice(d1, d2, d3, d4)
    print(f"Inputs: ({d1}, {d2}, {d3}, {d4})")
    print(f"Center: {center}  DR: {digital_root(center)}")
    for row in lattice:
        print(" ".join(f"{v:3d}" for v in row))
    return lattice, center
