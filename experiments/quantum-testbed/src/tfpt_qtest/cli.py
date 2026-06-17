"""``tfpt-qtest`` -- TFPT quantum testbed: entanglement spectrum + quench DSI + OTOC.

Internal-consistency (no external data): build the frozen kernel as a quantum object
and check the predicted patterns -- the entanglement-spectrum face of the recovery
channel (QT.01), and the *dynamical* discrete-scale-invariance signature in quench
recovery (QT.02) plus a free-fermion OTOC (QT.03).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import constants
from .clock import BEND as BEND_RATIO
from .clock import clock_identities, matched_filter_discriminate
from .entanglement import entanglement_spectrum
from .mtc import mtc_signatures
from .quench import freefermion_otoc, nongeometric_control, recovery_dsi_scan

RESULTS = Path(__file__).resolve().parents[2] / "results"


def _audit() -> int:
    print("=" * 74)
    print("TFPT quantum testbed -- frozen kernel + DSI ladder ratios")
    print("=" * 74)
    for k, v in constants.summary().items():
        print(f"  {k:24s} = {v:.6g}")
    print("\n  DSI ladder ratios (omega = 2pi/ln lambda; amplitude ~ exp(-pi*omega/2)):")
    from .dsi import amplitude_suppression, log_frequency
    for name, lam in constants.ladder_ratios().items():
        print(f"    {name:28s} lambda={lam:8.3f}  omega={log_frequency(lam):6.3f}  "
              f"amp~{amplitude_suppression(lam):.2e}")
    return 0


def _analyze(seed: int) -> int:
    print("=" * 74)
    print("QT -- TFPT quantum testbed (entanglement spectrum + quench DSI + OTOC)")
    print("=" * 74)

    print("\n[QT.01] entanglement spectrum of the second-quantised kernel")
    ent = entanglement_spectrum()
    print(f"    occupation (zeta) = {tuple(round(z, 6) for z in ent.occupation)}")
    print(f"    surprisals -ln(zeta) = {[round(s, 4) for s in ent.surprisals]} "
          f"(= 6 ln(3/2)=Delta, 6 ln 3)  [exact]")
    print(f"    modular energies ln((1-z)/z) = {[round(e, 4) for e in ent.modular_energies]} "
          f"(derived, + small 1-zeta shift)")
    print(f"    s_3/s_2 = {ent.s_ratio:.4f} (= ln3/ln(3/2), the FRB.09 clock ratio)")
    print(f"    protected zeta=1 mode (zero surprisal): {ent.protected_present}; "
          f"recovery I_n = {{1:{ent.recovery_I[1]:.3e}, 2:{ent.recovery_I[2]:.2e}}}")
    print(f"    -> {ent.verdict}")

    print("\n[QT.02] quench recovery -- discrete scale invariance + suppression law")
    scan = recovery_dsi_scan(constants.ladder_ratios(), seed=seed)
    print(f"    {'ladder ratio':28s} {'omega':>6s} {'amp~e^-piw/2':>12s} "
          f"{'fit amp':>8s} {'p':>6s}  DSI?")
    for r in scan:
        print(f"    {r.name:28s} {r.omega:6.3f} {r.suppression:12.2e} "
              f"{r.amplitude:8.4f} {r.p_value:6.3f}  {'YES' if r.detected else 'no'}")
    gap_lam = constants.ladder_ratios()["(3/2)^6 (energy gap)"]
    ctrl = nongeometric_control(gap_lam, seed=seed)
    print(f"    control (linear-rate ladder @ omega((3/2)^6)): amp={ctrl.amplitude:.4f} "
          f"p={ctrl.p_value:.3f} detected={ctrl.detected} (expect False)")

    print("\n[QT.03] free-fermion OTOC (kernel-ladder H, squared commutator)")
    otoc = freefermion_otoc(gap_lam, seed=seed)
    print(f"    ballistic front speed = {otoc.front_speed:.3f} sites/t; "
          f"on-site return DSI p={otoc.return_dsi_p:.3f} (detected={otoc.return_dsi_detected})")

    print("\n[QT.04] EXACT walled clock (v124/v126/v147) + recovery-waveform signature")
    clk = clock_identities()
    print(f"    rates {{0, {clk.rates[1]:.4f}=6ln(3/2), {clk.rates[2]:.4f}=6ln3}}; "
          f"bend {clk.bend:.4f}=ln3/ln(3/2); sheet slope {clk.sheet_slope:.0f}=|Z2|; "
          f"wall@n=3={clk.wall_at_nfam}")
    print(f"    -> {clk.verdict}")
    mf_k = matched_filter_discriminate(BEND_RATIO, seed=seed)        # kernel recovery
    mf_n = matched_filter_discriminate(5.0, seed=seed)               # non-kernel recovery
    print("    matched filter (fixed-ratio 2.7095 template vs free 2-exp):")
    print(f"      kernel curve (ratio 2.71): free ratio recovered {mf_k.free_ratio_recovered:.3f} "
          f"-> kernel recovery={mf_k.is_kernel_recovery} (expect True)")
    print(f"      non-kernel curve (ratio 5.0): free ratio recovered {mf_n.free_ratio_recovered:.3f} "
          f"-> kernel recovery={mf_n.is_kernel_recovery} (expect False)")

    print("\n[QT.05] particle/statistics layer: the carrier anyon MTC (v241/242/243)")
    mtc = mtc_signatures()
    print(f"    {mtc.n_sectors} sectors -> {mtc.n_bosons} bosons / {mtc.n_fermions} fermions "
          f"(theta=-1, phase pi = m=2) / {mtc.n_anyons} anyons")
    print(f"    statistical phase quanta: spin = pi/4 ({mtc.spin_phase_quantum:.4f}, 8th roots), "
          f"braiding = pi/2 ({mtc.braid_phase_quantum:.4f})")
    print(f"    distinct spin phases (rad): {[round(p, 3) for p in mtc.distinct_spin_phases]}")
    print(f"    Gauss-Milgram c = {mtc.central_charge:.0f} (=g_car+N_fam); integrable S="
          f"{mtc.integrable}; trivial on (E8)_1={mtc.trivial_on_E8}")
    print(f"    -> {mtc.verdict}")

    gap_row = next(r for r in scan if "(3/2)^6" in r.name)
    fine_row = next(r for r in scan if r.name.startswith("3/2"))
    verdict = (
        "the frozen kernel is carried by the QUANTUM dynamics, as a *dynamical* "
        "signature, not a static ratio: (QT.01) the entanglement spectrum reproduces "
        "the kernel exactly (surprisals 6 ln(3/2), 6 ln3; protected DFS mode; "
        "I_n=(2/3)^{6n}); (QT.02) a geometric ladder relaxes log-periodically at "
        f"omega=2pi/ln lambda with exp(-pi^2/ln lambda)-suppressed amplitude (detectable "
        f"only for the coarse (3/2)^6, p={gap_row.p_value:.3f}; invisible for 3/2, "
        f"p={fine_row.p_value:.3f}); (QT.04) but the EXACT clock (v124) is WALLED -- a "
        "single recovery is two modes + a protected floor with the det'-clean bend "
        f"rate ratio {BEND_RATIO:.4f}=ln3/ln(3/2) and NO third mode (pole at n=3), so "
        "sustained DSI needs a cascade. The sharp, falsifiable waveform signature is "
        "therefore: a fixed-ratio (2.7095) two-exponential recovery template with a "
        "non-decaying floor -- a matched filter on recovery WAVEFORMS (FRB tails, pulsar "
        "nu(t), GW ringdown residuals), not size histograms. (QT.05) the discrete->dynamic "
        "completion (v241-243) adds a DIFFERENT signature class: discrete statistical phases "
        "-- spin in units of pi/4 (8th roots), braiding in pi/2, with a dominant m=2 fermion "
        "sector (theta=-1) and c=8 -- reinterpreting the FRB.08 'm=2' as the PREDICTED fermion "
        "mode. Internal-consistency, no data."
    )
    ok = (ent.verdict.startswith("entanglement") and gap_row.detected
          and not fine_row.detected and not ctrl.detected
          and clk.verdict.startswith("walled") and mf_k.is_kernel_recovery
          and not mf_n.is_kernel_recovery and mtc.verdict.startswith("16 sectors"))
    print(f"\n==> VERDICT: {verdict}")

    RESULTS.mkdir(exist_ok=True)
    out = {
        "constants": constants.summary(),
        "qt01_entanglement": {
            "occupation": list(ent.occupation), "surprisals": ent.surprisals,
            "modular_energies": ent.modular_energies,
            "schmidt": ent.schmidt, "recovery_I": ent.recovery_I,
            "protected_present": ent.protected_present, "s_ratio": ent.s_ratio,
            "s_gap_is_delta": ent.s_gap_is_delta, "s_three_is_6ln3": ent.s_three_is_6ln3,
            "s_ratio_is_clock": ent.s_ratio_is_clock, "verdict": ent.verdict},
        "qt02_recovery_dsi": [vars(r) for r in scan],
        "qt02_control": vars(ctrl),
        "qt03_otoc": vars(otoc),
        "qt04_walled_clock": {
            "rates": clk.rates, "bend": clk.bend, "bend_curvature": clk.bend_curvature,
            "sheet_slope": clk.sheet_slope, "wall_at_nfam": clk.wall_at_nfam,
            "verdict": clk.verdict,
            "matched_filter_kernel": vars(mf_k), "matched_filter_nonkernel": vars(mf_n)},
        "qt05_mtc": {
            "n_sectors": mtc.n_sectors, "n_bosons": mtc.n_bosons, "n_fermions": mtc.n_fermions,
            "n_anyons": mtc.n_anyons, "spin_phase_quantum": mtc.spin_phase_quantum,
            "braid_phase_quantum": mtc.braid_phase_quantum, "distinct_spin_phases": mtc.distinct_spin_phases,
            "central_charge": mtc.central_charge, "integrable": mtc.integrable,
            "trivial_on_E8": mtc.trivial_on_E8, "verdict": mtc.verdict},
        "checks_passed": bool(ok),
        "verdict": verdict,
    }
    (RESULTS / "results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT quantum testbed: entanglement / DSI / OTOC")
    ap.add_argument("command", choices=["audit", "analyze"], nargs="?", default="analyze")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args(argv)
    if args.command == "audit":
        return _audit()
    return _analyze(args.seed)


if __name__ == "__main__":
    raise SystemExit(main())
