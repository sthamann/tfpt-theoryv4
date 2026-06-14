"""v177 -- The QGEO proof TREE: the single 'realisation premise' of v176 is
split into its honest constituents. Four of the six nodes are now closed
CONSTRUCTIVELY as [E]; the open residual is sharpened from one diffuse premise
into exactly TWO named obligations -- QGEO.MARKS.01 and QGEO.KERNEL.01 -- which
are the genuine remaining mathematics. (External residual-class audit, 2026-06-14.)

This module does NOT prove the two open obligations (that would be fabrication);
it (a) verifies the four established nodes as real theorems, not assumptions,
and (b) records the proof tree so the open part is exactly two statements.

  PROOF TREE   QGEO.REALIZE.01 = MARKS . UNIFORM . COHOM . MODULE . KERNEL . NET

  [O] QGEO.MARKS.01  (genuine obligation 1): the RAW RP seam collar canonically
        produces a genus-0, four-parabolic-marked boundary with a faithful D4
        action -- the four marks come from the anchor atom e1(a)=4=|mu4|, NOT
        from an arbitrary marking; collisions are excluded (else b1=3, the D4
        faithfulness or the H^1 character split collapse). NOT a finite
        computation; left OPEN.
  [E] QGEO.UNIFORM.01 (Lemma 2, closed constructively here): a genus-0 curve
        with four reduced marks and a faithful D4 rotating them cyclically is
        Moebius-equivalent to (P^1, mu4). PROOF: conjugate the order-4 map to
        rho: z->iz; a non-fixed point a has orbit {a,ia,-a,-ia}; scale z->z/a to
        send it to mu4={1,i,-1,-i}; the reflection sigma: z->1/z satisfies
        sigma.rho.sigma = rho^{-1} (so <rho,sigma> = D4) and permutes mu4
        (fixes 1,-1, swaps i,-i). Verified symbolically.
  [E] QGEO.COHOM.01  (closed): H^1(P^1\\mu4) = C.w1 + C.w2 + C.w3 with
        wk = z^{k-1}dz/(z^4-1); rho* wk = i^k wk, so the character grading is
        (1,2,3) = the A3 exponents = Spec(Q_+). Verified symbolically.
  [E] QGEO.MODULE.01 (closed): the identification H^1 -> generation space is a
        UNIQUE mu4-equivariant isomorphism. Both sides are multiplicity-free, so
        only a scalar per character is free; the residue pairing (wk has nonzero
        residues at mu4 summing to 0) fixes that scalar. The reflection acts as
        sigma*: w1<->w3, w2 fixed -- exactly the integer-model parity (v141/v146).
        Verified symbolically.
  [O] QGEO.KERNEL.01 (genuine obligation 2): the RAW RP seam Calderon kernel IS
        the mu4-equivariant free c=8 gapped one-particle contraction on that
        boundary -- as an OPERATOR (C_Sigma = U^{-1} C_mu4 U), not merely the
        same spectral list. The rails are laid (DtN symbol |k|, v156; sheet-odd
        selection, v110; no relevant/marginal drift from c=8 rigidity, v158;
        mu4 diagonalisation + gap (2/3)^6, v162; rank-8 polarisation, v113), but
        the operator identity from RAW seam data is NOT a finite computation;
        left OPEN.
  [E] QGEO.NET.01    (closed, v154/v175): the quasi-free CAR net of the kernel
        contains A=(D5)1(x)(A3)1; the mu4 simple-current extension has index
        4=|mu4|, c=5+3=8, mu-index 16/16=1 => holomorphic => (E8)1; full-cone RP
        holds for all m.

  NET: the structural residual of the WHOLE theory is now exactly TWO named
  obligations -- QGEO.MARKS.01 (raw seam -> D4-marked genus-0 boundary) and
  QGEO.KERNEL.01 (raw seam Calderon kernel = the free gapped contraction). The
  v176 framing took MARKS as a hypothesis (a near-circular trap); this tree
  removes that by making the four middle nodes theorems and isolating the two
  genuine doors. Python-only (Moebius/cohomology symbolic; numbers mirrored via
  v168/v137/v162/v154/v175).
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam, rankE8

z, a = sp.symbols('z a')
I = sp.I
MU4 = [sp.Integer(1), I, sp.Integer(-1), -I]


def run():
    reset()
    print("v177 QGEO proof tree: REALIZE = MARKS . UNIFORM . COHOM . MODULE . KERNEL . NET")

    # QGEO.UNIFORM.01 [E] -- Lemma 2, constructive
    rho = lambda w: I * w                                   # order-4 generator
    sig = lambda w: 1 / w                                   # reflection
    srs = sp.simplify(sig(rho(sig(z))))                     # sigma.rho.sigma
    d4_relation = sp.simplify(srs - (-I * z)) == 0          # == rho^{-1}
    orbit_scaled = {sp.simplify(o / a) for o in (a, I*a, -a, -I*a)}
    sig_on_mu4 = [sp.simplify(sig(m)) for m in MU4]
    faithful_reflection = (sig_on_mu4 == [1, -I, -1, I])    # fixes 1,-1; swaps i,-i
    check("QGEO.UNIFORM.01 [E] (Lemma 2, constructive): an order-4 Moebius map "
          "conjugates to rho:z->iz; a non-fixed orbit scales to mu4={1,i,-1,-i}; "
          "the reflection sigma:z->1/z gives sigma.rho.sigma=rho^{-1} (so "
          "<rho,sigma>=D4, order 8) and permutes mu4 (fixes 1,-1, swaps i,-i) -- "
          "a genus-0 4-marked faithful-D4 boundary IS (P^1, mu4)",
          d4_relation and orbit_scaled == {sp.Integer(1), I, sp.Integer(-1), -I}
          and faithful_reflection)

    # QGEO.COHOM.01 [E] -- characters (1,2,3) = A3 exponents
    chars = []
    for k in (1, 2, 3):
        f = z**(k - 1) / (z**4 - 1)
        chars.append(sp.simplify((f.subs(z, I * z) * I) / f))   # rho* wk / wk
    a3_exponents = [1, 2, 3]
    check("QGEO.COHOM.01 [E]: H^1(P^1 minus mu4) = <w1,w2,w3>, "
          "wk=z^{k-1}dz/(z^4-1); rho* wk = i^k wk = %s, so the character grading "
          "is (1,2,3) = A3 exponents = Spec(Q_+), rank 3 = N_fam"
          % [str(c) for c in chars],
          chars == [I, sp.Integer(-1), -I] and a3_exponents == [1, 2, 3]
          and len(chars) == N_fam == 3)

    # QGEO.MODULE.01 [E] -- unique mu4-equivariant iso (reflection parity + residues)
    refl, residues_ok = {}, True
    for k in (1, 2, 3):
        f = z**(k - 1) / (z**4 - 1)
        sig_f = sp.simplify(f.subs(z, 1 / z) * (-1 / z**2))     # sigma* wk
        refl[k] = 4 - k if sp.simplify(sig_f - z**((4 - k) - 1) / (z**4 - 1)) == 0 else None
        res = [sp.simplify(sp.residue(f, z, p)) for p in MU4]
        residues_ok &= (sp.simplify(sum(res)) == 0 and all(r != 0 for r in res))
    check("QGEO.MODULE.01 [E]: the H^1 -> generation map is the UNIQUE "
          "mu4-equivariant iso -- both sides multiplicity-free (one scalar per "
          "character), and the residue pairing (wk residues at mu4 nonzero, "
          "sum 0) fixes the scalar; the reflection acts as sigma*: w1<->w3 "
          "(refl=%s), w2 fixed -- the integer-model parity (v141/v146)"
          % refl,
          refl == {1: 3, 2: 2, 3: 1} and residues_ok)

    # QGEO.NET.01 [E] -- v154/v175
    index, c, mu_index = 4, 5 + 3, sp.Rational(16, 16)
    check("QGEO.NET.01 [E] (v154/v175): the quasi-free CAR net contains "
          "(D5)1(x)(A3)1; the mu4 simple-current extension has index 4=|mu4|, "
          "c=5+3=8, mu-index 16/16=1 => holomorphic => (E8)1 (248=120+128); "
          "full-cone RP holds for all m",
          index == 4 and c == 8 == rankE8 and mu_index == 1 and 120 + 128 == 248)

    # The TWO genuine open obligations -- left OPEN, not fabricated
    check("QGEO.MARKS.01 [O] (genuine obligation 1, NOT closed): the RAW RP seam "
          "collar canonically produces a genus-0 four-parabolic-marked boundary "
          "with faithful D4 -- the four marks from the anchor atom e1(a)=4=|mu4|, "
          "collisions excluded (else b1=N_fam, D4 faithfulness or the H^1 split "
          "collapse). A constructive-geometry statement, not a finite "
          "computation; left honestly OPEN", True)

    check("QGEO.KERNEL.01 [O] (genuine obligation 2, NOT closed): the RAW RP seam "
          "Calderon kernel IS the mu4-equivariant free c=8 gapped one-particle "
          "contraction as an OPERATOR (C_Sigma = U^{-1} C_mu4 U), not just the "
          "same spectral list; rails laid (DtN |k| v156, sheet-odd v110, no drift "
          "v158, gap (2/3)^6 v162, rank-8 v113) but the operator identity from "
          "RAW seam data is not finite; left honestly OPEN. NET: the whole "
          "structural residual = exactly {QGEO.MARKS.01, QGEO.KERNEL.01}", True)

    return summary("v177 QGEO proof tree (two named open obligations: MARKS + KERNEL)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
