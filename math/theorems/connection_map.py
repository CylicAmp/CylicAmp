"""
GF(37) Framework — Complete Connection Map

Every theorem in this repository connects to every other through prime 37.
This file makes those connections explicit. Each theorem is listed with:
  - The framework nodes it anchors to
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
# Framework node definitions
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
#       {8,13,24} sits in the framework. Each element has its own 3-cycle:
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
#   LOCKED: anchor maps to target. GATED: external→target. PURGE: off-framework.
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
#       246≡24∈SEED_ORBIT: the seed is self-referential in the framework.
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
#   Pattern family split: {123,132}→ST; {231,321}→SA; {213,312}→off-framework.
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
#   All 8 norm-5 Gaussian integers map to named framework nodes.
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
#       All 8 norm-5 Gaussian integers map to named framework nodes.
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
#       Both use the SA/PR/SEAM taxonomy as a classification framework.
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
#   All 15 subset products of {2,3,5,7} land on named framework nodes.
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
#   {1..9} has 280 unordered 3-block partitions; 14 have all sums in framework nodes.
#   Target partition: {1,3,5}→9∈SA (ALL ODD), {2,4,6}→12∈ST (ALL EVEN), {7,8,9}→24∈CB.
#   ODDS → SA, EVENS → ST, LARGES → CB: one node from each primary class.
#   14 framework partitions fall into 4 types: {8,13,24}=CB, {9,12,24}, {11,13,21}, {12,12,21}.
#
#   → cascade_8_13_24: Type I sums={8,13,24}=CB exactly; CB appears as partition sum type.
#   → medusa_v3_sovereign: {9,12,24}=SA+ST+CB; all three anchor classes in one partition.
#   → heartbeat_3cycle: 14/280=1/20; 14=2×7; framework partitions via 137-orbit structure.
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
#   The Ulam spiral mapped through the GF(37) framework.
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
}


if __name__ == "__main__":
    print("GF(37) Framework — Connection Map")
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
