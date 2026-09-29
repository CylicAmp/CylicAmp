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
}
INTS = list(range(-500, 5001)) + [10 ** k + j for k in range(5, 40) for j in (-1, 0, 1)]
TESTS = {
    'dr': INTS, 'digital_root': INTS, 'digit_sum': INTS,
    'is_prime': list(range(-50, 20001)) + [2 ** 31 - 1, (10 ** 4 + 7) ** 2, 10 ** 9 + 7],
}
STR_TESTS = ['0', '7', '123', '999999', '10000000001']
FLOAT_TESTS = [0.0, 3.0, 9.0, 12.0, 12.5, 3.7, 17.49, 17.5, -2.5, -9.0, 1e6 + 0.4]
BOOTSTRAP = ('import sys as _sys, pathlib as _pl\n'
             '_sys.path.append(str(next(p for p in _pl.Path(__file__).resolve().parents '
             'if (p / "functions.py").exists())))\n')


def outputs(f, xs):
    out = []
    for x in xs:
        try:
            out.append(repr(f(x)))
        except Exception as e:
            out.append('E:' + type(e).__name__)
    return out


def signature(name, f):
    return outputs(f, TESTS[name]) + outputs(f, STR_TESTS) + outputs(f, FLOAT_TESTS)


def py_files():
    for d, dirs, fs in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in ('.git', 'target', 'node_modules')]
        for fn in fs:
            p = os.path.join(d, fn)
            if fn.endswith('.py') and os.path.abspath(p) not in (os.path.join(ROOT, 'functions.py'), os.path.abspath(__file__)):
                yield p


def candidate_defs(tree):
    tops = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    counts = {}
    for n in tops:
        counts[n.name] = counts.get(n.name, 0) + 1
    for n in tops:
        a = n.args
        if n.name not in TARGETS or counts[n.name] != 1 or n.decorator_list:
            continue
        if len(a.args) != 1 or a.vararg or a.kwarg or a.kwonlyargs or a.defaults or a.posonlyargs:
            continue
        stored = {x.id for x in ast.walk(n) if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Store)}
        free = {x.id for x in ast.walk(n) if isinstance(x, ast.Name)} - {a.args[0].arg} - stored - set(dir(__builtins__)) - {'math'}
        if free:
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
            g = {'math': math}
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
