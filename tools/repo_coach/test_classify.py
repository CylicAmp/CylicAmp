from classify import classify, ContentType as C

CASES = [
    # the original DATA-regex failures
    ("for i in range(3):\n    print(i)",                 C.CODE),
    ("x, y = 1, 2",                                      C.CODE),
    ("# a note: see below\nprint('hi')",                 C.CODE),
    # the original ordering failures
    ("def test_sum():\n    assert 1 + 1 == 2",           C.TESTS),
    ("import pytest\n\ndef check():\n    pass",          C.TESTS),
    ("class TestThing:\n    def run(self):\n        pass", C.TESTS),
    # the original substring failures
    ("The latest version notes are here.\n\nSee below.", C.DOCUMENTATION),
    ("import sys\nsys.exit(0)",                          C.CODE),
    # genuine data
    ('{"a": 1, "b": [2, 3]}',                            C.DATA),
    ("name,score\nalice,10\nbob,12",                     C.DATA),
    # config
    ("[server]\nhost = localhost\nport = 8080",          C.CONFIGURATION),
    # docs
    ("# Getting Started\n\nInstall it, then run it.",    C.DOCUMENTATION),
    ("- first item\n- second item\n- third",             C.DOCUMENTATION),
    # javascript
    ("function add(a, b) { return a + b; }",             C.CODE),
    ("describe('add', () => { it('works', () => {}); });", C.TESTS),
    # plain code
    ("def f(x):\n    return x * 2",                      C.CODE),
]

print(f"{'expected':<14} {'got':<14} input")
print("-" * 72)
bad = 0
for text, expect in CASES:
    got, why = classify(text)
    ok = got is expect
    bad += 0 if ok else 1
    shown = text.replace("\n", "\\n")[:40]
    mark = "" if ok else "   <-- MISMATCH"
    print(f"{expect.value:<14} {got.value:<14} {shown}{mark}")

print(f"\nmismatches: {bad}")
assert bad == 0
print("PASS")
