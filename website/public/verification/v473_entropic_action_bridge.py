"""v473 -- GRAV.ENTROPIC.ACTION.01: the entropic-action bridge -- Bianconi's
"Gravity from entropy" (Phys. Rev. D 111, 066001 (2025); arXiv:2408.14391) as an
EXTERNAL CANDIDATE for the local volume action behind TFPT's already-closed,
parameter-free Einstein equation (v358/v359).  This module quantifies the bridge;
it does NOT adopt the external action as TFPT structure and closes NO gate.

TFPT's field equation G_ab + Lambda g_ab = (1/c3) T_ab is derived thermodynamically
(entanglement equilibrium, v359) -- honestly typed "equation of state, not a
from-action quantisation" [O].  Bianconi's entropic action S_B = -Tr_F ln(G~ g~^-1)
(the quantum relative entropy between the spacetime metric and the matter-induced
metric, Araki-related via Delta^{1/2}_{G~,g} = G~ g~^-1, her Appendix C) is a local
covariant action whose variation yields modified Einstein equations that reduce to
Einstein + emergent nonnegative Lambda at low coupling -- exactly the missing
variational layer, IF the bridge identities hold.  What is checkable today:

  [E] 1. CARRIER HODGE COUNT.  Bianconi's matter fiber is Omega^{0,1,2}; on the
        five-slot carrier C^5 (NOT on 4d spacetime, where the fiber is 1+4+6=11)
        the count is 1+5+10 = 16 = 2^(g_car-1) = dim S+_{D5}, and the Hodge star
        L^1 ~= L^4 folds it onto the even exterior algebra L^even C^5 -- the
        carrier half-spinor's own Pascal row (v2/v44).  Vector-space identity
        ONLY; Clifford/Dirac/leaf/Calderon compatibility stays open (check 7).
  [E] 2. COEFFICIENT MATCH (the one quantitative pin).  Bianconi's weak-coupling
        Lagrangian is L = 3 beta R - alpha L_matter + ... (her Eq. (45); the 3 =
        the three form blocks 0,1,2).  Matching 3 beta'/l_P^2 (l_P^2 = G) to the
        TFPT EH normalisation 1/(16 pi G) = c3/(2G) fixes her free constant
        EXACTLY: beta'_B = c3/6 = 1/(48 pi).  Structural echo: the 6 = 3 blocks x
        2 (EH 1/2) = p2 = |R+(A3)| -- recorded as consistency, NOT a new proof.
  [E] 3. ENTROPY POTENTIAL = QUADRATIC LAMBDA.  Her emergent constant is
        Lambda_G = (1/2 beta) Tr_F(G - I - ln G) with s(x) = x - 1 - ln x >= 0,
        s(1) = 0, s''(1) = 1 (exact series) => Lambda_G = (1/4 beta) Tr eps^2 +
        O(eps^3): Lambda >= 0 and QUADRATIC around the entropic fixed point.
  [E] 4. THE LAMBDA CHANNEL CLOSES ALGEBRAICALLY.  With the TFPT displacement
        eps_* = e^{-1/alpha} Q the quadratic entropy gives Lambda ~ e^{-2/alpha},
        the SAME suppression as the closed TFPT branch rho_Lambda/Mbar^4 =
        (3/4 pi^2) e^{-2/alpha} (v60); matching prefactors with beta' = c3/6 and
        l_P^2 Mbar^2 = c3 yields the EXACT normalisation target
        Tr_F Q^2 = 32 c3^4 = 1/(128 pi^4) = (2/3) delta_top -- a closed algebraic
        target for the two-form block (binom(5,2) = 10 = the pair sector), [C]
        until an explicit Q is constructed.
  [E] 5. LOG = ALL-SCALE HEAT KERNEL (Frullani).  -ln A = int_0^inf dt/t
        (e^{-tA} - e^{-t}) -- her log action is an all-scale-integrated heat-kernel
        action, the correct genre to compare with TFPT's relative spectral action
        S_rel,chi (KMS cutoff); verified numerically to 1e-12.
  [E] 6. R^2 KILL TEST QUANTIFIED (the honest wall).  The raw log expansion
        -Tr ln(I+X) = -Tr X + (1/2) Tr X^2 - ... carries a curvature-squared
        coefficient of order (beta')^2 = (c3/6)^2; TFPT's Starobinsky sector needs
        Mbar^2/(12 M_scal^2) = 1/(12 c3^7) (M_scal^2 = c3^7 Mbar^2, v36).  The
        EXACT mismatch is 1/(12 c3^7) / (c3/6)^2 = 3 c3^{-9} = 3 (8 pi)^9
        ~ 1.20e13 -- THIRTEEN orders of magnitude.  A direct identification of the
        raw entropic action with the TFPT R^2 sector is therefore FALSE without a
        mechanism (scalaron = light trace mode of the G-field generating c3^{-9},
        or KMS-spectral renormalisation) -- the pre-registered kill test.
  [C] 7. THE COMPRESSION CONJECTURE (recorded, not proven).  The bridge proper is
        P_Sigma (G~ g~^-1) P_Sigma = Delta_Sigma^{1/2} -- the physical Calderon
        compression of her relative metric operator equals the TFPT seam modular
        operator; if proven, S_B is a local volume representation of the TFPT
        relative spectral action.  Open with the operator-level Hodge items
        (Clifford action, Dirac intertwining, leaf involution, Calderon
        polarisation).  Lorentzian positivity of G~ g~^-1 is NOT automatic
        (timelike gradients); TFPT's OS/reflection-positive route is the sturdier
        construction -- recorded.
  [O] 8. NOT CLOSED.  The equation-of-state status of v359 stays [O]; adopting
        S_B would close it ONLY after (7) and the R^2 mechanism (6).  No status
        marker moves; external reference, zero TFPT knobs added.

NET TYPING: [E] the five exact identities + the quantified gap; [C] the
compression conjecture, the eps_* assignment and the Q-target; [O] the
variational-completion gate itself.  External anchor: G. Bianconi, "Gravity from
entropy", Phys. Rev. D 111, 066001 (2025), arXiv:2408.14391 (DOI
10.1103/PhysRevD.111.066001).  Mixed exact (sympy, Wolfram-mirrored) + one
numerical quadrature (mpmath).
"""
import mpmath as mp
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

pi = sp.pi
c3 = sp.Rational(1, 8) / pi


def run():
    reset()
    print("v473  GRAV.ENTROPIC.ACTION.01: the Bianconi entropic-action bridge (PRD 111, 066001 (2025))")

    # 1. carrier Hodge count: Omega^{<=2}(C^5) has dim 1+5+10 = 16 = dim S+_{D5}
    dims = [sp.binomial(g_car, k) for k in (0, 1, 2)]
    dim_splus = 2 ** (g_car - 1)
    even = [sp.binomial(g_car, k) for k in (0, 2, 4)]
    fiber_4d = sum(sp.binomial(4, k) for k in (0, 1, 2))
    check("CARRIER HODGE COUNT [E]: dim Omega^{0,1,2}(C^5) = %s = 16 = 2^(g_car-1) = "
          "dim S+_{D5}; Hodge star L^1 ~= L^4 folds onto L^even C^5 (dims %s); "
          "two-form block binom(5,2) = 10; on 4d spacetime the fiber is only "
          "1+4+6 = %d -- the 16 REQUIRES the five-slot carrier (vector-space "
          "identity only)" % ("+".join(str(d) for d in dims), even, fiber_4d),
          sum(dims) == dim_splus == sum(even) == 16 and dims[2] == 10 and fiber_4d == 11)

    # 2. coefficient match: 3 beta' / G = 1/(16 pi G)  =>  beta' = c3/6 = 1/(48 pi)
    beta_p = sp.solve(sp.Eq(3 * sp.Symbol('bp'), sp.Rational(1, 16) / pi), sp.Symbol('bp'))[0]
    p2_A3 = sp.binomial(4, 2)  # |R+(A3)| = 4*3/2 = 6 positive roots
    check("COEFFICIENT MATCH [E]: 3 beta'_B = 1/(16 pi) = c3/2 => beta'_B = %s = "
          "c3/6 = 1/(48 pi); the 6 = 3 form blocks x 2 (EH 1/2) = p2 = |R+(A3)| = %d "
          "(structural echo, not a proof)" % (beta_p, p2_A3),
          sp.simplify(beta_p - c3 / 6) == 0 and
          sp.simplify(beta_p - sp.Rational(1, 48) / pi) == 0 and p2_A3 == 6)

    # 3. entropy potential s(x) = x - 1 - ln x: nonnegative, quadratic minimum at x=1
    x, eps = sp.symbols('x eps', positive=True)
    s = x - 1 - sp.log(x)
    series = sp.series(s.subs(x, 1 + eps), eps, 0, 4).removeO()
    smin = sp.solve(sp.diff(s, x), x)
    check("ENTROPY POTENTIAL [E]: s(x) = x - 1 - ln x has unique stationary point "
          "x = %s with s = 0, s'' = 1, series s(1+eps) = %s => Lambda_G = "
          "(1/4 beta) Tr eps^2 + O(eps^3) >= 0, QUADRATIC around the fixed point"
          % (smin, series),
          smin == [1] and s.subs(x, 1) == 0 and sp.diff(s, x, 2).subs(x, 1) == 1 and
          sp.simplify(series - (eps ** 2 / 2 - eps ** 3 / 3)) == 0)

    # 4. Lambda channel: (1/4 beta) e^{-2/a} TrQ^2 = (3/4 pi^2) e^{-2/a} Mbar^2
    #    with beta = beta' l_P^2, l_P^2 Mbar^2 = G Mbar^2 = 1/(8 pi) = c3
    TrQ2 = sp.Symbol('TrQ2')
    sol = sp.solve(sp.Eq(TrQ2 / (4 * (c3 / 6) * c3), sp.Rational(3, 4) / pi ** 2), TrQ2)[0]
    delta_top = 48 * c3 ** 4
    check("LAMBDA CHANNEL [E->C]: eps_* = e^{-1/alpha} Q makes Lambda_G ~ e^{-2/alpha} "
          "= the closed v60 branch (3/4 pi^2) e^{-2/alpha}; prefactor match "
          "(beta' = c3/6, l_P^2 Mbar^2 = c3) => Tr_F Q^2 = %s = 32 c3^4 = "
          "1/(128 pi^4) = (2/3) delta_top -- exact algebraic target for the "
          "two-form (pair) block, Q itself unconstructed [C]" % sol,
          sp.simplify(sol - 32 * c3 ** 4) == 0 and
          sp.simplify(sol - sp.Rational(1, 128) / pi ** 4) == 0 and
          sp.simplify(sol - sp.Rational(2, 3) * delta_top) == 0)

    # 5. Frullani: -ln a = int_0^inf dt/t (e^{-t a} - e^{-t})  (all-scale heat kernel)
    mp.mp.dps = 30
    frul = lambda a: mp.quad(lambda t: (mp.e ** (-t * a) - mp.e ** (-t)) / t, [0, mp.inf])
    err = max(abs(frul(a) + mp.log(a)) for a in (mp.mpf('0.4'), mp.mpf('2.5')))
    check("LOG = ALL-SCALE HEAT KERNEL [E] (Frullani): -ln A = int dt/t (e^{-tA} - "
          "e^{-t}), max residual %.1e -- the entropic action is an all-scale "
          "heat-kernel action, the right genre against S_rel,chi (KMS cutoff)" % err,
          err < mp.mpf('1e-12'))

    # 6. R^2 kill test: raw (c3/6)^2 vs TFPT 1/(12 c3^7); exact gap 3 c3^-9 = 3 (8 pi)^9
    raw = (c3 / 6) ** 2
    staro = 1 / (12 * c3 ** 7)
    gap = sp.simplify(staro / raw)
    check("R^2 KILL TEST [E/X-guard]: raw log-expansion coefficient (c3/6)^2 vs "
          "TFPT Starobinsky Mbar^2/(12 M_scal^2) = 1/(12 c3^7) (M_scal^2 = c3^7 "
          "Mbar^2, v36) -- EXACT gap %s = 3 (8 pi)^9 ~ %.3e (13 orders): a direct "
          "identification of the raw entropic action with the TFPT R^2 sector is "
          "FALSE without a mechanism (light G-trace mode generating c3^{-9}, or "
          "KMS-spectral renormalisation)" % (gap, float(gap)),
          sp.simplify(gap - 3 * (8 * pi) ** 9) == 0 and
          abs(float(gap) - 1.2002728758784e13) / 1.2e13 < 1e-3)

    # 7. the compression conjecture (recorded)
    check("COMPRESSION CONJECTURE [C] (recorded, NOT proven): P_Sigma (G~ g~^-1) "
          "P_Sigma = Delta_Sigma^{1/2} -- the Calderon compression of the relative "
          "metric operator = the TFPT seam modular operator; plus the operator-level "
          "Hodge items (Clifford, Dirac, leaf involution, Calderon polarisation); "
          "Lorentzian positivity NOT automatic -- TFPT's OS route is the sturdier "
          "construction", True)

    # 8. nothing closes
    check("NOT CLOSED [O]: v359's equation-of-state status stays [O]; adopting S_B "
          "would close it only after (7) + the R^2 mechanism (6); no marker moves, "
          "zero TFPT knobs added (external anchor: Bianconi, PRD 111, 066001 (2025), "
          "arXiv:2408.14391)", True)

    return summary("v473 GRAV.ENTROPIC.ACTION.01: Bianconi entropic-action bridge -- [E] "
                   "1+5+10=16=dim S+ (carrier-only; 4d fiber is 11), beta'_B = c3/6 = 1/(48 pi) "
                   "pinned, Lambda_G quadratic-nonnegative with exact target Tr Q^2 = 32 c3^4, "
                   "Frullani all-scale heat kernel, R^2 gap EXACTLY 3 (8 pi)^9 ~ 1.2e13; [C] "
                   "compression conjecture P (G g^-1) P = Delta^1/2; [O] variational completion "
                   "open, no gate closed")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
