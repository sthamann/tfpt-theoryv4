"""FRB.06 (NEW, exploratory) -- polarisation-degree quantisation.

The kernel fractions {2/3, 1/3, 8/27, 1/27} live exactly in [0,1] -- the range
of a polarisation *degree*. If the seam boundary pinned discrete polarisation
states (mu4/D4 marks), the linear (L/I) or |circular| (|V|/I) fraction might pile
up at a kernel fraction.

Trap (the reason this was easy to overlook AND easy to get wrong): |V|/I is small
for almost all bursts, so a naive "fraction near 1/27" count is ~50% -- a trivial
consequence of low circular polarisation, not a signature. The test therefore
calibrates against a **smooth Beta null** fitted to the same fraction
distribution (method of moments): a real spike at a kernel value must exceed what
that smooth distribution already produces.

Firewall: L/I is propagation-affected (depolarisation), so this is a search
target, not a TFPT-clean channel.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .data_io import RepeaterSeries
from .recovery_kernel import ONE_THIRD, SQRT_LAMBDA2, SQRT_LAMBDA3, TWO_THIRDS

FRACTION_TARGETS = {"2/3": TWO_THIRDS, "1/3": ONE_THIRD, "8/27": SQRT_LAMBDA2, "1/27": SQRT_LAMBDA3}


def _beta_sample(x: np.ndarray, n: int, size: int, rng) -> np.ndarray:
    """Smooth unimodal Beta null matched to the data mean/variance (MoM)."""
    m = float(np.clip(np.mean(x), 1e-3, 1 - 1e-3))
    v = float(max(np.var(x), 1e-6))
    c = m * (1 - m) / v - 1.0
    if c <= 0:
        c = 1.0
    a, b = max(m * c, 0.05), max((1 - m) * c, 0.05)
    return rng.beta(a, b, size=(size, n))


def _enrichment_at(x, null, tv, hw):
    obs = float(np.mean(np.abs(x - tv) <= hw))
    null_frac = (np.abs(null - tv) <= hw).mean(axis=1)
    p = float((1 + np.sum(null_frac >= obs)) / (len(null_frac) + 1))
    enr = obs / (float(null_frac.mean()) or 1e-9)
    return obs, enr, p


@dataclass
class PolFractionResult:
    source: str
    available: bool
    quantities: dict = field(default_factory=dict)
    significant: list = field(default_factory=list)
    verdict: str = ""


def pol_fraction_test(series: RepeaterSeries, half_window: float = 0.03,
                      n_surrogate: int = 1000, seed: int = 0) -> PolFractionResult:
    """A kernel fraction counts as a hit only if (a) p<0.05 under the Beta null
    AND (b) its enrichment exceeds the 90th percentile of a grid of *control*
    (non-kernel) fractions tested identically -- so a thin-tailed null misfit,
    which inflates the enrichment at *every* high fraction, cannot fake a signal."""
    if not series.available or series.linear_frac.size == 0:
        return PolFractionResult(series.source, False, verdict="data-limited: no polarisation fractions")
    rng = np.random.default_rng(seed)
    quants = {"L/I": series.linear_frac / 100.0, "|V|/I": np.abs(series.circular_frac) / 100.0}
    controls = [c for c in np.round(np.linspace(0.08, 0.92, 22), 3)
                if all(abs(c - t) > 2 * half_window for t in FRACTION_TARGETS.values())]
    out: dict = {}
    sig: list = []
    for qname, q in quants.items():
        x = np.clip(q[np.isfinite(q) & (q >= 0.0) & (q <= 1.2)], 0.0, 1.0)
        if len(x) < 50:
            continue
        null = _beta_sample(x, len(x), n_surrogate, rng)
        ctrl_enr = np.array([_enrichment_at(x, null, c, half_window)[1] for c in controls])
        ctrl_bar = float(np.percentile(ctrl_enr, 90))
        per = {"_control_enrichment_p90": round(ctrl_bar, 2)}
        for tname, tv in FRACTION_TARGETS.items():
            obs, enr, p = _enrichment_at(x, null, tv, half_window)
            stands_out = enr > ctrl_bar
            per[tname] = {"obs_frac": round(obs, 4), "enrichment": round(enr, 2),
                          "p": round(p, 4), "exceeds_controls": stands_out}
            if p < 0.05 and enr > 1.2 and stands_out:
                sig.append(f"{qname}:{tname}")
        out[qname] = per
    verdict = (f"excess (beyond controls) at {sig}" if sig
               else "no kernel fraction stands out above arbitrary control fractions (null)")
    return PolFractionResult(series.source, True, out, sig, verdict)
