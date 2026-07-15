"""lazy01 -- theory contract: FORCING THE LAZY SPLIT FROM THE RESUMMED CLOCK
(the v486 [O] 'split selection' candidate closure; 2026-07-15).

v486 left open WHY the walk has (stay, hop) = (1/2, 1/6) instead of v327's
uniform (1/3, 1/3): 'selected by the physical spectrum, not yet derived from
a first principle'.  The named candidate was 'stay = 1/|Z2| as the
sheet-symmetric choice' -- vague.  This contract replaces it with a proved
ordering argument from the v124 resummed clock:

  C1 [E] RUNG READING: the one-step spectrum of the lazy rule M(1/2, 1/6)
     is EXACTLY the complete resummed-clock ladder below the wall,
         eig(M) = {(1 - n/N_fam) : n = 0, 1, 2} = {1, 2/3, 1/3},
     and v327's uniform rule instead puts its second pair mode ON the wall
     (eigenvalue 0 = 1 - 3/3): the degeneracy of v486 re-read as
     'odd channel collapsed to the wall'.
  C2 [E] DECK PARITY = RUNG INDEX: the sigma-even pair mode (1,1) carries
     rung n = 1 (survival 2/3) and the sigma-odd mode (1,-1) carries rung
     n = 2 (survival 1/3) -- each clock step n -> n+1 FLIPS the deck
     parity.  This is the structural home of the v486 parity assignment
     (omega_1 even-channel, omega_2 odd-channel) used by frb-parity-comb.
  C3 [E] FORCING: demanding (i) faithful realisation of the full ladder
     (eig(M) = {1, 2/3, 1/3} as a set -- no rung missing, no physical mode
     on the wall), (ii) Z2 equivariance (symmetric pair block), and
     (iii) non-negative rates, the assignment attractor->rung 0,
     even->rung 1, odd->rung 2 is the ONLY one possible (h >= 0 forces
     s + h >= s - h), and (s, h) = (1/2, 1/6) is UNIQUE.  The 'sheet-
     symmetric choice' candidate is superseded by this proof.
  C4 [E] BEND COROLLARY: the two comb tones of the empirical search
     program are one established number apart:
         omega_1 / omega_2 = rate(2)/rate(1) = log_{3/2} 3 = the v107/v124
     bend (2.70951...); equivalently omega_2 = omega_1 / bend.
  C5 [C/O] HONEST RESIDUAL: the channel count 3 = N_fam is forced by the
     clock wall (v124 pt 4); the clock ladder itself is an [I] identity on
     frozen spectra (v124) whose semiclassical derivation stays open
     (R1/[P]); the arity {|Z2|, N_fam} stays the anchor input.  NET: the
     v486 walk-level [O] 'split selection' REDUCES to established
     structure -- no independent choice remains at the walk level.

Contract only -- promotion decision after the summary gate.
"""
import json
from pathlib import Path

import sympy as sp

N_FAM = 3
Z2 = 2
P2 = 6  # |R+(A3)| hexagon size (v124)

results = {}


def rung(n):
    """v124 per-step survival of rung n: lambda_n^(1/p2) = 1 - n/N_fam."""
    return sp.Rational(N_FAM - n, N_FAM)


def rate(n):
    return -P2 * sp.log(rung(n))


def main():
    ok = True

    # ---- C1: one-step spectrum = complete clock ladder below the wall ----
    s0, h0 = sp.Rational(1, 2), sp.Rational(1, 6)
    M = sp.Matrix([[1, 0, 0], [0, s0, h0], [0, h0, s0]])
    eigs = set(M.eigenvals().keys())
    ladder = {rung(n) for n in range(N_FAM)}          # {1, 2/3, 1/3}
    wall = rung(N_FAM)                                # 0
    Mu = sp.Matrix([[1, 0, 0],
                    [0, sp.Rational(1, 3), sp.Rational(1, 3)],
                    [0, sp.Rational(1, 3), sp.Rational(1, 3)]])
    eigs_u = set(Mu.eigenvals().keys())
    c1 = (eigs == ladder) and (wall not in eigs) and (wall in eigs_u) \
        and (rung(2) not in eigs_u)
    results["C1_rung_reading"] = {
        "eig_lazy": sorted(str(e) for e in eigs),
        "clock_ladder_n012": sorted(str(e) for e in ladder),
        "wall_value_n3": str(wall),
        "eig_uniform": sorted(str(e) for e in eigs_u),
        "uniform_puts_odd_mode_on_wall": bool(wall in eigs_u),
        "pass": bool(c1)}
    ok &= c1

    # ---- C2: deck parity = rung index parity ----
    sigma = sp.Matrix([[0, 1], [1, 0]])               # deck involution on the pair
    B = sp.Matrix([[s0, h0], [h0, s0]])
    even_vec = sp.Matrix([1, 1])
    odd_vec = sp.Matrix([1, -1])
    lam_even = (B * even_vec)[0] / even_vec[0]
    lam_odd = (B * odd_vec)[0] / odd_vec[0]
    commutes = sp.simplify(B * sigma - sigma * B) == sp.zeros(2, 2)
    c2 = commutes and lam_even == rung(1) and lam_odd == rung(2)
    results["C2_deck_parity_equals_rung"] = {
        "B_commutes_with_sigma": bool(commutes),
        "sigma_even_mode_survival": str(lam_even), "is_rung_1": lam_even == rung(1),
        "sigma_odd_mode_survival": str(lam_odd), "is_rung_2": lam_odd == rung(2),
        "reading": "each clock step n->n+1 flips the deck parity",
        "pass": bool(c2)}
    ok &= c2

    # ---- C3: forcing (uniqueness incl. rung assignment) ----
    s, h = sp.symbols('s h', real=True)
    # symmetric pair block spectrum {s+h, s-h}; faithful ladder demand:
    # {s+h, s-h} = {2/3, 1/3} as a set -> two candidate assignments
    sol_A = sp.solve([sp.Eq(s + h, rung(1)), sp.Eq(s - h, rung(2))], [s, h],
                     dict=True)   # even->rung1, odd->rung2
    sol_B = sp.solve([sp.Eq(s + h, rung(2)), sp.Eq(s - h, rung(1))], [s, h],
                     dict=True)   # even->rung2, odd->rung1 (needs h < 0)
    hA = sol_A[0][h]
    hB = sol_B[0][h]
    c3 = (len(sol_A) == 1 and sol_A[0][s] == sp.Rational(1, 2)
          and hA == sp.Rational(1, 6) and hA >= 0
          and hB < 0)             # assignment B killed by non-negativity
    results["C3_forcing"] = {
        "assignment_even_rung1": {"s": str(sol_A[0][s]), "h": str(hA),
                                  "admissible_h_nonneg": bool(hA >= 0)},
        "assignment_even_rung2": {"s": str(sol_B[0][s]), "h": str(hB),
                                  "admissible_h_nonneg": bool(hB >= 0)},
        "conclusion": ("faithful ladder + Z2 symmetry + h >= 0 forces "
                       "UNIQUELY (s, h) = (1/2, 1/6) with even->rung1, "
                       "odd->rung2; the 'sheet-symmetric choice' candidate "
                       "is superseded by this proof"),
        "pass": bool(c3)}
    ok &= c3

    # ---- C4: bend corollary for the search tones ----
    # omega_i = 2 pi / gap_i with gap_even = p2 ln(3/2) (rung 1),
    # gap_odd = p2 ln 3 (rung 2)
    omega_1 = 2 * sp.pi / rate(1)
    omega_2 = 2 * sp.pi / rate(2)
    bend = sp.log(3) / sp.log(sp.Rational(3, 2))
    c4 = sp.simplify(omega_1 / omega_2 - bend) == 0
    results["C4_bend_corollary"] = {
        "omega_1": float(omega_1), "omega_2": float(omega_2),
        "omega1_over_omega2": float(omega_1 / omega_2),
        "bend_log32_3": float(bend),
        "identity": "omega_1/omega_2 = rate(2)/rate(1) = log_{3/2} 3 (v107 bend)",
        "pass": bool(c4)}
    ok &= c4

    # ---- C5: honest residual bookkeeping (typed, no computation claim) ----
    results["C5_honest_residual"] = {
        "channel_count_forced_by_wall": "3 = N_fam (v124 pt 4: rate(n)->oo at n=3)",
        "clock_status": "[I] identity on frozen spectra (v124); semiclassical "
                        "derivation open (R1/[P])",
        "arity_anchor": "{|Z2|, N_fam} = {2, 3} stays the input (P2/v23)",
        "net": "the v486 walk-level [O] 'split selection' reduces to v124 "
               "clock structure; no independent choice remains at the walk "
               "level",
        "pass": True}

    results["ALL_PASS"] = bool(ok)
    out = Path(__file__).with_name("lazy01_clock_rung_results.json")
    out.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    print("\nALL PASS" if ok else "\nFAILURES PRESENT")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
