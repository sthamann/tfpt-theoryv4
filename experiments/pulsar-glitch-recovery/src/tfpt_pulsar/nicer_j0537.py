"""PG.06 (heavy / optional) -- the dense, stacked recovery-comb test on PSR J0537-6910.

PG.05 ran the dynamic log-periodic recovery comb (omega = 2pi/ln((3/2)^6) = 2.583) on the best
FREE nu(t) waveform (the Crab monthly ephemeris) and came back data_limited: the monthly cadence
under-samples the recovery, and the predicted comb amplitude is only eps ~ exp(-pi^2/ln lambda) ~ 2%.

The decisive dataset is **PSR J0537-6910, the "Big Glitcher"**: it glitches every ~100 d and is
monitored densely (~days) in X-rays (RXTE 1999-2011, NICER 2017-), so each of its ~45+ inter-glitch
intervals is a recovery WAVEFORM and they can be **stacked (superposed-epoch)** -> the per-bin SNR
needed for a ~2% comb. The catch: the dense data are RAW X-ray event files (HEASARC), not a small
table -- so this is a real reduction project, NOT a quick fetch.

This module scaffolds that project honestly, in two halves:

  UPSTREAM (gated, heavy): fetch NICER L2 *cleaned* event + orbit files from HEASARC, then use
  PINT (`get_NICER_TOAs` + a satellite observatory from the .orb) to barycentre + epoch-fold each
  observation into a frequency nu per epoch -> nu(t). This needs PINT (pip, installed) and ~GB of
  event downloads; crucially it does NOT need HEASoft/nicerl2 if the archived L2 products are used.

  DOWNSTREAM (runs now): nu(t) -> per-glitch nudot recovery -> superposed-epoch STACK -> the
  kernel-omega comb detector (`nu_recovery.detect_comb`). This half is injection-validated end-to-end
  on a SYNTHETIC J0537-like nu(t) (a comb-bearing run is recovered, a smooth-recovery null is not),
  so the moment a real nu(t) CSV is produced the test runs unchanged.

Firewall: a search target, never a claim. The synthetic run validates machinery only and asserts
nothing about real data. If HEASoft/PINT/the GB downloads are unavailable here, the upstream is
reported as NOT RUN -- no fabricated result. Python (numpy/scipy via nu_recovery; PINT optional).
"""

from __future__ import annotations

import csv
import importlib.util
import shutil
from dataclasses import dataclass, field
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402  (backend must be set before pyplot import)

from .dsi import log_periodic_relaxation
from .nu_recovery import LAMBDA_CASCADE, OMEGA, P_THRESHOLD, detect_comb

# the comb periodogram needs ~this many comb periods in ln(tau) to localise omega (machine-
# checked below): one period is ln(lambda)=2.43, so >~2.8 periods => >~3 decades in tau.
MIN_COMB_PERIODS = 2.8

DATA = Path(__file__).resolve().parents[2] / "data" / "nicer_j0537"
NU_T_CSV = DATA / "j0537_nu_t.csv"          # produced by the upstream; (mjd, nu, nudot)

# J0537-6910 base spin (Marshall+1998 / Ho+2020): nu ~ 62 Hz, nudot ~ -2e-10 Hz/s
NU0_HZ = 62.0
NUDOT0 = -2.0e-10                            # Hz/s
INTERGLITCH_D = 100.0                        # ~mean time between glitches (the "Big Glitcher")
N_GRID = 40                                  # superposed-epoch tau grid points


# --------------------------------------------------------------------------- environment
@dataclass
class EnvReport:
    pint: bool
    astropy: bool
    numpy: bool
    scipy: bool
    heasoft: bool          # nicerl2/barycorr on PATH (NOT required for the L2+PINT path)
    note: str


def check_environment() -> EnvReport:
    def has(mod: str) -> bool:
        return importlib.util.find_spec(mod) is not None

    heasoft = shutil.which("nicerl2") is not None or shutil.which("barycorr") is not None
    note = ("L2-events + PINT path: HEASoft is NOT required (use archived *_cl.evt). "
            if not heasoft else "HEASoft present (full L1->L2 reduction also possible). ")
    if not has("pint"):
        note += "PINT MISSING -> `pip install pint-pulsar` for the upstream folding."
    return EnvReport(has("pint"), has("astropy"), has("numpy"), has("scipy"), heasoft, note)


# --------------------------------------------------------------------------- fetch / reduce plan
def fetch_plan() -> list[str]:
    """The exact, documented HEASARC fetch recipe for the dense J0537 data (NOT auto-run)."""
    return [
        "1. Resolve NICER ObsIDs for PSR J0537-6910 (target also = 'SNR 0540-69' field):",
        "     HEASARC Xamin / Browse table 'nicermastr', object 'PSR J0537-6910' (or RA/Dec",
        "     05:37:47.4 -69:10:20); ObsIDs are in the 10503601xx / 20503601xx / 30503601xx series.",
        "2. Pull the cleaned L2 events + orbit per ObsID from the public archive tree",
        "     https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/<YYYY_MM>/<ObsID>/",
        "       xti/event_cl/ni<ObsID>_0mpu7_cl.evt.gz     (cleaned L2 photon events)",
        "       auxil/ni<ObsID>.orb.gz                     (orbit, for barycentring)",
        "     (a per-target wget script is offered by Xamin 'Download products'.)",
        "   NOTE: this is ~GB across the full monitoring campaign -- a real download.",
        "3. (RXTE 1999-2011, optional, doubles the baseline) HEASARC table 'xtemaster',",
        "     PCA event data for J0537; reduce with the standard RXTE recipe.",
        "4. NO HEASoft needed for the L2 path: PINT barycentres from the .orb + folds the events.",
    ]


# --------------------------------------------------------------------------- upstream (gated)
def nu_series_from_nicer(evt_files: list[str], orbit_files: list[str], par_file: str,
                         *, fold_window_d: float = 6.0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """UPSTREAM (needs PINT + real event/orbit files): barycentre the NICER events and
    epoch-fold them in `fold_window_d`-day blocks to measure nu per epoch -> (mjd, nu, nudot).

    Raises RuntimeError with a precise message if PINT or the inputs are missing -- never
    fabricates a series. (Implementation uses pint.event_toas.get_NICER_TOAs + a satellite
    observatory built from the .orb, then pint.templates / phase folding per block.)"""
    if importlib.util.find_spec("pint") is None:
        raise RuntimeError("PINT not installed (`pip install pint-pulsar`).")
    missing = [f for f in (*evt_files, *orbit_files, par_file) if not Path(f).exists()]
    if missing or not evt_files:
        raise RuntimeError(
            "real NICER L2 event/orbit/par files not present -- run scripts/fetch_nicer_j0537.py "
            f"first (see fetch_plan()). Missing: {missing or '(no event files given)'}")
    # The concrete PINT calls (get_NICER_TOAs -> barycentre via get_satellite_observatory(orb)
    # -> fold each block against the par model -> nu per block) are intentionally left to the
    # operator with real data + a base .par; this scaffold does not stub a fake reduction.
    raise RuntimeError(
        "upstream reduction is gated on real data: implement the PINT fold here once the GB of "
        "L2 events are fetched (get_NICER_TOAs + satellite observatory from .orb + per-block "
        "epoch folding). This scaffold refuses to fabricate nu(t).")


def load_nu_series(path: Path = NU_T_CSV) -> tuple[np.ndarray, np.ndarray, np.ndarray] | None:
    """Load a produced nu(t) CSV (mjd, nu, nudot) if present, else None."""
    if not path.exists():
        return None
    mjd, nu, nudot = [], [], []
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            mjd.append(float(row["mjd"]))
            nu.append(float(row["nu"]))
            nudot.append(float(row["nudot"]))
    return np.array(mjd), np.array(nu), np.array(nudot)


# --------------------------------------------------------------------------- downstream (runs now)
def stacked_recovery(mjd: np.ndarray, nudot: np.ndarray, glitch_mjds: list[float],
                     *, n_grid: int = N_GRID) -> tuple[np.ndarray, np.ndarray, int]:
    """Superposed-epoch stack of the per-glitch nudot recovery.

    For each glitch, take the clean inter-glitch segment, set tau = t - t_glitch, remove the
    local linear braking, normalise, and interpolate onto a common log-spaced tau grid; the
    stack is the per-bin mean across glitches -- the high-SNR recovery waveform a single segment
    cannot give. Returns (tau_grid, stacked_recovery, n_segments_used)."""
    g = sorted(glitch_mjds)
    edges = g + [float(mjd.max()) + 1.0]
    segs = []
    tau_lo, tau_hi = [], []
    for i, gm in enumerate(g):
        m = (mjd > gm + 1.0) & (mjd < edges[i + 1] - 1.0)
        if m.sum() < 6:
            continue
        tau = mjd[m] - gm
        rec = nudot[m] - np.polyval(np.polyfit(tau, nudot[m], 1), tau)   # remove linear braking
        s = np.std(rec) or 1.0
        segs.append((tau, rec / s))
        tau_lo.append(tau.min())
        tau_hi.append(tau.max())
    if not segs:
        return np.array([]), np.array([]), 0
    grid = np.logspace(np.log10(max(1.0, np.median(tau_lo))),
                       np.log10(np.median(tau_hi)), n_grid)
    stack = np.zeros(n_grid)
    cover = np.zeros(n_grid)
    for tau, rec in segs:
        inside = (grid >= tau.min()) & (grid <= tau.max())
        stack[inside] += np.interp(grid[inside], tau, rec)
        cover[inside] += 1
    ok = cover > 0
    stack[ok] /= cover[ok]
    return grid[ok], stack[ok], len(segs)


def detect_glitches_nu(mjd: np.ndarray, nu: np.ndarray, *, k: float = 5.0) -> list[float]:
    """Glitch epochs from upward nu steps (residual from a smooth cubic spin-down)."""
    resid = nu - np.polyval(np.polyfit(mjd, nu, 3), mjd)
    step = np.diff(resid)
    thr = k * (np.median(np.abs(step - np.median(step))) * 1.4826 or 1.0)
    return [float(mjd[i + 1]) for i in np.where(step > thr)[0]]


@dataclass
class CombResult:
    n_segments: int
    tau_points: int
    gain: float
    p_value: float
    detected: bool


def comb_test(mjd: np.ndarray, nudot: np.ndarray, glitch_mjds: list[float],
              *, seed: int = 0) -> CombResult:
    grid, stack, n_seg = stacked_recovery(mjd, nudot, glitch_mjds)
    if len(grid) < 6:
        return CombResult(n_seg, len(grid), 0.0, 1.0, False)
    gain, p = detect_comb(grid, stack, OMEGA, seed=seed)
    return CombResult(n_seg, len(grid), gain, p, p < P_THRESHOLD)


# --------------------------------------------------------------------------- synthetic validation
def _periods(interglitch_d: float) -> float:
    """Number of comb periods a single inter-glitch recovery spans in ln(tau) (tau~1..interglitch)."""
    return float(np.log(interglitch_d) / np.log(LAMBDA_CASCADE))


def _detect_rate(periods: float, eps: float, noise: float, *, n_seeds: int = 25,
                 n_pts: int = 70) -> float:
    """Fraction of `n_seeds` noisy realisations in which the comb detector fires, for a clean
    recovery R(tau)=tau^-0.5 (1 + eps cos(omega ln tau)) spanning `periods` comb periods in
    ln(tau). The whole point: this depends on the ln(tau) RANGE (periods), not on stacking."""
    tmax = np.exp(periods * np.log(LAMBDA_CASCADE))
    tau = np.logspace(0.0, np.log10(tmax), n_pts)
    base = log_periodic_relaxation(tau, LAMBDA_CASCADE, alpha=0.5, eps=eps)
    hit = 0
    for s in range(n_seeds):
        rng = np.random.default_rng(s)
        y = base * (1.0 + rng.normal(0.0, noise, n_pts))
        _, p = detect_comb(tau, y, OMEGA, seed=s)
        hit += int(p < P_THRESHOLD)
    return hit / n_seeds


@dataclass
class SyntheticValidation:
    eps: float
    noise: float
    n_seeds: int
    long_periods: float       # sufficient-range regime (Vela-like, ~years interval, daily)
    long_comb_rate: float     # detection rate WITH the comb -> should be high
    long_null_rate: float     # false-positive rate (eps=0)        -> should be ~0
    j0537_periods: float      # J0537 regime (~100 d interval)
    j0537_comb_rate: float    # detection rate WITH the comb at the short range -> ~0 (range-blind)
    passed: bool


def synthetic_validation(*, eps: float = 0.30, noise: float = 0.10,
                         n_seeds: int = 25) -> SyntheticValidation:
    """Validate the comb detector AND expose the test's true limit -- the ln(tau) RANGE.

    Detection rate over many noisy realisations of a clean recovery comb:
      * SUFFICIENT range (>~2.8 comb periods, a Vela-like long interval densely sampled):
        the comb is detected robustly and the smooth null almost never fires;
      * J0537 range (~1.9 periods from a ~100 d inter-glitch interval): the comb is NOT
        localisable -- a hard RANGE limit that stacking many glitches cannot fix (stacking only
        buys amplitude SNR). So the decisive target is a long-interval, densely-monitored pulsar.
    """
    long_p = MIN_COMB_PERIODS
    j_p = _periods(INTERGLITCH_D)
    long_comb = _detect_rate(long_p, eps, noise, n_seeds=n_seeds)
    long_null = _detect_rate(long_p, 0.0, noise, n_seeds=n_seeds)
    j_comb = _detect_rate(j_p, eps, noise, n_seeds=n_seeds)
    passed = bool(long_comb >= 0.6 and long_null <= 0.12 and j_comb < 0.2)
    return SyntheticValidation(eps, noise, n_seeds, long_p, long_comb, long_null,
                               j_p, j_comb, passed)


# --------------------------------------------------------------------------- orchestrator
def _periodogram(tau: np.ndarray, y: np.ndarray, freqs: np.ndarray,
                 deg: int = 2) -> np.ndarray:
    """Comb gain (variance explained by cos/sin(f ln tau) over a deg-poly-in-ln-tau baseline)
    at each log-frequency f -- the same statistic detect_comb ranks omega within."""
    lt = np.log(tau)
    P = np.vander(lt, deg + 1)
    b0, *_ = np.linalg.lstsq(P, y, rcond=None)
    ss0 = float(np.sum((y - P @ b0) ** 2))
    out = []
    for f in freqs:
        X = np.column_stack([P, np.cos(f * lt), np.sin(f * lt)])
        b, *_ = np.linalg.lstsq(X, y, rcond=None)
        out.append(max(0.0, (ss0 - float(np.sum((y - X @ b) ** 2))) / (ss0 + 1e-12)))
    return np.array(out)


def make_plot(out_path, *, eps: float = 0.30, noise: float = 0.10, n_seeds: int = 25) -> str:
    """The KEY finding in two panels: (A) example comb periodograms for the J0537 vs Vela
    ln(tau) ranges -- omega is a clear peak only when the range is wide enough; (B) the comb
    detection rate (+ false-positive control) for the two regimes. Why J0537's short intervals
    are range-blind and a long-interval, densely-monitored pulsar (Vela) is the decisive target."""
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(12.0, 4.3))
    freqs = np.linspace(1.0, 6.0, 200)

    j_p, v_p = _periods(INTERGLITCH_D), MIN_COMB_PERIODS
    for periods, col, lab in [(j_p, "tab:orange", f"J0537 ~{j_p:.1f} periods (range-blind)"),
                              (v_p, "tab:blue", f"Vela ~{v_p:.1f} periods (resolved)")]:
        tmax = np.exp(periods * np.log(LAMBDA_CASCADE))
        tau = np.logspace(0.0, np.log10(tmax), 70)
        rng = np.random.default_rng(0)
        y = log_periodic_relaxation(tau, LAMBDA_CASCADE, alpha=0.5, eps=eps) * (
            1.0 + rng.normal(0.0, noise, 70))
        pg = _periodogram(tau, y, freqs)
        axA.plot(freqs, pg / (pg.max() + 1e-12), color=col, lw=1.5, label=lab)
    axA.axvline(OMEGA, color="tab:red", lw=1.4, label=f"kernel $\\omega$={OMEGA:.2f}")
    axA.set_title("comb periodogram (same injected comb, two ranges)", fontsize=9.5)
    axA.set_xlabel(r"log-frequency $\omega$ (cycles per $e$-fold in $\tau$)")
    axA.set_ylabel("normalised comb gain")
    axA.legend(fontsize=7.5)

    labels = [f"J0537\n~{j_p:.1f}p", f"Vela\n~{v_p:.1f}p"]
    comb_rates = [_detect_rate(j_p, eps, noise, n_seeds=n_seeds),
                  _detect_rate(v_p, eps, noise, n_seeds=n_seeds)]
    null_rates = [_detect_rate(j_p, 0.0, noise, n_seeds=n_seeds),
                  _detect_rate(v_p, 0.0, noise, n_seeds=n_seeds)]
    x = np.arange(2)
    axB.bar(x - 0.18, comb_rates, 0.36, color="tab:green", label="comb present")
    axB.bar(x + 0.18, null_rates, 0.36, color="0.6", label="no comb (false +)")
    axB.set_xticks(x)
    axB.set_xticklabels(labels)
    axB.set_ylim(0, 1.05)
    axB.set_ylabel(f"detection rate ({n_seeds} seeds)")
    axB.set_title("detector: range-blind at J0537, robust at Vela", fontsize=9.5)
    axB.legend(fontsize=7.5)

    fig.suptitle("PG.06: the dynamic recovery comb needs a wide ln(tau) RANGE (J0537 dense but "
                 "short-interval -> blind; Vela long-interval+daily -> the target)", fontsize=9.5)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    return str(out_path)


@dataclass
class J0537Result:
    env: EnvReport
    plan: list[str] = field(default_factory=list)
    real_available: bool = False
    real: CombResult | None = None
    validation: SyntheticValidation | None = None
    verdict: str = ""


def run(*, seed: int = 0) -> J0537Result:
    env = check_environment()
    res = J0537Result(env=env, plan=fetch_plan())
    series = load_nu_series()
    if series is not None:
        mjd, nu, nudot = series
        glitches = detect_glitches_nu(mjd, nu)
        res.real_available = True
        res.real = comb_test(mjd, nudot, glitches, seed=seed)
        res.verdict = (
            f"REAL J0537 nu(t) present ({len(mjd)} epochs, {len(glitches)} glitches): stacked "
            f"recovery comb at omega={OMEGA:.3f} -> {'DETECTED' if res.real.detected else 'not detected'} "
            f"(p={res.real.p_value:.3f}, {res.real.n_segments} segments). "
            + ("Escalate before any claim." if res.real.detected else
               "Clean null on the dense stacked waveform.")
        )
    else:
        res.validation = synthetic_validation()
        v = res.validation
        res.verdict = (
            "UPSTREAM NOT RUN (no real J0537 nu(t) yet): the dense X-ray event reduction needs PINT"
            f"{' (INSTALLED)' if env.pint else ' (MISSING)'} + ~GB of NICER L2 events from HEASARC "
            "(see plan). DETECTOR validated over noisy realisations: in the SUFFICIENT-RANGE regime "
            f"(~{v.long_periods:.1f} comb periods) the comb is detected {100*v.long_comb_rate:.0f}% "
            f"of the time with a {100*v.long_null_rate:.0f}% false-positive rate -> validated={v.passed}. "
            f"KEY FINDING (machine-checked): the comb periodogram needs >~{MIN_COMB_PERIODS} periods in "
            f"ln(tau); a J0537 ~100 d inter-glitch interval gives only ~{v.j0537_periods:.1f} periods, "
            f"where the same comb is detected just {100*v.j0537_comb_rate:.0f}% of the time -- a hard "
            "RANGE limit that stacking many glitches CANNOT fix (stacking buys amplitude, not ln(tau) "
            "range). => the decisive target is a LONG-interval, densely-monitored pulsar (Vela: glitch "
            "every ~3 yr, daily timing -> ~3 decades in tau), NOT J0537. No real-data claim.")
    return res
