"""
Run every .py file in math/theorems/ as a subprocess and report pass/fail.
Exit code 0 iff all files pass.
"""

import subprocess
import sys
from pathlib import Path


def main() -> None:
    theorems_dir = Path(__file__).resolve().parent
    self_name = Path(__file__).name

    test_files = sorted(
        f for f in theorems_dir.glob("*.py")
        if f.name != self_name and f.name != "__init__.py"
    )

    if not test_files:
        print("No theorem files found.")
        sys.exit(0)

    passed: list[str] = []
    failed: list[str] = []

    col = max(len(f.name) for f in test_files)

    for f in test_files:
        result = subprocess.run(
            [sys.executable, str(f)],
            capture_output=True,
            text=True,
            timeout=180,
        )
        if result.returncode == 0:
            passed.append(f.name)
            print(f"  PASS  {f.name}")
        else:
            failed.append(f.name)
            print(f"  FAIL  {f.name}")
            # Show first 3 lines of error output
            err_lines = (result.stderr or result.stdout or "").strip().splitlines()
            for line in err_lines[:3]:
                print(f"        {line}")

    total = len(test_files)
    print(f"\n  {len(passed)}/{total} passed", end="")
    if failed:
        print(f"  |  failed: {', '.join(failed)}")
        sys.exit(1)
    else:
        print()
        print("\n✅ All theorem files passed.")


if __name__ == "__main__":
    main()
