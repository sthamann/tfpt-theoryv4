/-
  TFPT Carrier — Main Theorem: Bundling All Premises
  --------------------------------------------------

  The headline bundled theorems of the project. Together they
  thread through:

    InvolutionProjectors      ε² = 1  →  orthogonal idempotents P_±
    LatticeRigidityGeneral    primitive oriented trace-zero pair
                              →  unique (q_-, q_+)
    TraceProjection           structural  tr Y = 0  from rank data
    HiggsIndexShadow          Higgs Stage-A certificate  →  dim E_+ = 2
    YukawaRank                Yukawa Stage-A certificate →  dim E_- = 3

  Three load-bearing conclusions are bundled here:

    primitive_pair_eq_sm     (q_-, q_+) = (-2, 3)  under the rank
                             data and the primitive oriented
                             trace-zero condition
    trace_Y_eq_zero          tr Y = 0
    carrier_polynomial_Y     6 Y² − Y − 1 = 0   in End_K M

  The hypotheses of these theorems are *structured Stage-A
  hypotheses*, not bare numerical assumptions. They are not
  axioms — they are parameters that downstream extensions can
  supply by deeper theorems.
-/

import Mathlib.LinearAlgebra.Trace
import Mathlib.LinearAlgebra.FiniteDimensional.Defs

import TfptCarrier.Polarization
import TfptCarrier.InvolutionProjectors
import TfptCarrier.LatticeRigidityGeneral
import TfptCarrier.Rigidity
import TfptCarrier.TraceProjection
import TfptCarrier.HiggsIndexShadow
import TfptCarrier.YukawaRank

namespace TFPT.Carrier.CarrierData

open TFPT.Carrier
open TFPT.Carrier.InvolutionProjectors
open TFPT.Carrier.HiggsIndexShadow
open TFPT.Carrier.YukawaRank

/--
The complete bundle of structured Stage-A hypotheses feeding the
carrier theorem.

Each field corresponds to one of the *upstream Lean theorems* now
available in this project:

* `polarization` — a `Polarization (Module.End K M)`. In a typical
  application this is produced from a `CarrierInvolution` via
  `toPolarization`, i.e. the boundary-involution layer.

* `rank_neg`, `rank_pos` — rank discharges for `E_-` and `E_+`.
  In a typical application these come from a `YukawaRankCertificate`
  and a `HiggsIndexCertificate` respectively.

This structure makes the dependency on the Stage-A hypotheses
visible at the type level: anyone calling the bundled theorems
must produce a `CarrierPremises` value, which in turn forces them
to expose the rank witnesses explicitly.
-/
structure CarrierPremises
    (K : Type*) [Field K] [CharZero K]
    (M : Type*) [AddCommGroup M] [Module K M] [FiniteDimensional K M] where
  polarization : Polarization (Module.End K M)
  rank_neg : Module.finrank K (LinearMap.range polarization.Pm) = 3
  rank_pos : Module.finrank K (LinearMap.range polarization.Pp) = 2

namespace CarrierPremises

variable {K M : Type*}
variable [Field K] [CharZero K] [AddCommGroup M] [Module K M] [FiniteDimensional K M]
variable (cp : CarrierPremises K M)

/-- The carrier hypercharge generator `Y = -(1/3) · P_- + (1/2) · P_+`. -/
noncomputable def Y : Module.End K M :=
  (-((1 : K)/3)) • cp.polarization.Pm + ((1 : K)/2) • cp.polarization.Pp

/--
**Bundled theorem (B1) — primitive integer pair specialises to
`(-2, 3)`.**

This is the *carrier rigidity* output of the project, threaded
through the present rank data. Given any integer pair `(qm, qp)`
satisfying the **primitive oriented trace-zero condition**

    3 · qm + 2 · qp = 0,   qm < 0 < qp,   gcd(|qm|, qp) = 1,

we have `(qm, qp) = (-2, 3)`. The rank data `(3, 2)` enters via the
trace-zero coefficients.

This is a *parametrised* statement: nothing in `CarrierPremises`
is consulted, but the result is bundled here for use by
`hypercharge_carrier_packet`.
-/
theorem primitive_pair_eq_sm
    (qm qp : ℤ)
    (htrace : 3 * qm + 2 * qp = 0)
    (hsign_m : qm < 0)
    (hsign_p : 0 < qp)
    (hgcd : Int.gcd qm qp = 1) :
    qm = -2 ∧ qp = 3 :=
  TFPT.Carrier.Rigidity.unique_carrier_pair qm qp htrace hsign_m hsign_p hgcd

/--
**Bundled theorem (B2) — trace identity.**

Under the carrier premises (polarization + rank-3 Yukawa
+ rank-2 Higgs discharges), the determinant-normalised generator
`Y` has vanishing trace:

    tr Y = 0.

The argument bundles `TraceProjection.trace_carrier_Y_eq_zero`
with the rank data of `CarrierPremises`.
-/
theorem trace_Y_eq_zero : LinearMap.trace K M cp.Y = 0 := by
  have hm : IsIdempotentElem cp.polarization.Pm := cp.polarization.idem_m
  have hp : IsIdempotentElem cp.polarization.Pp := cp.polarization.idem_p
  exact TraceProjection.trace_carrier_Y_eq_zero
    cp.polarization.Pm cp.polarization.Pp
    hm hp cp.rank_neg cp.rank_pos

/--
**Bundled theorem (B3) — carrier polynomial in End form.**

Under the carrier premises, the generator `Y` satisfies the
carrier polynomial identity

    6 · Y² − Y − 1 = 0

as endomorphisms of `M`. Here `6 · (-)` is the natural-number
scalar action; the identity `1` is the identity endomorphism.

The proof is a direct computation using the polarization axioms:

    Y² = (-1/3)² (P_- · P_-) + (-1/3)(1/2) (P_- · P_+)
         + (1/2)(-1/3) (P_+ · P_-) + (1/2)² (P_+ · P_+)
       = (1/9) P_- + (1/4) P_+         (using idem and orth)
    6 Y² = (2/3) P_- + (3/2) P_+
    6 Y² − Y = (2/3 + 1/3) P_- + (3/2 − 1/2) P_+ = P_- + P_+ = 1
    6 Y² − Y − 1 = 0.

The hypothesis `CharZero K` is genuinely needed (it ensures `1/2`,
`1/3`, `1/6` exist in `K`). For the same reason, `6` is invertible
in `Module.End K M`.
-/
theorem carrier_polynomial_Y :
    (6 : ℕ) • (cp.Y * cp.Y) - cp.Y - 1 = (0 : Module.End K M) := by
  have hmm := cp.polarization.idem_m
  have hpp := cp.polarization.idem_p
  have hmp := cp.polarization.orth_mp
  have hpm := cp.polarization.orth_pm
  have hc  := cp.polarization.complete
  -- Step 1: expand Y * Y using the polarization axioms.
  have hYY :
      cp.Y * cp.Y
        = ((1 : K)/9) • cp.polarization.Pm
            + ((1 : K)/4) • cp.polarization.Pp := by
    unfold Y
    rw [mul_add, add_mul, add_mul,
        smul_mul_smul_comm, smul_mul_smul_comm,
        smul_mul_smul_comm, smul_mul_smul_comm,
        hmm, hpp, hmp, hpm, smul_zero, smul_zero]
    rw [add_zero, zero_add]
    congr 1
    · congr 1; ring
    · congr 1; ring
  -- Step 2: substitute into 6 • (Y * Y) - Y - 1 and combine.
  rw [hYY]
  -- LHS: 6 • ((1/9) Pm + (1/4) Pp) - (- (1/3) Pm + (1/2) Pp) - 1
  --    = (6/9) Pm + (6/4) Pp + (1/3) Pm - (1/2) Pp - 1
  --    = (2/3 + 1/3) Pm + (3/2 - 1/2) Pp - 1
  --    = 1 Pm + 1 Pp - 1
  --    = Pm + Pp - 1
  --    = 1 - 1 = 0   (using completeness)
  unfold Y
  rw [show (6 : ℕ) • (((1 : K)/9) • cp.polarization.Pm
                       + ((1 : K)/4) • cp.polarization.Pp)
        = ((6 : K) * (1/9)) • cp.polarization.Pm
          + ((6 : K) * (1/4)) • cp.polarization.Pp by
    rw [← Nat.cast_smul_eq_nsmul (R := K)]
    rw [smul_add, smul_smul, smul_smul]
    push_cast; ring_nf]
  -- Goal: (6·(1/9)) • Pm + (6·(1/4)) • Pp - (-(1/3) • Pm + (1/2) • Pp) - 1 = 0
  rw [show (((6 : K) * (1/9))) = ((2 : K)/3) by ring,
      show (((6 : K) * (1/4))) = ((3 : K)/2) by ring]
  rw [show
      (((2 : K)/3) • cp.polarization.Pm + ((3 : K)/2) • cp.polarization.Pp)
        - (-(((1 : K)/3)) • cp.polarization.Pm + ((1 : K)/2) • cp.polarization.Pp)
        - 1
      = ((2 : K)/3 - (-(1 : K)/3)) • cp.polarization.Pm
          + ((3 : K)/2 - (1 : K)/2) • cp.polarization.Pp - 1 by
    rw [show (-(((1 : K)/3)) • cp.polarization.Pm) = ((-(1 : K)/3) • cp.polarization.Pm) by
      rw [neg_div]
    ]
    rw [show ((2 : K)/3 - (-(1 : K)/3)) • cp.polarization.Pm
          = ((2 : K)/3) • cp.polarization.Pm - ((-(1 : K)/3)) • cp.polarization.Pm by
      rw [sub_smul]]
    rw [show ((3 : K)/2 - (1 : K)/2) • cp.polarization.Pp
          = ((3 : K)/2) • cp.polarization.Pp - ((1 : K)/2) • cp.polarization.Pp by
      rw [sub_smul]]
    abel]
  rw [show ((2 : K)/3 - (-(1 : K)/3)) = 1 by ring,
      show ((3 : K)/2 - (1 : K)/2) = 1 by ring]
  rw [one_smul, one_smul]
  rw [hc, sub_self]

/--
**Top-level bundled theorem — the 3+2 hypercharge carrier packet.**

Under the carrier premises (Stage-A boundary involution +
Stage-A Higgs rank-2 certificate + Stage-A Yukawa rank-3
certificate, all reified into `CarrierPremises`), and given any
integer pair `(qm, qp)` satisfying the **primitive oriented
trace-zero condition**, the resulting generator
`Y = -(1/3) P_- + (1/2) P_+` enjoys *simultaneously*:

  * `(qm, qp) = (-2, 3)`,
  * `tr Y = 0`,
  * `6 · Y² − Y − 1 = 0`.

This is the 3+2 hypercharge carrier in its final assembled form.
"3+2 carrier" — not "full SM hypercharge spectrum"; the latter
would require further derived representations (duals, exterior
powers, tensor products) that are out of scope.
-/
theorem hypercharge_carrier_packet
    (qm qp : ℤ)
    (htrace : 3 * qm + 2 * qp = 0)
    (hsign_m : qm < 0)
    (hsign_p : 0 < qp)
    (hgcd : Int.gcd qm qp = 1) :
    (qm = -2 ∧ qp = 3)
    ∧ LinearMap.trace K M cp.Y = 0
    ∧ (6 : ℕ) • (cp.Y * cp.Y) - cp.Y - 1 = (0 : Module.End K M) :=
  ⟨primitive_pair_eq_sm qm qp htrace hsign_m hsign_p hgcd,
   cp.trace_Y_eq_zero,
   cp.carrier_polynomial_Y⟩

end CarrierPremises

end TFPT.Carrier.CarrierData
