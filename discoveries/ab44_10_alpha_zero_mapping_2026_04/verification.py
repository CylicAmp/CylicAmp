# Digit to Alpha label mapping
digit_to_label = {
    1: "ALO", 2: "ALE", 3: "AHO", 4: "AHE",
    5: "A51", 6: "BLE", 7: "BLO", 8: "BHE", 9: "BHO"
}

def get_ab_pattern(digits):
    ab = ["A" if d <= 5 else "B" for d in digits]
    return "".join(ab)

def get_parity(digits):
    parity = ["O" if d % 2 == 1 else "E" for d in digits]
    return "".join(parity)

print("AB44=10 → Alpha Zero Mapping (All 24 Structures)\n")
print(f"{'#':<3} {'Structure':<6} {'Labels':<30} {'A/B':<6} {'Parity':<6} {'AZ Level'}")

structures = [
    1289,1379,1469,2198,2378,2468,3197,3287,3467,4196,4286,4376,
    9821,9731,9641,8912,8732,8642,7913,7823,7643,6914,6824,6734
]

for i, num in enumerate(structures, 1):
    digits = [int(c) for c in str(num)]
    labels = "-".join(digit_to_label[d] for d in digits)
    ab_pat = get_ab_pattern(digits)
    parity = get_parity(digits)
    outer = digits[0]
    if outer in [1, 9]: az = "AZ1"
    elif outer in [2, 8]: az = "AZ2"
    elif outer in [3, 7]: az = "AZ3"
    elif outer in [4, 6]: az = "AZ4"
    else: az = "?"
    print(f"{i:<3} {num:<6} {labels:<30} {ab_pat:<6} {parity:<6} {az}")
