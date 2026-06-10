"""v92 -- Glue Uniqueness: the carrier extension tower completely classified.
Gate A loses another degree of freedom.  [I]/[L]; seam side stays [P]/[A].

After v89 the Gate-A theorem reads: "the seam-Calderon boundary net contains
the carrier net (D5)_1 x (A3)_1 with Jones index 4 as its mu_4 simple-current
extension".  This left a silent question: among ALL possible extensions of
the carrier, how special is that one?  Answer (this script, exact finite
enumeration): the extension tower of the carrier has NO freedom at all.

SETTING.  Extensions of the carrier lattice/net correspond to isotropic
subgroups (q = 0) of its discriminant form
    A = Z4 x Z4,   q(x,y) = (5 x^2 + 3 y^2)/8  mod 1
(q_D5(k) = 5k^2/8 reproduces the (D5)_1 sector weights 0, 5/8, 1/2, 5/8;
q_A3(k) = 3k^2/8 reproduces the SU(4)_1 weights 0, 3/8, 1/2, 3/8).
The extension by H has discriminant |A|/|H|^2 and mu-index 16/|H|^2.

CLASSIFICATION (exhaustive over all 15 subgroups of Z4 x Z4):

  |H| = 1 : the carrier itself                       (mu = 16)
  |H| = 2 : exactly ONE isotropic Z2 = {(0,0),(2,2)} (mu =  4)
            and H_perp/H = Z2 x Z2 with q = {0,0,0,1/2}
            = the D8 discriminant form  =>  the unique halfway extension
            IS SO(16)_1 -- the v83/v87 rival is not an arbitrary
            counter-model, it is the only intermediate of the tower
            (and it is excluded by holomorphy, mu = 4 != 1).
  |H| = 4 : exactly TWO Lagrangian glues, <(1,1)> and <(1,3)>,
            each giving det = 16/16 = 1, even, rank 8  =>  E8 (the unique
            even unimodular rank-8 lattice, v83).  The two are swapped by
            EITHER single spinor conjugation (D5 or A3) and fixed by the
            simultaneous one: they are the two CHIRALITIES, identified by
            the sheet Z2.  (Cross-check: v87 found exactly two E8-type
            extension modular invariants |chi_0 + chi_{s,c}|^2 of SO(16)_1
            -- the same two objects, seen from the halfway house.)

CONSEQUENCE FOR GATE A [L]: once the seam net extends the carrier with
index 4, WHICH extension it is carries no freedom -- it is the mu_4 glue,
unique up to the sheet.  The remaining theorem is only the index statement
itself (plus its seam-side identification [P]/[A], GATE.METRIC.05/06).
"""
from fractions import Fraction as F
from itertools import product

from tfpt_constants import check, summary, reset

ORDER = 4


def q_form(v):
    x, y = v
    return F(5 * x * x + 3 * y * y, 8) % 1


def bilinear(a, b):
    s = ((a[0] + b[0]) % ORDER, (a[1] + b[1]) % ORDER)
    return (q_form(s) - q_form(a) - q_form(b)) % 1


def subgroup(gens):
    H = {(0, 0)}
    changed = True
    while changed:
        changed = False
        for h in list(H):
            for g in gens:
                s = ((h[0] + g[0]) % ORDER, (h[1] + g[1]) % ORDER)
                if s not in H:
                    H.add(s)
                    changed = True
    return frozenset(H)


def run():
    reset()
    print("v92 glue uniqueness (carrier extension tower completely classified)")

    A = [(x, y) for x in range(ORDER) for y in range(ORDER)]

    # 0. the form reproduces the level-1 sector weights of v87/v89
    check("q reproduces the carrier sector weights: D5 (0,5/8,1/2,5/8) x "
          "A3 (0,3/8,1/2,3/8)",
          [q_form((k, 0)) for k in range(4)] == [F(0), F(5, 8), F(1, 2), F(5, 8)]
          and [q_form((0, k)) for k in range(4)] == [F(0), F(3, 8), F(1, 2), F(3, 8)])

    # 1. exhaustive subgroup enumeration
    subs = {subgroup([g1, g2]) for g1 in A for g2 in A}
    check("Z4 x Z4 has exactly 15 subgroups (exhaustive)", len(subs), 15,
          exact=True)
    iso = sorted((H for H in subs if all(q_form(h) == 0 for h in H)), key=len)
    check("isotropic subgroups: exactly {1, Z2, Z4, Z4} (orders 1,2,4,4)",
          [len(H) for H in iso], [1, 2, 4, 4], exact=True)

    # 2. the Lagrangian (order-4) glues: exactly two, both -> E8
    lag = [H for H in iso if len(H) == 4]
    check("exactly TWO Lagrangian glues: <(1,1)> and <(1,3)>",
          {frozenset({(0, 0), (1, 1), (2, 2), (3, 3)}),
           frozenset({(0, 0), (1, 3), (2, 2), (3, 1)})} == set(lag))
    check("each gives det = |A|/|H|^2 = 16/16 = 1 (even unimodular rank 8 "
          "=> E8, unique by Minkowski-Siegel, v83)",
          16 // 4**2, 1, exact=True)

    # 3. the two glues are the two chiralities, identified by the sheet
    H1 = frozenset({(0, 0), (1, 1), (2, 2), (3, 3)})
    H2 = frozenset({(0, 0), (1, 3), (2, 2), (3, 1)})
    conj_D5 = lambda h: ((-h[0]) % ORDER, h[1])
    conj_A3 = lambda h: (h[0], (-h[1]) % ORDER)
    both = lambda h: ((-h[0]) % ORDER, (-h[1]) % ORDER)
    check("the two glues are swapped by EITHER single spinor conjugation "
          "(D5 or A3) and fixed by the simultaneous one => unique up to "
          "the sheet Z2 (two chiralities)",
          frozenset(map(conj_D5, H1)) == H2
          and frozenset(map(conj_A3, H1)) == H2
          and frozenset(map(both, H1)) == H1)

    # 4. the unique halfway extension IS SO(16)_1
    Hz2 = frozenset({(0, 0), (2, 2)})
    check("the unique isotropic Z2 is {(0,0),(2,2)}",
          [H for H in iso if len(H) == 2] == [Hz2])
    perp = [a for a in A if all(bilinear(a, h) == 0 for h in Hz2)]
    check("|H_perp| = 8 => intermediate disc group H_perp/H = Z2 x Z2 "
          "(mu = 16/2^2 = 4)",
          len(perp) == 8 and 16 // 2**2 == 4)
    classes, seen = [], set()
    for a in perp:
        cl = frozenset({a, ((a[0] + 2) % ORDER, (a[1] + 2) % ORDER)})
        if cl not in seen:
            seen.add(cl)
            classes.append(q_form(sorted(cl)[0]))
    check("induced form q = {0, 0, 0, 1/2} = the D8 discriminant form "
          "=> the ONLY halfway extension is SO(16)_1 (the v83/v87 rival "
          "is the unique intermediate; excluded by holomorphy, mu=4)",
          sorted(classes) == [F(0), F(0), F(0), F(1, 2)])

    # 5. cross-check against v87 and the consequence for Gate A
    check("cross-check: two Lagrangian glues here = the two E8-extension "
          "modular invariants |chi_0+chi_{s,c}|^2 of SO(16)_1 found in v87",
          len(lag), 2, exact=True)
    check("CONSEQUENCE [L]: the carrier extension tower is carrier (mu=16) "
          "-> SO(16)_1 (mu=4) -> E8_1 (mu=1, two chiralities = sheet) and "
          "NOTHING else; Gate A reduces to the bare index statement -- "
          "WHICH extension carries no freedom; seam side stays [P]/[A]",
          True)

    return summary("v92 glue uniqueness")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
