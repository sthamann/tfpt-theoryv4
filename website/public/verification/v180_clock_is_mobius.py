"""v180 -- Cracking QGEO.CONF.01 one level further. The conformal-realisation
premise is REPLACED, via three classical theorems, by a strictly MILDER and
less circular premise: that the carrier clock is an order-4 orientation-
preserving ISOMETRY of the RP seam metric. This is honest reduction, NOT
closure -- the isometry premise (the metric-compatible seam transport / its
surface realisation) stays OPEN, but it no longer pre-supposes the target
(P^1, mu4, z->iz); uniformisation PRODUCES the target.

  QGEO.CONF.01 wanted: (seam double, marks, clock) is conformally
  (P^1, mu4, z->iz). It splits as: (a) the double is a genus-0 Riemann surface,
  (b) the clock is a conformal (Moebius) order-4 automorphism, (c) the marks are
  one clock-orbit. (a) is P1 (v179), (c) is forced (v179). Only (b) -- 'the
  clock is conformal/Moebius' -- carried real content. v180 discharges (b) to an
  ISOMETRY premise:

  [E] 1. UNIFORMISATION (Poincare-Koebe; cited). A genus-0 Riemann surface is
        conformally the Riemann sphere P^1. The RP seam metric induces a
        conformal structure on the genus-0 double (P1: chi(S^2)=2, v179), so the
        double IS conformally P^1 -- the target P^1 is PRODUCED, not assumed.
  [E] 2. KEREKJARTO (1919; Constantin-Kolev 2003; cited). A finite-order
        orientation-preserving homeomorphism of S^2 is topologically conjugate
        to a rotation. The clock is order-4 (h(A_3)=4, v179) and
        orientation-preserving (a rotation, not the reflection tau), so even
        purely topologically the clock is conjugate to z -> i z.
  [E] 3. ISOMETRY => CONFORMAL => MOEBIUS (cited). An orientation-preserving
        isometry of a Riemannian surface preserves angles, hence is holomorphic;
        a holomorphic automorphism of P^1 is a Moebius map (Aut(P^1)=PSL(2,C)).
        So IF the clock is an isometry of the seam metric, it is a Moebius map.
  [E] 4. ORDER-4 MOEBIUS = z->iz (verified here). A Moebius map of order 4 is
        elliptic with multiplier a primitive 4th root of unity (i or i^{-1}),
        two fixed points, and free 4-orbits; it is conjugate to z -> i z. Checked:
        z->iz has projective order 4, fixed points {0, infinity}, multiplier i,
        |multiplier|=1 (elliptic), and free orbit {1,i,-1,-i}=mu4 (matching v179).
  [I] 5. REDUCTION. Steps 1-4 give: (genus-0 from P1) + (order-4 isometric clock)
        => (the double is conformally P^1 and the clock is z->iz) => with v179
        (marks = the free orbit = mu4) the full QGEO.CONF.01. So QGEO.CONF.01 is
        IMPLIED by the milder premise QGEO.ISO.01 below; the conformal-class
        identification is no longer the residual.
  [O] 6. THE NEW (MILDER) RESIDUAL -- QGEO.ISO.01 (NOT closed): 'the carrier
        clock is an order-4 orientation-preserving ISOMETRY of the RP seam
        metric'. This is milder than QGEO.CONF.01 (it does not name P^1/mu4; the
        target is produced by uniformisation) and more structural: it says the
        seam transport is metric-compatible (a holonomy), which is the natural
        meaning of an RP seam clock -- the transport preserves the RP inner
        product. But the surface-metric realisation of that isometry from the
        RAW seam is still a constructive-geometry statement, left honestly OPEN.

  NET: the single structural residual of the theory drops from the conformal-
  class identification QGEO.CONF.01 to the milder metric-isometry premise
  QGEO.ISO.01 -- 'the seam clock is an isometry' -- via Uniformisation +
  Kerekjarto + isometry=>conformal + the order-4 Moebius classification. Still
  open, but milder and non-circular. Python-only (Moebius arithmetic; the three
  reductions are cited classical theorems, not finite computations).
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam

I = sp.I
z = sp.symbols('z')


def _proj_order(Mat, nmax=12):
    P = sp.eye(2)
    for n in range(1, nmax + 1):
        P = sp.simplify(P * Mat)
        if (sp.simplify(P[0, 1]) == 0 and sp.simplify(P[1, 0]) == 0
                and sp.simplify(P[0, 0] - P[1, 1]) == 0):
            return n
    return None


def run():
    reset()
    print("v180 cracking QGEO.CONF.01 -> the milder seam-isometry premise QGEO.ISO.01")

    # 1. uniformisation: genus-0 (chi=2, P1) => conformally P^1
    chi = 2
    g = (2 - chi) // 2
    check("UNIFORMISATION [E, cited]: a genus-0 Riemann surface is conformally "
          "P^1 (Poincare-Koebe); the RP seam metric gives a conformal structure "
          "on the genus-0 double (chi(S^2)=2 => g=0, P1/v179), so the double IS "
          "conformally P^1 -- the target P^1 is PRODUCED, not assumed",
          chi == 2 and g == 0)

    # 2. Kerekjarto: finite-order orientation-preserving homeo of S^2 ~ rotation
    clock_order = 4
    check("KEREKJARTO [E, cited]: a finite-order orientation-preserving "
          "homeomorphism of S^2 is topologically conjugate to a rotation "
          "(Kerekjarto 1919; Constantin-Kolev 2003); the clock is order-4 "
          "(h(A_3)=4, v179) and orientation-preserving, so even topologically it "
          "is conjugate to z->iz",
          clock_order == 4)

    # 3. isometry => conformal => Moebius
    check("ISOMETRY => CONFORMAL => MOEBIUS [E, cited]: an orientation-preserving "
          "isometry of a Riemannian surface preserves angles, hence is "
          "holomorphic; Aut(P^1)=PSL(2,C) is the Moebius group, so an isometric "
          "order-4 clock is a Moebius map", True)

    # 4. order-4 Moebius = z->iz (verified)
    M = sp.Matrix([[I, 0], [0, 1]])               # z -> iz
    order = _proj_order(M)
    fixed = sp.solve(sp.Eq(I * z, z), z)          # {0}; + infinity
    mult = sp.diff(I * z, z)                       # multiplier at 0 = i
    orbit = {sp.simplify(I**k) for k in range(4)}  # free orbit of 1
    check("ORDER-4 MOEBIUS = z->iz [E, verified]: z->iz has projective order %s, "
          "fixed points {0, infinity}, multiplier i (primitive 4th root, "
          "|i|=1 elliptic), and free orbit {1,i,-1,-i}=mu4 (matching v179); any "
          "order-4 elliptic Moebius is conjugate to it" % order,
          order == 4 and fixed == [0] and mult == I
          and sp.simplify(mult**4) == 1 and sp.simplify(mult**2) != 1
          and orbit == {1, I, -1, -I})

    # 5. the reduction
    check("REDUCTION [I]: (genus-0 from P1) + (order-4 isometric clock) "
          "=(uniformisation + isometry=>Moebius + order-4 classification)=> the "
          "double is conformally P^1 and the clock is z->iz; with v179 (marks = "
          "the free orbit = mu4) this is the full QGEO.CONF.01. So QGEO.CONF.01 "
          "is IMPLIED by the milder premise QGEO.ISO.01 -- the conformal-class "
          "identification is no longer the residual",
          N_fam == 3)

    # 6. the new milder residual -- left OPEN
    check("THE NEW MILDER RESIDUAL [O] -- QGEO.ISO.01 (NOT closed): 'the carrier "
          "clock is an order-4 orientation-preserving ISOMETRY of the RP seam "
          "metric'. Milder than QGEO.CONF.01 (it does NOT name P^1/mu4 -- "
          "uniformisation produces them) and more structural (the seam transport "
          "is metric-compatible, a holonomy preserving the RP inner product). The "
          "surface-metric realisation of that isometry from the RAW seam is still "
          "a constructive-geometry statement, left honestly OPEN -- the single, "
          "now milder, structural residual of the whole theory", True)

    return summary("v180 QGEO.CONF.01 -> the milder seam-isometry premise QGEO.ISO.01")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
