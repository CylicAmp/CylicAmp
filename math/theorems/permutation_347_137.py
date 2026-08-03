"""
Permutation analysis for digit sets {3,4,7} and {1,3,7}.

{3,4,7}: all 6 permutations have digit sum 14
{1,3,7}: all 6 permutations have digit sum 11
Outliers in user sequences: 753 (sum 15), 373 (sum 13)
"""

from itertools import permutations


def digit_sum(n):
    return sum(int(d) for d in str(n))


def digital_root(n):
    return (n - 1) % 9 + 1 if n > 0 else 9


def analyze_digit_set(digits, label):
    perms = sorted(int(''.join(map(str, p))) for p in permutations(digits))
    sums  = [digit_sum(n) for n in perms]
    print(f"\n{label}")
    print(f"  Permutations: {perms}")
    print(f"  Digit sums:   {sums}  (all {sums[0]}: {all(s==sums[0] for s in sums)})")
    return perms


def analyze_pairs(perms, label):
    print(f"\n  Pairs [{label}]:")
    seen = set()
    for i, a in enumerate(perms):
        for b in perms[i:]:
            key = (min(a,b), max(a,b))
            if key not in seen:
                seen.add(key)
                print(f"    {a} + {b} = {a+b},  {a} - {b} = {a-b}")


def run_assertions():
    from itertools import permutations as _perms

    p347 = sorted(int(''.join(map(str, p))) for p in _perms([3, 4, 7]))
    sums347 = [digit_sum(n) for n in p347]
    assert all(s == 14 for s in sums347), \
        f"{'{3,4,7}'} permutations have digit sums {sums347}, expected all 14"

    p137 = sorted(int(''.join(map(str, p))) for p in _perms([1, 3, 7]))
    sums137 = [digit_sum(n) for n in p137]
    assert all(s == 11 for s in sums137), \
        f"{'{1,3,7}'} permutations have digit sums {sums137}, expected all 11"

    assert len(p347) == 6, "|{3,4,7} perms| must be 6"
    assert len(p137) == 6, "|{1,3,7} perms| must be 6"
    assert digit_sum(753) == 15, "753 has digit sum 15"
    assert digit_sum(373) == 13, "373 has digit sum 13"


if __name__ == "__main__":
    run_assertions()
    print("=" * 50)
    print("PERMUTATION ANALYSIS: {3,4,7} AND {1,3,7}")
    print("=" * 50)

    p347 = analyze_digit_set([3, 4, 7], "{3,4,7}")
    analyze_pairs(p347, "3-4-7")

    p137 = analyze_digit_set([1, 3, 7], "{1,3,7}")
    analyze_pairs(p137, "1-3-7")

    print("\nOutliers from user sequences:")
    for n, expected in [(753, 15), (373, 13)]:
        ds = digit_sum(n)
        print(f"  {n}: digit sum = {ds}  ({'matches' if ds==expected else 'MISMATCH'})")

    print("\nMod-37 membership:")
    qr37 = set(pow(3, k, 37) for k in range(1, 19))
    for n in p347 + p137:
        print(f"  {n} mod 37 = {n%37},  in QR_37: {n%37 in qr37}")
