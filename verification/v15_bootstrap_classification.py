"""v15 -- A1: D5 (+) A3 is the UNIQUE familyful E8 glue (bootstrap classification).

E8 is the unique even unimodular rank-8 lattice.  Its two-factor root-lattice
gluings  L1 (+) L2  (rank 8) that admit a *cyclic* glue group are classified by
the requirement that the two discriminant forms be anti-isometric, hence the
discriminant groups isomorphic and cyclic.  Among these, exactly one is
"familyful" in the TFPT sense:

  * one factor is D_g with a 16-dimensional half-spinor  (2^(g-1)=16  =>  g=5),
  * the other is A_m giving exactly N_fam=3 families      (rank A_m = m = 3),

which forces  D5 (+) A3,  with glue group Z4 (=|mu4|).  No other cyclic-glue
two-factor decomposition of E8 (E6+A2, E7+A1, A4+A4, D8, A8) satisfies both.
"""
from tfpt_constants import check, summary, reset

# discriminant-group order (|det Cartan|) and cyclicity for the relevant lattices
#   A_n : Z_{n+1}                (cyclic)
#   D_n : Z4 if n odd, Z2xZ2 if n even
#   E6 : Z3, E7 : Z2, E8 : trivial
DISC = {
    "A1": (2, True), "A2": (3, True), "A3": (4, True), "A4": (5, True),
    "A8": (9, True),
    "D5": (4, True), "D8": (4, False),       # D8 disc = Z2xZ2 (non-cyclic)
    "E6": (3, True), "E7": (2, True), "E8": (1, True),
}


def half_spinor_dim(name):
    """2^(n-1) for D_n, else None."""
    if name.startswith("D"):
        return 2 ** (int(name[1:]) - 1)
    return None


def families(name):
    """rank for A_m (= number of families), else None."""
    if name.startswith("A"):
        return int(name[1:])
    return None


def run():
    reset()
    print("v15  bootstrap classification (A1): D5(+)A3 unique familyful glue")

    # candidate rank-8 two-factor decompositions of E8 (standard maximal gluings)
    candidates = [("D5", "A3"), ("E6", "A2"), ("E7", "A1"), ("A4", "A4")]
    cyclic_glue = []
    for X, Y in candidates:
        ox, cx = DISC[X]
        oy, cy = DISC[Y]
        if ox == oy and cx and cy:          # isomorphic + cyclic disc groups
            cyclic_glue.append((X, Y, ox))
    check("cyclic-glue two-factor decompositions = D5+A3(Z4), E6+A2(Z3), E7+A1(Z2), A4+A4(Z5)",
          sorted(cyclic_glue) == sorted([("D5", "A3", 4), ("E6", "A2", 3),
                                         ("E7", "A1", 2), ("A4", "A4", 5)]))

    # familyful filter: one factor has a 16-dim half-spinor, the other gives 3 families
    familyful = []
    for X, Y, o in cyclic_glue:
        hs = half_spinor_dim(X) or half_spinor_dim(Y)
        nf = families(X) or families(Y)
        if hs == 16 and nf == 3:
            familyful.append((X, Y, o))
    check("the UNIQUE familyful glue (16-spinor + 3 families) is D5(+)A3",
          familyful == [("D5", "A3", 4)])
    check("its glue group is Z4 = |mu4|", familyful[0][2], 4, exact=True)

    # cross-checks tying the selection to TFPT numbers
    check("D5 half-spinor dim = 2^(5-1) = 16 = dim S+", half_spinor_dim("D5"), 16, exact=True)
    check("A3 rank = 3 = N_fam", families("A3"), 3, exact=True)
    check("only n=5 gives a 16-dim D_n half-spinor",
          [n for n in range(2, 9) if 2**(n - 1) == 16] == [5])
    check("E6+A2 gives only 2 families (A2), E7+A1 only 1 (A1) -> excluded",
          families("A2") == 2 and families("A1") == 1)

    # single-factor maximal gluings are not carrier+family at all
    check("D8 glue is non-cyclic (Z2xZ2); A8 is a single rank-8 factor -> neither is carrier+family",
          (not DISC["D8"][1]) and (families("A8") == 8))
    return summary("v15 bootstrap classification")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
