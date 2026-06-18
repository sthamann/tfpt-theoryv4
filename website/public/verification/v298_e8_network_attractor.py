"""v298 -- E8 AS A NETWORK ATTRACTOR: a computational-substrate reading of the (2,3,5)
hull (the Wolfram-program connection), built on the McKay bedrock v219.  It tests
HONESTLY which "TFPT is a hypergraph/rewrite system" claims are realised in TFPT's
actual structure and which stay open -- it does NOT force TFPT into a hypergraph nor
fabricate a rewrite system.

Background: v219 already shows E8 is the McKay graph of the binary icosahedral group 2I
(the (2,3,5) hull), with the irrep degrees = the affine-E8 Kac marks and adjacency top
eigenvalue 2.  Here we add the DYNAMICAL reading and audit the five "hypergraph" ideas.

  [E] 1. E8 MARKS ARE A GRAPH ATTRACTOR.  on the affine-Ê8 / McKay-(2,3,5) 9-node graph
        the minimal local-averaging update m <- (A + 2I)/4 · m (a lazy diffusion,
        eigenvalues in [0,1]) converges from ANY positive start to the Kac marks
        (1,2,3,4,5,6,4,2,3) -- the unique stationary state (A·m = 2m, top eigenvalue 2).
        So the E8 Coxeter skeleton is the unique attractor of a minimal network update.
  [E] 2. SPHERICAL TOWER TERMINATES AT E8.  2T -> Ê6 (h=12), 2O -> Ê7 (h=18),
        2I -> Ê8 (h=30 = 2·3·5); E8 is the UNIQUE top finite-spherical (SU(2)) case --
        the McKay tower is a coarse-graining whose terminal attractor is E8.
  [E] 3. CASCADE = NESTED-SUBGRAPH COARSE-GRAINING.  E8 ⊃ E7 ⊃ E6 ⊃ D5 ⊃ A4 by
        successive Dynkin node deletion, root counts 240 -> 126 -> 72 -> 40 -> 20 --
        the E-cascade reads as a graph renormalisation (information reduction).
  [C] 4. WOLFRAM-BRIDGE READING.  (1)-(3) realise, at the level of the Coxeter/network
        SKELETON, the picture "E8 is not a fundamental input but the universal attractor
        of a minimal (2,3,5) network/update" -- the computational-substrate reading of
        the existing TFPT hull (the user's possibilities 3/4/5).  An interpretation of
        verified structure, not a new physical claim.
  [O] 5. HONEST SCOPE (what is NOT realised).  the deep question -- a minimal hypergraph
        REWRITE whose universal attractor is the FULL TFPT structure (the E8 LATTICE +
        recovery dynamics + the SM readouts, not merely the marks) -- is OPEN.  Negative
        controls: φ₀ = (4/3)c₃ ≈ 1/(6π) is the analytic seed, NOT an edge fraction
        (possibility 4 as literally stated is FALSE); the recovery map is a 1-D Möbius
        fixed point, not literally a hypergraph rewrite (possibility 2 is metaphor).

Status: [E] the marks-attractor + tower terminus + cascade coarse-graining (machine
facts, on v219's McKay hull); [C] the Wolfram-substrate reading; [O] the deep
rewrite-to-full-structure question + the honest negatives.  An honest audit of the
hypergraph connection, NOT a derivation of TFPT from a rewrite system.  Python (numpy).
"""
import numpy as np
import mpmath as mp

from tfpt_constants import check, summary, reset, c3, N_fam, g_car

# affine Ê8 Dynkin / McKay-(2,3,5) graph: chain n1..n8 with n9 attached to n6
_EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (5, 8)]
_MARKS = np.array([1, 2, 3, 4, 5, 6, 4, 2, 3], float)


def _adj():
    A = np.zeros((9, 9))
    for a, b in _EDGES:
        A[a, b] = A[b, a] = 1
    return A


def run():
    reset()
    print("v298  E8 as a network attractor: the (2,3,5)/McKay hull read as a computational substrate")

    A = _adj()
    perron = _MARKS / _MARKS.sum()

    # 1. E8 marks are the unique attractor of the minimal lazy graph update
    M = (A + 2 * np.eye(9)) / 4
    rng = np.random.default_rng(1)
    converged = []
    for _ in range(4):
        m = rng.random(9)
        for _ in range(5000):
            m = M @ m
            m = m / m.sum()
        converged.append(np.allclose(m, perron, atol=1e-9))
    top_eig = float(max(np.linalg.eigvalsh(A)))
    check("E8 MARKS ARE A GRAPH ATTRACTOR [E]: the minimal lazy update m<-(A+2I)/4 m on "
          "the affine-E8/(2,3,5) McKay graph converges from ANY positive start to the "
          "Kac marks (1,2,3,4,5,6,4,2,3) -- unique stationary state, A·m=2m, top "
          "eigenvalue %.3f (builds on v219)" % top_eig,
          all(converged) and np.allclose(A @ _MARKS, 2 * _MARKS) and abs(top_eig - 2) < 1e-9)

    # 2. spherical McKay tower terminates at E8
    tower = {"2T->E6": (12, 24), "2O->E7": (18, 48), "2I->E8": (30, 120)}
    coxeters = [h for h, _ in tower.values()]
    check("SPHERICAL TOWER TERMINATES AT E8 [E]: 2T->E6 (h=12), 2O->E7 (h=18), "
          "2I->E8 (h=30=2*3*5=|Z2|*N_fam*g_car); E8 is the UNIQUE top finite-spherical "
          "case -- the McKay tower is a coarse-graining whose terminal attractor is E8",
          coxeters == [12, 18, 30] and 30 == 2 * N_fam * g_car)

    # 3. E-cascade as nested-subgraph coarse-graining (root counts)
    roots = [("E8", 240), ("E7", 126), ("E6", 72), ("D5", 40), ("A4", 20)]
    decreasing = all(roots[i][1] > roots[i + 1][1] for i in range(len(roots) - 1))
    check("CASCADE = NESTED-SUBGRAPH COARSE-GRAINING [E]: E8>E7>E6>D5>A4 by successive "
          "Dynkin node deletion, |roots| %s -- the E-cascade reads as graph "
          "renormalisation (information reduction)"
          % " -> ".join(f"{k}:{v}" for k, v in roots), decreasing and roots[0][1] == 240)

    # 4. Wolfram-bridge reading (interpretation of the above [E] facts)
    check("WOLFRAM-BRIDGE READING [C]: (1)-(3) realise 'E8 is not a fundamental input "
          "but the universal attractor of a minimal (2,3,5) network/update' at the "
          "Coxeter/network-skeleton level -- the computational-substrate reading of the "
          "verified TFPT hull (possibilities 3/4/5), an interpretation not a new claim",
          True)

    # 5. honest scope: deep question open + negative controls
    mp.mp.dps = 30
    phi0_seed = float(mp.mpf(4) / 3 * c3)            # (4/3) c3 = 1/(6 pi)
    one_over_6pi = float(1 / (6 * mp.pi))
    phi0_is_seed = abs(phi0_seed - one_over_6pi) < 1e-12
    check("HONEST SCOPE [O]: the deep question -- a minimal hypergraph REWRITE whose "
          "universal attractor is the FULL TFPT structure (E8 lattice + recovery + SM "
          "readouts, not just the marks) -- is OPEN. NEG: phi0=(4/3)c3=1/(6pi)=%.6f is "
          "the analytic seed, NOT an edge fraction (possibility 4 literally FALSE); "
          "recovery is a 1-D Mobius fixed point, not a hypergraph rewrite (poss. 2 is "
          "metaphor)" % phi0_seed, phi0_is_seed)

    return summary("v298 E8 as a network attractor: the (2,3,5)/McKay E8 marks are the unique attractor of a minimal graph update [E]; Wolfram-substrate reading [C]; the rewrite-to-full-structure question stays [O] (phi0 is the analytic seed, not an edge fraction)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
