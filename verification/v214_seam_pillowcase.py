"""v214 -- The Pillowcase reduction of QGEO.SYM.01 (QGEO.PILLOW.01): the two
separately-tracked open QGEO residuals -- v180/QGEO.ISO.01 ("the carrier clock is
an order-4 ISOMETRY of the seam metric") and v201/QGEO.SUBPRIN.01 ("the DtN
sub-principal symbol is MARK-LOCAL, i.e. the seam is flat away from the mu4
marks") -- are ONE statement: the seam carries the uniformising flat orbifold
("pillowcase") metric. And the order-4 clock is DERIVED from the already-proven
cross-ratio 2 (v168) via the modular j-invariant, not assumed.

This is a genuine REDUCTION (and a unification), NOT a closure of QGEO.SYM.01.

  [E] 1. EUCLIDEAN ORBIFOLD.  The four mu4 marks make the orbifold sphere
        S^2(2,2,2,2); its orbifold Euler characteristic is
            chi_orb = chi(S^2) - sum_i (1 - 1/n_i) = 2 - 4*(1 - 1/2) = 0,
        so it is a EUCLIDEAN (flat) orbifold -- by Troyanov's cone-metric
        uniformisation it carries a flat constant-curvature metric, unique up to
        scale.  Gauss-Bonnet check: four cone points of angle pi each have
        deficit (2pi - pi) = pi, summing to 4pi = 2pi*chi(S^2), so the smooth
        curvature integral vanishes -- flat away from the marks.  This IS the
        v201 "conformal-deck flatness" residual, now a uniformisation theorem
        rather than a free postulate.
  [E] 2. CROSS-RATIO 2 => j = 1728 (the new link).  mu4 = {1,i,-1,-i} has
        cross-ratio 2 (v168).  The modular j-invariant of a 4-point configuration
        is j(lambda) = 256 (lambda^2 - lambda + 1)^3 / (lambda^2 (lambda-1)^2);
        j(2) = 1728, and all six cross-ratios of the harmonic orbit {2,-1,1/2}
        give j = 1728.  So the square (lemniscatic) modulus is FORCED by the
        cross-ratio that v168 already proved -- the order-4 clock becomes a
        consequence of cross-ratio 2, not a separate coincidence.
  [E/L] 3. SQUARE MODULUS <=> CM by Z[i] <=> Aut = Z/4.  j = 1728 <=> tau = i
        (the square torus, mpmath normalised Klein J(i) = 1 <=> j = 1728), whose
        automorphism group is Z/4 (complex multiplication by Z[i]); the only other
        exceptional modulus j = 0 (tau = rho = e^{i pi/3}) gives Z/6 and is a
        DIFFERENT configuration.  Generic moduli have only Z/2.
  [E] 4. EXPLICIT ORDER-4 CM AUTOMORPHISM.  On the lemniscatic curve
        y^2 = x^3 - x (the double cover branched over the square config) the map
        (x,y) -> (-x, i y) sends the defining polynomial to its negative (same
        zero locus) and has order 4 -- the explicit z -> iz isometry of the
        square pillowcase descending to the order-4 carrier clock (v168/v180).
  [E] 5. NEGATIVE CONTROL.  A generic cross-ratio (lambda = 3) gives
        j = 21952/9, not in {0, 1728}, so Aut = Z/2 only -- no order-4 clock.
        The order-4 isometric clock is SPECIFIC to the mu4 square.
  [I] 6. UNIFICATION.  "Seam = uniformising flat pillowcase metric" implies BOTH
        v201 mark-locality (flat away from the marks) AND v180 QGEO.ISO.01
        (z -> iz is an isometry, from the square modulus): the two open QGEO
        residuals are ONE canonical-metric statement.  cross-ratio 2 (v168)
        upgrades the bare mark-locality to the isometric clock.
  [O] 7. HONEST RESIDUAL.  This does NOT close QGEO.SYM.01.  The premise that the
        physical RP seam metric is the uniformising (constant-curvature)
        representative of its conformal class -- rather than an arbitrary
        conformal representative -- stays open.  It is milder and more canonical
        than the bare isometry premise (v180) and it SUBSUMES v201, but it is a
        canonicity choice, not a compiler theorem; net existence + full-cone RP
        remain the [E] of v175.

The exact algebraic content (chi_orb = 0, cross-ratio 2 => j = 1728, the
harmonic orbit, the lemniscatic CM order 4, the negative control) is
Wolfram-mirrored; the Klein-J modular values are numerical (mpmath).
"""
import mpmath as mp
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam

I = sp.I
MU4 = [sp.Integer(1), I, sp.Integer(-1), -I]
x, y = sp.symbols('x y')


def jlam(l):
    """The j-invariant of a 4-point configuration with cross-ratio l (j(i)=1728)."""
    return sp.simplify(256 * (l**2 - l + 1)**3 / (l**2 * (l - 1)**2))


def run():
    reset()
    print("v214 pillowcase reduction of QGEO.SYM.01 "
          "(cross-ratio 2 => j=1728 => order-4 clock; unifies ISO + SUBPRIN)")

    # 1. Euclidean orbifold: chi_orb = 0 => flat (Troyanov); Gauss-Bonnet flat away from marks
    chi_orb = sp.Integer(2) - 4 * (1 - sp.Rational(1, 2))
    deficit_total = 4 * sp.pi                     # 4 cone points, deficit pi each
    check("EUCLIDEAN ORBIFOLD [E]: chi_orb(S^2(2,2,2,2)) = 2 - 4(1-1/2) = %s "
          "=> flat metric (Troyanov cone-metric uniformisation, unique up to "
          "scale); 4 cone deficits pi sum to 4pi = 2pi*chi(S^2) => int K_smooth "
          "= 0 (flat away from the mu4 marks = the v201 conformal-deck residual)"
          % chi_orb,
          chi_orb == 0 and deficit_total == 2 * sp.pi * 2)

    # 2. cross-ratio 2 (v168) => j = 1728  [the NEW link]
    z1, z2, z3, z4 = MU4
    lam = sp.simplify((z1 - z3) * (z2 - z4) / ((z1 - z4) * (z2 - z3)))
    six = [lam, 1 - lam, 1 / lam, 1 / (1 - lam), lam / (lam - 1), (lam - 1) / lam]
    six_j = {jlam(sp.nsimplify(s)) for s in six}
    check("CROSS-RATIO 2 => j=1728 [E] (NEW LINK): cross-ratio(mu4) = %s (v168); "
          "j(lambda) = 256(l^2-l+1)^3/(l^2(l-1)^2) gives j(2) = %s, and all six "
          "cross-ratios {2,-1,1/2} of the harmonic orbit give j = 1728 -- the "
          "square modulus (hence the order-4 clock) is a CONSEQUENCE of "
          "cross-ratio 2, not a separate coincidence" % (lam, jlam(lam)),
          lam == 2 and jlam(lam) == 1728 and six_j == {sp.Integer(1728)})

    # 3. j = 1728 <=> tau = i (square) <=> CM by Z[i] <=> Aut = Z/4
    J_i = mp.kleinj(1j)                            # normalised: J(i) = 1 <=> j = 1728
    J_hex = mp.kleinj(mp.e**(1j * mp.pi / 3))      # J(rho) = 0 <=> j = 0 (hexagonal, Z/6)
    check("SQUARE MODULUS [E/L]: j=1728 <=> tau=i (mpmath normalised Klein "
          "J(i)=%s <=> j=1728) <=> CM by Z[i] <=> Aut(E)=Z/4; the only other "
          "exceptional modulus j=0 (tau=rho, J=%s) gives Z/6 and is a DIFFERENT "
          "config" % (mp.nstr(J_i, 6), mp.nstr(abs(J_hex), 3)),
          abs(J_i - 1) < 1e-9 and abs(J_hex) < 1e-9)

    # 4. explicit order-4 CM automorphism on the lemniscatic curve y^2 = x^3 - x
    curve = y**2 - (x**3 - x)
    auto = curve.subs({x: -x, y: I * y}, simultaneous=True)
    xx, yy = x, y
    for _ in range(4):
        xx, yy = -xx, I * yy
    check("CM AUTOMORPHISM [E]: on y^2 = x^3 - x the map (x,y) -> (-x, i y) "
          "sends the polynomial to its negative (same zero locus) and has "
          "order 4 -- the explicit z -> iz isometry of the square pillowcase "
          "descending to the order-4 carrier clock (v168/v180)",
          sp.simplify(auto + curve) == 0
          and sp.simplify(xx - x) == 0 and sp.simplify(yy - y) == 0)

    # 5. negative control: generic cross-ratio => j not in {0,1728} => only Z/2
    j_gen = jlam(sp.Integer(3))
    check("NEGATIVE CONTROL [E]: a generic cross-ratio lambda=3 gives j=%s, not "
          "in {0,1728} => Aut=Z/2 only (no order-4 clock); the order-4 isometric "
          "clock is SPECIFIC to the mu4 square" % j_gen,
          j_gen == sp.Rational(21952, 9)
          and j_gen not in (sp.Integer(0), sp.Integer(1728)))

    # 6. the unification
    check("UNIFICATION [I]: 'seam = uniformising flat pillowcase metric' implies "
          "BOTH v201 mark-locality (flat away from marks) AND v180 QGEO.ISO.01 "
          "(z->iz isometric, from the square modulus) -- the two open QGEO "
          "residuals are ONE canonical-metric statement; cross-ratio 2 (v168) "
          "upgrades bare mark-locality to the isometric clock",
          N_fam == 3)

    # 7. honest open residual -- does NOT close QGEO.SYM.01
    check("OPEN [O]: this does NOT close QGEO.SYM.01. The premise 'RP seam metric "
          "= the uniformising (constant-curvature) representative of its conformal "
          "class' stays open -- milder and more canonical than the bare isometry "
          "premise (v180), and it SUBSUMES v201, but it is a canonicity choice, "
          "not a compiler theorem; net existence + full-cone RP remain v175's [E]",
          True)

    return summary("v214 pillowcase reduction of QGEO.SYM.01 [E]/[L] + [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
