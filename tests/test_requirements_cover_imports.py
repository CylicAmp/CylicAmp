"""Every third-party library imported by a file pytest collects is declared for CI.

CI runs `pip install -r requirements-dev.txt` then `python -m pytest -v`. A test file that
imports a library not reachable from requirements-dev.txt (directly, through requirements.txt,
or as a dependency of a declared package) stops collection with ModuleNotFoundError -- the
2026-09-22..10-02 failure. This test fails first, naming the library to add.
Imports inside `try: ... except ImportError` (or ModuleNotFoundError / Exception) are optional
and skipped.
"""
import ast
import importlib.metadata as md
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
NORECURSE = {".git", "node_modules", "venv", ".venv", "build", "dist", "__pycache__"}
OPTIONAL = {"ImportError", "ModuleNotFoundError", "Exception"}


def norm(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def collected_files():
    for p in ROOT.rglob("*.py"):
        if any(part in NORECURSE or part.startswith(".") for part in p.relative_to(ROOT).parts[:-1]):
            continue
        n = p.name
        if n == "conftest.py" or (n.startswith("test_") and n.endswith(".py")) or n.endswith("_test.py"):
            yield p


def required_imports(path):
    tree = ast.parse(path.read_text(encoding="utf-8"), str(path))
    optional = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Try):
            caught = {getattr(h.type, "id", getattr(h.type, "attr", None)) for h in node.handlers if h.type is not None}
            if caught & OPTIONAL or any(h.type is None for h in node.handlers):
                optional |= {id(n) for b in node.body for n in ast.walk(b)}
    names = set()
    for node in ast.walk(tree):
        if id(node) in optional:
            continue
        if isinstance(node, ast.Import):
            names |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.add(node.module.split(".")[0])
    return names


def is_local(name, path):
    # the repo root, the file's folder, and every folder between (tests often add '..' to sys.path,
    # e.g. baserate/tests/test_intent_extractor.py importing baserate/modules)
    dirs = [d for d in path.parents if d == ROOT or ROOT in d.parents]
    return any((d / f"{name}.py").exists() or (d / name).is_dir() for d in dirs)


def declared_closure():
    todo, seen = [], set()

    def read(req):
        for line in (ROOT / req).read_text().splitlines():
            line = line.split("#")[0].strip()
            if line.startswith("-r"):
                read(line[2:].strip())
            elif line:
                todo.append(norm(re.split(r"[<>=!~;\[ ]", line, 1)[0]))
    read("requirements-dev.txt")
    while todo:
        d = todo.pop()
        if d in seen:
            continue
        seen.add(d)
        try:
            reqs = md.requires(d) or []
        except md.PackageNotFoundError:
            continue
        todo += [norm(re.split(r"[<>=!~;\[ (]", r, 1)[0]) for r in reqs if "extra ==" not in r]
    return seen


def test_every_collected_import_is_declared():
    mod2dist = md.packages_distributions()
    declared = declared_closure()
    missing = {}
    for path in collected_files():
        for name in required_imports(path):
            if name in sys.stdlib_module_names or is_local(name, path):
                continue
            dists = {norm(d) for d in mod2dist.get(name, [])}
            if not dists or not dists & declared:
                missing.setdefault(name, []).append(str(path.relative_to(ROOT)))
    assert not missing, ("add to requirements-dev.txt (module: files importing it): "
                         + "; ".join(f"{k}: {v[:3]}" for k, v in sorted(missing.items())))
