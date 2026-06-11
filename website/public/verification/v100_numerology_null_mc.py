"""v100 -- the numerology null test: look-elsewhere-corrected hit statistics.

Executes the long-standing TODO from the legacy CMB paper ("Numerology grammar
test: enumerate every reasonable algebraic combination of the primitives;
count how many also land within the observed windows") as a machine check of
the active suite.  It answers the only statistically meaningful form of the
question "is TFPT numerology?":

    Under an EXPLICIT null model -- random formulas drawn from a declared
    grammar that is at least as expressive as TFPT's own formula shapes,
    complexity-matched per observable -- what is the probability that a
    random "theory" reproduces the TFPT data scorecard?

Four layers:

  (A) EXACT LOOK-ELSEWHERE CENSUS.  For each scored observable the full
      grammar class is counted (no sampling): hit density p_i = (#expressions
      inside the observable's honest data window) / (#expressions inside the
      declared two-decade plausibility window).  The joint formula-fishing
      probability is prod p_i.  Robustness: the census is repeated with the
      coefficient bound and the plausibility window varied; the answer must
      be stable in order of magnitude.
  (B) MONTE CARLO over random dial settings (deterministic seeds): random
      rational coefficients inside TFPT's own formula skeletons -- with the
      seed phi0 fixed (MC-A) and with a random seed phi* drawn log-uniformly
      per pseudo-theory (MC-B).  Reported: hit-count distribution, maximum
      hits over all trials (TFPT scores 13/13 by construction).
  (C) NEGATIVE CONTROLS (the test must have power): perturbing the seed phi0
      by 1%/10%/30% collapses TFPT's own hit count; shuffling which measured
      value is assigned to which formula collapses it to ~0.
  (D) THE ALPHA CUBIC CLASS: all complexity-matched variants of the F_U1
      fixed-point equation (coefficients, M, transport exponent, resolvent
      power) are root-solved; only the TFPT equation lands within the
      achieved 4e-8 window of CODATA alpha^-1 -> p_alpha <= hits/N_class.

HONEST SCOPE (do not oversell):
  * No statistical test can give absolute certainty; the result is a
    look-elsewhere-corrected null probability CONDITIONAL on the declared
    grammar.  The grammar is published in full in the CONFIG block below and
    provably contains every TFPT formula it scores (fairness checks).
  * Data windows are conservative: each window is the MAXIMUM of TFPT's
    achieved deviation, the documented experimental sigma, the quote
    resolution of the documented central value, and (for quark ratios) the
    5% scheme-spread tolerance of v18.  Tension observables (theta13, s23,
    delta_CKM, m_mu/m_tau, beta) therefore enter with their honest LARGE
    windows and contribute almost nothing to the significance.
  * Measured centrals are exactly the ones already documented in this repo
    (predictions_frozen.json "experiment" fields, v62, v88, v18, tfpt_2
    tables); nothing is imported fresh for this test.
  * This is a numerical/statistical module (floats, RNG, numpy); it is
    Python-only by the suite's convention (like v62/v64/v65) and flagged as
    such in the Wolfram README.  Complementary to v84 (pre-registration
    freeze): v84 prevents future look-elsewhere drift, v100 quantifies the
    retrospective look-elsewhere burden.
"""
import json
import math
import os
import random
from fractions import Fraction

import numpy as np
import mpmath as mp

from tfpt_constants import check, summary, reset, phi0 as phi0_mp, c3 as c3_mp

# ---------------------------------------------------------------- CONFIG ----
PHI0 = float(phi0_mp)                    # retained seed (from c3 = 1/(8 pi))
LAM = math.sqrt(PHI0 * (1.0 - PHI0))     # Cabibbo lambda_C(phi0)
PI = math.pi
C3 = float(c3_mp)

# one-term grammar G1: value = (p/q) * phi^a * lam^c * (1+lam)^d * pi^b * e^(u/w)
G1_PQ_MAX = 130          # covers TFPT's largest coefficient 55/117
G1_A = range(-2, 3)      # phi exponent
G1_C = range(-3, 4)      # lambda exponent (s13 needs lam^3)
G1_D = range(-1, 2)      # (1+lam) exponent (s23 needs -1)
G1_B = range(-1, 2)      # pi exponent (beta needs -1)
G1_EXP_NUM, G1_EXP_DEN = 6, 6   # e^(u/w), |u|<=6, w<=6 (theta13 needs -5/6)

# two-term grammar G2: value = (p1/q1)*B1 +/- (p2/q2)*B2,
#   B = phi^a * lam^c * pi^b with a,c in 0..2, b in -1..1, coefficients <= 12
G2_PQ_MAX = 12
G2_A = range(0, 3)
G2_C = range(0, 3)
G2_B = range(-1, 2)

DECADE = 10.0            # plausibility window [m/DECADE, m*DECADE]
MC_TRIALS = 200_000
RNG_SEED = 20260611


def _half_ulp(s):
    """Half a unit-in-last-place of a documented decimal quote string."""
    if "." not in s:
        return 0.5
    return 0.5 * 10.0 ** (-len(s.split(".")[1]))


# ------------------------------------------------------- scored observables ----
# Measured centrals/sigmas are the repo-documented ones (see docstring).
# fields: id, predict(phi,lam), measured-quote, sigma (or None), extra window
# floor (quark scheme spread, v18), arity (1 or 2), TFPT G1/G2 encoding.
def _obs_table():
    return [
        # ---- two-term shapes (G2) ----
        dict(id="SIN2_THETA12", arity=2, quote="0.307", sigma=0.012, floor=0.0,
             pred=lambda f, l: 1.0 / 3.0 - f / 2.0,
             g2=((1, 3, 0, 0, 0), -1, (1, 2, 1, 0, 0)),
             src="NuFIT 6.0 (v62)"),
        dict(id="OMEGA_B", arity=2, quote="0.0493", sigma=None, floor=0.0,
             pred=lambda f, l: f - (f / 4.0) / PI,
             g2=((1, 1, 1, 0, 0), -1, (1, 4, 1, 0, -1)),
             src="Planck 2018 (registry)"),
        dict(id="DELTA_CKM_RAD", arity=2, quote="1.146681", sigma=3.0 * PI / 180.0,
             floor=0.0, cap=2.0 * PI,
             pred=lambda f, l: PI / 3.0 + 3.0 * l * l,
             g2=((1, 3, 0, 0, 1), +1, (3, 1, 0, 2, 0)),
             src="gamma_PDG 65.7 +- 3.0 deg (v88)"),
        # ---- one-term shapes (G1) ----
        dict(id="SIN2_THETA13", arity=1, quote="0.02195", sigma=0.00058, floor=0.0,
             pred=lambda f, l: f * math.exp(-5.0 / 6.0),
             g1=(1, 1, 1, 0, 0, 0, -5, 6), src="NuFIT 6.0 (v62)"),
        dict(id="BETA_RAD", arity=1, quote="0.00375246", sigma=0.074 * PI / 180.0,
             floor=0.0,
             pred=lambda f, l: f / (4.0 * PI),
             g1=(1, 4, 1, 0, 0, -1, 0, 1), src="ACT DR6 0.215+-0.074 deg (v62)"),
        dict(id="LAMBDA_C", arity=1, quote="0.2245", sigma=None, floor=0.0,
             pred=lambda f, l: l,
             g1=(1, 1, 0, 1, 0, 0, 0, 1), src="PDG (tfpt_2 CKM table)"),
        dict(id="S23_CKM", arity=1, quote="0.041", sigma=None, floor=0.0,
             pred=lambda f, l: f / (1.0 + l),
             g1=(1, 1, 1, 0, -1, 0, 0, 1), src="PDG ~0.041 (registry)"),
        dict(id="S13_CKM", arity=1, quote="0.0038", sigma=None, floor=0.0,
             pred=lambda f, l: l ** 3 / 3.0,
             g1=(1, 3, 0, 3, 0, 0, 0, 1), src="PDG ~0.0038 (registry)"),
        dict(id="MMU_OVER_MTAU", arity=1, quote="0.05946", sigma=None, floor=0.0,
             pred=lambda f, l: 8.0 / 7.0 * f,
             g1=(8, 7, 1, 0, 0, 0, 0, 1), src="PDG (registry)"),
        dict(id="ME_OVER_MMU", arity=1, quote="0.004836", sigma=None, floor=0.0,
             pred=lambda f, l: 12.0 / 7.0 * f * f,
             g1=(12, 7, 2, 0, 0, 0, 0, 1), src="PDG (registry)"),
        dict(id="MU_OVER_MD", arity=1, quote="0.47", sigma=None, floor=0.05,
             pred=lambda f, l: 55.0 / 117.0,
             g1=(55, 117, 0, 0, 0, 0, 0, 1), src="lattice/FLAG ~0.47 (v18 tol 5%)"),
        dict(id="MC_OVER_MS", arity=1, quote="13.6", sigma=None, floor=0.05,
             pred=lambda f, l: 34.0 / 47.0 / f,
             g1=(34, 47, -1, 0, 0, 0, 0, 1), src="PDG MSbar ~13.6 (v18 tol 5%)"),
        dict(id="MT_OVER_MB", arity=1, quote="41", sigma=None, floor=0.05,
             pred=lambda f, l: 3.0 / 26.0 / (f * f),
             g1=(3, 26, -2, 0, 0, 0, 0, 1), src="PDG ~41 (registry)"),
    ]


def build_observables():
    """Attach measured central m and conservative relative window w to each."""
    obs = _obs_table()
    for o in obs:
        m = float(o["quote"])
        pred = o["pred"](PHI0, LAM)
        achieved = abs(pred - m) / m
        sig = (o["sigma"] / m) if o["sigma"] else 0.0
        res = _half_ulp(o["quote"]) / m
        o["m"] = m
        o["pred_val"] = pred
        o["window"] = max(achieved, sig, res, o["floor"])
    return obs


# ------------------------------------------------ layer A: exact census ----
def g1_structures(phi, lam):
    """All G1 structure factors F = phi^a lam^c (1+lam)^d pi^b e^(u/w)."""
    exps = [(0, 1)] + [(u, w) for w in range(1, G1_EXP_DEN + 1)
                       for u in range(-G1_EXP_NUM, G1_EXP_NUM + 1)
                       if u != 0 and math.gcd(abs(u), w) == 1]
    fs = []
    for a in G1_A:
        for c in G1_C:
            for d in G1_D:
                for b in G1_B:
                    base = phi ** a * lam ** c * (1 + lam) ** d * PI ** b
                    for (u, w) in exps:
                        fs.append(base * math.exp(u / w))
    return np.array(fs)


def census_one_term(F, m, window, decade, pq_max, cap=None):
    """Count G1 expressions (p/q)*F inside the hit / plausibility windows."""
    lo_h, hi_h = m * (1 - window), m * (1 + window)
    lo_d, hi_d = m / decade, m * decade
    if cap is not None:
        hi_d = min(hi_d, cap)
    hits = dec = 0
    for q in range(1, pq_max + 1):
        for lo, hi, acc in ((lo_h, hi_h, "h"), (lo_d, hi_d, "d")):
            plo = np.ceil(q * lo / F)
            phi_ = np.floor(q * hi / F)
            cnt = np.clip(np.minimum(phi_, pq_max) - np.maximum(plo, 1) + 1,
                          0, None).sum()
            if acc == "h":
                hits += cnt
            else:
                dec += cnt
    return float(hits), float(dec)


def g2_terms(phi, lam, pq_max):
    """All G2 term values r*B (sorted numpy array)."""
    rats = [p / q for q in range(1, pq_max + 1) for p in range(1, pq_max + 1)
            if math.gcd(p, q) == 1]
    vals = []
    for a in G2_A:
        for c in G2_C:
            for b in G2_B:
                B = phi ** a * lam ** c * PI ** b
                vals.extend(r * B for r in rats)
    return np.sort(np.array(vals))


def census_two_term(T, m, window, decade, cap=None):
    """Count G2 expressions t1 +/- t2 inside the hit / plausibility windows."""
    lo_h, hi_h = m * (1 - window), m * (1 + window)
    lo_d, hi_d = m / decade, m * decade
    if cap is not None:
        hi_d = min(hi_d, cap)

    def count(lo, hi):
        # plus branch: t2 in [lo - t1, hi - t1]
        n = (np.searchsorted(T, hi - T, side="right")
             - np.searchsorted(T, lo - T, side="left")).sum()
        # minus branch: t2 in [t1 - hi, t1 - lo]
        n += (np.searchsorted(T, T - lo, side="right")
              - np.searchsorted(T, T - hi, side="left")).sum()
        return float(n)

    return count(lo_h, hi_h), count(lo_d, hi_d)


def run_census(obs, pq1, pq2, decade):
    F = g1_structures(PHI0, LAM)
    T = g2_terms(PHI0, LAM, pq2)
    out = {}
    for o in obs:
        cap = o.get("cap")
        if o["arity"] == 1:
            h, d = census_one_term(F, o["m"], o["window"], decade, pq1, cap)
        else:
            h, d = census_two_term(T, o["m"], o["window"], decade, cap)
        out[o["id"]] = (h, d, h / d if d else 1.0)
    return out


# ----------------------------------------- layer B: Monte Carlo pseudo-theories ----
def _rat(rng, pmax):
    return (int(rng.random() * pmax) + 1) / (int(rng.random() * pmax) + 1)


def random_theory_values(rng, phi, lam):
    """Random rational dials inside TFPT's own 13 formula skeletons."""
    eu = int(rng.random() * (2 * G1_EXP_NUM + 1)) - G1_EXP_NUM
    ew = int(rng.random() * G1_EXP_DEN) + 1
    return [
        _rat(rng, 12) - _rat(rng, 12) * phi,                  # theta12
        _rat(rng, 12) * phi - _rat(rng, 12) * phi / PI,       # Omega_b
        _rat(rng, 12) * PI + _rat(rng, 12) * lam * lam,       # delta_CKM
        _rat(rng, 12) * phi * math.exp(eu / ew),              # theta13
        _rat(rng, 12) * phi / PI,                             # beta (rad)
        _rat(rng, 12) * lam,                                  # lambda_C
        _rat(rng, 12) * phi / (1.0 + lam),                    # s23
        _rat(rng, 12) * lam ** 3,                             # s13
        _rat(rng, 12) * phi,                                  # mmu/mtau
        _rat(rng, 12) * phi * phi,                            # me/mmu
        _rat(rng, 130),                                       # mu/md
        _rat(rng, 130) / phi,                                 # mc/ms
        _rat(rng, 130) / (phi * phi),                         # mt/mb
    ]


MC_ORDER = ["SIN2_THETA12", "OMEGA_B", "DELTA_CKM_RAD", "SIN2_THETA13",
            "BETA_RAD", "LAMBDA_C", "S23_CKM", "S13_CKM", "MMU_OVER_MTAU",
            "ME_OVER_MMU", "MU_OVER_MD", "MC_OVER_MS", "MT_OVER_MB"]


def hit_count(values, obs_by_id):
    k = 0
    for oid, v in zip(MC_ORDER, values):
        o = obs_by_id[oid]
        if abs(v - o["m"]) <= o["window"] * o["m"]:
            k += 1
    return k


def run_mc(obs_by_id, trials, seed, random_seed_constant):
    rng = random.Random(seed)
    counts = [0] * 14
    for _ in range(trials):
        if random_seed_constant:
            phi = math.exp(rng.random() * (math.log(0.5) - math.log(0.005))
                           + math.log(0.005))
        else:
            phi = PHI0
        lam = math.sqrt(phi * (1.0 - phi))
        counts[hit_count(random_theory_values(rng, phi, lam), obs_by_id)] += 1
    return counts


# --------------------------------------------- layer D: the alpha cubic class ----
def alpha_class_census():
    """Root-solve every complexity-matched F_U1 variant; count CODATA hits.

    TFPT instance: r1=2, r2=4/5, M=41, transport e^(-2a), resolvent power -5/4.
    """
    pb = 1.0 / (6.0 * PI)
    dt = 48.0 * C3 ** 4
    r1s = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    r2s = np.array(sorted({float(Fraction(p, q))
                           for p in range(1, 11) for q in range(1, 6)}))
    Ms = np.arange(1, 61, dtype=float)
    ts = np.array([1.0, 2.0, 3.0])
    pws = np.array([-1.25, -1.0, -0.5])

    R1, R2, M, T, PW = np.meshgrid(r1s, r2s, Ms, ts, pws, indexing="ij")
    R1, R2, M, T, PW = (x.ravel() for x in (R1, R2, M, T, PW))
    n = R1.size

    lo = np.full(n, 1e-4)
    hi = np.full(n, 0.2)

    def f(a):
        Q = dt * np.exp(-T * a)
        ps = pb + Q * (1.0 - Q) ** PW
        return a ** 3 - R1 * C3 ** 3 * a ** 2 - R2 * C3 ** 6 * M * np.log(1.0 / ps)

    flo = f(lo)
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        left = (flo * fm) <= 0
        hi = np.where(left, mid, hi)
        lo = np.where(left, lo, mid)
        flo = np.where(left, flo, fm)
    roots = 0.5 * (lo + hi)
    ainv = 1.0 / roots

    codata = 137.035999177          # CODATA 2022 (v62)
    window = 4.0e-8                 # TFPT's achieved |Delta(alpha^-1)|, >= sigma
    hits = int(np.sum(np.abs(ainv - codata) <= window))

    # fairness: the TFPT combination is in the grid and reproduces the root
    sel = ((R1 == 2.0) & (np.abs(R2 - 0.8) < 1e-12) & (M == 41.0)
           & (T == 2.0) & (PW == -1.25))
    tfpt_ainv = float(ainv[sel][0])
    return n, hits, tfpt_ainv


# ----------------------------------------------------------------- driver ----
def run():
    reset()
    print("v100 numerology null test (look-elsewhere census + MC + controls)")

    obs = build_observables()
    obs_by_id = {o["id"]: o for o in obs}

    # (0) registry lock: the scored predictions are the frozen ones
    reg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "predictions_frozen.json")
    with open(reg_path) as fh:
        reg = {e["id"]: e["frozen_value"] for e in json.load(fh)["predictions"]}
    reg_map = {"SIN2_THETA12": "SIN2_THETA12_SEED", "BETA_RAD": None,
               "DELTA_CKM_RAD": "DELTA_CKM_RAD"}
    ok_reg = True
    for o in obs:
        rid = reg_map.get(o["id"], o["id"])
        if rid is None:
            continue
        ok_reg &= abs(o["pred_val"] - float(reg[rid])) <= 1e-9 * abs(float(reg[rid]))
    check("scored predictions == frozen registry values (v84 lock, 13 obs)", ok_reg)

    # (A) exact census at the declared budgets
    cen = run_census(obs, G1_PQ_MAX, G2_PQ_MAX, DECADE)
    log10_joint = 0.0
    print("  --- per-observable hit densities (exact census) ---")
    for o in obs:
        h, d, p = cen[o["id"]]
        log10_joint += math.log10(p)
        print(f"    {o['id']:<16} window {o['window']:9.2e}  "
              f"p_i = {h:>9.0f}/{d:>11.0f} = {p:9.3e}   [{o['src']}]")
    print(f"  joint formula-fishing probability prod p_i = 1e{log10_joint:.2f}")

    check("fairness: every TFPT formula is inside its declared grammar class "
          "(13/13 reconstruct)", fairness_reconstruct(obs))
    check("every per-observable density p_i < 1 (the class never trivialises)",
          all(cen[o["id"]][2] < 1.0 for o in obs))
    check("joint null probability prod p_i < 1e-12 (look-elsewhere corrected)",
          log10_joint < -12.0)

    # (A') robustness: budget and window variations stay in the same regime
    var = []
    for pq1, pq2, dec in ((80, 8, 10.0), (200, 16, 10.0),
                          (130, 12, 5.0), (130, 12, 20.0)):
        c2 = run_census(obs, pq1, pq2, dec)
        var.append(sum(math.log10(c2[o["id"]][2]) for o in obs))
    spread = max(abs(v - log10_joint) for v in var)
    print(f"  robustness: log10 joint under budget/window variation: "
          f"{[f'{v:.1f}' for v in var]} (max shift {spread:.2f} dex)")
    check("census robust: coefficient bound 80..200 and window 5x..20x shift "
          "log10(prod p_i) by < 3 dex", spread < 3.0)

    # (B) Monte Carlo pseudo-theories (deterministic seeds)
    cA = run_mc(obs_by_id, MC_TRIALS, RNG_SEED, random_seed_constant=False)
    cB = run_mc(obs_by_id, MC_TRIALS, RNG_SEED + 1, random_seed_constant=True)
    maxA = max(k for k, n in enumerate(cA) if n)
    maxB = max(k for k, n in enumerate(cB) if n)
    meanA = sum(k * n for k, n in enumerate(cA)) / MC_TRIALS
    meanB = sum(k * n for k, n in enumerate(cB)) / MC_TRIALS
    print(f"  MC-A (phi0 fixed, random dials): mean K = {meanA:.3f}, "
          f"max K = {maxA}/13 over {MC_TRIALS} trials; dist {cA[:maxA+1]}")
    print(f"  MC-B (random seed phi*):         mean K = {meanB:.3f}, "
          f"max K = {maxB}/13 over {MC_TRIALS} trials; dist {cB[:maxB+1]}")
    check(f"MC-A: no random-dial theory reaches 10/13 hits in {MC_TRIALS} "
          f"trials (TFPT: 13/13); observed max {maxA}", maxA < 10)
    check(f"MC-B: no random-seed theory reaches 10/13 hits in {MC_TRIALS} "
          f"trials; observed max {maxB}", maxB < 10)
    check("MC means are far below the scorecard (mean K < 2 in both runs)",
          meanA < 2.0 and meanB < 2.0)

    # (C) negative controls -- the test has power
    tfpt_vals = [o["pred_val"] for o in
                 (obs_by_id[i] for i in MC_ORDER)]
    check("control: TFPT's own dial settings score 13/13 (plumbing)",
          hit_count(tfpt_vals, obs_by_id), 13, exact=True)

    def k_at(eps):
        best = 0
        for s in (+1, -1):
            f = PHI0 * (1.0 + s * eps)
            l = math.sqrt(f * (1.0 - f))
            vals = [obs_by_id[i]["pred"](f, l) for i in MC_ORDER]
            best = max(best, hit_count(vals, obs_by_id))
        return best
    k001, k01, k03 = k_at(0.01), k_at(0.10), k_at(0.30)
    print(f"  seed-perturbation collapse: K(+-1%)={k001}, K(+-10%)={k01}, "
          f"K(+-30%)={k03}  (vs 13/13 at phi0)")
    check("control: perturbing phi0 by 1% collapses the scorecard (K <= 9)",
          k001 <= 9)
    check("control: perturbing phi0 by 10% collapses the scorecard (K <= 6)",
          k01 <= 6)

    rng = random.Random(RNG_SEED + 2)
    tot = mx = 0
    for _ in range(1000):
        perm = list(range(13))
        rng.shuffle(perm)
        k = sum(1 for i, j in enumerate(perm)
                if abs(tfpt_vals[i] - obs_by_id[MC_ORDER[j]]["m"])
                <= obs_by_id[MC_ORDER[j]]["window"] * obs_by_id[MC_ORDER[j]]["m"])
        tot += k
        mx = max(mx, k)
    print(f"  shuffled-data control: mean K = {tot/1000:.2f}, max K = {mx} "
          f"over 1000 permutations")
    check("control: shuffling data<->formula assignment collapses the "
          "scorecard (mean K <= 2, max K <= 6)", tot / 1000 <= 2.0 and mx <= 6)

    # (D) the alpha cubic class
    n_alpha, hits_alpha, tfpt_ainv = alpha_class_census()
    p_alpha = max(hits_alpha, 1) / n_alpha
    print(f"  alpha class: {n_alpha} F_U1 variants root-solved; "
          f"{hits_alpha} inside the 4e-8 CODATA window; p_alpha <= {p_alpha:.1e}")
    check("alpha fairness: the TFPT F_U1 instance is in the class and "
          "reproduces the frozen root", abs(tfpt_ainv - 137.0359992168407)
          < 1e-6)
    check("alpha look-elsewhere: at most 3 of the F_U1 variants hit the "
          f"4e-8 CODATA window (observed {hits_alpha})",
          1 <= hits_alpha <= 3)
    check("alpha null probability p_alpha < 1e-4", p_alpha < 1e-4)

    # headline
    log10_total = log10_joint + math.log10(p_alpha)
    print(f"  HEADLINE: P(random complexity-matched theory reproduces the "
          f"scorecard incl. alpha) <= 1e{log10_total:.1f}")
    print(f"            = {-log10_total * math.log2(10):.0f} bits of "
          f"look-elsewhere-corrected surprise (conditional on the declared "
          f"grammar; never 'certainty')")
    check("headline: joint null probability (13 obs + alpha) < 1e-16",
          log10_total < -16.0)

    return summary("v100 numerology null test")


def fairness_reconstruct(obs):
    """Re-evaluate every TFPT formula from its declared grammar encoding."""
    ok = True
    for o in obs:
        if o["arity"] == 1:
            p, q, a, c, d, b, u, w = o["g1"]
            ok &= (1 <= p <= G1_PQ_MAX and 1 <= q <= G1_PQ_MAX
                   and a in G1_A and c in G1_C and d in G1_D and b in G1_B
                   and abs(u) <= G1_EXP_NUM and 1 <= w <= G1_EXP_DEN)
            v = (p / q) * PHI0 ** a * LAM ** c * (1 + LAM) ** d * PI ** b \
                * math.exp(u / w)
        else:
            (p1, q1, a1, c1, b1), sgn, (p2, q2, a2, c2, b2) = o["g2"]
            ok &= all(1 <= x <= G2_PQ_MAX for x in (p1, q1, p2, q2))
            ok &= (a1 in G2_A and c1 in G2_C and b1 in G2_B
                   and a2 in G2_A and c2 in G2_C and b2 in G2_B)
            v = ((p1 / q1) * PHI0 ** a1 * LAM ** c1 * PI ** b1
                 + sgn * (p2 / q2) * PHI0 ** a2 * LAM ** c2 * PI ** b2)
        ok &= abs(v - o["pred_val"]) <= 1e-12 * max(abs(o["pred_val"]), 1e-30)
    return ok


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
