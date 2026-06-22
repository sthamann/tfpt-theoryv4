"""The five cross-domain recovery-comb channels (search.txt options A1-A3, B4-B5).

Each channel applies the SAME injection-validated comb detector (``comb.py``) to a recovery curve
from a different domain, and is typed by:

  * firewall_legitimacy -- how TFPT-legitimate the channel is. TFPT predicts the comb in
    BOUNDARY/HORIZON-recovery relaxations, so:
      "horizon"  = a genuine horizon/seam recovery (most legitimate);
      "surface"  = a compact-object surface/magnetosphere relaxation (borderline, as the firewall
                   already flags for pulsars -- a residual-recovery search target, not a horizon);
      "analog"   = a laboratory horizon analog (conceptually direct, needs bespoke data);
      "internal" = a controlled quantum system realising the ladder (theory/simulator side).
  * data_status -- real (data in hand) / fetchable / data_limited / needs_experiment.

NOTHING is claimed. Where data is in hand the comb runs; where it is not, the channel reports the
precise blocker. The ln(tau) RANGE gate (>~2.8 comb periods) is applied uniformly -- several
channels are range-blind by construction, which is itself the honest finding.
"""

from __future__ import annotations

import csv
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .comb import LAMBDA, MIN_COMB_PERIODS, OMEGA, run_comb

DATA = Path(__file__).resolve().parents[2] / "data"
FRB_WATERFALLS = (Path(__file__).resolve().parents[3]
                  / "frb-tfpt-signatures" / "new-data")
FRB_SRC = Path(__file__).resolve().parents[3] / "frb-tfpt-signatures" / "src"


@dataclass
class Channel:
    key: str
    domain: str
    firewall_legitimacy: str
    data_status: str
    note: str
    result: dict | None = None


# --------------------------------------------------------------------------- A1 magnetar
def channel_a1_magnetar() -> Channel:
    """Magnetar (SGR/AXP) post-outburst X-ray flux relaxation -- days..years (~3 decades in ln t),
    stackable over many outbursts. The cleanest WIDE-range recovery dataset; legitimacy 'surface'
    (magnetospheric/crustal relaxation, not a horizon -> a residual-recovery search target)."""
    csvf = DATA / "magnetar" / "flux_decay.csv"   # columns: t_days, flux, (flux_err)
    if csvf.exists():
        t, f = [], []
        with csvf.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                t.append(float(row["t_days"]))
                f.append(float(row["flux"]))
        t = np.array(t)
        rec = np.array(f) - np.polyval(np.polyfit(np.log(t), f, 1), np.log(t))
        res = run_comb(t, rec)
        return Channel("A1", "magnetar outburst flux relaxation", "surface", "real",
                       "post-outburst flux decay; comb test run", res)
    return Channel(
        "A1", "magnetar outburst flux relaxation", "surface", "data_limited",
        "FETCH: Swift/XRT light curves (UKSSDC build-your-own) or the homogeneous Coti Zelati+2018 "
        "magnetar-outburst sample (Swift/NICER/NuSTAR); drop flux(t) into data/magnetar/flux_decay.csv "
        "(t_days,flux). Then the comb runs unchanged. Wide ln(t) (~3 decades) makes this the best "
        "new candidate -- but the relaxation is magnetospheric (surface), so it is a search target "
        "with a firewall caveat, not a horizon recovery.")


# --------------------------------------------------------------------------- A2 BH late-time tail
def channel_a2_bh_tail() -> Channel:
    """Black-hole late-time power-law ringdown TAIL (and high-overtone QNM ln3) -- a genuine HORIZON
    relaxation. The post-ringdown t^-n tail is the cleanest horizon recovery, but it sits below the
    noise in current single-event data (covered, data-limited, by gw-ringdown-spectroscopy)."""
    return Channel(
        "A2", "BH late-time ringdown tail / QNM overtones", "horizon", "data_limited",
        "the post-ringdown power-law tail is a horizon recovery, but below current single-event "
        "SNR; high-overtone omega_R/T_H -> ln3=ln N_fam needs overtone spectroscopy (n=0 only "
        "today). Horizon-legitimate but data-limited (see gw-ringdown-spectroscopy). The comb "
        "detector is ready for a stacked late-time residual once high-SNR events accumulate (O5+).")


# --------------------------------------------------------------------------- A3 FRB burst tails
def _read_frb_profile(path: Path):
    """Frequency-summed intensity-vs-time profile of one PSRFITS/.calibP burst (reuses the FRB
    experiment's astropy reader). Returns (dt_s, profile) or None."""
    try:
        if str(FRB_SRC) not in sys.path:
            sys.path.insert(0, str(FRB_SRC))
        from frb_tfpt.psrfits import read_archive  # noqa: PLC0415  (optional cross-exp reader)
        arc = read_archive(str(path))
        spec = np.asarray(arc.data, dtype=float)          # (nchan, ntime) Stokes-I dynamic spectrum
        prof = spec.sum(axis=0) if spec.ndim == 2 else np.asarray(spec, float).ravel()
        return float(getattr(arc, "dt", 1.0)), prof
    except Exception:  # noqa: BLE001
        return None


def channel_a3_frb_tail() -> Channel:
    """FRB burst TAIL: the post-peak intensity decay of a bright repeater burst -- a horizon-
    residual recovery (firewall-legit). We have raw waterfalls in hand. BUT a single burst tail is
    ms-scale -> spans ~1 decade in ln(t) -> ~0.9 comb periods << 2.8 -> RANGE-BLIND by construction
    (stacking raises amplitude, not ln-range), exactly like a single GW ringdown."""
    files = sorted(FRB_WATERFALLS.glob("*.calibP")) if FRB_WATERFALLS.exists() else []
    if files:
        small = min(files, key=lambda p: p.stat().st_size)
        rd = _read_frb_profile(small)
        if rd is not None:
            dt, prof = rd
            ipk = int(np.argmax(prof))
            tail = prof[ipk + 1:]
            tail = tail[tail > 0]
            if len(tail) >= 8:
                tau = (np.arange(len(tail)) + 1.0) * dt
                rec = tail - np.polyval(np.polyfit(np.log(tau), tail, 1), np.log(tau))
                res = run_comb(tau, rec)
                return Channel("A3", "FRB burst tail (stacked)", "horizon-residual", "real",
                               f"read {small.name}; burst-tail comb test run", res)
    return Channel(
        "A3", "FRB burst tail (stacked)", "horizon-residual", "data_limited",
        "raw waterfalls present, but a single burst tail spans only ~1 decade in ln(t) "
        f"(~0.9 comb periods << the {MIN_COMB_PERIODS} needed) and is scattering-dominated -> "
        "RANGE-BLIND by construction; stacking many tails raises amplitude, not ln-range. "
        "(If the PSRFITS reader is unavailable the channel reports this analytic limit.)")


# --------------------------------------------------------------------------- B4 BEC analog horizon
def channel_b4_bec_analog() -> Channel:
    """BEC analog-horizon Hawking/Page recovery -- a laboratory horizon. The recovery-channel
    experiment (Test C) is the theory side (CPTP map, Page curve, Petz recovery at rate (2/3)^6);
    the empirical side is bespoke analog-gravity correlation data (e.g. Steinhauer-type)."""
    return Channel(
        "B4", "BEC analog-horizon Hawking/Page recovery", "analog", "needs_experiment",
        "conceptually the MOST direct boundary-recovery realisation: an analog horizon's "
        "Hawking-correlation / Page-style information recovery could carry the (2/3)^6 rate or the "
        "omega=2.58 comb. Theory side = recovery-channel (CPTP/Page/Petz). Empirical side needs "
        "time/scale-resolved analog-gravity correlation data (not a public table) -> needs_experiment.")


# --------------------------------------------------------------------------- B5 quantum simulator
def channel_b5_quantum_ladder() -> Channel:
    """A controlled quantum system (cold atoms / superconducting qubits) engineered with the
    geometric mode ladder gamma_k = gamma0 lambda^-k -> the comb appears BY CONSTRUCTION at
    omega=2.58 (quantum-testbed QT.01/QT.02/QT.04 show this synthetically)."""
    return Channel(
        "B5", "quantum-simulator geometric ladder", "internal", "needs_experiment",
        "a simulator relaxing through the frozen ladder shows the comb by construction "
        "(quantum-testbed proves it synthetically: DSI at omega=2pi/ln lambda, suppression "
        "e^{-pi^2/ln lambda}). The empirical side needs a built experiment (engineered rate "
        "ladder, read-out of the relaxation) -> needs_experiment.")


@dataclass
class DomainReport:
    omega: float
    lam: float
    min_periods: float
    channels: list[Channel] = field(default_factory=list)


def all_channels() -> DomainReport:
    return DomainReport(OMEGA, LAMBDA, MIN_COMB_PERIODS, [
        channel_a1_magnetar(), channel_a2_bh_tail(), channel_a3_frb_tail(),
        channel_b4_bec_analog(), channel_b5_quantum_ladder(),
    ])
