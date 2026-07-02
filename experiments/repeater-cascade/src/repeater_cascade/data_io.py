"""Loaders for the committed burst-time tables (see scripts/fetch_data.py for
provenance and hypotheses/repeater_cascade_v1.yaml for the frozen dataset list).

Each loader returns one or more ``BurstSeries``; downstream code never touches
raw files.  ``time_resolution_s`` is the dataset's hard timing floor -- the
preregistered gate keeps only taus >= 30x this value in the phase tests.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

DAY_S = 86400.0


@dataclass
class BurstSeries:
    """Time-ordered burst arrival times of ONE source from ONE instrument."""

    dataset_id: str
    source: str
    mjd: np.ndarray                      # sorted, days
    time_resolution_s: float
    provenance: str
    fluence: np.ndarray = field(default_factory=lambda: np.array([]))

    def __post_init__(self) -> None:
        order = np.argsort(self.mjd)
        self.mjd = np.asarray(self.mjd, dtype=float)[order]
        if self.fluence.size:
            self.fluence = np.asarray(self.fluence, dtype=float)[order]

    def __len__(self) -> int:
        return len(self.mjd)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _floats(rows: list[dict[str, str]], key: str) -> np.ndarray:
    out = np.full(len(rows), np.nan)
    for i, r in enumerate(rows):
        v = (r.get(key) or "").strip()
        if v:
            try:
                out[i] = float(v)
            except ValueError:
                pass
    return out


def load_frb20220912a() -> BurstSeries:
    rows = _read_csv(DATA_DIR / "frb20220912a_zhang2023.csv")
    mjd = _floats(rows, "mjd_bary")
    flu = _floats(rows, "fluence_jyms")
    ok = np.isfinite(mjd)
    return BurstSeries("fast_frb20220912a_zhang2023", "FRB20220912A", mjd[ok], 0.01,
                       "Zhang Y.-K.+2023 ApJ 955,142 (FAST; VizieR J/ApJ/955/142)",
                       fluence=flu[ok])


def load_frb20201124a() -> list[BurstSeries]:
    rows = _read_csv(DATA_DIR / "frb20201124a_fast.csv")
    out = []
    for episode, prov in [
        ("xu2022_spring", "Xu H.+2022 Nature 609,685 (FAST spring-2021; via Blinkverse)"),
        ("zhangyk2022_autumn", "Zhang Y.-K.+2022 RAA 22,124002 (FAST autumn-2021; via Blinkverse)"),
    ]:
        sel = [r for r in rows if r["episode"] == episode]
        mjd = _floats(sel, "mjd")
        flu = _floats(sel, "fluence_jyms")
        ok = np.isfinite(mjd)
        out.append(BurstSeries(f"fast_frb20201124a_{episode}", "FRB20201124A",
                               mjd[ok], 0.01, prov, fluence=flu[ok]))
    return out


def load_frb20240114a() -> BurstSeries:
    rows = _read_csv(DATA_DIR / "frb20240114a_fast.csv")
    mjd = _floats(rows, "mjd_topo")
    ok = np.isfinite(mjd)
    return BurstSeries("fast_frb20240114a_polcat", "FRB20240114A", mjd[ok], 0.001,
                       "FAST FRB20240114A polarization catalog v5 (ApJS 2025)")


def load_chime_cat2(min_bursts: int = 10) -> list[BurstSeries]:
    """One series per CHIME Cat2 repeater with >= min_bursts non-excluded bursts."""
    rows = _read_csv(DATA_DIR / "chime_cat2_repeaters.csv")
    per: dict[str, list[dict[str, str]]] = {}
    for r in rows:
        if r.get("excluded_flag") == "1":
            continue
        per.setdefault(r["repeater_name"], []).append(r)
    out = []
    for name, sel in sorted(per.items()):
        if len(sel) < min_bursts:
            continue
        mjd = _floats(sel, "mjd_400")
        flu = _floats(sel, "fluence_jyms")
        ok = np.isfinite(mjd)
        out.append(BurstSeries(f"chime_cat2_{name.lower()}", name, mjd[ok], 0.001,
                               "CHIME/FRB Catalog 2 (ApJS 283,34; CANFAR doi:10.11570/25.0066)",
                               fluence=flu[ok]))
    return out


def load_all() -> list[BurstSeries]:
    series = [load_frb20220912a(), *load_frb20201124a(), load_frb20240114a()]
    series += load_chime_cat2()
    return series
