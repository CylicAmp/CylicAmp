"""
GroupFramework — Primitive Roots 20 and 17 mod 37

Payload X = 23572481523

Core property:
    X % 37 == X % 11 == X % 407 == 8
    407 = 37 × 11 (CRT: gcd(37,11)=1 ensures uniqueness mod 407)

Generators: 20 and 17 are both primitive roots mod 37 (order 36).

Orbital symmetry:
    step_A = 3:  20^3 % 37 = 8  (target node)
    step_B = 33: 17^33 % 37 = 23 (17^(-3) mod 37, since 33 + 3 = 36)
    Product: 20^3 × 17^33 ≡ 8 × 23 ≡ 36 ≡ -1 (mod 37)

Cascade connections:
    8 × 20 mod 37 = 12  (sovereign target)
    8 × 17 mod 37 = 25  (sovereign anchor)
    37 - 20 - 17 = 0    (generators sum to the prime)
    37 - (20 + 8) = 9   = 3² = DR fixed point

Boundary derivation:
    DR(136) = 1, DR(296) = 8
    exponent = (1 + 8) // 3 = 3
    20^3 % 37 = 8 = target
"""

def digital_root(n):
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


class GroupFramework:
    def __init__(self, payload_str):
        self.X = int(payload_str)
        self.mod_primary = 37
        self.mod_secondary = 11
        self.mod_tertiary = 407
        self.gen_A = 20
        self.gen_B = 17
        self.target = self.X % self.mod_primary

    def run_tests(self):
        print("==================================================")
        print(f"FRAMEWORK INITIALIZATION: PAYLOAD X = {self.X}")
        print("==================================================\n")

        self._test_independent_residues()
        self._test_orbital_indexing()
        self._test_subtraction_matrices()
        self._test_multiplicative_products()
        self._test_fractions_and_percentages()
        self._test_inequalities()
        self._test_digital_roots()
        self._test_integrated_equations()

    def _test_independent_residues(self):
        print("--- 1. Base-Independent Residues ---")
        print(f"X % 37  == {self.X % self.mod_primary}  (Expected: {self.target})")
        print(f"X % 11  == {self.X % self.mod_secondary}  (Expected: {self.target})")
        print(f"X % 407 == {self.X % self.mod_tertiary}  (Expected: {self.target})")
        print(f"Proof: 37 * 11 == {self.mod_primary * self.mod_secondary}\n")

    def _test_orbital_indexing(self):
        print("--- 2. Orbital Indexing (Modulo 37) ---")
        step_A = 3
        step_B = 33
        print(f"{self.gen_A}^{step_A} % 37 == {(self.gen_A**step_A) % self.mod_primary}")
        print(f"{self.gen_B}^{step_B} % 37 == {(self.gen_B**step_B) % self.mod_primary}")
        prod = ((self.gen_A**step_A) * (self.gen_B**step_B)) % self.mod_primary
        print(f"20^3 × 17^33 mod 37 == {prod}  (≡ -1 mod 37: {prod == 36})\n")

    def _test_subtraction_matrices(self):
        print("--- 3. Subtraction Matrices & Linear Recurrence ---")
        print(f"37 - 20 - 17 = {37 - 20 - 17}")
        print(f"37 - (20 + 8) = {37 - (20 + 8)} (Matches 3^2: {3**2 == 37 - (20 + 8)})")
        print(f"20 - 17 = {20 - 17}")
        print(f"17 - 8  = {17 - 8}")
        print(f"20 - 8  = {20 - 8}\n")

    def _test_multiplicative_products(self):
        print("--- 4. Multiplicative Products ---")
        print(f"17 * 20 = {17 * 20}  | Modulo 37 -> {(17 * 20) % self.mod_primary}")
        print(f"17 * 37 = {17 * 37}")
        print(f"20 * 37 = {20 * 37}")
        print(f"17 * 20 * 37 = {17 * 20 * 37}")
        print(f"8 * 37 = {8 * 37}")
        print(f"8 * 20 = {8 * 20}  | Modulo 37 -> {(8 * 20) % self.mod_primary}  (sovereign target)")
        print(f"8 * 17 = {8 * 17}  | Modulo 37 -> {(8 * 17) % self.mod_primary}  (sovereign anchor)\n")

    def _test_fractions_and_percentages(self):
        print("--- 5. Division, Ratios & Percentages ---")
        print(f"17 / 20 = {17 / 20:.4f}  | Percentage: {(17 / 20) * 100:.2f}%")
        print(f"20 / 17 = {20 / 17:.4f}  | Percentage: {(20 / 17) * 100:.2f}%")
        print(f"17 / 37 = {17 / 37:.4f}  | Percentage: {(17 / 37) * 100:.2f}%")
        print(f"20 / 37 = {20 / 37:.4f}  | Percentage: {(20 / 37) * 100:.2f}%")
        print(f"8 / 37  = {8 / 37:.4f}  | Percentage: {(8 / 37) * 100:.2f}%")
        print(f"8 / 20  = {8 / 20:.4f}  | Percentage: {(8 / 20) * 100:.2f}%")
        print(f"8 / 17  = {8 / 17:.4f}  | Percentage: {(8 / 17) * 100:.2f}%\n")

    def _test_inequalities(self):
        print("--- 6. Inequalities and Magnitude Orderings ---")
        print(f"8 < 17 < 20 < 37 : {8 < 17 < 20 < 37}")
        print(f"17 + 20 <= 37    : {17 + 20 <= 37}")
        print(f"8 + 17 > 20      : {8 + 17 > 20}")
        print(f"8 + 20 < 37      : {8 + 20 < 37}")
        print(f"(17 * 20) > (8 * 37) : {(17 * 20) > (8 * 37)} ({17*20} > {8*37})\n")

    def _test_digital_roots(self):
        print("--- 7. Base-10 Digital Roots (DR) ---")
        terms = {
            "Payload X": self.X,
            "Modulus (37)": 37,
            "Generator A (20)": 20,
            "Generator B (17)": 17,
            "Target Node (8)": 8,
            "17 * 20 (340)": 340,
            "8 * 37 (296)": 296,
            "8 * 20 (160)": 160,
            "8 * 17 (136)": 136,
        }
        for name, val in terms.items():
            print(f"DR of {name} ({val}) -> {digital_root(val)}")
        print()

    def _test_integrated_equations(self):
        print("--- 8. Integrated Framework Equations ---")

        dr_296 = digital_root(296)
        mod_11_val = self.X % 11
        mod_37_val = self.X % 37
        equality_check = (mod_11_val == mod_37_val == dr_296 == self.target)
        print(f"Boundary constraint: X % 11 == X % 37 == DR(296) == 8 -> {equality_check}")

        dr_136 = digital_root(136)
        dr_296 = digital_root(296)
        exponent = (dr_136 + dr_296) // 3
        orbit_check = (self.gen_A ** exponent) % self.mod_primary

        print(f"Group orbit equation validation:")
        print(f"  Exponent = (DR(136) + DR(296)) // 3 = ({dr_136} + {dr_296}) // 3 = {exponent}")
        print(f"  20^{exponent} % 37 = {orbit_check} (matches target 8: {orbit_check == self.target})")
        print("==================================================")


# ── Assertions ───────────────────────────────────────────────────────────────

X = 23572481523

# Boundary constraint
assert X % 37 == 8
assert X % 11 == 8
assert X % 407 == 8
assert 37 * 11 == 407

# Primitive roots
def is_primitive_root(g, p):
    return all(pow(g, (p-1)//q, p) != 1 for q in [2, 3])  # prime factors of 36: {2,3}

assert is_primitive_root(20, 37)
assert is_primitive_root(17, 37)

# Orbital indexing
assert pow(20, 3, 37) == 8
assert pow(17, 33, 37) == 23
assert (pow(20, 3, 37) * pow(17, 33, 37)) % 37 == 36  # ≡ -1 mod 37

# Cascade connections
assert (8 * 20) % 37 == 12   # sovereign target
assert (8 * 17) % 37 == 25   # sovereign anchor
assert 37 - 20 - 17 == 0
assert 37 - (20 + 8) == 9

# Boundary derivation
assert digital_root(136) == 1
assert digital_root(296) == 8
assert (digital_root(136) + digital_root(296)) // 3 == 3
assert pow(20, 3, 37) == 8


if __name__ == "__main__":
    framework = GroupFramework("23572481523")
    framework.run_tests()
    print("\nAll assertions passed.")
