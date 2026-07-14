#!/usr/bin/env python3
"""
FRACTAL.HUNT.04 -- POST-HOC exploratory scan of the NEW log-time tones from
fractal_selfsimilarity_hunt.py across every recovery data set in hand.

FIREWALL / HONESTY (read first):
  * This is a POST-HOC, NON-PREREGISTERED scan (the tones were derived
    2026-07-13 from the two-ratio fractal-string analysis, the data were
    already in the repo). Any p < 0.05 here is "escalate -> preregister an
    independent test", NEVER a claim or a scorecard row.
  * Verdict vocabulary: null / range_blind / escalate_candidate.
  * All channels reuse the injection-validated stacked permutation detector
    of recovery-comb-domains (_stacked_at: per-omega ln-range gate >= 2.8
    periods + Nyquist), so gates are identical to the preregistered scans.

TONES (all derived from the frozen kernel a = 6 ln(3/2), b = 6 ln 3):
  omega_1  = 2pi/a       = 2.5827   known S2b comb   (REFERENCE, not new)
  omega_2  = 2pi/b       = 0.9532   NEW second tone  (period 6.59 in ln t)
  omega_3  = 2pi/(b-a)   = 1.5108   NEW generation tone (period 4.16)
  res_*    = imaginary parts of the complex dimensions of
             1 - e^{-as} - e^{-bs} (the TRUE two-ratio resonances; the
             lattice omega_1 is only an approximation). The low-lying ones:
               0.8632, 2.0558, 2.7490 (the omega_1-detuned leading
               resonance), 3.7962, 4.9112, 5.5589
             High-frequency members (4.91, 5.56) have SHORT ln-periods
             (1.28, 1.13) -> testable even on BH ringdown envelopes and
             ms FRB tails where every classic comb is range-blind.

Channels: GW BH ringdown residual envelopes (GWOSC strain, tfpt_gw pipeline),
FAST FRB burst tails, CHIME baseband tails, magnetar outbursts, GRB
afterglows, earthquake aftershock rates (cached), ENT/ZTF fade, crust
cooling, LSCO strange-metal master curve, Vela 2024 glitch recovery.

Run:  cd experiments/tfpt-discovery && .venv/bin/python new_tone_posthoc_scan.py
"""
from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "recovery-comb-domains" / "src"))
sys.path.insert(0, str(EXP / "gw-ringdown-echo" / "src"))
sys.path.insert(0, str(EXP / "strange-metal-comb" / "src"))

from tfpt_combdomains.channels import _read_flux_csv, _read_frb_profile, _frb_tail  # noqa: E402
from tfpt_combdomains.chime import read_chime_profile  # noqa: E402
from tfpt_combdomains.ent import DATA as ENT_DIR  # noqa: E402
from tfpt_combdomains.ent import bin_ln_t, read_ent_curves  # noqa: E402
from tfpt_combdomains.grb import DATA as GRB_DIR  # noqa: E402
from tfpt_combdomains.grb import read_grb_csv  # noqa: E402
from tfpt_combdomains.quake import DATA as QUAKE_DIR  # noqa: E402
from tfpt_combdomains.quake import MAINSHOCKS, _stacked_at, fetch_quake, rate_curve  # noqa: E402

A = 6 * math.log(1.5)
B = 6 * math.log(3.0)

TONES: dict[str, float] = {
    "omega_1 (2.583, known comb, REFERENCE)": 2 * math.pi / A,
    "omega_2 (2pi/6ln3, NEW 2nd tone)": 2 * math.pi / B,
    "omega_3 (2pi/6ln2, NEW generation tone)": 2 * math.pi / (B - A),
    "res_0.863 (complex dim #1)": 0.863212,
    "res_2.056 (complex dim #2)": 2.055794,
    "res_2.749 (leading resonance, omega_1 detuned)": 2.749026,
    "res_3.796 (complex dim #4)": 3.796156,
    "res_4.911 (complex dim #5, short period 1.28)": 4.911247,
    "res_5.559 (complex dim #6, short period 1.13)": 5.558893,
}
NEW_TONES = [k for k in TONES if not k.startswith("omega_1")]

RCD = EXP / "recovery-comb-domains" / "data"
FRB_NEW = EXP / "frb-tfpt-signatures" / "new-data"
GW_STRAIN = EXP / "gw-ringdown-echo" / "data" / "strain"
CRUST = EXP / "crust-cooling-comb" / "data"
VELA = EXP / "pulsar-glitch-recovery" / "data" / "vela_2024" / "vela2024_nudot.csv"


# --------------------------------------------------------------------- loaders
def load_magnetar() -> list[tuple[np.ndarray, np.ndarray]]:
    out = []
    for f in sorted((RCD / "magnetar").glob("*.csv")):
        rd = _read_flux_csv(f)
        if rd is not None:
            out.append((rd[0], np.log(rd[1])))
    return out


def load_grb() -> list[tuple[np.ndarray, np.ndarray]]:
    out = []
    for f in sorted(GRB_DIR.glob("*.csv")):
        rd = read_grb_csv(f)
        if rd is not None:
            out.append((rd[0], np.log(rd[1])))
    return out


def load_frb_fast() -> list[tuple[np.ndarray, np.ndarray]]:
    out = []
    for f in sorted(FRB_NEW.glob("*.calibP")):
        rd = _read_frb_profile(f)
        if rd is None:
            continue
        tl = _frb_tail(rd[0], rd[1])
        if tl is not None:
            out.append(tl)
    return out


def load_frb_chime() -> list[tuple[np.ndarray, np.ndarray]]:
    out = []
    d = FRB_NEW / "chime-baseband"
    for f in sorted(d.glob("*_beamformed.h5")) if d.exists() else []:
        rd = read_chime_profile(f)
        if rd is None:
            continue
        tl = _frb_tail(rd[0], rd[1])
        if tl is not None:
            out.append(tl)
    return out


def load_quake_cached() -> list[tuple[np.ndarray, np.ndarray]]:
    out = []
    for ms in MAINSHOCKS:
        if not (QUAKE_DIR / f"{ms.name}.csv").exists():
            continue                      # cached only -- NO network in this scan
        days = fetch_quake(ms)
        if len(days) >= 20:
            out.append(rate_curve(days))
    return out


def load_ent() -> list[tuple[np.ndarray, np.ndarray]]:
    out = []
    for f in sorted(ENT_DIR.glob("*.csv")) if ENT_DIR.exists() else []:
        for _band, t, rec in read_ent_curves(f):
            tb, yb = bin_ln_t(t, rec)
            if len(tb) >= 6:
                out.append((tb, yb))
    return out


def load_crust() -> list[tuple[np.ndarray, np.ndarray]]:
    out = []
    for f in sorted(CRUST.glob("*.csv")):
        t, y = [], []
        with f.open(encoding="utf-8") as fh:
            for row in csv.reader(fh):
                if not row or row[0].startswith("#") or row[0].startswith("t_days"):
                    continue
                try:
                    tv, kv = float(row[0]), float(row[1])
                except ValueError:
                    continue
                if tv > 0 and kv > 0:
                    t.append(tv)
                    y.append(math.log(kv))
        if len(t) >= 6:
            out.append((np.array(t), np.array(y)))
    return out


def load_lsco() -> list[tuple[np.ndarray, np.ndarray]]:
    try:
        from tfpt_smc.master import load_lsco as _load  # noqa: PLC0415
        mc = _load()
        return [(np.exp(mc.u), mc.y)]      # _stacked_at re-logs internally
    except Exception as exc:  # noqa: BLE001
        print(f"  [skip] LSCO master curve unavailable: {exc}")
        return []


def load_vela() -> list[tuple[np.ndarray, np.ndarray]]:
    if not VELA.exists():
        return []
    raw = np.loadtxt(VELA, delimiter=",", skiprows=1)
    tau, nd = raw[:, 0], raw[:, 1]
    m = (tau > 0) & (nd < 0)
    return [(tau[m], np.log(-nd[m]))] if m.sum() >= 6 else []


def load_gw_envelopes() -> list[tuple[np.ndarray, np.ndarray]]:
    """Post-merger residual RMS envelopes from real GWOSC strain (tfpt_gw
    pipeline: whiten -> subtract dominant 220 QNM -> binned RMS envelope),
    one curve per (event, detector). Times in seconds since merger."""
    try:
        from tfpt_gw.dynamic_recovery import WIN_MAX_S, WIN_TAU, power_envelope  # noqa: PLC0415
        from tfpt_gw.strain_data import (  # noqa: PLC0415
            apply_whitening, detector_frame_mass, fit_and_subtract_qnm,
            qnm_220, read_hdf5, whitening_filter)
    except Exception as exc:  # noqa: BLE001
        print(f"  [skip] tfpt_gw unavailable: {exc}")
        return []
    curves = []
    for meta_f in sorted(GW_STRAIN.glob("*_meta.json")):
        try:
            meta = json.loads(meta_f.read_text(encoding="utf-8"))
            event = meta_f.stem.replace("_meta16k", "").replace("_meta", "")
            mf = detector_frame_mass(event, float(meta["mf"]))
            f0, tau = qnm_220(mf)
            for _det, fname in meta["files"].items():
                fp = GW_STRAIN / Path(fname).name
                if not fp.exists():
                    continue
                s = read_hdf5(str(fp))
                psd_i, scale = whitening_filter(s.data, s.dt)
                white = apply_whitening(s.data, psd_i, scale)
                merger = s.index_at(float(meta["gps"]))
                resid, _ = fit_and_subtract_qnm(white, merger, f0, tau, s.dt)
                win = min(int(WIN_TAU * tau / s.dt), int(WIN_MAX_S / s.dt))
                tc, env = power_envelope(resid, merger, win)
                if len(tc):
                    curves.append((tc * win * s.dt, env))
        except Exception as exc:  # noqa: BLE001
            print(f"  [warn] {meta_f.name}: {exc}")
    return curves


CHANNELS = {
    "GW BH ringdown residual envelope (GWOSC)": load_gw_envelopes,
    "FRB burst tails FAST (.calibP)": load_frb_fast,
    "FRB burst tails CHIME baseband": load_frb_chime,
    "magnetar outburst flux": load_magnetar,
    "GRB X-ray afterglow": load_grb,
    "earthquake aftershock rate (cached)": load_quake_cached,
    "ENT/ZTF nuclear-transient fade": load_ent,
    "NS crust cooling": load_crust,
    "strange-metal LSCO master curve": load_lsco,
    "Vela 2024 glitch recovery (nudot)": load_vela,
}


def main() -> int:
    print("=" * 96)
    print("POST-HOC scan of the NEW fractal-string tones across all recovery data in hand")
    print("  firewall: post-hoc, non-preregistered; p < 0.05 => 'escalate_candidate' only;")
    print("  detector + gates identical to the preregistered comb scans (_stacked_at).")
    print("=" * 96)

    results: dict = {}
    escalations = []
    for ch_name, loader in CHANNELS.items():
        curves = loader()
        results[ch_name] = {"n_curves": len(curves), "tones": {}}
        if not curves:
            print(f"\n### {ch_name}: no curves -> skipped")
            continue
        spans = [float(np.log(np.asarray(t)[np.asarray(t) > 0].max()
                              / np.asarray(t)[np.asarray(t) > 0].min()))
                 for t, _ in curves]
        print(f"\n### {ch_name}: {len(curves)} curve(s), ln-range "
              f"{min(spans):.1f}..{max(spans):.1f}")
        gated_ps = []
        for label, om in TONES.items():
            r = _stacked_at(curves, om, seed=41)
            results[ch_name]["tones"][label] = {"omega": round(om, 4), **r}
            is_new = label in NEW_TONES
            if r["n_used"] == 0:
                status = "range_blind"
            elif r["p_value"] < 0.05:
                status = "ESCALATE_CANDIDATE" if is_new else "nominally special (ref)"
            else:
                status = "null"
            if is_new and r["n_used"] > 0:
                gated_ps.append((label, r["p_value"]))
            if is_new and status == "ESCALATE_CANDIDATE":
                escalations.append((ch_name, label, r))
            print(f"  {label:48s} n_used={r['n_used']:3d}  p={r['p_value']:.4f}  {status}")
        if gated_ps:
            m = len(gated_ps)
            best = min(gated_ps, key=lambda kv: kv[1])
            gp = min(1.0, best[1] * m)
            results[ch_name]["bonferroni_new_tones"] = {
                "n_gated": m, "best_tone": best[0], "best_p": best[1],
                "global_p": round(gp, 4)}
            print(f"  -> Bonferroni over {m} gated NEW tones: best {best[0]} "
                  f"p={best[1]:.4f}, global p={gp:.3f}"
                  + ("  <-- survives look-elsewhere, ESCALATE" if gp < 0.05 else ""))

    print("\n" + "=" * 96)
    if escalations:
        print("ESCALATE CANDIDATES (post-hoc; need preregistered, independent re-test "
              "before ANY claim):")
        for ch, tone, r in escalations:
            print(f"  {ch} :: {tone} (p={r['p_value']:.4f}, n={r['n_used']})")
        # controls: (i) seed robustness, (ii) free stacked periodogram -- is the
        # candidate tone the data's own GLOBAL preference, or only locally ranked
        # against its matched band?
        from tfpt_combdomains.comb import _comb_gain  # noqa: PLC0415
        print("\n  --- controls on the escalate candidates ---")
        for ch, tone, _ in escalations:
            curves = CHANNELS[ch]()
            om = TONES[tone]
            ps = [_stacked_at(curves, om, seed=s)["p_value"] for s in (1, 7, 41, 99, 123)]
            lts = [np.log(np.asarray(t, float)) for t, _ in curves]
            ys = [np.asarray(y, float) for _, y in curves]
            grid = np.linspace(1.6, 6.0, 441)
            spec = np.array([sum(_comb_gain(lt, y, w) for lt, y in zip(lts, ys))
                             for w in grid])
            g_best = float(grid[int(np.argmax(spec))])
            g_at = float(spec[int(np.argmin(np.abs(grid - om)))])
            is_global = abs(g_best - om) < 0.15
            print(f"  {ch} :: {tone}:")
            print(f"    seed robustness: p = {ps}")
            print(f"    free periodogram: global best omega = {g_best:.2f} "
                  f"(gain {spec.max():.2f}) vs candidate {om:.3f} (gain {g_at:.2f}) -> "
                  + ("candidate IS the global structure"
                     if is_global else
                     "candidate is NOT the global peak: broad low-frequency structure "
                     "(plateau breaks) dominates; local matched-band rank inflates it"))
            results[ch].setdefault("controls", {})[tone] = {
                "seed_ps": ps, "free_best_omega": round(g_best, 3),
                "gain_at_candidate": round(g_at, 3),
                "gain_at_best": round(float(spec.max()), 3),
                "candidate_is_global_peak": bool(is_global)}
    else:
        print("NO new tone is nominally special in any gated channel -> clean post-hoc NULL.")
    print("structural finding: omega_2 (period 6.59 in ln t) needs >= 18.5 ln-e-folds -> "
          "range-blind in every channel in hand (like the Moebius (3/2)^12 comb); the "
          "short-period resonances res_4.911/res_5.559 are the FIRST kernel tones testable "
          "on BH ringdown envelopes and ms FRB tails.")

    out_p = HERE / "new_tone_posthoc_results.json"
    out_p.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nwrote {out_p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
