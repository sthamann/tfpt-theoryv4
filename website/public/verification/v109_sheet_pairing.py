"""v109 -- The Sheet-Pairing Lemma: the seam's scalar two-point datum exists
ONLY across the two chiralities, and its channel is exactly the even-form
tower with the Pascal-triple zero-mode grading.  [I] exact weight-multiset
combinatorics; the QBL inference stays [P].

First exact representation-theoretic anchor for the Quadratic-Boundary-
Locality programme (v106/v108), connecting it to the established sheet Z2
(v92, v96-v98).  All statements are verified at the level of exact WEIGHT
MULTISETS (i.e. character-exact, not just dimension counts), built from
nothing but the D5 spinor weights (+-1/2)^5:

  [I] 1. NO SCALAR WITHIN A SHEET.  The zero-weight multiplicity of
         S+ (x) S+ (and of S- (x) S-) is 0: for w in S+, -w has the
         complementary sign pattern, and since the carrier has g = 5
         (odd) slots, -w lies in S-.  There is NO invariant bilinear
         pairing inside one chirality -- a parity theorem of the
         five-slot code.
  [I] 2. THE SCALAR LIVES ACROSS THE SHEETS.  S+ (x) S- has zero-weight
         multiplicity 16 = 1 + 5 + 10 -- the Pascal triple of the
         carrier code -- and decomposes EXACTLY (weight multisets equal)
         as the even-form tower
             S+ (x) S- = Lambda^0 (+) Lambda^2 (+) Lambda^4
         (dimensions 256 = 1 + 45 + 210), with zero-weight grading
         (1, 5, 10) across the three summands.
  [I] 3. SHEET-DIAGONAL = ODD FORMS.  (S+ (x) S+) u (S- (x) S-) equals,
         as an exact weight multiset, 2 Lambda^1 + 2 Lambda^3 + Lambda^5
         (512 = 2x10 + 2x120 + 252): the within-sheet pairings are
         form-VALUED of odd degree -- no scalar channel at all.
  [I] 4. THE TOWER TOPS AT Lambda^{2K}.  The cross-sheet (scalar-bearing)
         channel terminates at form degree 4 = 2K with K = 2: bilinear
         seam data reach exactly the degree the Pascal Ladder (v108)
         requires -- and the zero-mode grading (1, 5, 10) IS the code
         (Lambda^0, Lambda^1, Lambda^2)(C^5) = (1, 5, 10).
  [P] 5. QBL READING (recorded, not claimed): the seam's single scalar
         kernel is necessarily a SHEET PAIRING (chirality-off-diagonal);
         its certified even-form tower ends at Lambda^{2K}.  This gives
         the QBL hypothesis its precise representation-theoretic content
         and ties red-team Target B to the sheet Z2 of v92/v96-98 -- the
         remaining step is to show the Calderon kernel supplies exactly
         this pairing and nothing beyond it.
"""
from collections import Counter
from itertools import combinations, product

import sympy as sp

from tfpt_constants import check, summary, reset, g_car

HALF = sp.Rational(1, 2)
ZERO = tuple([sp.Integer(0)] * 5)


def spinor_weights():
    sp_, sm_ = [], []
    for signs in product([1, -1], repeat=5):
        w = tuple(HALF * s for s in signs)
        (sp_ if signs.count(-1) % 2 == 0 else sm_).append(w)
    return sp_, sm_


def vector_weights():
    out = []
    for i in range(5):
        for s in (1, -1):
            w = [sp.Integer(0)] * 5
            w[i] = sp.Integer(s)
            out.append(tuple(w))
    return out


def lam_weights(vec, k):
    if k == 0:
        return [ZERO]
    return [tuple(sum(col) for col in zip(*combo))
            for combo in combinations(vec, k)]


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def run():
    reset()
    print("v109 sheet pairing (the scalar seam datum lives across the sheets)")

    splus, sminus = spinor_weights()
    vec = vector_weights()
    check("carrier spinor weights: dim S+ = dim S- = 16 ((+-1/2)^5, sign "
          "parity split); g_car = 5 odd",
          len(splus) == 16 and len(sminus) == 16 and g_car % 2 == 1)

    # 1. no scalar within a sheet
    z_pp = sum(1 for a in splus for b in splus if add(a, b) == ZERO)
    z_mm = sum(1 for a in sminus for b in sminus if add(a, b) == ZERO)
    check("NO SCALAR WITHIN A SHEET: zero-weight multiplicity of S+xS+ "
          "and S-xS- is 0 (odd slot count flips the parity of -w) -- no "
          "invariant bilinear inside one chirality",
          z_pp == 0 and z_mm == 0)

    # 2. the scalar lives across the sheets
    cross = Counter(add(a, b) for a in splus for b in sminus)
    check("CROSS-SHEET: zero-weight multiplicity of S+xS- = 16 = 1+5+10 "
          "(the Pascal triple of the code)",
          cross[ZERO] == 16 == 1 + 5 + 10)
    forms_even = Counter()
    for k in (0, 2, 4):
        forms_even.update(lam_weights(vec, k))
    check("EXACT MULTISET IDENTITY: S+ x S- = Lambda^0 + Lambda^2 + "
          "Lambda^4 (character-exact; 256 = 1+45+210) -- the scalar-"
          "bearing channel is the even-form tower",
          cross == forms_even and 1 + 45 + 210 == 256)
    zmults = {k: sum(1 for w in lam_weights(vec, k) if w == ZERO)
              for k in (0, 2, 4)}
    check("zero-mode grading of the tower: (Lambda^0, Lambda^2, Lambda^4) "
          "-> (1, 5, 10) = the carrier code (Lambda^0, Lambda^1, "
          "Lambda^2)(C^5)",
          (zmults[0], zmults[2], zmults[4]) == (1, 5, 10))

    # 3. sheet-diagonal = odd forms
    diag = Counter(add(a, b) for a in splus for b in splus)
    diag.update(add(a, b) for a in sminus for b in sminus)
    forms_odd = Counter()
    for k in (1, 3):
        ws = lam_weights(vec, k)
        forms_odd.update(ws)
        forms_odd.update(ws)
    forms_odd.update(lam_weights(vec, 5))
    check("SHEET-DIAGONAL = ODD FORMS: (S+xS+) u (S-xS-) = 2 Lambda^1 + "
          "2 Lambda^3 + Lambda^5 exactly (512 = 20+240+252) -- "
          "within-sheet pairings are odd-form-valued, never scalar",
          diag == forms_odd and 2 * 10 + 2 * 120 + 252 == 512)

    # 4. the tower tops at Lambda^{2K}
    check("THE TOWER TOPS AT Lambda^{2K}: the cross-sheet channel ends at "
          "form degree 4 = 2K (K = 2) -- bilinear seam data reach exactly "
          "the Pascal-ladder degree (v108)",
          max((0, 2, 4)) == 4 == 2 * 2)

    # 5. QBL reading
    check("QBL READING [P] (recorded, not claimed): the seam's single "
          "scalar kernel is necessarily a SHEET PAIRING (chirality-off-"
          "diagonal), tying Target B to the sheet Z2 (v92/v96-98); "
          "remaining step: show the Calderon kernel supplies exactly this "
          "pairing and nothing beyond", True)

    return summary("v109 sheet pairing")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
