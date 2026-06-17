"""Loader/parser for the Jodrell Bank Glitch Catalogue.

The catalogue (``https://www.jb.man.ac.uk/pulsar/glitches/gTable.html``, Basu et
al. 2022, MNRAS 510, 4049) is a single HTML ``<table>`` whose header row is

    ['', 'Pulsar name', 'J-name', 'No.', 'MJD', '+/-', 'dF/F', '+/-',
     'dF1/F1', '+/-', 'References']

so each data row carries, per glitch:

* ``Pulsar name`` (B-name or J-name), ``J-name``
* ``No.``   -- the running glitch index *for that pulsar* (so multi-glitch
  pulsars and per-pulsar size ladders are reconstructable)
* ``MJD``   -- glitch epoch (waiting-time analysis)
* ``dF/F``  -- fractional spin-up ``Delta nu / nu`` in units of ``1e-9``
* ``dF1/F1`` -- fractional spin-down-rate change ``Delta nudot / nudot`` (``1e-3``)

The parser is deliberately tolerant: cells that are ``X`` / blank / non-numeric
(upper limits, missing errors) become ``None`` and never crash the load.  Only
this module talks to the raw HTML; everything downstream reads the small derived
``data/jbo_glitches.csv`` so the tests run without the 1.8 MB download.
"""

from __future__ import annotations

import csv
import re
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parents[2] / "data"
DERIVED_CSV = DATA / "jbo_glitches.csv"
RECOVERY_CSV = DATA / "yu2013_recovery.csv"

_CELL = re.compile(r"<t[dh][^>]*>(.*?)</t[dh]>", re.S | re.I)
_ROW = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S | re.I)
_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")


@dataclass(frozen=True)
class GlitchRecord:
    pulsar: str          # B-name (or J-name if no B-name); the catalogue "Pulsar name"
    jname: str
    glitch_no: int       # running per-pulsar index (1, 2, ...)
    mjd: float | None    # glitch epoch
    df_f: float | None   # Delta nu / nu in units of 1e-9 (the glitch "size")
    df_f_err: float | None
    df1_f1: float | None  # Delta nudot / nudot in units of 1e-3
    df1_f1_err: float | None
    reference: str


def _txt(cell: str) -> str:
    return _WS.sub(" ", _TAG.sub(" ", cell)).replace("&nbsp;", " ").strip()


def _num(cell: str) -> float | None:
    """Parse a numeric cell; ``X``/blank/non-numeric (upper limits) -> None."""
    s = _txt(cell)
    if not s or s.upper() == "X":
        return None
    s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        m = re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", s)
        return float(m.group()) if m else None


def parse_jbo_html(html: str) -> list[GlitchRecord]:
    """Parse the raw gTable.html into typed glitch records."""
    records: list[GlitchRecord] = []
    for row in _ROW.findall(html):
        cells = _CELL.findall(row)
        if len(cells) < 11:
            continue
        pulsar = _txt(cells[1])
        jname = _txt(cells[2])
        # the data rows have a J-name like '0534+2200'; skip header / banner rows
        if not re.match(r"^[BJ]?\d{4}[-+]\d", jname):
            continue
        no = _num(cells[3])
        records.append(
            GlitchRecord(
                pulsar=pulsar or jname,
                jname=jname,
                glitch_no=int(no) if no is not None else 0,
                mjd=_num(cells[4]),
                df_f=_num(cells[6]),
                df_f_err=_num(cells[7]),
                df1_f1=_num(cells[8]),
                df1_f1_err=_num(cells[9]),
                reference=_txt(cells[10]),
            )
        )
    return records


_HEADER = ["pulsar", "jname", "glitch_no", "mjd", "df_f", "df_f_err",
           "df1_f1", "df1_f1_err", "reference"]


def write_csv(records: list[GlitchRecord], path: Path = DERIVED_CSV) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=_HEADER)
        w.writeheader()
        for r in records:
            w.writerow(asdict(r))


def load_catalog(path: Path = DERIVED_CSV) -> list[GlitchRecord]:
    """Load the committed derived catalogue (no network)."""
    if not path.exists():
        raise FileNotFoundError(
            f"{path} missing -- run `python scripts/fetch_glitches.py` first "
            "(downloads + parses the Jodrell Bank gTable.html)."
        )
    out: list[GlitchRecord] = []
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            def f(key: str) -> float | None:
                v = row[key]
                return float(v) if v not in ("", "None") else None
            out.append(
                GlitchRecord(
                    pulsar=row["pulsar"], jname=row["jname"],
                    glitch_no=int(row["glitch_no"]),
                    mjd=f("mjd"), df_f=f("df_f"), df_f_err=f("df_f_err"),
                    df1_f1=f("df1_f1"), df1_f1_err=f("df1_f1_err"),
                    reference=row["reference"],
                )
            )
    return out


def glitch_sizes(records: list[GlitchRecord]) -> np.ndarray:
    """All finite, positive ``Delta nu / nu`` values (units 1e-9)."""
    s = np.array([r.df_f for r in records if r.df_f is not None], dtype=float)
    return s[np.isfinite(s) & (s > 0)]


def by_pulsar(records: list[GlitchRecord]) -> dict[str, list[GlitchRecord]]:
    """Group records by pulsar, each list time-ordered by glitch index/MJD."""
    groups: dict[str, list[GlitchRecord]] = {}
    for r in records:
        groups.setdefault(r.jname, []).append(r)
    for k in groups:
        groups[k] = sorted(
            groups[k],
            key=lambda r: (r.glitch_no, r.mjd if r.mjd is not None else 0.0),
        )
    return groups


# --------------------------------------------------------------------------- recovery (PG.04)
@dataclass(frozen=True)
class RecoveryRecord:
    """One exponential decay component of a post-glitch recovery (Yu+2013, Table 2,
    "previously reported parameters for the exponential recoveries")."""

    psr_j: str
    epoch_mjd: float | None
    dnu_g: float | None        # Delta nu_g / nu (1e-9)
    Q: float | None            # healing/recovery fraction of this component
    Q_err: float | None
    tau_d: float | None        # decay timescale (days)
    tau_d_err: float | None
    comp_index: int            # 0,1,2 = which decay component within the glitch
    reference: str             # \citet key from Yu+2013


_CITE = re.compile(r"\\citet\{([^}]+)\}")


def _clean_psr(s: str) -> str:
    return s.replace("$+$", "+").replace("$-$", "-").replace("$", "").strip()


def _parse_texval(s: str) -> tuple[float | None, float | None]:
    """Parse a LaTeX table value: ``0.001980(18)``, ``10(1)``, ``100``,
    ``0.8$^{+0.3}_{-0.2}$``, ``8.7(2.5)`` -> (central, rough error)."""
    s = s.strip().replace("\\", "")
    if not s:
        return None, None
    m = re.match(r"([-+]?\d*\.?\d+)\s*\$?\^\{?\+?([\d.]+)\}?_\{?-?([\d.]+)\}?\$?", s)
    if m:
        return float(m.group(1)), max(float(m.group(2)), float(m.group(3)))
    m = re.match(r"([-+]?\d*\.?\d+)\((\d+(?:\.\d+)?)\)", s)
    if m:
        val, errs = m.group(1), m.group(2)
        if "." in errs:
            err = float(errs)
        elif "." in val:
            err = float(errs) * 10 ** (-len(val.split(".")[1]))
        else:
            err = float(errs)
        return float(val), err
    m = re.match(r"([-+]?\d*\.?\d+)", s)
    return (float(m.group(1)), None) if m else (None, None)


def parse_yu2013_recovery(tex: str) -> list[RecoveryRecord]:
    """Parse Yu+2013 ``expTab.tex`` (10 columns: PSR J, Name, Age, B_s, Gl.Epoch,
    dnu_g/nu, dnudot_g/nudot, Q, tau_d, References).  Multi-component glitches occupy
    consecutive lines with empty leading cells; PSR/epoch are carried forward."""
    out: list[RecoveryRecord] = []
    psr: str | None = None
    epoch: float | None = None
    comp: dict[tuple[str | None, float | None], int] = {}
    for line in tex.splitlines():
        if "&" not in line or "PSR J" in line or "multicolumn" in line:
            continue
        cells = [c.strip() for c in line.split("&")]
        if len(cells) < 10:
            continue
        if cells[0]:
            psr = _clean_psr(cells[0])
        if cells[4].strip():
            epoch = _parse_texval(cells[4])[0]
        dnu = _parse_texval(cells[5])[0]
        q, q_err = _parse_texval(cells[7])
        tau, tau_err = _parse_texval(cells[8])
        ref_m = _CITE.search(cells[9])
        if q is None and tau is None:
            continue
        key = (psr, epoch)
        comp[key] = comp.get(key, -1) + 1
        out.append(RecoveryRecord(psr or "", epoch, dnu, q, q_err, tau, tau_err,
                                  comp[key], ref_m.group(1) if ref_m else ""))
    return out


_REC_HEADER = ["psr_j", "epoch_mjd", "dnu_g", "Q", "Q_err",
               "tau_d", "tau_d_err", "comp_index", "reference"]


def write_recovery_csv(records: list[RecoveryRecord], path: Path = RECOVERY_CSV) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=_REC_HEADER)
        w.writeheader()
        for r in records:
            w.writerow(asdict(r))


def load_recovery(path: Path = RECOVERY_CSV) -> list[RecoveryRecord]:
    """Load the committed derived Yu+2013 recovery table (no network)."""
    if not path.exists():
        raise FileNotFoundError(
            f"{path} missing -- run `python scripts/fetch_recovery.py` first "
            "(downloads the Yu+2013 arXiv e-print, parses expTab.tex)."
        )
    out: list[RecoveryRecord] = []
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            def f(key: str) -> float | None:
                v = row[key]
                return float(v) if v not in ("", "None") else None
            out.append(RecoveryRecord(
                psr_j=row["psr_j"], epoch_mjd=f("epoch_mjd"), dnu_g=f("dnu_g"),
                Q=f("Q"), Q_err=f("Q_err"), tau_d=f("tau_d"), tau_d_err=f("tau_d_err"),
                comp_index=int(row["comp_index"]), reference=row["reference"]))
    return out


def recovery_by_glitch(records: list[RecoveryRecord]) -> dict[tuple[str, float], list[RecoveryRecord]]:
    """Group recovery components by (pulsar, epoch), ordered by decay timescale."""
    groups: dict[tuple[str, float], list[RecoveryRecord]] = {}
    for r in records:
        if r.epoch_mjd is None:
            continue
        groups.setdefault((r.psr_j, r.epoch_mjd), []).append(r)
    for k in groups:
        groups[k] = sorted(groups[k], key=lambda r: (r.tau_d if r.tau_d else 0.0))
    return groups
