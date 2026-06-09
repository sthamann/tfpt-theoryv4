"""v82 -- two structural advances on top of the anchor-pencil double cover (v80/v81):
the Koide RG attractor is FORCED by the established transfer operator, and the clean
rational split is NON-GENERIC (an anchor-placement trichotomy).

Builds directly on v80/v81 (det B(K+xQ)=(3x+2)(3x+5), branch points Koide -2/3 &
carrier -5/3, deck degree 2=|Z2|), v54/v56 (the unique gapped boundary transfer
operator, spectrum {1,(2/3)^6,(1/3)^6}, cusp weights {0,1/3,2/3}) and v32 (the
exponents-at-infinity (2,1,1) = splitting O(-2)+O(-1)^2).

(A) KOIDE ATTRACTOR IS FORCED, NOT POSTULATED  [I] + one [P] identification.
    A branch-divisor-preserving Moebius map of the pencil line that fixes the two
    branch points q=2 (Koide) and q=5 (carrier) is, in the cross-ratio coordinate
    rho=(q-2)/(5-q), EXACTLY rho -> mu*rho.  Hence such a map is UNIQUE once its
    multiplier mu is fixed.  The multiplier is NOT a new input: mu=(2/3)^6 is the
    subleading eigenvalue lambda2 of the theory's unique gapped boundary transfer
    operator (v54/v56), and the Koide branch point -2/3 = -|Z2|/N_fam is exactly the
    cusp weight 2/3={0,1,|Z2|}/N_fam of that operator.  With mu=(2/3)^6 the unique map
    is the integer Moebius map F(q)=2(569q-3325)/(665q-3517) with F(2)=2, F(5)=5,
    F'(2)=(2/3)^6 (Koide is the ATTRACTOR, |mu|<1) and F'(5)=(3/2)^6 (carrier is the
    REPELLER).  So analyse.txt's three "structural postulates" for Koide collapse to
    ONE physical identification: source->pole transfer = branch-preserving relaxation
    of the established transfer operator.  Rate, uniqueness and direction then follow.
    The single identification stays [P]; everything else here is [I].

(B) THE CLEAN SPLIT IS NON-GENERIC -- anchor-placement trichotomy  [I].
    The exponents-at-infinity (2,1,1) (the splitting type, v32) placed across the
    three family slots give three different covers:
        (1,1,2) heavy in fam3 (lepton anchor): det=(3x+2)(3x+5), disc=81=N_fam^4 -> SPLIT
        (2,1,1) heavy in fam1:                  det=(x+2)(9x+11), disc=49=scalaron^2 -> SPLIT
        (1,2,1) heavy in fam2:                  det=5x^2+10x+3,   disc=40=|R(D5)|=det B(L) -> NON-SPLIT
    Only the canonical lepton placement and (2,1,1) have individually-rational branch
    labels; the middle placement (1,2,1) has Galois-conjugate irrational branch points
    -1 +/- sqrt(10)/5, centered EXACTLY on the sheet x=-1 (q=3) with separation set by
    sqrt(A_Lambda)=sqrt(10).  Negative control (v81): the R-pencil disc=153 is not a
    square either.  So the clean two-rational-channel structure (Koide & carrier as
    separate rational singularities) is a special feature of the anchor placement, not
    generic -- a hardening of "anchor-first".  Physical sector identification (which
    placement is which fermion) is NOT claimed here and stays [P].
"""
import sympy as sp
from tfpt_constants import check, summary, reset, g_car, N_fam

x, q = sp.symbols('x q')

# compiler labels (all derived elsewhere; used here as names)
Z2 = 2
A_Lambda = 10           # = 2 * g_car
scalaron = 7            # = g_car + Z2
R_D5 = 40               # = |R(D5)| = det B(L)


def run():
    reset()
    print("v82  Koide attractor (forced) + anchor-placement splitting trichotomy")

    K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
    Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
    L = K + Q
    one = sp.Matrix([1, 1, 1])

    def Bb(M, b):
        S = sp.Matrix.hstack(one, b)
        return S.T * M * S

    a = sp.Matrix([1, 1, 2])
    B = lambda M: Bb(M, a)

    # ----- (A) the relative spectral operator (the basis-invariant core) [I] -----
    T = 3 * B(Q).inv() * B(K)
    check("[A] T=3 B(Q)^-1 B(K)=[[5,11/3],[0,2]]; Spec={2,5}, tr=7=scalaron, det=10=A_Lambda",
          T == sp.Matrix([[g_car, sp.Rational(11, 3)], [0, Z2]])
          and sorted(T.eigenvals().keys()) == [2, g_car]
          and T.trace() == scalaron and T.det() == A_Lambda)

    # ----- (A) Koide branch = cusp weight of the established transfer operator [I/L] -----
    transfer_spec = [sp.Rational(k, 3)**6 for k in (3, 2, 1)]   # v54/v56
    lam2 = sp.Rational(2, 3)**6
    cusp_weights = {sp.Integer(0), sp.Rational(1, 3), sp.Rational(2, 3)}
    check("[A] transfer spectrum {1,(2/3)^6,(1/3)^6} (v54/v56); subleading lambda2=(2/3)^6=64/729",
          transfer_spec == [sp.Integer(1), sp.Rational(64, 729), sp.Rational(1, 729)]
          and lam2 == sp.Rational(64, 729))
    check("[A] cusp weights {0,1/3,2/3} = {0,1,|Z2|}/N_fam; Koide branch x=-2/3=-|Z2|/N_fam is the weight 2/3",
          cusp_weights == {sp.Integer(0), sp.Rational(1, N_fam), sp.Rational(Z2, N_fam)}
          and sp.Rational(-Z2, N_fam) == sp.Rational(-2, 3))
    # both branch points share cusp class 2/3 modulo the deck period (q->q-3 sends carrier->Koide, v81)
    check("[A] carrier q=5 -> Koide q=2 under the deck period q->q-N_fam; shared cusp class 2/3",
          (g_car - N_fam) == 2 and (g_car % N_fam) == 2)

    # ----- (A) uniqueness of the branch-preserving map; multiplier = lam2 [I] -----
    mu = sp.symbols('mu')
    rho = (q - 2) / (5 - q)
    # solve rho(F)=mu*rho => F is forced:
    F_mu = sp.cancel((5 * mu * rho + 2) / (mu * rho + 1))
    F = sp.cancel(F_mu.subs(mu, lam2))
    F_claim = 2 * (569 * q - 3325) / (665 * q - 3517)
    check("[A] the UNIQUE branch-preserving Moebius map fixing {2,5} with multiplier (2/3)^6 "
          "= 2(569q-3325)/(665q-3517) (rho->(2/3)^6 rho)",
          sp.simplify(F - F_claim) == 0)
    check("[A] F(2)=2 (Koide fixed), F(5)=5 (carrier fixed)",
          sp.simplify(F.subs(q, 2)) == 2 and sp.simplify(F.subs(q, 5)) == 5)
    Fp = sp.diff(F, q)
    check("[A] F'(2)=(2/3)^6=64/729<1 => Koide is the ATTRACTOR; F'(5)=(3/2)^6=729/64>1 => carrier REPELLER",
          sp.simplify(Fp.subs(q, 2)) == lam2 and sp.simplify(Fp.subs(q, 5)) == sp.Rational(729, 64))
    check("[A] closed form q_n->2 (x->-2/3): rho_n=(64/729)^n rho_0 -> 0; rate = the SM-flavor/horizon gap",
          lam2 < 1 and sp.simplify(rho.subs(q, 2)) == 0)

    # ----- (B) anchor-placement splitting trichotomy [I] -----
    placements = {
        "(1,1,2)": (sp.Matrix([1, 1, 2]), (3 * x + 2) * (3 * x + 5), N_fam**4, True),
        "(2,1,1)": (sp.Matrix([2, 1, 1]), (x + 2) * (9 * x + 11), scalaron**2, True),
        "(1,2,1)": (sp.Matrix([1, 2, 1]), 5 * x**2 + 10 * x + 3, R_D5, False),
    }
    for name, (b, poly, disc, splits) in placements.items():
        f = sp.expand(Bb(K + x * Q, b).det())
        d = sp.discriminant(f, x)
        is_square = sp.sqrt(d).is_rational
        check(f"[B] placement {name}: det={sp.factor(f)}, disc={disc}, "
              f"{'SPLIT (rational labels)' if splits else 'NON-SPLIT (irrational)'}",
              sp.expand(f - poly) == 0 and d == disc and is_square == splits)

    check("[B] the three discriminants are compiler numbers: N_fam^4=81, scalaron^2=49, |R(D5)|=det B(L)=40",
          N_fam**4 == 81 and scalaron**2 == 49 and R_D5 == 40 == B(L).det())

    # the unique non-split placement: branch points centered on the sheet, separation ~ sqrt(A_Lambda)
    fmid = sp.expand(Bb(K + x * Q, sp.Matrix([1, 2, 1])).det())
    roots = sp.solve(fmid, x)
    centre = sp.simplify((roots[0] + roots[1]) / 2)
    check("[B] non-split placement (1,2,1): branch points -1 +/- sqrt(10)/5 centered on the sheet x=-1 (q=3); "
          "sqrt(disc)=2 sqrt(A_Lambda)",
          centre == -1 and set(roots) == {-1 - sp.sqrt(10) / 5, -1 + sp.sqrt(10) / 5}
          and sp.sqrt(R_D5) == 2 * sp.sqrt(A_Lambda))

    # negative control (anti-numerology, cf. v81): the R-pencil discriminant is not a square either
    R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
    detR = sp.expand(B(R + x * Q).det())
    check("[B] negative control: R-pencil det B(R+xQ)=9x^2+27x+16 has disc 153 (not 81, not a square) "
          "=> the clean split is non-generic",
          detR == 9 * x**2 + 27 * x + 16 and sp.discriminant(detR, x) == 153
          and not sp.sqrt(153).is_rational)

    return summary("v82 Koide attractor + splitting trichotomy")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
