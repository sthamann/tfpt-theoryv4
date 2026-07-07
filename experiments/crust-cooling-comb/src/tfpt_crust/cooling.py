"""Crust-cooling recovery-comb analysis: reader, superposed-epoch stack, lambda-battery, floor.

Observable semantics (LOCKED before the data pass -- see hypotheses/crust_cooling_comb_v1.yaml):
the observable is the redshift-corrected effective surface temperature ``kT_eff^inf(t)`` versus time
since the end of the accretion outburst. The TFPT comb ``R(t)=power*(1+eps cos(omega ln t + phi))``
is a MULTIPLICATIVE fractional ripple on the smooth relaxation, so the recovery observable is
``y = ln(kT_eff)`` (the ripple becomes additive, amplitude ~eps, and the smooth exponential-to-floor
cooling is absorbed by the detector's degree-2 poly-in-ln(t) baseline -- identical treatment to the
recovery-comb-domains flux channels y=ln(flux)).

Crust cooling is the cleanest FLOOR-TERMINATED relaxation-to-attractor outside the horizon: the
crust relaxes to a nonzero core-equilibrium offset ``b`` (the well-known "cooling curves cannot be
fit without a constant offset" fact) -- a natural, if generic, test of the TFPT protected floor.

FIREWALL: crust cooling is neutron-star crust HEAT DIFFUSION at the surface, NOT a horizon/boundary
recovery and NOT a geometric mode ladder. There is no a-priori reason for omega=2.583 here, so a hit
would be a universal-DSI coincidence, NEVER TFPT confirmation. The sole value of this domain is as
the independent SECOND data world the discriminating comb needs (omega=2.583 in >=2 worlds).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

from .comb import (
    BATTERY_IDIO,
    BATTERY_LAMBDAS,
    LAMBDA,
    MIN_COMB_PERIODS,
    OMEGA,
    P_THRESHOLD,
    _omega,
    _stacked_at,
    comb_periods,
    detect_comb,
    run_comb,
    stacked_comb_test,
)

DATA = Path(__file__).resolve().parents[2] / "data"


# --------------------------------------------------------------------------- data ingestion
@dataclass
class CoolingCurve:
    name: str
    source: str
    t: np.ndarray            # days since end of outburst (>0)
    kT: np.ndarray           # effective surface temperature kT_eff^inf (eV)
    err: np.ndarray          # 1-sigma / quoted error (eV)
    provenance: str = ""
    ingest: str = ""
    notes: str = ""

    @property
    def y(self) -> np.ndarray:
        """Recovery observable y = ln(kT_eff): the fractional comb ripple becomes additive."""
        return np.log(self.kT)

    @property
    def ln_range(self) -> float:
        return float(np.log(self.t.max() / self.t.min())) if len(self.t) > 1 else 0.0

    @property
    def periods(self) -> float:
        return comb_periods(self.t)


def read_cooling_curve(path: Path) -> CoolingCurve | None:
    """Read a derived cooling CSV (``t_days_since_outburst,kT_eff_eV,err``; ``#``-comment header
    lines carry provenance). Returns a CoolingCurve with t, kT, err > 0, or None if < 4 points."""
    meta = {"source": path.stem, "provenance": "", "ingest": "", "notes": ""}
    t, kt, er = [], [], []
    try:
        with path.open(encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if not line:
                    continue
                if line.startswith("#"):
                    parts = [p.strip().strip('"') for p in line.lstrip("# ").split(",", 1)]
                    if len(parts) == 2 and parts[0] in meta:
                        meta[parts[0]] = parts[1]
                    continue
                cells = next(csv.reader([line]))
                if not cells or cells[0].lower().startswith("t_days"):
                    continue
                try:
                    tv, kv, ev = float(cells[0]), float(cells[1]), float(cells[2])
                except (IndexError, ValueError):
                    continue
                if tv > 0 and kv > 0:
                    t.append(tv)
                    kt.append(kv)
                    er.append(ev)
    except OSError:
        return None
    if len(t) < 4:
        return None
    order = np.argsort(t)
    t = np.asarray(t)[order]
    kt = np.asarray(kt)[order]
    er = np.asarray(er)[order]
    return CoolingCurve(path.stem, meta["source"], t, kt, er,
                        meta["provenance"], meta["ingest"], meta["notes"])


def load_all(data_dir: Path = DATA) -> list[CoolingCurve]:
    files = sorted(data_dir.glob("*.csv")) if data_dir.exists() else []
    return [c for c in (read_cooling_curve(p) for p in files) if c is not None]


# --------------------------------------------------------------------------- superposed-epoch stack
def superposed_epoch_stack(curves: list[CoolingCurve], *, deg: int = 2, seed: int = 0) -> dict:
    """The SUPERPOSED-EPOCH test the domain calls for: pool every cooling episode into ONE ln(t)
    series (each aligned at its own outburst end, t=0), after removing each curve's smooth
    exponential-to-floor trend (degree-`deg` poly-in-ln(t), which also removes the source-specific
    temperature offset). The pooled series spans the UNION ln-range, which -- unlike any single
    curve -- can clear the >=2.8-comb-period gate, and its density (~all epochs combined) beats the
    faint ~2% amplitude. Then rank the kernel omega=2.583 comb gain against the off-kernel
    periodogram (``detect_comb``).

    KEY ASSUMPTION (documented, optimistic): the comb PHASE phi is common across sources because the
    log-periodic cascade clock is anchored at the relaxation onset (t=0 = outburst end). If phi is
    source-random the pooled comb washes out (tested in the injection battery, `aligned=False`)."""
    lts, rs = [], []
    for c in curves:
        lt = np.log(c.t)
        P = np.vander(lt, deg + 1)
        b, *_ = np.linalg.lstsq(P, c.y, rcond=None)
        rs.append(c.y - P @ b)     # per-curve residual: removes trend + source offset
        lts.append(lt)
    lt_all = np.concatenate(lts)
    r_all = np.concatenate(rs)
    order = np.argsort(lt_all)
    t_all = np.exp(lt_all[order])
    r_all = r_all[order]
    periods = comb_periods(t_all)
    gain, p = detect_comb(t_all, r_all, seed=seed)
    enough = periods >= MIN_COMB_PERIODS
    return {"n_curves": len(curves), "n_points": int(len(t_all)),
            "comb_periods": round(periods, 2), "ln_range": round(float(np.log(t_all.max() /
             t_all.min())), 2), "range_sufficient": enough, "gain": round(gain, 4),
            "p_value": round(p, 4), "comb_detected": bool(p < P_THRESHOLD and enough),
            "omega": OMEGA}


# --------------------------------------------------------------------------- TFPT lambda-battery
def lambda_battery(curves: list[CoolingCurve], *, seed: int = 19) -> tuple[dict, float, int, str]:
    """The full TFPT log-period battery across all cooling episodes (the recovery-comb-domains
    quake/A5 look-elsewhere test): at every TFPT ratio lambda the phase-incoherent stacked comb gain
    at omega=2pi/ln(lambda) is ranked against its matched off-kernel pool, with a PER-lambda
    ln-range + Nyquist gate and a Bonferroni look-elsewhere correction over the gated lambdas.

    The single (3/2)^6 kernel (omega=2.583) is range-blind on these ~1.5-2.5-period curves, but the
    small-lambda entries (3/2, phi, 2, 3, ...) have larger omega (shorter log-period) and are
    well-sampled -- so this is the realistic multi-scale test. A small-lambda hit is LOW-specificity
    (dense among any scaling story); only an idiosyncratic-lambda survivor would be interesting."""
    pairs = [(c.t, c.y) for c in curves]
    battery: dict = {}
    for label, lam in BATTERY_LAMBDAS.items():
        res = _stacked_at(pairs, _omega(lam), seed=seed)
        battery[label] = {"lambda": round(lam, 4), "omega": round(_omega(lam), 3),
                          "idio": label in BATTERY_IDIO, **res}
    tested = [v for v in battery.values() if v["n_used"] > 0]
    min_p = min((v["p_value"] for v in tested), default=1.0)
    m_eff = max(1, len(tested))
    best = min(battery.items(), key=lambda kv: kv[1]["p_value"] if kv[1]["n_used"] else 1.0)
    return battery, round(min(1.0, min_p * m_eff), 4), m_eff, best[0]


# --------------------------------------------------------------------------- protected-floor test
def _exp_floor(t: np.ndarray, b: float, a: float, tau: float) -> np.ndarray:
    return b + a * np.exp(-t / tau)


def protected_floor(c: CoolingCurve) -> dict:
    """Test the TFPT PROTECTED FLOOR against the well-known "cooling curves need a constant offset"
    fact: fit kT_eff(t) = b + A exp(-t/tau) and report the floor b (core-equilibrium level) with its
    error. b>0 at high significance = the crust relaxes to a nonzero attractor, not to zero. This is
    the natural crust-cooling analogue of the TFPT protected floor w0 -- but it is GENERIC crust
    physics (shallow heating / core equilibrium), so it is a consistency check, NEVER TFPT-specific."""
    t, kt, err = c.t, c.kT, np.where(c.err > 0, c.err, 1.0)
    if len(t) < 4:
        return {"floor_eV": None, "reason": "too few points"}
    a0 = max(1.0, float(kt.max() - kt.min()))
    p0 = [float(kt.min()), a0, float(np.median(t))]
    bounds = ([0.0, 0.0, 1.0], [float(kt.max()), 10.0 * a0, 1.0e5])
    try:
        popt, pcov = curve_fit(_exp_floor, t, kt, p0=p0, sigma=err, absolute_sigma=True,
                               bounds=bounds, maxfev=20000)
    except (RuntimeError, ValueError):
        return {"floor_eV": None, "reason": "fit did not converge"}
    b, a, tau = (float(x) for x in popt)
    resid = (kt - _exp_floor(t, *popt)) / err
    dof = max(1, len(t) - 3)
    chi2_red = float(np.sum(resid ** 2) / dof)
    # inflate the formal error by sqrt(chi2_red) when the (single exp+floor) model fits imperfectly
    # -- the standard, honest way to avoid a spuriously precise floor significance.
    perr = np.sqrt(np.clip(np.diag(pcov), 0, None)) * max(1.0, chi2_red ** 0.5)
    b_err = float(perr[0])
    return {"floor_eV": round(b, 2), "floor_err_eV": round(b_err, 2),
            "floor_sigma": round(b / b_err, 1) if b_err > 0 else None,
            "amp_eV": round(a, 2), "tau_days": round(tau, 1),
            "chi2_red": round(chi2_red, 2),
            "floor_nonzero": bool(b_err > 0 and b > 3.0 * b_err)}


# --------------------------------------------------------------------------- injection on REAL grids
def _inject_curve(t: np.ndarray, eps: float, noise: float, rng: np.random.Generator, *,
                  phi: float = 0.0, kt0: float = 150.0, floor: float = 60.0,
                  tau: float = 300.0) -> np.ndarray:
    """Synthetic kT_eff(t) on a REAL epoch grid: exponential-to-floor cooling with a fractional
    log-periodic comb ripple at the kernel omega (eps) and multiplicative measurement noise."""
    smooth = floor + (kt0 - floor) * np.exp(-t / tau)
    kt = smooth * (1.0 + eps * np.cos(OMEGA * np.log(t) + phi))
    return kt * (1.0 + rng.normal(0.0, noise, len(t)))


def _stack_synthetic(grids: list[np.ndarray], eps: float, noise: float, rng: np.random.Generator,
                     *, aligned: bool) -> dict:
    curves = []
    for i, t in enumerate(grids):
        phi = 0.0 if aligned else rng.uniform(0.0, 2.0 * np.pi)
        kt = _inject_curve(t, eps, noise, rng, phi=phi)
        curves.append(CoolingCurve(f"inj{i}", f"inj{i}", np.asarray(t, float), kt,
                                   np.full(len(t), 1.0)))
    return superposed_epoch_stack(curves, seed=int(rng.integers(1_000_000)))


@dataclass
class InjectionResult:
    eps: float
    noise: float
    n_seeds: int
    aligned: float          # detect rate, phase-aligned comb injected (should rise with eps)
    misaligned: float       # detect rate, source-random phase (washes out -> ~false-alarm)
    label: str


def injection_recovery(grids: list[np.ndarray], *, eps_list=(0.02, 0.05, 0.15),
                       noise: float = 0.02, n_seeds: int = 40) -> tuple[list[InjectionResult], float]:
    """Injection-recovery on the REAL crust-cooling sampling (the actual epoch grids). Inject the
    kernel comb (aligned phase = the superposed-epoch test's assumption; and source-random phase =
    the washout control) and a comb-free null (eps=0), then measure the superposed-epoch detection
    rate. This quantifies the honest sensitivity floor: at the PREDICTED eps~2% the density-poor
    stack is expected to be underpowered (-> data_limited), while a strong comb must be recovered and
    the null must stay clean."""
    results = []
    for eps in eps_list:
        a = m = 0
        for s in range(n_seeds):
            rng = np.random.default_rng(7000 + s)
            a += int(_stack_synthetic(grids, eps, noise, rng, aligned=True)["comb_detected"])
            rng = np.random.default_rng(9000 + s)
            m += int(_stack_synthetic(grids, eps, noise, rng, aligned=False)["comb_detected"])
        results.append(InjectionResult(eps, noise, n_seeds, a / n_seeds, m / n_seeds,
                                       f"eps={eps:.0%}"))
    # comb-free null false-alarm rate (aligned machinery, no comb)
    fa = 0
    for s in range(n_seeds):
        rng = np.random.default_rng(11000 + s)
        fa += int(_stack_synthetic(grids, 0.0, noise, rng, aligned=True)["comb_detected"])
    return results, fa / n_seeds


# --------------------------------------------------------------------------- top-level driver
@dataclass
class CrustReport:
    curves: list[CoolingCurve]
    per_curve: list[dict]
    stack_incoherent: dict
    stack_superposed: dict
    battery: dict
    battery_global_p: float
    battery_m_eff: int
    battery_best: str
    floors: list[dict]
    injection: list[InjectionResult] = field(default_factory=list)
    injection_false_alarm: float = 1.0
