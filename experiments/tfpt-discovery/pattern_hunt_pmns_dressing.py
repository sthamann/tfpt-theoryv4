"""Pattern hunt 2026-07-02 -- exploratory, NOT load-bearing (tfpt-discovery sandbox).

Question: do the two standing PMNS tensions (sin^2 theta13 +2.0 sigma, sin^2 theta23
+1.76 sigma vs NuFIT 6.0) share ONE parameter-free structure inside the existing
TFPT vocabulary?  Candidate: the "atmospheric-sector dressing" -- multiply the
third-column readouts by (1 - phi0):

    sin^2 theta13 = phi0 (1 - phi0) e^{-5/6}  =  lambda_C^2 e^{-5/6}
    sin^2 theta23 = (1/2)(1 - phi0)           =  1/2 - phi0/2

Note the second form: theta23 then carries EXACTLY the same "-phi0/2" seam shift
that theta12 already carries (sin^2 theta12 = 1/3 - phi0/2, frozen record).
Relative size of both shifts = phi0 = 5.32% < (2/3)^6 = 8.78%, i.e. inside the
seam-gapped transport-correction bound (v393 class).

Second candidate: dm21^2/dm31^2 = |J_PMNS| (both sides fully fixed by frozen
TFPT angles+phase; the splitting ratio is currently NOT predicted at all).

Everything below is typed [P]-candidate / post-hoc; the honest look-elsewhere
burden is quantified with a v100-style grammar census.
"""
import math

import numpy as np
import mpmath as mp

mp.mp.dps = 40

# ---------------------------------------------------------------- primitives
PI = mp.pi
c3 = 1 / (8 * PI)
phibase = 1 / (6 * PI)
dtop = 48 * c3 ** 4
phi0 = phibase + dtop
PHI0 = float(phi0)

# frozen-registry Cabibbo (check both definitions against the frozen decimal)
FROZEN_LAM = mp.mpf("0.2243762368847217731120972")
lam_phi0 = mp.sqrt(phi0 * (1 - phi0))
lam_base = mp.sqrt(phibase * (1 - phibase))
LAM = float(lam_phi0)

E56 = math.exp(-5.0 / 6.0)

# ---------------------------------------------------------------- data (repo-documented)
# NuFIT 6.0 (as used in v62/v307 and experiments/neutrino-mixing)
S212_M, S212_S = 0.307, 0.012
S213_M, S213_S = 0.02195, 0.00058
S223_M, S223_S = 0.470, 0.017
# reactor-only combination (experiments/seed-consistency v3)
S213_R_M, S213_R_S = 0.02204, 0.00059
# NuFIT 6.0 NO splittings
DM21, DM21_S = 7.49e-5, 0.19e-5
DM31, DM31_S = 2.513e-3, 0.021e-3


def pull(pred, m, s):
    return (pred - m) / s


def jarlskog(s212, s213, s223, delta_deg):
    s12, c12 = math.sqrt(s212), math.sqrt(1 - s212)
    s13, c13 = math.sqrt(s213), math.sqrt(1 - s213)
    s23, c23 = math.sqrt(s223), math.sqrt(1 - s223)
    return s12 * c12 * s13 * c13 ** 2 * s23 * c23 * math.sin(math.radians(delta_deg))


print("=" * 78)
print("0. primitives / lambda_C definition check")
print("=" * 78)
print(f"  phi0                 = {mp.nstr(phi0, 20)}")
print(f"  sqrt(phi0(1-phi0))   = {mp.nstr(lam_phi0, 20)}")
print(f"  sqrt(phib(1-phib))   = {mp.nstr(lam_base, 20)}")
print(f"  frozen registry      = {mp.nstr(FROZEN_LAM, 20)}")
print(f"  -> registry matches phi0-def: {abs(lam_phi0 - FROZEN_LAM) < mp.mpf('1e-20')}")
print(f"  (2/3)^6 transport bound = {(2/3)**6:.6f};  phi0 rel. shift = {PHI0:.6f}")

# ---------------------------------------------------------------- 1. dressing table
print()
print("=" * 78)
print("1. PMNS atmospheric-sector dressing (parameter-free, existing vocabulary)")
print("=" * 78)

rows = [
    ("s2_12  record  1/3 - phi0/2", 1 / 3 - PHI0 / 2, S212_M, S212_S),
    ("s2_13  record  phi0 e^-5/6", PHI0 * E56, S213_M, S213_S),
    ("s2_13  DRESSED phi0(1-phi0) e^-5/6", PHI0 * (1 - PHI0) * E56, S213_M, S213_S),
    ("s2_13  DRESSED vs reactor-only", PHI0 * (1 - PHI0) * E56, S213_R_M, S213_R_S),
    ("s2_23  record  1/2 (texture)", 0.5, S223_M, S223_S),
    ("s2_23  DRESSED 1/2 - phi0/2", 0.5 - PHI0 / 2, S223_M, S223_S),
]
for name, p, m, s in rows:
    print(f"  {name:<38} pred {p: .6f}  data {m:.5f}({s:.5f})  pull {pull(p, m, s):+6.2f} sigma")

# ---------------------------------------------------------------- 2. seed-block effect
print()
print("=" * 78)
print("2. effect on the shared-seed block (theta13 was the dominant stress leg)")
print("=" * 78)
# old inversion: phi_hat = s213 / e^-5/6
phi_old = S213_R_M / E56
phi_old_s = S213_R_S / E56
# new inversion: phi(1-phi) = s213/e^-5/6  ->  phi = (1 - sqrt(1-4y))/2
y = S213_R_M / E56
phi_new = (1 - math.sqrt(1 - 4 * y)) / 2
phi_new_s = (S213_R_S / E56) / math.sqrt(1 - 4 * y)
print(f"  implied phi0 (record formula, reactor-only): {phi_old:.6f} +- {phi_old_s:.6f}"
      f"  -> z = {(phi_old - PHI0) / phi_old_s:+.2f} sigma vs axiom")
print(f"  implied phi0 (dressed formula, reactor-only): {phi_new:.6f} +- {phi_new_s:.6f}"
      f"  -> z = {(phi_new - PHI0) / phi_new_s:+.2f} sigma vs axiom")

# ---------------------------------------------------------------- 3. J = splitting ratio
print()
print("=" * 78)
print("3. candidate: dm21^2/dm31^2 = |J_PMNS| (splitting ratio currently unpredicted)")
print("=" * 78)
r_meas = DM21 / DM31
r_sig = r_meas * math.sqrt((DM21_S / DM21) ** 2 + (DM31_S / DM31) ** 2)
J_frozen = jarlskog(1 / 3 - PHI0 / 2, PHI0 * E56, 0.5, 240.0)
J_dressed = jarlskog(1 / 3 - PHI0 / 2, PHI0 * (1 - PHI0) * E56, 0.5 - PHI0 / 2, 240.0)
print(f"  measured dm21^2/dm31^2 = {r_meas:.6f} +- {r_sig:.6f}   (NuFIT 6.0 NO)")
print(f"  |J| (frozen angles, delta=240deg)   = {abs(J_frozen):.6f} "
      f" pull {pull(abs(J_frozen), r_meas, r_sig):+6.2f} sigma")
print(f"  |J| (dressed angles, delta=240deg)  = {abs(J_dressed):.6f} "
      f" pull {pull(abs(J_dressed), r_meas, r_sig):+6.2f} sigma")
m2m3 = math.sqrt(r_meas)
m2m3_s = 0.5 * r_sig / math.sqrt(r_meas)
print(f"  (equivalent: m2/m3 = {m2m3:.5f} +- {m2m3_s:.5f}; sqrt|J|_frozen = "
      f"{math.sqrt(abs(J_frozen)):.5f})")

# ---------------------------------------------------------------- 4. dressing LEE
print()
print("=" * 78)
print("4. honest dressing census: how many equally-simple dressings fix BOTH tensions?")
print("=" * 78)
xs = [("phi0", PHI0), ("phi0/2", PHI0 / 2), ("lambda_C", LAM), ("c3", float(c3)),
      ("lambda_C^2", LAM * LAM), ("(2/3)^6", (2 / 3) ** 6), ("dtop", float(dtop)),
      ("phibase", float(phibase))]
n_joint = 0
winners = []
for name, x in xs:
    for sgn in (+1, -1):
        p13 = PHI0 * E56 * (1 + sgn * x)
        p23 = 0.5 * (1 + sgn * x)
        ok13 = abs(pull(p13, S213_M, S213_S)) <= 1.0
        ok23 = abs(pull(p23, S223_M, S223_S)) <= 1.0
        if ok13 and ok23:
            n_joint += 1
            winners.append(f"{'+' if sgn > 0 else '-'}{name}")
print(f"  multiplicative dressings tried: {2 * len(xs)}; joint |pull|<=1 on BOTH: "
      f"{n_joint}  -> {winners}")

# ---------------------------------------------------------------- 5. grammar census (v100-style)
print()
print("=" * 78)
print("5. v100-style look-elsewhere census (G1 grammar) for headline + broad scan")
print("=" * 78)

G1_PQ_MAX = 60
DECADE = 10.0


def g1_structures():
    exps = [(0, 1)] + [(u, w) for w in range(1, 7)
                       for u in range(-6, 7)
                       if u != 0 and math.gcd(abs(u), w) == 1]
    fs = []
    for a in range(-2, 3):
        for cc in range(-3, 4):
            for d in range(-1, 2):
                for b in range(-1, 2):
                    base = PHI0 ** a * LAM ** cc * (1 + LAM) ** d * math.pi ** b
                    for (u, w) in exps:
                        fs.append(base * math.exp(u / w))
    return np.array(fs)


def census_one(F, m, window):
    lo_h, hi_h = m * (1 - window), m * (1 + window)
    lo_d, hi_d = m / DECADE, m * DECADE
    hits = dec = 0.0
    for q in range(1, G1_PQ_MAX + 1):
        for lo, hi, which in ((lo_h, hi_h, "h"), (lo_d, hi_d, "d")):
            plo = np.ceil(q * lo / F)
            phi_ = np.floor(q * hi / F)
            cnt = np.clip(np.minimum(phi_, G1_PQ_MAX) - np.maximum(plo, 1) + 1,
                          0, None).sum()
            if which == "h":
                hits += cnt
            else:
                dec += cnt
    return hits, dec


F = g1_structures()
targets = [
    ("s2_13 NuFIT (window 1 sigma)", S213_M, S213_S / S213_M),
    ("dm21/dm31 ratio (window 1 sigma)", r_meas, r_sig / r_meas),
    ("alpha_s(M_Z) 0.1179(9)", 0.1179, 0.0009 / 0.1179),
    ("Omega_c/Omega_b Planck 5.364(65)", 5.3643, 0.0646 / 5.3643),
    ("sigma_8 0.8111(60)", 0.8111, 0.0060 / 0.8111),
    ("sin2thetaW(M_Z) 0.23122(4)", 0.23122, 0.00004 / 0.23122),
    ("m_p/m_e CODATA (window 5e-5)", 1836.15267343, 5e-5),
    ("m2/m3 (window 1 sigma)", m2m3, m2m3_s / m2m3),
]
for name, m, w in targets:
    h, d = census_one(F, m, w)
    dens = h / d if d else float("nan")
    print(f"  {name:<38} hits {h:>8.0f} / decade {d:>11.0f}  density {dens:.3e}")

# a few explicit simple candidates for the broad-scan targets, for the record
print()
print("  explicit simple candidates (for the record, all post-hoc):")
cands = [
    ("alpha_s(MZ) ~ 3 c3 = 3/(8pi)", 3 * float(c3), 0.1179, 0.0009),
    ("mp/me ~ 6 pi^5 (Lenz 1951; = pi^4/phibase)", 6 * math.pi ** 5, 1836.15267343,
     1836.15267343 * 5e-5),
]
for name, p, m, s in cands:
    print(f"    {name:<44} pred {p: .6f}  data {m:.6f}  pull {pull(p, m, s):+7.2f} sigma")

# ---------------------------------------------------------------- 6. Omega_c curiosity
print()
print("=" * 78)
print("6. curiosity: Omega_c = (2/7)(1 - 1/(4pi))  <=>  Omega_c/Omega_b = 2/(7 phi0)")
print("=" * 78)
# Planck 2018 TT,TE,EE+lowE+lensing: Omega_c h^2 = 0.1200(12), h = 0.6736(54)
OCH2, OCH2_S = 0.1200, 0.0012
H, H_S = 0.6736, 0.0054
oc_m = OCH2 / H ** 2
oc_s = oc_m * math.sqrt((OCH2_S / OCH2) ** 2 + (2 * H_S / H) ** 2)
oc_p = (2.0 / 7.0) * (1 - 1 / (4 * math.pi))
print(f"  measured Omega_c = {oc_m:.5f} +- {oc_s:.5f}   (Planck 2018)")
print(f"  (2/7)(1-1/4pi)   = {oc_p:.5f}   pull {pull(oc_p, oc_m, oc_s):+6.2f} sigma")
ratio_p = oc_p / ((1 - 1 / (4 * math.pi)) * PHI0)
print(f"  -> Omega_c/Omega_b = 2/(7 phi0) = {ratio_p:.4f}  vs  h^2-ratio "
      f"{0.1200 / 0.02237:.4f} +- {0.1200 / 0.02237 * math.sqrt((0.0012/0.12)**2 + (0.00015/0.02237)**2):.4f}")
# coefficient-class LEE: how many reduced fractions p/q (q<=12) x (1-1/4pi) hit the window?
hits = []
for q in range(1, 13):
    for p in range(1, 13):
        if math.gcd(p, q) != 1:
            continue
        v = (p / q) * (1 - 1 / (4 * math.pi))
        if abs(v - oc_m) <= oc_s:
            hits.append(f"{p}/{q}")
print(f"  coefficient-class LEE (p/q<=12, factor (1-1/4pi), window 1 sigma): "
      f"{len(hits)} hit(s) -> {hits}")
print("  NOTE: conflicts conceptually with the axion-spine DM branch (Omega_a h^2 = "
      "0.125 dynamical, F_transfer) -- a boundary formula for Omega_c would be a "
      "SECOND reading of the same question. Numerology-flagged, post-hoc.")

# ---------------------------------------------------------------- 6b. CKM third-gen sector
print()
print("=" * 78)
print("6b. THE PATTERN: all third-generation mixings share the SAME (1-phi0) factor")
print("=" * 78)
# frozen CKM readouts (predictions_frozen.json) + repo-documented data (v307/PDG 2024)
S23_CKM = PHI0 / (1 + LAM)          # 0.043428
S13_CKM = LAM ** 3 / 3              # 0.0037654
VCB_M, VCB_S = 0.0411, 0.0013
VUB_M, VUB_S = 0.00382, 0.00024
LAMC_M, LAMC_S = 0.2245, 0.0005

sector = [
    # (name, frozen pred, measured, sigma, generation-pair)
    ("s2_13 PMNS (1-3)", PHI0 * E56, S213_M, S213_S),
    ("s2_23 PMNS (2-3)", 0.5, S223_M, S223_S),
    ("V_cb   CKM  (2-3)", S23_CKM, VCB_M, VCB_S),
    ("V_ub   CKM  (1-3)", S13_CKM, VUB_M, VUB_S),
]
undressed = [
    ("s2_12 PMNS (1-2)", 1 / 3 - PHI0 / 2, S212_M, S212_S),
    ("lam_C  CKM  (1-2)", LAM, LAMC_M, LAMC_S),
]
print("  third-generation mixings, frozen vs x(1-phi0) dressed:")
chi2_f = chi2_d = 0.0
devs, sigs = [], []
for name, p, m, s in sector:
    pf, pd = pull(p, m, s), pull(p * (1 - PHI0), m, s)
    chi2_f += pf ** 2
    chi2_d += pd ** 2
    rel_dev = m / p - 1
    rel_sig = s / p
    devs.append(rel_dev)
    sigs.append(rel_sig)
    print(f"    {name:<20} frozen {p:.6f} ({pf:+5.2f}s)   dressed {p * (1 - PHI0):.6f}"
          f" ({pd:+5.2f}s)   rel.dev {100 * rel_dev:+.2f}% +- {100 * rel_sig:.2f}%")
print("  1-2 mixings (must stay UNdressed):")
for name, p, m, s in undressed:
    print(f"    {name:<20} frozen {p:.6f} ({pull(p, m, s):+5.2f}s)   "
          f"dressed would be ({pull(p * (1 - PHI0), m, s):+5.2f}s)")
print(f"  joint chi^2 (4 third-gen obs): frozen {chi2_f:.2f}  ->  dressed {chi2_d:.2f}"
      f"   (Delta chi^2 = {chi2_f - chi2_d:.2f}, ZERO new parameters)")

# common-suppression statistics: weighted mean of relative deviations
w = [1 / s ** 2 for s in sigs]
mean_dev = sum(wi * di for wi, di in zip(w, devs)) / sum(w)
mean_sig = 1 / math.sqrt(sum(w))
print(f"  weighted common rel. deviation of the 4 third-gen mixings: "
      f"{100 * mean_dev:+.2f}% +- {100 * mean_sig:.2f}%")
print(f"    vs 0        (no suppression) : {mean_dev / mean_sig:+.2f} sigma")
print(f"    vs -phi0    ({-100 * PHI0:.2f}%)      : {(mean_dev + PHI0) / mean_sig:+.2f} sigma")
print(f"    vs -c3      ({-100 * float(c3):.2f}%)      : {(mean_dev + float(c3)) / mean_sig:+.2f} sigma")
print(f"    vs -(2/3)^6 ({-100 * (2 / 3) ** 6:.2f}%)      : {(mean_dev + (2 / 3) ** 6) / mean_sig:+.2f} sigma")
print(f"    vs -dtop    ({-100 * float(dtop):.4f}%)    : {(mean_dev + float(dtop)) / mean_sig:+.2f} sigma")

# Gatto relation in TFPT vocabulary (standard folklore, for completeness)
print()
print("  (folklore check) Gatto: m_s/m_d = 1/lambda_C^2 = 1/(phi0(1-phi0)) = "
      f"{1 / (PHI0 * (1 - PHI0)):.3f}  vs lattice/PDG ~ 20.0(1.0)  "
      f"pull {pull(1 / (PHI0 * (1 - PHI0)), 20.0, 1.0):+.2f} sigma")

# ---------------------------------------------------------------- 7. consequences of r = |J|
print()
print("=" * 78)
print("7. if dm21^2/dm31^2 = |J| held: neutrino spectrum consequences (NO)")
print("=" * 78)
m3 = math.sqrt(DM31)                       # eV
m2_pred = m3 * math.sqrt(abs(J_frozen))
sigma_pred = m3 * (1 + math.sqrt(abs(J_frozen)))
print(f"  m3 = sqrt(dm31^2) = {m3:.5f} eV (measured input; absolute scale stays [O])")
print(f"  predicted m2 = m3 sqrt|J| = {m2_pred:.5f} eV  "
      f"(measured sqrt(dm21^2) = {math.sqrt(DM21):.5f} eV)")
print(f"  predicted Sigma m_nu (m1~0) = m3(1+sqrt|J|) = {sigma_pred:.5f} eV "
      f"(vs 0.0586 documented)")
print()
print("  m2/m3 candidate table (record vs new):")
m23_cands = [
    ("RECORD  pi phi0 (tfpt_2 table, '~0.167')", math.pi * PHI0),
    ("NEW     sqrt|J_frozen|", math.sqrt(abs(J_frozen))),
    ("NEW     lambda_C (1 - lambda_C)", LAM * (1 - LAM)),
]
for name, p in m23_cands:
    print(f"    {name:<44} {p:.5f}  pull {pull(p, m2m3, m2m3_s):+6.2f} sigma")

# ---------------------------------------------------------------- 8. decision layer
print()
print("=" * 78)
print("8. decision layer: what would confirm/kill the two candidate patterns")
print("=" * 78)
# (a) ladder-base reading, third-gen: Daya Bay alone already discriminates
DB_M, DB_S = 0.02175, 0.00065
print("  (a) third-gen ladder-base rule  phi0 -> lambda_C^2 = phi0(1-phi0)  "
      "+  cos(2 theta23) = phi0:")
print(f"      cos2theta23: measured {1 - 2 * S223_M:.4f} +- {2 * S223_S:.4f} "
      f" vs phi0 = {PHI0:.4f}  ({(1 - 2 * S223_M - PHI0) / (2 * S223_S):+.2f} sigma)")
for name, p in [("record  phi0 e^-5/6", PHI0 * E56),
                ("dressed lambda_C^2 e^-5/6", PHI0 * (1 - PHI0) * E56)]:
    print(f"      theta13 vs Daya Bay only 0.02175(65): {name:<28} "
          f"pull {pull(p, DB_M, DB_S):+6.2f} sigma")
d_rec = pull(PHI0 * E56, DB_M, DB_S) ** 2 - pull(PHI0 * (1 - PHI0) * E56, DB_M, DB_S) ** 2
print(f"      Daya-Bay-only Delta chi^2 (record - dressed) = {d_rec:+.2f}")
print("      KILL (dressed): sin^2 theta13 stabilising at the NuFIT global "
      "0.0231-side, or V_cb(exclusive) confirmed ~0.0395 (then BOTH readings fail)")
print("      DEGENERACY: (1-phi0) vs (1-c3) vs (1-lambda_C^2) suppression "
      "differ by <1.4%; need sigma(rel)<0.5% on one channel to separate")
# (b) splitting-ratio relation: JUNO precision era
print("  (b) dm21^2/dm31^2 = |J_PMNS|:")
print(f"      relation value {abs(J_frozen):.6f}; measured {r_meas:.6f} +- {r_sig:.6f}"
      f" ({pull(abs(J_frozen), r_meas, r_sig):+.2f} sigma)")
print("      JUNO will push sigma(dm21^2) and sigma(dm31^2) to ~0.2-0.5% -> the "
      "window shrinks ~4x; a stable offset > 3 sigma kills the relation")
print("      NOTE: relation uses the UNDRESSED frozen angles; with dressed angles "
      f"|J| = {abs(J_dressed):.6f} ({pull(abs(J_dressed), r_meas, r_sig):+.2f} sigma)"
      " -- the two candidates pull against each other at JUNO precision")
