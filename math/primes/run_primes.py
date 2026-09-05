"""
run_primes.py

Continuous prime output. Runs forever; stop with Ctrl-C.
Usage:
  python math/primes/run_primes.py
  python math/primes/run_primes.py 10000        # start from 10000
  python math/primes/run_primes.py 10000 500    # start=10000, print every 500th
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prime_engine import prime_generator

start = int(sys.argv[1]) if len(sys.argv) > 1 else 2
every = int(sys.argv[2]) if len(sys.argv) > 2 else 1  # print every Nth prime

count = 0
t0 = time.time()

print(f"  Running prime generator from {start}  (print every {every}, Ctrl-C to stop)")
print(f"  {'#':>8}  {'prime':>12}  {'label':<6}  DR  elapsed")
print(f"  {'-'*52}")

try:
    for p, label, dr in prime_generator(start):
        count += 1
        if count % every == 0:
            elapsed = time.time() - t0
            print(f"  {count:>8}  {p:>12}  {label:<6}  {dr:>2}  {elapsed:.1f}s")
except KeyboardInterrupt:
    elapsed = time.time() - t0
    print(f"\n  Stopped at prime #{count}: {p}  ({elapsed:.1f}s elapsed)")
