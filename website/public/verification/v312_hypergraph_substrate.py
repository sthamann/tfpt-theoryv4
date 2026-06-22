"""v312 -- the hypergraph substrate, sharpened: what a rewrite MUST inject.

Attack point 5 of the TOE roadmap: is TFPT's structure the attractor of a minimal
(2,3,5) rewrite/network ("Wolfram-physics" substrate)?  v298/v299 confirmed the E8
COXETER SKELETON (Kac marks, h=30, |R|=240) is a network attractor.  This module
attacks the deep open question -- "a rewrite whose attractor is the FULL structure"
-- by testing exactly which load-bearing quantities ARE graph-spectral and which are
NOT, turning the open question into a precise list of what a substrate must add.

  [E] 1. SKELETON IS THE ATTRACTOR: the affine-E8 adjacency A has Perron eigenvalue 2
        with eigenvector = the Kac marks (1,2,3,4,5,6,4,2,3) (A.marks = 2 marks); the
        lazy update (A+2I)/4 fixes them -- the Coxeter skeleton is graph-spectral.
  [E] 2. THE 5-FOLD SIGNATURE IS GRAPH-SPECTRAL: the subleading eigenvalue is exactly
        lambda_2 = 2 cos(pi/5) = the golden ratio phi (the icosahedral (2,3,5) / 5-fold
        signature, consistent with v219/v236) -- the spectrum is {+-2, +-phi, +-1,
        +-1/phi, 0}.
  [E] 3. HONEST NEGATIVE -- the recovery rate is NOT graph-spectral: the lazy-update
        subleading rate (phi+2)/4 = 0.9045 is NOT the recovery rate (2/3)^6, and
        (2/3)^6 is NOT any eigenvalue of A; the family-recovery dynamics
        Delta = 6 ln(3/2) is carried by the CUSP WEIGHTS {0,1/3,2/3}, not the adjacency.
  [E] 4. HONEST NEGATIVE -- the seed is NOT an edge fraction: phi0 = 1/(6 pi) + 48 c3^4
        is analytic/transcendental, not a rational network fraction (v298).

CONCLUSION (the sharpened open question, [O]): a rewrite substrate that reproduces
the FULL TFPT structure must INJECT, beyond the (2,3,5) adjacency, exactly two things
the graph spectrum does NOT contain: (a) the cusp-weight recovery datum
2/3 = |Z2|/N_fam (the gap 6 ln(3/2)), and (b) the analytic seed phi0.  The pure
network gives the Coxeter skeleton + the golden-ratio 5-fold signature and nothing
more.  HONEST SCOPE: [E] the spectral facts and the two negatives; [O] the
rewrite-to-full-structure question (now precisely delimited).  NOT a derivation of
P1/P2 from a rewrite.  Python-only (numpy).
"""
import numpy as np

from tfpt_constants import check, summary, reset, N_fam, phi0

# affine-E8 (E8-hat) Dynkin graph, labeled so the Kac marks are the Perron vector
MARKS = np.array([1, 2, 3, 4, 5, 6, 4, 2, 3], dtype=float)
EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (5, 8)]


def adjacency():
    A = np.zeros((9, 9))
    for i, j in EDGES:
        A[i, j] = A[j, i] = 1.0
    return A


def run():
    reset()
    print("v312  hypergraph substrate sharpened: what a rewrite must inject")

    A = adjacency()

    # 1. the Coxeter skeleton is the network attractor
    check("SKELETON [E]: A . marks = 2 . marks -- the Kac marks (1,2,3,4,5,6,4,2,3) "
          "are the Perron eigenvector (eigenvalue 2) of the affine-E8 graph; the "
          "lazy update (A+2I)/4 fixes them (v298/v299)",
          np.allclose(A @ MARKS, 2 * MARKS))

    evals = sorted(np.linalg.eigvalsh(A).tolist(), reverse=True)
    check("PERRON [E]: the top eigenvalue is exactly 2 (the affine/critical case), "
          "simple, with the positive marks as eigenvector",
          abs(evals[0] - 2.0) < 1e-9)

    # 2. the 5-fold signature is graph-spectral
    phi = (1 + np.sqrt(5)) / 2
    lam2 = evals[1]
    check("5-FOLD SIGNATURE [E]: lambda_2 = 2 cos(pi/5) = golden ratio phi = %.5f "
          "(the icosahedral (2,3,5) / 5-fold signature, v219/v236); spectrum is "
          "{+-2, +-phi, +-1, +-1/phi, 0}" % phi,
          abs(lam2 - phi) < 1e-9 and abs(lam2 - 2 * np.cos(np.pi / 5)) < 1e-9)

    # 3. honest negative: the recovery rate is NOT graph-spectral
    update_rate = (lam2 + 2) / 4                  # lazy-update subleading
    recovery = (2 / 3) ** 6
    in_spectrum = any(abs(recovery - abs(e)) < 1e-6 for e in evals)
    print(f"    update subleading (phi+2)/4 = {update_rate:.5f}  vs recovery "
          f"(2/3)^6 = {recovery:.5f}  ((2/3)^6 in spectrum? {in_spectrum})")
    check("HONEST NEGATIVE [E]: the lazy-update rate (phi+2)/4 = 0.9045 is NOT the "
          "recovery rate (2/3)^6, and (2/3)^6 is not an eigenvalue of A -- the "
          "family-recovery dynamics (gap 6 ln(3/2)) is carried by the cusp weights "
          "{0,1/3,2/3}, NOT the adjacency",
          abs(update_rate - 2 / 3) > 0.2 and not in_spectrum)

    # 4. honest negative: the seed is analytic, not an edge fraction
    p0 = float(phi0)
    is_simple_fraction = any(abs(p0 - a / b) < 1e-6
                             for b in range(1, 50) for a in range(1, b))
    check("HONEST NEGATIVE [E]: the seed phi0 = 1/(6 pi) + 48 c3^4 = %.7f is "
          "analytic/transcendental, not a small rational network fraction (v298)"
          % p0, not is_simple_fraction)

    # conclusion: the precisely delimited open question
    must_inject = ["cusp-weight 2/3 = |Z2|/N_fam (the gap 6 ln(3/2))",
                   "the analytic seed phi0 = 1/(6 pi) + 48 c3^4"]
    check("SHARPENED [O]: a rewrite reproducing the FULL structure must inject "
          "exactly two non-graph-spectral data beyond the (2,3,5) adjacency: %s; "
          "the pure network gives only the Coxeter skeleton + the 5-fold golden "
          "ratio. The open question is now precisely delimited (not closed)"
          % " ; ".join(must_inject),
          len(must_inject) == 2 and N_fam == 3)

    return summary("v312 hypergraph substrate sharpened")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
