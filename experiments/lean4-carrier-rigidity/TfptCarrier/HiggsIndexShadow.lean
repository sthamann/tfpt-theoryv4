/-
  TFPT Carrier — Higgs Index, Algebraic Shadow
  --------------------------------------------

  TFPT Paper 2 derives `dim E_+ = 2` from the compact Higgs index,
  which in geometric form reads

      H^0(P^1, O(1)) ≅ K[X, Y]_1  ≅  K · X ⊕ K · Y,

  i.e. the space of homogeneous degree-1 polynomials in two
  variables. The geometric content (line bundles, sheaf cohomology
  on `P^1`) is heavy in Lean. This module formalises the
  **algebraic shadow** of the index: the explicit description of
  degree-1 binary forms as a 2-dimensional `K`-vector space.

  Three-stage discharge of `dim E_+ = 2`:

  Stage A.  Honest interface `HiggsIndexCertificate K Eplus`:
            a linear isomorphism `Eplus ≃ₗ[K] Fin 2 → K`.
            This stage replaces the bare numerical input with a
            structural witness.

  Stage B.  This module.  Identifies the target of the equivalence
            with the algebraic shadow `DegreeOneBinaryForms K`,
            which has `Module.finrank K _ = 2` by direct computation.

  Stage C.  Future work.  Build the equivalence
            `Eplus ≃ₗ[K] H^0(P^1, O(1))` from the Calderón
            polarization plus the compact Higgs index.  This is the
            geometric step that would close the chain to Paper 2.

  See `TfptCarrier/CarrierData.lean` for how stages A and B feed
  the main carrier theorem.
-/

import Mathlib.LinearAlgebra.FiniteDimensional.Defs
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.FreeModule.Finite.Basic
import Mathlib.Data.Fin.VecNotation

namespace TFPT.Carrier.HiggsIndexShadow

variable (K : Type*) [Field K]

/--
The algebraic shadow of `H^0(P^1, O(1))`: degree-one binary forms in
`K[X, Y]`, identified as `K^2` with basis `(X, Y)`.

This is *not* a free-standing model of projective space; it is the
explicit description of the global sections of `O(1)`, which is the
only piece of `P^1` geometry needed to fix `dim E_+ = 2`.
-/
abbrev DegreeOneBinaryForms : Type _ := Fin 2 → K

/--
**Algebraic Higgs-shadow theorem.**

The space of degree-one binary forms in two variables over `K` has
dimension `2`.

In TFPT terms: this is the dimension count behind the compact Higgs
index argument that forces `dim E_+ = 2`. The full geometric
statement `dim H^0(P^1, O(1)) = 2` reduces to this once the
identification `H^0(P^1, O(1)) ≅ K[X, Y]_1` is made.
-/
theorem finrank_degreeOneBinaryForms :
    Module.finrank K (DegreeOneBinaryForms K) = 2 := by
  show Module.finrank K (Fin 2 → K) = 2
  rw [Module.finrank_fintype_fun_eq_card]
  exact Fintype.card_fin 2

/--
**Stage-A interface for the Higgs index.**

A `HiggsIndexCertificate` is a linear equivalence between the
positive polarization block `Eplus` and the algebraic shadow of
`H^0(P^1, O(1))`. Producing such a certificate is the formal
interface to "compact Higgs index implies `dim E_+ = 2`".

The full TFPT proof of Paper 2 would build the certificate from the
Calderón polarization data plus the index computation. Here we take
the certificate as a structural input; from it, `dim Eplus = 2`
follows mechanically.
-/
structure HiggsIndexCertificate
    (K : Type*) [Field K]
    (Eplus : Type*) [AddCommGroup Eplus] [Module K Eplus] where
  toForms : Eplus ≃ₗ[K] DegreeOneBinaryForms K

variable {K}
variable {Eplus : Type*} [AddCommGroup Eplus] [Module K Eplus]

/-- A `HiggsIndexCertificate` transfers finite-dimensionality. -/
instance (cert : HiggsIndexCertificate K Eplus) :
    FiniteDimensional K Eplus :=
  Module.Finite.equiv cert.toForms.symm

/--
**Higgs corollary**: a Higgs-index certificate forces
`dim Eplus = 2`.

Combining stage A (the certificate) with stage B (`finrank` of the
shadow) gives the rank discharge needed by the carrier rigidity
theorem.
-/
theorem HiggsIndexCertificate.finrank_Eplus_eq_two
    (cert : HiggsIndexCertificate K Eplus) :
    Module.finrank K Eplus = 2 := by
  rw [LinearEquiv.finrank_eq cert.toForms]
  exact finrank_degreeOneBinaryForms K

end TFPT.Carrier.HiggsIndexShadow
