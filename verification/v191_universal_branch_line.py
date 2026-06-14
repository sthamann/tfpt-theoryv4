"""v191 -- The 'universal branch line' (external-review proposal, point 3),
HONESTLY typed as a [C] structural alignment, NOT an [E] theorem. The affine map
q = 7/2 + (N_fam^2/2) m carries the Schwarzschild-de Sitter branch points
m = +-1/N_fam onto the flavor branch points {2,5} = {|Z2|, g_car}, with the
midpoint 7/2 (the branch-divisor sum 7 over 2 / the scalaron half-exponent). The
arithmetic is exact, but the existence of such a map is a tautology (any two pairs
of points are affinely equivalent), so the slope and midpoint are FORCED by the
data, not independent predictions. The genuine shared content -- the 2/3 = |Z2|/N_fam
ramification of the mass-to-transport double cover -- is already established
(tfpt_2, tfpt_horizon_readouts). This module records the alignment and is explicit
that it is NOT a new theorem.

  [E] 1. THE THREE LANDING POINTS.  Under q = 7/2 + (N_fam^2/2) m:
        m=-1/N_fam -> q=2 (Koide branch = |Z2|), m=0 -> q=7/2 (scalaron midpoint),
        m=+1/N_fam -> q=5 (carrier branch = g_car).
  [E] 2. THE ENDPOINTS ARE THE COMPILER LABELS.  q=2=|Z2|, q=5=g_car; the SdS
        branch points are +-1/N_fam (separation 2/N_fam = 2/3 = |Z2|/N_fam, the
        deck-involution distance, tfpt_horizon_readouts); the flavor branch sum
        is 2+5 = 7 (= the mass-pencil branch-divisor sum -7/N_fam read in the
        q-coordinate, tfpt_2), midpoint 7/2.
  [C] 3. HONEST TYPING: ALIGNMENT, NOT THEOREM.  The affine map exists for ANY
        two pairs of points (two intervals are always affinely equivalent), so
        its slope N_fam^2/2 and midpoint 7/2 are DETERMINED by the four numbers
        {-1/3,1/3} and {2,5} -- mnemonics, not forced independent predictions.
        The genuine shared structure is the 2/3 = |Z2|/N_fam ramification of the
        mass<->transport double cover, ALREADY established (tfpt_2 branch
        divisor; tfpt_horizon SdS branch). So this is a [C] structural alignment
        exhibiting a known parallel, never promoted to [E].
  [C] 4. NEGATIVE CONTROL (why it is not predictive).  A decoy pair, e.g.
        {3,4} instead of {2,5}, admits an equally exact affine map from the same
        SdS branch points -- so 'an affine map exists' carries no content; only
        the LABELS (2=|Z2|, 5=g_car, 7=sum) and the shared 2/3 do.

  Exact (symbolic affine algebra); the typing is [C] by construction.
"""
import sympy as sp

from tfpt_constants import g_car, N_fam, check, summary, reset

Z2 = 2


def run():
    reset()
    print("v191 universal branch line: an exact affine relabeling [C], NOT a new theorem")

    m = sp.symbols("m")
    q = sp.Rational(7, 2) + sp.Rational(N_fam**2, 2) * m       # q = 7/2 + (9/2) m
    qm = q.subs(m, sp.Rational(-1, N_fam))
    q0 = q.subs(m, 0)
    qp = q.subs(m, sp.Rational(1, N_fam))
    check("THREE LANDING POINTS [E]: q = 7/2 + (N_fam^2/2) m maps m=-1/N_fam -> "
          "%s, m=0 -> %s, m=+1/N_fam -> %s" % (qm, q0, qp),
          qm == 2 and q0 == sp.Rational(7, 2) and qp == 5)

    sep = sp.Rational(2, N_fam)
    check("ENDPOINTS ARE COMPILER LABELS [E]: q=2=|Z2|=%d, q=5=g_car=%d; SdS "
          "branch separation 2/N_fam = %s = |Z2|/N_fam (deck-involution distance); "
          "flavor branch sum 2+5 = 7 (mass-pencil branch-divisor sum -7/N_fam in "
          "the q-coordinate, tfpt_2), midpoint 7/2"
          % (Z2, g_car, sep),
          2 == Z2 and 5 == g_car and sep == sp.Rational(2, 3) and (2 + 5) == 7)

    check("ALIGNMENT, NOT THEOREM [C]: the affine map exists for ANY two pairs of "
          "points (two intervals are always affinely equivalent), so the slope "
          "N_fam^2/2 = %s and midpoint 7/2 are DETERMINED by {-1/3,1/3}->{2,5}, "
          "not forced independent predictions; the genuine shared content is the "
          "2/3 = |Z2|/N_fam ramification of the mass<->transport double cover, "
          "already established (tfpt_2, tfpt_horizon). [C], never [E]"
          % sp.Rational(N_fam**2, 2), True)

    # negative control: a decoy endpoint pair admits an equally exact affine map
    a, b = sp.symbols("a b")
    # solve q = a + b*m with q(-1/3)=3, q(1/3)=4 (decoy {3,4})
    sol = sp.solve([a + b * sp.Rational(-1, N_fam) - 3, a + b * sp.Rational(1, N_fam) - 4], [a, b])
    decoy_exists = sol[a] == sp.Rational(7, 2) and sol[b] == sp.Rational(3, 2)
    check("NEGATIVE CONTROL [C]: a decoy pair {3,4} admits an equally exact "
          "affine map (a=%s, b=%s) from the same SdS branch points, so 'an affine "
          "map exists' carries NO content -- only the labels (2=|Z2|, 5=g_car, "
          "sum 7) and the shared 2/3 do" % (sol[a], sol[b]),
          decoy_exists)

    return summary("v191 universal branch line: exact affine relabeling [C] (alignment, not a theorem)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
