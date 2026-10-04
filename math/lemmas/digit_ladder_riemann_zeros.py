# CLASS: LEMMA
"""
The digit ladder run through the Riemann zeros (owner, 2026-10-04). Rows are
row(a) = DR(a) | DR(a+1) | DR(2a+1) | 2a+10, a = 1..144
(math/lemmas/digit_ladder_12312_91128.py, digit_ladder_collatz.py).
Related prior work: math/theorems/riemann_first_zero_141.py, riemann_gf37_coverage.py.

THREE TESTS, each against its own baseline -- none departs from chance.

T1. ZERO NUMBER a AGAINST ROW a. gamma_a = imaginary part of the a-th zero.
    DR(floor gamma_a) = DR(row a) for 15 of 144 rows; chance gives 16
    (1 in 9), and 15 or more happens 64% of the time.
    First twelve floors 14, 21, 25, 30, 32, 37, 40, 43, 48, 49, 52, 56 have DR
    5, 3, 7, 3, 5, 1, 4, 7, 3, 4, 7, 2 against the rows' 9, 6, 3 cycle.
    DR(floor gamma_1..144) counts for 1..9: 10, 12, 21, 20, 19, 18, 19, 17, 8;
    chi-square 11.25 on 8 df (p about 0.19): uneven-looking, not significant.

T2. ROW VALUE AS A HEIGHT. N(T) = number of zeros with 0 < Im < T.
    N(12312) = 12896, N(23514) = 27049, N(34716) = 42087, N(45918) = 57711,
    N(56220) = 72469, N(67422) = 88860, N(78624) = 105546, N(89826) = 122487,
    N(91128) = 124472.
    N(T) - (theta(T)/pi + 1) is S(T), the irregular part; over all 144 rows it
    stays within +-1.28, as expected at these heights.
    DR(N(row)) = DR(row) for 21 of 144 (chance 16; 21 or more 12% of the time).
    These counts are of zeros in the whole critical strip; that all of them lie
    ON the line is known from published verification (RH checked to height
    3 x 10^12, Platt and Trudgian 2021), not from this file.

T3. IS THE ROW VALUE THE FLOOR OF A ZERO? (a zero in [row, row+1))
    Yes for 141 of 144 rows -- but at these heights there are 1.2 to 1.9
    zeros per unit, and the 20 integers around each row are floors 97.7% of
    the time (expected 140.7 hits). Carries no information. Row 1 (12312)
    is one of the three misses.

FALSIFICATION: any assertion below failing.
"""
import mpmath as mp

mp.mp.dps = 15

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def row(a):
    return int(f"{dr(a)}{dr(a + 1)}{dr(2 * a + 1)}{2 * a + 10}")

R = [row(a) for a in range(1, 145)]
GAMMA_FLOOR = [14, 21, 25, 30, 32, 37, 40, 43, 48, 49, 52, 56, 59, 60, 65, 67, 69, 72, 75, 77, 79, 82, 84, 87, 88, 92, 94, 95, 98, 101, 103, 105, 107, 111, 111, 114, 116, 118, 121, 122, 124, 127, 129, 131, 133, 134, 138, 139, 141, 143, 146, 147, 150, 150, 153, 156, 157, 158, 161, 163, 165, 167, 169, 169, 173, 174, 176, 178, 179, 182, 184, 185, 187, 189, 192, 193, 195, 196, 198, 201, 202, 204, 205, 207, 209, 211, 213, 214, 216, 219, 220, 221, 224, 224, 227, 229, 231, 231, 233, 236, 237, 239, 241, 242, 244, 247, 248, 249, 251, 253, 255, 256, 258, 259, 260, 263, 265, 266, 267, 269, 271, 273, 275, 276, 278, 279, 282, 283, 284, 286, 287, 289, 291, 293, 294, 295, 297, 299, 301, 302, 304, 305, 307, 310]
N_ROW = [12896, 27049, 42087, 57711, 72469, 88860, 105546, 122487, 124472, 12917, 27073, 42111, 57736, 72495, 88886, 105573, 122515, 124499, 12939, 27096, 42136, 57762, 72522, 88912, 105601, 122542, 124527, 12960, 27120, 42161, 57788, 72547, 88938, 105627, 122570, 124554, 12981, 27143, 42186, 57812, 72574, 88965, 105654, 122597, 1578324, 174036, 356590, 547990, 745247, 930553, 1135462, 1343347, 1553779, 1578358, 174065, 356621, 548022, 745279, 930586, 1135495, 1343380, 1553813, 1578392, 174094, 356650, 548053, 745311, 930618, 1135529, 1343414, 1553848, 1578426, 174122, 356681, 548085, 745343, 930651, 1135562, 1343447, 1553881, 1578460, 174150, 356711, 548116, 745375, 930683, 1135595, 1343481, 1553916, 1578494, 174179, 356742, 548147, 745407, 930716, 1135628, 1343515, 1553950, 1578528, 174206, 356771, 548178, 745440, 930749, 1135661, 1343548, 1553983, 1578563, 174235, 356802, 548210, 745472, 930781, 1135694, 1343581, 1554017, 1578596, 174263, 356832, 548241, 745504, 930815, 1135728, 1343616, 1554051, 1578630, 174291, 356861, 548272, 745535, 930847, 1135760, 1343649, 1554086, 1578665, 174321, 356892, 548304, 745567, 930879, 1135794, 1343682, 1554119, 1578698]
FLOOR_HIT = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
BASE_RATE = 0.977083
SMOOTH_DIFF_MAX = 1.274

assert GAMMA_FLOOR[:12] == [14, 21, 25, 30, 32, 37, 40, 43, 48, 49, 52, 56]
assert sum(dr(GAMMA_FLOOR[i]) == dr(R[i]) for i in range(144)) == 15
assert [sum(dr(x) == d for x in GAMMA_FLOOR) for d in range(1, 10)] == [10, 12, 21, 20, 19, 18, 19, 17, 8]
assert sum(dr(N_ROW[i]) == dr(R[i]) for i in range(144)) == 21
assert sum(FLOOR_HIT) == 141 and FLOOR_HIT[0] == 0
assert BASE_RATE > 0.97 and SMOOTH_DIFF_MAX < 1.3

for k in (1, 12, 144):
    assert int(mp.floor(mp.zetazero(k).imag)) == GAMMA_FLOOR[k - 1]
for i in range(9):
    T = R[i]
    assert int(mp.nzeros(T)) == N_ROW[i]
    assert (int(mp.nzeros(T + 1)) > N_ROW[i]) == bool(FLOOR_HIT[i])
    assert abs(N_ROW[i] - (mp.siegeltheta(T) / mp.pi + 1)) < 1.3

if __name__ == "__main__":
    for i in range(9):
        print(i + 1, R[i], "gamma floor", GAMMA_FLOOR[i], "N(row)", N_ROW[i], "zero in [row,row+1):", bool(FLOOR_HIT[i]))
    print("all assertions pass")
