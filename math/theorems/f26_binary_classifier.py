"""
F26 Binary Classifier

Final, minimal implementation of the two-state classifier.
No dead branches. No GATED tier. Clean binary partition of {1..36}.

  SINGULARITY (1 node):   {30}      — self-referential, domain ∩ range
  F26_ANCHORS (3 nodes):  {4, 9, 25} — domain maps into range
  PURGE       (32 nodes): all others

Domain (anchors):  {4, 9, 25, 30}   — inputs with DR=3 residues
Range  (targets):  {3, 12, 21, 30}  — DR=3 residues

Bijective map: 4→30, 9→12, 25→21, 30→3
"""

DOMAIN = {4, 9, 25, 30}
RANGE  = {3, 12, 21, 30}


def f26_classifier(node):
    residue = (node * 137) % 37
    if node in DOMAIN and residue in RANGE:
        if node == 30:
            return f"NODE {node}: [SINGULARITY] Self-Referential Fixed Point. SYSTEM ACTIVE."
        return f"NODE {node}: [F26_ANCHORS] Bijective Alignment Confirmed. ACCESS GRANTED."
    else:
        return f"NODE {node}: [PURGE] Entropy detected. SIGNAL TERMINATED."


# Assertions
assert all('F26_ANCHORS' in f26_classifier(n) or 'SINGULARITY' in f26_classifier(n)
           for n in DOMAIN)
assert all('PURGE' in f26_classifier(n) for n in range(1, 37) if n not in DOMAIN)
assert 'SINGULARITY' in f26_classifier(30)


if __name__ == "__main__":
    print(f26_classifier(30))
    print(f26_classifier(4))
    print(f26_classifier(3))
    print(f26_classifier(15))
    print()
    f26 = [n for n in range(1, 37) if 'PURGE' not in f26_classifier(n)]
    print(f"F26 nodes: {f26}  ({len(f26)}/36)")
    print(f"Purge nodes:     {36 - len(f26)}/36")
    print()
    print("All assertions passed.")
