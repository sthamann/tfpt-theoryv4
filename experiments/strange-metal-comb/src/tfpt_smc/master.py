"""Strange-metal master-curve construction + comb-ripple tests (SMC.01..SMC.07).

Observable semantics (LOCKED before the data pass -- hypotheses/strange_metal_comb_v1.yaml):
the observable is the real optical conductivity sigma1(omega, T) of LSCO x=0.24 (Michon+ 2023
open data), collapsed onto the paper's own omega/T master curve. With Planckian nu=1 scaling
sigma(omega,T) ~ T^-1 F(omega/T), the master observable is

    y = ln(T * sigma1)   versus   u = ln(hbar*omega / k_B T),

and the TFPT comb (1 + eps cos(OMEGA u + phi)) is an ADDITIVE ripple of amplitude ~eps in y.
Ingestion follows the SOURCE PAPER's own scaling analysis (fig02 code in the Yareta archive):
sigma1[kS/cm] = 0.134518794412 * E[eV] * eps2, temperatures from 40 K (normal state, above the
Tc=19 K / phase-fluctuation region), energies up to 0.4 eV (below interband). The DETECTOR is
the frozen recovery-comb kernel (comb.py, verbatim port, guarded by tests/).

FIREWALL: strange metals have NO established boundary-recovery structure; even a hit would be a
universal-DSI coincidence, never TFPT confirmation. A null is expected and informative.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.interpolate import LSQUnivariateSpline

from .comb import (
    MIN_COMB_PERIODS,
    OMEGA,
    P_THRESHOLD,
    TFPT_LAMBDAS,
    _comb_gain,
    _omega,
    kernel_pvalue,
)

DATA = Path(__file__).resolve().parents[2] / "data"

KB_EV = 8.61733027353e-5          # Boltzmann constant in eV/K (as in the paper's fig02 code)
SIGMA_CONV = 0.134518794412       # eps0*eV/hbar in kS/cm: sigma1[kS/cm] = conv * E[eV] * eps2
LSCO_TEMPS = (9, 15, 20, 30, 40, 50, 60, 75, 100, 150, 200, 250, 300)   # columns of the file
T_MIN = 40.0                      # the paper's own scaling window: temperatures from 40 K
E_MAX = 0.4                       # the paper's own scaling window: energies up to 0.4 eV
E_MAX_DRUDE = 1.0                 # control window: stay intraband (below Au/Cu interband edge)
T_DRUDE = 295.0                   # room temperature assumed for the Ordal tables
SPLINE_KNOT_SPACING = 3.0         # in u; WIDER than one comb period (2.43) so the spline
                                  # baseline cannot absorb the kernel ripple


# --------------------------------------------------------------------------- data ingestion
@dataclass
class MasterCurve:
    name: str
    u: np.ndarray                 # ln(hbar*omega / k_B T), sorted ascending
    y: np.ndarray                 # ln(T^x * sigma1)
    T_of: np.ndarray              # temperature label per point (K)
    temps: tuple[float, ...]      # distinct temperatures used
    n_dropped: int                # non-positive sigma1 points dropped (noise floor)
    provenance: str

    @property
    def u_range(self) -> float:
        return float(self.u.max() - self.u.min())

    @property
    def periods(self) -> float:
        return self.u_range / np.log(TFPT_LAMBDAS["(3/2)^6 (recovery comb)"])


def load_lsco(path: Path = DATA / "lsco_x0p24_epsilon.txt") -> MasterCurve:
    """Build the LSCO x=0.24 sigma1(omega/T)*T master curve from the Michon+ 2023 dielectric
    function, with the PAPER's own conversion, temperature window and energy window."""
    raw = np.loadtxt(path)
    E = raw[:, 0]
    us, ys, ts = [], [], []
    dropped = 0
    kept_T = []
    for k, T in enumerate(LSCO_TEMPS):
        if T < T_MIN:
            continue
        kept_T.append(float(T))
        eps2 = raw[:, 2 * (k + 1)]
        m = (E <= E_MAX) & (eps2 > 0)
        dropped += int(((E <= E_MAX) & ~(eps2 > 0)).sum())
        sigma1 = SIGMA_CONV * E[m] * eps2[m]      # kS/cm
        us.append(np.log(E[m] / (KB_EV * T)))
        ys.append(np.log(T * sigma1))
        ts.append(np.full(m.sum(), float(T)))
    u = np.concatenate(us)
    y = np.concatenate(ys)
    t = np.concatenate(ts)
    order = np.argsort(u)
    return MasterCurve("LSCO_x0.24", u[order], y[order], t[order], tuple(kept_T), dropped,
                       "Michon+ 2023 Nat.Commun. 14:3033 open data (Yareta, CC-BY-4.0), "
                       "Epsilon_LSCO-0p24.txt; y=ln(T*sigma1), paper window T>=40K, E<=0.4eV")


def load_drude(path: Path, name: str) -> MasterCurve:
    """A conventional-metal control curve: sigma1 from tabulated n,k (eps2 = 2nk), single
    temperature, intraband window."""
    E, n, k = [], [], []
    with path.open(encoding="utf-8") as fh:
        for row in csv.reader(fh):
            if not row or row[0].startswith("#"):
                continue
            E.append(float(row[0]))
            n.append(float(row[1]))
            k.append(float(row[2]))
    E, n, k = np.asarray(E), np.asarray(n), np.asarray(k)
    m = (E <= E_MAX_DRUDE) & (n * k > 0)
    sigma1 = SIGMA_CONV * E[m] * 2.0 * n[m] * k[m]
    u = np.log(E[m] / (KB_EV * T_DRUDE))
    order = np.argsort(u)
    return MasterCurve(name, u[order], np.log(sigma1)[order],
                       np.full(m.sum(), T_DRUDE)[order], (T_DRUDE,), int((~m).sum()),
                       f"Ordal n,k tables via refractiveindex.info (CC0); {path.name}, "
                       f"E<={E_MAX_DRUDE}eV intraband window, T={T_DRUDE}K assumed")


# --------------------------------------------------------------------------- detrend variants
def poly_residuals(u: np.ndarray, y: np.ndarray, deg: int) -> np.ndarray:
    P = np.vander(u, deg + 1)
    b, *_ = np.linalg.lstsq(P, y, rcond=None)
    return y - P @ b


def spline_residuals(u: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Cubic smoothing-spline baseline with interior knots every SPLINE_KNOT_SPACING in u
    (wider than one comb period, so the baseline cannot track the kernel ripple)."""
    knots = np.arange(u.min() + SPLINE_KNOT_SPACING, u.max() - 1e-9, SPLINE_KNOT_SPACING)
    spl = LSQUnivariateSpline(u, y, knots, k=3)
    return y - spl(u)


def per_T_residuals(mc: MasterCurve, deg: int = 2, y: np.ndarray | None = None) -> np.ndarray:
    """Detrend each temperature's segment separately (absorbs per-T calibration offsets and
    imperfect collapse), then pool -- the superposed-epoch convention of crust-cooling-comb.
    Each single-T segment spans only ~2.1 comb periods (partially absorbing the comb), but the
    segments are offset in u and the comb phase is common in u, so the pooled field retains it."""
    yy = mc.y if y is None else y
    r = np.empty_like(yy)
    for T in mc.temps:
        m = mc.T_of == T
        r[m] = poly_residuals(mc.u[m], yy[m], deg)
    return r


# --------------------------------------------------------------------------- SMC.01 kernel rank
def dense_rank(u: np.ndarray, y: np.ndarray, *, deg: int | None = 2,
               residuals: np.ndarray | None = None,
               f_lo: float = 1.0, f_hi: float = 6.0, n_freq: int = 400) -> dict:
    """Preregistered off-kernel periodogram rank on a DENSE uniform grid omega in [1,6]:
    p = fraction of off-kernel log-frequencies (kernel +/-10% excluded) whose comb gain >= the
    kernel gain. `deg` uses the frozen joint poly+harmonic gain; `residuals` (spline / per-T
    variants) uses a constant+harmonic gain on the precomputed residual field -- either way the
    statistic is exchangeable across omega under H0."""
    if residuals is not None:
        lt, yy, d = u, residuals, 0
    else:
        lt, yy, d = u, y, int(deg)
    fs = np.linspace(f_lo, f_hi, n_freq)
    g0 = _comb_gain(lt, yy, OMEGA, deg=d)
    off = fs[np.abs(fs - OMEGA) > 0.1 * OMEGA]
    null = np.array([_comb_gain(lt, yy, f, deg=d) for f in off])
    return {"gain": round(g0, 6), "p_value": round(float((1 + np.sum(null >= g0))
            / (len(null) + 1)), 4), "n_off": int(len(off)),
            "best_off_omega": round(float(off[np.argmax(null)]), 3)}


# --------------------------------------------------------------------------- SMC.02 amplitude
def amplitude_fit(u: np.ndarray, r: np.ndarray, omega: float = OMEGA) -> dict:
    """Least-squares eps_hat, phi_hat of eps*cos(omega u + phi) on the residuals r(u)."""
    X = np.column_stack([np.ones_like(u), np.cos(omega * u), np.sin(omega * u)])
    b, *_ = np.linalg.lstsq(X, r, rcond=None)
    eps = float(np.hypot(b[1], b[2]))
    phi = float(np.arctan2(-b[2], b[1]))
    return {"eps_hat": round(eps, 5), "phi_hat": round(phi, 3),
            "resid_rms": round(float(np.std(r)), 5)}


# --------------------------------------------------------------------------- SMC.03 nulls
def _eps_at_kernel(u: np.ndarray, r: np.ndarray) -> float:
    X = np.column_stack([np.ones_like(u), np.cos(OMEGA * u), np.sin(OMEGA * u)])
    b, *_ = np.linalg.lstsq(X, r, rcond=None)
    return float(np.hypot(b[1], b[2]))


def null_batteries(mc: MasterCurve, r: np.ndarray, *, n_draws: int = 1000,
                   seed: int = 0) -> dict:
    """(a) residual point-permutation null (destroys everything incl. autocorrelation --
    anti-conservative on smooth data, reported for completeness); (b) per-temperature cyclic
    shift null (preserves each T-segment's autocorrelation, destroys the common comb phase in u
    -- the conservative block-style null). Prereg: report both, use the LARGER p."""
    eps_obs = _eps_at_kernel(mc.u, r)
    rng = np.random.default_rng(seed)
    perm = np.empty(n_draws)
    for i in range(n_draws):
        perm[i] = _eps_at_kernel(mc.u, rng.permutation(r))
    p_perm = float((1 + np.sum(perm >= eps_obs)) / (n_draws + 1))
    shift = np.empty(n_draws)
    r2 = np.empty_like(r)
    for i in range(n_draws):
        for T in mc.temps:
            m = mc.T_of == T
            seg = r[m]
            r2[m] = np.roll(seg, int(rng.integers(1, max(2, len(seg)))))
        shift[i] = _eps_at_kernel(mc.u, r2)
    p_shift = float((1 + np.sum(shift >= eps_obs)) / (n_draws + 1))
    return {"eps_obs": round(eps_obs, 5),
            "p_permutation": round(p_perm, 4), "p_block_shift": round(p_shift, 4),
            "p_conservative": round(max(p_perm, p_shift), 4),
            "eps95_null": round(float(np.quantile(shift, 0.95)), 5)}


# --------------------------------------------------------------------------- SMC.04 battery
def lambda_battery(mc: MasterCurve, *, seed: int = 19) -> tuple[dict, float, int, str]:
    """Full TFPT log-period battery on the master curve: matched-pool permutation p at each
    omega=2pi/ln(lambda) (frozen kernel_pvalue), per-lambda u-range (>=2.8 periods of THAT
    lambda) + Nyquist gate, Bonferroni look-elsewhere over the gated lambdas."""
    t = np.exp(mc.u)
    dln = float(np.median(np.diff(mc.u))) or 1e-9
    nyq = np.pi / dln
    battery: dict = {}
    for i, (label, lam) in enumerate(TFPT_LAMBDAS.items()):
        om = _omega(lam)
        periods = mc.u_range / np.log(lam)
        gated = bool(periods >= MIN_COMB_PERIODS and om <= nyq)
        entry = {"lambda": round(lam, 4), "omega": round(om, 3),
                 "periods": round(periods, 2), "gated": gated,
                 "idio": label in {"3/2 (1/Koide, fundamental)", "phi (golden, g_car=5)",
                                   "(3/2)^6 (recovery comb)"}}
        if gated:
            p, g = kernel_pvalue(t, mc.y, omega=om, seed=seed + i)
            entry.update({"p_value": round(p, 4), "gain": round(g, 6),
                          "comb_detected": bool(p < P_THRESHOLD)})
        else:
            entry.update({"p_value": 1.0, "gain": 0.0, "comb_detected": False})
        battery[label] = entry
    tested = [v for v in battery.values() if v["gated"]]
    min_p = min((v["p_value"] for v in tested), default=1.0)
    m_eff = max(1, len(tested))
    best = min((kv for kv in battery.items() if kv[1]["gated"]),
               key=lambda kv: kv[1]["p_value"], default=(None, None))[0]
    return battery, round(min(1.0, min_p * m_eff), 4), m_eff, best or "none gated"


# --------------------------------------------------------------------------- SMC.05 injection
def injection_power(mc: MasterCurve, *, eps_list=(0.0173, 0.05), n_seeds: int = 40,
                    seed0: int = 7000, variant: str = "primary") -> list[dict]:
    """Inject a multiplicative kernel ripple (random phase per seed) into the REAL master curve
    and rerun the detector (detection = p < 0.05; the u-range gate is already satisfied by the
    real curve). `variant="primary"` is the frozen deg-2 detector; `variant="spline"` is the
    most sensitive documented detrend (knots wider than one comb period) -- the honest power
    statement uses BOTH. The eps=0.0173 row answers: is the data precision even sufficient?"""
    out = []
    for eps in eps_list:
        hits, ps = 0, []
        for s in range(n_seeds):
            rng = np.random.default_rng(seed0 + s)
            phi = rng.uniform(0.0, 2.0 * np.pi)
            y_inj = mc.y + np.log(1.0 + eps * np.cos(OMEGA * mc.u + phi))
            if variant == "spline":
                res = dense_rank(mc.u, y_inj, residuals=spline_residuals(mc.u, y_inj))
            elif variant == "per_T":
                res = dense_rank(mc.u, y_inj, residuals=per_T_residuals(mc, deg=2, y=y_inj))
            else:
                res = dense_rank(mc.u, y_inj, deg=2)
            ps.append(res["p_value"])
            hits += int(res["p_value"] < P_THRESHOLD)
        out.append({"eps": eps, "variant": variant, "n_seeds": n_seeds,
                    "detect_rate": round(hits / n_seeds, 3),
                    "median_p": round(float(np.median(ps)), 4)})
    return out
