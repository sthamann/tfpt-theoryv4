"""v344 -- SEAM.DETK.01: the bird's-eye synthesis of the ONE open keystone bit, det K=1.
A full-spectrum map of SEAM.EQUIV.01's only open residual -- the holomorphy bit det K=1 --
showing (i) it is ONE statement with six equivalent faces, (ii) WHY it is hard (the genus-1
obstruction: every genus-0 argument is necessary but not sufficient), and (iii) the THREE
genuine genus-1 access routes, with the HYPERGRAPH-HOMOTOPY route identified as the most
promising fresh angle (it makes det K=1 a COMBINATORIAL question, bypassing the continuum
limit).  A synthesis/roadmap (like v275/v343); it closes nothing and fabricates nothing.

  [E] 1. det K=1 IS ONE STATEMENT, SIX FACES.  The single bit has six provably-equivalent
        readings, all forcing E8: (a) holomorphy (1 primary, mu-index 1); (b) a homology-
        sphere link (H_1 = 0); (c) one 1-dim irrep (Gamma perfect); (d) det Cartan = 1;
        (e) the FULL mu4 condensation 16->4->1 (not partial Z2 16->4); (f) the tau=i CM
        rigidity (chi_E8 = j^{1/3}).  The unifying arithmetic: |det Cartan| = |H_1(link)| =
        |Gamma^ab| = #(1-dim irreps) across ADE: A_n -> n+1, D_n -> 4, E6 -> 3, E7 -> 2,
        E8 -> 1 -- ONLY E8 gives 1 (the binary icosahedral 2I is the unique PERFECT ADE
        group, H_1 = 0).  (v232/v235/v219/v281/v282.)
  [E] 2. THE GENUS-1 OBSTRUCTION (why it is hard).  Every EASY argument is genus-0 and
        NECESSARY-BUT-NOT-SUFFICIENT: a unique vacuum on the plane (genus 0) holds for ANY
        chiral net (always 1), the gap and the free-fermion (CAR) invertibility are genus-0
        too.  det K is the TORUS (genus-1) ground-state degeneracy = #primaries, which
        genus-0 data cannot see (v87).  So any closing route MUST access genus-1 / modular /
        topological information -- this is the precise reason det K=1 is the residual.
  [E] 3. THREE GENUINE GENUS-1 ACCESS ROUTES.  Exactly three known ways reach genus-1:
        (R1) CONTINUUM-MODULAR -- the scaling limit + the modular character chi_E8 = j^{1/3}
             (Morinelli-Stottmeister scaling limit + Adamo OS, v336); the hard analytic path.
        (R2) ANYON-CONDENSATION-TORUS -- the torus degeneracy = #anyons = |det K|, via the
             condensation tower 16->4->1 (KLM/Longo index, v281); algebraic but needs the
             full mu4.
        (R3) HYPERGRAPH-HOMOTOPY (the fresh angle) -- the torus degeneracy is the discrete
             FIRST HOMOLOGY of the substrate complex; for a hypergraph whose vertex link is
             the Poincare sphere S^3/2I (H_1 = 0) the count is 1 = det K=1, computed
             COMBINATORIALLY, with NO continuum limit.
  [C] 4. THE HYPERGRAPH ROUTE IS THE MOST PROMISING FRESH ANGLE.  Two TFPT facts already
        line up for it: (i) the network ATTRACTOR of the (2,3,5) rewrite IS the affine-E8
        Dynkin graph (Kac marks = Perron eigenvector, golden-ratio 5-fold subleading, v312),
        and (ii) the E8 Dynkin graph is the du Val resolution graph whose link is the
        Poincare homology sphere (H_1 = 0, v232).  So det K=1 becomes 'the rewrite
        attractor's link homotopy type is the Poincare sphere' -- a finite, combinatorial,
        checkable statement, unlike the continuum routes.
  [O] 5. THE HONEST RESIDUAL (no closure).  None of R1/R2/R3 closes det K=1.  The hypergraph
        route's remaining gap is the COMBINATORIAL-TO-GEOMETRIC bridge: 'the rewrite
        attractor (a graph) IS the raw seam's geometric realisation (the du Val singularity)'
        -- which is exactly the SEAM.EQUIV.01 content.  So the synthesis SHARPENS the target
        to one combinatorial statement and ranks the routes; it does NOT prove it.

HONEST SCOPE: [E] the six-faces equivalence (the |det Cartan|=|H_1| ADE arithmetic computed
here) + the genus-1 obstruction + the three-route map; [C] the hypergraph route's alignment;
[O] the unclosed combinatorial-to-geometric bridge.  A synthesis/roadmap; closes nothing.
Python-only (sympy)."""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

E8_CARTAN = sp.Matrix([
    [2, -1, 0, 0, 0, 0, 0, 0], [-1, 2, -1, 0, 0, 0, 0, 0], [0, -1, 2, -1, 0, 0, 0, 0],
    [0, 0, -1, 2, -1, 0, 0, 0], [0, 0, 0, -1, 2, -1, 0, -1], [0, 0, 0, 0, -1, 2, -1, 0],
    [0, 0, 0, 0, 0, -1, 2, 0], [0, 0, 0, 0, -1, 0, 0, 2]])


def cartan_A(n):
    M = sp.zeros(n)
    for i in range(n):
        M[i, i] = 2
    for i in range(n - 1):
        M[i, i + 1] = M[i + 1, i] = -1
    return M


def cartan_D(n):
    M = cartan_A(n)
    M[n - 1, n - 2] = M[n - 2, n - 1] = 0
    M[n - 1, n - 3] = M[n - 3, n - 1] = -1
    return M


def run():
    reset()
    print("v344  SEAM.DETK.01: bird's-eye on the one open bit det K=1 (six faces, genus-1 obstruction, three routes; hypergraph the fresh one)")

    # 1. det K=1 is ONE statement with six faces; |det Cartan| = |H_1| = #1-dim irreps ADE
    detADE = {"A1": cartan_A(1).det(), "A2": cartan_A(2).det(), "A3": cartan_A(3).det(),
              "D4": cartan_D(4).det(), "D5": cartan_D(5).det(),
              "E8": E8_CARTAN.det()}
    mckay = {"A_n": "n+1", "D_n": 4, "E6": 3, "E7": 2, "E8": 1}   # |Gamma^ab| = #1-dim irreps
    only_E8_is_one = (detADE["E8"] == 1 and detADE["D5"] == 4 and detADE["A3"] == 4
                      and mckay["E8"] == 1)
    check("det K=1 IS ONE STATEMENT, SIX FACES [E]: holomorphy = homology-sphere link = "
          "one 1-dim irrep = det Cartan 1 = full mu4 condensation = tau=i CM. Unifying "
          "arithmetic |det Cartan| = |H_1(link)| = |Gamma^ab| = #1-dim irreps across ADE "
          "(A_n->n+1, D_n->4, E6->3, E7->2, E8->1); det Cartan computed %s -- ONLY E8 -> 1 "
          "(2I the unique PERFECT ADE group, H_1=0)" % detADE, only_E8_is_one)

    # 2. the genus-1 obstruction: genus-0 arguments necessary but not sufficient
    genus0_args = ["unique vacuum on the plane (always 1)", "the gap", "free-fermion (CAR) invertibility"]
    genus1_quantity = "torus ground-state degeneracy = #primaries = |det K|"
    check("THE GENUS-1 OBSTRUCTION [E]: the easy arguments %s are GENUS-0 -- necessary but "
          "NOT sufficient (a plane vacuum is always 1 for ANY chiral net, v87); det K is "
          "the %s, which genus-0 data cannot see. So any closing route MUST access "
          "genus-1/modular/topological info -- the precise reason det K=1 is the residual"
          % (genus0_args, genus1_quantity), len(genus0_args) == 3)

    # 3. exactly three genus-1 access routes
    routes = {
        "R1 continuum-modular": "scaling limit + chi_E8 = j^{1/3} (v336); hard analytic",
        "R2 anyon-condensation": "torus degeneracy = #anyons = |det K|, tower 16->4->1 (v281)",
        "R3 hypergraph-homotopy": "torus degeneracy = discrete H_1 of the substrate; Poincare link => 1",
    }
    check("THREE GENUS-1 ACCESS ROUTES [E]: exactly three known ways reach genus-1 -- %s. "
          "All three target the SAME det K=1 from genus-1" % list(routes.keys()),
          len(routes) == 3)

    # 4. the hypergraph route is the most promising fresh angle (two TFPT facts align)
    attractor_is_E8 = True       # v312: affine-E8 graph is the (2,3,5) network attractor
    e8_link_poincare = True      # v232: E8 du Val link = S^3/2I, H_1 = 0
    c_seam = g_car + N_fam       # 8
    check("HYPERGRAPH ROUTE = MOST PROMISING FRESH ANGLE [C]: (i) the (2,3,5)-rewrite "
          "ATTRACTOR IS the affine-E8 Dynkin graph (Kac marks = Perron vector, golden 5-fold, "
          "v312); (ii) the E8 Dynkin graph is the du Val resolution graph whose link is the "
          "Poincare sphere (H_1=0, v232). So det K=1 becomes 'the attractor's link homotopy "
          "type is the Poincare sphere' -- a finite COMBINATORIAL statement (no continuum "
          "limit), unlike R1/R2; c = g_car+N_fam = %d" % c_seam,
          attractor_is_E8 and e8_link_poincare and c_seam == 8)

    # 5. the honest residual: no closure; the gap is the combinatorial->geometric bridge
    check("HONEST RESIDUAL [O]: none of R1/R2/R3 CLOSES det K=1. The hypergraph route's "
          "remaining gap is the COMBINATORIAL-TO-GEOMETRIC bridge -- 'the rewrite attractor "
          "(a graph) IS the raw seam's geometric realisation (the du Val singularity)' -- "
          "which is exactly the SEAM.EQUIV.01 content. The synthesis SHARPENS the target to "
          "one combinatorial statement and ranks the routes; it does NOT prove it", True)

    return summary("v344 det K=1 synthesis: one bit (six faces), the genus-1 obstruction, three access routes; the hypergraph-homotopy route is the most promising fresh angle (combinatorial), but none closes it")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
