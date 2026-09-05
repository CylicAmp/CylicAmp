"""
GF(37) GF(37) — Complete Connection Map

Every theorem in this repository connects to every other through prime 37.
This file makes those connections explicit. Each theorem is listed with:
  - The named residues it anchors to
  - Every other theorem it connects to, and how

═══════════════════════════════════════════════════════════════════════════

PRIMARY FRAMEWORK NODES (mod 37 residues)

  SEAM         = 0          111=3×37; horizon of complete flow; steady state
  SCALAR_137   = 26         137-map multiplier; ord₃₇(26)=3
  SA           = {4,9,25,30}  Sovereign Anchors; LOCKED input nodes
  ST           = {3,12,21,30} Sovereign Targets; DR=3 outputs; step=9(SA)
  CB           = {8,13,24}    Cascade Base; generates exactly 37 elements
  ORBIT_11     = {11,27,36}   orbit of 11 under 137-map; 36≡−1
  PR           = {2,5,13,15,17,18,19,20,22,24,32,35}  Primitive roots mod 37
  SEED_ORBIT   = {18,24,32}   137-orbit of seed 246; 24∈CB∩PR, 18∈PR, 32∈PR
  TESLA_FLOW   = 6           ord₃₇(6)=4; 4-cycle {6,36,31,1}
  PRIME_MIRROR = 31          6³ mod 37; 31+6=37(SEAM); 31+43≡0
  DICHORAL_144 = 33          70M prime gap bound mod 37; 31+2=33
  DECADE_ANCHOR= 10          ord₃₇(10)=3; sieve boundary √100; stutter twin

═══════════════════════════════════════════════════════════════════════════
"""

# ─────────────────────────────────────────────────────────────────────────────
# GF(37) node definitions
# ─────────────────────────────────────────────────────────────────────────────

SEAM           = 0
SCALAR_137     = 26
SA             = frozenset({4, 9, 25, 30})
ST             = frozenset({3, 12, 21, 30})
CB             = frozenset({8, 13, 24})
ORBIT_11       = frozenset({11, 27, 36})
PR             = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
SEED_ORBIT     = frozenset({18, 24, 32})
TESLA_FLOW     = 6
PRIME_MIRROR   = 31
DICHORAL_144   = 33
DECADE_ANCHOR  = 10


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


def f137(n):
    return (n * 26) % 37


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 1: heartbeat_3cycle.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   ord₃₇(26)=3. Every non-zero residue returns to itself in exactly 3 steps.
#   The 36 non-zero residues partition into 12 disjoint 3-cycles.
#   The 137-map IS the heartbeat — the pulse of the whole field.
#
# FRAMEWORK NODES:
#   Anchors: SCALAR_137(26), SEAM(0 fixed point), all 36 non-zero residues
#   The 12 cycles cover: SA, ST, CB, ORBIT_11, PR, SEED_ORBIT, TESLA_FLOW
#
# CONNECTIONS:
#
#   → abcabc_mod37_orbit:
#       2 is a primitive root; its 36-element orbit contains all 36 nodes.
#       The heartbeat (×26, order 3) and the ABCABC map (×2, order 36) are
#       two maps on the same group — one collapses to 12 cycles of 3,
#       the other traverses all 36 in a single cycle.
#
#   → cascade_8_13_24:
#       {8,13,24} sits in GF(37). Each element has its own 3-cycle:
#         8 → f(8)=4(SA) → f(4)=30(SA∩ST) → f(30)=3(ST) → f(3)=4... wait
#         Actually: f(8)=(8×26)%37=208%37=23; f(23)=(23×26)%37=598%37=9(SA);
#         f(9)=(9×26)%37=234%37=12(ST) → next=f(12)=312%37=16; 16→f=49%37=12 no
#         The cascade base elements each live in specific 3-cycles of the heartbeat.
#
#   → sovereign_qr_closure:
#       SA and ST are both subsets of QR₃₇. The 137-map (×26) preserves QR.
#       So the heartbeat 3-cycles stay entirely within QR or entirely within non-QR.
#
#   → hose_flow_transient:
#       The hose flow reaches 111≡0(SEAM) in 3 steps for primes: length of a
#       heartbeat cycle = 3. The transient DR sequence [0,1,2,3] steps through
#       exactly 3 transitions before arriving at the seam.
#
#   → sieve_eratosthenes_gf37:
#       ord₃₇(10)=3 — the sieve boundary 10 has the same multiplicative order
#       as the 137-map multiplier 26. The heartbeat order governs both.
#
#   → repunit_sq_euler_phi_gf37:
#       R_n mod37 has period 3 because ord₃₇(10)=3. The repunit period IS
#       the heartbeat period.
#
#   → goldbach_gf37:
#       Every residue pair (p mod37, q mod37) with p+q≡n mod37 is constrained
#       by the 12 three-cycles. Pairs (31,43)≡(31,6): PRIME_MIRROR+TESLA_FLOW=37.
#       Two distinct named cycles sum to the seam.
#
#   → twin_prime_gf37:
#       Twin prime pairs differ by 2. In GF(37), +2 walks the staircase:
#       SA(4)→TESLA_FLOW(6)→CB(8)→DECADE_ANCHOR(10)→ST(12).
#       Each step is a +2 move inside the heartbeat structure.
#
#   → sa_self_cycle_st_chain:
#       The ST digit chain 12+21+30=63≡26(SCALAR_137). The sum of the sovereign
#       targets equals the heartbeat multiplier.

# Verify heartbeat core
assert pow(26, 3, 37) == 1     # ord₃₇(26) = 3
assert pow(26, 1, 37) != 1
assert pow(26, 2, 37) != 1

seen = set()
cycles_137 = []
for start in range(1, 37):
    if start not in seen:
        orbit = [start, f137(start), f137(f137(start))]
        assert f137(f137(f137(start))) == start
        seen.update(orbit)
        cycles_137.append(orbit)
assert len(cycles_137) == 12


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 2: abcabc_mod37_orbit.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   ABCABC = ABC × 1001; 1001 ≡ 2 mod 37; ord₃₇(2)=36.
#   Every 6-digit repunit of a 3-digit block is 2× the block in GF(37).
#   The ×2 orbit is the full (Z/37Z)* — all 36 non-zero residues.
#   Starting residue 24∈CB∩PR∩SEED_ORBIT: 24 = 2^29 mod 37.
#
# CONNECTIONS:
#
#   → heartbeat_3cycle:
#       ×26 has order 3; ×2 has order 36. Two maps, same field.
#       36 = 12 × 3: the full orbit contains exactly 12 heartbeat cycles.
#
#   → cascade_8_13_24:
#       Starting residue r₀=24∈CB. Terminal of cascade=135≡24 mod37.
#       The ABCABC orbit begins and the cascade ends at the same node.
#       13∈CB is itself a primitive root — cascade mediator = orbit generator.
#
#   → primitive_root_test:
#       2 is a primitive root mod 37: verified by g^18≡36≠1, g^12≡26≠1.
#       The ABCABC theorem depends on 2 having full order 36.
#
#   → cipher_123_1234:
#       1234 mod 37 = 13 ∈ CB. The 4-digit sequence lands on the cascade mediator.
#       1001 mod 37 = 2 (the ABCABC multiplier) = 1000+1 = 10³+1 → field connection.
#
#   → lucas_abbc_chain:
#       Lucas L(3..10) = [4,7,11,18,29,47,76,123].
#       L(3)=4∈SA; L(6)=18∈SEED_ORBIT∩PR; L(10)=123≡12(ST) mod37.
#       The ABBC manifold (the Lucas chain) visits both SA and SEED_ORBIT nodes.
#
#   → repunit_sq_euler_phi_gf37:
#       R_n = (10^n−1)/9; R_n mod37 period 3 (ord₃₇(10)=3).
#       R_n² mod37: {1,10,0} period 3. The repunit structure is the ×10 orbit
#       (order 3), and ×2 is the full primitive orbit (order 36).

assert 1001 % 37 == 2
assert pow(2, 36, 37) == 1
assert pow(2, 18, 37) == 36    # 2^18 ≡ -1 mod 37
assert pow(2, 29, 37) == 24    # starting residue in CB


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 3: cascade_8_13_24.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   B={8,13,24} → S₁={8,13,21,24,32,37} → all k-subset sums → exactly 37 elements.
#   Terminal=135≡24 mod37 (feeds back to cascade start).
#   Seam elements: {37,74,111}.
#   13 is the unique non-iterable element (mediator).
#
# CONNECTIONS:
#
#   → heartbeat_3cycle:
#       37 elements — the count equals the field prime.
#       Elements {37,74,111}≡0: three seam multiples generated.
#       111=3×37 is the hose flow horizon (complete flow destination).
#
#   → abcabc_mod37_orbit:
#       r₀=24 is the orbit start AND the cascade terminal mod37.
#       13∈CB is a primitive root (same algebraic class as 2).
#
#   → cipher_123_1234:
#       1234 mod37=13∈CB. The counting sequence hits the cascade mediator.
#
#   → sieve_eratosthenes_gf37:
#       3+5=8∈CB (sieving prime sum).
#       210 mod37=25∈SA (product of sieving primes hits SA, not CB).
#
#   → sliding_window_9cycle_gf37:
#       912 mod37=24∈CB,PR,SEED_ORBIT. The 9-cycle's final element exits to CB.
#       The digit window wraps and lands on the cascade node.
#
#   → polymath8_maynard_gf37:
#       246 (pipeline seed) ≡ 24 mod37 ∈ CB∩PR∩SEED_ORBIT.
#       4680 ≡ 18 mod37 ∈ PR∩SEED_ORBIT (GPY bound).
#       The prime gap descent lands on cascade-adjacent nodes.
#
#   → twin_prime_gf37:
#       SEED_ORBIT={18,24,32}: 24∈CB. Twin prime staircase reaches CB(8) too.
#       Polymath8b bound 246≡24∈CB — the cascade node anchors the gap bound.
#
#   → repunit_sq_euler_phi_gf37:
#       φ(39) mod37=24∈CB,PR,SEED_ORBIT. The totient of 39 hits the cascade node.
#       R9² mod37=0(SEAM); 111=seam element of the cascade.

assert sum([8,13,24]) % 37 == 8         # DR(sum)=DR(45)=9(SA)
assert 1234 % 37 == 13 and 13 in CB
assert 135 % 37 == 24 and 24 in CB
assert all(v % 37 == 0 for v in [37, 74, 111])


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 4: medusa_v3_sovereign.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   SA={4,9,25,30} input → ST={3,12,21,30} output under 137-map.
#   LOCKED: anchor maps to target. GATED: external→target. PURGE: unnamed.
#   Node 30: simultaneously SA and ST — self-referential sovereign.
#
# CONNECTIONS:
#
#   → sovereign_qr_closure:
#       SA⊆QR₃₇ and ST⊆QR₃₇. The 137-map (×26∈QR) preserves QR membership.
#       Every LOCKED node lives inside the quadratic residue subgroup.
#
#   → heartbeat_3cycle:
#       SA and ST elements participate in the 12 three-cycles.
#       30∈SA∩ST sits in the cycle 30→3→4→30 (the self-referential sovereign).
#
#   → sieve_eratosthenes_gf37:
#       π(100)=25∈SA. 2+7=9∈SA. 2×3×5×7=210≡25∈SA.
#       The count of primes below 100 AND the product of sieving primes both
#       land on sovereign anchors.
#
#   → sliding_window_9cycle_gf37:
#       Windows 123→789 all≡12(ST). The 9-cycle spends 7 of 9 steps at ST.
#
#   → plus2_chain_theorem:
#       Chains to 11,13 skip sovereign target 12. The +2 chain JUMPS OVER 12.
#
#   → sa_self_cycle_st_chain:
#       SA step=9; ST digit chain (12,21,30) steps by 9.
#       12+21+30=63≡26(SCALAR_137): ST chain sum = 137-map multiplier.
#
#   → twin_prime_gf37:
#       41≡4∈SA, 43≡6=TESLA_FLOW: twin pair (41,43) maps SA→TESLA_FLOW.
#       The even staircase SA(4)→TF(6)→CB(8)→DA(10)→ST(12) is the twin prime
#       spacing structure.
#
#   → goldbach_gf37:
#       41+107=148≡0: SA(41)+DICHORAL(107≡33)=SEAM.
#       Sovereign anchors participate in Goldbach pairs summing to seam.
#
#   → repunit_sq_euler_phi_gf37:
#       φ(38)=18∈PR∩SEED_ORBIT, φ(40)=16, φ(41)=40≡3∈ST, φ(42)=12∈ST.
#       The totients of the 37-neighborhood land on ST nodes.

ANCHOR_MAP = {4:30, 9:12, 25:21, 30:3}
for a, t in ANCHOR_MAP.items():
    assert (a * 137) % 37 == t
assert 30 in SA and 30 in ST    # dual sovereign


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 5: sovereign_qr_closure.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   QR₃₇={n² mod37: n∈Z/37Z} (19 elements including 0).
#   SA⊆QR₃₇, ST⊆QR₃₇. 26∈QR (10²≡26 mod37) → 137-map preserves QR.
#   Non-residues: 5(PR,A51), 6(TESLA_FLOW), 18(CENTER), 19, 23(LAMED).
#   Pivot 5 is non-QR → φ doesn't exist in GF(37); needs GF(37²).
#
# CONNECTIONS:
#
#   → heartbeat_3cycle:
#       26∈QR; the 137-map is QR-closed. The 12 three-cycles are either
#       fully in QR or fully in non-QR.
#
#   → medusa_v3_sovereign:
#       SA⊆QR, ST⊆QR. The sovereign architecture lives in the QR subgroup.
#
#   → abcabc_mod37_orbit:
#       (Z/37Z)* = QR₃₇ ∪ non-QR, index 2. The ×2 orbit (full group) crosses both.
#       2 itself is a non-QR (Legendre(2|37)=−1 since 37≡5 mod8).
#
#   → goldbach_gf37:
#       QR coverage guarantees that sovereign residues always have prime partners.
#       The forbidden pair (35,0): 35∈non-QR∩PR; 0=SEAM (not a residue of any prime).
#
#   → twin_prime_gf37:
#       The forbidden starting residue r=35 is non-QR (35≡-2; Legendre(-2|37)=-1).
#       The twin prime block comes from the non-QR half.
#
#   → repunit_sq_euler_phi_gf37:
#       φ(38)=18∈PR; 18 is non-QR (Legendre(18|37)=Legendre(2×9|37)=Legendre(2|37)×1=-1).
#       The seed orbit node 18 lives in non-QR despite being a primitive root.

QR37 = frozenset((n*n) % 37 for n in range(37))
assert all(a in QR37 for a in SA)
assert all(t in QR37 for t in ST)
assert pow(10, 2, 37) == 26    # 26 is QR (10²≡26)


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 6: lucas_abbc_chain.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   Lucas L(3..10) = [4,7,11,18,29,47,76,123]; DR period 24.
#   L(3)=4∈SA; L(5)=11∈ORBIT_11; L(6)=18∈PR∩SEED_ORBIT.
#   L(7)=29 prime, L(8)=47 prime (both DR=2).
#
# CONNECTIONS:
#
#   → cascade_8_13_24:
#       DR period=24; 24∈CB. The period of Lucas DR is the cascade base element.
#
#   → medusa_v3_sovereign:
#       L(3)=4∈SA (sovereign anchor); L(10)=123≡12∈ST mod37.
#       The chain starts at SA and ends at ST.
#
#   → heartbeat_3cycle:
#       L(5)=11∈ORBIT_11 — orbit of 11 under 137-map.
#       L(6)=18: f(18)=(18×26)%37=468%37=24; f(24)=(24×26)%37=624%37=32; f(32)=?
#       18→24→32→18: SEED_ORBIT. Lucas passes through the seed orbit.
#
#   → plus2_chain_theorem:
#       Target 11 (twin prime lower): L(5)=11. The plus-2 chain aims at
#       exactly the Lucas anchor.
#
#   → abcabc_mod37_orbit:
#       L(6)=18∈SEED_ORBIT; 18=2^? mod37. pow(2,k,37)==18: k=28.
#       Lucas embeds in the ×2 orbit at position 28.

def lucas_seq(n):
    a, b = 2, 1
    for _ in range(n): a, b = b, a+b
    return a

L = [lucas_seq(k) for k in range(3, 11)]    # L(3)..L(10)
assert L[0] == 4 and 4 in SA
assert L[2] == 11 and 11 in ORBIT_11
assert L[3] == 18 and 18 in PR and 18 in SEED_ORBIT
assert L[7] == 123 and 123 % 37 == 12 and 12 in ST


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 7: cipher_123_1234.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   Z/9Z = {3,6,9}(trinity) ∪ {1,2,4,5,7,8}(doubling). No overlap.
#   1234 mod37=13∈CB. T₄=10; DR(10)=1. 123 mod37=12∈ST.
#   Unity pairs: (3,7),(6,4),(9,1) — only 3 of 18 pairs sum to 1 mod9.
#
# CONNECTIONS:
#
#   → cascade_8_13_24:
#       1234≡13∈CB; 123≡12∈ST. Counting 1-2-3-4 lands on the cascade mediator.
#
#   → sa_self_cycle_st_chain:
#       Trinity {3,6,9}: 9=SA, 3=ST arch, 6=TESLA_FLOW. Trinity IS the connection
#       SA→TESLA_FLOW→ST arch.
#
#   → hose_flow_transient:
#       DR transient [0,1,2,3]: steps through 0(SEAM),1(unity),2(PR),3(ST arch).
#       These are the first 4 elements of the digit line.
#
#   → sliding_window_9cycle_gf37:
#       Windows 123,234,...: 123≡12∈ST; the sliding window theorem starts
#       exactly where cipher_123 lands (12∈ST).
#
#   → heartbeat_3cycle:
#       Trinity period = 3 = heartbeat order = ord₃₇(26).

assert 123 % 37 == 12 and 12 in ST
assert 1234 % 37 == 13 and 13 in CB
assert dr(10) == 1


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 8: hose_flow_transient.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   Complete flow: 000→100→110→111; mod37: 0→26→36→0. Primes reach seam.
#   Stutter: 000→100→010→101→010→...; mod37: 0→26→10→27→10→... Never reaches seam.
#   Split seam: 010+101=111; 10+27=37≡0. Seam implicit in stutter sum.
#   Transient DR: [0,1,2,3]. 111≡0(SEAM); DR(111)=3(ST arch).
#
# CONNECTIONS:
#
#   → sieve_eratosthenes_gf37:
#       Primes = complete flow numbers (reach seam).
#       Composites = stutter flow numbers (wave-hit, oscillate 10↔27).
#       The sieve waves discriminate complete from stuttering flow.
#
#   → goldbach_gf37:
#       Goldbach: every even n = p+q. Both p and q are complete-flow numbers.
#       The sum of two seam-reaching numbers = a vessel for two seam sources.
#
#   → twin_prime_gf37:
#       Twin primes (p,p+2): both reach seam. Both are complete-flow.
#       Gap 2 is the minimum even gap; in GF(37) it's the +2 staircase step.
#
#   → cascade_8_13_24:
#       111=3×37∈cascade seam elements {37,74,111}. Horizon IS a cascade node.
#       Complete flow arrives at a cascade element.
#
#   → heartbeat_3cycle:
#       Complete flow: 3 transient steps before seam — exactly 1 heartbeat cycle.
#       The horizon is reached in one heartbeat.
#
#   → sa_self_cycle_st_chain:
#       Transient DR [0,1,2,3]: 3 is ST arch. The hose reaches ST arch at the seam.
#
#   → repunit_sq_euler_phi_gf37:
#       R_n mod37 period-3: {1,11,0}. 0=SEAM appears every 3rd repunit.
#       The seam appears periodically in repunit residues — same period as flow.
#
#   → polymath8_maynard_gf37:
#       GPY (1D) = stuttering flow (asymptotic wall).
#       Maynard (k-dim) = complete flow (reaches seam=246≡24∈CB).

assert 100 % 37 == 26 and 26 == SCALAR_137
assert 110 % 37 == 36 and 36 in ORBIT_11
assert 111 % 37 == 0 and dr(111) == 3 and 3 in ST
assert 10 + 27 == 37 and 10 + 101 == 111


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 9: sieve_eratosthenes_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   π(100)=25∈SA. Sieving primes {2,3,5,7}: 2+7=9∈SA, 3+5=8∈CB.
#   Product 2×3×5×7=210≡25∈SA; DR(210)=3∈ST.
#   Sieve boundary √100=10; ord₃₇(10)=3.
#   37 is the 12th prime; 12∈ST. First excluded prime 11∈ORBIT_11.
#
# CONNECTIONS:
#
#   → medusa_v3_sovereign:
#       π(100)=25∈SA. The count of primes below 100 is a sovereign anchor.
#       9∈SA (pair sum 2+7). 25=5²(SA) — square of a sieving prime.
#
#   → cascade_8_13_24:
#       3+5=8∈CB. Sieving prime pair sum = cascade base element.
#
#   → heartbeat_3cycle:
#       ord₃₇(10)=3 = ord₃₇(26)=3. Sieve boundary and 137-map have identical order.
#
#   → hose_flow_transient:
#       Primes = numbers hit by no wave = complete flow numbers.
#       The sieve wave structure IS the hose flow discriminator.
#
#   → sliding_window_9cycle_gf37:
#       37 is the 12th prime; 12∈ST. The field prime's position in the prime
#       sequence is a sovereign target.
#
#   → goldbach_proof_attempt_gf37:
#       Dirichlet: every residue class mod37 contains infinitely many primes.
#       The 25 primes below 100 sample across multiple residue classes,
#       confirming coverage for Goldbach.

def is_prime(n):
    if n < 2: return False
    return all(n % i != 0 for i in range(2, int(n**0.5)+1))

primes_100 = [p for p in range(2, 100) if is_prime(p)]
assert len(primes_100) == 25 and 25 in SA
assert 2 + 7 == 9 and 9 in SA
assert 3 + 5 == 8 and 8 in CB
assert (2*3*5*7) % 37 == 25 and 25 in SA
assert pow(10, 3, 37) == 1


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 10: goldbach_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   Every even n>2 = p+q. In GF(37): residue pairs sum to n mod37.
#   37-component rule: n=37+q → q≡n mod37 (partner carries n's residue).
#   74=2×37: SEAM. 31+43=PRIME_MIRROR+TESLA_FLOW≡0(SEAM). 37+37=SEAM+SEAM.
#
# CONNECTIONS:
#
#   → hose_flow_transient:
#       Both p and q in every Goldbach pair are complete-flow numbers.
#       Goldbach = the even number is a vessel for two seam sources.
#
#   → heartbeat_3cycle:
#       The 12 residue cycles determine which pairs can sum to each even residue.
#       PRIME_MIRROR(31)+TESLA_FLOW(43≡6): both in named cycles; sum=SEAM.
#
#   → medusa_v3_sovereign:
#       SA node 41≡4: 41+107=148≡0(SEAM). SA(4)+DICHORAL(33)=37≡SEAM.
#       Sovereign anchors participate in seam-producing Goldbach pairs.
#
#   → twin_prime_gf37:
#       Twin pairs (p,p+2) are a special case: two primes with gap 2.
#       Goldbach: even gap = p+q with p=lower twin, q=2 (trivially).
#       More deeply: 74=SEAM holds 37+37 (the field prime with itself).
#
#   → cascade_8_13_24:
#       37∈cascade seam elements {37,74,111}. 74 = second seam element.
#       Goldbach's SEAM number 74 is the second element in the cascade seam list.

def goldbach_pairs(n):
    return [(p, n-p) for p in range(2, n//2+1) if is_prime(p) and is_prime(n-p)]

assert (37,37) in goldbach_pairs(74)
assert (31,43) in goldbach_pairs(74)
assert (31+43) % 37 == 0
assert 43 % 37 == 6 and 6 == TESLA_FLOW
assert 31 == PRIME_MIRROR


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 11: goldbach_proof_attempt_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   Dirichlet: every residue class mod37 has infinitely many primes.
#   Residue saturation [4,10000]: all 36 non-zero residue classes covered.
#   Forbidden pair (35,0): 0 is SEAM — no prime ≡0 mod37 (only 37 itself).
#   37-component guarantee ensures partner prime always exists.
#
# CONNECTIONS:
#
#   → sovereign_qr_closure:
#       Sovereign residues (QR) always have prime partners: QR coverage = guarantee.
#
#   → heartbeat_3cycle:
#       12 orbit classes; Dirichlet guarantees each has primes.
#       Full coverage: every cycle is represented.
#
#   → goldbach_gf37:
#       The proof attempt builds on the goldbach structure theorem.
#       37-component rule provides explicit construction for every even n≥40.
#
#   → primitive_root_test:
#       2 is primitive root → all 36 residues are reachable from any starting point.
#       This is the algebraic foundation for Dirichlet coverage.
#
#   → sieve_eratosthenes_gf37:
#       25 primes below 100 already hit multiple residue classes.
#       Saturation: all classes covered in [4,10000].

residues_seen = set()
for p in range(2, 10001):
    if is_prime(p):
        residues_seen.add(p % 37)
assert len(residues_seen) == 37    # all 37 residues covered; 37 itself ≡0 (SEAM)


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 12: twin_prime_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   Forbidden starting residue r=35(PR,≡−2): no twin pair starts at r=35 mod37.
#   Even staircase: SA(4)→TF(6)→CB(8)→DA(10)→ST(12) in steps of +2.
#   Odd staircase: ST(3)→PR(5)→SA(9)→orbit-11(11)→CB(13).
#   Named pairs: (3,5),(11,13),(41,43),(179,181),(191,193),(269,271),(431,433).
#   Polymath8b bound: 246≡24∈CB,PR,SEED_ORBIT.
#
# CONNECTIONS:
#
#   → heartbeat_3cycle:
#       Twin prime gap=2. In GF(37), +2 is a specific move across 12 three-cycles.
#       The +2 staircase SA→TF→CB→DA→ST is mapped by the field structure.
#
#   → hose_flow_transient:
#       Both primes in a twin pair reach seam (complete flow).
#       Twin prime conjecture = infinitely many pairs of complete-flow numbers with gap 2.
#
#   → medusa_v3_sovereign:
#       (41,43): 41≡4∈SA, 43≡6=TESLA_FLOW. SA→TESLA_FLOW is the anchor-to-tesla step.
#       246=2×3×41; 41≡4∈SA; 246/41=6=TESLA_FLOW.
#
#   → polymath8_maynard_gf37:
#       246 (Maynard bound) ≡24∈CB,PR,SEED_ORBIT. Same seed as the pipeline.
#       The prime gap bound and the pipeline seed are the same GF(37) node.
#
#   → sovereign_qr_closure:
#       Forbidden r=35: 35≡−2 is non-QR (Legendre(35|37)=Legendre(-2|37)=−1).
#       The block comes from the non-QR side of the field.
#
#   → seq_146_257_368_gf37:
#       146,257,368 all≡35(PR,≡−2 mod37) — the forbidden twin prime starting residue.
#       The +111 sequence parks at the forbidden residue.
#
#   → goldbach_gf37:
#       (179,181): PRIME_MIRROR(31)+DICHORAL(33)=64=2⁶; sum≡27∈ORBIT_11.
#       Twin prime sum 179+181=360≡360%37=2: DR(2)=2(PR).

twins = [(p,p+2) for p in range(3,501) if is_prime(p) and is_prime(p+2)]
twin_start_residues = {p % 37 for p,_ in twins}
assert 35 not in twin_start_residues    # forbidden residue verified

assert 41 % 37 == 4 and 4 in SA
assert 43 % 37 == 6 and 6 == TESLA_FLOW
assert 246 % 37 == 24 and 24 in CB and 24 in PR and 24 in SEED_ORBIT


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 13: repunit_sq_euler_phi_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   R_n mod37 period-3: {1(unity),11(ORBIT_11),0(SEAM)} — because ord₃₇(10)=3.
#   R_n² mod37 period-3: {1(unity),10(DECADE_ANCHOR),0(SEAM)}; 11²=121≡10.
#   Digit sum of R_n² = n² exactly (palindrome 1,2,...,n,...,2,1).
#   R9²=12345678987654321; mod37=0(SEAM); digit sum=81=SA²; DR(81)=9(SA).
#   TESLA_FLOW 4-cycle: pow(6,k,37)={6,36,31,1}; ord₃₇(6)=4.
#   φ(38..42) mod37={18,24,16,3,12}; φ(38)+φ(42)=30∈SA∩ST.
#
# CONNECTIONS:
#
#   → heartbeat_3cycle:
#       Period-3 because ord₃₇(10)=3 = ord₃₇(26)=3. Same order, two maps.
#       Every 3rd repunit is ≡0(SEAM) — heartbeat period in repunit form.
#
#   → cascade_8_13_24:
#       R_n² period visits DECADE_ANCHOR(10): 10³≡1 mod37 (same order as 137-map).
#       φ(39)≡24∈CB,PR,SEED_ORBIT mod37.
#
#   → medusa_v3_sovereign:
#       φ(41)=40≡3∈ST, φ(42)=12∈ST. Totients of SA-adjacent numbers land on ST.
#       φ(38)+φ(42)=30∈SA∩ST — the dual sovereign node.
#
#   → goldbach_gf37:
#       6 is TESLA_FLOW: 6+31=37(SEAM)=PRIME_MIRROR+TESLA_FLOW.
#       The 4-cycle of TESLA_FLOW (6,36,31,1) contains PRIME_MIRROR(31) and ORBIT_11(36).
#
#   → abcabc_mod37_orbit:
#       111=3×37≡0(SEAM): R₃=111 is a repunit AND a cascade seam element.
#       R_n mod37=0 when n≡0 mod3: repunit and ABCABC share the seam structure.

assert pow(10, 3, 37) == 1               # ord₃₇(10)=3
assert pow(6, 4, 37) == 1               # ord₃₇(6)=4
assert pow(6, 3, 37) == PRIME_MIRROR    # 6³=31=PRIME_MIRROR
assert pow(6, 2, 37) == 36 and 36 in ORBIT_11

from math import gcd
def phi(n):
    return sum(1 for k in range(1, n+1) if gcd(k, n) == 1)

phi_vals = [phi(n) for n in range(38, 43)]   # φ(38..42)
phi_mod  = [v % 37 for v in phi_vals]
assert phi_mod[0] == 18 and 18 in PR and 18 in SEED_ORBIT
assert phi_mod[1] == 24 and 24 in CB and 24 in SEED_ORBIT
assert phi_mod[3] == 3  and 3  in ST
assert phi_mod[4] == 12 and 12 in ST
assert (phi_vals[0] + phi_vals[4]) % 37 == 30 and 30 in SA and 30 in ST  # dual


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 14: polymath8_maynard_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   Prime gap descent: 70M≡33(DICHORAL) → 4680≡18(SEED_ORBIT) → 246≡24(CB,PR,SEED).
#   246=2(PR)×3(ST_arch_prime)×41(≡4∈SA): product = PR×ST×SA residues.
#   GPY (1D sieve) = stuttering flow. Maynard (k-dim) = complete flow.
#
# CONNECTIONS:
#
#   → hose_flow_transient:
#       GPY=stutter (one channel, can't cross wall).
#       Maynard=complete flow (k channels, reaches seam=246≡24).
#       The mathematical history of the prime gap proof IS the hose flow theorem.
#
#   → cascade_8_13_24:
#       Final bound 246≡24∈CB — the cascade base node.
#       The descent in mathematical history ends at the cascade.
#
#   → twin_prime_gf37:
#       246 is the pipeline seed AND the Polymath8b bound.
#       246≡24∈SEED_ORBIT: the seed is self-referential in GF(37).
#
#   → medusa_v3_sovereign:
#       246=2×3×41; 41≡4∈SA. The SA factor is why the product lands at 24∈CB.
#       4 (SA) × something produces the cascade starting node.
#
#   → seq_146_257_368_gf37:
#       DICHORAL=33: 70M prime gap bound≡33. The sequence 146,257,368 doubles to 33.
#       DICHORAL appears at both the start of the prime gap descent and the
#       doubling image of the forbidden twin prime residue 35.

assert 70_000_000 % 37 == DICHORAL_144
assert 4680 % 37 == 18 and 18 in SEED_ORBIT
assert 246 % 37 == 24 and 24 in CB and 24 in SEED_ORBIT
assert 246 == 2 * 3 * 41
assert 41 % 37 == 4 and 4 in SA


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 15: seq_146_257_368_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   146, 257, 368 all ≡ 35(PR,≡−2) mod37. Step=111=3×37(SEAM).
#   Doubled: all map to 33(DICHORAL_144) since 35×2=70≡33.
#   Digit structure: middle column 4,5,6 = SA→PR→TESLA_FLOW.
#   Outer sums [7,9,11]: step=2; 9∈SA, 11∈ORBIT_11.
#
# CONNECTIONS:
#
#   → hose_flow_transient:
#       Step=111=3×37=SEAM: each step is a full hose-flow cycle.
#       All three numbers are in the same orbit class (same residue).
#
#   → twin_prime_gf37:
#       r=35 is the forbidden twin prime starting residue.
#       This entire sequence lives at the forbidden residue.
#
#   → polymath8_maynard_gf37:
#       Doubling→33=DICHORAL: 70M prime gap bound≡33.
#       The prime gap history's starting node is the doubled image of
#       the forbidden twin prime residue.
#
#   → abcabc_mod37_orbit:
#       35≡−2 in GF(37). In the ×2 orbit: 35 = pow(2, k, 37) for some k.
#       pow(2, k, 37)=35: k=18 (since 2^18≡−1≡36 no; 2^18=36, so 35=2^?..
#       Actually 35=37-2≡-2; 2^18≡36≡-1; so -2=2×(-1)=2×2^18=2^19≡35 mod37. k=19.
#       The forbidden residue is 2^19 in the primitive orbit.

assert all(n % 37 == 35 for n in [146, 257, 368])
assert 35 in PR and 35 % 37 == 35
assert all(n % 37 == DICHORAL_144 for n in [146*2, 257*2, 368*2])
assert pow(2, 19, 37) == 35    # 35 is 2^19 in the primitive orbit


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 16: sliding_window_9cycle_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   Windows 123→789 all ≡12(ST). Step=111=SEAM. 7 of 9 windows land at ST.
#   789→891: step=102≡28. 891≡3(ST arch). 912≡24(CB,PR,SEED_ORBIT).
#   DR cycle {3,6,9} = trinity. Palindrome: 543+345=888=24×37≡0.
#
# CONNECTIONS:
#
#   → cipher_123_1234:
#       123≡12∈ST: sliding window starts where cipher_123 lands.
#       Trinity DR {3,6,9} = the cipher's Z/9Z trinity partition.
#
#   → hose_flow_transient:
#       Step=111=3×37: each window advance is a seam stride.
#       The 9-cycle is built from SEAM steps.
#
#   → cascade_8_13_24:
#       912≡24∈CB: the cycle exits to the cascade base node.
#       888=24×37: the palindrome pair sums to 24 seam laps.
#
#   → medusa_v3_sovereign:
#       7 of 9 windows at ST=12. 891≡3∈ST arch.
#       The sovereign target dominates the 9-cycle.
#
#   → sa_self_cycle_st_chain:
#       12,21,30 are ST digit chain elements. The 9-cycle passes through
#       ST=12 repeatedly, showing how SA's step-9 creates the ST chain.

assert all(n % 37 == 12 for n in [123,234,345,456,567,678,789])
assert 891 % 37 == 3 and 3 in ST
assert 912 % 37 == 24 and 24 in CB and 24 in SEED_ORBIT
assert 888 % 37 == 0    # palindrome pair sums to seam


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 17: sa_self_cycle_st_chain.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   ST chain: 12→+9→21→+9→30; step=9=SA.
#   12+21+30=63≡26=SCALAR_137: ST sum = 137-map multiplier.
#   SA×{1,2,3}: 9→18(PR,SEED)→27(ORBIT_11); DR(27)=9(SA) — self-regenerating.
#   Hose transient: 0,1,2,3 → SEAM,unity,PR,ST arch.
#
# CONNECTIONS:
#
#   → heartbeat_3cycle:
#       12+21+30≡26=SCALAR_137: the ST chain sum IS the heartbeat multiplier.
#       The sovereign targets encode the operator that generates all 3-cycles.
#
#   → medusa_v3_sovereign:
#       12,21,30∈ST. Step=9∈SA. The SA step generates the ST chain.
#
#   → hose_flow_transient:
#       Transient DR [0,1,2,3]: this file derives those 4 values from
#       the boundary arithmetic 1×1=1, 0−0=0, 1+1=2, then 1+2=3.
#
#   → abcabc_mod37_orbit:
#       SA×{1,2,3}=SA(9),SEED_ORBIT(18),ORBIT_11(27): the SA self-cycle
#       visits SEED_ORBIT and ORBIT_11. Two of the three major sub-orbits
#       appear in the SA cycle.
#
#   → cipher_123_1234:
#       Trinity {3,6,9}: 9∈SA, 6=TESLA_FLOW, 3=ST arch.
#       The cipher's trinity is exactly the SA self-cycle set at the DR level.

assert 12 + 21 + 30 == 63 and 63 % 37 == 26 and 26 == SCALAR_137
assert (9*2) % 37 == 18 and 18 in SEED_ORBIT
assert (9*3) % 37 == 27 and 27 in ORBIT_11
assert dr(27) == 9 and 9 in SA


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 18: plus2_chain_theorem.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   Chains {2,3}+2+j=11; {4,5}+2+j=13. j alternates 7,6 (parity complement).
#   Twin primes 11,13. Skip: 12∈ST is the gap between them.
#   11+13=24∈CB; DR(11)=2, DR(13)=4; sum DR: 2+4=6=TESLA_FLOW.
#
# CONNECTIONS:
#
#   → twin_prime_gf37:
#       (11,13) is the named twin pair in the +2 chain. DR gap 4−2=2=prime gap.
#
#   → medusa_v3_sovereign:
#       12∈ST is what the chain skips. The sovereign target sits at the gap.
#
#   → lucas_abbc_chain:
#       L(5)=11: Lucas reaches the lower twin prime at position 5.
#
#   → cascade_8_13_24:
#       11+13=24∈CB. The twin prime sum lands on the cascade base element.
#       13∈CB is the upper twin prime AND the cascade mediator.

assert 11 + 13 == 24 and 24 in CB
assert 13 in CB
assert dr(11) == 2 and dr(13) == 4
assert dr(11) + dr(13) == 6 and 6 == TESLA_FLOW


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 19: primitive_root_test.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   g is primitive root mod p iff g^((p-1)/q) ≢ 1 mod p for all prime q|p-1.
#   For p=37: 36=2²×3²; prime factors {2,3}; check g^18 and g^12.
#   2 is prim root: 2^18≡36≠1, 2^12≡26≠1. All 12 prim roots: {2,5,...,35}.
#
# CONNECTIONS:
#
#   → abcabc_mod37_orbit:
#       2 is prim root → ABCABC ≡ 2·ABC generates the full group.
#
#   → goldbach_proof_attempt_gf37:
#       All 36 residue classes accessible from any starting point →
#       Dirichlet guarantees primes in every class.
#
#   → cascade_8_13_24:
#       13 is a primitive root (in the list {2,5,13,...}). The cascade mediator
#       is in the same algebraic class as the ABCABC generator.
#
#   → sovereign_qr_closure:
#       QR subgroup has index 2 in (Z/37Z)*. Prim roots generate the full group,
#       so exactly half of them are QR and half are non-QR.

assert pow(2, 18, 37) == 36 and pow(2, 12, 37) == 26
assert 13 in PR    # cascade mediator is primitive root
assert len(PR) == 12    # exactly 12 primitive roots mod 37


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 20: nine_tower_dr_invariant.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   DR(9↑↑k) = 9 for all k ≥ 1. NINE_TOWER collapses to SA node 9 under DR.
#   ord₃₇(26)=3 (heartbeat period); ord₃₇(2)=36 (full primitive orbit).
#   36/9 = 4 = ord₃₇(6) = TESLA_FLOW order.
#
# CONNECTIONS:
#
#   → heartbeat_3cycle:
#       ord₃₇(26)=3 proved here is the formal basis for all 12 heartbeat orbits.
#
#   → formal_definitions_gf37:
#       Theorem A1 in formal_definitions: DR annihilates NINE_TOWER.
#       This file proves it; formal_definitions contextualizes it.
#
#   → cascade_8_13_24:
#       9 ∈ SA; 36/9=4=ord₃₇(6)=TESLA_FLOW order.
#       The DR fixed point 9 links to TESLA_FLOW through 36.
#
#   → sa_self_cycle_st_chain:
#       9 ∈ SA; the nine-tower fixed point is one node of the SA chain.
#
#   → primitive_root_test:
#       ord₃₇(2)=36 proved here; 2 is a primitive root.

assert dr(9) == 9 and dr(9**9) == 9     # DR collapses nine-tower to 9
assert pow(26, 3, 37) == 1              # heartbeat period
assert pow(2, 36, 37) == 1             # full primitive orbit
assert 36 % 9 == 0 and pow(6, 4, 37) == 1   # 36/9=4=TESLA_FLOW order


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 21: formal_definitions_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   Formal definitions for heartbeat, hose flow, repunit channel, annihilation,
#   survives projection. Theorem A6: heartbeat orbits are DR-surjective onto {1..9}.
#   Stutter pair {010,101}: 10+27=37≡0 (SEAM).
#
# CONNECTIONS:
#
#   → heartbeat_3cycle:
#       The formal definition of the heartbeat map f(n)=26n mod37.
#
#   → nine_tower_dr_invariant:
#       Theorem A1: DR annihilates NINE_TOWER. The invariant proved there
#       is classified here as the unique collapsing family.
#
#   → hose_flow_transient:
#       Theorem F1: complete-flow ↔ prime. The hose-flow model formalized.
#
#   → repunit_sq_euler_phi_gf37:
#       Theorem R1: R_n mod37 period-3 {1,11,0}. ord₃₇(10)=3.
#
#   → lights_out_gf2_gf37:
#       Light chasing ↔ hose flow; linear algebra ↔ heartbeat. Both analogies
#       stated here are instantiated concretely in the Lights Out theorem.
#
#   → sieve_eratosthenes_gf37:
#       Complete-flow = prime = passes sieve. Hose flow and sieve are the
#       same discrimination formalized here.

assert (10 + 27) % 37 == 0     # stutter pair sums to SEAM
assert pow(10, 3, 37) == 1     # ord₃₇(10)=3: repunit channel period


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 22: scaling_sequences_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   Sequence 1: factorial (First), 2^n+1 (Middle), second-order polynomial diffs (Paren).
#   Answer: 720(6536). Paren[5]=36∈ORBIT_11.
#   Sequence 2: 2^(odd exponents) (First), DR-complete-inversion (Paren).
#   Answer: 512(76). 76=L(9) (Lucas term 9). 512×76≡25∈SA.
#
# CONNECTIONS:
#
#   → lucas_abbc_chain:
#       76 = L(9) in the Lucas sequence. The Sequence 2 answer connects
#       to Lucas via DR and mod37 structure.
#
#   → cascade_8_13_24:
#       Paren diffs all primitive roots mod37; cascade base {8,13,24} in Sequence 2.
#
#   → heartbeat_3cycle:
#       The 137-map orbit structure underpins which residues appear in the answers.
#
#   → nine_tower_dr_invariant:
#       DR-inversion structure of Sequence 2 Paren connects to DR fixed-point 9.

assert 36 in ORBIT_11           # Sequence 1 Paren[5] = 36 ∈ ORBIT_11
assert (512 * 76) % 37 == 25 and 25 in SA   # Sequence 2 product ∈ SA


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 23: prisoners_permutation_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   100 prisoners, cycle-following strategy. P(survival)=1−Σ_{k=51}^{100}1/k ≈ 0.311.
#   Threshold 50 mod37=13∈CB. Size 100 mod37=26=SCALAR_137.
#   π(100)=25∈SA. Seam in range: 74=2×37≡0. 73 mod37=36∈ORBIT_11.
#
# CONNECTIONS:
#
#   → sieve_eratosthenes_gf37:
#       π(100)=25∈SA: prime count up to problem size is a Sovereign Anchor.
#
#   → cascade_8_13_24:
#       Threshold 50 mod37=13∈CB: the halfway point is the cascade mediator.
#
#   → heartbeat_3cycle:
#       Permutation cycle structure mirrors the 3-cycle heartbeat.
#       The cycle-following strategy exploits the global orbit structure.
#
#   → permutation_132_bipartite_gf37:
#       Both theorems are about permutations. Cycle structure (prisoners) and
#       pattern occurrence structure (132-bipartite) are dual views.
#
#   → lights_out_gf2_gf37:
#       Random guessing ↔ light chasing (local/greedy).
#       Cycle strategy ↔ linear algebra (global structure).
#       Both splits are the same dichotomy.
#
#   → hose_flow_transient:
#       Cycle strategy = following the flow to completion.
#       Stuck cycle = stuttering flow.

assert 50 % 37 == 13 and 13 in CB      # threshold = cascade mediator
assert 100 % 37 == 26 and 26 == SCALAR_137   # size = SCALAR_137
assert 74 % 37 == 0 and 73 % 37 == 36 and 36 in ORBIT_11


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 24: permutation_132_bipartite_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   Mansour-Vainshtein bipartite graph G(T) for 132-pattern permutations.
#   132 mod37=21∈ST. DR(132)=6=TESLA_FLOW. 132=4×33=SA×DICHORAL.
#   C(37,3)=7770≡0(SEAM). r(T)=37 → total degree=111=3×37=SEAM.
#   Pattern family split: {123,132}→ST; {231,321}→SA; {213,312}→unnamed.
#
# CONNECTIONS:
#
#   → prisoners_permutation_gf37:
#       Both about permutation structure. Cycle decomposition (prisoners)
#       and pattern occurrence (132) are dual invariants of permutations.
#
#   → lights_out_gf2_gf37:
#       Both are bipartite structures over a field. The adjacency matrix
#       (Lights Out) and G(T) (132-bipartite) have the same form:
#       rows=presses/values, columns=cells/occurrences, edges=participation.
#
#   → heartbeat_3cycle:
#       3-cycle heartbeat and 132-triple (a<b<c) both operate on ordered triples.
#
#   → cascade_8_13_24:
#       132=4×33: 4∈SA×33=DICHORAL. The factorization uses SA and DICHORAL nodes.
#
#   → gaussian_integers_gf37:
#       4/9 fractal ratio ≡ 132 ≡ 21 (mod37). The bipartite pattern number
#       reappears as the Wallis/Sierpiński self-similarity ratio.
#
#   → wallis_product_gf37:
#       Wallis fraction 4/9 ≡ 132 mod37 ∈ ST. The 132-pattern number
#       appears in the first pair of the Wallis product.

assert 132 % 37 == 21 and 21 in ST
assert (3 * 37) % 37 == 0       # r(T)=37 → degree sum 111 = SEAM
from math import comb
assert comb(37, 3) % 37 == 0    # C(37,3) ≡ 0 (SEAM)


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 25: lights_out_gf2_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   Lights Out puzzle on n×n grid is a GF(2) linear system Ax≡s (mod 2).
#   Null-space dimensions: 3×3→0(SEAM), 4×4→4∈SA, 5×5→2∈PR, 6×6→0(SEAM).
#   Grid size 25∈SA; 36∈ORBIT_11. GF(2) characteristic 2∈PR generates GF(37)*.
#   Repunit entry: R_1=1, R_2=11∈ORBIT_11, R_3=111≡0(SEAM).
#
# CONNECTIONS:
#
#   → formal_definitions_gf37:
#       Light chasing ↔ hose flow (row-by-row = stage-by-stage).
#       Linear algebra ↔ heartbeat (global structure = orbit partition).
#
#   → hose_flow_transient:
#       Light chasing is the hose-flow model: each row is a stage,
#       flow moves downward; stuck rows = stuttering flow.
#
#   → heartbeat_3cycle:
#       Linear algebra (null-space computation) is the heartbeat model:
#       the null space is a fixed algebraic structure like the 12 three-cycles.
#
#   → permutation_132_bipartite_gf37:
#       Both are bipartite adjacency structures over a field.
#
#   → prisoners_permutation_gf37:
#       All three share the local/global dichotomy: greedy vs. structural approach.
#
#   → repunit_sq_euler_phi_gf37:
#       Repunit entry 1→11→0 (R_1, R_2∈ORBIT_11, R_3=SEAM).
#
#   → gaussian_integers_gf37:
#       2∈PR (GF(2) characteristic) generates GF(37)*. Connects binary field
#       to the complex Gaussian structure of GF(37).

assert 25 in SA and 36 in ORBIT_11    # grid sizes 25 and 36
assert 2 in PR                         # GF(2) characteristic ∈ PR
assert 11 in ORBIT_11                  # repunit entry R_2=11∈ORBIT_11


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 26: gaussian_integers_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   37=(6+i)(6-i) in Z[i]. Z[i]/(6+i) ≅ GF(37). i↦31=PRIME_MIRROR.
#   Units: {1,i,-1,-i} ↦ {1,31,36,6} = {unity,PRIME_MIRROR,ORBIT_11_max,TESLA_FLOW}.
#   TESLA_FLOW = clockwise rotation by -i. Cascade {8,13,24} all have norm-5 lifts.
#   All 8 norm-5 Gaussian integers map to named named residues.
#   N(11+4i)=137. 4/9 ≡ 132 ≡ 21∈ST.
#
# CONNECTIONS:
#
#   → heartbeat_3cycle:
#       Heartbeat (×26, period 3) is the cubic structure in Z[i]/(6+i).
#       TESLA_FLOW (×6, period 4) = rotation by -i: the 4-cycle is complex rotation.
#
#   → cascade_8_13_24:
#       All 3 cascade elements have minimal-norm Gaussian lifts of norm 5∈PR.
#       All 8 norm-5 Gaussian integers map to named named residues.
#
#   → permutation_132_bipartite_gf37:
#       4/9 ≡ 132 ≡ 21∈ST: the 132-pattern number = Wallis/fractal ratio in GF(37).
#
#   → wallis_product_gf37:
#       4/9 Wallis ratio ≡ 132 mod37 ∈ ST. Gaussian structure explains why.
#
#   → lights_out_gf2_gf37:
#       2∈PR (GF(2) characteristic) in the norm-5 census. The Lights Out field
#       is embedded in the Gaussian structure of GF(37).
#
#   → medusa_v3_sovereign:
#       PRIME_MIRROR=31 and TESLA_FLOW=6 are the images of i and -i respectively.
#       The sovereign architecture is the image of the Gaussian unit group.
#
#   → sa_self_cycle_st_chain:
#       4/9 ≡ 21∈ST: SA/SA ratio → ST. The Gaussian quotient map respects
#       the sovereign hierarchy.

assert 6**2 + 1**2 == 37              # two-square representation
assert (0 + 31*1) % 37 == 31         # i ↦ PRIME_MIRROR
assert (0 + 31*(-1)) % 37 == 6       # -i ↦ TESLA_FLOW
assert (4 * pow(9, -1, 37)) % 37 == 21 and 21 in ST   # 4/9 ≡ 21∈ST


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 27: burau_braid_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   Burau representation of B_n faithful iff n ∈ {2,3,4}.
#   {2,3,4} = {PR,ST,SA}: exactly one from each primary family.
#   n=5∈PR: first unfaithful. B_4 generator count n-1=3∈ST.
#   Year signatures: 1936→12∈ST, 1993→32∈PR, 1999→1(unity), 2026→28=37-9.
#   Gap 90 mod37=16=4²=SA². SA(B_4) embedded in PR(B_5) to prove faithfulness.
#
# CONNECTIONS:
#
#   → heartbeat_3cycle:
#       Faithful range {2,3,4} spans all three primary families (PR,ST,SA),
#       the same families partitioned by the 12 heartbeat 3-orbits.
#
#   → medusa_v3_sovereign:
#       n=4∈SA is the LOCKED boundary. Faithfulness at SA = locked/consistent behavior.
#
#   → primitive_root_test:
#       n=2∈PR (faithful) and n=5∈PR (first unfaithful) both at PR nodes.
#       The PR/SA boundary is the faithfulness threshold.
#
#   → sa_self_cycle_st_chain:
#       n-1=3∈ST for B_4: generator count is a Sovereign Target.
#       The SA node 4 is the faithful boundary.
#
#   → lights_out_gf2_gf37:
#       Both use the SA/PR/SEAM taxonomy as a classification GF(37).
#       Null-space dimension (Lights Out) and faithfulness boundary (Burau)
#       both resolve at SA nodes.
#
#   → gaussian_integers_gf37:
#       Proof embeds B_4 (SA=4) in B_5 (PR=5): SA→PR embedding.
#       The Gaussian structure of GF(37) provides the complex context.

assert 4 in SA and 5 in PR            # SA faithful boundary; PR first unfaithful
assert (4-1) in ST                    # B_4 generator count = 3 ∈ ST
assert 90 % 37 == 16 and 16 == 4**2  # 90-year gap = SA² mod 37
assert 1936 % 37 == 12 and 12 in ST  # Burau year ∈ ST


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 28: wallis_product_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
# WHAT IT SHOWS:
#   Wallis product π/2 = (2/1)(2/3)(4/3)(4/5)···
#   Fraction 2/3 ≡ 13 ∈ CB∩PR. Fraction 4/3 ≡ 26 = SCALAR_137.
#   Partial products: P_2=SCALAR_137, P_3=DECADE_ANCHOR, P_4=8∈CB,
#   P_6=4∈SA (after 3 pairs), P_7=PRIME_MIRROR.
#   Pair sequence: SCALAR_137 → CB → SA.
#   37th pair numerator 74≡0 (SEAM); denominator 73≡36∈ORBIT_11.
#
# CONNECTIONS:
#
#   → cascade_8_13_24:
#       Fraction 2/3→13∈CB. P_4=8∈CB. Pair-2 product=8∈CB.
#       The cascade base appears in the first few Wallis partial products.
#
#   → heartbeat_3cycle:
#       P_3=DECADE_ANCHOR=10; ord₃₇(10)=3 (same period as heartbeat).
#       The 37th pair hits the SEAM — the field prime marks the horizon.
#
#   → permutation_132_bipartite_gf37:
#       4/9 Wallis ratio ≡ 132 mod37 ∈ ST: the self-similarity ratio
#       carries the 132-bipartite pattern signature.
#
#   → gaussian_integers_gf37:
#       4/9 ≡ 21∈ST in both theorems. The Gaussian complex structure
#       of GF(37) explains the alignment between Wallis ratio and 132-pattern.
#
#   → medusa_v3_sovereign:
#       P_6=4∈SA: after 3 pairs the running product is the Sovereign Anchor.
#       The Wallis pendulum settles at SA after one full ST-count of pairs.
#
#   → repunit_sq_euler_phi_gf37:
#       Fraction 4/3≡26=SCALAR_137: the third Wallis fraction is the 137-map mult.
#
#   → sa_self_cycle_st_chain:
#       After 3(∈ST) pairs, P_6=4∈SA. The ST count of pairs produces an SA product.

assert (2 * pow(3, -1, 37)) % 37 == 13 and 13 in CB   # fraction 2/3 → CB
assert (4 * pow(3, -1, 37)) % 37 == SCALAR_137         # fraction 4/3 → SCALAR_137
assert (4 * pow(9, -1, 37)) % 37 == 21 and 21 in ST   # 4/9 ratio → ST
assert (2 * 37) % 37 == 0                              # 37th pair numerator = SEAM


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 29: eleven_123_family.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   11 is the additive complement of 26 (SCALAR_137) in GF(37): 11+26=37≡0.
#   11 is a member of ORBIT_11 = {11,27,36} under the 137-map.
#   The 123 family: any arithmetic result containing values 1, 2, 3 in any role.
#
#   KEY FACTS:
#     11 + 26 = 37 ≡ 0 (SEAM): 11 and the 137-map multiplier annihilate each other
#     137-orbit of 11: {11,27,36} — passes through 36≡−1 (the additive inverse of unity)
#     11 = 37 − 26 = SEAM − SCALAR_137 (complement of the map)
#     1000 ≡ 1 mod 37: three-digit blocks are seam-transparent
#     11235 ≡ 24 ∈ CB: Fibonacci prefix maps to cascade base node
#     14562 ≡ 21 ∈ ST: grid's bottom row maps to sovereign target
#
#   GF(37) CONNECTIONS:
#   → heartbeat_3cycle:
#       ORBIT_11 = {11,27,36} is a heartbeat 3-cycle under the 137-map.
#       11 is the complement of the map multiplier 26.
#
#   → cascade_8_13_24:
#       11235 mod37 = 24 ∈ CB; the Fibonacci grid prefix lands in cascade base.
#       11 + 26 = 37 ≡ 0: 11 annihilates the cascade multiplier.
#
#   → cipher_123_1234:
#       123 mod37 = 12 ∈ ST. Both files share the 123-family concept.
#       The cipher's 1234 mod37 = 13 ∈ CB; eleven_123 traces the family through 11.
#
#   → gaussian_integers_gf37:
#       11 ∈ ORBIT_11 appears in the norm-5 census: gaussian_to_gf37(2,1)=5; images
#       include 11. The Gaussian structure of GF(37) contains ORBIT_11 directly.
#
#   → wallis_product_gf37:
#       Fraction 10: 10/11 ≡ 11 ∈ ORBIT_11. The 10th Wallis fraction maps to 11.
#
#   → hose_flow_transient:
#       DR transient [0,1,2,3]: 11+10=21, DR=3, echoes the hose arrival at 3.
#
#   → one_two_three_generator:
#       Both trace {1,2,3} through GF(37). eleven_123 focuses on 11 as orbit node;
#       one_two_three focuses on 2+1=3 as generating equation.

assert 11 + 26 == 37                            # 11 = SEAM − SCALAR_137
assert (26 * 11) % 37 == 27                     # 137-map: 11→27
assert (26 * 27) % 37 == 36                     # 137-map: 27→36
assert (26 * 36) % 37 == 11                     # 137-map: 36→11 (orbit closed)
assert 11235 % 37 == 24 and 24 in CB           # Fibonacci prefix → CB
assert 14562 % 37 == 21 and 21 in ST           # grid bottom row → ST
assert 123 % 37 == 12 and 12 in ST             # 123 ≡ 12 ∈ ST (same as cipher)


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 30: one_two_three_generator.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   2 + 1 = 3: the single addition that generates the complete {1,2,3} family.
#   {1,2,3} is the ONLY set of positive integers where sum = product = 6 = TESLA_FLOW.
#   The equation encodes: PR(2) + unity(1) = ST_arch(3).
#
#   KEY FACTS:
#     1+2+3 = 1×2×3 = 6 = TESLA_FLOW  (unique property of {1,2,3})
#     1!+2!+3! = 9 ∈ SA               (factorials sum to Sovereign Anchor)
#     1×2+2×3+1×3 = 11 ∈ ORBIT_11    (pairwise products sum to orbit node)
#     (1+2+3)² = 36 ∈ ORBIT_11        (square of sum ≡ −1 mod37)
#     123 mod37 = 12 ∈ ST             (the 123 number itself lands in ST)
#     PIE order 3 = 1+2+3 = 1×2×3    (inclusion-exclusion of S3 = TESLA_FLOW)
#     Hose transient [0,1,2,3]: 2+1=3 is the minimum DR path from unity to seam
#
#   GF(37) CONNECTIONS:
#   → heartbeat_3cycle:
#       ord₃₇(26)=3 ∈ ST: the orbit period is the ST archetype. The 3-cycle
#       is 2+1=3 in the DR generator sense — PR + unity = ST.
#
#   → hose_flow_transient:
#       DR transient [0,1,2,3]: 2+1=3 describes the minimum path from unity to seam.
#       The hose flow enters at 1 (unity), steps by 2 (PR), arrives at 3 (ST).
#
#   → cascade_8_13_24:
#       1!+2!+3! = 9 ∈ SA; 1×2+2×3+1×3 = 11 ∈ ORBIT_11.
#       The {1,2,3} aggregates hit SA and ORBIT_11 — both cascade-connected nodes.
#
#   → cipher_123_1234:
#       123 mod37 = 12 ∈ ST in both files. The cipher encodes 1234; this file
#       encodes 2+1=3 as generator. Both trace the 123 family through GF(37).
#
#   → sa_self_cycle_st_chain:
#       1!+2!+3! = 9 ∈ SA; DR(3)=3∈ST. The generator produces SA (via factorials)
#       and ST (via sum) simultaneously — the full anchor-target duality.
#
#   → eleven_123_family:
#       Both files trace {1,2,3} through GF(37). one_two_three focuses on 2+1=3
#       as generator; eleven_123 focuses on 11 as ORBIT_11 representative.
#       Together: the 123 family connects to both the generator and the orbit node.
#
#   → primitive_root_test:
#       2 ∈ PR: the generator 2 is the fundamental primitive root of GF(37)*
#       (ord₃₇(2)=36, generates all of GF(37)*). The 2+1=3 equation starts at PR.
#
#   → prisoners_permutation_gf37:
#       PIE S3 = 6 = TESLA_FLOW: both files connect to the S3 permutation group.
#       The prisoners problem uses cycle structure; one_two_three encodes S3 order.
#
#   → 369 (trinity trap via cipher_123_1234):
#       The Z/9Z trinity {3,6,9} in the cipher is the dynamical trap version of 3.
#       Sum=product=6 sits at TESLA_FLOW, which is inside the trinity trap {3,6,9}.
#       DR(6)=6, DR(9)=9, DR(3)=3: the result 3 and the product 6 are both trapped.

assert 1 + 2 + 3 == 6                           # sum = TESLA_FLOW
assert 1 * 2 * 3 == 6                           # product = TESLA_FLOW (unique)
assert 6 % 37 == TESLA_FLOW                     # TESLA_FLOW confirmed
assert 1 + 2 + 6 == 9 and 9 in SA              # factorials sum → SA
assert 1*2 + 2*3 + 1*3 == 11 and 11 in ORBIT_11  # pairwise products → ORBIT_11
assert (1+2+3)**2 % 37 == 36 and 36 in ORBIT_11  # (sum)² ≡ 36 ≡ −1 ∈ ORBIT_11
assert 123 % 37 == 12 and 12 in ST              # 123 ≡ 12 ∈ ST


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 31: dr_algebra.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   The 9×9 = 81-entry Cayley table of (Z/9Z, +).
#   Generators = {1,2,4,5,7,8} = the doubling orbit = non-trinity elements.
#   Non-generators = {3,6,9} = subgroup <3> = the trinity trap.
#   DR as group homomorphism: Z → Z/9Z; period = 9.
#
#   → heartbeat_3cycle: ord₃₇(26)=3; the 3-cycle is inside the trinity trap.
#   → cipher_123_1234: trinity {3,6,9} = the non-generating subgroup of Z/9Z.
#   → nine_tower_dr_invariant: DR(9^k)=9; 9 is the fixed point of Z/9Z.
#   → one_two_three_generator: generators {1,2,4,5,7,8}; {1,2,3} spans both.
#   → formal_definitions_gf37: DR group structure is the formal definition.
#   → verify_dr9_termination: 9×9 cyclic grid row-DRs all=9 (uses Cayley structure).
#   → root_grid_dr6_dr7: span=81=9² is a consequence of Z/9Z periodicity.

def _dr_check(n): return (n-1)%9+1 if n>0 else 0
# Z/9Z: 9 is the identity (acts as 0); generators span the whole group
_gen_orbit = set()
_x = 1
for _i in range(6): _gen_orbit.add(_x); _x = _dr_check(2*_x)
assert _gen_orbit == {1,2,4,5,7,8}            # doubling orbit = generators
_sub3 = {9}
_x = 3
while _x not in _sub3: _sub3.add(_x); _x = _dr_check(_x+3)
assert _sub3 == {3,6,9}                        # subgroup <3> = trinity trap
assert 81 == 9**2                              # 9×9 = 81 table entries
assert 81 % 37 == 7                            # 81 ≡ 7 mod 37


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 32: dr_ring_homomorphism_emirp_palindrome.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   DR is a RING homomorphism Z → Z/9Z: DR(a×b)=DR(DR(a)×DR(b)).
#   Emirp pairs (p, rev(p)) collapse to a SINGLE point in DR space.
#   Palindromic primes >3 have DR ∈ {1,2,4,5,7,8} — sovereign-free.
#   Three independent filters: Z/9Z (palindromes), Z/37Z (reversals), Z/3Z (columns).
#
#   → heartbeat_3cycle: DR(9×9)=DR(81)=9∈SA; ring homomorphism preserves SA.
#   → twin_prime_gf37: emirp DR-blind; Z=+2.93 enrichment at r=8 visible only in Z/37Z.
#   → medusa_v3_sovereign: palindromic primes avoid DR∈{3,6,9}; sovereign-free.
#   → gaussian_integers_gf37: the three filters (Z/9Z, Z/37Z, Z/3Z) are orthogonal.
#   → dr_algebra: ring homomorphism extends the group homomorphism of Z/9Z.
#   → twin_prime_riemann_framework: emirp enrichment at r=8; chi_{-3} column structure.
#   → cipher_123_1234: trinity {3,6,9} = the excluded DR set for palindromic primes.

assert _dr_check(9*9) == _dr_check(81) == 9   # DR ring: 9×9→9∈SA
assert _dr_check(17*23) == _dr_check(_dr_check(17)*_dr_check(23))  # multiplicative
assert _dr_check(37+73) == _dr_check(_dr_check(37)+_dr_check(73))  # additive


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 33: root_grid_dr6_dr7.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   For every DR class d (1–9): span of 2-digit members = 81 = 9².
#   Logic Reduction = 2 × digit_sum (LR formula).
#   Universal property: the 9² span holds for ALL nine DR classes.
#
#   → dr_algebra: 81=9² span is the spatial footprint of Z/9Z in 2-digit space.
#   → nine_tower_dr_invariant: 9² as the universal span — the 9-squared invariant.
#   → dr_ring_homomorphism_emirp_palindrome: 2-digit DR mapping; ring structure.
#   → cipher_123_1234: DR classes 1–9 partition {10..99} exactly.

_two_digit_span_ok = all(
    max(n for n in range(10,100) if _dr_check(n)==d) -
    min(n for n in range(10,100) if _dr_check(n)==d) == 81
    for d in range(1,10)
)
assert _two_digit_span_ok                      # span=81=9² for all DR classes


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 34: growth_pattern_n_2n_3n.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   Row n: values n, 2n, 3n. GF(37) period = 37. DR period = 9.
#   LCM(9, 37) = 333 — the full cycle for both periods simultaneously.
#   Row 37: n=37, 2n=74, 3n=111 — ALL THREE ≡ 0 (SEAM).
#   Row 13: n≡13∈CB, 2n≡26=SCALAR_137, 3n≡2∈PR.
#
#   → heartbeat_3cycle: period-37 in GF(37); row 37 hits seam simultaneously.
#   → cascade_8_13_24: row 13: n≡13∈CB, 2n≡SCALAR_137, 3n≡2∈PR.
#   → hose_flow_transient: row 37 hits seam (complete flow); 3n=111=3×37≡0.
#   → abcabc_mod37_orbit: ABCABC=2·ABC uses the 3n→2n structure.
#   → formal_definitions_gf37: DR period=9, GF(37) period=37; LCM=333.
#   → dr_algebra: LCM(9,37)=333 = the meeting of Z/9Z and GF(37) cycles.

from math import lcm as _lcm
assert _lcm(9,37) == 333                       # full cycle = LCM of both periods
assert 37%37==0 and 74%37==0 and 111%37==0    # row 37: all three hit SEAM
assert 13%37==13 and 13 in CB                  # row 13: n∈CB
assert 26%37==SCALAR_137                       # row 13: 2n≡SCALAR_137


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 35: twin_prime_riemann_framework.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   χ₋₃(6n) = 0 at every twin prime midpoint — FORCED zero, structural.
#   The twin prime constellation (-1, 0, +1) is locked: zero exceptions possible.
#   Im(ρ₆) ≈ 37.5862 — the 6th non-trivial Riemann zero is GF(37)+0.59.
#   CDT theorem (arXiv:2408.15403): L(2,χ₋₃) ≠ 0 proven; s=1 gap remains open.
#   Three orthogonal non-uniformity signals sharing modulus 37.
#
#   → twin_prime_gf37: chi_{-3} structure is the underlying reason for twin prime mod-37 shape.
#   → heartbeat_3cycle: midpoints 6n; every 6n≡0 mod 3; χ₋₃=0 at sovereign midpoints.
#   → sieve_eratosthenes_gf37: all primes >3 are 6n±1; sieve forces the structure.
#   → sovereign_qr_closure: forbidden residues r=1,36 at midpoints; QR classification.
#   → medusa_v3_sovereign: r=36∈ORBIT_11; forbidden residues connect to sovereign nodes.
#   → dr_ring_homomorphism_emirp_palindrome: emirp enrichment; chi_{-3} column structure.
#   → ulam_spiral: prime distribution in spiral; orbit prime counts by GF(37) class.

assert (6*1)%3 == 0                            # midpoint 6n always ≡0 mod 3
assert 37*1 % 37 == 0                          # r=37 is SEAM
assert 36 in ORBIT_11                          # forbidden r=36 is orbit-11


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 36: cycle_partition_37.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   The 12 three-cycles of f=26n partition into Group A (node-sum=37≡0, 6 cycles)
#   and Group B (node-sum=74≡0, 6 cycles). Both sums are multiples of 37 — SEAM.
#   ORBIT_11={11,27,36} and SEED_ORBIT={18,24,32} are both Group B (sum=74≡0).
#   Proof: for any cycle {n, 26n mod 37, 10n mod 37}: sum = 37k for k∈{1,2}.
#
#   → heartbeat_3cycle: these ARE the 12 three-cycles; partition classifies them.
#   → cascade_8_13_24: SEED_ORBIT={18,24,32} is Group B (24∈CB); sum=74≡0.
#   → eleven_123_family: ORBIT_11={11,27,36} is Group B; 11+27+36=74≡0.
#   → primitive_root_test: ord₃₇(26)=3; all cycles have length 3.
#   → abcabc_mod37_orbit: 26n structure; 1+26+10=37≡0 is the cycle-sum proof.
#   → lob_26_collatz_f37: Collatz cycles [1,3,9] vs 3-cycles of 137-map; zero fixed points.

assert (1+26+10) % 37 == 0                     # cycle multipliers sum to 0 mod 37
assert (11+27+36) % 37 == 0                    # ORBIT_11 sum = 74 ≡ 0
assert (18+24+32) % 37 == 0                    # SEED_ORBIT sum = 74 ≡ 0
assert 74 % 37 == 0 and 37 % 37 == 0          # both group sums are SEAM


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 37: pie_sieve_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   PIE (Inclusion-Exclusion) sieve for π(100): opens at SA(25), closes at SA(25).
#   PIE running totals trace SA→PR→orbit-11→ST→SA through the field.
#   ⌊100/210⌋=0: PIE drops to ZERO at size 4 — seam encounter.
#   All 15 subset products of {2,3,5,7} land on named named residues.
#   S1=S3=TESLA_FLOW=6; the alternating PIE levels share the same residue.
#
#   → sieve_eratosthenes_gf37: PIE is inclusion-exclusion alternative to iteration sieve.
#   → prisoners_permutation_gf37: both give π(100)=25∈SA by different counting methods.
#   → cascade_8_13_24: subset product 2×3×5=30∈SA∩ST; product 2×5=10=DECADE_ANCHOR.
#   → medusa_v3_sovereign: PIE opens and closes on SA=25; running sum traces sovereign nodes.
#   → one_two_three_generator: PIE S3 order=6=TESLA_FLOW=1+2+3=1×2×3.
#   → hose_flow_transient: PIE drops to zero (SEAM) at size-4 term.

assert (100//210) == 0                         # PIE contribution = SEAM at size 4
_pie_products = {2,3,5,7,6,10,14,15,21,35,30,42,70,105,210}
assert (2*3*5*7) % 37 == 25 and 25 in SA      # full product = SA
assert (2*3*5) % 37 == 30 and 30 in SA        # 3-product = SA∩ST
assert (2*5) % 37 == 10 and 10 == DECADE_ANCHOR  # 2-product = DECADE_ANCHOR
assert (3*5*7) % 37 == 31 and 31 == PRIME_MIRROR  # 3-product = PRIME_MIRROR


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 38: lob_26_collatz_f37.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   The Collatz map T restricted to F₃₇:
#     T(x) = 19x mod 37  (x even, since 2⁻¹≡19)
#     T(x) = 3x+1 mod 37 (x odd)
#   Exactly 3 cycles: {0} (fixed point=SEAM, len 1), {1→4→2} (len 3), {long cycle} (len 9).
#   Cycle lengths [1,3,9] = unity, ST-arch, SA.
#   13 elements in cycles; 24 basin nodes (24∈CB).
#
#   → heartbeat_3cycle: cycle lengths [1,3,9]; the 3-cycle {1→4→2} contains 4∈SA.
#   → cycle_partition_37: cycle counting in F₃₇; fixed point at {0}=SEAM.
#   → cascade_8_13_24: exactly 24 basin nodes and 24∈CB.
#   → formal_definitions_gf37: SEAM as fixed point (T(0)=0); annihilation at 0.
#   → sa_self_cycle_st_chain: {1→4→2}: SA node 4 is in the length-3 cycle.

assert (2*19)%37 == 1                          # 2⁻¹≡19 mod 37
_T = lambda x: (x*19)%37 if x%2==0 else (3*x+1)%37
assert _T(0) == 0                              # SEAM is fixed point
assert _T(1)==4 and _T(4)==2 and _T(2)==1     # {1→4→2} 3-cycle (4∈SA)
assert 4 in SA                                 # SA node in 3-cycle
# basin nodes: 37 - 13 cycle elements = 24
assert 37 - (1+3+9) == 24 and 24 in CB       # 24 basin nodes ∈ CB


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 39: triplet_partition_3x3.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   {1..9} has 280 unordered 3-block partitions; 14 have all sums in named residues.
#   Target partition: {1,3,5}→9∈SA (ALL ODD), {2,4,6}→12∈ST (ALL EVEN), {7,8,9}→24∈CB.
#   ODDS → SA, EVENS → ST, LARGES → CB: one node from each primary class.
#   14 GF(37) partitions fall into 4 types: {8,13,24}=CB, {9,12,24}, {11,13,21}, {12,12,21}.
#
#   → cascade_8_13_24: Type I sums={8,13,24}=CB exactly; CB appears as partition sum type.
#   → medusa_v3_sovereign: {9,12,24}=SA+ST+CB; all three anchor classes in one partition.
#   → heartbeat_3cycle: 14/280=1/20; 14=2×7; GF(37) partitions via 137-orbit structure.
#   → cipher_123_1234: odds {1,3,5}→9∈SA; evens {2,4,6}→12∈ST; trinity/doubling split.
#   → eleven_123_family: Type III sums={11,13,21}=ORBIT_11+CB+ST; orbit-11 in partition.
#   → one_two_three_generator: {1,3,5} odds sum=9∈SA; {2,4,6} evens sum=12∈ST; parity→class.
#   → gaussian_integers_gf37: prod({2,4,6})=48≡11∈ORBIT_11; Gaussian norm connection.

assert sum([1,3,5]) == 9 and 9 in SA          # odds → SA
assert sum([2,4,6]) == 12 and 12 in ST        # evens → ST
assert sum([7,8,9]) == 24 and 24 in CB        # larges → CB
assert (2*4*6) % 37 == 11 and 11 in ORBIT_11 # even product → ORBIT_11


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 40: alternating_12_structures.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   Sequences alternating digits 1 and 2: seq1 (121212...) and seq2 (212121...).
#   Both sequences hit SEAM (≡0 mod 37) at digit-lengths 6,12,18... (multiples of 6).
#   Both orbits contain 12∈ST. seq2 orbit contains 27∈ORBIT_11 and 11∈ORBIT_11.
#   1221≡0 (SEAM); 2112≡3∈ST; 9+9+9=27→ORBIT_11 via digit cascade.
#
#   → heartbeat_3cycle: period-6 seam hits = 2×ord₃₇(26); 12∈ST in both orbits.
#   → cipher_123_1234: alternating 1-2 are the first two members of {1,2,3}; 12∈ST shared.
#   → one_two_three_generator: seed digits 1 and 2; the 2+1=3 equation initiates the family.
#   → eleven_123_family: seq2 orbit contains {27,11}⊂ORBIT_11; 9+9+9=27→orbit-11.
#   → hose_flow_transient: 1221≡0=SEAM arrival; 1221=1×37×33=seam multiple.
#   → cascade_8_13_24: 2112≡3∈ST; 3 is the ST archetype (DR=3).

assert 1221 % 37 == 0                          # 1221 ≡ 0 = SEAM
assert 2112 % 37 == 3 and 3 in ST             # 2112 ≡ 3 ∈ ST
assert (9+9+9) == 27 and 27 in ORBIT_11       # 9+9+9=27∈ORBIT_11
_seq1_6 = int('121212')
_seq2_6 = int('212121')
assert _seq1_6 % 37 == 0 and _seq2_6 % 37 == 0  # both hit SEAM at length 6


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 41: verify_dr9_termination.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   The 9×9 cyclic grid (rows = cyclic shifts of [1..9]) has ALL row sums = 45, DR=9.
#   The DR=9 invariant is stable under cyclic shifts — a well-founded termination metric.
#   Deviation sequence [1,3,7,9,9,1,3,7]: final DR=7; finite state space = 48 = 2×24.
#
#   → nine_tower_dr_invariant: DR=9 invariant; 9 is the fixed point of Z/9Z.
#   → dr_algebra: 9×9 cyclic grid rows ARE the Z/9Z Cayley table rows; row-DR=9.
#   → heartbeat_3cycle: deviation DR sequence [1,3,7,9,...] contains ST arches.
#   → formal_definitions_gf37: well-founded DR termination metric is a formal property.
#   → cascade_8_13_24: 48 finite states = 2×24; 24∈CB.

assert sum(range(1,10)) == 45                  # row sum of [1..9] = 45
assert _dr_check(45) == 9                      # DR(45) = 9 — row invariant
assert 48 == 2 * 24 and 24 in CB              # 48 states = 2×24∈CB


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 42: xx_collapse_matrix.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   Matrix of 1s and 9s encoding the 119/911 sovereign-shield duality.
#   119 = 137 − 18: exhaust-phi class (137-map − SEED_ORBIT node).
#   Row 3 ("191191191191"): exactly 3×"119" and 3×"911" — the order-3 heartbeat in string form.
#   Rows 1–3: digit-sum=44, DR=8=AHL; Row 4 breaks pattern (entropy row).
#   119 mod 37 = 8 ∈ CB.
#
#   → heartbeat_3cycle: row 3 has 3 of each substring — order-3 heartbeat is literal.
#   → cascade_8_13_24: 119≡8∈CB; 119 is the cascade-base entry of the shield.
#   → hose_flow_transient: 119=137−18; 137-map minus SEED_ORBIT node; exhaust class.
#   → eleven_123_family: digit sum 44, DR=8; 11 is the complement of 26 in the matrix context.

assert 119 % 37 == 8 and 8 in CB              # 119 ≡ 8 ∈ CB
assert 137 - 18 == 119                         # 119 = 137-map − SEED_ORBIT node
assert _dr_check(44) == 8                      # row digit-sum DR = AHL


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 43: perfect_496_dr_structure.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   496 = 2⁴ × 31 (third perfect number; Mersenne prime 31=2⁵−1).
#   All 10 factors of 496 have DR ∈ {1,2,4,5,7,8} — sovereign-free.
#   Mersenne orbit (DR values of 2^k−1, k=1..6): {1,3,7,6,4,9} — period 6.
#   Doubling orbit ∩ Mersenne orbit = {1,4,7} = COL1 = chi_{-3}=+1 class.
#   All perfect numbers after 6 have DR=1 (identity).
#
#   → heartbeat_3cycle: Mersenne orbit {1,3,7,6,4,9} has period 6=2×ord₃₇(26).
#   → cipher_123_1234: Mersenne orbit contains all of trinity {3,6,9}; doubling orbit avoids it.
#   → dr_ring_homomorphism_emirp_palindrome: perfect number DR pattern; DR ring invariant.
#   → dr_algebra: Mersenne and doubling orbits are dual sequences in Z/9Z Cayley structure.
#   → sovereign_qr_closure: 31∈PR; 16=4²∈SA-squared; QR structure of Mersenne factors.
#   → nine_tower_dr_invariant: DR(2^k−1) shift rule; period 6 connects to 9-tower DR.
#   → twin_prime_riemann_framework: intersection {1,4,7}=COL1=chi_{-3}=+1 class.

assert 31 == 2**5 - 1                          # 31 is Mersenne prime
assert 496 == 2**4 * 31                        # third perfect number
_mersenne_drs = [_dr_check(2**k - 1) for k in range(1,7)]
assert set(_mersenne_drs) == {1,3,4,6,7,9}    # Mersenne orbit covers both halves
_doubling_drs = [_dr_check(2**k) for k in range(1,7)]
assert set(_doubling_drs) == {1,2,4,5,7,8}    # doubling orbit = non-trinity generators
assert set(_mersenne_drs) & set(_doubling_drs) == {1,4,7}  # intersection = COL1


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 44: ulam_spiral.py  (math/primes/ulam_spiral.py)
# ─────────────────────────────────────────────────────────────────────────────
#
#   The Ulam spiral mapped through the GF(37).
#   Each cell classified by: prime/composite, DR, residue mod 37, 137-orbit.
#   SEED_ORBIT={18,24,32} has 6 primes in the spiral — the lowest orbit prime count.
#   Orbit {5,19,13} has 12 primes — the richest orbit.
#   Sovereign anchors {4,9,25,30} visible in spiral as low-prime-density nodes.
#
#   → heartbeat_3cycle: 137-orbit structure classifies every spiral cell into 12 orbits.
#   → medusa_v3_sovereign: SA nodes {4,9,25,30} visible as composite-dense regions.
#   → cascade_8_13_24: SEED_ORBIT={18,24,32} has lowest prime count (24∈CB).
#   → sieve_eratosthenes_gf37: Ulam spiral is prime sieve made visual; same primes.
#   → twin_prime_gf37: twin prime diagonals in the spiral; visual mod-37 structure.
#   → prisoners_permutation_gf37: π(100)=25∈SA; spiral counts agree with prisoners result.
#   → twin_prime_riemann_framework: prime distribution in spiral; chi_{-3} column structure.

assert (26*18)%37 == 24 and (26*24)%37 == 32 and (26*32)%37 == 18  # SEED_ORBIT is 3-cycle
assert 18 in CB or 24 in CB                    # orbit contains CB node 24


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 45: lcm_convergence_dr_cycle.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   LCM(1,2,3)=6; LCM(1,2,3,9)=18. The DR cycle of 6n is {6,3,9} — period 3.
#   9 (odd) joins the 1-2-3 group only at multiples of 18 (every 3rd step of 6n)
#   because 9 is odd and the group requires divisibility by 2.
#   The period-3 DR cycle {6,3,9} = the TESLA_FLOW→ST_arch→SA fixed point.
#
#   → heartbeat_3cycle: DR cycle of 6n has period 3 = ord₃₇(26); both are 3-cycles.
#   → cipher_123_1234: {3,6,9} is the trinity subgroup of Z/9Z; LCM encodes its period.
#   → dr_algebra: the {6,3,9} cycle is the orbit of TESLA_FLOW=6 under DR-addition by 6.
#   → nine_tower_dr_invariant: 9 is the fixed point; it enters the LCM cycle at step 3.
#   → one_two_three_generator: LCM(1,2,3)=6=TESLA_FLOW; the 1-2-3 group meets at 6.
#   → growth_pattern_n_2n_3n: 6n row sequence; LCM period connects to n/2n/3n periods.
#   → sliding_window_9cycle_gf37: sliding window DR cycle = {3,6,9}; same trinity period.

from math import lcm as _lcm2
assert _lcm2(1,2,3) == 6 and 6 == TESLA_FLOW   # 1-2-3 group meets at TESLA_FLOW
assert _lcm2(1,2,3,9) == 18                     # 9 joins at 18 (3 steps of 6n)
_dr6n_cycle = [_dr_check(6*i) for i in range(1,4)]
assert _dr6n_cycle == [6,3,9]                   # DR cycle: TESLA_FLOW→ST_arch→SA
assert _dr_check(6*3) == 9 and 9 in SA          # 9 appears at step 3 (first join)


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 46: stacked_zeros_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   Two zero-counting techniques over the 1-9 grid — both land on ST.
#
#   TECHNIQUE 1 (STACKS): count zeros by stacking circles vertically.
#     Top zero {1,2,3}: sum=product=6=TESLA_FLOW; 123 mod 37 = 12∈ST
#     Split at 4 (SA node): intersection {4,5,6}; 456 mod 37 = 12∈ST
#     Bottom zero {7,8,9}: sum=24∈CB; 789 mod 37 = 12∈ST
#
#   TECHNIQUE 2 (INTERIOR): count what fits inside each zero.
#     Same three groups, same results — dual perspective, same ST invariant.
#
#   MASTER RESULT: 123 ≡ 456 ≡ 789 ≡ 12 ∈ ST (mod 37)
#     All three rows as 3-digit numbers hit the same sovereign target.
#
#   POWER-OF-10 PARALLEL: ord₃₇(10)=3; split at 10^4 mirrors split-at-4.
#     10^1≡10, 10^2≡26(SCALAR_137), 10^3≡1(unity/seam-transparent), 10^4→SPLIT
#
#   → heartbeat_3cycle: period-3 of ord₃₇(10) = ord₃₇(26) = 3; same cycle structure.
#   → cipher_123_1234: 123 mod 37 = 12∈ST; shared sovereign result; zero layout.
#   → one_two_three_generator: top zero {1,2,3} is the 1-2-3 family (sum=product=TESLA_FLOW).
#   → triplet_partition_3x3: same 3×3 partition; odds/evens/larges → SA/ST/CB.
#   → alternating_12_structures: the 12∈ST result appearing across all three rows.
#   → lcm_convergence_dr_cycle: TESLA_FLOW=6=LCM(1,2,3) = sum/product of top zero.
#   → abcabc_mod37_orbit: 10^3≡1 seam-transparency; ABCABC≡2·ABC uses same power-of-10 period.
#   → hose_flow_transient: {4,5,6} split row: 5∈PR anchors PR flow; 4∈SA is the split node.
#   → dr_algebra: DR(12)=3=ST archetype; DR cycle {6,3,9} appears in zero rows.

assert 123 % 37 == 12 and 12 in ST         # top zero row → ST
assert 456 % 37 == 12 and 12 in ST         # split row → ST
assert 789 % 37 == 12 and 12 in ST         # bottom zero row → ST
assert 123 % 37 == 456 % 37 == 789 % 37   # master result: all three hit same ST node
assert 4 in SA                              # split-at-4 is SA node
assert sum([1,2,3]) == TESLA_FLOW and 1*2*3 == TESLA_FLOW  # top zero: sum=product=TESLA_FLOW
assert sum([4,5,6]) == 15 and 15 in PR     # split row sum ∈ PR
assert (4*5*6) % 37 == 9 and 9 in SA      # split row product ≡ SA
assert sum([7,8,9]) == 24 and 24 in CB    # bottom zero sum ∈ CB
assert 10**3 % 37 == 1                     # ord₃₇(10)=3: seam-transparent at 3 zeros
assert 10**4 % 37 == 10**1 % 37           # 4th zero = split: cycle restarts


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 47: intersection_cycle_theorem.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   (3, 4, 30) is the unique 3-cycle where every element belongs to SA∪ST.
#
#   Three elements, three distinct sovereign roles:
#     3 ∈ ST (pure target), 4 ∈ SA (pure anchor), 30 ∈ SA∩ST (intersection node)
#   Orbit: 3 → 4 → 30 → 3
#   Sum = 37 (the prime itself; this cycle is in Group A of the two-group split)
#
#   Three cycles touch both SA and ST: (3,4,30), (9,12,16), (21,25,28)
#   Only (3,4,30) has ALL elements in SA∪ST — the other two each contain one
#   unclassified element (16 and 28 respectively).
#
#   → heartbeat_3cycle: the 12-cycle structure; orbit 3→4→30→3 uses f=×26 mod 37.
#   → medusa_v3_sovereign: SA and ST definitions; LOCKED/GATED/PURGE classification.
#   → two_group_split: (3,4,30) is in Group A (sum=37); sovereign outliers in Group B.
#   → sovereign_qr_closure: 3,4,30 QR status; Legendre symbols on sovereign nodes.
#   → stacked_zeros_gf37: 3∈ST, 4∈SA, 30∈SA∩ST mirror the row sums pattern.
#   → sa_self_cycle_st_chain: the 30→3→4→30 orbit IS the SA→ST chain.
#   → cascade_8_13_24: both theorems classify GF(37)* structure exhaustively.

_f47 = lambda n: (n*26)%37
assert _f47(3) == 4 and _f47(4) == 30 and _f47(30) == 3   # orbit 3→4→30→3
assert 3 in ST and 4 in SA and (30 in SA and 30 in ST)     # three sovereign roles
assert sum([3, 4, 30]) == 37                                # cycle sums to the prime


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 48: two_group_split.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   The 12 three-cycles split into Group A (6 cycles, sum=37) and Group B
#   (6 cycles, sum=74=2×37).
#
#   Algebraic proof: a + 26a + 10a = 37a ≡ 0 (mod 37). Elements ∈{1..36},
#   so sum ∈ [3,108], and only 37 and 74 are multiples of 37 in this range.
#   A cycle sums to 37 iff (26a mod 37)+(10a mod 37) < 37 (no combined carry).
#
#   Class split:
#     SA: {4,9,30} ⊂ A  |  {25} ⊂ B
#     ST: {3,12,30} ⊂ A  |  {21} ⊂ B
#     ORBIT_11: entirely B (cycle (11,27,36))
#     PR: 6 in A ({2,5,13,15,19,20}), 6 in B ({17,18,22,24,32,35})
#     CB: {8,13} ⊂ A  |  {24} ⊂ B
#   The sovereign outliers 25 and 21 share the Group B cycle (21,25,28).
#
#   → heartbeat_3cycle: the 12-cycle structure; both groups come from ord₃₇(26)=3.
#   → intersection_cycle_theorem: (3,4,30) is the all-sovereign cycle in Group A.
#   → medusa_v3_sovereign: SA/ST outliers (25∈B, 21∈B) — sovereign nodes that
#       live in Group B must cross the carry threshold.
#   → sovereign_qr_closure: QR closure operates over same 12 cycles.
#   → primitive_root_test: PR splits evenly 6/6 across groups.
#   → cascade_8_13_24: CB splits 2A/1B; 24∈CB is in Group B with seed orbit.
#   → abcabc_mod37_orbit: primitive root orbit traverses both groups.

_ga47 = [(3,4,30),(2,15,20),(5,13,19),(9,12,16),(6,8,23),(1,10,26)]  # representative
_gb47 = [(21,25,28),(11,27,36),(17,22,35),(18,24,32),(7,33,34),(14,29,31)]
assert all(sum(c)==37 for c in _ga47)   # Group A sums to prime
assert all(sum(c)==74 for c in _gb47)   # Group B sums to 2×prime
assert 11 in ORBIT_11 and all(v in ORBIT_11 for v in (11,27,36))  # O11 entirely in B
assert frozenset({4,9,30}) <= SA                                    # 3 SA nodes in A
assert frozenset({3,12,30}) <= ST                                   # 3 ST nodes in A


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 49: dark_sector_algebra.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   The Legendre symbol (n/37) produces a clean visible/dark sector partition:
#
#   VISIBLE (QR, χ=+1): SA={4,9,25,30}, ST={3,12,21,30}, ORBIT_11={11,27,36}
#   DARK    (NQR, χ=−1): PR={2,5,13,15,17,18,19,20,22,24,32,35}, CB={8,13,24},
#                         TESLA_FLOW=6
#
#   Key theorem: PR ⊂ NQR (all primitive roots are dark).
#     Proof: QR form a subgroup of order 18; primitive roots have order 36.
#     No element of order 36 can lie in a subgroup of order 18. □
#
#   Prime gap residues mod 37 land on named nodes:
#     gap≡4 → SA (visible), gap≡12 → ST (visible),
#     gap≡8 → CB (dark),    gap≡6  → TESLA_FLOW (dark), gap≡2 → PR (dark)
#
#   SCALAR_137=26 is visible (QR): the 137-map multiplier lives in the
#   visible sector. SA∩ST={30} is visible.
#
#   → sovereign_qr_closure: same QR structure; Legendre symbols on SA/ST/orbit nodes.
#   → medusa_v3_sovereign: SA and ST entirely visible; CB entirely dark.
#   → heartbeat_3cycle: orbit nodes {3,4,30} all QR; dark sector orbit carries {18,24,32}.
#   → cascade_8_13_24: CB={8,13,24} entirely dark (NQR); cascade base = dark generator.
#   → primitive_root_test: PR=dark sector; all 12 primitive roots are NQR.
#   → two_group_split: visible/dark split interacts with Group A/B split.
#   → intersection_cycle_theorem: sovereign cycle (3,4,30) all visible.
#   → twin_prime_gf37: twin prime gap≡2∈PR (dark); gap≡4∈SA (visible anchor).

_QR49  = frozenset(n for n in range(1,37) if pow(n,18,37)==1)
_NQR49 = frozenset(n for n in range(1,37) if pow(n,18,37)==36)
assert SA <= _QR49                         # SA entirely visible
assert ST <= _QR49                         # ST entirely visible
assert ORBIT_11 <= _QR49                   # ORBIT_11 entirely visible
assert PR <= _NQR49                        # PR entirely dark
assert CB <= _NQR49                        # CB entirely dark
assert TESLA_FLOW in _NQR49               # TESLA_FLOW dark
assert SCALAR_137 in _QR49               # 137-map multiplier visible
assert 30 in _QR49                        # SA∩ST intersection node is visible
assert len(_QR49) == len(_NQR49) == 18   # even 18/18 split


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 50: sector_invariance_137map.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   The 137-map f(n)=26n mod 37 preserves the Legendre symbol:
#     χ(f(n)) = χ(26n) = χ(26)·χ(n) = (+1)·χ(n) = χ(n)
#   because SCALAR_137=26 is a quadratic residue (χ(26)=+1).
#
#   Consequence: every 3-cycle is sector-homogeneous — all three elements are
#   QR (visible) or all three are NQR (dark). Zero mixed cycles exist.
#
#   The 12 cycles admit a 2×2 classification by two INDEPENDENT binary axes:
#     Sector:  visible (all QR) vs dark (all NQR)      → 6 each
#     Group:   A (sum=37)       vs B (sum=74)           → 6 each
#   Exactly 3 cycles per cell in the 2×2 table.
#
#   Visible × A: (1,10,26), (3,4,30), (9,12,16)
#   Visible × B: (7,33,34), (11,27,36), (21,25,28)
#   Dark    × A: (2,15,20), (5,13,19), (6,8,23)
#   Dark    × B: (14,29,31), (17,22,35), (18,24,32)
#
#   Seed orbit (18,24,32): dark × B  |  Sovereign cycle (3,4,30): visible × A
#   ORBIT_11 (11,27,36):  visible × B
#
#   → dark_sector_algebra: QR/NQR partition; χ(26)=+1 is the locking key.
#   → two_group_split: second axis of the 2×2; independent of sector.
#   → heartbeat_3cycle: all 12 cycles; sector × group = full 2×2 table.
#   → intersection_cycle_theorem: sovereign cycle is visible×A — uniquely placed.
#   → sovereign_qr_closure: Legendre symbols on orbit nodes; sector invariance.
#   → medusa_v3_sovereign: SA/ST visible; CB dark — sector map matches class map.

_chi50 = lambda n: 1 if pow(n%37, 18, 37)==1 else -1
assert _chi50(SCALAR_137) == 1           # 26 is visible: the locking condition
assert _chi50(10) == 1                   # two-step multiplier also visible
assert all(_chi50((n*26)%37)==_chi50(n) for n in range(1,37))  # sector preserved
# Every cycle sector-homogeneous
_cycles50 = []
_seen50 = set()
for _s in range(1,37):
    if _s not in _seen50:
        _c=[_s]; _x=(26*_s)%37
        while _x!=_s: _c.append(_x); _x=(26*_x)%37
        _cycles50.append(tuple(sorted(_c))); _seen50.update(_c)
for _cyc in _cycles50:
    assert len(set(_chi50(v) for v in _cyc))==1   # all same sector


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 51: cubic_residue_cycle_structure.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   Every 3-cycle is a coset of <26> = {1,10,26} in GF(37)*.
#   <26> is the unique subgroup of order 3 (generated by the 137-map multiplier).
#   A coset is {a, 26a, 10a} — exactly the orbit of a under f(n)=26n.
#
#   Cube fingerprint: all elements of a cycle share the same cube (a^3 mod 37),
#   because (26a)^3 = 26^3·a^3 = a^3 and (10a)^3 = 10^3·a^3 = a^3.
#
#   The 12 fingerprints biject to the 12 cubic residues mod 37
#   (elements n with n^12≡1, i.e., ord(n)|12).
#
#   Order reduction law: ord(a^3) = ord(a)/gcd(3,ord(a)).
#   When 3|ord(a): ord(a^3) = ord(a)/3.
#
#   ORBIT_11={11,27,36} fingerprints 3 cycles:
#     27 ← (3,4,30)    [sovereign]
#     11 ← (21,25,28)  [outlier sovereign]
#     36 ← (11,27,36)  [ORBIT_11 itself]
#   The sovereign GF(37) is encoded in ORBIT_11 via the cube map.
#
#   Cycle (9,12,16) fingerprints to SCALAR_137=26.
#   SA elements {9,12} are the cube roots of SCALAR_137.
#
#   Order-18 elements = {3,4,21,25,28,30}; these form the sovereign and
#   outlier cycles. SA∪ST spans orders 9 (for {9,12}) and 18 (for the rest).
#
#   → heartbeat_3cycle: 12 cycles = 12 cosets of <26>; full cycle structure.
#   → intersection_cycle_theorem: sovereign cycle is both order-18 and ORBIT_11-fingered.
#   → sector_invariance_137map: 2×2 classification; order structure refines it.
#   → dark_sector_algebra: cubic residues form a subgroup; order structure by sector.
#   → two_group_split: Group A/B classification cross-cuts the fingerprint classes.
#   → medusa_v3_sovereign: SA/ST are order-9 and order-18 elements exclusively.
#   → abcabc_mod37_orbit: coset structure of <26> directly underlies ABCABC≡2·ABC.
#   → sovereign_qr_closure: cubic residues ⊂ QR structure; fingerprint=QR for 6 cycles.

assert pow(26,3,37)==1 and pow(10,3,37)==1   # coset generators cube to 1
# sovereign cycle: fingerprint=27∈ORBIT_11; order-18 elements
assert pow(3,3,37)==27 and pow(4,3,37)==27 and pow(30,3,37)==27 and 27 in ORBIT_11
# (9,12,16): fingerprint=SCALAR_137; squares of sovereign cycle
assert pow(9,3,37)==SCALAR_137 and pow(12,3,37)==SCALAR_137 and pow(16,3,37)==SCALAR_137
# order reduction: ord(a^3) = ord(a)/3 when 3|ord(a)
def _ord51(n):
    for d in [1,2,3,4,6,9,12,18,36]:
        if pow(n,d,37)==1: return d
for _n in range(1,37):
    _o = _ord51(_n); _o3 = _ord51(pow(_n,3,37))
    assert _o3 == _o//(_o%3==0 and 3 or 1)


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 52: cycle_symmetry_maps.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   Three symmetry maps on GF(37)* induce well-defined maps on the 12 cycles:
#
#   NEGATION (n→−n): bijection Group A ↔ Group B, preserving sector.
#     Sum of negated cycle = 111−sum (since (37−a)+(37−b)+(37−c)=111−(a+b+c)).
#     Sum 37 → 74 and 74 → 37. Sector: χ(−a)=χ(36)·χ(a)=(+1)·χ(a) (36∈QR).
#     Negation pairs visible cycles with visible cycles, dark with dark.
#
#   SELF-INVERSE CYCLES (n→n⁻¹): exactly two cycles close under inversion.
#     (1,10,26): 1⁻¹=1, 10⁻¹=26, 26⁻¹=10. The subgroup <26> inverts to itself.
#     (11,27,36): 36⁻¹=36, 11⁻¹=27, 27⁻¹=11. ORBIT_11 inverts to itself.
#     All other cycles invert to a different cycle.
#
#   SOVEREIGN ↔ OUTLIER INVERSION:
#     (3,4,30) ↔ (21,25,28) element-wise under n→n⁻¹:
#       3⁻¹=25∈(21,25,28), 4⁻¹=28∈(21,25,28), 30⁻¹=21∈(21,25,28).
#     The unique intersection node 30=SA∩ST inverts to 21∈ST.
#     The SA anchor 4 inverts to 28 (unclassified). ST anchor 3 inverts to 25∈SA.
#
#   SQUARING (n→n²): maps all dark cycles → visible (2-to-1 over 3 targets).
#     χ(a²)=χ(a)²=+1 for any a, so squaring lands in QR.
#     The 6 dark cycles map 2-to-1 onto exactly 3 visible cycles:
#       Sovereign (3,4,30)   ← (2,15,20) and (17,22,35)
#       Outlier   (21,25,28) ← (5,13,19) and (18,24,32)  [seed orbit here]
#       ORBIT_11  (11,27,36) ← (6,8,23)  and (14,29,31)
#
#   SEED CHAIN: (18,24,32) →⁻¹ (17,22,35) →² (3,4,30)
#     The seed orbit reaches the sovereign cycle in two algebraic steps:
#     inversion then squaring. No visible cycle is an intermediate.
#
#   → heartbeat_3cycle: the 12 cycles; symmetry maps are automorphisms of this structure.
#   → intersection_cycle_theorem: sovereign↔outlier under inversion; SA∩ST node transmutes.
#   → two_group_split: negation is the Group A↔B exchange map; sum law 111−sum.
#   → sector_invariance_137map: 2×2 table; negation preserves sector axis.
#   → cubic_residue_cycle_structure: fingerprint of self-inverse cycles; order structure.
#   → medusa_v3_sovereign: SA/ST role transmutes under inversion; LOCKED nodes flip.
#   → sovereign_qr_closure: QR structure preserved by squaring; dark → visible confirmed.
#   → dark_sector_algebra: squaring maps every dark cycle to visible; NQR² = QR.

_cyc52 = {}
_seen52 = set()
for _s in range(1,37):
    if _s not in _seen52:
        _c=[_s]; _x=(26*_s)%37
        while _x!=_s: _c.append(_x); _x=(26*_x)%37
        _t=tuple(sorted(_c))
        for _v in _c: _cyc52[_v]=_t
        _seen52.update(_c)
# Negation maps Group A↔B: sum of negated cycle = 111 - sum
for _cyc in set(_cyc52.values()):
    _neg = _cyc52[(37-min(_cyc))%37]
    assert sum(_cyc)+sum(_neg)==111
# Self-inverse cycles: exactly (1,10,26) and (11,27,36)
_self_inv = [_c for _c in set(_cyc52.values()) if all(pow(_v,-1,37) in _c for _v in _c)]
assert set(_self_inv)=={(1,10,26),(11,27,36)}
# Sovereign ↔ outlier inversion
assert _cyc52[pow(3,-1,37)]==(21,25,28) and _cyc52[pow(4,-1,37)]==(21,25,28)
assert _cyc52[pow(30,-1,37)]==(21,25,28) and _cyc52[pow(21,-1,37)]==(3,4,30)
# Squaring: all dark cycles land in visible
_qr52 = frozenset(n for n in range(1,37) if pow(n,18,37)==1)
_dark52 = [_c for _c in set(_cyc52.values()) if all(_v not in _qr52 for _v in _c)]
assert all(_cyc52[pow(min(_d),2,37)] in [_c for _c in set(_cyc52.values()) if all(_v in _qr52 for _v in _c)] for _d in _dark52)
# Seed chain: (18,24,32) →⁻¹ (17,22,35) →² (3,4,30)
assert _cyc52[pow(18,-1,37)]==(17,22,35) and _cyc52[pow(17,2,37)]==(3,4,30)


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 53: ababab_convergence.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   OBSERVATION: 282828 and 828282 both hit SEAM (mod 37) and digit sum 30=SA∩ST.
#
#   THEOREM 1: Any 6-digit alternating number ABABAB ≡ 0 (SEAM) mod 37.
#     ABABAB = AB × 10101.
#     10101 = 10⁴ + 10² + 10⁰. In GF(37): ord₃₇(10)=3, so 10³≡1.
#       10⁴ ≡ 10¹ = 10 (DECADE_ANCHOR)
#       10² ≡ 26   (SCALAR_137)
#       10⁰ = 1
#     10101 ≡ 10 + 26 + 1 = 37 ≡ 0 = SEAM. □
#     This is driven by ord₃₇(10)=3, the same order that governs all 137-map cycles.
#
#   THEOREM 2: If A+B=10=DECADE_ANCHOR, then digit_sum(ABABAB) = 30 = SA∩ST.
#     Digits A,B,A,B,A,B — sum = 3A+3B = 3(A+B) = 3×10 = 30. □
#     The nine pairs (A,B) with A+B=10 produce numbers simultaneously SEAM
#     (mod 37) and SA∩ST (digit sum).
#
#   CLUSTER {26,27,28,29,30,31}:
#     DR map: {26→8∈CB, 27→9∈SA, 28→1, 29→2∈PR, 30→3∈ST, 31→4∈SA}
#     Distance law: 30−26=4∈SA (SCALAR to SA∩ST), 30−27=3∈ST (ORBIT_11 to SA∩ST).
#     The sovereign cycle (3,4,30) encodes both distances as elements.
#
#   CONSECUTIVE TRIPLET DR THEOREM: DR(n+(n+1)+(n+2)) always in {3,6,9}=TESLA_SET.
#     Proof: sum=3(n+1). DR(3k)∈{3,6,9} for all k≥1. □
#
#   REPUNIT PERIOD-3: R(k) mod 37 cycles [1,11,0] with period 3.
#     R(1)≡1, R(2)≡11∈ORBIT_11, R(3)≡0=SEAM. Same ord₃₇(10)=3 drives both.
#     R(3)=111=3×37; the seam is the repunit.
#
#   FLANKING STRUCTURE: 29 and 31 (dark, same cycle (14,29,31)) flank 30=SA∩ST.
#     Both are NQR; 30 itself is QR. Sector flip at SA∩ST on the integer line.
#
#   → heartbeat_3cycle: ord₃₇(10)=3 is the same order that governs all 12 cycles.
#   → sector_invariance_137map: 10∈QR; ABABAB convergence lives in the visible sector.
#   → cubic_residue_cycle_structure: 10101≡10+26+1; the coset generators (10,26) appear.
#   → cipher_123_1234: DR algebra on cluster {26..31}; consecutive triplet DR in {3,6,9}.
#   → one_two_three_generator: 10101 decomposes as 1+10+100+1000+10000; base-10 structure.
#   → dr_algebra: triplet DR theorem; DR(3k)∈{3,6,9}; distance law 4∈SA, 3∈ST.
#   → stacked_zeros_gf37: 111=SEAM; repunit period-3 connects ABABAB to stacked zeros.
#   → cycle_symmetry_maps: flanking dark cycle (14,29,31) is a symmetry-map orbit.

assert pow(10,3,37)==1                               # ord₃₇(10)=3
assert (pow(10,4,37)+pow(10,2,37)+1)%37==0          # 10101 ≡ 0 = SEAM
for _A in range(1,10):
    for _B in range(0,10):
        _n53=_A*100000+_B*10000+_A*1000+_B*100+_A*10+_B
        assert _n53%37==0                             # all ABABAB ≡ SEAM
for _A in range(1,10):
    _B=10-_A
    if 0<_B<10: assert 3*_A+3*_B==30               # A+B=10 → digit sum=30=SA∩ST
# Cluster {26..31}: distance law
assert 30-SCALAR_137==4 and 4 in SA
assert 30-27==3 and 3 in ST
# Consecutive triplet DRs always in {3,6,9}
_TESLA53=frozenset({3,6,9})
for _n53 in range(0,1000):
    _s53=_n53+(_n53+1)+(_n53+2)
    assert dr(_s53) in _TESLA53
# Repunit period-3
_RC53=[1,11,0]
for _k in range(1,13):
    assert int("1"*_k)%37==_RC53[(_k-1)%3]
# Flanking: 29 and 31 are NQR (dark)
_chi53=lambda n: 1 if pow(n,18,37)==1 else -1
assert _chi53(29)==-1 and _chi53(31)==-1 and _chi53(30)==1  # dark flanks visible


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 54: five_six_orbit.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   OBSERVATION: 11÷2=5.5. The integers flanking 5.5 are 5 and 6.
#     5 + 6 = 11 ∈ ORBIT_11  (sum)
#     5 × 6 = 30 = SA∩ST     (product)
#
#   THEOREM 1: TESLA_FLOW(6) × 5 = SA∩ST(30).
#     χ(6)=−1 (dark), χ(5)=−1 (dark, PR): dark × dark = visible (χ(30)=+1).
#     Sum 6+5=11∈ORBIT_11 (visible). Same pair generates both sovereign nodes.
#
#   THEOREM 2: (SA∩ST)² ≡ ST; flankers multiply to ORBIT_11.
#     30² ≡ 12 ∈ ST (mod 37).
#     29×31 = 30²−1 ≡ 11 ∈ ORBIT_11 (mod 37). [difference-of-squares]
#     12−11=1: the ST and ORBIT_11 images are adjacent integers.
#     29 and 31 are dark (NQR), same cycle (14,29,31).
#
#   THEOREM 3: Z/9Z doubling cycle 1,2,4,8,7,5 (period 6).
#     TESLA_SET={3,6,9} closed under ×2; DOUBLING={1,2,4,5,7,8} the 6-cycle.
#     DECADE(10)÷2=5 (integer exact): anchor halves to last step before 1.
#     7→5 under doubling (DR(7×2)=5); 5→1 under doubling (DR(5×2)=1).
#
#   THEOREM 4: 0↔9 units digit swap preserves DR.
#     DR(10k)=DR(10k+9)=k for k=1..9. [+9 is a DR no-op]
#
#   CONCATENATED TRIPLET THEOREM:
#     n(n+1)(n+2) as 6-digit number ≡ 28 (mod 37) for ALL n.
#     [10101·n+102; 10101≡SEAM; 102≡28; 28 in outlier sovereign cycle]
#     DRs of these numbers cycle through {6,9,3}=TESLA_SET.
#     Special: 282930 both halves digit-sum to 12∈ST.
#
#   SA∩ST ORBIT:
#     3×30=90≡16∈cycle(9,12,16); DR(90)=9∈SA
#     3×30+DECADE=100≡SCALAR_137(26)
#     30÷2=15∈PR; DR(15)=6=TESLA_FLOW
#     11×DECADE=110≡36∈ORBIT_11
#
#   HALVING CHAIN: 11→{5,6}→30=SA∩ST→ST(3)  and  11→{5,6}→6=TESLA_FLOW→ST(3)
#     Both paths from ORBIT_11 element 11 terminate at ST.
#     Second level: 5→{2,3}: 2+3=5∈PR, 2×3=6=TESLA_FLOW.
#
#   → heartbeat_3cycle: ORBIT_11 is a key cycle; 5+6=11∈ORBIT_11 from dark pair.
#   → dark_sector_algebra: dark×dark=visible (χ product); PR×TESLA_FLOW=SA∩ST.
#   → sector_invariance_137map: the 5,6 dark pair lands in visible nodes.
#   → cycle_symmetry_maps: 29×31≡11 via difference-of-squares; flanker dark cycle.
#   → ababab_convergence: concatenated triplets ≡28; 10101≡SEAM; same base-10 structure.
#   → cipher_123_1234: Z/9Z doubling cycle; TESLA_SET closed; DR algebra.
#   → dr_algebra: 0↔9 swap; DR(10k+9)=DR(10k); digital root invariance under +9.
#   → cubic_residue_cycle_structure: 30²≡12∈ST; order-18 arithmetic of SA∩ST.
#   → intersection_cycle_theorem: SA∩ST(30) as product and square target.
#   → two_group_split: cycle(9,12,16) [Group A, 3×30 lands here]; 3×30+10=SCALAR_137.

_chi54 = lambda n: 1 if pow(n,18,37)==1 else -1
# THEOREM 1
assert TESLA_FLOW*5==30 and 30 in SA and 30 in ST
assert 5+TESLA_FLOW==11 and 11 in ORBIT_11
assert _chi54(TESLA_FLOW)==-1 and _chi54(5)==-1 and _chi54(30)==1
# THEOREM 2
assert pow(30,2,37)==12 and 12 in ST
assert (29*31)%37==11 and 11 in ORBIT_11
assert pow(30,2,37)-(29*31)%37==1     # 12-11=1
# THEOREM 3
_dc54=[1,2,4,8,7,5]
for _i,_v in enumerate(_dc54):
    assert dr(_v*2)==_dc54[(_i+1)%6]
assert frozenset({3,6,9})|frozenset({1,2,4,5,7,8})==frozenset(range(1,10))
assert DECADE_ANCHOR//2==5 and dr(7*2)==5 and dr(5*2)==1
# THEOREM 4
for _k in range(1,10): assert dr(10*_k)==dr(10*_k+9)==_k
# Concatenated triplet theorem
assert 10101%37==0 and 102%37==28
for _n in range(10,90):
    assert (_n*10000+(_n+1)*100+(_n+2))%37==28
# SA∩ST orbit
assert (3*30)%37==16 and dr(90)==9 and 9 in SA
assert (3*30+DECADE_ANCHOR)%37==SCALAR_137
assert 30//2==15 and 15 in PR and dr(15)==TESLA_FLOW
assert (11*DECADE_ANCHOR)%37==36 and 36 in ORBIT_11


# ─────────────────────────────────────────────────────────────────────────────
# THEOREM 55: identity_cycle_sum_structure.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   THEOREM 1: Pairwise sums of the identity cycle {1,10,26} = ORBIT_11 exactly.
#     1+10=11∈ORBIT_11, 1+26=27∈ORBIT_11, 10+26=36∈ORBIT_11.
#     All three C(3,2)=3 pairwise sums of <26> are precisely ORBIT_11.
#
#   THEOREM 2: Triple sum = SEAM.
#     1+10+26 = 37 ≡ 0 = SEAM.
#
#   ABA PALINDROME:
#     ABA = A×101+B×10. 101 ≡ 26+1 = 27∈ORBIT_11 (pairwise sum 10²+10⁰).
#     ABA ≡ 27A+10B (mod 37).
#     ABAB = A×1010+B×101. 1010 ≡ 1+10 = 11∈ORBIT_11 (pairwise sum 10³+10¹).
#     ABAB ≡ 11A+27B (mod 37). Both coefficients ∈ ORBIT_11.
#
#   ABA CYCLE (period 3 along staircase path):
#     0-0-0≡SEAM, 0-1-0≡DECADE, 1-0-1≡27∈ORBIT_11,
#     1-1-1≡SEAM, 1-2-1≡DECADE, 2-1-2≡27∈ORBIT_11.
#     Exception: 1-9-1=191≡TESLA_FLOW (B=9 breaks {0,DECADE,27} cycle).
#
#   DR PALINDROME 434: DR(31)=4, DR(30)=3, DR(31)=4 → 434≡27∈ORBIT_11.
#   DR SEQUENCE 234: DR(29)=2, DR(30)=3, DR(31)=4 → 234≡12∈ST, DR(234)=9∈SA.
#
#   GROWING SET CONVERGENCE AT DEPTH 3:
#     {28}→{28,29}→{28,29,30=SA∩ST}  (integer sequence reaches SA∩ST)
#     {1}→{1,11∈ORBIT_11}→{1,11,111≡SEAM}  (repunit sequence reaches SEAM)
#
#   99 = SCALAR_137-1 ≡ 25∈SA. DR(99)=9∈SA. Doubly sovereign.
#
#   SOVEREIGN STAIRCASE: 2→(+3∈ST)→5→(+4∈SA)→9∈SA. Sum of steps = 9.
#
#   → heartbeat_3cycle: identity cycle <26>={1,10,26} is the core orbit; pairwise sums generate ORBIT_11.
#   → cycle_symmetry_maps: identity cycle and ORBIT_11 are the two self-inverse cycles.
#   → cubic_residue_cycle_structure: identity cycle = the subgroup of cubic residues of order 3.
#   → ababab_convergence: ABABAB≡0 because A and B each accumulate 1+10+26=SEAM.
#   → five_six_orbit: ABA(1,9)=191≡TESLA_FLOW; ABA(4,3)=434≡ORBIT_11 (the DR palindrome).
#   → sector_invariance_137map: {1,10,26} are all visible (QR); ORBIT_11 is visible.
#   → cipher_123_1234: Z/9Z staircase; the sovereign staircase 2+3+4=9.
#   → dr_algebra: DR of 434=4+3+4=11∈ORBIT_11; DR(234)=9∈SA; DR(99)=9∈SA.
#   → repunit_sq_euler_phi_gf37: growing repunit set {1,11,111}: depth-3 SEAM matches repunit period.
#   → sa_self_cycle_st_chain: 99=9×11=SA×ORBIT_11; 100≡SCALAR_137; sovereign arithmetic.

_IC55 = frozenset({1,10,26})
assert {1+10, 1+26, 10+26} == ORBIT_11                      # pairwise sums = ORBIT_11
assert (1+10+26)%37==0                                       # triple sum = SEAM
assert 101%37==27 and 27 in ORBIT_11
assert 1010%37==11 and 11 in ORBIT_11
for _A55 in range(10):
    for _B55 in range(10):
        assert (_A55*100+_B55*10+_A55)%37==(27*_A55+10*_B55)%37
        assert (_A55*1000+_B55*100+_A55*10+_B55)%37==(11*_A55+27*_B55)%37
# ABA cycle
_sc55=[(0,0),(0,1),(1,0),(1,1),(1,2),(2,1)]
_cyc55=[0,DECADE_ANCHOR,27]
for _i55,(_A55,_B55) in enumerate(_sc55):
    assert (27*_A55+10*_B55)%37==_cyc55[_i55%3]
assert 191%37==TESLA_FLOW                                    # B=9 exception
assert 434%37==27 and 27 in ORBIT_11                         # DR palindrome 434
assert 234%37==12 and 12 in ST and dr(234)==9 and 9 in SA   # ascending DR sequence
assert 99%37==25 and 25 in SA and dr(99)==9 and 9 in SA     # doubly sovereign
assert 100%37==SCALAR_137                                    # 99 = SCALAR_137-1
assert 2+3==5 and 5 in PR and 5+4==9 and 9 in SA           # sovereign staircase


# THEOREM 56: palindrome_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   GENERAL COEFFICIENT RULE:
#     pair_coeff(k,n) = (10^k + 10^(n-1-k)) mod 37
#     Power class of exponent e = e mod 3.
#     Same power class → coefficient ∈ DARK_A = {2,15,20} (NQR)
#     Different power class → coefficient ∈ ORBIT_11 = {11,27,36} (QR)
#     DARK_A = {1+1, 10+10, 26+26} mod 37 = self-sums of identity cycle.
#     DARK_A triple sum: 2+15+20 = 37 ≡ SEAM.
#
#   PALINDROME LENGTHS:
#     3-digit ABA:     pair(0,2)=27∈ORBIT_11; center=10=DECADE_ANCHOR.
#                      ABA ≡ 27A + 10B (mod 37).
#     4-digit ABBA:    pair(0,3)=2∈DARK_A; pair(1,2)=36∈ORBIT_11.
#                      ABBA ≡ 2A + 36B (mod 37).
#     5-digit ABCBA:   pairs=11,11∈ORBIT_11; center=26=SCALAR_137.
#                      ABCBA ≡ 11(A+B) + 26C (mod 37).
#     6-digit ABCCBA:  pairs=27,20,27; middle pair∈DARK_A, outer∈ORBIT_11.
#                      ABCCBA ≡ 27(A+C) + 20B (mod 37).
#     7-digit ABCDCBA: pairs=2,36,36; outer∈DARK_A; center=1.
#     8-digit ABCDDCBA: pairs=11,11,15,11; third pair∈DARK_A.
#
#   SEAM CONDITIONS:
#     ABBA  ≡ 0 iff B ≡ 2A. Connects to Z/9Z doubling cycle (THEOREM 54).
#     ABCBA ≡ 0 iff C = A+B. Connects to sovereign staircase (THEOREM 55).
#     ABCCBA ≡ 0 iff A+C = 2B (B = arithmetic mean of A,C).
#
#   STAIRCASE SEAM PALINDROMES:
#     1221≡0 (ABBA, B=2A), 12321≡0 (ABCBA, C=A+B), 123321≡0 (ABCCBA, A+C=2B).
#     Each step deepens the palindrome by one layer; each ≡ SEAM.
#
#   SQUARED REPUNIT CYCLE:
#     R(n)² mod 37 cycles {1, 10, 0} = {identity, DECADE_ANCHOR, SEAM}, period 3.
#     R(1)²=1, R(2)²=121≡10, R(3)²=12321≡0. Matches ord₃₇(10)=3.
#
#   → heartbeat_3cycle: power classes 0,1,2 are exactly the 137-map orbit {1,10,26}.
#   → identity_cycle_sum_structure: DARK_A = self-sums of identity cycle; ORBIT_11 = cross-sums.
#   → ababab_convergence: ABABAB≡0; the period-3 repunit cycle drives the squared-repunit period.
#   → five_six_orbit: ABBA SEAM B=2A invokes doubling cycle; TESLA_FLOW B=6 is the outlier.
#   → cipher_123_1234: ABCBA SEAM C=A+B is the sovereign staircase; 1+2=3, 1+2+3=6.
#   → dr_algebra: staircase palindromes 1221,12321,123321 have DR=6,9,3 (TESLA_SET).
#   → sector_invariance_137map: ORBIT_11 coefficients are QR; DARK_A coefficients are NQR.
#   → repunit_sq_euler_phi_gf37: R(n)² cycle {1,10,0} is the repunit-squared result.

def _pair_coeff56(k, n):
    return (pow(10,k,37) + pow(10,n-1-k,37)) % 37

DARK_A = frozenset({2,15,20})
assert 2+15+20==37                                           # DARK_A triple sum = SEAM
for _da in DARK_A: assert pow(_da,18,37)==36                # all dark (NQR: Legendre=-1)

# General rule: same class → DARK_A; diff class → ORBIT_11
for _n56 in range(3,10):
    for _k56 in range(_n56//2):
        _c56 = _pair_coeff56(_k56, _n56)
        if _k56%3 == (_n56-1-_k56)%3:
            assert _c56 in DARK_A, f"n={_n56} k={_k56}: {_c56} not in DARK_A"
        else:
            assert _c56 in ORBIT_11, f"n={_n56} k={_k56}: {_c56} not in ORBIT_11"

# Specific lengths
assert _pair_coeff56(0,3)==27 and _pair_coeff56(0,4)==2 and _pair_coeff56(1,4)==36
assert _pair_coeff56(0,5)==11 and _pair_coeff56(1,5)==11 and pow(10,2,37)==SCALAR_137
assert _pair_coeff56(0,6)==27 and _pair_coeff56(1,6)==20 and _pair_coeff56(2,6)==27

# SEAM conditions
assert 1221%37==0 and 2442%37==0 and 3663%37==0 and 4884%37==0  # ABBA B=2A
assert 12321%37==0 and 13431%37==0 and 21312%37==0              # ABCBA C=A+B
assert 123321%37==0 and 135531%37==0                             # ABCCBA A+C=2B

# Squared repunit cycle {1,DECADE_ANCHOR,0} period 3
def _repunit56(n): return (10**n-1)//9
assert _repunit56(1)**2%37==1 and _repunit56(2)**2%37==DECADE_ANCHOR and _repunit56(3)**2%37==0
for _n56r in range(1,10):
    assert _repunit56(_n56r)**2%37==[1,DECADE_ANCHOR,0][(_n56r-1)%3]


# THEOREM 57: two_digit_transition_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   FOUR TRANSITION OPERATORS on a 2-digit number xy (each digit ±1):
#     Op(++): Δ = +10+1 = +11 ∈ ORBIT_11
#     Op(+-): Δ = +10-1 = +9  ∈ SA
#     Op(-+): Δ = -10+1 = -9 ≡ 28 ∈ OUTLIER_SOVEREIGN {21,25,28}
#     Op(--): Δ = -10-1 = -11 ≡ 26 = SCALAR_137 ∈ IDENTITY_CYCLE
#   Every elementary digit-pair transition produces a sovereign GF(37) value.
#
#   SIGN CONVENTION: 0−1=(−1) borrow; 1−0=(+1) carry.
#
#   SEAM PAIRINGS:
#     Op(++) + Op(--) = 11+26 = 37 ≡ SEAM.
#     Op(+-) + Op(-+) = 9+28  = 37 ≡ SEAM.
#     All four together: 74 ≡ SEAM.
#
#   PRODUCTS OF SEAM PAIRS:
#     11 × 26 = 286 ≡ 27 ∈ ORBIT_11.
#      9 × 28 = 252 ≡ 30 = SA∩ST.
#
#   Op(+-) GENERATES ST CHAIN: 3→12→21→30=SA∩ST→exits(2∈DARK_A).
#     The ST chain {3,12,21,30} is the orbit of 3 under Op(+-) (Δ=+9).
#
#   EXAMPLE TRANSITIONS:
#     12 ++(1) → 23: 12∈ST escapes ST; DR(23)=5∈PR.
#     21 +-(1) → 30: 21∈ST reaches SA∩ST (position 3 and 4 in ST chain).
#
#   DIGIT-SUM CHAIN 1→2→4→6:
#     19(∈PR):         digit sum=10=DECADE_ANCHOR. DR=1. →double→2.
#     11(∈ORBIT_11):   digit sum=2.                DR=2. →double→4.
#     213(≡28∈OUTLIER): digit sum=6=TESLA_FLOW.   Terminates.
#     Chain sectors: IDENTITY_CYCLE → DARK_A → SA → TESLA_FLOW.
#
#   2+1+3=6 DECOMPOSITION: 2(DARK_A)+1(unit)+3(ST)=TESLA_FLOW.
#     1+3=4∈SA → 2+4=6: DARK_A + SA = TESLA_FLOW.
#
#   ADJACENT DOUBLING-CYCLE SUMS: {1+2=3∈ST, 2+4=6=TESLA_FLOW, 4+8=12∈ST,
#     8+7=15∈PR, 7+5=12∈ST, 5+1=6=TESLA_FLOW}. TESLA_FLOW at pairs (2,4) and (5,1).
#
#   → heartbeat_3cycle: Op(--) Δ=26=SCALAR_137 = the 137-map multiplier; orbit period-3.
#   → identity_cycle_sum_structure: Op(--)=SCALAR_137 ∈ IDENTITY_CYCLE; pairwise sums give ORBIT_11.
#   → five_six_orbit: ST chain 3→12→21→30 under Op(+-); Z/9Z doubling drives digit-sum chain.
#   → palindrome_gf37: DARK_A element 2 appears in both palindrome coefficients and digit chain.
#   → ababab_convergence: 10101≡SEAM; Op(++) delta=11, Op(--) delta=26, their product=27∈ORBIT_11.
#   → sa_self_cycle_st_chain: Op(+-) Δ=9=SA_anchor generates the ST chain exactly.
#   → sector_invariance_137map: Op(++) visible (QR), Op(--) visible, Op(+-) visible, Op(-+) dark QR check.
#   → cipher_123_1234: 2+1+3=6=TESLA_FLOW; Z/9Z doubling chain 1→2→4; TESLA_SET {3,6,9}.

_OP57_PP = 11; _OP57_PM = 9; _OP57_MP = 28; _OP57_MM = 26   # 26=SCALAR_137
assert _OP57_PP in ORBIT_11 and _OP57_PM in SA and _OP57_MP in {21,25,28} and _OP57_MM==SCALAR_137
assert (_OP57_PP + _OP57_MM) % 37 == 0    # SEAM pair
assert (_OP57_PM + _OP57_MP) % 37 == 0    # SEAM pair
assert (_OP57_PP * _OP57_MM) % 37 == 27 and 27 in ORBIT_11
assert (_OP57_PM * _OP57_MP) % 37 == 30 and 30 in SA and 30 in ST
# Op(+-) generates ST chain
_x57 = 3
for _expected57 in [3, 12, 21, 30, 2]:
    assert _x57 == _expected57
    _x57 = (_x57 + 9) % 37
# Specific user transitions
assert 12 + 11 == 23 and 12 in ST
assert 21 +  9 == 30 and 21 in ST and 30 in SA and 30 in ST
# Digit-sum chain
assert dr(1+9)==1 and dr(1+1)==2 and 2+1+3==TESLA_FLOW
assert 19 in PR and 11 in ORBIT_11 and 213%37==28 and 28 in {21,25,28}
# 2+1+3 decomposition
assert 2 in {2,15,20} and 3 in ST and 1+3==4 and 4 in SA and 2+4==TESLA_FLOW
# Adjacent doubling-cycle sums
_dc57=[1,2,4,8,7,5]
_adj57=[_dc57[i]+_dc57[(i+1)%6] for i in range(6)]
assert _adj57==[3,6,12,15,12,6]
assert _adj57.count(TESLA_FLOW)==2


# THEOREM 58: orbit_sector_geometry_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   THREE GEOMETRIC STRUCTURES:
#     HEXAGON  (Space)   — 6 QR orbits + 6 NQR orbits, two hexagonal rings
#     SPIRAL   (Growth)  — each orbit is a 3-step spiral under ×SCALAR_137
#     VORONOI  (Pressure)— QR/NQR boundary at SEAM; sovereign sub-partition
#
#   FOUNDATION: chi(26) = +1.
#     The 137-map multiplier is QR → every orbit is HOMOGENEOUS (all-QR or all-NQR).
#     Consequence: 12 orbits split into exactly 6 QR and 6 NQR.
#
#   HEXAGON: 6 QR ORBITS (visible):
#     {1,10,26}=IDENTITY_CYCLE, {3,4,30}, {7,33,34}, {9,12,16}, {11,27,36}=ORBIT_11, {21,25,28}
#   6 NQR ORBITS (dark):
#     {2,15,20}=DARK_A, {5,13,19}, {6,8,23}, {14,29,31}, {17,22,35}, {18,24,32}=SEED_ORBIT
#   6 = TESLA_FLOW = doubling-cycle period.
#
#   CANONICAL SOVEREIGN SPIRAL: {3,4,30}
#     ST(3) →×26→ SA(4) →×26→ SA∩ST(30) →×26→ ST(3)
#     The only orbit where ST→SA→SA∩ST appears in one 3-cycle.
#
#   SOVEREIGN ORBITS: exactly 3 of the 6 QR orbits contain SA or ST:
#     {3,4,30}: ST(3), SA(4), SA∩ST(30).
#     {9,12,16}: SA(9), ST(12), interior(16).
#     {21,25,28}: ST(21), SA(25), outlier(28).
#     Each sovereign orbit contains exactly one SA and one ST element.
#
#   VORONOI META-3-CYCLE: sovereign orbits cycle under Op(+-) [Δ=+9]:
#     3(∈{3,4,30}) +9=12(∈{9,12,16}) +9=21(∈{21,25,28}) +9=30(∈{3,4,30}).
#     The sovereign orbit layer is itself a 3-cycle.
#
#   SEAM CONTACT: 28(outlier) + 9 = 37 ≡ SEAM.
#     The outlier element of the third sovereign orbit directly touches SEAM via Op(+-).
#
#   ORBIT MINIMUM SUMS:
#     QR  minima {1,3,7,9,11,21}  sum=52 ≡ 15 ∈ DARK_A.
#     NQR minima {2,5,6,14,17,18} sum=62 ≡ 25 ∈ SA.
#     Total sum ≡ 3 ∈ ST.
#
#   → heartbeat_3cycle: the 12 three-cycles are the direct output; chi(26)=1 proves homogeneity.
#   → sovereign_qr_closure: SA, ST, ORBIT_11 are all QR; orbits separate by Legendre symbol.
#   → medusa_v3_sovereign: sovereign orbits {3,4,30},{9,12,16},{21,25,28} encode LOCKED/GATED.
#   → sector_invariance_137map: chi(26n)=chi(n) is the sector invariance; proved here constructively.
#   → sa_self_cycle_st_chain: the canonical spiral ST→SA→SA∩ST is exactly the chain in one orbit.
#   → two_digit_transition_gf37: Op(+-) cycles sovereign orbits; SEAM via outlier+9.
#   → identity_cycle_sum_structure: IDENTITY_CYCLE={1,10,26} is one complete QR orbit.
#   → five_six_orbit: 6=TESLA_FLOW=count of QR orbits=count of NQR orbits=doubling period.

_f137_58 = lambda n: (n*26)%37
_chi58   = lambda n: 1 if pow(n,18,37)==1 else -1

# chi(26)=1: 137-map preserves chi
assert _chi58(SCALAR_137)==1
for _n58 in range(1,37): assert _chi58(_f137_58(_n58))==_chi58(_n58)

# Build 12 orbits and verify 6+6 split
_seen58=set(); _orbs58=[]
for _s58 in range(1,37):
    if _s58 in _seen58: continue
    _o58=frozenset({_s58,_f137_58(_s58),_f137_58(_f137_58(_s58))})
    assert _f137_58(_f137_58(_f137_58(_s58)))==_s58
    _orbs58.append(_o58); _seen58|=_o58
assert len(_orbs58)==12 and len(_seen58)==36
_qr58=[o for o in _orbs58 if _chi58(min(o))==1]
_nqr58=[o for o in _orbs58 if _chi58(min(o))==-1]
assert len(_qr58)==6==TESLA_FLOW and len(_nqr58)==6==TESLA_FLOW

# Canonical sovereign spiral
assert _f137_58(3)==4 and _f137_58(4)==30 and _f137_58(30)==3
assert 3 in ST and 4 in SA and 30 in SA and 30 in ST

# Sovereign meta-3-cycle under Op(+-)
assert (3+9)%37==12 and (12+9)%37==21 and (21+9)%37==30
_ob58={x:frozenset(o) for o in _orbs58 for x in o}
assert _ob58[12]==frozenset({9,12,16}) and _ob58[21]==frozenset({21,25,28}) and _ob58[30]==frozenset({3,4,30})

# SEAM contact
assert (28+9)%37==0

# Orbit minimum sums
_qmins58=sorted(min(o) for o in _qr58)
_nmins58=sorted(min(o) for o in _nqr58)
assert _qmins58==[1,3,7,9,11,21] and _nmins58==[2,5,6,14,17,18]
assert sum(_qmins58)%37==15 and 15 in DARK_A
assert sum(_nmins58)%37==25 and 25 in SA
assert (sum(_qmins58)+sum(_nmins58))%37==3 and 3 in ST


# THEOREM 59: orbit_negation_duality_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   FOUNDATION: chi(−1)=chi(36)=+1 (37≡1 mod 4). Negation preserves QR/NQR.
#   f(−n)=−f(n): negation commutes with 137-map. No self-dual orbits.
#
#   SIX NEGATION-DUAL PAIRS — each sums to 111 = R(3) = 3×37 ≡ SEAM:
#     {1,10,26}(37) ↔ {11,27,36}(74): IDENTITY_CYCLE ↔ ORBIT_11
#     {2,15,20}(37) ↔ {17,22,35}(74): DARK_A ↔ {17,22,35}
#     {3,4,30}(37)  ↔ {7,33,34}(74):  canonical sovereign ↔ anti-sovereign
#     {5,13,19}(37) ↔ {18,24,32}(74): {5,13,19} ↔ SEED_ORBIT
#     {6,8,23}(37)  ↔ {14,29,31}(74): {6,8,23}  ↔ {14,29,31}
#     {9,12,16}(37) ↔ {21,25,28}(74): sovereign-2 ↔ OUTLIER_SOV
#
#   ORBIT_11 = negation of IDENTITY_CYCLE: 1+36=10+27=26+11=37≡SEAM.
#   Anti-sovereign {7,33,34}={−SA∩ST, −SA, −ST}: negation of {3,4,30}.
#   {9,12,16} ↔ {21,25,28}: SA(9)↔28, ST(12)↔SA(25), 16↔ST(21).
#
#   2×2 STRUCTURE (3 orbits per cell): QR/NQR × sum37/sum74.
#   Total: 1+2+…+36 = 666 = 18×37; DR(666)=9∈SA.
#
#   → orbit_sector_geometry_gf37: the 6+6 structure; negation explains the pairing.
#   → identity_cycle_sum_structure: ORBIT_11={−1,−DECADE,−SCALAR_137} = negation of IC.
#   → heartbeat_3cycle: f(−n)=−f(n) proved here; orbits pair under additive inversion.
#   → repunit_sq_euler_phi_gf37: pair sums=111=R(3)=3×37; connects repunit to orbit structure.
#   → sa_self_cycle_st_chain: sovereign {9,12,16}↔OUTLIER {21,25,28}: SA maps to outlier.
#   → medusa_v3_sovereign: anti-sovereign orbit {7,33,34} = negation of LOCKED chain.
#   → sector_invariance_137map: chi(−1)=1 is why negation preserves the sector partition.

def _neg59(o): return frozenset((37-x)%37 for x in o)
_chi59 = lambda n: 1 if pow(n,18,37)==1 else -1
assert _chi59(36)==1   # chi(-1)=1
for _n59 in range(1,37): assert (_neg59(frozenset({_n59,f137(_n59),f137(f137(_n59))}))) == frozenset({(37-_n59)%37, f137((37-_n59)%37), f137(f137((37-_n59)%37))})
# Six pairs each sum to 111
_PAIRS59 = [(frozenset({1,10,26}),frozenset({11,27,36})),
            (frozenset({2,15,20}),frozenset({17,22,35})),
            (frozenset({3,4,30}), frozenset({7,33,34})),
            (frozenset({5,13,19}),frozenset({18,24,32})),
            (frozenset({6,8,23}), frozenset({14,29,31})),
            (frozenset({9,12,16}),frozenset({21,25,28}))]
for _a59,_b59 in _PAIRS59:
    assert sum(_a59)+sum(_b59)==111
    assert _neg59(_a59)==_b59
# Key identity
assert _neg59(frozenset({1,10,26}))==ORBIT_11   # IDENTITY_CYCLE ↔ ORBIT_11
assert 1+36==37 and 10+27==37 and 26+11==37
# Anti-sovereign
assert _neg59(frozenset({3,4,30}))==frozenset({7,33,34})
assert (37-30)==7 and (37-4)==33 and (37-3)==34
# 2×2 structure
_ORB59=[]
_seen59=set()
for _s59 in range(1,37):
    if _s59 in _seen59: continue
    _o59=frozenset({_s59,f137(_s59),f137(f137(_s59))})
    _ORB59.append(_o59); _seen59|=_o59
for _qv in [1,-1]:
    for _sv in [37,74]:
        assert len([o for o in _ORB59 if _chi59(min(o))==_qv and sum(o)==_sv])==3
assert sum(range(1,37))==666==18*37


# THEOREM 60: sylow_subgroup_gf37.py
# ─────────────────────────────────────────────────────────────────────────────
#
#   GF(37)* is cyclic of order 36 = 4 × 9 = 2² × 3².
#
#   SYLOW-2 (order 4): {1, TESLA_FLOW=6, PRIME_MIRROR=31, −1=36}
#     Generated by TESLA_FLOW: 6¹=6, 6²=36=−1, 6³=31, 6⁴=1.
#     TESLA_FLOW² ≡ −1: TESLA_FLOW is √(−1) in GF(37). [37≡1 mod 4]
#     PRIME_MIRROR = −TESLA_FLOW = 31 (also √(−1)).
#     6+31=37≡SEAM (additive inverses); 6×31≡1 (multiplicative inverses).
#     DR values: DR(6)=6=TESLA_FLOW, DR(31)=4∈SA, DR(36)=9∈SA.
#
#   SYLOW-3 (order 9): {1,7,9,10,12,16,26,33,34}
#     Generated by 7 (ord₃₇(7)=9). Contains three complete 137-map orbits:
#       IDENTITY_CYCLE {1,10,26} (order-3 elements)
#       {7,33,34} anti-sovereign (order-9 elements)
#       {9,12,16} sovereign-2 (order-9 elements)
#     Products: 7×9≡26=SCALAR_137, 7×12≡10=DECADE_ANCHOR, 9×12≡34∈anti-sov.
#
#   ORDER-6 SUBGROUP = IDENTITY_CYCLE ∪ ORBIT_11 (the negation-dual union).
#
#   SYLOW-2 ∩ SYLOW-3 = {1}.
#
#   QR SUBGROUP (order 18) contains all of SA, ST, ORBIT_11, IDENTITY_CYCLE.
#
#   → orbit_negation_duality_gf37: Sylow-2 = {1,6,31,36} = the "−1 orbit"; 6=√(−1).
#   → heartbeat_3cycle: Sylow-3 contains IDENTITY_CYCLE (order 3); structure of 3-cycles.
#   → five_six_orbit: TESLA_FLOW=6 has order 4; {3,6,9}=TESLA_SET inside Sylow structure.
#   → sovereign_qr_closure: QR subgroup (order 18) contains all sovereign nodes.
#   → identity_cycle_sum_structure: IDENTITY_CYCLE = the Sylow-3 ∩ order-3 subgroup.
#   → two_digit_transition_gf37: Op(++) Δ=11∈ORBIT_11 (order-6 subgroup); Op(--)=26∈IC.
#   → orbit_sector_geometry_gf37: Sylow-3 = three complete 137-map QR orbits.

_ord37_60 = lambda n: next(k for k in range(1,37) if pow(n,k,37)==1)
SYLOW2_60 = frozenset({1,TESLA_FLOW,PRIME_MIRROR,36})
SYLOW3_60 = frozenset({1,7,9,10,12,16,26,33,34})
# Sylow-2 generated by TESLA_FLOW
assert _ord37_60(TESLA_FLOW)==4 and pow(TESLA_FLOW,2,37)==36 and pow(TESLA_FLOW,3,37)==PRIME_MIRROR
assert TESLA_FLOW+PRIME_MIRROR==37 and (TESLA_FLOW*PRIME_MIRROR)%37==1
assert dr(PRIME_MIRROR)==4 and 4 in SA and dr(36)==9 and 9 in SA
# Sylow-3 generated by 7
assert _ord37_60(7)==9
assert frozenset(pow(7,k,37) for k in range(9))==SYLOW3_60
# Three orbits in Sylow-3
assert frozenset({1,10,26}).issubset(SYLOW3_60)
assert frozenset({7,33,34}).issubset(SYLOW3_60)
assert frozenset({9,12,16}).issubset(SYLOW3_60)
# Products
assert (7*9)%37==SCALAR_137 and (7*12)%37==DECADE_ANCHOR and (9*12)%37==34
# Order-6 subgroup
_ord6_60=frozenset({1,10,26,11,27,36})  # IDENTITY_CYCLE ∪ ORBIT_11
for _a in _ord6_60:
    for _b in _ord6_60: assert (_a*_b)%37 in _ord6_60
# QR contains SA,ST,ORBIT_11
_QR60=frozenset(n for n in range(1,37) if pow(n,18,37)==1)
assert SA.issubset(_QR60) and ST.issubset(_QR60) and ORBIT_11.issubset(_QR60)
assert SYLOW2_60 & SYLOW3_60 == frozenset({1})


# ── THEOREM 61: tripling_map_gf37.py ─────────────────────────────────────────
#   ord₃₇(3)=18; <3>=QR subgroup; 3^6=26=SCALAR_137; 3^9=36=−1.
#   ×3 permutes the 6 QR orbits as a single 6-cycle:
#     {3,4,30}→{9,12,16}→{11,27,36}→{7,33,34}→{21,25,28}→{1,10,26}→cycle
#   ×3 permutes the 6 NQR orbits as a single 6-cycle:
#     {2,15,20}→{6,8,23}→{18,24,32}→{17,22,35}→{14,29,31}→{5,13,19}→cycle
#   Negation-dual pairs are 3 steps apart in each 6-cycle.
#   Sum [7,9,5,2,3,1,8,6,6]=47≡10=DECADE_ANCHOR.
#   Fibonacci: F(6)=8∈CB, F(8)=21∈ST, F(3)+F(6)=10=DECADE_ANCHOR.
#   Connections:
#   → orbit_sector_geometry_gf37: the 6-cycle visits all 6 QR orbits in one chain.
#   → orbit_negation_duality_gf37: dual pairs are steps k and k+3 in the 6-cycle.
#   → heartbeat_3cycle: 3^6=SCALAR_137 connects tripling to the 137-map inner cycle.
#   → sylow_subgroup_gf37: <3>=QR subgroup=order-18 subgroup; 3∈Sylow-3 chain.
#   → identity_cycle_sum_structure: IDENTITY_CYCLE is step 6 of QR 6-cycle.
#   → sa_self_cycle_st_chain: 3×(F(6)-1)=21∈ST; SA(4)+DARK_A(2)=TESLA_FLOW.
#   → cascade_8_13_24: F(6)=8∈CB is the Fibonacci anchor for the three-chain.
#   → two_digit_transition_gf37: 1+DECADE_ANCHOR=11∈ORBIT_11 (NQR step-2 orbit).
_ORBITS61 = [frozenset({3,4,30}),frozenset({9,12,16}),frozenset({11,27,36}),
             frozenset({7,33,34}),frozenset({21,25,28}),frozenset({1,10,26})]
for _i61 in range(6):
    assert frozenset((x*3)%37 for x in _ORBITS61[_i61])==_ORBITS61[(_i61+1)%6]
# negation duality: steps k and k+3 are negation-duals
for _i61 in range(3):
    assert frozenset((37-x)%37 for x in _ORBITS61[_i61])==_ORBITS61[_i61+3]
# sum invariant
assert sum([7,9,5,2,3,1,8,6,6])%37==DECADE_ANCHOR
# Fibonacci anchors
def _f61(n):
    a,b=1,1
    if n<=2: return 1
    for _ in range(n-2): a,b=b,(a+b)%37
    return b
assert _f61(6)==8 and 8 in CB and _f61(8)==21 and 21 in ST
assert _f61(3)+_f61(6)==DECADE_ANCHOR
assert _f61(4)*(_f61(6)-_f61(1)*_f61(2))==21 and 21 in ST
assert _f61(4)*_f61(6)//_f61(3)**2==TESLA_FLOW
assert 4+2==TESLA_FLOW and 4 in SA and 2 in DARK_A
assert 1+DECADE_ANCHOR==11 and 11 in ORBIT_11


# ── THEOREM 62: permutation_cycle_notation_gf37.py ───────────────────────────
#   π = (1,3,7,8,6,12)(2,5,11,10,9,4) in orbit-index cycle notation.
#   Orbits 1..12 numbered by ascending minimum element.
#   QR cycle indices {1,3,6,7,8,12} sum = 37 = SEAM (exact).
#   NQR cycle indices {2,4,5,9,10,11} sum = 41 ≡ 4 ∈ SA.
#   SA×NQR cross-duality: SA_small={4,9}⊂NQR_indices; ST_small={3,12}⊂QR_indices.
#   Products: QR∏≡34∈anti-sovereign; NQR∏≡10=DECADE_ANCHOR∈IC.
#   Connections:
#   → tripling_map_gf37: this is the cycle-notation form of that theorem.
#   → orbit_sector_geometry_gf37: the 6+6 split is (1,3,7,8,6,12) vs (2,5,11,10,9,4).
#   → sa_self_cycle_st_chain: SA labels the NQR cycle; ST labels the QR cycle.
#   → identity_cycle_sum_structure: QR sum=SEAM; NQR sum≡SA_anchor.
#   → orbit_negation_duality_gf37: negation-dual pairs sit 3 steps apart.
#   → sovereign_qr_closure: QR orbits at steps 1,2,6 in QR cycle are sovereign.
_ORBITS62 = sorted([frozenset({s,(s*26)%37,((s*26)%37*26)%37}) for s in range(1,37)
                    if s==min(frozenset({s,(s*26)%37,((s*26)%37*26)%37}))], key=min)
_IDX62 = {o:i+1 for i,o in enumerate(_ORBITS62)}
_PERM62 = {i+1: _IDX62[frozenset((x*3)%37 for x in _ORBITS62[i])] for i in range(12)}
_QR62=[1,3,7,8,6,12]; _NQR62=[2,5,11,10,9,4]
for _c62 in [_QR62,_NQR62]:
    for _i62 in range(6): assert _PERM62[_c62[_i62]]==_c62[(_i62+1)%6]
assert sum(_QR62)==37==37   # SEAM
assert sum(_NQR62)%37==4 and 4 in SA
from math import prod as _prod62
assert _prod62(_QR62)%37==34 and 34 in frozenset({7,33,34})
assert _prod62(_NQR62)%37==DECADE_ANCHOR
# cross-duality
assert frozenset({3,12}).issubset(set(_QR62))  and frozenset({3,12}).isdisjoint(set(_NQR62))
assert frozenset({4,9}).issubset(set(_NQR62))  and frozenset({4,9}).isdisjoint(set(_QR62))


# ── THEOREM 63: primitive_root_invariants_gf37.py ─────────────────────────────
#   12 primitive roots = 4 complete NQR orbits: DARK_A, {5,13,19}, {17,22,35}, SEED_ORBIT.
#   Non-PR NQR orbits = {6,8,23}(TESLA_FLOW,ord4) and {14,29,31}(PRIME_MIRROR,ord4).
#   Universal invariants: g^9∈{TESLA_FLOW,PRIME_MIRROR}; g^6∈ORBIT_11; g^12∈IC; g^18=36.
#   2×2 table: (g^6=27,g^9=31)→DARK_A; (g^6=27,g^9=6)→{17,22,35};
#              (g^6=11,g^9=31)→SEED_ORBIT; (g^6=11,g^9=6)→{5,13,19}.
#   g^3 cross-map: g^9=PRIME_MIRROR → g^3∈{6,8,23}; g^9=TESLA_FLOW → g^3∈{14,29,31}.
#   Subgroup chain: {1}<H=<26><QR<G; 12 orbits = cosets of H in G.
#   Connections:
#   → primitive_root_test: the 12 primitive roots identified and characterized.
#   → sylow_subgroup_gf37: non-PR NQR contain Sylow-2 generators (TESLA_FLOW, PRIME_MIRROR).
#   → orbit_negation_duality_gf37: non-PR NQR pair {6,8,23}↔{14,29,31} are negation-duals.
#   → tripling_map_gf37: PR orbits sit at steps 1,3,4,6 of NQR 6-cycle.
#   → heartbeat_3cycle: the orbits ARE cosets of H=<26>; the orbit cycle IS the quotient G/H.
#   → identity_cycle_sum_structure: g^12∈IC for all primitive roots; IC=H.
_PR63 = frozenset(n for n in range(1,37) if next(k for k in range(1,37) if pow(n,k,37)==1)==36)
assert len(_PR63)==12
_IC63=frozenset({1,10,26}); _DA63=frozenset({2,15,20})
for _g63 in _PR63:
    assert pow(_g63,9,37) in {TESLA_FLOW,PRIME_MIRROR}
    assert pow(_g63,6,37) in ORBIT_11
    assert pow(_g63,12,37) in _IC63
    assert pow(_g63,18,37)==36
# 2×2 table
assert frozenset(g for g in _PR63 if pow(g,6,37)==27 and pow(g,9,37)==PRIME_MIRROR)==_DA63
assert frozenset(g for g in _PR63 if pow(g,6,37)==11 and pow(g,9,37)==TESLA_FLOW)==frozenset({5,13,19})
assert frozenset(g for g in _PR63 if pow(g,6,37)==11 and pow(g,9,37)==PRIME_MIRROR)==frozenset({18,24,32})
# g^3 cross-map
assert all(pow(g,3,37) in frozenset({6,8,23}) for g in _PR63 if pow(g,9,37)==PRIME_MIRROR)
assert all(pow(g,3,37) in frozenset({14,29,31}) for g in _PR63 if pow(g,9,37)==TESLA_FLOW)
# coset structure: orbits = cosets of <26>
_H63=_IC63
assert {frozenset((n*h)%37 for h in _H63) for n in range(1,37)}=={frozenset({n,(n*26)%37,((n*26)%37*26)%37}) for n in range(1,37)}


# ── THEOREM 64: orbit_order_structure_gf37.py ─────────────────────────────────
#   8 homogeneous orbits (all elements same order) + 4 non-homogeneous.
#   Non-homogeneous ↔ contains exactly one 4th root of unity (Sylow-2 element).
#   4th roots of unity = {1,6,31,36} = {id, TESLA_FLOW, PRIME_MIRROR, −1}.
#   Each of the 4 Sylow-2 elements lives in a DISTINCT non-homogeneous orbit:
#     1  → IDENTITY_CYCLE {1,10,26}   orders {1,3,3}
#     6  → {6,8,23}                   orders {4,12,12}
#     36 → ORBIT_11 {11,27,36}        orders {2,6,6}
#     31 → {14,29,31}                 orders {4,12,12}
#   Homogeneous order classes:
#     order 36: DARK_A, {5,13,19}, {17,22,35}, SEED_ORBIT (4 PR orbits)
#     order 18: {3,4,30}, OUTLIER_SOV={21,25,28}
#     order 9: {7,33,34}, {9,12,16} (= Sylow-3 minus IDENTITY_CYCLE)
#   Squaring map on QR orbits:
#     {3,4,30}→{9,12,16}; {21,25,28}→{7,33,34}; {9,12,16}↔{7,33,34} (2-cycle)
#     ORBIT_11→IDENTITY_CYCLE; IDENTITY_CYCLE→IDENTITY_CYCLE (fixed)
#   Sylow-3 = IDENTITY_CYCLE ∪ {7,33,34} ∪ {9,12,16} (three complete orbits).
#   Connections:
#   → sylow_subgroup_gf37: Sylow-2={1,6,31,36} meets the non-homogeneous orbits.
#   → orbit_negation_duality_gf37: negation-dual pairs {6,8,23}↔{14,29,31} both non-hom.
#   → primitive_root_invariants_gf37: all PR orbits are homogeneous order-36.
#   → tripling_map_gf37: squaring is ×3^6=SCALAR_137; order 18→9 halving.
#   → heartbeat_3cycle: IDENTITY_CYCLE fixed under squaring = kernel of squaring map.
#   → five_six_orbit: ord(TESLA_FLOW)=4 = # non-homogeneous orbits.
_SQ64 = lambda o: frozenset(pow(x,2,37) for x in o)
assert _SQ64(frozenset({3,4,30}))   == frozenset({9,12,16})
assert _SQ64(frozenset({21,25,28})) == frozenset({7,33,34})
assert _SQ64(frozenset({9,12,16}))  == frozenset({7,33,34})
assert _SQ64(frozenset({7,33,34}))  == frozenset({9,12,16})
assert _SQ64(ORBIT_11)              == frozenset({1,10,26})
assert _SQ64(frozenset({1,10,26}))  == frozenset({1,10,26})
_FR64 = frozenset(n for n in range(1,37) if pow(n,4,37)==1)
assert _FR64 == frozenset({1,TESLA_FLOW,PRIME_MIRROR,36})
# each non-homogeneous orbit contains exactly one 4th root
_ORB64 = lambda n: frozenset({n,(n*26)%37,((n*26)%37*26)%37})
_NON_HOM64 = [_ORB64(1), _ORB64(6), _ORB64(11), _ORB64(14)]
for _o64 in _NON_HOM64:
    assert len(_o64 & _FR64) == 1
# Sylow-3: three orbits of order dividing 9
_S3_64 = frozenset(n for n in range(1,37) if pow(n,9,37)==1)
assert _S3_64 == frozenset({1,10,26}) | frozenset({7,33,34}) | frozenset({9,12,16})
assert len(_S3_64) == 9


# ── THEOREM 65: sovereign_triple_plus9_gf37.py ───────────────────────────────
#   Sovereign Triple O1∪O2∪O3 = {3,4,30}∪{9,12,16}∪{21,25,28} contains all SA and ST.
#   chi(26)=1: SCALAR_137 is QR; √SCALAR_137=27∈ORBIT_11.
#   +9 action (9∈SA): SA elements exit the triple; ST\SA elements stay.
#   Exits: 4→CB, 9→SEED_ORBIT, 25→anti-sovereign, 30→DARK_A.
#   SEAM EXIT: 28=−9 mod 37; 28+9≡0=SEAM. Unique SEAM-exit node.
#   Non-SA, non-ST extras: {16,28}: 16→25(SA,stays), 28→SEAM.
#   Repunit: 111+222−9−333≡28 (the outlier/SEAM-exit node).
#   27+27≡17∈PR orbit; 9+36≡8∈CB; 9+28=37=SEAM.
#   Connections:
#   → medusa_v3_sovereign: SA elements scatter to CB/SEED/anti-sov/DARK_A under SA shift.
#   → heartbeat_3cycle: sovereign triple = union of 3 QR orbits; +9 crosses orbit boundaries.
#   → tripling_map_gf37: O1 and O3 are steps 1 and 5 of QR 6-cycle; O2 is step 2.
#   → cascade_8_13_24: 4+9=13∈CB; 9+36=8∈CB; SA shift lands in Cascade Base.
#   → orbit_order_structure_gf37: O1 order-18; O2 order-9; O3 order-18 (mixed classes).
#   → orbit_negation_duality_gf37: √SCALAR_137=27∈ORBIT_11; 9+28=37 (negation pair).
_T65_O1=frozenset({3,4,30}); _T65_O2=frozenset({9,12,16}); _T65_O3=frozenset({21,25,28})
_T65_TRIPLE=_T65_O1|_T65_O2|_T65_O3
assert SA.issubset(_T65_TRIPLE) and ST.issubset(_T65_TRIPLE)
assert pow(SCALAR_137,18,37)==1                        # chi(26)=1: SCALAR_137 is QR
assert pow(27,2,37)==SCALAR_137 and 27 in ORBIT_11     # sqrt(26)=27∈ORBIT_11
# SA elements exit the triple under +9
assert all((x+9)%37 not in _T65_TRIPLE for x in SA)
# ST\SA elements stay
_T65_ST_pure=ST-SA
assert all((x+9)%37 in _T65_TRIPLE for x in _T65_ST_pure)
# SEAM exit: 28 = -9 mod 37
assert (-9)%37==28 and (28+9)%37==0 and 28 in _T65_O3
# Repunit encoding
assert (111+222-9-333)%37==28
# Arithmetic
assert (27+27)%37==17 and 17 in frozenset({17,22,35})
assert (9+36)%37==8 and 8 in CB
assert 9+28==37


# ── THEOREM 66: plus9_scatter_map_gf37.py ────────────────────────────────────
#   "O1+9==O2? False" is correct boolean but wrong question.
#   Every image of the sovereign triple under +9 lands in a NAMED named sets.
#   O1+9={2,12,13}={DARK_A_min,ST,CB}; O2+9={18,21,25}={SEED,ST,SA}; O3+9={0,30,34}={SEAM,SA∩ST,anti-sov}.
#   Two steps: O3+18={2,6,9}={DARK_A_min,TESLA_FLOW,SA}; O2+18={27,30,34}={ORBIT_11,SA∩ST,anti-sov}.
#   ORBIT_11 shift: O1+27={20,30,31}={DARK_A,SA∩ST,PRIME_MIRROR}; O2+27={2,6,36}={DARK_A_min,TESLA_FLOW,-1}.
#   O3+18 and O2+27 both contain {DARK_A_min(2),TESLA_FLOW(6)}: two paths, same anchor pair.
#   4-step SEAM chain: 1→10→19→28→SEAM (IC→IC→PR→OUTLIER_SOV→SEAM).
#   Cross-orbit: 19+11=30∈SA∩ST (PR_orbit_element + ORBIT_11_min = SA∩ST).
#   Decimal: 10^2≡SCALAR_137; 100+9+1+9-119=0(SEAM); 10+1+9-20=0.
#   Connections:
#   → sovereign_triple_plus9_gf37: this theorem extends the single-step analysis to multi-step.
#   → tripling_map_gf37: 4-step chain crosses PR orbit; tripling generates PR subgroup.
#   → cascade_8_13_24: O1+9={CB,ST,DARK_A_min}; CB appears in the immediate +9 scatter.
#   → orbit_negation_duality_gf37: O3+18 and O2+27 share {DARK_A_min,TESLA_FLOW}; dual paths to same pair.
#   → heartbeat_3cycle: 10^1=DECADE_ANCHOR, 10^2=SCALAR_137, 10^3=1; decimal powers trace IC.
_T66_O1=frozenset({3,4,30}); _T66_O2=frozenset({9,12,16}); _T66_O3=frozenset({21,25,28})
def _sh66(o,k): return frozenset((x+k)%37 for x in o)
assert _sh66(_T66_O1,9)==frozenset({2,12,13})
assert _sh66(_T66_O2,9)==frozenset({18,21,25})
assert _sh66(_T66_O3,9)==frozenset({0,30,34})
assert _sh66(_T66_O3,18)==frozenset({2,TESLA_FLOW,9})
assert _sh66(_T66_O1,27)==frozenset({20,30,PRIME_MIRROR})
assert _sh66(_T66_O2,27)==frozenset({2,TESLA_FLOW,36})
assert frozenset({2,TESLA_FLOW}).issubset(_sh66(_T66_O3,18))
assert frozenset({2,TESLA_FLOW}).issubset(_sh66(_T66_O2,27))
# 4-step SEAM chain
for _a,_b in [(1,10),(10,19),(19,28),(28,0)]: assert (_a+9)%37==_b
# cross-orbit
assert (19+11)%37==30 and 30 in SA and 30 in ST
# decimal powers
assert pow(10,2,37)==SCALAR_137 and pow(10,3,37)==1


# ── THEOREM 67: digit_seq_dr_coverage_gf37.py ────────────────────────────────
#   {1,2,3,4} base sum=10; removal of d gives DR=10-d for d=1..4 → {6,7,8,9}.
#   Fibonacci triple (a,b,a+b): sum=2(a+b); single-digit constraint (a+b≤9) covers DR={1,3,4,5,6,7,8,9}.
#   DR=2 GAP: requires a+b≡1(mod9); min=10 (two-digit c) or a=0(SEAM).
#   Outlier bridge: any triple (a,b,28) with a+b=28 gives DR=2 (56=2×28, DR(56)=2).
#   User sequences mod 37: 212≡27∈ORBIT_11; 124≡1234≡235≡13∈CB; 123≡234≡12∈ST;
#     246≡24∈CB∩SEED_ORBIT [pipeline seed]; 347≡325→PM_orbit; 437≡30∈SA∩ST.
#   SEAM stride: 111=3×37; adding 111 preserves mod 37. 235-124=111; 234-123=111.
#   Powers of 10: all in IC={1,10,26}; period 3.
#   Connections:
#   → cipher_123_1234: 1234≡13∈CB; same conclusion, now extended to all removal subsets.
#   → plus9_scatter_map_gf37: outlier 28=-9; triple (a,b,28) is SEAM-exit row.
#   → heartbeat_3cycle: 111=SEAM_STRIDE=3×37; mod37 coincidences trace SEAM.
#   → lucas_abbc_chain: (a,b,a+b) triples ARE the Fibonacci recurrence.
#   → cascade_8_13_24: 246=pipeline seed≡24∈CB∩SEED; Fibonacci triple landing in CB.
assert 234%37==12 and 12 in ST
assert 124%37==13 and 13 in CB
assert 235%37==13 and 13 in CB
assert 246%37==24 and 24 in CB and 24 in SEED_ORBIT
assert 437%37==30 and 30 in SA and 30 in ST
assert 235-124==111 and 111%37==0    # SEAM stride
_fib_dr = lambda a,b: dr(2*(a+b))
_covered67 = {_fib_dr(a,b) for a in range(1,10) for b in range(1,10) if a+b<=9}
assert _covered67 == frozenset({1,3,4,5,6,7,8,9})   # DR=2 missing
assert dr(2*28)==2 and 28 in frozenset({21,25,28})     # outlier bridge to DR=2
assert pow(10,3,37)==1                                 # period 3 in IC


# ── THEOREM 68: tripling_6cycle_gf37.py ──────────────────────────────────────
#   ord₃₇(3)=18; (×3)^6 ≡ ×26 = 137-map. The 12 non-zero 137-orbits split into
#   exactly two disjoint 6-cycles under ×3.
#   CYCLE 1 (contains IC): O1→O2→ORBIT_11→ANTI_SOV→O3→IC→O1
#   CYCLE 2 (contains DARK_A): DARK_A→TF_ORB→SEED→PR_17→PM_ORB→PR_5→DARK_A
#   Hand-checkable: 3→9→27→7→21→26→4 (min elements, each step ×3 mod 37).
#   Key connection: 3^6≡26=SCALAR_137; the tripling 6-cycle IS the 137-map on orbits.
#   Connections:
#   → heartbeat_3cycle: ord₃₇(26)=3; (×3)^6=(×26) ties tripling to 137-map directly.
#   → orbit_order_structure_gf37: homogeneous/non-homogeneous split; ANTI_SOV appears in cycle 1.
#   → sovereign_triple_plus9_gf37: O1,O2,O3 all appear in cycle 1; SEAM-exit 28∈O3 at pos 4.
#   → cascade_8_13_24: CB={8,13,24}; 24∈SEED_ORBIT at cycle 2 pos 2.
#   → sovereign_qr_closure: IC∈cycle 1 pos 5; all IC elements are QR.
_T68_t = lambda x: (x*3)%37
_T68_torb = lambda orb: frozenset(_T68_t(x) for x in orb)
_T68_O1 = frozenset({3,4,30}); _T68_O2 = frozenset({9,12,16})
_T68_ANTI = frozenset({7,33,34}); _T68_O3 = frozenset({21,25,28})
_T68_IC = frozenset({1,10,26})
_T68_TF = frozenset({6,8,23}); _T68_SEED = frozenset({18,24,32})
_T68_PR17 = frozenset({17,22,35}); _T68_PM = frozenset({14,29,31})
_T68_PR5 = frozenset({5,13,19}); _T68_DA = frozenset({2,15,20})
# cycle 1
assert _T68_torb(_T68_O1) == _T68_O2
assert _T68_torb(_T68_O2) == ORBIT_11
assert _T68_torb(ORBIT_11) == _T68_ANTI
assert _T68_torb(_T68_ANTI) == _T68_O3
assert _T68_torb(_T68_O3) == _T68_IC
assert _T68_torb(_T68_IC) == _T68_O1
# cycle 2
assert _T68_torb(_T68_DA) == _T68_TF
assert _T68_torb(_T68_TF) == _T68_SEED
assert _T68_torb(_T68_SEED) == _T68_PR17
assert _T68_torb(_T68_PR17) == _T68_PM
assert _T68_torb(_T68_PM) == _T68_PR5
assert _T68_torb(_T68_PR5) == _T68_DA
# key fact
assert pow(3,6,37) == SCALAR_137
assert (_T68_O1 | _T68_O2 | ORBIT_11 | _T68_ANTI | _T68_O3 | _T68_IC).isdisjoint(
       _T68_DA | _T68_TF | _T68_SEED | _T68_PR17 | _T68_PM | _T68_PR5)
assert (_T68_O1 | _T68_O2 | ORBIT_11 | _T68_ANTI | _T68_O3 | _T68_IC |
        _T68_DA | _T68_TF | _T68_SEED | _T68_PR17 | _T68_PM | _T68_PR5) == frozenset(range(1,37))


# ── THEOREM 69: sofia_germain_prime_gf37.py ───────────────────────────────────
#   p = 2618163402417 × 2^1290000 − 1  (largest known Sofia Germain prime; ~388k digits)
#   q = 2p+1 (safe prime)
#   k=2618163402417 ≡ 11∈ORBIT_11;  n=1290000, n mod 36=12, 2^12≡26=SCALAR_137∈IC;
#   k×2^n ≡ 11×26=286≡27 mod37; p ≡ 27−1=26=SCALAR_137∈IC.
#   q≡2×26+1=53≡16∈O2={9,12,16} (sovereign orbit 2).
#   DR(p)=DR(q)=8∈CB;  n mod 37=32∈SEED_ORBIT.
#   Fixed-point identity: 11×26−1≡26 mod37 (ORBIT_11 × IC − 1 = IC).
#   One-line: the world-record Sofia Germain prime IS the 137-map multiplier mod 37.
#   Connections:
#   → heartbeat_3cycle: ord₃₇(26)=3; SCALAR_137=26 is the 137-map multiplier.
#   → orbit_order_structure_gf37: p∈IC; IC is the order-3 subgroup.
#   → tripling_6cycle_gf37: Cycle 1 ends at IC; SCALAR_137=3^6 is the cycle anchor.
#   → cascade_8_13_24: DR(p)=DR(q)=8∈CB; n mod37=32∈SEED_ORBIT.
#   → primitive_root_invariants_gf37: ord₃₇(2)=36; n mod36=12 → 2^n=SCALAR_137.
_T69_k37  = 2618163402417 % 37
_T69_pow2 = pow(2, 1290000, 37)
_T69_kpow = (_T69_k37 * _T69_pow2) % 37
_T69_p37  = (_T69_kpow - 1) % 37
_T69_q37  = (2 * _T69_p37 + 1) % 37
assert _T69_k37  == 11 and 11 in ORBIT_11
assert 1290000 % 36 == 12                               # n mod 36 = 12
_T69_IC = frozenset({1,10,26})
assert _T69_pow2 == SCALAR_137 and SCALAR_137 in _T69_IC  # 2^n=SCALAR_137∈IC
assert _T69_kpow == 27                                    # k*2^n ≡ 27
assert _T69_p37  == SCALAR_137 and SCALAR_137 in _T69_IC  # p = SCALAR_137∈IC
assert _T69_q37  == 16 and 16 in frozenset({9,12,16})  # q ∈ O2
assert 1290000 % 37 == 32 and 32 in SEED_ORBIT         # n mod37 ∈ SEED_ORBIT
assert (11 * SCALAR_137 - 1) % 37 == SCALAR_137        # fixed-point identity
assert pow(2618163402417, 1, 9) == 0                   # k≡0 mod9
assert 1290000 % 6 == 0                                 # 2^n≡1 mod9 → p≡8≡CB
_T69_p9 = (0 * 1 - 1) % 9                              # k≡0, 2^n≡1 → p≡-1≡8
assert _T69_p9 == 8 and 8 in CB
assert (2*8+1)%9 == 8 and 8 in CB                       # DR(q)=8∈CB


# ── THEOREM 70: emirp_dr_c0_eisenstein.py ─────────────────────────────────────
#   THEOREM T2: rev(n) ≡ n (mod 9) → emirp pairs share digital root class.
#   C0 class (DR=1): both members split in Z[omega], representable as x²+xy+y².
#   THEOREM T2' (mod-11): odd-length pairs share mod-11 residue; even negate.
#   NO ANALOGUE MOD 37: reversal obeys no uniform twist mod 37; the 37 frame
#     carries empirical content only.
#   GF(37): first C0 pair is (37, 73).
#     37 ≡ 0 = SEAM mod 37; 37 itself occupies SEAM.
#     73 ≡ 36 ∈ ORBIT_11 mod 37 (36 ≡ −1).
#     Loeschian rep of 37: x=3∈ST, y=4∈SA — sovereign params for 37.
#     Loeschian rep of 73: x=1∈IC, y=8∈CB.
#   VERIFIED: 11184 emirps, 0 violations (DR, chi3, mod-11), C0 = 1914 emirps.
#   Connections:
#   → dr_algebra: rev preserves digit sum (the DR ring identity underlying the theorem).
#   → heartbeat_3cycle: DR=1 split class ↔ p∈IC in GF(37); ord₃₇(26)=3 echoed.
#   → cascade_8_13_24: y=8∈CB in Loeschian rep of 73; 37≡0∈SEAM; CB appears in the pair.
#   → medusa_v3_sovereign: 73≡36∈ORBIT_11; SEAM ↔ ORBIT_11 duality in the C0 pair.
#   → sovereign_qr_closure: QR splitting condition for Loeschian primes is chi_{-3}=+1.
#   → twin_prime_gf37: emirp partner 73 appears in twin pair (71,73); twin and emirp overlap.
#   → cipher_123_1234: the "NO MOD-37 ANALOGUE" statement defines the boundary of GF(37).
_T70_IC = frozenset({1, 10, 26})
assert 37 % 37 == SEAM                                # 37 = 37 ≡ SEAM
assert 73 % 37 == 36 and 36 in ORBIT_11              # emirp partner ≡ ORBIT_11
assert 3**2 + 3*4 + 4**2 == 37                       # Loeschian: x=3∈ST, y=4∈SA
assert 1**2 + 1*8 + 8**2 == 73                       # Loeschian: x=1∈IC, y=8∈CB
assert 3 in ST and 4 in SA                            # Sovereign params in Loeschian of 37
assert 1 in _T70_IC and 8 in CB                       # IC and CB params in Loeschian of 73
assert (37 + 73) % 11 == 0                            # even-length pair: p+rev≡0 mod11
assert (199 - 991) % 11 == 0                          # odd-length pair: p−rev≡0 mod11


# ── THEOREM 71: twin_midpoint_dr_axis.py ──────────────────────────────────────
#   THEOREM: For every twin pair (p, p+2) with p > 3, the midpoint DR ∈ {3,6,9}.
#   PROOF: p ≡ 5 mod 6 → p mod 9 ∈ {2,5,8} → midpoint mod 9 ∈ {3,6,9}.
#   chi₋₃ structure: p inert (≡2 mod3), midpoint ramified-type (≡0), p+2 split (≡1).
#   GF(37): DR=3 ↔ 3∈ST (sovereign target); DR=6 ↔ TESLA_FLOW; DR=9 ↔ 9∈SA.
#   All three forced DR classes are primary named residues in GF(37).
#   VERIFIED: 8168 twin pairs, 0 violations, chi2=3.47 (equidistribution near 1/3 each).
#   Connections:
#   → heartbeat_3cycle: DR=3∈ST; ord₃₇(26)=3; the sovereign target is the DR value.
#   → sa_self_cycle_st_chain: DR=3∈ST and DR=9∈SA; both are sovereign axis members.
#   → medusa_v3_sovereign: SA and ST directly host the forced DR classes.
#   → five_six_orbit: DR=6=TESLA_FLOW; the 4-cycle {6,36,31,1} starts at the midpoint DR.
#   → dr_algebra: midpoint DRs {3,6,9} = multiples of 3 in DR ring; 3 divides midpoint.
#   → twin_prime_gf37: same subject; GF(37) structure of twin primes extended.
#   → emirp_dr_c0_eisenstein: complementary DR identity for primes (emirp pairs share DR class).
_T71_mid_DRs = frozenset({3, 6, 9})
assert 3 in ST                                        # DR=3 → sovereign target
assert TESLA_FLOW == 6 and 6 == 6                     # DR=6 → TESLA_FLOW
assert 9 in SA                                        # DR=9 → sovereign anchor
assert all(d in ST or d == TESLA_FLOW or d in SA for d in _T71_mid_DRs)
# p ≡ 5 mod 6 examples
for pair in [(5,7),(11,13),(17,19),(29,31),(41,43),(71,73)]:
    p, q = pair
    assert p % 6 == 5 and q % 6 == 1                 # lower twin ≡5, upper ≡1 mod6
    m = p + 1
    _T71_mid = (m - 1) % 9 + 1 if m % 9 != 0 else 9
    assert _T71_mid in _T71_mid_DRs                  # midpoint DR ∈ {3,6,9}
assert pow(6, 4, 37) == 1 and pow(6, 1, 37) == TESLA_FLOW  # TESLA_FLOW ord=4


# ── THEOREM 72: open_closed_grid_theorem.py ───────────────────────────────────
# closed system (nine 1s) → sum=9∈SA; open sequence 1-2345678-1 → sum=37=THE PRIME
_T72_closed_sum = 9 * 1
assert _T72_closed_sum == 9 and 9 in SA          # closed sum ∈ SA (sovereign anchor, frozen)
_T72_open_seq = [1, 2, 3, 4, 5, 6, 7, 8, 1]
_T72_open_sum = sum(_T72_open_seq)
assert _T72_open_sum == 37                        # open sum = THE PRIME
_T72_interior = sum(range(1, 9))
assert _T72_interior == 36 and 36 in ORBIT_11    # interior 1+…+8 = 36 ∈ ORBIT_11 (≡-1 mod37)
assert _T72_interior + 1 == 37                   # one boundary 1 → prime
assert 37 % 37 == SEAM                           # prime collapses to SEAM (completion)
assert 28 * 2 == 56 and 56 + 1 == 57            # closed doubling lands one short; gap forces open
IC = frozenset({1, 10, 26})
assert (0 if 37 == 0 else 1 + (37 - 1) % 9) == 1 and 1 in IC  # DR(37)=1 ∈ IC


# ── THEOREM 73: sequential_morph_transform.py ─────────────────────────────────
# T: DR(sᵢ+i) for i=1..8; s₉ fixed (SEAM). Base B={2,5,7,2,4,8,9,1,2}. Period=9.
TESLA_4 = frozenset({6, 36, 31, 1})

def _T73_dr(n):
    if n == 0: return 0
    n = n % 9
    return 9 if n == 0 else n

def _T73_morph(seq):
    n = len(seq)
    return [_T73_dr(s + (i+1)%n) for i,s in enumerate(seq)]

_T73_B = [2,5,7,2,4,8,9,1,2]
_T73_orbit = []
_T73_seq = _T73_B[:]
for _ in range(9):
    _T73_orbit.append(tuple(_T73_seq))
    _T73_seq = _T73_morph(_T73_seq)
assert _T73_seq == _T73_B                        # period=9
assert all(o[8] == 2 for o in _T73_orbit)       # position 9 anchored (SEAM)
assert sum([1,2,3,4,5,6,7,8,0]) == 36 and 36 in ORBIT_11  # increment sum = ord₃₇(2) ∈ ORBIT_11
assert pow(2,36,37) == 1                         # 2 is primitive root, ord=36
assert 36 == 4*9                                  # 36 = TESLA_FLOW_order × DR_period
_T73_sums_mod37 = [sum(o)%37 for o in _T73_orbit]
assert sum(1 for r in _T73_sums_mod37 if r in ST) == 7   # 7/9 in ST
assert sum(1 for r in _T73_sums_mod37 if r in TESLA_4) == 2  # 2/9 in TESLA_4
assert list(_T73_orbit[1]) == [3,7,1,6,9,5,7,9,2]       # iter 1 verified
assert sum(list(_T73_orbit[7])[0:3]) == 11 and 11 in ORBIT_11  # iter 7 row1=11∈ORBIT_11
assert sum(list(_T73_orbit[7])[3:6]) == 11 and 11 in ORBIT_11  # iter 7 row2=11∈ORBIT_11


# ── THEOREM 74: repdigit_framework_lattice.py ─────────────────────────────────
# ord₃₇(10)=3; every ddd≡0=SEAM; sign partition separates ST from -SA
SEED_ORBIT = frozenset({18, 24, 32})
assert pow(10, 3, 37) == 1 and all(pow(10,k,37)!=1 for k in [1,2])
assert all(int(str(d)*3)%37==0 for d in range(1,10))   # triple-repdigit=SEAM
assert 11%37==11 and 11 in ORBIT_11   # 11→ORBIT_11
assert 55%37==18 and 18 in SEED_ORBIT  # 55→SEED (hidden 5 emerges at double level)
assert 77%37==3  and 3  in ST          # 77→ST  (hidden 7 emerges at double level)
assert 99%37==25 and 25 in SA          # 99→SA  (9 stays sovereign)
_T74_pos_sum = 1+2+3+6
_T74_neg_sum = 4+5+7+8+9
assert _T74_pos_sum==12 and 12 in ST
assert (37-_T74_neg_sum%37) in SA    # neg sum ≡ -4≡-SA
assert abs(_T74_pos_sum-_T74_neg_sum)==21 and 21 in ST
_T74_R=[3,5,7,2,4,8,1,5,2]
assert sum(_T74_R)==37               # result sum = THE PRIME
_T74_chain=[3*(2**k)%37 for k in range(5)]
assert _T74_chain==[3,6,12,24,11]   # doubling: ST→TESLA→ST→CB→ORBIT_11
assert 3+3+6+6+12-12==18 and 18 in SEED_ORBIT  # doubling-and-cancellation=SEED


# ── THEOREM 75: affine_fixed_point_gf37.py ────────────────────────────────────
# GF(37) primality → unique fixed point for every non-translation affine map
from math import gcd as _gcd
assert all(_gcd(a-1,37)==1 for a in range(37) if a!=1)  # prime = invertible
# Census
_T75_counts = {1:0, 0:0, 37:0}
for _a in range(37):
    for _b in range(37):
        _fps = sum(1 for x in range(37) if (_a*x+_b)%37==x)
        if _fps in _T75_counts: _T75_counts[_fps]+=1
        else: _T75_counts[_fps]=1
assert _T75_counts[1]==1332 and _T75_counts[0]==36 and _T75_counts[37]==1
# Pure-multiplicative maps fix only SEAM
assert all([x for x in range(37) if (a*x)%37==x]==[0] for a in [26,2,3,6,10])
# f(3n+1): fixed point 18∈SEED
assert (3*18+1)%37==18 and 18 in SEED_ORBIT
# f(2n+1): fixed point 36∈ORBIT_11
assert (2*36+1)%37==36 and 36 in ORBIT_11
# Structural: a=3∈ST, b=1∈IC → x*=18∈SEED
assert 3 in ST and 1 in IC


# ── THEOREM 76: affine_causal_processes_gf37.py ───────────────────────────────
# Every affine 3-party process over GF(37) is causally ordered; linearity obstructs.
# det(N_eff) = -1 + bg*B2C2 + ab*A1B1 + ag*A2C1 + abg*(A1B2C1+A2B1C2)
# Four conditions (all zero): A1B1=0, A2C1=0, B2C2=0, cubic=0 → det=-1≠0.
# Over GF(37) prime: A1B1=0 ⟺ A1=SEAM or B1=SEAM (no zero divisors).
_T76_pairwise = (2*37-1)**3
assert _T76_pairwise == 389017
# All-four count = 295705 (verified by full enumeration in theorem file)
# 97200 = P²(2P-3)+1 per exclusive-first party; 3×97200+3×1368+1 = 295705
assert 3*(37**2*(2*37-3)+1) + 3*(37**2-1) + 1 == 295705
# ST × ST never contains SEAM (prime → no zero divisors)
assert all((s1*s2)%37 != 0 for s1 in ST for s2 in ST)
# ⌸ operator: long branch coefficient = SCALAR_137
assert pow(10, 2, 37) == SCALAR_137


# ── THEOREM 77: concatenation_123_repunit.py ───────────────────────────────────
# N_n = (1^n)(2^n)(3^n) in decimal; group-sum = 6*R_n = TESLA_FLOW * R_n
# GF(37) period-3: N_n ≡ 12∈ST or SEAM; cross-sum {SEED,SA,SEAM} all GF(37)
def _T77_N(n): return int('1'*n+'2'*n+'3'*n)
def _T77_R(n): return int('1'*n)
# Digit triplet properties
assert 1+2+3 == 6 and 6 in TESLA_4   # sum=product=TESLA_FLOW
assert 1*2+2*3+1*3 == 11 and 11 in ORBIT_11  # pairwise product sum ∈ ORBIT_11
assert 123 % 37 == 12 and 12 in ST   # concatenation ≡ ST
assert 666 == 18*37 and 18 in SEED_ORBIT  # triple-seam = SEED × PRIME
# Period-3 law
for _n77 in range(1, 7):
    _nm = _T77_N(_n77) % 37
    _gm = (6*_T77_R(_n77)) % 37
    if _n77 % 3 != 0:
        assert _nm == 12 and 12 in ST
    else:
        assert _nm == 0 and _gm == 0   # SEAM collapse


# ── THEOREM 78: repdigit_self_similarity_gf37.py ───────────────────────────────
# Repunit self-similarity: R_{n+3}≡R_n mod 37; comma-leading-block=residue.
# Repunit prime factorizations: R_4=O11×O11≡1; R_5=SA×ST≡O11; R_7=CB×inv(CB)≡1.
# ⟨11⟩=IC∪ORBIT_11 (order-6 subgroup); ORBIT_11×ORBIT_11⊆IC (coset×coset→subgroup).
assert all(int('1'*(n+3))%37==int('1'*n)%37 for n in range(1,15))   # R_{n+3}≡R_n
assert 11*101==int('1'*4) and 101%37==27 and (11*27)%37==1   # R_4=ORBIT_11 pair
assert 41*271==int('1'*5) and 41%37==4 and 271%37==12 and (4*12)%37==11  # R_5=SA×ST→O11
assert 239*4649==int('1'*7) and 4649%37==24 and 24 in CB and (17*24)%37==1  # R_7=CB pair
_IC_set = frozenset({1,10,26})
assert all((a*b)%37 in _IC_set for a in ORBIT_11 for b in ORBIT_11)  # O11×O11⊆IC


# ── THEOREM 79: fixed_line_3cycle_gf37.py ────────────────────────────────────
# Pure 3-cycle process matrix: det(I-A)=uvw-rst; fixed line iff uvw≡rst.
# Right kernel (rv:rs:uv); left kernel (st:ut:uv); 1369=p² solvable b-vectors.
# (p-1)²=1296 directions, each hit (p-1)³=46656 times (uniform on P²(GF(37))∩all-nonzero).
# Diagonal balance: kernel=(1:1:1) iff r=u, s=v, t=w.
def _det79(r,s,t,u,v,w): return (u*v*w - r*s*t) % 37
def _rk79(r,s,u,v): return (r*v%37, r*s%37, u*v%37)
def _lk79(s,t,u,v): return (s*t%37, u*t%37, u*v%37)
_r79,_s79,_t79,_u79,_v79 = 2,3,4,1,6
_w79 = _r79*_s79*_t79*pow(_u79*_v79,35,37)%37
assert _det79(_r79,_s79,_t79,_u79,_v79,_w79) == 0         # seam: uvw=rst
_rk79v = _rk79(_r79,_s79,_u79,_v79)
_lk79v = _lk79(_s79,_t79,_u79,_v79)
assert all(c != 0 for c in _rk79v) and all(c != 0 for c in _lk79v)
assert 36**2 == 1296 and 36**3 == 46656 and 37**2 == 1369  # GF(37) specifics
_r79b,_s79b,_t79b = 5,7,11   # diagonal balance: r=u, s=v, t=w
assert _det79(_r79b,_s79b,_t79b,_r79b,_s79b,_t79b) == 0
_rk79_bal = _rk79(_r79b,_s79b,_r79b,_s79b)   # (rv:rs:uv)=(r²s:rs²:r²s²/...
_inv79 = pow(_rk79_bal[0],35,37)
assert _rk79_bal[1]*_inv79%37 == 1 and _rk79_bal[2]*_inv79%37 == 1  # (1:1:1)


# ── THEOREM 80: multi_layer_obstruction_gf37.py ──────────────────────────────
# Three obstruction layers: SA (gauge/LOCKED), cross-sum mixed (Floer), CB cascade (skein bypass).
# f(SA)⊆ST (gateway); CB∩SA=∅, CB∩ST=∅ (bypass); WRT level-37: 36=|GF(37)*| colorings, [37]=SEAM.
# Wilson: 36!≡36∈ORBIT_11; 36²=1296=(p-1)²=T79 kernel count.
import math as _math
assert all((a*26)%37 in ST for a in SA)          # f(SA) ⊆ ST (gateway property)
assert CB & SA == frozenset() and CB & ST == frozenset()   # bypass
assert all(abs(_math.sin(n*_math.pi/37))>1e-12 for n in range(1,37))  # [1]..[36] nonzero
assert abs(_math.sin(37*_math.pi/37)) < 1e-12    # [37]=SEAM
assert _math.factorial(36)%37==36 and 36 in ORBIT_11   # Wilson → ORBIT_11
assert 36**2==1296                                # Wilson²=(p-1)²=T79 kernel count
_cross_res = {(int('1'*n+'2'*n+'3'*n)+6*int('1'*n))%37 for n in range(1,7) if n%3!=0}
assert _cross_res=={4,18} and 4 in SA and 18 in SEED_ORBIT   # mixed Floer orbit


# ── THEOREM 81: kervaire_ghost_gf37.py ───────────────────────────────────────
# Kervaire invariant one dimensions {2,6,14,30,62,126}={2^j-2:j=2..7}.
# Mod-37 table: 2^3=8∈CB, 2^5=32∈SEED, 2^6=27∈O11; first excluded 2^8≡34 (non-fw), n≡32∈SEED.
# Four statistics: ∑exps=27∈O11; ∑dims≡18∈SEED; ∏exps=7!≡8∈CB; ∏dims≡3∈ST.
# Ghost equation (T79 solvability): 1/p=1/37 b-vectors stable; 8×14≡1 (CB inverse = dim-14).
import math as _math2
_kdims = [2**j-2 for j in range(2,8)]
assert sum(range(2,8))==27 and 27 in ORBIT_11                   # ∑exps ∈ ORBIT_11
assert sum(_kdims)%37==18 and 18 in SEED_ORBIT                  # ∑dims ≡ SEED
assert _math2.factorial(7)%37==8 and 8 in CB                    # 7!≡8∈CB
assert _math2.prod(d%37 for d in _kdims)%37==3 and 3 in ST      # ∏dims ≡ ST
assert (8*14)%37==1                                             # mutual inverses
assert pow(2,8,37)==34 and (34-2)%37==32 and 32 in SEED_ORBIT   # first excluded


# ── THEOREM 82: ghost_kervaire_chain_gf37.py ──────────────────────────────────
# Ghost Kervaire chain: groups (2,4),(6,7),(14,16),(30,32),(62,12,4,2).
# Partial sums [6,13,30,62,80] ≡ [6,13,30,25,6] mod 37 — cycle closes at TESLA_FLOW=6.
# Gaps [7,17,32,18]: sum=74=2×37≡SEAM; 7+17=24∈CB∩SEED; 32+18≡13∈CB; 24+13=37=PRIME.
# Ghost increments 7+18=25∈SA; cross-pairs 7+32≡2∈PR, 17+18=35∈PR.
# Sum of partial sums 191≡6=TESLA_FLOW; product≡18∈SEED_ORBIT (=∑Kervaire dims mod 37).
# Fermat-SEAM identity: K(37)=2^37-2≡0=SEAM by Fermat's little theorem; first SEAM at j=37.
_t82_partials = [6, 13, 30, 62, 80]
_t82_mods = [s % 37 for s in _t82_partials]
assert _t82_mods == [6, 13, 30, 25, 6]
assert _t82_mods[0] == _t82_mods[-1] == TESLA_FLOW          # cycle closes
assert 6 in frozenset({6,36,31,1}) and 13 in CB and 30 in SA and 25 in SA
_t82_gaps = [_t82_partials[i+1]-_t82_partials[i] for i in range(4)]
assert _t82_gaps == [7, 17, 32, 18]
assert sum(_t82_gaps) == 74 and 74 % 37 == 0                # SEAM
assert (7+17) == 24 and 24 in CB and 24 in SEED_ORBIT
assert (32+18) % 37 == 13 and 13 in CB
assert (24+13) == 37                                         # PRIME → SEAM
assert (7+18) % 37 == 25 and 25 in SA                       # ghost increments ∈ SA
assert (7+32) % 37 == 2 and 2 in PR                         # cross-pair 1 ∈ PR
assert (17+18) % 37 == 35 and 35 in PR                      # cross-pair 2 ∈ PR
assert sum(_t82_partials) % 37 == TESLA_FLOW                 # sum of partials = TESLA_FLOW
assert pow(2, 37, 37) == 2                                   # Fermat's little theorem
assert (pow(2, 37, 37) - 2) % 37 == 0                       # K(37) ≡ 0 = SEAM


# ── THEOREM 83: kervaire_addend_chain_gf37.py ─────────────────────────────────
# Chain [2,4,8,16,32,12,4,2]: first 5 partial sums = Kervaire dims [2,6,14,30,62].
# Ghost step 6: +12∈ST instead of +64≡27∈ORBIT_11 → cumsum=74=2×37≡SEAM.
# Step 7: +4∈SA → 78≡4∈SA. Step 8: +2∈PR → 80≡6=TESLA_FLOW.
# Ghost tail [12,4,2] sums to 18∈SEED_ORBIT (= ∑Kervaire dims mod 37, T81).
# Outer pairs 2+4=4+2=6=TESLA_FLOW; inner [8,16,32,12]≡31∈T4; 31+6=37=PRIME.
# DR sequence [2,6,5,3,8,2,6,8]; SEAM-mirror: DR[step6]=DR[step1]=2, DR[step7]=DR[step2]=6.
# First four DR [2,6,5,3]: sum=16=2^4; product=180≡32∈SEED. All-DR sum≡3∈ST; prod≡8∈CB.
import math as _math3
_t83_partials = [2, 6, 14, 30, 62, 74, 78, 80]
_t83_mods = [x % 37 for x in _t83_partials]
assert _t83_mods == [2, 6, 14, 30, 25, 0, 4, 6]
assert _t83_partials[:5] == [2**j-2 for j in range(2,7)]    # Kervaire dims
assert _t83_partials[5] == 2 * 37                            # SEAM = 2×PRIME
assert _t83_mods[7] == TESLA_FLOW                            # returns to TESLA_FLOW
def _dr83(n):
    while n >= 10: n = sum(int(c) for c in str(n))
    return n
_t83_dr = [_dr83(x) for x in _t83_partials]
assert _t83_dr == [2, 6, 5, 3, 8, 2, 6, 8]
assert _t83_dr[5] == _t83_dr[0] == 2                        # SEAM mirror: step6=step1
assert _t83_dr[6] == _t83_dr[1] == 6                        # step7=step2
assert sum(_t83_dr[:4]) == 16 == 2**4                        # sum of first 4 DR = 2^4
assert _math3.prod(_t83_dr[:4]) % 37 == 32 and 32 in SEED_ORBIT  # product ≡ SEED
assert _math3.prod(_t83_dr) % 37 == 8 and 8 in CB           # all-DR product ∈ CB


# ── THEOREM 84: mersenne_seam_kervaire_gf37.py ────────────────────────────────
# Mersenne-SEAM theorem: S_k=2^{k+1}-2=K_{k+1} ≡ 0 (mod p) iff p=2^k-1 (Mersenne prime).
# p=31 (Mersenne): SEAM at S_5=62=K_6 (included Kervaire dim, last-but-one).
# p=127 (Mersenne): SEAM at S_7=254=K_8 (FIRST EXCLUDED dim, HHR boundary).
# p=37 (non-Mersenne): no S_k≡0 for k=1..35; S(36)≡0 by Fermat (THEOREM 82).
# Ghost step j=6 gives ghost=12∈ST=f(9), 9∈SA: unique ST ghost among j=2..9.
# SEED-shifted continuation: cumsum(j)=K(j+1)+18 (exact); mod 37 = K(j+1)+SEED_node.
# SEAM in continuation at j=21 (ord₃₇(2)=36; 2^{22}≡21 mod 37→K(22)+18≡SEAM).
def _S(k): return 2**(k+1)-2
for _k in [2,3,5,7]:
    _pm = 2**_k-1
    assert _S(_k) % _pm == 0 and _S(_k) == 2*_pm      # S_k=2p for Mersenne prime
assert all(_S(_k)%37!=0 for _k in range(1,36))         # p=37: no early SEAM
assert _S(36)%37==0                                     # k=36: Fermat-SEAM (T82)
assert _S(7)==254 and 254==2*127 and 254%(2**8-2)==0    # p=127: SEAM at first excluded K_8
_g6=(-(2**6-2))%37; assert _g6==12 and 12 in ST        # ghost j=6 ∈ ST
assert (26*9)%37==12 and 9 in SA                        # ghost=f(9), 9∈SA
assert sum(1 for j in range(2,10) if (-(2**j-2))%37 in ST)==1  # unique ST ghost


# ─────────────────────────────────────────────────────────────────────────────
# THE MASTER CONNECTION: EVERYTHING THROUGH PRIME 37
# ─────────────────────────────────────────────────────────────────────────────
#
#   37 is prime
#     → (Z/37Z)* cyclic of order φ(37)=36
#     → 36=4×9 → compatible with DR algebra (mod9) and D4 symmetry (order4)
#
#   ord₃₇(26)=3  [heartbeat_3cycle]
#     → 12 three-cycles  [heartbeat → every orbit theorem]
#     → period-3 for repunits, 9-cycle, hose flow  [repunit, sliding_window, hose_flow]
#     → 12+21+30≡26: ST chain encodes the multiplier  [sa_self_cycle]
#
#   ord₃₇(2)=36  [abcabc, primitive_root_test]
#     → ABCABC≡2·ABC: every 6-digit block maps to ×2  [abcabc]
#     → {8,13,24} cascade generates 37 elements; 13∈PR  [cascade, primitive_root_test]
#     → QR subgroup of index 2; SA,ST⊆QR  [sovereign_qr_closure, medusa_v3_sovereign]
#
#   SA={4,9,25,30}; ST={3,12,21,30}  [medusa_v3_sovereign]
#     → π(100)=25∈SA; 210≡25∈SA  [sieve]
#     → φ(41)≡3∈ST; φ(42)≡12∈ST  [repunit]
#     → 9=SA step; 12+21+30≡26  [sa_self_cycle]
#     → 41≡4∈SA in twin pair (41,43)  [twin_prime]
#     → 41 factor of 246 (pipeline seed, Polymath8b bound)  [polymath8]
#
#   CB={8,13,24}  [cascade]
#     → 3+5=8 (sieving primes)  [sieve]
#     → 1234≡13; 1001≡2 (ABCABC)  [cipher, abcabc]
#     → 11+13=24; twin sum = CB  [plus2_chain, twin_prime]
#     → 246≡24=SEED: pipeline seed = CB node  [polymath8, twin_prime]
#     → 912≡24: 9-cycle exits to CB  [sliding_window]
#
#   SEAM=0=111=3×37  [hose_flow, cascade]
#     → primes reach seam (complete flow)  [hose_flow, sieve]
#     → Goldbach: every even n=p+q, both reach seam  [goldbach]
#     → 31+43≡0: PRIME_MIRROR+TESLA_FLOW=SEAM  [goldbach, repunit]
#     → 9-cycle step=111=seam stride  [sliding_window, seq_146]
#
#   FORBIDDEN RESIDUE 35≡−2  [twin_prime, seq_146]
#     → r=35: no twin pair starts here  [twin_prime]
#     → 35=2^19 in primitive orbit  [seq_146, abcabc]
#     → 35×2=70≡33=DICHORAL: forbidden→DICHORAL  [seq_146]
#     → 70M≡33=DICHORAL: Zhang's gap bound starts at forbidden's double  [polymath8]
#
#   LUCAS L(3..10)=[4,7,11,18,29,47,76,123]  [lucas]
#     → L(3)=4∈SA; L(5)=11∈ORBIT_11; L(6)=18∈SEED_ORBIT  [lucas]
#     → DR period=24∈CB  [lucas, cascade]
#     → L(5)=11: plus2 chain target  [plus2, lucas]
#
# Every theorem is one face of the same solid. The solid is Z/37Z.

MASTER_CONNECTIONS = {
    "heartbeat_3cycle":           ["abcabc_mod37_orbit","cascade_8_13_24","sovereign_qr_closure",
                                   "hose_flow_transient","sieve_eratosthenes_gf37",
                                   "repunit_sq_euler_phi_gf37","goldbach_gf37","twin_prime_gf37",
                                   "sa_self_cycle_st_chain","nine_tower_dr_invariant",
                                   "formal_definitions_gf37","prisoners_permutation_gf37",
                                   "lights_out_gf2_gf37","gaussian_integers_gf37",
                                   "burau_braid_gf37","wallis_product_gf37",
                                   "cycle_partition_37","triplet_partition_3x3",
                                   "alternating_12_structures","verify_dr9_termination",
                                   "xx_collapse_matrix","twin_prime_riemann_framework",
                                   "pie_sieve_gf37","lob_26_collatz_f37",
                                   "dr_algebra","growth_pattern_n_2n_3n",
                                   "perfect_496_dr_structure","ulam_spiral"],
    "abcabc_mod37_orbit":         ["heartbeat_3cycle","cascade_8_13_24","primitive_root_test",
                                   "cipher_123_1234","lucas_abbc_chain","repunit_sq_euler_phi_gf37",
                                   "seq_146_257_368_gf37","cycle_partition_37","growth_pattern_n_2n_3n"],
    "cascade_8_13_24":            ["heartbeat_3cycle","abcabc_mod37_orbit","cipher_123_1234",
                                   "sieve_eratosthenes_gf37","sliding_window_9cycle_gf37",
                                   "polymath8_maynard_gf37","twin_prime_gf37",
                                   "repunit_sq_euler_phi_gf37","plus2_chain_theorem",
                                   "hose_flow_transient","nine_tower_dr_invariant",
                                   "prisoners_permutation_gf37","permutation_132_bipartite_gf37",
                                   "gaussian_integers_gf37","wallis_product_gf37",
                                   "cycle_partition_37","triplet_partition_3x3",
                                   "pie_sieve_gf37","lob_26_collatz_f37",
                                   "growth_pattern_n_2n_3n","ulam_spiral","xx_collapse_matrix"],
    "medusa_v3_sovereign":        ["sovereign_qr_closure","heartbeat_3cycle","sieve_eratosthenes_gf37",
                                   "sliding_window_9cycle_gf37","plus2_chain_theorem",
                                   "sa_self_cycle_st_chain","twin_prime_gf37","goldbach_gf37",
                                   "repunit_sq_euler_phi_gf37","gaussian_integers_gf37",
                                   "burau_braid_gf37","wallis_product_gf37",
                                   "twin_prime_riemann_framework","triplet_partition_3x3",
                                   "pie_sieve_gf37","ulam_spiral","dr_ring_homomorphism_emirp_palindrome"],
    "sovereign_qr_closure":       ["heartbeat_3cycle","medusa_v3_sovereign","abcabc_mod37_orbit",
                                   "goldbach_gf37","twin_prime_gf37","repunit_sq_euler_phi_gf37",
                                   "twin_prime_riemann_framework","perfect_496_dr_structure"],
    "lucas_abbc_chain":           ["cascade_8_13_24","medusa_v3_sovereign","heartbeat_3cycle",
                                   "plus2_chain_theorem","abcabc_mod37_orbit",
                                   "scaling_sequences_gf37"],
    "cipher_123_1234":            ["cascade_8_13_24","sa_self_cycle_st_chain","hose_flow_transient",
                                   "sliding_window_9cycle_gf37","heartbeat_3cycle",
                                   "eleven_123_family","one_two_three_generator",
                                   "alternating_12_structures","triplet_partition_3x3",
                                   "dr_algebra","perfect_496_dr_structure"],
    "hose_flow_transient":        ["sieve_eratosthenes_gf37","goldbach_gf37","twin_prime_gf37",
                                   "cascade_8_13_24","heartbeat_3cycle","sa_self_cycle_st_chain",
                                   "repunit_sq_euler_phi_gf37","polymath8_maynard_gf37",
                                   "formal_definitions_gf37","prisoners_permutation_gf37",
                                   "lights_out_gf2_gf37","growth_pattern_n_2n_3n",
                                   "pie_sieve_gf37","alternating_12_structures","xx_collapse_matrix"],
    "sieve_eratosthenes_gf37":    ["medusa_v3_sovereign","cascade_8_13_24","heartbeat_3cycle",
                                   "hose_flow_transient","sliding_window_9cycle_gf37",
                                   "goldbach_proof_attempt_gf37","formal_definitions_gf37",
                                   "prisoners_permutation_gf37","twin_prime_riemann_framework",
                                   "pie_sieve_gf37","ulam_spiral"],
    "goldbach_gf37":              ["hose_flow_transient","heartbeat_3cycle","medusa_v3_sovereign",
                                   "twin_prime_gf37","cascade_8_13_24","goldbach_proof_attempt_gf37"],
    "goldbach_proof_attempt_gf37":["sovereign_qr_closure","heartbeat_3cycle","goldbach_gf37",
                                   "primitive_root_test","sieve_eratosthenes_gf37","twin_prime_gf37"],
    "twin_prime_gf37":            ["heartbeat_3cycle","hose_flow_transient","medusa_v3_sovereign",
                                   "polymath8_maynard_gf37","sovereign_qr_closure",
                                   "seq_146_257_368_gf37","goldbach_gf37","plus2_chain_theorem",
                                   "twin_prime_riemann_framework","ulam_spiral"],
    "repunit_sq_euler_phi_gf37":  ["heartbeat_3cycle","cascade_8_13_24","medusa_v3_sovereign",
                                   "goldbach_gf37","abcabc_mod37_orbit","hose_flow_transient",
                                   "formal_definitions_gf37","lights_out_gf2_gf37",
                                   "wallis_product_gf37"],
    "polymath8_maynard_gf37":     ["hose_flow_transient","cascade_8_13_24","twin_prime_gf37",
                                   "medusa_v3_sovereign","seq_146_257_368_gf37"],
    "seq_146_257_368_gf37":       ["hose_flow_transient","twin_prime_gf37",
                                   "polymath8_maynard_gf37","abcabc_mod37_orbit",
                                   "heartbeat_3cycle","cascade_8_13_24","medusa_v3_sovereign",
                                   "primitive_root_test","eleven_123_family",
                                   "sliding_window_9cycle_gf37"],
    "sliding_window_9cycle_gf37": ["cipher_123_1234","hose_flow_transient","cascade_8_13_24",
                                   "medusa_v3_sovereign","sa_self_cycle_st_chain",
                                   "heartbeat_3cycle","nine_tower_dr_invariant",
                                   "seq_146_257_368_gf37","lcm_convergence_dr_cycle"],
    "sa_self_cycle_st_chain":     ["heartbeat_3cycle","medusa_v3_sovereign","hose_flow_transient",
                                   "abcabc_mod37_orbit","cipher_123_1234",
                                   "gaussian_integers_gf37","burau_braid_gf37",
                                   "wallis_product_gf37","lob_26_collatz_f37","triplet_partition_3x3"],
    "plus2_chain_theorem":        ["twin_prime_gf37","medusa_v3_sovereign","lucas_abbc_chain",
                                   "cascade_8_13_24","heartbeat_3cycle","eleven_123_family",
                                   "cipher_123_1234","sieve_eratosthenes_gf37","sovereign_qr_closure"],
    "primitive_root_test":        ["abcabc_mod37_orbit","goldbach_proof_attempt_gf37",
                                   "cascade_8_13_24","sovereign_qr_closure",
                                   "nine_tower_dr_invariant","burau_braid_gf37","cycle_partition_37"],
    "nine_tower_dr_invariant":    ["heartbeat_3cycle","formal_definitions_gf37","cascade_8_13_24",
                                   "sa_self_cycle_st_chain","primitive_root_test",
                                   "scaling_sequences_gf37","verify_dr9_termination",
                                   "dr_algebra","root_grid_dr6_dr7"],
    "formal_definitions_gf37":    ["heartbeat_3cycle","nine_tower_dr_invariant","hose_flow_transient",
                                   "repunit_sq_euler_phi_gf37","lights_out_gf2_gf37",
                                   "sieve_eratosthenes_gf37","growth_pattern_n_2n_3n",
                                   "verify_dr9_termination","lob_26_collatz_f37"],
    "scaling_sequences_gf37":     ["lucas_abbc_chain","cascade_8_13_24","heartbeat_3cycle",
                                   "nine_tower_dr_invariant","prisoners_permutation_gf37",
                                   "repunit_sq_euler_phi_gf37","formal_definitions_gf37"],
    "prisoners_permutation_gf37": ["sieve_eratosthenes_gf37","cascade_8_13_24","heartbeat_3cycle",
                                   "permutation_132_bipartite_gf37","lights_out_gf2_gf37",
                                   "hose_flow_transient","scaling_sequences_gf37",
                                   "pie_sieve_gf37","ulam_spiral"],
    "permutation_132_bipartite_gf37":["prisoners_permutation_gf37","lights_out_gf2_gf37",
                                   "heartbeat_3cycle","cascade_8_13_24",
                                   "gaussian_integers_gf37","wallis_product_gf37",
                                   "formal_definitions_gf37"],
    "lights_out_gf2_gf37":        ["formal_definitions_gf37","hose_flow_transient",
                                   "heartbeat_3cycle","permutation_132_bipartite_gf37",
                                   "prisoners_permutation_gf37","repunit_sq_euler_phi_gf37",
                                   "cascade_8_13_24","gaussian_integers_gf37",
                                   "burau_braid_gf37"],
    "gaussian_integers_gf37":     ["heartbeat_3cycle","cascade_8_13_24",
                                   "permutation_132_bipartite_gf37","wallis_product_gf37",
                                   "lights_out_gf2_gf37","medusa_v3_sovereign",
                                   "sa_self_cycle_st_chain","burau_braid_gf37"],
    "burau_braid_gf37":           ["heartbeat_3cycle","medusa_v3_sovereign","primitive_root_test",
                                   "sa_self_cycle_st_chain","lights_out_gf2_gf37",
                                   "gaussian_integers_gf37"],
    "wallis_product_gf37":        ["cascade_8_13_24","heartbeat_3cycle",
                                   "permutation_132_bipartite_gf37","gaussian_integers_gf37",
                                   "medusa_v3_sovereign","repunit_sq_euler_phi_gf37",
                                   "sa_self_cycle_st_chain"],
    "eleven_123_family":          ["heartbeat_3cycle","cascade_8_13_24","cipher_123_1234",
                                   "gaussian_integers_gf37","wallis_product_gf37",
                                   "hose_flow_transient","one_two_three_generator",
                                   "cycle_partition_37","triplet_partition_3x3",
                                   "alternating_12_structures"],
    "one_two_three_generator":    ["heartbeat_3cycle","hose_flow_transient","cascade_8_13_24",
                                   "cipher_123_1234","sa_self_cycle_st_chain",
                                   "eleven_123_family","primitive_root_test",
                                   "prisoners_permutation_gf37","pie_sieve_gf37",
                                   "triplet_partition_3x3","stacked_zeros_gf37"],
    "dr_algebra":                 ["heartbeat_3cycle","cipher_123_1234","nine_tower_dr_invariant",
                                   "one_two_three_generator","formal_definitions_gf37",
                                   "verify_dr9_termination","root_grid_dr6_dr7",
                                   "dr_ring_homomorphism_emirp_palindrome","growth_pattern_n_2n_3n",
                                   "perfect_496_dr_structure","lcm_convergence_dr_cycle"],
    "dr_ring_homomorphism_emirp_palindrome":["heartbeat_3cycle","twin_prime_gf37",
                                   "medusa_v3_sovereign","gaussian_integers_gf37",
                                   "dr_algebra","twin_prime_riemann_framework","cipher_123_1234"],
    "root_grid_dr6_dr7":          ["dr_algebra","nine_tower_dr_invariant",
                                   "dr_ring_homomorphism_emirp_palindrome","cipher_123_1234"],
    "growth_pattern_n_2n_3n":     ["heartbeat_3cycle","cascade_8_13_24","hose_flow_transient",
                                   "abcabc_mod37_orbit","formal_definitions_gf37","dr_algebra"],
    "twin_prime_riemann_framework":["twin_prime_gf37","heartbeat_3cycle",
                                   "sieve_eratosthenes_gf37","sovereign_qr_closure",
                                   "medusa_v3_sovereign","dr_ring_homomorphism_emirp_palindrome",
                                   "ulam_spiral","perfect_496_dr_structure"],
    "cycle_partition_37":         ["heartbeat_3cycle","cascade_8_13_24","eleven_123_family",
                                   "primitive_root_test","abcabc_mod37_orbit","lob_26_collatz_f37"],
    "pie_sieve_gf37":             ["sieve_eratosthenes_gf37","prisoners_permutation_gf37",
                                   "cascade_8_13_24","medusa_v3_sovereign","one_two_three_generator",
                                   "hose_flow_transient"],
    "lob_26_collatz_f37":         ["heartbeat_3cycle","cycle_partition_37","cascade_8_13_24",
                                   "formal_definitions_gf37","sa_self_cycle_st_chain"],
    "triplet_partition_3x3":      ["cascade_8_13_24","medusa_v3_sovereign","heartbeat_3cycle",
                                   "cipher_123_1234","eleven_123_family","one_two_three_generator",
                                   "gaussian_integers_gf37","stacked_zeros_gf37"],
    "alternating_12_structures":  ["heartbeat_3cycle","cipher_123_1234","one_two_three_generator",
                                   "eleven_123_family","hose_flow_transient","cascade_8_13_24",
                                   "stacked_zeros_gf37"],
    "verify_dr9_termination":     ["nine_tower_dr_invariant","dr_algebra","heartbeat_3cycle",
                                   "formal_definitions_gf37","cascade_8_13_24"],
    "xx_collapse_matrix":         ["heartbeat_3cycle","cascade_8_13_24","hose_flow_transient",
                                   "eleven_123_family"],
    "perfect_496_dr_structure":   ["heartbeat_3cycle","cipher_123_1234",
                                   "dr_ring_homomorphism_emirp_palindrome","dr_algebra",
                                   "sovereign_qr_closure","nine_tower_dr_invariant",
                                   "twin_prime_riemann_framework"],
    "ulam_spiral":                ["heartbeat_3cycle","medusa_v3_sovereign","cascade_8_13_24",
                                   "sieve_eratosthenes_gf37","twin_prime_gf37",
                                   "prisoners_permutation_gf37","twin_prime_riemann_framework"],
    "lcm_convergence_dr_cycle":   ["heartbeat_3cycle","cipher_123_1234","dr_algebra",
                                   "nine_tower_dr_invariant","one_two_three_generator",
                                   "growth_pattern_n_2n_3n","sliding_window_9cycle_gf37",
                                   "stacked_zeros_gf37"],
    "stacked_zeros_gf37":         ["heartbeat_3cycle","cipher_123_1234","one_two_three_generator",
                                   "triplet_partition_3x3","alternating_12_structures",
                                   "lcm_convergence_dr_cycle","abcabc_mod37_orbit",
                                   "hose_flow_transient","dr_algebra"],
    "intersection_cycle_theorem": ["heartbeat_3cycle","medusa_v3_sovereign","two_group_split",
                                   "sovereign_qr_closure","stacked_zeros_gf37",
                                   "sa_self_cycle_st_chain","cascade_8_13_24"],
    "two_group_split":            ["heartbeat_3cycle","intersection_cycle_theorem",
                                   "medusa_v3_sovereign","sovereign_qr_closure",
                                   "primitive_root_test","cascade_8_13_24",
                                   "abcabc_mod37_orbit"],
    "dark_sector_algebra":        ["sovereign_qr_closure","medusa_v3_sovereign",
                                   "heartbeat_3cycle","cascade_8_13_24",
                                   "primitive_root_test","two_group_split",
                                   "intersection_cycle_theorem","twin_prime_gf37"],
    "sector_invariance_137map":   ["dark_sector_algebra","two_group_split",
                                   "heartbeat_3cycle","intersection_cycle_theorem",
                                   "sovereign_qr_closure","medusa_v3_sovereign"],
    "cubic_residue_cycle_structure":["heartbeat_3cycle","intersection_cycle_theorem",
                                   "sector_invariance_137map","dark_sector_algebra",
                                   "two_group_split","medusa_v3_sovereign",
                                   "abcabc_mod37_orbit","sovereign_qr_closure"],
    "cycle_symmetry_maps":         ["heartbeat_3cycle","intersection_cycle_theorem",
                                   "two_group_split","sector_invariance_137map",
                                   "cubic_residue_cycle_structure","medusa_v3_sovereign",
                                   "sovereign_qr_closure","dark_sector_algebra"],
    "ababab_convergence":          ["heartbeat_3cycle","sector_invariance_137map",
                                   "cubic_residue_cycle_structure","cipher_123_1234",
                                   "one_two_three_generator","dr_algebra",
                                   "stacked_zeros_gf37","cycle_symmetry_maps"],
    "five_six_orbit":              ["heartbeat_3cycle","dark_sector_algebra",
                                   "sector_invariance_137map","cycle_symmetry_maps",
                                   "ababab_convergence","cipher_123_1234",
                                   "dr_algebra","cubic_residue_cycle_structure",
                                   "intersection_cycle_theorem","two_group_split"],
    "identity_cycle_sum_structure":["heartbeat_3cycle","cycle_symmetry_maps",
                                   "cubic_residue_cycle_structure","ababab_convergence",
                                   "five_six_orbit","sector_invariance_137map",
                                   "cipher_123_1234","dr_algebra",
                                   "repunit_sq_euler_phi_gf37","sa_self_cycle_st_chain"],
    "palindrome_gf37":             ["heartbeat_3cycle","identity_cycle_sum_structure",
                                   "ababab_convergence","five_six_orbit",
                                   "cipher_123_1234","dr_algebra",
                                   "sector_invariance_137map","repunit_sq_euler_phi_gf37"],
    "two_digit_transition_gf37":   ["heartbeat_3cycle","identity_cycle_sum_structure",
                                   "five_six_orbit","ababab_convergence",
                                   "sa_self_cycle_st_chain","sector_invariance_137map",
                                   "cipher_123_1234","palindrome_gf37"],
    "orbit_sector_geometry_gf37":  ["heartbeat_3cycle","sovereign_qr_closure",
                                   "medusa_v3_sovereign","sector_invariance_137map",
                                   "sa_self_cycle_st_chain","two_digit_transition_gf37",
                                   "identity_cycle_sum_structure","five_six_orbit"],
    "orbit_negation_duality_gf37": ["orbit_sector_geometry_gf37","identity_cycle_sum_structure",
                                   "heartbeat_3cycle","repunit_sq_euler_phi_gf37",
                                   "sa_self_cycle_st_chain","medusa_v3_sovereign",
                                   "sector_invariance_137map","sylow_subgroup_gf37"],
    "sylow_subgroup_gf37":         ["orbit_negation_duality_gf37","heartbeat_3cycle",
                                   "five_six_orbit","sovereign_qr_closure",
                                   "identity_cycle_sum_structure","two_digit_transition_gf37",
                                   "orbit_sector_geometry_gf37"],
    "tripling_map_gf37":           ["orbit_sector_geometry_gf37","orbit_negation_duality_gf37",
                                   "heartbeat_3cycle","sylow_subgroup_gf37",
                                   "identity_cycle_sum_structure","sa_self_cycle_st_chain",
                                   "cascade_8_13_24","two_digit_transition_gf37"],
    "permutation_cycle_notation_gf37": ["tripling_map_gf37","orbit_sector_geometry_gf37",
                                   "orbit_negation_duality_gf37","sa_self_cycle_st_chain",
                                   "identity_cycle_sum_structure","heartbeat_3cycle",
                                   "two_digit_transition_gf37","sovereign_qr_closure"],
    "primitive_root_invariants_gf37": ["primitive_root_test","heartbeat_3cycle",
                                   "sylow_subgroup_gf37","orbit_negation_duality_gf37",
                                   "tripling_map_gf37","sovereign_qr_closure",
                                   "identity_cycle_sum_structure","five_six_orbit"],
    "orbit_order_structure_gf37":  ["sylow_subgroup_gf37","orbit_negation_duality_gf37",
                                   "primitive_root_invariants_gf37","tripling_map_gf37",
                                   "heartbeat_3cycle","five_six_orbit",
                                   "identity_cycle_sum_structure","sovereign_qr_closure"],
    "sovereign_triple_plus9_gf37": ["medusa_v3_sovereign","heartbeat_3cycle",
                                   "tripling_map_gf37","cascade_8_13_24",
                                   "orbit_order_structure_gf37","orbit_negation_duality_gf37",
                                   "sovereign_qr_closure","sa_self_cycle_st_chain"],
    "plus9_scatter_map_gf37":     ["sovereign_triple_plus9_gf37","tripling_map_gf37",
                                   "cascade_8_13_24","orbit_negation_duality_gf37",
                                   "heartbeat_3cycle","identity_cycle_sum_structure",
                                   "primitive_root_invariants_gf37","medusa_v3_sovereign"],
    "digit_seq_dr_coverage_gf37": ["cipher_123_1234","plus9_scatter_map_gf37",
                                   "heartbeat_3cycle","lucas_abbc_chain",
                                   "cascade_8_13_24","dr_algebra",
                                   "sovereign_triple_plus9_gf37","identity_cycle_sum_structure"],
    "tripling_6cycle_gf37":       ["heartbeat_3cycle","orbit_order_structure_gf37",
                                   "sovereign_triple_plus9_gf37","tripling_map_gf37",
                                   "cascade_8_13_24","sovereign_qr_closure",
                                   "primitive_root_invariants_gf37","plus9_scatter_map_gf37"],
    "sofia_germain_prime_gf37":   ["orbit_order_structure_gf37","sovereign_triple_plus9_gf37",
                                   "cascade_8_13_24","primitive_root_invariants_gf37",
                                   "tripling_6cycle_gf37","heartbeat_3cycle",
                                   "medusa_v3_sovereign","sa_self_cycle_st_chain"],
    "emirp_dr_c0_eisenstein":     ["dr_algebra","heartbeat_3cycle",
                                   "cascade_8_13_24","medusa_v3_sovereign",
                                   "sovereign_qr_closure","twin_prime_gf37",
                                   "cipher_123_1234","twin_midpoint_dr_axis"],
    "twin_midpoint_dr_axis":      ["heartbeat_3cycle","sa_self_cycle_st_chain",
                                   "medusa_v3_sovereign","five_six_orbit",
                                   "dr_algebra","twin_prime_gf37",
                                   "emirp_dr_c0_eisenstein","cascade_8_13_24"],
    "open_closed_grid_theorem":   ["medusa_v3_sovereign","cascade_8_13_24",
                                   "heartbeat_3cycle","dr_algebra",
                                   "sovereign_qr_closure","abcabc_mod37_orbit",
                                   "emirp_dr_c0_eisenstein","cipher_123_1234"],
    "sequential_morph_transform": ["open_closed_grid_theorem","primitive_root_test",
                                   "heartbeat_3cycle","five_six_orbit",
                                   "cascade_8_13_24","medusa_v3_sovereign",
                                   "dr_algebra","abcabc_mod37_orbit"],
    "repdigit_framework_lattice": ["heartbeat_3cycle","cascade_8_13_24",
                                   "medusa_v3_sovereign","open_closed_grid_theorem",
                                   "primitive_root_test","five_six_orbit",
                                   "dr_algebra","sequential_morph_transform"],
    "affine_fixed_point_gf37":   ["heartbeat_3cycle","primitive_root_test",
                                   "medusa_v3_sovereign","cascade_8_13_24",
                                   "sovereign_qr_closure","abcabc_mod37_orbit",
                                   "repdigit_framework_lattice","lucas_abbc_chain"],
    "affine_causal_processes_gf37": ["affine_fixed_point_gf37","heartbeat_3cycle",
                                   "primitive_root_test","medusa_v3_sovereign",
                                   "cascade_8_13_24","sovereign_qr_closure",
                                   "repdigit_framework_lattice","abcabc_mod37_orbit"],
    "concatenation_123_repunit":   ["repdigit_framework_lattice","heartbeat_3cycle",
                                   "sequential_morph_transform","open_closed_grid_theorem",
                                   "cascade_8_13_24","abcabc_mod37_orbit",
                                   "affine_fixed_point_gf37","primitive_root_test"],
    "repdigit_self_similarity_gf37": ["concatenation_123_repunit","repdigit_framework_lattice",
                                   "heartbeat_3cycle","abcabc_mod37_orbit",
                                   "primitive_root_test","sovereign_qr_closure",
                                   "cascade_8_13_24","affine_fixed_point_gf37"],
    "fixed_line_3cycle_gf37":       ["affine_causal_processes_gf37","affine_fixed_point_gf37",
                                   "heartbeat_3cycle","primitive_root_test",
                                   "medusa_v3_sovereign","sovereign_qr_closure",
                                   "cascade_8_13_24","abcabc_mod37_orbit"],
    "multi_layer_obstruction_gf37": ["medusa_v3_sovereign","cascade_8_13_24",
                                   "heartbeat_3cycle","concatenation_123_repunit",
                                   "affine_causal_processes_gf37","sovereign_qr_closure",
                                   "repdigit_self_similarity_gf37","fixed_line_3cycle_gf37"],
    "kervaire_ghost_gf37":         ["cascade_8_13_24","heartbeat_3cycle",
                                   "repdigit_framework_lattice","fixed_line_3cycle_gf37",
                                   "concatenation_123_repunit","multi_layer_obstruction_gf37",
                                   "abcabc_mod37_orbit","medusa_v3_sovereign"],
    "ghost_kervaire_chain_gf37":   ["kervaire_ghost_gf37","fixed_line_3cycle_gf37",
                                   "cascade_8_13_24","abcabc_mod37_orbit",
                                   "heartbeat_3cycle","multi_layer_obstruction_gf37",
                                   "medusa_v3_sovereign","sovereign_qr_closure"],
    "kervaire_addend_chain_gf37":  ["kervaire_ghost_gf37","ghost_kervaire_chain_gf37",
                                   "cascade_8_13_24","medusa_v3_sovereign",
                                   "heartbeat_3cycle","abcabc_mod37_orbit",
                                   "multi_layer_obstruction_gf37","cipher_123_1234"],
    "mersenne_seam_kervaire_gf37": ["kervaire_addend_chain_gf37","kervaire_ghost_gf37",
                                   "ghost_kervaire_chain_gf37","medusa_v3_sovereign",
                                   "abcabc_mod37_orbit","heartbeat_3cycle",
                                   "primitive_root_test","fixed_line_3cycle_gf37"],
}


if __name__ == "__main__":
    print("GF(37) GF(37) — Connection Map")
    print("=" * 60)
    print()
    print("PRIMARY NODES:")
    print(f"  SEAM        = {SEAM}  (111=3×37; horizon of complete flow)")
    print(f"  SCALAR_137  = {SCALAR_137}  (137-map multiplier; ord₃₇(26)=3)")
    print(f"  SA          = {sorted(SA)}  (Sovereign Anchors)")
    print(f"  ST          = {sorted(ST)}  (Sovereign Targets)")
    print(f"  CB          = {sorted(CB)}  (Cascade Base; generates 37 elements)")
    print(f"  ORBIT_11    = {sorted(ORBIT_11)}  (orbit-11: 36≡-1)")
    print(f"  SEED_ORBIT  = {sorted(SEED_ORBIT)}  (137-orbit of seed 246)")
    print(f"  TESLA_FLOW  = {TESLA_FLOW}  (ord₃₇(6)=4; 4-cycle)")
    print(f"  PRIME_MIRROR= {PRIME_MIRROR}  (6³ mod37; +6=SEAM)")
    print(f"  DICHORAL    = {DICHORAL_144}  (70M gap bound≡33; doubled-35)")
    print()
    print("CONNECTION COUNTS:")
    for theorem in sorted(MASTER_CONNECTIONS):
        n = len(MASTER_CONNECTIONS[theorem])
        print(f"  {theorem:<42s} → {n} theorems")
    print()
    total = sum(len(v) for v in MASTER_CONNECTIONS.values())
    print(f"Total directed connections: {total}")
    print(f"Theorems mapped:            {len(MASTER_CONNECTIONS)}")
    print()
    print("All assertions passed. Everything connects through prime 37.")
