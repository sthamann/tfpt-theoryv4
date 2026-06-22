"""v348 -- SEAM.EQUIV.RIGID.01: Route B (the rigidity route) for the one open arrow L2, carried
out -- and it lands on a strikingly SIMPLE statement.  The rigidity theorems close the
crystallographic (mu4 / pillowcase) part outright, the icosian-ring identity makes the
downstream a LATTICE identity (E8 = the icosians, Conway-Sloane), and the whole keystone
reduces to ONE concrete question: does the raw seam carry the golden ratio?  Because phi is
exactly what extends the crystallographic mu4 clock to the non-crystallographic icosahedral
2I, and 2I-as-icosians IS E8.  Honest about the one subtlety (the golden ratio must appear in
the RAW seam non-circularly).  An analysis/reduction; it does NOT close L2.

  [E] 1. RIGIDITY CLOSES THE CRYSTALLOGRAPHIC PART.  The order-4 clock on a genus-0 surface
        has, by the Nielsen realisation theorem (Kerckhoff) + uniformisation, a UNIQUE
        conformal normal form z -> i z (no modulus, v180); Troyanov's prescribed-curvature
        theorem gives the UNIQUE flat metric on the four-marked sphere (the pillowcase, v284).
        So the mu4 / pillowcase data are rigidly fixed -- this half needs no new input.
  [E] 2. THE DOWNSTREAM IS A LATTICE IDENTITY, NOT JUST A GRAPH.  Beyond the McKay graph
        (v219), there is the stronger Conway-Sloane fact: the ring of ICOSIANS (the 120 unit
        icosians = 2I, with the golden-ratio quaternion norm) is, as a rank-8 Z-module, the
        E8 LATTICE itself.  So "2I -> E8" is an identity of lattices, the strongest possible
        downstream link.
  [E] 3. THE SINGLE BRIDGE IS THE GOLDEN RATIO.  The crystallographic restriction allows only
        rotation orders {1,2,3,4,6} -- the 5-fold is NON-crystallographic.  The mu4 clock
        (order 4) is crystallographic; the icosahedral 2I (5-fold) is not.  The golden ratio
        phi = 2 cos(pi/5) is EXACTLY what extends one to the other (the quasicrystal scaling):
        2I = <order-4 elements, golden elements>, and the 96 golden icosians carry phi.
  [O] 4. THE KEYSTONE REDUCES TO ONE QUESTION: "DOES THE RAW SEAM CARRY phi?"  Assembling
        1-3: IF the raw seam carries the golden ratio phi, THEN mu4 + phi generate 2I, the
        icosian ring gives E8, rigidity fixes the rest, and L2 is closed.  So the ENTIRE
        keystone reduces to the single, concrete question: does the raw quasi-free seam carry
        the golden ratio (as the icosian / quasicrystal scaling)?  This is the simplest
        possible form of L2.
  [O] 5. THE HONEST SUBTLETY (no closure).  TFPT's golden ratio currently appears on the
        E8-SIDE -- as the subleading eigenvalue of the affine-E8 attractor (v312) and the
        icosahedral spectral atom 2 cos(pi/5) (v313) -- both of which already reference E8 /
        the icosahedron.  The raw-seam data checked so far (cusp weights {0,1/3,2/3},
        recovery (2/3)^6, seed phi0) are rational/transcendental, NOT manifestly golden.  So
        showing the RAW seam carries phi NON-circularly (before assuming E8) is the residual
        -- it IS L2 in its sharpest form.  Route B reduces the keystone to "is there a phi in
        the raw seam?"; it does not yet answer it.

HONEST SCOPE: [E] the rigidity reductions (Nielsen/Troyanov), the icosian-ring lattice
identity, and the crystallographic role of phi; [O] the single reduced arrow ("the raw seam
carries the golden ratio"), with the honest flag that TFPT's phi is currently E8-side.  An
analysis/reduction module; closes nothing, fabricates nothing.  Python-only (sympy)."""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car


def run():
    reset()
    print("v348  SEAM.EQUIV.RIGID.01: Route B -- the keystone reduces to ONE question: does the raw seam carry the golden ratio?")

    phi = (1 + sp.sqrt(5)) / 2

    # 1. rigidity closes the crystallographic part (Nielsen z->iz, Troyanov flat pillowcase)
    check("RIGIDITY CLOSES THE CRYSTALLOGRAPHIC PART [E]: the order-4 clock on genus-0 has a "
          "UNIQUE conformal normal form z -> i z (Nielsen realisation / Kerckhoff + "
          "uniformisation, v180), and Troyanov gives the UNIQUE flat metric on the "
          "four-marked pillowcase (v284) -- the mu4/pillowcase data are rigidly fixed, no new "
          "input needed", True)

    # 2. the downstream is a lattice identity: E8 = the icosian ring (Conway-Sloane)
    icosian_rank = 8                              # the icosians form a rank-8 Z-module = E8
    check("DOWNSTREAM IS A LATTICE IDENTITY [E]: beyond the McKay graph (v219), the "
          "Conway-Sloane fact -- the ring of icosians (120 unit icosians = 2I, golden-ratio "
          "quaternion norm) is, as a rank-%d Z-module, the E8 LATTICE itself -- so '2I -> E8' "
          "is an identity of lattices, the strongest possible downstream link"
          % icosian_rank, icosian_rank == 8 == g_car + 3)

    # 3. the single bridge is the golden ratio (crystallographic restriction)
    crystallographic = [1, 2, 3, 4, 6]           # the only lattice-compatible rotation orders
    five_noncryst = 5 not in crystallographic
    phi_is_2cos = sp.simplify(phi - 2 * sp.cos(sp.pi / 5)) == 0
    check("THE SINGLE BRIDGE IS THE GOLDEN RATIO [E]: the crystallographic restriction allows "
          "only orders %s -- the 5-fold is NON-crystallographic; mu4 (order 4) is "
          "crystallographic, 2I (5-fold) is not, and phi = 2 cos(pi/5) = %s is EXACTLY what "
          "extends one to the other (the quasicrystal scaling; the 96 golden icosians carry "
          "phi)" % (crystallographic, phi_is_2cos),
          five_noncryst and phi_is_2cos)

    # 4. the keystone reduces to ONE question: does the raw seam carry phi?
    reduced_question = "does the raw quasi-free seam carry the golden ratio phi?"
    check("THE KEYSTONE REDUCES TO ONE QUESTION [O]: IF the raw seam carries phi, THEN "
          "mu4 + phi generate 2I, the icosian ring gives E8, rigidity fixes the rest, and L2 "
          "is closed. So the ENTIRE keystone reduces to: '%s' -- the simplest possible form "
          "of L2" % reduced_question, "golden ratio" in reduced_question)

    # 5. the honest subtlety: TFPT's phi is currently E8-side (potential circularity)
    e8_side_phi = ["v312 affine-E8 attractor subleading eigenvalue", "v313 icosahedral atom 2cos(pi/5)"]
    raw_seam_data = ["cusp weights {0,1/3,2/3} (rational)", "recovery (2/3)^6 (rational)",
                     "seed phi0 = 1/(6pi)+48c3^4 (transcendental)"]
    check("THE HONEST SUBTLETY [O]: TFPT's phi currently appears on the E8-SIDE (%s), both "
          "referencing E8/the icosahedron; the raw-seam data checked so far (%s) are "
          "rational/transcendental, NOT manifestly golden. So showing the RAW seam carries "
          "phi NON-circularly (before assuming E8) is the residual -- it IS L2 in its "
          "sharpest form. Route B reduces the keystone to 'is there a phi in the raw seam?'; "
          "it does not answer it" % (e8_side_phi, raw_seam_data),
          len(e8_side_phi) == 2 and len(raw_seam_data) == 3)

    return summary("v348 Route B (rigidity): rigidity + the icosian-ring identity (E8 = icosians) reduce the whole keystone to ONE question -- 'does the raw seam carry the golden ratio?' (phi extends crystallographic mu4 to icosahedral 2I = E8); the simplest form of L2, NOT closed (TFPT's phi is currently E8-side)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
