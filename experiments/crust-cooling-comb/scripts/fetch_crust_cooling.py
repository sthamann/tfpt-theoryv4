#!/usr/bin/env python3
"""Regenerate the small derived crust-cooling CSVs in ``data/`` from published tables.

HONEST PROVENANCE (read this): neutron-star crust-cooling curves are published as spectral-fit
tables (kT_eff^infty per observation), NOT as machine-readable VizieR/FITS catalogues. Every point
below is **transcribed from the published paper table** (`transcribed`), not digitised from a
figure and not fabricated -- transcribing a printed *table* is more accurate than figure
digitisation. Where the paper reports MJD we convert with the paper's own end-of-outburst epoch
`t0`; where it reports `t - t0` (days since outburst end) we use that directly. Two `t0` values are
ESTIMATED (flagged `t0_estimated`) because the paper states the month, not an MJD; both affected
curves are range-blind anyway, so the estimate cannot move any verdict.

Each source -> ``data/<name>.csv`` with header ``t_days_since_outburst,kT_eff_eV,err``.
kT_eff is the redshift-corrected effective surface temperature seen by an observer at infinity.

Run:  python scripts/fetch_crust_cooling.py
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"


@dataclass
class Curve:
    name: str                         # -> data/<name>.csv
    source: str                       # physical source (for grouping distinct worlds)
    provenance: str                   # paper + table, cited
    ingest: str                       # "transcribed" (from a printed table) -- honesty tag
    mode: str                         # "mjd" (rows are MJD) | "tsince" (rows are t-t0 days)
    t0: float | None                  # end-of-outburst MJD (mode="mjd"); else None
    rows: list[tuple[float, float, float]]  # (MJD-or-tdays, kT_eff_eV, err_eV)
    notes: str = ""
    t0_estimated: bool = False        # honesty flag: is t0 an estimate (month only)?
    excluded: list[int] = field(default_factory=list)  # row indices dropped (flares etc.)


# ---------------------------------------------------------------- the six named targets (real) ---
CURVES: list[Curve] = [
    # === KS 1731-260 === 12.5-yr outburst, ended 2001; monitored 14.5 yr to crust-core equilibrium.
    Curve(
        "KS1731-260", "KS1731-260",
        "Merritt et al. 2016, ApJ 833, 186, Table 1 (redshift-corrected kT_eff^inf; "
        "t0 = MJD 51930.5, last outburst detection, Cackett et al. 2006).",
        "transcribed", "mjd", 51930.5,
        [(51995.1, 104.6, 1.3), (52165.7, 89.5, 1.03), (52681.6, 76.4, 1.8),
         (52859.5, 73.8, 1.9), (53430.5, 71.7, 1.4), (53512.9, 70.3, 1.9),
         (54969.7, 64.5, 1.8), (57242.1, 64.4, 1.2)],
        notes="Crust reached thermal equilibrium with the core by ~3200 d (kTeff floor ~64 eV).",
    ),
    # === MXB 1659-29 === two independent cooling epochs (outburst I ended MJD 52162; II MJD 57809.7)
    Curve(
        "MXB1659-29_ob1", "MXB1659-29",
        "Parikh et al. 2019, A&A 624, A84, Table 1 (After Outburst I; t0 = MJD 52162).",
        "transcribed", "mjd", 52162.0,
        [(52197.7, 111.1, 1.3), (52563.0, 79.5, 1.6), (52711.6, 73.0, 1.9),
         (52768.7, 67.8, 2.1), (53566.4, 55.5, 2.4), (54583.8, 54.8, 3.2)],
        notes="~2.5-yr outburst I; cooled ~111->55 eV. Independent relaxation epoch #1 of this NS.",
    ),
    Curve(
        "MXB1659-29_ob2", "MXB1659-29",
        "Parikh et al. 2019, A&A 624, A84, Table 1 (After Outburst II; t0 = MJD 57809.7).",
        "transcribed", "mjd", 57809.7,
        [(57822.0, 91.5, 8.8), (57835.8, 87.9, 1.4), (57868.0, 82.7, 2.0),
         (57937.6, 74.8, 2.5), (57987.3, 75.1, 2.4), (58151.5, 66.0, 3.0),
         (58314.4, 56.3, 4.2)],
        notes="~1.7-yr outburst II (2015-2017); cooled ~92->56 eV. Independent relaxation epoch #2.",
    ),
    # === XTE J1701-462 === 1.6-yr super-Eddington outburst ended MJD 54321.95 (t0). Fast cooler.
    Curve(
        "XTEJ1701-462", "XTEJ1701-462",
        "Fridriksson et al. 2011, ApJ 736, 162, Table 1 (t-t0 in days; t0 = MJD 54321.95; "
        "1sigma errors). XMM-3 (row idx 5) is an accretion FLARE (PL frac 53%), EXCLUDED per paper.",
        "transcribed", "tsince", None,
        [(2.95, 163.1, 3.5), (10.81, 158.2, 2.5), (16.24, 155.2, 1.3), (49.49, 149.2, 1.3),
         (174.33, 128.7, 4.7), (225.72, 157.8, 1.8), (298.30, 135.1, 2.0), (431.07, 125.5, 3.1),
         (540.08, 125.0, 1.5), (592.68, 128.4, 2.3), (652.62, 123.3, 2.2), (705.38, 123.0, 2.0),
         (795.63, 123.7, 1.7), (1158.84, 120.6, 1.7)],
        excluded=[5],  # XMM-3 flare (kT jumps to 157.8 between ~129 and ~135 eV neighbours)
        notes="e-folding ~112-133 d; floor kTeq ~123 eV. Flare row 5 (XMM-3) dropped.",
    ),
    # === EXO 0748-676 === ~24-yr outburst ended 2008 Sep (MJD 54714). Small temperature swing.
    Curve(
        "EXO0748-676", "EXO0748-676",
        "Degenaar et al. 2014, ApJ 791, 47, Table 2 (kT_eff^inf; t0 = MJD 54714, Degenaar+2009; "
        "90% CL errors). 1980 Einstein pre-outburst point excluded (not part of the cooling).",
        "transcribed", "mjd", 54714.0,
        [(54755.5, 129.1, 2.3), (54776.0, 126.1, 2.2), (54886.0, 122.6, 2.6),
         (54908.0, 120.0, 2.0), (54992.0, 117.8, 2.5), (55013.0, 115.5, 2.2),
         (55306.0, 116.8, 2.5), (55364.0, 116.2, 1.9), (55489.0, 115.4, 2.2),
         (55745.0, 117.6, 2.2), (56505.0, 109.9, 2.0)],
        notes="Cooled ~129->110 eV; shallow swing. (Parikh+2020 later report a late-time rise.)",
    ),
    # === MAXI J0556-332 === strongest-heated NS; multi-outburst (t0 = end of outburst I).
    Curve(
        "MAXIJ0556-332_ob1", "MAXIJ0556-332",
        "Parikh et al. 2017, ApJL 851, L28, Table 1 (days since end of outburst I). Rows 1-11: "
        "outburst-I cooling; outburst II did NOT significantly reheat, so cooling continues on trend.",
        "transcribed", "tsince", None,
        [(5.4, 333.1, 5.5), (16.0, 324.1, 2.5), (23.3, 305.4, 2.5), (51.0, 286.9, 1.9),
         (104.3, 255.2, 0.9), (134.9, 247.1, 1.0), (150.8, 246.8, 2.1), (291.7, 215.8, 2.2),
         (496.8, 186.8, 1.0), (850.1, 161.5, 0.8), (1222.6, 145.4, 1.0)],
        notes="Cooled ~333->145 eV. Hottest known crust cooler (~15-17 MeV/nucleon shallow heat).",
    ),
    Curve(
        "MAXIJ0556-332_ob3", "MAXIJ0556-332",
        "Parikh et al. 2017, ApJL 851, L28, Table 1 (After Outburst III), re-zeroed to end of "
        "outburst III. t0(OBIII) ESTIMATED ~1443 d after end of OB I (paper: last point ~350 d "
        "after OBIII end); re-cooling ~167->131 eV.",
        "transcribed", "tsince", None,
        [(7.6, 166.9, 1.8), (40.1, 155.1, 2.8), (101.2, 142.9, 3.3), (127.5, 139.9, 1.4),
         (232.4, 135.6, 3.5), (350.0, 130.9, 1.5)],
        t0_estimated=True,
        notes="Outburst III reheated the crust to ~167 eV; independent re-cooling epoch.",
    ),
    # === Aql X-1 === recurrent transient (outburst ~yearly); crust NEVER fully cools -> messy.
    Curve(
        "AqlX-1_2016", "AqlX-1",
        "Li/Ootes et al. 2019, MNRAS 488, 99 (stz1963), Table 1 (2016-2017 quiescence; kT_eff^inf). "
        "t0 ESTIMATED ~MJD 57650 (outburst 'ceased 2016 September'; quiescence began before Oct 10).",
        "transcribed", "mjd", 57650.0,
        [(57677.7, 118.9, 4.5), (57692.9, 116.2, 2.8), (57714.8, 117.5, 1.3),
         (57804.7, 110.7, 1.1), (57859.1, 102.6, 2.5)],
        t0_estimated=True,
        notes="FIREWALL-MESSY: recurrent (~yearly) short outbursts; crust does not reach the core "
              "floor between them (Ootes+2018). Short baseline -> range-blind. Included for the "
              "named target list; low weight.",
    ),
]


def write_all() -> list[tuple[str, int, float, float]]:
    DATA.mkdir(parents=True, exist_ok=True)
    out: list[tuple[str, int, float, float]] = []
    for c in CURVES:
        rows = []
        for i, (a, kt, err) in enumerate(c.rows):
            if i in c.excluded:
                continue
            t = (a - c.t0) if c.mode == "mjd" else a
            if t > 0:
                rows.append((round(t, 3), kt, err))
        rows.sort()
        path = DATA / f"{c.name}.csv"
        with path.open("w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["# source", c.source])
            w.writerow(["# provenance", c.provenance])
            w.writerow(["# ingest", c.ingest + (" (t0 ESTIMATED)" if c.t0_estimated else "")])
            if c.notes:
                w.writerow(["# notes", c.notes])
            w.writerow(["t_days_since_outburst", "kT_eff_eV", "err"])
            for t, kt, err in rows:
                w.writerow([f"{t:.3f}", f"{kt:.4g}", f"{err:.4g}"])
        tmin = min(r[0] for r in rows)
        tmax = max(r[0] for r in rows)
        out.append((c.name, len(rows), tmin, tmax))
        print(f"  wrote {path.name:24s} {len(rows):2d} pts  t=[{tmin:.1f}, {tmax:.1f}] d"
              + ("  [t0 estimated]" if c.t0_estimated else ""))
    return out


def main() -> int:
    print("=" * 82)
    print("Regenerating derived crust-cooling CSVs from PUBLISHED TABLES (transcribed, cited)")
    print("=" * 82)
    got = write_all()
    n_src = len({c.source for c in CURVES})
    print(f"\n  {len(got)} cooling episodes across {n_src} distinct sources -> {DATA}")
    print("  All points transcribed from published spectral-fit tables (not figure-digitised, "
          "not fabricated).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
