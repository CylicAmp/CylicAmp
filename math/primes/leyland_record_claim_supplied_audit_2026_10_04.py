# CLASS: AUDIT
"""
Audit of supplied record LIT-PRIME-2026 (2026-10-04): "the Leyland record is now
10243^5100 + 5100^10243, 41,080 digits, proved prime by ECPP in 2025". Mathematics only.

DISPROVED
  L1 10243^5100 + 5100^10243 is NOT PRIME: it is divisible by 113 and by 5101 (checked below by
     modular exponentiation). No primality proof of it can exist.
  L2 It has 37,977 digits, not 41,080 (10243 x log10 5100 = 37,976.x).
  L3 Even if it were prime it could not be the record: the 2023 record 104824^5 + 5^104824 has
     73,269 digits (leyland check in prime_families_survey_supplied_audit_2026_10_04.py, S8).

CONSISTENT WITH WHAT WAS ALREADY CHECKED
  L4 HP(49) unresolved past step 119 (a 251-digit composite there); Wolstenholme primes: none other
     below 10^11. Both match the sources recorded on 2026-10-04.

PROTOCOL
  L5 Under the owner's protocol (PROTOCOL.md): a literature lookup with "COMPUTATION: None" cannot
     carry PROOF STATUS "COMPUTATIONALLY VERIFIED"; the sources are not named ("external
     cryptographic and arithmetic research repository database"); and "Distributed Mersenne Prime
     search networks" is not a dependency of any of the three items. Contradiction CONTR-LIT-008's
     resolution in favour of Claim B is therefore rejected for the Leyland part: Claim B's number
     is composite.
FALSIFICATION: any assertion failing.
"""
import math

for p in (113, 5101):                                                                     # L1
    assert (pow(10243, 5100, p) + pow(5100, 10243, p)) % p == 0
assert math.floor(10243 * math.log10(5100)) + 1 == 37977 != 41080                          # L2
assert 5100 * math.log10(10243) < 10243 * math.log10(5100)
assert math.floor(104824 * math.log10(5)) + 1 == 73269 > 37977                            # L3
