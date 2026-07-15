"""
Magnitude Tier Framework

Each tier n defines:
  Null state:       0...0  (n+3 digits)
  Activation (1):   1 followed by zeros
  Saturation (9):   9...9  (n+3 digits)
  Resonance sig:    tier# — computed value

The resonance signature stabilizes to +1111 increments from tier 4.
"""


def digital_root(n):
    n = abs(int(n))
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


TIERS = [
    {"tier": 1,  "null": 0,                      "activation": 1,                      "saturation": 9,                      "resonance": 41},
    {"tier": 2,  "null": 0,                       "activation": 10,                     "saturation": 99,                     "resonance": 591},
    {"tier": 3,  "null": 0,                        "activation": 100,                    "saturation": 999,                    "resonance": 6151},
    {"tier": 4,  "null": 0,                         "activation": 1000,                   "saturation": 9999,                   "resonance": 7222},
    {"tier": 5,  "null": 0,                          "activation": 10000,                  "saturation": 99999,                  "resonance": 8333},
    {"tier": 6,  "null": 0,                           "activation": 100000,                 "saturation": 999999,                 "resonance": 9444},
    {"tier": 7,  "null": 0,                            "activation": 1000000,                "saturation": 9999999,                "resonance": 10555},
    {"tier": 8,  "null": 0,                             "activation": 10000000,               "saturation": 99999999,               "resonance": 11666},
    {"tier": 9,  "null": 0,                              "activation": 100000000,              "saturation": 999999999,              "resonance": 12777},
    {"tier": 10, "null": 0,                               "activation": 1000000000,             "saturation": 9999999999,             "resonance": 13888},
    {"tier": 11, "null": 0,                                "activation": 10000000000,            "saturation": 99999999999,            "resonance": 14999},
    {"tier": 12, "null": 0,                                 "activation": 100000000000,           "saturation": 999999999999,           "resonance": 16110},
    {"tier": 13, "null": 0,                                  "activation": 1000000000000,          "saturation": 9999999999999,          "resonance": 17221},
    {"tier": 14, "null": 0,                                   "activation": 10000000000000,         "saturation": 99999999999999,         "resonance": 18332},
    {"tier": 15, "null": 0,                                    "activation": 100000000000000,        "saturation": 999999999999999,        "resonance": 19443},
    {"tier": 16, "null": 0,                                     "activation": 1000000000000000,       "saturation": 9999999999999999,       "resonance": 20554},
    {"tier": 17, "null": 0,                                      "activation": 10000000000000000,      "saturation": 99999999999999999,      "resonance": 21665},
    {"tier": 18, "null": 0,                                       "activation": 100000000000000000,     "saturation": 999999999999999999,     "resonance": 22776},
    {"tier": 19, "null": 0,                                        "activation": 1000000000000000000,    "saturation": 9999999999999999999,    "resonance": 23887},
    {"tier": 20, "null": 0,                                         "activation": 10000000000000000000,   "saturation": 99999999999999999999,   "resonance": 24998},
    {"tier": 21, "null": 0,                                          "activation": 100000000000000000000,  "saturation": 999999999999999999999,  "resonance": 26109},
]


def analyze_tier(t):
    r = t["resonance"]
    a = t["activation"]
    s = t["saturation"]
    n = t["tier"]
    return {
        "tier":           n,
        "activation":     a,
        "saturation":     s,
        "resonance":      r,
        "res_dr":         digital_root(r),
        "res_mod37":      r % 37,
        "act_mod37":      a % 37,
        "sat_mod37":      s % 37,
        "sat_dr":         digital_root(s),   # always 9
        "act_dr":         digital_root(a),   # always 1
    }


def resonance_delta():
    """Differences between consecutive resonance signatures."""
    return [
        TIERS[i+1]["resonance"] - TIERS[i]["resonance"]
        for i in range(len(TIERS) - 1)
    ]


if __name__ == "__main__":
    print("MAGNITUDE TIER ANALYSIS")
    print("=" * 70)
    print(f"{'Tier':>4}  {'Resonance':>8}  {'DR':>3}  {'mod37':>6}  {'Act mod37':>9}  {'Sat mod37':>9}")
    print("-" * 70)
    for t in TIERS:
        a = analyze_tier(t)
        print(f"{a['tier']:>4}  {a['resonance']:>8}  {a['res_dr']:>3}  {a['res_mod37']:>6}  {a['act_mod37']:>9}  {a['sat_mod37']:>9}")

    print()
    print("Resonance deltas (consecutive differences):")
    deltas = resonance_delta()
    for i, d in enumerate(deltas):
        print(f"  tier {i+1} → {i+2}: +{d}")

    print()
    print("Resonance signatures mod 37:")
    for t in TIERS:
        r = t["resonance"]
        print(f"  tier {t['tier']:>2}: {r} mod 37 = {r % 37}  DR = {digital_root(r)}")
