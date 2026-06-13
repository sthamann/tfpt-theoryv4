"""v160 -- Seam Gaussianity from the admissible fixed point: the CONDITIONAL
theorem, and the one premise it really rests on.

This module formalises the proposed closure of premise (A) ("the seam bulk is
a reflection-positive free/Gaussian field") as a fixed-point statement:

    RP seam kernel  +  gapped PF transport  +  QBL (one kernel = the net)
        =>  quasi-free seam  (all higher cumulants vanish).

The structure of the argument is exact and machine-checkable in the finite
model; what it does NOT do, on the current evidence, is close (A).  It RELOCATES
(A) to a single, sharper, internal statement -- the honest content of this
module:

    [P]  THE SCOPE PREMISE.  The gapped Perron-Frobenius uniqueness proven in
         v56 holds on the THREE-dimensional scalar transfer spectrum
         {1,(2/3)^6,(1/3)^6} (the flavor gap / horizon Page-recovery rates),
         NOT on the cone of OS-positive Schwinger functionals (the states whose
         higher connected cumulants kappa_{2n} this theorem must contract).
         Closing (A) requires extending v56's primitivity + spectral gap from
         that 3-dim readout space to the full correlation cone.  That extension
         is NOT established here; it is the entire remaining load.

So v160 is a [P]/[C] reframing module in the spirit of v157/v158: the parts
that PASS are the exact algebra (quasi-free => kappa_{2n}=0; Wick/Pfaffian
functoriality => the quasi-free state is a transport fixed point; the PF
dichotomy on a toy cone; the dimension gap between v56's space and the cone);
the part that is recorded-not-proven is the scope premise.  Python-only
(numpy/sympy + stdlib); no exact-identity content for the Wolfram mirror.

  [I] 1. QUASI-FREE => ALL HIGHER CONNECTED CUMULANTS VANISH.  For a fermionic
         Gaussian (quasi-free) state with covariance Gamma the 2n-point moment
         is the Pfaffian of the 2n x 2n submatrix; the moment<->cumulant
         (set-partition Moebius) inversion then gives kappa(S) = 0 for every
         |S| >= 3 and kappa(S) = Gamma_ij for |S| = 2 -- verified exactly on a
         concrete pure Majorana covariance for ALL 4- and 6-point subsets.
         "The Wick state is Gaussian" is therefore not an assumption but an
         identity of the one 2-point kernel (the v113 'one kernel = net'
         property, restated at the level of cumulants).
  [I] 2. THE QUASI-FREE STATE IS A TRANSPORT FIXED POINT (functoriality).  A
         kernel-preserving transport O.Gamma.O^T = Gamma fixes every correlator,
         because each correlator is a Pfaffian of (a submatrix of) Gamma -- so
         if the degree-2 datum K_Sigma is fixed, the whole quasi-free state is
         fixed.  Checked: an O commuting with Gamma leaves all 4- and 6-point
         functions invariant.
  [I] 3. THE PERRON-FROBENIUS DICHOTOMY (toy cone).  A primitive positive map
         with a spectral gap has a UNIQUE fixed ray; any state component off the
         fixed ray decays geometrically at the sub-leading rate.  Hence a
         non-Gaussian piece kappa_{2n} != 0 is impossible: if it were fixed it
         would be a SECOND fixed ray (kills uniqueness); if not fixed it lies in
         the gapped complement and decays to 0.  Demonstrated on a 5-dim toy
         transport: gapped => 1-dim fixed space (unique); a degenerate variant
         with a second unit eigenvalue => 2-dim fixed space (a non-Gaussian
         fixed datum <=> loss of uniqueness).
  [I] 4. THE QUALITATIVE CLAIM NEEDS ONLY gap > 0.  kappa_{2n} -> 0 follows from
         ANY sub-leading rate < 1; the specific value Delta = 6 log(3/2) (i.e.
         lambda2 = (2/3)^6) only sets the DECAY RATE.  Carrying that scalar
         value into the higher-cumulant sectors is an over-extension unless
         those sectors are shown to sit in the gap -- see point 5.
  [P] 5. THE SCOPE PREMISE (recorded, NOT proven -- the whole remaining load).
         v56 establishes primitivity + gap on a 3-dim space (len(spec) = 3).
         The quasi-free seam state already has C(16,4) = 1820 degree-4 and
         C(16,6) = 8008 degree-6 connected-cumulant directions: the cone the
         transport must act on (primitively, with a gap) to force kappa_{2n}=0
         has dimension >> 3.  PF uniqueness on the 3-dim readout spectrum does
         NOT, as a matter of dimension, imply PF uniqueness on the correlation
         cone.  NON-CIRCULARITY: assumption "unique fixed ray" must hold on the
         FULL cone (incl. non-Gaussian functionals); if it held only on the
         quasi-free sub-cone the argument would assume what it proves.  THIS is
         the equivalent open statement (A) reduces to:
             "the admissible TFPT seam transport is a primitive, spectrally
              gapped, RP-cone-preserving map on the full Schwinger cone --
              not only on the scalar readout spectrum of v56."
         Smaller and sharper than 'prove Gaussianity', but unproven.
"""
import math
from itertools import combinations

import numpy as np

from tfpt_constants import check, summary, reset, g_car, N_fam


def _pure_cov(n, seed):
    """A pure fermionic Gaussian covariance Gamma = Q J Q^T (real antisymmetric,
    i*Gamma a contraction with Gamma^2 = -I)."""
    rng = np.random.default_rng(seed)
    Q, _ = np.linalg.qr(rng.standard_normal((n, n)))
    J = np.kron(np.eye(n // 2), np.array([[0.0, 1.0], [-1.0, 0.0]]))
    G = Q @ J @ Q.T
    return (G - G.T) / 2


def _pfaffian(G, idx):
    """Pfaffian of the antisymmetric submatrix on the ordered index tuple idx."""
    if len(idx) == 0:
        return 1.0
    if len(idx) % 2 == 1:
        return 0.0
    head, rest = idx[0], idx[1:]
    total = 0.0
    for t, j in enumerate(rest):
        sub = tuple(x for x in rest if x != j)
        total += (-1) ** t * G[head, j] * _pfaffian(G, sub)
    return total


def _set_partitions(items):
    """Yield every set partition of the tuple `items`; each block is an ascending
    tuple (items must be ascending)."""
    items = list(items)
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for part in _set_partitions(rest):
        yield [(first,)] + part                       # first as its own block
        for i in range(len(part)):                    # first prepended to a block
            yield part[:i] + [(first,) + part[i]] + part[i + 1:]


def _concat_sign(S, concat):
    """Parity (+/-1) of the permutation taking the ascending tuple S to `concat`
    (a reordering of S's elements) -- the fermionic Pfaffian/Grassmann sign."""
    pos = {x: i for i, x in enumerate(S)}
    seq = [pos[x] for x in concat]
    inv = sum(1 for i in range(len(seq)) for j in range(i + 1, len(seq))
              if seq[i] > seq[j])
    return -1.0 if inv % 2 else 1.0


def _cumulants(G, max_size):
    """Connected (fermionic) cumulants kappa(S) from the moments m(S) = Pf(G[S])
    by the SIGNED set-partition moment<->cumulant inversion
        m(S) = sum_pi sgn(pi) prod_B kappa(B).
    Odd blocks give kappa = 0 (no odd correlators); even blocks commute so the
    block order is immaterial.  Returns {S (ascending tuple): value}."""
    kap = {}

    def kappa(S):
        if S in kap:
            return kap[S]
        val = _pfaffian(G, S)
        for part in _set_partitions(S):
            if len(part) == 1:                        # the trivial {S} block = kappa(S)
                continue
            blocks = sorted(part, key=lambda b: b[0])
            concat = tuple(x for b in blocks for x in b)
            prod = 1.0
            for b in blocks:
                prod *= kappa(b)
            val -= _concat_sign(S, concat) * prod
        kap[S] = val
        return val

    n = G.shape[0]
    for size in range(1, max_size + 1):
        for S in combinations(range(n), size):
            kappa(S)
    return kap


def run():
    reset()
    print("v160 seam gaussianity from the admissible fixed point "
          "(conditional theorem; the load is the scope premise)")

    # ---- 1. quasi-free => higher connected cumulants vanish (exact) ----
    n = 8
    G = _pure_cov(n, 7)
    pure = np.allclose((1j * G) @ (1j * G), np.eye(n))
    kap = _cumulants(G, 6)
    k2_ok = all(abs(kap[p] - G[p[0], p[1]]) < 1e-9
                for p in combinations(range(n), 2))
    k4_max = max(abs(kap[s]) for s in combinations(range(n), 4))
    k6_max = max(abs(kap[s]) for s in combinations(range(n), 6))
    check("QUASI-FREE => kappa_{2n}=0 for n>=2: with the 2n-point moment = "
          "Pf(Gamma submatrix), the set-partition moment<->cumulant inversion "
          "gives kappa(|S|=2) = Gamma_ij and kappa(|S|=4) = kappa(|S|=6) = 0 "
          "EXACTLY (concrete pure Majorana covariance, all subsets) -- 'the "
          "Wick state is Gaussian' is an identity of the one 2-point kernel",
          pure and k2_ok and k4_max < 1e-9 and k6_max < 1e-9)

    # ---- 2. kernel-preserving transport => the quasi-free state is fixed ----
    # an orthogonal O commuting with Gamma fixes the kernel, hence every Pfaffian
    w, V = np.linalg.eig(1j * G)              # i*Gamma is Hermitian, real spectrum +-1
    theta = 0.37
    # rotation inside each conjugate eigichpair keeps i*Gamma (hence Gamma) fixed
    O = np.real(V @ np.diag(np.exp(1j * theta * np.sign(w.real))) @ np.linalg.inv(V))
    Gt = O @ G @ O.T
    kernel_fixed = np.allclose(Gt, G, atol=1e-9)
    inv4 = max(abs(_pfaffian(Gt, s) - _pfaffian(G, s))
               for s in combinations(range(n), 4))
    inv6 = max(abs(_pfaffian(Gt, s) - _pfaffian(G, s))
               for s in combinations(range(n), 6))
    check("FIXED POINT BY FUNCTORIALITY: a kernel-preserving transport "
          "O.Gamma.O^T = Gamma fixes EVERY correlator (each is a Pfaffian of a "
          "Gamma submatrix) -- so fixing the degree-2 datum K_Sigma fixes the "
          "whole quasi-free state; all 4- and 6-point functions invariant",
          kernel_fixed and inv4 < 1e-9 and inv6 < 1e-9)

    # ---- 3. the Perron-Frobenius dichotomy on a toy cone ----
    lam2 = (2.0 / 3.0) ** 6
    spec = np.array([1.0, lam2, lam2 ** 2, lam2 ** 3, lam2 ** 4])  # gap: 1 then <1
    M = np.array([[1, 1, 1, 1, 1], [0, 1, 2, 3, 4], [0, 0, 1, 3, 6],
                  [0, 0, 0, 1, 4], [0, 0, 0, 0, 1]], float)        # invertible
    T = M @ np.diag(spec) @ np.linalg.inv(M)
    fixed_dim = 5 - np.linalg.matrix_rank(T - np.eye(5), tol=1e-9)
    # degenerate variant: a SECOND unit eigenvalue (a 'fixed kappa_{2n}')
    Tdeg = M @ np.diag([1.0, 1.0, lam2 ** 2, lam2 ** 3, lam2 ** 4]) @ np.linalg.inv(M)
    fixed_dim_deg = 5 - np.linalg.matrix_rank(Tdeg - np.eye(5), tol=1e-9)
    check("PF DICHOTOMY: a gapped primitive transport has a UNIQUE fixed ray "
          "(fixed-space dim 1); a non-Gaussian fixed datum would be a SECOND "
          "fixed ray (degenerate variant => fixed-space dim 2) and break "
          "uniqueness -- 'kappa_{2n} fixed => contradiction'",
          fixed_dim == 1 and fixed_dim_deg == 2)

    # off-fixed-ray components (the non-fixed cumulant modes) live in the gapped
    # complement; in the eigenbasis they are scaled by spec[1:] (all < 1) and
    # decay geometrically at the sub-leading rate lambda2 = (2/3)^6
    nonfixed = spec[1:]                            # [lam2, lam2^2, lam2^3, lam2^4]
    x = np.ones(4)
    after = (nonfixed ** 12) * x
    decayed = np.linalg.norm(after) <= (lam2 ** 12) * np.linalg.norm(x) * (1 + 1e-6)
    check("PF DICHOTOMY: an off-fixed-ray component (a non-fixed kappa_{2n}) "
          "lies in the gapped complement (eigenvalues spec[1:] all < 1) and "
          "decays geometrically at the sub-leading rate lambda2 = (2/3)^6 -> 0 "
          "in the IR -- 'kappa_{2n} not fixed => contracted away by the gap'",
          decayed and float(nonfixed.max()) < 1.0)

    # ---- 4. the qualitative claim needs only gap > 0 (not the value) ----
    decays_for_any_gap = True
    for lam in (0.9, 0.5, 0.1):
        nf = np.array([lam, lam ** 2, lam ** 3, lam ** 4])
        decays_for_any_gap &= (np.linalg.norm((nf ** 200) * x) < 1e-6)
    check("QUALITATIVE GAUSSIANITY NEEDS ONLY gap>0: kappa_{2n}->0 for ANY "
          "sub-leading rate lambda2 in (0,1); the specific Delta=6 log(3/2) "
          "((2/3)^6) only sets the DECAY RATE -- so carrying that scalar value "
          "into the higher-cumulant sectors is an over-extension unless they "
          "are shown to sit in the gap",
          decays_for_any_gap)

    # ---- 5. THE SCOPE PREMISE: v56 acts on 3 scalars, the cone is huge ----
    v56_dim = 3                              # len({1,(2/3)^6,(1/3)^6})
    seam_majoranas = 2 * (g_car + N_fam)     # 16 = 2 * rank E8
    deg4 = math.comb(seam_majoranas, 4)      # 1820 degree-4 cumulant directions
    deg6 = math.comb(seam_majoranas, 6)      # 8008 degree-6
    check("THE SCOPE GAP IS REAL: v56's gapped PF uniqueness lives on a "
          "3-dim scalar transfer spectrum {1,(2/3)^6,(1/3)^6}; the quasi-free "
          "16-Majorana seam state already has C(16,4)=1820 degree-4 and "
          "C(16,6)=8008 degree-6 connected-cumulant directions -- the "
          "correlation cone the transport must contract has dimension >> 3, so "
          "PF uniqueness on the readout space does NOT imply it on the cone",
          v56_dim == 3 and seam_majoranas == 16 and deg4 == 1820 and deg6 == 8008
          and deg4 > v56_dim)

    check("THE ONE REMAINING PREMISE [P] (recorded, NOT proven): (A) is "
          "equivalent to 'the admissible TFPT seam transport is a primitive, "
          "spectrally gapped, RP-cone-preserving map on the FULL Schwinger "
          "cone, not only on the scalar readout spectrum of v56'. Given it, "
          "steps 1-3 close (A) (quasi-free fixed point unique => kappa_{2n}=0 "
          "=> carrier net A => (E8)1, v113/v154/v156); non-circular only if "
          "uniqueness holds on the full cone (incl. non-Gaussian functionals). "
          "This is a strictly smaller, internal, exact-testable statement than "
          "'prove Gaussianity' -- but it is the entire remaining load, and v56 "
          "as it stands does not supply it", True)

    return summary("v160 seam gaussianity from the admissible fixed point")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
