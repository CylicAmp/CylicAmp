---
name: standalone-export
description: Produce a dependency-free, self-checking Python file of a result so the owner can run it anywhere (phone, online Python) and have it tested outside this environment. Use whenever the owner asks for code to show or test elsewhere, and for any result worth independent verification. Worked example: math/theorems/grid81_standalone.py -- plain Python 3, prints PASS/FAIL per claim, re-checks the general claims up to 1,000,000.
---

# standalone-export

1. **No imports beyond the standard library.** Replace sympy with a small
   sieve or Miller-Rabin written in the file.
2. **One `check(name, ok)` per claim**, printing PASS or FAIL, and a final
   ALL PASS / SOME CHECKS FAILED line.
3. **Test beyond the example.** If the claim is general (about all primes),
   check it far past the displayed range (LIMIT = 10**6) as well as on the
   displayed cases, and cross-check any shortcut formula against the slow
   definition (dr formula vs repeated digit sum).
4. **Run it here first**, time it (it should finish in seconds), commit it.
5. **Give the owner** the path, the phone command
   (`cd ~/CylicAmp-real && git pull`, then `python <path>`), and the full
   code inline so it can be pasted into any Python 3 runner.
