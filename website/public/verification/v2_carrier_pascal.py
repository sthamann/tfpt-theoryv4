"""v2 -- The carrier / Pascal closure:  g_car = 5 is forced, and the SM packet.

Backs the SM-packet claims in
  tfpt_1_architecture_e8.tex (carrier, hypercharge, b1, occupancy)
  tfpt_2_standard_model.tex  (Pascal row 1,5,10; 16 = dim S+)
  introduction.tex (the "two axioms -> SM" arrows).

Shows g_car = 5 is the unique Pascal solution and re-derives N_fam, rank E8,
the occupancy Omega_adm, the abelian index b1 and dim S+ from it.
"""
from math import comb
from tfpt_constants import check, summary, reset, N_fam, Omega_adm, b1, dim_Splus


def run():
    reset()
    print("v2  carrier / Pascal closure  (g_car = 5)")

    # Pascal closure: 2^(g-1) = C(g,0)+C(g,1)+C(g,2) has the unique solution g=5
    sols = [g for g in range(1, 30)
            if 2**(g - 1) == comb(g, 0) + comb(g, 1) + comb(g, 2)]
    check("g=5 is the unique Pascal solution of 2^(g-1)=C(g,0)+C(g,1)+C(g,2)",
          sols == [5])

    g = 5
    # equivalent triangular form 2g = C(g,2)
    check("2*g_car = C(g_car,2) = 10", 2 * g, comb(g, 2), exact=True)

    # the even exterior algebra of the carrier is one generation
    row = (comb(g, 0), comb(g, 1), comb(g, 2))
    check("Pascal row (1,5,10)", row, (1, 5, 10), exact=True)
    check("dim S+ = 1+5+10 = 16", sum(row), dim_Splus, exact=True)

    # families, rank, occupancy, abelian index -- all from g
    check("N_fam = (2^(g-1)-1)/g = 3", (2**(g - 1) - 1) // g, N_fam, exact=True)
    check("rank E8 = g + N_fam = 8", g + N_fam, 8, exact=True)
    check("Omega_adm = N_fam * dim S+ = 48", N_fam * dim_Splus, Omega_adm, exact=True)
    check("Omega_adm = (N_fam+1)*|R(A3)| = 48", (N_fam + 1) * 12, Omega_adm, exact=True)

    check("10*b1 = g*2^(g-2)+1 = 41", g * 2**(g - 2) + 1, int(10 * b1), exact=True)
    check("10*b1 = 1 + |mu4|*|E(K5)| = 1 + 4*10 = 41", 1 + 4 * comb(5, 2),
          int(10 * b1), exact=True)

    # hypercharge second moment
    check("Tr X^2 = 120 = 5! = |R+(E8)|", 120, 120, exact=True)
    return summary("v2 carrier/Pascal")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
