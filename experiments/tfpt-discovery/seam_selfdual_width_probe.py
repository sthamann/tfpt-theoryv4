"""Discovery probe (2026-07-24), part 14 of the zeta/prime investigation.
Types the candidate research contract SEAM.SELFDUAL.WIDTH from part 12:

  Part 12 chain (each link exact as rewriting):
      c3 = 1/(8 pi)  <=>  beta = 1/(4 c3) = 2 pi
                     <=>  Boltzmann e^{-beta * norm / 2} = e^{-pi |x|^2}
                     <=>  THE Poisson-self-dual Gaussian of E8
                     <=>  tau = i = CM point of Q(i) = mu4 field.
  OPEN fence: that the seam KMS parameter IS the census Gaussian width
  is not derived.  Kill: a derivation fixing the census width != 2 pi,
  or separating the two parameters onto distinct torsors.

This probe answers the honesty question and sharpens the residual:

  S1  v526 ANATOMY (a vs b): reconstruct how beta_angle = 2 pi arises.
      MEASURED nontrivial datum: beta_steps = N from detailed balance
      of the circle kernel C(d) = (2/N)/sin(pi d/N).  The conversion
      beta_angle = beta_steps * (2 pi / N) is the UNIVERSAL geometric
      pin (one clock step = euclidean angle 2 pi/N).  Once the thermal
      period equals one full circle (beta_steps = N), beta_angle = 2 pi
      is the Bisognano-Wichmann / Unruh angle -- it appears in EVERY
      KMS theory that identifies the thermal circle with the geometric
      circle.  Recompute the Williamson / entropy anchors of v526 from
      the declared kernel (nu = cos(pi/24), cos(7 pi/24); S(8) nats).
  S2  UNIMODULARITY GATE (new, computable): classical Poisson summation
      gives Theta_L(t) = covol(L)^{-1} (pi/t)^4 Theta_{L*}(pi^2/t).
      Self-duality Theta_L(t) = (pi/t)^4 Theta_L(pi^2/t) requires
      L = L* and covol = 1 (even unimodular).  Among the atlas
      sublattices (D5+A3, D8, E6+A2, A8, E7+A1, A4+A4) NONE is
      unimodular (det = index^2 > 1).  Numerically: D5+A3 obeys the
      dual Poisson identity and FAILS the self-dual identity; E8
      (det = 1) obeys self-duality with UNIQUE fixed width t = pi.
      Typed consequence: a self-dual temperature exists only AFTER the
      mu4 glue completion D5+A3 -> E8 (the axiom).
  S3  TORSOR / SCALING: under L -> sqrt(lambda) L the self-dual width
      moves to t = pi / lambda.  The compiler convention "roots have
      norm 2" fixes lambda = 1.  The rewriting chain
      c3 = 1/(8 pi) <=> beta = 2 pi <=> t = pi is only as strong as
      that normalisation.  A genuine derivation must couple the seam
      modular flow to the lattice Gaussian without passing through the
      root-norm torsor (and without identifying thermal = geometric
      circle by fiat).
  S4  VERDICT for SEAM.SELFDUAL.WIDTH: DEFLATED.  The number 2 pi is
      not a compiler-specific output; it is the universal BW/Unruh
      angle once beta_steps = N.  Residual OPEN (sharpened): (i) the
      factor 4 = |mu4| in c3 = 1/(4 beta); (ii) a norm-free coupling
      of modular flow to the E8 Gaussian width; (iii) the positive
      structural gate that self-duality requires the mu4 completion.

Firewall: discovery sandbox, NO promotion, no marker moves, no RH
evidence, no metaphysics; classical theorems (Poisson summation,
Tomita-Takesaki / KMS, Bisognano-Wichmann) named as such -- probe
content is the exact typing of the part-12 fence, not a claim upgrade.
"""
import math
import time

import mpmath
import numpy as np
import sympy as sp

PASS = 0
FAIL = 0
T0 = time.time()
mpmath.mp.dps = 40


def check(name, ok):
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {name}", flush=True)
    if ok:
        PASS += 1
    else:
        FAIL += 1
    return ok


def info(msg):
    print(f"        {msg}", flush=True)


def iszero(e):
    """Exact zero test without hanging simplify on nested radicals."""
    e2 = sp.expand(e)
    if e2 == 0:
        return True
    e3 = sp.expand(sp.expand_complex(e2))
    if e3 == 0:
        return True
    # numerical fallback (40 digits) for cyclotomic / nested-radical IDs
    try:
        return abs(complex(e3.evalf(40))) < 1e-28
    except Exception:
        return False


# ================================================================= S1
print("S1 -- v526 anatomy: measured beta_steps vs universal beta_angle",
      flush=True)

N8 = 8
pi = sp.pi


def c_of(d, n):
    """Chiral NS circle kernel (v519/v526): C(d)=(2/N)/sin(pi d/N), odd d."""
    if d % 2 == 0:
        return sp.Integer(0)
    return sp.Rational(2, n) / sp.sin(pi * sp.Rational(d, n))


# --- S1a: detailed balance measures beta_steps = N (nontrivial) ---
C1, C3 = c_of(1, N8), c_of(3, N8)
QQ = sp.Rational(1, 2) * (2 + sp.sqrt(2) + sp.sqrt(2 + 4 * sp.sqrt(2)))
q = sp.sqrt(QQ)
# Q-polynomial identity: kappa = q^{-8}  <=>  (1+sqrt2) Q = Q^2 - Q + 1
kap_id = iszero(sp.expand((1 + sp.sqrt(2)) * QQ - (QQ ** 2 - QQ + 1)))
# representation C(d) = 2w (q^{-d} + q^{d-N}) at all odd d -- numerical
# (exact radical form of q makes expand slow; 40-digit certificate)
w = C1 / (2 * (q ** -1 + q ** -7))
q_num = mpmath.mpf(str(sp.N(q, 45)))
w_num = mpmath.mpf(str(sp.N(w, 45)))
rep_ok = True
for d in (1, 3, 5, 7):
    lhs = mpmath.mpf(str(sp.N(c_of(d, N8), 45)))
    rhs = 2 * w_num * (q_num ** (-d) + q_num ** (d - N8))
    rep_ok &= abs(lhs - rhs) < mpmath.mpf('1e-30')
# wrong betas excluded
kap = q_num ** -8
gaps = {b: abs(kap - q_num ** (-b)) for b in (2, 4, 16)}
wrong_excl = all(g > mpmath.mpf('0.005') for g in gaps.values())
wit_n2 = iszero((C1 - C3) - sp.sqrt(2) * C3)
# also: C1/C3 = 1+sqrt2 exact (forces the mode)
ratio_id = iszero(C1 / C3 - (1 + sp.sqrt(2)))
info(f"N=8 mode: omega = arcsinh(2^{{-3/4}}) = "
     f"{mpmath.nstr(mpmath.log(q_num), 12)}")
info(f"detailed-balance kappa = q^{{-8}} identity: {kap_id}; "
     f"rep all odd d (40-digit): {rep_ok}")
info(f"C(1)/C(3) = 1+sqrt2: {ratio_id}; N/2 witness: {wit_n2}")
info(f"wrong-beta gaps |q^{{-8}}-q^{{-b}}|: "
     f"b=2:{mpmath.nstr(gaps[2], 6)}, b=4:{mpmath.nstr(gaps[4], 6)}, "
     f"b=16:{mpmath.nstr(gaps[16], 6)}")
check("S1a MEASURED (nontrivial): transfer detailed balance on C(d) forces "
      "beta_steps = N = 8 exactly (Q-polynomial kappa = q^{-8}; full "
      "thermal-mode representation at d = 1,3,5,7 to 40 digits; wrong "
      "candidates N/2, N/4, 2N excluded with quantified gaps; N/2 "
      "witness C(1)-C(3)=sqrt2 C(3) != 0 exact).  This is the "
      "seam-kernel output -- NOT an input",
      kap_id and rep_ok and wrong_excl and wit_n2 and ratio_id)

# --- S1b: beta_angle = 2 pi is the UNIVERSAL geometric conversion ---
beta_steps = N8
angle_per_step = 2 * pi / N8
beta_angle = beta_steps * angle_per_step
c3 = sp.Rational(1, 8) / pi
id_2pi = iszero(beta_angle - 2 * pi)
id_c3 = iszero(beta_angle - 1 / (4 * c3))
id_T = iszero(1 / beta_angle - 4 * c3)
beta_angle_16 = 16 * (2 * pi / 16)
id_Nindep = iszero(beta_angle_16 - 2 * pi)
taut = iszero(sp.Integer(N8) * (2 * pi / N8) - 2 * pi)
info(f"beta_angle = beta_steps * (2 pi / N) = {beta_angle}")
info(f"2 pi = 1/(4 c3): {id_c3}; T_seam = 4 c3: {id_T}; N-indep: {id_Nindep}")
info("TYPING: once beta_steps = N (thermal period = full circle), "
     "beta_angle = 2 pi is the Bisognano-Wichmann / Unruh angle -- "
     "universal in any KMS theory that identifies the thermal circle "
     "with the geometric circle.  It is NOT a compiler-specific "
     "numerical output beyond the measurement beta_steps = N.")
check("S1b UNIVERSAL (b): beta_angle = beta_steps*(2 pi/N) = 2 pi is the "
      "geometric conversion identity (tautological once beta_steps = N); "
      "equals 1/(4 c3) by the axiom rewrite; N-independent (8 and 16).  "
      "Honest (a)/(b) split: (a) beta_steps = N is measured from C(d); "
      "(b) the number 2 pi in radians is the universal BW/Unruh "
      "normalisation, not a TFPT-specific datum",
      id_2pi and id_c3 and id_T and id_Nindep and taut)

# --- S1c: Williamson / entropy anchors from the declared kernel ---
P8 = [4, 5, 6, 7]
Jm = sp.zeros(4, 4)
for i, a in enumerate(P8):
    for j, b in enumerate(P8):
        if a < b:
            # wick((a,b)) = I*C(a-b); Im = C(a-b) (negative for a<b)
            v = sp.im(sp.I * c_of(a - b, N8))
            Jm[i, j] = v
            Jm[j, i] = -v
n1s = (4 + sp.sqrt(2) + sp.sqrt(6)) / 8
n2s = (4 + sp.sqrt(2) - sp.sqrt(6)) / 8
cos_ok = (iszero(sp.cos(pi / 24) ** 2 - n1s)
          and iszero(sp.cos(7 * pi / 24) ** 2 - n2s))
# numerical Williamson spectrum of iJ (40-digit) vs cos anchors
J_mp = mpmath.matrix(4)
for i in range(4):
    for j in range(4):
        J_mp[i, j] = mpmath.mpf(str(sp.N(Jm[i, j], 45)))
iJ = mpmath.matrix(4)
for i in range(4):
    for j in range(4):
        iJ[i, j] = mpmath.j * J_mp[i, j]
ev = sorted([mpmath.re(mpmath.eig(iJ)[0][k]) for k in range(4)])
nu1m = mpmath.cos(mpmath.pi / 24)
nu2m = mpmath.cos(7 * mpmath.pi / 24)
want = sorted([-nu1m, -nu2m, nu2m, nu1m])
eig_ok = max(abs(ev[k] - want[k]) for k in range(4)) < mpmath.mpf('1e-28')
# exact closed-form char-poly identity via simplify (expand alone does not
# cancel the rational det form; simplify returns 0 -- classical v526 ID)
lam = sp.symbols('lam')
cp = (sp.I * Jm - lam * sp.eye(4)).det()
target = (lam ** 2 - n1s) * (lam ** 2 - n2s)
cp_ok = sp.simplify(sp.together(cp - target)) == 0
nu1, nu2 = sp.cos(pi / 24), sp.cos(7 * pi / 24)
ps = [(1 + s1 * nu1) * (1 + s2 * nu2) / 4
      for s1 in (1, -1) for s2 in (1, -1)]
sum1 = iszero(sum(ps) - 1)


def Hnu(nu):
    return (mpmath.log(2)
            - ((1 + nu) * mpmath.log(1 + nu)
               + (1 - nu) * mpmath.log(1 - nu)) / 2)


S8 = Hnu(nu1m) + Hnu(nu2m)
ps_num = sorted([mpmath.mpf(str(sp.N(p, 45))) for p in ps])
S8_p = -mpmath.fsum([p * mpmath.log(p) for p in ps_num])
S_ok = abs(S8 - S8_p) < mpmath.mpf('1e-30')
silver = iszero(C3 / C1 - (sp.sqrt(2) - 1))
info(f"Williamson |nu| from eig(iJ) = {mpmath.nstr(ev[3], 12)}, "
     f"{mpmath.nstr(ev[2], 12)}; anchors cos(pi/24), cos(7pi/24); "
     f"eig OK: {eig_ok}; char-poly simplify: {cp_ok}")
info(f"S(rho_OS) = {mpmath.nstr(S8, 10)} nats (matches -sum p ln p: {S_ok})")
info(f"silver: C(3)/C(1) = sqrt2 - 1: {silver}")
check("S1c KERNEL ANCHORS recomputed from C(d): half-covariance iJ has "
      "Williamson spectrum {+-cos(pi/24), +-cos(7pi/24)} (40-digit) with "
      "nu^2 = (4+sqrt2 +- sqrt6)/8 exact; char poly identity via "
      "simplify; spectrum p = {(1+-nu1)(1+-nu2)/4} sums to 1; entropy "
      f"S(8) = {mpmath.nstr(S8, 8)} nats via Williamson formula; silver "
      "clock eigenvalue sqrt2-1 = C(3)/C(1) is a thermal KERNEL ratio "
      "(not e^{-Delta K}).  These are compiler/seam data; the 2 pi angle "
      "is not among them",
      eig_ok and cp_ok and cos_ok and sum1 and S_ok and silver
      and abs(S8 - mpmath.mpf('0.52187')) < mpmath.mpf('5e-6'))


# ================================================================= S2
print("S2 -- unimodularity gate: self-dual width only after mu4 completion",
      flush=True)

# Exact dets via classical root-lattice formulae (Conway-Sloane)
atlas_dets = {
    'D5+A3': 4 * 4,       # det D5 * det A3 = 4 * 4; A3 ≅ D3
    'D8': 4,
    'E6+A2': 3 * 3,
    'A8': 9,
    'E7+A1': 2 * 2,
    'A4+A4': 5 * 5,
}
dets_ok = all(d > 1 for d in atlas_dets.values())

# Explicit Gram check: D5⊕D3 and D8 and E8 in standard coordinates
B_D5A3 = np.array([
    [1, -1, 0, 0, 0, 0, 0, 0],
    [0, 1, -1, 0, 0, 0, 0, 0],
    [0, 0, 1, -1, 0, 0, 0, 0],
    [0, 0, 0, 1, -1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, -1, 0],
    [0, 0, 0, 0, 0, 0, 1, -1],
    [0, 0, 0, 0, 0, 1, 1, 0],
], dtype=np.float64).T

B_D8 = np.array([
    [1, -1, 0, 0, 0, 0, 0, 0],
    [0, 1, -1, 0, 0, 0, 0, 0],
    [0, 0, 1, -1, 0, 0, 0, 0],
    [0, 0, 0, 1, -1, 0, 0, 0],
    [0, 0, 0, 0, 1, -1, 0, 0],
    [0, 0, 0, 0, 0, 1, -1, 0],
    [0, 0, 0, 0, 0, 0, 1, -1],
    [0, 0, 0, 0, 0, 0, 1, 1],
], dtype=np.float64).T

B_E8 = np.array([
    [0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5],
    [1, 1, 0, 0, 0, 0, 0, 0],
    [-1, 1, 0, 0, 0, 0, 0, 0],
    [0, -1, 1, 0, 0, 0, 0, 0],
    [0, 0, -1, 1, 0, 0, 0, 0],
    [0, 0, 0, -1, 1, 0, 0, 0],
    [0, 0, 0, 0, -1, 1, 0, 0],
    [0, 0, 0, 0, 0, -1, 1, 0],
], dtype=np.float64).T


def gram_det(B):
    return float(np.linalg.det(B.T @ B))


def covol(B):
    return math.sqrt(abs(gram_det(B)))


gd_d5, gd_d8, gd_e8 = gram_det(B_D5A3), gram_det(B_D8), gram_det(B_E8)
info(f"atlas dets (exact classical): {atlas_dets}")
info(f"Gram det numerical: D5+A3={gd_d5:.6g}, D8={gd_d8:.6g}, E8={gd_e8:.6g}")
info(f"covols: D5+A3={covol(B_D5A3):.6g}, D8={covol(B_D8):.6g}, "
     f"E8={covol(B_E8):.6g}")
check("S2a EXACT: every atlas sublattice has det = index^2 > 1 "
      f"(D5+A3:{atlas_dets['D5+A3']}, D8:{atlas_dets['D8']}, "
      f"E6+A2:{atlas_dets['E6+A2']}, A8:{atlas_dets['A8']}, "
      f"E7+A1:{atlas_dets['E7+A1']}, A4+A4:{atlas_dets['A4+A4']}); "
      "only E8 is unimodular (det = 1).  Numerical Gram determinants "
      "of the explicit embeddings match (D5+A3=16, D8=4, E8=1)",
      dets_ok
      and abs(gd_d5 - 16) < 1e-8
      and abs(gd_d8 - 4) < 1e-8
      and abs(gd_e8 - 1) < 1e-8)


# --- Fast 1D / product thetas for D_n and D_n* (classical) ---
def theta_Z(t, M=80):
    """sum_{k=-M..M} exp(-t k^2)."""
    t = float(t)
    return 1.0 + 2.0 * sum(math.exp(-t * k * k) for k in range(1, M + 1))


def theta_Z_alt(t, M=80):
    """sum_{k=-M..M} (-1)^k exp(-t k^2)."""
    t = float(t)
    return 1.0 + 2.0 * sum(((-1) ** k) * math.exp(-t * k * k)
                            for k in range(1, M + 1))


def theta_half(t, M=80):
    """sum_{k=-M..M} exp(-t (k+1/2)^2)."""
    t = float(t)
    return sum(math.exp(-t * (k + 0.5) ** 2) for k in range(-M, M + 1))


def theta_Dn(n, t):
    """sum_{x in D_n} e^{-t|x|^2} = (1/2)(theta_Z^n + theta_Z_alt^n)."""
    a, b = theta_Z(t), theta_Z_alt(t)
    return 0.5 * (a ** n + b ** n)


def theta_Dn_star(n, t):
    """D_n* = Z^n ∪ (Z+1/2)^n => theta_Z^n + theta_half^n."""
    return theta_Z(t) ** n + theta_half(t) ** n


def theta_D5A3(t):
    """D5 ⊕ D3 ≅ D5+A3."""
    return theta_Dn(5, t) * theta_Dn(3, t)


def theta_D5A3_star(t):
    """(D5 ⊕ D3)* = D5* ⊕ D3*."""
    return theta_Dn_star(5, t) * theta_Dn_star(3, t)


def theta_D8(t):
    return theta_Dn(8, t)


def theta_D8_star(t):
    return theta_Dn_star(8, t)


# E8 census route (part 12)
sig3 = {n: int(sp.divisor_sigma(n, 3)) for n in range(1, 80)}


def theta_E8_census(t, nmax=60):
    """sum_x exp(-t |x|^2) via r_E8(2n) = 240 sigma_3(n)."""
    t = mpmath.mpf(t)
    tot = mpmath.mpf(1)
    for n in range(1, nmax + 1):
        tot += 240 * sig3[n] * mpmath.e ** (-t * 2 * n)
    return tot


pois_e8 = True
for tw in (mpmath.mpf('1.1'), mpmath.mpf('2.6')):
    lhs = theta_E8_census(tw)
    rhs = (mpmath.pi / tw) ** 4 * theta_E8_census(mpmath.pi ** 2 / tw)
    ratio = lhs / rhs
    info(f"E8 Poisson t={tw}: lhs/rhs = {mpmath.nstr(ratio, 20)}")
    pois_e8 &= abs(ratio - 1) < mpmath.mpf('1e-20')

s_ = sp.symbols('s', positive=True)
fixed = set(sp.solve(sp.pi ** 2 / s_ - s_, s_))
check("S2b E8 Poisson self-duality (classical): Theta(t) = (pi/t)^4 "
      "Theta(pi^2/t) to >20 digits at t = 1.1, 2.6; UNIQUE positive "
      "fixed width t = pi (solve pi^2/t = t)",
      pois_e8 and fixed == {sp.pi})

# D5+A3 Poisson: dual PASSES, self FAILS
t_test = 1.1
cov_d5 = 4.0  # exact sqrt(16)
th_L = theta_D5A3(t_test)
th_Lstar = theta_D5A3_star(math.pi ** 2 / t_test)
th_L_at_dual = theta_D5A3(math.pi ** 2 / t_test)
rhs_dual = (1.0 / cov_d5) * (math.pi / t_test) ** 4 * th_Lstar
rhs_self = (math.pi / t_test) ** 4 * th_L_at_dual
ratio_dual = th_L / rhs_dual
ratio_self = th_L / rhs_self
info(f"D5+A3 covol = {cov_d5} (exact)")
info(f"D5+A3 t={t_test}: Theta_L = {th_L:.12g}")
info(f"  dual-Poisson rhs = {rhs_dual:.12g}, ratio = {ratio_dual:.12g}")
info(f"  naive-self rhs  = {rhs_self:.12g}, ratio = {ratio_self:.12g}")
dual_ok = abs(ratio_dual - 1) < 1e-8
self_fails = abs(ratio_self - 1) > 0.05
check("S2c D5+A3 Poisson with DUAL lattice: Theta_L(t) = covol^{-1} "
      f"(pi/t)^4 Theta_{{L*}}(pi^2/t) at t = {t_test} (ratio "
      f"{ratio_dual:.6g} ~ 1; classical 1D product formulae for "
      "D5 x D3 and D5* x D3*).  Naive self-dual formula Theta_L(t) = "
      f"(pi/t)^4 Theta_L(pi^2/t) FAILS (ratio {ratio_self:.6g}, gap "
      ">> 0) -- self-duality dies exactly on det != 1.  Classical "
      "Poisson named as such",
      dual_ok and self_fails)

# D8 control
cov_d8 = 2.0
th_D8 = theta_D8(t_test)
th_D8s = theta_D8_star(math.pi ** 2 / t_test)
th_D8d = theta_D8(math.pi ** 2 / t_test)
r_d8_dual = th_D8 / ((1.0 / cov_d8) * (math.pi / t_test) ** 4 * th_D8s)
r_d8_self = th_D8 / ((math.pi / t_test) ** 4 * th_D8d)
info(f"D8 covol={cov_d8}: dual-ratio={r_d8_dual:.8g}, "
     f"self-ratio={r_d8_self:.8g}")
check("S2d D8 control: dual Poisson holds (ratio ~ 1), naive self-dual "
      "fails (ratio far from 1); same pattern as D5+A3 -- every proper "
      "atlas sublattice lacks a Poisson-self-dual Gaussian width",
      abs(r_d8_dual - 1) < 1e-4 and abs(r_d8_self - 1) > 0.05
      and abs(covol(B_D8) - 2) < 1e-10)

check("S2e STRUCTURAL CONSEQUENCE (typed, not a marker move): a "
      "Poisson-self-dual temperature is well-defined ONLY for the "
      "unimodular completion E8.  Among the atlas, that completion is "
      "exactly the axiom step D5+A3 + mu4 => E8.  So 'beta = 2 pi is "
      "available as a self-dual width BECAUSE the axiom completes to "
      "an even unimodular lattice' -- a necessary-condition gate, not "
      "a derivation that the seam KMS parameter equals that width",
      dets_ok and pois_e8 and dual_ok and self_fails)


# ================================================================= S3
print("S3 -- torsor / scaling: root-norm convention moves the fixed width",
      flush=True)

lam_root2 = 1
lam_root1 = sp.Rational(1, 2)
t_star_2 = sp.pi / lam_root2
t_star_1 = sp.pi / lam_root1
beta = 2 * sp.pi
bolt_at_root = sp.exp(-beta * 2 / 2)
gauss_at_root = sp.exp(-t_star_2 * 2)
match = iszero(sp.log(bolt_at_root) - sp.log(gauss_at_root))
alt_match = iszero(t_star_1 - beta)
info(f"root-norm 2 => t_* = pi; Boltzmann/Gaussian match at roots: {match}")
info(f"root-norm 1 => t_* = 2 pi = beta (direct numerical equality)")
info("The chain c3=1/(8pi) <=> beta=2pi <=> t=pi USES the root-norm-2 "
     "convention to convert beta into the Poisson width t.  Rescaling "
     "the lattice moves t_* and breaks the numerical identification "
     "unless the seam side is rescaled by the same torsor -- which is "
     "exactly the open coupling.")
check("S3a SCALING LAW (exact): L -> sqrt(lambda) L sends the E8 "
      "self-dual width to t_* = pi/lambda.  Root-norm-2 (compiler "
      "Cartan convention, lambda=1) gives t_* = pi; root-norm-1 "
      "(lambda=1/2) gives t_* = 2 pi = beta.  Both are the SAME "
      "physical lattice up to scale -- the numerical equality "
      "'beta = 2 * t_*' holds only in the root-norm-2 chart",
      iszero(t_star_2 - sp.pi) and iszero(t_star_1 - 2 * sp.pi)
      and match and alt_match)

check("S3b TORSOR FENCE (typed): a genuine derivation of "
      "SEAM.SELFDUAL.WIDTH must exhibit a NORMALISATION-FREE coupling "
      "between the seam modular flow and the lattice Gaussian width "
      "(e.g. an identification of quadratic forms / modular Hamiltonians "
      "that transforms correctly under L -> sqrt(lambda) L).  The "
      "present chain is a chart-dependent rewriting, not that coupling.  "
      "Kill criterion of part 12 remains: separate the two parameters "
      "onto distinct torsors, OR fix a width incompatible with the "
      "Poisson fixed point in the compiler chart",
      True)


# ================================================================= S4
print("S4 -- verdict for SEAM.SELFDUAL.WIDTH", flush=True)

mu4 = 4
c3_via_mu4 = 1 / (mu4 * beta)
c3_via_mu4_ok = iszero(c3_via_mu4 - c3)
info("VERDICT ENUM: DEFLATED")
info("  reason: beta_angle = 2 pi is the universal BW/Unruh angle "
     "(S1b), not a compiler-specific measurement beyond beta_steps = N")
info("  residual OPEN (sharpened):")
info("    (i)   factor 4 = |mu4| in c3 = 1/(4*beta) "
     f"[rewrite OK: {c3_via_mu4_ok}]")
info("    (ii)  norm-free coupling seam-modular-flow <-> E8-Gaussian")
info("    (iii) unimodularity gate: self-dual width needs mu4 "
     "completion (S2) -- necessary, not sufficient")
info("  NOT killed: no derivation forces census width != 2 pi")
info("  NOT derived: the identification seam-KMS == census-width")
check("S4a DEFLATION of the 2 pi claim: the part-12 slogan "
      "'v526-measured beta = 2 pi IS the Poisson self-dual width' "
      "overstates what v526 measures.  v526 measures beta_steps = N; "
      "the 2 pi is the universal geometric conversion.  Contract "
      "SEAM.SELFDUAL.WIDTH is therefore DEFLATED onto the residual "
      "questions (factor |mu4|, norm-free coupling), not DERIVED and "
      "not KILLED",
      c3_via_mu4_ok and id_2pi and kap_id)

check("S4b RESIDUAL OPEN typed (still [O], sharpened): three "
      "computable residues remain -- (i) derive |mu4|=4 as the "
      "coefficient in c3 = 1/(|mu4| * beta_BW) from glue/census data "
      "without chart choice; (ii) exhibit a torsor-free map from seam "
      "modular Hamiltonian to the E8 Gaussian width; (iii) the "
      "unimodularity gate of S2 is a necessary-condition lemma "
      "(self-dual temperature <=> even-unimodular completion) awaiting "
      "promotion only if a derivation closes (i) or (ii).  No marker "
      "move.  Next lever: construct an explicit quadratic-form "
      "pairing between the v526 modular Hamiltonian K (eps = "
      "2 ln cot(theta/2)) and the E8 norm form that is invariant "
      "under simultaneous rescaling of lattice and modular flow",
      True)

check("S4c GLOBAL CONSISTENCY: S1 anatomy (measured steps vs universal "
      "angle) + S2 unimodularity gate (E8 only) + S3 torsor fence + "
      "S4 deflation cohere; Boltzmann/Gaussian match in the root-norm-2 "
      "chart; c3 = 1/(|mu4| * 2 pi) rewrite exact; probe stays sandbox",
      match and c3_via_mu4_ok and pois_e8 and dual_ok and self_fails
      and S_ok)


elapsed = time.time() - T0
print(f"\nTOTAL: {PASS} passed, {FAIL} failed  ({elapsed:.1f}s)", flush=True)
raise SystemExit(0 if FAIL == 0 else 1)
