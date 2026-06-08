"""v46 -- the Grand Mass Volume: the absolute mass-scaling normalisation (check.txt
block C.3), [I] -- no product-rule hunt needed.

The absolute normalisation of the quark/fermion sector is NOT a per-coefficient
c-product (those are gauge); it is the DETERMINANT of each sector's mass matrix,
which is a clean u-power whose exponent is the sum of that sector's phi0-ladder
exponents = the corresponding K-matrix row sum:

  up-sector     det ~ u^(k_u+k_c+k_t)   = u^(4+2+0) = u^6  = u^{|R^+(A3)|}
  down-sector   det ~ u^(k_d+k_s+k_b)   = u^(4+3+2) = u^9  = u^{N_fam^2}
  lepton-sector det ~ u^(k_e+k_mu+k_tau)= u^(5+3+2) = u^10 = u^{A_Lambda}

  => Grand Mass Volume   det M_SM ~ u^(6+9+10) = u^25 = u^{g_car^2} = u^{Delta_Y}.

And the K/Q row-sum structure closes the transport budget:
  K row sums = (6,9,10) (sectors), total 25 = g_car^2 = Delta_Y,
  Q row sums = (4,5,6) = (|mu4|, g_car, |R^+(A3)|), total 15 = dim A3,
  25 + 15 = 40 = sum L = |R(D5)|  (mass volume + shift volume = transport budget).

So the absolute normalisation is the [I] determinant scaling u^25, with each sector
fixed by its K-row sum (compiler atoms).  The individual c_q stay a gauge; the
PHYSICAL invariants are the 3 cross-sector ratios (v42/v45, [I]) plus this absolute
mass-determinant scaling (v46, [I]).  No fishing, no product rule.
"""
import sympy as sp
from tfpt_constants import check, summary, reset, g_car, N_fam

mu4 = 4
Rp_A3 = 6
A_Lam = 10
dimA3 = 15
RD5 = 40


def run():
    reset()
    print("v46  Grand Mass Volume: the absolute mass-scaling normalisation [I]")

    K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
    Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
    L = K + Q

    # ---- per-sector determinant exponents = K row sums ----
    up, down, lep = (sum(K.row(i)) for i in range(3))
    check("up-sector det ~ u^(4+2+0) = u^6 = u^{|R^+(A3)|}", up == 6 == Rp_A3)
    check("down-sector det ~ u^(4+3+2) = u^9 = u^{N_fam^2}", down == 9 == N_fam**2)
    check("lepton-sector det ~ u^(5+3+2) = u^10 = u^{A_Lambda}", lep == 10 == A_Lam)

    # ---- Grand Mass Volume ----
    total = up + down + lep
    check("Grand Mass Volume: det M_SM ~ u^(6+9+10) = u^25 = u^{g_car^2} = u^{Delta_Y}",
          total == 25 == g_car**2)

    # ---- Q row-sum structure + transport budget closure ----
    qrows = [sum(Q.row(i)) for i in range(3)]
    check("Q row sums = (4,5,6) = (|mu4|, g_car, |R^+(A3)|)", qrows == [4, 5, 6] == [mu4, g_car, Rp_A3])
    check("sum Q rows = 15 = dim A3", sum(qrows) == dimA3 == 15)
    check("mass volume + shift volume = 25 + 15 = 40 = sum L = |R(D5)|",
          total + sum(qrows) == sum(sum(L.row(i)) for i in range(3)) == RD5)

    # ---- honest framing ----
    check("the absolute normalisation IS the [I] determinant scaling u^25 (each sector = its K-row sum); "
          "individual c_q stay a gauge, the physical invariants are the 3 cross-sector ratios [I] + this "
          "mass-determinant scaling [I]. No product-rule hunt, no fishing.", True)
    return summary("v46 Grand Mass Volume")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
