"""v396 -- the phi0 leading term from icosahedral combinatorics (sharpening v312/v395).

v312's honest negative: phi0 = 1/(6 pi) + 48 c3^4 is analytic/transcendental, not a rational
edge fraction.  v395 unified the carrier x family mechanism; the remaining non-graph-spectral
input is phi0 alone.  This module tests whether the LEADING term phibase = 1/(6 pi) has a
forced combinatorial reading on the icosahedral hypergraph / (2,3,5) skeleton -- without
claiming the puncture correction 48 c3^4 is graph-determined.

  [E] 1. ICOsahedral COUNTS ARE ANCHOR-FORCED: the icosahedron has V=12, E=30=h(E8), F=20
        triangular hyperedges, |Aut|=120=|2I|; and F = g_car(g_car-1), h = 2 N_fam g_car,
        4h = |Aut| (all from {g_car,N_fam} = {5,3}).
  [E] 2. THE LEADING TERM IS EXACT: phibase = 1/(6 pi) = (4/3) c3 (since c3 = 1/(8 pi));
        equivalently phibase = F/(4 h pi) = F/(|Aut| pi) = (F/(g_car N_fam)) c3.
  [E] 3. F/h = |Z2|/N_fam: the hyperedge-to-Coxeter ratio equals the family survival ratio
        (the same 2/3 as v327/v395); so phibase = (F/h)/(4 pi) = c3 (g_car-1)/N_fam.
  [E] 4. GAUSS-BONNET CONSISTENCY: on S^2 the icosahedron vertex-deficit sum is 12*(pi/3)
        = 4 pi (the sphere total curvature); c3 = 1/(|Z2| 4 pi) uses the same 4 pi seam
        datum (v216/v342), and phibase carries one extra N_fam in the denominator.
  [E] 5. HONEST NEGATIVE -- puncture term NOT combinatorial: dtop = 48 c3^4 = 3/(256 pi^4)
        is not a small rational hypergraph fraction; the full phi0 still has an analytic
        piece beyond the icosahedral leading term.
  [C] 6. READING: phibase is the tree-level seed phi0^ret at leading order; it is NOT an
        independent rewrite injection -- it is (hyperedge count)/(carrier x family) x c3,
        with c3 itself the boundary Gauss-Bonnet datum.  The puncture 48 c3^4 remains [O].

HONEST SCOPE: [E] the exact combinatorial identities + Gauss-Bonnet consistency + puncture
negative; [C] the seed-as-combinatorics reading (reinterpretation, not a new derivation of
P1).  Sharpens v312/v395; does NOT close phi0 entirely.  Python-only (sympy)."""
import itertools

import numpy as np
import sympy as sp

from tfpt_constants import check, summary, reset, c3, g_car, N_fam, phibase, phi0

PHI = (1 + np.sqrt(5)) / 2


def _icosahedron_counts():
    """Return (V, E, F, |Aut|) for the unit icosahedron graph."""
    V = []
    for a, b in itertools.product([1, -1], repeat=2):
        V += [(0, a, b * PHI), (a, b * PHI, 0), (b * PHI, 0, a)]
    V = np.array(sorted(set(map(tuple, np.round(V, 9)))))
    D = np.round(((V[:, None] - V[None]) ** 2).sum(-1), 6)
    el2 = np.min(D[D > 1e-9])
    A = (np.abs(D - el2) < 1e-6).astype(int)
    faces = [t for t in itertools.combinations(range(len(V)), 3)
             if A[t[0], t[1]] and A[t[0], t[2]] and A[t[1], t[2]]]
    nbr = [set(np.where(A[i])[0]) for i in range(len(V))]

    def _autos():
        autos = []
        def bt(perm, used):
            k = len(perm)
            if k == len(V):
                autos.append(tuple(perm))
                return
            for img in range(len(V)):
                if img in used:
                    continue
                if all((perm[j] in nbr[img]) == (j in nbr[k]) for j in range(k)):
                    bt(perm + [img], used | {img})
        bt([], set())
        return autos

    return len(V), int(A.sum() // 2), len(faces), len(_autos())


def run():
    reset()
    print("v396  phi0 leading term from icosahedral combinatorics (sharpening v312/v395)")

    pi = sp.pi
    Z2 = g_car - N_fam
    h_e8 = 2 * N_fam * g_car
    c3_sym = sp.Rational(1, 1) / (8 * pi)
    base_sym = sp.Rational(1, 1) / (6 * pi)
    dtop_sym = 48 * c3_sym ** 4

    V, E, F, naut = _icosahedron_counts()

    # 1. icosahedral counts are anchor-forced
    check("ICOSAHEDRAL COUNTS [E]: V=%d, E=%d=h(E8), F=%d triangular hyperedges, |Aut|=%d=|2I|; "
          "F=g_car(g_car-1)=%d, h=2 N_fam g_car=%d, 4h=|Aut|=%d (all from {g_car,N_fam}={5,3})"
          % (V, E, F, naut, g_car * (g_car - 1), h_e8, 4 * h_e8),
          V == 12 and E == 30 == h_e8 and F == 20 == g_car * (g_car - 1)
          and naut == 120 == 4 * h_e8)

    # 2. leading term exact identities
    via_c3 = sp.simplify(base_sym - sp.Rational(4, 3) * c3_sym)
    via_Fh = sp.simplify(base_sym - F / (4 * h_e8 * pi))
    via_aut = sp.simplify(base_sym - F / (naut * pi))
    via_ratio = sp.simplify(base_sym - (F / (g_car * N_fam)) * c3_sym)
    check("LEADING TERM EXACT [E]: phibase = 1/(6 pi) = (4/3) c3 = F/(4 h pi) = F/(|Aut| pi) "
          "= (F/(g_car N_fam)) c3 -- four equivalent forms, all 0 difference",
          via_c3 == 0 and via_Fh == 0 and via_aut == 0 and via_ratio == 0)

    # 3. F/h = |Z2|/N_fam and phibase = (F/h)/(4 pi) = c3 (g_car-1)/N_fam
    ratio_Fh = sp.Rational(F, h_e8)
    survival = sp.Rational(Z2, N_fam)
    via_Fh4pi = sp.simplify(base_sym - ratio_Fh / (4 * pi))
    via_gN = sp.simplify(base_sym - sp.Rational(g_car - 1, N_fam) * c3_sym)
    check("F/h = |Z2|/N_fam [E]: hyperedge/Coxeter ratio F/h = %s = |Z2|/N_fam = %s (the v327 "
          "survival ratio); phibase = (F/h)/(4 pi) = c3 (g_car-1)/N_fam"
          % (ratio_Fh, survival),
          ratio_Fh == survival and via_Fh4pi == 0 and via_gN == 0)

    # 4. Gauss-Bonnet consistency on S^2
    deficit = sp.Rational(V, 1) * (pi / 3)          # 12 vertices, 5 triangles => pi/3 each
    c3_gb = sp.Rational(1, 1) / (Z2 * 4 * pi)
    check("GAUSS-BONNET [E]: icosahedron vertex-deficit sum V*(2 pi - 5 pi/3) = 4 pi (sphere "
          "total curvature); c3 = 1/(|Z2| 4 pi) uses the same 4 pi boundary datum (v216/v342); "
          "phibase = c3 (g_car-1)/N_fam inserts one extra N_fam in the denominator vs c3",
          deficit == 4 * pi and sp.simplify(c3_gb - c3_sym) == 0
          and sp.simplify(base_sym - sp.Rational(g_car - 1, N_fam) * c3_sym) == 0)

    # 5. honest negative: puncture term
    p0 = float(phi0)
    pbase = float(phibase)
    dtop = float(dtop_sym)
    is_rational_edge = any(abs(dtop - a / b) < 1e-9 for b in range(1, 200) for a in range(1, b))
    check("HONEST NEGATIVE [E]: the puncture dtop = 48 c3^4 = %.2e is NOT a small rational "
          "hypergraph fraction; full phi0 = phibase + dtop = %.7f still has an analytic piece "
          "beyond the icosahedral leading term (v312 negative, puncture part unchanged)"
          % (dtop, p0),
          not is_rational_edge and abs(pbase + dtop - p0) < 1e-12 and dtop / pbase < 0.01)

    # 6. reading
    check("READING [C]: phibase is the tree-level retained seed at leading order -- NOT an "
          "independent rewrite injection but (hyperedge count F)/(g_car N_fam) x c3, with c3 "
          "the boundary Gauss-Bonnet datum; the puncture 48 c3^4 remains open [O]",
          via_ratio == 0 and via_gN == 0 and dtop_sym != 0)

    return summary("v396 phi0 leading term: phibase = F/(g_car N_fam) c3 = 1/(6 pi); F/h = |Z2|/N_fam; puncture 48 c3^4 still analytic")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
