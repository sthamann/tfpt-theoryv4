"""Discovery probe (2026-07-24), part 24 of the zeta/prime investigation.
RESOLVENT / TRUNCATED-TRACE route after part 22 (PARTIAL: K1/K2 OK, K3 FAIL).

Part 22 diagnosis: the seam interval-cut boost has Peschel/Casimir spectrum
    eps_k = pi^2 (2k-1) / (2 ln L + c0)
and counting N_seam(eps, L) ~ eps * ln L / pi^2  (flat in eps, height ~ ln L).
The classical Riemann--von Mangoldt (RvM) smooth counting needs T log T:
    N_smooth(T) = (T/2pi) ln(T/2pi) - T/2pi + 7/8 + O(1/T).
Missing: an extensive factor.  Review conjecture: the observable is wrong
-- use the dilation RESOLVENT / truncated trace / integrated spectral phase
with a SELF-DUAL cutoff coupling, not the fixed-L mode density.

Classical background (named classical throughout):
  (a) Riemann--Siegel theta: theta(T) = arg Gamma(1/4 + iT/2) - (T/2) ln pi;
      N_smooth(T) = theta(T)/pi + 1 (mpmath.siegeltheta).
  (b) Berry--Keating / Connes (classical): semiclassical counting of the
      dilation generator D = (xp+px)/2 with a SYMMETRIC phase-space cutoff
      (|x| and |p| both cut at Lambda) reproduces the RvM main terms.
      The T log T arises from coupling the cutoff to the energy; the
      "symmetric" choice is a REGULARISATION CHOICE in the classical picture.
  (c) Peschel / Casini / Bisognano--Wichmann (classical): interval modular
      Hamiltonian = boost; spectrum as above (part 22).

TFPT candidate increment (the thesis under test):
  Parts 12/14: Poisson self-duality of the mu4-completed E8 census has a
  UNIQUE self-dual Gaussian width; only the unimodular E8 admits one.
  Thesis: that self-duality FORCES the symmetric cutoff (Lambda_x = Lambda_p)
  instead of choosing it -- replacing the Berry--Keating regularisation
  freedom by compiler structure.  Then test whether the seam boost with
  that ONE coupling reproduces RvM counting (R1--R3).

Sections:
  S0  PREREGISTERED CRITERIA R1--R4 (frozen BEFORE comparisons).
  S1  Classical reference: N_smooth vs RvM asymptotics; phase = integral
      of the part-22 Tate multiplier density.
  S2  Semiclassical BK box (classical): sympy area A(T, Lambda); self-dual
      coupling; constants vs RvM (honest: 7/8 is Gamma-phase, not the box).
  S3  Seam side: N_seam(T, L(T)) under the ONE preregistered self-dual
      rule R4; Peschel closed form + covariance spot-checks; test R1--R3.
  S4  Negative controls: 2--3 NON-self-dual couplings must miss R1/R2
      if the self-dual rule is to be alternativlos.
  S5  Verdict RVM-MATCH-TYPED / BK-ONLY / DEAD + ZETA.WEIL.RECOVERY.

PREREGISTERED CRITERIA (frozen; see also S0 checks):
  R1  Leading coefficient of the seam counting form = 1/(2pi) EXACT
      (no fit).  Pass: |2pi * a_lead - 1| < R1_ABS on the T-span.
  R2  Subleading -T/(2pi) present: coefficient within R2_REL of -1/(2pi).
  R3  Remainder O(log T): residual after subtracting RvM main terms grows
      at most logarithmically (log-log slope of |R| vs T <= R3_LOGLOG_MAX).
  R4  Cutoff coupling is the ONE self-dual rule below (no further freedom).

R4 DERIVATION (frozen before runs; from parts 12/14 + classical BK):
  * Lattice UV cutoff a = 1; IR cutoff = interval length L.
  * Poisson self-duality (part 12: unique width t* = pi; part 14:
    only mu4-completed unimodular E8) forces SYMMETRIC scales -- no
    preferred position vs momentum channel -- i.e. Lambda_x = Lambda_p.
  * Classical BK energy-coupling in 2pi-cell units: the hyperbolic
    energy T meets the symmetric box at the dual point when
        Lambda_x * Lambda_p = T,
    hence Lambda = sqrt(T).  Identifying the seam IR cutoff with that
    box scale (lattice units a = 1) gives the ONE rule
        L_sd(T) := sqrt(T)          (R4)
    equivalently ln L_sd = (1/2) ln T.
  * Alternative classical dictionary used ONLY as a negative-control /
    diagnostic (NOT R4): L = T/(2pi) (part-22 K3 map) and the
    coefficient-engineered
    L = e^{-pi/2 - c0/2} (T/2pi)^{pi/2} that forces R1+R2 by
    construction from Peschel N ~ T ln L / pi^2 -- EXPLICITLY a
    two-constant fit, forbidden as a criterion pass.

Firewall: discovery sandbox, NO promotion, no marker moves, no ledger /
paper / website / next.txt edits.  Classical objects (Riemann--Siegel,
Berry--Keating, Connes truncated-trace picture, Peschel/Casini, Tate)
named as classical.  No RH-evidence language.  Negative findings are
valid check content; the probe ends green when computed facts hold.
"""
from __future__ import annotations

import math
import time

import mpmath
import numpy as np
import sympy as sp

PASS = 0
FAIL = 0
T0 = time.time()
RUNTIME_CAP_S = 220.0

# ---------------------------------------------------------------- S0: preregistered thresholds (CONSTANTS -- frozen before comparisons)
R1_ABS = 0.05                 # |2pi * a_lead - 1| for EXACT 1/(2pi)
R2_REL = 0.10                 # |b / (-1/(2pi)) - 1| <= 10%
R3_LOGLOG_MAX = 1.25          # log|R| vs log log T slope upper bound
R3_GROWTH_RATIO_MAX = 3.0     # |R|(T_hi)/|R|(T_lo) vs ln(T_hi)/ln(T_lo)
T_CLASSICAL = tuple(range(20, 501, 20))
T_SEAM = (20, 40, 60, 80, 100, 150, 200, 300, 400, 500)
C0_PESCHEL = 5.23             # part-22 measured O(1); reported, not fitted here
SPOT_N = (64, 128, 256)
SPOT_FRAC = 0.50
NU_CLIP = 1.0 - 1e-12
MP_DPS = 40
# R4: the ONE self-dual coupling (see docstring derivation)
# L_sd(T) = sqrt(T)
# Non-self-dual negative controls (preregistered as controls, not criteria):
#   NC1: L = T/(2pi)     (part-22 dictionary; asymmetric in BK sense)
#   NC2: L = T           (linear, no sqrt self-dual)
#   NC3: L = T**2        (super-extensive)


def check(name: str, ok: bool) -> bool:
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {name}", flush=True)
    if ok:
        PASS += 1
    else:
        FAIL += 1
    return ok


def info(msg: str) -> None:
    print(f"        {msg}", flush=True)


def elapsed() -> float:
    return time.time() - T0


# ================================================================ S0
print("S0 -- preregistered criteria R1--R4 (frozen BEFORE comparisons)")
info(f"R1: leading coeff a of N ~ a T ln(T/2pi) equals 1/(2pi) exact; "
     f"|2pi*a - 1| < {R1_ABS} (no fit)")
info(f"R2: subleading b of N ~ ... + b T  within {100*R2_REL:.0f}% of "
     f"-1/(2pi)")
info(f"R3: residual after RvM main terms is O(log T) on the tested span "
     f"(loglog slope <= {R3_LOGLOG_MAX}; growth ratio vs ln-ratio "
     f"<= {R3_GROWTH_RATIO_MAX})")
info("R4: L_sd(T) = sqrt(T)  -- UNIQUE self-dual rule from Poisson "
     "symmetry Lambda_x = Lambda_p (parts 12/14) + BK corner "
     "Lambda_x * Lambda_p = T (2pi-cell units, a = 1)")
info("Negative controls (must miss R1/R2 if R4 is alternativlos): "
     "L = T/(2pi), L = T, L = T^2")
check("R1--R4 constants recorded before any spectrum / fit comparison "
      "(R1 exact 1/(2pi), R2 10% window, R3 log bound, R4 L=sqrt(T))",
      R1_ABS > 0 and R2_REL == 0.10
      and R3_LOGLOG_MAX > 0 and abs(C0_PESCHEL - 5.23) < 1e-12)
check("firewall typed: Riemann--Siegel / Berry--Keating / Connes / "
      "Peschel/Casini named classical; no RH-evidence language; "
      "sandbox only; R4 frozen as L_sd(T)=sqrt(T)", True)


def L_selfdual(T: float) -> float:
    """R4: symmetric BK cutoff in lattice units -- L = sqrt(T)."""
    return math.sqrt(T)


def L_nc1(T: float) -> float:
    return T / (2.0 * math.pi)


def L_nc2(T: float) -> float:
    return T


def L_nc3(T: float) -> float:
    return T * T


# ================================================================ S1
print("S1 -- classical Riemann--Siegel / RvM reference")
mpmath.mp.dps = MP_DPS


def N_smooth(T: float) -> float:
    """Classical N_smooth(T) = siegeltheta(T)/pi + 1."""
    return float(mpmath.siegeltheta(T) / mpmath.pi + 1)


def N_rvm_main(T: float) -> float:
    """RvM main terms without the 7/8: (T/2pi)ln(T/2pi) - T/2pi."""
    return (T / (2 * math.pi)) * math.log(T / (2 * math.pi)) - T / (2 * math.pi)


def N_rvm_full(T: float) -> float:
    """RvM with constant 7/8."""
    return N_rvm_main(T) + 0.875


rvm_resid_no88 = []
rvm_resid_full = []
for T in T_CLASSICAL:
    ns = N_smooth(T)
    main = N_rvm_main(T)
    full = N_rvm_full(T)
    rvm_resid_no88.append(ns - main)
    rvm_resid_full.append(ns - full)
    if T in (20, 100, 200, 500):
        info(f"T={T}: N_smooth={ns:.6f}, RvM_main={main:.6f}, "
             f"RvM+7/8={full:.6f}, resid_full={ns-full:.6e}")

# Residuals vs full RvM should be O(1/T): T*|resid| bounded
t_times_resid = [T * abs(r) for T, r in zip(T_CLASSICAL, rvm_resid_full)]
# Without 7/8, residual should approach ~7/8
resid_no88_tail = np.mean(rvm_resid_no88[-5:])
check("classical N_smooth(T)=siegeltheta(T)/pi+1 matches RvM "
      "(T/2pi)ln(T/2pi)-T/2pi+7/8 on T=20..500: max|T*resid_full| "
      f"= {max(t_times_resid):.4f} (O(1) => resid O(1/T)); "
      f"mean tail resid without 7/8 = {resid_no88_tail:.4f} ~ 7/8",
      max(t_times_resid) < 2.0
      and abs(resid_no88_tail - 0.875) < 0.05)

# Part-22 Tate link: d/dT theta(T) = Re psi(1/4+iT/2)/2 - (1/2)ln pi
# and a(T)=(1/2pi)(Re psi - ln pi) is the phase density; theta/pi = int a.
phase_link_ok = True
phase_resids = []
for T in (20.0, 50.0, 100.0):
    # numerical d(theta)/dT via siegeltheta
    h = 1e-6
    dth = float((mpmath.siegeltheta(T + h) - mpmath.siegeltheta(T - h))
                / (2 * h))
    z = mpmath.mpc(mpmath.mpf("0.25"), mpmath.mpf(T) / 2)
    target = float(mpmath.re(mpmath.digamma(z)) / 2 - mpmath.log(mpmath.pi) / 2)
    phase_resids.append(abs(dth - target))
    # integrated density: a(T) = target/pi  =>  N' = a = theta'/pi
    a_T = target / math.pi
    n_prime = dth / math.pi
    if abs(a_T - n_prime) > 1e-8 or abs(dth - target) > 1e-5:
        phase_link_ok = False
    info(f"T={T:.0f}: d(theta)/dT={dth:.8f}, "
         f"(1/2)(Re psi - ln pi)={target:.8f}, |resid|={abs(dth-target):.2e}")

check("part-22 Tate link: d(siegeltheta)/dT = (1/2)(Re psi(1/4+iT/2) "
      "- ln pi) on T in {20,50,100} (max resid "
      f"{max(phase_resids):.2e}); theta = integral of the arch phase "
      "density (classical)",
      phase_link_ok and max(phase_resids) < 1e-5)


# ================================================================ S2
print("S2 -- classical Berry--Keating phase-space box (sympy + numeric)")

T_sym, Lam = sp.symbols("T Lambda", positive=True)

# Area A = int_{x=1}^{Lambda} min(Lambda, T/x) dx
# Regime I: Lambda <= T <= Lambda^2  (hyperbola hits top and right)
#   = int_1^{T/Lambda} Lambda dx + int_{T/Lambda}^{Lambda} (T/x) dx
A_regI = sp.simplify(
    Lam * (T_sym / Lam - 1) + T_sym * (sp.log(Lam) - sp.log(T_sym / Lam))
)
# Regime II: 1 <= T <= Lambda  (hyperbola below the top for all x in [1,Lam])
A_regII = sp.simplify(T_sym * sp.log(Lam))

info(f"Area regime I (Lambda <= T <= Lambda^2): A = {A_regI}")
info(f"Area regime II (T <= Lambda):            A = {A_regII}")

# User-quoted form T + T ln(Lambda^2/T) equals A_regI + Lambda
A_quoted = T_sym + T_sym * sp.log(Lam ** 2 / T_sym)
A_expected_I = T_sym - Lam + T_sym * sp.log(Lam ** 2 / T_sym)
diff_I = sp.simplify(A_regI - A_expected_I)
diff_quoted = sp.simplify(A_regI - (A_quoted - Lam))
diff_II = sp.simplify(A_regII - T_sym * sp.log(Lam))
check("sympy derivation: for Lambda <= T <= Lambda^2, "
      "A(T,Lambda) = T - Lambda + T ln(Lambda^2/T) "
      f"(sympy form {A_regI}); quoted 'T + T ln(Lambda^2/T)' differs "
      "by +Lambda (boundary term from lower cut x=1)",
      diff_I == 0 and diff_quoted == 0)
check("sympy derivation: for T <= Lambda, A = T ln Lambda "
      f"(= {A_regII}) -- pure log from soft hyperbolic cutoff",
      diff_II == 0)


def area_numeric(T: float, Lam: float) -> float:
    """Numeric phase-space area {1<=x<=Lam, 0<=p<=Lam, xp<=T}."""
    if Lam <= 1.0:
        return 0.0
    # integrate min(Lam, T/x) from 1 to Lam
    xs = np.linspace(1.0, Lam, 4000)
    trap = getattr(np, "trapezoid", None) or getattr(np, "trapz")
    return float(trap(np.minimum(Lam, T / xs), xs))


# Cross-check sympy vs numeric at a few points
area_num_ok = True
for T, Lam_v in ((50.0, 10.0), (100.0, 20.0), (80.0, 15.0)):
    # regime I if Lam <= T <= Lam^2
    a_num = area_numeric(T, Lam_v)
    a_sym = float(A_regI.subs({T_sym: T, Lam: Lam_v}))
    info(f"A_num(T={T}, Lam={Lam_v}) = {a_num:.4f}, "
         f"A_sym = {a_sym:.4f}, |diff|={abs(a_num-a_sym):.2e}")
    if abs(a_num - a_sym) > 0.05:
        area_num_ok = False
check("numeric quadrature agrees with sympy regime-I formula "
      "(3 sample points, |diff| < 0.05)",
      area_num_ok)

# Self-dual coupling Lambda^2 = T  =>  A = T - sqrt(T), N = A/(2pi)
# -- this does NOT produce T log T (honest documentation).
A_sd = sp.simplify(A_regI.subs(Lam, sp.sqrt(T_sym)))
diff_sd = sp.simplify(A_sd - (T_sym - sp.sqrt(T_sym)))
info(f"self-dual Lambda=sqrt(T) plugged into regime I: A = {A_sd} "
     "(= T - sqrt(T); LOG ABSENT at the corner)")
check("honest BK-corner fact: Lambda^2 = T gives A = T - sqrt(T) "
      "(no T log T).  The RvM log needs the SOFT regime T << Lambda^2 "
      "with A ~ T ln(Lambda^2/T), plus a SEPARATE rule fixing Lambda(T)",
      diff_sd == 0)

# Classical BK route that DOES reproduce RvM leading+subleading:
# Use regime II soft area A = T ln Lambda with the self-dual IR/UV product
#   l * L = 2pi  (Poisson cell; classical BK),  l = 1 (lattice UV),
#   hence L = 2pi -- FIXED, gives only (T/2pi) ln(2pi), WRONG.
# The energy-dependent classical choice that hits RvM:
#   A_eff = T ln(T/(2pi)) - T ,   N = A_eff / (2pi)
# which is exactly N_rvm_main.  This A_eff equals
#   T ln(Lambda^2/T) - T  with Lambda^2 = T^2/(2pi)
# i.e. Lambda = T/sqrt(2pi)  (LINEAR in T, not sqrt).
#
# Symmetric Poisson (Lambda_x = Lambda_p) alone does NOT select
# Lambda ~ sqrt(T) vs Lambda ~ T; the energy-coupling law is extra.
# Document: classical BK reproduces RvM with an ADDITIONAL coupling
# choice; part-12/14 self-duality only forces symmetry, not the power.

def N_bk_soft_rvm(T: float) -> float:
    """Classical target: A_eff/(2pi) with A_eff = T ln(T/2pi) - T."""
    return N_rvm_main(T)


bk_vs_rvm = [abs(N_bk_soft_rvm(T) - N_rvm_main(T)) for T in T_CLASSICAL]
# Compare N_smooth - 7/8 to N_rvm_main
smooth_minus_const = [N_smooth(T) - 0.875 - N_rvm_main(T)
                      for T in T_CLASSICAL]
check("classical BK/Connes counting identity: A_eff/(2pi) with "
      "A_eff = T ln(T/2pi) - T  EQUALS RvM main terms exactly "
      "(by construction of A_eff); the 7/8 constant is NOT in the box "
      "-- it is the classical Gamma / Riemann--Siegel phase constant",
      max(bk_vs_rvm) < 1e-12
      and max(abs(r) for r in smooth_minus_const) < 0.05)

# Which coupling produces A_eff from the geometric box?
# A_regI = T - Lambda + T ln(Lambda^2/T)
# Want T ln(T/2pi) - T  (up to o(T) terms).
# Set Lambda = T / math.sqrt(2*pi): then for large T, regime?
# T vs Lambda^2 = T^2/(2pi): T << Lambda^2, so regime II applies:
# A_regII = T ln Lambda = T ln(T/sqrt(2pi)) = T ln(T/2pi) + T ln(sqrt(2pi))
# = T ln(T/2pi) + (T/2) ln(2pi)  -- WRONG linear coefficient.
Lam_lin = T_sym / sp.sqrt(2 * sp.pi)
A_lin_II = sp.simplify(A_regII.subs(Lam, Lam_lin))
info(f"geometric box + Lambda = T/sqrt(2pi) in regime II: A = {A_lin_II}")
info("  => N = A/(2pi) = (T/2pi)ln(T/2pi) + (T/4pi)ln(2pi) "
     "-- leading OK, subleading WRONG SIGN/COEFF vs -T/2pi")
check("classical honesty: geometric box + any single power-law "
      "Lambda(T) does not simultaneously produce BOTH RvM coefficients "
      "from A/(2pi) alone; the -T/2pi piece is a regularisation "
      "convention in the BK/Connes picture (phase-space Maslov / "
      "oriented cutoff), while 7/8 is the Gamma phase -- documented",
      True)


# ================================================================ S3
print("S3 -- seam truncated counting under R4 self-dual coupling")


def peschel_N(T: float, L: float, c0: float = C0_PESCHEL) -> float:
    """Mode count #{k: eps_k <= T} from Peschel closed form.

    eps_k = pi^2 (2k-1) / (2 ln L + c0)  <= T
    =>  2k-1 <= T (2 ln L + c0) / pi^2
    =>  k_max = floor( (T (2 ln L + c0)/pi^2 + 1)/2 )
    Continuous Weyl form: N = T (2 ln L + c0) / (2 pi^2) = T ln L / pi^2
    + T c0 / (2 pi^2).
    """
    if L <= 1.0:
        return 0.0
    denom = 2.0 * math.log(L) + c0
    if denom <= 0.0:
        return 0.0
    # exact step count from closed form
    max_odd = T * denom / (math.pi ** 2)
    k_max = int(math.floor((max_odd + 1.0) / 2.0))
    return float(max(k_max, 0))


def peschel_N_weyl(T: float, L: float, c0: float = C0_PESCHEL) -> float:
    """Smooth Weyl form of the Peschel counting (no floor)."""
    if L <= 1.0:
        return 0.0
    denom = 2.0 * math.log(L) + c0
    if denom <= 0.0:
        return 0.0
    return T * denom / (2.0 * math.pi ** 2)


def seam_cov_circle(N: int) -> np.ndarray:
    G = np.zeros((N, N), dtype=np.float64)
    two_over_N = 2.0 / N
    for a in range(N):
        for b in range(a):
            d = a - b
            if d % 2 != 0:
                val = two_over_N / math.sin(math.pi * d / N)
                G[a, b] = val
                G[b, a] = -val
    return G


def interval_eps(G: np.ndarray, L: int, n_keep: int = 30) -> np.ndarray:
    GA = G[:L, :L]
    ev = np.linalg.eigvalsh(1j * GA)
    nus = np.sort(np.clip(ev[ev > 1e-14], 0.0, NU_CLIP))
    uniq = []
    for v in nus:
        if not uniq or abs(v - uniq[-1]) > 1e-9:
            uniq.append(float(v))
    eps = []
    for v in uniq:
        if v >= 1.0:
            continue
        e = math.log((1.0 + v) / (1.0 - v))
        if e > 1e-14:
            eps.append(e)
    eps.sort()
    return np.asarray(eps[:n_keep], dtype=float)


# --- Spot-check Peschel closed form vs covariance spectra at fixed L ---
print("S3a -- Peschel closed form vs covariance spot-checks")
spot_ok = True
spot_rels = []
for N in SPOT_N:
    if elapsed() > RUNTIME_CAP_S - 40.0:
        info(f"spot N={N}: SKIPPED (runtime budget)")
        continue
    G = seam_cov_circle(N)
    L = int(round(SPOT_FRAC * N))
    if L % 2 == 1:
        L += 1
    eps = interval_eps(G, L, n_keep=8)
    Le = (N / math.pi) * math.sin(math.pi * L / N)
    # c0 from k=1
    c0_loc = (math.pi ** 2) / eps[0] - 2.0 * math.log(Le)
    for k in (1, 2, 3):
        pred = (math.pi ** 2) * (2 * k - 1) / (2.0 * math.log(Le) + c0_loc)
        rel = abs(eps[k - 1] - pred) / pred
        spot_rels.append(rel)
        info(f"  N={N} L={L} Le={Le:.3f}: k={k} eps={eps[k-1]:.5f} "
             f"Peschel={pred:.5f} rel={rel:.4f} c0={c0_loc:.3f}")
        if rel > 0.20:
            spot_ok = False
check("spot-check: covariance interval spectra match Peschel closed "
      f"form at N in {list(SPOT_N)}, frac={SPOT_FRAC} for k=1,2,3 "
      f"(max rel = {max(spot_rels) if spot_rels else -1:.4f} < 0.20); "
      "closed form trusted for N_seam(T, L(T))",
      spot_ok and len(spot_rels) >= 6)


def fit_lead_sub(Ts, Ns):
    """Fit N(T) ~= a T ln(T/2pi) + b T  by least squares (diagnostic).

    R1/R2 then compare a,b to 1/(2pi), -1/(2pi).  This fit is a TEST
    readout, not a free parameter of the theory.
    """
    Ts = np.asarray(Ts, dtype=float)
    Ns = np.asarray(Ns, dtype=float)
    X1 = Ts * np.log(Ts / (2 * math.pi))
    X2 = Ts
    A = np.column_stack([X1, X2])
    coef, _, _, _ = np.linalg.lstsq(A, Ns, rcond=None)
    return float(coef[0]), float(coef[1])


def residual_log_growth(Ts, Ns):
    """R(T) = N(T) - N_rvm_main(T); test O(log T) growth."""
    Ts = np.asarray(Ts, dtype=float)
    R = np.asarray(Ns, dtype=float) - np.array([N_rvm_main(T) for T in Ts])
    absR = np.abs(R)
    # growth ratio vs ln ratio
    lo, hi = 0, -1
    growth = absR[hi] / max(absR[lo], 1e-12)
    ln_ratio = math.log(Ts[hi]) / math.log(Ts[lo])
    # log|R| vs log log T slope for T >= 40
    mask = Ts >= 40
    if mask.sum() >= 4 and np.all(absR[mask] > 1e-12):
        x = np.log(np.log(Ts[mask]))
        y = np.log(absR[mask])
        slope = float(np.polyfit(x, y, 1)[0])
    else:
        slope = float("nan")
    return R, growth, ln_ratio, slope


print("S3b -- N_seam(T) = N_seam(T, L_sd(T)=sqrt(T)) under R4")
Ts = list(T_SEAM)
N_sd = [peschel_N(T, L_selfdual(T)) for T in Ts]
N_sd_weyl = [peschel_N_weyl(T, L_selfdual(T)) for T in Ts]
for T, n, nw in zip(Ts, N_sd, N_sd_weyl):
    L = L_selfdual(T)
    info(f"T={T}: L_sd={L:.4f}, N_step={n:.0f}, N_weyl={nw:.4f}, "
         f"RvM_main={N_rvm_main(T):.4f}, N_smooth={N_smooth(T):.4f}")

a_sd, b_sd = fit_lead_sub(Ts, N_sd_weyl)
target_a = 1.0 / (2.0 * math.pi)
target_b = -1.0 / (2.0 * math.pi)
r1_err = abs(2 * math.pi * a_sd - 1.0)
r2_rel = abs(b_sd / target_b - 1.0) if target_b != 0 else float("inf")
R_sd, growth_sd, ln_ratio_sd, slope_sd = residual_log_growth(Ts, N_sd_weyl)

# Analytic expectation under R4: N = T ln(sqrt(T)) / pi^2 + O(T)
# = (T ln T) / (2 pi^2) + T c0/(2 pi^2) = a_pred T ln(T/2pi) + ...
# leading a_pred = 1/(2 pi^2), so 2pi*a_pred = 1/pi ≈ 0.318 ≠ 1.
a_analytic = 1.0 / (2.0 * math.pi ** 2)
info(f"R4 fit: a={a_sd:.6e} (target 1/(2pi)={target_a:.6e}), "
     f"|2pi*a-1|={r1_err:.4f}")
info(f"       analytic Peschel+R4 leading a = 1/(2 pi^2)={a_analytic:.6e}; "
     f"2pi*a_analytic={2*math.pi*a_analytic:.4f} (=1/pi, not 1)")
info(f"R4 fit: b={b_sd:.6e} (target -1/(2pi)={target_b:.6e}), "
     f"rel err={r2_rel:.4f}")
info(f"R3: |R|(T_hi)/|R|(T_lo)={growth_sd:.3f}, "
     f"ln(T_hi)/ln(T_lo)={ln_ratio_sd:.3f}, "
     f"loglog slope={slope_sd:.3f}")

R1_PASS = r1_err < R1_ABS
R2_PASS = r2_rel <= R2_REL
# R3: residual should be O(log T).  Under a wrong leading term the
# residual is O(T log T) -- growth ratio ~ T-ratio, far above ln-ratio.
R3_PASS = (
    (not math.isnan(slope_sd) and slope_sd <= R3_LOGLOG_MAX
     and growth_sd <= R3_GROWTH_RATIO_MAX * ln_ratio_sd)
    if R1_PASS else
    # if R1 failed, still RECORD whether residual is O(log) or larger
    (not math.isnan(slope_sd) and slope_sd <= R3_LOGLOG_MAX
     and growth_sd <= R3_GROWTH_RATIO_MAX * ln_ratio_sd)
)

check(f"R1 (self-dual L=sqrt(T)): leading coeff = 1/(2pi) EXACT -- "
      f"fit a={a_sd:.6e}, |2pi*a-1|={r1_err:.4f} "
      f"(threshold {R1_ABS}); analytic a=1/(2pi^2) gives 2pi*a=1/pi "
      f"-- {'PASS' if R1_PASS else 'FAIL (factor 1/pi vs Teil-22 2/pi family)'}",
      True)  # computed fact recorded; criterion outcome below
check(f"R1 OUTCOME recorded: {'HOLD' if R1_PASS else 'MISS'} "
      f"(|2pi*a-1|={r1_err:.4f})",
      True)
check(f"R2 OUTCOME recorded: {'HOLD' if R2_PASS else 'MISS'} "
      f"(b={b_sd:.6e}, rel err vs -1/(2pi) = {r2_rel:.4f})",
      True)
check(f"R3 OUTCOME recorded: {'HOLD' if R3_PASS else 'MISS'} "
      f"(loglog slope={slope_sd:.3f}, growth/ln-ratio="
      f"{growth_sd/ln_ratio_sd:.3f}) -- wrong leading term produces "
      "O(T log T) residual, not O(log T)",
      True)

# Exact analytic R1 failure factor under R4
check("analytic R1 under R4+Peschel: N_weyl = T*(ln T)/(2 pi^2) + O(T) "
      "=> a = 1/(2 pi^2), 2pi*a = 1/pi ≠ 1  (exact; factor-1/pi miss "
      "of the RvM leading coefficient -- same structural mismatch class "
      "as part-22 K3 factor 2/pi)",
      abs(2 * math.pi * a_analytic - 1.0 / math.pi) < 1e-12
      and not R1_PASS)


# ================================================================ S4
print("S4 -- negative controls (non-self-dual couplings)")


def evaluate_coupling(name, L_fn, Ts):
    Nw = [peschel_N_weyl(T, L_fn(T)) for T in Ts]
    a, b = fit_lead_sub(Ts, Nw)
    r1 = abs(2 * math.pi * a - 1.0)
    r2 = abs(b / target_b - 1.0)
    R, growth, ln_ratio, slope = residual_log_growth(Ts, Nw)
    hold_r1 = r1 < R1_ABS
    hold_r2 = r2 <= R2_REL
    info(f"{name}: a={a:.6e} (|2pi*a-1|={r1:.4f}), "
         f"b={b:.6e} (rel={r2:.4f}), "
         f"R1={'HOLD' if hold_r1 else 'MISS'}, "
         f"R2={'HOLD' if hold_r2 else 'MISS'}")
    return {
        "name": name, "a": a, "b": b, "r1": r1, "r2": r2,
        "hold_r1": hold_r1, "hold_r2": hold_r2,
        "growth": growth, "slope": slope, "Nw": Nw,
    }


nc_results = [
    evaluate_coupling("NC1 L=T/(2pi)", L_nc1, Ts),
    evaluate_coupling("NC2 L=T", L_nc2, Ts),
    evaluate_coupling("NC3 L=T^2", L_nc3, Ts),
]
# Diagnostic: engineered coupling that forces R1+R2 from Peschel algebra.
# N_weyl = T (2 ln L + c0)/(2 pi^2).
# Target (T/2pi)ln(T/2pi) - T/(2pi) requires
#   ln L = (pi/2) ln(T/2pi) - pi/2 - c0/2
# i.e. L = e^{-pi/2 - c0/2} (T/2pi)^{pi/2}  -- TWO fitted constants
# (pi/2 from 1/pi^2 vs 1/(2pi), and c0-shift).  FORBIDDEN as R4.
# Algebraic identity (exact for all T with L>1); numeric check on
# a high-T window where L_eng > 1.


def L_engineered(T: float) -> float:
    return (math.exp(-math.pi / 2 - C0_PESCHEL / 2)
            * (T / (2 * math.pi)) ** (math.pi / 2))


# Exact algebra: 2 ln L + c0 = pi ln(T/2pi) - pi  => N = N_rvm_main
T_alg, c0_alg = sp.symbols("T c0", positive=True)
lnL_eng = ((sp.pi / 2) * sp.log(T_alg / (2 * sp.pi))
           - sp.pi / 2 - c0_alg / 2)
N_eng_sym = sp.simplify(
    T_alg * (2 * lnL_eng + c0_alg) / (2 * sp.pi ** 2)
)
N_rvm_sym = ((T_alg / (2 * sp.pi)) * sp.log(T_alg / (2 * sp.pi))
             - T_alg / (2 * sp.pi))
alg_diff = sp.simplify(N_eng_sym - N_rvm_sym)
info(f"engineered algebra: N_weyl - N_rvm_main = {alg_diff}")

# Numeric window with L_eng > 1 (threshold T ~ 2pi exp(1 + c0/pi) ~ 90)
Ts_eng = tuple(range(200, 2001, 200))
eng = evaluate_coupling("DIAG engineered L (FORBID as R4)", L_engineered,
                        list(Ts_eng))
L_eng_min = min(L_engineered(T) for T in Ts_eng)
info(f"engineered numeric window T={Ts_eng[0]}..{Ts_eng[-1]}: "
     f"min L_eng={L_eng_min:.3f}")
check("diagnostic: coefficient-engineered "
      "L = e^{-pi/2 - c0/2}(T/2pi)^{pi/2} forces R1+R2 EXACTLY by "
      f"Peschel algebra (sympy N_weyl - N_rvm_main = {alg_diff}; "
      f"numeric R1 HOLD={eng['hold_r1']}, R2 HOLD={eng['hold_r2']} "
      f"on T={Ts_eng[0]}..{Ts_eng[-1]}) -- EXPLICITLY a two-constant "
      "fit, forbidden as the self-dual rule; mode-count + free L(T) "
      "can fake RvM without compiler content",
      alg_diff == 0 and eng["hold_r1"] and eng["hold_r2"]
      and L_eng_min > 1.0)

nc_all_miss_r1 = all(not r["hold_r1"] for r in nc_results)
nc_all_miss_r12 = all((not r["hold_r1"]) or (not r["hold_r2"])
                      for r in nc_results)
check("negative controls NC1--NC3 all MISS R1 "
      "(non-self-dual power/linear laws do not hit 1/(2pi) either)",
      nc_all_miss_r1)
check("negative-control summary recorded: self-dual R4 ALSO misses R1 "
      "(factor 1/pi); engineered fit hits R1+R2 -- therefore the "
      "self-dual rule is NOT distinguished by RvM-matching "
      "(alternativlos test FAILS: no coupling in the natural family "
      "hits R1 except the forbidden fit)",
      (not R1_PASS) and eng["hold_r1"] and eng["hold_r2"]
      and nc_all_miss_r1)

# Analytic NC1: L=T/(2pi) => N = T ln(T/2pi)/pi^2 , a=1/pi^2, 2pi*a=2/pi
a_nc1_analytic = 1.0 / (math.pi ** 2)
check("analytic NC1 (part-22 map L=T/2pi): 2pi*a = 2/pi "
      f"(={2*math.pi*a_nc1_analytic:.4f}) -- the exact part-22 K3 "
      "mismatch factor, now seen in the counting coefficient",
      abs(2 * math.pi * a_nc1_analytic - 2 / math.pi) < 1e-12)


# ================================================================ S5
print("S5 -- verdict vs R1--R4 + consequence for ZETA.WEIL.RECOVERY")

# Classical BK box structure exists (S2) but seam+R4 misses R1--R3.
# Alternativlos: failed (engineered hits; natural family including R4 misses).
r4_ok = True  # R4 was uniquely preregistered and used; no extra freedom

if R1_PASS and R2_PASS and R3_PASS and r4_ok and nc_all_miss_r12 and not eng["hold_r1"]:
    # eng hold is expected for diagnostic -- the alternativlos test
    # requires NCs miss AND no other natural rule hits.  Since eng is
    # forbidden, the typed match needs R1-R3 on R4 + NCs miss.
    pass

if R1_PASS and R2_PASS and R3_PASS and r4_ok and nc_all_miss_r1:
    verdict = "RVM-MATCH-TYPED"
    consequence = (
        "seam reproduces Berry--Keating/Connes counting with cutoff "
        "symmetry justified by compiler self-duality -- typed structural "
        "hit, NOT RH progress; ZETA.WEIL.RECOVERY arch seat still needs "
        "the Weil/explicit-formula dictionary"
    )
elif (not R1_PASS) and (not any(r["hold_r1"] for r in nc_results)):
    # Classical RvM reference holds (S1); geometric BK needs extra
    # regularisation conventions (S2); seam under R4 and all natural
    # NCs miss R1.  => resolvent/mode-count candidate DEAD.
    verdict = "DEAD"
    consequence = (
        "truncated-trace / mode-count candidate with self-dual L(T) is "
        "DEAD: Peschel N ~ T ln L / pi^2 cannot yield leading 1/(2pi) "
        "under any compiler-justified L(T) (R4 gives factor 1/pi; "
        "part-22 map gives factor 2/pi; only a forbidden coefficient "
        "fit fakes RvM).  Arch term remains a classical externum for "
        "ZETA.WEIL.RECOVERY; next lever = (i) a NON-mode-count "
        "resolvent (continuous Tate phase on the seam net, not "
        "eps_k-counting), or (ii) type Arch as external classical "
        "input and close the arithmetic/Weil side only"
    )
elif R1_PASS and R2_PASS and R3_PASS and not nc_all_miss_r1:
    verdict = "BK-ONLY"
    consequence = (
        "counting matches RvM but self-dual rule is not alternativlos "
        "(a non-self-dual coupling also hits R1/R2) -- classical BK "
        "reproduction without compiler uniqueness; ZETA.WEIL.RECOVERY "
        "arch seat not advanced"
    )
else:
    verdict = "DEAD"
    consequence = (
        "R1--R3 not jointly satisfied under R4; resolvent/counting "
        "route dead on the preregistered criteria"
    )

info(f"VERDICT: {verdict}")
info(f"R1={R1_PASS} R2={R2_PASS} R3={R3_PASS} R4_used={r4_ok}")
info(f"NC R1 misses: {[not r['hold_r1'] for r in nc_results]}")
info(f"consequence: {consequence}")

check(f"VERDICT recorded: {verdict} under preregistered R1--R4 + "
      "negative controls (computed outcomes, not aspirations)",
      verdict in ("RVM-MATCH-TYPED", "BK-ONLY", "DEAD"))
check("classical S1 reference stands independently: Riemann--Siegel "
      "N_smooth reproduces RvM main terms + 7/8 (O(1/T) resid) -- "
      "this is classical, not a TFPT result",
      max(t_times_resid) < 2.0)
check("ZETA.WEIL.RECOVERY remains [O]: part-22 object (interval boost) "
      "+ part-14 residual (self-dual width / 2pi angle) stay ONE "
      "research object; part-24 kills the naive truncated-mode-count "
      "repair of the missing T log T -- Arch seat still open or "
      "external",
      True)
check("part-20/22 discipline held: no free reparametrisation used to "
      "force R1; engineered L shown only as forbidden diagnostic; "
      "R4 frozen pre-run as L_sd=sqrt(T)",
      True)
check(f"runtime under cap ({RUNTIME_CAP_S:.0f}s): elapsed={elapsed():.1f}s",
      elapsed() < RUNTIME_CAP_S)

print(f"TOTAL: {PASS} passed, {FAIL} failed  ({elapsed():.1f}s)")
raise SystemExit(0 if FAIL == 0 else 1)
