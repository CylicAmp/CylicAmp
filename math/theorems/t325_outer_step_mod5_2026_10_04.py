# CLASS: OUTER_STEP_MOD5
"""
Processes the 10-node outer step sequence through the Casting Out Fives engine.
Calculates individual node residues and checks the total structural remainder.
(Owner-supplied 2026-10-04; audit: outer_step_mod5_supplied_audit_2026_10_04.py --
the -1 comes from listing 12 at both ends; the 9-node loop's sums are 20 and 20.)
"""

def run_mod5_analysis():
    sequence = [12, 23, 34, 45, 56, 67, 78, 89, 91, 12]
    mod5_sequence = [(int(str(x)[0]) % 5, int(str(x)[1]) % 5) for x in sequence]
    left_mod_sum = sum(p[0] for p in mod5_sequence)
    right_mod_sum = sum(p[1] for p in mod5_sequence)
    print(f"Left {left_mod_sum}  Right {right_mod_sum}  Net {left_mod_sum - right_mod_sum}")
    assert left_mod_sum == 21
    assert right_mod_sum == 22
    assert left_mod_sum - right_mod_sum == -1

if __name__ == "__main__":
    run_mod5_analysis()
