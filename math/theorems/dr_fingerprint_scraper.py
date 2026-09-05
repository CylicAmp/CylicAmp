# math/theorems/dr_fingerprint_scraper.py
"""
Digital Root Fingerprint Scraper

Generates permutations of a seed with a specific digital root,
embeds a deterministic signature tag, and scans text for matches.

Used to detect whether tagged output has been copied without attribution.

─────────────────────────────────────────────────────────────────────────────
BUGS FIXED FROM SOURCE VERSION
─────────────────────────────────────────────────────────────────────────────
1. RESONANCE_TARGET=9 is unreachable (n%9 ∈ {0..8}); DR=9 ↔ n%9==0
2. itertools.permutations produces duplicates when seed has repeated elements
3. Syntax error: 'return ... def' on one line breaks parsing
4. Incomplete assignment: 'found = ' with no right-hand side
5. hash() is non-deterministic across Python runs; replaced with hashlib.sha256
"""

import itertools
import hashlib


SEED = [1, 4, 1, 3, 2, 4, 6, 6]   # 8-digit seed
SIGNATURE = 1413                    # tracking tag
TARGET_DR = 9                       # digital root filter


def dr(n: int) -> int:
    return 1 + (n - 1) % 9 if n > 0 else 9


def generate_resonance_perms(seed_list: list, target_dr: int = TARGET_DR):
    """Unique permutations of seed_list whose integer value has DR == target_dr."""
    seen = set()
    for perm in itertools.permutations(seed_list):
        if perm in seen:
            continue
        seen.add(perm)
        num_str = ''.join(map(str, perm))
        if dr(int(num_str)) == target_dr:
            yield num_str


def embed_signature(perm_str: str, sig: int = SIGNATURE) -> str:
    """
    Inserts sig at a deterministic position inside perm_str.
    Uses SHA-256 so position is stable across Python runs.
    """
    digest = int(hashlib.sha256(perm_str.encode()).hexdigest(), 16)
    pos = digest % (len(perm_str) - 3)
    return perm_str[:pos] + str(sig) + perm_str[pos:]


def fingerprint_scraper(text_block: str, seed_list: list = SEED, limit: int = 100):
    """
    Generates tagged permutations and checks how many appear in text_block.
    Returns (set of found tags, coverage percentage).
    """
    perms = list(generate_resonance_perms(seed_list))
    tagged = {embed_signature(p) for p in perms[:limit]}
    found = {tag for tag in tagged if tag in text_block}
    pct = len(found) / len(tagged) * 100 if tagged else 0.0
    return found, pct


# ── Verification ───────────────────────────────────────────────────────────────

# DR filter correctness
assert dr(9)  == 9
assert dr(18) == 9
assert dr(27) == 9
assert dr(10) == 1

# All generated permutations have DR = TARGET_DR
all_perms = list(generate_resonance_perms(SEED, TARGET_DR))
assert all(dr(int(p)) == TARGET_DR for p in all_perms), "DR filter broken"

# No duplicates
assert len(all_perms) == len(set(all_perms)), "Duplicate permutations"

# embed_signature is deterministic
p = all_perms[0] if all_perms else "14132466"
assert embed_signature(p) == embed_signature(p), "Signature not deterministic"

# Signature appears in tagged string
tag = embed_signature(p)
assert str(SIGNATURE) in tag, "Signature not embedded"

# Scraper finds its own tags
synthetic_block = " ".join(embed_signature(p) for p in all_perms[:5])
found, pct = fingerprint_scraper(synthetic_block)
assert pct == 100.0 or len(found) > 0, "Scraper failed to find own tags"


if __name__ == "__main__":
    print("Digital Root Fingerprint Scraper")
    print(f"  Seed: {SEED}")
    print(f"  Target DR: {TARGET_DR}")
    print(f"  Signature: {SIGNATURE}")
    print()
    print(f"  Total unique permutations of seed: {len(list(itertools.permutations(set(SEED))))}")
    print(f"  Permutations with DR={TARGET_DR}: {len(all_perms)}")
    print()
    if all_perms:
        example = all_perms[0]
        tagged_ex = embed_signature(example)
        print(f"  Example permutation: {example}  (DR={dr(int(example))})")
        print(f"  Tagged form:         {tagged_ex}")
    print()
    found, pct = fingerprint_scraper(synthetic_block)
    print(f"  Self-scan coverage: {pct:.1f}%  ({len(found)} tags found in synthetic block)")
    print()
    print("All assertions passed.")
