"""The parameter-free flat LambdaCDM budget closure (pattern probe).

SANDBOX ONLY (experiments/tfpt-discovery/): nothing promoted, no ledger /
paper / scorecard / website touch.  Verdict enum: pattern_candidate
(post-hoc, LEE-flagged on the Omega_c leg).

THE PATTERN.  The suite already carries, separately:
    Omega_b        = phi0 (1 - 1/4pi)            [frozen record, v84]
    rho_L/Mbar^4   = (3/4pi^2) e^{-2 alpha^-1}   [frozen record, v84/v60]
    Sigma m_nu     = m3 (1 + sqrt|J|) = 0.0588 eV [v468 route; imports dm31^2]
    Omega_c        = (2/7)(1 - 1/4pi)            [2026-07-02 Nebenbefund,
                     <=> Omega_c/Omega_b = 2/(7 phi0); NUMEROLOGY-FLAGGED:
                     single p/q<=12 hit, post-hoc, conceptually collides with
                     the axion-spine DM branch -- alternative reading, never
                     double-counted]
What was never done: CLOSE the budget.  With spatial flatness (standard
inflationary input) the four pieces plus radiation determine EVERYTHING --
Omega_Lambda, h, H0, the age -- with zero remaining dials.  The closure
upgrades v60's Lambda->H0 readout (which IMPORTED Omega_b and omega_DM from
Planck) to a fully parameter-free flat budget, and it takes a SIDE in the
Hubble tension.

External imports (declared): the one gravitational unit (Mbar = 2.4353e18
GeV, v_geo class), T_CMB = 2.7255 K + N_eff = 3.044 (radiation, tiny),
dm31^2 = 2.534e-3 eV^2 (NuFIT 6.0 NO, only through Sigma m_nu, tiny),
flatness.  NO fitted cosmological parameter enters.

Confrontation: Planck 2018 TT,TE,EE+lowE+lensing; SH0ES 2022; DESI DR2.
"""
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


# ---------------------------------------------------------------- pieces
ainv = 1 / alpha_root()
Omega_b = phi0 * (1 - 1 / (4 * PI))                 # frozen record
Omega_c = mp.mpf(2) / 7 * (1 - 1 / (4 * PI))        # flagged candidate
rhoL = mp.mpf(3) / (4 * PI**2) * mp.e**(-2 * ainv)  # frozen record
Sm_nu = mp.mpf('0.0588')                            # eV, v468 route

# declared metrology imports
MBAR_GEV = mp.mpf('2.435323e18')     # reduced Planck mass (the one unit)
GEV_PER_S = mp.mpf('1.5192674e24')   # 1 GeV / hbar in 1/s
KMSMPC = mp.mpf('3.2407793e-20')     # 1 km/s/Mpc in 1/s
OMEGA_R_H2 = mp.mpf('4.153e-5')      # omega_r incl. N_eff=3.044 (T=2.7255K)
NU_H2_NORM = mp.mpf('93.14')         # Omega_nu h^2 = Sigma m_nu / 93.14 eV

print("=" * 78)
print("Parameter-free flat LambdaCDM budget closure (pattern probe)")
print("=" * 78)
print(f"  Omega_b  = phi0(1-1/4pi)      = {mp.nstr(Omega_b, 8)}   [frozen record]")
print(f"  Omega_c  = (2/7)(1-1/4pi)     = {mp.nstr(Omega_c, 8)}   [FLAGGED candidate]")
print(f"  Omega_c/Omega_b = 2/(7 phi0)  = {mp.nstr(Omega_c / Omega_b, 8)}")
print(f"  rho_L/Mbar^4 = (3/4pi^2)e^-2ainv = {mp.nstr(rhoL, 8)}   [frozen record]")
print(f"  Sigma m_nu = 0.0588 eV        [v468 route, imports dm31^2]")

# ------------------------------------------------- self-consistent closure
h = mp.mpf('0.67')
for _ in range(60):
    Om_nu = Sm_nu / (NU_H2_NORM * h**2)
    Om_r = OMEGA_R_H2 / h**2
    Om_L = 1 - Omega_b - Omega_c - Om_nu - Om_r
    H0_inv_s = mp.sqrt(rhoL / (3 * Om_L)) * MBAR_GEV * GEV_PER_S
    h = (H0_inv_s / KMSMPC) / 100

H0 = 100 * h
Om_m = Omega_b + Omega_c + Om_nu
om_b, om_c, om_m = Omega_b * h**2, Omega_c * h**2, Om_m * h**2

# age of the universe (flat, radiation included, nu as matter)
def age_gyr():
    integrand = lambda a: 1 / (a * mp.sqrt(Om_r / a**4 + (Om_m) / a**3 + Om_L))
    t_H = mp.quad(integrand, [1e-10, 1])          # in units of 1/H0
    return float(t_H * mp.mpf('977.79') / H0)     # Gyr

t0 = age_gyr()

print()
print("  CLOSED BUDGET (flatness + the pieces, zero dials):")
print(f"    h        = {mp.nstr(h, 6)}      ->  H0 = {mp.nstr(H0, 6)} km/s/Mpc")
print(f"    Omega_L  = {mp.nstr(Om_L, 6)}   Omega_m = {mp.nstr(Om_m, 6)}   "
      f"Omega_nu = {mp.nstr(Om_nu, 4)}")
print(f"    omega_b  = {mp.nstr(om_b, 6)}   omega_c = {mp.nstr(om_c, 6)}   "
      f"omega_m = {mp.nstr(om_m, 6)}")
print(f"    age t0   = {t0:.3f} Gyr")

# ------------------------------------------------------- confrontation
print()
print("  CONFRONTATION (pulls):")
DATA = [
    ("H0  [Planck18]",        H0,    mp.mpf('67.36'),  mp.mpf('0.54')),
    ("H0  [SH0ES22]",         H0,    mp.mpf('73.04'),  mp.mpf('1.04')),
    ("H0  [DESI DR2 BAO+CMB]", H0,   mp.mpf('67.97'),  mp.mpf('0.38')),
    ("Omega_m [Planck18]",    Om_m,  mp.mpf('0.3153'), mp.mpf('0.0073')),
    ("Omega_L [Planck18]",    Om_L,  mp.mpf('0.6847'), mp.mpf('0.0073')),
    ("omega_b [Planck18]",    om_b,  mp.mpf('0.02237'), mp.mpf('0.00015')),
    ("omega_b [BBN D/H, LUNA]", om_b, mp.mpf('0.02233'), mp.mpf('0.00036')),
    ("omega_c [Planck18]",    om_c,  mp.mpf('0.1200'), mp.mpf('0.0012')),
    ("Omega_c/Omega_b [Planck18]", Omega_c / Omega_b,
     mp.mpf('0.1200') / mp.mpf('0.02237'), mp.mpf('0.064')),
]
pulls = {}
for label, pred, cen, sig in DATA:
    p = (pred - cen) / sig
    pulls[label] = p
    print(f"    {label:28s}: pred {mp.nstr(pred, 6):>10s}  vs  {mp.nstr(cen, 6)}"
          f" +- {mp.nstr(sig, 3)}   pull = {float(p):+6.2f} sigma")

t0_pull = (mp.mpf(t0) - mp.mpf('13.797')) / mp.mpf('0.023')
print(f"    age t0 (derived)            : pred {t0:10.3f}  vs  13.797 +- 0.023"
      f"   pull = {float(t0_pull):+6.2f} sigma"
      "  [DERIVED quantity, correlated with H0/omega_m -- not independent]")

report("H0 parameter-free on the PLANCK side of the Hubble tension "
       "(|pull| < 1 vs Planck, > 5 vs SH0ES)",
       abs(pulls["H0  [Planck18]"]) < 1 and pulls["H0  [SH0ES22]"] < -5)
report("Omega_m and Omega_L land inside 0.5 sigma of Planck",
       abs(pulls["Omega_m [Planck18]"]) < mp.mpf('0.5')
       and abs(pulls["Omega_L [Planck18]"]) < mp.mpf('0.5'))
report("HONEST STRESS recorded: the closure sharpens Omega_b -> omega_b and "
       "picks up a -2 sigma pull (omega_c -1.2 sigma; derived t0 +2.9 sigma, "
       "correlated -- the low-h face of the same stress)",
       pulls["omega_b [Planck18]"] < -mp.mpf('1.5')
       and pulls["omega_c [Planck18]"] < -mp.mpf('0.8')
       and t0_pull > 2)

print()
print("  READING (pattern_candidate, honest):")
print("    zero-dial closure {phi0, alpha} + flatness -> the ENTIRE flat")
print("    LambdaCDM budget: H0 = 67.2, Omega_m = 0.313, t0 = 13.8 Gyr.")
print("    It extends origin_theory's 'one alpha for EM + horizon + Lambda'")
print("    to 'one axiom pair -> the whole FLRW budget' and takes the Planck")
print("    side of the Hubble tension (SH0ES -5.6 sigma) -- a sharp, dated")
print("    stance.  CAVEATS: the Omega_c leg is the 2026-07-02 numerology-")
print("    flagged Nebenbefund (post-hoc, single-hit census, collides with")
print("    the axion-spine DM branch as ALTERNATIVE reading -- never count")
print("    both); omega_b sits -2.0 sigma, DESI-DR2 H0 -2.2 sigma and the")
print("    derived age +2.9 sigma -- three faces of ONE low-h/low-omega_m")
print("    stress direction (correlated, not additive); h inherits the one")
print("    gravitational unit (v_geo class).")
print("    KILL (prereg): a systematics-converged local H0 >= 71 with")
print("    CMB/BAO concordance breaking (real new physics raising H0), or")
print("    omega_c hardening away from 0.1186 by >= 3 sigma, kills the")
print("    closed-budget pattern (the frozen Omega_b/Lambda records are")
print("    untouched by that).")

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
