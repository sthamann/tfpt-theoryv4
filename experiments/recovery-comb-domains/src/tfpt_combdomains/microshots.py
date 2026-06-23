"""(B1) The microshot/sub-burst CASCADE test on the vetted Nançay ECLAT catalog.

The dynamic TFPT recovery kernel predicts, in a boundary-recovery relaxation, (i) a resummed
recovery CLOCK ``rate(n) = -6 ln(1 - n/N_fam)`` -> a 3-step cascade with gap ratio
``ln 3 / ln(3/2) = 2.7095`` and a hard WALL at ``n = N_fam = 3`` (verification v124, FRB.09), and
(ii) a log-periodic (DSI) comb at ``omega = 2pi/ln((3/2)^6) = 2.583`` in the recovery curve.

Within a single ultra-bright FRB the resolved MICROSHOTS form a real intra-burst cascade. We use
the *vetted, published* microshot arrival times of FRB 20220912A bursts B1 (27 shots) and B2
(18 shots), manually identified by Hewitt et al. 2023 (MNRAS 526, 2039; Zenodo 10552561,
``Figure2+6.ipynb``) -- not our own peak-finding, so there is no noise-vs-shot ambiguity.

Firewall: a search target (horizon-residual), NEVER a claim. Microshots are an intra-burst point
process, so this tests the kernel's DYNAMICS (gap clock / wall / time-DSI). It needs no amplitudes;
the echo-ratio (64/729) energy test is a separate, amplitude-based extension.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from .comb import LAMBDA, MIN_COMB_PERIODS, OMEGA

# --- vetted microshot arrival times (ms), Hewitt et al. 2023, Zenodo 10552561 / Figure2+6.ipynb ---
B1_TIMES_MS = [11.9, 15.625, 15.8, 15.970, 16.136, 16.198, 16.358, 16.55, 16.715, 16.905, 17.016,
               17.130, 17.336, 17.401, 17.463, 17.753, 17.848, 17.976, 18.089, 18.135, 18.440,
               18.552, 18.601, 18.634, 18.843, 19.674, 19.869]
B2_TIMES_MS = [11.333, 11.544, 11.649, 11.710, 12.186, 12.232, 12.313, 12.6, 13.041, 13.342,
               13.450, 13.596, 13.708, 13.827, 13.935, 13.995, 14.061, 15.115]

CLOCK_RATIO = math.log(3) / math.log(1.5)        # 2.7095, the resummed-clock gap ratio (v124)
PLACEBO_RATIOS = (1.7, 2.2, 3.3, 4.5)            # arbitrary non-clock controls (FRB.09 placebo set)
RATIO_TOL_DEX = 0.10                              # +/- 0.10 in log10 (FRB echo tolerance)
N_NULL = 4000

# amplitude (echo-ratio) extension: the published NRT filterbanks (Zenodo 10552561, gitignored)
ECLAT = (Path(__file__).resolve().parents[3] / "frb-tfpt-signatures" / "new-data" / "eclat-microshots")
NRT_FREQS = np.linspace(1738, 1230, 128)         # NRT channel centres (MHz), Figure2+6.ipynb
# (fil, DM, norm-region n1, n2, crop_s) -- exactly the prep_burst calls in Figure2+6.ipynb
NRT_PREP = {"B1": ("b_59881.fil", 219.356, 9000, 12500, 60e-3),
            "B2": ("b_59884.fil", 219.377, 12500, 15000, 30e-3)}
# kernel echo targets: energy reads lambda, amplitude reads sqrt(lambda) (FRB.02 observable split)
ECHO_ENERGY = (64 / 729, 1 / 729)
ECHO_AMP = (8 / 27, 1 / 27)


def _gaps(t: np.ndarray) -> np.ndarray:
    return np.diff(np.sort(np.asarray(t, float)))


def gap_clock(t: np.ndarray, rng: np.random.Generator) -> dict:
    """Consecutive gap ratios rho_i = g_{i+1}/g_i: do they pile up at the clock 2.7095 (or 1/it)?
    Null = shuffle the gaps (destroys order, keeps the gap distribution); placebo = arbitrary
    non-clock ratios must NOT beat the kernel."""
    g = _gaps(t)
    if len(g) < 3:
        return {"n_ratios": 0, "enrichment": 0.0, "p": 1.0, "placebo_max_enr": 0.0, "supported": False}
    rho = g[1:] / g[:-1]
    lr = np.log10(rho)

    def _count(target: float) -> int:
        lt = math.log10(target)
        return int(np.sum(np.abs(lr - lt) < RATIO_TOL_DEX) + np.sum(np.abs(-lr - lt) < RATIO_TOL_DEX))

    obs = _count(CLOCK_RATIO)
    null = np.empty(N_NULL)
    for k in range(N_NULL):
        gs = rng.permutation(g)
        rs = np.log10(gs[1:] / gs[:-1])
        null[k] = np.sum(np.abs(rs - math.log10(CLOCK_RATIO)) < RATIO_TOL_DEX) + \
            np.sum(np.abs(-rs - math.log10(CLOCK_RATIO)) < RATIO_TOL_DEX)
    p = float((1 + np.sum(null >= obs)) / (N_NULL + 1))
    mean_null = float(null.mean()) or 1e-9
    enr = obs / mean_null
    placebo_enr = max(_count(pr) / (mean_null + 1e-9) for pr in PLACEBO_RATIOS)
    return {"n_ratios": len(rho), "obs": obs, "enrichment": round(enr, 3), "p": round(p, 4),
            "placebo_max_enr": round(placebo_enr, 3),
            "supported": bool(p < 0.05 and enr > 1.2 and enr > placebo_enr)}


def cascade_wall(t: np.ndarray, rng: np.random.Generator) -> dict:
    """Longest run of monotonically DECREASING gaps (an accelerating recovery cascade). TFPT caps
    such a cascade at N_fam=3; a wall is a DEFICIT of long runs vs a gap-shuffle null."""
    g = _gaps(t)
    if len(g) < 3:
        return {"longest_run": 0, "p_deficit": 1.0, "supported": False}

    def longest_dec(gg: np.ndarray) -> int:
        best = run = 1
        for i in range(1, len(gg)):
            run = run + 1 if gg[i] < gg[i - 1] else 1
            best = max(best, run)
        return best

    obs = longest_dec(g)
    null = np.array([longest_dec(rng.permutation(g)) for _ in range(N_NULL)])
    p_def = float((1 + np.sum(null <= obs)) / (N_NULL + 1))      # is the data's longest run SHORT?
    return {"longest_run": int(obs), "mean_null_run": round(float(null.mean()), 2),
            "p_deficit": round(p_def, 4), "supported": bool(obs <= 3 and p_def < 0.05)}


def time_comb(t: np.ndarray, rng: np.random.Generator, n_pool: int = 400) -> dict:
    """Log-periodic (DSI) clustering of the microshot times at the kernel lambda=(3/2)^6. Times are
    taken relative to a forest onset t0 = t_min - median_gap (so all tau>0); Rayleigh power at the
    kernel omega ranked against a matched off-kernel pool. Range-limited: needs >=2.8 periods."""
    ts = np.sort(np.asarray(t, float))
    g = np.diff(ts)
    t0 = ts[0] - float(np.median(g))
    tau = ts - t0
    x = np.log(tau[tau > 0])
    if len(x) < 6:
        return {"periods": 0.0, "range_sufficient": False, "p": 1.0, "rayleigh": 0.0}
    periods = float((x.max() - x.min()) / math.log(LAMBDA))

    def rayleigh(om: float) -> float:
        return float(abs(np.sum(np.exp(1j * om * x))) / len(x))

    r0 = rayleigh(OMEGA)
    fs = rng.uniform(0.72 * OMEGA, 1.40 * OMEGA, n_pool)
    fs = fs[np.abs(fs - OMEGA) > 0.06 * OMEGA]
    pool = np.array([rayleigh(f) for f in fs])
    p = float((1 + np.sum(pool >= r0)) / (len(pool) + 1))
    return {"periods": round(periods, 2), "range_sufficient": bool(periods >= MIN_COMB_PERIODS),
            "rayleigh": round(r0, 4), "p": round(p, 4),
            "detected": bool(p < 0.05 and periods >= MIN_COMB_PERIODS)}


def _nrt_profile(fil: Path, dm: float, n1: int, n2: int, crop: float):
    """Reproduce the published prep_burst (Figure2+6.ipynb): Your reader -> Stokes I -> sub-bin
    super-dedispersion -> per-channel normalize -> S/N profile, cropped. Returns (tsamp, profile)."""
    import sys as _sys  # noqa: PLC0415
    if str(ECLAT) not in _sys.path:
        _sys.path.insert(0, str(ECLAT))
    import your  # noqa: PLC0415  (optional: only when the gitignored NRT data is present)
    import basic_funcs  # noqa: PLC0415
    import super_dedisperse  # noqa: PLC0415
    y = your.Your(str(fil))
    tsamp = float(y.your_header.tsamp)
    nstart = int((100e-3 / tsamp) - (10e-3 / tsamp))
    d = y.get_data(nstart, y.your_header.nspectra - nstart, npoln=4)
    si = d[:, 0, :].T + d[:, 1, :].T                        # Stokes I = AA + BB (NRT linear basis)
    si = super_dedisperse.super_dedisperse(si, dm, NRT_FREQS, tsamp, 10)
    si = basic_funcs.normalize(si, si[:, n1:n2])
    prof = np.mean(si, axis=0)
    off = prof[n1:n2]
    prof = (prof - np.mean(off)) / np.std(off)
    return tsamp, prof[: int(crop / tsamp)]


def _peak_fluxes(prof: np.ndarray, tsamp: float, times_ms: list[float], win: int = 2) -> np.ndarray:
    """Per-microshot peak S/N (local max within +/-win bins of the catalog time), in time order."""
    out = []
    for t in sorted(times_ms):
        b = int(round(t * 1e-3 / tsamp))
        lo, hi = max(0, b - win), min(len(prof), b + win + 1)
        out.append(float(np.max(prof[lo:hi])) if hi > lo else np.nan)
    return np.array(out)


def echo_ratio(amps: np.ndarray, rng: np.random.Generator) -> dict:
    """Consecutive microshot peak-flux ratios vs the recovery kernel, both channels (FRB.02 split):
    energy r=F_{n+1}/F_n vs {64/729,1/729}; amplitude sqrt(r) vs {8/27,1/27}. Null = within-burst
    shuffle of the fluxes (keeps the flux distribution, destroys order). A free-quotient placebo
    guards against numerology: the best off-kernel ratio must not beat the kernel."""
    a = amps[np.isfinite(amps) & (amps > 0)]
    if len(a) < 4:
        return {"n_ratios": 0, "energy": {}, "amplitude": {}, "supported": False}
    r = a[1:] / a[:-1]
    lr = np.log10(r)

    def _hits(targets, transform_log) -> int:
        x = transform_log(lr)
        return int(sum(np.sum(np.abs(x - math.log10(tt)) < RATIO_TOL_DEX)
                       + np.sum(np.abs(-x - math.log10(tt)) < RATIO_TOL_DEX) for tt in targets))

    def _channel(targets, transform_log) -> dict:
        obs = _hits(targets, transform_log)
        null = np.empty(N_NULL)
        for k in range(N_NULL):
            ash = rng.permutation(a)
            lrs = np.log10(ash[1:] / ash[:-1])
            xs = transform_log(lrs)
            null[k] = sum(np.sum(np.abs(xs - math.log10(tt)) < RATIO_TOL_DEX)
                          + np.sum(np.abs(-xs - math.log10(tt)) < RATIO_TOL_DEX) for tt in targets)
        mean_null = float(null.mean()) or 1e-9
        p = float((1 + np.sum(null >= obs)) / (N_NULL + 1))
        return {"obs": obs, "enrichment": round(obs / mean_null, 3), "p": round(p, 4)}

    en = _channel(ECHO_ENERGY, lambda x: x)              # energy: r vs lambda
    am = _channel(ECHO_AMP, lambda x: x / 2.0)           # amplitude: sqrt(r)=r^{1/2} -> log/2 vs sqrt(lambda)
    # free-quotient placebo: best arbitrary echo ratio in [0.02,0.5] must not beat the kernel
    qs = np.linspace(math.log10(0.02), math.log10(0.5), 40)
    best_free = max(int(np.sum(np.abs(lr - q) < RATIO_TOL_DEX) + np.sum(np.abs(-lr - q) < RATIO_TOL_DEX))
                    for q in qs)
    supported = bool((en["p"] < 0.05 and en["enrichment"] > 1.2 and en["obs"] >= best_free)
                     or (am["p"] < 0.05 and am["enrichment"] > 1.2 and am["obs"] >= best_free))
    return {"n_ratios": len(r), "energy": en, "amplitude": am,
            "best_free_quotient_hits": best_free, "supported": supported}


def analyze(seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    out = {"firewall": "search target (horizon-residual), not a claim",
           "source": "FRB 20220912A microshots, Hewitt et al. 2023 (MNRAS 526, 2039; Zenodo 10552561)",
           "kernel": {"clock_ratio": CLOCK_RATIO, "omega": OMEGA, "lambda": LAMBDA,
                      "wall": 3, "min_comb_periods": MIN_COMB_PERIODS},
           "bursts": {}}
    print("=" * 82)
    print("(B1) microshot cascade kernel test -- vetted Nançay ECLAT catalog (Hewitt+2023)")
    print(f"  clock ratio ln3/ln(3/2)={CLOCK_RATIO:.4f}  wall=N_fam=3  comb omega={OMEGA:.3f}")
    print("=" * 82)
    for name, times in (("B1", B1_TIMES_MS), ("B2", B2_TIMES_MS)):
        t = np.array(times)
        res = {"n_shots": len(t), "span_ms": round(float(t.max() - t.min()), 3),
               "gap_clock": gap_clock(t, rng), "wall": cascade_wall(t, rng),
               "time_comb": time_comb(t, rng), "echo": None}
        # amplitude (echo-ratio) extension, if the NRT filterbanks are present
        prep = NRT_PREP.get(name)
        if prep and (ECLAT / prep[0]).exists():
            try:
                tsamp, prof = _nrt_profile(ECLAT / prep[0], prep[1], prep[2], prep[3], prep[4])
                amps = _peak_fluxes(prof, tsamp, times)
                res["echo"] = echo_ratio(amps, rng)
                res["echo"]["peak_snr_range"] = [round(float(np.nanmin(amps)), 1),
                                                 round(float(np.nanmax(amps)), 1)]
            except Exception as e:  # noqa: BLE001
                res["echo"] = {"error": str(e)[:120]}
        out["bursts"][name] = res
        gc, wl, tc = res["gap_clock"], res["wall"], res["time_comb"]
        print(f"\n  [{name}] {len(t)} microshots over {res['span_ms']} ms")
        print(f"    gap clock 2.71: enrichment={gc['enrichment']} p={gc['p']} "
              f"placebo={gc['placebo_max_enr']} -> supported={gc['supported']}")
        print(f"    cascade wall:   longest decreasing-gap run={wl['longest_run']} "
              f"(null mean {wl['mean_null_run']}) p_deficit={wl['p_deficit']} -> supported={wl['supported']}")
        print(f"    time DSI comb:  periods={tc['periods']} (gate {MIN_COMB_PERIODS}) "
              f"rayleigh p={tc['p']} -> detected={tc['detected']}")
        ec = res["echo"]
        if ec and "energy" in ec and ec["energy"]:
            print(f"    echo ratio:     energy(64/729) enr={ec['energy']['enrichment']} p={ec['energy']['p']}"
                  f" | amp(8/27) enr={ec['amplitude']['enrichment']} p={ec['amplitude']['p']}"
                  f" | free-q max hits={ec['best_free_quotient_hits']} -> supported={ec['supported']}")
        elif ec and "error" in ec:
            print(f"    echo ratio:     SKIPPED ({ec['error']})")
        else:
            print("    echo ratio:     SKIPPED (NRT filterbanks not present; fetch Zenodo 10552561 nrt_data)")
    any_support = any(b["gap_clock"]["supported"] or b["wall"]["supported"] or b["time_comb"]["detected"]
                      or (b.get("echo") or {}).get("supported", False)
                      for b in out["bursts"].values())
    has_echo = any((b.get("echo") or {}).get("energy") for b in out["bursts"].values())
    out["verdict"] = (
        "NO microshot-cascade kernel signature on the vetted catalog: the gap ratio does not pile up "
        "at the clock 2.71 above a gap-shuffle null + placebo, there is no protected wall at 3, the "
        "time-DSI comb is not special (range-limited <2.8 periods), and"
        + (" the amplitude echo ratio is not enriched at 64/729 or 8/27 (a free quotient beats the "
           "kernel)" if has_echo else " the amplitude echo-ratio extension awaits the NRT flux data")
        + " -> clean NULL across all channels. No claim." if not any_support else
        "A microshot-cascade kernel feature SURVIVED a null in >=1 burst -> ESCALATE (independent "
        "cross-check), never a claim from N<=2 bursts.")
    print(f"\n==> {out['verdict']}")
    results = Path(__file__).resolve().parents[2] / "results" / "microshot_cascade.json"
    results.parent.mkdir(exist_ok=True)
    results.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {results}")
    return out


if __name__ == "__main__":
    analyze()
