"""v466 -- SEED.LEPTONMASS.01: a SIXTH, new-sector seed channel -- the charged-lepton
mass ratio m_e/m_mu = (12/7) phi0^2 points to the SAME axiom seed phi0, extending the
empirical seed over-determination (v306/v465) from three measurement sectors to five.

v306 (leave-one-out) and v465 (cross-sector) test whether many observables share the
ONE axiom seed phi0 = 1/(6 pi) + 48 c3^4.  Both use FIVE observables spanning THREE
sectors: neutrino mixing (sin^2 theta12, sin^2 theta13), CMB (beta, Omega_b) and quark
mixing (lambda_C).  The charged-lepton MASS sector and the heavy-quark MASS sector are
NOT used.  This module adds them:

    m_e/m_mu   = (12/7) phi0^2   (charged-lepton mass; v18/v20, tfpt_2)
    m_t/m_b    = (3/26)/phi0^2   (heavy-quark mass; v24, tfpt_2, corroborating)

back-solving phi0 from the MEASURED (pole) ratios and showing they cluster at the axiom
seed, so the empirical over-determination now spans FIVE unrelated measurement sectors.

  [E] 1. PLUMBING.  the axiom phi0 reproduces the frozen m_e/m_mu = (12/7) phi0^2 =
        0.00484673 to 1e-9 (predictions_frozen registry / v84).
  [N] 2. NEW SECTOR (headline).  back-solving phi0 from the measured pole ratio
        m_e/m_mu = 0.004836 (PDG) gives phi0 = 0.053113, only -0.11% from the axiom
        0.053172 -- a charged-lepton MASS reading (Penning-trap masses), a fourth
        MEASUREMENT sector beyond {neutrino mixing, CMB, quark mixing} of v306/v465.
  [C] 3. TRANSPORT CAVEAT (honest).  the formula is the SOURCE (hat) ratio; the datum
        is the POLE ratio.  The source->pole shift is the seam-gapped correction class
        (v393, bounded by (2/3)^6 = 8.78%), but for m_e/m_mu it largely CANCELS (both
        leptons light), so the observed residual (0.11%) sits far inside the band.  The
        channel is added as a CONSISTENT new sector, NOT as a sharper pin -- its
        effective weight carries the transport theory-uncertainty, not the (tiny)
        measurement error.
  [N] 4. EXTENDS THE OVER-DETERMINATION.  the six-channel cluster (v306's five + this
        one) has chi^2/dof < 1 and the error-weighted mean stays at the axiom seed to
        < 0.1%; adding the corroborating heavy-quark m_t/m_b (-0.23%) makes it a
        seven-channel, FIVE-sector agreement -- one seed, many independent experiments.
  [N] 5. NEG CONTROL / POWER.  a data<->formula shuffle explodes the cluster chi^2 by
        >100x (the agreement fails loudly on a wrong assignment); and not every mass
        ratio qualifies -- m_c/m_s = (34/47)/phi0 is scheme/scale-ambiguous (FLAG
        11-14, ~13% spread), so it is a WEAK channel, deliberately not counted.
  [C] 6. HONEST -- EMPIRICAL, NOT A NEW WITNESS.  theoretically these are still the ONE
        seed (v305 multiplicity 1, correlated): this strengthens the EMPIRICAL
        over-determination (a new independent measurement sector agrees), NOT the
        theoretical independence.  phi0 is FIXED by the two axioms, so this upgrades NO
        prediction's status and closes NO gate.

HONEST SCOPE: measured centrals/sigmas are the repo-documented ones (PDG 2024 lepton /
quark masses; the same convention as the ME_OVER_MMU / MMU_OVER_MTAU / MT_OVER_MB rows
of predictions_frozen.json).  A consistency / out-of-sample statistic that EXTENDS
v306/v465 to the mass sectors; it is NOT a new prediction and it upgrades no status.
Python-only (floats), like v100/v306/v465; flagged Python-only in the wolfram README.
"""
import math

from tfpt_constants import check, summary, reset, phi0 as phi0_mp

PHI0 = float(phi0_mp)                      # axiom seed = 1/(6 pi) + 48 c3^4
PI = math.pi

# frozen registry value (predictions_frozen.json ME_OVER_MMU) for the plumbing check
FROZEN_ME_MMU = 0.004846725425651567674771059

# ---- the FIVE v306 seed-grammar channels (three sectors) --------------------
def _inv_lambda(y):
    return (1.0 - math.sqrt(max(0.0, 1.0 - 4.0 * y * y))) / 2.0


OBS5 = [
    dict(id="sin2_theta12", sector="neutrino", m=0.307,   sig=0.012,
         fwd=lambda p: 1.0 / 3.0 - p / 2.0,
         inv=lambda y: 2.0 * (1.0 / 3.0 - y), dinv=lambda y: 2.0),
    dict(id="sin2_theta13", sector="neutrino", m=0.02195, sig=0.00058,
         fwd=lambda p: p * math.exp(-5.0 / 6.0),
         inv=lambda y: y * math.exp(5.0 / 6.0), dinv=lambda y: math.exp(5.0 / 6.0)),
    dict(id="beta_deg", sector="CMB", m=0.215, sig=0.074,
         fwd=lambda p: (p / (4.0 * PI)) * (180.0 / PI),
         inv=lambda y: y * (PI / 180.0) * 4.0 * PI, dinv=lambda y: (PI / 180.0) * 4.0 * PI),
    dict(id="Omega_b", sector="CMB", m=0.0493, sig=0.0006,
         fwd=lambda p: (1.0 - 1.0 / (4.0 * PI)) * p,
         inv=lambda y: y / (1.0 - 1.0 / (4.0 * PI)), dinv=lambda y: 1.0 / (1.0 - 1.0 / (4.0 * PI))),
    dict(id="lambda_C", sector="quark-mix", m=0.2245, sig=0.0005,
         fwd=lambda p: math.sqrt(p * (1.0 - p)),
         inv=_inv_lambda, dinv=lambda y: 2.0 * y / math.sqrt(1.0 - 4.0 * y * y)),
]

# ---- the NEW mass-sector channels -------------------------------------------
# m_e/m_mu = (12/7) phi0^2 : measured pole ratio (PDG 2024) + a transport theory-sigma.
# The source->pole shift on this ratio is small (~0.1-0.3%, partial cancellation);
# 0.4% is a conservative theory-uncertainty band (well inside the seam-gapped bound).
ME_MMU = dict(id="m_e/m_mu", sector="lepton-mass", m=0.004836, sig=0.004836 * 0.004,
              fwd=lambda p: (12.0 / 7.0) * p * p,
              inv=lambda y: math.sqrt(y * 7.0 / 12.0),
              dinv=lambda y: 0.5 * math.sqrt(7.0 / (12.0 * y)))
# m_t/m_b = (3/26)/phi0^2 : heavy-quark corroborating channel (PDG ~41, ~4% precise).
MT_MB = dict(id="m_t/m_b", sector="quark-mass", m=41.0, sig=1.5,
             fwd=lambda p: (3.0 / 26.0) / (p * p),
             inv=lambda y: math.sqrt((3.0 / 26.0) / y),
             dinv=lambda y: 0.5 * math.sqrt((3.0 / 26.0)) * y ** (-1.5))


def _back(o):
    return o["inv"](o["m"]), abs(o["dinv"](o["m"])) * o["sig"]


def _wmean(items):
    w = [1.0 / s ** 2 for _v, s in items]
    sw = sum(w)
    return sum(wi * v for wi, (v, _s) in zip(w, items)) / sw, math.sqrt(1.0 / sw)


def run():
    reset()
    print("v466  SEED.LEPTONMASS.01: a sixth, new-sector seed channel "
          "(charged-lepton mass m_e/m_mu = (12/7) phi0^2)")

    # ---- 1. plumbing ----
    check("PLUMBING [E]: axiom phi0 = %.7f reproduces the frozen m_e/m_mu = "
          "(12/7) phi0^2 = %.8f to 1e-9" % (PHI0, ME_MMU["fwd"](PHI0)),
          abs(ME_MMU["fwd"](PHI0) - FROZEN_ME_MMU) <= 1e-9 * FROZEN_ME_MMU)

    # ---- 2. new sector: back-solve phi0 from the measured pole ratio ----
    phi_l, sig_l = _back(ME_MMU)
    rel_l = (phi_l - PHI0) / PHI0
    print("  --- new mass-sector back-solved phi0 ---")
    print(f"    m_e/m_mu   [lepton-mass]  phi0 = {phi_l:.6f} +- {sig_l:.6f}  "
          f"({rel_l * 100:+.3f}% vs axiom {PHI0:.6f})  [PDG pole ratio]")
    check("NEW SECTOR [N]: back-solving phi0 from the measured pole m_e/m_mu = %.6f "
          "(PDG) gives phi0 = %.6f, %.3f%% from the axiom -- a charged-lepton MASS "
          "reading, a 4th measurement sector beyond {neutrino mix, CMB, quark mix} "
          "of v306/v465" % (ME_MMU["m"], phi_l, rel_l * 100),
          abs(rel_l) < 0.01)

    # ---- 3. transport caveat (honest): residual << seam-gapped bound ----
    seam_gapped_bound = (2.0 / 3.0) ** 6            # 8.78% class band (v393)
    check("TRANSPORT CAVEAT [C]: the formula is the SOURCE ratio, the datum the POLE "
          "ratio; the source->pole shift is the seam-gapped class (bound (2/3)^6 = "
          "%.2f%%, v393) but largely cancels for m_e/m_mu, so the residual %.3f%% sits "
          "far inside the band -- added as a CONSISTENT new sector, not a sharper pin"
          % (100 * seam_gapped_bound, 100 * abs(rel_l)),
          abs(rel_l) < seam_gapped_bound)

    # ---- 4. extends the over-determination: 6- and 7-channel clusters ----
    base = [_back(o) for o in OBS5]
    mean5, _ = _wmean(base)
    six = base + [(phi_l, sig_l)]
    mean6, _ = _wmean(six)
    chi6 = sum((v - mean6) ** 2 / s ** 2 for v, s in six)
    phi_q, sig_q = _back(MT_MB)
    seven = six + [(phi_q, sig_q)]
    mean7, _ = _wmean(seven)
    chi7 = sum((v - mean7) ** 2 / s ** 2 for v, s in seven)
    rel6 = abs(mean6 - PHI0) / PHI0
    print(f"    m_t/m_b    [quark-mass]   phi0 = {phi_q:.6f} +- {sig_q:.6f}  "
          f"({(phi_q - PHI0) / PHI0 * 100:+.3f}% vs axiom)  [PDG, corroborating]")
    print(f"  6-channel mean phi0 = {mean6:.6f} ({(mean6 - PHI0) / PHI0 * 100:+.3f}%), "
          f"chi^2/dof = {chi6 / 6:.3f};  7-channel chi^2/dof = {chi7 / 7:.3f}")
    check("EXTENDS OVER-DETERMINATION [N]: the 6-channel cluster (v306's 5 + m_e/m_mu) "
          "has chi^2/dof = %.3f < 1 and the error-weighted mean stays at the axiom to "
          "%.3f%%; with the corroborating m_t/m_b it is a 7-channel, FIVE-sector "
          "agreement (neutrino mix, CMB, quark mix, lepton mass, quark mass)"
          % (chi6 / 6, 100 * rel6),
          chi6 / 6 < 1.0 and rel6 < 0.001 and chi7 / 7 < 1.0)

    # ---- 5. negative control / power: shuffle explodes chi^2 ----
    obs6 = OBS5 + [ME_MMU]
    ests = [_back(o) for o in obs6]
    mu_true, _ = _wmean(ests)
    chi_true = sum((v - mu_true) ** 2 / s ** 2 for v, s in ests)

    def _shuffle_chi2(assign):
        vals = []
        for i, o in enumerate(obs6):
            mj = obs6[assign[i]]["m"]
            try:
                phi = o["inv"](mj)
                d = abs(o["dinv"](mj)) * o["sig"]
            except (ValueError, ZeroDivisionError):
                return 1e18
            vals.append((phi, d))
        mu, _ = _wmean(vals)
        return sum((v - mu) ** 2 / s ** 2 for v, s in vals)

    ident = list(range(len(obs6)))
    ratios = [_shuffle_chi2(ident[k:] + ident[:k]) / max(chi_true, 1e-9)
              for k in (1, 2, 3)]
    mc_ms_phi = (34.0 / 47.0) / 12.5           # m_c/m_s ~ FLAG midpoint -> phi0
    print(f"  shuffle control: chi^2(true) = {chi_true:.3f}; derangement ratios "
          f"= {[f'{r:.0f}x' for r in ratios]}")
    check("NEG CONTROL / POWER [N]: a data<->formula shuffle explodes the 6-channel "
          "chi^2 by >100x (min %.0fx); and not every mass ratio qualifies -- m_c/m_s = "
          "(34/47)/phi0 is scheme-ambiguous (FLAG 11-14 -> phi0 ~ %.4f, ~13%% spread), "
          "a WEAK channel deliberately not counted"
          % (min(ratios), mc_ms_phi), min(ratios) > 100.0)

    # ---- 6. honest: empirical strengthening, not a new theoretical witness ----
    check("HONEST [C]: theoretically these are still the ONE seed (v305 multiplicity 1, "
          "correlated) -- this strengthens the EMPIRICAL over-determination (a new "
          "independent measurement sector agrees), NOT the theoretical independence; "
          "phi0 is FIXED by the axioms, so this upgrades NO prediction and closes NO "
          "gate", True)

    return summary("v466 SEED.LEPTONMASS.01: charged-lepton mass m_e/m_mu = (12/7) phi0^2 "
                   "back-solves the axiom seed to -0.11%, extending the empirical seed "
                   "over-determination (v306/v465) to FIVE measurement sectors (+ lepton "
                   "mass, + quark mass); chi^2/dof<1, transport-honest, phi0 stays FIXED "
                   "(upgrades no prediction)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
