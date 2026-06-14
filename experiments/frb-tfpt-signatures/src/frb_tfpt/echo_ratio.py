"""FRB.02 -- recovery / echo fluence-ratio test.

If clustered afterbursts are boundary echoes of one discharge, the cleanest
prediction is that consecutive-burst ratios pile up at a recovery eigenvalue:

    E_{n+1}/E_n ~ lambda2 = 64/729   (energy)   or
    A_{n+1}/A_n ~ sqrt(lambda2) = 8/27 (field amplitude),

and possibly at the sub-burst step 2/3.  We compute consecutive-burst fluence
ratios for a time-ordered, clustered burst train and test for an excess of
log-ratios near each kernel ratio, calibrated by time-shuffled surrogates
(which destroy any real ordering while preserving the fluence distribution).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .data_io import RepeaterSeries
from .recovery_kernel import KernelRatio, kernel_ratios


def _bh_qvalues(pvals: list[float]) -> list[float]:
    """Benjamini-Hochberg FDR q-values for a list of p-values."""
    p = np.asarray(pvals, float)
    n = len(p)
    order = np.argsort(p)
    q = np.empty(n)
    prev = 1.0
    for rank in range(n - 1, -1, -1):
        i = order[rank]
        prev = min(prev, p[i] * n / (rank + 1))
        q[i] = prev
    return q.tolist()


@dataclass
class RatioTargetHit:
    name: str
    target: float
    log_target: float
    n_near: int
    enrichment: float           # observed near-count / mean surrogate near-count
    p_value: float              # surrogate-calibrated


@dataclass
class EchoResult:
    source: str
    n_pairs: int
    hits: list[RatioTargetHit] = field(default_factory=list)
    c_echo: float = 0.0
    note: str = ""


def _consecutive_log_ratios(fluence: np.ndarray, mjd: np.ndarray,
                            cluster_dt_days: float | None) -> np.ndarray:
    order = np.argsort(mjd)
    f, t = fluence[order], mjd[order]
    ok = np.isfinite(f) & (f > 0) & np.isfinite(t)
    f, t = f[ok], t[ok]
    lr = np.log10(f[1:] / f[:-1])
    dt = np.diff(t)
    if cluster_dt_days is not None:
        lr = lr[dt <= cluster_dt_days]
    return lr


def echo_ratio_test(source: str, fluence: np.ndarray, mjd: np.ndarray,
                    cluster_dt_days: float | None = None, half_window_dex: float = 0.1,
                    targets: list[KernelRatio] | None = None,
                    n_surrogate: int = 2000, seed: int = 0) -> EchoResult:
    lr = _consecutive_log_ratios(fluence, mjd, cluster_dt_days)
    n = len(lr)
    if n < 10:
        return EchoResult(source, n, [], 0.0, "too few consecutive pairs")

    targets = targets or kernel_ratios()
    # surrogates: shuffle fluences, recompute consecutive log-ratios
    rng = np.random.default_rng(seed)
    f = fluence[np.isfinite(fluence) & (fluence > 0)]
    logf = np.log10(f)
    surr_lrs = []
    for _ in range(n_surrogate):
        s = rng.permutation(logf)
        surr_lrs.append(np.diff(s)[:n])
    surr = np.array(surr_lrs)

    hits, best = [], 0.0
    for t in targets:
        # test both the ratio and its inverse (decay direction is arbitrary)
        for sign, lt in ((+1, np.log10(t.value)), (-1, -np.log10(t.value))):
            obs = int(np.sum(np.abs(lr - lt) <= half_window_dex))
            null = np.sum(np.abs(surr - lt) <= half_window_dex, axis=1)
            mean_null = float(null.mean()) or 1e-9
            p = float((1 + np.sum(null >= obs)) / (n_surrogate + 1))
            enr = obs / mean_null
            hits.append(RatioTargetHit(
                f"{t.name}{'^-1' if sign < 0 else ''}", t.value if sign > 0 else 1 / t.value,
                lt, obs, enr, p))
            if p < 0.05 and enr > 1:
                best = max(best, 1.0 - p / 0.05)
    return EchoResult(source, n, hits, float(np.clip(best, 0, 1)),
                      f"{n} consecutive pairs; best surrogate-calibrated excess scored")


@dataclass
class SessionEchoResult:
    source: str
    n_bursts: int
    n_pairs: int
    n_sessions: int
    targets: dict                  # name -> {ratio, enrichment, p, q}
    c_echo: float
    verdict: str


def evaluate_echo_ratios_by_session(series: RepeaterSeries, half_window_dex: float = 0.10,
                                    n_surrogate: int = 2000, seed: int = 0,
                                    q_threshold: float = 0.05) -> SessionEchoResult:
    """Session-aware consecutive energy/fluence-ratio test with BH q-values.

    Consecutive log-ratios are taken *within* each observing session (so a gap
    between sessions never creates a spurious pair). Energy is used when present,
    else fluence. Surrogates shuffle within each session (preserving the session
    energy distribution and the session structure).
    """
    if not series.available:
        return SessionEchoResult(series.source, 0, 0, 0, {}, 0.0, "data-limited")
    val = series.energy if np.isfinite(series.energy).sum() else series.fluence
    sess = series.session_id if series.session_id.size else np.zeros(len(series.mjd))
    mjd = series.mjd

    def session_logratios(values: np.ndarray) -> np.ndarray:
        out = []
        for s in np.unique(sess):
            m = (sess == s)
            v, t = values[m], mjd[m]
            ok = np.isfinite(v) & (v > 0) & np.isfinite(t)
            v, t = v[ok], t[ok]
            if len(v) < 2:
                continue
            order = np.argsort(t)
            v = v[order]
            out.append(np.log10(v[1:] / v[:-1]))
        return np.concatenate(out) if out else np.array([])

    lr = session_logratios(val)
    n_pairs = len(lr)
    n_sessions = int(len(np.unique(sess)))
    if n_pairs < 20:
        return SessionEchoResult(series.source, len(val), n_pairs, n_sessions, {}, 0.0,
                                 f"too few within-session pairs ({n_pairs})")

    rng = np.random.default_rng(seed)
    # surrogates: shuffle values within each session, recompute within-session ratios
    surr = []
    for _ in range(n_surrogate):
        v2 = val.copy()
        for s in np.unique(sess):
            m = np.where(sess == s)[0]
            v2[m] = rng.permutation(val[m])
        surr.append(session_logratios(v2))

    targets, names, pvals = {}, [], []
    for t in kernel_ratios():
        for sign, lt, label in ((+1, np.log10(t.value), t.name),
                                (-1, -np.log10(t.value), f"{t.name}^-1")):
            obs = int(np.sum(np.abs(lr - lt) <= half_window_dex))
            null = np.array([np.sum(np.abs(s - lt) <= half_window_dex) for s in surr])
            mean_null = float(null.mean()) or 1e-9
            p = float((1 + np.sum(null >= obs)) / (n_surrogate + 1))
            targets[label] = {"ratio": t.value if sign > 0 else 1.0 / t.value,
                              "enrichment": obs / mean_null, "p": p}
            names.append(label); pvals.append(p)
    for label, q in zip(names, _bh_qvalues(pvals)):
        targets[label]["q"] = q

    sig = [n for n in names if targets[n]["q"] < q_threshold and targets[n]["enrichment"] > 1.2]
    c = float(np.clip(max((1 - targets[n]["q"] / q_threshold) for n in sig), 0, 1)) if sig else 0.0
    verdict = (f"support: {sig}" if sig else "clean null (no q<%.2f kernel-ratio excess)" % q_threshold)
    return SessionEchoResult(series.source, len(val), n_pairs, n_sessions, targets, c, verdict)
