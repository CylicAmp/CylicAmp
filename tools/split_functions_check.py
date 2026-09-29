"""
Run each planned file before and after the rewrite, in a scratch copy of the
repo, and compare stdout + stderr + exit code.

    python3 tools/split_functions_check.py <plan.json> <scratch_dir> <out.json>

Baseline is run twice; a file whose two baseline runs differ is marked
'nondeterministic' and left unchanged. A file that times out is marked
'timeout' and left unchanged. Only files marked 'same' should be rewritten.
"""
import hashlib, json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
plan_path, scratch, out_path = sys.argv[1:4]
TIMEOUT = 20
ENV = dict(os.environ, MPLBACKEND='Agg', PYTHONHASHSEED='0')


def run(wt, rel):
    try:
        r = subprocess.run([sys.executable, rel], cwd=wt, capture_output=True, timeout=TIMEOUT, env=ENV, stdin=subprocess.DEVNULL)
        return hashlib.sha256(r.stdout + b'\0' + r.stderr + b'\0' + str(r.returncode).encode()).hexdigest()
    except subprocess.TimeoutExpired:
        return 'TIMEOUT'


def copy_repo(dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns('.git', 'target', 'node_modules', '__pycache__'))


plan = json.load(open(plan_path))
files = sorted({e['file'] for e in plan})
a, b = os.path.join(scratch, 'before'), os.path.join(scratch, 'after')
copy_repo(a)
copy_repo(b)
sys.path.insert(0, ROOT)
import importlib.util
spec = importlib.util.spec_from_file_location('sf', os.path.join(ROOT, 'tools', 'split_functions.py'))
sf = importlib.util.module_from_spec(spec); spec.loader.exec_module(sf)
sf.ROOT = b
sf.apply(plan)

def check(rel):
    h1 = run(a, rel)
    if h1 == 'TIMEOUT':
        return rel, 'timeout'
    h2 = run(a, rel)
    if h1 != h2:
        return rel, 'nondeterministic'
    h3 = run(b, rel)
    return rel, 'same' if h3 == h1 else ('timeout_after' if h3 == 'TIMEOUT' else 'DIFFERENT')

with ThreadPoolExecutor(4) as ex:
    res = dict(ex.map(check, files))
json.dump(res, open(out_path, 'w'), indent=1)
from collections import Counter
print(Counter(res.values()))
