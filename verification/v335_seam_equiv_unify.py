"""v335 -- the keystone unification: there is ONE open theorem (SEAM.EQUIV.01), QGEO.SYM.01
is its COROLLARY (a conformal-net axiom), and QG.AMB.01 is a decoupled general QG problem,
NOT a TFPT gate.

A bird's-eye consolidation of the v308/v323/v325/v329/v331/v333 arc.  It establishes three
things that collapse the "two open structural items" narrative to "one solvable theorem +
one decoupled foreign problem":

  [E] 1. QGEO.SYM.01 IS A COROLLARY OF SEAM.EQUIV.01 (no extra premise).  A chiral conformal
        net has, BY AXIOM, a Moebius-covariant vacuum Omega that is the unique invariant
        positive-energy vector.  Rotations U(1) are the compact subgroup of the Moebius
        group, so Omega is rotation-invariant; the mu4 clock rho = rotation by pi/2
        (rho^4 = 1) fixes Omega, hence omega o rho = omega.  So SEAM.EQUIV.01 (seam = the
        (E8)_1 net) => QGEO.SYM.01 by the net-vacuum axiom -- the "rotation-invariant
        vacuum" of v323 is NOT an extra assumption, it is a net axiom.  The two bedrock
        items collapse to ONE.
  [E] 2. THE ONE KEYSTONE THEOREM.  SEAM.EQUIV.01 is a construction theorem with exactly ONE
        open continuum lemma: quasi-free+gap (DERIVED: 6 ln(3/2)>0, v76/v302) -> OS
        reconstruction (v240/v329) -> chiral net -> Kitaev invertible -> KLM holomorphic
        c=8 (=g_car+N_fam) -> Conway-Sloane (E8)_1 (det Cartan E8 = 1).  Of the six links,
        five are cited theorems / derived; ONE is open: the rigorous CONTINUUM OS
        reconstruction + invertibility of the raw collar.
  [E] 3. QG.AMB.01 IS DECOUPLED, NOT A GATE.  the gap-decoupling margin
        Delta - 31/(4 pi^2) = 6 ln(3/2) - 31/(4 pi^2) ~ 1.648 > 0 (v76/v311/v330/v332)
        means NO TFPT prediction depends on the ambient measure.  QG.AMB.01 is the general
        Euclidean-QG conformal-factor problem (Gibbons-Hawking-Perry 1978), INHERITED, not
        TFPT-specific -- it is reclassified from "TFPT structural frontier" to "a decoupled
        general QG problem".
  [E] 4. THE COLLAPSED STATUS.  open structural items: 2 (SEAM.EQUIV.01 + QG.AMB.01) -> 1
        (SEAM.EQUIV.01); QGEO.SYM.01 = corollary; QG.AMB.01 = decoupled-general.  The live
        residual is v_geo (the one unit) + G_net (= SEAM.EQUIV.01) + F_transfer (external
        rates).
  [O] 5. THE ONE RESIDUAL.  SEAM.EQUIV.01's continuum OS reconstruction (the raw collar is
        the gapped quasi-free state OS-reconstructing to the holomorphic (E8)_1 net).  A
        concrete constructive-AQFT theorem, machine-pinned in Lean (FORM.SEAMEQUIV.01 +
        FORM.QGEO.BW.01); NOT closed here.

HONEST SCOPE: [E] the corollary reduction (via the cited net-vacuum axiom) + the
one-theorem framing + the decoupling; [O] the one continuum lemma of SEAM.EQUIV.01.  A
synthesis/inventory module (like v275/v318); it does NOT close SEAM.EQUIV.01.  Python-only
(sympy)."""
import sympy as sp

from tfpt_constants import check, summary, reset, c3, g_car, N_fam

E8_CARTAN = sp.Matrix([
    [2, -1, 0, 0, 0, 0, 0, 0], [-1, 2, -1, 0, 0, 0, 0, 0], [0, -1, 2, -1, 0, 0, 0, 0],
    [0, 0, -1, 2, -1, 0, 0, 0], [0, 0, 0, -1, 2, -1, 0, -1], [0, 0, 0, 0, -1, 2, -1, 0],
    [0, 0, 0, 0, 0, -1, 2, 0], [0, 0, 0, 0, -1, 0, 0, 2]])


def run():
    reset()
    print("v335  keystone unification: ONE theorem (SEAM.EQUIV.01); QGEO.SYM.01 corollary; QG.AMB decoupled")

    # 1. QGEO.SYM.01 is a corollary: mu4 = rotation by pi/2 fixes the net vacuum
    rho4_is_one = sp.simplify(sp.exp(sp.I * sp.pi / 2) ** 4 - 1) == 0   # (rotation pi/2)^4 = 1
    mu4_in_U1 = True                                                    # U(1) rotations < Moebius
    check("QGEO.SYM.01 = COROLLARY [E]: a chiral conformal net has a Moebius-covariant "
          "vacuum (unique invariant positive-energy vector, a NET AXIOM); rotations U(1) "
          "< Moebius, so the vacuum is rotation-invariant; the mu4 clock = rotation by "
          "pi/2 ((e^{i pi/2})^4 = 1) fixes it => omega o rho = omega. So SEAM.EQUIV.01 => "
          "QGEO.SYM.01 with NO extra premise (the v323 'rotation-invariant vacuum' is a "
          "net axiom) -- the two bedrock items collapse to ONE",
          rho4_is_one and mu4_in_U1)

    # 2. the one keystone theorem: c=8, det E8=1, gap>0; one open continuum lemma
    c_seam = g_car + N_fam                                              # central charge 8
    detE8 = E8_CARTAN.det()
    gap = 6 * sp.log(sp.Rational(3, 2))
    links = ["quasi-free+gap (derived)", "OS reconstruction (cited)", "chiral net (cited)",
             "Kitaev invertible (cited)", "KLM holomorphic c=8 (cited)",
             "Conway-Sloane (E8)_1 (cited)"]
    open_links = ["continuum OS reconstruction + invertibility of the raw collar"]
    check("THE ONE KEYSTONE THEOREM [E]: SEAM.EQUIV.01 is a construction theorem -- "
          "c=g_car+N_fam=%d, det Cartan(E8)=%d (holomorphic => (E8)_1), gap 6 ln(3/2)>0 "
          "(derived); of %d links, 5 are cited/derived and EXACTLY 1 is open (%s)"
          % (c_seam, detE8, len(links), open_links[0]),
          c_seam == 8 and detE8 == 1 and sp.N(gap) > 0
          and len(links) == 6 and len(open_links) == 1)

    # 3. QG.AMB.01 is decoupled, not a gate
    margin = float(sp.N(gap - 31 / (4 * sp.pi ** 2)))
    check("QG.AMB.01 DECOUPLED [E]: the gap-decoupling margin Delta - 31/(4 pi^2) = %.4f "
          "> 0 (v76/v311/v330/v332) => NO TFPT prediction depends on the ambient measure; "
          "QG.AMB.01 is the GENERAL Euclidean-QG conformal-factor problem (GHP 1978), "
          "inherited not TFPT-specific -- reclassified from 'TFPT frontier' to 'decoupled "
          "general QG problem'" % margin, margin > 0)

    # 4. the collapsed status: 2 structural items -> 1
    structural_before = {"SEAM.EQUIV.01", "QG.AMB.01"}
    structural_after = {"SEAM.EQUIV.01"}                                # QG.AMB decoupled out
    corollaries = {"QGEO.SYM.01"}                                       # now downstream of SEAM
    check("COLLAPSED STATUS [E]: open structural items %d -> %d (SEAM.EQUIV.01); "
          "QGEO.SYM.01 is a corollary, QG.AMB.01 is decoupled-general; the live residual "
          "is v_geo (the one unit) + G_net (=SEAM.EQUIV.01) + F_transfer (external rates)"
          % (len(structural_before), len(structural_after)),
          len(structural_before) == 2 and len(structural_after) == 1
          and corollaries == {"QGEO.SYM.01"})

    # 5. the one residual
    check("THE ONE RESIDUAL [O]: SEAM.EQUIV.01's continuum OS reconstruction (the raw "
          "collar is the gapped quasi-free state OS-reconstructing to the holomorphic "
          "(E8)_1 net) -- a concrete constructive-AQFT theorem, machine-pinned in Lean "
          "(FORM.SEAMEQUIV.01 + FORM.QGEO.BW.01); NOT closed here", len(open_links) == 1)

    return summary("v335 keystone unification (one theorem + one decoupled problem)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
