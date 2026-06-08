"""v81 -- the mass-transport pencil P(x)=K+xQ as a projective line with two anchor-block
singularities, and the double cover branched over them.

CENTRAL RESULT (the double cover -- [I/L]).  The anchor-block determinant
    det B(K+xQ) = 9x^2+21x+10 = (3x+2)(3x+5)
is a QUADRATIC, so y^2 = det B(K+xQ) is a 2:1 cover of the pencil line, ramified exactly over its
two zeros.  Hence the Koide/gap point x=-|Z2|/N_fam=-2/3 and the carrier point x=-g_car/N_fam=-5/3
are the TWO BRANCH POINTS of one double cover (deck involution y -> -y, degree 2 = |Z2| = the sheet).
  - branch locus = -(spine ends {2,5})/N_fam  (|Z2| and g_car, the two ends of the spine (2,3,4,5))
  - discriminant = 81 = N_fam^4 (perfect square => rational branch points, split cover)
  - branch separation = 1 = one transport period (the K->L step x:0->1); deck-translation x->x+1
    carries the carrier point onto the Koide point.
So Koide is literally "the other side" of the carrier point under the sheet double cover.

The two clearing matrices at the branch points (clear the 3-denominator):
  KOIDE point   C_{2/3} := 3K-2Q : reproduces the D5(+)A3 carrier glue
       tr=15=dim A3, sum=45=dim D5, sigma2=20=det L, det=60=D_start;
       rank-one anchor block B(C23)=(g_car,scalaron)^T (N_fam^2,|Pl(K)|) = (5,7)^T(9,11), sum=240=|R(E8)|.
  CARRIER point C_{5/3} := 3K-5Q : a charge-NEUTRAL SM-signature matrix
       sum=0, chi=(lam+|Z2|)(lam^2+lam+|R+(A3)|)=(lam+2)(lam^2+lam+6),
       rowSums=(-2,2,0) (sheet pair + neutral), colSums=(-6,-1,7) (hexagon, Higgs singlet, scalaron deficit).

Scalaron as the mixed anchor area [I]:  B_L=B_K+B_Q (linearity), so the polarization / mixed
discriminant det(B_K+B_Q)-det B_K-det B_Q = 40-10-9 = 21 = N_fam*7, i.e. 7 = mixed disc / N_fam.

Sheet-endpoint readout of c_u/c_d [I]:  at K-Q, B(K-Q)=[[10,13],[14,18]], sum=55, B12=13=Delta_Q,
and c_u/c_d = sum B / (det B_Q * B12) = 55/(9*13) = 55/117 (diagnostic; Plucker v37 stays canonical).

DEEPER (what the cover unifies):
  - BRANCH DIVISOR = (scalaron, A_Lambda).  The two branch points have sum = -scalaron/N_fam and
    product = A_Lambda/N_fam^2; equivalently the integer labels {|Z2|,g_car}={2,5} have sum=7=scalaron,
    product=10=A_Lambda, diff=3=N_fam.  So the scalaron is the TRACE of the branch divisor of the
    mass-transport double cover -- the several scalaron readouts (Omega-10b1, A_Lambda-N_fam, g_car+|Z2|,
    mixed anchor disc) all collapse to this one geometric origin.
  - FIBER & SHEET.  y^2=det B is A_Lambda at K and 4*A_Lambda at L, so transport K->L multiplies the fiber
    by |Z2|; the Z2 sheet endpoint x=-1 lies between the branch points where y^2=-|Z2|<0 -- the sheet lives
    on the imaginary branch cut joining Koide and the carrier.
  - ANCHOR-FIRST.  The clean cover is a property of the anchor 2-plane <1,a>; the full-3-space cubic
    det(K+xQ) has disc -1132 and an irrational real root, so the anchor projection is what regularises it.
"""
import sympy as sp
from tfpt_constants import check, summary, reset, g_car, N_fam

x, lam = sp.symbols('x lam')


def run():
    reset()
    print("v81  singular pencil + double cover")

    K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
    Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
    L = K + Q
    one = sp.Matrix([1, 1, 1]); a = sp.Matrix([1, 1, 2])
    B = lambda M: sp.Matrix([[(one.T * M * one)[0], (one.T * M * a)[0]],
                             [(a.T * M * one)[0], (a.T * M * a)[0]]])
    asum = lambda M: sum(M)
    sig2 = lambda M: sp.Rational(1, 2) * (M.trace()**2 - (M * M).trace())

    # --- DOUBLE COVER (central) [I/L] ---
    f = sp.expand(B(K + x * Q).det())
    roots = sorted(sp.solve(f, x))
    check("[DC] det B(K+xQ)=(3x+2)(3x+5) is quadratic => double cover y^2=det B(K+xQ); branch points "
          "{-|Z2|/N_fam,-g_car/N_fam}={-5/3,-2/3} = -(spine ends 2,5)/N_fam; deck degree 2=|Z2|",
          f == 9 * x**2 + 21 * x + 10 and roots == [sp.Rational(-5, 3), sp.Rational(-2, 3)]
          and roots == [sp.Rational(-2, N_fam), sp.Rational(-g_car, N_fam)][::-1])
    check("[DC] discriminant of det B(K+xQ) = 81 = N_fam^4 (perfect square => rational, split cover); "
          "sqrt = 9 = N_fam^2 = det B_Q",
          sp.discriminant(f, x) == 81 == N_fam**4 and sp.sqrt(sp.discriminant(f, x)) == N_fam**2 == B(Q).det())
    check("[DC] branch separation = 1 = one transport period (K->L is x:0->1); deck-translation x->x+1 "
          "carries carrier point -5/3 onto Koide point -2/3",
          abs(roots[0] - roots[1]) == 1 and roots[0] + 1 == roots[1])

    # --- branch-divisor symmetric functions = (scalaron, A_Lambda) [I/L] : unifies the scalaron ---
    s = roots[0] + roots[1]; p = roots[0] * roots[1]
    check("[DC] branch-divisor symmetric fns: sum = -scalaron/N_fam = -7/3, product = A_Lambda/N_fam^2 = 10/9; "
          "equivalently the integer labels {|Z2|,g_car}={2,5} have sum=7=scalaron, product=10=A_Lambda, "
          "diff=3=N_fam => the scalaron is the TRACE of the branch divisor (not a leftover)",
          s == sp.Rational(-7, 3) and p == sp.Rational(10, 9)
          and 2 + g_car == 7 and 2 * g_car == 10 and g_car - 2 == N_fam
          and -N_fam * s == 7 and N_fam**2 * p == 10)

    # --- fiber coordinate: transport doubles it; the Z2 sheet sits on the cut between branch points [I] ---
    fiber = lambda xv: f.subs(x, xv)
    check("[DC] fiber y^2=det B: at K (x=0) y^2=10=A_Lambda, at L (x=1) y^2=40=4*A_Lambda, so transport K->L "
          "multiplies the fiber y by |Z2|=2; the Z2 sheet endpoint x=-1 lies BETWEEN the branch points where "
          "y^2=det B(K-Q)=-2=-|Z2|<0 (imaginary branch cut Koide<->carrier), fiber = i*sqrt(|Z2|)",
          fiber(0) == 10 and fiber(1) == 40 and sp.sqrt(fiber(1)) / sp.sqrt(fiber(0)) == 2
          and fiber(-1) == -2 and sp.Rational(-5, 3) < -1 < sp.Rational(-2, 3))

    # --- the clean cover lives on the anchor 2-plane <1,a>: full 3-space cubic is NOT rational [I] ---
    cub = sp.expand((K + x * Q).det())
    check("[DC] the clean double cover is a property of the anchor 2-plane <1,a>: the full-3-space determinant "
          "det(K+xQ)=3x^3+7x^2+6x+4 has discriminant -1132 (one irrational real root ~ -1.605, not a branch "
          "point) => the anchor projection is what regularises the geometry (anchor-first)",
          cub == 3 * x**3 + 7 * x**2 + 6 * x + 4 and sp.discriminant(cub, x) == -1132
          and not sp.real_roots(cub)[0].is_rational)

    # --- KOIDE point C_{2/3}=3K-2Q [I/L] ---
    C23 = 3 * K - 2 * Q
    check("[Koide] C_{2/3}=3K-2Q: tr=15=dim A3, sum=45=dim D5, sigma2=20=det L, det=60=D_start",
          C23.trace() == 15 and asum(C23) == 45 and sig2(C23) == 20 and C23.det() == 60)
    check("[Koide] anchor block B(C_{2/3})=(g_car,scalaron)^T (N_fam^2,|Pl K|)=(5,7)^T(9,11) rank-one "
          "(forced by the singularity det B=0); sum=240=|R(E8)|=(g_car+7)(N_fam^2+11)",
          B(C23) == sp.Matrix([g_car, 7]) * sp.Matrix([[N_fam**2, 11]]) and asum(B(C23)) == 240
          and B(C23).det() == 0 and (g_car + 7) * (N_fam**2 + 11) == 240)

    # --- CARRIER point C_{5/3}=3K-5Q [I/L] ---
    C53 = 3 * K - 5 * Q
    check("[carrier] C_{5/3}=3K-5Q is charge-neutral: sum=0; chi=(lam+|Z2|)(lam^2+lam+|R+A3|)="
          "(lam+2)(lam^2+lam+6); rowSums=(-2,2,0), colSums=(-6,-1,7)",
          asum(C53) == 0
          and sp.factor(C53.charpoly(lam).as_expr()) == (lam + 2) * (lam**2 + lam + 6)
          and [sum(C53.row(i)) for i in range(3)] == [-2, 2, 0]
          and [sum(C53.col(j)) for j in range(3)] == [-6, -1, 7])

    # --- scalaron = mixed anchor area [I] ---
    check("[scalaron] B_L=B_K+B_Q (linearity); mixed discriminant det(B_K+B_Q)-det B_K-det B_Q="
          "40-10-9=21=N_fam*7 => 7 = mixed anchor area / N_fam (not a leftover)",
          B(L) == B(K) + B(Q)
          and B(L).det() - B(K).det() - B(Q).det() == 21 == N_fam * 7
          and (B(L).det() - B(K).det() - B(Q).det()) / N_fam == 7)

    # --- sheet-endpoint readout of c_u/c_d [I] ---
    BKQ = B(K - Q)
    check("[u/d] sheet endpoint K-Q: B(K-Q)=[[10,13],[14,18]], sum=55, B12=13=Delta_Q, det(K-Q)=2=|Z2|; "
          "c_u/c_d = sum B/(det B_Q * B12)=55/(9*13)=55/117 (diagnostic; Plucker v37 canonical)",
          BKQ == sp.Matrix([[10, 13], [14, 18]]) and asum(BKQ) == 55 and BKQ[0, 1] == 13
          and (K - Q).det() == 2
          and sp.Rational(asum(BKQ), B(Q).det() * BKQ[0, 1]) == sp.Rational(55, 117))
    return summary("v81 singular pencil + double cover")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
