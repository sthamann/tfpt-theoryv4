"""A5 -- extreme/ambiguous nuclear transient (AGN-disk TDE) optical recovery-comb channel.

Why ENTs.  An extreme nuclear transient like J2245+3743 (AGN J224554.84+374326.5, z=2.554;
Graham et al. 2025, Nature Astronomy, arXiv:2511.02178) brightened by >40x in 2018 and has been
SLOWLY FADING for years -- the favoured reading is the tidal disruption of a >30 M_sun star in an
AGN accretion disk, with ~10^54 erg of UV/optical energy released.  A years-long optical fade is a
WIDE-ln(t) SINGLE recovery curve: the ZTF zr fade of J2245 spans ~3.2 comb periods at
lambda=(3/2)^6, clearing the hard >2.8 ln-range gate that the ms-scale FRB tails (A3/A3b) cannot
and that even most magnetar outbursts (A1) struggle with.  This is exactly the data type the
recovery-comb search is starved for, and it is the channel motivated by the J2245 note.

Observable.  The fade is a smooth power-law-ish decay in flux, so the recovery observable is
y = ln(flux) (flux = 10^(-0.4 mag)); the detector's degree-2 poly-in-ln(t) baseline absorbs the
smooth decay/break trend (identical treatment to the A1 magnetar and A4 GRB channels).  The test
asks only whether the kernel log-frequency omega = 2pi/ln((3/2)^6) = 2.583 -- or any TFPT
log-period in the battery -- is SPECIAL on top of that smooth trend.

Firewall (honest).  An AGN-disk TDE is an ACCRETION / central-engine relaxation, NOT a horizon
recovery -- legitimacy 'surface' (borderline, identical to the A4 GRB-plateau and A1 magnetar
channels).  A comb here would be a universal-DSI-shape coincidence, NEVER a TFPT confirmation; a
clean NULL on this wide-ln(t) curve is the informative outcome.  z=2.554 time-dilation stretches
the observed time axis MULTIPLICATIVELY = an additive shift in ln(t), so it moves the comb PHASE
but adds NO ln-range -- the years-long observed baseline + dense early sampling are what give the
range, not the redshift.

Data.  Public ZTF DR PSF photometry from the IRSA ZTF light-curve service (anonymous, no login):
``https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves?POS=CIRCLE <ra> <dec> <r>&FORMAT=CSV``.
``fetch_all()`` pulls the curated ENT list by position and normalises each to
``data/ent/<name>.csv`` (header ``mjd,mag,magerr,band``; only ``catflags==0`` good epochs).
NOTHING is fabricated -- a position with no ZTF detection simply yields no file.
"""
from __future__ import annotations

import csv
import io
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parents[2] / "data" / "ent"
IRSA = "https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves?"
UA = "tfpt-combdomains/0.1 (research; recovery-comb ENT channel)"
MAGERR_MAX = 0.30   # drop the noisiest epochs (keep catflags==0 AND a sane error)


@dataclass(frozen=True)
class EntTarget:
    name: str          # filesystem-safe id -> <name>.csv
    ra_deg: float
    dec_deg: float
    note: str


# Curated extreme/ambiguous nuclear transients with a wide-baseline ZTF fade.  Coordinates are the
# key; a position with no ZTF detection self-skips (never fabricated).  J2245 is verified against
# the IRSA service (oid 733101200023066, ~1440 good g/r/i epochs MJD 58242..60967).
ENT_TARGETS: tuple[EntTarget, ...] = (
    EntTarget("J2245+3743", 341.47850, 37.72403,
              "AGN J224554.84+374326.5, z=2.554; brightened >40x in 2018, slowly fading; "
              "AGN-disk TDE of a >30 Msun star (Graham+2025, Nat. Astron., arXiv:2511.02178)"),
)


def _build_url(ra: float, dec: float, radius_deg: float) -> str:
    pos = f"CIRCLE {ra:.6f} {dec:.6f} {radius_deg:.5f}"
    return IRSA + urllib.parse.urlencode({"POS": pos, "BANDNAME": "g,r,i", "FORMAT": "CSV"})


def _parse_irsa(text: str) -> list[tuple[float, float, float, str]]:
    """Parse the IRSA ZTF light-curve CSV: keep catflags==0 + magerr<=MAGERR_MAX good epochs.
    Returns [(mjd, mag, magerr, band)] sorted by mjd. ``band`` is the ZTF filtercode (zg/zr/zi)."""
    out: list[tuple[float, float, float, str]] = []
    for row in csv.DictReader(io.StringIO(text)):
        try:
            if int(float(row["catflags"])) != 0:
                continue
            mjd = float(row["mjd"])
            mag = float(row["mag"])
            magerr = float(row["magerr"])
            band = (row["filtercode"] or "").strip()
        except (KeyError, TypeError, ValueError):
            continue
        if mjd > 0 and mag > 0 and 0.0 < magerr <= MAGERR_MAX and band:
            out.append((mjd, mag, magerr, band))
    out.sort()
    return out


def _write_csv(name: str, rows: list[tuple[float, float, float, str]]) -> Path:
    DATA.mkdir(parents=True, exist_ok=True)
    out = DATA / f"{name}.csv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["mjd", "mag", "magerr", "band"])
        for mjd, mag, magerr, band in rows:
            w.writerow([f"{mjd:.6f}", f"{mag:.4f}", f"{magerr:.4f}", band])
    return out


def fetch_one(tg: EntTarget, *, radius_deg: float = 0.0014, timeout: float = 120.0
              ) -> tuple[Path, int] | None:
    """Fetch + normalise one ENT ZTF light curve. Returns (path, n_good_epochs) or None."""
    req = urllib.request.Request(_build_url(tg.ra_deg, tg.dec_deg, radius_deg),
                                 headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
            text = resp.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError, OSError):
        return None
    rows = _parse_irsa(text)
    if len(rows) < 6:
        return None
    return _write_csv(tg.name, rows), len(rows)


def fetch_all(targets: tuple[EntTarget, ...] = ENT_TARGETS,
              *, pause_s: float = 1.0) -> list[tuple[str, int]]:
    """Fetch the curated ENT set from IRSA (polite pause). Returns [(name, n_epochs)]."""
    got: list[tuple[str, int]] = []
    for tg in targets:
        r = fetch_one(tg)
        if r is None:
            print(f"  MISS {tg.name:14s} (RA={tg.ra_deg:.4f} Dec={tg.dec_deg:+.4f}) -- "
                  "no ZTF light curve returned, skipped")
        else:
            path, n = r
            got.append((tg.name, n))
            print(f"  OK   {tg.name:14s}: {n} good epochs -> {path.name}")
        time.sleep(pause_s)
    print(f"\n  fetched {len(got)}/{len(targets)} ENT light curves into {DATA}")
    return got


def read_ent_curves(path: Path) -> list[tuple[str, np.ndarray, np.ndarray]]:
    """Read a normalised ENT light curve (header ``mjd,mag,magerr,band``) into per-band recovery
    curves.  For each ZTF band: flux = 10^(-0.4 mag); the recovery origin is the brightest epoch
    (max flux = min mag); returns [(band, t_days_post_peak, ln_flux)] for post-peak points only.
    Bands with < 6 post-peak points are dropped."""
    try:
        with path.open(encoding="utf-8") as fh:
            rd = csv.DictReader(fh)
            cols = {(c or "").strip().lower(): c for c in (rd.fieldnames or [])}
            mk, gk, bk = cols.get("mjd"), cols.get("mag"), cols.get("band")
            if not mk or not gk or not bk:
                return []
            by_band: dict[str, list[tuple[float, float]]] = {}
            for row in rd:
                try:
                    mjd, mag, band = float(row[mk]), float(row[gk]), (row[bk] or "").strip()
                except (TypeError, ValueError):
                    continue
                if mjd > 0 and mag > 0 and band:
                    by_band.setdefault(band, []).append((mjd, mag))
    except OSError:
        return []

    out: list[tuple[str, np.ndarray, np.ndarray]] = []
    for band, pts in by_band.items():
        pts.sort()
        mjd = np.array([p[0] for p in pts], float)
        mag = np.array([p[1] for p in pts], float)
        flux = 10.0 ** (-0.4 * mag)
        t = mjd - mjd[int(np.argmax(flux))]   # origin = brightest (max-flux) epoch
        m = t > 0
        if int(m.sum()) >= 6:
            out.append((band, t[m], np.log(flux[m])))
    return out


def bin_ln_t(t: np.ndarray, y: np.ndarray, *, n_bins: int = 70, min_count: int = 2
             ) -> tuple[np.ndarray, np.ndarray]:
    """Equal-ln(t) bins -> (t_center, median y per bin).  Near-uniform ln(t) weighting (the natural
    frame for a log-periodic comb) that also damps the stochastic AGN/seasonal scatter; the comb
    survives as a residual on y(ln t).  Mirrors quake.rate_curve for a flux observable."""
    t = np.asarray(t, float)
    y = np.asarray(y, float)
    lt = np.log(t)
    edges = np.linspace(lt.min(), lt.max(), n_bins + 1)
    idx = np.clip(np.digitize(lt, edges) - 1, 0, n_bins - 1)
    tc, yb = [], []
    for j in range(n_bins):
        sel = idx == j
        if int(np.sum(sel)) >= min_count:
            tc.append(float(np.exp(0.5 * (edges[j] + edges[j + 1]))))
            yb.append(float(np.median(y[sel])))
    return np.array(tc), np.array(yb)


def main(argv: list[str] | None = None) -> int:
    """`tfpt-combdomains fetch-ent` -- pull the curated ENT ZTF light curves (IRSA) for A5."""
    print("=" * 78)
    print("Fetch ZTF DR optical light curves (IRSA) for the A5 nuclear-transient comb channel")
    print("=" * 78)
    fetch_all()
    print("\nNow run: tfpt-combdomains analyze   (A5 ingests data/ent/*.csv)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
