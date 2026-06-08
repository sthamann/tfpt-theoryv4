"""v53 -- the compiler core: everything from the single pair (g_car, N_fam)=(5,3).

This is the "big-picture" consolidation.  It records three exact structural facts
that compress the whole integer skeleton of the compiler:

(1) GENERATOR LADDER.  The two boundary integers (g_car, N_fam)=(5,3) generate the
    core ladder by sum and difference:
        rank(E8) = g_car + N_fam = 8   (the D5(+)A3 rank split)
        |Z2|     = g_car - N_fam = 2   (carrier - family = sheet parity)

(2) PYTHAGOREAN MASS-VOLUME SPLIT (Dirac difference-of-squares).  (N_fam,|mu4|,g_car)
    = (3,4,5) is THE Pythagorean triple, g_car^2 = N_fam^2 + |mu4|^2, and this is not
    decorative: the grand-mass-volume exponent Delta_Y = g_car^2 = 25 (det M_SM ~
    phi0^25, v46) splits over the sectors exactly as
        Delta_Y = g_car^2 = N_fam^2  +  (g_car-N_fam)(g_car+N_fam)
                          = N_fam^2  +  |Z2|*rank(E8)
                          =   9      +     16
                          = down     +  (up+lep) = dim S^+.
    i.e. the down-sector mass exponent is N_fam^2 and the up+lepton exponent is the
    difference of squares |Z2|*rank(E8) = dim S^+ = 16.  (K-row sums (6,9,10), v37/v46.)

(3) ANCHOR CHAR-POLY (Wolfram uniqueness).  The anchor a=(1,1,2) is the UNIQUE 3-element
    multiset (entries in 0..6) whose elementary symmetric functions are the compiler
    atoms (|mu4|, g_car, |Z2|)=(4,5,2); equivalently its characteristic polynomial is
        chi_a(t) = (t-1)^2 (t-2) = t^3 - |mu4| t^2 + g_car t - |Z2|,
    so the compiler atoms ARE the coefficients of the anchor's char-poly.

All three are exact [I].  They are new READINGS/syntheses of atoms already verified
in v23/v37/v46/v47, not new physical inputs.
"""
import sympy as sp
from itertools import combinations_with_replacement
from tfpt_constants import check, summary, reset, g_car, N_fam

mu4 = 4
Z2 = 2


def run():
    reset()
    print("v53  compiler core: everything from (g_car, N_fam)=(5,3)")

    # ---- (1) generator ladder ----
    check("rank(E8) = g_car + N_fam = 8", g_car + N_fam == 8)
    check("|Z2| = g_car - N_fam = 2 (carrier - family = sheet parity)", g_car - N_fam == Z2)
    check("the 5 core integers {|Z2|,N_fam,|mu4|,g_car,rank E8}={2,3,4,5,8} all flow from (5,3)",
          sorted({g_car - N_fam, N_fam, mu4, g_car, g_car + N_fam}) == [2, 3, 4, 5, 8])

    # ---- (2) Pythagorean mass-volume split ----
    check("(N_fam,|mu4|,g_car)=(3,4,5) Pythagorean: g_car^2 = N_fam^2 + |mu4|^2 = 25",
          g_car**2 == N_fam**2 + mu4**2 == 25)
    K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
    rows = [sum(K.row(i)) for i in range(3)]  # (up,down,lep) mass-volume exponents
    check("K row sums (up,down,lep) = (6,9,10), total = g_car^2 = 25 = Delta_Y", rows == [6, 9, 10] and sum(rows) == 25)
    check("down exponent = N_fam^2 = 9", rows[1] == N_fam**2 == 9)
    check("up+lep exponent = (g_car-N_fam)(g_car+N_fam) = |Z2|*rank(E8) = dim S+ = 16 [diff of squares]",
          rows[0] + rows[2] == (g_car - N_fam) * (g_car + N_fam) == Z2 * (g_car + N_fam) == 16)

    # ---- (3) anchor char-poly + uniqueness ----
    a = (1, 1, 2)
    e1 = a[0] + a[1] + a[2]
    e2 = a[0] * a[1] + a[0] * a[2] + a[1] * a[2]
    e3 = a[0] * a[1] * a[2]
    check("e_k(1,1,2) = (|mu4|,g_car,|Z2|) = (4,5,2)", (e1, e2, e3) == (mu4, g_car, Z2))
    t = sp.symbols('t')
    chi = sp.expand((t - 1)**2 * (t - 2))
    check("char poly chi_a(t) = (t-1)^2(t-2) = t^3 - |mu4|t^2 + g_car t - |Z2|",
          chi == t**3 - mu4 * t**2 + g_car * t - Z2)
    hits = [m for m in combinations_with_replacement(range(0, 7), 3)
            if (m[0] + m[1] + m[2], m[0] * m[1] + m[0] * m[2] + m[1] * m[2], m[0] * m[1] * m[2]) == (mu4, g_car, Z2)]
    check("anchor (1,1,2) is the UNIQUE 3-multiset (0..6) with e_k=(|mu4|,g_car,|Z2|)", hits == [(1, 1, 2)])
    return summary("v53 compiler core")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
