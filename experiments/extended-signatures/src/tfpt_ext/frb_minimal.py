"""Standalone FRB loaders + echo/PA tests (no frb_tfpt package import)."""

from __future__ import annotations

import csv
import math
import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

FRB_DATA = Path(__file__).resolve().parents[3] / "frb-tfpt-signatures" / "data"

ECHO_TARGETS = (
    ("lambda2", 64 / 729),
    ("sqrt_lambda2", 8 / 27),
    ("two_thirds", 2 / 3),
)


@dataclass
class Series:
    source: str
    available: bool
    mjd: np.ndarray
    energy: np.ndarray = field(default_factory=lambda: np.array([]))
    fluence: np.ndarray = field(default_factory=lambda: np.array([]))
    pa_deg: np.ndarray = field(default_factory=lambda: np.array([]))

    def __len__(self) -> int:
        return len(self.mjd)


def _read_vizier(path: Path) -> tuple[list[str], list[list[str]]]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    body = [ln for ln in lines if ln and not ln.startswith("#")]
    if len(body) < 4:
        raise ValueError(f"{path}: not a VizieR table")
    cols = [c.strip() for c in body[0].split("\t")]
    rows = []
    for ln in body[3:]:
        if set(ln.replace("\t", "")) <= set("- "):
            continue
        cells = ln.split("\t")
        if len(cells) == len(cols):
            rows.append([c.strip() for c in cells])
    return cols, rows


def _col(cols: list[str], rows: list[list[str]], name: str) -> np.ndarray:
    j = cols.index(name)
    out = np.full(len(rows), np.nan)
    for i, r in enumerate(rows):
        v = r[j]
        if v in ("", "-9999", "-9999.0"):
            continue
        try:
            out[i] = float(v)
        except ValueError:
            pass
    return out


def load_fast_121102() -> Series:
    path = FRB_DATA / "frb20121102_fast_li2021_1652.tsv"
    if not path.exists():
        return Series("FRB 20121102A (FAST)", False, np.array([]))
    cols, rows = _read_vizier(path)
    return Series(
        "FRB 20121102A (FAST, Li+2021)",
        True,
        _col(cols, rows, "MJD"),
        energy=_col(cols, rows, "E"),
        fluence=_col(cols, rows, "Fluence"),
    )


def _read_delimited(path: Path) -> tuple[list[str], list[list[str]]]:
    rows_raw = [ln for ln in path.read_text(encoding="utf-8", errors="replace").splitlines()
                if ln.strip() and not ln.lstrip().startswith("#")]
    delim = "\t" if rows_raw and rows_raw[0].count("\t") >= rows_raw[0].count(",") else ","
    header = [c.strip().lower() for c in rows_raw[0].split(delim)]
    data = [r.split(delim) for r in rows_raw[1:] if len(r.split(delim)) == len(header)]
    return header, data


def load_fast_20240114A_pol() -> Series:
    for cand in (
        "FAST_FRB20240114A_pol_catalog_v5.csv",
        "FAST_FRB20240114A_pol_catalog.csv",
        "frb20240114A_fast_pol_catalog.tsv",
    ):
        path = FRB_DATA / cand
        if not path.exists():
            continue
        header, rows = _read_delimited(path)
        aliases = {
            "mjd": ["mjd", "mjd_topo", "mjdtopo"],
            "pa": ["pa", "pa_deg", "pa_mean(deg)", "pa_mean"],
        }

        def grab(key: str) -> np.ndarray:
            for alias in aliases[key]:
                if alias in header:
                    j = header.index(alias)
                    out = np.full(len(rows), np.nan)
                    for i, r in enumerate(rows):
                        try:
                            out[i] = float(re.sub(r"\([^)]*\)", "", r[j].split("+or-")[0]).strip())
                        except (ValueError, IndexError):
                            pass
                    return out
            return np.array([])

        mjd, pa = grab("mjd"), grab("pa")
        if mjd.size == 0:
            continue
        return Series("FRB 20240114A (FAST pol)", True, mjd, pa_deg=pa)
    return Series("FRB 20240114A (FAST pol)", False, np.array([]))


def blinkverse_series(min_bursts: int = 200) -> list[Series]:
    path = FRB_DATA / "blinkverse_bursts.csv"
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        rows = list(csv.DictReader(fh))
    by_src: dict[str, list[dict]] = {}
    for r in rows:
        s = (r.get("source") or "").strip()
        if s:
            by_src.setdefault(s, []).append(r)
    out: list[Series] = []

    def fval(x) -> float:
        s = str(x or "").strip()
        if not s:
            return np.nan
        try:
            return float(re.split(r"\+or-", s)[0].split()[0])
        except ValueError:
            return np.nan

    for src, rs in sorted(by_src.items(), key=lambda kv: -len(kv[1])):
        if len(rs) < min_bursts:
            continue
        mjd = np.array([fval(r.get("mjd")) for r in rs])
        energy = np.array([fval(r.get("energy")) for r in rs])
        fluence = np.array([fval(r.get("fluence")) for r in rs])
        out.append(Series(f"{src} (Blinkverse)", True, mjd, energy=energy, fluence=fluence))
    return out


def all_series() -> list[Series]:
    series: list[Series] = []
    s = load_fast_121102()
    if s.available:
        series.append(s)
    pol = load_fast_20240114A_pol()
    if pol.available and pol.pa_deg.size:
        series.append(pol)
    series.extend(blinkverse_series())
    return series


@dataclass
class EchoHit:
    name: str
    p_value: float


@dataclass
class EchoResult:
    source: str
    n_pairs: int
    hits: list[EchoHit] = field(default_factory=list)
    note: str = ""


def echo_ratio_test(
    source: str,
    fluence: np.ndarray,
    mjd: np.ndarray,
    cluster_dt_days: float = 1.0,
    seed: int = 0,
) -> EchoResult:
    order = np.argsort(mjd)
    f, t = fluence[order], mjd[order]
    ok = np.isfinite(f) & (f > 0) & np.isfinite(t)
    f, t = f[ok], t[ok]
    lr = np.log10(f[1:] / f[:-1])
    dt = np.diff(t)
    lr = lr[dt <= cluster_dt_days]
    n = len(lr)
    if n < 10:
        return EchoResult(source, n, [], "too few pairs")

    rng = np.random.default_rng(seed)
    logf = np.log10(f)
    hits: list[EchoHit] = []
    for name, ratio in ECHO_TARGETS:
        for lt in (math.log10(ratio), -math.log10(ratio)):
            obs = int(np.sum(np.abs(lr - lt) <= 0.1))
            null = []
            for _ in range(1000):
                s = rng.permutation(logf)
                null.append(int(np.sum(np.abs(np.diff(s)[:n] - lt) <= 0.1)))
            p = float((1 + sum(x >= obs for x in null)) / (len(null) + 1))
            hits.append(EchoHit(name, p))
    return EchoResult(source, n, hits)


@dataclass
class PaResult:
    best_m: int
    p_value: float


def pa_angle_classes(pa_deg: np.ndarray, m_values: tuple[int, ...] = (2, 4, 8), seed: int = 0) -> PaResult:
    pa = pa_deg[np.isfinite(pa_deg)] % 180.0
    n = len(pa)
    if n < 10:
        return PaResult(0, 1.0)

    def z_stat(m: int) -> float:
        th = np.deg2rad(2.0 * m * pa)
        return n * (np.cos(th).mean() ** 2 + np.sin(th).mean() ** 2)

    rng = np.random.default_rng(seed)
    best_m, best_p = 0, 1.0
    for m in m_values:
        z = z_stat(m)
        null = []
        for _ in range(1000):
            th = np.deg2rad(2.0 * m * (rng.uniform(0, 180, n) % 180.0))
            null.append(n * (np.cos(th).mean() ** 2 + np.sin(th).mean() ** 2))
        p = float((1 + sum(x >= z for x in null)) / (len(null) + 1))
        if p < best_p:
            best_m, best_p = m, p
    return PaResult(best_m, best_p)
