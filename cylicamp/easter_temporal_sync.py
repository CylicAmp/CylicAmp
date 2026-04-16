#!/usr/bin/env python3
"""
Easter Temporal Synchronization — MSW Framework Layer
======================================================
Maps the 2026 Easter window onto the 37-field to identify active
resonance gates in the current calendar year.

Key findings:
  Easter 2026 DoY = 93  → 93 mod 37 = 19  (19-Center seal active)
  Current DoY    = 106  → 106 mod 37 = 32  (32 = 2⁵, DR = 5)
  Gap since Easter = 13 → 13 mod 37 = 13  (6th prime, DR = 4)

Cycle locks:
  532-year Easter cycle: 2026 mod 532 = 430 → 430 mod 37 = 23  (Z-seed)
  Next NULL gates (mod 37 = 0): Day 111 (Apr 21), Day 148 (May 28)
  137-seed gate: Day 137 (May 17) — bridges to Seed 191↔137 layer

© 2026 Michael Warren Song. All Rights Reserved.
"""

import datetime
import math

# ── Constants ─────────────────────────────────────────────────────────────

EASTER_2026     = datetime.date(2026, 4,  3)   # Gregorian Easter 2026
PIVOT_37        = 37                            # 37-field pivot
CYCLE_532       = 532                           # Metonic (19y) × Solar (28y)
CYCLE_53200     = 53200                         # 532 × 100 — grand cycle
Z_SEED          = 23                            # Z-seed (DR = 5)
CENTER_19       = 19                            # 19-center seal
YEAR            = 2026


# ── Core arithmetic ───────────────────────────────────────────────────────

def digital_root(n):
    """DR(n) — iterated digit sum to single digit."""
    n = abs(int(n))
    if n == 0:
        return 0
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def day_of_year(d: datetime.date) -> int:
    """Return 1-based day-of-year for date d."""
    return d.timetuple().tm_yday


def date_from_doy(year: int, doy: int) -> datetime.date:
    """Return the date for a given 1-based day-of-year."""
    return datetime.date(year, 1, 1) + datetime.timedelta(days=doy - 1)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


# ── Temporal analysis ─────────────────────────────────────────────────────

def easter_seal(easter: datetime.date = EASTER_2026) -> dict:
    """
    37-field seal for Easter date.

    Easter 2026 falls on DoY 93.
    93 mod 37 = 19 — the 19-Center seal (7² − 30 = 19, Tesla flow ≡ 6).
    """
    doy = day_of_year(easter)
    r   = doy % PIVOT_37

    assert doy == 93,   "Easter 2026 DoY mismatch"
    assert r == 19,     "Easter mod 37 ≠ 19"
    assert r == CENTER_19

    return {
        'date':       easter.isoformat(),
        'doy':        doy,
        'mod_37':     r,
        'seal':       '19-Center',
        'dr':         digital_root(r),
        'is_prime':   is_prime(r),
    }


def current_position(today: datetime.date | None = None) -> dict:
    """
    Current calendar position relative to Easter.

    April 16 = DoY 106; 106 mod 37 = 32 = 2⁵; DR(32) = 5 (Z-seed DR).
    Gap from Easter = 13; 13 mod 37 = 13 (6th prime); DR(13) = 4.
    """
    if today is None:
        today = datetime.date.today()

    doy  = day_of_year(today)
    gap  = (today - EASTER_2026).days
    r    = doy % PIVOT_37
    rg   = gap % PIVOT_37

    return {
        'date':          today.isoformat(),
        'doy':           doy,
        'mod_37':        r,
        'dr':            digital_root(r),
        'days_since_easter': gap,
        'gap_mod_37':    rg,
        'gap_dr':        digital_root(rg),
        'position_note': f"DoY {doy} = {r} (mod 37); 32 = 2⁵" if r == 32 else f"DoY {doy} ≡ {r} (mod 37)",
    }


def cycle_analysis(year: int = YEAR) -> dict:
    """
    Easter cycle positions for the given year.

    532-year cycle (Metonic 19y × Solar 28y):
      2026 mod 532 = 430 → 430 mod 37 = 23 = Z-seed
    53200-year grand cycle:
      2026 mod 53200 = 2026 (year is within first cycle)
    """
    pos_532   = year % CYCLE_532
    pos_532r  = pos_532 % PIVOT_37
    pos_53200 = year % CYCLE_53200

    assert pos_532  == 430, "532-cycle position mismatch"
    assert pos_532r == Z_SEED, "532-cycle 37-residue ≠ Z-seed"

    return {
        'year':              year,
        'cycle_532_pos':     pos_532,
        'cycle_532_mod_37':  pos_532r,
        'z_seed_lock':       pos_532r == Z_SEED,
        'cycle_53200_pos':   pos_53200,
        'cycle_note':        f"{year} mod 532 = {pos_532} → mod 37 = {pos_532r} (Z-seed lock)",
    }


def null_gates(year: int = YEAR, start_doy: int = 1) -> list:
    """
    All days in `year` where DoY mod 37 = 0 (NULL elements).

    These are the structural zero-points of the 37-field within the year.
    """
    gates = []
    for doy in range(start_doy, 366):
        if doy % PIVOT_37 == 0:
            try:
                d = date_from_doy(year, doy)
            except ValueError:
                break
            gates.append({
                'doy':  doy,
                'date': d.isoformat(),
                'days_from_easter': (d - EASTER_2026).days,
            })
    return gates


def seed_gates(year: int = YEAR) -> list:
    """
    Days whose DoY carries a seed value in the 37-field.

    Tracks: Z-seed (23), 17-seed (17), 19-center (19), 137-bridge (26).
    """
    seed_residues = {23: 'Z-seed', 17: '17-seed', 19: '19-center', 26: '137-bridge'}
    gates = []
    for doy in range(1, 366):
        r = doy % PIVOT_37
        if r in seed_residues:
            try:
                d = date_from_doy(year, doy)
            except ValueError:
                break
            gates.append({
                'doy':          doy,
                'date':         d.isoformat(),
                'mod_37':       r,
                'seed_name':    seed_residues[r],
                'dr':           digital_root(doy),
                'days_from_easter': (d - EASTER_2026).days,
            })
    return gates


# ── Full report ───────────────────────────────────────────────────────────

def run(today: datetime.date | None = None):
    if today is None:
        today = datetime.date(2026, 4, 16)   # audit anchor date

    seal    = easter_seal()
    pos     = current_position(today)
    cycles  = cycle_analysis()
    nulls   = null_gates(start_doy=day_of_year(today))
    seeds   = [g for g in seed_gates() if g['days_from_easter'] >= 0]

    print("=" * 60)
    print("  EASTER TEMPORAL SYNC — MSW Framework")
    print("  © 2026 Michael Warren Song")
    print("=" * 60)
    print()

    print("  EASTER 2026 SEAL")
    print(f"  Date:          {seal['date']}  (DoY {seal['doy']})")
    print(f"  {seal['doy']} mod 37 = {seal['mod_37']}  → {seal['seal']}  "
          f"(prime={seal['is_prime']}, DR={seal['dr']})")
    print()

    print("  CURRENT POSITION")
    print(f"  Date:          {pos['date']}  (DoY {pos['doy']})")
    print(f"  DoY mod 37  =  {pos['mod_37']}  (32 = 2⁵, DR={pos['dr']})")
    print(f"  Days elapsed:  {pos['days_since_easter']}  → "
          f"{pos['gap_mod_37']} (mod 37), DR={pos['gap_dr']}")
    print()

    print("  CYCLE LOCKS")
    print(f"  {cycles['cycle_note']}")
    print(f"  2026 mod 53200 = {cycles['cycle_53200_pos']}  (within first grand cycle)")
    print()

    print("  UPCOMING NULL GATES (DoY mod 37 = 0)")
    for g in nulls[:4]:
        print(f"  Day {g['doy']:>3d}  {g['date']}  (+{g['days_from_easter']:>3d} from Easter)")
    print()

    print("  SEED GATES AFTER EASTER")
    print(f"  {'DoY':>4}  {'Date':<12}  {'mod37':>5}  {'Seed':<14}  {'DR':>3}  {'+Days':>6}")
    print("  " + "-" * 52)
    for g in seeds[:12]:
        print(f"  {g['doy']:>4}  {g['date']:<12}  {g['mod_37']:>5}  "
              f"{g['seed_name']:<14}  {g['dr']:>3}  {g['days_from_easter']:>6}")
    print()

    print("  ALL ASSERTIONS PASSED — TEMPORAL LOCK CONFIRMED")
    print("=" * 60)

    return {'seal': seal, 'position': pos, 'cycles': cycles,
            'null_gates': nulls, 'seed_gates': seeds}


if __name__ == "__main__":
    run()
