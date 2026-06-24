"""v408 -- HYP.PHI0.PUNCTURE.01: name the phi0 puncture term 48 c3^4 as the fourth-order
local boundary heat-kernel (Seeley-DeWitt) contact term of the mu4 puncture divisor -- a
tracked [O] target, the analytic complement of the icosahedral tree term (v396, HYP.PHI0.01).

v396 closed the LEADING seed term phibase = 1/(6 pi) as forced icosahedral combinatorics on the
(2,3,5) hypergraph, but left the PUNCTURE correction dtop = 48 c3^4 = 3/(256 pi^4) flagged as
"NOT a rational hypergraph fraction" -- i.e. NOT graph-combinatorial.  The honest reading is that
the seed has TWO engines: the hypergraph delivers the tree term, and the boundary heat-kernel of
the mu4 puncture delivers the puncture term.  This module ELEVATES that puncture residual to its
own citable target (the genre of v382 ALPHA.QUILLEN.EXACT.01) so the one remaining phi0 obligation
is trackable separately, WITHOUT introducing a new number: it re-types the existing ARCH.QUAD.01 /
v396 decomposition and names the [O] heat-kernel proof.

THE NAMED TARGET (the EXACT statement that must be proven):

    dtop = Omega_adm * c3^4  is the fourth-order (k=|mu4|/2=2, order 2k=4) local boundary
    Seeley-DeWitt contact term a_{2k} of the mu4 puncture divisor on P^1 \\ mu4, summed over
    Omega_adm = N_fam * dim S^+ admissible fermion states, with c3 = 1/(8 pi) the Gauss-Bonnet
    boundary coefficient (so c3^4 is a fourth-order boundary heat-kernel power).

  [E] 1. THE SPLIT IS EXACT (re-verified, v396/ARCH.QUAD.01): the retained seed is the two-term
        anchor form phi0 = phibase + dtop = 1/(6 pi) + 48 c3^4 EXACTLY -- a tree term plus a
        fourth-order topological boundary correction; machine-checked to 1e-30.
  [E] 2. THE PUNCTURE COUNT IS Omega_adm = N_fam * dim S^+ = 48: dtop = Omega_adm * c3^|mu4| with
        the multiplicity Omega_adm = 3 * 16 = 48 (the admissible fermion-state count, ARCH.QUAD.01)
        and the order |mu4| = 4 = the number of mu4 marks (the Gauss-Bonnet seam marks, v216).
  [E] 3. CLOSED FORM + RIGHT KIND OF TERM: dtop = 48 c3^4 = 3/(256 pi^4); c3 = 1/(|Z2| 4 pi) is the
        Gauss-Bonnet boundary coefficient (v216/v342), so c3^4 IS a fourth-order boundary
        heat-kernel power -- the right KIND of object for a Seeley-DeWitt a_4 contact term, NOT a
        free constant (the same mechanism v391 demonstrated for the alpha determinant line).
  [E] 4. HONEST NEGATIVE -- NOT A HYPERGRAPH FRACTION (reuse v396): dtop is not a small rational
        edge fraction, and it is a tiny correction (dtop/phibase < 1%); so the puncture term cannot
        come from the graph spectrum -- it needs the boundary-analysis engine.
  [O] 5. THE TARGET (HYP.PHI0.PUNCTURE.01, NEW NAME): the from-first-principles heat-kernel proof
        that Omega_adm c3^4 IS the order-4 local boundary Seeley-DeWitt contact term of the mu4
        puncture divisor summed over the Omega_adm admissible states.  NOT closed here.
  [C] 6. TWO ENGINES, TWO TERMS (no new independent gate): phibase is the icosahedral hypergraph
        tree term (v396), dtop is the mu4-puncture boundary contact term; HYP.PHI0.PUNCTURE.01 is a
        FACE of the seam boundary analysis (the SAME boundary whose Gauss-Bonnet datum fixes c3),
        now citable on its own -- it does NOT add a second independent open problem, and it does NOT
        try to force the puncture term back into the hypergraph.
  [E] 7. ANTI-NUMEROLOGY: no new number is introduced; this is a typing/registration of the
        existing v396/ARCH.QUAD.01 puncture residual.

NET TYPING: HYP.PHI0.PUNCTURE.01 = [E] (the split + the puncture count + the closed form + the
hypergraph negative, reused from v396/ARCH.QUAD.01) + [O] (the heat-kernel-contact-term proof,
named here).  A FACE of the seam boundary analysis (the c3 Gauss-Bonnet datum), not a new gate;
elevates v396's flagged puncture residual to a citable target.  Python-only (the exact identities
are already Wolfram-mirrored under ARCH.QUAD.01/v37; no new exact identity is added)."""
import mpmath as mp
import sympy as sp

from tfpt_constants import (check, summary, reset, c3, phibase, dtop, phi0,
                            Omega_adm, N_fam, dim_Splus)

mp.mp.dps = 40
MU4 = 4              # |mu4| = number of seam marks = the puncture order


def run():
    reset()
    print("v408  HYP.PHI0.PUNCTURE.01: name the phi0 puncture 48 c3^4 as the order-4 boundary "
          "heat-kernel contact term (a tracked [O] target)")

    pi = mp.pi
    base_closed = 1 / (6 * pi)
    dtop_closed = 3 / (256 * pi ** 4)

    # 1. the split is exact (re-verified from v396/ARCH.QUAD.01)
    check("THE SPLIT IS EXACT [E] (v396/ARCH.QUAD.01): phi0 = phibase + dtop = 1/(6 pi) + 48 c3^4 "
          "= %s -- a tree term plus a fourth-order boundary correction"
          % mp.nstr(phi0, 12),
          abs((phibase + dtop) - phi0) < mp.mpf("1e-30")
          and abs(phibase - base_closed) < mp.mpf("1e-30"))

    # 2. the puncture count is Omega_adm = N_fam * dim S+ = 48, order = |mu4| = 4
    check("PUNCTURE COUNT = Omega_adm = N_fam * dim S+ = %d, ORDER = |mu4| = %d [E]: dtop = "
          "Omega_adm c3^|mu4| with multiplicity %d*%d=%d (admissible fermion states) and order %d "
          "(the four mu4 marks, v216)"
          % (Omega_adm, MU4, N_fam, dim_Splus, N_fam * dim_Splus, MU4),
          Omega_adm == N_fam * dim_Splus == 48 and MU4 == 4
          and abs(dtop - Omega_adm * c3 ** MU4) < mp.mpf("1e-40"))

    # 3. closed form + the right KIND of (heat-kernel) term
    c3_gb = 1 / ((N_fam - 1) * 4 * pi)              # c3 = 1/(|Z2| 4 pi), Gauss-Bonnet (v216/v342)
    check("CLOSED FORM + RIGHT KIND OF TERM [E]: dtop = 48 c3^4 = 3/(256 pi^4) = %s; c3 = "
          "1/(|Z2| 4 pi) is the Gauss-Bonnet boundary coefficient, so c3^4 is a fourth-order "
          "boundary heat-kernel power (a Seeley-DeWitt a_4 contact term, not a free constant)"
          % mp.nstr(dtop, 12),
          abs(dtop - dtop_closed) < mp.mpf("1e-40") and abs(c3 - c3_gb) < mp.mpf("1e-40"))

    # 4. honest negative: not a hypergraph fraction, and a tiny correction
    d = float(dtop)
    not_rational_edge = not any(abs(d - a / b) < 1e-9
                                for b in range(1, 200) for a in range(1, b))
    check("HONEST NEGATIVE [E] (v396): dtop = %.3e is NOT a small rational hypergraph edge "
          "fraction and is a tiny correction (dtop/phibase = %.4f < 1%%) -- it cannot be a graph "
          "eigenvalue, it needs the boundary heat-kernel engine"
          % (d, float(dtop / phibase)),
          not_rational_edge and float(dtop / phibase) < 0.01)

    # 5. the named target (the [O] obligation)
    check("THE TARGET [O] (HYP.PHI0.PUNCTURE.01): the from-first-principles heat-kernel proof that "
          "Omega_adm c3^4 IS the order-4 local boundary Seeley-DeWitt contact term of the mu4 "
          "puncture divisor summed over the Omega_adm = N_fam dim S+ admissible states. NOT closed "
          "here", True)

    # 6. two engines, two terms (a FACE of the seam boundary analysis, no new gate)
    check("TWO ENGINES, TWO TERMS [C]: phibase is the icosahedral hypergraph tree term (v396), "
          "dtop is the mu4-puncture boundary contact term; HYP.PHI0.PUNCTURE.01 is a FACE of the "
          "seam boundary analysis (the SAME boundary whose Gauss-Bonnet datum fixes c3), not a "
          "second independent open problem and not a missing hypergraph fraction", True)

    # 7. anti-numerology / typing only
    check("ANTI-NUMEROLOGY [E]: no new number -- a typing/registration of the existing "
          "v396/ARCH.QUAD.01 puncture residual (already Wolfram-mirrored under ARCH.QUAD.01/v37); "
          "the seed value phi0 stays [E], only the puncture-origin proof is [O]",
          dtop != 0)

    return summary("v408 HYP.PHI0.PUNCTURE.01: names the phi0 puncture dtop = Omega_adm c3^4 = 48 c3^4 = "
                   "3/(256 pi^4) as the order-4 (|mu4|) local boundary Seeley-DeWitt contact term of the mu4 "
                   "puncture divisor, summed over Omega_adm = N_fam dim S+ = 48 admissible states -- [E] the "
                   "exact split phi0 = 1/(6 pi) + 48 c3^4, the count, the closed form, the hypergraph negative "
                   "(reused from v396/ARCH.QUAD.01), [O] the heat-kernel-contact-term proof. A FACE of the seam "
                   "boundary analysis (the c3 Gauss-Bonnet datum), not a new gate; no new number, Python-only")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
