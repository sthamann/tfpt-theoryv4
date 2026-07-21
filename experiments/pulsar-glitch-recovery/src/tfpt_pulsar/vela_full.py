"""PG.06b FULL -- the complete NICER Vela reduction (all 665 archive observations).

PG.06b proved the download->barycentre->fold pipeline on ONE observation and stopped at
the honest wall (a comb-quality nu(t) needs more than a per-obs H-test). This module runs
the FULL reduction the manifest (data/nicer_vela/manifest_full_reduction.json, frozen
BEFORE the bulk download) preregisters:

  STAGE 1  fast barycentring (astropy + DE421 + orbit-file cubic spline; validated against
           PINT's get_NICER_TOAs on obsid 0020180102 to 3.4 us RMS, i.e. 4e-5 cycles) +
           per-obs Z^2/H frequency measurement against a piecewise ephemeris predictor
           (PuMA 2021 .par, LVK 2024 .par, JBO 2019 step). Soft band PI 20-120
           (0.2-1.2 keV), chosen on the one PUBLIC proof obs (H 145 vs 100 unfiltered);
           the band only affects SNR, never the comb statistic.

  STAGE 2  segment-coherent nu fits: photons of neighbouring obs (gap <= a cycle-safe
           bound) are combined into one coherent Z^2 fit -> nu to ~1e-8..1e-7 Hz. A
           coherence check (coherent Z^2 vs the incoherent per-obs sum) flags cycle
           slips; flagged segments fall back to the incoherent weighted mean
           (the preregistered "piecewise nu fits" alternative -- documented, since a
           full multi-month phase connection over timing noise is a research project).

  STAGE 3  per glitch window (2019 / 2021 / 2024): delta-nu(tau) relative to the
           pre-glitch local spin fit -> SANITY GATE (published Delta nu/nu must be
           reproduced) -> PG.08-protocol comb observable (refit-absorption basis
           {1, tau, tau^2, exp(-tau/tau_d_i)} projected out) -> frozen detector at
           omega = 2*pi/ln((3/2)^6) + off-kernel periodogram + within-segment shuffle +
           lambda battery (Bonferroni) + end-to-end injection (eps_90 sensitivity).

IMPORTANT correction to the PG.06b scaffold: the old single-obs "detection" at
F0 = 11.19275 Hz (H=18.4 on a 40k subsample) was a NOISE peak -- the true Vela frequency
at MJD 57941.5, predicted by the phase-connected PuMA ephemeris and confirmed on all
430,739 photons, is F0 = 11.1861692 Hz (H = 99.7 unfiltered, 145 in the soft band).
The full reduction supersedes that row.

Firewall: search-target tooling; no claim. Python (numpy/scipy/astropy).
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parents[2] / "data"
NV = DATA / "nicer_vela"
RAW = NV / "raw"
BARY = NV / "bary"
PEROBS_CSV = NV / "vela_nu_perobs_full.csv"
SEGMENTS_CSV = NV / "vela_nu_t_full.csv"

# --- Vela astrometry (PuMA phase-connected par, POSEPOCH 59417.6193) ---------------
RA_DEG = 128.83596949291667          # 08:35:20.6326783
DEC_DEG = -45.17605676111111         # -45:10:33.80434
PMRA_MAS_YR = -49.68                 # mas/yr (alpha* convention)
PMDEC_MAS_YR = 29.9
POSEPOCH_MJD = 59417.6193

MJDREFI, MJDREFF = 56658, 0.000777592592592593   # NICER MET reference (TT)
C_KM_S = 299792.458
PI_LO, PI_HI = 20, 120               # 0.2-1.2 keV soft band (see module docstring)
H_MIN_DETECT = 25.0                  # H-test acceptance (p ~ 4e-5, safe for 665 trials)
MIN_PHOTONS = 300                    # bary-cache floor; short obs still feed segment fits
MIN_TSPAN_S = 64.0

# glitch epochs (JBO catalogue / phase-connected pars)
GLEP_2019 = 58515.5929
GLEP_2021 = 59417.6194
GLEP_2024 = 60429.86975
DNU_NU_PUBLISHED = {"2019": 2.5012e-6, "2021": 1.26e-6, "2024": 2.38e-6}

DE421_URL = "ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp/de421.bsp"


# =============================================================== fast barycentring
def _n_hat(mjd: float) -> np.ndarray:
    """Vela unit vector at epoch `mjd`, proper motion applied."""
    dt_yr = (mjd - POSEPOCH_MJD) / 365.25
    ra = RA_DEG + PMRA_MAS_YR * dt_yr / 3.6e6 / math.cos(math.radians(DEC_DEG))
    dec = DEC_DEG + PMDEC_MAS_YR * dt_yr / 3.6e6
    ra, dec = math.radians(ra), math.radians(dec)
    return np.array([math.cos(dec) * math.cos(ra), math.cos(dec) * math.sin(ra),
                     math.sin(dec)])


def barycenter_obs(obsid: str) -> dict | None:
    """Barycentre one observation's soft-band photons; cache to BARY/ni<obsid>.npz.

    Returns meta dict (obsid, mjd_mid, tspan_s, n_ph) or None if unusable.
    Validated against PINT (get_NICER_TOAs + satellite obs) to 3.4 us RMS.
    """
    from astropy.coordinates import get_body_barycentric, solar_system_ephemeris
    from astropy.io import fits
    from astropy.time import Time
    from astropy.units import km
    from astropy.utils.data import download_file
    from scipy.interpolate import CubicSpline

    out = BARY / f"ni{obsid}.npz"
    if out.exists():
        z = np.load(out)
        tb = z["tb_mjd"]
        return {"obsid": obsid, "mjd_mid": float(tb.mean()),
                "tspan_s": float((tb.max() - tb.min()) * 86400.0), "n_ph": int(len(tb))}

    evt_p, orb_p = RAW / f"ni{obsid}_cl.evt", RAW / f"ni{obsid}.orb"
    if not evt_p.exists() or not orb_p.exists():
        return None
    try:
        with fits.open(evt_p) as f:
            hdr = f["EVENTS"].header
            met = np.asarray(f["EVENTS"].data["TIME"], np.float64)
            pi = np.asarray(f["EVENTS"].data["PI"], np.int32)
        with fits.open(orb_p) as f:
            od = f["ORBIT"].data
            omet = np.asarray(od["TIME"], float)
            oxyz = np.vstack([np.asarray(od[c], float) for c in "XYZ"]).T / 1e3  # m->km
    except Exception:  # noqa: BLE001  (truncated/corrupt file -> skip, logged upstream)
        return None
    met = met + float(hdr.get("TIMEZERO", 0.0))
    band = (pi >= PI_LO) & (pi < PI_HI)
    ok = band & (met >= omet[0]) & (met <= omet[-1])
    met = np.sort(met[ok])
    if len(met) < MIN_PHOTONS or (met[-1] - met[0]) < MIN_TSPAN_S:
        return None

    cs = [CubicSpline(omet, oxyz[:, k]) for k in range(3)]
    r_sc = np.vstack([c(met) for c in cs]).T
    t_tt = Time(MJDREFI, MJDREFF + met / 86400.0, format="mjd", scale="tt")
    dt_tdb = (t_tt.tdb.jd1 - t_tt.jd1 + t_tt.tdb.jd2 - t_tt.jd2) * 86400.0
    gi = np.unique(np.concatenate([np.arange(0, len(met), 1000), [len(met) - 1]]))
    kernel = download_file(DE421_URL, cache=True)
    with solar_system_ephemeris.set(kernel):
        pe = get_body_barycentric("earth", t_tt[gi].tdb)
    re = np.vstack([pe.x.to_value(km), pe.y.to_value(km), pe.z.to_value(km)]).T
    if len(gi) > 3:
        re_i = np.vstack([CubicSpline(met[gi], re[:, k])(met) for k in range(3)]).T
    else:
        re_i = np.repeat(re[:1], len(met), axis=0)
    mjd_mid = MJDREFI + MJDREFF + float(met.mean()) / 86400.0
    roemer = (re_i + r_sc) @ _n_hat(mjd_mid) / C_KM_S
    tb_mjd = MJDREFI + MJDREFF + (met + dt_tdb + roemer) / 86400.0

    BARY.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out, tb_mjd=tb_mjd)
    return {"obsid": obsid, "mjd_mid": float(tb_mjd.mean()),
            "tspan_s": float((tb_mjd.max() - tb_mjd.min()) * 86400.0),
            "n_ph": int(len(tb_mjd))}


def load_bary(obsid: str) -> np.ndarray | None:
    p = BARY / f"ni{obsid}.npz"
    return np.load(p)["tb_mjd"] if p.exists() else None


# =============================================================== spin predictor
def _parse_par_full(path: Path) -> dict:
    vals: dict[str, float] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        tok = line.split()
        if len(tok) < 2:
            continue
        try:
            vals[tok[0].upper()] = float(tok[1].replace("D", "e").replace("d", "e"))
        except ValueError:
            continue
    return vals


@dataclass
class SpinPredictor:
    """Piecewise Vela spin model for scan centring (accuracy needed: ~1e-4 Hz; the
    per-obs scan half-width is 4e-4 Hz). Built from the two committed phase-connected
    pars + the JBO 2019 step for the pre-2019 era."""

    puma: dict
    lvk: dict

    @classmethod
    def load(cls) -> "SpinPredictor":
        return cls(_parse_par_full(DATA / "puma_iar" / "J0835-4510_glitch.par"),
                   _parse_par_full(DATA / "vela_2024" / "J0835-4510_long_F3.par"))

    @staticmethod
    def _eval(vals: dict, t_mjd: float, n_f: int) -> tuple[float, float]:
        dt = (t_mjd - vals["PEPOCH"]) * 86400.0
        f = sum(vals.get(f"F{k}", 0.0) * dt**k / math.factorial(k) for k in range(n_f))
        fd = sum(vals.get(f"F{k}", 0.0) * dt ** (k - 1) / math.factorial(k - 1)
                 for k in range(1, n_f))
        glep = vals.get("GLEP_1")
        if glep is not None and t_mjd > glep:
            tg = (t_mjd - glep) * 86400.0
            f += vals.get("GLF0_1", 0.0) + vals.get("GLF1_1", 0.0) * tg \
                 + 0.5 * vals.get("GLF2_1", 0.0) * tg**2
            fd += vals.get("GLF1_1", 0.0) + vals.get("GLF2_1", 0.0) * tg
            i = 1
            while f"GLF0D_{i}" in vals and f"GLTD_{i}" in vals:
                a, td = vals[f"GLF0D_{i}"], vals[f"GLTD_{i}"] * 86400.0
                f += a * math.exp(-tg / td)
                fd += -a / td * math.exp(-tg / td)
                i += 1
        return f, fd

    def predict(self, t_mjd: float) -> tuple[float, float]:
        """(f0, fdot) at barycentric MJD t."""
        if t_mjd >= 60353.0:                       # LVK 2024 par era
            return self._eval(self.lvk, t_mjd, 4)
        f, fd = self._eval(self.puma, t_mjd, 3)
        if t_mjd < GLEP_2019:                      # remove the 2019 glitch going back
            f -= DNU_NU_PUBLISHED["2019"] * self.puma["F0"]
            fd -= 8.69e-3 * self.puma["F1"]        # JBO dF1/F1 = 8.69e-3
        return f, fd


# =============================================================== Z^2 / H machinery
def z2_h(phase: np.ndarray, mmax: int = 8) -> tuple[float, float]:
    """(H statistic, Z^2_1) of pulse phases in [0,1)."""
    n = len(phase)
    two_pi_k = 2.0 * np.pi * np.arange(1, mmax + 1)[:, None]
    arg = two_pi_k * phase[None, :]
    z2 = 2.0 / n * np.cumsum(np.cos(arg).sum(axis=1) ** 2
                             + np.sin(arg).sum(axis=1) ** 2)
    return float(np.max(z2 - 4.0 * np.arange(mmax))), float(z2[0])


def _z2_1_grid(tsec: np.ndarray, freqs: np.ndarray, fdot: float) -> np.ndarray:
    """Z^2_1 over a frequency grid (vectorised over photons per frequency)."""
    quad = 0.5 * fdot * tsec * tsec
    out = np.empty(len(freqs))
    for i, f in enumerate(freqs):
        ph = 2.0 * np.pi * ((f * tsec + quad) % 1.0)
        out[i] = (np.cos(ph).sum() ** 2 + np.sin(ph).sum() ** 2)
    return 2.0 / len(tsec) * out


@dataclass
class ObsMeasure:
    obsid: str
    mjd_mid: float
    tspan_s: float
    n_ph: int
    f0: float | None
    sigma_f: float | None
    h_stat: float
    z2_1: float
    detected: bool


# NICER's ISS-orbit data gaps (~5570 s) put strong aliases at ~1.8e-4 Hz spacing.
# The scan window half-width MUST stay below half that spacing so the true peak is
# unambiguous; the prediction has to be good to the same level (it is: phase-connected
# pars in-era, and a rescue pass with locally-updated predictions everywhere else).
ALIAS_SPACING_HZ = 1.8e-4
SCAN_HALF_HZ = 8.0e-5


def measure_f0(tb_mjd: np.ndarray, f_pred: float, fdot: float, *,
               half: float = SCAN_HALF_HZ, step: float = 1e-6,
               n_full: int = 250000, seed: int = 0
               ) -> tuple[float, float, float, float]:
    """Single-stage full-photon Z^2_1 scan around the predicted frequency (window
    kept below the orbital-alias spacing), then a fine local refinement.

    Returns (f0, sigma_f, H, Z2_1). sigma_f from the Z^2 curvature (delta Z^2 = 1
    is the 1-sigma contour since Z^2 ~ 2 ln L for a sinusoidal profile).
    """
    t0 = tb_mjd.mean()
    tsec = np.asarray((tb_mjd - t0) * 86400.0, np.float64)
    rng = np.random.default_rng(seed)
    full = tsec if len(tsec) <= n_full else np.sort(rng.choice(tsec, n_full, replace=False))
    grid = np.arange(f_pred - half, f_pred + half, step)
    fc = float(grid[np.argmax(_z2_1_grid(full, grid, fdot))])

    step2 = 2e-7
    grid = np.arange(fc - 3e-6, fc + 3e-6, step2)
    z2 = _z2_1_grid(full, grid, fdot)
    i = int(np.argmax(z2))
    if 0 < i < len(grid) - 1:
        d1 = 0.5 * (z2[i + 1] - z2[i - 1])
        d2 = z2[i + 1] - 2.0 * z2[i] + z2[i - 1]
        off = -d1 / d2 if d2 < 0 else 0.0
        f0 = float(grid[i] + np.clip(off, -1, 1) * step2)
        sigma = float(step2 / math.sqrt(max(-d2, 1e-12)))       # dZ2=1 contour
    else:
        f0, sigma = float(grid[i]), step2
    quad = 0.5 * fdot * full * full
    h, z21 = z2_h((f0 * full + quad) % 1.0)
    return f0, sigma, h, z21


def measure_obs(obsid: str, pred: SpinPredictor, *, seed: int = 0,
                f_pred_override: float | None = None, half: float = SCAN_HALF_HZ,
                h_min: float = H_MIN_DETECT) -> ObsMeasure | None:
    """STAGE-1 per-obs measurement (bary cache -> Z^2 scan)."""
    meta = barycenter_obs(obsid)
    if meta is None:
        return None
    tb = load_bary(obsid)
    f_model, fdot = pred.predict(meta["mjd_mid"])
    f_pred = f_pred_override if f_pred_override is not None else f_model
    f0, sig, h, z21 = measure_f0(tb, f_pred, fdot, half=half, seed=seed)
    det = bool(h >= h_min and abs(f0 - f_pred) < 0.98 * half
               and F_PHYS_LO < f0 < F_PHYS_HI)
    return ObsMeasure(obsid, meta["mjd_mid"], meta["tspan_s"], meta["n_ph"],
                      f0 if det else None, sig if det else None, h, z21, det)


# =============================================================== local spin model
GLITCH_EDGES = (GLEP_2019, GLEP_2021, GLEP_2024)


def _era(mjd: float) -> int:
    return int(np.searchsorted(np.asarray(GLITCH_EDGES), mjd))


# physical bounds: Vela's spin over the whole NICER era (11.187..11.183 Hz);
# any per-obs/segment frequency outside this window is an artefact, never Vela.
F_PHYS_LO, F_PHYS_HI = 11.180, 11.192


class LocalSpinModel:
    """Smooth local frequency model through the DETECTED per-obs f0 values --
    weighted local quadratic (tricube kernel in time; fitted in DAYS and around the
    local mean for conditioning), never fitted across a giant-glitch epoch. Used for
    the rescue-pass scan centring and the Stage-2 fdot."""

    def __init__(self, rows: list[dict], *, half_window_d: float = 45.0):
        det = sorted((r for r in rows if r.get("detected")
                      and r.get("f0") and F_PHYS_LO < r["f0"] < F_PHYS_HI),
                     key=lambda r: r["mjd_mid"])
        self.t = np.array([r["mjd_mid"] for r in det])
        self.f = np.array([r["f0"] for r in det])
        self.w0 = np.array([1.0 / max(r["sigma_f"], 1e-9) ** 2 for r in det])
        self.era = np.array([_era(x) for x in self.t])
        self.h = half_window_d

    def predict(self, mjd: float) -> tuple[float, float] | None:
        """(f0, fdot[Hz/s]) from the local weighted polynomial, or None."""
        m = (self.era == _era(mjd)) & (np.abs(self.t - mjd) < self.h)
        if m.sum() < 4:
            m = (self.era == _era(mjd)) & (np.abs(self.t - mjd) < 3 * self.h)
            if m.sum() < 3:
                return None
        dt_d = self.t[m] - mjd                                   # days: well conditioned
        f_ref = float(np.mean(self.f[m]))
        u = np.abs(dt_d) / max(self.h, 1e-9)
        w = self.w0[m] * np.clip(1 - np.minimum(u, 1.0) ** 3, 1e-3, None) ** 3
        deg = 2 if m.sum() >= 6 else 1
        V = np.vander(dt_d, deg + 1)
        beta, *_ = np.linalg.lstsq(V * np.sqrt(w)[:, None],
                                   (self.f[m] - f_ref) * np.sqrt(w), rcond=None)
        f0 = f_ref + float(beta[-1])
        fdot = float(beta[-2]) / 86400.0 if deg >= 1 else 0.0
        if not (F_PHYS_LO < f0 < F_PHYS_HI):
            return None
        return f0, fdot


# =============================================================== STAGE 2: segments
@dataclass
class SegmentFit:
    mjd_mid: float
    tspan_d: float
    n_obs: int
    n_det: int               # per-obs detections inside the segment
    n_ph: int
    f0: float
    sigma_f: float
    z2_coh: float
    z2_incoh_sum: float
    coherent: bool           # coherence check passed (no cycle-slip suspicion)


def build_segments(rows: list[dict], *, max_gap_d: float = 1.5,
                   max_span_d: float = 6.0) -> list[list[dict]]:
    """Group ALL usable per-obs rows (detected or not -- every photon helps the
    coherent segment fit) into candidate segments; a segment never crosses a
    giant-glitch epoch."""
    rows = sorted((r for r in rows if r.get("mjd_mid")), key=lambda r: r["mjd_mid"])
    segs: list[list[dict]] = []
    cur: list[dict] = []
    for r in rows:
        if cur and (r["mjd_mid"] - cur[-1]["mjd_mid"] > max_gap_d
                    or r["mjd_mid"] - cur[0]["mjd_mid"] > max_span_d
                    or _era(r["mjd_mid"]) != _era(cur[-1]["mjd_mid"])):
            segs.append(cur)
            cur = []
        cur.append(r)
    if cur:
        segs.append(cur)
    return segs


def fit_segment(seg: list[dict], local: "LocalSpinModel", pred: SpinPredictor, *,
                n_max: int = 400000, seed: int = 0) -> SegmentFit | None:
    """Coherent Z^2_1 fit across ALL photons of one segment, prior-centred on the
    detected members (or the local spin model), with a cycle-slip check: the coherent
    Z^2 must reach a sizeable fraction of the incoherent per-obs sum. Falls back to
    the incoherent inverse-variance mean when the check fails (the preregistered
    piecewise-nu alternative)."""
    tbs = [load_bary(r["obsid"]) for r in seg]
    tbs = [t for t in tbs if t is not None]
    if not tbs:
        return None
    tb = np.concatenate(tbs)
    tb.sort()
    t0 = float(tb.mean())
    tsec = (tb - t0) * 86400.0
    span_s = float(tsec.max() - tsec.min())
    if span_s < MIN_TSPAN_S:
        return None
    lp = local.predict(t0)
    fdot = lp[1] if lp is not None else pred.predict(t0)[1]
    if not (-5e-11 < fdot < 1e-11):          # Vela fdot is always ~ -1.56e-11 Hz/s
        fdot = pred.predict(t0)[1]

    det = [r for r in seg if r.get("detected")]
    if det:
        f_at_t0 = np.array([r["f0"] + fdot * (t0 - r["mjd_mid"]) * 86400.0 for r in det])
        w = np.array([1.0 / max(r["sigma_f"], 1e-9) ** 2 for r in det])
        f_inc = float(np.sum(w * f_at_t0) / np.sum(w))
        sig_inc = float(1.0 / math.sqrt(np.sum(w)))
    elif lp is not None:
        f_inc, sig_inc = lp[0], 5e-6
    else:
        return None
    if not (F_PHYS_LO < f_inc < F_PHYS_HI):
        return None
    z2_sum = float(sum(r["z2_1"] for r in det)) if det else 0.0

    rng = np.random.default_rng(seed)
    use = tsec if len(tsec) <= n_max else np.sort(rng.choice(tsec, n_max, replace=False))
    step = max(1.0 / (40.0 * span_s), 2e-9)
    half = min(max(6.0 * sig_inc, 30.0 * step), 3e-5)
    grid = np.arange(f_inc - half, f_inc + half, step)
    if len(grid) > 25000:
        grid = np.linspace(f_inc - half, f_inc + half, 25000)
    z2 = _z2_1_grid(use, grid, fdot)
    i = int(np.argmax(z2))
    scale = len(tsec) / len(use)                     # Z^2 scales ~ n for a real signal
    z2_coh = float(z2[i] * scale)
    n_eff_trials = max(2.0, 2.0 * half * span_s)
    strong = z2_coh > 2.0 * math.log(20.0 * n_eff_trials)     # safely above scan noise
    coherent = bool(strong and (z2_coh > 0.35 * z2_sum or not det)
                    and 0 < i < len(grid) - 1)
    if coherent:
        d1 = 0.5 * (z2[i + 1] - z2[i - 1])
        d2 = z2[i + 1] - 2.0 * z2[i] + z2[i - 1]
        off = -d1 / d2 if d2 < 0 else 0.0
        f0 = float(grid[i] + np.clip(off, -1, 1) * (grid[1] - grid[0]))
        sigma = float((grid[1] - grid[0]) / math.sqrt(max(-d2 * scale, 1e-12)))
    elif det:
        f0, sigma = f_inc, sig_inc                   # documented fallback
    else:
        return None
    return SegmentFit(t0, span_s / 86400.0, len(seg), len(det), int(len(tb)), f0,
                      sigma, z2_coh, z2_sum, coherent)
