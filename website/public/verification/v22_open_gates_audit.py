"""v22 -- audit contract for the residual gates A2, B3, B4, B5, B6, C7.

These are the genuine research-frontier gates (Alessandro 5.0 review).  None is
*closed* here -- that would be dishonest.  Instead this script machine-pins the
EXACT reduction of each gate: the part that is proved/forced, and the precisely
named residual that stays open.  This makes the open gates explicit audit
contracts rather than vague gaps.

  A2  H2 parabolic<->transport equivalence + unitarity (U)
  B3  geometric origin of Q (Q+/Q- from D4-equivariant parabolic geometry)
  B4  R modulo Mehta-Seshadri unitarity (U)
  B5  N_star (reheating input vs compiler output)
  B6  covariant metric-sector field equation
  C7  full quantum gravity (boundary-kernel measure beyond FRW)
"""
import sympy as sp
import mpmath as mp
from tfpt_constants import check, summary, reset, c3, N_fam, Mbar

mp.mp.dps = 30


def run():
    reset()
    print("v22  residual-gates audit contract (A2,B3,B4,B5,B6,C7)")

    # ---- A2 / B4: parabolic scaffolding is forced; only the (U) flag realisation is open ----
    mu4 = 4
    check("A2: parabolic deg E = -|mu4| = -4 (pardeg zero)", -mu4, -4, exact=True)
    # 4 = 2+1+1 is the unique partition of |mu4| into 3 positive parts -> O(-2)+O(-1)^2
    parts3 = [p for p in sp.utilities.iterables.partitions(4) if sum(p.values()) == 3]
    check("A2: 4=2+1+1 is the UNIQUE splitting into 3 positive parts", parts3 == [{2: 1, 1: 2}])
    R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
    check("B4: residue branch selector det R = h(D5) = 8 (sibling {1,3,4} gives 4)", R.det() == 8)
    check("A2/B4 RESIDUAL (open): D4-fixed locus is positive-dim (v19) -> (U) selects the "
          "stable point; R unconditional only GIVEN (U)+flag", True)

    # ---- B3: Q algebra forced; geometric realisation of Q+/Q- open ----
    Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
    t = sp.symbols('t')
    # Q_+ = upper-triangular A3 grading with spectrum {1,2,3} (the A3 exponents)
    check("B3: Q char poly = (t-1)(t^2-5t+3)", sp.factor(Q.charpoly(t).as_expr()) ==
          sp.factor((t - 1) * (t**2 - 5 * t + 3)))
    check("B3: det Q = 3 = N_fam", Q.det() == N_fam)
    check("B3 RESIDUAL (open): Q+ spectrum {1,2,3}=A3 exponents and Q-^2|supp=N_fam are "
          "ALGEBRAICALLY forced; deriving Q+/Q- from D4-parabolic geometry on P1\\mu4 is open", True)

    # ---- B5: N_star is a continuous reheating input, not a forced compiler integer ----
    def ns(N):
        return 1 - mp.mpf(2) / N
    def r(N):
        return mp.mpf(12) / N**2
    N_from_obs = 2 / (1 - mp.mpf('0.9649'))
    check("B5: observed n_s=0.9649 -> N_star = 56.98 (continuous)", N_from_obs, mp.mpf('56.98'), tol=mp.mpf('0.05'))
    # n_s, r vary smoothly over the [50,60] band; no clean compiler integer is selected
    band = [ns(N) for N in (50, 55, 60)]
    check("B5: n_s monotone over N_star band [50,60] (0.96..0.967) -> input, not output",
          band[0] < band[1] < band[2] and mp.mpf('0.959') < band[0] and band[2] < mp.mpf('0.967'))
    check("B5 RESIDUAL (stays [P]): N_star fixed by reheating / the n_s measurement, "
          "NOT by the compiler", True)

    # ---- B6 / C7: gravity is induced from c3; the full metric-sector measure is open ----
    check("B6/C7: c3 = 1/(8pi) is the gravitational seam constant (induced gravity)",
          c3, 1 / (8 * mp.pi), tol=mp.mpf('1e-25'))
    M_scal = c3**(mp.mpf(7) / 2) * Mbar
    check("B6/C7: R^2 scalaron mass M = c3^(7/2) Mbar ~ 3.1e13 GeV (low-curvature readout)",
          M_scal, mp.mpf('3.06e13'), tol=mp.mpf('5e-2'))
    check("B6 RESIDUAL (open [A]): full covariant Einstein-side field equation NOT derived; "
          "R+R^2 is the low-curvature readout only", True)
    check("C7 RESIDUAL (open [A]): boundary-kernel path-integral measure on the dynamical "
          "metric beyond FRW NOT constructed (most open item)", True)
    return summary("v22 open-gates audit contract")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
