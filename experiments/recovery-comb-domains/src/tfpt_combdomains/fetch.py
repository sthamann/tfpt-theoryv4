"""Get REAL magnetar outburst light curves for the A1 recovery-comb channel.

The A1 channel needs post-outburst X-ray flux(t) over days..years (wide ln t) for one or more
transient magnetars. Two honest, reproducible paths (NOTHING is ever fabricated):

  1. ``--normalize`` (guaranteed): convert a real table you downloaded -- a Swift/XRT light curve
     (UKSSDC "build your own light curve") or a Coti Zelati+2018 Magnetar Outburst Online Catalogue
     ("download all data", http://magnetars.ice.csic.es) export -- into the canonical schema
     ``data/magnetar/<source>.csv`` with header ``t_days,flux[,flux_err]`` (onset-relative days).

  2. ``--swift`` (best-effort auto): if the ``swifttools`` package is installed
     (``pip install swifttools``), pull Swift-XRT long-term light curves for the curated
     transient-magnetar list by position. On any API/network failure the precise manual step for
     that source is printed instead -- never a placeholder curve.

After fetching, run ``tfpt-combdomains analyze`` -- A1 ingests every ``data/magnetar/*.csv``,
tests the kernel omega=2.58 per outburst, and STACKS them (see comb.stacked_comb_test).
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "magnetar"


@dataclass(frozen=True)
class Target:
    name: str          # filesystem-safe source id (becomes <name>.csv)
    onset_mjd: float    # outburst onset (t_days = MJD - onset_mjd)
    ra_deg: float
    dec_deg: float
    note: str


# Curated transient magnetars with a well-defined outburst onset and a wide (days..years) X-ray
# monitoring baseline -- the regime where a ~3-decade ln(t) recovery comb could live.
TARGETS: tuple[Target, ...] = (
    Target("Swift_J1822.3-1606", 55757.0, 275.5854, -16.0726,
           "2011-07-15 outburst; Swift/XMM/Chandra (Scholz+2012, Rea+2012)"),
    Target("SGR_1745-2900", 56410.0, 266.4172, -29.0080,
           "2013-04-24 Galactic-centre magnetar; Swift/Chandra (Coti Zelati+2015)"),
    Target("1E_1547.0-5408", 54852.0, 237.7250, -54.3064,
           "2009-01-22 outburst; Swift/XMM (Bernardini+2011)"),
    Target("Swift_J1818.0-1607", 58920.0, 274.5100, -16.1300,
           "2020-03-12 outburst; Swift/NICER/NuSTAR"),
    Target("SGR_1935+2154", 56843.0, 293.7322, 21.8967,
           "2014-07-05 first activation; many outbursts; Swift/NICER"),
    Target("XTE_J1810-197", 58088.0, 272.4612, -19.7314,
           "2018 reactivation; Swift/NICER (2003 outburst pre-Swift)"),
)


def _write_csv(name: str, rows: list[tuple[float, float, float | None]]) -> Path:
    rows = sorted((t, f, e) for t, f, e in rows if t > 0 and f > 0)
    DATA.mkdir(parents=True, exist_ok=True)
    out = DATA / f"{name}.csv"
    has_err = any(e is not None for _, _, e in rows)
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["t_days", "flux", "flux_err"] if has_err else ["t_days", "flux"])
        for t, f, e in rows:
            w.writerow([f"{t:.6g}", f"{f:.6g}", f"{e:.6g}"] if has_err else [f"{t:.6g}", f"{f:.6g}"])
    return out


def _read_table(path: Path) -> list[list[str]]:
    """Read a CSV or whitespace/qdp table into rows of string cells (comment lines dropped)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    rows: list[list[str]] = []
    delim_csv = "," in text.splitlines()[0] if text.strip() else False
    for line in text.splitlines():
        s = line.strip()
        if not s or s[0] in "#!;" or s.upper().startswith(("READ", "NO ", "@")):
            continue
        rows.append(next(csv.reader([s])) if delim_csv else s.split())
    return rows


def normalize(raw: Path, name: str, *, onset_mjd: float | None, time_col: int, flux_col: int,
              err_col: int | None, is_mjd: bool) -> Path:
    """Convert a real downloaded table -> canonical data/magnetar/<name>.csv. Column indices are
    0-based; ``--mjd`` converts an MJD time column to onset-relative days using ``onset_mjd``."""
    rows = _read_table(raw)
    out_rows: list[tuple[float, float, float | None]] = []
    for r in rows:
        try:
            tv = float(r[time_col])
            fv = float(r[flux_col])
        except (IndexError, ValueError):
            continue
        if is_mjd:
            if onset_mjd is None:
                raise SystemExit("ERROR: --mjd requires --onset-mjd (or a curated --source).")
            tv = tv - onset_mjd
        ev: float | None = None
        if err_col is not None:
            try:
                ev = abs(float(r[err_col]))
            except (IndexError, ValueError):
                ev = None
        out_rows.append((tv, fv, ev))
    if len(out_rows) < 6:
        raise SystemExit(f"ERROR: parsed only {len(out_rows)} usable (t>0,flux>0) rows from {raw}.")
    out = _write_csv(name, out_rows)
    print(f"  wrote {out}  ({sum(1 for t, *_ in out_rows if t > 0)} points)")
    return out


def fetch_swift(targets: tuple[Target, ...], radius_arcsec: float = 40.0) -> int:
    """Swift-XRT long-term light curves via the UKSSDC ``swifttools`` package (LSXPS catalogue):
    cone-search each curated position -> nearest LSXPS source -> its observation-binned total-band
    rate curve -> normalised data/magnetar/<source>.csv. Degrades to a precise manual instruction
    per source if the package/API/network is unavailable (never a placeholder curve).

    Note: swifttools needs ``distutils`` (import setuptools shims it on Python >= 3.12)."""
    try:
        import setuptools  # noqa: F401, PLC0415  (enables the distutils shim on Python >= 3.12)
    except Exception:  # noqa: BLE001, S110
        pass
    try:
        from swifttools.ukssdc.query import SXPSQuery  # noqa: PLC0415 (optional heavy dep)
    except Exception as exc:  # noqa: BLE001
        print(f"  swifttools unavailable ({exc}).")
        print("  install:  pip install swifttools setuptools   (Python <= 3.13 recommended)")
        _print_manual(targets)
        return 1
    got = 0
    for tg in targets:
        try:
            q = SXPSQuery(cat="LSXPS", silent=True)
            q.addConeSearch(ra=tg.ra_deg, dec=tg.dec_deg, radius=radius_arcsec, units="arcsec")
            q.submit()
            res = q.results
            if res is None or len(res) == 0:
                print(f"  {tg.name}: no LSXPS source within {radius_arcsec:.0f}\"; {tg.note}")
                continue
            sid = int(res.iloc[0]["LSXPS_ID"])          # results are sorted by offset -> nearest
            q.getLightCurves(timeFormat="MJD", binning="observation", bands="all", returnData=True)
            block = q.lightCurves.get(sid) or next(iter(q.lightCurves.values()))
            df = block.get("Total_rates") if isinstance(block, dict) else None
            if df is None or len(df) < 6:
                print(f"  {tg.name}: LSXPS {sid} has too few total-band points; {tg.note}")
                continue
            rows = [(float(r["Time"]) - tg.onset_mjd, float(r["Rate"]),
                     0.5 * (abs(float(r.get("RatePos", 0.0))) + abs(float(r.get("RateNeg", 0.0))))
                     or None)
                    for _, r in df.iterrows()]
            out = _write_csv(tg.name, rows)
            npos = sum(1 for t, *_ in rows if t > 0)
            got += 1
            print(f"  {tg.name}: LSXPS {sid} ({res.iloc[0].get('IAUName', '?')}), {len(rows)} pts "
                  f"({npos} post-onset) -> {out.name}")
        except Exception as exc:  # noqa: BLE001
            print(f"  {tg.name}: swifttools fetch failed ({exc}); manual: {tg.note}")
    print(f"\n  fetched {got}/{len(targets)} via swifttools (LSXPS). Now run `... analyze`.")
    return 0 if got else 1


def _print_manual(targets: tuple[Target, ...]) -> None:
    print("\n  MANUAL (guaranteed) -- download a real light curve, then normalise it:")
    print("    Swift/XRT: https://www.swift.ac.uk/user_objects/  (build a light curve at the RA/Dec)")
    print("    MOOC:      http://magnetars.ice.csic.es  ('download all data' per source)")
    print("    then:  tfpt-combdomains fetch-magnetar --normalize <file> --source <name> "
          "--time-col 0 --flux-col 1 [--err-col 2] [--mjd]")
    print("\n  curated targets (name  onset_MJD  RA  Dec):")
    for tg in targets:
        print(f"    {tg.name:22s} {tg.onset_mjd:9.1f}  {tg.ra_deg:8.4f} {tg.dec_deg:+8.4f}  {tg.note}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="fetch-magnetar",
                                 description="Fetch/normalise real magnetar light curves for A1.")
    ap.add_argument("--list", action="store_true", help="print the curated magnetar targets")
    ap.add_argument("--swift", action="store_true", help="best-effort Swift-XRT fetch via swifttools")
    ap.add_argument("--normalize", metavar="RAWFILE", help="convert a downloaded table to canonical CSV")
    ap.add_argument("--source", help="curated target name (sets onset MJD) or a free-form id")
    ap.add_argument("--onset-mjd", type=float, help="outburst onset MJD (for --mjd, if not curated)")
    ap.add_argument("--time-col", type=int, default=0)
    ap.add_argument("--flux-col", type=int, default=1)
    ap.add_argument("--err-col", type=int, default=None)
    ap.add_argument("--mjd", action="store_true", help="time column is MJD -> convert to onset-rel days")
    args = ap.parse_args(argv)

    by_name = {t.name: t for t in TARGETS}
    if args.list or not (args.swift or args.normalize):
        _print_manual(TARGETS)
        return 0
    if args.swift:
        return fetch_swift(TARGETS)
    raw = Path(args.normalize)
    if not raw.exists():
        raise SystemExit(f"ERROR: {raw} not found.")
    name = args.source or raw.stem
    onset = args.onset_mjd
    if name in by_name and onset is None:
        onset = by_name[name].onset_mjd
    normalize(raw, name, onset_mjd=onset, time_col=args.time_col, flux_col=args.flux_col,
              err_col=args.err_col, is_mjd=args.mjd)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
