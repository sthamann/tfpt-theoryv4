"""A4 -- GRB X-ray afterglow plateau: the widest-ln(t) astrophysical recovery-comb channel.

Why GRBs.  A Swift-XRT afterglow flux light curve spans ~100 s to ~10^6-10^7 s -- 4-5
decades in time, i.e. ~4-5 comb periods at lambda=(3/2)^6 -- so a SINGLE GRB clears the
hard ln(t)-range gate (>= 2.8 periods) that the ms-scale FRB tails (A3/A3b, ~1 decade) and
even most magnetar outbursts (A1, ~3 decades) struggle with. And there are >1000 public
Swift-XRT light curves, so the faint ~1.7% comb can be stacked with real statistics. This is
the widest-ln(t) astrophysical recovery in hand.

Observable.  The afterglow is a power law (plateau -> steeper decay), so the recovery
observable is y = ln(flux) and the detector's degree-2 poly-in-ln(t) baseline absorbs the
smooth power-law/break trend (identical treatment to the A1 magnetar channel); the test asks
only whether the kernel log-frequency omega = 2pi/ln((3/2)^6) = 2.583 is SPECIAL on top of
that smooth trend.

Firewall (honest).  A GRB X-ray plateau is a central-engine / accretion relaxation
(magnetar spin-down or fallback accretion), NOT a horizon recovery -- legitimacy 'surface'
(borderline, like the magnetar channel). A comb here would be a universal-DSI-shape result,
never a TFPT confirmation; a NULL on this wide-ln(t), high-statistics channel is the
informative outcome (it is NOT data-limited, unlike the horizon-legitimate A2/B4).

Data.  Public Swift-XRT GRB flux light curves from the UK Swift Science Data Centre
(Evans et al. 2007/2009, https://www.swift.ac.uk/xrt_curves/<targetID>/flux.qdp).
``fetch_all()`` pulls a curated set of long/plateau GRBs and normalises each to
``data/grb/<name>.csv`` (header ``t_s,flux,flux_err``, T0-relative seconds); the real GRB
name is read from the file header, so a wrong/curated target id self-corrects (it is simply
skipped if it does not return a valid light curve). NOTHING is fabricated.
"""
from __future__ import annotations

import csv
import time
import urllib.error
import urllib.request
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parents[2] / "data" / "grb"
UKSSDC = "https://www.swift.ac.uk/xrt_curves/{tid:08d}/flux.qdp"
UA = "tfpt-combdomains/0.1 (research; recovery-comb GRB channel)"

# Curated long / X-ray-plateau GRBs with wide-baseline Swift-XRT afterglows.  The 11-digit
# UKSSDC target id is the key; the human label is only a hint (the real name is read from the
# downloaded header).  A wrong id just misses -- never fabricated.
GRB_TARGETS: tuple[tuple[str, int], ...] = (
    ("GRB 060729", 221755),   # classic ~5-decade plateau (confirmed)
    ("GRB 060614", 214805),   # long, nearby (confirmed)
    ("GRB 070110", 255443),   # famous internal plateau + sharp drop
    ("GRB 061121", 239899),
    ("GRB 091029", 373570),
    ("GRB 100621A", 425151),
    ("GRB 130427A", 554620),  # brightest, very wide
    ("GRB 080319B", 306757),  # naked-eye
    ("GRB 061007", 232683),
    ("GRB 050801", 148522),
    ("GRB 060526", 211957),
    ("GRB 050922C", 156467),
    ("GRB 110213A", 445414),
    ("GRB 090618", 355083),
    ("GRB 081008", 331093),
    ("GRB 051221A", 173780),
    ("GRB 050416A", 114753),
    ("GRB 080430", 310613),
    ("GRB 060124", 178750),
    ("GRB 100418A", 419797),
    ("GRB 120326A", 518626),
    ("GRB 121128A", 539866),
    ("GRB 100901A", 433065),
    ("GRB 110422A", 451901),
)


def _parse_qdp(text: str) -> tuple[list[tuple[float, float, float]], str]:
    """Parse a UKSSDC flux.qdp: return ([(t_s, flux, flux_err)], grb_name).
    Columns (after `READ TERR 1 2`): Time, T+ve, T-ve, Flux, Fluxpos, Fluxneg.
    Handles the multiple WT/PC `! ... data` sections and `NO NO ...` separators."""
    name = ""
    rows: list[tuple[float, float, float]] = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("!") or s.startswith("READ") or s.startswith("@"):
            if "name:" in s:
                # "! ... name: GRB 060729 ..."
                frag = s.split("name:", 1)[1].strip()
                name = frag.split(",")[0].strip()
            continue
        if s.upper().startswith("NO"):           # section separator (NO NO NO ...)
            continue
        parts = s.split()
        if len(parts) < 4:
            continue
        try:
            t = float(parts[0])
            flux = float(parts[3])
            ferr = abs(float(parts[4])) if len(parts) > 4 else 0.0
        except ValueError:
            continue
        if t > 0 and flux > 0:
            rows.append((t, flux, ferr))
    rows.sort()
    return rows, name


def _write_csv(name: str, rows: list[tuple[float, float, float]]) -> Path:
    DATA.mkdir(parents=True, exist_ok=True)
    safe = name.replace(" ", "_")
    out = DATA / f"{safe}.csv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["t_s", "flux", "flux_err"])
        for t, f, e in rows:
            w.writerow([f"{t:.6g}", f"{f:.6g}", f"{e:.6g}"])
    return out


def fetch_one(tid: int, *, timeout: float = 30.0) -> tuple[Path, str, int] | None:
    """Fetch + normalise one GRB flux light curve. Returns (path, real_name, n_points) or None."""
    url = UKSSDC.format(tid=tid)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError, OSError):
        return None
    rows, name = _parse_qdp(text)
    if len(rows) < 6:
        return None
    name = name or f"GRB_target_{tid}"
    return _write_csv(name, rows), name, len(rows)


def fetch_all(targets: tuple[tuple[str, int], ...] = GRB_TARGETS,
              *, pause_s: float = 1.0) -> list[tuple[str, int]]:
    """Fetch the curated set (polite 1 s pause between requests). Returns [(name, n_points)]."""
    got: list[tuple[str, int]] = []
    for label, tid in targets:
        r = fetch_one(tid)
        if r is None:
            print(f"  MISS {label:14s} (target {tid:08d}) -- no valid light curve, skipped")
        else:
            _path, name, n = r
            got.append((name, n))
            print(f"  OK   {name:14s} (target {tid:08d}): {n} points")
        time.sleep(pause_s)
    print(f"\n  fetched {len(got)}/{len(targets)} GRB light curves into {DATA}")
    return got


def read_grb_csv(path: Path) -> tuple[np.ndarray, np.ndarray] | None:
    """Read a normalised GRB light curve (header t_s,flux[,flux_err]); return (t_s, flux)."""
    try:
        with path.open(encoding="utf-8") as fh:
            rd = csv.DictReader(fh)
            cols = {(c or "").strip().lower(): c for c in (rd.fieldnames or [])}
            tk = cols.get("t_s") or cols.get("t") or cols.get("t_days")
            fk = cols.get("flux") or cols.get("rate")
            if not tk or not fk:
                return None
            t, f = [], []
            for row in rd:
                try:
                    tv, fv = float(row[tk]), float(row[fk])
                except (TypeError, ValueError):
                    continue
                if tv > 0 and fv > 0:
                    t.append(tv)
                    f.append(fv)
    except OSError:
        return None
    return (np.array(t), np.array(f)) if len(t) >= 6 else None


def main(argv: list[str] | None = None) -> int:
    """`tfpt-combdomains fetch-grb` -- pull the curated Swift-XRT plateau-GRB light curves."""
    print("=" * 78)
    print("Fetch Swift-XRT GRB afterglow flux light curves (UKSSDC) for the A4 comb channel")
    print("=" * 78)
    fetch_all()
    print("\nNow run: tfpt-combdomains analyze   (A4 ingests data/grb/*.csv)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
