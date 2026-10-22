# CLASS: AUDIT
"""
Checks of the owner's engine: tools/owner_engine.py (Python) and dashboards/owner_engine/index.html (the page),
built 2026-10-22 from owner_work #416 ("can you put my work together into a functional algorithm that's going to
get me somewhere?"). Plain Python; the browser part needs playwright and Chromium and is skipped if they are missing.
Run: python3 dashboards/owner_engine/check_owner_engine.py

1. Every rule of the owner's work in tools/owner_engine.py passes, and the control (a false rule) fails.
2. The walk: from n = 3 on, a twin pair 2n - 1, 2n + 1 only comes at place 3 of 1 2 3; the hits n / 3 are the m of
   OEIS A002822 ("Numbers m such that 6m-1, 6m+1 are twin primes", first 40 terms fetched 2026-10-22).
3. The page computes the same profile as Python for a list of numbers, the same walk, and shows PASS on every rule
   and FAIL on the control.

FALSIFICATION: any assertion failing.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import owner_engine as E  # noqa: E402

# 1. the rules
results, control = E.check()
assert all(ok for *_, ok in results), [r for r in results if not r[3]]
assert len(results) == 12 and control is False

# 2. the walk and OEIS A002822
A002822 = [1, 2, 3, 5, 7, 10, 12, 17, 18, 23, 25, 30, 32, 33, 38, 40, 45, 47, 52, 58, 70, 72, 77, 87, 95, 100,
           103, 107, 110, 135, 137, 138, 143, 147, 170, 172, 175, 177, 182, 192]
w = E.walk(1, 600)
assert w["missed"] == [] and w["pairs"][0] == (2, 3, 5)
hits = [n for n, lo, hi in w["pairs"] if n > 2]
assert [n // 3 for n in hits] == A002822 and all(n % 3 == 0 for n in hits)
assert w["three_ends"] == [3, 9]

# the profile of 137, spot values
p = E.profile(137)
assert p["chain"] == [137, 11, 2] and p["flip"]["flip"] == 731 and p["frameworks"]["twins"] == [139]
assert p["frameworks"]["orbit"] == "IC" and p["frameworks"]["loop_of_1_over_n"] == 8
assert p["neighbours"]["different"] == 11 and p["halving"]["roots"] == [2, 1, 5, 7]
assert E.profile(3)["one_two_three"]["three_ends"] and E.profile(3)["one_two_three"]["three"]["pre"] == "125"

# 3. the page
NUMBERS = [1, 2, 3, 4, 5, 9, 13, 41, 99, 100, 137, 246, 891, 1009, 1137, 7919, 9999, 123456, 1009019, 9999999]
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

if sync_playwright is not None:
    import os
    exe = "/opt/pw-browsers/chromium" if os.path.exists("/opt/pw-browsers/chromium") else None
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()
            page = browser.new_page()
            page.goto((HERE / "index.html").as_uri())
            page.wait_for_function("window.OwnerEngineChecks && window.OwnerEngineChecks.length === 13", timeout=120000)
            for n in NUMBERS:
                js = json.loads(page.evaluate("n => JSON.stringify(window.OwnerEngine.profile(n))", n))
                py = json.loads(json.dumps(E.profile(n)))
                assert js == py, (n, [k for k in py if js.get(k) != py[k]])
            jw = json.loads(page.evaluate("() => JSON.stringify(window.OwnerEngine.walk(1, 5000))"))
            pw_ = E.walk(1, 5000)
            assert [tuple(x) for x in jw["pairs"]] == pw_["pairs"] and jw["missed"] == [] and jw["predicted"] == pw_["predicted"]
            checks = page.evaluate("() => window.OwnerEngineChecks")
            assert [c["ok"] for c in checks[:-1]] == [True] * 12 and checks[-1]["message"] == "control" and checks[-1]["ok"] is False
            badges = page.locator(".badge").all_inner_texts()
            assert badges == ["PASS"] * 12 + ["FAIL"], badges
            assert page.locator("#ledger .row").count() == 11
            browser.close()
        print("page: same answers as Python for %d numbers and the walk to 5000; 12 PASS, control FAIL" % len(NUMBERS))
    except Exception as e:  # a missing browser binary is not a failure of the mathematics
        if "Executable doesn't exist" in str(e) or "BrowserType.launch" in str(e):
            print("browser part skipped:", str(e).splitlines()[0])
        else:
            raise

if __name__ == "__main__":
    print("owner engine: 12 rules PASS, control FAIL; walk hits / 3 = OEIS A002822 (40 terms); 3-step ends at 3 and 9")
