# CLASS: THEOREM
"""
T432 — The carry map and the digital-root ring Z/(b-1)

Definitions. s_b(x) = base-b digit sum. dr_b(x) = the digital root (x mod b-1 with
0 -> b-1 for x > 0). CARRY MAP C_b(x, y) = number of carries when adding x + y in
base b.

(1) KUMMER'S IDENTITY (proved). C_b(x,y) = (s_b(x) + s_b(y) - s_b(x+y)) / (b-1).
    Each carry replaces a column sum b by digit 0 plus 1 carried: the digit sum
    drops by exactly b - 1. Hence s_b(x) + s_b(y) and s_b(x+y) lie in the same coset
    of (b-1)Z, and C_b counts the coset steps between them. This is WHY digital
    roots are additive mod b-1: carries are invisible modulo b-1.

(2) BOUNDARY CARRIES (proved). If D + d = b^k with D, d >= 1 and v = v_b(D) (trailing
    zeros), then v_b(d) = v and C_b(D, d) = k - v exactly: below position v both
    digits are 0 (no carry); at position v the digits sum to b; above, each column
    is (b-1) + carry = b, up to position k-1. Therefore
        s_b(D) + s_b(d) = 1 + (b-1)(k - v),
    and dr_b(D) + dr_b(d) = b (the supplied "absolute invariant", which needs
    D, d >= 1; it fails at d = 0). The carry DEPTH is k - v, unbounded in k.

(3) THE DIGITAL-ROOT RING R_b = Z/(b-1). With n = b - 1 = prod p_i^a_i:
      units          phi(n), group = prod (Z/p_i^a_i)^x  (cyclic iff n in {1,2,4,p^a,2p^a})
                     (the table lists these prime-power factors, e.g. n=35 prints
                      C4xC6 = (Z/5)^x (Z/7)^x, which is C2xC12 in invariant factors)
      idempotents    2^omega(n)      (one per CRT splitting)
      nilpotents     n / rad(n)
      zero divisors  n - phi(n) - 1  (nonzero non-units)
      2 invertible   iff n odd       iff b even  (the midpoint inverse b/2)
    CLASS: FIELD if n prime; LOCAL if n a prime power; MIXED if omega(n) >= 2.

(4) BASE 13: R_13 = Z/12 = Z/4 x Z/3, MIXED. Units {1,5,7,11} = C2 x C2 (not
    cyclic: every unit squares to 1). Idempotents {0,1,4,9}. Nilpotents {0,6}. Zero
    divisors {2,3,4,6,8,9,10}. 2 not invertible (13 odd). Digit ring Z/13 = F_13,
    primitive roots {2,6,7,11}.

(5) GF(37). Base 38 is the base whose digital-root ring IS GF(37) (38 - 1 = 37):
    in base 38 casting out 37s is dr, and the 137-map (x -> 26x) acts on digital
    roots. Base 37 (the prime itself) has R_37 = Z/36 = Z/4 x Z/9, MIXED, units
    C2 x C6 (order 12), 4 idempotents, 6 nilpotents; 2 not invertible (37 odd).
    Recorded as structure; no claim that base 38 is otherwise distinguished.

(6) BASE 37 (m = 36 = 2^2 * 3^2, MIXED). Seven proper islands (2),(3),(4),(6),
    (9),(12),(18); nilradical (6) = {0,6,12,18,24,30}; idempotents {0,1,9,28}
    (9 = (1,0), 28 = (0,1) under Z/4 x Z/9); 12 units, orders 1,2,3,6 (C2 x C6).
    CARRY COMPLEMENT f(r) = 1 - r: NO fixed point (36 even), so two parts with
    D + d = 37^k never share a digital root. f sends every island I onto 1 + I; a
    coset a + (d) is preserved iff 2a = 1 (mod d), possible only for odd d:
    a = 2 for (3), a = 5 for (9); no coset of an even-index island is preserved.
    DOUBLING x2: not a permutation (image = (2), 18 elements). Every orbit reaches
    the ideal (4) within 2 steps (the Z/4 component dies), and (4) = Z/9 via
    x -> x mod 9. On it x2 is EXACTLY base 10's picture: unit cycle
    (4 8 16 32 28 20) = (4 8 7 5 1 2) mod 9, island cycle (12 24) = (3 6), fixed 0
    (the 9 class). Base 37 doubling = transient collapse onto base 10's 3-6-9 ring.
    DIGITAL-ROOT RING = DISCRETE-LOG RING. 2 is primitive mod 37, so dlog_2:
    GF(37)* -> Z/36 is an isomorphism and the base-37 digital-root ring is the
    exponent ring of GF(37)*. The 137-map x -> 26x has dlog_2(26) = 12, so it is
    translation by 12 on Z/36 and its 12 orbits are the cosets of the island (12).
    PRIOR ART: the Z/12 orbit quotient is T138 (also T200, T285, T339, "dlog mod
    12"). New here only: that quotient is Z/36 modulo the ideal (12) of the
    base-37 digital-root ring. dr_37(137) = 29, a unit of order 6.

(7) BASE 38 (m = 37: the root ring IS GF(37), a FIELD). Dual of base 37: the
    digit ring Z/38 = Z/2 x Z/19 is mixed while the root ring is a field (base 37
    had digit field F_37 and mixed root ring Z/36). Each carry lowers the digit sum
    by 37, so s_38(x) = x (mod 37): the base-38 digital root is reduction in GF(37).
    No proper islands (ideals); nilradical {0}; idempotents {0,1}; x2 is a single
    36-cycle on units (2 primitive mod 37) plus fixed 0.
    CARRY COMPLEMENT f(r) = 1 - r: exactly one fixed point, r = 19 = b/2 = 2^-1,
    and 19 lies in CAS_EXT = {5,13,19}. For D + d = 38^k (D, d >= 1) the digital
    roots sum to 38 and coincide only when both are 19.
    THEOREM: f maps NO coset xH of any subgroup H of GF(37)* with |H| = d >= 2
    onto a coset. Proof: sum_{h in H} h = 0 (the d-th roots of unity), so
    1 - xH = yH would give d = 0 in GF(37), impossible for d <= 36. In particular
    no 137-orbit (coset of <26>) maps to an orbit. f fixes 19 and swaps the
    primitive sixth roots 11 <-> 27 (roots of r^2 - r + 1), both in NEG_H;
    f(NEG_H) = {2, 11, 27}.
    The 12 x 12 incidence #{x in O_i : 1 - x in O_j} is the order-12 cyclotomic
    number matrix of p = 37 (Gauss/Dickson) -- standard, recorded not claimed.

(8) BASE 39 (m = 38 = 2 * 19, square-free MIXED = F_2 x F_19). Two islands:
    (2) = the 19 evens, (19) = {0, 19}. Nilradical {0}. Idempotents {0,1,19,20}
    (19 = (1,0), 20 = (0,1)). Units: 18, cyclic C18 (primitive roots 3,13,15,...).
    Zero divisors: 19. CARRY COMPLEMENT: no fixed point (38 even); f(I) = 1 + I for
    both islands; preserved coset only 10 + (19) = {10, 29}, which f swaps
    (10 = 2^-1 in F_19). Two parts with D + d = 39^k never share a digital root.
    DOUBLING: image = the evens in ONE step; evens = F_19 (x -> x mod 19) and 2 is
    primitive mod 19, so x2 is a single 18-cycle on nonzero evens plus fixed 0.
    dr_39(137) = 23, a unit of order 9.
    FORCED, not information: the factor 19 is 38/2, the same 19 that is 2^-1 mod
    37 in base 38 (both come from 38 = 2 * 19).

(9) DOUBLING COLLAPSE (all bases, proved). Write m = b - 1 = 2^a * n, n odd. Under
    Z/m = Z/2^a x Z/n, x2 is nilpotent of index a on the first factor and a
    bijection on the second. Every orbit enters the ideal (2^a) = Z/n within a
    steps, and there x2 is EXACTLY doubling in the root ring of base n + 1.
    Base 37: a = 2, n = 9 -> base 10's 3-6-9 ring. Base 39: a = 1, n = 19 -> F_19.
    Even b (m odd): a = 0, x2 is a permutation (the midpoint-inverse case).

(10) BASE 40 (m = 39 = 3 * 13, square-free MIXED = F_3 x F_13; b EVEN). Islands
    (3) (13 elements) and (13) = {0,13,26}. Nilradical {0}. Idempotents
    {0,1,13,27} (13 = (1,0), 27 = (0,1)). Units 24 = C2 x C12 (max order 12, not
    cyclic). Zero divisors 14.
    CARRY COMPLEMENT: 39 odd, so f has exactly one fixed point, r = 20 = b/2 = 2^-1
    (20 = 2 mod 3, 7 mod 13: the preserved cosets 2 + (3) and 7 + (13) meet in 20).
    For D + d = 40^k the digital roots are equal only when both are 20.
    DOUBLING (a = 0, permutation): two unit 12-cycles; island (3) = F_13 carries one
    12-cycle (2 primitive mod 13); island (13) = F_3 carries (13 26); 0 fixed.
    CONTINGENT: dr_40(137) = 137 mod 39 = 20, the carry midpoint itself, because
    2 * 137 = 274 = 7 * 39 + 1 (273 = 3*7*13). MULT = 26 lies in the island (13).

(11) BASE 41 (m = 40 = 2^3 * 5, MIXED = Z/8 x Z/5). Six proper islands (2),(4),
    (5),(8),(10),(20). Nilradical (10) = {0,10,20,30}; 10 has nilpotency index 3
    (10^2 = 20, 10^3 = 0) -- the cube in 2^3, unlike the index-2 islands of
    prime-square moduli. Idempotents {0,1,16,25} (25 = (1,0), 16 = (0,1)).
    Units 16 = C2 x C2 x C4 (orders: one 1, seven 2, eight 4). Zero divisors 23.
    CARRY COMPLEMENT: no fixed point (40 even). Only preserved coset:
    3 + (5) = {3,8,...,38} (2*3 = 1 mod 5); no coset of an even-index island is
    preserved.
    DOUBLING: settles in exactly v2(40) = 3 steps onto (8) = {0,8,16,24,32} = Z/5
    (base 6's root ring F_5); there (8 16 32 24) = (3 1 2 4) mod 5, 2 primitive
    mod 5, and the idempotent 16 = (0,1) lies on the cycle.
    dr_41(137) = 17, dr_41(37) = 37: units of order 4. 26 is a non-unit, and
    10 (= 26^-1 in GF(37)) is NILPOTENT here.

(12) BASE 42 (m = 41 prime: root ring GF(41), a FIELD; b EVEN). No proper islands;
    nilradical {0}; idempotents {0,1}. CARRY COMPLEMENT: exactly one fixed point
    r = 21 = b/2 = 2^-1, a QR of order 20. As in base 38 (same proof: roots of
    unity sum to 0, d <= 40 < 41), f maps no coset of any subgroup of GF(41)* of
    order >= 2 onto a coset. |f(QR) & QR| = 9 = (p-5)/4, the classical cyclotomic
    number of order 2 for p = 41 = 1 mod 4 (recorded, not claimed).
    DOUBLING: permutation, but ord_41(2) = 20 (41 = 1 mod 8, so 2 is a QR): two
    20-cycles, the QRs and the QNRs, plus fixed 0. Smallest primitive root 6.
    No primitive sixth roots (41 = 2 mod 3): r^2 - r + 1 has no root, unlike base 38.
    CONTINGENT: 26 is a PRIMITIVE ROOT mod 41; 10 and 37 have order 5 (41 | 10^5 - 1
    = 9 * 41 * 271, the period-5 decimal of 1/41) and 37 = 10^-1 = 10^4 mod 41
    (10000 - 37 = 9963 = 41 * 3^5). dr_42(137) = 14, order 8, a QNR.

(13) BASE 43 (m = 42 = 2*3*7, square-free MIXED = F_2 x F_3 x F_7). Six proper
    islands (2),(3),(6),(7),(14),(21). Nilradical {0}. EIGHT idempotents
    {0,1,7,15,21,22,28,36}, one per CRT pattern in {0,1}^3. Units 12 = C2 x C6.
    Zero divisors 29. CARRY COMPLEMENT: no fixed point (42 even); preserved cosets
    2 + (3), 4 + (7), 11 + (21) = {11, 32} (f swaps 11 and 32).
    DOUBLING: one step (v2 = 1) onto (2) = Z/21 = base 22's root ring F_3 x F_7;
    there ord(2) = lcm(2, 3) = 6: cycles (2 4 8 16 32 22), (10 20 40 38 34 26) on
    the Z/21-units, (6 12 24), (18 36 30) on its F_7 island, (14 28) on its F_3
    island, and 0. The idempotent 22 = (0,1,1), identity of Z/21, is on a cycle.
    dr_43(137) = 11, a unit of order 6, lying in the preserved coset 11 + (21).

(14) 137 IS THE CARRY MIDPOINT MODULO EVERY DIVISOR OF 273 (contingent, proved).
    2 * 137 - 1 = 273 = 3 * 7 * 13, so 137 = 2^-1 mod d for every d | 273. In every
    base b with b - 1 | 273 -- b = 4, 8, 14, 22, 40, 92, 274 -- dr_b(137) is the
    unique fixed point b/2 of the carry complement; in any base whose root modulus
    has odd part dividing 273 (e.g. base 43, odd part 21), 137 lies in the
    preserved coset of that odd island. Base 40 (section 10) and base 43 are two
    instances of this one fact.

(15) BASE 44 (m = 43 prime: root ring GF(43), a FIELD; b EVEN). Carry complement
    fixes exactly r = 22 = 2^-1 (a QNR). f maps no coset of any subgroup of order
    >= 2 onto a coset (same roots-of-unity proof). |f(QR) & QR| = 10 = (p-3)/4,
    the classical count for p = 3 mod 4 (recorded). DOUBLING: permutation with
    ord_43(2) = 14 (2 is a QNR, 43 = 3 mod 8): three 14-cycles plus 0; smallest
    primitive root 3. Cube roots of unity {1, 6, 36}; primitive sixth roots {7, 37}
    (roots of r^2 - r + 1), swapped by f (1 - 7 = -6 = 37).
    CONTINGENT: 37 IS A PRIMITIVE SIXTH ROOT OF UNITY MOD 43 (37 = -6, 6^3 = 1;
    37^2 - 37 + 1 = 1333 = 43 * 31). 26 is a primitive root mod 43 (as mod 41).
    10 has order 21 (1/43 has decimal period 21). dr_44(137) = 8 = 2^3, order 14.

(16) BASE 45 (m = 44 = 2^2 * 11, MIXED = Z/4 x Z/11). Proper islands (2),(4),(11),
    (22). Nilradical (22) = {0, 22} (index 2). Idempotents {0,1,12,33} (33 = (1,0),
    12 = (0,1)). Units 20 = C2 x C10. Zero divisors 23. CARRY COMPLEMENT: no fixed
    point (44 even); only preserved coset 6 + (11) = {6,17,28,39} (6 = 2^-1 mod 11).
    DOUBLING: settles in v2(44) = 2 steps onto (4) = Z/11 = base 12's root ring;
    2 primitive mod 11: one 10-cycle (4 8 16 32 20 40 36 28 12 24) plus 0; the
    idempotent 12 = (0,1) lies on it.
    CONTINGENT: dr_45(137) = 5 and dr_45(37) = 37 are units of order 5 with
    37 = 137^3 (mod 44), since 5^3 = 125 = 2*44 + 37. 26 and 10 are non-units.
    Notation (supplied note, correct): dr is the least POSITIVE residue; it differs
    from Z -> Z/(b-1) exactly on positive multiples of b-1 (dr gives b-1, the
    residue gives 0). The complement identity dr(D) + dr(d) = b is an integer
    equation and needs that convention; this file's dr() follows it.

(17) BASE 46 (m = 45 = 3^2 * 5 = 1+2+...+9, MIXED = Z/9 x Z/5; b EVEN). Proper
    islands (3),(5),(9),(15). Nilradical (15) = {0,15,30}. Idempotents
    {0,1,10,36}: 10 = (1,0), 36 = (0,1). Units 24 = C6 x C4 (max order 12). Zero
    divisors 20. CARRY COMPLEMENT: exactly one fixed point r = 23 = b/2 = 2^-1, and
    EVERY island has a preserved coset (m odd): 2+(3), 3+(5), 5+(9), 8+(15), all
    meeting at 23. DOUBLING: a permutation (m odd) with ord(2) = lcm(6, 4) = 12.
    BASE 10 INSIDE BASE 46: the island (5) = {0,5,...,40} is a ring isomorphic to
    Z/9 (x -> x mod 9), i.e. base 10's root ring, and its identity is 10:
    10 = 1 (mod 9), 10 = 0 (mod 5), 10^2 = 10 (mod 45). The island (9) is Z/5.
    CONTINGENT: 10 is an IDEMPOTENT of Z/45; 26 is an involution (26^2 = 676 =
    15*45 + 1); dr_46(137) = 2 (137 = 3*45 + 2), order 12; 37 has order 4.

(18) THE MIDPOINT AND ITS EVEN FLANKS (supplied observation, proved). In base 10
    the roots 1..9 have centre 5 = b/2 = 2^-1 mod 9, the carry complement's unique
    fixed point; the complement pairs (4,6),(3,7),(2,8),(1,9) mirror around it, and
    4, 6 -- "highest even on the left, lowest even on the right" -- are the pair
    nearest the centre. For even b the flanks b/2 - 1, b/2 + 1 are EVEN iff
    b = 2 (mod 4). Base 46 = 2 (mod 4) repeats base 10: centre 23, flanks 22, 24.
    Base 40 = 0 (mod 4) does not: centre 20, flanks 19, 21 odd.

(19) BASE 47 (m = 46 = 2 * 23, square-free MIXED = F_2 x F_23). Islands (2), (23)
    = {0, 23}. Nilradical {0}. Idempotents {0,1,23,24}. Units 22, cyclic C22. Zero
    divisors 23. CARRY COMPLEMENT: no fixed point; only preserved coset
    12 + (23) = {12, 35} (12 = 2^-1 mod 23). DOUBLING: one step onto the evens
    = F_23; ord_23(2) = 11 (2 is a QR mod 23), so two 11-cycles plus 0.
    CONTINGENT: dr_47(137) = 45 = -1, an involution (138 = 3 * 46); 37 GENERATES
    the unit group (order 22). 26 and 10 are non-units.

(20) BASE 48 (m = 47 prime: root ring GF(47), a FIELD; b EVEN). Carry complement
    fixes exactly r = 24 = 2^-1. No coset of any subgroup of order >= 2 maps to a
    coset (roots-of-unity sum). |f(QR) & QR| = 11 = (p-3)/4 (p = 3 mod 4). No
    primitive sixth roots (47 = 2 mod 3). DOUBLING: permutation, ord_47(2) = 23
    (2 is a QR, 47 = 7 mod 8): two 23-cycles plus 0; primitive root 5.
    CONTINGENT: 137 = 43, 26 and 10 are all PRIMITIVE ROOTS mod 47; 37 has order 23
    (a QR). 47 = 10 (mod 37), in IC.

(21) BASE 49 (m = 48 = 2^4 * 3, MIXED = Z/16 x Z/3). Eight proper islands
    (2),(3),(4),(6),(8),(12),(16),(24). Nilradical (6), 8 elements; 6 has
    nilpotency index 4 (6^3 = 24, 6^4 = 0) -- the 2^4 factor. Idempotents
    {0,1,16,33} (33 = (1,0), 16 = (0,1)). Units 16 = C2 x C2 x C4. Zero divisors 31.
    CARRY COMPLEMENT: no fixed point; only preserved coset 2 + (3).
    DOUBLING: settles in exactly v2(48) = 4 steps -- the longest transient in
    bases 37..49 -- onto (16) = {0,16,32} = Z/3 = base 4's root ring, where it is
    the 2-cycle (16 32); the idempotent 16 lies on it.
    dr_49(137) = 41, an involution (41^2 = 1681 = 35*48 + 1); dr_49(37) = 37,
    order 4. 26 and 10 are non-units.

(22) BASE 50 (m = 49 = 7^2, LOCAL; b EVEN) -- base 10's picture at the prime 7.
    One island (7) = nilradical, 7 elements, and it squares to 0: every product of
    two island elements is 0, i.e. has digital root 49 (as 3, 6, 9 products all
    have root 9 in base 10). Idempotents {0,1}. Units 42, cyclic. Zero divisors 6.
    CARRY COMPLEMENT: fixed point 25 = b/2 = 2^-1, lying in the preserved coset
    4 + (7). DOUBLING: permutation; ord_49(2) = 21 (ord_7(2) = 3, 2^3 = 8 != 1 mod
    49): two 21-cycles on units; on the island (7 14 28), (21 42 35), and 0.
    CONTINGENT: 26 and 10 are PRIMITIVE ROOTS mod 49; 137 = 39 and 37 have order 21.

(23) BASE 51 (m = 50 = 2 * 5^2, MIXED = Z/2 x Z/25). Islands (2),(5),(10),(25).
    Nilradical (10) = {0,10,20,30,40}, index 2 (10^2 = 0). Idempotents {0,1,25,26}
    (25 = (1,0), 26 = (0,1)). Units 20, cyclic. Zero divisors 29.
    CARRY COMPLEMENT: no fixed point; preserved cosets 3 + (5) and 13 + (25)
    (13 = 2^-1 mod 25). DOUBLING: one step onto the evens = Z/25 = base 26's root
    ring; 2 primitive mod 25: a 20-cycle (2 4 8 16 ... 38 26) ending at the
    idempotent 26 = 2^20, and the island cycle (10 20 40 30), plus 0.
    CONTINGENT -- all three project constants take structural roles here:
      dr_51(137) = 37  (137 = 2*50 + 37), and 37 GENERATES the unit group (C20);
      26 is the IDEMPOTENT (0,1), the identity of the Z/25 factor, 26 = 2^20;
      10 is NILPOTENT (10^2 = 100 = 2*50).

(24) BASE 52 (m = 51 = 3 * 17, square-free MIXED = F_3 x F_17; b EVEN). Islands
    (3) = F_17 (17 elements), (17) = F_3. Nilradical {0}. Idempotents {0,1,18,34}.
    Units 32 = C2 x C16. Zero divisors 18. CARRY COMPLEMENT: fixed point
    26 = b/2 = 2^-1 -- MULT itself, FORCED by the choice b = 2 * 26 -- lying in the
    preserved cosets 2 + (3) and 9 + (17). DOUBLING: permutation, ord(2) =
    lcm(2, 8) = 8: cycles 1 x (0), 1 x length 2, 6 x length 8. ord(26) = 8 = ord(2)
    (forced: inverses). CONTINGENT: dr_52(137) = 35 is an involution
    (35^2 = 1225 = 24*51 + 1); 37 and 10 have the maximal order 16.

(25) BASE 53 (m = 52 = 2^2 * 13, MIXED = Z/4 x Z/13). Islands (2),(4),(13),(26).
    Nilradical (26) = {0, 26}. Idempotents {0,1,13,40} (13 = (1,0), 40 = (0,1)).
    Units 24 = C2 x C12. Zero divisors 27. CARRY COMPLEMENT: no fixed point; only
    preserved coset 7 + (13) (7 = 2^-1 mod 13). DOUBLING: settles in v2(52) = 2
    steps onto (4) = Z/13 = base 14's root ring; 2 primitive mod 13, one 12-cycle
    (4 8 16 32 12 24 48 44 36 20 40 28) through the idempotent 40, plus 0.
    CONTINGENT: MULT = 26 is NILPOTENT here, the only nonzero one (26^2 = 676 =
    13*52); dr_53(137) = 33 and 37 are units of order 12; 10 is a zero divisor.

(26) BASE 54 (m = 53 prime: root ring GF(53), a FIELD; b EVEN). Carry complement
    fixes exactly 27 = 2^-1 (= 3^3). No coset of any subgroup of order >= 2 maps to
    a coset. |f(QR) & QR| = 12 = (p-5)/4 (p = 1 mod 4). No primitive sixth roots
    (53 = 2 mod 3). DOUBLING: 2 is PRIMITIVE mod 53 (53 = 5 mod 8 makes 2 a QNR;
    2^4 = 16 != 1): a single 52-cycle on all nonzero residues plus 0 -- the same
    shape as base 38 (2 primitive mod 37).
    CONTINGENT: 137 = 31 and 26 are primitive roots; 37 has order 26; 10 has order
    13 (1/53 has decimal period 13). dlog_2: 26 -> 25, 37 -> 30, 10 -> 48.

(27) BASE 55 (m = 54 = 2 * 3^3, MIXED = Z/2 x Z/27). Islands (2),(3),(6),(9),(18),
    (27). Nilradical (6), 9 elements; 6 has nilpotency index 3 (6^2 = 36, 6^3 = 0)
    -- the 3^3 factor. Idempotents {0,1,27,28}. Units 18, cyclic. Zero divisors 35.
    CARRY COMPLEMENT: no fixed point; preserved cosets 2+(3), 5+(9), 14+(27).
    DOUBLING: one step onto the evens = Z/27 = base 28's (local) root ring:
    an 18-cycle on its units (2 primitive mod 27), a 6-cycle (6 12 24 48 42 30) on
    its island, the 2-cycle (18 36), and 0.
    CONTINGENT: 37 IS A CUBE ROOT OF UNITY mod 54 (37^2 = 19, 37*19 = 703 =
    13*54 + 1; cube roots {1, 19, 37}) -- the role 26 plays in GF(37).
    dr_55(137) = 29 GENERATES the unit group (order 18). 26 and 10 are zero divisors.

(28) BASE 56 (m = 55 = 5 * 11, square-free MIXED = F_5 x F_11; b EVEN). Islands
    (5) = F_11, (11) = F_5. Nilradical {0}. Idempotents {0,1,11,45} (11 = (1,0),
    45 = (0,1)). Units 40 = C4 x C10 (max order 20). Zero divisors 14.
    CARRY COMPLEMENT: fixed point 28 = b/2 = 2^-1, in the preserved cosets 3 + (5)
    and 6 + (11). DOUBLING: permutation, ord(2) = lcm(4, 10) = 20; cycles: (0), one
    4-cycle (on the F_5 island), one 10-cycle (on the F_11 island), two 20-cycles
    on units. CONTINGENT: dr_56(137) = 27 and 37 have the maximal order 20; 26 has
    order 5; 10 is a zero divisor.

(29) BASE 57 (m = 56 = 2^3 * 7, MIXED = Z/8 x Z/7). Islands (2),(4),(7),(8),(14),
    (28). Nilradical (14) = {0,14,28,42}; 14 has nilpotency index 3 (14^2 = 28,
    14^3 = 0). Idempotents {0,1,8,49} (49 = (1,0), 8 = (0,1)). Units 24 =
    C2 x C2 x C6. Zero divisors 31. CARRY COMPLEMENT: no fixed point; only
    preserved coset 4 + (7). DOUBLING: settles in v2(56) = 3 steps onto
    (8) = Z/7 = base 8's root ring F_7; there ord(2) = 3: cycles (8 16 32),
    (24 48 40), (0); the idempotent 8 lies on one.
    CONTINGENT: dr_57(137) = 25 is a PRIMITIVE CUBE ROOT OF UNITY mod 56
    (25^2 = 9, 25 * 9 = 225 = 4*56 + 1; cube roots {1, 9, 25}) -- the same role
    137 = 26 plays in GF(37), where it drives the 137-map. 37 has order 6; 26 and
    10 are zero divisors.

(30) BASE 58 (m = 57 = 3 * 19, square-free MIXED = F_3 x F_19; b EVEN). Islands
    (3) = F_19, (19) = F_3. Nilradical {0}. Idempotents {0,1,19,39}. Units 36 =
    C2 x C18. Zero divisors 20. CARRY COMPLEMENT: fixed point 29 = b/2 = 2^-1, in
    the preserved cosets 2 + (3) and 10 + (19). DOUBLING: permutation, ord(2) =
    lcm(2, 18) = 18 (2 primitive mod 19): cycles (0), one 2-cycle (F_3 island),
    three 18-cycles. Cube roots of unity {1, 7, 49}.
    CONTINGENT: 37 is an INVOLUTION mod 57 (37^2 = 1369 = 24*57 + 1);
    dr_58(137) = 23 and 10 have the maximal order 18; 26 has order 6.

(31) BASE 59 (m = 58 = 2 * 29, square-free MIXED = F_2 x F_29). Islands (2), (29).
    Nilradical {0}. Idempotents {0,1,29,30}. Units 28, cyclic. Zero divisors 29.
    CARRY COMPLEMENT: no fixed point; only preserved coset 15 + (29) = {15, 44}
    (15 = 2^-1 mod 29). DOUBLING: one step onto the evens = F_29; 2 is primitive
    mod 29, so a single 28-cycle plus 0.
    CONTINGENT: dr_59(137) = 21 and 37 both GENERATE the unit group (order 28);
    26 and 10 are non-units.

(32) BASE 60 (sexagesimal; m = 59 prime: root ring GF(59), a FIELD; b EVEN). The
    starkest digit/root contrast in the sweep: the digit ring Z/60 = Z/4 x Z/3 x
    Z/5 has 8 idempotents {0,1,16,21,25,36,40,45}; the root ring has only {0,1}.
    CARRY COMPLEMENT: fixes exactly 30 = b/2 = 2^-1. No coset of any subgroup of
    order >= 2 maps to a coset. |f(QR) & QR| = 14 = (p-3)/4. No primitive sixth
    roots (59 = 2 mod 3). DOUBLING: 2 is PRIMITIVE mod 59 (59 = 3 mod 8, 58 =
    2*29): one 58-cycle on nonzero residues plus 0.
    CONTINGENT: 37 and 10 are PRIMITIVE ROOTS mod 59 (so 1/59 has full decimal
    period 58); dr_60(137) = 19 and 26 are QRs of order 29.

(33) BASE 61 (m = 60 = 2^2 * 3 * 5, MIXED = Z/4 x Z/3 x Z/5) -- base 60's DIGIT
    ring is base 61's ROOT ring (forced: m = b - 1). Ten proper islands
    (2),(3),(4),(5),(6),(10),(12),(15),(20),(30). Nilradical {0, 30}. Eight
    idempotents {0,1,16,21,25,36,40,45}. Units 16 = C2 x C2 x C4. Zero divisors 43.
    CARRY COMPLEMENT: no fixed point; preserved cosets 2+(3), 3+(5), 8+(15).
    DOUBLING: settles in v2(60) = 2 steps onto (4) = Z/15 = base 16's root ring;
    there ord(2) = 4: cycles (4 8 16 32), (12 24 48 36), (28 56 52 44), (20 40), (0).
    Z/15's idempotents 1, 6, 10 appear as 16, 36, 40 -- each on a doubling cycle.
    dr_61(137) = 17 and 37 have order 4; 26 and 10 are zero divisors.

(34) BASE 62 (m = 61 prime: root ring GF(61), a FIELD; b EVEN). Carry complement
    fixes exactly 31 = 2^-1. No coset of any subgroup of order >= 2 maps to a
    coset. |f(QR) & QR| = 14 = (p-5)/4 (p = 1 mod 4). 61 = 1 mod 3: cube roots of
    unity {1, 13, 47}, primitive sixth roots {14, 48}, swapped by f. DOUBLING: 2 is
    PRIMITIVE mod 61: one 60-cycle plus 0.
    CONTINGENT: 26 and 10 are PRIMITIVE ROOTS mod 61 (1/61 has full decimal period
    60); 37 has order 20; dr_62(137) = 15, a QR of order 15.

(35) BASE 63 (m = 62 = 2 * 31, square-free MIXED = F_2 x F_31). Islands (2), (31).
    Nilradical {0}. Idempotents {0,1,31,32}. Units 30, cyclic. Zero divisors 31.
    CARRY COMPLEMENT: no fixed point; only preserved coset 16 + (31) = {16, 47}.
    DOUBLING: one step onto the evens = F_31, where ord(2) = 5 (31 = 2^5 - 1, a
    Mersenne prime): six 5-cycles plus 0.
    CONTINGENT: dr_63(137) = 13 GENERATES the unit group (order 30); 37 has
    order 6; 26 and 10 are non-units.

(36) BASE 64 (m = 63 = 3^2 * 7, MIXED = Z/9 x Z/7; b = 2^6 EVEN). Islands (3),(7),
    (9),(21). Nilradical (21) = {0,21,42}. Idempotents {0,1,28,36} (28 = (1,0),
    36 = (0,1)). Units 36 = C6 x C6. Zero divisors 26. CARRY COMPLEMENT: fixed
    point 32 = b/2 = 2^-1; every island has a preserved coset (m odd): 2+(3),
    4+(7), 5+(9), 11+(21).
    DOUBLING: ord(2) = 6 EXACTLY, FORCED: 2^6 = 64 = b = 1 (mod b - 1). (General:
    in base b = 2^k, ord_{b-1}(2) = k.)
    BASE 10 INSIDE BASE 64: the island (7) is Z/9 (x -> x mod 9) with identity 28;
    on it x2 runs (7 14 28 56 49 35) = (7 5 1 2 4 8) mod 9, base 10's doubling
    cycle, and (21 42) = (3 6). (Cf. base 46, where Z/9 sits as the island (5).)
    CONTINGENT: 37 is a CUBE ROOT OF UNITY mod 63 (37^2 = 46, 37*46 = 1702 =
    27*63 + 1); dr_64(137) = 11, 26 and 10 have order 6.

(37) BASE 65 (m = 64 = 2^6, LOCAL). Islands (2),(4),(8),(16),(32) -- a chain. The
    nilradical is (2), all 32 evens; 2 has nilpotency index 6. Idempotents {0,1}.
    Units 32 = C2 x C16. Zero divisors 31. CARRY COMPLEMENT: no fixed point and no
    preserved coset (every island has even index); f(r) = 1 - r maps the nilradical
    (evens) BIJECTIVELY onto the unit group (odds) -- the two halves of the ring.
    DOUBLING IS NILPOTENT on the whole ring: every orbit reaches 0 within
    v2(64) = 6 steps (a = 6, n = 1 in the doubling-collapse theorem: the surviving
    ideal is {0}). First base in the sweep with no nonzero doubling cycle.
    26 and 10 are nilpotent of index 6; dr_65(137) = 9 (order 8) and 37 (order 16)
    are units.

(38) BASE 66 (m = 65 = 5 * 13, square-free MIXED = F_5 x F_13; b EVEN). Islands
    (5) = F_13, (13) = F_5. Nilradical {0}. Idempotents {0,1,26,40} (26 = (1,0),
    40 = (0,1)). Units 48 = C4 x C12. Zero divisors 16. CARRY COMPLEMENT: fixed
    point 33 = b/2 = 2^-1, in the preserved cosets 3 + (5) and 7 + (13).
    DOUBLING: permutation, ord(2) = lcm(4, 12) = 12: (0), one 4-cycle, five
    12-cycles.
    CONTINGENT: MULT = 26 is the IDEMPOTENT (1,0) -- the identity of the island
    (13) = F_5 -- and lies on that island's doubling cycle (13 26 52 39). (Second
    base where 26 is idempotent; cf. base 51.) dr_66(137) = 7 and 37 have the
    maximal order 12; 10 is a non-unit.

(39) BASE 67 (m = 66 = 2 * 3 * 11, square-free MIXED = F_2 x F_3 x F_11). Six islands
    (2),(3),(6),(11),(22),(33). Nilradical {0}. EIGHT idempotents
    {0,1,12,22,33,34,45,55}. Units 20 = C2 x C10. Zero divisors 45. CARRY
    COMPLEMENT: no fixed point; preserved cosets 2+(3), 6+(11), 17+(33).
    DOUBLING: one step onto the evens = Z/33 = base 34's root ring F_3 x F_11,
    where ord(2) = lcm(2, 10) = 10: three 10-cycles, (22 44), and 0.
    dr_67(137) = 5 has order 10; 37 has order 5; 26 and 10 are zero divisors.

(40) WHEN IS 26 IDEMPOTENT (forced, all bases). 26 is idempotent mod m iff
    m | 26^2 - 26 = 650 = 2 * 5^2 * 13. The moduli are 2,5,10,13,25,26,50,65,130,
    ...; in the sweep that is exactly base 51 (m = 50) and base 66 (m = 65). The
    double appearance is a divisibility fact about 650, not a coincidence.
    (Supplied-audit corrections, 2026-09-28: base 51 has NO carry fixed point
    (m = 50 even; 2*25 = 50 = 0); units of maximal order 12 in Z/65 = C4 x C12
    number 24, not 16 (16 with ord b = 12, plus 8 with ord b in {3,6}, ord a = 4).)

(41) BASE 68 (m = 67 prime: root ring GF(67), a FIELD; b EVEN). Carry complement
    fixes exactly 34 = (m+1)/2 = b/2 = 2^-1 (standardized rule: f(r) = 1 - r has
    a fixed point iff m is odd, and then it is (m+1)/2). No coset of any subgroup
    of order >= 2 maps to a coset. |f(QR) & QR| = 16 = (p-3)/4. 67 = 1 mod 3: cube
    roots {1, 29, 37}, primitive sixth roots {30, 38}, swapped by f. DOUBLING: 2 is
    PRIMITIVE mod 67 (smallest primitive root): one 66-cycle plus 0.
    CONTINGENT: 37 IS A PRIMITIVE CUBE ROOT OF UNITY MOD 67 (37^2 = 29, 37*29 =
    1073 = 16*67 + 1) -- as mod 54 and mod 63 (bases 55, 64). 26 and 10 have order
    33; dr_68(137) = 3 has order 22.

(42) BASE 69 (m = 68 = 2^2 * 17, MIXED = Z/4 x Z/17). Islands (2),(4),(17),(34).
    Nilradical (34) = {0, 34}. Idempotents {0,1,17,52} (17 = (1,0), 52 = (0,1)).
    Units 32 = C2 x C16. Zero divisors 35. CARRY COMPLEMENT: no fixed point
    (m even); only preserved coset 9 + (17). DOUBLING: settles in v2(68) = 2 steps
    onto (4) = Z/17 = base 18's root ring F_17, where ord(2) = 8: two 8-cycles
    (4 8 16 32 64 60 52 36), (12 24 48 28 56 44 20 40), and 0; the idempotent 52
    lies on the first.
    CONTINGENT: dr_69(137) = 1 -- 137 is the IDENTITY of base 69's root ring
    (137 = 2*68 + 1; 136 = 2^3 * 17). 37 has maximal order 16; 26 and 10 are zero
    divisors.

(43) BASE 70 (m = 69 = 3 * 23, square-free MIXED = F_3 x F_23; b EVEN). Islands
    (3) = F_23, (23) = F_3. Nilradical {0}. Idempotents {0,1,24,46} (46 = (1,0),
    24 = (0,1)). Units 44 = C2 x C22. Zero divisors 24. CARRY COMPLEMENT: fixed
    point 35 = (m+1)/2 = b/2, in the preserved cosets 2 + (3) and 12 + (23).
    DOUBLING: permutation, ord(2) = lcm(2, 11) = 22 (ord_23(2) = 11): cycles (0),
    one 2-cycle (F_3 island), two 11-cycles (F_23 island), two 22-cycles (units).
    CONTINGENT: dr_70(137) = 68 = -1, an involution (138 = 2 * 69); 26, 37 and 10
    all have the maximal order 22.

(44) BASE 71 (m = 70 = 2 * 5 * 7, square-free MIXED = F_2 x F_5 x F_7). Six islands
    (2),(5),(7),(10),(14),(35). Nilradical {0}. Eight idempotents
    {0,1,15,21,35,36,50,56}. Units 24 = C4 x C6 (8 of maximal order 12). Zero
    divisors 45. CARRY COMPLEMENT: no fixed point; preserved cosets 3+(5), 4+(7),
    18+(35). DOUBLING: one step onto the evens = Z/35 = base 36's root ring
    F_5 x F_7, ord(2) = lcm(4, 3) = 12: cycles 1 x (0), two 3-cycles (F_7 island),
    one 4-cycle (F_5 island), two 12-cycles (units of Z/35).
    dr_71(137) = 67 and 37 have maximal order 12 (base rate 8/24 = 1/3); 26 and 10
    are zero divisors.
    BASE RATE for "maximal order" claims (Lane 1): mod 69, 30 of 44 units (68%)
    have maximal order 22, so base 70's "26, 37, 10 all maximal" has chance about
    0.68^3 = 31% -- generic, not a signal (as with 24/48 mod 65).

(45) BASE 72 (m = 71 prime: root ring GF(71), a FIELD; b EVEN). Carry complement
    fixes exactly 36 = (m+1)/2. No coset of any subgroup of order >= 2 maps to a
    coset. |f(QR) & QR| = 17 = (p-3)/4. No primitive sixth roots (71 = 2 mod 3).
    DOUBLING: 71 = 7 mod 8 makes 2 a QR; ord_71(2) = 35: two 35-cycles (the QRs and
    the QNRs) plus 0. Smallest primitive root 7.
    dr_72(137) = 66 = -5 has order 10 (QNR); 26 order 14 (QNR); 37 order 7 (QR);
    10 order 35 (QR; 1/71 has decimal period 35).

(46) CAPSTONE: THE PARITY DICHOTOMY (consolidates (9) and (41); proved).
    With m = b - 1 = 2^a * n, n odd:
      b EVEN (a = 0): doubling is a PERMUTATION of Z/m, and f(r) = 1 - r has
        exactly one fixed point, r* = (m+1)/2 = b/2 -- forced for every even base.
      b ODD  (a >= 1): f has NO fixed point, and doubling reaches the ideal
        (2^a) = Z/n in EXACTLY a = v2(m) steps (not always one), then acts as
        doubling on Z/n, the root ring of base n + 1.
    Odd bases 37..71, (b: a, n): 37:2,9  39:1,19  41:3,5  43:1,21  45:2,11
    47:1,23  49:4,3  51:1,25  53:2,13  55:1,27  57:3,7  59:1,29  61:2,15
    63:1,31  65:6,1 (all of Z/64 collapses to {0})  67:1,33  69:2,17  71:1,35.
    (A supplied draft said "collapses onto the evens in one step" for every odd b;
    that holds only when v2(b-1) = 1. It also listed base 63 as even -- 63 is odd,
    m = 62 even.) The real variation lives one level down: the cycle signature
    (ord of 2 in each field factor) and where the project's numbers land in it.

(47) BASE 73 (m = 72 = 2^3 * 3^2, MIXED = Z/8 x Z/9). Ten proper islands
    (2),(3),(4),(6),(8),(9),(12),(18),(24),(36). Nilradical (6), 12 elements, index
    3 (6^3 = 216 = 3*72). Idempotents {0,1,9,64} (9 = (1,0), 64 = (0,1)). Units 24
    = C2 x C2 x C6. Zero divisors 47. CARRY COMPLEMENT: no fixed point (b odd);
    preserved cosets 2+(3), 5+(9).
    DOUBLING: settles in v2(72) = 3 steps onto (8) = Z/9 = BASE 10'S ROOT RING
    (identity 64): unit cycle (8 16 32 64 56 40) = (8 7 5 1 2 4) mod 9 and
    nilpotent cycle (24 48) = (6 3) -- base 10's doubling picture after a 3-step
    transient. (Third embedding of base 10's ring: bases 46, 64, 73.)
    CONTINGENT: 37 is an INVOLUTION mod 72 (37^2 = 1369 = 19*72 + 1);
    dr_73(137) = 65 has order 6; 26 and 10 are zero divisors.

(48) BASE 74 (m = 73 prime: root ring GF(73), a FIELD; b = 2 * 37 EVEN). The carry
    complement's unique fixed point is (m+1)/2 = 37 -- the project prime is the
    carry MIDPOINT of base 74 (FORCED by b = 2 * 37; 37 = 2^-1 mod 73). No coset of
    any subgroup of order >= 2 maps to a coset. |f(QR) & QR| = 17 = (p-5)/4.
    73 = 1 mod 3: cube roots {1, 8, 64} = {1, 2^3, 2^6}, primitive sixth roots
    {9, 65}, swapped by f. DOUBLING: ord_73(2) = 9 (2^9 - 1 = 511 = 7 * 73): eight
    9-cycles plus 0; smallest primitive root 5. 37 = 2^-1 has order 9 too.
    CONTINGENT: dr_74(137) = 64 = 2^6 is a PRIMITIVE CUBE ROOT OF UNITY mod 73 --
    the role 137 = 26 plays in GF(37) (the 137-map) and 137 = 25 plays mod 56
    (base 57). 26 is a PRIMITIVE ROOT mod 73; 10 has order 8 (1/73 has decimal
    period 8).

(49) BASE 75 (m = 74 = 2 * 37, square-free MIXED = F_2 x GF(37)) -- the root ring
    CONTAINS GF(37). Islands (2) (the 37 evens, = GF(37) via x -> x mod 37, identity
    38) and (37) = {0, 37}. Nilradical {0}. Idempotents {0,1,37,38}. Units 36,
    cyclic. CARRY COMPLEMENT: no fixed point (b odd); only preserved coset
    19 + (37) = {19, 56} (19 = 2^-1 in GF(37), the base-38 midpoint). DOUBLING: one
    step onto the evens = GF(37), then ONE 36-cycle -- GF(37)'s own generator walk
    (2 primitive mod 37).
    FORCED BY 74 = 2 * 37 (not contingent): 37 is the IDEMPOTENT (1,0); 26 and 10
    lie in the GF(37) island as (0,26), (0,10); dr_75(137) = 63 = (1, 26), so
    multiplying by 137 acts on the GF(37) island as the 137-map x -> 26x.

(50) THE "~" OPERATION (supplied digit table, decoded and proved). Every row
    a ~ b of the supplied table equals rev((a + b) mod 99), e.g. 12 ~ 11 = rev(23) =
    32, 56 ~ 55 = rev(111 mod 99 = 12) = 21, 99 ~ 19 = rev(118 mod 99 = 19) = 91.
    REVERSAL IS MULTIPLICATION BY 10 MOD 99: n = 10x + y gives 10n = 100x + 10y =
    x + 10y = rev(n) (mod 99), and 10^2 = 1 (mod 99), so reversal is an
    involution. Hence a ~ b = 10(a + b) in Z/99 -- the ROOT RING OF BASE 100
    (m = 99 = 9 * 11). Mod 9, 10 = 1: reversal leaves digital roots unchanged,
    which is why each row's reduction equals dr(a + b). Mod 11, 10 = -1: reversal
    negates the alternating digit sum. The block totals (115 -> 7, 159 -> 6,
    871 -> 7, 429 -> 6, 241 -> 7) are running digital-root sums of the row
    results, chained block to block.

(51) BASE 76 (m = 75 = 3 * 5^2, MIXED = Z/3 x Z/25; b EVEN). Islands (3),(5),(15),
    (25). Nilradical (15) = {0,15,30,45,60}. Idempotents {0,1,25,51} (25 = (1,0),
    51 = (0,1)). Units 40 = C2 x C20. Zero divisors 34. CARRY COMPLEMENT: fixed
    point 38 = (m+1)/2; every island has a preserved coset (m odd): 2+(3), 3+(5),
    8+(15), 13+(25). DOUBLING: permutation, ord(2) = lcm(2, 20) = 20: cycles (0),
    one 2-cycle, three 4-cycles, three 20-cycles.
    FORCED BY SMALL DIVISIBILITIES: 26 = (2, 1) = (-1, 1) is an INVOLUTION (26 - 1 =
    25; cf. bases 51, 66 where 25 | 26 - 1 made 26 idempotent); 137 = 62 and 37
    share the Z/25 coordinate 12 because 137 - 37 = 100 = 4 * 25 -- both of maximal
    order 20. 10 is a zero divisor.

(52) ABBA / DDDD PALINDROME PAIRS (supplied list, forced facts). For the pairs
    (1221,1111), (2332,2222), ..., (9119,9999):
      abba = 11 (91a + 10b): every even-length palindrome is divisible by 11;
      dddd = 1111 d and 1111 = 30*37 + 1, so dddd = d (mod 37);
      abba = 2a - b (mod 37) (1001 = 2, 110 = -1): only 1221 = 3 * 11 * 37 is
        divisible by 37 (the only pair with b = 2a);
      abba - dddd = 110 (b - a) = +-110, except 9119 - 9999 = -880 (b wraps to 1);
      abba + baab = 1111 (a + b) = a + b (mod 37).
    The inner digit b = a +- 1 (signs + + - + - - - + +) follows no rule found here;
    recorded as the supplier's choice.

(53) THE TWO SUPPLIED RULES ARE ONE RING (supplied: "the pattern is the rules").
    Read a 4-digit number as two base-100 digits; the root ring is Z/99 =
    Z/9 x Z/11 (base 100's digital-root ring). Then
      REVERSE  h -> rev(h)            is  x10  = (1, -1)  in Z/9 x Z/11;
      ~        a ~ b = rev(a+b mod 99) is  10(a+b);
      MIRROR   h -> h|rev(h) = abba   is  x11 = 1 + reversal = (2, 0),
    since abba = 100 h + rev(h) = h + 10 h = 11 h (mod 99). Every palindrome of the
    supplied list is h|rev(h) for a half h that is an OPERAND of the ~ table
    (12,11,23,22,32,33,45,44,54,55,65,66,76,77,89,88,91,99). Reading the
    coordinates: reversal keeps the digital root (mod 9: x1) and negates the mod-11
    part; mirroring DOUBLES the digital root and KILLS the mod-11 part -- which is
    why every palindrome is divisible by 11 and dr(abba) = dr(2h). Both rules are
    multiplications by units/zero-divisors of the base-100 root ring: 10 is a unit
    of order 2, 11 is a zero divisor (11 * 9 = 99 = 0).

(54) L-CUPS (supplied definition, 2026-09-28). A HALF L-cup is a 2 x 2 digit block
    with three cells equal to d and one cell d + 1 ("3 x 1 plus 1"), e.g.
        12      the rows are 2-digit numbers; the odd rows of the supplied ~ table
        11      (12/11, 23/22, 34/33, ...) are half L-cups.
    A FULL L-cup mirrors each row to an odd palindrome: 12 -> 121, 11 -> 111.
    FORCED FACTS (d = 1..8, so d + 1 is a digit):
      * Every full-cup row is = 0, 10 or 27 (mod 37), independent of d:
            ddd = 111 d = 0          (111 = 3 * 37),
            d(d+1)d = 111 d + 10 = 10        (10 in IC = {1,10,26}),
            (d+1)d(d+1) = 111 d + 101 = 27   (27 in NEG_H = {11,27,36}).
      * Half-cup rows are 11 d + {0, 1, 10}: mod 11 the raised cell is exactly
        0, +1 or -1 -- in base 100's root ring Z/99 the half cup is the repdigit
        11 d shifted by 0, 1 or the reversal-image 10.
      * Digital roots: ddd -> 3d, d(d+1)d -> 3d + 1, (d+1)d(d+1) -> 3d + 2.
      * The model cup 12/11 -> 121/111: 121 = 11^2, 111 = 3 * 37 = 0 (mod 37),
        121 = 10 (mod 37).
    EDGE d = 9: d + 1 is not a digit; the supplied table wraps it to 1 (91/99,
    99/19). Then 919 = 31 and 191 = 6 (mod 37), outside {0, 10, 27}: the mod-37
    rule holds exactly for d = 1..8.

(55) BASE 77 (m = 76 = 2^2 * 19, MIXED = Z/4 x Z/19). Islands (2),(4),(19),(38).
    Nilradical (38) = {0, 38}. Idempotents {0,1,20,57} (57 = (1,0), 20 = (0,1)).
    Units 36 = C2 x C18. Zero divisors 39. CARRY COMPLEMENT: no fixed point (b odd);
    only preserved coset 10 + (19). DOUBLING: settles in v2(76) = 2 steps onto
    (4) = Z/19 = base 20's root ring F_19; 2 primitive mod 19: one 18-cycle plus 0.
    CONTINGENT: 37 = (1, -1) is an INVOLUTION mod 76 (37^2 = 1369 = 18*76 + 1);
    dr_77(137) = 61 has order 9; 26 and 10 are non-units.

(56) SPIN COMBINATORICS OF L-CUPS AND MICHAEL L's (supplied pictures, modelled).
    Cells of the 2 x 2 block clockwise 0 = TL, 1 = TR, 2 = BR, 3 = BL; a spin is
    i -> i + 1 (mod 4) (the group C4).
      L-CUP: one odd cell ("3 x 1 plus 1"): 4 placements, ONE spin-orbit; no
        chirality. Colour rotation = which colour is the odd one (d vs d + 1).
      MICHAEL L: two distinct marks (black, 0) and two blanks: 4 * 3 = 12
        placements. The offset k = pos(0) - pos(black) (mod 4) is spin-invariant,
        so there are EXACTLY 3 spin-orbits of size 4: k = 1 (adjacent clockwise),
        k = 2 (diagonal), k = 3 (adjacent counter-clockwise). The four supplied
        MLs have k = 3, 1, 2, 2 -- all three orbits appear.
      With reflections (D4) or with the colour swap black <-> 0, k = 1 and k = 3
        merge: 2 orbits (adjacent, diagonal).
    So both shapes "spin the same way" (free C4-orbits of size 4); the difference is
    CHIRALITY: an ML's adjacent types come in a clockwise / counter-clockwise pair
    that only a flip or colour swap identifies; an L-cup has one mark and none.

(57) BASE 78 (m = 77 = 7 * 11, square-free MIXED = F_7 x F_11; b EVEN). Islands
    (7) = F_11, (11) = F_7. Nilradical {0}. Idempotents {0,1,22,56}. Units 60 =
    C6 x C10 (max order 30). Zero divisors 16. CARRY COMPLEMENT: fixed point
    39 = (m+1)/2, in the preserved cosets 4 + (7) and 6 + (11). DOUBLING:
    permutation, ord(2) = lcm(3, 10) = 30: (0), two 3-cycles (F_7 island), one
    10-cycle (F_11 island), two 30-cycles.
    CONTINGENT: 137 = (4, 5) and 26 = (5, 4) in F_7 x F_11 -- swapped coordinates
    (137 mod 7 = 4 = 26 mod 11, 137 mod 11 = 5 = 26 mod 7), a residue coincidence.
    ord(26) = 30 (maximal), ord(137) = ord(37) = 15, ord(10) = 6.

(58) DIRECTION / DISTANCE STATES (supplied "number-flow machine" test, run).
    Over all 81 ordered digit pairs (a, b), the state (U/D/E, |b - a|) takes 17
    values (E0, U1..U8, D1..D8); reversal (a,b) -> (b,a) flips U <-> D and keeps
    the distance; its orbits are 45 (9 fixed E-pairs, 36 swapped pairs).
    DIRECTION IS NOT A ROOT-RING INVARIANT: in Z/9, D4 = U5 (-4 = 5); the step
    that survives reduction is (b - a) mod 9. CLOSURE is then exact: repeating a
    step s returns after 9/gcd(s, 9) steps -- 9 for s coprime to 3 (e.g. 1-5-9,
    U4, visits every root), 3 for s = 3, 6 (the 3-6-9 island and its cosets).
    The parity grid 123/456/789 -> checkerboard is FORCED (n = 3r + c + 1 = r + c + 1
    mod 2, as 3 is odd), hence invariant under every rotation and reflection.

(59) BASE 79 (m = 78 = 2 * 3 * 13, square-free MIXED = F_2 x F_3 x F_13). Six islands
    (2),(3),(6),(13),(26),(39). Nilradical {0}. Eight idempotents
    {0,1,13,27,39,40,52,66}. Units 24 = C2 x C12. Zero divisors 53. CARRY
    COMPLEMENT: no fixed point (b odd); preserved cosets 2+(3), 7+(13), 20+(39).
    DOUBLING: one step onto the evens = Z/39 = base 40's root ring F_3 x F_13,
    ord(2) = lcm(2, 12) = 12: (0), one 2-cycle, three 12-cycles.
    dr_79(137) = 59 and 37 have maximal order 12; 26 = (0,2,0) and 10 = (0,1,10)
    are zero divisors.

(60) SUPPLIED "SHARPENED ML SYSTEM" AUDIT, checked. CORRECT: rotation R and
    reversal X of an n-string generate the dihedral group of order 2n -- all 6
    permutations for n = 3 (S_3), only 18 of 9! for n = 9; 32 distinct (direction,
    |delta|, parity-pattern) states over the 81 pairs. WRONG: "the units wrap
    n9 -> (n+1)0 always coincides with a dr-wrap 9 -> 1". Under +1 the digital root
    ALWAYS rises by exactly one (cyclically); it wraps 9 -> 1 only after multiples
    of 9, while the units digit wraps after n = 9 (mod 10). They coincide only for
    n = 9 (mod 90): 12 of the 100 units-wraps below 1000 (9, 99, 189, 279, ...);
    e.g. 19 -> 20 takes dr 1 -> 2. A units wrap is a CARRY, and carries are
    invisible mod 9 (section 1): zero marks the mod-10 carry, not the mod-9 wrap.
    NOT CHECKED: the supplied 9 x 9 field table A(r,c) = dr(r + c - 1) (table not
    provided); the claim is internally consistent (it would be Z/9's Cayley table).

(61) BASE 80 (m = 79 prime: root ring GF(79), a FIELD; b EVEN). Carry complement
    fixes exactly 40 = (m+1)/2. No coset of any subgroup of order >= 2 maps to a
    coset. |f(QR) & QR| = 19 = (p-3)/4. 79 = 1 mod 3: cube roots {1, 23, 55},
    primitive sixth roots {24, 56}, swapped by f. DOUBLING: 79 = 7 mod 8 makes 2 a
    QR; ord_79(2) = 39: two 39-cycles plus 0; smallest primitive root 3.
    CONTINGENT: 37 is a PRIMITIVE ROOT mod 79; 26 has order 39; 10 has order 13
    (1/79 has decimal period 13); dr_80(137) = 58 has order 26.

(62) THREE-DIGIT BOUNDARY TEST (supplied, all 729 triples reproduced). For
    (a,b,c) in {1..9}^3 with dL = b - a, dR = c - b: the boundary pair determines
    the triple up to the translation b; 217 pairs are realizable, 48 fix b
    uniquely; centre-multiplicity census 48,42,36,30,24,18,12,6,1 (weighted 729).
    FORCED: a + b + c = 3b + dR - dL, so the total is dR - dL (mod 3) and
    3(b mod 3) + dR - dL (mod 9): the interior enters only through the coefficient
    3, i.e. as one ternary phase b mod 3. With (direction, |delta|, parities) on both
    boundaries: 386 realizable state pairs, 168 fix b. Counterexample to "boundary
    fixes the mod-9 state": (1,1,1), (3,3,3), (5,5,5) share dL = dR = 0 with totals
    3, 0, 6 (mod 9).

(63) BASE 81 = 3^4 (m = 80 = 2^4 * 5, MIXED = Z/16 x Z/5). Eight proper islands
    (2),(4),(5),(8),(10),(16),(20),(40). Nilradical (10), 8 elements; 10 has
    nilpotency index 4 (10^3 = 40, 10^4 = 0). Idempotents {0,1,16,65} (65 = (1,0),
    16 = (0,1)). Units 32 = C2 x C4 x C4 of EXPONENT 4 (every unit has order 1, 2
    or 4) -- the smallest unit exponent in the sweep. Zero divisors 47.
    CARRY COMPLEMENT: no fixed point (b odd); only preserved coset 3 + (5).
    DOUBLING: settles in v2(80) = 4 steps onto (16) = Z/5 = base 6's root ring F_5:
    the cycle (16 32 64 48) = (1 2 4 3) mod 5 starts at the idempotent 16.
    dr_81(137) = 57 and 37 have order 4; 10 is NILPOTENT (index 4); 26 is a zero
    divisor.
    (Ledger notes, 2026-09-28: a supplied ledger again stated "16 of 48 units of
    order 12" mod 65 -- the count is 24 (section 40). Its refinement is right: the
    nonzero part of an island is a multiplicative group (identity the idempotent,
    e.g. 40 for (5) mod 65), but the island itself is not a field.)

(64) BASE 82 (m = 81 = 3^4, LOCAL). Islands (3) (27 elements = nilradical, index 4),
    (9), (27) -- a chain. Idempotents {0,1}. Units 54, cyclic; 2 is PRIMITIVE mod 81
    (primitive mod 9 and 2^6 = 64 != 1 mod 27). CARRY COMPLEMENT: fixed point 41 =
    (m+1)/2 (b even), in the preserved cosets 2+(3), 5+(9), 14+(27). DOUBLING:
    exactly ONE cycle per 3-adic layer: lengths 54 (units), 18 (3 x units mod 27),
    6 (9 x units mod 9), 2 (27, 54), 1 (0).
    REFINES BASE 10: 9 | 81, so dr_82(n) mod 9 = n mod 9 -- the base-82 root
    determines the base-10 root (reduction Z/81 -> Z/9).
    FORCED: 37 = 1 + 4*9 and 10 = 1 + 9 lie in the kernel 1 + 9Z/81 of that
    reduction, a group of order 9, so both have order 9. CONTINGENT: dr_82(137) =
    56 is a PRIMITIVE ROOT (order 54); 26 has order 6. 405 = 5 * 81 = 0 here.

(65) THE 405 EVALUATION (supplied, all reproduced; all forced). The 3 x 3 all-9 field
    gives E_digit = 9*9 = 81 and E_cycle = 9*45 = 405; ratio 5 = mean of 1..9; both
    and their difference 324 = 4*81 have v3 = 4 (v3(9N) = v3(36N) = 2 + v3(N)).
    The 9 x 9 mod-9 Cayley table also totals 9*45 = 405 (each row a permutation of
    1..9): same total, same reason -- nine complete 1..9 cycles. Moments
    M_r = 9 sum_{j<=9} j^r: 405, 2565, 18225, 137997, 1087425, 8805645, 72723825,
    609581997; M_r = 0 (mod 81) for r odd (pair j with 9 - j), 54 for r even
    (sum j^{2k} = 6 mod 9). Centred sums: odd ones 0; 540, 6372, 88020; variance
    20/3. 405 = 35 = -2 (mod 37) is PRIMITIVE (2 primitive, -2 = 2^19, gcd(19,36) =
    1); 405 = 10 (mod 79), order 13, cycle 1,10,21,52,46,65,18,22,62,67,38,64,8.

(66) THE CARRY COMPLEMENT IS A REFLECTION (every even base; proved). For m odd and
    r* = (m+1)/2 (2r* = 1): f(r) - r* = 1 - r - r* = -(r - r*) (mod m). So f is the
    point reflection about the midpoint, and for every prime power p^a || m it
    preserves the CAPPED valuation min(v_p(r - r*), a) -- the valuation of the
    displacement in Z/p^a. Hence the shells {r : v_p(r - r*) = k} are f-invariant
    in every even base, not only in local rings. (Capping is needed: mod 45,
    27 and -27 = 18 have v_3 = 3, 2 but both reach the cap v_3(45) = 2.) Checked
    for every even b <= 200. In base 82 (supplied analysis, reproduced) the shells
    about 41 have sizes 54, 18, 6, 2, 1 -- equal to the doubling cycle lengths,
    since both count {x : v_3(x) = k}, centred at 41 and at 0 -- and f is 1 fixed
    point + 27 + 9 + 3 + 1 = 40 transpositions.

(67) BASE 83 (m = 82 = 2 * 41, square-free MIXED = F_2 x GF(41)). Islands (2) (the 41
    evens = GF(41) via x -> x mod 41, identity 42) and (41) = {0, 41}. Nilradical
    {0}. Idempotents {0,1,41,42}. Units 40, cyclic. Zero divisors 41. CARRY
    COMPLEMENT: no fixed point (b odd); only preserved coset 21 + (41) = {21, 62}
    (21 = 2^-1 in GF(41), the base-42 midpoint). DOUBLING: one step onto the evens =
    GF(41), where ord(2) = 20: two 20-cycles plus 0.
    26 = (0, 26) and 10 = (0, 10) lie in the GF(41) island (cf. base 42: 26 primitive
    mod 41, 10 of order 5); 37 = (1, 37) is a unit of order 5 (37 = 10^-1 mod 41);
    dr_83(137) = 55 = (1, 14) has order 8.

(68) BASE 84 (m = 83 prime: root ring GF(83), a FIELD; b EVEN). Carry complement
    fixes exactly 42 = (m+1)/2. No coset of any subgroup of order >= 2 maps to a
    coset. |f(QR) & QR| = 20 = (p-3)/4. No primitive sixth roots (83 = 2 mod 3).
    DOUBLING: 2 is PRIMITIVE mod 83 (83 = 3 mod 8, 82 = 2 * 41): one 82-cycle plus 0.
    FORCED: the QRs form the index-2 subgroup of PRIME order 41, so every QR other
    than 1 has order 41 -- 26, 37 and 10 are QRs, hence all of order 41 (1/83 has
    decimal period 41). CONTINGENT: dr_84(137) = 54 is a PRIMITIVE ROOT (a QNR).
    (Ledger for bases 66..83 as JSON: math/ledgers/t432_bases_66_83.json, checked by
    tools/t432_ledger_check.py -- 23/23.)

(69) BASE 85 (m = 84 = 2^2 * 3 * 7, MIXED = Z/4 x F_3 x F_7). Ten islands
    (2),(3),(4),(6),(7),(12),(14),(21),(28),(42). Nilradical {0, 42}. Eight
    idempotents {0,1,21,28,36,49,57,64}. Units 24 = C2 x C2 x C6. Zero divisors 59.
    CARRY COMPLEMENT: no fixed point (b odd); preserved cosets 2+(3), 4+(7),
    11+(21). DOUBLING: settles in v2(84) = 2 steps onto (4) = Z/21 = base 22's root
    ring F_3 x F_7, ord(2) = 6: cycles (0), one 2-cycle, two 3-cycles, two 6-cycles.
    CONTINGENT: 37 is a CUBE ROOT OF UNITY mod 84 (37^2 = 25, 37 * 25 = 925 =
    11*84 + 1); dr_85(137) = 53 has order 6; 26 and 10 are zero divisors.

(70) BASE 86 (m = 85 = 5 * 17, square-free MIXED = F_5 x F_17; b EVEN). Islands
    (5) = F_17, (17) = F_5. Nilradical {0}. Idempotents {0,1,35,51} (51 = (1,0),
    35 = (0,1)). Units 64 = C4 x C16. Zero divisors 20. CARRY COMPLEMENT: fixed
    point 43 = (m+1)/2 (a reflection, section 66), in the preserved cosets 3 + (5)
    and 9 + (17). DOUBLING: permutation, ord(2) = lcm(4, 8) = 8: (0), one 4-cycle,
    ten 8-cycles.
    FORCED BY SMALL DIVISIBILITIES: dr_86(137) = 52 = (2, 1) -- its F_17 coordinate
    is 1 because 136 = 8 * 17 (the fact behind dr_69(137) = 1); 26 = (1, 9) since
    25 | 26 - 1. ord(137) = 4, ord(26) = 8; 37 = (2, 3) has order 16, the maximal
    ELEMENT order in R^x = C4 x C16 (not the order of the doubling map, which is 8);
    10 is a zero divisor.

(71) BASE 87 (m = 86 = 2 * 43, square-free MIXED = F_2 x GF(43)). Islands (2) (the 43
    evens = GF(43) via x -> x mod 43, identity 44 -- base 44's field) and (43) =
    {0, 43}. Nilradical {0}. Idempotents {0,1,43,44}. Units 42, cyclic. Zero
    divisors 43. CARRY COMPLEMENT: no fixed point (b odd); only preserved coset
    22 + (43) = {22, 65} (22 = 2^-1 in GF(43), the base-44 midpoint). DOUBLING: one
    step onto the evens = GF(43), where ord(2) = 14: three 14-cycles plus 0.
    CARRIED OVER FROM BASE 44 (section 15): 37 = (1, 37) has order 6 -- its GF(43)
    coordinate is the primitive sixth root of unity found there; dr_87(137) = 51 =
    (1, 8) with 8 = 2^3 (137 = 8 mod 43), order 14; 26 = (0, 26) and 10 = (0, 10)
    lie in the GF(43) island, with coordinate orders 42 and 21.

(72) BASE 88 (m = 87 = 3 * 29, square-free MIXED = F_3 x F_29; b EVEN). Islands
    (3) = F_29, (29) = F_3. Nilradical {0}. Idempotents {0,1,30,58} (58 = (1,0),
    30 = (0,1)). Units 56 = C2 x C28. Zero divisors 30. CARRY COMPLEMENT: reflection
    about 44 = (m+1)/2, preserved cosets 2 + (3), 15 + (29). DOUBLING: permutation,
    ord(2) = lcm(2, 28) = 28 (2 primitive mod 29): (0), one 2-cycle, three 28-cycles.
    dr_88(137) = 50, 26, 37 and 10 ALL have the maximal element order 28. BASE RATE:
    24 of the 56 units (43%) have order 28 (only those whose C28 coordinate has
    order 28; an order-14 coordinate paired with order 2 gives lcm 14, not 28), so
    all four has chance ~0.43^4 = 3.4% -- not a signal given the many bases and
    properties examined in this sweep.

(73) BASE 89 (m = 88 = 2^3 * 11, MIXED = Z/8 x F_11). Islands (2),(4),(8),(11),(22),
    (44). Nilradical (22) = {0,22,44,66}, index 3 (22^2 = 44, 22^3 = 0). Idempotents
    {0,1,33,56} (33 = (1,0), 56 = (0,1)). Units 40 = C2 x C2 x C10. Zero divisors 47.
    CARRY COMPLEMENT: no fixed point (b odd); only preserved coset 6 + (11).
    DOUBLING: settles in v2(88) = 3 steps onto (8) = F_11 = base 12's root ring; 2
    primitive mod 11: one 10-cycle (8 16 32 64 40 80 72 56 24 48) through the
    idempotent 56 (its identity), plus 0.
    dr_89(137) = 49 = (1, 5) has order 5; 37 = (5, 4) has order 10; 26 and 10 are
    zero divisors.

(74) ON "TEST THE CONSEQUENCE" (supplied methodology note, 2026-09-28). Agreed that a
    thought experiment is worth what it forces and what would falsify it. But the
    note's own example -- "every (a, b) with component orders (4, 16) mod 85 has
    order 16" -- CANNOT FAIL: in a CRT product the order is the lcm of the component
    orders (a theorem). Run exhaustively it passes 16/16 (phi(4) * phi(16) = 16
    elements), which confirms the harness, not the mathematics (null-control /
    miss-test). A consequence with selectivity asks something the structure does NOT
    force -- e.g. whether a claimed special property exceeds its counted base rate
    (section 72: 24/56 units of maximal order, so "all four maximal" has chance 3.4%).

(75) BASE 90 (m = 89 prime: root ring GF(89), a FIELD; b EVEN). Carry complement:
    reflection about 45 = (m+1)/2. No coset of any subgroup of order >= 2 maps to a
    coset. |f(QR) & QR| = 21 = (p-5)/4. No primitive sixth roots (89 = 2 mod 3).
    DOUBLING: 89 = 1 mod 8 makes 2 a QR, and ord_89(2) = 11 (89 | M11 = 2^11 - 1 =
    23 * 89): eight 11-cycles plus 0. Smallest primitive root 3.
    FORCED -- 10 IS A GOLDEN RATIO MOD 89: 10^2 - 10 - 1 = 89, so 10 (and 80) are the
    roots of x^2 - x - 1 in GF(89). This is exactly why 1/89 = sum F_k / 10^(k+1)
    (put x = 1/10 in x/(1 - x - x^2)); and ord_89(10) = 44 = the Pisano period
    pi(89). 89 = F_11, the Fibonacci prime of T245's 89 <-> 233 read-off cycle.
    CONTINGENT: 137 = 48 and 26 are PRIMITIVE ROOTS mod 89; 37 has order 8. The index
    11 in both 89 = F_11 and 89 | 2^11 - 1 is recorded as a coincidence (no mechanism
    found).

(76) THE 1212 LOOP (supplied sequence 1212, 2112, 2121, 3912, 4812, ..., 9312, 1212).
    10 distinct states, 10 transitions, closed. FORCED BY CONSTRUCTION (cannot fail):
    every state has digit sum 6 or 15, both = 6 (mod 9), so every dr is 6 and every
    difference is divisible by 9; the "convergence" values 33, 15, 24, 60 (and
    48 + 12, 32 + 1, 12 + 12) are simply members of the class 6 (mod 9) -- any
    n = 6 (mod 9) passes. GF(37) READING (not visible mod 9): the run 3912 -> 9312
    steps by +900 and 900 = 12 (mod 37), so it is the arithmetic progression
    27, 2, 14, 26, 1, 13, 25 (mod 37); it meets MULT = 26 (6612) and then 1 (7512)
    consecutively because 26 + 12 = 38 = 1 -- a step fact, not a signal.

(77) BASE 91 (m = 90 = 2 * 3^2 * 5, MIXED = F_2 x Z/9 x F_5). Ten islands (2),(3),(5),
    (6),(9),(10),(15),(18),(30),(45). Nilradical {0,30,60}. Eight idempotents
    {0,1,10,36,45,46,55,81}. Units 24 = C2 x C12. Zero divisors 65. CARRY COMPLEMENT:
    no fixed point (b odd); preserved cosets 2+(3), 3+(5), 5+(9), 8+(15), 23+(45).
    DOUBLING: one step onto the evens = Z/45 = base 46's root ring, ord(2) = 12.
    BASE 10 INSIDE BASE 91, LITERALLY (forced: 10 = 1 mod 9, 10 = 0 mod 2 and mod 5):
    10 is an IDEMPOTENT (10^2 = 100 = 90 + 10) and x -> 10x embeds Z/9 as the island
    (10) = 10 * {0..8} with identity 10. Doubling there is base 10's doubling times
    ten: (10 20 40 80 70 50) = 10 * (1 2 4 8 7 5) and (30 60) = 10 * (3 6).
    (Fourth embedding of base 10's ring: bases 46, 64, 73, 91.)
    dr_91(137) = 47 has order 12; 37 = (1, 1, 2) has order 4; 26 is a zero divisor.
    (Supplied 1212-cycle ledger: agrees with section 76; 900-beat accounting checks,
    900 + (9 + 1791) + 6*900 - 8100 = 0.)

(78) BASE 92 (m = 91 = 7 * 13, SQUAREFREE = F_7 x F_13). Two islands (7),(13).
    Nilradical {0}. Four idempotents {0,1,14,78}. Units 72 = C6 x C12, max order 12.
    Zero divisors 19 = 7 + 13 - 1. CARRY COMPLEMENT: fixed point 46 = b/2 (b even);
    preserved cosets 4+(7), 7+(13) (2a = 1 in each factor). DOUBLING: 2 is a unit,
    permutation of order lcm(3, 12) = 12, no collapse (v_2(91) = 0).
    dr_92(137) = 46 = 2^-1 = the carry midpoint: FORCED, the section-(14) case
    91 | 273 = 2*137 - 1; its order is ord(2) = 12 for the same reason.
    26 = (5, 0) is a zero divisor (13 | 26); 37 = (2, 11) has order 12;
    10 = (3, 10) has order 6.

(79) 1212 LOOP, CONSTRUCTIVE AUDIT (supplied request: exact T, invariants, a map phi
    with phi(T x) = 2 phi(x)).
    T: not an arithmetic map. It is defined only by its table, a 10-cycle with
    increments 900, 9, 1791, 900 x 6, -8100 (sum 0). The increments generate 9Z
    (gcd 9; 1791 = 9 * 199), so the only invariant forced by them is x mod 9 = 6 --
    already section (76).
    phi BY REDUCTION FAILS: mod 9 every state is 6 and 2 * 6 = 3; mod 37 the states are
    28,3,12,27,2,14,26,1,13,25 and 2 * 28 = 19 != 3. Doubling on GF(37)* has a single
    orbit of length 36, so the only equivariant phi into Z/37 is phi = 0.
    phi BY CHOICE ALWAYS EXISTS: a 10-cycle is conjugate to doubling on a length-10
    orbit, which needs ord_d(2) = 10, d | 2^10 - 1 = 1023 = 3 * 11 * 31. Smallest
    modulus: 11, phi(x_k) = 2^k mod 11. Mod 11 the states themselves read
    2,0,9,7,5,3,1,10,8,6 (900 = -2 mod 11), not a doubling orbit. Any 10-cycle admits
    this phi, so it carries no information specific to 1212. Into Z/9 only a
    non-injective phi exists (doubling orbits there have lengths 1, 2, 6; a 2-cycle
    {3,6} divides 10).

(80) BASE 93 (m = 92 = 2^2 * 23, MIXED = Z/4 x F_23). Four islands (2),(4),(23),(46).
    Nilradical {0,46}. Four idempotents {0,1,24,69}. Units 44 = C2 x C22, max order
    22. Zero divisors 48. CARRY COMPLEMENT: no fixed point (b odd); one preserved
    coset, 12+(23). DOUBLING: collapses in v_2(92) = 2 steps onto (4) = Z/23 (identity
    24 = (0, 1)); there ord(2) = 11, so the image is {0} plus two 11-cycles.
    dr_93(137) = 45 = (1, -1), order 2: FORCED by 138 = 6 * 23 and 137 = 1 mod 4.
    26 = (2, 3) and 10 = (2, 10) are zero divisors; 37 = (1, 14) has order 22.
    (Supplied restatement of section (77): phi(a) = 10a maps Z/9 onto 10Z/90 as a ring
    isomorphism commuting with doubling -- checked; same content as (77).)

(81) BASE 94 (m = 93 = 3 * 31, SQUAREFREE = F_3 x F_31). Two islands (3),(31).
    Nilradical {0}. Four idempotents {0,1,31,63}. Units 60 = C2 x C30, max order 30.
    Zero divisors 33 = 3 + 31 - 1. CARRY COMPLEMENT: fixed point 47 = b/2; preserved
    cosets 2+(3), 16+(31). DOUBLING: permutation (v_2(93) = 0) of order lcm(2, 5) = 10;
    31 = 2^5 - 1 (Mersenne) gives ord_31(2) = 5; orbit lengths 1, 2, 5, 10.
    dr_94(137) = 44 = (2, 13) has order 30, the maximum (contingent, not forced).
    26 = (2, 26) and 37 = (1, 6) have order 6; 10 = (1, 10) has order 15.

(82) BASE 95 (m = 94 = 2 * 47, SQUAREFREE = F_2 x F_47). Two islands (2),(47).
    Nilradical {0}. Four idempotents {0,1,47,48}. Units 46, CYCLIC (m = 2p). Zero
    divisors 48. CARRY COMPLEMENT: no fixed point (b odd); one preserved coset
    24+(47). DOUBLING: one step onto (2) = F_47 (identity 48 = (0, 1)); there
    ord(2) = 23 (47 = 7 mod 8, so 2 is a QR), so the image is {0} plus two 23-cycles.
    dr_95(137) = 43 = (1, -4) is a PRIMITIVE ROOT mod 94, order 46 (contingent).
    37 = (1, 37) has order 23; 26 and 10 are even, hence zero divisors, though both
    are primitive roots mod 47.

(83) BASE 96 (m = 95 = 5 * 19, SQUAREFREE = F_5 x F_19). Two islands (5),(19).
    Nilradical {0}. Four idempotents {0,1,20,76}. Units 72 = C4 x C18, max order 36.
    Zero divisors 23 = 5 + 19 - 1. CARRY COMPLEMENT: fixed point 48 = b/2; preserved
    cosets 3+(5), 10+(19). DOUBLING: permutation of order lcm(4, 18) = 36, the
    maximum -- 2 is primitive mod 5 and mod 19; orbit lengths 1, 4, 18, 36.
    dr_96(137) = 42 = (2, 4) also has order 36. 26 = (1, 7) has ORDER 3, as it does
    in GF(37) (7^3 = 343 = 18*19 + 1; contingent). 37 = (2, -1) has order 4; 10 is a
    zero divisor (5 | 10).

(84) BASE 97 (m = 96 = 2^5 * 3, MIXED = Z/32 x F_3). Ten islands. Nilradical = (6),
    16 elements (m/rad(m) = 96/6). Four idempotents {0,1,33,64}. Units 32 =
    C2 x C8 x C2, max order 8. Zero divisors 64. CARRY COMPLEMENT: no fixed point
    (b odd); one preserved coset, 2+(3) -- every 2-power ideal has 2a = 1 unsolvable.
    DOUBLING: collapses in v_2(96) = 5 steps (base 65, m = 2^6, takes 6), onto
    (32) = {0,32,64} = F_3 (identity 64 = (0, 1)); there doubling is 32 <-> 64.
    dr_97(137) = 41 = (9, 2) has order 4; 37 = (5, 1) has order 8, the maximum;
    26 and 10 are even, hence zero divisors.

(85) BASE 98 (m = 97, PRIME FIELD GF(97)). No islands, no zero divisors, units
    C96 (primitive root 5). CARRY COMPLEMENT: fixed point 49 = b/2; no proper cosets
    exist to preserve. DOUBLING: 97 = 1 mod 8, so 2 is a QR, ord(2) = 48: {0} plus
    the two cosets of the squares as 48-cycles.
    137 = 40, 26, 37 and 10 are ALL primitive roots mod 97 (each has chance
    phi(96)/96 = 1/3; all four: contingent). 10 primitive: 1/97 has full period 96.

FALSIFICATION: any assertion below failing.
"""
import random
from math import gcd
from sympy import factorint, totient, primitive_root, is_primitive_root


def digits(x, b):
    out = []
    while x:
        out.append(x % b)
        x //= b
    return out


def s(x, b):
    return sum(digits(x, b))


def carries(x, y, b):
    c = n = 0
    while x or y or c:
        t = x % b + y % b + c
        c = 1 if t >= b else 0
        n += c
        x //= b
        y //= b
    return n


def dr(x, b):
    return 0 if x == 0 else 1 + (x - 1) % (b - 1)


def vb(x, b):
    v = 0
    while x % b == 0:
        x //= b
        v += 1
    return v


# (1) Kummer's identity
random.seed(432)
for _ in range(20000):
    b = random.randint(2, 40)
    x = random.randint(0, 10**12)
    y = random.randint(0, 10**12)
    assert (s(x, b) + s(y, b) - s(x + y, b)) == (b - 1) * carries(x, y, b)

# (2) boundary carries
for b in range(2, 30):
    for k in range(1, 6):
        N = b**k
        for D in range(1, N, max(1, N // 300)):
            d = N - D
            v = vb(D, b)
            assert vb(d, b) == v
            assert carries(D, d, b) == k - v
            assert s(D, b) + s(d, b) == 1 + (b - 1) * (k - v)
            assert dr(D, b) + dr(d, b) == b


# (3) the ring Z/n, n = b - 1
def elementary_divisors_units(n):
    out = []
    for p, a in factorint(n).items():
        if p == 2:
            if a == 2:
                out.append(2)
            elif a >= 3:
                out += [2, 2 ** (a - 2)]
        else:
            out.append((p - 1) * p ** (a - 1))
    return sorted(x for x in out if x > 1)


def ring_profile(n):
    U = [x for x in range(n) if gcd(x, n) == 1]
    idem = [x for x in range(n) if x * x % n == x]
    nil = [x for x in range(n) if pow(x, n, n) == 0]  # x^n = 0 iff nilpotent
    zd = [x for x in range(1, n) if gcd(x, n) > 1]
    om = len(factorint(n))
    kind = "FIELD" if om == 1 and max(factorint(n).values()) == 1 else ("LOCAL" if om == 1 else "MIXED")
    rad = 1
    for p in factorint(n):
        rad *= p
    # closed forms
    assert len(U) == totient(n)
    assert len(idem) == 2**om
    assert len(nil) == n // rad
    assert len(zd) == n - totient(n) - 1
    # unit-group structure: element-order census matches the elementary divisors
    ed = elementary_divisors_units(n)
    cyclic = any(is_primitive_root(g, n) for g in U) if n > 2 else True
    assert cyclic == (len(ed) <= 1)
    return dict(n=n, kind=kind, units=len(U), unit_group=ed or [1], cyclic=cyclic,
                idempotents=idem, nilpotents=nil, zero_divisors=len(zd), two_inv=gcd(2, n) == 1)


TABLE = {b: ring_profile(b - 1) for b in range(3, 41)}
for b, r in TABLE.items():
    assert r["two_inv"] == (b % 2 == 0)

# (4) base 13
r13 = TABLE[13]
assert r13["kind"] == "MIXED" and r13["unit_group"] == [2, 2] and not r13["cyclic"]
assert r13["idempotents"] == [0, 1, 4, 9] and r13["nilpotents"] == [0, 6]
assert [x for x in range(1, 12) if gcd(x, 12) > 1] == [2, 3, 4, 6, 8, 9, 10]
assert all(u * u % 12 == 1 for u in (1, 5, 7, 11))
assert [g for g in range(1, 13) if is_primitive_root(g, 13)] == [2, 6, 7, 11]

# (5) GF(37)
r38 = TABLE[38]
assert r38["kind"] == "FIELD" and r38["units"] == 36 and r38["cyclic"]
r37 = TABLE[37]
assert r37["kind"] == "MIXED" and r37["unit_group"] == [2, 6] and len(r37["idempotents"]) == 4
assert len(r37["nilpotents"]) == 6 and not r37["two_inv"]
assert primitive_root(37) == 2

# (6) base 37: carry map coset structure on Z/36
m = 36
assert [d for d in range(2, m) if m % d == 0] == [2, 3, 4, 6, 9, 12, 18]
assert [x for x in range(m) if pow(x, m, m) == 0] == [0, 6, 12, 18, 24, 30]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 9, 28]
assert not [r for r in range(m) if (1 - r) % m == r]
pres = {d: [a for a in range(d) if (1 - a) % d == a] for d in (2, 3, 4, 6, 9, 12, 18)}
assert pres == {2: [], 3: [2], 4: [], 6: [], 9: [5], 12: [], 18: []}
assert len({2 * x % m for x in range(m)}) == 18
assert all(any((x * 2**k) % 4 == 0 for k in range(3)) for x in range(m))
cyc = [4, 8, 16, 32, 28, 20]
assert all(cyc[(i + 1) % 6] == 2 * cyc[i] % m for i in range(6))
assert [x % 9 for x in cyc] == [4, 8, 7, 5, 1, 2] and [12 % 9, 24 % 9] == [3, 6]
assert sorted(x % 9 for x in range(0, m, 4)) == list(range(9))
DLOG = {pow(2, k, 37): k for k in range(36)}
assert len(DLOG) == 36 and DLOG[26] == 12
ORB = {frozenset({x, 26 * x % 37, 26 * 26 * x % 37}) for x in range(1, 37)}
assert len(ORB) == 12 and all(len({DLOG[y] % 12 for y in o}) == 1 for o in ORB)
assert 137 % 36 == 29

# (7) base 38: root ring GF(37)
p = 37
assert [r for r in range(p) if (1 - r) % p == r] == [19] and 2 * 19 % p == 1
CAS_EXT = {5, 13, 19}
assert 19 in CAS_EXT
assert sorted((1 - x) % p for x in (11, 27, 36)) == [2, 11, 27]
assert [r for r in range(p) if (r * r - r + 1) % p == 0] == [11, 27]
assert all(pow(2, k, p) != 1 for k in range(1, 36))
for d in (2, 3, 4, 6, 9, 12, 18, 36):
    H = {pow(2, 36 // d * i, p) for i in range(d)}
    assert sum(H) % p == 0
    cos = {frozenset(x * h % p for h in H) for x in range(1, p)}
    assert not any(frozenset((1 - x) % p for x in c) in cos for c in cos)

# (8) base 39
m = 38
assert [d for d in range(2, m) if m % d == 0] == [2, 19]
assert [x for x in range(m) if pow(x, m, m) == 0] == [0]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 19, 20]
assert not [r for r in range(m) if (1 - r) % m == r]
assert [a for a in range(19) if (1 - a) % 19 == a] == [10] and (1 - 10) % m == 29
assert sorted({2 * x % m for x in range(m)}) == list(range(0, m, 2))
assert sorted(x % 19 for x in range(0, m, 2)) == list(range(19))
assert all(pow(2, k, 19) != 1 for k in range(1, 18))
assert 137 % m == 23 and next(k for k in range(1, 19) if pow(23, k, m) == 1) == 9


# (9) doubling collapse, every base b = 3..60
def v2(n):
    a = 0
    while n % 2 == 0:
        n //= 2
        a += 1
    return a


for b in range(3, 61):
    m = b - 1
    a = v2(m)
    n = m >> a
    ideal = set(range(0, m, 2**a))
    assert all((x * 2**a) % m in ideal for x in range(m))                  # enters within a steps
    if a:
        assert any((x * 2**(a - 1)) % m not in ideal for x in range(m))    # a is sharp
    assert sorted(x % n for x in ideal) == list(range(n)) if n > 1 else True
    assert all((2 * x) % m % n == (2 * (x % n)) % n for x in ideal)        # x2 on (2^a) = x2 on Z/n

# (10) base 40
m = 39
assert [d for d in range(2, m) if m % d == 0] == [3, 13]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 13, 27]
assert [r for r in range(m) if (1 - r) % m == r] == [20]
assert 20 % 3 == 2 and 20 % 13 == 7
assert 137 % m == 20 and 2 * 137 % m == 1 and 273 == 3 * 7 * 13
assert 26 % 13 == 0
assert sorted({2 * x % m for x in range(m)}) == list(range(m))          # permutation
assert next(k for k in range(1, 13) if pow(2, k, 13) == 1) == 12
assert (2 * 13) % m == 26 and (2 * 26) % m == 13

# (11) base 41
m = 40
assert [d for d in range(2, m) if m % d == 0] == [2, 4, 5, 8, 10, 20]
assert [x for x in range(m) if pow(x, m, m) == 0] == [0, 10, 20, 30]
assert pow(10, 2, m) == 20 and pow(10, 3, m) == 0
assert [x for x in range(m) if x * x % m == x] == [0, 1, 16, 25]
assert not [r for r in range(m) if (1 - r) % m == r]
assert {d: [a for a in range(d) if (1 - a) % d == a] for d in (2, 4, 5, 8, 10, 20)} == \
    {2: [], 4: [], 5: [3], 8: [], 10: [], 20: []}
assert all((x * 8) % m in {0, 8, 16, 24, 32} for x in range(m))
assert any((x * 4) % m not in {0, 8, 16, 24, 32} for x in range(m))
assert [2 * y % m for y in (8, 16, 32, 24)] == [16, 32, 24, 8]
assert 137 % m == 17 and pow(17, 4, m) == 1 and pow(17, 2, m) != 1
assert pow(37, 4, m) == 1 and pow(37, 2, m) != 1

# (12) base 42
p = 41
QR41 = {x * x % p for x in range(1, p)}
assert [r for r in range(p) if (1 - r) % p == r] == [21] and 21 in QR41
assert {pow(2, k, p) for k in range(20)} == QR41 and pow(2, 20, p) == 1
assert not [r for r in range(p) if (r * r - r + 1) % p == 0]
assert len({(1 - x) % p for x in QR41} & QR41) == (p - 5) // 4 == 9
assert all(pow(26, 40 // q, p) != 1 for q in (2, 5))                     # 26 primitive mod 41
assert pow(10, 5, p) == 1 and pow(37, 5, p) == 1 and 10 * 37 % p == 1
assert pow(10, 4, p) == 37 and 10**5 - 1 == 9 * 41 * 271 and 10000 - 37 == 41 * 3**5
assert 137 % p == 14 and pow(14, 8, p) == 1 and pow(14, 4, p) != 1 and 14 not in QR41
for d in (2, 4, 5, 8, 10, 20, 40):
    H = {pow(6, 40 // d * i, p) for i in range(d)}
    cos = {frozenset(x * h % p for h in H) for x in range(1, p)}
    assert not any(frozenset((1 - x) % p for x in c) in cos for c in cos)

# (13) base 43
m = 42
assert [d for d in range(2, m) if m % d == 0] == [2, 3, 6, 7, 14, 21]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 7, 15, 21, 22, 28, 36]
assert not [r for r in range(m) if (1 - r) % m == r]
assert {d: [a for a in range(d) if (1 - a) % d == a] for d in (2, 3, 6, 7, 14, 21)} == \
    {2: [], 3: [2], 6: [], 7: [4], 14: [], 21: [11]}
assert (1 - 11) % m == 32 and (1 - 32) % m == 11
assert len({2 * x % m for x in range(m)}) == 21
assert [2 * y % m for y in (2, 4, 8, 16, 32, 22)] == [4, 8, 16, 32, 22, 2]
assert 137 % m == 11 and pow(11, 6, m) == 1 and pow(11, 3, m) != 1 and pow(11, 2, m) != 1

# (14) 137 = 2^-1 mod every divisor of 273
assert 2 * 137 - 1 == 273 == 3 * 7 * 13
D273 = [d for d in range(2, 274) if 273 % d == 0]
assert D273 == [3, 7, 13, 21, 39, 91, 273]
assert all(2 * 137 % d == 1 for d in D273)
for b in [d + 1 for d in D273]:
    assert [r for r in range(b - 1) if (1 - r) % (b - 1) == r] == [b // 2] == [137 % (b - 1) or b - 1]

# (15) base 44
p = 43
QR43 = {x * x % p for x in range(1, p)}
assert [r for r in range(p) if (1 - r) % p == r] == [22] and 22 not in QR43
assert len({(1 - x) % p for x in QR43} & QR43) == (p - 3) // 4 == 10
assert pow(2, 14, p) == 1 and all(pow(2, k, p) != 1 for k in range(1, 14))
assert [r for r in range(1, p) if pow(r, 3, p) == 1] == [1, 6, 36]
assert [r for r in range(p) if (r * r - r + 1) % p == 0] == [7, 37] and (1 - 7) % p == 37
assert pow(37, 6, p) == 1 and all(pow(37, k, p) != 1 for k in (1, 2, 3)) and 37 * 37 - 37 + 1 == 43 * 31
assert all(pow(26, 42 // q, p) != 1 for q in (2, 3, 7))
assert pow(10, 21, p) == 1 and all(pow(10, 21 // q, p) != 1 for q in (3, 7))
assert 137 % p == 8 == 2**3
for d in (2, 3, 6, 7, 14, 21, 42):
    H = {pow(3, 42 // d * i, p) for i in range(d)}
    cos = {frozenset(x * h % p for h in H) for x in range(1, p)}
    assert not any(frozenset((1 - x) % p for x in c) in cos for c in cos)

# (16) base 45
m = 44
assert [d for d in range(2, m) if m % d == 0] == [2, 4, 11, 22]
assert [x for x in range(m) if pow(x, m, m) == 0] == [0, 22]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 12, 33]
assert not [r for r in range(m) if (1 - r) % m == r]
assert {d: [a for a in range(d) if (1 - a) % d == a] for d in (2, 4, 11, 22)} == {2: [], 4: [], 11: [6], 22: []}
C45 = [4, 8, 16, 32, 20, 40, 36, 28, 12, 24]
assert all(C45[(i + 1) % 10] == 2 * C45[i] % m for i in range(10))
assert all((x * 4) % m in set(C45) | {0} for x in range(m))
assert 137 % m == 5 and pow(5, 3, m) == 37 and pow(5, 5, m) == 1 and pow(37, 5, m) == 1
assert dr(9, 10) == 9 and 9 % 9 == 0 and dr(10, 10) == 1 and dr(45, 10) == 9

# (17) base 46
m = 45
assert m == sum(range(10))
assert [d for d in range(2, m) if m % d == 0] == [3, 5, 9, 15]
assert [x for x in range(m) if pow(x, m, m) == 0] == [0, 15, 30]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 10, 36]
assert [r for r in range(m) if (1 - r) % m == r] == [23]
assert {d: [a for a in range(d) if (1 - a) % d == a] for d in (3, 5, 9, 15)} == {3: [2], 5: [3], 9: [5], 15: [8]}
assert all(23 % d == a[0] for d, a in {3: [2], 5: [3], 9: [5], 15: [8]}.items())
I5 = list(range(0, m, 5))
assert sorted(x % 9 for x in I5) == list(range(9))                        # (5) = Z/9 as a ring
assert all((x * y) % m % 9 == (x % 9) * (y % 9) % 9 for x in I5 for y in I5)
assert 10 % 9 == 1 and 10 % 5 == 0 and 10 * 10 % m == 10 and all(10 * x % m == x for x in I5)
assert 26 * 26 % m == 1 and 137 % m == 2
assert sorted({2 * x % m for x in range(m)}) == list(range(m)) and pow(2, 12, m) == 1

# (18) midpoint flanks
for b in range(4, 400, 2):
    c = b // 2
    assert (2 * c) % (b - 1) == 1 % (b - 1)
    assert ((c - 1) % 2 == 0 and (c + 1) % 2 == 0) == (b % 4 == 2)
    assert (c - 1) + (c + 1) == b

# (19) base 47
m = 46
assert [d for d in range(2, m) if m % d == 0] == [2, 23]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 23, 24]
assert not [r for r in range(m) if (1 - r) % m == r]
assert [a for a in range(23) if (1 - a) % 23 == a] == [12]
assert next(k for k in range(1, 23) if pow(2, k, 23) == 1) == 11
assert 137 % m == m - 1 and 138 == 3 * m
assert all(pow(37, 22 // q, m) != 1 for q in (2, 11))

# (20) base 48
p = 47
QR47 = {x * x % p for x in range(1, p)}
assert [r for r in range(p) if (1 - r) % p == r] == [24]
assert len({(1 - x) % p for x in QR47} & QR47) == 11 and not [r for r in range(p) if (r * r - r + 1) % p == 0]
assert pow(2, 23, p) == 1 and 2 in QR47
assert all(all(pow(g, 46 // q, p) != 1 for q in (2, 23)) for g in (137 % p, 26, 10))
assert pow(37, 23, p) == 1 and 47 % 37 == 10

# (21) base 49
m = 48
assert [d for d in range(2, m) if m % d == 0] == [2, 3, 4, 6, 8, 12, 16, 24]
assert [x for x in range(m) if pow(x, m, m) == 0] == list(range(0, m, 6))
assert pow(6, 3, m) == 24 and pow(6, 4, m) == 0
assert [x for x in range(m) if x * x % m == x] == [0, 1, 16, 33]
assert not [r for r in range(m) if (1 - r) % m == r] and [a for a in range(3) if (1 - a) % 3 == a] == [2]
assert all((x * 16) % m in {0, 16, 32} for x in range(m)) and any((x * 8) % m not in {0, 16, 32} for x in range(m))
assert 2 * 16 % m == 32 and 2 * 32 % m == 16
assert 137 % m == 41 and 41 * 41 % m == 1 and pow(37, 4, m) == 1 and pow(37, 2, m) != 1

# (22) base 50
m = 49
assert [d for d in range(2, m) if m % d == 0] == [7]
assert all(a * b % m == 0 for a in range(0, m, 7) for b in range(0, m, 7))
assert [r for r in range(m) if (1 - r) % m == r] == [25] and 25 % 7 == 4
assert pow(2, 21, m) == 1 and pow(2, 3, m) != 1 and pow(2, 7, m) != 1
assert [2 * y % m for y in (7, 14, 28, 21, 42, 35)] == [14, 28, 7, 42, 35, 21]
assert all(pow(g, 42 // q, m) != 1 for g in (26, 10) for q in (2, 3, 7))
assert pow(137 % m, 21, m) == 1 and pow(37, 21, m) == 1

# (23) base 51
m = 50
assert [d for d in range(2, m) if m % d == 0] == [2, 5, 10, 25]
assert [x for x in range(m) if pow(x, m, m) == 0] == [0, 10, 20, 30, 40] and 10 * 10 % m == 0
assert [x for x in range(m) if x * x % m == x] == [0, 1, 25, 26]
assert not [r for r in range(m) if (1 - r) % m == r]
assert [a for a in range(5) if (1 - a) % 5 == a] == [3] and [a for a in range(25) if (1 - a) % 25 == a] == [13]
assert pow(2, 20, m) == 26 and len({pow(2, k, m) for k in range(1, 21)}) == 20
assert [2 * y % m for y in (10, 20, 40, 30)] == [20, 40, 30, 10]
assert 137 % m == 37 and all(pow(37, 20 // q, m) != 1 for q in (2, 5))

# (24) base 52
m = 51
assert [d for d in range(2, m) if m % d == 0] == [3, 17]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 18, 34]
assert [r for r in range(m) if (1 - r) % m == r] == [26] and 26 % 3 == 2 and 26 % 17 == 9
assert pow(2, 8, m) == 1 and pow(26, 8, m) == 1 and pow(26, 4, m) != 1
assert 137 % m == 35 and 35 * 35 % m == 1
assert pow(37, 16, m) == 1 and pow(37, 8, m) != 1 and pow(10, 16, m) == 1 and pow(10, 8, m) != 1

# (25) base 53
m = 52
assert [d for d in range(2, m) if m % d == 0] == [2, 4, 13, 26]
assert [x for x in range(m) if pow(x, m, m) == 0] == [0, 26] and 26 * 26 == 13 * m
assert [x for x in range(m) if x * x % m == x] == [0, 1, 13, 40]
assert not [r for r in range(m) if (1 - r) % m == r] and [a for a in range(13) if (1 - a) % 13 == a] == [7]
C53 = [4, 8, 16, 32, 12, 24, 48, 44, 36, 20, 40, 28]
assert all(C53[(i + 1) % 12] == 2 * C53[i] % m for i in range(12)) and all((4 * x) % m in set(C53) | {0} for x in range(m))
assert 137 % m == 33 and pow(33, 12, m) == 1 and pow(33, 6, m) != 1 and pow(33, 4, m) != 1
assert pow(37, 12, m) == 1 and pow(37, 6, m) != 1 and pow(37, 4, m) != 1

# (26) base 54
p = 53
QR53 = {x * x % p for x in range(1, p)}
assert [r for r in range(p) if (1 - r) % p == r] == [27] and 27 == 3**3
assert len({(1 - x) % p for x in QR53} & QR53) == 12 and not [r for r in range(p) if (r * r - r + 1) % p == 0]
assert all(pow(2, 52 // q, p) != 1 for q in (2, 13)) and 2 not in QR53
assert all(all(pow(g, 52 // q, p) != 1 for q in (2, 13)) for g in (137 % p, 26))
assert pow(37, 26, p) == 1 and pow(37, 13, p) != 1 and pow(37, 2, p) != 1
assert pow(10, 13, p) == 1 and pow(10, 1, p) != 1
assert [pow(2, k, p) for k in (25, 30, 48)] == [26, 37, 10]

# (27) base 55
m = 54
assert [d for d in range(2, m) if m % d == 0] == [2, 3, 6, 9, 18, 27]
assert [x for x in range(m) if pow(x, m, m) == 0] == list(range(0, m, 6)) and pow(6, 2, m) == 36 and pow(6, 3, m) == 0
assert [x for x in range(m) if x * x % m == x] == [0, 1, 27, 28]
assert {d: a for d in (3, 9, 27) for a in [[a for a in range(d) if (1 - a) % d == a]]} == {3: [2], 9: [5], 27: [14]}
assert [2 * y % m for y in (6, 12, 24, 48, 42, 30)] == [12, 24, 48, 42, 30, 6] and 2 * 18 % m == 36 and 2 * 36 % m == 18
assert [x for x in range(m) if pow(x, 3, m) == 1] == [1, 19, 37] and 37 * 37 % m == 19 and 37 * 19 == 13 * m + 1
assert 137 % m == 29 and all(pow(29, 18 // q, m) != 1 for q in (2, 3))

# (28) base 56
m = 55
assert [d for d in range(2, m) if m % d == 0] == [5, 11]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 11, 45]
assert [r for r in range(m) if (1 - r) % m == r] == [28] and 28 % 5 == 3 and 28 % 11 == 6
assert pow(2, 20, m) == 1 and pow(2, 10, m) != 1 and pow(2, 4, m) != 1
assert 137 % m == 27 and pow(27, 20, m) == 1 and pow(27, 10, m) != 1 and pow(27, 4, m) != 1
assert pow(37, 20, m) == 1 and pow(37, 10, m) != 1 and pow(37, 4, m) != 1 and pow(26, 5, m) == 1

# (29) base 57
m = 56
assert [d for d in range(2, m) if m % d == 0] == [2, 4, 7, 8, 14, 28]
assert [x for x in range(m) if pow(x, m, m) == 0] == [0, 14, 28, 42] and pow(14, 2, m) == 28 and pow(14, 3, m) == 0
assert [x for x in range(m) if x * x % m == x] == [0, 1, 8, 49]
assert not [r for r in range(m) if (1 - r) % m == r] and [a for a in range(7) if (1 - a) % 7 == a] == [4]
assert all((x * 8) % m in {0, 8, 16, 24, 32, 40, 48} for x in range(m)) and any((x * 4) % m not in {0, 8, 16, 24, 32, 40, 48} for x in range(m))
assert [2 * y % m for y in (8, 16, 32, 24, 48, 40)] == [16, 32, 8, 48, 40, 24]
assert 137 % m == 25 and [x for x in range(m) if pow(x, 3, m) == 1] == [1, 9, 25] and 25 * 9 == 4 * m + 1
assert pow(37, 6, m) == 1 and pow(37, 3, m) != 1 and pow(37, 2, m) != 1

# (30) base 58
m = 57
assert [d for d in range(2, m) if m % d == 0] == [3, 19]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 19, 39]
assert [r for r in range(m) if (1 - r) % m == r] == [29] and 29 % 3 == 2 and 29 % 19 == 10
assert pow(2, 18, m) == 1 and pow(2, 9, m) != 1 and pow(2, 6, m) != 1
assert [x for x in range(m) if pow(x, 3, m) == 1] == [1, 7, 49]
assert 37 * 37 == 24 * m + 1 and 137 % m == 23
assert all(pow(g, 18 // q, m) != 1 for g in (23, 10) for q in (2, 3)) and pow(26, 6, m) == 1 and pow(26, 3, m) != 1 and pow(26, 2, m) != 1

# (31) base 59
m = 58
assert [d for d in range(2, m) if m % d == 0] == [2, 29]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 29, 30]
assert not [r for r in range(m) if (1 - r) % m == r] and [a for a in range(29) if (1 - a) % 29 == a] == [15]
assert all(pow(2, 28 // q, 29) != 1 for q in (2, 7))
assert 137 % m == 21 and all(pow(g, 28 // q, m) != 1 for g in (21, 37) for q in (2, 7))

# (32) base 60
p = 59
QR59 = {x * x % p for x in range(1, p)}
assert [x for x in range(60) if x * x % 60 == x] == [0, 1, 16, 21, 25, 36, 40, 45]
assert [r for r in range(p) if (1 - r) % p == r] == [30]
assert len({(1 - x) % p for x in QR59} & QR59) == 14 and not [r for r in range(p) if (r * r - r + 1) % p == 0]
assert all(pow(g, 58 // q, p) != 1 for g in (2, 37, 10) for q in (2, 29))
assert 137 % p == 19 and all(pow(g, 29, p) == 1 and g in QR59 for g in (19, 26))

# (33) base 61
m = 60
assert [d for d in range(2, m) if m % d == 0] == [2, 3, 4, 5, 6, 10, 12, 15, 20, 30]
assert [x for x in range(m) if pow(x, m, m) == 0] == [0, 30]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 16, 21, 25, 36, 40, 45]
assert {d: a for d in (3, 5, 15) for a in [[a for a in range(d) if (1 - a) % d == a]]} == {3: [2], 5: [3], 15: [8]}
I4 = set(range(0, m, 4))
assert all((x * 4) % m in I4 for x in range(m)) and sorted(x % 15 for x in I4) == list(range(15))
for c in ((4, 8, 16, 32), (12, 24, 48, 36), (28, 56, 52, 44), (20, 40)):
    assert all(c[(i + 1) % len(c)] == 2 * c[i] % m for i in range(len(c)))
assert [16 % 15, 36 % 15, 40 % 15] == [1, 6, 10]
assert 137 % m == 17 and pow(17, 4, m) == 1 and pow(17, 2, m) != 1 and pow(37, 4, m) == 1 and pow(37, 2, m) != 1

# (34) base 62
p = 61
QR61 = {x * x % p for x in range(1, p)}
assert [r for r in range(p) if (1 - r) % p == r] == [31]
assert len({(1 - x) % p for x in QR61} & QR61) == 14
assert [r for r in range(1, p) if pow(r, 3, p) == 1] == [1, 13, 47]
assert [r for r in range(p) if (r * r - r + 1) % p == 0] == [14, 48] and (1 - 14) % p == 48
assert all(pow(g, 60 // q, p) != 1 for g in (2, 26, 10) for q in (2, 3, 5))
assert pow(37, 20, p) == 1 and all(pow(37, 20 // q, p) != 1 for q in (2, 5))
assert 137 % p == 15 and pow(15, 15, p) == 1 and all(pow(15, 15 // q, p) != 1 for q in (3, 5))

# (35) base 63
m = 62
assert [d for d in range(2, m) if m % d == 0] == [2, 31]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 31, 32]
assert not [r for r in range(m) if (1 - r) % m == r] and [a for a in range(31) if (1 - a) % 31 == a] == [16]
assert pow(2, 5, 31) == 1 and 31 == 2**5 - 1
assert 137 % m == 13 and all(pow(13, 30 // q, m) != 1 for q in (2, 3, 5))
assert pow(37, 6, m) == 1 and pow(37, 3, m) != 1 and pow(37, 2, m) != 1

# (36) base 64
m = 63
assert [d for d in range(2, m) if m % d == 0] == [3, 7, 9, 21]
assert [x for x in range(m) if pow(x, m, m) == 0] == [0, 21, 42]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 28, 36]
assert [r for r in range(m) if (1 - r) % m == r] == [32]
assert {d: [a for a in range(d) if (1 - a) % d == a] for d in (3, 7, 9, 21)} == {3: [2], 7: [4], 9: [5], 21: [11]}
assert pow(2, 6, m) == 1 and all(pow(2, k, m) != 1 for k in range(1, 6))
for k in range(2, 20):                                              # base 2^k: ord_{2^k - 1}(2) = k
    assert next(j for j in range(1, k + 1) if pow(2, j, 2**k - 1) == 1 % (2**k - 1)) == k
I7_64 = list(range(0, m, 7))
assert sorted(x % 9 for x in I7_64) == list(range(9)) and 28 % 9 == 1 and 28 % 7 == 0
assert [y % 9 for y in (7, 14, 28, 56, 49, 35)] == [7, 5, 1, 2, 4, 8] and [21 % 9, 42 % 9] == [3, 6]
assert all(2 * a % m == b for a, b in [(7, 14), (14, 28), (28, 56), (56, 49), (49, 35), (35, 7), (21, 42), (42, 21)])
assert 37 * 37 % m == 46 and 37 * 46 == 27 * m + 1
assert 137 % m == 11 and all(pow(g, 6, m) == 1 and pow(g, 2, m) != 1 and pow(g, 3, m) != 1 for g in (11, 26, 10))

# (37) base 65
m = 64
assert [d for d in range(2, m) if m % d == 0] == [2, 4, 8, 16, 32]
assert [x for x in range(m) if pow(x, m, m) == 0] == list(range(0, m, 2)) and pow(2, 6, m) == 0 and pow(2, 5, m) != 0
assert [x for x in range(m) if x * x % m == x] == [0, 1]
assert not [r for r in range(m) if (1 - r) % m == r]
assert sorted((1 - x) % m for x in range(0, m, 2)) == list(range(1, m, 2))
assert all(x * 64 % m == 0 for x in range(m)) and any(x * 32 % m for x in range(m))
assert all(pow(r, 6, m) == 0 and pow(r, 5, m) != 0 for r in (26, 10))
assert 137 % m == 9 and pow(9, 8, m) == 1 and pow(9, 4, m) != 1 and pow(37, 16, m) == 1 and pow(37, 8, m) != 1

# (38) base 66
m = 65
assert [d for d in range(2, m) if m % d == 0] == [5, 13]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 26, 40] and 26 % 5 == 1 and 26 % 13 == 0
assert [r for r in range(m) if (1 - r) % m == r] == [33] and 33 % 5 == 3 and 33 % 13 == 7
assert pow(2, 12, m) == 1 and pow(2, 6, m) != 1 and pow(2, 4, m) != 1
assert [2 * y % m for y in (13, 26, 52, 39)] == [26, 52, 39, 13]
assert all(26 * x % m == x for x in range(0, m, 13))                   # identity on the island (13)
assert 137 % m == 7 and all(pow(g, 12, m) == 1 and pow(g, 6, m) != 1 and pow(g, 4, m) != 1 for g in (7, 37))

# (39) base 67, (40) the 26-idempotent criterion
m = 66
assert [d for d in range(2, m) if m % d == 0] == [2, 3, 6, 11, 22, 33]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 12, 22, 33, 34, 45, 55]
assert not [r for r in range(m) if (1 - r) % m == r]
assert {d: [a for a in range(d) if (1 - a) % d == a] for d in (3, 11, 33)} == {3: [2], 11: [6], 33: [17]}
assert sorted({2 * x % m for x in range(m)}) == list(range(0, m, 2)) and pow(2, 10, 33) == 1 and pow(2, 5, 33) != 1
assert 2 * 22 % m == 44 and 2 * 44 % m == 22
assert 137 % m == 5 and pow(5, 10, m) == 1 and pow(5, 5, m) != 1 and pow(37, 5, m) == 1
assert [mm for mm in range(2, 201) if (26 * 26 - 26) % mm == 0] == [2, 5, 10, 13, 25, 26, 50, 65, 130]
assert [b for b in range(37, 68) if (26 * 26 - 26) % (b - 1) == 0] == [51, 66]
assert not [r for r in range(50) if (1 - r) % 50 == r]
from math import gcd as _g
assert sum(1 for u in range(65) if _g(u, 65) == 1 and pow(u, 12, 65) == 1 and pow(u, 6, 65) != 1 and pow(u, 4, 65) != 1) == 24

# (41) base 68
p = 67
QR67 = {x * x % p for x in range(1, p)}
assert [r for r in range(p) if (1 - r) % p == r] == [34] == [(p + 1) // 2]
assert len({(1 - x) % p for x in QR67} & QR67) == 16
assert [r for r in range(1, p) if pow(r, 3, p) == 1] == [1, 29, 37] and 37 * 37 % p == 29 and 37 * 29 == 16 * p + 1
assert [r for r in range(p) if (r * r - r + 1) % p == 0] == [30, 38] and (1 - 30) % p == 38
assert all(pow(2, 66 // q, p) != 1 for q in (2, 3, 11))
assert all(pow(g, 33, p) == 1 and pow(g, 11, p) != 1 and pow(g, 3, p) != 1 for g in (26, 10))
assert 137 % p == 3 and pow(3, 22, p) == 1 and pow(3, 11, p) != 1 and pow(3, 2, p) != 1
for mm in (44, 45, 50, 65):                                          # standardized fixed-point table
    assert [r for r in range(mm) if (1 - r) % mm == r] == ([(mm + 1) // 2] if mm % 2 else [])

# (42) base 69
m = 68
assert [d for d in range(2, m) if m % d == 0] == [2, 4, 17, 34]
assert [x for x in range(m) if pow(x, m, m) == 0] == [0, 34]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 17, 52]
assert not [r for r in range(m) if (1 - r) % m == r] and [a for a in range(17) if (1 - a) % 17 == a] == [9]
C69 = [4, 8, 16, 32, 64, 60, 52, 36]
assert all(C69[(i + 1) % 8] == 2 * C69[i] % m for i in range(8)) and all((4 * x) % m % 4 == 0 for x in range(m))
assert 137 % m == 1 and 136 == 2**3 * 17
assert pow(37, 16, m) == 1 and pow(37, 8, m) != 1

# (43) base 70
m = 69
assert [d for d in range(2, m) if m % d == 0] == [3, 23]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 24, 46]
assert [r for r in range(m) if (1 - r) % m == r] == [35] and 35 % 3 == 2 and 35 % 23 == 12
assert pow(2, 11, 23) == 1 and pow(2, 22, m) == 1 and pow(2, 11, m) != 1
assert 137 % m == m - 1 and 138 == 2 * m
assert all(pow(g, 22, m) == 1 and pow(g, 11, m) != 1 and pow(g, 2, m) != 1 for g in (26, 37, 10))

# (44) base 71 + base-rate check
m = 70
assert [d for d in range(2, m) if m % d == 0] == [2, 5, 7, 10, 14, 35]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 15, 21, 35, 36, 50, 56]
assert not [r for r in range(m) if (1 - r) % m == r]
assert {d: [a for a in range(d) if (1 - a) % d == a] for d in (5, 7, 35)} == {5: [3], 7: [4], 35: [18]}
assert sorted({2 * x % m for x in range(m)}) == list(range(0, m, 2)) and pow(2, 12, 35) == 1 and pow(2, 6, 35) != 1 and pow(2, 4, 35) != 1
assert 137 % m == 67 and all(pow(g, 12, m) == 1 and pow(g, 6, m) != 1 and pow(g, 4, m) != 1 for g in (67, 37))
from math import gcd as _g2
_ord = lambda u, mm: next(k for k in range(1, mm) if pow(u, k, mm) == 1)
assert sum(1 for u in range(70) if _g2(u, 70) == 1 and _ord(u, 70) == 12) == 8
assert sum(1 for u in range(69) if _g2(u, 69) == 1 and _ord(u, 69) == 22) == 30

# (45) base 72, (46) parity dichotomy across b = 3..200
p = 71
QR71 = {x * x % p for x in range(1, p)}
assert [r for r in range(p) if (1 - r) % p == r] == [36] and len({(1 - x) % p for x in QR71} & QR71) == 17
assert pow(2, 35, p) == 1 and pow(2, 5, p) != 1 and pow(2, 7, p) != 1 and 2 in QR71
assert 137 % p == 66 and pow(66, 10, p) == 1 and pow(66, 5, p) != 1 and pow(66, 2, p) != 1
assert pow(26, 14, p) == 1 and pow(26, 7, p) != 1 and pow(37, 7, p) == 1 and pow(10, 35, p) == 1 and pow(10, 7, p) != 1 and pow(10, 5, p) != 1
for b in range(3, 201):
    mm = b - 1
    a = v2(mm)
    n = mm >> a
    fp = [r for r in range(mm) if (1 - r) % mm == r]
    perm = len({2 * x % mm for x in range(mm)}) == mm
    if b % 2 == 0:
        assert perm and fp == [b // 2]
    else:
        assert not perm and not fp
        ideal = set(range(0, mm, 2**a))
        assert all((x * 2**a) % mm in ideal for x in range(mm))
        assert any((x * 2**(a - 1)) % mm not in ideal for x in range(mm))

# (47) base 73
m = 72
assert [d for d in range(2, m) if m % d == 0] == [2, 3, 4, 6, 8, 9, 12, 18, 24, 36]
assert [x for x in range(m) if pow(x, m, m) == 0] == list(range(0, m, 6)) and pow(6, 3, m) == 0 and pow(6, 2, m) != 0
assert [x for x in range(m) if x * x % m == x] == [0, 1, 9, 64]
assert not [r for r in range(m) if (1 - r) % m == r]
I8_73 = list(range(0, m, 8))
assert all(x * 8 % m in I8_73 for x in range(m)) and any(x * 4 % m not in I8_73 for x in range(m))
assert sorted(x % 9 for x in I8_73) == list(range(9)) and 64 % 9 == 1 and 64 % 8 == 0
assert [y % 9 for y in (8, 16, 32, 64, 56, 40)] == [8, 7, 5, 1, 2, 4] and [24 % 9, 48 % 9] == [6, 3]
assert 37 * 37 == 19 * m + 1 and 137 % m == 65 and pow(65, 6, m) == 1 and pow(65, 3, m) != 1 and pow(65, 2, m) != 1

# (48) base 74
p = 73
QR73 = {x * x % p for x in range(1, p)}
assert [r for r in range(p) if (1 - r) % p == r] == [37] and 2 * 37 % p == 1
assert pow(2, 9, p) == 1 and pow(2, 3, p) != 1 and 511 == 7 * p and pow(37, 9, p) == 1 and pow(37, 3, p) != 1
assert [r for r in range(1, p) if pow(r, 3, p) == 1] == [1, 8, 64] == [1, pow(2, 3, p), pow(2, 6, p)]
assert [r for r in range(p) if (r * r - r + 1) % p == 0] == [9, 65] and (1 - 9) % p == 65
assert len({(1 - x) % p for x in QR73} & QR73) == 17
assert 137 % p == 64 and pow(64, 3, p) == 1
assert all(pow(26, 72 // q, p) != 1 for q in (2, 3)) and pow(10, 8, p) == 1 and pow(10, 4, p) != 1

# (49) base 75, (50) the ~ operation
m = 74
assert [d for d in range(2, m) if m % d == 0] == [2, 37]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 37, 38]
assert sorted(x % 37 for x in range(0, m, 2)) == list(range(37)) and 38 % 37 == 1 and 38 % 2 == 0
assert not [r for r in range(m) if (1 - r) % m == r] and [a for a in range(37) if (1 - a) % 37 == a] == [19]
assert len({pow(2, k, m) for k in range(1, 37)}) == 36
assert (37 % 2, 37 % 37) == (1, 0) and 37 * 37 % m == 37
assert 137 % m == 63 and (63 % 2, 63 % 37) == (1, 26)
assert all((63 * x) % m % 37 == 26 * (x % 37) % 37 for x in range(0, m, 2))
_rev = lambda n: int(f"{n:02d}"[::-1])
_pairs = [(12, 11), (11, 21), (23, 22), (22, 32), (34, 33), (33, 43), (45, 44), (44, 54), (56, 55), (55, 65),
          (67, 66), (66, 76), (78, 77), (77, 87), (89, 88), (88, 98), (91, 99), (99, 19)]
_vals = [32, 23, 54, 45, 76, 67, 98, 89, 21, 12, 43, 34, 65, 56, 87, 78, 19, 91]
assert all(_rev((a + b) % 99) == v == 10 * (a + b) % 99 for (a, b), v in zip(_pairs, _vals))
assert all(_rev(n) == 10 * n % 99 for n in range(1, 99)) and 100 % 99 == 1

# (51) base 76, (52) abba/dddd
m = 75
assert [d for d in range(2, m) if m % d == 0] == [3, 5, 15, 25]
assert [x for x in range(m) if pow(x, m, m) == 0] == [0, 15, 30, 45, 60]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 25, 51]
assert [r for r in range(m) if (1 - r) % m == r] == [38]
assert {d: [a for a in range(d) if (1 - a) % d == a] for d in (3, 5, 15, 25)} == {3: [2], 5: [3], 15: [8], 25: [13]}
assert pow(2, 20, m) == 1 and pow(2, 10, m) != 1 and pow(2, 4, m) != 1
assert 26 * 26 % m == 1 and (26 % 3, 26 % 25) == (2, 1)
assert 137 % m == 62 and 62 % 25 == 37 % 25 == 12 and 137 - 37 == 4 * 25
assert all(pow(g, 20, m) == 1 and pow(g, 10, m) != 1 and pow(g, 4, m) != 1 for g in (62, 37))
_P = [1221, 2332, 3223, 4554, 5445, 6556, 7667, 8998, 9119]
assert all(n % 11 == 0 and n % 37 == (2 * (n // 1000) - (n // 100) % 10) % 37 for n in _P)
assert [n for n in _P if n % 37 == 0] == [1221] and 1111 == 30 * 37 + 1
assert all(int(f"{a}{b}{b}{a}") + int(f"{b}{a}{a}{b}") == 1111 * (a + b) for a in range(1, 10) for b in range(1, 10))

# (53) reversal = x10, mirror = x11 in Z/99
_PAL = [1221, 1111, 2332, 2222, 3223, 3333, 4554, 4444, 5445, 5555, 6556, 6666, 7667, 7777, 8998, 8888, 9119, 9999]
_OPS = {x for p in _pairs for x in p}
assert all(n == 100 * (n // 100) + _rev(n // 100) and (n // 100) in _OPS for n in _PAL)
assert all(n % 99 == 11 * (n // 100) % 99 and n % 11 == 0 and dr(n, 10) == dr(2 * (n // 100), 10) for n in _PAL)
assert (10 % 9, 10 % 11) == (1, 10) and (11 % 9, 11 % 11) == (2, 0) and 10 * 10 % 99 == 1 and 11 * 9 % 99 == 0
assert all((100 * h + _rev(h)) % 99 == 11 * h % 99 for h in range(100))

# (54) L-cups
for d in range(1, 9):
    e = d + 1
    assert int(f"{d}{d}{d}") % 37 == 0 and int(f"{d}{e}{d}") % 37 == 10 and int(f"{e}{d}{e}") % 37 == 27
    assert {(10 * d + d) % 11, (10 * d + e) % 11, (10 * e + d) % 11} == {0, 1, 10}
    assert (dr(111 * d, 10), dr(111 * d + 10, 10), dr(111 * d + 101, 10)) == (dr(3 * d, 10), dr(3 * d + 1, 10), dr(3 * d + 2, 10))
assert 121 == 11**2 and 111 == 3 * 37 and 121 % 37 == 10
assert (919 % 37, 191 % 37) == (31, 6)

# (55) base 77, (56) spin combinatorics
m = 76
assert [d for d in range(2, m) if m % d == 0] == [2, 4, 19, 38]
assert [x for x in range(m) if pow(x, m, m) == 0] == [0, 38] and [x for x in range(m) if x * x % m == x] == [0, 1, 20, 57]
assert not [r for r in range(m) if (1 - r) % m == r] and [a for a in range(19) if (1 - a) % 19 == a] == [10]
assert all(pow(2, 18 // q, 19) != 1 for q in (2, 3)) and all((4 * x) % m % 4 == 0 for x in range(m))
assert 37 * 37 == 18 * m + 1 and 137 % m == 61 and pow(61, 9, m) == 1 and pow(61, 3, m) != 1
_ML = [(a, b) for a in range(4) for b in range(4) if a != b]
_orb = lambda confs, grp: len({frozenset(g(c) for g in grp) for c in confs})
_C4 = [lambda c, s=s: ((c[0] + s) % 4, (c[1] + s) % 4) for s in range(4)]
_D4 = _C4 + [lambda c, s=s: (((1 - c[0]) + s) % 4, ((1 - c[1]) + s) % 4) for s in range(4)]
_SW = _C4 + [lambda c, s=s: ((c[1] + s) % 4, (c[0] + s) % 4) for s in range(4)]
assert len(_ML) == 12 and _orb(_ML, _C4) == 3 and _orb(_ML, _D4) == 2 and _orb(_ML, _SW) == 2
assert [(b - a) % 4 for a, b in [(2, 1), (0, 1), (3, 1), (1, 3)]] == [3, 1, 2, 2]
assert len({frozenset((i + s) % 4 for s in range(4)) for i in range(4)}) == 1

# (57) base 78, (58) direction states
m = 77
assert [d for d in range(2, m) if m % d == 0] == [7, 11] and [x for x in range(m) if x * x % m == x] == [0, 1, 22, 56]
assert [r for r in range(m) if (1 - r) % m == r] == [39] and 39 % 7 == 4 and 39 % 11 == 6
assert pow(2, 30, m) == 1 and all(pow(2, 30 // q, m) != 1 for q in (2, 3, 5))
assert (137 % 7, 137 % 11) == (4, 5) and (26 % 7, 26 % 11) == (5, 4)
assert pow(26, 30, m) == 1 and all(pow(26, 30 // q, m) != 1 for q in (2, 3, 5))
_st = lambda a, b: ("E", 0) if a == b else (("U" if b > a else "D"), abs(b - a))
_pp = [(a, b) for a in range(1, 10) for b in range(1, 10)]
assert len({_st(a, b) for a, b in _pp}) == 17 and len({frozenset({p, p[::-1]}) for p in _pp}) == 45
assert (-4) % 9 == 5 and {s: 9 // gcd(s, 9) for s in range(1, 9)} == {1: 9, 2: 9, 3: 3, 4: 9, 5: 9, 6: 3, 7: 9, 8: 9}
assert all((3 * r + c + 1) % 2 == (r + c + 1) % 2 for r in range(3) for c in range(3))

# (59) base 79, (60) audit checks
m = 78
assert [d for d in range(2, m) if m % d == 0] == [2, 3, 6, 13, 26, 39]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 13, 27, 39, 40, 52, 66]
assert not [r for r in range(m) if (1 - r) % m == r]
assert {d: [a for a in range(d) if (1 - a) % d == a] for d in (3, 13, 39)} == {3: [2], 13: [7], 39: [20]}
assert sorted({2 * x % m for x in range(m)}) == list(range(0, m, 2)) and pow(2, 12, 39) == 1 and pow(2, 6, 39) != 1 and pow(2, 4, 39) != 1
assert 137 % m == 59 and all(pow(g, 12, m) == 1 and pow(g, 6, m) != 1 and pow(g, 4, m) != 1 for g in (59, 37))
def _dih(n):
    s = tuple(range(1, n + 1)); seen = {s}; fr = [s]
    while fr:
        t_ = fr.pop()
        for u in (t_[1:] + t_[:1], t_[::-1]):
            if u not in seen:
                seen.add(u); fr.append(u)
    return len(seen)
assert _dih(3) == 6 and _dih(9) == 18
_w = [n for n in range(1, 1000) if n % 10 == 9]
assert len(_w) == 100 and [n for n in _w if dr(n, 10) == 9] == [n for n in range(1, 1000) if n % 90 == 9] and len([n for n in _w if dr(n, 10) == 9]) == 12
assert all(dr(n + 1, 10) == dr(n, 10) % 9 + 1 for n in range(1, 5000))

# (61) base 80, (62) 729-triple boundary test
p = 79
QR79 = {x * x % p for x in range(1, p)}
assert [r for r in range(p) if (1 - r) % p == r] == [40] and len({(1 - x) % p for x in QR79} & QR79) == 19
assert [r for r in range(1, p) if pow(r, 3, p) == 1] == [1, 23, 55] and [r for r in range(p) if (r * r - r + 1) % p == 0] == [24, 56]
assert pow(2, 39, p) == 1 and pow(2, 13, p) != 1 and pow(2, 3, p) != 1
assert all(pow(37, 78 // q, p) != 1 for q in (2, 3, 13)) and pow(10, 13, p) == 1 and pow(26, 39, p) == 1 and pow(26, 13, p) != 1
assert 137 % p == 58 and pow(58, 26, p) == 1 and pow(58, 13, p) != 1 and pow(58, 2, p) != 1
from collections import defaultdict as _dd, Counter as _Ct
_T = [(a, b, c) for a in range(1, 10) for b in range(1, 10) for c in range(1, 10)]
_by = _dd(list)
for a, b, c in _T:
    _by[(b - a, c - b)].append(b)
_mu = _Ct(len(v) for v in _by.values())
assert len(_by) == 217 and [_mu[k] for k in range(1, 10)] == [48, 42, 36, 30, 24, 18, 12, 6, 1]
assert all((a + b + c) % 9 == (3 * (b % 3) + (c - b) - (b - a)) % 9 for a, b, c in _T)
assert [(3 * x) % 9 for x in (1, 3, 5)] == [3, 0, 6]

# (63) base 81
m = 80
assert [d for d in range(2, m) if m % d == 0] == [2, 4, 5, 8, 10, 16, 20, 40]
assert [x for x in range(m) if pow(x, m, m) == 0] == list(range(0, m, 10)) and pow(10, 3, m) == 40 and pow(10, 4, m) == 0
assert [x for x in range(m) if x * x % m == x] == [0, 1, 16, 65]
assert all(pow(u, 4, m) == 1 for u in range(m) if gcd(u, m) == 1)
assert not [r for r in range(m) if (1 - r) % m == r] and [a for a in range(5) if (1 - a) % 5 == a] == [3]
assert all(x * 16 % m in {0, 16, 32, 48, 64} for x in range(m)) and any(x * 8 % m not in {0, 16, 32, 48, 64} for x in range(m))
assert [2 * y % m for y in (16, 32, 64, 48)] == [32, 64, 48, 16]
assert 137 % m == 57 and pow(57, 4, m) == 1 and pow(57, 2, m) != 1 and pow(37, 4, m) == 1 and pow(37, 2, m) != 1
assert all(40 * y % 65 == y for y in range(0, 65, 5))                    # 40 = identity of the island (5) mod 65

# (64) base 82, (65) 405
m = 81
assert [d for d in range(2, m) if m % d == 0] == [3, 9, 27] and sum(pow(x, m, m) == 0 for x in range(m)) == 27
assert pow(3, 4, m) == 0 and pow(3, 3, m) != 0 and [x for x in range(m) if x * x % m == x] == [0, 1]
assert all(pow(2, 54 // q, m) != 1 for q in (2, 3)) and pow(2, 6, 27) != 1
assert [r for r in range(m) if (1 - r) % m == r] == [41] and (41 % 3, 41 % 9, 41 % 27) == (2, 5, 14)
assert all((n % 81) % 9 == n % 9 for n in range(1, 10000))
assert all(pow(g, 9, m) == 1 and pow(g, 3, m) != 1 for g in (37, 10)) and 37 % 9 == 1 and 10 % 9 == 1
assert 137 % m == 56 and all(pow(56, 54 // q, m) != 1 for q in (2, 3)) and pow(26, 6, m) == 1 and pow(26, 3, m) != 1 and pow(26, 2, m) != 1
assert 405 % m == 0 and 405 == 5 * 81 and 405 - 81 == 4 * 81
_M = [9 * sum(j**r for j in range(1, 10)) for r in range(1, 9)]
assert _M == [405, 2565, 18225, 137997, 1087425, 8805645, 72723825, 609581997]
assert [x % 81 for x in _M] == [0, 54, 0, 54, 0, 54, 0, 54]
assert [9 * sum((j - 5)**k for j in range(1, 10)) for k in (2, 4, 6)] == [540, 6372, 88020]
assert 405 % 37 == 35 and all(pow(35, 36 // q, 37) != 1 for q in (2, 3)) and 405 % 79 == 10

# (66) reflection theorem, (67) base 83
from sympy import factorint as _fi
for b in range(4, 202, 2):
    mm = b - 1; rs = (mm + 1) // 2
    for r in range(mm):
        fr = (1 - r) % mm
        assert (fr - rs) % mm == (-(r - rs)) % mm
        for p_, a_ in _fi(mm).items():
            pa = p_**a_
            def _vc(x, p_=p_, a_=a_, pa=pa):
                x %= pa
                if x == 0:
                    return a_
                k = 0
                while x % p_ == 0:
                    x //= p_; k += 1
                return k
            assert _vc(r - rs) == _vc(fr - rs)
_sh = _Ct(min(4, next((k for k in range(5) if ((r - 41) % 81) % 3**(k + 1)), 4)) for r in range(81))
assert [_sh[k] for k in range(5)] == [54, 18, 6, 2, 1]
m = 82
assert [d for d in range(2, m) if m % d == 0] == [2, 41] and [x for x in range(m) if x * x % m == x] == [0, 1, 41, 42]
assert sorted(x % 41 for x in range(0, m, 2)) == list(range(41)) and 42 % 41 == 1
assert not [r for r in range(m) if (1 - r) % m == r] and [a for a in range(41) if (1 - a) % 41 == a] == [21]
assert pow(2, 20, 41) == 1 and pow(2, 10, 41) != 1 and pow(2, 4, 41) != 1
assert 137 % m == 55 and (55 % 2, 55 % 41) == (1, 14) and pow(55, 8, m) == 1 and pow(55, 4, m) != 1
assert pow(37, 5, m) == 1 and 37 * 10 % 41 == 1

# (68) base 84
p = 83
QR83 = {x * x % p for x in range(1, p)}
assert [r for r in range(p) if (1 - r) % p == r] == [42] and len({(1 - x) % p for x in QR83} & QR83) == 20
assert not [r for r in range(p) if (r * r - r + 1) % p == 0] and pow(2, 41, p) != 1 and pow(2, 2, p) != 1
assert all(g in QR83 and pow(g, 41, p) == 1 for g in (26, 37, 10)) and len(QR83) == 41
assert 137 % p == 54 and pow(54, 41, p) != 1 and pow(54, 2, p) != 1

# (69) base 85
m = 84
assert len([d for d in range(2, m) if m % d == 0]) == 10 and [x for x in range(m) if pow(x, m, m) == 0] == [0, 42]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 21, 28, 36, 49, 57, 64]
assert not [r for r in range(m) if (1 - r) % m == r]
assert {d: [a for a in range(d) if (1 - a) % d == a] for d in (3, 7, 21)} == {3: [2], 7: [4], 21: [11]}
assert all(x * 4 % m % 4 == 0 for x in range(m)) and pow(2, 6, 21) == 1 and pow(2, 3, 21) != 1 and pow(2, 2, 21) != 1
assert 37 * 37 % m == 25 and 37 * 25 == 11 * m + 1
assert 137 % m == 53 and pow(53, 6, m) == 1 and pow(53, 3, m) != 1 and pow(53, 2, m) != 1

# (70) base 86
m = 85
assert [d for d in range(2, m) if m % d == 0] == [5, 17] and [x for x in range(m) if x * x % m == x] == [0, 1, 35, 51]
assert [r for r in range(m) if (1 - r) % m == r] == [43] and (43 % 5, 43 % 17) == (3, 9)
assert pow(2, 8, m) == 1 and pow(2, 4, m) != 1
assert 137 % m == 52 and (52 % 5, 52 % 17) == (2, 1) and 136 == 8 * 17 and pow(52, 4, m) == 1 and pow(52, 2, m) != 1
assert (26 % 5, 26 % 17) == (1, 9) and pow(26, 8, m) == 1 and pow(26, 4, m) != 1
assert pow(37, 16, m) == 1 and pow(37, 8, m) != 1

# (71) base 87
m = 86
assert [d for d in range(2, m) if m % d == 0] == [2, 43] and [x for x in range(m) if x * x % m == x] == [0, 1, 43, 44]
assert sorted(x % 43 for x in range(0, m, 2)) == list(range(43)) and 44 % 43 == 1
assert not [r for r in range(m) if (1 - r) % m == r] and [a for a in range(43) if (1 - a) % 43 == a] == [22]
assert pow(2, 14, 43) == 1 and pow(2, 7, 43) != 1 and pow(2, 2, 43) != 1
assert pow(37, 6, m) == 1 and pow(37, 3, m) != 1 and pow(37, 2, m) != 1 and (37 * 37 - 37 + 1) % 43 == 0
assert 137 % m == 51 and 137 % 43 == 8 == 2**3 and pow(51, 14, m) == 1 and pow(51, 7, m) != 1

# (72) base 88
m = 87
assert [d for d in range(2, m) if m % d == 0] == [3, 29] and [x for x in range(m) if x * x % m == x] == [0, 1, 30, 58]
assert [r for r in range(m) if (1 - r) % m == r] == [44] and (44 % 3, 44 % 29) == (2, 15)
assert pow(2, 28, m) == 1 and pow(2, 14, m) != 1 and pow(2, 4, m) != 1
assert 137 % m == 50 and all(pow(g, 28, m) == 1 and pow(g, 14, m) != 1 and pow(g, 4, m) != 1 for g in (50, 26, 37, 10))
assert sum(1 for u in range(m) if gcd(u, m) == 1 and pow(u, 28, m) == 1 and pow(u, 14, m) != 1 and pow(u, 4, m) != 1) == 24

# (73) base 89, (74) the forced lcm test
m = 88
assert [d for d in range(2, m) if m % d == 0] == [2, 4, 8, 11, 22, 44]
assert [x for x in range(m) if pow(x, m, m) == 0] == [0, 22, 44, 66] and pow(22, 2, m) == 44 and pow(22, 3, m) == 0
assert [x for x in range(m) if x * x % m == x] == [0, 1, 33, 56]
assert not [r for r in range(m) if (1 - r) % m == r] and [a for a in range(11) if (1 - a) % 11 == a] == [6]
_C89 = [8, 16, 32, 64, 40, 80, 72, 56, 24, 48]
assert all(_C89[(i + 1) % 10] == 2 * _C89[i] % m for i in range(10)) and all(x * 8 % m % 8 == 0 for x in range(m)) and 56 % 11 == 1
assert 137 % m == 49 and pow(49, 5, m) == 1 and pow(37, 10, m) == 1 and pow(37, 5, m) != 1 and pow(37, 2, m) != 1
def _o(u, mm):
    k, x = 1, u % mm
    while x != 1:
        x = x * u % mm; k += 1
    return k
_els = [u for u in range(85) if gcd(u, 85) == 1 and _o(u % 5, 5) == 4 and _o(u % 17, 17) == 16]
assert len(_els) == 16 and all(_o(u, 85) == 16 for u in _els)

# (75) base 90
p = 89
QR89 = {x * x % p for x in range(1, p)}
assert [r for r in range(p) if (1 - r) % p == r] == [45] and len({(1 - x) % p for x in QR89} & QR89) == 21
assert pow(2, 11, p) == 1 and 2**11 - 1 == 23 * p and not [r for r in range(p) if (r * r - r + 1) % p == 0]
assert 10 * 10 - 10 - 1 == p and [r for r in range(p) if (r * r - r - 1) % p == 0] == [10, 80]
from fractions import Fraction as _Fr
_F = [0, 1]
for _ in range(70):
    _F.append(_F[-1] + _F[-2])
assert abs(sum(_Fr(_F[k], 10**(k + 1)) for k in range(1, 70)) - _Fr(1, 89)) < _Fr(1, 10**50)
assert pow(10, 44, p) == 1 and all(pow(10, 44 // q, p) != 1 for q in (2, 11))
assert next(k for k in range(1, 200) if _F[k] % p == 0 and _F[k + 1] % p == 1) == 44 and _F[11] == 89
assert 137 % p == 48 and all(pow(g, 88 // q, p) != 1 for g in (48, 26) for q in (2, 11)) and pow(37, 8, p) == 1 and pow(37, 4, p) != 1

# (76) the 1212 loop
_seq = [1212, 2112, 2121, 3912, 4812, 5712, 6612, 7512, 8412, 9312, 1212]
assert len(set(_seq)) == 10 and {dr(s, 10) for s in _seq} == {6}
assert all((_seq[i + 1] - _seq[i]) % 9 == 0 for i in range(10))
assert [s % 37 for s in _seq[3:10]] == [27, 2, 14, 26, 1, 13, 25] and 900 % 37 == 12

# (77) base 91
m = 90
assert len([d for d in range(2, m) if m % d == 0]) == 10 and [x for x in range(m) if pow(x, m, m) == 0] == [0, 30, 60]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 10, 36, 45, 46, 55, 81]
assert not [r for r in range(m) if (1 - r) % m == r]
_T10 = list(range(0, m, 10))
assert 10 * 10 % m == 10 and all(10 * x % m == x for x in _T10) and sorted(x % 9 for x in _T10) == list(range(9))
assert [y // 10 for y in (10, 20, 40, 80, 70, 50)] == [1, 2, 4, 8, 7, 5] and all(2 * a % m == b for a, b in [(10, 20), (20, 40), (40, 80), (80, 70), (70, 50), (50, 10), (30, 60), (60, 30)])
assert 137 % m == 47 and pow(47, 12, m) == 1 and pow(47, 6, m) != 1 and pow(47, 4, m) != 1 and pow(37, 4, m) == 1 and pow(37, 2, m) != 1
assert 900 + 9 + 1791 + 6 * 900 - 8100 == 0

# (78) base 92
m = 91
assert [d for d in range(2, m) if m % d == 0] == [7, 13] and [x for x in range(m) if x * x % m == x] == [0, 1, 14, 78]
assert [r for r in range(m) if (1 - r) % m == r] == [46] and 137 % m == 46 == pow(2, -1, m) and 273 % m == 0
assert sum(1 for x in range(m) if gcd(x, m) == 1) == 72 and next(k for k in range(1, 99) if pow(2, k, m) == 1) == 12
assert next(k for k in range(1, 99) if pow(37, k, m) == 1) == 12 and next(k for k in range(1, 99) if pow(10, k, m) == 1) == 6 and gcd(26, m) == 13

# (79) 1212 constructive audit
_inc = [_seq[i + 1] - _seq[i] for i in range(10)]
assert _inc == [900, 9, 1791] + [900] * 6 + [-8100] and gcd(*_inc) == 9
assert [s % 37 for s in _seq[:10]] == [28, 3, 12, 27, 2, 14, 26, 1, 13, 25] and 2 * 28 % 37 != 3
assert [s % 11 for s in _seq[:10]] == [2, 0, 9, 7, 5, 3, 1, 10, 8, 6]
assert min(d for d in range(2, 2000) if d % 2 and next(k for k in range(1, d + 1) if pow(2, k, d) == 1) == 10) == 11 and 1023 == 3 * 11 * 31

# (80) base 93
m = 92
assert [d for d in range(2, m) if m % d == 0] == [2, 4, 23, 46] and [x for x in range(m) if pow(x, m, m) == 0] == [0, 46]
assert [x for x in range(m) if x * x % m == x] == [0, 1, 24, 69] and not [r for r in range(m) if (1 - r) % m == r]
assert {2 * 2 * x % m for x in range(m)} == set(range(0, m, 4)) and 24 * 4 % m == 4 and pow(2, 11, 23) == 1
assert 137 % m == 45 and 45 * 45 % m == 1 and 138 == 6 * 23 and pow(37, 22, m) == 1 and pow(37, 11, m) != 1
assert all(10 * a * 10 * b % 90 == 10 * a * b % 90 for a in range(9) for b in range(9))

# (81) base 94
m = 93
assert [d for d in range(2, m) if m % d == 0] == [3, 31] and [x for x in range(m) if x * x % m == x] == [0, 1, 31, 63]
assert [r for r in range(m) if (1 - r) % m == r] == [47] and sum(1 for x in range(m) if gcd(x, m) == 1) == 60
assert next(k for k in range(1, 99) if pow(2, k, m) == 1) == 10 and pow(2, 5, 31) == 1
_o = lambda x: next(k for k in range(1, 99) if pow(x, k, m) == 1)
assert 137 % m == 44 and _o(44) == 30 and _o(26) == 6 and _o(37) == 6 and _o(10) == 15

# (82) base 95
m = 94
assert [x for x in range(m) if x * x % m == x] == [0, 1, 47, 48] and not [r for r in range(m) if (1 - r) % m == r]
assert {2 * x % m for x in range(m)} == set(range(0, m, 2)) and 48 * 2 % m == 2 and pow(2, 23, 47) == 1
_o = lambda x, n=m: next(k for k in range(1, 99) if pow(x, k, n) == 1)
assert 137 % m == 43 and _o(43) == 46 and _o(37) == 23 and _o(26, 47) == 46 and _o(10, 47) == 46

# (83) base 96
m = 95
assert [x for x in range(m) if x * x % m == x] == [0, 1, 20, 76] and [r for r in range(m) if (1 - r) % m == r] == [48]
_o = lambda x, n=m: next(k for k in range(1, 99) if pow(x, k, n) == 1)
assert _o(2) == 36 and 137 % m == 42 and _o(42) == 36 and _o(26) == 3 and _o(37) == 4 and gcd(10, m) == 5

# (84) base 97
m = 96
assert [x for x in range(m) if x * x % m == x] == [0, 1, 33, 64] and [x for x in range(m) if pow(x, m, m) == 0] == list(range(0, m, 6))
_S = set(range(m))
for _ in range(5):
    _S = {2 * x % m for x in _S}
assert _S == {0, 32, 64} and {2 * x % m for x in _S} == _S and 64 * 64 % m == 64 and not [r for r in range(m) if (1 - r) % m == r]
_o = lambda x, n=m: next(k for k in range(1, 99) if pow(x, k, n) == 1)
assert 137 % m == 41 and _o(41) == 4 and _o(37) == 8 and max(_o(u) for u in range(m) if gcd(u, m) == 1) == 8

# (85) base 98
m = 97
_o = lambda x, n=m: next(k for k in range(1, 99) if pow(x, k, n) == 1)
assert [r for r in range(m) if (1 - r) % m == r] == [49] and _o(2) == 48 and 137 % m == 40
assert all(_o(v) == 96 for v in (40, 26, 37, 10, 5))

if __name__ == "__main__":
    print("T432 carry map + digital-root rings")
    print("  (1) Kummer C_b = (s(x)+s(y)-s(x+y))/(b-1): 20000 random checks, b = 2..40")
    print("  (2) D + d = b^k: carries = k - v_b(D); s(D)+s(d) = 1+(b-1)(k-v); dr sum = b")
    print(f"  {'b':>3} {'n=b-1':>6} {'class':>6} {'|U|':>4} {'U structure':>14} "
          f"{'#idem':>5} {'#nil':>4} {'#zd':>4} {'2^-1':>5}")
    for b, r in TABLE.items():
        ug = "x".join(f"C{x}" for x in r["unit_group"])
        print(f"  {b:>3} {r['n']:>6} {r['kind']:>6} {r['units']:>4} {ug:>14} "
              f"{len(r['idempotents']):>5} {len(r['nilpotents']):>4} {r['zero_divisors']:>4} "
              f"{'yes' if r['two_inv'] else 'no':>5}")
    cls = {}
    for b, r in TABLE.items():
        cls.setdefault(r["kind"], []).append(b)
    for k, v in cls.items():
        print(f"  {k}: bases {v}")
