"""FO.05 -- the activity EPISODE as transfer unit (exploratory surface leakage).

Excitation writes marks, one episode = one transfer step, quiescence = recovery.
All prior ladders ran burst-to-burst; this tests the episode aggregation level:
  (i)  consecutive quiescence-gap ratios on the teeth {3/2, (3/2)^3, (3/2)^6};
  (ii) episode-integrated energy/fluence ratios on the partner teeth (2/3)^k.

Episode = maximal burst cluster with inter-burst gap <= 5 d (frozen primary;
10 d flagged secondary). Valid episode >= 5 bursts; source needs >= 4 valid
episodes; gap ratios only over consecutive valid-episode pairs. KNOWN dominant
systematic: telescope scheduling (documented; escalate-only). Nulls: gap/energy
permutation within source + placebo teeth + Bonferroni over sources.
"""

from __future__ import annotations

import numpy as np

from . import constants as c
from .data import SourceBursts

EPISODE_GAP_PRIMARY_D = 5.0
EPISODE_GAP_SECONDARY_D = 10.0
MIN_EP_BURSTS = 5
MIN_EPISODES = 4
N_PERM = 2000


def episodes(mjd: np.ndarray, gap_d: float) -> list[np.ndarray]:
    edges = np.where(np.diff(mjd) > gap_d)[0] + 1
    return list(np.split(np.arange(len(mjd)), edges))


def _tooth_hits(ratios: np.ndarray, teeth: list[float]) -> int:
    lg = np.log10(ratios)
    hits = 0
    for tooth in teeth:
        lt = np.log10(tooth)
        hits += int(np.sum((np.abs(lg - lt) <= c.TOL_DEX)
                           | (np.abs(lg + lt) <= c.TOL_DEX)))
    return hits


def _ratio_test(rng: np.random.Generator, values: np.ndarray, teeth: list[float]
                ) -> dict:
    """Consecutive-ratio tooth test with sequence-permutation null."""
    r_obs = values[1:] / values[:-1]
    obs = _tooth_hits(r_obs, teeth)
    null = np.empty(N_PERM)
    for i in range(N_PERM):
        v = rng.permutation(values)
        null[i] = _tooth_hits(v[1:] / v[:-1], teeth)
    return {"n_ratios": int(r_obs.size), "hits": obs,
            "null_mean": round(float(null.mean()), 3),
            "enrichment": round(float(obs / max(null.mean(), 1e-9)), 3),
            "p": float((1 + np.sum(null >= obs)) / (N_PERM + 1))}


def _source_axis(rng: np.random.Generator, sb: SourceBursts, gap_d: float) -> dict | None:
    eps = episodes(sb.mjd, gap_d)
    valid = [e for e in eps if e.size >= MIN_EP_BURSTS]
    if len(valid) < MIN_EPISODES:
        return None
    # quiescence gaps between CONSECUTIVE valid episodes (no invalid in between)
    valid_set = {id(e): e for e in valid}
    gaps = []
    for a, b in zip(eps[:-1], eps[1:]):
        if id(a) in valid_set and id(b) in valid_set:
            gaps.append(sb.mjd[b[0]] - sb.mjd[a[-1]])
    gaps = np.array(gaps)
    out = {"source": sb.source, "gap_def_d": gap_d, "n_bursts": int(len(sb.mjd)),
           "n_episodes_valid": len(valid), "n_quiescence_gaps": int(gaps.size)}
    teeth = list(c.TIME_TEETH.values())
    if gaps.size >= 3:
        out["gap_ratio_test"] = _ratio_test(rng, gaps, teeth)
        out["gap_placebo"] = {str(p): _ratio_test(rng, gaps, [p])
                              for p in c.PLACEBO_TEETH}
    if sb.energy is not None:
        e_ep = []
        for e in valid:
            v = sb.energy[e]
            v = v[np.isfinite(v) & (v > 0)]
            if v.size:
                e_ep.append(v.sum())
        e_ep = np.array(e_ep)
        if e_ep.size >= 3:
            out["energy_ratio_test"] = _ratio_test(
                rng, e_ep, list(c.ENERGY_TEETH.values()))
            out["energy_kind"] = sb.energy_kind
    return out


def run(sources: list[SourceBursts], seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    primary, secondary = [], []
    for sb in sources:
        r = _source_axis(rng, sb, EPISODE_GAP_PRIMARY_D)
        if r:
            primary.append(r)
        r2 = _source_axis(rng, sb, EPISODE_GAP_SECONDARY_D)
        if r2:
            secondary.append(r2)

    def _min_bonf(rows: list[dict], key: str) -> tuple[float | None, int]:
        ps = [r[key]["p"] for r in rows if key in r]
        if not ps:
            return None, 0
        return min(1.0, min(ps) * len(ps)), len(ps)

    p_gap, n_gap = _min_bonf(primary, "gap_ratio_test")
    p_en, n_en = _min_bonf(primary, "energy_ratio_test")

    if n_gap == 0 and n_en == 0:
        verdict = "data_limited"
        note = "no source clears the episode gates (>=4 valid episodes)"
    elif (p_gap is not None and p_gap < 0.05) or (p_en is not None and p_en < 0.05):
        verdict = "hint_flag"
        note = "escalate-only; scheduling systematics are the default reading"
    else:
        verdict = "null"
        note = ("no tooth enrichment at the episode aggregation level "
                "(quiescence gaps + episode-integrated energies)")

    return {
        "axis": "FO.05_episode_transfer",
        "episode_gap_primary_d": EPISODE_GAP_PRIMARY_D,
        "sources_primary": primary,
        "sources_secondary_10d_flagged": secondary,
        "bonferroni": {"gap_ratio_p": p_gap, "n_gap_sources": n_gap,
                       "energy_ratio_p": p_en, "n_energy_sources": n_en},
        "systematic_on_record": "observing-schedule selection dominates quiescence gaps",
        "verdict": verdict,
        "note": note,
    }
