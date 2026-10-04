# CLASS: IDENTITY
"""
EX-001, the worked example of the owner's Mathematical Audit Protocol
(.claude/skills/audit-supplied/PROTOCOL.md), as a runnable record.

ID: EX-001
STATEMENT: For the integers 2 and 3, 2 + 3 = 5.
OBJECT CLASSIFICATION: IDENTITY
AUDIT LEVEL: A3 INDEPENDENT CROSS-CHECK
VERIFICATION MODE: DIRECT-CALCULATION, INDEPENDENT-CROSS-CHECK, REPRODUCIBLE
PROOF STATUS: PROVED
EVIDENCE: direct addition; independent count of five objects (below, as list lengths).
SCOPE: the stated integer inputs and ordinary integer addition.
DEPENDENCIES: integer addition; inputs 2 and 3; none unresolved.
REPRODUCTION: python3 math/theorems/ex001_protocol_example.py
"""
assert 2 + 3 == 5
assert len(["*"] * 2 + ["*"] * 3) == 5
