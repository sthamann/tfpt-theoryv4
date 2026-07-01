"""Ingest every recovery-comb channel and reduce it to a per-channel comb-power measurement.

Two tiers, by what the sibling experiment leaves on disk:

  TIER A -- reproducible ABSOLUTE eps (the recovery curve is committed AND the observable is
            ``ln(flux)``, so the fitted comb amplitude IS the fractional eps the theory predicts):
              A1 magnetar, A4 GRB, A5 ENT  (all 'surface' firewall).
            We re-run the shared comb fit locally (we do NOT edit the sibling) to get a_hat +/- a
            red-noise-aware null band -> eps^2 +/- se per gated source -> combined per channel.

  TIER B -- gain-only / no usable absolute eps (raw curve is gitignored/absent, or the observable
            is not a fractional-flux modulation, or the single event is degenerate):
              A3/A3b FRB tails (linear intensity, raw waterfalls absent),
              PG.05 Crab nudot (linear detrended nudot, monthly cadence),
              GW ringdown (single-event bend degeneracy; no cascade comb eps),
              A2 BH tail, PG.07/PG.06b Vela (pipeline only), crust-cooling (if present).
            We read the stored comb gain and report a NORMALISED amplitude sqrt(2*gain) as context
            only -- explicitly NOT comparable to the absolute 2% prediction.

Group typing follows the sibling firewall: 'horizon' + 'horizon-residual' -> the boundary/horizon
group (where TFPT predicts a universal eps); 'surface' -> the surface group. The all-channel group
is their union and is legitimate ONLY as a universal-DSI bound.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np

from .combfit import estimate_comb
from .metalimit import combine_power, upper_limit

EXPERIMENTS = Path(__file__).resolve().parents[3]
RCD = EXPERIMENTS / "recovery-comb-domains"
PULSAR = EXPERIMENTS / "pulsar-glitch-recovery"
GW_DIR = EXPERIMENTS / "gw-ringdown-echo"
CRUST = EXPERIMENTS / "crust-cooling-comb"

HORIZON = "horizon"
SURFACE = "surface"


@dataclass
class ChannelRecord:
    key: str
    domain: str
    group: str            # "horizon" | "surface"
    firewall: str         # sibling firewall_legitimacy
    observable: str       # what the amplitude means + its units
    data_status: str
    usable_abs: bool      # feeds the ABSOLUTE-eps meta-limit?
    n_sources: int
    n_gated: int
    eps2: float           # channel-level debiased comb power (~ eps^2); NaN if not usable
    se_power: float
    eps_hat: float        # absolute fractional comb amplitude point estimate; NaN if not usable
    sigma_amp: float
    eps95: float          # per-channel absolute one-sided 95% UL; NaN if not usable
    norm_amp: float | None  # normalised amplitude sqrt(2*gain) (context; not absolute eps)
    gain: float | None
    p_value: float | None
    per_source: list[dict] = field(default_factory=list)
    note: str = ""

    def as_dict(self) -> dict:
        d = asdict(self)
        for key in ("eps2", "se_power", "eps_hat", "sigma_amp", "eps95"):
            d[key] = None if math.isnan(d[key]) else round(float(d[key]), 6)
        if d["norm_amp"] is not None:
            d["norm_amp"] = round(float(d["norm_amp"]), 6)
        if d["gain"] is not None:
            d["gain"] = round(float(d["gain"]), 6)
        if d["p_value"] is not None:
            d["p_value"] = round(float(d["p_value"]), 6)
        return d


NAN = float("nan")


# --------------------------------------------------------------------------- readers (reproduce)
def _read_flux_csv(path: Path) -> tuple[np.ndarray, np.ndarray] | None:
    """Read a committed magnetar/GRB light curve (header t_days|t|t_s, flux|rate). (t, flux)>0."""
    try:
        with path.open(encoding="utf-8") as fh:
            rd = csv.DictReader(fh)
            cols = {(c or "").strip().lower(): c for c in (rd.fieldnames or [])}
            tk = cols.get("t_days") or cols.get("t") or cols.get("t_s")
            fk = cols.get("flux") or cols.get("rate")
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


def _read_ent_bands(path: Path) -> list[tuple[str, np.ndarray, np.ndarray]]:
    """Per-band ENT recovery curves, binned in ln(t) (mirrors recovery-comb-domains/ent.py)."""
    try:
        with path.open(encoding="utf-8") as fh:
            rd = csv.DictReader(fh)
            cols = {(c or "").strip().lower(): c for c in (rd.fieldnames or [])}
            mk, gk, bk = cols.get("mjd"), cols.get("mag"), cols.get("band")
            if not mk or not gk or not bk:
                return []
            by_band: dict[str, list[tuple[float, float]]] = {}
            for row in rd:
                try:
                    mjd, mag, band = float(row[mk]), float(row[gk]), (row[bk] or "").strip()
                except (TypeError, ValueError):
                    continue
                if mjd > 0 and mag > 0 and band:
                    by_band.setdefault(band, []).append((mjd, mag))
    except OSError:
        return []
    out: list[tuple[str, np.ndarray, np.ndarray]] = []
    for band, pts in by_band.items():
        pts.sort()
        mjd = np.array([p[0] for p in pts], float)
        mag = np.array([p[1] for p in pts], float)
        flux = 10.0 ** (-0.4 * mag)
        t = mjd - mjd[int(np.argmax(flux))]
        m = t > 0
        if int(m.sum()) >= 6:
            tb, yb = _bin_ln_t(t[m], np.log(flux[m]))
            if len(tb) >= 6:
                out.append((band, tb, yb))
    return out


def _bin_ln_t(t: np.ndarray, y: np.ndarray, *, n_bins: int = 70,
              min_count: int = 2) -> tuple[np.ndarray, np.ndarray]:
    lt = np.log(t)
    edges = np.linspace(lt.min(), lt.max(), n_bins + 1)
    idx = np.clip(np.digitize(lt, edges) - 1, 0, n_bins - 1)
    tc, yb = [], []
    for j in range(n_bins):
        sel = idx == j
        if int(np.sum(sel)) >= min_count:
            tc.append(float(np.exp(0.5 * (edges[j] + edges[j + 1]))))
            yb.append(float(np.median(y[sel])))
    return np.array(tc), np.array(yb)


def _load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _stored_gains(rcd: dict | None, key: str) -> dict[str, float]:
    """Map source-name -> stored comb gain for a recovery-comb-domains channel (cross-check)."""
    if not rcd:
        return {}
    for ch in rcd.get("channels", []):
        if ch.get("key") == key and ch.get("result"):
            per = ch["result"].get("per_source") or ch["result"].get("per_band") or []
            out: dict[str, float] = {}
            for p in per:
                name = p.get("source", "?")
                if "band" in p:
                    name = f"{name}:{p['band']}"
                out[name] = float(p.get("gain", 0.0))
            return out
    return {}


# --------------------------------------------------------------------------- Tier A builder
def _reduce_sources(sources: list[tuple[str, np.ndarray, np.ndarray]], *,
                    stored: dict[str, float], seed: int) -> tuple[list[dict], dict]:
    """Fit each source, attach the stored gain for cross-check, combine the GATED ones in power."""
    per: list[dict] = []
    for name, t, y in sources:
        est = estimate_comb(t, y, seed=seed)
        d = est.as_dict()
        d["source"] = name
        if name in stored:
            d["gain_stored"] = round(stored[name], 6)
            d["gain_reproduced_ok"] = bool(abs(est.gain - stored[name]) < 5e-3)
        per.append(d)
    gated = [d for d in per if d["range_sufficient"]]
    comb = combine_power([d["eps2"] for d in gated], [d["se_power"] for d in gated])
    ul = upper_limit(comb, rho=0.0)
    summary = {"n_gated": len(gated), "eps2": comb.eps2, "se_power": comb.se_power,
               "tau2": comb.tau2, "eps_hat": ul["eps_hat"], "sigma_amp": ul["sigma_amp"],
               "eps95": ul["eps95"]}
    return per, summary


def _tier_a(key: str, domain: str, firewall: str, group: str,
            sources: list[tuple[str, np.ndarray, np.ndarray]], stored: dict[str, float],
            note: str, seed: int) -> ChannelRecord:
    per, s = _reduce_sources(sources, stored=stored, seed=seed)
    usable = s["n_gated"] > 0
    xok = [d.get("gain_reproduced_ok") for d in per if "gain_reproduced_ok" in d]
    xnote = (f" reproduced gain matches stored for {sum(bool(v) for v in xok)}/{len(xok)} sources."
             if xok else "")
    return ChannelRecord(
        key=key, domain=domain, group=group, firewall=firewall,
        observable="ln(flux) -> fitted comb amplitude == fractional eps (absolute)",
        data_status="real" if usable else "data_limited",
        usable_abs=usable, n_sources=len(per), n_gated=s["n_gated"],
        eps2=s["eps2"] if usable else NAN, se_power=s["se_power"] if usable else NAN,
        eps_hat=s["eps_hat"] if usable else NAN, sigma_amp=s["sigma_amp"] if usable else NAN,
        eps95=s["eps95"] if usable else NAN, norm_amp=None, gain=None, p_value=None,
        per_source=per, note=note + xnote)


# --------------------------------------------------------------------------- Tier B builder
def _tier_b(key: str, domain: str, firewall: str, group: str, observable: str,
            gain: float | None, p_value: float | None, data_status: str,
            note: str) -> ChannelRecord:
    norm = math.sqrt(2.0 * gain) if (gain is not None and gain > 0) else None
    return ChannelRecord(
        key=key, domain=domain, group=group, firewall=firewall, observable=observable,
        data_status=data_status, usable_abs=False, n_sources=0, n_gated=0,
        eps2=NAN, se_power=NAN, eps_hat=NAN, sigma_amp=NAN, eps95=NAN,
        norm_amp=norm, gain=gain, p_value=p_value, per_source=[], note=note)


# --------------------------------------------------------------------------- channels
def channel_a1(rcd: dict | None, seed: int) -> ChannelRecord:
    files = sorted((RCD / "data" / "magnetar").glob("*.csv"))
    sources: list[tuple[str, np.ndarray, np.ndarray]] = []
    for f in files:
        rd = _read_flux_csv(f)
        if rd is not None:
            sources.append((f.stem, np.asarray(rd[0]), np.log(rd[1])))
    return _tier_a("A1", "magnetar outburst flux relaxation", SURFACE, SURFACE, sources,
                   _stored_gains(rcd, "A1"),
                   "REAL Swift-XRT/LSXPS magnetar light curves, y=ln(flux); surface firewall "
                   "(magnetospheric/crustal relaxation, not a horizon).", seed)


def channel_a4(rcd: dict | None, seed: int) -> ChannelRecord:
    files = sorted((RCD / "data" / "grb").glob("*.csv"))
    sources = [(f.stem, np.asarray(rd[0]), np.log(rd[1]))
               for f in files if (rd := _read_flux_csv(f)) is not None]
    return _tier_a("A4", "GRB X-ray afterglow plateau", SURFACE, SURFACE, sources,
                   _stored_gains(rcd, "A4"),
                   "REAL Swift-XRT GRB afterglow light curves, y=ln(flux); surface firewall "
                   "(central-engine/accretion relaxation, not a horizon).", seed)


def channel_a5(rcd: dict | None, seed: int) -> ChannelRecord:
    files = sorted((RCD / "data" / "ent").glob("*.csv"))
    sources: list[tuple[str, np.ndarray, np.ndarray]] = []
    for f in files:
        for band, tb, yb in _read_ent_bands(f):
            sources.append((f"{f.stem}:{band}", tb, yb))
    return _tier_a("A5", "nuclear transient (AGN-disk TDE) optical fade", SURFACE, SURFACE, sources,
                   _stored_gains(rcd, "A5"),
                   "REAL ZTF nuclear-transient fade, y=ln(flux) binned in ln(t); surface firewall "
                   "(accretion/central-engine relaxation, not a horizon).", seed)


def _rcd_channel_gain(rcd: dict | None, key: str) -> tuple[float | None, float | None, str]:
    if not rcd:
        return None, None, "recovery_comb_domains.json absent"
    for ch in rcd.get("channels", []):
        if ch.get("key") == key:
            res = ch.get("result")
            if res:
                return float(res.get("gain", 0.0)), float(res.get("p_value", 1.0)), ch.get("note", "")
            return None, None, ch.get("note", "")
    return None, None, f"channel {key} not found"


def channel_a3(rcd: dict | None) -> ChannelRecord:
    g, p, note = _rcd_channel_gain(rcd, "A3")
    return _tier_b("A3", "FRB burst tail (FAST/GBT, stacked)", "horizon-residual", HORIZON,
                   "linear detrended intensity tail -> normalised amplitude only (raw .calibP "
                   "waterfalls gitignored/absent -> no absolute eps)", g, p, "gain_only",
                   "Horizon-residual boundary recovery, but the recovery observable is a "
                   "scattering-dominated linear intensity tail and the raw waterfalls are not on "
                   "disk -> stacked NULL only, no absolute eps. " + note)


def channel_a3b(rcd: dict | None) -> ChannelRecord:
    g, p, note = _rcd_channel_gain(rcd, "A3b")
    return _tier_b("A3b", "CHIME baseband FRB burst tail (stacked)", "horizon-residual", HORIZON,
                   "linear detrended intensity tail -> normalised amplitude only (raw baseband "
                   "HDF5 gitignored/absent -> no absolute eps)", g, p, "gain_only",
                   "Cleaner (coherently dedispersed) FRB tails, still linear-intensity + raw data "
                   "absent -> stacked NULL only, no absolute eps. " + note)


def channel_a2(rcd: dict | None) -> ChannelRecord:
    _, _, note = _rcd_channel_gain(rcd, "A2")
    return _tier_b("A2", "BH late-time ringdown tail / QNM overtones", HORIZON, HORIZON,
                   "post-ringdown power-law tail (below single-event SNR -> no eps)", None, None,
                   "data_limited",
                   "Horizon-legitimate but below current single-event SNR; no comb eps available. "
                   + note)


def channel_gw() -> ChannelRecord:
    return _tier_b("GW", "GW ringdown dynamic recovery (Stage-2 walled clock)", HORIZON, HORIZON,
                   "single-event ringdown envelope -> the bend is degenerate with one exponential "
                   "(two-mode R^2 gain ~1.3e-3); a single ringdown is not a cascade -> NO comb eps",
                   None, None, "data_limited",
                   "The TFPT-relevant HORIZON channel. gw-ringdown-echo Stage-2 finds "
                   "NO_KERNEL_RECOVERY on real GW150914/GW190521 strain and proves that within one "
                   "monotone recovery the comb is structurally unmeasurable (needs a many-event "
                   "cascade). No results.json / no eps; strain gitignored. -> data_limited.")


def channel_pg05() -> ChannelRecord:
    js = _load_json(PULSAR / "results" / "pg05_recovery_comb.json")
    gain = p = None
    note = "pg05_recovery_comb.json absent"
    per: list[dict] = []
    if js:
        segs = js.get("segments", [])
        # the pg05 'amplitude' field is actually the comb GAIN at omega (see nu_recovery.py)
        gains = [float(s.get("amplitude", 0.0)) for s in segs]
        ps = [float(s.get("p_value", 1.0)) for s in segs]
        per = [{"source": f"glitch_{int(s.get('glitch_mjd', 0))}", "n_points": s.get("n_points"),
                "gain": round(float(s.get("amplitude", 0.0)), 6),
                "p_value": round(float(s.get("p_value", 1.0)), 6),
                "norm_amp": round(math.sqrt(2.0 * float(s.get("amplitude", 0.0))), 6)}
               for s in segs]
        if gains:
            gain = float(np.mean(gains))
            p = float(np.min(ps))
            note = (f"REAL Crab nudot: {len(segs)} inter-glitch segments, monthly cadence; "
                    "linear detrended nudot (NOT ln-flux) -> normalised amplitude only, and "
                    "small-N segments are noise-floor-dominated -> no absolute eps. "
                    + js.get("verdict", "")[:200])
    rec = _tier_b("PG.05", "Crab dynamic recovery comb on nu-dot(t)", "surface", SURFACE,
                  "linear detrended nudot recovery -> normalised amplitude only (not fractional "
                  "flux; monthly cadence undersamples the fast transient)", gain, p,
                  "data_limited", note)
    rec.per_source = per
    rec.n_sources = len(per)
    return rec


def channel_vela() -> ChannelRecord:
    js = _load_json(PULSAR / "results" / "pg06b_vela.json")
    note = "pg06b_vela.json absent"
    if js:
        note = ("REAL NICER Vela reduction PROVEN (F0=11.193 Hz detected) but only a per-obs "
                "H-test; a comb-quality phase-connected nu(t) needs a multi-hour timing project "
                "-> no recovery curve, no comb eps. " + js.get("verdict", "")[:160])
    return _tier_b("PG.07", "NICER Vela recovery comb (pipeline only)", "surface", SURFACE,
                   "no comb-quality nu(t) yet -> no eps", None, None, "data_limited", note)


def channel_crust() -> ChannelRecord:
    """crust-cooling-comb runs in parallel: ingest a results JSON if the sibling produced one."""
    files = sorted((CRUST / "results").glob("*.json")) if (CRUST / "results").exists() else []
    js = None
    for f in files:
        js = _load_json(f)
        if js:
            break
    if not js:
        return _tier_b("crust", "neutron-star crust-cooling recovery comb", "surface", SURFACE,
                       "sibling result absent (runs in parallel) -> not ingested", None, None,
                       "absent", "crust-cooling-comb/results/*.json not present at analyze time "
                       "(parallel sibling); gracefully skipped -- add later if it lands.")
    gain = js.get("gain")
    if gain is None:
        for v in js.values():
            if isinstance(v, dict) and "gain" in v:
                gain = v.get("gain")
                break
    p = js.get("p_value")
    return _tier_b("crust", "neutron-star crust-cooling recovery comb", "surface", SURFACE,
                   "crust-cooling curve comb gain (ingested from sibling; treated as normalised "
                   "context unless it exposes an absolute eps)",
                   float(gain) if gain is not None else None,
                   float(p) if p is not None else None, "gain_only",
                   "Ingested crust-cooling-comb sibling result (read-only). Reported as normalised "
                   "context; verify its observable before any absolute-eps use.")


def all_channels(*, seed: int = 0) -> list[ChannelRecord]:
    """Build every channel record (Tier A reproduced locally; Tier B read-only)."""
    rcd = _load_json(RCD / "results" / "recovery_comb_domains.json")
    return [
        channel_a1(rcd, seed), channel_a4(rcd, seed), channel_a5(rcd, seed),
        channel_a3(rcd), channel_a3b(rcd), channel_a2(rcd), channel_gw(),
        channel_pg05(), channel_vela(), channel_crust(),
    ]
