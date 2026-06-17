"""v228 -- the Riemann-Roch index gate: P2 as the mode space of a degree-4 divisor.

Origin Theory already reads the carrier rank and family count off the SAME
four-point divisor mu4 on P^1 by the two canonical functors (v189): the cycle
side rank H1(P^1 minus mu4) = deg-1 = 3 = N_fam (A3) and the function side
h0(P^1, O(mu4)) = deg+1 = 5 = g_car (D5).  This script states that pairing as a
single INDEX GATE: a degree-4 seam divisor on P^1 forces (h0, rank H1) = (5,3),
hence rank E8 = 5+3 = 8 and |Z2| = 5-3 = 2, and the even Clifford algebra of the
5-dim function space closes to the D5 half-spinor 16.

This is a better bedrock LANGUAGE for P2 (a Riemann-Roch reading of the seam
divisor) -- NOT a proof of g_car=5 from nothing: it is conditional on the raw seam
producing a degree-4 (= |mu4|) divisor, which is the QGEO.SYM.01 deck premise
(v181/v214/v216).  So it relocates P2 from "5 slots, trust me" to "the genus-0
mode count of a 4-mark seam divisor".

  [E] 1. deg D = 4 on P^1 => h0(O(D)) = deg+1 = 5 = g_car (Riemann-Roch on P^1,
        h1(O(D))=0 for deg>=0: h0 = deg + 1).
  [E] 2. rank H1(P^1 \ {4 points}) = #points - 1 = 3 = N_fam.
  [E] 3. h0 + rank H1 = 8 = rank E8; h0 - rank H1 = 2 = |Z2|; (h0+H1)/2 = 4 = |mu4|.
  [E] 4. Lambda^even(C^5) = C(5,0)+C(5,2)+C(5,4) = 1+10+5 = 16 = dim S^+ (the
        D5 = so(10) half-spinor) -- the function space's even Clifford closure.
  [E] 5. NEGATIVE CONTROLS: deg 3 -> (4,2), deg 5 -> (6,4); only deg 4 = |mu4|
        gives (5,3) with rank-8 closure; colliding marks lower H1 and break N_fam.

Status: [E] for the index arithmetic; [C] for the physical mode-space reading;
[O] stays for "the raw seam produces the degree-4 divisor" (= QGEO.SYM.01).
Mirrored in wolfram/tfpt_readouts_extension.wl.
"""
from math import comb

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8, dim_Splus


def h0_P1(deg):
    """h^0(P^1, O(D)) for an effective divisor of degree deg (Riemann-Roch, g=0)."""
    return deg + 1 if deg >= 0 else 0


def rank_H1_complement(npts):
    """rank H_1(P^1 minus npts points) = npts - 1."""
    return npts - 1


def run():
    reset()
    print("v228  Riemann-Roch index gate: degree-4 seam divisor => (g_car, N_fam) = (5,3)")

    deg = 4    # |mu4| -- the four seam marks
    h0 = h0_P1(deg)
    h1c = rank_H1_complement(deg)
    check("deg D = 4 (= |mu4|) on P^1 => h0(O(D)) = deg+1 = 5 = g_car "
          "(Riemann-Roch, genus 0)", h0 == g_car == 5)
    check("rank H1(P^1 \\ 4 marks) = 4-1 = 3 = N_fam (A3 cycles)",
          h1c == N_fam == 3)
    check("h0 + rank H1 = 5 + 3 = 8 = rank E8 (the D5(+)A3 rank split)",
          h0 + h1c == rankE8 == 8)
    check("h0 - rank H1 = 5 - 3 = 2 = |Z2| (carrier - family = sheet parity)",
          h0 - h1c == 2)
    check("(h0 + rank H1)/2 = 4 = |mu4| (the divisor degree returns as the glue index)",
          (h0 + h1c) // 2 == deg == 4)
    even_clifford = comb(g_car, 0) + comb(g_car, 2) + comb(g_car, 4)
    check("Lambda^even(C^5) = C(5,0)+C(5,2)+C(5,4) = 1+10+5 = 16 = dim S^+ "
          "(the D5=so(10) half-spinor: the function space's even Clifford closure)",
          even_clifford == dim_Splus == 16)

    # negative controls
    check("NEG deg 3: (h0, rank H1) = (4, 2), sum 6 != rank E8; 4-mark count broken",
          (h0_P1(3), rank_H1_complement(3)) == (4, 2))
    check("NEG deg 5: (h0, rank H1) = (6, 4), sum 10 != rank E8; wrong carrier",
          (h0_P1(5), rank_H1_complement(5)) == (6, 4))
    check("NEG colliding marks (3 distinct of 4) -> rank H1 = 2 -> N_fam=2, breaks "
          "the family count: the degree-4 SQUARE (4 distinct marks) is required",
          rank_H1_complement(3) == 2)

    return summary("v228 RR index gate (degree-4 divisor => carrier 5, family 3)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
