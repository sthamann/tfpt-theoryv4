"""Loaders for the two real FRB datasets used in this experiment.

Both files are VizieR ``asu-tsv`` exports (see ``data/README.md`` for the exact
query URLs and citations).  The parser is deliberately generic so the same code
reads any VizieR tab-separated table.

Datasets
--------
* ``chime_catalog1.tsv``           -- CHIME/FRB Catalogue 1 (J/ApJS/257/59),
                                      600 bursts, the canonical public FRB sample.
* ``frb20121102_aggarwal2021.tsv`` -- 144 bursts of the repeater FRB 20121102A
                                      (Aggarwal et al. 2021, J/ApJ/922/115),
                                      a single source in a single epoch, so
                                      fluence is directly proportional to energy.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def read_vizier_tsv(path: str | Path) -> tuple[list[str], list[list[str]]]:
    """Parse a VizieR ``asu-tsv`` file into (column names, data rows).

    VizieR layout after the ``#`` comment block is: one header line of column
    names, one line of units, one line of ``---`` separators, then the data.
    """
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    body = [ln for ln in lines if ln and not ln.startswith("#")]
    if len(body) < 3:
        raise ValueError(f"{path}: too few non-comment lines to be a VizieR table")
    columns = [c.strip() for c in body[0].split("\t")]
    rows: list[list[str]] = []
    for ln in body[3:]:  # skip header, units, dashed separator
        if set(ln.replace("\t", "")) <= set("- "):
            continue
        cells = ln.split("\t")
        if len(cells) != len(columns):
            continue
        rows.append([c.strip() for c in cells])
    return columns, rows


def _col(columns: list[str], rows: list[list[str]], name: str) -> np.ndarray:
    """Return one column as a float array (missing/non-numeric -> NaN)."""
    j = columns.index(name)
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


def _scol(columns: list[str], rows: list[list[str]], name: str) -> list[str]:
    j = columns.index(name)
    return [r[j].strip() for r in rows]


@dataclass
class BurstTable:
    """A flat, source-tagged burst table with the fields the analysis needs.

    Any field that the source catalogue does not provide is left as an empty /
    all-NaN array, and the dependent test reports "no data" rather than guessing.
    """

    source: str
    name: list[str]                                  # per-burst source id
    fluence: np.ndarray                              # Jy ms (proxy for energy)
    mjd: np.ndarray                                  # arrival time (days)
    peak_freq: np.ndarray = field(default_factory=lambda: np.array([]))   # MHz
    low_freq: np.ndarray = field(default_factory=lambda: np.array([]))    # MHz
    high_freq: np.ndarray = field(default_factory=lambda: np.array([]))   # MHz
    dm: np.ndarray = field(default_factory=lambda: np.array([]))          # pc/cm^3
    sub_num: np.ndarray = field(default_factory=lambda: np.array([]))     # sub-burst index
    rm: np.ndarray = field(default_factory=lambda: np.array([]))          # rad/m^2
    pa: np.ndarray = field(default_factory=lambda: np.array([]))          # deg
    repeater: list[str] = field(default_factory=list)                     # repeater name or ""

    def __len__(self) -> int:
        return len(self.name)


def load_chime_catalog1(path: str | Path | None = None) -> BurstTable:
    """CHIME/FRB Catalogue 1 (600 bursts).

    Note: CHIME fluences are *lower limits* (unknown position in the beam), and
    most sources are one-off with unknown distance, so the population fluence is
    a coarse energy proxy.  This catalogue's strength is breadth (repeater vs
    non-repeater, DM, sub-burst frequency drift), not absolute energetics.
    """
    path = Path(path) if path else DATA_DIR / "chime_catalog1.tsv"
    cols, rows = read_vizier_tsv(path)
    rp_raw = _scol(cols, rows, "RpName")
    repeater = ["" if x in ("-9999", "") else x for x in rp_raw]
    return BurstTable(
        source="CHIME/FRB Catalogue 1",
        name=_scol(cols, rows, "Name"),
        fluence=_col(cols, rows, "Fluence"),
        mjd=_col(cols, rows, "MJD400"),
        peak_freq=_col(cols, rows, "Fpk"),
        low_freq=_col(cols, rows, "b_Freq"),
        high_freq=_col(cols, rows, "B_Freq"),
        dm=_col(cols, rows, "DMfitb"),
        sub_num=_col(cols, rows, "Nsb"),
        repeater=repeater,
    )


def load_frb121102_aggarwal(path: str | Path | None = None) -> BurstTable:
    """FRB 20121102A burst components (Aggarwal et al. 2021), single epoch.

    All 144 components come from the same source on MJD 57644-57645, so the
    component fluence ``S`` is a clean, distance-independent energy proxy -- the
    ideal input for the per-source energy-cascade (discreteness) test.
    """
    path = Path(path) if path else DATA_DIR / "frb20121102_aggarwal2021.tsv"
    cols, rows = read_vizier_tsv(path)
    n = len(rows)
    return BurstTable(
        source="FRB 20121102A (Aggarwal+2021)",
        name=["FRB20121102A"] * n,
        fluence=_col(cols, rows, "S"),
        mjd=_col(cols, rows, "MJD"),
        peak_freq=_col(cols, rows, "muf"),
        dm=_col(cols, rows, "DM"),
        repeater=["FRB20121102A"] * n,
    )


def _num(s: str) -> float:
    """Parse an IOP-ascii numeric cell: 'cdots'/'' -> nan; strip '+or-' errors
    and trailing parenthetical uncertainties like '-110.28(5)'."""
    s = s.strip()
    if not s or s.lower() == "cdots":
        return np.nan
    s = s.split("+or-")[0]
    s = re.sub(r"\([^)]*\)", "", s).strip()   # drop (uncertainty) notation
    try:
        return float(s)
    except ValueError:
        return np.nan


@dataclass
class DMzTable:
    """Localized FRBs with measured host redshift, for the Macquart/Omega_b test."""

    source: str
    name: list[str]
    z: np.ndarray
    dm_obs: np.ndarray
    dm_mw: np.ndarray              # Milky-Way (disk + halo)
    dm_host_obs: np.ndarray       # observed-frame host DM (NaN if unmodelled)
    dm_cosmic: np.ndarray         # DM_obs - DM_MW - DM_host_obs (the IGM term)

    def __len__(self) -> int:
        return len(self.name)


def load_dmz_table4(path: str | Path | None = None) -> DMzTable:
    """36 localized FRBs with full DM decomposition (ApJ adb84d, Table A1).

    Columns: Name, z_spec, DM_obs, refs, DM_MW(disk;NE2001), DM_MW(halo),
    DM_IGM, DM_host^s (source frame = DM_host*(1+z)), L_Halpha.
    """
    path = Path(path) if path else DATA_DIR / "frb_dmz_adb84d_table4.txt"
    name, z, dmo, dmmw, dmh, dmc = [], [], [], [], [], []
    for ln in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        if not ln.startswith("FRB "):
            continue
        c = ln.split("\t")
        zz, dm_obs = _num(c[1]), _num(c[2])
        dm_mw = _num(c[4]) + _num(c[5])
        dm_host_obs = _num(c[7]) / (1.0 + zz)   # source-frame -> observed-frame
        name.append(c[0].replace("FRB ", "").strip())
        z.append(zz); dmo.append(dm_obs); dmmw.append(dm_mw); dmh.append(dm_host_obs)
        dmc.append(dm_obs - dm_mw - dm_host_obs)
    return DMzTable("Localized FRBs (ApJ adb84d, full DM budget)", name,
                    np.array(z), np.array(dmo), np.array(dmmw), np.array(dmh), np.array(dmc))


def load_dmz_sharma(path: str | Path | None = None, dm_host_rest: float = 60.0) -> DMzTable:
    """117 localized FRBs (Sharma+2024, adeb72 Table 1): z, DM, DM_exc=DM-DM_MW.

    No per-FRB host model, so a constant rest-frame host prior ``dm_host_rest``
    (default 60 pc/cm^3, divided by 1+z) is subtracted to estimate DM_cosmic.
    """
    path = Path(path) if path else DATA_DIR / "frb_dmz_adeb72_table1.txt"
    rx = re.compile(r"^\d{8}[A-Z]")
    name, z, dmo, dmmw, dmh, dmc = [], [], [], [], [], []
    for ln in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        if not rx.match(ln):
            continue
        c = ln.split("\t")
        zz, dm_total, dm_exc = _num(c[1]), _num(c[2]), _num(c[3])
        if not np.isfinite(zz) or not np.isfinite(dm_exc):
            continue
        host_obs = dm_host_rest / (1.0 + zz)
        name.append("FRB" + c[0].strip())
        z.append(zz); dmo.append(dm_total); dmmw.append(dm_total - dm_exc)
        dmh.append(host_obs); dmc.append(dm_exc - host_obs)
    return DMzTable("Localized FRBs (Sharma+2024, DM_exc - host prior)", name,
                    np.array(z), np.array(dmo), np.array(dmmw), np.array(dmh), np.array(dmc))


@dataclass
class PolTable:
    """FRB polarisation properties (Pandhi+2024): extragalactic RM per source."""

    source: str
    name: list[str]
    rm_eg: np.ndarray          # RM_obs - RM_MW (rad/m^2)
    li: np.ndarray             # linear polarisation fraction L/I


def load_pandhi_pol(path: str | Path | None = None) -> PolTable:
    """118 CHIME non-repeating FRBs with RM (Pandhi+2024, Table 1)."""
    path = Path(path) if path else DATA_DIR / "frb_pol_pandhi2024_table1.txt"
    name, rm, li = [], [], []
    for ln in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        if not ln.startswith("FRB "):
            continue
        c = ln.split("\t")
        rm_obs, rm_mw = _num(c[5]), _num(c[7])   # RM_obs,FDF and RM_MW
        name.append(c[0].split("^")[0].replace("FRB ", "").strip())
        rm.append(rm_obs - rm_mw)
        li.append(_num(c[2]))
    return PolTable("CHIME non-repeaters (Pandhi+2024)", name, np.array(rm), np.array(li))


@dataclass
class RepeaterSeries:
    """A single-repeater, time-ordered burst series for the recovery-kernel tests.

    Any field a dataset does not provide is an all-NaN array; ``available`` is
    False when the backing file is absent (the dependent test then reports
    "data-limited" instead of guessing).
    """

    source: str
    available: bool
    mjd: np.ndarray
    energy: np.ndarray = field(default_factory=lambda: np.array([]))         # erg
    fluence: np.ndarray = field(default_factory=lambda: np.array([]))        # Jy ms
    dm: np.ndarray = field(default_factory=lambda: np.array([]))
    rm: np.ndarray = field(default_factory=lambda: np.array([]))             # rad/m^2
    rm_err: np.ndarray = field(default_factory=lambda: np.array([]))
    pa_deg: np.ndarray = field(default_factory=lambda: np.array([]))
    pa_err: np.ndarray = field(default_factory=lambda: np.array([]))
    linear_frac: np.ndarray = field(default_factory=lambda: np.array([]))
    circular_frac: np.ndarray = field(default_factory=lambda: np.array([]))
    freq_low: np.ndarray = field(default_factory=lambda: np.array([]))
    freq_high: np.ndarray = field(default_factory=lambda: np.array([]))
    session_id: np.ndarray = field(default_factory=lambda: np.array([]))

    def __len__(self) -> int:
        return len(self.mjd)


def _daily_sessions(mjd: np.ndarray) -> np.ndarray:
    """Session label = integer MJD (one observing night) when none is provided."""
    return np.floor(np.asarray(mjd, dtype=float)).astype(float)


def load_fast_121102_1652(path: str | Path | None = None) -> RepeaterSeries:
    """1652 bursts of FRB 20121102A from FAST (Li et al. 2021, Nature 598, 267).

    VizieR ``J/other/Nat/598.267/tables1``. Columns: Burst, MJD, DM, Width,
    Bandwidth, Fp, Fluence, **E (energy, erg)**. Same source ⇒ E is a clean,
    distance-independent energy — the proper input for the FRB.02 echo test and
    the energy cascade. Sessions are taken as integer-MJD nights.
    """
    path = Path(path) if path else DATA_DIR / "frb20121102_fast_li2021_1652.tsv"
    cols, rows = read_vizier_tsv(path)
    mjd = _col(cols, rows, "MJD")
    return RepeaterSeries(
        source="FRB 20121102A (FAST, Li+2021, 1652 bursts)",
        available=True,
        mjd=mjd,
        energy=_col(cols, rows, "E"),
        fluence=_col(cols, rows, "Fluence"),
        dm=_col(cols, rows, "DM"),
        session_id=_daily_sessions(mjd),
    )


# --- generic delimited-table reader for the drop-in repeater catalogues ----
_COL_ALIASES = {
    "mjd": ["mjd", "mjd_topo", "mjdtopo", "toa", "mjd_bary", "mjd_inf", "time"],
    "energy": ["energy", "e", "e_iso", "energy_erg"],
    "fluence": ["fluence", "fluence_jyms", "s", "fluence_jy_ms"],
    "dm": ["dm", "dm_obs", "dmeff", "dm_eff"],
    "rm": ["rm", "rm_obs", "rm_radm2"],
    "rm_err": ["rm_err", "e_rm", "rm_error"],
    "pa_deg": ["pa", "pa_deg", "pa0", "pa_0", "pa_intrinsic", "pa_mean(deg)",
               "pa_mean", "pa(deg)"],
    "pa_err": ["pa_err", "e_pa", "pa_error", "pa_mean_err(deg)"],
    "linear_frac": ["linear_fraction", "l/i", "li", "dol", "lfrac"],
    "circular_frac": ["circular_fraction", "v/i", "vi", "doc", "vfrac"],
    "freq_low": ["freq_low", "frequency_low", "f_low", "flow"],
    "freq_high": ["freq_high", "frequency_high", "f_high", "fhigh"],
    "session_id": ["session_id", "session", "epoch", "mjd_session"],
}


def _read_delimited(path: Path) -> tuple[list[str], list[list[str]]]:
    text = path.read_text(encoding="utf-8", errors="replace").splitlines()
    rows = [ln for ln in text if ln.strip() and not ln.lstrip().startswith("#")]
    delim = "\t" if rows and rows[0].count("\t") >= rows[0].count(",") else ","
    header = [c.strip().lower() for c in rows[0].split(delim)]
    data = [r.split(delim) for r in rows[1:] if len(r.split(delim)) == len(header)]
    return header, data


def _load_dropin_repeater(source: str, filename: str,
                          path: str | Path | None) -> RepeaterSeries:
    """Load a drop-in repeater CSV/TSV by column aliases; data-limited if absent."""
    p = Path(path) if path else DATA_DIR / filename
    if not p.exists():
        return RepeaterSeries(source, available=False, mjd=np.array([]))
    header, rows = _read_delimited(p)

    def grab(field_key: str) -> np.ndarray:
        for alias in _COL_ALIASES[field_key]:
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

    mjd = grab("mjd")
    sess = grab("session_id")
    if sess.size == 0 and mjd.size:
        sess = _daily_sessions(mjd)
    return RepeaterSeries(
        source=source, available=True, mjd=mjd, energy=grab("energy"),
        fluence=grab("fluence"), dm=grab("dm"), rm=grab("rm"), rm_err=grab("rm_err"),
        pa_deg=grab("pa_deg"), pa_err=grab("pa_err"), linear_frac=grab("linear_frac"),
        circular_frac=grab("circular_frac"), freq_low=grab("freq_low"),
        freq_high=grab("freq_high"), session_id=sess,
    )


_FRB20240114A_FILES = (
    "FAST_FRB20240114A_pol_catalog_v5.csv",   # cleanest: clean header + full-precision MJD
    "FAST_FRB20240114A_pol_catalog.csv",
    "FAST_FRB20240114A_pol_catalog_v4.csv",
    "frb20240114A_fast_pol_catalog.tsv",
)


def load_fast_20240114A_pol(path: str | Path | None = None) -> RepeaterSeries:
    """FAST polarisation catalogue of FRB 20240114A (6131 bursts; ScienceDB
    DOI 10.57760/sciencedb.Fastro.00040, arXiv:2603.20663).

    Columns: BurstID, MJD_topo, RM, DM, Weff, Bandwidth, S/N, DOL (=L/I),
    DOC (=V/I), PA_mean(deg). Activates FRB.04 (RM/PA Markov spectrum) and
    rm_staircase. Tries the released CSV filenames first, then the generic
    drop-in name.
    """
    if path is None:
        for cand in _FRB20240114A_FILES:
            if (DATA_DIR / cand).exists():
                path = DATA_DIR / cand
                break
    return _load_dropin_repeater("FRB 20240114A (FAST pol; n_raw=6134 catalogue rows)",
                                 "frb20240114A_fast_pol_catalog.tsv", path)


def load_frb20240619D(path: str | Path | None = None) -> RepeaterSeries:
    """Wideband catalogue of FRB 20240619D (1539 bursts; MeerKAT/Murriyang/Lovell).

    Drop-in: place the burst table at ``data/frb20240619D_wideband.tsv`` with
    columns including MJD, fluence, DM, RM, frequency band. Activates the RM
    memory / session-decay / frequency-window stress tests.
    """
    return _load_dropin_repeater("FRB 20240619D (wideband, 1539 bursts)",
                                 "frb20240619D_wideband.tsv", path)


def repeater_subsets(tbl: BurstTable, min_bursts: int = 8) -> dict[str, np.ndarray]:
    """Indices of each repeater source with at least ``min_bursts`` entries."""
    out: dict[str, list[int]] = {}
    for i, rp in enumerate(tbl.repeater):
        if rp:
            out.setdefault(rp, []).append(i)
    return {k: np.array(v) for k, v in out.items() if len(v) >= min_bursts}
