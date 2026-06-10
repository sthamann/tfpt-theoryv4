"""v85 -- Master-Cover Theorem: next.txt P3 answered, P6 honest negative, P4 typed.

Resolves the prioritised open questions P3/P4/P6 of the anchor-block
double-cover programme (next.txt, secs. 3-4; builds on v80/v81/v82).

P3 (the family of covers -- ANSWERED, [I]/[L]):
    There is exactly ONE anchor-block double cover on the pencil plane
    span{K,Q}, the master cover  y^2 = det B(K+xQ) = (3x+2)(3x+5).
    For ANY basis change G = [[alpha,beta],[gamma,delta]] in GL(2),
        det B((aK+bQ) + x(cK+dQ)) = (gamma x + alpha)^2 * p_KQ(moebius_G(x)),
    an exact symbolic identity, so every member of the family is the SAME
    cover up to a Moebius reparametrisation of the line, and
        disc = 81 * det(G)^2 = N_fam^4 * det(G)^2.
    The observed family in next.txt P3 is exactly this orbit:
        branch(L+xQ)  = {-8/3,-5/3} = branch - 1      (transport translation)
        branch(K+xL)  = {-5/8,-2/5} = x/(1+x)-preimages
        branch(Q+xK)  = {-3/2,-3/5} = 1/branch        (basis swap)
    and the 'auffaellige' rung -8/3 = -rank(E8)/N_fam is no new structure:
    it is the carrier point shifted by one transport period,
        -(g_car + N_fam)/N_fam = -g_car/N_fam - 1   (rank E8 = g_car + N_fam).
    Negative controls: leaving the anchor plane breaks the structure --
    the R-direction covers have non-square discriminants (153, 201), i.e.
    non-split branch points (anchor-first, consistent with v82(B)).

P6 (mu4 = Z4 vs deck Z2 -- HONEST NEGATIVE, [I]):
    The natural 4-sheet candidate over the transport tower,
    y^4 = det B(K+xQ) * det B(L+xQ), FACTORS through a forced square
    (3x+5)^2 (the shared carrier point), so mu4 does NOT act as a genuine
    4:1 cover of the pencil line.  What the tower generates instead is a
    ladder of double covers: rung n has branch {-2/3-n, -5/3-n}, and the
    second-level cover w^2 = (3x+2)(3x+8) (disc 324 = 18^2) connects Koide
    directly to -rank(E8)/N_fam at branch separation 2 = |Z2| periods.

P4 (scalaron trace -> Starobinsky parameters -- TYPED, [I] + honest scope):
    The branch divisor fixes the SCALE exponent only: trace = -7/3 =
    -scalaron/N_fam, so M_scal = c3^{7/2} Mbar is algebraically addressed
    (v80/v81).  The tilt observables n_s = 1 - 2/N_star and r = 12/N_star^2
    are functions of the external reheating input N_star ALONE -- the cover
    cannot promote them from [P]; only the mass scale is algebraic.
    (Registered as bands over N_star in [50,60] in predictions_frozen.json.)

All statements here are exact integer/symbolic arithmetic [I] (with the
Lie-data labels [L]); the physical readings (Koide branch <-> physical Koide
value, sheet <-> Spin(10) half-spinor) remain [P] exactly as typed in
v81/v82 and next.txt sec. 5.
"""
import sympy as sp
from tfpt_constants import check, summary, reset

x = sp.symbols('x')
al, be, ga, de = sp.symbols('alpha beta gamma delta')

K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
L = K + Q
ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])     # the anchor a = (1,1,2)

N_FAM, G_CAR, Z2, RANK_E8, SCALARON = 3, 5, 2, 8, 7


def anchor_block(M):
    return sp.Matrix([[(ONE.T * M * ONE)[0], (ONE.T * M * A)[0]],
                      [(A.T * M * ONE)[0], (A.T * M * A)[0]]])


def cover_poly(M, N):
    return sp.expand(sp.det(anchor_block(M + x * N)))


def branch(M, N):
    return sorted(sp.solve(cover_poly(M, N), x))


def run():
    reset()
    print("v85 master-cover theorem (next.txt P3 answered; P6 negative; P4 typed)")

    # ---- the master cover -------------------------------------------------
    pKQ = cover_poly(K, Q)
    check("master cover det B(K+xQ) = (3x+2)(3x+5)",
          sp.factor(pKQ) == sp.factor((3 * x + 2) * (3 * x + 5)), exact=False)
    check("master discriminant = 81 = N_fam^4",
          sp.discriminant(pKQ, x), N_FAM**4, exact=True)
    check("branch locus = {-g_car/N_fam, -|Z2|/N_fam} = {-5/3, -2/3}",
          branch(K, Q) == [sp.Rational(-5, 3), sp.Rational(-2, 3)])

    # ---- P3: GL(2) Moebius covariance => ONE cover up to reparametrisation
    M2 = al * K + be * Q
    N2 = ga * K + de * Q
    p2 = sp.expand(sp.det(anchor_block(M2 + x * N2)))
    moebius_image = pKQ.subs(x, (de * x + be) / (ga * x + al))
    residual = sp.simplify(p2 - sp.expand((ga * x + al)**2 * moebius_image))
    check("GL(2) covariance: det B(G.(K,Q)+x..) = (gamma x+alpha)^2 p_KQ(moebius_G x) "
          "(exact symbolic identity)", residual == 0)
    check("disc transforms as 81*det(G)^2 (master invariant x square)",
          sp.factor(sp.discriminant(p2, x)) == sp.factor(81 * (al * de - be * ga)**2))

    # the observed family = the GL(2) orbit of the master cover
    check("branch(L+xQ) = master branch - 1 (transport translation)",
          branch(L, Q) == [b - 1 for b in branch(K, Q)])
    check("branch(K+xL) = x/(1+x)-preimages {-5/8,-2/5}",
          branch(K, L) == [sp.Rational(-5, 8), sp.Rational(-2, 5)])
    check("branch(Q+xK) = 1/branch (basis swap) {-3/2,-3/5}",
          branch(Q, K) == [sp.Rational(-3, 2), sp.Rational(-3, 5)])

    # the 'auffaellige' rung -8/3 explained: carrier - one transport period
    check("-8/3 = -rank(E8)/N_fam = carrier point - 1 (rank E8 = g_car + N_fam, "
          "no new structure)",
          sp.Rational(-RANK_E8, N_FAM) == sp.Rational(-G_CAR, N_FAM) - 1
          and RANK_E8 == G_CAR + N_FAM)

    # negative controls: outside the anchor plane the cover does NOT split
    dR1 = sp.discriminant(cover_poly(R, Q), x)
    dR2 = sp.discriminant(cover_poly(K, R), x)
    check("R-direction non-split: disc(R+xQ)=153 not a square (anchor-first)",
          dR1 == 153 and not sp.sqrt(dR1).is_rational)
    check("R-direction non-split: disc(K+xR)=201 not a square (anchor-first)",
          dR2 == 201 and not sp.sqrt(dR2).is_rational)

    # ---- P6: honest negative on a genuine Z4 cover ------------------------
    prod = sp.factor(cover_poly(K, Q) * cover_poly(L, Q))
    check("4-sheet candidate factors through the forced square (3x+5)^2 "
          "=> mu4 is NOT a 4:1 cover of the pencil line",
          prod == sp.factor((3 * x + 2) * (3 * x + 5)**2 * (3 * x + 8)))
    w2 = sp.cancel(prod / (3 * x + 5)**2)
    check("second-level cover w^2=(3x+2)(3x+8): disc=324=18^2, split",
          sp.discriminant(sp.expand(w2), x) == 324)
    check("second-level branch {-2/3,-8/3}: Koide <-> rank E8, separation "
          "2 = |Z2| transport periods",
          sorted(sp.solve(w2, x)) == [sp.Rational(-8, 3), sp.Rational(-2, 3)]
          and sp.Rational(-2, 3) - sp.Rational(-8, 3) == Z2)
    n = sp.symbols('n')
    check("transport tower rung n: branch = {-2/3-n, -5/3-n} (ladder of double "
          "covers, never a single 4:1 object)",
          sorted(sp.solve(cover_poly(K + n * Q, Q), x),
                 key=lambda e: e.subs(n, 0)) ==
          [-n - sp.Rational(5, 3), -n - sp.Rational(2, 3)])

    # ---- P4: the cover fixes the SCALE, not the tilt ----------------------
    tr = sum(branch(K, Q))
    check("branch-divisor trace = -7/3 = -scalaron/N_fam (algebraic address "
          "of the scalaron exponent, v80/v81)",
          tr == sp.Rational(-SCALARON, N_FAM))
    Ns = sp.symbols('N_star', positive=True)
    n_s = 1 - 2 / Ns
    r_t = 12 / Ns**2
    check("n_s and r depend on the external N_star ALONE (d/dN_star != 0): the "
          "cover cannot promote the tilt from [P]; only M_scal is algebraic",
          sp.diff(n_s, Ns) != 0 and sp.diff(r_t, Ns) != 0
          and SCALARON == Z2 + G_CAR)

    return summary("v85 master cover")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
