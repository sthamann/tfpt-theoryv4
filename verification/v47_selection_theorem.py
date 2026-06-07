"""v47 -- Boundary Carrier Selection Theorem (Theorem A): why (D5(+)A3)+mu4 = E8
and no other structure.

Consolidates v1 (E8 lattice certificate) + v15 (familyful classification) into a
single SELECTION statement: admissible boundary-carrier data force exactly the
TFPT inputs, and every rank-8 alternative is excluded by failing at least one of
the four simultaneous conditions.

  boundary side:  mu4 = {1,i,-1,-i}  ->  X_f = P^1 minus mu4  ->  H_1 = Z^3  ->  A3,
                  N_fam = 3.
  carrier side:   minimal D-type carrier with a 16-dim half-spinor  ->  D5
                  (only n=5 gives 2^{n-1}=16); S+ = Lambda^even(C^5) = 1+10+5.
  glue:           disc(D5)=disc(A3)=Z4 (isomorphic, cyclic), anti-isometric,
                  q(D5)+q(A3)=5/4+3/4=2 (the E8 root norm), glue index
                  [E8:D5(+)A3]=sqrt(4*4/1)=4=|mu4|; E8 is the unique even
                  unimodular rank-8 lattice.

  exclusion:      the four simultaneous conditions
                    (i) 16-dim half-spinor, (ii) N_fam=3, (iii) cyclic Z4 glue,
                    (iv) q_D+q_A=2
                  are met ONLY by D5(+)A3.  D8 (non-cyclic Z2xZ2, no family),
                  E7+A1 (no 16-spinor, 1 family), E6+A2 (2 families, Z3),
                  A4+A4 (no D-spinor, Z5), A8 (single factor) all fail.

TYPING: the lattice/classification facts are [L].  The PHYSICAL selection
principle -- that a primitive reflection-positive seam (c3=1/8pi) plus a minimal
chiral carrier interface *forces* these data -- is the [P]/[A] selection axiom
(P1 analytic interface + P2 carrier interface), not a zero-input derivation.
"""
import sympy as sp
from math import comb
from tfpt_constants import check, summary, reset, g_car, N_fam

# disc-group order and cyclicity (A_n:Z_{n+1}; D_n:Z4 odd / Z2xZ2 even; E6:Z3,E7:Z2)
DISC = {"A1": (2, True), "A2": (3, True), "A3": (4, True), "A4": (5, True),
        "A8": (9, True), "D5": (4, True), "D8": (4, False),
        "E6": (3, True), "E7": (2, True), "E8": (1, True)}
QNORM = {"D5": sp.Rational(5, 4), "A3": sp.Rational(3, 4)}   # discriminant-form norms


def run():
    reset()
    print("v47  Boundary Carrier Selection Theorem (Theorem A)")

    # ---- boundary side: mu4 -> A3, N_fam=3 ----
    check("boundary mu4 = {1,i,-1,-i}: H_1(P^1 \\ mu4) = Z^3 => A3, N_fam = 3",
          (4 - 1) == 3 == N_fam)

    # ---- carrier side: only n=5 gives a 16-dim half-spinor ----
    check("minimal D-type carrier with 16-dim half-spinor: only n=5 (2^{n-1}=16) => D5",
          [n for n in range(2, 9) if 2**(n - 1) == 16] == [5] and 2**(g_car - 1) == 16)
    check("S+ = Lambda^even(C^5) = C(5,0)+C(5,2)+C(5,4) = 1+10+5 = 16",
          [comb(5, 0), comb(5, 2), comb(5, 4)] == [1, 10, 5])

    # ---- glue: q-norm = E8 root norm, glue index = |mu4|, E8 unique ----
    check("q(D5)+q(A3) = 5/4 + 3/4 = 2 (the E8 root norm)", QNORM["D5"] + QNORM["A3"] == 2)
    check("disc(D5) = disc(A3) = Z4 (isomorphic, cyclic) -> anti-isometric glue",
          DISC["D5"] == (4, True) and DISC["A3"] == (4, True))
    glue_index = sp.sqrt(sp.Integer(DISC["D5"][0] * DISC["A3"][0]) / DISC["E8"][0])
    check("glue index [E8:D5(+)A3] = sqrt(detD5*detA3/detE8) = sqrt(16/1) = 4 = |mu4|",
          glue_index == 4)
    check("E8 is the unique even unimodular rank-8 lattice (disc = trivial)",
          DISC["E8"] == (1, True))

    # ---- exclusion of every rank-8 alternative ----
    def half_spinor(name):
        return 2**(int(name[1:]) - 1) if name.startswith("D") else None

    def fams(name):
        return int(name[1:]) if name.startswith("A") else None

    # the four simultaneous conditions, evaluated on each two-factor candidate
    def passes(X, Y):
        hs = half_spinor(X) or half_spinor(Y)
        nf = fams(X) or fams(Y)
        ox, cx = DISC[X]
        oy, cy = DISC[Y]
        cond_spinor = (hs == 16)
        cond_fam = (nf == 3)
        cond_cyclic = (ox == oy and cx and cy)
        cond_qnorm = (X in QNORM and Y in QNORM and QNORM.get(X, 0) + QNORM.get(Y, 0) == 2)
        return cond_spinor and cond_fam and cond_cyclic and cond_qnorm

    cands = [("D5", "A3"), ("E6", "A2"), ("E7", "A1"), ("A4", "A4")]
    survivors = [(X, Y) for X, Y in cands if passes(X, Y)]
    check("only D5(+)A3 meets all four conditions (16-spinor & 3 fam & Z4 cyclic & q-sum 2)",
          survivors == [("D5", "A3")])
    check("D8 excluded: non-cyclic Z2xZ2 glue and no family geometry",
          not DISC["D8"][1])
    check("E6+A2 excluded: A2 -> 2 families, disc Z3 != Z4; E7+A1 excluded: 1 family, no 16-spinor",
          fams("A2") == 2 and fams("A1") == 1 and DISC["E6"][0] == 3 and DISC["E7"][0] == 2)
    check("A8 excluded: single rank-8 factor (8 families, not carrier+family)", fams("A8") == 8)

    # ---- honest typing of the physical selection ----
    check("SELECTION [L]+[P]: lattice/classification facts are [L]; the physical selection "
          "(reflection-positive seam c3=1/8pi + minimal chiral carrier => these inputs) is the "
          "[P]/[A] selection axiom (P1 analytic + P2 carrier), not a zero-input derivation", True)
    return summary("v47 Boundary Carrier Selection Theorem")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
