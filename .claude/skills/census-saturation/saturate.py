"""Run a census at several bounds and report whether the shape count settled."""
import subprocess, sys

def saturated(counts, factor=3.0):
    """counts: [(bound, n_shapes)] ascending. Flat over a >= factor range?"""
    if len(counts) < 2:
        return None, "need at least two bounds"
    last = counts[-1][1]
    flat = [b for b, n in counts if n == last]
    if not flat or len(flat) < 2:
        return False, f"count still rising: {counts[-2][1]} -> {last}"
    span = counts[-1][0] / flat[0]
    if span >= factor:
        return True, f"flat at {last} from {flat[0]} to {counts[-1][0]} ({span:.1f}x range)"
    return False, f"flat only over {span:.1f}x; need {factor}x"

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(__doc__)
        print("usage: saturate.py <census_script> B1 B2 B3 ...")
        print("  census_script must print the shape count for the bound given as argv[1]")
        sys.exit(2)
    script, bounds = sys.argv[1], [int(b) for b in sys.argv[2:]]
    counts = []
    for b in bounds:
        out = subprocess.run([sys.executable, script, str(b)],
                             capture_output=True, text=True).stdout.strip().splitlines()
        counts.append((b, int(out[-1].split()[-1])))
        print(f"  n <= {b:>10} : {counts[-1][1]:5} shapes")
    ok, why = saturated(counts)
    print(f"\nSATURATED: {ok} -- {why}")
    if not ok:
        print("The census is a SAMPLE. Do not write that these shapes cover the branch.")
    sys.exit(0 if ok else 1)
