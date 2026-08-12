# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

CylicAmp is a Python framework for generating and analyzing 4x4 lattice structures using **digital root** calculations. A digital root reduces a number to a single digit by iteratively summing its digits (e.g., 19 → 1+9=10 → 1+0=1, so DR=1). The project groups all possible lattices by their center's digital root and visualizes them via CLI and a web UI.

## Commands

**Install (editable mode):**
```bash
pip install -e .
```

**Run CLI:**
```bash
python main.py
```

**Run all tests:**
```bash
python -m pytest tests/
```

**Run a single test:**
```bash
python -m pytest tests/test_core.py::test_digital_root_single_digit -v
```

No linting tools are configured.

## Architecture

The codebase has two entry points and three modules:

- **`main.py`** — CLI entry point; calls `display.run(digit_set=(0, 1, 2))`
- **`index.html`** — Standalone dark-themed web UI (no server required)
- **`cylicamp/core.py`** — All mathematical logic (pure functions, no classes)
- **`cylicamp/display.py`** — Formats and prints lattice output
- **`cylicamp/__init__.py`** — Re-exports the main public functions

### Core Data Flow

1. `generate_all_lattices(digit_set)` in `core.py` uses `itertools.product` to produce all permutations of 4 core digits from the digit set (e.g., `(0,1,2)` → 3⁴=81 combinations).
2. For each combination `(d1, d2, d3, d4)`, `build_full_lattice()` constructs a 4x4 symmetric lattice and computes the center sum.
3. `digital_root()` is applied to the center sum to get the lattice's DR group.
4. Results are stored in a `defaultdict(list)` keyed by digital root (0–9), where each value is a list of dicts: `{"core": tuple, "lattice": list[list[int]], "center": int, "digital_root": int}`.
5. `display.py` iterates this grouped dict and pretty-prints lattices by DR group.

### Extending Digit Sets

To explore larger lattice spaces, change the `digit_set` in `main.py`. Using `(0,1,2,3)` produces 4⁴=256 lattices. The architecture scales automatically.
