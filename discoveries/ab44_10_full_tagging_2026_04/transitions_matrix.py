print("AB44=10 Transition Matrix (Parity-Based)\n")

states = [
    ("1289","OEEO"),("1379","OOOO"),("1469","OEEO"),
    ("2198","EOOE"),("2378","EOOE"),("2468","EEEE"),
    ("3197","OOOO"),("3287","OEEO"),("3467","OEEO"),
    ("4196","EOOE"),("4286","EEEE"),("4376","EOOE"),
    ("9821","OEEO"),("9731","OOOO"),("9641","OEEO"),
    ("8912","EOOE"),("8732","EOOE"),("8642","EEEE"),
    ("7913","OOOO"),("7823","OEEO"),("7643","OEEO"),
    ("6914","EOOE"),("6824","EEEE"),("6734","EOOE"),
]

A51 = [s for s, p in states if p in ["OEEO", "OOOO"]]
AZ1 = [s for s, p in states if p in ["EOOE", "EEEE"]]

print("A51 → AZ1 transitions:\n")
for s in A51:
    print(f"{s} -> {', '.join(AZ1)}")

print("\nAZ1 → A51 transitions:\n")
for s in AZ1:
    print(f"{s} -> {', '.join(A51)}")
