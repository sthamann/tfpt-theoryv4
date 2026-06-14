"""The TFPT FRB fingerprint score.

``problem_b.txt`` final section:

    Score = w_E*C_E + w_RM*C_RM + w_P*C_P + w_nu*C_nu + w_H*C_H

Each component lives in [0, 1].  Components without data (e.g. C_RM / C_P with a
catalogue that has no polarimetry) are dropped and the weights renormalised over
the *available* axes, so a missing axis never silently counts as a pass or a
fail.  The number of axes scoring > 0.5 is reported alongside the weighted score
(the "4-of-7 interesting / 6-of-7 paper-worthy" heuristic of the note).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

AxisStatus = Literal["support", "candidate", "null", "consistency", "data_limited"]


@dataclass
class EvidenceAxis:
    """One search-target axis with the bookkeeping needed to gate 'support'."""

    name: str
    score: float
    status: AxisStatus
    p_value: float | None = None
    q_value: float | None = None
    discriminating: bool = False     # can the test single out TFPT (vs e.g. Planck)?
    replicated: bool = False         # seen in >= 2 independent sources/channels?
    note: str = ""

    def qualifies_as_support(self, q_threshold: float = 0.01) -> bool:
        return (self.status == "support" and self.discriminating and self.replicated
                and self.q_value is not None and self.q_value < q_threshold)


def aggregate_axes(axes: list[EvidenceAxis], q_threshold: float = 0.01) -> dict:
    """Combine axes into an overall verdict.

    The overall verdict can only become 'confirmed' if at least one axis is a
    genuine, replicated, discriminating support with q < threshold. Otherwise it
    stays 'not_confirmed_not_refuted' (or 'refuted' if a kill-test axis fails).
    """
    buckets: dict[str, list[str]] = {
        "support_axes": [], "candidate_axes": [], "null_axes": [],
        "consistency_axes": [], "data_limited_axes": [],
    }
    for a in axes:
        if a.qualifies_as_support(q_threshold):
            buckets["support_axes"].append(a.name)
        elif a.status in ("candidate", "support"):
            # a 'support'-status axis that fails replication/q falls back to candidate
            buckets["candidate_axes"].append(a.name)
        elif a.status == "null":
            buckets["null_axes"].append(a.name)
        elif a.status == "consistency":
            buckets["consistency_axes"].append(a.name)
        else:
            buckets["data_limited_axes"].append(a.name)
    verdict = "confirmed" if buckets["support_axes"] else "not_confirmed_not_refuted"
    return {"verdict": verdict, **buckets}


@dataclass(frozen=True)
class FingerprintWeights:
    w_E: float = 0.35     # energy cascade -- the decisive, model-independent axis
    w_RM: float = 0.20    # RM staircase
    w_P: float = 0.15     # PA angle classes
    w_nu: float = 0.15    # frequency-drift quantisation
    w_H: float = 0.15     # host-galaxy anomaly

    def as_map(self) -> dict[str, float]:
        return {"C_E": self.w_E, "C_RM": self.w_RM, "C_P": self.w_P,
                "C_nu": self.w_nu, "C_H": self.w_H}


@dataclass
class Fingerprint:
    source: str
    components: dict[str, float | None]
    weights_used: dict[str, float]
    score: float
    axes_available: int
    axes_passed: int
    verdict: str
    notes: dict[str, str] = field(default_factory=dict)


def compute_fingerprint(source: str, components: dict[str, float | None],
                        weights: FingerprintWeights | None = None,
                        notes: dict[str, str] | None = None,
                        pass_threshold: float = 0.5) -> Fingerprint:
    w = (weights or FingerprintWeights()).as_map()
    available = {k: v for k, v in components.items() if v is not None}
    wsum = sum(w[k] for k in available) or 1.0
    used = {k: w[k] / wsum for k in available}
    score = sum(used[k] * available[k] for k in available)
    n_pass = sum(1 for v in available.values() if v >= pass_threshold)

    if score >= 0.6 and n_pass >= 3:
        verdict = "strong TFPT-like fingerprint (paper-worthy threshold)"
    elif score >= 0.4 or n_pass >= 2:
        verdict = "partial / interesting fingerprint"
    else:
        verdict = "no TFPT-specific fingerprint (consistent with standard models)"
    return Fingerprint(source, components, used, float(score),
                       len(available), n_pass, verdict, notes or {})
