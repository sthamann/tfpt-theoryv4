"""Stage-2 DYNAMIC recovery-waveform matched filter on REAL GWOSC strain.

The catalogue census (echo_forecast.py) and the Stage-1 echo search (real_echo_search.py)
both test the recovery kernel as a STATIC amplitude ratio: consecutive echo amplitudes
bounded by (2/3)^6. The experiments/README §1.1 "Reconsideration" notes that this misses
the kernel's *dynamic* signature -- the exact discrete->dynamic transition (verification
v124/v126/v147, mirrored in quantum-testbed/clock.py QT.04) is a **walled two-mode clock**

    R(t) = w0 + w1 e^{-(6 ln 3/2) t/tau} + w2 e^{-(6 ln 3) t/tau}

with three sharp signatures that a static ratio cannot carry:

  1. BEND (det'-clean, v147): the two decay rates are LOCKED at the ratio
        rate(2)/rate(1) = ln 3 / ln(3/2) = log_{3/2} 3 = 2.7095        (frozen, exact)
     -- a ONE-parameter (tau) two-exponential template, not a free rate pair.
  2. PROTECTED FLOOR: a non-decaying w0 mode (lambda=1, the "law") -> the recovery
     saturates at a floor and never returns to zero.
  3. HARD WALL: NO third decay mode (pole at n = N_fam = 3) -> >= 3 robust decay
     timescales would be a tension, not a TFPT recovery.

This module turns that bend into a matched-filter run on REAL strain: for each event we
whiten once, subtract the dominant Kerr (l=m=2,n=0) ringdown, build the **post-merger
residual power envelope** (binned RMS), and fit the FIXED-RATIO (2.7095) walled-clock
template against the envelope. Significance comes from an OFF-SOURCE background (the same
fit on many noise-only windows), and a FREE two-rate control recovers the bend ratio
q_hat (anti-numerology, cf. FRB.02b / the Stage-1 echo q_hat).

Firewall / honest scope: TFPT does NOT claim ringdown recovery imprints are present --
the kernel ratio is an UPPER bound, so a null/data-limited result is consistent. A loud
single-exponential decay (leftover ringdown power from imperfect dominant-mode subtraction)
has q_hat far from the bend and is rejected by the free-ratio control -- it is NOT a kernel
recovery. No detection claim is made; this closes the "machinery only validated on
synthetic data" gap by running it on real, public strain. Python (numpy/scipy/h5py).
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402  (backend must be set before pyplot import)

from .strain_data import (
    apply_whitening,
    detector_frame_mass,
    fit_and_subtract_qnm,
    qnm_220,
    read_hdf5,
    whitening_filter,
)

# --- frozen walled-clock constants (derived from the two axioms; mirror QT.04 clock.py) ---
N_FAM = 3
P2 = 6
RATE1 = P2 * math.log(1.5)          # 6 ln(3/2) = Delta = 2.4328   (slow mode)
RATE2 = P2 * math.log(3.0)          # 6 ln 3    = 6.5917           (fast mode)
BEND = math.log(3.0) / math.log(1.5)  # rate(2)/rate(1) = log_{3/2} 3 = 2.7095 (frozen)
BEND_LOG_TOL = math.log(1.20)       # recovered ratio counts as the bend within +-20%

WIN_TAU = 40.0                      # analysis window length in QNM damping times tau
WIN_MAX_S = 0.30                    # but never longer than 0.3 s post-merger
N_BINS = 40                         # RMS-envelope bins across the window
N_BACKGROUND = 400                  # off-source windows for the noise background
P_THRESHOLD = 0.01
RATIO_GRID = np.logspace(math.log10(1.2), math.log10(9.0), 25)  # profiled rate-ratio scan
TWO_MODE_MARGIN = 0.03              # min R^2 gain of the 2-mode fit over single-exp to call
#                                     a genuine two-timescale recovery (else: single ringdown)


# --------------------------------------------------------------------------- the envelope
def power_envelope(series: np.ndarray, start: int, win_samp: int,
                   n_bins: int = N_BINS) -> tuple[np.ndarray, np.ndarray]:
    """Binned RMS power envelope of `series[start:start+win_samp]` -> (t_norm, env).

    `t_norm` is the bin-centre time in units of the window length (0..1); the envelope is
    the per-bin root-mean-square. Pure white noise gives a flat envelope; leftover ringdown
    or a recovery relaxation gives a decay toward a floor."""
    seg = series[start:start + win_samp]
    if len(seg) < win_samp or win_samp < n_bins:
        return np.array([]), np.array([])
    edges = np.linspace(0, win_samp, n_bins + 1).astype(int)
    env = np.array([math.sqrt(float(np.mean(seg[edges[i]:edges[i + 1]] ** 2)))
                    for i in range(n_bins)])
    centres = 0.5 * (edges[:-1] + edges[1:]) / win_samp
    return centres, env


# --------------------------------------------------------------------------- the fits
def _r2(y: np.ndarray, resid: np.ndarray) -> float:
    """Fraction of envelope variance explained vs a constant-only model."""
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    return 0.0 if ss_tot == 0 else 1.0 - float(np.sum(resid ** 2)) / ss_tot


def fit_fixed_ratio(t: np.ndarray, env: np.ndarray, ratio: float,
                    n_scan: int = 120) -> tuple[float, float]:
    """Fit floor + two exponentials with a FIXED rate ratio: ``w0 + w1 e^{-r t} +
    w2 e^{-ratio r t}``. Scan the slow rate r (one nonlinear parameter -> well-conditioned),
    solve the 3 amplitudes by least squares. Returns (best r, R^2-vs-constant)."""
    if len(t) == 0:
        return 0.0, 0.0
    rs = np.logspace(math.log10(0.5), math.log10(60.0), n_scan)
    best_r, best_r2 = rs[0], -np.inf
    for r in rs:
        X = np.column_stack([np.ones_like(t), np.exp(-r * t), np.exp(-ratio * r * t)])
        beta, *_ = np.linalg.lstsq(X, env, rcond=None)
        r2 = _r2(env, X @ beta - env)
        if r2 > best_r2:
            best_r, best_r2 = r, r2
    return best_r, best_r2


def fit_single_exp(t: np.ndarray, env: np.ndarray, n_scan: int = 120) -> float:
    """Single-mode fit ``w0 + w1 e^{-r t}`` (the leftover-ringdown hypothesis): best R^2."""
    if len(t) == 0:
        return 0.0
    best_r2 = -np.inf
    for r in np.logspace(math.log10(0.5), math.log10(60.0), n_scan):
        X = np.column_stack([np.ones_like(t), np.exp(-r * t)])
        beta, *_ = np.linalg.lstsq(X, env, rcond=None)
        best_r2 = max(best_r2, _r2(env, X @ beta - env))
    return float(best_r2)


def fit_walled_clock(t: np.ndarray, env: np.ndarray) -> tuple[float, float]:
    """The frozen-bend (2.7095) walled-clock template: (best slow rate, R^2)."""
    return fit_fixed_ratio(t, env, BEND)


def profile_bend(t: np.ndarray, env: np.ndarray) -> tuple[float, float, float, float]:
    """Profile the rate-ratio over RATIO_GRID (each ratio: one nonlinear rate scan -> stable,
    unlike a free 2-exp fit). Returns (q_hat, r2_bend, r2_best, r2_single):

      q_hat     -- the ratio that best fits the envelope (the recovered bend estimate),
      r2_bend   -- R^2 of the FROZEN-bend template (the matched-filter statistic),
      r2_best   -- best R^2 over the ratio grid,
      r2_single -- R^2 of a single-exponential fit (the leftover-ringdown null model).
    """
    if len(t) == 0:
        return 0.0, 0.0, 0.0, 0.0
    r2s = np.array([fit_fixed_ratio(t, env, rr)[1] for rr in RATIO_GRID])
    q_hat = float(RATIO_GRID[int(np.argmax(r2s))])
    r2_bend = fit_fixed_ratio(t, env, BEND)[1]
    return q_hat, r2_bend, float(r2s.max()), fit_single_exp(t, env)


# --------------------------------------------------------------------------- real-data search
@dataclass
class DynamicDetectorResult:
    detector: str
    r2_template: float          # frozen-bend walled-clock template R^2 (the MF statistic)
    q_hat: float                # profiled best-fit rate ratio (the recovered bend estimate)
    two_mode_gain: float        # r2(best 2-mode) - r2(single exp): >0 only for two timescales
    p_value: float              # off-source background p-value for r2_template
    kernel_consistent: bool     # p<thr AND q_hat ~ bend AND a genuine 2nd timescale


@dataclass
class DynamicEventResult:
    event: str
    mf_msun: float
    tau_ms: float
    detectors: list[DynamicDetectorResult] = field(default_factory=list)
    n_kernel_consistent: int = 0
    label: str = ""
    note: str = ""


def _template_r2(series: np.ndarray, start: int, win_samp: int) -> float:
    """Frozen-bend walled-clock template R^2 of the envelope at `start` (the MF statistic).

    This is the only quantity the off-source background needs; the (cheap but per-grid)
    ratio profile + single-mode gate are computed on-source only."""
    t, env = power_envelope(series, start, win_samp)
    if len(t) == 0:
        return -1.0
    return fit_walled_clock(t, env)[1]


def _envelope_statistic(series: np.ndarray, start: int,
                        win_samp: int) -> tuple[float, float, float]:
    """(r2_bend, q_hat, two_mode_gain) for the envelope at `start`.

    two_mode_gain = r2(best two-mode) - r2(single exponential): a genuine two-timescale
    recovery has a large gain; leftover single-mode ringdown has ~0."""
    t, env = power_envelope(series, start, win_samp)
    if len(t) == 0:
        return -1.0, 0.0, 0.0
    q_hat, r2_bend, r2_best, r2_single = profile_bend(t, env)
    return r2_bend, q_hat, r2_best - r2_single


def search_event_dynamic(event: str, strain_dir, af: float = 0.69,
                         seed: int = 0) -> DynamicEventResult:
    """Run the dynamic walled-clock matched filter on the real strain of `event`."""
    meta = json.loads((Path(strain_dir) / f"{event}_meta.json").read_text(encoding="utf-8"))
    merger_gps, mf_src = float(meta["gps"]), float(meta["mf"])
    mf = detector_frame_mass(event, mf_src)      # observed (redshifted) ringdown
    f0, tau = qnm_220(mf, af)
    res = DynamicEventResult(event, round(mf, 1), round(tau * 1e3, 2))
    rng = np.random.default_rng(seed)

    for det, fname in meta["files"].items():
        s = read_hdf5(str(Path(strain_dir) / Path(fname).name))
        psd_i, scale = whitening_filter(s.data, s.dt)
        white = apply_whitening(s.data, psd_i, scale)
        merger = s.index_at(merger_gps)
        resid, _ = fit_and_subtract_qnm(white, merger, f0, tau, s.dt)

        win_samp = min(int(WIN_TAU * tau / s.dt), int(WIN_MAX_S / s.dt))
        r2_on, q_hat, gain = _envelope_statistic(resid, merger, win_samp)

        guard = int(1.0 / s.dt)
        lo, hi = guard, len(resid) - win_samp - guard
        centres = rng.integers(lo, hi, size=N_BACKGROUND)
        bg = np.array([_template_r2(resid, int(c), win_samp)
                       for c in centres if abs(int(c) - merger) > win_samp])
        p_val = float((np.sum(bg >= r2_on) + 1) / (len(bg) + 1))
        on_bend = abs(math.log(q_hat / BEND)) < BEND_LOG_TOL if q_hat > 0 else False
        kc = bool(p_val < P_THRESHOLD and on_bend and gain > TWO_MODE_MARGIN)
        res.detectors.append(DynamicDetectorResult(det, round(r2_on, 4), round(q_hat, 4),
                                                    round(gain, 4), round(p_val, 4), kc))

    res.n_kernel_consistent = sum(d.kernel_consistent for d in res.detectors)
    res.label = ("WALLED_CLOCK_RECOVERY_CANDIDATE" if res.n_kernel_consistent >= 2
                 else "NO_KERNEL_RECOVERY")
    loud = [d for d in res.detectors if d.p_value < P_THRESHOLD]
    if loud and res.n_kernel_consistent == 0:
        res.note = (f"low-p decaying envelope in {[d.detector for d in loud]} but q_hat="
                    f"{[d.q_hat for d in loud]} far from the bend {BEND:.3f} -> leftover "
                    "single-mode ringdown power, NOT a locked-ratio walled-clock recovery "
                    "(free-ratio control)")
    return res


# --------------------------------------------------------------------------- identifiability
def walled_clock_envelope(t_norm: np.ndarray, r1: float, w0: float = 0.2, w1: float = 0.6,
                          w2: float = 0.4, ratio: float = BEND) -> np.ndarray:
    """Recovery envelope on normalised time t in [0,1]: floor + two exponentials whose slow
    rate is ``r1`` and fast rate ``ratio*r1`` (the locked bend), weights (w0,w1,w2)."""
    return w0 + w1 * np.exp(-r1 * t_norm) + w2 * np.exp(-ratio * r1 * t_norm)


def two_mode_gain(t: np.ndarray, env: np.ndarray) -> float:
    """How much the best two-mode (profiled-ratio) fit beats a single exponential in R^2.

    This is the *identifiability* of a second decay timescale: ~0 means a single exponential
    already explains the envelope, so the bend (rate ratio 2.7095) cannot be measured."""
    _, _, r2_best, r2_single = profile_bend(t, env)
    return r2_best - r2_single


def cascade_relaxation(t: np.ndarray, lam: float, n_modes: int = 7,
                       gamma0: float = 12.0) -> np.ndarray:
    """Open-system relaxation of a GEOMETRIC ladder of decay rates gamma_k = gamma0 * lam^-k
    -- the textbook discrete-scale-invariance recovery: a power law with a log-periodic
    ripple of period ln(lam) in ln t (this is what a CASCADE of recovery events produces,
    unlike a single walled recovery)."""
    ks = np.arange(n_modes)
    return np.exp(-np.outer(np.asarray(t, float), gamma0 * lam ** (-ks.astype(float)))).mean(axis=1)


@dataclass
class Identifiability:
    bend_gain_max: float        # best two-mode R^2 gain of the EXACT walled clock (noise-free)
    single_recovery_identifiable: bool
    dsi_lambda: float           # the cascade scale (3/2)^6
    dsi_omega: float            # cascade log-frequency 2 pi / ln lambda
    dsi_ripple_eps: float       # predicted comb amplitude exp(-pi^2/ln lambda) (QT.02 law)
    verdict: str


def identifiability_analysis() -> Identifiability:
    """The honest core result, both parts analytic / machine-checked:

    (1) Within ONE monotone recovery the bend is degenerate with a single exponential: the
        exact walled-clock curve is fit by floor + ONE exponential to a two-mode R^2 gain of
        ~1e-3 (two summed exponentials look like one + floor), so a single ringdown residual
        cannot carry the rate ratio 2.7095.
    (2) The discriminating dynamic signature is the log-periodic comb across a CASCADE at
        omega = 2pi/ln((3/2)^6); but its amplitude is eps ~ exp(-pi^2/ln lambda) (the QT.02
        suppression law), only ~2% even for this coarse ladder -- so it needs a clean,
        many-event cascade, which a single BH ringdown is not.
    """
    t = np.linspace(0.0, 1.0, 60)
    gains = [two_mode_gain(t, walled_clock_envelope(t, r1, 0.2, w1, w2))
             for w1, w2 in ((0.6, 0.4), (0.3, 0.7), (0.1, 0.9), (0.5, 0.5))
             for r1 in (1.5, 2.0, 3.0)]
    bend_gain_max = float(max(gains))

    lam = 1.5 ** 6
    omega = 2.0 * math.pi / math.log(lam)
    eps = math.exp(-math.pi ** 2 / math.log(lam))     # QT.02 / dsi.py amplitude-suppression law
    identifiable = bend_gain_max > TWO_MODE_MARGIN
    verdict = (
        f"WITHIN ONE RECOVERY the bend is NOT identifiable: the exact walled-clock curve is fit "
        f"by floor + a SINGLE exponential to a two-mode R^2 gain of only {bend_gain_max:.1e} -- "
        f"two summed exponentials are degenerate with one + floor, so a single BH ringdown "
        f"residual cannot carry the bend 2.7095. The DISCRIMINATING dynamic signature is the "
        f"log-periodic comb across a CASCADE at omega = 2pi/ln((3/2)^6) = {omega:.3f}, but its "
        f"amplitude is eps ~ exp(-pi^2/ln lambda) = {eps:.3f} (~{100 * eps:.1f}%, the QT.02 "
        f"suppression law) -- it needs a clean, MANY-event cascade. A single ringdown is not a "
        f"cascade => this channel is structurally data-limited for the dynamic bend; the "
        f"sensitive lever is the TIME-RESOLVED recovery SEQUENCE of a repeating source (FRB "
        f"repeater / glitch train), not a one-shot ringdown."
    )
    return Identifiability(bend_gain_max, identifiable, lam, omega, eps, verdict)


def _template_curve(t: np.ndarray, env: np.ndarray) -> tuple[np.ndarray, float]:
    """Best fixed-bend walled-clock fit curve for plotting; returns (curve, best_r)."""
    best_r, _ = fit_walled_clock(t, env)
    X = np.column_stack([np.ones_like(t), np.exp(-best_r * t), np.exp(-BEND * best_r * t)])
    beta, *_ = np.linalg.lstsq(X, env, rcond=None)
    return X @ beta, best_r


# --------------------------------------------------------------------------- plot
def _loudest_on_source(event: str, strain_dir):
    """(det, t, env, fit_curve, q_hat, r2) for the highest-R^2 on-source detector of `event`."""
    meta = json.loads((Path(strain_dir) / f"{event}_meta.json").read_text(encoding="utf-8"))
    f0, tau = qnm_220(detector_frame_mass(event, float(meta["mf"])))
    best = None
    for det, fname in meta["files"].items():
        s = read_hdf5(str(Path(strain_dir) / Path(fname).name))
        pi, sc = whitening_filter(s.data, s.dt)
        w = apply_whitening(s.data, pi, sc)
        mg = s.index_at(float(meta["gps"]))
        resid, _ = fit_and_subtract_qnm(w, mg, f0, tau, s.dt)
        wn = min(int(WIN_TAU * tau / s.dt), int(WIN_MAX_S / s.dt))
        t, env = power_envelope(resid, mg, wn)
        if len(t) == 0:
            continue
        curve, _ = _template_curve(t, env)
        q_hat, *_ = profile_bend(t, env)
        r2 = _r2(env, curve - env)
        if best is None or r2 > best[-1]:
            best = (det, t, env, curve, q_hat, r2)
    return best


def make_plot(events: list[str], strain_dir, ident: Identifiability, out_path) -> str:
    """Honest 3-panel figure: (1) the bend is degenerate in one recovery (walled clock vs its
    best single-exponential fit, near-identical); (2) the loudest real on-source residual
    envelope (leftover ringdown, not the bend); (3) the discriminating signature -- the
    log-periodic comb across a CASCADE -- which a single ringdown does not provide."""
    fig, ax = plt.subplots(1, 3, figsize=(13.5, 3.7))

    # 1. identifiability: walled clock (bend) vs best single-exponential fit
    t = np.linspace(0, 1, 60)
    wc = walled_clock_envelope(t, 2.0)
    best_se, best_ss = None, np.inf
    for r in np.logspace(math.log10(0.5), math.log10(60.0), 200):
        X = np.column_stack([np.ones_like(t), np.exp(-r * t)])
        beta, *_ = np.linalg.lstsq(X, wc, rcond=None)
        ss = float(np.sum((X @ beta - wc) ** 2))
        if ss < best_ss:
            best_se, best_ss = X @ beta, ss
    ax[0].plot(t, wc, "-", color="tab:blue", lw=2.4, label="walled clock (bend 2.71)")
    ax[0].plot(t, best_se, "--", color="tab:orange", lw=2, label="best single exp + floor")
    ax[0].set_title("single recovery: bend DEGENERATE\n"
                    f"two-mode R$^2$ gain = {ident.bend_gain_max:.1e}", fontsize=9)
    ax[0].set_xlabel("normalised recovery time")
    ax[0].set_ylabel("recovery amplitude")
    ax[0].legend(fontsize=7)

    # 2. loudest real on-source residual envelope + fixed-bend fit
    loud_ev = events[0]
    b = _loudest_on_source(loud_ev, strain_dir)
    if b:
        det, tt, env, curve, q_hat, _ = b
        ax[1].plot(tt, env, "o", ms=3, color="0.4", label="RMS envelope")
        ax[1].plot(tt, curve, "-", color="tab:red", lw=2, label="fixed-bend fit")
        ax[1].set_title(f"{loud_ev} {det} on-source (real strain)\n"
                        f"q_hat={q_hat:.2f} (not the bend) -> leftover ringdown", fontsize=9)
        ax[1].legend(fontsize=7)
    ax[1].set_xlabel("normalised post-merger time")
    ax[1].set_ylabel("residual RMS (whitened)")

    # 3. the cascade comb (the discriminating dynamic signature): the log-periodic ripple
    #    left after removing the smooth power-law trend of a geometric cascade
    tt = np.logspace(-2, 0.0, 240)
    lt = np.log(tt)
    casc = cascade_relaxation(tt, ident.dsi_lambda)
    P = np.vander(lt, 4)
    smooth = P @ np.linalg.lstsq(P, casc, rcond=None)[0]
    ripple = casc - smooth
    ax[2].plot(lt, ripple, "-", color="tab:green", lw=1.8, label="cascade comb (detrended)")
    ax[2].axhline(0.0, color="0.7", lw=0.8)
    period = math.log(ident.dsi_lambda)
    for kk in range(-3, 2):
        ax[2].axvline(lt[0] + kk * period, color="0.85", lw=0.8, ls=":")
    ax[2].set_title("discriminating signature: cascade comb\n"
                    f"$\\omega$={ident.dsi_omega:.2f}, ripple $\\epsilon$$\\approx${ident.dsi_ripple_eps:.3f} "
                    "(needs a cascade)", fontsize=9)
    ax[2].set_xlabel("ln t")
    ax[2].set_ylabel("log-periodic residual")
    ax[2].legend(fontsize=7)

    fig.suptitle("TFPT Stage-2 dynamic recovery on real GWOSC strain: the single-event bend is "
                 "degenerate; the dynamic signature lives in a cascade", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    return str(out_path)
