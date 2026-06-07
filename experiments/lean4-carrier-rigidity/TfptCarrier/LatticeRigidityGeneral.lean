/-
  TFPT Carrier — General Lattice Rigidity
  ---------------------------------------

  The carrier rigidity theorem of TFPT Paper 2 picks out the integer
  pair `(q₋, q₊) = (-2, 3)` from the rank data `(dim E₋, dim E₊) = (3, 2)`.

  This module proves the *general* statement parametrised by arbitrary
  positive integer ranks `(m, n)`:

      For positive `m, n` and integers `qm, qp` satisfying
          m · qm + n · qp = 0
          qm < 0 < qp
          Int.gcd qm qp = 1
      one has  qm = -(n / d)  and  qp = m / d  where  d = Nat.gcd m n.

  The earlier specialisation `(m, n) = (3, 2)` becomes a one-line
  corollary: `d = gcd(3, 2) = 1`, hence `(qm, qp) = (-2, 3)`.

  Concretely the proof avoids hard-wiring the answer:

  - From `m · qm + n · qp = 0` one shows `(n / d) ∣ |qm|` and
    `(m / d) ∣ qp`.
  - The primitivity hypothesis `gcd(qm, qp) = 1` then forces the
    common scaling factor to be `1`.
  - Sign hypotheses select the unique signed representative
    `qm = -n/d, qp = m/d`.

  This module depends only on `Mathlib.Data.Int.GCD`, `Nat.GCD`, and
  basic `Int` lemmas. It is independent of `Polarization.lean`.
-/

import Mathlib.Data.Int.GCD
import Mathlib.Data.Nat.GCD.Basic
import Mathlib.RingTheory.Coprime.Basic
import Mathlib.RingTheory.Coprime.Lemmas
import Mathlib.Tactic.Linarith

namespace TFPT.Carrier.LatticeRigidityGeneral

open Int Nat

/--
**General lattice rigidity.**

For positive ranks `m, n` and integer charges `qm, qp` satisfying

    m * qm + n * qp = 0,
    qm < 0 < qp,
    Int.gcd qm qp = 1,

the pair `(qm, qp)` is uniquely determined:

    qm = -(n / d),    qp = m / d,    d := Nat.gcd m n.

Equivalent statement using `Int.natAbs`: `|qm| = n / d` and `qp = m / d`.

For the SM-relevant case `(m, n) = (3, 2)`, the gcd `d` is `1`, so
the conclusion specialises to `(qm, qp) = (-2, 3)`.
-/
theorem primitive_trace_free_pair_general
    (m n : ℕ)
    (hm : 0 < m) (hn : 0 < n)
    (qm qp : ℤ)
    (htrace : (m : ℤ) * qm + (n : ℤ) * qp = 0)
    (hneg : qm < 0)
    (hpos : 0 < qp)
    (hgcd : Int.gcd qm qp = 1) :
    qm = -((n / Nat.gcd m n : ℕ) : ℤ) ∧
    qp = ((m / Nat.gcd m n : ℕ) : ℤ) := by
  -- Notation.
  set d := Nat.gcd m n with hd_def
  set m' : ℕ := m / d with hm'_def
  set n' : ℕ := n / d with hn'_def
  -- d > 0 since m > 0 and n > 0.
  have hd_pos : 0 < d := Nat.gcd_pos_of_pos_left _ hm
  -- m = d * m', n = d * n'.
  have hm_eq : m = d * m' := (Nat.div_mul_cancel (Nat.gcd_dvd_left _ _)).symm.trans
    (by rw [Nat.mul_comm])
  have hn_eq : n = d * n' := (Nat.div_mul_cancel (Nat.gcd_dvd_right _ _)).symm.trans
    (by rw [Nat.mul_comm])
  -- gcd(m', n') = 1.
  have hcop : Nat.Coprime m' n' := Nat.coprime_div_gcd_div_gcd hd_pos
  -- Reduce the trace equation modulo d.
  -- m * qm + n * qp = d*m' * qm + d*n' * qp = d * (m' qm + n' qp) = 0.
  have htrace' : (m' : ℤ) * qm + (n' : ℤ) * qp = 0 := by
    have h1 : (d : ℤ) * ((m' : ℤ) * qm + (n' : ℤ) * qp) = 0 := by
      have := htrace
      rw [hm_eq, hn_eq] at this
      push_cast at this
      linarith
    have hd_ne : (d : ℤ) ≠ 0 := by exact_mod_cast Nat.pos_iff_ne_zero.mp hd_pos
    exact (mul_eq_zero.mp h1).resolve_left hd_ne
  -- Now `m' * qm = -n' * qp`.  Hence `n' ∣ m' * qm` and, using
  -- coprimality of `m'` and `n'`, we deduce `n' ∣ qm`.
  have hm'qm : (m' : ℤ) * qm = -((n' : ℤ) * qp) := by linarith
  have hdvd_n' : (n' : ℤ) ∣ qm := by
    have h1 : (n' : ℤ) ∣ ((m' : ℤ) * qm) := by
      rw [hm'qm]; exact dvd_neg.mpr (dvd_mul_right _ _)
    -- gcd((n' : ℤ), (m' : ℤ)) = 1
    have hcop' : IsCoprime ((n' : ℤ)) ((m' : ℤ)) := by
      rw [Int.isCoprime_iff_gcd_eq_one]
      have : Int.gcd ((n' : ℤ)) ((m' : ℤ)) = Nat.gcd n' m' := by
        simp [Int.gcd]
      rw [this, Nat.Coprime.symm hcop]
    exact hcop'.dvd_of_dvd_mul_left h1
  -- Write qm = -k * n'.  k > 0 from sign of qm.
  obtain ⟨k', hk'⟩ := hdvd_n'  -- qm = n' * k'
  -- Since qm < 0 and n' ≥ 0, we need k' < 0.  Let k = -k' > 0.
  have hn'_pos : 0 < (n' : ℤ) := by
    have : 0 < n' := by
      rw [hn'_def]
      exact Nat.div_pos (Nat.le_of_dvd hn (Nat.gcd_dvd_right _ _)) hd_pos
    exact_mod_cast this
  have hm'_pos : 0 < (m' : ℤ) := by
    have : 0 < m' := by
      rw [hm'_def]
      exact Nat.div_pos (Nat.le_of_dvd hm (Nat.gcd_dvd_left _ _)) hd_pos
    exact_mod_cast this
  have hk'_neg : k' < 0 := by
    rcases lt_trichotomy k' 0 with h | h | h
    · exact h
    · subst h; simp at hk'; omega
    · exfalso
      have : 0 ≤ (n' : ℤ) * k' := mul_nonneg hn'_pos.le h.le
      omega
  set k : ℤ := -k' with hk_def
  have hk_pos : 0 < k := by simp [hk_def]; exact hk'_neg
  have hqm_eq : qm = -((n' : ℤ) * k) := by
    have : qm = (n' : ℤ) * k' := hk'
    rw [this, hk_def]; ring
  -- Substituting into m' * qm = -n' * qp gives qp = m' * k.
  have hqp_eq : qp = (m' : ℤ) * k := by
    have h1 : (m' : ℤ) * (-((n' : ℤ) * k)) = -((n' : ℤ) * qp) := by
      rw [← hqm_eq]; exact hm'qm
    have h2 : -((m' : ℤ) * ((n' : ℤ) * k)) = -((n' : ℤ) * qp) := by
      have : (m' : ℤ) * (-((n' : ℤ) * k)) = -((m' : ℤ) * ((n' : ℤ) * k)) := by ring
      linarith
    have h3 : (m' : ℤ) * ((n' : ℤ) * k) = (n' : ℤ) * qp := by linarith
    have h4 : (n' : ℤ) * ((m' : ℤ) * k) = (n' : ℤ) * qp := by linarith
    have hn'_ne : (n' : ℤ) ≠ 0 := ne_of_gt hn'_pos
    exact (mul_left_cancel₀ hn'_ne h4).symm
  -- Now `Int.gcd qm qp = k.natAbs` because qm = -n' k, qp = m' k and gcd(n', m') = 1.
  have hgcd_k : Int.gcd qm qp = k.natAbs := by
    rw [hqm_eq, hqp_eq]
    -- gcd(-n' k, m' k) = |k| * gcd(-n', m') = |k| * gcd(n', m') = |k| * 1 = |k|
    have e1 : Int.gcd (-((n' : ℤ) * k)) ((m' : ℤ) * k)
            = Int.gcd ((n' : ℤ) * k) ((m' : ℤ) * k) := by
      rw [Int.gcd, Int.gcd]
      congr 1
      exact Int.natAbs_neg _
    rw [e1]
    -- Pull out k: gcd(n' * k, m' * k) = |k| * gcd(n', m')
    have e2 : Int.gcd ((n' : ℤ) * k) ((m' : ℤ) * k) = k.natAbs * Nat.gcd n' m' := by
      rw [show ((n' : ℤ) * k) = k * (n' : ℤ) by ring,
          show ((m' : ℤ) * k) = k * (m' : ℤ) by ring,
          Int.gcd_mul_left]
      rfl
    rw [e2]
    rw [show Nat.gcd n' m' = 1 from Nat.Coprime.symm hcop]
    simp
  have hk_abs : k.natAbs = 1 := by rw [hgcd_k] at hgcd; exact hgcd
  -- k > 0 and |k| = 1 force k = 1.
  have hk1 : k = 1 := by
    have := Int.natAbs_eq k
    rcases this with h | h
    · rw [h, hk_abs]; rfl
    · exfalso
      have : k = -(1 : ℤ) := by rw [h, hk_abs]; rfl
      linarith
  -- Finally substitute k = 1 and read off (qm, qp).
  refine ⟨?_, ?_⟩
  · rw [hqm_eq, hk1, mul_one]
  · rw [hqp_eq, hk1, mul_one]

/--
**Specialised corollary**: the SM case `(m, n) = (3, 2)`.

Since `Nat.gcd 3 2 = 1`, the general theorem reduces to
`(qm, qp) = (-2, 3)`.
-/
theorem primitive_trace_free_pair_3_2
    (qm qp : ℤ)
    (htrace : 3 * qm + 2 * qp = 0)
    (hneg : qm < 0)
    (hpos : 0 < qp)
    (hgcd : Int.gcd qm qp = 1) :
    qm = -2 ∧ qp = 3 := by
  have := primitive_trace_free_pair_general 3 2
    (by decide) (by decide) qm qp
    (by push_cast; linarith) hneg hpos hgcd
  obtain ⟨h1, h2⟩ := this
  refine ⟨?_, ?_⟩
  · rw [h1]; decide
  · rw [h2]; decide

end TFPT.Carrier.LatticeRigidityGeneral
