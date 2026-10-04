# CLASS: HIGH_LOW_PARITY_SPLIT
"""
Automated tracking of the high/low left/right parity framework.
Verifies the binary delta shifts (0 for evens, 2 for odds) between 
the 12346789 and 12345678 systems.
"""

def execute_parity_audit():
    # Sequence A: 1234 | 6789
    seq_A_left = [1, 2, 3, 4]
    seq_A_right = [6, 7, 8, 9]
    
    # Sequence B: 1234 | 5678
    seq_B_left = [1, 2, 3, 4]
    seq_B_right = [5, 6, 7, 8]
    
    # Left sides are identical
    assert seq_A_left == seq_B_left
    
    # Extract structural labels according to the framework definitions
    low_even_R_A = seq_A_right[0] # 6
    low_odd_R_A  = seq_A_right[1] # 7
    high_even_R_A = seq_A_right[2] # 8
    high_odd_R_A  = seq_A_right[3] # 9
    
    low_odd_R_B  = seq_B_right[0] # 5
    low_even_R_B = seq_B_right[1] # 6
    high_odd_R_B  = seq_B_right[2] # 7
    high_even_R_B = seq_B_right[3] # 8
    
    # Compute intersections across the labels
    delta_low_even = low_even_R_A - low_even_R_B
    delta_low_odd  = low_odd_R_A - low_odd_R_B
    delta_high_even = high_even_R_A - high_even_R_B
    delta_high_odd  = high_odd_R_A - high_odd_R_B
    
    print("Label deltas computed:")
    print(f"  Low Even Right Delta: {delta_low_even}")
    print(f"  Low Odd Right Delta: {delta_low_odd}")
    print(f"  High Even Right Delta: {delta_high_even}")
    print(f"  High Odd Right Delta: {delta_high_odd}")
    
    # Hard assertions validating the 0/2 structural split
    assert delta_low_even == 0
    assert delta_low_odd == 2
    assert delta_high_even == 0
    assert delta_high_odd == 2

if __name__ == "__main__":
    execute_parity_audit()
