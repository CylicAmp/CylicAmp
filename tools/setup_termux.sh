#!/data/data/com.termux/files/usr/bin/bash
# Set up and check CylicAmp on Android (Termux).   Run:  bash tools/setup_termux.sh
#
# Why: `pip install -r requirements.txt` fails on Termux -- pip compiles
# matplotlib from source, which needs ninja -> cmake, and cmake stops with
# "iconv is required, but was not found". Termux ships these prebuilt instead
# (checked 2026-10-02 against termux-packages master):
#   matplotlib 3.11.2, python-numpy 2.4.4, python-scipy 1.18.1,
#   python-pillow 12.3.0, python-cryptography 50.0.2
# sympy, networkx and pytest are pure Python, so pip installs them without compiling.
#
# Every step prints what it did; nothing exits silently.

cd "$(dirname "$0")/.." || { echo "STOP: cannot enter the repo folder"; exit 1; }
echo "== repo: $PWD"
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "STOP: $PWD is not a git checkout"; exit 1; }

echo "== 1/4 package lists"
pkg update -y || echo "WARN: pkg update reported an error; continuing"

echo "== 2/4 prebuilt packages"
want="python python-pip git python-numpy python-scipy matplotlib python-pillow python-cryptography"
have=""; missing=""
for p in $want; do
  c=$(apt-cache policy "$p" 2>/dev/null | awk '/Candidate:/ {print $2; exit}')
  if [ -n "$c" ] && [ "$c" != "(none)" ]; then have="$have $p"; else missing="$missing $p"; fi
done
[ -n "$missing" ] && echo "WARN: not in your repositories:$missing"
pkg install -y $have || echo "WARN: pkg install reported an error"

echo "== 3/4 pure-Python packages"
python3 -m pip install sympy networkx pytest || echo "WARN: pip reported an error"

echo "== 4/4 check"
python3 - <<'PY'
import importlib
for name in ("numpy", "scipy", "matplotlib", "PIL", "cryptography", "sympy", "networkx", "pytest"):
    try:
        m = importlib.import_module(name)
        print(f"  ok       {name} {getattr(m, '__version__', '')}")
    except Exception as e:
        print(f"  MISSING  {name}: {e}")
PY
for f in forensic/mdh/strict_linker.py forensic/mdh/supplied/audit_paper_2026_10_02.py math/theorems/k8_case_b_complete.py; do
  if python3 "$f" >/dev/null 2>&1; then echo "  pass     $f"; else echo "  FAIL     $f"; fi
done
python3 -m pytest -q forensic/mdh/test_strict_linker.py forensic/mdh/test_mdh.py 2>&1 | tail -1
echo "== done"
