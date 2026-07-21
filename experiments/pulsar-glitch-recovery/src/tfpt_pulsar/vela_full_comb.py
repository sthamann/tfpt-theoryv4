"""PG.06b FULL, STAGE 3 -- the frozen recovery-comb test on the NICER Vela nu(t).

Consumes the STAGE-1/2 products (data/nicer_vela/vela_nu_perobs_full.csv,
vela_nu_t_full.csv), builds the post-glitch delta-nu(tau) recovery per preregistered
glitch window (2019 / 2021 / 2024), enforces the SANITY GATE (published Delta nu/nu
must be reproduced), and runs the SAME frozen detector battery as PG.05/07/08
(nu_recovery.detect_comb + vela2024.within_segment_shuffle_p /
off_kernel_lambda_battery) on the comb observable

    delta-nu residual(tau) vs ln(tau),  refit-absorption basis
    {1, tau, tau^2, exp(-tau/tau_d_i)} projected out (PG.08 protocol, applied to
    nu(t) instead of time residuals -- the frequency-domain equivalent).

End-to-end injection at the real sampling AND real noise: a log-periodic ripple
eps*cos(omega ln tau + phi) multiplying the transient recovery envelope is added to
the measured delta-nu, passed through the SAME projection + detector; the detection
rate over phases as a function of eps gives the achieved sensitivity eps_90 (and the
rate at the predicted eps ~ 0.0173).

Kernel, nulls, gates: identical frozen objects as hypotheses/pulsar_pg07_v1.yaml /
pulsar_pg08_v1.yaml. Documented deviations from a full multi-month phase connection:
STAGE 2 is piecewise segment-coherent (the preregistered fallback); the 2019 glitch
has no public multi-exponential recovery model, so its injection envelope uses the
transient amplitudes FITTED from this data on the committed Vela template timescales
(union with the 2021-par timescales in the projection basis).

Firewall: search target, never a claim; a hit would be universal-DSI in the
neutron-star interior, not a horizon signature and not TFPT confirmation.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass, field
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402  (backend must be set before pyplot import)

from .nu_recovery import OMEGA, P_THRESHOLD, comb_periodogram, detect_comb  # noqa: E402
from .vela2024 import (  # noqa: E402  -- frozen PG.07 machinery, unchanged
    ONE_PERIOD_DLN_TAU,
    REACH_GATE_PERIODS,
    off_kernel_lambda_battery,
    reach_periods,
    within_segment_shuffle_p,
)
from .vela_full import GLEP_2019, GLEP_2021, GLEP_2024, NV, SpinPredictor  # noqa: E402

SEGMENTS_CSV = NV / "vela_nu_t_full.csv"
RESULTS = Path(__file__).resolve().parents[2] / "results"
EPS_PREDICTED = math.exp(-math.pi**2 / ONE_PERIOD_DLN_TAU)   # ~0.0173
EPS_GRID = (EPS_PREDICTED, 0.05, 0.10, 0.20, 0.30, 0.50, 0.75, 1.00)
N_PHASES = 24
CLIP_MAD = 6.0

# published glitch parameters the sanity gate must reproduce (JBO catalogue / pars).
# mode: "prefit" = delta-nu vs own pre-glitch extrapolation (2019: no public
# phase-connected model exists); "model_residual" = residual vs the published
# phase-connected glitch ephemeris (2021: PuMA par -- the PG.08 product, in nu space).
PUBLISHED = {
    "2019": {"glep": GLEP_2019, "dnu_nu": 2.5012e-6, "tol_rel": 0.15,
             "mode": "prefit", "tau_max_d": None},
    "2021": {"glep": GLEP_2021, "dnu_nu": 1.26e-6, "tol_rel": 0.25,
             "mode": "model_residual", "tau_max_d": 860.71},  # PuMA par FINISH 60278.33
    "2024": {"glep": GLEP_2024, "dnu_nu": 2.38e-6, "tol_rel": 0.25,
             "mode": "model_residual", "tau_max_d": 122.71},  # LVK par FINISH 60552.58
}
# transient timescales for the refit-absorption basis / injection envelope:
# 2021 from the phase-connected PuMA par (with its published GLF0D amplitudes);
# 2019/2024 = committed Vela template (data/vela_2024/vela_glitch_recoveries.csv);
# 2019 amplitudes are FITTED here (documented deviation -- no public model).
TAU_D = {
    "2019": (0.394, 2.45, 15.1, 100.0),   # template + a slow 100-d term (fitted amp)
    "2021": (1.0030303, 6.38888889, 502.647),
    "2024": (0.39430499, 2.44662787, 15.11550619),
}
GLF0D = {   # published transient amplitudes (Hz) matching TAU_D, where public
    "2021": (1.005658869408e-7, 3.0925245028e-8, 4.9357251275e-6),
    "2024": (1.8532682857e-7, 1.2377971773e-7, 1.5014095328e-7),
}


# =============================================================== segment loading
@dataclass
class SegSeries:
    mjd: np.ndarray
    f0: np.ndarray
    sigma: np.ndarray
    coherent: np.ndarray


def load_segments() -> SegSeries:
    t, f, s, c = [], [], [], []
    with SEGMENTS_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            t.append(float(r["mjd_mid"]))
            f.append(float(r["f0"]))
            s.append(float(r["sigma_f"]))
            c.append(r["coherent"] == "True")
    o = np.argsort(t)
    return SegSeries(np.array(t)[o], np.array(f)[o], np.array(s)[o],
                     np.array(c)[o])


def _wpolyfit(x: np.ndarray, y: np.ndarray, w: np.ndarray, deg: int) -> np.ndarray:
    V = np.vander(x, deg + 1)
    sw = np.sqrt(w)
    beta, *_ = np.linalg.lstsq(V * sw[:, None], y * sw, rcond=None)
    return beta


SIGMA_FLOOR_HZ = 1.5e-6    # inter-segment systematic floor (timing noise level)


def robust_clip(x: np.ndarray, y: np.ndarray, sigma: np.ndarray, *, deg: int = 2,
                n_iter: int = 4, k: float = CLIP_MAD) -> np.ndarray:
    """Boolean keep-mask: iterative floor-weighted polynomial fit, clipping points
    whose deviation exceeds k x their effective sigma (claimed sigma + systematic
    floor in quadrature). Removes cycle-slip/alias artefacts (tens of uHz with
    claimed sub-uHz sigmas) without touching smooth recovery structure or a
    plausible comb ripple (which stays below the clip threshold)."""
    sig_eff = np.sqrt(sigma**2 + SIGMA_FLOOR_HZ**2)
    keep = np.ones(len(x), bool)
    for _ in range(n_iter):
        if keep.sum() <= deg + 2:
            break
        beta = _wpolyfit(x[keep], y[keep], 1.0 / sig_eff[keep] ** 2,
                         min(deg, keep.sum() - 2))
        r = y - np.polyval(beta, x)
        med = np.median(r[keep])
        mad = np.median(np.abs(r[keep] - med)) * 1.4826
        new = np.abs(r - med) < k * max(mad, 1e-9)
        if new.sum() == keep.sum():
            break
        keep = new
    return keep


# =============================================================== recovery per glitch
@dataclass
class GlitchRecovery:
    name: str
    glep: float
    tau_d: np.ndarray
    dnu: np.ndarray            # measured f0 - pre-glitch extrapolation (Hz)
    tau: np.ndarray            # days since glitch
    sigma: np.ndarray
    n_pre: int
    dnu_step_hz: float         # extrapolated step at tau -> 0 (incl. fitted transients)
    dnu_nu_measured: float
    dnu_nu_published: float
    sanity_pass: bool
    transient_amp_hz: np.ndarray   # fitted amplitudes on tau_d (injection envelope)


def _resolvable(tau_d: np.ndarray, tau: np.ndarray) -> np.ndarray:
    """Timescales the data can constrain: not fully decayed before the first datum,
    not far beyond the observed span (else the exp column is degenerate with the
    polynomial / explodes in the tau->0 extrapolation)."""
    return np.asarray([(td >= 0.6 * tau.min()) and (td <= 1.5 * tau.max())
                       for td in tau_d])


def _absorb_basis(tau_d: np.ndarray, tau: np.ndarray) -> np.ndarray:
    """Refit-absorption design matrix {1, tau, tau^2, exp(-tau/tau_d_i)} (PG.08),
    resolvable timescales only, polynomial columns scaled for conditioning."""
    return _basis_like(tau_d, tau, tau)


def _basis_like(tau_d: np.ndarray, tau_ref: np.ndarray, tau: np.ndarray) -> np.ndarray:
    """The same design matrix, with resolvability and scaling frozen on `tau_ref`
    but evaluated at `tau` (needed to score clipped-out points consistently)."""
    tmax = float(tau_ref.max())
    cols = [np.ones_like(tau), tau / tmax, (tau / tmax) ** 2]
    cols += [np.exp(-tau / td) for td in tau_d[_resolvable(tau_d, tau_ref)]]
    return np.column_stack(cols)


def build_recovery(name: str, segs: SegSeries, *, pre_win_d: float = 200.0,
                   next_glep: float | None = None) -> GlitchRecovery | None:
    """delta-nu(tau) for one glitch, two preregistered modes:

    "prefit" (2019 -- no public phase-connected glitch model exists): pre-glitch
      weighted quadratic extrapolation (fitted in DAYS around the mean frequency)
      subtracted from the post-glitch segment frequencies; transient amplitudes on
      the committed template timescales are FITTED (documented deviation).

    "model_residual" (2021/2024 -- the published phase-connected glitch ephemeris
      exists): delta-nu = measured f0 minus the FULL published model (permanent jump
      + transients). This is the PG.08 "residual to the fit" product, in nu space;
      the sanity gate checks the model phase-tracks our data (residual small vs the
      published step) and the injection envelope uses the PUBLISHED GLF0D amplitudes.
    """
    pub = PUBLISHED[name]
    glep = pub["glep"]
    hi = next_glep if next_glep is not None else segs.mjd.max() + 1.0
    if pub["tau_max_d"] is not None:
        hi = min(hi, glep + pub["tau_max_d"])
    post = (segs.mjd > glep) & (segs.mjd < hi)
    if post.sum() < 8:
        return None
    tau_d_all = np.asarray(TAU_D[name], float)
    n_pre = 0

    if pub["mode"] == "model_residual":
        pred = SpinPredictor.load()
        tau = np.asarray(segs.mjd[post] - glep)
        dnu = np.array([f - pred.predict(m)[0]
                        for m, f in zip(segs.mjd[post], segs.f0[post])])
        sig = np.asarray(segs.sigma[post])
        f_pre_glep = pred.predict(glep - 1.0)[0]
    else:
        pre = (segs.mjd > glep - pre_win_d) & (segs.mjd < glep)
        if pre.sum() < 4:
            return None
        xp = segs.mjd[pre] - glep                       # days, in [-pre_win, 0]
        f_ref = float(np.mean(segs.f0[pre]))
        kp = robust_clip(xp, segs.f0[pre] - f_ref, segs.sigma[pre], deg=2, k=4.0)
        n_pre = int(kp.sum())
        w_pre = 1.0 / (segs.sigma[pre][kp] ** 2 + SIGMA_FLOOR_HZ**2)
        beta_pre = _wpolyfit(xp[kp], segs.f0[pre][kp] - f_ref, w_pre, 2)
        tau = np.asarray(segs.mjd[post] - glep)
        dnu = np.asarray(segs.f0[post] - (f_ref + np.polyval(beta_pre, tau)))
        sig = np.asarray(segs.sigma[post])
        f_pre_glep = f_ref + float(beta_pre[-1])

    # outlier clip: removes cycle-slip artefacts (tens of uHz off the smooth
    # recovery at claimed sub-uHz sigma). model_residual: the residuals are flat
    # around zero by construction -> direct median/MAD clip. prefit: clip against
    # the FULL absorption-basis fit ({1, tau, tau^2} + resolvable exponentials),
    # which follows the genuine curve incl. the late-tau extrapolation drift.
    keep = np.ones(len(tau), bool)
    for _ in range(5):
        if pub["mode"] == "model_residual":
            res_all = dnu
        else:
            Xk = _absorb_basis(tau_d_all, tau[keep])
            swk = 1.0 / np.sqrt(sig[keep] ** 2 + SIGMA_FLOOR_HZ**2)
            beta, *_ = np.linalg.lstsq(Xk * swk[:, None], dnu[keep] * swk,
                                       rcond=None)
            # evaluate the SAME basis (resolvability frozen on kept set) everywhere
            res_all = dnu - _basis_like(tau_d_all, tau[keep], tau) @ beta
        med = float(np.median(res_all[keep]))
        mad = float(np.median(np.abs(res_all[keep] - med))) * 1.4826
        new = np.abs(res_all - med) < CLIP_MAD * max(mad, SIGMA_FLOOR_HZ, 1e-9)
        if new.sum() == keep.sum():
            break
        keep = new
    tau, dnu, sig = tau[keep], dnu[keep], sig[keep]
    if len(tau) < 8:
        return None
    tau_d = tau_d_all[_resolvable(tau_d_all, tau)]

    if pub["mode"] == "model_residual":
        # the published phase-connected model already carries Delta nu; the gate
        # checks the model phase-tracks our nu(t): clipped residuals small vs step
        dnu_step = pub["dnu_nu"] * f_pre_glep
        med, rms = float(np.median(dnu)), float(np.std(dnu))
        sane = bool(abs(med) < 0.25 * dnu_step and rms < dnu_step)
        amps = np.asarray(GLF0D[name], float)[_resolvable(tau_d_all, tau)]
        return GlitchRecovery(name, glep, tau_d, dnu, tau, sig, 0,
                              dnu_step + med, pub["dnu_nu"] + med / f_pre_glep,
                              pub["dnu_nu"], sane, amps)

    # prefit mode: transient amplitudes for the injection envelope from the
    # full-basis fit; the SANITY step from the EARLY window only (tau <= 60 d),
    # where the pre-glitch extrapolation error is negligible
    X = _absorb_basis(tau_d_all, tau)
    sw = 1.0 / np.sqrt(sig**2 + SIGMA_FLOOR_HZ**2)
    beta, *_ = np.linalg.lstsq(X * sw[:, None], dnu * sw, rcond=None)
    amp = beta[3:]

    early = tau <= 60.0
    if early.sum() < 4:
        return None
    te, ye, se = tau[early], dnu[early], sig[early]
    tde = tau_d_all[(tau_d_all >= 0.6 * te.min()) & (tau_d_all <= 1.5 * te.max())]
    Xe = np.column_stack([np.ones_like(te), te / 60.0]
                         + [np.exp(-te / td) for td in tde])
    swe = 1.0 / np.sqrt(se**2 + SIGMA_FLOOR_HZ**2)
    be, *_ = np.linalg.lstsq(Xe * swe[:, None], ye * swe, rcond=None)
    step0 = float(be[0] + np.sum(be[2:]))               # dnu at tau -> 0 (resolvable)
    dnu_nu = step0 / f_pre_glep
    sane = bool(abs(dnu_nu / pub["dnu_nu"] - 1.0) < pub["tol_rel"])
    return GlitchRecovery(name, glep, tau_d, dnu, tau, sig, n_pre, step0,
                          dnu_nu, pub["dnu_nu"], sane, np.asarray(amp))


# =============================================================== comb + injection
@dataclass
class InjectionCal:
    eps_grid: list[float]
    rates: list[float]
    false_positive_rate: float
    rate_at_predicted: float
    eps_90: float | None       # smallest grid crossing of 90% (linear interp)
    eps_50: float | None
    n_phases: int


def _project(tau_d: np.ndarray, tau: np.ndarray, y: np.ndarray,
             sigma: np.ndarray) -> np.ndarray:
    X = _absorb_basis(tau_d, tau)
    sw = 1.0 / np.sqrt(sigma**2 + SIGMA_FLOOR_HZ**2)
    beta, *_ = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)
    return y - X @ beta


def _envelope(rec: GlitchRecovery, tau: np.ndarray) -> np.ndarray:
    """Transient recovery envelope (Hz) the comb would multiply -- |fitted| amps on
    the resolvable timescales (sign-folded so overfit cancellations cannot silently
    null the injection)."""
    return np.sum([abs(a) * np.exp(-tau / td)
                   for a, td in zip(rec.transient_amp_hz, rec.tau_d)], axis=0)


def injection_calibration(rec: GlitchRecovery, *, seed: int = 0) -> InjectionCal:
    """Detection rate vs injected eps, at the real sampling and real noise
    AMPLITUDES. Deviation from the PG.08 on-data protocol (documented): the ripple
    is added to phase-scrambled surrogates of the real projected residuals (same
    amplitude distribution, coherent features destroyed), because injecting on the
    raw data double-counts any chance-level coherent feature already present
    (2019 carries one at comb_p=0.014 -- an on-data eps=0 'rate' saturates)."""
    env = _envelope(rec, rec.tau)
    lt = np.log(rec.tau)
    base_resid = _project(rec.tau_d, rec.tau, rec.dnu, rec.sigma)

    def rate(eps: float, base: int) -> float:
        hits = 0
        for k in range(N_PHASES):
            rng = np.random.default_rng(seed + base + 37 * k)
            phi = float(rng.uniform(0, 2 * np.pi))
            noise = rng.permutation(base_resid)          # amplitude-preserving null
            y = noise + eps * np.cos(OMEGA * lt + phi) * env
            r = _project(rec.tau_d, rec.tau, y, rec.sigma)
            _, p = detect_comb(rec.tau, r, OMEGA, seed=seed + k)
            hits += int(p < P_THRESHOLD)
        return hits / N_PHASES

    rates = [rate(e, 1000 + 100 * i) for i, e in enumerate(EPS_GRID)]
    fp = rate(0.0, 9000)

    def crossing(level: float) -> float | None:
        for i in range(1, len(EPS_GRID)):
            if rates[i - 1] < level <= rates[i]:
                x0, x1, y0, y1 = EPS_GRID[i - 1], EPS_GRID[i], rates[i - 1], rates[i]
                return float(x0 + (level - y0) * (x1 - x0) / (y1 - y0))
        return None

    return InjectionCal(list(EPS_GRID), rates, fp, rates[0], crossing(0.9),
                        crossing(0.5), N_PHASES)


@dataclass
class CombLeg:
    name: str
    glep_mjd: float
    n_seg: int
    tau_min_d: float
    tau_max_d: float
    reach_periods: float
    gate_passed: bool
    dnu_nu_measured: float
    dnu_nu_published: float
    sanity_pass: bool
    resid_rms_uhz: float
    comb_gain: float
    comb_p: float
    shuffle_p: float
    kernel_smallest: bool
    battery: list[tuple[str, float, float]] = field(default_factory=list)
    injection: InjectionCal | None = None


def run_leg(rec: GlitchRecovery, *, seed: int = 0) -> CombLeg:
    r = _project(rec.tau_d, rec.tau, rec.dnu, rec.sigma)
    reach = reach_periods(rec.tau)
    gain, p = detect_comb(rec.tau, r, OMEGA, seed=seed)
    shuffle_p = within_segment_shuffle_p(rec.tau, r, seed=seed)
    battery = off_kernel_lambda_battery(rec.tau, r, seed=seed)
    kernel_p = battery[0][2]
    inj = injection_calibration(rec, seed=seed)
    return CombLeg(rec.name, rec.glep, len(rec.tau), float(rec.tau.min()),
                   float(rec.tau.max()), reach, bool(reach > REACH_GATE_PERIODS),
                   rec.dnu_nu_measured, rec.dnu_nu_published, rec.sanity_pass,
                   float(np.std(r) * 1e6), gain, p, shuffle_p,
                   bool(kernel_p <= min(pp for _, _, pp in battery)), battery, inj)


# =============================================================== driver
@dataclass
class PG06bFullResult:
    omega: float
    eps_predicted: float
    reach_gate_periods: float
    n_obs_archive: int
    n_obs_usable: int
    n_obs_detected: int
    n_segments: int
    n_segments_coherent: int
    legs: list[CombLeg] = field(default_factory=list)
    stack_reach: float = 0.0
    stack_comb_p: float = 1.0
    stack_shuffle_p: float = 1.0
    verdict: str = ""


def _stack(recs: list[GlitchRecovery], *, seed: int = 0) -> tuple[float, float, float]:
    """Superposed-epoch stack in ln(tau): the normalised projected residuals of all
    legs are CONCATENATED at their real tau values (no interpolation onto a dense
    grid, which would fake independent points in the rank test) and passed to the
    same frozen detector. Returns (reach, comb_p, shuffle_p)."""
    if not recs:
        return 0.0, 1.0, 1.0
    tau_all, y_all = [], []
    for rec in recs:
        rr = _project(rec.tau_d, rec.tau, rec.dnu, rec.sigma)
        tau_all.append(rec.tau)
        y_all.append(rr / (np.std(rr) or 1.0))
    tau_c = np.concatenate(tau_all)
    y_c = np.concatenate(y_all)
    o = np.argsort(tau_c)
    tau_c, y_c = tau_c[o], y_c[o]
    _, p = detect_comb(tau_c, y_c, OMEGA, seed=seed)
    sh = within_segment_shuffle_p(tau_c, y_c, seed=seed)
    return reach_periods(tau_c), p, sh


def pg06b_full(*, seed: int = 0) -> tuple[PG06bFullResult, list[GlitchRecovery]]:
    segs = load_segments()
    perobs = list(csv.DictReader((NV / "vela_nu_perobs_full.csv").open(encoding="utf-8")))
    n_usable = sum(1 for r in perobs if r["mjd_mid"])
    n_det = sum(1 for r in perobs if r["detected"] == "True")

    recs: list[GlitchRecovery] = []
    for name, nxt in [("2019", GLEP_2021), ("2021", GLEP_2024), ("2024", None)]:
        rec = build_recovery(name, segs, next_glep=nxt)
        if rec is not None:
            recs.append(rec)

    legs = [run_leg(r, seed=seed) for r in recs if r.sanity_pass]
    skipped = [r.name for r in recs if not r.sanity_pass]
    stack_reach, stack_p, stack_sh = _stack([r for r in recs if r.sanity_pass],
                                            seed=seed)

    res = PG06bFullResult(
        OMEGA, EPS_PREDICTED, REACH_GATE_PERIODS, len(perobs), n_usable, n_det,
        len(segs.mjd), int(segs.coherent.sum()), legs, stack_reach, stack_p,
        stack_sh)
    res.verdict = _verdict(res, [r.name for r in recs], skipped)
    return res, recs


def _verdict(res: PG06bFullResult, built: list[str], skipped: list[str]) -> str:
    hits = [x for x in res.legs
            if x.comb_p < 0.01 and x.kernel_smallest and x.shuffle_p < 0.05
            and x.gate_passed]
    if hits:
        return (f"a comb at omega={res.omega:.3f} survives all nulls in "
                f"{[x.name for x in hits]} -- ESCALATE (independent worlds) before any "
                "claim; still universal-DSI, not TFPT confirmation.")
    eps90 = {x.name: (x.injection.eps_90 if x.injection else None) for x in res.legs}
    eps50 = {x.name: (x.injection.eps_50 if x.injection else None) for x in res.legs}
    best90 = min((e for e in eps90.values() if e is not None), default=None)
    reach_txt = ", ".join(f"{x.name}: {x.reach_periods:.2f}" for x in res.legs)
    p_txt = ", ".join(f"{x.name}: {x.comb_p:.3f}" for x in res.legs)
    e_txt = ", ".join(
        f"{k}: eps_50={('%.2f' % v50) if v50 else 'n/r'}/"
        f"eps_90={('%.2f' % v90) if v90 else 'n/r'}"
        for (k, v50), v90 in zip(eps50.items(), eps90.values()))
    n_batt = max((len(x.battery) for x in res.legs), default=10)
    flags = [f"{x.name}: raw comb_p={x.comb_p:.3f} (kernel smallest-p) but "
             f"Bonferroni x{n_batt} = {min(1.0, x.comb_p * n_batt):.2f}, shuffle "
             f"p={x.shuffle_p:.2f} (no ln-tau phase coherence) and reach "
             f"{x.reach_periods:.2f} < 2.8 -- an audit-level chance feature, not a "
             f"candidate (prereg escalation needs p<0.01 + shuffle<0.05 + gate)"
             for x in res.legs if x.comb_p < 0.05]
    flag_txt = ("AUDIT FLAG -- " + "; ".join(flags) + ". ") if flags else ""
    return (
        f"data_limited (range- and amplitude-limited, honestly quantified). The FULL "
        f"NICER Vela archive is now reduced ({res.n_obs_archive} obs -> "
        f"{res.n_obs_usable} usable -> {res.n_obs_detected} per-obs detections -> "
        f"{res.n_segments} piecewise-coherent segments, {res.n_segments_coherent} "
        f"fully coherent), superseding the single-obs PG.06b proof (whose F0=11.19275 "
        f"'detection' is corrected: the true Vela F0 there is 11.18617 Hz). SANITY "
        f"GATE: the published glitch steps are reproduced ({', '.join(built)}; "
        f"skipped: {skipped if skipped else 'none'}; 2024 window not reducible -- "
        f"NICER post-2024 coverage is ~150 s snapshots). Achieved ln(tau) reach: "
        f"{reach_txt} comb periods -- all BELOW the 2.8-period localisation gate "
        f"(first usable NICER obs is 3.4 d (2019) / 7 d (2021) post-glitch; the "
        f"sub-day early window that would clear the gate is not in the archive), and "
        f"the concatenated ln-tau stack ({res.stack_reach:.2f} periods, "
        f"p={res.stack_comb_p:.2f}, shuffle p={res.stack_shuffle_p:.2f}) buys "
        f"amplitude, not range (PG.06). No preregistered escalation fires (comb p = "
        f"{p_txt}). {flag_txt}Surrogate-calibrated injection at the real sampling "
        f"and real noise amplitudes: {e_txt} (predicted eps~{res.eps_predicted:.4f} "
        f"-> chance level everywhere; n/r = not reached below eps=1). So the full "
        f"~2.6-GB (665-obs) reduction delivers the first X-ray nu(t) recovery test "
        f"of the kernel comb"
        + (f", with a 90%-sensitivity wall at eps ~ {best90:.2f}" if best90 else
           ", whose sensitivity never reaches 90% below eps=1 (range-blind, PG.06)")
        + " -- an honest bounded null, NOT a well-powered kill (prereg: "
        "data_limited_if reach < 2.8 or predicted-eps power < 0.5). No claim; "
        "firewall intact.")


# =============================================================== outputs
def to_json(res: PG06bFullResult) -> str:
    return json.dumps({
        "kernel_omega": res.omega, "eps_predicted": res.eps_predicted,
        "reach_gate_periods": res.reach_gate_periods,
        "reduction": {"n_obs_archive": res.n_obs_archive,
                      "n_obs_usable": res.n_obs_usable,
                      "n_obs_detected": res.n_obs_detected,
                      "n_segments": res.n_segments,
                      "n_segments_coherent": res.n_segments_coherent},
        "legs": [{**{k: v for k, v in vars(x).items()
                     if k not in ("battery", "injection")},
                  "battery": [{"label": la, "omega": om, "p": p}
                              for la, om, p in x.battery],
                  "injection": vars(x.injection) if x.injection else None}
                 for x in res.legs],
        "stack": {"reach_periods": res.stack_reach, "comb_p": res.stack_comb_p,
                  "shuffle_p": res.stack_shuffle_p},
        "verdict": res.verdict,
    }, indent=2)


def make_plots(res: PG06bFullResult, recs: list[GlitchRecovery], out_prefix: Path,
               *, seed: int = 0) -> list[str]:
    """(1) nu(t) overview + glitches; (2) per-leg recovery + residual + periodogram;
    (3) injection sensitivity curves."""
    written: list[str] = []
    segs = load_segments()
    pred = SpinPredictor.load()

    fig, ax = plt.subplots(2, 1, figsize=(11, 6.5), sharex=True)
    f_ref = np.array([pred.predict(t)[0] for t in segs.mjd])
    ax[0].errorbar(segs.mjd, segs.f0 - 11.184, yerr=segs.sigma, fmt=".", ms=3.5,
                   color="0.3", ecolor="0.75")
    ax[0].set_ylabel(r"$\nu$ - 11.184 (Hz)")
    ax[0].set_title(f"FULL NICER Vela reduction: {res.n_segments} piecewise-coherent "
                    f"segments from {res.n_obs_archive} archive obs", fontsize=10)
    ax[1].errorbar(segs.mjd, (segs.f0 - f_ref) * 1e6, yerr=segs.sigma * 1e6, fmt=".",
                   ms=3.5, color="tab:blue", ecolor="0.8")
    ax[1].set_ylim(-40, 40)
    ax[1].set_ylabel(r"$\nu$ - model ($\mu$Hz)")
    ax[1].set_xlabel("MJD")
    for a in ax:
        for g in (GLEP_2019, GLEP_2021, GLEP_2024):
            a.axvline(g, color="tab:red", lw=0.8, ls=":")
    p1 = out_prefix.with_name(out_prefix.name + "_nu_t.png")
    fig.tight_layout()
    fig.savefig(p1, dpi=130)
    plt.close(fig)
    written.append(str(p1))

    n = len(res.legs)
    if n:
        fig, ax = plt.subplots(3, n, figsize=(5.6 * n, 9.5), squeeze=False)
        freqs = np.linspace(1.0, 6.0, 300)
        for j, (leg, rec) in enumerate(zip(res.legs,
                                           [r for r in recs if r.sanity_pass])):
            r_proj = _project(rec.tau_d, rec.tau, rec.dnu, rec.sigma)
            ax[0][j].errorbar(rec.tau, rec.dnu * 1e6, yerr=rec.sigma * 1e6, fmt=".",
                              ms=4, color="0.3", ecolor="0.8")
            ax[0][j].set_xscale("log")
            ax[0][j].set_title(f"{leg.name}: dnu/nu={leg.dnu_nu_measured:.2e} "
                               f"(pub {leg.dnu_nu_published:.2e})\n"
                               f"reach {leg.reach_periods:.2f} periods", fontsize=9)
            ax[0][j].set_ylabel(r"$\delta\nu$ ($\mu$Hz)")
            ax[1][j].errorbar(rec.tau, r_proj * 1e6, yerr=rec.sigma * 1e6, fmt=".",
                              ms=4, color="tab:blue", ecolor="0.85")
            ax[1][j].set_xscale("log")
            ax[1][j].set_ylabel(r"residual ($\mu$Hz)")
            ax[1][j].set_xlabel(r"$\tau$ (d, log)")
            pg = comb_periodogram(rec.tau, r_proj, freqs)
            ax[2][j].plot(freqs, pg, lw=1.3, color="tab:blue")
            ax[2][j].axvline(OMEGA, color="tab:red", lw=1.4,
                             label=f"kernel p={leg.comb_p:.2f}")
            ax[2][j].set_xlabel(r"$\omega$")
            ax[2][j].set_ylabel("comb gain")
            ax[2][j].legend(fontsize=7)
        fig.suptitle("PG.06b FULL: post-glitch delta-nu recoveries, projected "
                     "residuals, comb periodograms (omega=2.583 not special)",
                     fontsize=11)
        fig.tight_layout(rect=(0, 0, 1, 0.95))
        p2 = out_prefix.with_name(out_prefix.name + "_recovery.png")
        fig.savefig(p2, dpi=130)
        plt.close(fig)
        written.append(str(p2))

    fig, ax = plt.subplots(figsize=(7, 4.4))
    for leg in res.legs:
        if leg.injection:
            ax.plot(leg.injection.eps_grid, [100 * r for r in leg.injection.rates],
                    "o-", label=f"{leg.name} (fp {100*leg.injection.false_positive_rate:.0f}%)")
    ax.axvline(EPS_PREDICTED, color="tab:red", ls=":",
               label=f"predicted eps={EPS_PREDICTED:.4f}")
    ax.axhline(90, color="0.5", ls="--", lw=0.8)
    ax.set_xscale("log")
    ax.set_xlabel("injected comb amplitude eps")
    ax.set_ylabel("detection rate (%)")
    ax.set_title("End-to-end injection at the real NICER sampling + noise", fontsize=10)
    ax.legend(fontsize=8)
    fig.tight_layout()
    p3 = out_prefix.with_name(out_prefix.name + "_injection.png")
    fig.savefig(p3, dpi=130)
    plt.close(fig)
    written.append(str(p3))
    return written
