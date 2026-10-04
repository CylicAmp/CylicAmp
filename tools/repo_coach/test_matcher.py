from matcher import find_sensitive, primary_directory, GUIDELINE_DIRECTORIES

FALSE_POSITIVES = [
    "author = 'Michael Song'",
    "def authenticate_user(): pass",
    "# authorized reviewers only",
    "from math import tokenize",
    "SECRETARY_GENERAL = 1",
    "tokenizer.encode(text)",
    "Authority on the subject",
    "secretary_notes.md",
]
TRUE_POSITIVES = [
    ("password = 'hunter2'",                  "password"),
    ("API_KEY = os.environ['X']",             "api_key"),
    ("my_api_key = load()",                   "api_key"),
    ("-----BEGIN PRIVATE KEY-----",           "BEGIN PRIVATE KEY"),
    ("the secret is safe",                    "secret"),
    ("auth = Bearer(...)",                    "auth"),
    ("load('weights.hdf5')",                  "hdf5"),
    ("render via jinja2 template",            "jinja2"),
    ("AWS_SECRET=abc",                        "secret"),
]

print("MUST NOT FLAG (these broke the old substring matcher):")
bad = 0
for s in FALSE_POSITIVES:
    hit = find_sensitive(s)
    ok = not hit
    bad += 0 if ok else 1
    print(f"  {'ok     ' if ok else 'FLAGGED'}  {s:34s} {hit if hit else ''}")

print("\nMUST FLAG (detection must survive the fix):")
missed = 0
for s, expect in TRUE_POSITIVES:
    hit = find_sensitive(s)
    ok = expect in hit
    missed += 0 if ok else 1
    print(f"  {'caught ' if ok else 'MISSED '}  {s:34s} {hit}")

print("\nDIRECTORY FIX:")
print(f"  DATA directories = {GUIDELINE_DIRECTORIES['DATA']}  (was 'data' only)")
print(f"  primary_directory('DATA') = {primary_directory('DATA')!r}")

print(f"\nfalse positives: {bad}   missed detections: {missed}")
assert bad == 0 and missed == 0
print("PASS")
