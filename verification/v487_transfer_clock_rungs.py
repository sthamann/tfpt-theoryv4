"""v487 -- HYP.REWRITE.03: the lazy split (1/2, 1/6) is FORCED by the
resummed clock -- the v486 [O] 'split selection' closes onto v124
structure.  The walk's one-step spectrum is the COMPLETE clock ladder
below the wall; deck parity = rung index; the two search tones are one
bend apart.  Sharpens HYP.REWRITE.02; no gate closes.

Background.  v486 exhibited the unique lazy Z2-pair walk (stay, hop,
leak) = (1/2, 1/6, 1/3) generating the full transfer spectrum
{1, (2/3)^6, (1/3)^6}, but left the SPLIT SELECTION open: '(1/2, 1/6)
vs uniform (1/3, 1/3) is selected by the physical spectrum, not yet
derived from a first principle' (named candidate: sheet-symmetric
choice -- vague).  The v124 resummed clock reads the transfer
eigenvalues as lambda_n = (1 - n/N_fam)^{p_2} with a POLE (wall) at
n = N_fam.  This module proves the split selection is clock-ladder
faithfulness -- definitional for a full-spectrum generator:

  [E] 1. RUNG READING: the one-step spectrum of the lazy rule is
        EXACTLY the complete resummed-clock ladder below the wall,
        eig(M) = {1 - n/3 : n = 0, 1, 2} = {1, 2/3, 1/3}; v327's
        uniform rule instead puts its second pair mode ON the wall
        (0 = 1 - 3/3) -- the v486 degeneracy re-read as 'odd channel
        collapsed to the wall'.
  [E] 2. DECK PARITY = RUNG INDEX: the sigma-even pair mode (1,1)
        carries rung n = 1 (survival 2/3), the sigma-odd mode (1,-1)
        carries rung n = 2 (survival 1/3); each clock step n -> n+1
        flips the deck parity.  This is the structural home of the
        v486 parity assignment (omega_1 even-channel, omega_2
        odd-channel) tested by the frb-parity-comb search.
  [E] 3. FORCING: demanding (i) the faithful ladder (no rung missing,
        no physical mode on the wall -- definitional for a
        full-spectrum generator), (ii) Z2 equivariance (symmetric pair
        block), (iii) non-negative rates, BOTH the split (s, h) =
        (1/2, 1/6) AND the assignment even -> rung 1, odd -> rung 2
        are UNIQUE (the swapped assignment needs h = -1/6 < 0).  The
        v486 'sheet-symmetric choice' candidate is superseded by this
        proof; the walk-level [O] closes.
  [E] 4. BEND COROLLARY: the two comb tones of the empirical search
        program are one established number apart,
            omega_1 / omega_2 = rate(2)/rate(1) = log_{3/2} 3
        (the v107/v124 bend, 2.70951...) -- the tone ratio of the
        parity-comb search IS the bend of the pulsar-clock search.
  [O] 5. HONEST RESIDUAL: the channel count 3 = N_fam is forced by the
        clock wall (v124 pt 4); the ladder itself is an [I] identity
        on frozen spectra whose semiclassical derivation stays open
        (R1/[P]); the arity {|Z2|, N_fam} = {2, 3} stays the anchor
        input.  NET: no independent choice remains at the walk level.

Contract provenance: experiments/theory-contracts/
lazy01_clock_rung_forcing.py (2026-07-15).  Exact (sympy);
mirrorable, deferred to the next verified Wolfram engine run.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam, g_car

Z2 = g_car - N_fam                    # |Z2| = 2
P2 = 6                                # |R+(A3)| hexagon size (v124)


def rung(n):
    return sp.Rational(N_fam - n, N_fam)


def rate(n):
    return -P2 * sp.log(rung(n))


def run():
    reset()
    print("v487  HYP.REWRITE.03: the lazy split is forced by the resummed "
          "clock (ladder faithfulness); deck parity = rung index")

    s0, h0 = sp.Rational(1, 2), sp.Rational(1, 6)
    M = sp.Matrix([[1, 0, 0], [0, s0, h0], [0, h0, s0]])
    Mu = sp.Matrix([[1, 0, 0],
                    [0, sp.Rational(1, 3), sp.Rational(1, 3)],
                    [0, sp.Rational(1, 3), sp.Rational(1, 3)]])

    # 1. rung reading
    eigs = set(M.eigenvals().keys())
    ladder = {rung(n) for n in range(N_fam)}
    wall = rung(N_fam)
    eigs_u = set(Mu.eigenvals().keys())
    check("RUNG READING [E]: the lazy rule's one-step spectrum is EXACTLY "
          "the complete v124 clock ladder below the wall, eig(M) = "
          "{1 - n/3 : n = 0, 1, 2} = {1, 2/3, 1/3}; v327's uniform rule "
          "puts its second pair mode ON the wall (0 = 1 - 3/3) -- the v486 "
          "degeneracy re-read as 'odd channel collapsed to the wall'",
          eigs == ladder and wall not in eigs
          and wall in eigs_u and rung(2) not in eigs_u)

    # 2. deck parity = rung index
    sigma = sp.Matrix([[0, 1], [1, 0]])
    B = sp.Matrix([[s0, h0], [h0, s0]])
    lam_even = (B * sp.Matrix([1, 1]))[0]
    lam_odd = (B * sp.Matrix([1, -1]))[0]
    check("DECK PARITY = RUNG INDEX [E]: [B, sigma] = 0; the sigma-even "
          "pair mode carries rung n = 1 (survival 2/3), the sigma-odd mode "
          "rung n = 2 (survival 1/3) -- each clock step flips the deck "
          "parity; the structural home of the v486 parity assignment "
          "(omega_1 even-channel, omega_2 odd-channel; frb-parity-comb)",
          sp.simplify(B * sigma - sigma * B) == sp.zeros(2, 2)
          and lam_even == rung(1) and lam_odd == rung(2))

    # 3. forcing (split + assignment unique)
    s, h = sp.symbols('s h', real=True)
    sol_A = sp.solve([sp.Eq(s + h, rung(1)), sp.Eq(s - h, rung(2))],
                     [s, h], dict=True)
    sol_B = sp.solve([sp.Eq(s + h, rung(2)), sp.Eq(s - h, rung(1))],
                     [s, h], dict=True)
    check("FORCING [E]: faithful ladder (no rung missing, no physical mode "
          "on the wall -- definitional for a full-spectrum generator) + Z2 "
          "equivariance + rates >= 0 force UNIQUELY both the split (s, h) "
          "= (1/2, 1/6) AND the assignment even -> rung 1, odd -> rung 2 "
          "(the swapped assignment needs h = -1/6 < 0, inadmissible); the "
          "v486 [O] 'split selection' closes at the walk level",
          len(sol_A) == 1 and sol_A[0][s] == sp.Rational(1, 2)
          and sol_A[0][h] == sp.Rational(1, 6) and sol_A[0][h] >= 0
          and sol_B[0][h] < 0)

    # 4. bend corollary
    omega_1 = 2 * sp.pi / rate(1)
    omega_2 = 2 * sp.pi / rate(2)
    bend = sp.log(3) / sp.log(sp.Rational(3, 2))
    check("BEND COROLLARY [E]: the two comb tones of the search program "
          "are one bend apart: omega_1/omega_2 = rate(2)/rate(1) = "
          "log_{3/2} 3 = 2.70951... (v107/v124) -- the parity-comb tone "
          "ratio IS the pulsar-clock bend",
          sp.simplify(omega_1 / omega_2 - bend) == 0)

    # 5. honest residual
    check("HONEST RESIDUAL [O]: the channel count 3 = N_fam is forced by "
          "the clock wall (v124 pt 4); the ladder is an [I] identity on "
          "frozen spectra with the semiclassical derivation open (R1/[P]); "
          "the arity {|Z2|, N_fam} = {2, 3} stays the anchor input; no "
          "independent choice remains at the walk level",
          {Z2, N_fam} == {2, 3} and sp.limit(-P2 * sp.log(1 - sp.Symbol('x')
          / N_fam), sp.Symbol('x'), N_fam, dir='-') == sp.oo)

    return summary("v487 HYP.REWRITE.03: the lazy split (1/2, 1/6) is "
                   "FORCED -- the walk's spectrum is the complete v124 "
                   "clock ladder below the wall (uniform rule = odd mode "
                   "on the wall); deck parity = rung index (home of the "
                   "parity assignment); omega_1/omega_2 = bend; the v486 "
                   "walk-level [O] closes onto v124 structure (arity + "
                   "clock derivation stay the open inputs)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
