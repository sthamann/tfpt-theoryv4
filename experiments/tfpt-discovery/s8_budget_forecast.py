"""S8 forecast from the parameter-free flat budget (pattern probe).

SANDBOX ONLY (experiments/tfpt-discovery/): nothing promoted, no ledger /
paper / website touch.  Verdict enum: pattern_candidate (inherits the
NUMEROLOGY FLAG of the Omega_c leg from flat_budget_closure.py; the A_s
branches inherit the N_star branch ambiguity of cmb-inflation-scalaron).

THE GAP THIS CLOSES.  flat_budget_closure.py (2026-07-03) fixed the whole
FLRW background with zero dials (h = 0.6715, omega_b = 0.02207, omega_c =
0.11857, Sigma m_nu = 0.0588 eV) and took a side in the HUBBLE tension --
but no STRUCTURE observable was ever computed.  The second big cosmology
tension is S8 = sigma8 (Omega_m/0.3)^0.5: the 2026 landscape is bifurcated
(DES Y6 low at 2.4-2.7 sigma vs Combined-CMB, KiDS-Legacy consistent <1
sigma).  With the budget frozen, sigma8 follows from A_s + transfer physics
(CAMB) with NO remaining freedom per A_s branch, so TFPT must take a side
here too.

A_s branches (cmb-inflation-scalaron, honest):
  A. frozen slow-channel point N_star = 51.4:  A_s = N*^2 c3^7/(24 pi^2)
     = 1.755e-9  (the branch Planck A_s already disfavours at ~11 sigma)
  B. profiled N_star = 56.1 (A_s-preferred branch): A_s = 2.091e-9
  C. geometry-only reading: (A_s, n_s) IMPORTED from Planck 2018 (declared
     import) -- tests the budget's (h, omega_b, omega_c, Sigma m_nu) shape
     alone, independent of the reheating branch.

Confrontation (2026): Combined CMB (Planck+ACT DR6+SPT-3G) S8 = 0.836
+0.012/-0.013 (arXiv:2602.12238); Planck18 alone 0.832 +- 0.013;
KiDS-Legacy 0.815 +0.016/-0.021 (A&A 2025); DES Y6 3x2pt 0.789 +- 0.012
(arXiv:2601.14559); DES Y6 shear NLA 0.798 +0.014/-0.015; HSC Y3
(DESI-recalibrated) 0.805 +- 0.018 (arXiv:2511.18134).

Requires: camb (pip install camb; in the tfpt-discovery venv).
"""
import math

import camb
import mpmath as mp

mp.mp.dps = 40
PI = mp.pi
c3 = 1 / (8 * PI)
phi0 = 1 / (6 * PI) + 48 * c3**4

FAILS = []


def report(name, ok):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)
    return ok


def alpha_root():
    pb = 1 / (6 * PI)
    dt = 48 * c3**4

    def F(a):
        Q = dt * mp.e**(-2 * a)
        ps = pb + Q * (1 - Q)**(mp.mpf(-5) / 4)
        return a**3 - 2 * c3**3 * a**2 - (mp.mpf(4) / 5) * c3**6 * 41 * mp.log(1 / ps)

    return mp.findroot(F, mp.mpf('0.0073'))


# ------------------------------------------------ the frozen budget (identical
# to flat_budget_closure.py -- recomputed here so the probe is self-contained)
ainv = 1 / alpha_root()
Omega_b = phi0 * (1 - 1 / (4 * PI))                 # frozen record
Omega_c = mp.mpf(2) / 7 * (1 - 1 / (4 * PI))        # FLAGGED candidate leg
rhoL = mp.mpf(3) / (4 * PI**2) * mp.e**(-2 * ainv)  # frozen record
Sm_nu = mp.mpf('0.0588')                            # eV, v468 route

MBAR_GEV = mp.mpf('2.435323e18')
GEV_PER_S = mp.mpf('1.5192674e24')
KMSMPC = mp.mpf('3.2407793e-20')
OMEGA_R_H2 = mp.mpf('4.153e-5')
NU_H2_NORM = mp.mpf('93.14')

h = mp.mpf('0.67')
for _ in range(60):
    Om_nu = Sm_nu / (NU_H2_NORM * h**2)
    Om_r = OMEGA_R_H2 / h**2
    Om_L = 1 - Omega_b - Omega_c - Om_nu - Om_r
    H0_inv_s = mp.sqrt(rhoL / (3 * Om_L)) * MBAR_GEV * GEV_PER_S
    h = (H0_inv_s / KMSMPC) / 100

H0 = float(100 * h)
om_b = float(Omega_b * h**2)
om_c = float(Omega_c * h**2)
Om_m = float(Omega_b + Omega_c + Om_nu)

print("=" * 78)
print("S8 forecast from the parameter-free flat budget (pattern probe)")
print("=" * 78)
print(f"  budget: H0 = {H0:.3f}, omega_b = {om_b:.5f}, omega_c = {om_c:.5f}, "
      f"Omega_m = {Om_m:.4f}, Sigma m_nu = {float(Sm_nu)} eV")

# ------------------------------------------------------------ A_s branches
c3f = float(c3)
AS_BRANCHES = {
    "A_frozen_Nstar_51.4": {
        "N_star": 51.4,
        "A_s": 51.4**2 * c3f**7 / (24 * math.pi**2),
        "n_s": 1 - 2 / 51.4,
        "note": "frozen slow-channel point (A_s-disfavoured at ~11 sigma; kept for honesty)",
    },
    "B_profiled_Nstar_56.1": {
        "N_star": 56.1,
        "A_s": 56.1**2 * c3f**7 / (24 * math.pi**2),
        "n_s": 1 - 2 / 56.1,
        "note": "profiled N_star (the A_s-preferred branch of cmb-inflation-scalaron)",
    },
    "C_geometry_only_planck_As": {
        "N_star": None,
        "A_s": 2.100e-9,
        "n_s": 0.9649,
        "note": "(A_s, n_s) IMPORTED from Planck 2018 -- tests the budget geometry alone",
    },
}

DATA = [
    ("Combined CMB (P+ACT+SPT 2026)", 0.836, 0.013),
    ("Planck18 alone",                0.832, 0.013),
    ("KiDS-Legacy (2025)",            0.815, 0.019),
    ("HSC Y3 (DESI-recal 2025)",      0.805, 0.018),
    ("DES Y6 3x2pt (2026)",           0.789, 0.012),
    ("DES Y6 shear NLA (2026)",       0.798, 0.015),
]


def s8_for(A_s: float, n_s: float) -> tuple[float, float]:
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=H0, ombh2=om_b, omch2=om_c, mnu=float(Sm_nu),
                       omk=0.0, tau=0.054)
    pars.InitPower.set_params(As=A_s, ns=n_s)
    pars.set_matter_power(redshifts=[0.0], kmax=10.0)
    pars.NonLinear = camb.model.NonLinear_none
    results = camb.get_results(pars)
    sigma8 = float(results.get_sigma8_0())
    om_m_camb = float(results.get_Omega('baryon') + results.get_Omega('cdm')
                      + results.get_Omega('nu'))
    return sigma8, sigma8 * math.sqrt(om_m_camb / 0.3)


print()
rows = {}
for name, br in AS_BRANCHES.items():
    sigma8, S8 = s8_for(br["A_s"], br["n_s"])
    rows[name] = (sigma8, S8)
    print(f"  branch {name}: A_s = {br['A_s']:.4g}, n_s = {br['n_s']:.4f}"
          f"  ->  sigma8 = {sigma8:.4f},  S8 = {S8:.4f}")
    print(f"         ({br['note']})")

print()
print("  CONFRONTATION (pulls, branch C = geometry-only):")
_, S8_C = rows["C_geometry_only_planck_As"]
pulls = {}
for label, cen, sig in DATA:
    p = (S8_C - cen) / sig
    pulls[label] = p
    print(f"    {label:32s} {cen:.3f} +- {sig:.3f}   pull {p:+5.2f} sigma")

print()
print("  CHECKS:")
report("branch C (geometry-only) S8 within 1 sigma of KiDS-Legacy AND Planck18",
       ok=abs(pulls["KiDS-Legacy (2025)"]) < 1 and abs(pulls["Planck18 alone"]) < 1)
report("branch C sits AGAINST DES Y6 3x2pt (>= 2 sigma high)",
       ok=pulls["DES Y6 3x2pt (2026)"] >= 2)
report("branch B (profiled N_star) lands in the same band as branch C (< 0.02 in S8)",
       ok=abs(rows["B_profiled_Nstar_56.1"][1] - S8_C) < 0.02)
report("branch A (frozen N_star = 51.4) is structure-disfavoured (S8 < 0.79, the "
       "known ~11-sigma A_s branch stress, now visible in structure)",
       ok=rows["A_frozen_Nstar_51.4"][1] < 0.79)

print()
sA, s8A = rows["A_frozen_Nstar_51.4"]
sB, s8B = rows["B_profiled_Nstar_56.1"]
print("  READING (honest):")
print(f"    the parameter-free budget geometry puts TFPT at S8 = {S8_C:.3f} -- on the")
print("    CMB/KiDS-Legacy side of the 2026 S8 bifurcation and >=2 sigma AGAINST the")
print("    low DES Y6 value: TFPT predicts the DES-vs-KiDS split resolves on the")
print("    KiDS side (survey systematics), exactly as it predicts the Hubble split")
print("    resolves on the Planck side (flat_budget_closure).")
print(f"    A_s branch spread: N*=51.4 -> S8 = {s8A:.3f} (disfavoured branch);")
print(f"    N*=56.1 -> S8 = {s8B:.3f}; geometry-only -> {S8_C:.3f}.")
print("    FLAGS: Omega_c leg numerology-flagged (single p/q<=12 hit, post-hoc,")
print("    collides with the axion-spine DM branch as alternative reading); A_s")
print("    branch ambiguity documented in cmb-inflation-scalaron; tau_reio = 0.054")
print("    imported (S8 insensitive at the quoted precision).")
print("    KILL (prereg): a systematics-converged lensing S8 <= 0.79 replicated")
print("    across KiDS/DES/HSC/LSST (i.e. the DES-side reading winning) at >= 5")
print("    sigma from the budget value strikes the closure pattern -- the frozen")
print("    Omega_b / Lambda records are untouched (only the closure PATTERN falls).")

print()
if FAILS:
    print(f"RESULT: {len(FAILS)} check(s) FAILED: {FAILS}")
    raise SystemExit(1)
print("ALL CHECKS PASS -- pattern_candidate (sandbox; nothing promoted)")
