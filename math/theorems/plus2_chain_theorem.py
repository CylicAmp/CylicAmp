"""
+2 Chain Theorem: Fixed-Sum Collapse to DR∈{2,4}

Any chain of the form  n + 2 + j  where j = (target - n - 2)
collapses to either 11 or 13, producing DR∈{2,4}.

The +2 step is invariant. The third addend j is the complement
that forces the sum onto {11, 13}.

Observed chains:
  2+2=4+7=11  DR=2    j = 11-2-2 = 7
  4+2=6+7=13  DR=4    j = 13-4-2 = 7
  3+2=5+6=11  DR=2    j = 11-3-2 = 6
  5+2=7+6=13  DR=4    j = 13-5-2 = 6

Meta-structure:
  DR(11) = 2,  DR(13) = 4  -> output always in {2, 4}
  11 + 13 = 24,  DR(24) = 6  (RL-E in Alpha Grid)
   2 +  4 =  6,  DR(6)  = 6  (same DR as sum of targets)
  Both input-DR sum and target sum reduce to DR=6.
"""


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


chains = [
    (2, 2, 7),
    (4, 2, 7),
    (3, 2, 6),
    (5, 2, 6),
]

# All chains sum to 11 or 13
for a, b, c in chains:
    assert a + b + c in {11, 13}
    assert dr(a + b + c) in {2, 4}

# j is always the complement: target - n - 2
for a, b, c in chains:
    target = a + b + c
    assert c == target - a - b

# Meta: DR sums both collapse to 6
assert dr(11 + 13) == 6
assert dr(2 + 4) == 6


if __name__ == "__main__":
    print("+2 Chain Theorem:")
    for a, b, c in chains:
        s = a + b + c
        print(f"  {a}+{b}={a+b}+{c}={s}  DR={dr(s)}  (j={c}={s}-{a}-{b})")
    print()
    print(f"Output DRs always in {{2,4}}")
    print(f"DR(11+13) = DR(24) = {dr(24)}")
    print(f"DR(2+4)   = DR(6)  = {dr(6)}")
    print(f"Both collapse to DR=6 (RL-E)")
    print()
    print("All assertions passed.")
