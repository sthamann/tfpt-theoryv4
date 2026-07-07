"""Loaders for the committed catalogs used by FO.02-FO.06.

All files live in SIBLING experiments (committed there); nothing is fetched:
  * FAST pol v5 FRB 20240114A -- frb-tfpt-signatures/data/FAST_FRB20240114A_pol_catalog_v5.csv
  * Blinkverse multi-source    -- frb-tfpt-signatures/data/blinkverse_bursts.csv
  * CHIME Cat1 (VizieR TSV)    -- frb-tfpt-signatures/data/chime_catalog1.tsv
  * CHIME Cat2 repeaters       -- repeater-cascade/data/chime_cat2_repeaters.csv

Anti double-counting (prereg): FRB 20240114A enters only via the v5 catalog and
is excluded from the Blinkverse selection; Blinkverse rows are deduplicated by
(source, mjd rounded to 1e-6 d).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

EXPS = Path(__file__).resolve().parents[3]
POL_CSV = EXPS / "frb-tfpt-signatures" / "data" / "FAST_FRB20240114A_pol_catalog_v5.csv"
BLINK_CSV = EXPS / "frb-tfpt-signatures" / "data" / "blinkverse_bursts.csv"
CAT1_TSV = EXPS / "frb-tfpt-signatures" / "data" / "chime_catalog1.tsv"
CAT2_CSV = EXPS / "repeater-cascade" / "data" / "chime_cat2_repeaters.csv"
LI_TSV = EXPS / "frb-tfpt-signatures" / "data" / "frb20121102_fast_li2021_1652.tsv"
ZHANG_CSV = EXPS / "repeater-cascade" / "data" / "frb20220912a_zhang2023.csv"

SESSION_GAP_D = 0.2
DAY_S = 86400.0


def _f(row: dict, key: str) -> float:
    try:
        return float(row[key])
    except (ValueError, KeyError, TypeError):
        return np.nan


@dataclass
class PolCatalog:
    """FRB 20240114A v5, time-sorted."""
    mjd: np.ndarray
    rm: np.ndarray
    rm_err: np.ndarray
    dm: np.ndarray
    weff_ms: np.ndarray
    dol: np.ndarray
    doc: np.ndarray
    pa_deg: np.ndarray


def load_pol_v5() -> PolCatalog:
    rows = []
    with POL_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            mjd = _f(r, "MJD_topo")
            if not np.isfinite(mjd):
                continue
            rm_err = 0.5 * (_f(r, "RM_err_left") + _f(r, "RM_err_right"))
            rows.append((mjd, _f(r, "RM"), rm_err, _f(r, "DM"), _f(r, "Weff(ms)"),
                         _f(r, "DOL"), _f(r, "DOC"), _f(r, "PA_mean(deg)")))
    rows.sort()
    cols = list(zip(*rows))
    return PolCatalog(*(np.array(c, dtype=float) for c in cols))


def sessions(mjd: np.ndarray, gap_d: float = SESSION_GAP_D) -> list[np.ndarray]:
    """Index arrays per session (gap > gap_d opens a session); >= 2 bursts."""
    edges = np.where(np.diff(mjd) > gap_d)[0] + 1
    return [idx for idx in np.split(np.arange(len(mjd)), edges) if len(idx) >= 2]


@dataclass
class SourceBursts:
    source: str
    mjd: np.ndarray
    energy: np.ndarray | None      # None if no usable energy/fluence column
    energy_kind: str = "none"


def load_blinkverse(min_bursts: int = 100, min_baseline_d: float = 200.0,
                    exclude: tuple[str, ...] = ("FRB20240114A",)) -> list[SourceBursts]:
    per_source: dict[str, dict[float, float]] = {}
    kind: dict[str, str] = {}
    with BLINK_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            src = (r.get("source") or "").strip()
            if not src or src in exclude:
                continue
            mjd = _f(r, "mjd")
            if not np.isfinite(mjd):
                continue
            e = _f(r, "energy")
            if not np.isfinite(e) or e <= 0:
                e = _f(r, "fluence")
                k = "fluence"
            else:
                k = "energy"
            key = round(mjd, 6)             # dedupe multi-reference rows
            d = per_source.setdefault(src, {})
            if key not in d or not np.isfinite(d[key]):
                d[key] = e if np.isfinite(e) and e > 0 else np.nan
                kind.setdefault(src, k)
    out = []
    for src, d in per_source.items():
        mjd = np.array(sorted(d))
        if len(mjd) < min_bursts or (mjd[-1] - mjd[0]) < min_baseline_d:
            continue
        e = np.array([d[m] for m in sorted(d)])
        has_e = np.isfinite(e).mean() > 0.5
        out.append(SourceBursts(src, mjd, e if has_e else None,
                                kind.get(src, "none") if has_e else "none"))
    return sorted(out, key=lambda s: -len(s.mjd))


def load_cat2(min_bursts: int = 50) -> list[SourceBursts]:
    per: dict[str, list[tuple[float, float]]] = {}
    with CAT2_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r.get("excluded_flag", "0").strip() == "1":
                continue
            mjd = _f(r, "mjd_400")
            if not np.isfinite(mjd):
                continue
            per.setdefault(r["repeater_name"].strip(), []).append(
                (mjd, _f(r, "fluence_jyms")))
    out = []
    for src, rows in per.items():
        if len(rows) < min_bursts:
            continue
        rows.sort()
        mjd = np.array([a for a, _ in rows])
        e = np.array([b for _, b in rows])
        out.append(SourceBursts(f"{src}(CHIME)", mjd,
                                e if np.isfinite(e).mean() > 0.5 else None, "fluence"))
    return sorted(out, key=lambda s: -len(s.mjd))


def load_li2021() -> SourceBursts:
    """FRB 20121102A (Li+2021 VizieR TSV): MJD + isotropic energy (erg)."""
    rows = []
    for r in csv.reader(LI_TSV.open(encoding="utf-8"), delimiter="\t"):
        if not r or (r[0].lstrip().startswith(("#", "recno", "-", "d", " "))
                     and not r[0].strip().isdigit()):
            continue
        try:
            rows.append((float(r[2]), float(r[12])))
        except (ValueError, IndexError):
            continue
    rows.sort()
    mjd = np.array([a for a, _ in rows])
    e = np.array([b for _, b in rows])
    keep = e > 0
    return SourceBursts("FRB20121102A(Li2021)", mjd[keep], e[keep], "energy")


def load_zhang2023() -> SourceBursts:
    """FRB 20220912A (Zhang+2023): barycentric MJD + energy (1e36 erg)."""
    rows = []
    with ZHANG_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                rows.append((float(r["mjd_bary"]), float(r["energy_1e36erg"])))
            except (ValueError, KeyError):
                continue
    rows.sort()
    mjd = np.array([a for a, _ in rows])
    e = np.array([b for _, b in rows])
    keep = e > 0
    return SourceBursts("FRB20220912A(Zhang2023)", mjd[keep], e[keep], "energy")


@dataclass
class RmSeries:
    """Per-burst multivariate series for the intra-session test (FO.02b)."""
    source: str
    mjd: np.ndarray
    obs: dict[str, np.ndarray]      # observable name -> per-burst values (nan-padded)


def pol_v5_series(cat: PolCatalog) -> RmSeries:
    w = np.where(cat.weff_ms > 0, cat.weff_ms, np.nan)
    return RmSeries("FRB20240114A", cat.mjd, {
        "RM": cat.rm, "DM": cat.dm, "log10Weff": np.log10(w), "DOL": cat.dol})


def load_blinkverse_20201124a() -> RmSeries:
    """FRB 20201124A per-burst RM series from the committed Blinkverse export
    (Xu+2022 rows; rm_qufit preferred, rm_syn fallback; dedup by mjd @1e-6 d)."""
    rows: dict[float, tuple] = {}
    with BLINK_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if (r.get("source") or "").strip() != "FRB20201124A":
                continue
            mjd = _f(r, "mjd")
            if not np.isfinite(mjd):
                continue
            rm = _f(r, "rm_qufit")
            if not np.isfinite(rm):
                rm = _f(r, "rm_syn")
            if not np.isfinite(rm):
                continue
            width = _f(r, "width")
            rows[round(mjd, 6)] = (rm,
                                   np.log10(width) if width > 0 else np.nan,
                                   _f(r, "polar_l"), _f(r, "polar_c"))
    mjd = np.array(sorted(rows))
    cols = np.array([rows[m] for m in sorted(rows)], dtype=float)
    return RmSeries("FRB20201124A", mjd, {
        "RM": cols[:, 0], "log10Width": cols[:, 1],
        "polar_L": cols[:, 2], "polar_C": cols[:, 3]})


@dataclass
class Cat1:
    """CHIME Cat1 first sub-bursts (Nsb==0, excluded_flag==0, clean width fit)."""
    log_width: np.ndarray          # log10 s (fitburst)
    log_bw: np.ndarray             # log10 MHz (B_Freq - b_Freq)
    is_repeater: np.ndarray        # bool
    n_flagged_out: int = 0


def load_cat1() -> Cat1:
    header: list[str] | None = None
    rows, n_out = [], 0
    for raw in CAT1_TSV.open(encoding="utf-8"):
        if raw.startswith("#") or not raw.strip():
            continue
        parts = [p.strip() for p in raw.rstrip("\n").split("\t")]
        if header is None:
            if parts and parts[0] == "recno":
                header = parts
            continue
        if not parts[0].isdigit():
            continue                      # units / dashes lines
        r = dict(zip(header, parts))
        if r.get("Flag") != "0" or r.get("Nsb") != "0":
            n_out += 1
            continue
        if r.get("l_Widthfitb") == "<":   # upper-limit width -> unusable
            n_out += 1
            continue
        try:
            w = float(r["Widthfitb"])
            hi, lo = float(r["B_Freq"]), float(r["b_Freq"])
        except (ValueError, KeyError):
            n_out += 1
            continue
        if w <= 0 or hi <= lo:
            n_out += 1
            continue
        rep = r.get("RpName", "-9999") not in ("-9999", "", None)
        rows.append((np.log10(w), np.log10(hi - lo), rep))
    lw = np.array([a for a, _, _ in rows])
    lb = np.array([b for _, b, _ in rows])
    y = np.array([c for _, _, c in rows], dtype=bool)
    return Cat1(lw, lb, y, n_out)
