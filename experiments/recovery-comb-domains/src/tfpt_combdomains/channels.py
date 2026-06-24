"""The six cross-domain recovery-comb channels (A1-A3b, B4-B5).

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
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .chime import read_chime_profile
from .comb import LAMBDA, MIN_COMB_PERIODS, OMEGA, run_comb, stacked_comb_test
from .grb import DATA as GRB_DIR
from .grb import read_grb_csv

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
MAGNETAR_DIR = DATA / "magnetar"


def _read_flux_csv(path: Path) -> tuple[np.ndarray, np.ndarray] | None:
    """Read a normalised magnetar light curve (header ``t_days,flux[,flux_err]``; onset-relative
    days, flux/rate in any consistent unit). Returns (t_days, flux) with t, flux > 0, or None."""
    try:
        with path.open(encoding="utf-8") as fh:
            rd = csv.DictReader(fh)
            cols = {(c or "").strip().lower(): c for c in (rd.fieldnames or [])}
            tk = cols.get("t_days") or cols.get("t")
            fk = cols.get("flux") or cols.get("rate") or cols.get("flux_unabs")
            if not tk or not fk:
                return None
            t, f = [], []
            for row in rd:
                try:
                    tv, fv = float(row[tk]), float(row[fk])
                except (TypeError, ValueError):
                    continue
                if tv > 0 and fv > 0:
                    t.append(tv)
                    f.append(fv)
    except OSError:
        return None
    return (np.array(t), np.array(f)) if len(t) >= 6 else None


def channel_a1_magnetar() -> Channel:
    """Magnetar (SGR/AXP) post-outburst X-ray flux relaxation -- days..years (~3 decades in ln t),
    stackable over many outbursts: the widest-ln(t), best-sampled recovery data in hand. Legitimacy
    'surface' (magnetospheric/crustal relaxation, a residual-recovery search target, not a horizon).

    Sharp pipeline: each normalised light curve in ``data/magnetar/*.csv`` -> recovery observable
    ``y = ln(flux)`` (so the orders-of-magnitude power-law decay is absorbed by the detector's
    degree-2 ln-t baseline, not dominated by the bright early points); a per-curve ln-range gate;
    then a phase-incoherent STACK over all sufficiently-ranged outbursts to beat the intrinsic ~2%
    single-curve amplitude. Get data with ``tfpt-combdomains fetch-magnetar``."""
    files = sorted(MAGNETAR_DIR.glob("*.csv")) if MAGNETAR_DIR.exists() else []
    per: list[dict] = []
    curves: list[tuple[np.ndarray, np.ndarray]] = []
    for fpath in files:
        rd = _read_flux_csv(fpath)
        if rd is None:
            continue
        t, flux = rd
        rec = np.log(flux)                       # recovery observable in log space
        res = run_comb(t, rec)
        res["source"] = fpath.stem
        per.append(res)
        if res["range_sufficient"]:
            curves.append((t, rec))

    if not per:
        return Channel(
            "A1", "magnetar outburst flux relaxation", "surface", "data_limited",
            "NO data yet. FETCH: `tfpt-combdomains fetch-magnetar` pulls Swift/XRT long-term light "
            "curves (swifttools/UKSSDC) for a curated transient-magnetar list; or drop the Coti "
            "Zelati+2018 MOOC ('download all data', http://magnetars.ice.csic.es) light curve(s) "
            "into data/magnetar/<source>.csv (header t_days,flux[,flux_err], onset-relative days). "
            "Wide ln(t) (~3 decades) makes this the best new candidate -- relaxation is "
            "magnetospheric (surface), a search target with a firewall caveat, not a horizon recovery.")

    stack = stacked_comb_test(curves) if curves else None
    head = (f"REAL data: {len(per)} outburst light curve(s); {len(curves)} clear the ln-range gate "
            f"(>= {MIN_COMB_PERIODS} comb periods). ")
    detail = "; ".join(
        f"{p['source']} (periods={p['comb_periods']}, p={p['p_value']}"
        + ("" if p["range_sufficient"] else ", <gate: range-blind, EXCLUDED") + ")"
        for p in per)
    if stack and stack["n_used"]:
        tail = (f". STACKED over {stack['n_used']} outbursts: kernel omega={OMEGA:.2f} is "
                + (f"SPECIAL (p={stack['p_value']}) -> ESCALATE (independent cross-check first)"
                   if stack["comb_detected"]
                   else f"NOT special (p={stack['p_value']}) -> clean NULL")
                + " (magnetospheric/surface -> firewall caveat, not a horizon recovery).")
    else:
        tail = (". No single outburst clears the ln-range gate yet -> RANGE-LIMITED; add more "
                "wide-baseline (days..years) light curves (stacking raises amplitude, not ln-range).")
    agg = {
        "n_points": int(sum(p["n_points"] for p in per)),
        "comb_periods": max(p["comb_periods"] for p in per),
        "range_sufficient": bool(curves),
        "gain": (stack or {}).get("gain", 0.0),
        "p_value": (stack or {}).get("p_value", 1.0),
        "comb_detected": bool(stack and stack["comb_detected"]),
        "omega": OMEGA,
        "n_sources": len(per),
        "n_stacked": (stack or {}).get("n_used", 0),
        "per_source": per,
    }
    return Channel("A1", "magnetar outburst flux relaxation (stacked)", "surface", "real",
                   head + detail + tail, agg)


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
    """Frequency-summed Stokes-I intensity-vs-time profile of one PSRFITS/.calibP burst (reuses the
    FRB experiment's astropy reader). Returns (dt_s, profile, src_name) or None."""
    try:
        if str(FRB_SRC) not in sys.path:
            sys.path.insert(0, str(FRB_SRC))
        from frb_tfpt.psrfits import read_archive  # noqa: PLC0415  (optional cross-exp reader)
        arc = read_archive(str(path))
        spec = np.asarray(arc.I, dtype=float)             # (nchan, nbin) Stokes-I dynamic spectrum
        prof = spec.sum(axis=0) if spec.ndim == 2 else np.asarray(spec, float).ravel()
        dt = float(np.atleast_1d(arc.tbin).ravel()[0])
        return dt, prof, (arc.source or "").strip()
    except Exception:  # noqa: BLE001
        return None


def _frb_tail(dt: float, prof: np.ndarray) -> tuple[np.ndarray, np.ndarray] | None:
    """Post-peak intensity tail as a recovery curve: tau = (bins since peak) * dt, recovery = the
    positive tail with its smooth linear-in-ln(tau) trend removed (the detector then re-detrends
    with a degree-2 ln-t baseline). Returns (tau, rec) or None if the tail is too short."""
    ipk = int(np.argmax(prof))
    tail = np.asarray(prof[ipk + 1:], float)
    tail = tail[tail > 0]
    if len(tail) < 8:
        return None
    tau = (np.arange(len(tail)) + 1.0) * dt
    rec = tail - np.polyval(np.polyfit(np.log(tau), tail, 1), np.log(tau))
    return tau, rec


def channel_a3_frb_tail() -> Channel:
    """FRB burst TAIL (stacked): the post-peak intensity decay of bright repeater bursts -- a
    horizon-residual recovery (firewall-legit). A single ms-scale tail is scattering/noise-dominated
    (a WEAK null), so the sharper test STACKS the phase-incoherent kernel comb gain across many
    bright bursts (the SAME meta-test as A1), keeping the hard per-curve ln-range gate. Reads every
    raw waterfall in ``frb-tfpt-signatures/new-data/*.calibP``."""
    files = sorted(FRB_WATERFALLS.glob("*.calibP")) if FRB_WATERFALLS.exists() else []
    per: list[dict] = []
    curves: list[tuple[np.ndarray, np.ndarray]] = []
    for fpath in files:
        rd = _read_frb_profile(fpath)
        if rd is None:
            continue
        dt, prof, src = rd
        tl = _frb_tail(dt, prof)
        if tl is None:
            continue
        tau, rec = tl
        res = run_comb(tau, rec)
        res["source"] = fpath.stem
        res["frb"] = src or "?"
        per.append(res)
        if res["range_sufficient"]:
            curves.append((tau, rec))

    if not per:
        return Channel(
            "A3", "FRB burst tail (stacked)", "horizon-residual", "data_limited",
            "no readable raw waterfall in frb-tfpt-signatures/new-data/*.calibP (or the PSRFITS "
            "reader/astropy is unavailable). A single ms-scale FRB tail spans ~1 decade in ln(t) and "
            f"is scattering-dominated; the stack needs several bright bursts each clearing the "
            f"{MIN_COMB_PERIODS}-period ln-range gate (stacking raises amplitude, not ln-range).")

    by_src = Counter(p["frb"] for p in per)  # raw SRC_NAME; FAST 'J2000-1234' = FRB 20121102A campaign
    stack = stacked_comb_test(curves) if curves else None
    head = (f"REAL data: {len(per)} bright FRB burst waterfall(s) across {len(by_src)} repeater(s) "
            f"[{', '.join(f'{s}x{n}' for s, n in by_src.items())}]; {len(curves)} clear the "
            f"ln-range gate (>= {MIN_COMB_PERIODS} comb periods). ")
    detail = "; ".join(
        f"{p['source']} (periods={p['comb_periods']}, p={p['p_value']}"
        + ("" if p["range_sufficient"] else ", <gate: range-blind, EXCLUDED") + ")"
        for p in per)
    if stack and stack["n_used"]:
        tnote = (f". STACKED over {stack['n_used']} burst tails: kernel omega={OMEGA:.2f} is "
                 + (f"SPECIAL (p={stack['p_value']}) -> ESCALATE (independent cross-check first)"
                    if stack["comb_detected"]
                    else f"NOT special (p={stack['p_value']}) -> clean NULL")
                 + " (horizon-residual, but FRB tails are scattering/noise-dominated and the comb is "
                   "an intrinsic ~2% effect -> a weak constraint, not a horizon detection).")
    else:
        tnote = ". No burst tail clears the ln-range gate -> RANGE-LIMITED."
    agg = {
        "n_points": int(sum(p["n_points"] for p in per)),
        "comb_periods": max(p["comb_periods"] for p in per),
        "range_sufficient": bool(curves),
        "gain": (stack or {}).get("gain", 0.0),
        "p_value": (stack or {}).get("p_value", 1.0),
        "comb_detected": bool(stack and stack["comb_detected"]),
        "omega": OMEGA,
        "n_sources": len(per),
        "n_stacked": (stack or {}).get("n_used", 0),
        "per_source": per,
    }
    return Channel("A3", "FRB burst tail (stacked)", "horizon-residual", "real",
                   head + detail + tnote, agg)


# --------------------------------------------------------------------------- A3b CHIME baseband
CHIME_DIR = FRB_WATERFALLS / "chime-baseband"


def channel_a3b_chime_baseband() -> Channel:
    """CHIME/FRB baseband-catalog burst TAILS (stacked) -- the same horizon-residual tail-comb as
    A3, but on coherently-dedispersed, full-Stokes, 2.56 us CHIME baseband (DOI 10.11570/23.0029).
    Higher data QUALITY (genuine scattering tails, not noise-filled range) than the FAST/GBT
    .calibP; the physical ms-burst ceiling (no 3-decade recovery) is unchanged. Each file is a
    distinct one-off FRB, so this is a multi-source stack by construction."""
    files = sorted(CHIME_DIR.glob("*_beamformed.h5")) if CHIME_DIR.exists() else []
    per: list[dict] = []
    curves: list[tuple[np.ndarray, np.ndarray]] = []
    for fpath in files:
        rd = read_chime_profile(fpath)
        if rd is None:
            continue
        dt, prof, src = rd
        tl = _frb_tail(dt, prof)
        if tl is None:
            continue
        tau, rec = tl
        res = run_comb(tau, rec)
        res["source"] = src
        per.append(res)
        if res["range_sufficient"]:
            curves.append((tau, rec))

    if not per:
        return Channel(
            "A3b", "CHIME baseband FRB burst tail (stacked)", "horizon-residual", "data_limited",
            "no CHIME beamformed HDF5 in frb-tfpt-signatures/new-data/chime-baseband/ (or h5py "
            "unavailable). Fetch a subset of the 140 baseband-catalog files (DOI 10.11570/23.0029) "
            "with the CADC vos client: `vcp vos:AstroDataCitationDOI/CISTI.CANFAR/23.0029/data/"
            "beamformed_files/<FRB>_beamformed.h5 .` (each ~0.15-4 GB; pick the smallest/brightest).")

    stack = stacked_comb_test(curves) if curves else None
    head = (f"REAL CHIME baseband (2.56us, coherently dedispersed, full-Stokes): {len(per)} "
            f"distinct FRB(s); {len(curves)} clear the ln-range gate (>= {MIN_COMB_PERIODS} comb "
            "periods). ")
    detail = "; ".join(
        f"{p['source']} (periods={p['comb_periods']}, p={p['p_value']}"
        + ("" if p["range_sufficient"] else ", <gate: range-blind, EXCLUDED") + ")"
        for p in per)
    if stack and stack["n_used"]:
        tnote = (f". STACKED over {stack['n_used']} CHIME burst tails: kernel omega={OMEGA:.2f} is "
                 + (f"SPECIAL (p={stack['p_value']}) -> ESCALATE (independent cross-check first)"
                    if stack["comb_detected"]
                    else f"NOT special (p={stack['p_value']}) -> clean NULL")
                 + " (coherently-dedispersed genuine scattering tails -> cleaner than FAST, but a ms "
                   "burst still has no wide recovery and the comb is an intrinsic ~2% effect -> a "
                   "weak constraint, not a horizon detection).")
    else:
        tnote = ". No CHIME burst tail clears the ln-range gate -> RANGE-LIMITED."
    agg = {
        "n_points": int(sum(p["n_points"] for p in per)),
        "comb_periods": max(p["comb_periods"] for p in per),
        "range_sufficient": bool(curves),
        "gain": (stack or {}).get("gain", 0.0),
        "p_value": (stack or {}).get("p_value", 1.0),
        "comb_detected": bool(stack and stack["comb_detected"]),
        "omega": OMEGA,
        "n_sources": len(per),
        "n_stacked": (stack or {}).get("n_used", 0),
        "per_source": per,
    }
    return Channel("A3b", "CHIME baseband FRB burst tail (stacked)", "horizon-residual", "real",
                   head + detail + tnote, agg)


# --------------------------------------------------------------------------- A4 GRB plateau
def channel_a4_grb() -> Channel:
    """GRB X-ray afterglow plateau (stacked) -- the WIDEST-ln(t) astrophysical recovery in hand.
    A Swift-XRT flux light curve spans ~100 s..10^6-10^7 s (4-5 decades = 4-5 comb periods), so a
    SINGLE GRB clears the ln-range gate the ms FRB tails (A3) cannot, and >1000 public curves make
    the faint ~1.7% comb stackable with real statistics -- so this channel is NOT data-limited.
    Recovery observable y = ln(flux) (the detector's degree-2 ln-t baseline absorbs the power-law
    plateau/break trend, as in A1). Legitimacy 'surface': a central-engine/accretion relaxation,
    NOT a horizon recovery -- a comb here is a universal-DSI coincidence, a NULL is the informative
    outcome. Get data with ``tfpt-combdomains fetch-grb``."""
    files = sorted(GRB_DIR.glob("*.csv")) if GRB_DIR.exists() else []
    per: list[dict] = []
    curves: list[tuple[np.ndarray, np.ndarray]] = []
    for fpath in files:
        rd = read_grb_csv(fpath)
        if rd is None:
            continue
        t, flux = rd
        rec = np.log(flux)                        # recovery observable in log space
        res = run_comb(t, rec)
        res["source"] = fpath.stem
        per.append(res)
        if res["range_sufficient"]:
            curves.append((t, rec))

    if not per:
        return Channel(
            "A4", "GRB X-ray afterglow plateau (stacked)", "surface", "data_limited",
            "NO data yet. FETCH: `tfpt-combdomains fetch-grb` pulls public Swift-XRT GRB flux light "
            "curves (UKSSDC, Evans+2007/2009) for a curated long/plateau-GRB list into "
            "data/grb/<name>.csv (header t_s,flux[,flux_err], T0-relative seconds). A single GRB "
            "afterglow spans 4-5 decades in ln(t) (4-5 comb periods) -> clears the gate that the ms "
            "FRB tails cannot; central-engine relaxation (surface firewall), not a horizon recovery.")

    stack = stacked_comb_test(curves) if curves else None
    head = (f"REAL data: {len(per)} Swift-XRT GRB afterglow(s); {len(curves)} clear the ln-range gate "
            f"(>= {MIN_COMB_PERIODS} comb periods -- most single GRBs do, ~4-5 decades). ")
    detail = "; ".join(
        f"{p['source']} (periods={p['comb_periods']}, p={p['p_value']}"
        + ("" if p["range_sufficient"] else ", <gate: EXCLUDED") + ")"
        for p in per)
    if stack and stack["n_used"]:
        tail = (f". STACKED over {stack['n_used']} GRBs: kernel omega={OMEGA:.2f} is "
                + (f"SPECIAL (p={stack['p_value']}) -> ESCALATE (independent cross-check first)"
                   if stack["comb_detected"]
                   else f"NOT special (p={stack['p_value']}) -> clean NULL")
                + " (central-engine/accretion relaxation -> surface firewall, not a horizon recovery; "
                  "but WIDE-ln(t) + high-statistics, so this NULL is well-powered, NOT data-limited).")
    else:
        tail = ". No GRB clears the ln-range gate yet -> RANGE-LIMITED (unexpected; check the fetch)."
    agg = {
        "n_points": int(sum(p["n_points"] for p in per)),
        "comb_periods": max(p["comb_periods"] for p in per),
        "range_sufficient": bool(curves),
        "gain": (stack or {}).get("gain", 0.0),
        "p_value": (stack or {}).get("p_value", 1.0),
        "comb_detected": bool(stack and stack["comb_detected"]),
        "omega": OMEGA,
        "n_sources": len(per),
        "n_stacked": (stack or {}).get("n_used", 0),
        "per_source": per,
    }
    return Channel("A4", "GRB X-ray afterglow plateau (stacked)", "surface", "real",
                   head + detail + tail, agg)


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
        channel_a3b_chime_baseband(), channel_a4_grb(),
        channel_b4_bec_analog(), channel_b5_quantum_ladder(),
    ])
