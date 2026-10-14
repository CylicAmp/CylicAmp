#!/usr/bin/env python3
"""Collatz (3n+1) file index, read from git on every branch (built 2026-10-14).

Owner, #276 (2026-10-14), in the screenshot attached to that message:
  "I know no more of my Langdon ants or my collaze conjectures 3+1 proves no
   even mentions"
(typos: Langdon for Langton, collaze for Collatz.)

This prints the table in records/collatz_langton_index_2026_10_14.md:
every file on any branch (refs/remotes/origin/* and the local HEAD) whose text
contains "collatz", plus the files about the 3n+1 map mod 37 that never use
the name. For each: branches, first docstring line, the date it was first
added and the git author of that commit (git log --all --full-history
--diff-filter=A; --full-history is needed, without it git hides the add
commit of T271, T346, T425 ... behind the 2026-10-02 import).

    python3 tools/collatz_index.py          table + reproduction asserts
    python3 tools/collatz_index.py --run    also runs every Collatz code file
"""
import ast, os, re, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def git(*a):
    return subprocess.run(('git',) + a, capture_output=True, text=True, cwd=REPO).stdout


REMOTES = git('for-each-ref', '--format=%(refname)', 'refs/remotes/origin/').split()

# files about the 3n+1 map that never say "Collatz", found with
#   git grep -iE '3 ?\*? ?[nx] ?\+ ?1|3·[nx] ?\+ ?1|hailstone|syracuse'
# (the spaced form "3 * x + 1" matters: a first search for '3n ?\+ ?1|3x ?\+ ?1'
# alone missed LoB 20, T349, T354 and T355).
# Left out: T174 (Ehrhart 3n^2+3n+1), T250 (k = 3x+1 parametrisation) and
# three_block_ladder.py (3N+1 = a power) are not the 3n+1 map;
# .claude/skills/finite-dynamics/dyn.py has "3*x+1" 37 only as a usage example.
THREE_N_PLUS_ONE = [
    'math/primes/modal_crossing_orbit.py',          # LoB 20, 2026-04-23: f(n) = 3n+1 mod 37
    'math/visualizations/ModalCrossingVisual.jsx',  # LoB 20 drawing (JavaScript, not run)
    'math/theorems/lob_25_legendre_applications.py',
    'math/theorems/cascade_constants_audit.py',
    'math/theorems/lob_88_g_ord18_cycle.py',
    'math/theorems/affine_fixed_point_gf37.py',
    'math/theorems/theorem_193_process_functions_zp.py',
    'math/theorems/theorem_349_cubic_map_conjugacy_gf37.py',
    'math/theorems/theorem_353_fa_trajectory_correction_gf37.py',
    'math/theorems/theorem_354_fb_trajectory_gf37.py',
    'math/theorems/theorem_355_conjugate_orbit_and_layer3_gf37.py',
]

# code files whose subject is Collatz / 3n+1 (run with --run)
SUBJECT = [
    'math/theorems/lob_26_collatz_f37.py',
    'math/theorems/collatz_mod37_basin.py',
    'math/theorems/collatz_v2_equidistribution.py',
    'math/theorems/theorem_271_collatz_map_gf37.py',
    'math/theorems/theorem_346_collatz_137_proper_subgroup_gf37.py',
    'math/theorems/theorem_425_collatz_lob26_dynamics_descent_gf37.py',
    'math/theorems/theorem_426_5n_plus_1_map_gf37.py',
    'math/theorems/theorem_427_7n_plus_1_map_gf37.py',
    'math/theorems/theorem_428_parity_word_determinant_sieve.py',
    'math/lemmas/digit_ladder_rows5_on_and_repdigit_lines.py',
    'math/lemmas/digit_ladder_collatz.py',
    'math/lemmas/collatz_zeros_supplied_audit_2026_10_04.py',
    'math/theorems/thread2_collatz_twin_centres.py',
] + THREE_N_PLUS_ONE


# this script and the index it prints contain the word themselves
SELF = {'tools/collatz_index.py', 'records/collatz_langton_index_2026_10_14.md'}


def collatz_paths():
    hits = git('grep', '-il', 'collatz', *REMOTES, 'HEAD').splitlines()
    return sorted({h.split(':', 1)[1] for h in hits} - SELF)


def branches(p):
    return [r.replace('refs/remotes/origin/', '') for r in REMOTES
            if git('cat-file', '-t', f'{r}:{p}').strip() == 'blob']


def first_line(p, src):
    if p.endswith('.py'):
        try:
            ds = ast.get_docstring(ast.parse(src))
        except SyntaxError:
            return '(does not parse)'
        if not ds:
            return '(no docstring)'
        lines = [l.strip() for l in ds.strip().splitlines() if l.strip()]
        # a docstring that opens with the file's own name: give the next line
        if lines[0] == p.rsplit('/', 1)[-1] and len(lines) > 1:
            return lines[1]
        return lines[0]
    line = next((l.strip() for l in src.splitlines() if l.strip()), '')
    if line in ('[', '{'):
        return '(JSON, no docstring)'
    if line == '---':
        m = re.search(r'^name:\s*(.+)$', src, re.M)
        return f'(skill "{m.group(1).strip()}", no docstring)' if m else '(skill)'
    return line


def first_add(p):
    rows = []
    out = git('log', '--all', '--full-history', '--diff-filter=A',
              '--date=format:%Y-%m-%d',
              '--format=%at|%ad|%an|%cn|%h|%(trailers:key=Claude-Session,valueonly,separator=;)', '--', p)
    for a in out.strip().splitlines():
        t, d, an, cn, h, tr = a.split('|', 5)
        # since a078f2c (2026-10-14) session commits carry the owner's name as
        # author and Claude as committer: show the committer when it differs
        rows.append((int(t), d, an if an == cn else f'{an}, committer {cn}', h, bool(tr.strip())))
    rows.sort()
    t0 = rows[0][0]
    first = [r for r in rows if r[0] == t0]
    return first[0][1], sorted({r[2] for r in first}), [r[3] for r in first], any(r[4] for r in first)


IMPORTS = {'3bc8c4c': '509-file root commit', '26dcd38': '1585-file root commit'}


def row(p):
    br = branches(p)
    local = git('cat-file', '-t', f'HEAD:{p}').strip() == 'blob'
    src = git('show', f'{"HEAD" if local else "refs/remotes/origin/" + br[0]}:{p}')
    date, authors, commits, trailer = first_add(p)
    return dict(path=p, br=br, first=first_line(p, src), date=date, authors=authors,
                commits=commits, trailer=trailer, n=len(re.findall('collatz', src, re.I)))


def groups(rows):
    seen = {}
    for r in rows:
        key = tuple(r['br'])
        if key not in seen:
            seen[key] = 'B%d' % (len(seen) + 1)
    return seen


def md(rows, g):
    out = ['| file | branches | first docstring line | added | author (git) | "collatz" count |',
           '|---|---|---|---|---|---|']
    for r in rows:
        c = ', '.join(r['commits'])
        note = ''.join(' [%s]' % IMPORTS[x] for x in r['commits'] if x in IMPORTS)
        auth = ' / '.join(r['authors']) + (' (Claude-Session trailer)' if r['trailer'] else '')
        first = r['first'].replace('|', '\\|')
        out.append(f"| `{r['path']}` | {g[tuple(r['br'])]} | {first} | {r['date']} `{c}`{note} | {auth} | {r['n']} |")
    return '\n'.join(out)


def reproduce():
    p = 37
    C = lambda x: (3 * x + 1) % p
    assert [x for x in range(p) if C(x) == x] == [18]          # T271 fixed point
    assert [x for x in range(p) if C(x) == 0] == [12]          # T271 seam preimage
    T = lambda x: (19 * x) % p if x % 2 == 0 else (3 * x + 1) % p
    cycles = set()
    for s in range(p):
        seen, x = [], s
        while x not in seen:
            seen.append(x); x = T(x)
        cycles.add(frozenset(seen[seen.index(x):]))
    assert sorted(map(len, cycles)) == [1, 3, 9]               # LoB 26
    assert sum(map(len, cycles)) == 13
    order = lambda a: next(k for k in range(1, p) if pow(a, k, p) == 1)
    assert (order(2), order(3), order(26)) == (36, 18, 3)      # T346
    lens, seen = [], set()
    for s in range(p):
        if s in seen:
            continue
        x, L = s, 0
        while True:
            seen.add(x); x = C(x); L += 1
            if x == s:
                break
        lens.append(L)
    assert sorted(lens) == [1, 18, 18]                         # T346: C = 1 + two 18-cycles
    orb0, x = [0], C(0)                                         # LoB 20 (2026-04-23): orbit_p
    while x != 0:
        orb0.append(x); x = C(x)
    assert orb0 == [0, 1, 4, 13, 3, 10, 31, 20, 24, 36, 35, 32, 23, 33, 26, 5, 16, 12]

    def steps(n):
        k = 0
        while n != 1:
            n = 3 * n + 1 if n % 2 else n // 2; k += 1
        return k

    def max_odd(n):
        m = 0
        while n != 1:
            if n % 2:
                m = max(m, n)
            n = 3 * n + 1 if n % 2 else n // 2
        return m
    assert steps(12312) == 37 and steps(27) == 111 and steps(108) == 113   # ladder row 1; thread 2
    assert all(max_odd(c) == 3077 for c in (108, 432, 462, 570, 660)) and 3077 == 17 * 181
    print('reproduced: T271 fixed point 18, seam preimage 12; LoB26 cycles 1+3+9 = 13;'
          ' ord 2,3,26 = 36,18,3; C = 1 + 18 + 18; 12312 -> 1 in 37 steps; 3077 trunk')


if __name__ == '__main__':
    paths = collatz_paths()
    rows = [row(p) for p in paths]
    rows3 = [row(p) for p in THREE_N_PLUS_ONE]
    # 51 on 2026-10-14 (50 + langton_ant_highway_2026_10_14.py); later files raise it
    assert len(rows) >= 51, len(rows)
    assert all(r['n'] == 0 for r in rows3)
    by_date = lambda rs: sorted(rs, key=lambda r: (r['date'], r['path']))
    subject = by_date([r for r in rows if r['path'] in SUBJECT])
    is_cite = lambda q: q.startswith('math/') and q.endswith('.py') and 'INDEX' not in q
    cites = by_date([r for r in rows if r['path'] not in SUBJECT and is_cite(r['path'])])
    index = by_date([r for r in rows if r['path'] not in SUBJECT and not is_cite(r['path'])])
    assert len(subject) == 13 and len(cites) + len(index) == len(rows) - 13
    g = groups(subject + by_date(rows3) + cites + index)
    print('Branch sets:')
    for key, name in g.items():
        print(f'  {name} ({len(key)}): ' + ', '.join(key))
    print('\nA. Collatz is the subject (%d files, oldest first):\n' % len(subject))
    print(md(subject, g))
    print('\nA2. The 3n+1 map mod 37 without the word Collatz (%d files):\n' % len(rows3))
    print(md(by_date(rows3), g))
    print('\nB. Other math code that uses or cites the Collatz work (%d):\n' % len(cites))
    print(md(cites, g))
    print('\nC. Indexes, catalogs, skills, records, owner_work (%d):\n' % len(index))
    print(md(index, g))
    reproduce()
    if '--run' in sys.argv:
        bad, py = [], [f for f in SUBJECT if f.endswith('.py')]
        for f in py:
            rc = subprocess.run([sys.executable, f], cwd=REPO, capture_output=True, timeout=600).returncode
            print(f'  rc={rc}  {f}')
            if rc:
                bad.append(f)
        assert not bad, bad
        print(f'all {len(py)} Collatz / 3n+1 Python files exit 0'
              ' (ModalCrossingVisual.jsx is JavaScript and is not run)')
