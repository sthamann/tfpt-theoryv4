"""Multi-source replication for FRB.02 (echo ratios) and FRB.04 (RM spectrum).

The preregistration requires **>= 2 independent sources** for support. With the
Blinkverse multi-source DB plus the FAST catalogues we can now run the same
frozen tests across several repeaters and ask whether any theory-channel signal
*replicates*. A signal that appears in one source and vanishes in others is not
support; a clean multi-source null is a strong negative.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .data_io import RepeaterSeries
from .echo_ratio import evaluate_echo_semantic
from .markov_spectrum import markov_spectrum_test
from .rm_relaxation_step import rm_step_relaxation_test


@dataclass
class MultiSourceEcho:
    sources: list[str]
    per_source: dict = field(default_factory=dict)        # source -> summary
    replicated_targets: dict = field(default_factory=dict)  # "channel:target" -> [sources]
    replicated: bool = False
    verdict: str = ""


def multi_source_echo(series_list: list[RepeaterSeries], q_threshold: float = 0.01,
                      n_surrogate: int = 600, seed: int = 0) -> MultiSourceEcho:
    """Run the semantics-correct echo test on each source; a *theory-channel*
    target counts as replicated if it is significant (q<q_threshold) in >=2 sources."""
    per: dict = {}
    counts: dict = {}
    names: list[str] = []
    for s in series_list:
        if not s.available:
            continue
        r = evaluate_echo_semantic(s, q_threshold=q_threshold, n_surrogate=n_surrogate, seed=seed)
        if r.n_pairs < 20:
            continue
        names.append(r.source)
        theory_sig = []
        for cn, ch in r.channels.items():
            if not ch["audit"]:
                theory_sig.extend(f"{cn}:{t}" for t in ch["significant"])
        audit_sig = []
        for cn, ch in r.channels.items():
            if ch["audit"]:
                audit_sig.extend(ch["significant"])
        per[r.source] = {"n_bursts": r.n_bursts, "n_pairs": r.n_pairs,
                         "n_sessions": r.n_sessions, "raw_column": r.raw_column,
                         "theory_significant": theory_sig, "audit_significant": audit_sig}
        for key in theory_sig:
            counts.setdefault(key, []).append(r.source)
    replicated_targets = {k: v for k, v in counts.items() if len(v) >= 2}
    replicated = bool(replicated_targets)
    if replicated:
        verdict = f"REPLICATED theory-channel excess: {replicated_targets}"
    elif counts:
        verdict = (f"single-source theory excesses only (no replication): "
                   f"{ {k: v for k, v in counts.items()} }")
    else:
        verdict = (f"clean multi-source null across {len(names)} sources "
                   f"(no theory-channel kernel excess anywhere)")
    return MultiSourceEcho(names, per, replicated_targets, replicated, verdict)


@dataclass
class MultiSourceRM:
    sources: list[str]
    per_source: dict = field(default_factory=dict)
    v1_replicated: bool = False     # energy-kernel mu4 spectrum supported in >=2 sources
    v2_replicated: bool = False     # step-kernel proximity survives AR(1)-drift in >=2 sources
    verdict: str = ""


def multi_source_rm(series_list: list[RepeaterSeries], seed: int = 0) -> MultiSourceRM:
    """Run the RM Markov spectrum (v1 energy kernel) and the v2 step-relaxation
    test on each source with an RM time series; report replication."""
    per: dict = {}
    names: list[str] = []
    v1_ok, v2_ok = [], []
    for s in series_list:
        mk = markov_spectrum_test(s, channel="rm", seed=seed)
        if not mk.available:
            continue
        st = rm_step_relaxation_test(s, seed=seed)
        names.append(s.source)
        v1_pass = bool(mk.ci_contains_kernel and mk.null_p < 0.01)
        v2_pass = bool(st.ci_contains_kernel and st.null_p < 0.01)
        per[s.source] = {
            "n": mk.n,
            "v1_energy_eigs": mk.eigs, "v1_overall_null_p": mk.null_p,
            "v1_ci_contains_kernel": mk.ci_contains_kernel, "v1_pass": v1_pass,
            "v2_step_eigs": st.eigs, "v2_overall_null_p": st.null_p,
            "v2_ar1_drift_p": st.null_pvals.get("ar1_drift"),
            "v2_ci_contains_kernel": st.ci_contains_kernel, "v2_pass": v2_pass,
        }
        if v1_pass:
            v1_ok.append(s.source)
        if v2_pass:
            v2_ok.append(s.source)
    v1_rep, v2_rep = len(v1_ok) >= 2, len(v2_ok) >= 2
    verdict = (f"v1 mu4 spectrum: {'REPLICATED' if v1_rep else 'null'} "
               f"({len(v1_ok)}/{len(names)} sources); "
               f"v2 step-relaxation: {'REPLICATED' if v2_rep else 'not replicated'} "
               f"({len(v2_ok)}/{len(names)} survive the AR(1)-drift null)")
    return MultiSourceRM(names, per, v1_rep, v2_rep, verdict)
