# CLASS: WORKLOAD_ACCELERATOR
"""
Core automated workbench for the T325 framework.
Ingests numerical strings, processes them through the 45-capacity drain loops,
applies the T432 carry map, filters mod 5/9, and tracks high/low parity splits.
"""
import sys

def get_digital_root(n):
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r

def cast_out_fives(n):
    return n % 5

def analyze_raw_number(n):
    """Instantly extracts the complete multi-operational signature of a target value."""
    s_num = str(n)
    digit_list = [int(char) for char in s_num if char.isdigit()]
    digit_sum = sum(digit_list)
    
    # 1. Container Fill & Drain Metrics
    full_45_bins = digit_sum // 45
    remainder_fill = digit_sum % 45
    
    # 2. Modulo Grid Lines
    mod9 = get_digital_root(n)
    mod5 = cast_out_fives(n)
    
    # 3. High/Low Parity Split Mapping (Left vs Right half)
    half_len = len(digit_list) // 2
    left_half = digit_list[:half_len] if half_len > 0 else digit_list
    right_half = digit_list[half_len:] if half_len > 0 else []
    
    print(f"==================================================")
    print(f"T325 ENGINE DATA LOG FOR INPUT VALUE: {n}")
    print(f"==================================================")
    print(f"COLUMN LENGTH : {len(s_num)} digits")
    print(f"DIGIT SUM     : {digit_sum}")
    print(f"ROOTS         : Mod 9 -> {mod9} | Mod 5 -> {mod5}")
    print(f"45-CONTAINERS : Full: {full_45_bins} | Active Fill Level: {remainder_fill}/45")
    print(f"SPATIAL SPLIT : Left Array: {left_half} | Right Array: {right_half}")
    
    # Isolate Extreme Left High Even / Right Low Even if the tokens match
    if 4 in left_half and 6 in right_half:
        print("  -> FLAG: [4-0-6] High Even Left & Low Even Right Boundaries Locked.")
    print(f"==================================================\n")
    return {
        "sum": digit_sum, "mod9": mod9, "mod5": mod5, 
        "bins": full_45_bins, "fill": remainder_fill
    }

def process_21_row_block_rotation(b1, b2, b3):
    """Simulates the 3x7 structural block-rotation gears automatically."""
    print("EXECUTING 21-ROW MATRIX GENERATION SEQUENCE...")
    blocks = [list(b1), list(b2), list(b3)]
    
    # Pre-calculated rotation indices to preserve the 8-root matrix track
    for r in range(1, 22):
        row_str = "".join(blocks[0]) + "".join(blocks[1]) + "".join(blocks[2])
        val = int(row_str)
        root = get_digital_root(val)
        
        # Verify the invariant law of the 8-family holds
        assert root == 8
        print(f"  Row {r:02d}: {row_str[:3]}-{row_str[3:6]}-{row_str[6:]} | Invariant Root: {root}")
        
        # Clockwise shuffle operations mapping the 3x7 gear teeth
        if r % 3 == 0:
            blocks[0] = blocks[0][1:] + blocks[0][:1]
        if r % 7 == 0:
            blocks[1] = blocks[1][1:] + blocks[1][:1]
        blocks[2] = blocks[2][2:] + blocks[2][:2]

if __name__ == "__main__":
    # Test 1: Validate the 405 Saturated Matrix Capacity
    grid_audit = analyze_raw_number(405)
    assert grid_audit["sum"] == 9
    assert grid_audit["mod9"] == 9
    assert grid_audit["mod5"] == 0
    
    # Test 2: Run the 100th Prime milestone
    analyze_raw_number(541)
    
    # Test 3: Run the High/Low boundary lock
    analyze_raw_number(406)
    
    # Test 4: Run the Master Block Rotation Sequence
    process_21_row_block_rotation("246", "572", "135")
