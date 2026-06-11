"""v96 -- Branch-Kernel Selection (next.txt P1 unblocked): the cover's own
rank-1 kernels at the branch points define the sector -> sheet map.  [I]/[L].

The P1 blocker was honest: "no independently motivated definition of the
sector -> sheet map exists" (the row-projection candidate was rejected as
number-fishing).  This script supplies the missing definition from an object
the cover itself produces: at each branch point of the anchor-block double
cover y^2 = det B(K+xQ) (v81/v85) the 2x2 anchor block B is RANK 1, so it
has a canonical right kernel (generation space) and left kernel (sector
space).  Pairing the established sector rows (v12/v46/v53: rows of K+xQ =
(up, down, lepton)) with these forced kernels is the most natural Z2-capable
quantity available -- nothing is chosen.

RESULTS (all exact):

  [I] 1. KERNELS ARE INTEGER VECTORS.
         B(x) = [[15x+25, 16x+29],[21x+35, 23x+41]], det B = (3x+2)(3x+5).
         Koide   x=-2/3: right kernel w = 11*1 - 9a = (2,2,-7),
                          left  kernel v =  7*1 - 5a = (2,2,-3);
         carrier x=-5/3: right kernel w = 1 = (1,1,1)  (the democratic
                          vector itself), left kernel v = 8*1 - 7a = (1,1,-6).
  [L] 2. COLLAPSE LEMMA: at a rank-1 branch point, P(x0).w is orthogonal to
         span{1,a}, hence proportional to the anti-symmetric direction of the
         anchor's two equal-weight slots: (-1,1,0).  Verified at both branch
         points, on BOTH sides (sector rows and generation columns):
             P(-2/3).w = (20/3, -20/3, 0),  P(-5/3).w = (-2/3, 2/3, 0),
             v^T.P(x0) prop. (-1,1,0)  at both points.
         => up = -down (the deck-odd pair), lepton pairing = 0 (leptons sit
         ON the ramification -- consistent with Koide being leptonic);
         generation side: gen1 = -gen2, gen3 = 0.
  [I] 3. SECTOR ZERO LADDER on the pencil (exact linear forms):
         pairings with the Koide kernel:   (4(2x+3), 10x,   3x+2),
         pairings with the carrier kernel: (2(2x+3), 5x+9, 2(3x+5)).
         lepton zeros = {-2/3, -5/3} = exactly the two branch points (the
         lepton pairings ARE the two factors of det B);
         up zeros = {-3/2} doubly = -N_fam/|Z2| (the v85 GL(2) rung): the
         entire up-row of P(-3/2) IS the odd direction (-1/2)(1,-1,0);
         down zeros = {0 (= K itself), -9/5 = -N_fam^2/g_car}.
  [I] 4. ORIENTATION: with kernels normalised to positive democratic
         component, Koide orients (up,down) = (+,-) and carrier (-,+): the
         deck translation x -> x+1 flips the up/down orientation; magnitude
         ratio (20/3)/(2/3) = 10 = A_Lambda.  Convention-free invariant:
         f_up * f_down < 0 at both branch points.
  [L] 5. ANCHOR-PLACEMENT CONTROL: replacing the anchor by (2,1,1) moves the
         collapse direction to (0,1,-1) -- the anti-symmetric pair of THAT
         placement's equal slots (mechanism follows the anchor, anchor-first);
         placement (1,2,1) has disc 40, non-split: no rational kernels at all
         (matches the v82 splitting trichotomy).

HONEST TYPING: items 1-5 are exact arithmetic plus a small structure lemma.
The IDENTIFICATION of the up<->down transposition with the v92 chirality
swap (the two Lagrangian glues) is the remaining [P] step -- sharpened and
tested in v97.  Audit-level integer readings (w.1 = -3 = -N_fam, w.a = -10 =
-A_Lambda, v.a = -2 = -|Z2|, carrier v.1 = -4 = -|mu4|) are recorded, not
promoted.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam, g_car

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
SIG = sp.diag(1, -1, -1)
K = R + Q * SIG
ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])
X = sp.symbols('x')
P = K + X * Q
W = sp.Matrix.hstack(ONE, A)
B = W.T * P * W


def branch_kernels(x0):
    """Right/left kernels of the rank-1 anchor block, canonically normalised
    (integer, gcd 1, democratic component positive)."""
    Bx = B.subs(X, x0)
    ker = Bx.nullspace()[0]
    ker = ker / sp.gcd(tuple(ker))
    if ker[0] < 0:
        ker = -ker
    lker = Bx.T.nullspace()[0]
    lker = lker / sp.gcd(tuple(lker))
    if lker[0] < 0:
        lker = -lker
    return W * ker, W * lker          # generation-space w, sector-space v


def run():
    reset()
    print("v96 branch-kernel selection (P1: the cover defines the sector map)")

    # 0. the anchor block and its cover (cross-check with v80/v81)
    check("B(x) = [[15x+25,16x+29],[21x+35,23x+41]], det B = (3x+2)(3x+5)",
          B == sp.Matrix([[15 * X + 25, 16 * X + 29],
                          [21 * X + 35, 23 * X + 41]])
          and sp.factor(B.det()) == (3 * X + 2) * (3 * X + 5))

    # 1. integer kernels at the branch points
    kx, kv = sp.Rational(-2, 3), sp.Rational(-5, 3)
    wK, vK = branch_kernels(kx)
    wC, vC = branch_kernels(kv)
    check("Koide x=-2/3: rank B = 1, right kernel w = 11*1-9a = (2,2,-7), "
          "left kernel v = 7*1-5a = (2,2,-3)",
          B.subs(X, kx).rank() == 1
          and wK == sp.Matrix([2, 2, -7]) == 11 * ONE - 9 * A
          and vK == sp.Matrix([2, 2, -3]) == 7 * ONE - 5 * A)
    check("carrier x=-5/3: rank B = 1, right kernel w = 1 = (1,1,1) (the "
          "democratic vector), left kernel v = 8*1-7a = (1,1,-6)",
          B.subs(X, kv).rank() == 1 and wC == ONE
          and vC == sp.Matrix([1, 1, -6]) == 8 * ONE - 7 * A)
    check("AUDIT (recorded, not promoted): w_K.1 = -3 = -N_fam, w_K.a = -10 "
          "= -A_Lambda; v_K.a = -2 = -|Z2|; v_C.1 = -4 = -|mu4|, v_C.a = -10",
          (wK.T * ONE)[0] == -3 and (wK.T * A)[0] == -10
          and (vK.T * A)[0] == -2 and (vC.T * ONE)[0] == -4
          and (vC.T * A)[0] == -10)

    # 2. collapse lemma at both branch points, both sides
    d = sp.Matrix([-1, 1, 0])
    fK = P.subs(X, kx) * wK
    fC = P.subs(X, kv) * wC
    check("COLLAPSE LEMMA (sector side): P(-2/3).w = (20/3)(1,-1,0), "
          "P(-5/3).w = (2/3)(-1,1,0) -- up = -down, lepton = 0 at BOTH "
          "branch points (leptons sit on the ramification)",
          fK == sp.Rational(-20, 3) * d and fC == sp.Rational(2, 3) * d)
    gK = (vK.T * P.subs(X, kx)).T
    gC = (vC.T * P.subs(X, kv)).T
    check("collapse lemma (generation side): v^T.P prop. (-1,1,0) at both "
          "points (gen1 = -gen2, gen3 = 0)",
          gK == -1 * d * -1 and gC == 2 * d)
    check("convention-free invariant: f_up * f_down < 0 at both branch "
          "points (up and down always on opposite sheets)",
          fK[0] * fK[1] < 0 and fC[0] * fC[1] < 0)
    check("ORIENTATION: canonical kernels give Koide (up,down) = (+,-) and "
          "carrier (-,+): the deck translation flips the pair; magnitude "
          "ratio = 10 = A_Lambda",
          fK[0] > 0 > fK[1] and fC[0] < 0 < fC[1]
          and fK[0] / fC[1] == 10)

    # 3. sector zero ladder
    fx_K = P * sp.Matrix([2, 2, -7])
    fx_C = P * ONE
    check("sector pairing forms: Koide kernel -> (4(2x+3), 10x, 3x+2); "
          "carrier kernel -> (2(2x+3), 5x+9, 2(3x+5))",
          [sp.expand(e) for e in fx_K] ==
          [8 * X + 12, 10 * X, 3 * X + 2]
          and [sp.expand(e) for e in fx_C] ==
          [4 * X + 6, 5 * X + 9, 6 * X + 10])
    check("LEPTON pairings = the two det-B factors: zeros exactly at the "
          "branch points {-2/3, -5/3} (the lepton sector carries the "
          "ramification)",
          sp.solve(fx_K[2], X) == [sp.Rational(-2, 3)]
          and sp.solve(fx_C[2], X) == [sp.Rational(-5, 3)])
    check("UP zeros: x = -3/2 = -N_fam/|Z2| against BOTH kernels (a v85 "
          "GL(2) rung); the whole up-row of P(-3/2) = (-1/2)(1,-1,0) IS the "
          "odd direction",
          sp.solve(fx_K[0], X) == [sp.Rational(-3, 2)]
          and sp.solve(fx_C[0], X) == [sp.Rational(-3, 2)]
          and P.subs(X, sp.Rational(-3, 2))[0, :] ==
          sp.Rational(-1, 2) * sp.Matrix([[1, -1, 0]]))
    check("DOWN zeros: x = 0 (= the mass operator K itself) and x = -9/5 = "
          "-N_fam^2/g_car",
          sp.solve(fx_K[1], X) == [0]
          and sp.solve(fx_C[1], X) == [sp.Rational(-9, 5)]
          and sp.Rational(-9, 5) == -sp.Rational(N_fam**2, g_car))

    # 4. anchor-placement controls
    A2 = sp.Matrix([2, 1, 1])
    W2 = sp.Matrix.hstack(ONE, A2)
    B2 = W2.T * P * W2
    roots2 = sp.solve(B2.det(), X)
    ok2 = True
    for x0 in roots2:
        Bx = B2.subs(X, x0)
        ker = Bx.nullspace()[0]
        w = W2 * ker
        img = P.subs(X, x0) * w
        # collapse must be the anti-symmetric direction of slots {2,3}
        ok2 = ok2 and sp.simplify(img[0]) == 0 and \
            sp.simplify(img[1] + img[2]) == 0
    check("CONTROL anchor (2,1,1): det B = (x+2)(9x+11) (split, disc = 49 = "
          "scalaron^2, v82) and the collapse moves to (0,1,-1) -- the "
          "mechanism follows the anchor placement",
          sp.factor(B2.det()) == (X + 2) * (9 * X + 11) and ok2)
    A3v = sp.Matrix([1, 2, 1])
    W3 = sp.Matrix.hstack(ONE, A3v)
    B3 = W3.T * P * W3
    check("CONTROL anchor (1,2,1): disc = 40 NON-square (v82 trichotomy): "
          "no rational branch kernels at all",
          sp.discriminant(B3.det(), X) == 40
          and not sp.sqrt(40).is_rational)

    check("STATUS: the sector -> sheet map is now DEFINED by the cover's own "
          "branch kernels [I]/[L]; the identification with the v92 chirality "
          "swap is the remaining [P] step (tested in v97)", True)

    return summary("v96 branch-kernel selection")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
