#!/data/data/com.termux/files/usr/bin/bash
# Set up CylicAmp's Python dependencies on Android (Termux).
#
# `pip install -r requirements.txt` fails on Termux: pip tries to compile
# matplotlib from source, which needs ninja -> cmake, and the cmake build stops
# with "iconv is required, but was not found". numpy and scipy would also have
# to compile. Termux ships all four already built, at versions that satisfy
# requirements.txt (checked 2026-10-02 against termux-packages master):
#   matplotlib 3.11.2, python-numpy 2.4.4, python-scipy 1.18.1, python-pillow 12.3.0
# Installed this way, pip finds them satisfied and only fetches sympy (pure Python).
#
# Run from inside the CylicAmp folder:   bash tools/setup_termux.sh
set -e
pkg install -y python python-pip git matplotlib python-numpy python-scipy python-pillow
pip install -r requirements.txt
pip install pytest
python3 - <<'PY'
import sympy, numpy, scipy, matplotlib, PIL
print("ok: sympy", sympy.__version__, "| numpy", numpy.__version__, "| scipy", scipy.__version__,
      "| matplotlib", matplotlib.__version__, "| pillow", PIL.__version__)
PY
