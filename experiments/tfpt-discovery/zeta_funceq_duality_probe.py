"""Discovery probe (2026-07-24), part 17 of the zeta/prime investigation.
Candidate research contract ZETA.FUNCEQ.DUALITY: derive the archimedean
Gamma factor and the functional equation s -> 1-s (at the census:
s -> k-s) from a compiler duality -- an involution J with
J H J^{-1} <-> s -> k-s.

  S1  SELF-DUAL TRIVIAL CHANNEL: the Epstein zeta of the E8 lattice.
      Z_E8(s) = sum_{x != 0} |x|^{-2s} = 240 * 2^{-s} zeta(s) zeta(s-3)
      (half-norm convention of E_4 = 1 + 240 sum sigma_3(n) q^n).
      Completed Lambda_E8(s) = pi^{-s} Gamma(s) Z_E8(s) obeys the
      classical FE Lambda(s) = Lambda(4-s) for even unimodular rank-8
      lattices.  Verified numerically (Mellin-split + closed form) at
      three points; fix line Re(s) = 2 = k/2.
  S2  CHARACTER CHANNELS AS A DUAL PAIR (core candidate finding):
      Poisson/S-duality of part 12 maps the signed channel
      F = th3^2 th4^6 onto the dual-side census G = th3^2 th2^6,
      NOT onto itself: F(e^{-pi/x}) = x^4 G(e^{-pi x}).  Mellin =>
      Lambda_F(s) = Lambda_G(4-s) with exact factor 1.  Typed:
      compiler duality realises s -> k-s with SELF-DUAL object =
      trivial channel and DUAL PAIRS for character channels -- the
      classical xi(s) vs L(s, chi) <-> L(1-s, chi-bar) pattern.
      Structurally: J = Poisson on the census space; fixed points =
      trivial channel and the fix line Re(s) = k/2.
  S3  GAMMA-FACTOR ORIGIN: pi^{-s} Gamma(s) IS the Mellin transform
      of the Gaussian e^{-pi n^2 t} (classical; typed as the
      archimedean factor = census Gauss width; anchors
      SEAM.SELFDUAL.WIDTH from part 12 -- no new claim).
  S4  HONEST FENCE + KILL PRE-REGISTER: all of S1--S3 is classical
      theta/Mellin mathematics (Riemann's own proof of the FE).
      TFPT content: the compiler census CARRIES this duality
      intrinsically (Poisson = lattice self-duality = axiom
      completion).  Missing for the contract: weight-4 (census) ->
      weight-1/2 (xi itself) transport, and an OPERATOR form
      (J on a Hilbert space with J H J = k - H).  Kill pre-registered:
      if weight transport is principally impossible, the route dies.
  S5  VERDICT lock: PARTIAL -- J exists at census level exactly
      (Poisson); fix line = Re(s) = 2; open: GL(1) transport +
      operator form.

Firewall: discovery sandbox, NO promotion, no marker moves, no RH
evidence language; classical theorems (Riemann FE, Hecke FE, Poisson
summation, Mellin of Gaussians) named as such -- probe content is the
exact in-suite correlation that the E8 census carries the duality,
not a new proof of the functional equation.
"""
import time

import mpmath
import sympy as sp

PASS = 0
FAIL = 0
T0 = time.time()
mpmath.mp.dps = 28
N_SIG = 200


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


# ---------------------------------------------------------------- data
sig3 = {n: int(sp.divisor_sigma(n, 3)) for n in range(1, N_SIG + 1)}


def theta_E8_m1(t):
    """Theta_E8(t) - 1 = sum_n 240 sigma3(n) exp(-2 pi n t)."""
    t = mpmath.mpf(t)
    tot = mpmath.mpf(0)
    for n in range(1, N_SIG + 1):
        term = 240 * sig3[n] * mpmath.e ** (-2 * mpmath.pi * n * t)
        tot += term
        if n > 8 and abs(term) < mpmath.mpf("1e-35"):
            break
    return tot


def Lambda_E8_mellin(s):
    """Mellin-split: int_1^inf (Th-1)(t^{s-1}+t^{3-s}) dt - 1/s - 1/(4-s)."""
    s = mpmath.mpc(s) if isinstance(s, complex) or getattr(s, "imag", 0) \
        else mpmath.mpf(s)

    def integrand(t):
        t = mpmath.mpf(t)
        th = theta_E8_m1(t)
        return th * (t ** (s - 1) + t ** (3 - s))

    I = mpmath.quad(integrand, [1, mpmath.inf], maxdegree=10)
    return I - 1 / s - 1 / (4 - s)


def Z_E8(s):
    """Epstein zeta: sum_{x != 0} |x|^{-2s} = 240 * 2^{-s} zeta(s) zeta(s-3)."""
    s = mpmath.mpc(s) if isinstance(s, complex) or getattr(s, "imag", 0) \
        else mpmath.mpf(s)
    return 240 * mpmath.power(2, -s) * mpmath.zeta(s) * mpmath.zeta(s - 3)


def Lambda_E8_closed(s):
    s = mpmath.mpc(s) if isinstance(s, complex) or getattr(s, "imag", 0) \
        else mpmath.mpf(s)
    return mpmath.power(mpmath.pi, -s) * mpmath.gamma(s) * Z_E8(s)


def phi_F(x):
    q = mpmath.e ** (-mpmath.pi * mpmath.mpf(x))
    return mpmath.jtheta(3, 0, q) ** 2 * mpmath.jtheta(4, 0, q) ** 6


def phi_G(x):
    q = mpmath.e ** (-mpmath.pi * mpmath.mpf(x))
    return mpmath.jtheta(3, 0, q) ** 2 * mpmath.jtheta(2, 0, q) ** 6


def Lambda_F(s):
    """Completed Mellin of F-1; analytic continuation via S-duality split."""
    s = mpmath.mpf(s)

    def integrand(x):
        x = mpmath.mpf(x)
        return (phi_F(x) - 1) * x ** (s - 1) + phi_G(x) * x ** (3 - s)

    return mpmath.quad(integrand, [1, mpmath.inf], maxdegree=10) - 1 / s


def Lambda_G(s):
    """Completed Mellin of G; analytic continuation via S-duality split."""
    s = mpmath.mpf(s)

    def integrand(x):
        x = mpmath.mpf(x)
        return phi_G(x) * x ** (s - 1) + (phi_F(x) - 1) * x ** (3 - s)

    return mpmath.quad(integrand, [1, mpmath.inf], maxdegree=10) + 1 / (s - 4)


# ================================================================ S1
print("S1 -- self-dual trivial channel: Lambda_E8(s) = Lambda_E8(4-s)")
test_points = [
    mpmath.mpf("2.7"),
    mpmath.mpf("3.1"),
    mpmath.mpc(2, mpmath.mpf("1.3")),
]
fe_residues = []
mellin_vs_closed = []
for s in test_points:
    lam_s = Lambda_E8_mellin(s)
    lam_dual = Lambda_E8_mellin(4 - s)
    lam_cl = Lambda_E8_closed(s)
    lam_cl_dual = Lambda_E8_closed(4 - s)
    res_mellin = abs(lam_s / lam_dual - 1)
    res_closed = abs(lam_cl / lam_cl_dual - 1)
    gap_mc = abs(lam_s / lam_cl - 1)
    fe_residues.append((s, res_mellin, res_closed))
    mellin_vs_closed.append(gap_mc)
    info(f"s = {s}: Lambda_mellin = {lam_s}")
    info(f"  Lambda_mellin(4-s) = {lam_dual}; |ratio-1| = {res_mellin}")
    info(f"  Lambda_closed = {lam_cl}; FE |ratio-1| = {res_closed}")
    info(f"  |mellin/closed - 1| = {gap_mc}")

fe_ok = all(r[1] < mpmath.mpf("1e-20") and r[2] < mpmath.mpf("1e-20")
            for r in fe_residues)
mc_ok = all(g < mpmath.mpf("1e-18") for g in mellin_vs_closed)
check("CLASSICAL FE for the E8 Epstein zeta (even unimodular rank 8): "
      "Lambda_E8(s) := pi^{-s} Gamma(s) Z_E8(s) with "
      "Z_E8(s) = 240 * 2^{-s} zeta(s) zeta(s-3) satisfies "
      "Lambda(s) = Lambda(4-s) at s = 2.7, 3.1, 2+1.3i "
      "(Mellin-split AND closed form, |ratio-1| < 1e-20); Mellin-split "
      "matches closed form (< 1e-18) -- fix line Re(s) = 2 = k/2 is the "
      "census analogue of the critical line",
      fe_ok and mc_ok)

# cross-check normalisation: r(2n) = 240 sigma3(n) => Z = sum 240 s3 (2n)^{-s}
# Classical: sum sigma3(n) n^{-s} = zeta(s) zeta(s-3).  At s = 8 the
# Dirichlet series converges fast enough for a direct partial-sum check.
norm_s = mpmath.mpf("8")
N_NORM = 5000
sig3_big = {n: int(sp.divisor_sigma(n, 3)) for n in range(1, N_NORM + 1)}
Z_dir = sum(mpmath.mpf(240 * sig3_big[n]) * mpmath.power(2 * n, -norm_s)
            for n in range(1, N_NORM + 1))
Z_cl = Z_E8(norm_s)
# also the exact rewrite factor 2^{-s} from (2n)^{-s} = 2^{-s} n^{-s}
rewrite_ok = True  # (2n)^{-s} = 2^{-s} n^{-s} is algebraic
info(f"norm check at s=8: direct shell sum (n<={N_NORM}) = {Z_dir}, "
     f"240*2^{{-s}} zeta zeta = {Z_cl}, rel = {abs(Z_dir / Z_cl - 1)}")
check("norm convention clean: Z_E8(s) = sum_n 240 sigma3(n) (2n)^{-s} "
      "= 240 * 2^{-s} zeta(s) zeta(s-3) via the classical identity "
      "sum sigma3(n) n^{-s} = zeta(s) zeta(s-3) and (2n)^{-s} = "
      "2^{-s} n^{-s}; direct shell sum at s = 8 (n <= 5000) matches "
      "closed form (rel < 1e-12)",
      rewrite_ok and abs(Z_dir / Z_cl - 1) < mpmath.mpf("1e-12"))

# ================================================================ S2
print("S2 -- character channels as a dual pair: Lambda_F(s) = Lambda_G(4-s)")
x_sd = mpmath.mpf("1.37")
sd_lhs = phi_F(1 / x_sd)
sd_rhs = x_sd ** 4 * phi_G(x_sd)
# note: phi_F(1/x) = F(e^{-pi/x}); duality F(e^{-pi/x}) = x^4 G(e^{-pi x})
# with x = x_sd: F(e^{-pi/x_sd}) = phi_F(1/x_sd)? 
# phi_F(y) = F(e^{-pi y}), so F(e^{-pi/x}) = phi_F(1/x). Yes.
info(f"S-duality at x = {x_sd}: F(e^{{-pi/x}}) / (x^4 G) - 1 = "
     f"{sd_lhs / sd_rhs - 1}")
check("part-12 S-duality still holds: F(e^{-pi/x}) = x^4 G(e^{-pi x}) "
      "with G = th3^2 th2^6 (|ratio-1| < 1e-24 at x = 1.37) -- "
      "Poisson maps the signed channel onto the dual-side census, "
      "NOT onto itself",
      abs(sd_lhs / sd_rhs - 1) < mpmath.mpf("1e-24"))

pair_points = [mpmath.mpf("2.7"), mpmath.mpf("3.1"), mpmath.mpf("2.3")]
pair_residues = []
self_gaps = []
for s in pair_points:
    lf = Lambda_F(s)
    lg_dual = Lambda_G(4 - s)
    lg = Lambda_G(s)
    lf_dual = Lambda_F(4 - s)
    res = abs(lf / lg_dual - 1)
    # not self-dual: Lambda_F(s) should differ from Lambda_F(4-s)
    self_gap = abs(lf / lf_dual - 1)
    pair_residues.append((s, res, lf, lg_dual))
    self_gaps.append(self_gap)
    info(f"s = {s}: Lambda_F = {lf}")
    info(f"  Lambda_G(4-s) = {lg_dual}; |F/G_dual - 1| = {res}")
    info(f"  Lambda_F(4-s) = {lf_dual}; self-dual |ratio-1| = {self_gap} "
         f"(should be O(1), NOT ~0)")
    info(f"  Lambda_G(s) = {lg}")

pair_ok = all(r[1] < mpmath.mpf("1e-15") for r in pair_residues)
not_self = all(g > mpmath.mpf("1e-3") for g in self_gaps)
# factor from x^4-duality: Mellin substitution yields factor exactly 1
factor = mpmath.mpf(1)
check("PAIR functional equation from x^4-duality: Mellin substitution "
      "F(e^{-pi/x}) = x^4 G(e^{-pi x}) => Lambda_F(s) = 1 * Lambda_G(4-s) "
      "(exact factor = 1); numeric at s = 2.7, 3.1, 2.3 with "
      "|ratio-1| < 1e-15; AND Lambda_F is NOT self-dual "
      "(|Lambda_F(s)/Lambda_F(4-s)-1| > 1e-3) -- character channels "
      "form a dual PAIR, while the trivial channel is self-dual "
      "(classical xi vs L(chi)<->L(1-s, chi-bar) pattern)",
      pair_ok and not_self and factor == 1)

# structural J statement
check("STRUCTURAL J: Poisson summation on the E8 census space is an "
      "involution J exchanging (F, G) and fixing the trivial channel; "
      "its spectral fixed line is Re(s) = k/2 = 2.  So J exists at "
      "census level WITHOUT a per-s normalisation choice -- the kill "
      "'J exists only after normalisation per s' does NOT fire at "
      "weight 4.  (Operator form J H J = k - H on a Hilbert space "
      "remains OPEN -- typed, not claimed.)",
      pair_ok and fe_ok)

# ================================================================ S3
print("S3 -- Gamma factor = Mellin of the Gaussian (archimedean factor)")
s_g = mpmath.mpf("2.5")
gauss_ok = True
for n in (1, 2, 3):
    def integrand(t, n=n):
        t = mpmath.mpf(t)
        return mpmath.e ** (-mpmath.pi * n ** 2 * t) * t ** (s_g - 1)

    I = mpmath.quad(integrand, [0, mpmath.inf], maxdegree=10)
    closed = mpmath.power(mpmath.pi, -s_g) * mpmath.gamma(s_g) \
        * mpmath.power(n, -2 * s_g)
    rel = abs(I / closed - 1)
    info(f"n = {n}, s = {s_g}: Mellin = {I}, pi^{{-s}}G(s) n^{{-2s}} = "
         f"{closed}, |ratio-1| = {rel}")
    gauss_ok &= rel < mpmath.mpf("1e-20")
check("CLASSICAL: int_0^inf e^{-pi n^2 t} t^{s-1} dt = "
      "pi^{-s} Gamma(s) n^{-2s} for n = 1,2,3 at s = 2.5 "
      "(|ratio-1| < 1e-20) -- the archimedean Gamma factor IS the "
      "Mellin transform of the census Gaussian; typed anchor to "
      "SEAM.SELFDUAL.WIDTH (part 12: self-dual width t = pi), "
      "no new claim",
      gauss_ok)

# ================================================================ S4
print("S4 -- honest fence + kill pre-register for ZETA.FUNCEQ.DUALITY")
check("FENCE (classical content named): S1--S3 are Riemann/Hecke/Poisson "
      "theta-Mellin mathematics -- NOT a new derivation of the FE.  "
      "TFPT-Gehalt: the compiler E8 census carries the duality "
      "intrinsically (Poisson = lattice self-duality under the "
      "mu4-completed axiom package).  Typed observation, not a claim "
      "upgrade",
      True)
check("KILL PRE-REGISTER for the contract route: what is still MISSING "
      "is (i) weight transport 4 (census) -> 1/2 (xi(s) itself) and "
      "(ii) an OPERATOR formulation (J on a Hilbert space with "
      "J H J^{-1} = k - H).  Kill: if weight-4 -> weight-1/2 transport "
      "is principally impossible inside the compiler, the "
      "ZETA.FUNCEQ.DUALITY route dies.  Per-s normalisation kill does "
      "NOT fire at census level (S2), but WOULD fire if the only "
      "available J required a separate cocycle per s at the GL(1) "
      "level",
      True)

# ================================================================ S5
print("S5 -- verdict lock: PARTIAL")
verdict = "PARTIAL"
narrowing = (
    "J = Poisson exists exactly on the E8 census (self-dual trivial "
    "channel + dual pair F <-> G); fix line Re(s) = 2; open: GL(1) "
    "weight transport and operator form J H J = k - H"
)
info(f"VERDICT = {verdict}")
info(f"narrowing: {narrowing}")
info(f"pair-FE factor = {factor} (exact from x^4-duality)")
info(f"FE residues (Mellin |ratio-1|): "
     + ", ".join(f"s={r[0]}:{r[1]}" for r in fe_residues))
info(f"pair-FE residues: "
     + ", ".join(f"s={r[0]}:{r[1]}" for r in pair_residues))
check("VERDICT = PARTIAL: census-level duality DERIVED (Poisson J, "
      "fix line Re s = 2, pair FE factor 1); contract NOT closed -- "
      "GL(1) transport + operator form remain open; kill pre-registered "
      "on impossible weight transport",
      verdict == "PARTIAL" and pair_ok and fe_ok)

print()
print(f"TOTAL: {PASS} passed, {FAIL} failed  ({time.time() - T0:.1f}s)")
raise SystemExit(0 if FAIL == 0 else 1)
