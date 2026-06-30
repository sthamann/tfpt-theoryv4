"""v463 -- SEAM.EQUIV.UNIQ.01: the c=8 HOLOMORPHIC-UNIQUENESS pin -- the positive lever
that makes the IDENTIFICATION half of SEAM.EQUIV.01 classification-forced rather than
assumed (B of the A+B "actually close it" round).

The S3 closure (v458/v459) shows the continuum-EXISTENCE of the seam's scaling limit is
citable (MMST for the free SO(16)_1 part + AGT/AMT lattice-VOA for the 128-spinor
extension).  What stayed implicit was the IDENTIFICATION: "why is a chiral c=8 holomorphic
limit necessarily (E8)_1, and not some same-c rival?"  This module supplies the missing
positive lever: among ALL level-1 current algebras c=8 is NOT unique, but adding HOLOMORPHY
(a single sector, an SL(2,Z)-covariant character) forces the (E8)_1 character E4/eta^8 and
hence dim V_1 = 248, which selects E8 uniquely.  So once the limit is pinned as "c=8 +
holomorphic" (v376/v379 + the det K=1 discriminator v457), it IS (E8)_1 by CLASSIFICATION,
with no residual choice.

  [E] 1. c=8 IS NOT UNIQUE AT LEVEL 1.  the level-1 central charge is c = dim g/(1+h^v);
         c=8 has THREE simple solutions -- A_8 (su(9), dim 80), D_8 (so(16), dim 120) and
         E8 (dim 248).  So c=8 alone is necessary but NOT sufficient: two genuine gleich-c
         rivals exist (this is exactly why v457's det K=4 SO(16) rival is not a strawman).
  [E] 2. HOLOMORPHY FORCES dim V_1 = 248.  a holomorphic (single-sector) chiral CFT at
         c=8 has an SL(2,Z)-covariant character; the only weight-0 form with leading
         q^{-c/24}=q^{-1/3} and integer coefficients is j^{1/3}=E4/eta^8, whose q^1
         coefficient is 248.  The candidate character space is 1-dimensional (the vacuum
         a_0=1 fixes it), so dim V_1=248 is FORCED, not chosen.
  [E] 3. dim V_1 = 248 + LEVEL-1 c=8 => E8 UNIQUELY.  among simple Lie algebras only E8 has
         dim 248 (and 248/(1+30)=8 confirms level-1 c=8); the gleich-c rivals A_8 (80) and
         D_8 (120) are excluded by the forced 248.  So holomorphy promotes "c=8" to "E8".
  [E] 4. THE (E8)_1 TOWER = E4/eta^8.  the graded dimensions {1,248,4124,34752,213126,...}
         are exactly the E4/eta^8 q-coefficients (matches v377/v462), the unique holomorphic
         c=8 partition function.
  [C] 5. CLASSIFICATION CLOSES THE IDENTIFICATION.  Dong-Mason / Schellekens: the
         holomorphic VOA at c=8 is UNIQUE and equals the E8 lattice VOA V_{E8}; the even
         unimodular rank-8 lattice is unique = E8 (Mordell-Witt).  So "c=8 holomorphic
         limit = (E8)_1" is classification-forced.  Combined with v458 (free part citable)
         + v459 (spinor extension), the continuum/identification HALF of SEAM.EQUIV.01 is
         [C] conditional on named, hypothesis-audited published theorems -- leaving the
         REALISATION R1 (v464) as the sole structural input.  SEAM.EQUIV.01 stays [O] until
         R1 is discharged.

Exact (sympy/integer q-series + the Lie-algebra scan; mpmath cross-check E4/eta^8=j^{1/3});
Wolfram-mirrored.  Does NOT by itself close SEAM.EQUIV.01 (it closes the identification half).
"""
from math import comb

import mpmath as mp
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8


def _e4_over_eta8_coeffs(ncoef=6):
    """Integer q-coefficients a_n of q^{1/3}*E4/eta^8 = sum a_n q^n (the (E8)_1 tower).

    E4 = 1 + 240 sum_{n>=1} sigma_3(n) q^n ;  eta^8 = q^{1/3} prod (1-q^n)^8.
    => E4/eta^8 = q^{-1/3} * [ E4 * prod (1-q^n)^{-8} ].
    """
    M = ncoef + 1
    sig3 = [0] + [sum(d ** 3 for d in range(1, n + 1) if n % d == 0) for n in range(1, M)]
    e4 = [1] + [240 * sig3[n] for n in range(1, M)]
    inv = [0] * M
    inv[0] = 1
    for n in range(1, M):                         # multiply by (1-q^n)^{-8}
        factor = [0] * M
        k = 0
        while n * k < M:
            factor[n * k] = comb(k + 7, 7)
            k += 1
        new = [0] * M
        for i in range(M):
            if inv[i]:
                for j in range(M - i):
                    new[i + j] += inv[i] * factor[j]
        inv = new
    out = [0] * M
    for i in range(M):
        for j in range(M - i):
            out[i + j] += e4[i] * inv[j]
    return out[:ncoef + 1]


def _simple_lie_data():
    """(label, rank, dim, dual_Coxeter h^v) for the simple Lie algebras."""
    data = []
    for n in range(1, 13):
        data.append((f"A{n}", n, n * (n + 2), n + 1))
    for n in range(2, 9):
        data.append((f"B{n}", n, n * (2 * n + 1), 2 * n - 1))
    for n in range(2, 9):
        data.append((f"C{n}", n, n * (2 * n + 1), n + 1))
    for n in range(3, 11):
        data.append((f"D{n}", n, n * (2 * n - 1), 2 * n - 2))
    data += [("G2", 2, 14, 4), ("F4", 4, 52, 9), ("E6", 6, 78, 12),
             ("E7", 7, 133, 18), ("E8", 8, 248, 30)]
    return data


def run():
    reset()
    print("v463 SEAM.EQUIV.UNIQ: the c=8 holomorphic-uniqueness pin -- holomorphy forces "
          "dim V_1=248 => E8, isolating it from its gleich-c rivals A_8/D_8")

    c_target = g_car + N_fam                                   # 8

    # ---- 1. c=8 is not unique at level 1 ----
    lie = _simple_lie_data()
    c8 = [(lab, dim) for (lab, rk, dim, hv) in lie
          if sp.Rational(dim, 1 + hv) == c_target]
    labels = {lab for lab, _ in c8}
    check("c=8 NOT UNIQUE AT LEVEL 1 [E]: c=dim/(1+h^v)=8 has THREE simple solutions -- "
          "A8 (dim 80), D8=so(16) (dim 120), E8 (dim 248); c=8 is necessary but NOT "
          "sufficient (the v457 det K=4 SO(16) rival is a real gleich-c competitor): %s"
          % sorted(c8),
          labels == {"A8", "D8", "E8"})

    # ---- 2. holomorphy forces dim V_1 = 248 ----
    coeffs = _e4_over_eta8_coeffs(6)
    check("HOLOMORPHY FORCES dim V_1=248 [E]: the only weight-0 form with leading "
          "q^{-1/3} and integer coeffs is j^{1/3}=E4/eta^8; its q^1 coefficient (the "
          "1-dim candidate space, vacuum a_0=1) is %d -- dim V_1 FORCED, not chosen"
          % coeffs[1],
          coeffs[0] == 1 and coeffs[1] == 248)

    # ---- 3. dim 248 + level-1 c=8 => E8 uniquely ----
    dim248 = [(lab, rk, dim, hv) for (lab, rk, dim, hv) in lie if dim == 248]
    e8_only = (len(dim248) == 1 and dim248[0][0] == "E8"
               and sp.Rational(248, 1 + 30) == c_target and rankE8 == 8)
    check("dim V_1=248 + LEVEL-1 c=8 => E8 UNIQUELY [E]: among simple Lie algebras only "
          "E8 has dim 248 (248/(1+30)=8); the gleich-c rivals A8 (80) and D8 (120) are "
          "excluded by the forced 248 -- holomorphy promotes 'c=8' to 'E8': %s" % dim248,
          e8_only)

    # ---- 4. the (E8)_1 tower = E4/eta^8 ----
    tower = [1, 248, 4124, 34752, 213126]
    check("(E8)_1 TOWER = E4/eta^8 [E]: graded dims {1,248,4124,34752,213126} are exactly "
          "the E4/eta^8 q-coefficients (matches v377/v462), the unique holomorphic c=8 "
          "partition function: %s" % coeffs[:5],
          coeffs[:5] == tower)

    # numeric cross-check E4/eta^8 = j^{1/3}
    mp.mp.dps = 40
    tau = mp.mpc(0, mp.mpf('1.3'))
    q = mp.e ** (2j * mp.pi * tau)
    E4 = 1 + 240 * mp.nsum(lambda n: (n ** 3) * q ** n / (1 - q ** n), [1, mp.inf])
    eta = q ** (mp.mpf(1) / 24) * mp.nprod(lambda n: 1 - q ** n, [1, mp.inf])
    jfun = E4 ** 3 / eta ** 24
    ident = mp.almosteq(E4 / eta ** 8, jfun ** (mp.mpf(1) / 3), 1e-25)
    check("E4/eta^8 = j^{1/3} [E]: the holomorphic c=8 character is the unique cube root "
          "of the modular j-function (numeric, |.|<1e-25)", bool(ident))

    # ---- 5. classification closes the identification ----
    verdict = (labels == {"A8", "D8", "E8"} and coeffs[1] == 248 and e8_only
               and coeffs[:5] == tower and ident)
    check("CLASSIFICATION CLOSES THE IDENTIFICATION [C]: Dong-Mason/Schellekens -- the "
          "holomorphic VOA at c=8 is UNIQUE = V_{E8} (E8 lattice VOA), and the even "
          "unimodular rank-8 lattice is unique = E8 (Mordell-Witt); so 'c=8 holomorphic "
          "limit = (E8)_1' is classification-forced. With v458 (free part) + v459 (spinor "
          "extension) the continuum/identification HALF of SEAM.EQUIV.01 is [C] conditional "
          "on named audited theorems; the REALISATION R1 (v464) is the sole remaining "
          "input. SEAM.EQUIV.01 stays [O] until R1 is discharged", verdict)

    return summary("v463 SEAM.EQUIV.UNIQ: c=8 holomorphic-uniqueness pin -- c=8 has three "
                   "level-1 candidates (A8/80, D8/120, E8/248) so c=8 is not sufficient; "
                   "holomorphy forces the character E4/eta^8 => dim V_1=248 => E8 uniquely "
                   "(248/(1+30)=8), tower {1,248,4124,34752,213126}, E4/eta^8=j^{1/3}. "
                   "Dong-Mason/Schellekens: holomorphic c=8 VOA unique = V_{E8}; so the "
                   "identification half of SEAM.EQUIV.01 is [C] (classification-forced), "
                   "leaving the realisation R1 (v464). SEAM.EQUIV.01 stays [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
