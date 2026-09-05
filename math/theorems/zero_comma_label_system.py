"""
Zero-Comma Labeling System

n zeros (n ≥ 4) split by standard thousands-grouping.
Each zero-string gets a label built from three rules:

  entry    = n - 3   (1-indexed from n=4)
  first    = DR(entry)              cycles 1..9 as n grows
  K        = floor((n-1)/3)         number of commas in zero-string
  left_size = n mod 3  (0 → 3)     size of leftmost group (1, 2, or 3)

  Label digits:
    K = 1  → first + "1" + str(left_size)     (3 digits, varies within level)
    K ≥ 2  → first + "".join(str(k)+"3"       (grows by 2 digits per level,
                             for k=1..K)        same within each level)

  Display: label_digits formatted as a number (commas or decimal at 9+).

STRUCTURE:
  Each level contains exactly 3 zero-strings (n ≡ 1,2,0 mod 3).
  Within a K≥2 level, the suffix is IDENTICAL for all three — only
  the first digit (DR of entry) changes.
  Adding 3 zeros (n → n+3) appends one more "(K+1)3" to the suffix.
  This sequence has no ceiling.

WHY K=1 DIFFERS:
  When there is only one comma, the right group is always 3 zeros.
  The label encodes left_size (1,2,3) as the third digit, creating
  palindromes (111, 212, 313) for the first cycle where DR(entry)=left_size.
  From K≥2 onward, all right groups are 3 and get encoded as "3",
  interleaved with comma ordinals (1,2,3,...).

LEVEL TABLE:
  K  n-range   label size  suffix (fixed within level)
  1  4-6        3 digits    "1" + left_size (varies)
  2  7-9        5 digits    "1323"
  3  10-12      7 digits    "132333"
  4  13-15      9 digits    "13233343"  (displayed X.XXXXXXXX)
  5  16-18     11 digits    "1323334353"
  ...
  K  ...       2K+1 digits  "".join(str(k)+"3" for k in 1..K)
"""


def dr(n):
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


def comma_groups(n):
    if n <= 0:
        return []
    groups, r = [], n
    while r > 3:
        groups.append(3)
        r -= 3
    groups.append(r)
    return list(reversed(groups))


def zero_string(n):
    return ",".join("0" * g for g in comma_groups(n))


def label_digits(n):
    """Raw label digits (no formatting) for n zeros (n ≥ 4)."""
    assert n >= 4
    entry = n - 3
    first = dr(entry)
    K = (n - 1) // 3
    left_size = n % 3 or 3
    if K == 1:
        suffix = "1" + str(left_size)
    else:
        suffix = "".join(str(k) + "3" for k in range(1, K + 1))
    return str(first) + suffix


def format_label(raw):
    """Display raw label digits as a number (commas or decimal)."""
    if len(raw) <= 3:
        return raw
    if len(raw) <= 7:
        return "{:,}".format(int(raw))
    # 9+ digits: first digit . rest (avoids commas at large scale)
    return raw[0] + "." + raw[1:]


# ---------------------------------------------------------------------------
# Assertions — verify every published example
# ---------------------------------------------------------------------------

_examples = {
    4:  "111",
    5:  "212",
    6:  "313",
    7:  "41323",
    8:  "51323",
    9:  "61323",
    10: "7132333",
    11: "8132333",
    12: "9132333",
    13: "113233343",
    14: "213233343",
    15: "313233343",
}

for n, expected in _examples.items():
    got = label_digits(n)
    assert got == expected, f"n={n}: got {got!r}, expected {expected!r}"

# DR cycling: first digit = DR(entry) = DR(n-3), period 9
for n in range(4, 40):
    assert int(label_digits(n)[0]) == dr(n - 3), f"n={n}: first digit mismatch"

# Level suffix identical for all 3 members when K ≥ 2
for K in range(2, 7):
    ns = [n for n in range(4, 50) if (n - 1) // 3 == K]
    suffixes = {label_digits(n)[1:] for n in ns}
    assert len(suffixes) == 1, f"K={K}: suffixes differ: {suffixes}"

# Suffix length = 2K for K ≥ 2
for K in range(2, 7):
    n = 3 * K + 1  # first n in this level
    raw = label_digits(n)
    assert len(raw) == 2 * K + 1, f"K={K}: label length {len(raw)} ≠ 2K+1={2*K+1}"


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Zero-Comma Labeling System")
    print("=" * 72)
    print()
    print(f"  {'n':>3}  {'zero-string':>26}  K  {'label_raw':<18}  formatted")
    print("  " + "-" * 68)

    for n in range(4, 22):
        zs = zero_string(n)
        K = (n - 1) // 3
        raw = label_digits(n)
        fmt = format_label(raw)
        lv = "← K=1 (varies)" if K == 1 else ""
        print(f"  {n:>3}  {zs:>26}  {K}  {raw:<18}  {fmt}  {lv}")

    print()
    print("Level suffix table (K ≥ 2 — fixed within each level):")
    for K in range(2, 8):
        suffix = "".join(str(k) + "3" for k in range(1, K + 1))
        n_range = f"n = {3*K+1}–{3*(K+1)}"
        print(f"  K={K}  {n_range:<12}  suffix = '{suffix}'")

    print()
    print("DR of entry cycles 1→9 forever:")
    entries = [dr(n - 3) for n in range(4, 22)]
    print(f"  {entries}")
    print()
    print("All assertions passed.")
