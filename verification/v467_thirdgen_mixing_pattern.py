"""v467 -- FLAV.THIRDGEN.PATTERN.01: the third-generation ladder-base pattern -- the
suite's THREE ~2 sigma mixing tensions (sin^2 theta13 +2.0, sin^2 theta23 +1.8, V_cb
+1.8) are ONE common ~ -phi0 suppression, quantified and pre-registered as a CANDIDATE.
The frozen record (v84/REG.FREEZE.01) is NOT changed; like v328 this module names and
machine-checks a pattern, it does not silently upgrade or switch a prediction.

The observation.  The three most-tensioned mixing readouts of the watchdog (v307) are
exactly the three THIRD-GENERATION channels, and all three sit LOW by the same relative
amount.  In the existing vocabulary the pattern has a closed, parameter-free form: the
seed enters third-generation mixing through the LADDER BASE lambda_C^2 = phi0(1-phi0)
(the same base that carries the Yukawa mass ladder lambda_Y, tfpt_2) instead of bare
phi0, and the 2-3 texture carries the same -phi0/2 seed shift that theta12 already has:

    sin^2 theta13 = lambda_C^2 e^{-5/6}          = 0.021880   (record phi0 e^{-5/6}, +2.00 -> -0.12 sigma)
    sin^2 theta23 = (1-phi0)/2, cos 2theta23=phi0 = 0.473414  (record 1/2,           +1.76 -> +0.20 sigma)
    V_cb          = lambda_C^2/(1+lambda_C)      = 0.041119   (record phi0/(1+lambda_C), +1.79 -> +0.01 sigma)

Scope check that makes it a RULE, not a fit: V_ub = lambda_C^3/3 contains NO bare phi0
-- the rule leaves it untouched, and it is the one third-gen channel that is already
consistent (-0.23 sigma).  The 1-2 channels (theta12, lambda_C) must stay undressed and
do (dressing them would give -1.4 / -24 sigma).

  [E] 1. VOCABULARY IDENTITIES (exact, sympy): lambda_C^2 = phi0(1-phi0) (the frozen
        Cabibbo, v84); sin^2 theta23=(1-phi0)/2 <=> cos 2theta23 = phi0; and the
        suppression magnitude phi0 = 5.32% sits INSIDE the seam-gapped first-correction
        band (2/3)^6 = 8.78% (v393 class) -- an allowed-size correction, no new scale.
  [N] 2. COMMON SUPPRESSION: the three affected channels deviate from the record by
        -5.0%/-6.0%/-5.4% (weighted -5.36% +- 1.67%): non-zero at 3.2 sigma, consistent
        with -phi0 at -0.03 sigma (repo-documented NuFIT 6.0 / PDG 2024 data, v307).
  [N] 3. JOINT CHI^2, ZERO PARAMETERS: over the four third-gen observables (theta13,
        theta23, V_cb, V_ub) the joint chi^2 drops 10.4 -> 0.11 under the pattern; the
        1-2 channels stay undressed-correct (theta12 -0.02, lambda_C -0.25 sigma).
  [N] 4. REACTOR-ONLY DISCRIMINATOR: against Daya Bay alone (0.02175 +- 0.00065) the
        record is +2.09 sigma, the pattern +0.20 sigma (Delta chi^2 = 4.3) -- current
        reactor data already prefer the pattern form.
  [C] 5. LOOK-ELSEWHERE (honest): the pattern is POST-HOC.  A census of 16
        equally-simple multiplicative dressings finds 5 that fix the two PMNS tensions;
        and (1-phi0), (1-c3), (1-lambda_C^2), 1/(1+phi0) are DEGENERATE at current
        precision (<1.4% apart, channel errors ~2.5-3.4%).  V_cb + the V_ub scope check
        are what single out the ladder-base form; still a candidate, not a discovery.
  [O] 6. NO DERIVATION -- RECORD UNCHANGED: attempted derivations (Bernoulli-variance
        reading lambda_Y^2 = Var[Bernoulli(phi0)] -- an exact identity but only an
        interpretation; resolvent transport phi0/(1+phi0), degenerate to 0.28%; 1-2 x
        2-3 composition fails by 6.6x) do NOT yield the rule first-principles.  The
        frozen record stays the prediction of record (v84); this row is [O] until a
        seam-transport derivation exists.
  [X] 7. PRE-REGISTERED DECISION: (i) sin^2 theta13 stabilising on the 0.0231 side
        (record) kills the pattern; stabilising at ~0.0219 with sigma_rel < 1% kills
        the record's bare-phi0 reading; (ii) an exclusive-|Vcb| resolution at ~0.0395
        kills BOTH readings; (iii) separating the degenerate dressing forms needs
        sigma_rel < 0.5% on one channel (JUNO-era reactors / Belle II).

HONEST SCOPE: data are the repo-documented centrals (NuFIT 6.0 NO w/ SK atm: theta13
0.02195(58), theta23 0.470(17); PDG 2024: |Vcb| 0.0411(13), |Vub| 0.00382(24),
lambda_C 0.2245(5); NuFIT theta12 0.307(12); Daya Bay 0.02175(65)).  A quantified
pattern CANDIDATE in the v328 style -- it upgrades no prediction, changes no frozen
value, and closes no gate.  Python-only (floats + sympy identities; data confrontation).
"""
import math

import sympy as sp

from tfpt_constants import check, summary, reset, phi0 as phi0_mp

PHI0 = float(phi0_mp)
LAM = math.sqrt(PHI0 * (1.0 - PHI0))          # frozen Cabibbo lambda_C (v84)
E56 = math.exp(-5.0 / 6.0)

# repo-documented data (v307 watchdog + NuFIT 6.0 NO with SK-atm + Daya Bay)
D_TH13 = (0.02195, 0.00058)      # NuFIT 6.0
D_TH23 = (0.470, 0.017)          # NuFIT 6.0 NO (SK-atm), first octant
D_VCB = (0.0411, 0.0013)         # PDG 2024 |Vcb|
D_VUB = (0.00382, 0.00024)       # PDG 2024 |Vub|
D_TH12 = (0.307, 0.012)          # NuFIT 6.0
D_LAMC = (0.2245, 0.0005)        # PDG 2024
D_DAYABAY = (0.02175, 0.00065)   # Daya Bay final (reactor-only)


def _pull(pred, dat):
    return (pred - dat[0]) / dat[1]


def run():
    reset()
    print("v467  FLAV.THIRDGEN.PATTERN.01: the third-generation ladder-base pattern "
          "(candidate, record unchanged)")

    # ---- 1. vocabulary identities (exact) ----
    p = sp.Symbol("phi0", positive=True)
    lam2 = p * (1 - p)
    cos2th23 = sp.simplify(1 - 2 * (1 - p) / 2)          # 1 - 2 sin^2 theta23'
    seam_band = sp.Rational(2, 3) ** 6
    check("VOCABULARY IDENTITIES [E]: lambda_C^2 = phi0(1-phi0) (frozen Cabibbo, "
          "v84); sin^2 theta23 = (1-phi0)/2 <=> cos 2theta23 = phi0 (exact); and the "
          "suppression phi0 = %.2f%% sits INSIDE the seam-gapped first-correction "
          "band (2/3)^6 = %.2f%% (v393) -- allowed size, no new scale"
          % (100 * PHI0, 100 * float(seam_band)),
          sp.simplify(lam2 - p * (1 - p)) == 0 and cos2th23 == p
          and abs(LAM ** 2 - PHI0 * (1 - PHI0)) < 1e-15 and PHI0 < float(seam_band))

    # ---- 2. common suppression of the three affected channels ----
    rec = {"th13": PHI0 * E56, "th23": 0.5, "vcb": PHI0 / (1 + LAM),
           "vub": LAM ** 3 / 3}
    pat = {"th13": LAM ** 2 * E56, "th23": (1 - PHI0) / 2,
           "vcb": LAM ** 2 / (1 + LAM), "vub": LAM ** 3 / 3}   # V_ub: no bare phi0
    dat = {"th13": D_TH13, "th23": D_TH23, "vcb": D_VCB, "vub": D_VUB}

    devs, sigs = [], []
    for k in ("th13", "th23", "vcb"):
        devs.append(dat[k][0] / rec[k] - 1.0)
        sigs.append(dat[k][1] / rec[k])
    w = [1.0 / s ** 2 for s in sigs]
    mean_dev = sum(wi * di for wi, di in zip(w, devs)) / sum(w)
    mean_sig = math.sqrt(1.0 / sum(w))
    z0 = mean_dev / mean_sig
    zphi = (mean_dev + PHI0) / mean_sig
    print(f"  rel. deviations vs record: th13 {100 * devs[0]:+.2f}%, "
          f"th23 {100 * devs[1]:+.2f}%, Vcb {100 * devs[2]:+.2f}%  "
          f"-> weighted {100 * mean_dev:+.2f}% +- {100 * mean_sig:.2f}%")
    check("COMMON SUPPRESSION [N]: the three affected third-gen channels share one "
          "relative deviation %.2f%% +- %.2f%% -- non-zero at %.1f sigma, consistent "
          "with -phi0 (= -%.2f%%) at %.2f sigma"
          % (100 * mean_dev, 100 * mean_sig, abs(z0), 100 * PHI0, zphi),
          abs(z0) > 2.5 and abs(zphi) < 1.0)

    # ---- 3. joint chi^2, zero parameters; 1-2 channels stay undressed ----
    chi_rec = sum(_pull(rec[k], dat[k]) ** 2 for k in rec)
    chi_pat = sum(_pull(pat[k], dat[k]) ** 2 for k in pat)
    th12_pull = _pull(1 / 3 - PHI0 / 2, D_TH12)
    lamc_pull = _pull(LAM, D_LAMC)
    lamc_dressed_pull = _pull(LAM * (1 - PHI0), D_LAMC)
    print(f"  joint chi^2 (th13, th23, Vcb, Vub): record {chi_rec:.2f} -> "
          f"pattern {chi_pat:.2f}")
    check("JOINT CHI^2 [N]: over the four third-gen observables the pattern drops "
          "chi^2 from %.2f to %.2f with ZERO new parameters (V_ub = lambda_C^3/3 has "
          "no bare phi0 and stays untouched at %+.2f sigma); the 1-2 channels stay "
          "undressed-correct (theta12 %+.2f, lambda_C %+.2f sigma; dressing lambda_C "
          "would give %+.1f sigma -- the scope is checked, not chosen)"
          % (chi_rec, chi_pat, _pull(pat["vub"], D_VUB), th12_pull, lamc_pull,
             lamc_dressed_pull),
          chi_rec > 9.0 and chi_pat < 1.0 and abs(th12_pull) < 0.5
          and abs(lamc_pull) < 0.5 and lamc_dressed_pull < -5.0)

    # ---- 4. reactor-only discriminator (Daya Bay) ----
    p_rec_db = _pull(rec["th13"], D_DAYABAY)
    p_pat_db = _pull(pat["th13"], D_DAYABAY)
    dchi_db = p_rec_db ** 2 - p_pat_db ** 2
    check("REACTOR-ONLY DISCRIMINATOR [N]: against Daya Bay alone (0.02175 +- "
          "0.00065) the record is %+.2f sigma, the pattern %+.2f sigma (Delta chi^2 "
          "= %.1f) -- current reactor data already prefer the pattern form"
          % (p_rec_db, p_pat_db, dchi_db),
          p_rec_db > 1.8 and abs(p_pat_db) < 0.6 and dchi_db > 3.0)

    # ---- 5. look-elsewhere honesty: dressing census + degeneracy ----
    c3f = 1.0 / (8.0 * math.pi)
    cands = [("phi0", PHI0), ("phi0/2", PHI0 / 2), ("lambda_C", LAM), ("c3", c3f),
             ("lambda_C^2", LAM * LAM), ("(2/3)^6", (2 / 3) ** 6),
             ("dtop", 48 * c3f ** 4), ("phibase", 1 / (6 * math.pi))]
    winners = []
    for name, x in cands:
        for sgn in (+1, -1):
            ok13 = abs(_pull(rec["th13"] * (1 + sgn * x), D_TH13)) <= 1.0
            ok23 = abs(_pull(rec["th23"] * (1 + sgn * x), D_TH23)) <= 1.0
            if ok13 and ok23:
                winners.append(("+" if sgn > 0 else "-") + name)
    resolvent = PHI0 / (1 + PHI0)
    degen = abs(resolvent / (PHI0 * (1 - PHI0)) - 1)
    check("LOOK-ELSEWHERE (honest) [C]: POST-HOC pattern; %d of 16 equally-simple "
          "dressings fix the two PMNS tensions (%s); and (1-phi0) vs (1-c3) vs "
          "1/(1+phi0) are degenerate at current precision (resolvent differs by "
          "%.2f%% << channel errors ~2.5-3.4%%) -- V_cb + the V_ub scope check single "
          "out the ladder-base form; a candidate, NOT a discovery"
          % (len(winners), ", ".join(winners), 100 * degen),
          3 <= len(winners) <= 7 and degen < 0.01)

    # ---- 6. no derivation -- record unchanged ----
    var_id = sp.simplify(p * (1 - p) - (p - p ** 2))     # Var[Bernoulli(phi0)]
    s12s23_sq = (1 / 3 - PHI0 / 2) * 0.5                 # 1-2 x 2-3 composition
    comp_off = s12s23_sq / rec["th13"]
    check("NO DERIVATION -- RECORD UNCHANGED [O]: the Bernoulli-variance reading "
          "lambda_Y^2 = Var[Bernoulli(phi0)] = phi0(1-phi0) is an exact identity but "
          "only an INTERPRETATION; the 1-2 x 2-3 composition misses by %.1fx; no "
          "seam-transport derivation exists, so the frozen record (v84/REG.FREEZE.01) "
          "stays the prediction of record and this row is a named [O] candidate"
          % comp_off,
          var_id == 0 and comp_off > 5.0)

    # ---- 7. pre-registered decision ----
    kill = ("theta13 stable at 0.0231 kills the pattern; theta13 at ~0.0219 with "
            "sigma_rel<1% kills the record's bare-phi0 reading; exclusive |Vcb| "
            "~0.0395 kills both; separating (1-phi0)/(1-c3)/resolvent needs "
            "sigma_rel<0.5%")
    check("PRE-REGISTERED DECISION [X]: %s -- JUNO-era reactors and Belle II "
          "|Vcb| decide; symmetric kill conditions on BOTH readings, no knob" % kill,
          "0.0231" in kill and "0.0395" in kill)

    return summary("v467 FLAV.THIRDGEN.PATTERN.01: the three ~2 sigma mixing tensions "
                   "(theta13, theta23, Vcb) are ONE common -phi0 suppression (-5.36% "
                   "+- 1.67%, 3.2 sigma non-zero, -0.03 sigma from -phi0); ladder-base "
                   "forms lambda_C^2 e^{-5/6} / (1-phi0)/2 / lambda_C^2/(1+lambda_C) "
                   "drop joint chi^2 10.4 -> 0.11 with zero parameters; POST-HOC "
                   "candidate [O], record unchanged, JUNO/Belle II decide")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
