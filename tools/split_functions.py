"""
Replace per-file copies of shared functions with imports from functions.py.

    python3 tools/split_functions.py plan   > plan.json   # which files, which variant
    python3 tools/split_functions.py apply  plan.json     # rewrite those files

A copy is replaced only if
  * it is a single top-level def of that name in the file,
  * it takes one plain argument and uses no file-level globals,
  * its outputs (values and exception types) equal one variant in functions.py
    on every test input below.
The rewrite puts, in place of the def:
    import sys as _sys, pathlib as _pl
    _sys.path.append(str(next(p for p in _pl.Path(__file__).resolve().parents if (p / "functions.py").exists())))
    from functions import <variant> as <name>
so the file keeps calling its function by its old name. Whether a file's
printed output is unchanged is checked separately (tools/split_functions_check.py).
"""
import ast, json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import functions as FN  # noqa: E402

TARGETS = {
    'dr': ['dr', 'dr_signed', 'dr_pos', 'dr_strict', 'dr9', 'dr9_signed', 'dr9_pos', 'dr_iter', 'dr9_iter'],
    'digital_root': ['dr', 'dr_signed', 'dr_pos', 'dr_strict', 'dr9', 'dr9_signed', 'dr9_pos', 'dr_iter', 'dr9_iter'],
    'digit_sum': ['digit_sum', 'digit_sum_abs', 'digit_sum_str'],
    'is_prime': ['is_prime'],
    'legendre': ['euler_criterion', 'euler_criterion37', 'legendre', 'legendre37', 'legendre_by_residue'],
    'orbit_of': ['orbit_of', 'orbit_of_next', 'orbit_of_assert', 'orbit_of_key',
                 'orbit_of_unknown', 'orbit_of_q', 'orbit_of_v1'],
}
# Targets whose copies read file-level tables (orbit_of reads ORBITS, P): the
# copy is evaluated with the file's own top-level constants, built by running
# only its side-effect-free top-level assignments.
NEEDS_GLOBALS = {'orbit_of'}
INTS = list(range(-500, 5001)) + [10 ** k + j for k in range(5, 40) for j in (-1, 0, 1)]
TESTS = {
    'dr': INTS, 'digital_root': INTS, 'digit_sum': INTS,
    'is_prime': list(range(-50, 20001)) + [2 ** 31 - 1, (10 ** 4 + 7) ** 2, 10 ** 9 + 7],
    'orbit_of': list(range(-40, 400)) + [10 ** 12 + 5, None],
    'legendre': [(a, p) for p in (2, 3, 5, 7, 11, 13, 37, 73, 101) for a in range(-40, 120)]
                + [(a, m) for m in (9, 15, 21, 25) for a in range(-5, 30)]
                + [(a,) for a in range(-5, 80)] + [(10 ** 15 + 3, 37)],
}
# Targets whose copies take two arguments (possibly with a default).
MULTI_ARG = {'legendre'}
STR_TESTS = ['0', '7', '123', '999999', '10000000001']
FLOAT_TESTS = [0.0, 3.0, 9.0, 12.0, 12.5, 3.7, 17.49, 17.5, -2.5, -9.0, 1e6 + 0.4]
BOOTSTRAP = ('import sys as _sys, pathlib as _pl\n'
             '_sys.path.append(str(next(p for p in _pl.Path(__file__).resolve().parents '
             'if (p / "functions.py").exists())))\n')


def outputs(f, xs):
    out = []
    for x in xs:
        try:
            out.append(repr(f(*x) if isinstance(x, tuple) else f(x)))
        except Exception as e:
            out.append('E:' + type(e).__name__)
    return out


def signature(name, f):
    if name in MULTI_ARG:
        return outputs(f, TESTS[name])
    return outputs(f, TESTS[name]) + outputs(f, STR_TESTS) + outputs(f, FLOAT_TESTS)


def py_files():
    for d, dirs, fs in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in ('.git', 'target', 'node_modules')]
        for fn in fs:
            p = os.path.join(d, fn)
            if fn.endswith('.py') and os.path.abspath(p) not in (os.path.join(ROOT, 'functions.py'), os.path.abspath(__file__)):
                yield p


SAFE_CALLS = {'set', 'frozenset', 'dict', 'range', 'sorted', 'list', 'tuple', 'len', 'sum', 'pow',
              'zip', 'enumerate', 'int', 'min', 'max', 'abs', 'reversed', 'map', 'filter', 'any', 'all', 'str'}


def _side_effect_free(node):
    for c in ast.walk(node):
        if isinstance(c, ast.Call):
            f = c.func
            if isinstance(f, ast.Name) and f.id in SAFE_CALLS:
                continue
            if isinstance(f, ast.Attribute) and f.attr in ('items', 'keys', 'values', 'union', 'copy'):
                continue
            return False
        if isinstance(c, ast.Lambda):
            return False
    return True


def file_constants(tree, path):
    g = {'math': math}
    for n in tree.body:
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            mods = [a.name for a in n.names] if isinstance(n, ast.Import) else [n.module or '']
            if all(m.split('.')[0] in ('math', 'collections', 'itertools', 'functools', 'fractions') for m in mods):
                try:
                    exec(compile(ast.Module([n], []), path, 'exec'), g)
                except Exception:
                    pass
        elif isinstance(n, (ast.Assign, ast.AnnAssign)) and _side_effect_free(n):
            try:
                exec(compile(ast.Module([n], []), path, 'exec'), g)
            except Exception:
                pass
    return g


def candidate_defs(tree):
    tops = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    counts = {}
    for n in tops:
        counts[n.name] = counts.get(n.name, 0) + 1
    for n in tops:
        a = n.args
        if n.name not in TARGETS or counts[n.name] != 1 or n.decorator_list:
            continue
        if n.name in MULTI_ARG:
            if len(a.args) != 2 or a.vararg or a.kwarg or a.kwonlyargs or a.posonlyargs:
                continue
        elif len(a.args) != 1 or a.vararg or a.kwarg or a.kwonlyargs or a.defaults or a.posonlyargs:
            continue
        stored = {x.id for x in ast.walk(n) if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Store)}
        free = {x.id for x in ast.walk(n) if isinstance(x, ast.Name)} - {x.arg for x in a.args} - stored - set(dir(__builtins__)) - {'math'}
        if free and n.name not in NEEDS_GLOBALS:
            continue
        yield n


def plan():
    variant_sig = {name: {v: signature(name, getattr(FN, v)) for v in vs} for name, vs in TARGETS.items()}
    result = []
    for p in sorted(py_files()):
        try:
            src = open(p, encoding='utf-8').read()
            tree = ast.parse(src)
        except Exception:
            continue
        for n in candidate_defs(tree):
            body = [s for s in n.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value, str))]
            for arg in n.args.args:
                arg.annotation = None
            fdef = ast.FunctionDef(name='F', args=n.args, body=body, decorator_list=[], returns=None, type_params=[])
            g = file_constants(tree, p) if n.name in NEEDS_GLOBALS else {'math': math}
            try:
                exec(ast.unparse(ast.fix_missing_locations(ast.Module(body=[fdef], type_ignores=[]))), g)
            except Exception:
                continue
            sig = signature(n.name, g['F'])
            match = [v for v, s in variant_sig[n.name].items() if s == sig]
            if match:
                result.append({'file': os.path.relpath(p, ROOT), 'name': n.name, 'variant': match[0],
                               'lines': [n.lineno, n.end_lineno]})
    return result


def apply(entries):
    by_file = {}
    for e in entries:
        by_file.setdefault(e['file'], []).append(e)
    for rel, es in by_file.items():
        p = os.path.join(ROOT, rel)
        lines = open(p, encoding='utf-8').read().split('\n')
        es.sort(key=lambda e: e['lines'][0])
        first = es[0]['lines'][0]
        for e in reversed(es):
            s, t = e['lines']
            imp = f"from functions import {e['variant']}" + ('' if e['variant'] == e['name'] else f" as {e['name']}")
            block = (BOOTSTRAP if s == first else '') + imp
            lines[s - 1:t] = block.split('\n')
        open(p, 'w', encoding='utf-8').write('\n'.join(lines))


if __name__ == '__main__':
    if sys.argv[1] == 'plan':
        json.dump(plan(), sys.stdout, indent=1)
    elif sys.argv[1] == 'apply':
        apply(json.load(open(sys.argv[2])))
