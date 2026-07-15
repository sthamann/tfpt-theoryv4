"""frb-parity-comb analysis CLI (PC.01-PC.03 + injection calibration).

Run:  cd experiments/frb-parity-comb && PYTHONPATH=src python -m tfpt_pc.cli analyze --seed 0
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from . import constants as C
from .data import (even_channel_sessions, load_li2021, load_pol_v5,
                   load_zhang2023, odd_channel_sessions)
from .signed_comb import (InjectionResult, N_SIGN_PERM, even_session_test,
                          fisher, inject_odd, odd_session_test)

RESULTS = Path(__file__).resolve().parents[2] / "results" / "results.json"


def analyze(seed: int = 0) -> dict:
    out: dict = {"experiment": "frb-parity-comb v1 (PC.01-PC.03)",
                 "frozen": C.summary(),
                 "firewall": ("boundary-recovery search target; deck/Z2 reading "
                              "of signed circular polarization (coupling "
                              "unforced); a null is a valid outcome; nothing "
                              "load-bearing")}
    b = load_pol_v5()
    odd = odd_channel_sessions(b)
    n_sig = sum(len(u) for u, _ in odd)
    out["primary_dataset"] = {
        "id": "FRB20240114A pol v5", "n_bursts_total": int(len(b.mjd)),
        "n_significant_handedness_in_sessions": int(n_sig),
        "n_sessions_with_signs": len(odd),
        "session_sizes": [len(u) for u, _ in odd],
        "session_reach_periods_omega1": [round((u.max() - u.min())
                                               * C.OMEGA_1 / 6.2832, 2)
                                         for u, _ in odd],
    }

    # ---- PC.01: omega_1 FORBIDDEN in the odd channel --------------------------
    pc01_sessions = []
    ps = []
    for i, (u, s) in enumerate(odd):
        r = odd_session_test(u, s, C.OMEGA_1, seed=seed + i)
        pc01_sessions.append({"session": i, **asdict(r)})
        if r.gate != "fail":
            ps.append(r.p_sign_perm)
    p_fisher = fisher(ps, 1 / (N_SIGN_PERM + 1)) if ps else float("nan")
    pc01_verdict = ("NULL (selection rule holds: no omega_1 signed power)"
                    if (not ps or p_fisher >= 0.01)
                    else "OMEGA_1 ODD-POWER EXCESS -> escalate-only")
    out["PC01_selection_rule_omega1_odd"] = {
        "gated_sessions": len(ps), "per_session": pc01_sessions,
        "fisher_p": None if not ps else round(p_fisher, 4),
        "prediction": "NULL (v486 parity assignment)", "verdict": pc01_verdict}

    # ---- PC.02: omega_2 comb in the odd channel -------------------------------
    pc02_sessions = []
    ps2, gates2 = [], []
    for i, (u, s) in enumerate(odd):
        r = odd_session_test(u, s, C.OMEGA_2, seed=seed + 100 + i,
                             relaxed_ok=True)
        pc02_sessions.append({"session": i, **asdict(r)})
        if r.gate != "fail":
            ps2.append(r.p_sign_perm)
            gates2.append(r.gate)
    p2_fisher = fisher(ps2, 1 / (N_SIGN_PERM + 1)) if ps2 else float("nan")
    if not ps2:
        pc02_verdict = ("data_limited (no session passes even the relaxed "
                        "omega_2 reach gate -- the odd-channel clock needs "
                        "~18.5 e-folds of ln tau at the primary gate)")
    elif p2_fisher < 0.01 and all(g == "primary" for g in gates2):
        pc02_verdict = "OMEGA_2 ODD-CHANNEL CANDIDATE -> escalate-only"
    else:
        pc02_verdict = (f"null-at-current-reach (gates: {gates2}; Fisher "
                        f"p={p2_fisher:.3f}); stays data_limited per the S-b "
                        "amplitude budget (comb-2 fades x64 per period)")
    out["PC02_omega2_odd_channel"] = {
        "gated_sessions": len(ps2), "gates": gates2,
        "per_session": pc02_sessions,
        "fisher_p": None if not ps2 else round(p2_fisher, 4),
        "verdict": pc02_verdict}

    # ---- PC.03: omega_2 must not be an even-channel line ----------------------
    pc03 = {}
    for src, loader in (("FRB20240114A", None), ("FRB20220912A", load_zhang2023),
                        ("FRB20121102A", load_li2021)):
        bb = b if loader is None else loader()
        rows = []
        for u in even_channel_sessions(bb):
            r = even_session_test(u, C.OMEGA_2, seed=seed)
            if r["gate"] != "fail":
                rows.append(r)
        pc03[src] = {"gated_sessions": len(rows), "sessions": rows,
                     "fisher_p": (round(fisher([r["p_surrogate"] for r in rows],
                                               1 / (C.N_SURROGATE + 1)), 4)
                                  if rows else None)}
    even_ps = [v["fisher_p"] for v in pc03.values() if v["fisher_p"] is not None]
    pc03_verdict = ("NULL in the even channel (consistent with the frozen "
                    "new-tone scan nulls)" if all(p >= 0.01 for p in even_ps)
                    else "even-channel omega_2 line -> would CONTRADICT the "
                         "parity assignment (escalate)") if even_ps else \
                   "data_limited (no gated even-channel session at omega_2)"
    out["PC03_omega2_even_channel"] = {**pc03, "verdict": pc03_verdict}

    # ---- injection calibration (odd channel) ----------------------------------
    inj1 = inject_odd(odd, C.OMEGA_1, seed=seed + 1)
    inj2 = inject_odd(odd, C.OMEGA_2, seed=seed + 2)
    out["injection_odd"] = {
        "omega_1": asdict(inj1), "omega_2": asdict(inj2),
        "s_b_budget_note": ("v486 S-b: comb-2/comb-1 tooth amplitude = 2^-6 "
                            "per period; smallest detectable eps above "
                            "defines the honest reach")}

    def _reach(inj: InjectionResult, thresh: float = 0.8) -> str:
        for e, r in zip(inj.eps_grid, inj.detection_rate):
            if r >= thresh:
                return f"powered (>={int(100 * thresh)}%) from eps ~ {e}"
        return "not powered on this dataset at eps <= 0.5"
    out["PC01_selection_rule_omega1_odd"]["power_note"] = _reach(inj1)
    out["PC02_omega2_odd_channel"]["power_note"] = _reach(inj2)
    return out


IXPE_RESULTS = RESULTS.parent / "results_ixpe.json"


def analyze_ixpe(seed: int = 0) -> dict:
    from . import ixpe

    out: dict = {"experiment": "frb-parity-comb v1.1 -- IXPE leg (IX.01-03)",
                 "dataset": "IXPE 03250499, 1E 1841-045 post-outburst ToO "
                            "(2024-09-28..10-10; outburst epoch ~MJD 60542)",
                 "semantics": ("IXPE is LINEAR-only -> EVEN sector only; the "
                               "Z2-odd handedness channel does not exist in "
                               "X-rays (recorded in the v1.1 addendum BEFORE "
                               "the data pass)"),
                 "firewall": ("magnetar bursts = surface channel (A5 class); "
                              "a hit is a universal-DSI candidate, never "
                              "direct TFPT confirmation; nothing load-bearing")}
    t = ixpe.load_events()
    span = float(t[-1] - t[0])
    out["photons_2_8_keV"] = int(len(t))
    out["span_s"] = round(span, 1)
    # envelope anchor honesty (recorded, not tested)
    import math
    ln_reach_env = math.log((t[-1] - t[0] + 39 * 86400) / (39 * 86400))
    out["envelope_anchor"] = {
        "t_minus_outburst_d": [39.0, 51.2],
        "ln_reach": round(ln_reach_env, 3),
        "omega1_periods": round(ln_reach_env * C.OMEGA_1 / (2 * math.pi), 3),
        "verdict": "data_limited by construction (recorded, not tested)"}

    bursts = ixpe.find_bursts(t)
    out["bursts_found"] = [{"t_peak_met": round(b.t_peak, 3),
                            "counts_0p1s": b.counts_peak,
                            "local_mean": round(b.local_rate, 3),
                            "tail_p": b.tail_p} for b in bursts]
    sessions = ixpe.burst_sessions(t, bursts)
    out["n_burst_sessions"] = len(sessions)
    out["session_stats"] = [{"n_photons": len(u),
                             "reach_omega1": round(float(u.max() - u.min()) * C.OMEGA_1 / (2 * math.pi), 2),
                             "reach_omega2": round(float(u.max() - u.min()) * C.OMEGA_2 / (2 * math.pi), 2)}
                            for u in sessions]

    for name, omega, role in (("IX01_omega2_forbidden", C.OMEGA_2, "forbidden"),
                              ("IX02_omega1_allowed", C.OMEGA_1, "allowed")):
        rows, ps, gates = [], [], []
        for i, u in enumerate(sessions):
            r = ixpe.even_comb_test(u, omega, seed=seed + i)
            rows.append(r)
            if r["gate"] != "fail":
                ps.append(r["p_surrogate"])
                gates.append(r["gate"])
        pf = fisher(ps, 1 / (C.N_SURROGATE + 1)) if ps else float("nan")
        if not ps:
            verdict = "data_limited (no gate-passing burst session)"
        elif role == "forbidden":
            verdict = ("EVEN-CHANNEL OMEGA_2 LINE -> contradicts the v486 "
                       "parity assignment (escalate-only)"
                       if pf < 0.01 else
                       f"NULL (forbidden line absent; Fisher p={pf:.3f})")
        else:
            verdict = ("omega_1 comb candidate -> escalate-only" if pf < 0.01
                       else f"null-at-current-power (Fisher p={pf:.3f})")
        out[name] = {"gated_sessions": len(ps), "gates": gates,
                     "sessions": rows,
                     "fisher_p": None if not ps else round(pf, 4),
                     "verdict": verdict}

    out["IX03_injection"] = {
        "omega_1": ixpe.inject_even(sessions, C.OMEGA_1, seed=seed + 7),
        "omega_2": ixpe.inject_even(sessions, C.OMEGA_2, seed=seed + 8),
        "note": "thinning injection on real photon times; compare eps_base = 0.0173"}
    return out


NICER_RESULTS = RESULTS.parent / "results_nicer.json"


def analyze_nicer(seed: int = 0) -> dict:
    import math

    import numpy as np

    from . import nicer

    out: dict = {"experiment": "frb-parity-comb v1.2 -- NICER burst-storm "
                               "leg (NI.01-03)",
                 "dataset": "NICER 3020560101, SGR 1935+2154 (2020-04-28 "
                            "storm; Younes+2020 ApJL 904 L21)",
                 "semantics": ("arrival-time combs = Z2-EVEN sector only "
                               "(prereg v1.2 BEFORE the data pass)"),
                 "firewall": ("magnetar bursts = surface channel (A5 "
                              "class); a hit is a universal-DSI candidate, "
                              "never direct TFPT confirmation; nothing "
                              "load-bearing")}
    t, gti, choice = nicer.load_chosen()
    out["file_choice"] = choice
    out["photons_1_10_keV"] = int(len(t))
    out["gti_total_s"] = round(float(np.sum(gti[:, 1] - gti[:, 0])), 1)

    bursts = nicer.find_bursts(t)
    out["n_bursts"] = len(bursts)
    cls = nicer.clusters(bursts)
    out["clusters"] = [{"n_bursts": len(c),
                        "span_s": round(c[-1].t_peak - c[0].t_peak, 1)}
                       for c in cls]

    fam_a = nicer.storm_sessions(bursts)
    fam_b = nicer.photon_sessions(t, bursts)
    out["family_A_sessions"] = [
        {"n_bursts": len(u) + 1,
         "ln_reach": round(float(u.max() - u.min()), 2),
         "reach_omega1": round(float(u.max() - u.min()) * C.OMEGA_1
                               / (2 * math.pi), 2),
         "reach_omega2": round(float(u.max() - u.min()) * C.OMEGA_2
                               / (2 * math.pi), 2)} for u in fam_a]
    out["family_B_sessions"] = [
        {"n_photons": len(u),
         "reach_omega1": round(float(u.max() - u.min()) * C.OMEGA_1
                               / (2 * math.pi), 2)} for u in fam_b]

    for name, omega, role in (("NI01_omega2_forbidden", C.OMEGA_2,
                               "forbidden"),
                              ("NI02_omega1_allowed", C.OMEGA_1, "allowed")):
        rows, ps, gates = [], [], []
        for i, u in enumerate(fam_a):
            r = nicer.even_comb_test(u, omega, min_n=nicer.MIN_BURSTS_A - 1,
                                     seed=seed + i)
            rows.append({"family": "A", **r})
            if r["gate"] != "fail":
                ps.append(r["p_surrogate"])
                gates.append(f"A:{r['gate']}")
        for i, u in enumerate(fam_b):
            r = nicer.even_comb_test(u, omega, min_n=nicer.MIN_PHOTONS_B,
                                     seed=seed + 50 + i)
            rows.append({"family": "B", **r})
            if r["gate"] != "fail":
                ps.append(r["p_surrogate"])
                gates.append(f"B:{r['gate']}")
        pf = fisher(ps, 1 / (C.N_SURROGATE + 1)) if ps else float("nan")
        if not ps:
            verdict = "data_limited (no gate-passing session)"
        elif role == "forbidden":
            verdict = ("EVEN-CHANNEL OMEGA_2 LINE -> contradicts the v486 "
                       "parity assignment (escalate-only)"
                       if pf < 0.01 and len(ps) >= 2 else
                       f"NULL (forbidden line absent; Fisher p={pf:.3f}; "
                       f"gates {gates})")
        else:
            verdict = ("omega_1 comb candidate -> escalate-only"
                       if pf < 0.01 else
                       f"null-at-current-power (Fisher p={pf:.3f}; gates "
                       f"{gates})")
        out[name] = {"gated_sessions": len(ps), "gates": gates,
                     "sessions": rows,
                     "fisher_p": None if not ps else round(pf, 4),
                     "verdict": verdict}

    out["NI03_injection"] = {
        "family_A_omega1": nicer.inject_thinning(
            fam_a, C.OMEGA_1, min_n=nicer.MIN_BURSTS_A - 1, seed=seed + 7),
        "family_A_omega2": nicer.inject_thinning(
            fam_a, C.OMEGA_2, min_n=nicer.MIN_BURSTS_A - 1, seed=seed + 8),
        "family_B_omega1": nicer.inject_thinning(
            fam_b, C.OMEGA_1, min_n=nicer.MIN_PHOTONS_B, seed=seed + 9),
        "note": ("comb-modulated thinning on the real times; compare "
                 "eps_base = 0.0173 and the S-b budget at the recorded "
                 "ln-reach")}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("analyze")
    a.add_argument("--seed", type=int, default=0)
    b = sub.add_parser("analyze-ixpe")
    b.add_argument("--seed", type=int, default=0)
    c = sub.add_parser("analyze-nicer")
    c.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    if args.cmd == "analyze":
        out = analyze(seed=args.seed)
        RESULTS.parent.mkdir(exist_ok=True)
        RESULTS.write_text(json.dumps(out, indent=2) + "\n")
        print(json.dumps({k: (v if not isinstance(v, dict) else
                              {kk: vv for kk, vv in v.items()
                               if kk not in ("per_session", "sessions")})
                          for k, v in out.items()}, indent=2))
        print(f"\nresults -> {RESULTS}")
    elif args.cmd == "analyze-ixpe":
        out = analyze_ixpe(seed=args.seed)
        IXPE_RESULTS.parent.mkdir(exist_ok=True)
        IXPE_RESULTS.write_text(json.dumps(out, indent=2) + "\n")
        print(json.dumps({k: (v if not isinstance(v, dict) else
                              {kk: vv for kk, vv in v.items()
                               if kk not in ("sessions", "bursts_found",
                                             "session_stats")})
                          for k, v in out.items()}, indent=2))
        print(f"\nresults -> {IXPE_RESULTS}")
    elif args.cmd == "analyze-nicer":
        out = analyze_nicer(seed=args.seed)
        NICER_RESULTS.parent.mkdir(exist_ok=True)
        NICER_RESULTS.write_text(json.dumps(out, indent=2) + "\n")
        print(json.dumps({k: (v if not isinstance(v, dict) else
                              {kk: vv for kk, vv in v.items()
                               if kk != "sessions"})
                          for k, v in out.items()}, indent=2))
        print(f"\nresults -> {NICER_RESULTS}")


if __name__ == "__main__":
    main()
