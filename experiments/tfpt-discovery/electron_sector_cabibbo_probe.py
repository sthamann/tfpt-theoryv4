"""Whitespot probe (bird's-eye round 2026-07-03): the ELECTRON SECTOR and the
CABIBBO-ANGLE ANOMALY -- two data surfaces the suite has never confronted.

SANDBOX ONLY (experiments/tfpt-discovery/): nothing is promoted, no ledger /
paper / scorecard / website touch.  Verdict enum used here: watch_candidate /
falsified_reading / route_candidate.  All flags honest, LEE stated.

PART A -- the alpha metrology triangle.
    TFPT's flagship [E] number alpha^-1 = 137.0359992168 (v3/v84, exact root
    of F_U1) has so far only been compared to CODATA 2022 (+1.9 sigma,
    scorecard row).  But the metrology world is internally split:
        Rb 2020  (Morel+,  Nature 588, 61):   137.035999206(11)
        Cs 2018  (Parker+, Science 360, 191): 137.035999046(27)   (Rb-Cs 5.4 sigma!)
        a_e 2023 (Fan+, PRL 130, 071801) + SM: 137.035999166(15)
    TFPT takes a SIDE in this fight -- that is a free, dated kill surface
    nobody has recorded.

PART B -- lepton universality of the g-2 seam vertex (v204).
    a_mu^seam = delta_2/(2 pi) = 45/(524288 pi^9) = 2.879e-9 is written as a
    pure compiler number with NO lepton-mass dependence.  If the seam-loop
    projection were flavor-UNIVERSAL, the same 2.879e-9 would be added to a_e
    -- and a_e is measured to 1.3e-13.  This internal catch has never been
    checked.  We type the three natural scalings (universal / linear /
    quadratic in m_l/m_mu) against the 2023 electron datum.

PART C -- the Cabibbo-angle anomaly as the THIRD dissolution watchdog.
    TFPT fixes lambda_C = sqrt(phi0(1-phi0)) = 0.2243762 exactly (frozen v84)
    and the CKM assembly is exactly unitary (frozen delta_CKM texture).  Like
    the sterile axis (N_fam=3 exact) and the evolving-DE axis (w=-1 exact),
    the ~3 sigma first-row deficit |V_ud|^2+|V_us|^2+|V_ub|^2 = 0.9983(7)
    (PDG 2026) is then required to DISSOLVE -- and TFPT says on WHICH side.

Data sources (frozen 2026-07-03):
  - alpha^-1 determinations: Morel+ 2020, Parker+ 2018, CODATA22 (RMP 97,
    025002), Fan+ 2023 (PRL 130, 071801).
  - a_e = 1.15965218059(13)e-3 (Fan+ 2023); a_e^SM(alpha_Rb) =
    1.159652180252(95)e-3 (Fan+ 2023); a_e^SM(alpha_Cs) = 1.15965218161(23)e-3
    (Parker+ 2018).
  - PDG 2026 rev. "Vud, Vus, the Cabibbo Angle, and CKM Unitarity":
    V_ud(0+->0+) = 0.97367(32); V_ud(n, PDG averages) = 0.97441(88);
    V_ud(n, best) = 0.97413(42); V_ud(pi_e3) = 0.9739(27);
    V_us(Kl3, Nf=2+1+1) = 0.22330(53); kaon average (S=2.5) V_us = 0.22431(85);
    V_us/V_ud(Kmu2) = 0.23108(51); V_us(tau) = 0.2207(14);
    V_us(hyperon) = 0.2250(27); first row = 0.9983(7).
  - a_tau (CMS PbPb gamma gamma -> tau tau, PRL 131, 151803): 0.0009 +0.0032/-0.0031.
  - PDG lepton masses: m_e = 0.51099895069 MeV, m_mu = 105.6583755 MeV,
    m_tau = 1776.93 MeV.
"""
import mpmath as mp

mp.mp.dps = 40
PI = mp.pi
c3 = 1 / (8 * PI)                      # P1
phi0 = 1 / (6 * PI) + 48 * c3**4       # axis seed

FAILS = []


def report(name, ok):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)
    return ok


def alpha_root():
    """Unique positive root of F_U1 (identical closure to v3/v84, M = 41)."""
    pb = 1 / (6 * PI)
    dt = 48 * c3**4

    def F(a):
        Q = dt * mp.e**(-2 * a)
        ps = pb + Q * (1 - Q)**(mp.mpf(-5) / 4)
        return a**3 - 2 * c3**3 * a**2 - (mp.mpf(4) / 5) * c3**6 * 41 * mp.log(1 / ps)

    return mp.findroot(F, mp.mpf('0.0073'))


# ----------------------------------------------------------------------------
print("=" * 78)
print("PART A -- alpha metrology triangle (TFPT exact alpha vs the split world)")
print("=" * 78)

ainv = 1 / alpha_root()
print(f"  TFPT alpha^-1 (exact root, v3/v84) = {mp.nstr(ainv, 16)}")

ALPHA_DATA = [
    # label, central, sigma
    ("Rb 2020 recoil (Morel+)",       mp.mpf('137.035999206'), mp.mpf('11e-9')),
    ("CODATA 2022",                   mp.mpf('137.035999177'), mp.mpf('21e-9')),
    ("a_e 2023 + SM (Fan+)",          mp.mpf('137.035999166'), mp.mpf('15e-9')),
    ("Cs 2018 recoil (Parker+)",      mp.mpf('137.035999046'), mp.mpf('27e-9')),
]
pulls_a = {}
for label, cen, sig in ALPHA_DATA:
    p = (ainv - cen) / sig
    pulls_a[label] = p
    print(f"    vs {label:28s}: {mp.nstr(cen, 13)}  pull = {float(p):+6.2f} sigma")

rbcs = (ALPHA_DATA[0][1] - ALPHA_DATA[3][1]) / mp.sqrt(ALPHA_DATA[0][2]**2 + ALPHA_DATA[3][2]**2)
print(f"    (internal Rb-Cs split: {float(rbcs):+.1f} sigma -- the metrology fight)")

report("TFPT alpha sits on the Rb SIDE of the 5.4-sigma Rb/Cs fight (<1.1 sigma from Rb)",
       ok=abs(pulls_a["Rb 2020 recoil (Morel+)"]) < mp.mpf('1.1'))
report("Cs 2018 would REJECT the TFPT alpha at >5 sigma (dated kill surface exists)",
       ok=pulls_a["Cs 2018 recoil (Parker+)"] > 5)
report("NEW stress point: the a_e-route alpha is the sharpest single comparison "
       f"({float(pulls_a['a_e 2023 + SM (Fan+)']):+.2f} sigma, never recorded)",
       ok=3 < pulls_a["a_e 2023 + SM (Fan+)"] < 4)

# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("PART B -- lepton universality of the seam vertex a_l^seam (v204 catch)")
print("=" * 78)

a_mu_seam = mp.mpf(45) / 524288 / PI**9
m_e, m_mu, m_tau = mp.mpf('0.51099895069'), mp.mpf('105.6583755'), mp.mpf('1776.93')
r_e, r_tau = m_e / m_mu, m_tau / m_mu

# electron residual against the SM evaluated at the EXACT TFPT alpha.
a_e_exp,   s_exp = mp.mpf('1.15965218059e-3'), mp.mpf('1.3e-13')     # Fan+ 2023
a_sm_rb,  s_rb  = mp.mpf('1.159652180252e-3'), mp.mpf('9.5e-14')     # SM @ alpha_Rb
a_sm_cs         = mp.mpf('1.15965218161e-3')                          # SM @ alpha_Cs
ainv_rb, ainv_cs = ALPHA_DATA[0][1], ALPHA_DATA[3][1]

slope = (a_sm_cs - a_sm_rb) / (ainv_cs - ainv_rb)      # d a_SM / d alpha^-1
print(f"  d a_SM/d alpha^-1 (from Rb/Cs SM pair) = {mp.nstr(slope, 6)}  "
      f"(analytic ~ -alpha^2/(2 pi) = {mp.nstr(-1/(2*PI*ainv**2), 6)})")

a_sm_tfpt = a_sm_rb + slope * (ainv - ainv_rb)
s_th_tfpt = mp.mpf('2.0e-14')     # intrinsic SM theory unc once alpha is exact
resid = a_e_exp - a_sm_tfpt
s_resid = mp.sqrt(s_exp**2 + s_th_tfpt**2)
print(f"  a_e residual @ TFPT-exact alpha: ({mp.nstr(resid*1e13, 4)} +- "
      f"{mp.nstr(s_resid*1e13, 3)}) e-13  ->  {float(resid/s_resid):+.2f} sigma")

print(f"  a_mu^seam = 45/(524288 pi^9) = {mp.nstr(a_mu_seam, 6)}")
scalings = [
    ("UNIVERSAL  (p=0, as literally written in v204)", a_mu_seam),
    ("LINEAR     (p=1, ~m_l chirality flip only)",     a_mu_seam * r_e),
    ("QUADRATIC  (p=2, standard heavy-NP scaling)",    a_mu_seam * r_e**2),
]
for label, da in scalings:
    pull = (da - resid) / s_resid
    print(f"    {label}: da_e = {mp.nstr(da, 4)}  -> pull vs residual "
          f"{float(pull):+9.1f} sigma")

report("UNIVERSAL reading of the v204 bridge is FALSIFIED by a_e (>1e4 sigma)",
       ok=(scalings[0][1] - resid) / s_resid > 10000)
report("LINEAR scaling is falsified too (~1e2 sigma)",
       ok=(scalings[1][1] - resid) / s_resid > 50)
report("QUADRATIC scaling survives (contribution 6.7e-14 < residual band)",
       ok=abs(scalings[2][1]) < 3 * s_resid)

# post-hoc exponent hunt (numerology-flagged, LEE stated)
p_needed = mp.log(resid / a_mu_seam) / mp.log(r_e)
p_lo = mp.log((resid - s_resid) / a_mu_seam) / mp.log(r_e)
p_hi = mp.log((resid + s_resid) / a_mu_seam) / mp.log(r_e)
print(f"  IF (TFPT alpha exact) AND (a_e residual = seam vertex): needed exponent "
      f"p = {mp.nstr(p_needed, 4)}  (band [{mp.nstr(p_hi, 4)}, {mp.nstr(p_lo, 4)}])")
da_53 = a_mu_seam * r_e**mp.mpf('5/3')
print(f"  candidate p = 5/3 (= k_Y embedding index, v470): da_e = "
      f"{mp.nstr(da_53, 4)}  -> {float((da_53 - resid)/s_resid):+.2f} sigma")
print("  LEE: simple-exponent census {1, 7/6, 4/3, 3/2, 5/3, 11/6, 2} in the "
      "+-1 sigma window -> only 5/3 hits, but expected hits ~0.8 -> a hit is "
      "CHEAP; pattern-level only, post-hoc, NOT a claim.")
report("p = 5/3 lands inside the 1-sigma band (post-hoc route_candidate, LEE-flagged)",
       ok=abs((da_53 - resid) / s_resid) < 1)

a_tau_seam_q  = a_mu_seam * r_tau**2
a_tau_seam_53 = a_mu_seam * r_tau**mp.mpf('5/3')
print(f"  tau forecast: p=2 -> {mp.nstr(a_tau_seam_q, 3)}; p=5/3 -> "
      f"{mp.nstr(a_tau_seam_53, 3)}; CMS bound ~3e-3 -> 4 orders below "
      "sensitivity (no near-term tau test)")

# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("PART C -- Cabibbo-angle anomaly: the THIRD dissolution watchdog")
print("=" * 78)

lamC = mp.sqrt(phi0 * (1 - phi0))
s13 = mp.mpf('0.003765384454486429837965432')     # frozen S13_CKM (v84)
V_ud_tfpt = mp.sqrt(1 - lamC**2 - s13**2)
print(f"  TFPT lambda_C = sqrt(phi0(1-phi0)) = {mp.nstr(lamC, 10)}  (frozen v84)")
print(f"  TFPT + exact unitarity  =>  V_ud = {mp.nstr(V_ud_tfpt, 10)}")

VUS_DATA = [
    ("kaon average (PDG26, S=2.5)", mp.mpf('0.22431'), mp.mpf('0.00085')),
    ("Kl3 (Nf=2+1+1 f+(0))",        mp.mpf('0.22330'), mp.mpf('0.00053')),
    ("hyperon decays",              mp.mpf('0.2250'),  mp.mpf('0.0027')),
    ("tau decays",                  mp.mpf('0.2207'),  mp.mpf('0.0014')),
]
# Kmu2 route: V_us/V_ud = 0.23108(51) -> with unitarity V_us = r/sqrt(1+r^2)
r_kmu2, s_r = mp.mpf('0.23108'), mp.mpf('0.00051')
vus_kmu2 = r_kmu2 / mp.sqrt(1 + r_kmu2**2)
s_kmu2 = s_r / (1 + r_kmu2**2)**mp.mpf('1.5')
VUS_DATA.insert(2, ("Kmu2 route (r=0.23108(51))", vus_kmu2, s_kmu2))

print("  V_us determinations vs TFPT lambda_C:")
pulls_c = {}
for label, cen, sig in VUS_DATA:
    p = (lamC - cen) / sig
    pulls_c[label] = p
    print(f"    {label:30s}: {mp.nstr(cen, 6)} +- {mp.nstr(sig, 3)}  "
          f"pull = {float(p):+5.2f} sigma")

VUD_DATA = [
    ("superallowed 0+->0+ (PDG26)",  mp.mpf('0.97367'), mp.mpf('0.00032')),
    ("neutron (PDG averages)",       mp.mpf('0.97441'), mp.mpf('0.00088')),
    ("neutron (best tau_n/gA)",      mp.mpf('0.97413'), mp.mpf('0.00042')),
    ("pion beta decay",              mp.mpf('0.9739'),  mp.mpf('0.0027')),
]
print("  V_ud determinations vs the TFPT-unitarity value:")
for label, cen, sig in VUD_DATA:
    p = (V_ud_tfpt - cen) / sig
    pulls_c[label] = p
    print(f"    {label:30s}: {mp.nstr(cen, 6)} +- {mp.nstr(sig, 3)}  "
          f"pull = {float(p):+5.2f} sigma")

first_row = mp.mpf('0.9983')
print(f"  PDG26 first row = {first_row}(7)  ->  -2.4 sigma deficit; "
      "TFPT requires EXACTLY 1 (frozen unitary assembly)")

report("TFPT lambda_C on the PDG26 rescaled kaon average: |pull| < 0.2 sigma",
       ok=abs(pulls_c["kaon average (PDG26, S=2.5)"]) < mp.mpf('0.2'))
report("TFPT sits BETWEEN Kl3 (+2.0 s) and Kmu2 (-1.6 s) -> predicts the two "
       "routes CONVERGE onto 0.22438",
       ok=pulls_c["Kl3 (Nf=2+1+1 f+(0))"] > 0 > pulls_c["Kmu2 route (r=0.23108(51))"])
report("V_ud side: superallowed is the outlier (+2.6 s), ALL neutron/pion routes "
       "agree with TFPT (<1 s)",
       ok=(pulls_c["superallowed 0+->0+ (PDG26)"] > 2
           and abs(pulls_c["neutron (best tau_n/gA)"]) < 1
           and abs(pulls_c["neutron (PDG averages)"]) < 1
           and abs(pulls_c["pion beta decay"]) < 1))

print()
print("  WATCHDOG READING (prediction of record, dissolution axis E candidate):")
print("    like steriles (N_fam=3) and evolving DE (w=-1), TFPT requires the")
print("    Cabibbo anomaly to DISSOLVE: V_us -> 0.22438 (both kaon routes")
print("    converge), the deficit resolves on the V_ud/nuclear-structure side")
print("    (neutron-decay values already there).  Deciders this decade:")
print("    PIONEER (pi_e3, R_e/mu), lattice f+(0)+fK/fpi, superallowed NS/RC")
print("    re-evaluations, tau_n/gA consensus.")
print("    KILL (prereg): a converged all-route V_us (S~1) with")
print("    |V_us - 0.224376| >= 5 sigma; or a systematics-converged first-row")
print("    deficit >= 5 sigma (kills exact unitarity of the frozen assembly).")
print("    Anti-double-count: lambda_C is phi0-derived -> independence_group")
print("    phi0_seed, shares the seed with beta/Omega_b/theta12/theta13.")

# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("PART D -- one-liner: frozen lepton-ratio registry vs pole data (context)")
print("=" * 78)
mmu_mtau_frozen = mp.mpf('0.06076794534496631692490568')
me_mmu_frozen = mp.mpf('0.004846725425651567674771059')
d1 = (mmu_mtau_frozen - m_mu / m_tau) / (m_mu / m_tau)
d2 = (me_mmu_frozen - m_e / m_mu) / (m_e / m_mu)
print(f"  m_mu/m_tau frozen vs PDG pole: {float(d1)*100:+.2f}%  | "
      f"m_e/m_mu: {float(d2)*100:+.2f}%  (both inside the (2/3)^6 = 8.78% "
      "transport band; v466 class, nothing new)")

print()
print("=" * 78)
if FAILS:
    print(f"RESULT: {len(FAILS)} check(s) FAILED:")
    for f in FAILS:
        print("  -", f)
else:
    print("RESULT: ALL PROBE CHECKS PASS (sandbox; nothing promoted)")
print("=" * 78)
raise SystemExit(1 if FAILS else 0)
