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
