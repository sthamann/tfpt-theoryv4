/-
  TFPT Carrier — Layer 3: Discrete Rigidity (SM case)
  ---------------------------------------------------

  The SM-relevant carrier rigidity theorem `(q_-, q_+) = (-2, 3)`
  is now a one-line specialisation of the *general* lattice
  rigidity theorem proved in `LatticeRigidityGeneral.lean`. The
  general theorem covers any positive rank pair `(m, n)`; setting
  `(m, n) = (3, 2)` recovers the SM case.

  This separation matters: hard-coding `(-2, 3)` would conflate
  *theorem* with *answer*. Promoting the rigidity result to its
  general parametric form makes the integer answer a consequence,
  not an input.
-/

import TfptCarrier.LatticeRigidityGeneral

namespace TFPT.Carrier.Rigidity

/--
**Discrete carrier rigidity for the SM case `(m, n) = (3, 2)`.**

Let `q_-, q_+ : ℤ` satisfy

  * `3 q_- + 2 q_+ = 0` (trace-zero / determinant-preserving),
  * `q_- < 0 < q_+`     (sign of polarization),
  * `Int.gcd q_- q_+ = 1` (primitive lattice vector).

Then `q_- = -2` and `q_+ = 3`. This is the unique solution; no other
integer pair is compatible with the three hypotheses.

Specialisation of
`TFPT.Carrier.LatticeRigidityGeneral.primitive_trace_free_pair_general`
to `(m, n) = (3, 2)`.
-/
theorem unique_carrier_pair
    (qm qp : ℤ)
    (htrace   : 3 * qm + 2 * qp = 0)
    (hsign_m  : qm < 0)
    (hsign_p  : 0 < qp)
    (hgcd     : Int.gcd qm qp = 1) :
    qm = -2 ∧ qp = 3 :=
  TFPT.Carrier.LatticeRigidityGeneral.primitive_trace_free_pair_3_2
    qm qp htrace hsign_m hsign_p hgcd

end TFPT.Carrier.Rigidity
