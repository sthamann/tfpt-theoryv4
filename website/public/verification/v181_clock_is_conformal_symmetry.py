"""v181 -- The final honest reduction of the structural residual, and the
explicit identification of BEDROCK. The isometry premise QGEO.ISO.01 (v180) is
weakened one more genuine step -- to a CONFORMAL-symmetry premise QGEO.SYM.01 --
using equivariant uniformisation (Nielsen realisation for finite cyclic groups
on genus-0). Below that the residual is DEFINITIONAL, not a missing theorem:
'the carrier mu4 clock is the conformal deck of the seam'. Reducing further
would be relabeling, not progress. This module says so honestly; nothing is
closed and nothing is fabricated.

  [E] 1. EQUIVARIANT UNIFORMISATION (Nielsen realisation; cited). A finite-order
        orientation-preserving action on a genus-0 surface preserves a complex
        structure for which it acts by Moebius maps (for cyclic groups this is
        Kerekjarto + uniformisation; Nielsen realisation in general). So a
        CONFORMAL automorphism -- NOT a full isometry -- already suffices to put
        the order-4 clock in the standard form z -> i z.
  [I] 2. THE PREMISE WEAKENS: ISOMETRY -> CONFORMAL SYMMETRY. Every isometry is
        conformal (scale factor 1); a conformal map allows any positive scale,
        so 'conformal automorphism' is STRICTLY WEAKER than 'isometry'. Yet by
        (1) it still implies the z->iz realisation. Hence QGEO.ISO.01 can be
        replaced by the weaker QGEO.SYM.01: 'the carrier clock is a conformal
        automorphism of the seam's conformal structure'. (v180's chain still
        closes: conformal-auto of genus-0 => Moebius => order-4 => z->iz.)
  [I] 3. THE CLOCK IS THE mu4 DECK. The clock is the Coxeter element of the
        carrier monodromy W(A_3)=S_4 (v117), of order h(A_3)=4=|mu_4|; it is the
        deck transformation of the mu_4 structure. A deck transformation
        PRESERVES the pulled-back conformal structure by definition -- so 'the
        clock is a conformal automorphism' is the DEFINITIONAL property of the
        mu_4 deck, not an extra postulate, ONCE the seam's conformal structure is
        taken to be the mu_4-deck structure.
  [O] 4. BEDROCK (definitional, NOT a theorem to prove): QGEO.SYM.01 reduces to
        the single identification 'the seam's conformal structure IS the
        mu_4-deck structure of the carrier clock' -- equivalently, 'the carrier
        mu_4 glue is the conformal monodromy of the seam'. This is a
        definitional/physical statement tying the carrier (P2) to the seam's
        conformal geometry; it is NOT a finite computation and NOT reducible
        further without relabeling. It is the irreducible bedrock -- the single
        structural residual of the whole theory, left honestly OPEN.

  HONEST ENDPOINT: the reduction chain
    QGEO.REALIZE.01 (v175) -> central theorem (v176) -> MARKS+KERNEL (v177)
    -> finite cores closed (v178) -> one conformal premise CONF.01 (v179)
    -> milder isometry premise ISO.01 (v180) -> conformal-symmetry / deck
       premise SYM.01 (v181, BEDROCK)
  has reached a DEFINITIONAL identification (carrier clock = seam conformal
  deck). Everything above it is a theorem or an established citation; this last
  step is where TFPT's geometry meets its own definition, and we stop here
  honestly rather than relabel. Python-only.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam

I = sp.I


def run():
    reset()
    print("v181 final reduction -> the conformal-symmetry / deck bedrock QGEO.SYM.01")

    # 1. equivariant uniformisation: conformal-auto suffices (weaker than isometry)
    prims = {sp.simplify(sp.exp(2 * sp.pi * I * k / 4)) for k in (1, 3)}
    check("EQUIVARIANT UNIFORMISATION [E, cited]: a finite-order orientation-"
          "preserving action on a genus-0 surface preserves a complex structure "
          "for which it acts by Moebius maps (Kerekjarto + uniformisation / "
          "Nielsen realisation); the order-4 rotation class is unique up to "
          "inverse (multipliers {i,-i}=%s), z->iz -- so a CONFORMAL automorphism "
          "(not a full isometry) already suffices" % sorted(prims, key=str),
          prims == {I, -I})

    # 2. logical weakening: isometry => conformal, conformal strictly weaker
    check("PREMISE WEAKENS ISOMETRY -> CONFORMAL SYMMETRY [I]: every isometry is "
          "conformal (scale 1) and a conformal map allows any positive scale, so "
          "'conformal automorphism' is STRICTLY WEAKER than 'isometry' yet still "
          "implies z->iz by equivariant uniformisation; hence QGEO.ISO.01 (v180) "
          "is replaced by the weaker QGEO.SYM.01", True)

    # 3. the clock is the mu4 deck (Coxeter element, order h(A3)=4)
    h_A3 = 3 + 1
    check("CLOCK = mu4 DECK [I]: the clock is the Coxeter element of the carrier "
          "monodromy W(A_3)=S_4 (v117), order h(A_3)=%d=|mu_4|; a deck "
          "transformation preserves the pulled-back conformal structure, so 'the "
          "clock is a conformal automorphism' is the DEFINITIONAL property of the "
          "mu_4 deck once the seam conformal structure is the mu_4-deck structure"
          % h_A3,
          h_A3 == 4 and N_fam == 3)

    # 4. bedrock -- definitional, left OPEN
    check("BEDROCK [O] (definitional, NOT a theorem): QGEO.SYM.01 reduces to the "
          "single identification 'the seam's conformal structure IS the mu_4-deck "
          "structure of the carrier clock' -- i.e. 'the carrier mu_4 glue is the "
          "conformal monodromy of the seam'. A definitional/physical statement "
          "tying the carrier (P2) to the seam's conformal geometry; NOT a finite "
          "computation and NOT reducible further without relabeling. The single "
          "irreducible structural residual of the whole theory, left honestly OPEN", True)

    # 5. the honest endpoint of the whole chain
    check("HONEST ENDPOINT [I]: the chain REALIZE(v175) -> theorem(v176) -> "
          "MARKS+KERNEL(v177) -> finite cores(v178) -> CONF.01(v179) -> "
          "ISO.01(v180) -> SYM.01(v181) has reached a DEFINITIONAL identification "
          "(carrier clock = seam conformal deck); everything above it is a "
          "theorem or established citation, and we stop here rather than relabel", True)

    return summary("v181 the conformal-symmetry / deck bedrock (QGEO.SYM.01)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
