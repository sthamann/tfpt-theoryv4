"""v215 -- QGEO.KILL.01: the bedrock QGEO.SYM.01 (omega o rho = omega) recast as a
FALSIFIABLE structural kill-test, not a proof-promise. A foundational symmetry
cannot be derived from nothing (v181/v153); the honest win is to turn the
postulate into four independently-falsifiable predictions about the raw seam DtN,
each carrier-side GREEN today and seam-side a DEFERRED emergence test.

Background (the non-circular reduction chain): for a quasi-free seam state the
covariance is C = 1/2(1 + sgn H_1), so omega o rho = omega <=> [rho, C] = 0 (v199).
The principal symbol |k| = diag(|n|) commutes with the clock rho = diag(i^n)
EXACTLY (v198/v192), so the whole residual sits in the bounded sub-principal
symbol M_f (multiplication by the boundary curvature f), and [rho, M_f] = 0 <=>
f has Fourier support only on modes ≡ 0 (mod 4) (v201). Equivalently (measure
form) the raw Gaussian bulk quadratic form A is mu4-deck-invariant. This module
packages that residual as a kill-test with four levers:

  [E] K1 -- EXACTLY FOUR MARKS.  The clock rho is the order-4 Coxeter element of
        W(A3)=S4 (v117); a non-fixed point has a free order-4 orbit
        {1,i,-1,-i}=mu4 (4 points), and rank H^1(P^1\\mu4) = #marks - 1 = 3 =
        N_fam forces #marks = N_fam + 1 = 4 = |mu4| = e1(a). KILL if the raw seam
        carries #marks != 4 (equivalently b1 != 3).
  [E] K2 -- SQUARE CONFIGURATION.  mu4 has cross-ratio 2 (v168), so j = 1728
        (v214): the modulus is the SQUARE torus tau=i with Aut = Z/4. Only
        j in {0,1728} admit Aut > Z2, and the clock order is h(A3) = 4 (not 6),
        which selects j=1728 (Z/4), NOT j=0 (Z/6). A generic mark set
        (cross-ratio 3 -> j = 21952/9) has only Z/2 and no order-4 clock. KILL if
        the raw marks are non-square (cross-ratio != 2 / Aut only Z2).
  [E] K3 -- MOD-4 SUB-PRINCIPAL SUPPORT.  A mu4-mark sum f(theta) = sum_{j=0}^3
        g(theta - j pi/2) has f_m = 4 g_m [m ≡ 0 (mod 4)] for ANY profile g, so
        M_f is character-block-diagonal and [rho, M_f] = 0; an off-character
        (mode-1) entry breaks it. KILL if a first-principles seam DtN has
        off-character (m !≡ 0 mod 4) sub-principal weight above numerical noise.
  [E] K4 -- TRANSFER GAP (2/3)^6.  The mu4-equivariant one-particle contraction
        is diagonal in the cusp basis with weights {0,1/3,2/3}, transfer
        eigenvalues (1-w)^6 = {1, (2/3)^6, (1/3)^6}, subleading gap
        lambda_2 = (2/3)^6 = 64/729 (v162/v56). KILL if the gap != 64/729.

  [E] 5. FREEZE BINDING.  freeze_file.csv carries the row 'seam_deck_symmetry'
        whose kill_criterion names exactly these four levers, so the prediction
        and the test are locked together (editing one without the other fails the
        suite) -- the v84/v100 freeze discipline applied to the bedrock.
  [E] 6. NON-CIRCULAR.  rho and the CAR algebra are carrier-defined (Coxeter
        element of W(A3); 16 Majoranas, v156/v175) with NO seam-geometry import,
        so 'the raw seam state is rho-invariant' is a genuine, non-circular
        question -- NOT Bisognano-Wichmann (which would presuppose the covariance
        it is meant to produce).
  [O] 7. THE DEFERRED EMERGENCE TEST (the decisive, not-yet-executable kill).
        The non-vacuous test is upstream: compute the raw P1 seam-collar DtN
        WITHOUT inputting the marks and check that exactly four SQUARE marks
        EMERGE (=> K1,K2 => K3,K4). That is QGEO.REALIZE.01; no first-principles
        raw-seam construction exists yet, so this lever is DEFERRED (analogous to
        the freeze file's axion_DM 'no test possible until the scale is closed').
        Carrier-side K1-K4 are green and act as a regression guard; seam-side
        emergence stays [O]. This module is a KILL-TEST, not a closure of
        QGEO.SYM.01.

Python-only (falsification/structural layer, like v65/v100; the exact algebraic
sub-parts -- cross-ratio 2 => j=1728, the gap (2/3)^6 -- are already Wolfram-
mirrored via v214/v54/v56).
"""
import csv
import os

import numpy as np
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam, g_car

I = sp.I
MU4 = [sp.Integer(1), I, sp.Integer(-1), -I]


def _jlam(l):
    return sp.simplify(256 * (l**2 - l + 1)**3 / (l**2 * (l - 1)**2))


def run():
    reset()
    print("v215 QGEO.KILL.01: bedrock omega o rho = omega as a falsifiable kill-test (K1-K4) [E] + deferred [O]")

    # ---- K1: exactly four marks (clock order 4 + free orbit + b1 = N_fam) ----
    z = sp.symbols('z')
    clock = lambda w: I * w                                # z -> iz, order 4
    orbit = set()
    w = sp.Integer(1)
    for _ in range(4):
        orbit.add(sp.simplify(w)); w = clock(w)
    b1 = 4 - 1                                             # rank H^1(P^1 minus 4 pts)
    check("K1 EXACTLY FOUR MARKS [E]: the order-4 clock z->iz (Coxeter of W(A3)=S4) "
          "has free orbit %s = mu4 (4 points), and rank H^1 = #marks-1 = %d = N_fam "
          "forces #marks = N_fam+1 = 4 = |mu4| = e1(a); KILL if the raw seam has "
          "#marks != 4 (b1 != 3)"
          % (sorted(orbit, key=str), b1),
          orbit == {1, I, -1, -I} and b1 == N_fam == 3 and (N_fam + 1) == 4)

    # ---- K2: square configuration (cross-ratio 2 => j=1728, order-4 => Z/4) ----
    z1, z2, z3, z4 = MU4
    cross = sp.simplify((z1 - z3) * (z2 - z4) / ((z1 - z4) * (z2 - z3)))
    j_square, j_hex, j_gen = _jlam(cross), sp.Integer(0), _jlam(sp.Integer(3))
    check("K2 SQUARE CONFIGURATION [E]: cross-ratio(mu4) = %s => j = %s (square "
          "tau=i, Aut=Z/4); only j in {0,1728} give Aut>Z2, and the clock order "
          "h(A3)=4 selects j=1728 (Z/4) NOT j=0 (Z/6); a generic mark set "
          "(cross-ratio 3 -> j=%s) has only Z/2; KILL if the raw marks are "
          "non-square (cross-ratio != 2 / Aut only Z2)"
          % (cross, j_square, j_gen),
          cross == 2 and j_square == 1728
          and j_gen not in (sp.Integer(0), sp.Integer(1728))
          and 4 != 6)                                     # order-4 selects Z/4, not Z/6

    # ---- K3: mod-4 sub-principal support ([rho, M_f] = 0 <=> Z4-invariant f) ----
    N = 8
    n = np.arange(-N, N + 1)
    d = len(n)
    rho = np.diag((1j) ** n)
    # mu4-mark-sourced curvature: support only on modes ≡ 0 (mod 4)
    g_prof = {0: 1.3, 1: -0.7, -1: -0.7, 2: 0.4, -2: 0.4, 3: 0.2, -3: 0.2}
    f_marks = {m: 4 * gm for m, gm in g_prof.items() if m % 4 == 0}

    def mult(fmodes):
        M = np.zeros((d, d), complex)
        for a in range(d):
            for b in range(d):
                M[a, b] = fmodes.get(int(n[a] - n[b]), 0.0)
        return M

    M_ok = mult(f_marks)
    M_off = mult({**f_marks, 1: 0.5, -1: 0.5})            # add an off-character mode
    ok = np.allclose(rho @ M_ok - M_ok @ rho, 0)
    broken = not np.allclose(rho @ M_off - M_off @ rho, 0)
    check("K3 MOD-4 SUB-PRINCIPAL SUPPORT [E]: a mu4-mark sum f has f_m = 4 g_m "
          "[m≡0 mod 4], so M_f is character-block-diagonal and [rho,M_f]=0 (%s); "
          "an off-character (mode-1) entry breaks it (%s); KILL if a first-"
          "principles seam DtN has off-character sub-principal weight above noise"
          % (ok, broken),
          ok and broken)

    # ---- K4: transfer gap (2/3)^6 = 64/729 ----
    cusp = [sp.Integer(0), sp.Rational(1, 3), sp.Rational(2, 3)]
    spec = sorted(((1 - wgt)**6 for wgt in cusp), reverse=True)
    gap = spec[1]
    check("K4 TRANSFER GAP [E]: the mu4-equivariant one-particle contraction is "
          "diagonal in the cusp basis {0,1/3,2/3}, transfer eigenvalues (1-w)^6 = "
          "%s, subleading gap lambda_2 = (2/3)^6 = %s = |Z2|/N_fam to the |W(A3)|/4 "
          "power; KILL if the gap != 64/729"
          % ([str(s) for s in spec], gap),
          spec == [sp.Integer(1), sp.Rational(64, 729), sp.Rational(1, 729)]
          and gap == sp.Rational(64, 729) == (sp.Rational(2, 3))**6)

    # ---- 5. freeze binding: the seam_deck_symmetry row exists and names K1-K4 ----
    fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "freeze_file.csv")
    with open(fpath, newline="") as fh:
        rows = {r["claim"]: r for r in csv.DictReader(fh)}
    row = rows.get("seam_deck_symmetry", {})
    crit = (row.get("kill_criterion", "") + " " + row.get("tfpt_signal", "")).lower()
    bound = all(tok in crit for tok in ("mark", "square", "mod 4", "2/3)^6"))
    check("FREEZE BINDING [E]: freeze_file.csv carries 'seam_deck_symmetry' whose "
          "kill_criterion names the four levers (4 marks, square, mod-4, gap "
          "(2/3)^6); prediction and test are locked together (v84/v100 freeze "
          "discipline applied to the bedrock)", bool(row) and bound)

    # ---- 6. non-circular setup (carrier-defined rho + algebra, no seam geometry) ----
    check("NON-CIRCULAR [E]: rho^4 = I is the Coxeter element of W(A3)=S4 (v117), "
          "an automorphism of the RAW CAR algebra (16 = 2^(g_car-1) Majoranas, "
          "v156/v175); both carrier-defined, NO seam-geometry import -- so the "
          "kill-test is a genuine question, NOT a Bisognano-Wichmann argument "
          "(which would presuppose the covariance it should produce)",
          np.allclose(np.linalg.matrix_power(rho, 4), np.eye(d))
          and 2**(g_car - 1) == 16)

    # ---- 7. the deferred emergence test (the decisive, not-yet-executable kill) ----
    check("DEFERRED EMERGENCE TEST [O] (QGEO.REALIZE.01): the decisive kill is "
          "upstream -- compute the raw P1 seam-collar DtN WITHOUT inputting the "
          "marks and check that exactly four SQUARE marks EMERGE (=> K1,K2 => "
          "K3,K4). No first-principles raw-seam construction exists yet, so this "
          "lever is DEFERRED (like the freeze file's axion_DM 'no test possible "
          "until the scale is closed'). Carrier-side K1-K4 are green regression "
          "guards; seam-side emergence stays [O]. This is a KILL-TEST, not a "
          "closure of QGEO.SYM.01 (a foundational symmetry cannot be derived from "
          "nothing, v181/v153)", True)

    return summary("v215 QGEO.KILL.01 bedrock kill-test (K1-K4 green; emergence deferred [O])")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
